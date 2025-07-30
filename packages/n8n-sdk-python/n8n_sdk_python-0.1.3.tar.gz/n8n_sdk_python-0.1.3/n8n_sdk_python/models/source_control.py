"""
n8n source control data models.
Define source control related data structures.
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Any

from pydantic import Field

from .base import N8nBaseModel


class ScmPullRequest(N8nBaseModel):
    """Source control pull request model
    
    Corresponds to the request body of POST /source-control/pull, used to pull data from remote repository
    """
    force: Optional[bool] = Field(False, description="Whether to force pull, force mode will ignore local modifications")
    variables: Optional[dict[str, Any]] = Field(None, description="Environment variables to apply during pull operation, can be used to resolve conflicts")


class ScmPullResponseVariables(N8nBaseModel):
    """Variables changes in source control pull response, records variable changes during pull operation"""
    added: Optional[list[str]] = Field(default_factory=list, description="List of variable key names added during pull operation")
    changed: Optional[list[str]] = Field(default_factory=list, description="List of variable key names modified during pull operation")


class ScmPullResponseCredential(N8nBaseModel):
    """Credential brief information in source control pull response, represents credentials affected by pull operation"""
    id: str = Field(..., description="Unique identifier of the credential")
    name: str = Field(..., description="Name of the credential")
    type: str = Field(..., description="Type of the credential, such as 'github', 'slack', etc.")


class ScmPullResponseWorkflow(N8nBaseModel):
    """Workflow brief information in source control pull response, represents workflows affected by pull operation"""
    id: str = Field(..., description="Unique identifier of the workflow")
    name: str = Field(..., description="Name of the workflow")


class ScmPullResponseTagItem(N8nBaseModel):
    """Tag item in source control pull response, represents tag information in pull operation"""
    id: str = Field(..., description="Unique identifier of the tag")
    name: str = Field(..., description="Name of the tag")


class ScmPullResponseTagMapping(N8nBaseModel):
    """Tag mapping in source control pull response, represents association between workflows and tags"""
    workflowId: str = Field(..., description="Unique identifier of the workflow")
    tagId: str = Field(..., description="Unique identifier of the tag")


class ScmPullResponseTags(N8nBaseModel):
    """Tag changes in source control pull response, records changes to tags and tag mappings"""
    tags: Optional[list[ScmPullResponseTagItem]] = Field(default_factory=list, description="List of tags in pull operation")
    mappings: Optional[list[ScmPullResponseTagMapping]] = Field(default_factory=list, description="List of tag mappings in pull operation")


class ScmPullResponse(N8nBaseModel):
    """Source control pull response model
    
    Corresponds to the response body of POST /source-control/pull, contains details of pull operation results
    """
    variables: Optional[ScmPullResponseVariables] = Field(None, description="Variable change information")
    credentials: Optional[list[ScmPullResponseCredential]] = Field(default_factory=list, description="List of credentials affected by pull operation")
    workflows: Optional[list[ScmPullResponseWorkflow]] = Field(default_factory=list, description="List of workflows affected by pull operation")
    tags: Optional[ScmPullResponseTags] = Field(None, description="Changes to tags and tag mappings")

class ScmProvider(str, Enum):
    """Source control provider enum, defines supported source code management systems"""
    GITHUB = "github"  # GitHub repository
    GITLAB = "gitlab"  # GitLab repository
    BITBUCKET = "bitbucket"  # Bitbucket repository
    GITEA = "gitea"  # Gitea self-hosted Git service
    CUSTOM = "custom"  # Custom Git service


class ScmConnectionType(str, Enum):
    """Source control connection type enum, defines methods of authentication to source code repositories"""
    OAUTH2 = "oauth2"  # OAuth2 authentication
    PERSONAL_ACCESS_TOKEN = "personalAccessToken"  # Personal access token
    BASIC_AUTH = "basicAuth"  # Basic authentication (username/password)
    SSH_KEY = "sshKey"  # SSH key authentication


class PullRequestState(str, Enum):
    """Pull request state enum, defines possible states of a PR"""
    OPEN = "open"  # Open/unresolved
    CLOSED = "closed"  # Closed/rejected
    MERGED = "merged"  # Merged


class ScmConnection(N8nBaseModel):
    """Source control connection data model, represents a connection configuration to a source code repository"""
    id: str = Field(..., description="Unique identifier of the connection")
    name: str = Field(..., description="Display name of the connection")
    provider: ScmProvider = Field(..., description="Source code provider type")
    repositoryUrl: str = Field(..., description="Repository URL")
    branchName: str = Field(..., description="Branch name to use")
    connectionType: ScmConnectionType = Field(..., description="Connection authentication type")
    connected: bool = Field(False, description="Whether the connection is active")
    settings: Optional[dict[str, Any]] = Field(None, description="Additional settings for the connection, such as authentication information")
    createdAt: Optional[datetime] = Field(None, description="Connection creation time")
    updatedAt: Optional[datetime] = Field(None, description="Connection last update time")


class ScmConnectionCreate(N8nBaseModel):
    """Create source control connection request model, used to create a new source code connection"""
    name: str = Field(..., description="Display name of the connection")
    provider: ScmProvider = Field(..., description="Source code provider type")
    repositoryUrl: str = Field(..., description="Repository URL")
    branchName: Optional[str] = Field("main", description="Branch name to use, defaults to main")
    connectionType: ScmConnectionType = Field(..., description="Connection authentication type")
    settings: Optional[dict[str, Any]] = Field(None, description="Additional settings for the connection, including authentication information")


class ScmConnectionUpdate(N8nBaseModel):
    """Update source control connection request model, used to modify properties of an existing connection"""
    name: Optional[str] = Field(None, description="New display name for the connection")
    provider: Optional[ScmProvider] = Field(None, description="Source code provider type")
    repositoryUrl: Optional[str] = Field(None, description="New repository URL")
    branchName: Optional[str] = Field(None, description="New branch name to use")
    connectionType: Optional[ScmConnectionType] = Field(None, description="Connection authentication type")
    settings: Optional[dict[str, Any]] = Field(None, description="Additional settings for the connection")


class PullRequestStatus(N8nBaseModel):
    """Pull request status data model, represents the current status of a PR"""
    pullRequestId: str = Field(..., description="Unique identifier of the pull request")
    state: PullRequestState = Field(..., description="Current state of the pull request")
    title: str = Field(..., description="Title of the pull request")
    url: str = Field(..., description="Web URL of the pull request")
    createdAt: datetime = Field(..., description="Pull request creation time")
    updatedAt: Optional[datetime] = Field(None, description="Pull request last update time")
    mergedAt: Optional[datetime] = Field(None, description="Pull request merge time, if merged")
    closedAt: Optional[datetime] = Field(None, description="Pull request close time, if closed")


class CommitInfo(N8nBaseModel):
    """Commit information data model, represents detailed information about a Git commit"""
    id: str = Field(..., description="SHA identifier of the commit")
    message: str = Field(..., description="Commit message")
    date: datetime = Field(..., description="Commit time")
    author: str = Field(..., description="Commit author")
    url: Optional[str] = Field(None, description="Web URL of the commit")


class ScmStatus(N8nBaseModel):
    """Source control status data model, represents the current status of a source code connection"""
    connected: bool = Field(..., description="Whether the source code connection is active")
    currentBranch: Optional[str] = Field(None, description="Current working branch")
    latestCommit: Optional[CommitInfo] = Field(None, description="Latest commit information")
    pendingChanges: bool = Field(False, description="Whether there are uncommitted changes")
    activePullRequest: Optional[PullRequestStatus] = Field(None, description="Active pull request, if any")


class StatusItemType(str, Enum):
    """Status item type enum, defines types of resources that can be tracked"""
    WORKFLOW = "workflow"  # Workflow
    CREDENTIAL = "credential"  # Credential
    VARIABLE = "variable"  # Variable
    TAG = "tag"  # Tag
    OWNER = "owner"  # Owner
    OTHER = "other"  # Other types


class StatusItemStatus(str, Enum):
    """Status item status enum, defines change states of resources"""
    CREATED = "created"  # Newly created
    MODIFIED = "modified"  # Modified
    DELETED = "deleted"  # Deleted
    RENAMED = "renamed"  # Renamed
    CONFLICT = "conflict"  # Conflict


class StatusItem(N8nBaseModel):
    """Status item data model, represents a resource item tracked by source control"""
    id: str = Field(..., description="Unique identifier of the item")
    name: str = Field(..., description="Name of the item")
    type: StatusItemType = Field(..., description="Type of the item")
    status: StatusItemStatus = Field(..., description="Change status of the item")
    oldName: Optional[str] = Field(None, description="Old name of the item, only used in rename operations")


class StatusList(N8nBaseModel):
    """Status list response model, contains all item statuses tracked by source control"""
    data: list[StatusItem] = Field(..., description="List of status items")
    count: int = Field(..., description="Total number of status items")


class PullRequestCreate(N8nBaseModel):
    """Create pull request request model, used to create a new PR"""
    title: str = Field(..., description="Title of the pull request")
    description: Optional[str] = Field(None, description="Detailed description of the pull request")
    targetBranch: Optional[str] = Field(None, description="Target branch, defaults to the repository's default branch")


class BranchCreate(N8nBaseModel):
    """Create branch request model, used to create a new Git branch"""
    name: str = Field(..., description="Name of the new branch")
    fromBranch: Optional[str] = Field(None, description="Branch to create from, defaults to current branch")