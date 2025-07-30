"""
n8n user data models.
Define user-related data structures.
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Any

from pydantic import Field

from .base import N8nBaseModel


class UserRole(str, Enum):
    """User role enum, defines possible user roles and permission levels in the system"""
    GLOBAL_OWNER = "global:owner"  # Global owner, has the highest permissions in the system
    GLOBAL_ADMIN = "global:admin"  # Global admin, can manage system settings and users
    GLOBAL_MEMBER = "global:member"  # Global member, basic access permissions
    OWNER = "owner"  # Owner of specific resources
    ADMIN = "admin"  # Administrator of specific resources
    EDITOR = "editor"  # Can edit specific resources
    DEFAULT = "default"  # Default role


class AuthenticatedUser(N8nBaseModel):
    """Authenticated user data model, represents the currently logged-in user and their complete information"""
    id: str = Field(..., description="Unique identifier of the user")
    email: str = Field(..., description="User's email address, typically used as login name")
    firstName: Optional[str] = Field(None, description="User's first name")
    lastName: Optional[str] = Field(None, description="User's last name")
    fullName: Optional[str] = Field(None, description="User's full name (first name + last name)")
    password: Optional[str] = Field(None, description="User password (typically not returned)")
    isOwner: bool = Field(False, description="Whether the user is the system owner")
    isPending: bool = Field(False, description="Whether the user is in pending confirmation status")
    signInType: Optional[str] = Field(None, description="User's sign-in type")
    role: Optional[str] = Field(None, description="User's role as a string representation")
    createdAt: Optional[datetime] = Field(None, description="User creation time")
    updatedAt: Optional[datetime] = Field(None, description="User last update time")
    settings: Optional[dict[str, Any]] = Field(None, description="User's personal settings")
    globalRole: UserRole = Field(UserRole.GLOBAL_MEMBER, description="User's global role")
    authenticationMethod: Optional[str] = Field(None, description="User's authentication method")


class User(N8nBaseModel):
    """User data model, represents user information in API responses
    
    Corresponds to the response of GET /users and GET /users/{id}
    """
    id: str = Field(..., description="Unique identifier of the user")
    email: str = Field(..., description="User's email address")
    firstName: Optional[str] = Field(None, description="User's first name")
    lastName: Optional[str] = Field(None, description="User's last name")
    isOwner: bool = Field(False, description="Whether the user is the system owner")
    isPending: bool = Field(False, description="Whether the user is in pending status, needs activation")
    signInType: Optional[str] = Field(None, description="User's sign-in type, such as 'email'")
    createdAt: Optional[datetime] = Field(None, description="User account creation time")
    updatedAt: Optional[datetime] = Field(None, description="User information last update time")
    role: Optional[UserRole] = Field(None, description="User's role in the system")
    inviteAcceptUrl: Optional[str] = Field(None, description="User invitation acceptance URL, only returned when creating a user")
    emailSent: Optional[bool] = Field(None, description="Whether the invitation email has been sent, only returned when creating a user")


class UserShort(N8nBaseModel):
    """Simplified user data model, contains only basic information, used for lists or references"""
    id: str = Field(..., description="Unique identifier of the user")
    email: str = Field(..., description="User's email address")
    firstName: Optional[str] = Field(None, description="User's first name")
    lastName: Optional[str] = Field(None, description="User's last name")


class UserCreate(N8nBaseModel):
    """Create single user request model"""
    email: str = Field(..., description="New user's email address, will be used as login name")
    firstName: Optional[str] = Field(None, description="New user's first name")
    lastName: Optional[str] = Field(None, description="New user's last name")
    role: Optional[UserRole] = Field(UserRole.GLOBAL_MEMBER, description="New user's role")
    password: Optional[str] = Field(None, description="New user's initial password")


class UserCreateItem(N8nBaseModel):
    """Single user item in a multi-user creation request
    
    Corresponds to an array item in the request body of POST /users
    """
    email: str = Field(..., description="New user's email address")
    role: Optional[UserRole] = Field(UserRole.GLOBAL_MEMBER, description="New user's role, defaults to global member")
    firstName: Optional[str] = Field(None, description="New user's first name")
    lastName: Optional[str] = Field(None, description="New user's last name")


class UserCreateResponseItem(N8nBaseModel):
    """Single user item in the user creation response, includes result or error
    
    Corresponds to the user creation result in the response of POST /users
    """
    user: Optional[User] = Field(None, description="Successfully created user information")
    error: Optional[str] = Field(None, description="Error occurred during user creation")


class UserUpdateRequest(N8nBaseModel):
    """Update user role request model
    
    Corresponds to the request body of PATCH /users/{id}/role
    """
    newRoleName: UserRole = Field(..., description="New role name for the user")


class UsersList(N8nBaseModel):
    """Users list response model, used to get information for multiple users
    
    Corresponds to the response of GET /users
    """
    data: list[User] = Field(..., description="List of users")
    nextCursor: Optional[str] = Field(None, description="Pagination cursor, used to get the next page of data")
    count: Optional[int] = Field(None, description="Total number of users")
