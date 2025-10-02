"""User & Team Management Endpoints (4 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all user and team-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_service_users(
        org_id: int,
        project_id: Optional[int] = None,
        include_disabled: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List service users with merge handling.
        
        Args:
            org_id: Organization identifier
            project_id: Optional project filter
            include_disabled: Include disabled users
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            JSON array of users with merge status
        """
        endpoint = f"organization/{org_id}/service_users/"
        
        params = {
            "limit": limit,
            "offset": offset,
            "include_disabled": include_disabled
        }
        
        if project_id:
            params["project_id"] = project_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_user_mapping(
        org_id: int,
        user_keys: str,
        service_ids: str
    ) -> str:
        """
        Map user keys to human-readable names.
        
        Args:
            org_id: Organization identifier
            user_keys: JSON array of user_key/service_id pairs
            service_ids: Comma-separated service IDs
        
        Returns:
            JSON mapping of user keys to names
        
        Example user_keys:
        [{"user_key": "john.doe", "service_id": "123"}]
        """
        endpoint = f"organization/{org_id}/service_user/get_map/"
        
        try:
            keys_list = json.loads(user_keys) if isinstance(user_keys, str) else user_keys
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in user_keys parameter"})
        
        data = {
            "user_keys": keys_list,
            "service_ids": service_ids.split(",") if isinstance(service_ids, str) else service_ids
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_user_tags(
        org_id: int,
        user_ids: Optional[str] = None,
        tag_ids: Optional[str] = None
    ) -> str:
        """
        Get user categorization tags.
        
        Args:
            org_id: Organization identifier
            user_ids: Optional comma-separated user IDs
            tag_ids: Optional comma-separated tag IDs
        
        Returns:
            JSON with user tags and categories
        """
        endpoint = f"organization/{org_id}/service_user/tags/"
        
        params = {}
        if user_ids:
            params["user_ids"] = user_ids
        if tag_ids:
            params["tag_ids"] = tag_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_team_categories(
        org_id: int,
        include_users: bool = True
    ) -> str:
        """
        List team categories and hierarchies.
        
        Args:
            org_id: Organization identifier
            include_users: Include user assignments
        
        Returns:
            JSON array of team categories with hierarchy
        """
        endpoint = f"organization/{org_id}/categories/"
        
        params = {
            "include_users": include_users
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

