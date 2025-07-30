from codemie_tools.base.models import ToolMetadata

GITHUB_TOOL = ToolMetadata(
    name="github",
    description="""
        Tool implemented with python rest client and is used to work with Github Public REST API. 
        Accepts single json object which MUST contain: 'method', 'url', 'method_arguments', 'header' that later will be 
        passed to python requests library. Authorization token will be passed as header parameter.
        all parameters MUST be generated based on the Github Public REST API specification.
        Request MUST be a valid JSON object that will pass json.loads validation.
        url MUST be valid https url and start with https://api.github.com
        """,
    label="Github",
    user_description="""
        Provides access to the GitHub REST API, allowing for a wider range of operations compared to tools using official Python libraries. This tool enables the AI assistant to perform various GitHub-specific tasks and retrieve detailed information about repositories, issues, pull requests, and more.
        Before using it, it is necessary to add a new integration for the tool by providing:
        1. GitHub Server URL
        2. GitHub Personal Access Token with appropriate scopes
        Usage Note:
        Use this tool when you need to perform GitHub-specific operations that are not covered by other specialized tools.
        """.strip(),
)

GITLAB_TOOL = ToolMetadata(
    name="gitlab",
    description="""
        Tool implemented with python rest client and is used to work with Gitlab Public REST API. 
        Accepts single json object which MUST contain: 'method', 'url', 'method_arguments', 'header' that later will be 
        passed to python requests library. Authorization token will be passed as header parameter.
        all parameters MUST be generated based on the Gitlab Public REST API specification.
        Request MUST be a valid JSON object that will pass json.loads validation.
        'url' MUST always start with /api/v4/.
        """,
    label="Gitlab",
    user_description="""
        Provides access to the Gitlab REST API, allowing for a wider range of operations compared to tools using official Python libraries. This tool enables the AI assistant to perform various Gitlab-specific tasks and retrieve detailed information about repositories, issues, pull requests, and more.
        Before using it, it is necessary to add a new integration for the tool by providing:
        1. Gitlab Server URL
        2. Gitlab Personal Access Token with appropriate scopes
        Usage Note:
        Use this tool when you need to perform Gitlab-specific operations that are not covered by other specialized tools.
        """.strip(),
)
