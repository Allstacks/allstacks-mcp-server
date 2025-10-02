"""Labels & Label Families - Categorization and tagging system"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all labels-related tools with the MCP server"""
    
    # ============================================================================
    # Labels
    # ============================================================================
    
    @mcp.tool()
    async def list_labels(
        org_id: int,
        label_family_id: Optional[int] = None,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all labels for an organization with optional filtering by label family.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/labels/
        
        Manage labels for service items within an organization. Labels help categorize
        and organize work items, commits, pull requests, and other service items.
        
        Args:
            org_id: Organization identifier
            label_family_id: Optional filter by label family ID
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of labels with hierarchy information
        """
        endpoint = f"organization/{org_id}/labels/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if label_family_id:
            params["label_family_id"] = label_family_id
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_label(
        org_id: int,
        name: str,
        label_family_id: Optional[int] = None,
        description: Optional[str] = None,
        color: Optional[str] = None
    ) -> str:
        """
        Create a new label for categorizing service items.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/labels/
        
        Args:
            org_id: Organization identifier
            name: Label name (REQUIRED)
            label_family_id: Optional parent label family
            description: Optional label description
            color: Optional color code (hex format)
        
        Returns:
            Created label with ID
        """
        endpoint = f"organization/{org_id}/labels/"
        
        data = {"name": name}
        
        if label_family_id:
            data["label_family_id"] = label_family_id
        if description:
            data["description"] = description
        if color:
            data["color"] = color
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_label(org_id: int, label_id: int) -> str:
        """
        Get specific label details including usage statistics.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/labels/{id}/
        
        Args:
            org_id: Organization identifier
            label_id: Label identifier
        
        Returns:
            JSON with label information including:
            - Label ID, name, and description
            - Label family and hierarchy information
            - Usage statistics and metadata
            - Color and display settings
        """
        endpoint = f"organization/{org_id}/labels/{label_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_label(
        org_id: int,
        label_id: int,
        label_data: str
    ) -> str:
        """
        Update label properties.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/labels/{id}/
        
        Args:
            org_id: Organization identifier
            label_id: Label identifier
            label_data: JSON string with label updates (name, description, color, etc.)
        
        Returns:
            Updated label details
        """
        endpoint = f"organization/{org_id}/labels/{label_id}/"
        
        try:
            data = json.loads(label_data) if isinstance(label_data, str) else label_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in label_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_label(
        org_id: int,
        label_id: int,
        delete_children: bool = False
    ) -> str:
        """
        Delete a label with optional cascading to child labels.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/labels/{id}/
        
        Notes:
        - Labels with 'Untracked' name cannot be deleted manually
        - Deleting a label can optionally delete child labels
        - Label operations are performed through the LabelsService
        
        Args:
            org_id: Organization identifier
            label_id: Label identifier
            delete_children: If True, also delete all child labels (default: False)
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/labels/{label_id}/"
        
        params = {}
        if delete_children:
            params["delete_children"] = delete_children
        
        result = await api_client.request("DELETE", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Label Families
    # ============================================================================

    @mcp.tool()
    async def list_label_families(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all label families (hierarchical label groups) for the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/labels/label_families/
        
        Label families provide hierarchical organization of labels, allowing for
        multi-level categorization structures.
        
        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of label families with their hierarchies
        """
        endpoint = f"organization/{org_id}/labels/label_families/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_label_family(
        org_id: int,
        name: str,
        description: Optional[str] = None,
        parent_family_id: Optional[int] = None
    ) -> str:
        """
        Create a new label family for hierarchical organization.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/labels/label_families/
        
        Args:
            org_id: Organization identifier
            name: Family name (REQUIRED)
            description: Optional family description
            parent_family_id: Optional parent family for nested hierarchies
        
        Returns:
            Created label family with ID
        """
        endpoint = f"organization/{org_id}/labels/label_families/"
        
        data = {"name": name}
        
        if description:
            data["description"] = description
        if parent_family_id:
            data["parent_family_id"] = parent_family_id
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_label_family(org_id: int, family_id: int) -> str:
        """
        Get specific label family details including all child labels.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/labels/label_families/{id}/
        
        Args:
            org_id: Organization identifier
            family_id: Label family identifier
        
        Returns:
            JSON with label family details and hierarchy
        """
        endpoint = f"organization/{org_id}/labels/label_families/{family_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_label_family(
        org_id: int,
        family_id: int,
        family_data: str
    ) -> str:
        """
        Update label family properties.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/labels/label_families/{id}/
        
        Args:
            org_id: Organization identifier
            family_id: Label family identifier
            family_data: JSON string with family updates (name, description, etc.)
        
        Returns:
            Updated label family details
        """
        endpoint = f"organization/{org_id}/labels/label_families/{family_id}/"
        
        try:
            data = json.loads(family_data) if isinstance(family_data, str) else family_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in family_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_label_family(
        org_id: int,
        family_id: int,
        delete_labels: bool = False
    ) -> str:
        """
        Delete a label family with optional cascading to labels.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/labels/label_families/{id}/
        
        Args:
            org_id: Organization identifier
            family_id: Label family identifier
            delete_labels: If True, also delete all labels in this family (default: False)
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/labels/label_families/{family_id}/"
        
        params = {}
        if delete_labels:
            params["delete_labels"] = delete_labels
        
        result = await api_client.request("DELETE", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Bulk Label Operations
    # ============================================================================

    @mcp.tool()
    async def bulk_assign_labels(
        org_id: int,
        service_item_ids: str,
        label_ids: str
    ) -> str:
        """
        Assign labels to multiple service items in bulk.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/labels/bulk_assign/
        
        Args:
            org_id: Organization identifier
            service_item_ids: Comma-separated list of service item IDs (REQUIRED)
            label_ids: Comma-separated list of label IDs to assign (REQUIRED)
        
        Returns:
            Confirmation with count of items updated
        """
        endpoint = f"organization/{org_id}/labels/bulk_assign/"
        
        data = {
            "service_item_ids": service_item_ids,
            "label_ids": label_ids
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def bulk_remove_labels(
        org_id: int,
        service_item_ids: str,
        label_ids: str
    ) -> str:
        """
        Remove labels from multiple service items in bulk.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/labels/bulk_remove/
        
        Args:
            org_id: Organization identifier
            service_item_ids: Comma-separated list of service item IDs (REQUIRED)
            label_ids: Comma-separated list of label IDs to remove (REQUIRED)
        
        Returns:
            Confirmation with count of items updated
        """
        endpoint = f"organization/{org_id}/labels/bulk_remove/"
        
        data = {
            "service_item_ids": service_item_ids,
            "label_ids": label_ids
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Service Item Labels
    # ============================================================================

    @mcp.tool()
    async def get_service_item_labels(
        org_id: int,
        service_item_id: int
    ) -> str:
        """
        Get all labels assigned to a specific service item.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/service_items/{service_item_id}/labels/
        
        Args:
            org_id: Organization identifier
            service_item_id: Service item identifier
        
        Returns:
            JSON array of labels assigned to the service item
        """
        endpoint = f"organization/{org_id}/service_items/{service_item_id}/labels/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def assign_service_item_label(
        org_id: int,
        service_item_id: int,
        label_id: int
    ) -> str:
        """
        Assign a label to a service item.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/service_items/{service_item_id}/labels/
        
        Args:
            org_id: Organization identifier
            service_item_id: Service item identifier
            label_id: Label ID to assign
        
        Returns:
            Confirmation of assignment
        """
        endpoint = f"organization/{org_id}/service_items/{service_item_id}/labels/"
        
        data = {"label_id": label_id}
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def remove_service_item_label(
        org_id: int,
        service_item_id: int,
        label_id: int
    ) -> str:
        """
        Remove a label from a service item.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/service_items/{service_item_id}/labels/{label_id}/
        
        Args:
            org_id: Organization identifier
            service_item_id: Service item identifier
            label_id: Label ID to remove
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/service_items/{service_item_id}/labels/{label_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
