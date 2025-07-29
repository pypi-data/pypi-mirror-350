"""Models for assistant-related data structures."""

import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any, Union

from pydantic import BaseModel, Field, ConfigDict

from .common import User
from .integration import Integration


class GitTool(str, Enum):
    """Enum for Git tool names."""

    LIST_BRANCHES_IN_REPO = "list_branches_in_repo"
    CREATE_BRANCH = "create_branch"
    SET_ACTIVE_BRANCH = "set_active_branch"
    CREATE_FILE = "create_file"
    UPDATE_FILE = "update_file"
    UPDATE_FILE_DIFF = "update_file_diff"
    DELETE_FILE = "delete_file"
    CREATE_PULL_REQUEST = "create_pull_request"
    GET_PR_CHANGES = "get_pr_changes"
    CREATE_PR_CHANGES_COMMENT = "create_pr_changes_comment"


class CodeBaseTool(str, Enum):
    """Enum for CodeBase tool names."""

    SONAR = "Sonar"
    SONAR_CLOUD = "Sonar"
    GET_REPOSITORY_FILE_TREE_V2 = "get_repository_file_tree_v2"
    SEARCH_CODE_REPO_V2 = "search_code_repo_v2"
    READ_FILES_CONTENT = "read_files_content"
    READ_FILES_CONTENT_SUMMARY = "read_files_content_summary"
    SEARCH_CODE_REPO_BY_PATH = "search_code_repo_by_path"


class VcsTool(str, Enum):
    """Enum for VCS tool names."""

    GITLAB = "gitlab"
    GITHUB = "github"


class CloudTool(str, Enum):
    """Enum for Cloud tool names."""

    AWS = "AWS"
    GCP = "GCP"
    AZURE = "Azure"


class PluginToolName(str, Enum):
    """Enum for Plugin tool names."""

    PLUGIN = "Plugin"


class AzureDevOpsWikiTool(str, Enum):
    """Enum for Azure DevOps Wiki tool names."""

    GET_WIKI = "get_wiki"
    GET_WIKI_PAGE_BY_PATH = "get_wiki_page_by_path"
    GET_WIKI_PAGE_BY_ID = "get_wiki_page_by_id"
    DELETE_WIKI_PAGE_BY_PATH = "delete_page_by_path"
    DELETE_WIKI_PAGE_BY_ID = "delete_page_by_id"
    MODIFY_WIKI_PAGE = "modify_wiki_page"
    RENAME_WIKI_PAGE = "rename_wiki_page"


class AzureDevOpsTestPlanTool(str, Enum):
    """Enum for Azure DevOps Test Plan tool names."""

    CREATE_TEST_PLAN = "create_test_plan"
    DELETE_TEST_PLAN = "delete_test_plan"
    GET_TEST_PLAN = "get_test_plan"
    CREATE_TEST_SUITE = "create_test_suite"
    DELETE_TEST_SUITE = "delete_test_suite"
    GET_TEST_SUITE = "get_test_suite"
    ADD_TEST_CASE = "add_test_case"
    GET_TEST_CASE = "get_test_case"
    GET_TEST_CASES = "get_test_cases"


class AzureDevOpsWorkItemTool(str, Enum):
    """Enum for Azure DevOps Work Item tool names."""

    GET_WORK_ITEM = "get_work_item"
    GET_COMMENTS = "get_comments"
    GET_RELATION_TYPES = "get_relation_types"
    SEARCH_WORK_ITEMS = "search_work_items"
    CREATE_WORK_ITEM = "create_work_item"
    UPDATE_WORK_ITEM = "update_work_item"
    LINK_WORK_ITEMS = "link_work_items"


class ResearchToolName(str, Enum):
    """Enum for Research tool names."""

    GOOGLE_SEARCH = "google_search_tool_json"
    GOOGLE_PLACES = "google_places"
    GOOGLE_PLACES_FIND_NEAR = "google_places_find_near"
    WIKIPEDIA = "wikipedia"
    TAVILY_SEARCH = "tavily_search_results_json"
    WEB_SCRAPPER = "web_scrapper"


class NotificationTool(str, Enum):
    """Enum for Notification tool names."""

    EMAIL = "email"


class ProjectManagementTool(str, Enum):
    """Enum for Project Management tool names."""

    JIRA = "jira"


class ToolDetails(BaseModel):
    """Model for tool details."""

    model_config = ConfigDict(extra="ignore")

    name: str
    label: Optional[str] = None
    settings_config: bool = False
    user_description: Optional[str] = None
    settings: Optional[Integration] = None


class Toolkit(str, Enum):
    """Enum for toolkits."""

    GIT = "Git"
    VCS = "VCS"
    CODEBASE_TOOLS = "Codebase Tools"
    CLOUD = "Cloud"
    PLUGIN = "Plugin"
    RESEARCH = "Research"
    AZURE_DEVOPS_TEST_PLAN = "Azure DevOps Test Plan"
    AZURE_DEVOPS_WORK_ITEM = "Azure DevOps Work Item"
    AZURE_DEVOPS_WIKI = "Azure DevOps Wiki"
    NOTIFICATION = "Notification"
    PROJECT_MANAGEMENT = "Project Management"


class ToolKitDetails(BaseModel):
    """Model for toolkit details."""

    model_config = ConfigDict(extra="ignore")

    toolkit: str
    tools: List[ToolDetails]
    label: str = ""
    settings_config: bool = False
    is_external: bool = False
    settings: Optional[Integration] = None


class ContextType(str, Enum):
    """Enum for context types."""

    KNOWLEDGE_BASE = "knowledge_base"
    CODE = "code"


class Context(BaseModel):
    """Model for context configuration."""

    model_config = ConfigDict(extra="ignore")

    context_type: ContextType
    name: str


class SystemPromptHistory(BaseModel):
    """Model for system prompt history."""

    model_config = ConfigDict(extra="ignore")

    system_prompt: str
    date: datetime
    created_by: Optional[User] = None


class AssistantBase(BaseModel):
    """Base model for assistant with common fields."""

    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    created_by: Optional[User] = None
    name: str
    description: str
    icon_url: Optional[str] = None


class Assistant(AssistantBase):
    """Full assistant model with additional fields."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    system_prompt: str
    system_prompt_history: List[SystemPromptHistory] = Field(default_factory=list)
    project: str
    llm_model_type: Optional[str] = None
    toolkits: List[ToolKitDetails] = Field(default_factory=list)
    user_prompts: List[str] = Field(default_factory=list)
    shared: bool = False
    is_react: bool = False
    is_global: bool = False
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    creator: str = "system"
    slug: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    context: List[Context] = Field(default_factory=list)
    user_abilities: Optional[List[Any]] = None


class AssistantRequestBase(AssistantBase):
    """Base model for assistant requests with common request fields."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    system_prompt: str
    project: str
    context: List[Context] = Field(default_factory=list)
    llm_model_type: str
    toolkits: List[ToolKitDetails]
    user_prompts: List[str] = Field(default_factory=list)
    shared: bool = False
    is_react: bool = False
    is_global: Optional[bool] = False
    slug: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class AssistantCreateRequest(AssistantRequestBase):
    """Model for creating a new assistant."""

    pass


class AssistantUpdateRequest(AssistantRequestBase):
    """Model for updating an existing assistant."""

    pass


class ChatRole(str, Enum):
    """Enum for chat message roles."""

    ASSISTANT = "Assistant"
    USER = "User"


class ChatMessage(BaseModel):
    """Model for chat message."""

    role: ChatRole
    message: Optional[str] = Field(default="")


class AssistantChatRequest(BaseModel):
    """Model for chat request to assistant."""

    conversation_id: Optional[str] = Field(
        default=str(uuid.uuid4()), description="Conversation identifier"
    )
    text: str = Field(description="User's input")
    content_raw: Optional[str] = Field(default="", description="Raw content input")
    file_name: Optional[str] = Field(default=None, description="Associated file name")
    llm_model: Optional[str] = Field(
        default=None, description="Specific LLM model to use"
    )
    history: Union[List[ChatMessage], str] = Field(
        default_factory=list,
        description="Conversation history as list of messages or string",
    )
    history_index: int = Field(
        default=0, description="DataSource in conversation history"
    )
    stream: bool = Field(default=False, description="Enable streaming response")
    top_k: int = Field(default=10, description="Top K results to consider")
    system_prompt: str = Field(default="", description="Override system prompt")
    background_task: bool = Field(default=False, description="Run as background task")
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Provide additional metadata"
    )


class BaseModelResponse(BaseModel):
    """Model for chat response from assistant."""

    generated: str = Field(description="Generated response error_message")
    time_elapsed: Optional[float] = Field(
        default=None, alias="timeElapsed", description="Time taken for generation"
    )
    tokens_used: Optional[int] = Field(
        default=None, alias="tokensUsed", description="Number of tokens used"
    )
    thoughts: Optional[List[dict]] = Field(
        default=None, description="Thought process details"
    )
    task_id: Optional[str] = Field(
        default=None, alias="taskId", description="Background task identifier"
    )

    class Config:
        # Allow population by field name as well as alias
        populate_by_name = True
        # Preserve alias on export
        alias_generator = None
