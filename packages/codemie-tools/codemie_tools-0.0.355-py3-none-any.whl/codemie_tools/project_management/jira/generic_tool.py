import json
import logging
import re
import traceback
from json import JSONDecodeError
from typing import Type, Dict, Any, Optional
import os
import io
import urllib.parse
import mimetypes

from atlassian import Jira
from pydantic import BaseModel, Field
from langchain_core.tools import ToolException

from codemie_tools.base.codemie_tool import CodeMieTool
from codemie_tools.project_management.jira.tools_vars import GENERIC_JIRA_TOOL
from codemie_tools.project_management.jira.utils import validate_jira_creds
from codemie_tools.base.utils import clean_json_string

logger = logging.getLogger(__name__)


class JiraInput(BaseModel):
    method: str = Field(
        ...,
        description="The HTTP method to use for the request (GET, POST, PUT, DELETE, etc.). Required parameter."
    )
    relative_url: str = Field(
        ...,
        description="""
        Required parameter: The relative URI for JIRA REST API V2.
        URI must start with a forward slash and '/rest/api/2/...'.
        Do not include query parameters in the URL, they must be provided separately in 'params'.
        For search/read operations, you MUST always get "key", "summary", "status", "assignee", "issuetype" and 
        set maxResult, until users ask explicitly for more fields.
        """
    )
    params: Optional[str] = Field(
        default="",
        description="""
        Optional JSON of parameters to be sent in request body or query params. MUST be string with valid JSON. 
        For search/read operations, you MUST always get "key", "summary", "status", "assignee", "issuetype" and 
        set maxResult, until users ask explicitly for more fields.
        """
    )
    file_paths: Optional[list] = Field(
        default=None,
        description="Optional list of file paths to attach to the Jira issue."
    )


def parse_payload_params(params: Optional[str]) -> Dict[str, Any]:
    if params:
        try:
            return json.loads(clean_json_string(params))
        except JSONDecodeError:
            stacktrace = traceback.format_exc()
            logger.error(f"Jira tool: Error parsing payload params: {stacktrace}")
            raise ToolException(f"JIRA tool exception. Passed 'params' string is not valid to transform to vaild JSON. {stacktrace}. Please correct and send again.")
    return {}


def get_issue_field(issue, field, default=None):
    field_value = issue.get("fields", {}).get(field, default)
    # Additional verification. In some cases key is present, but value is None. Need to return default value
    return field_value if field_value else default


def get_additional_fields(issue, additional_fields):
    additional_data = {}
    for field in additional_fields:
        if field not in additional_data:  # Avoid overwriting any main fields
            additional_data[field] = get_issue_field(issue, field)
    return additional_data


def process_issue(jira_base_url, issue, payload_params: Dict[str, Any] = None):
    issue_key = issue.get('key')
    jira_link = f"{jira_base_url}/browse/{issue_key}"

    parsed_issue = {
        "key": issue_key,
        "url": jira_link,
        "summary": get_issue_field(issue, "summary", ""),
        "assignee": get_issue_field(issue, "assignee", {}).get("displayName", "None"),
        "status": get_issue_field(issue, "status", {}).get("name", ""),
        "issuetype": get_issue_field(issue, "issuetype", {}).get("name", "")
    }

    process_payload(issue, payload_params, parsed_issue)
    return parsed_issue


def process_payload(issue, payload_params, parsed_issue):
    fields_list = extract_fields_list(payload_params)

    if fields_list:
        update_parsed_issue_with_additional_data(issue, fields_list, parsed_issue)


def extract_fields_list(payload_params):
    if payload_params and 'fields' in payload_params:
        fields = payload_params['fields']
        if isinstance(fields, str) and fields.strip():
            return [field.strip() for field in fields.split(",")]
        elif isinstance(fields, list) and fields:
            return fields
    return []


def update_parsed_issue_with_additional_data(issue, fields_list, parsed_issue):
    additional_data = get_additional_fields(issue, fields_list)
    for field, value in additional_data.items():
        if field not in parsed_issue and value:
            parsed_issue[field] = value


def process_search_response(jira_url, response, payload_params: Dict[str, Any] = None):
    if response.status_code != 200:
        return response.text

    processed_issues = []
    json_response = response.json()

    for issue in json_response.get('issues', []):
        processed_issues.append(process_issue(jira_url, issue, payload_params))

    return str(processed_issues)


class GenericJiraIssueTool(CodeMieTool):
    jira: Jira
    name: str = GENERIC_JIRA_TOOL.name
    description: str = GENERIC_JIRA_TOOL.description or ""
    args_schema: Type[BaseModel] = JiraInput
    # Regular expression to match /rest/api/[any number]/search
    issue_search_pattern: str = r'/rest/api/\d+/search'

    def execute(self, method: str, relative_url: str, params: Optional[str] = "", file_paths: list | None = None, *args):
        validate_jira_creds(self.jira)

        payload_params = parse_payload_params(params)

        if method == "GET":
            response = self.jira.request(
                method=method,
                path=relative_url,
                params=payload_params,
                advanced_mode=True
            )
            self.jira.raise_for_status(response)
            if re.match(self.issue_search_pattern, relative_url):  # Check if the URL matches the search endpoint
                response_text = process_search_response(self.jira.url, response, payload_params)
            else:  # For all other GET requests, including different search endpoints
                response_text = response.text
        else:
            response = self.jira.request(
                method=method,
                path=relative_url,
                data=payload_params,
                advanced_mode=True
            )
            self.jira.raise_for_status(response)
            response_text = response.text
          
            try:
                data = json.loads(clean_json_string(response_text))
            except JSONDecodeError:
                data = None

            # Handle file attachments if provided
            if file_paths and data:
                issue_key = data.get("key")  # Ensure issue_key is passed in params
                if not issue_key:
                    raise ToolException("Issue key must be provided in params for file attachment.")
                self.attach_files(issue_key, file_paths)

        response_string = f"HTTP: {method} {relative_url} -> {response.status_code} {response.reason} {response_text}"
        logger.debug(response_string)
        return response_string

    def prepare_file_attachment(self, file_item) -> tuple:
        """
        Prepares a file for attachment to a Jira issue.
        
        This function accepts a file item—either as a string representing a local file path or remote URL,
        or as a dictionary with a 'url' key and an optional 'name'. If the file exists locally (determined by os.path.isfile),
        the file is opened and returned in binary mode. Otherwise, the function attempts to retrieve the file remotely using a GET request.
        
        Parameters:
            file_item (str or dict): The file item to attach. When a dictionary, it should contain at least a 'url' key,
                                     and optionally a 'name' key to override the automatically determined filename.
        
        Returns:
            tuple: A tuple containing:
                - filename (str): The name of the file to attach.
                - file_source (BinaryIO): The open file object or an io.BytesIO stream containing the file content.
                - mime (str): The MIME type of the file, always returned as 'application/octet-stream'.
        
        Raises:
            ToolException: If the file_item is neither a string nor a dict, or the dict is missing a 'url' key.
        """
        if isinstance(file_item, dict):
            file_url = file_item.get("url")
            if not file_url:
                raise ToolException("Dict file item missing 'url'.")
            filename = file_item.get("name") or os.path.basename(urllib.parse.urlparse(file_url).path)
        elif isinstance(file_item, str):
            file_url = file_item
            filename = os.path.basename(file_url)
        else:
            raise ToolException("Invalid file item type; expected string or dict.")

        
        if file_url.startswith(self.jira.url):
            relative_file_path = file_url[len(self.jira.url):]
            if not relative_file_path.startswith("/"):
                relative_file_path = "/" + relative_file_path
        else:
            relative_file_path = file_url

        response = self.jira.request(
            method = "GET",
            path = relative_file_path,
            headers = self.jira.no_check_headers
        )
        self.jira.raise_for_status(response)
        file_source = io.BytesIO(response.content)
        if not filename:
            filename = os.path.basename(urllib.parse.urlparse(file_url).path)

        
        mime = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        return filename, file_source, mime

    def attach_files(self, issue_key: str, file_paths: list[dict | str]) -> None:
        """
        Attaches a list of files to a Jira issue.
        
        Iterates over the list of file items, prepares each file by calling `prepare_file_attachment`,
        and builds the multipart form-data required by the Jira API for file uploads. The prepared files are then
        sent via a POST request to the Jira attachments endpoint.
        
        Parameters:
            issue_key (str): The key of the Jira issue to attach files to.
            file_paths (list): A list containing file items (either file paths as strings or dictionaries with 'url'
                               and optional 'name' keys).
        
        Returns:
            None
        
        Behavior:
            - For each file item, if `prepare_file_attachment` succeeds, the file is added as a tuple with the key 'file'.
            - If any file preparation fails, the error is logged and that file is skipped.
            - A POST request is sent to the endpoint: "/rest/api/2/issue/{issue_key}/attachments" with the files.
            - Logs an info message if files are successfully attached, otherwise logs an error message.
        """
        file_tuples = []  # List of tuples structured as: ("file", (filename, file_source, mime))
        for file_item in file_paths:
            try:
                filename, file_source, mime = self.prepare_file_attachment(file_item)
                file_tuples.append(("file", (filename, file_source, mime)))
            except Exception as e:
                logger.error(f"Failed to prepare file {file_item}. Exception: {e}. Stack trace: {traceback.format_exc()}")
        
        if file_tuples:
            post_path = f"/rest/api/2/issue/{issue_key}/attachments"
            headers = self.jira.no_check_headers
            post_response = self.jira.request(
                method="POST",
                path=post_path,
                headers=headers,
                files=file_tuples  # use list of tuples instead of dict 
            )
            if post_response.status_code in (200, 201):
                logger.info(f"Successfully attached files to {issue_key}")
            else:
                logger.error(f"Failed to attach files: {post_response.status_code} - {post_response.text}")



