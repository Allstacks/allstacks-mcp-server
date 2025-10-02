"""Labels & Tagging Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all label and tagging-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_labels(
        org_id: int,
        label_type: Optional[str] = None,
        project_id: Optional[int] = None
    ) -> str:
        """
        List all labels in the organization.
        
        Args:
            org_id: Organization identifier
            label_type: Optional type filter (epic, feature, story)
            project_id: Optional project filter
        
        Returns:
            JSON array of labels
        """
        endpoint = f"organization/{org_id}/labels/"
        
        params = {}
        if label_type:
            params["label_type"] = label_type
        if project_id:
            params["project_id"] = project_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_label(
        org_id: int,
        name: str,
        color: str,
        description: Optional[str] = None,
        label_type: str = "general"
    ) -> str:
        """
        Create a new label.
        
        Args:
            org_id: Organization identifier
            name: Label name
            color: Hex color code
            description: Optional description
            label_type: Type of label (general, epic, feature)
        
        Returns:
            Created label with ID
        """
        endpoint = f"organization/{org_id}/labels/"
        
        data = {
            "name": name,
            "color": color,
            "label_type": label_type
        }
        if description:
            data["description"] = description
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def add_service_user_tags(
        org_id: int,
        service_user_ids: str,
        tag_ids: str
    ) -> str:
        """
        Add tags to service users.
        
        Args:
            org_id: Organization identifier
            service_user_ids: Comma-separated user IDs
            tag_ids: Comma-separated tag IDs to add
        
        Returns:
            JSON with tagging results
        """
        endpoint = f"organization/{org_id}/service_user/service_user_tags/"
        
        data = {
            "service_user_ids": [int(x) for x in service_user_ids.split(",")],
            "tags": [int(x) for x in tag_ids.split(",")]
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def remove_service_user_tags(
        org_id: int,
        service_user_ids: str,
        tag_ids: str
    ) -> str:
        """
        Remove tags from service users.
        
        Args:
            org_id: Organization identifier
            service_user_ids: Comma-separated user IDs
            tag_ids: Comma-separated tag IDs to remove
        
        Returns:
            JSON with removal results
        """
        endpoint = f"organization/{org_id}/service_user/service_user_tags/"
        
        data = {
            "service_user_ids": [int(x) for x in service_user_ids.split(",")],
            "tags": [int(x) for x in tag_ids.split(",")],
            "remove": True
        }
        
        result = await api_client.request("DELETE", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_manageable_roles(org_id: int) -> str:
        """
        Get manageable roles and permissions for the organization.
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with roles and permissions matrix
        """
        endpoint = f"organization/{org_id}/manageable_roles"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

