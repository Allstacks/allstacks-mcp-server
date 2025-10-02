"""Work Bundles - Selectable work bundle management for planning and tracking"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all work bundle tools with the MCP server"""
    
    @mcp.tool()
    async def list_work_bundles(
        project_id: int,
        include_completed: bool = False,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List work bundles (selectable work bundles) for a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/work_bundles/
        
        Work bundles are collections of work items that can be selected together
        for planning, forecasting, and tracking.
        
        Args:
            project_id: Project identifier
            include_completed: Include completed work bundles (default: False)
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of work bundles with metadata and item counts
        """
        endpoint = f"project/{project_id}/work_bundles/"
        
        params = {
            "include_completed": include_completed,
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_work_bundle(
        project_id: int,
        name: str,
        description: Optional[str] = None,
        service_item_ids: Optional[str] = None
    ) -> str:
        """
        Create a new work bundle.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/
        
        Args:
            project_id: Project identifier
            name: Work bundle name (REQUIRED)
            description: Optional description
            service_item_ids: Optional comma-separated service item IDs to include initially
        
        Returns:
            Created work bundle with ID
        """
        endpoint = f"project/{project_id}/work_bundles/"
        
        data = {"name": name}
        
        if description:
            data["description"] = description
        if service_item_ids:
            data["service_item_ids"] = service_item_ids
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_work_bundle(project_id: int, bundle_id: int) -> str:
        """
        Get detailed information about a specific work bundle.
        
        From OpenAPI: GET /api/v1/project/{project_id}/work_bundles/{id}/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
        
        Returns:
            JSON with work bundle details including all service items
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_work_bundle(
        project_id: int,
        bundle_id: int,
        bundle_data: str
    ) -> str:
        """
        Update work bundle properties.
        
        From OpenAPI: PUT/PATCH /api/v1/project/{project_id}/work_bundles/{id}/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
            bundle_data: JSON string with bundle updates (name, description, etc.)
        
        Returns:
            Updated work bundle details
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/"
        
        try:
            data = json.loads(bundle_data) if isinstance(bundle_data, str) else bundle_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in bundle_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_work_bundle(project_id: int, bundle_id: int) -> str:
        """
        Delete a work bundle.
        
        From OpenAPI: DELETE /api/v1/project/{project_id}/work_bundles/{id}/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def add_items_to_work_bundle(
        project_id: int,
        bundle_id: int,
        service_item_ids: str
    ) -> str:
        """
        Add service items to a work bundle.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/{id}/add_items/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
            service_item_ids: Comma-separated service item IDs to add (REQUIRED)
        
        Returns:
            Updated work bundle with new item count
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/add_items/"
        
        data = {"service_item_ids": service_item_ids}
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def remove_items_from_work_bundle(
        project_id: int,
        bundle_id: int,
        service_item_ids: str
    ) -> str:
        """
        Remove service items from a work bundle.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/{id}/remove_items/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
            service_item_ids: Comma-separated service item IDs to remove (REQUIRED)
        
        Returns:
            Updated work bundle with new item count
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/remove_items/"
        
        data = {"service_item_ids": service_item_ids}
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_work_bundle_forecast(
        project_id: int,
        bundle_id: int,
        confidence_level: int = 80,
        time_zone: str = "UTC"
    ) -> str:
        """
        Get forecast data for a specific work bundle.
        
        From OpenAPI: GET /api/v1/project/{project_id}/work_bundles/{id}/forecast/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
            confidence_level: Confidence percentage (50-95) (default: 80)
            time_zone: Timezone string (default: UTC)
        
        Returns:
            JSON with forecast completion dates and probability distributions
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/forecast/"
        
        params = {
            "confidence_level": confidence_level,
            "time_zone": time_zone
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_work_bundle_metrics(
        project_id: int,
        bundle_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC"
    ) -> str:
        """
        Get metrics data for a work bundle.
        
        From OpenAPI: GET /api/v1/project/{project_id}/work_bundles/{id}/metrics/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
        
        Returns:
            JSON with velocity, cycle time, and other metrics for the bundle
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/metrics/"
        
        params = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def clone_work_bundle(
        project_id: int,
        bundle_id: int,
        new_name: str
    ) -> str:
        """
        Clone a work bundle with a new name.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/{id}/clone/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier to clone
            new_name: Name for the cloned bundle (REQUIRED)
        
        Returns:
            Cloned work bundle with new ID
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/clone/"
        
        data = {"name": new_name}
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def mark_work_bundle_complete(project_id: int, bundle_id: int) -> str:
        """
        Mark a work bundle as completed.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/{id}/complete/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
        
        Returns:
            Updated work bundle with completed status
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/complete/"
        
        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def reopen_work_bundle(project_id: int, bundle_id: int) -> str:
        """
        Reopen a completed work bundle.
        
        From OpenAPI: POST /api/v1/project/{project_id}/work_bundles/{id}/reopen/
        
        Args:
            project_id: Project identifier
            bundle_id: Work bundle identifier
        
        Returns:
            Updated work bundle with reopened status
        """
        endpoint = f"project/{project_id}/work_bundles/{bundle_id}/reopen/"
        
        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

