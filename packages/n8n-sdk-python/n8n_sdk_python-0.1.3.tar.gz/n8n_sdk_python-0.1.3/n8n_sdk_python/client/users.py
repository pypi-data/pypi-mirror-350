"""
N8n User API client for managing user accounts.

This module provides a client for interacting with the n8n User API,
enabling user management operations such as listing, creating,
retrieving, and deleting users, as well as modifying user roles.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.users import (
    UsersList, UserCreateItem, UserCreateResponseItem, User, UserRole
)
from ..models.base import N8nBaseModel # For generic response like operation status


class UserClient(BaseClient):
    """
    Client for interacting with the n8n User API.
    
    Provides methods for user management, including listing users,
    creating users, retrieving user details, deleting users, and
    modifying user roles within the n8n instance.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def list_users(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        include_role: Optional[bool] = None,
        project_id: Optional[str] = None
    ) -> UsersList:
        """
        Retrieve all users from the n8n instance.
        
        This endpoint is only available to the instance owner.
        
        Args:
            limit: Maximum number of users to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            include_role: Whether to include user roles in the response
            project_id: Filter users by project ID
            
        Returns:
            A UsersList object containing user data and pagination info
            
        API Docs: https://docs.n8n.io/api/v1/users/#retrieve-all-users
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if include_role is not None:
            params["includeRole"] = include_role
        if project_id is not None:
            params["projectId"] = project_id
        
        response_data = await self.get(endpoint="/v1/users", params=params)
        return UsersList(**response_data)

    async def create_users(
        self,
        users: list[UserCreateItem | dict[str, Any]]
    ) -> list[UserCreateResponseItem]:
        """
        Create one or more users in the n8n instance.
        
        Args:
            users: List of user objects to create, either as UserCreateItem 
                  instances or dictionaries with 'email' and optional 'role' fields
                  
        Returns:
            List of created user objects with invitation details
            
        Raises:
            TypeError: If user items are not of the expected format
            
        API Docs: https://docs.n8n.io/api/v1/users/#create-multiple-users
        """
        _users: list[UserCreateItem] = []
        for user_input_item in users:
            if isinstance(user_input_item, dict):
                _users.append(UserCreateItem(**user_input_item))
            elif isinstance(user_input_item, UserCreateItem):
                _users.append(user_input_item)
            else:
                raise TypeError(
                    "Each item in 'users' list must be a UserCreateItem instance or a dict, "
                    f"got {type(user_input_item).__name__} for item {user_input_item!r}"
                )
        
        # Convert list[UserCreateItem] to list[Dict] for the JSON body
        users_payload = [user.model_dump(exclude_none=True) for user in _users]
        response_data = await self.post(endpoint="/v1/users", json=users_payload)
        # Assuming the response is a list of dictionaries, each can be parsed into UserCreateResponseItem
        return [UserCreateResponseItem(**item) for item in response_data]

    async def get_user(
        self,
        user_id_or_email: str,
        include_role: Optional[bool] = None
    ) -> User:
        """
        Retrieve a user from the n8n instance by ID or email.
        
        This endpoint is only available to the instance owner.
        
        Args:
            user_id_or_email: The ID or email address of the user to retrieve
            include_role: Whether to include the user's role in the response
            
        Returns:
            A User object containing detailed user information
            
        API Docs: https://docs.n8n.io/api/v1/users/#get-user-by-id-email
        """
        params = {}
        if include_role is not None:
            params["includeRole"] = include_role
            
        response_data = await self.get(endpoint=f"/v1/users/{user_id_or_email}", params=params)
        return User(**response_data)

    async def delete_user(
        self,
        user_id_or_email: str
    ) -> None:
        """
        Delete a user from the n8n instance.
        
        Args:
            user_id_or_email: The ID or email address of the user to delete
            
        Returns:
            None: The API returns 204 No Content on success
            
        API Docs: https://docs.n8n.io/api/v1/users/#delete-a-user
        """
        await self.delete(endpoint=f"/v1/users/{user_id_or_email}")
        # For 204 No Content, typically no specific model is returned, or a generic success message model.
        # Here, returning None as per API spec. A custom model for operation status could also be used.
        return None

    async def update_user_role(
        self,
        user_id_or_email: str,
        new_role: UserRole | str
    ) -> None:
        """
        Change a user's global role in the n8n instance.
        
        Args:
            user_id_or_email: The ID or email address of the user to update
            new_role: The new role to assign, either as a UserRole enum value
                     or a string matching one of the valid role values
                     
        Returns:
            None: The API returns 200 with no specific response body on success
            
        Raises:
            TypeError: If new_role is not a valid UserRole enum value or string
            
        API Docs: https://docs.n8n.io/api/v1/users/#change-a-user-s-global-role
        """
        _new_role: UserRole
        if isinstance(new_role, str):
            try:
                _new_role = UserRole(new_role)
            except ValueError as e:
                raise TypeError(f"Invalid string value for UserRole: '{new_role}'. Valid values are: {[r.value for r in UserRole]}. Error: {e}") from e
        elif isinstance(new_role, UserRole):
            _new_role = new_role
        else:
            raise TypeError(f"'new_role' must be a UserRole instance or a str, got {type(new_role).__name__}")

        payload = {"newRoleName": _new_role.value}
        await self.patch(endpoint=f"/v1/users/{user_id_or_email}/role", json=payload)
        # Similar to delete, API docs don't specify a clear response model for success, often it's just a status.
        # Returning None for now.
        return None 