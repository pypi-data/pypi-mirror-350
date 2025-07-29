from codemie_tools.base.models import ToolMetadata

GENERIC_JIRA_TOOL = ToolMetadata(
    name="generic_jira_tool",
    description="""
    JIRA Tool for Official Atlassian JIRA REST API V2 to call, searching, creating, updating issues, etc. 
    You must provide the following args: relative_url, method, params. 
    1. 'method': The HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE' etc.
    2. 'relative_url': Required relative URI of the JIRA API to call. URI must start with a forward slash and '/rest/api/2/...'.
    Do not include query parameters in the URL, they must be provided separately in 'params'.
    3. 'params': Optional of parameters to be sent in request body or query params.
    For search/read operations, you MUST get minimum required fields only, until users ask explicitly for more fields.
    If some required information is not provided by user, try find by querying API, if not found ask user.
    For updating status for issues you MUST get available statuses for issue first, compare with user input and after 
    that proceed if you can.
    For the attached files you MUST get the file paths from user and attach them to the issue.
    For the description with the attached files you MUST get the file paths from user and attach them to the issue, put into description the file name in the format !filename|thumbnail!
    """,
    label="Generic Jira",
    user_description="""
    Provides access to the Jira API, enabling interaction with Jira project management and issue tracking features. This tool allows the AI assistant to perform various operations related to issues, projects, and workflows in both Jira Server and Jira Cloud environments.
    Before using it, it is necessary to add a new integration for the tool by providing:
    1. Alias (A friendly name for the Jira integration)
    2. Jira URL
    3. Username/email for Jira (Required for Jira Cloud)
    4. Token (API token or Personal Access Token)
    Usage Note:
    Use this tool when you need to manage Jira issues, projects, sprints, or retrieve information from your Jira environment.
    """.strip()
)
