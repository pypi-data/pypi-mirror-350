import json
import logging
import base64
import functools
import math
from typing import Any, Dict, Type, Optional

import requests
from pydantic import BaseModel, Field
from langchain_core.tools import ToolException

from codemie_tools.base.codemie_tool import CodeMieTool
from codemie_tools.vcs.tools_vars import GITHUB_TOOL, GITLAB_TOOL

logger = logging.getLogger(__name__)

class JsonInput(BaseModel):
    query: str = Field(description="""
        Accepts valid json ONLY! No comments allowed! PRIVATE-TOKEN will be provided separately"""
    )


logger = logging.getLogger(__name__)

def file_response_handler(execute_method):
    """
    Decorator to handle responses and only decode Base64-encoded file content.
    Why Calculate Size as `original_size * 1/4`:
    -------------------------------------------
    After decoding Base64, the original content is processed for tokenization. Base64 inflates
    file size by 4/3 (33% larger), so decoding reduces it back to 3/4 of the encoded size.
    To estimate the tokenization size, further adjustments on calculation is required 1/3 and depends on the
    encoding logic (e.g., tiktoken). This calculation ensures efficient handling of large files
    while respecting tokenization limits.

    """
    @functools.wraps(execute_method)
    def wrapper(*args, **kwargs):
        tool_instance = args[0]
        # Execute the original execute method
        response = execute_method(*args, **kwargs)

        if not isinstance(response, dict) or response.get("type") != "file":
            return response  # Return the original response if not a file

        original_size = response.get("size", 0)
        encoding = response.get("encoding", None)

        if encoding != "base64":
            logger.info("File encoding is not Base64. No decoding performed.")
            return response

        # Estimate Base64-encoded size and check against the limit
        estimated_encoded_size = math.floor(original_size * 1/ 4)
        if estimated_encoded_size > tool_instance.tokens_size_limit:
            logger.warning(
                "File too large for Base64 decoding. "
                f"Estimated Base64 size: {estimated_encoded_size} bytes, limit: {tool_instance.tokens_size_limit}."
            )
            response["error"] = (
                f"File too large for Base64 decoding (estimated size: {estimated_encoded_size} bytes,"
                f" limit: {tool_instance.tokens_size_limit})."
            )

            return response

        # Attempt to decode the Base64 content
        try:
            if response.get("content"):
                decoded_content = base64.b64decode(response["content"]).decode("utf-8")
                response["content"] = decoded_content  # Replace encoded content with decoded content
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode Base64 content: {e}")
            response["error"] = "Failed to decode Base64 content: Invalid UTF-8 encoding"
        except Exception as e:
            logger.error(f"Failed to decode Base64 content: {e}")
            response["error"] = "Failed to decode Base64 content: Incorrect padding"

        return response

    return wrapper


class GithubTool(CodeMieTool):
    name: str = GITHUB_TOOL.name
    description: str = GITHUB_TOOL.description
    args_schema: Type[BaseModel] = JsonInput
    access_token: Optional[str] = None

    @file_response_handler
    def execute(self, query: str, *args):
        if not self.access_token:
            logger.error("No Git credentials found for this repository")
            raise ToolException("No Git credentials found for repository. Provide Git credentials in 'User Settings'")
        request_json = json.loads(query)
        return requests.request(
            method=request_json.get('method'),
            url=request_json.get('url'),
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.access_token}"
            },
            data=json.dumps(request_json.get('method_arguments'))
        ).json()


class GitlabInput(JsonInput):
    query: str = """
        Accepts valid json ONLY! No comments allowed! PRIVATE-TOKEN will be provided separately
        json object which MUST contain: 'method', 'url', 'method_arguments', 'header' that later will be 
        passed to python requests library. 'url' MUST always start with /api/v4/.
        all parameters MUST be generated based on the Gitlab Public REST API specification.
        Request MUST be a valid JSON object that will pass json.loads validation.
    """


class GitlabTool(CodeMieTool):
    name: str = GITLAB_TOOL.name
    args_schema: Type[BaseModel] = GitlabInput
    base_url: Optional[str] = None
    access_token: Optional[str] = None
    description: str = GITLAB_TOOL.description

    def execute(self, query: str, *args) -> str:
        if not self.access_token:
            logger.error("No Git credentials found for this repository")
            raise ToolException("No Git credentials found for repository. Provide Git credentials in 'User Settings'")

        try:
            request_json = json.loads(query)
            method = request_json.get('method')
            url = f"{self.base_url}/{request_json.get('url')}"
            method_arguments = request_json.get("method_arguments", {})


            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }

            # Determine whether to use `params` or `json`
            if method == "GET":
                response = requests.request(method=method, url=url, headers=headers, params=method_arguments)
            else:
                response = requests.request(method=method, url=url, headers=headers, data=method_arguments)

            response_string = f"HTTP: {method} {url} -> {response.status_code} {response.reason} {response.text}"
            logger.debug(response_string)
            return response_string

        except (TypeError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse GitLab response: {e}")
            raise ToolException(f"Failed to parse GitLab response: {e}")