"""Service Items & Filtering Endpoints (6 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all service items-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_service_items(
        project_id: int,
        item_types: Optional[str] = None,
        service_ids: Optional[str] = None,
        assignee_ids: Optional[str] = None,
        parent_item_ids: Optional[str] = None,
        updated_after: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List service items with comprehensive filtering.
        
        Args:
            project_id: Project identifier
            item_types: Comma-separated types (CARD,COMMIT,PULL_REQUEST)
            service_ids: Comma-separated service IDs
            assignee_ids: Comma-separated assignee user IDs
            parent_item_ids: Comma-separated parent item IDs
            updated_after: ISO date for items updated after
            status: Item status filter
            limit: Maximum items to return
            offset: Pagination offset
        
        Returns:
            JSON array of service items
        """
        endpoint = f"project/{project_id}/service_items/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if item_types:
            params["item_types"] = item_types
        if service_ids:
            params["service_ids"] = service_ids
        if assignee_ids:
            params["assignee_ids"] = assignee_ids
        if parent_item_ids:
            params["parent_item_ids"] = parent_item_ids
        if updated_after:
            params["updated_after"] = updated_after
        if status:
            params["status"] = status
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_item_props(
        project_id: int,
        item_types: Optional[str] = None,
        data_types: Optional[str] = None,
        many: bool = False,
        versioned: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        Get available properties for service items (for filtering).
        
        Args:
            project_id: Project identifier
            item_types: Comma-separated item types to filter
            data_types: Comma-separated prop data types
            many: Include many-valued properties
            versioned: Include versioned properties
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            JSON array of available properties with metadata
        """
        endpoint = f"project/{project_id}/item_props/"
        
        params = {
            "limit": limit,
            "offset": offset,
            "many": many,
            "versioned": versioned
        }
        
        if item_types:
            params["item_types"] = item_types
        if data_types:
            params["data_types"] = data_types
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_configuration_options(
        org_id: int,
        metric: Optional[int] = None,
        item_types: Optional[str] = None
    ) -> str:
        """
        Get configuration options for metrics and filtering.
        
        Args:
            org_id: Organization identifier
            metric: Metric ID for metric-specific options
            item_types: Comma-separated item types
        
        Returns:
            JSON with available configuration options
        """
        endpoint = f"organization/{org_id}/configuration_options/"
        
        params = {}
        if metric:
            params["metric"] = metric
        if item_types:
            params["item_types"] = item_types
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def search_service_items(
        project_id: int,
        query: str,
        item_types: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Full-text search across service items.
        
        Args:
            project_id: Project identifier
            query: Search query string
            item_types: Optional comma-separated item types to search
            limit: Maximum results
        
        Returns:
            JSON array of matching service items
        """
        endpoint = f"project/{project_id}/service_items/search/"
        
        params = {
            "q": query,
            "limit": limit
        }
        
        if item_types:
            params["item_types"] = item_types
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_parent_service_items(
        project_id: int,
        service_item_ids: str,
        depth: int = 1
    ) -> str:
        """
        Get hierarchical parent items using upward link traversal.
        
        Args:
            project_id: Project identifier
            service_item_ids: Comma-separated service item IDs
            depth: Traversal depth (1-5)
        
        Returns:
            JSON with parent hierarchy
        """
        endpoint = f"project/{project_id}/service_items/parents/"
        
        params = {
            "service_item_ids": service_item_ids,
            "depth": min(max(depth, 1), 5)  # Limit depth between 1-5
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_filter_sets(
        project_id: int,
        metric_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> str:
        """
        Get saved filter sets for metrics.
        
        Args:
            project_id: Project identifier
            metric_type: Optional metric type to filter
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            JSON array of filter sets
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if metric_type:
            params["metric_type"] = metric_type
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

