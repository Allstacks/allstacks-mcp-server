"""Users, Teams, and Team Members Management"""

import json
from typing import Optional

from .._json_input import JsonObjectInput, JsonValueInput, parse_json_input


def register_tools(mcp, api_client):
    """Register all user and team management tools with the MCP server"""

    # ============================================================================
    # Organization Users & Members
    # ============================================================================

    @mcp.tool()
    async def list_org_users(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        List all users in the organization with their roles and permissions.

        From OpenAPI: GET /api/v1/organization/{org_id}/users/

        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Organization users with roles and metadata
        """
        endpoint = f"organization/{org_id}/users/"

        params: dict[str, object] = {"limit": limit, "offset": offset}

        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_org_user(org_id: int, user_id: int) -> str:
        """
        Get specific user details from the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/users/{id}/

        Args:
            org_id: Organization identifier
            user_id: User identifier

        Returns:
            JSON with detailed user information
        """
        endpoint = f"organization/{org_id}/users/{user_id}/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_org_user(
        org_id: int, user_id: int, user_data: JsonObjectInput
    ) -> str:
        """
        Update user information in the organization.

        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/users/{id}/

        Args:
            org_id: Organization identifier
            user_id: User identifier
            user_data: JSON string or object with user updates

        Returns:
            Updated user information
        """
        endpoint = f"organization/{org_id}/users/{user_id}/"

        try:
            data = parse_json_input(user_data, name="user_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_manageable_roles(org_id: int) -> str:
        """
        Get roles that the current user can manage in the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/manageable_roles

        Returns an object containing:
        - all_roles: Object mapping role IDs to role information (name, rank, description)
        - assignable_roles: Array of role IDs the user can assign

        Args:
            org_id: Organization identifier

        Returns:
            JSON with manageable roles structure
        """
        endpoint = f"organization/{org_id}/manageable_roles"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_org_user_invites(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        List pending user invites for the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/user_invites/

        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Pending invites
        """
        endpoint = f"organization/{org_id}/user_invites/"

        params: dict[str, object] = {"limit": limit, "offset": offset}

        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def create_user_invite(
        org_id: int,
        email: str,
        role_id: Optional[int] = None,
        projects: Optional[JsonValueInput] = None,
    ) -> str:
        """
        Create a new user invitation.

        From OpenAPI: POST /api/v1/organization/{org_id}/user_invites/

        Args:
            org_id: Organization identifier
            email: Email address of the person to invite (REQUIRED)
            role_id: Optional role ID to assign
            projects: Optional JSON string or object of project assignments

        Returns:
            Created invite details
        """
        endpoint = f"organization/{org_id}/user_invites/"

        data: dict[str, object] = {"email": email}

        if role_id:
            data["role_id"] = role_id
        if projects is not None:
            try:
                data["projects"] = parse_json_input(projects, name="projects")
            except ValueError as e:
                return json.dumps({"error": str(e)})

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_user_invite(org_id: int, invite_id: int) -> str:
        """
        Get specific user invite details.

        From OpenAPI: GET /api/v1/organization/{org_id}/user_invites/{id}/

        Args:
            org_id: Organization identifier
            invite_id: Invite identifier

        Returns:
            JSON with invite details
        """
        endpoint = f"organization/{org_id}/user_invites/{invite_id}/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_user_invite(
        org_id: int, invite_id: int, invite_data: JsonObjectInput
    ) -> str:
        """
        Update a pending user invitation.

        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/user_invites/{id}/

        Args:
            org_id: Organization identifier
            invite_id: Invite identifier
            invite_data: JSON string or object with invite updates

        Returns:
            Updated invite details
        """
        endpoint = f"organization/{org_id}/user_invites/{invite_id}/"

        try:
            data = parse_json_input(invite_data, name="invite_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_user_invite(org_id: int, invite_id: int) -> str:
        """
        Delete/cancel a pending user invitation.

        From OpenAPI: DELETE /api/v1/organization/{org_id}/user_invites/{id}/

        Args:
            org_id: Organization identifier
            invite_id: Invite identifier

        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/user_invites/{invite_id}/"

        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def resend_user_invite(org_id: int, invite_id: int) -> str:
        """
        Resend a pending user invitation email.

        From OpenAPI: POST /api/v1/organization/{org_id}/user_invites/{id}/resend/

        Args:
            org_id: Organization identifier
            invite_id: Invite identifier

        Returns:
            Confirmation of resend
        """
        endpoint = f"organization/{org_id}/user_invites/{invite_id}/resend/"

        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Project Users & Service Users
    # ============================================================================

    @mcp.tool()
    async def list_project_users(
        project_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        List users associated with a specific project.

        From OpenAPI: GET /api/v1/project/{project_id}/users/

        Returns an array of users in the format:
        [
            {
                "id": <service user id>,
                "service_user_full_name": "John Person",
                "service_id": <service ID>,
                "enabled": True,
                "ext_user_id": ...,
                "created_at": ...,
                "service_name": "Bitbucket",
                "display_name": "John Person"
            },
            ...
        ]

        Args:
            project_id: Project identifier
            ordering: Optional ordering field for sorting results
            limit: Number of results to return per page (default: 100)
            offset: The initial index from which to return the results (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Project users with service details
        """
        endpoint = f"project/{project_id}/users/"

        params: dict[str, object] = {"limit": limit, "offset": offset}

        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def list_service_users_v2(
        project_id: int,
        service_user_ids: Optional[str] = None,
        only_enabled: bool = False,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        List service users with v2 endpoint providing enhanced data.

        From OpenAPI: GET /api/v1/project/{project_id}/service_users_v2/

        Args:
            project_id: Project identifier
            service_user_ids: Optional comma-separated list of service user IDs to filter
            only_enabled: Return only enabled users (default: False)
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Service users with enhanced metadata
        """
        endpoint = f"project/{project_id}/service_users_v2/"

        params: dict[str, object] = {
            "limit": limit,
            "offset": offset,
            "only_enabled": only_enabled,
        }

        if service_user_ids:
            params["service_user_ids[]"] = service_user_ids.split(",")
        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    # ============================================================================
    # Team Tags
    # ============================================================================

    @mcp.tool()
    async def list_team_tags(project_id: int, response_format: str = "json") -> str:
        """
        Fetch all team tags for a project.

        From OpenAPI: GET /api/v1/project/{project_id}/tag

        Args:
            project_id: Project identifier
            response_format: Output encoding: json (default) or toon

        Returns:
            Team tags
        """
        endpoint = f"project/{project_id}/tag"

        return await api_client.request_text(
            "GET", endpoint, response_format=response_format
        )

    @mcp.tool()
    async def get_team_tag(project_id: int, tag_id: int) -> str:
        """
        Fetch a specific team tag.

        From OpenAPI: GET /api/v1/project/{project_id}/tag/{tag_id}

        Args:
            project_id: Project identifier
            tag_id: Service User Tag ID

        Returns:
            JSON with team tag details
        """
        endpoint = f"project/{project_id}/tag/{tag_id}"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def add_team_tag(
        project_id: int, tag_id: int, tag_data: Optional[JsonObjectInput] = None
    ) -> str:
        """
        Add/update a tag to a team.

        From OpenAPI: POST /api/v1/project/{project_id}/tag/{tag_id}

        Args:
            project_id: Project identifier
            tag_id: Service User Tag ID
            tag_data: Optional JSON string or object with tag configuration

        Returns:
            Created/updated tag details
        """
        endpoint = f"project/{project_id}/tag/{tag_id}"

        data: dict[str, object] = {}
        if tag_data is not None:
            try:
                parsed_tag_data = parse_json_input(tag_data, name="tag_data")
            except ValueError as e:
                return json.dumps({"error": str(e)})
            if not isinstance(parsed_tag_data, dict):
                return json.dumps({"error": "tag_data must be a JSON object"})
            data = parsed_tag_data

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def remove_team_tag(project_id: int, tag_id: int) -> str:
        """
        Remove a tag from a team.

        From OpenAPI: DELETE /api/v1/project/{project_id}/tag/{tag_id}

        Args:
            project_id: Project identifier
            tag_id: Service User Tag ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"project/{project_id}/tag/{tag_id}"

        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Personal Access Tokens
    # ============================================================================

    @mcp.tool()
    async def list_personal_access_tokens(
        org_id: int, response_format: str = "json"
    ) -> str:
        """
        List all personal access tokens for the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/personal_access_tokens/

        Args:
            org_id: Organization identifier
            response_format: Output encoding: json (default) or toon

        Returns:
            Personal access tokens
        """
        endpoint = f"organization/{org_id}/personal_access_tokens/"

        return await api_client.request_text(
            "GET", endpoint, response_format=response_format
        )

    @mcp.tool()
    async def create_personal_access_token(
        org_id: int, name: str, expires_at: Optional[str] = None
    ) -> str:
        """
        Create a new personal access token.

        From OpenAPI: POST /api/v1/organization/{org_id}/personal_access_tokens/

        Args:
            org_id: Organization identifier
            name: Name for the token (REQUIRED)
            expires_at: Optional expiration date (ISO format)

        Returns:
            Created token details including the token value (only shown once)
        """
        endpoint = f"organization/{org_id}/personal_access_tokens/"

        data: dict[str, object] = {"name": name}
        if expires_at:
            data["expires_at"] = expires_at

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_personal_access_token(org_id: int, token_id: int) -> str:
        """
        Get details of a specific personal access token.

        From OpenAPI: GET /api/v1/organization/{org_id}/personal_access_tokens/{id}/

        Note: Token value is not returned for security.

        Args:
            org_id: Organization identifier
            token_id: Token identifier

        Returns:
            JSON with token details (excluding token value)
        """
        endpoint = f"organization/{org_id}/personal_access_tokens/{token_id}/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_personal_access_token(org_id: int, token_id: int) -> str:
        """
        Delete/revoke a personal access token.

        From OpenAPI: DELETE /api/v1/organization/{org_id}/personal_access_tokens/{id}/

        Args:
            org_id: Organization identifier
            token_id: Token identifier

        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/personal_access_tokens/{token_id}/"

        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
