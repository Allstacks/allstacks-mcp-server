"""Dashboards & Widgets Management - Complete dashboard CRUD operations"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all dashboard-related tools with the MCP server"""
    
    # ============================================================================
    # Organization Dashboards
    # ============================================================================
    
    @mcp.tool()
    async def list_org_dashboards(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all dashboards for an organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/dashboards/
        
        Manage analytics dashboards for the organization. Users can create, view, 
        and modify dashboards containing various widgets and metrics.
        
        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of dashboards with metadata
        """
        endpoint = f"organization/{org_id}/dashboards/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_org_dashboard(org_id: int, dashboard_data: str) -> str:
        """
        Create a new dashboard for the organization.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/dashboards/
        
        Args:
            org_id: Organization identifier
            dashboard_data: JSON string with dashboard configuration (name, description, etc.)
        
        Returns:
            Created dashboard with ID
        """
        endpoint = f"organization/{org_id}/dashboards/"
        
        try:
            data = json.loads(dashboard_data) if isinstance(dashboard_data, str) else dashboard_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in dashboard_data parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_dashboard_names(org_id: int) -> str:
        """
        Get a simplified list of dashboard names and IDs for dropdown/selection purposes.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/dashboards/names/
        
        Use Cases:
        - Populating dashboard selection dropdowns
        - Quick reference for dashboard names and IDs
        - Building navigation menus
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON array of dashboard objects with id and name only
        """
        endpoint = f"organization/{org_id}/dashboards/names/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_org_dashboard(org_id: int, dashboard_id: int) -> str:
        """
        Get detailed information about a specific dashboard.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/dashboards/{id}/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier
        
        Returns:
            JSON with dashboard details including widgets and configuration
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_org_dashboard(
        org_id: int,
        dashboard_id: int,
        dashboard_data: str
    ) -> str:
        """
        Update a dashboard's configuration.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/dashboards/{id}/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier
            dashboard_data: JSON string with dashboard updates
        
        Returns:
            Updated dashboard details
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/"
        
        try:
            data = json.loads(dashboard_data) if isinstance(dashboard_data, str) else dashboard_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in dashboard_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_org_dashboard(org_id: int, dashboard_id: int) -> str:
        """
        Delete a dashboard.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/dashboards/{id}/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def clear_dashboard_widgets(org_id: int, dashboard_id: int) -> str:
        """
        Remove all widgets from a dashboard.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/dashboards/{id}/clear_widgets/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier
        
        Returns:
            Confirmation of widget removal
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/clear_widgets/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def clone_dashboard(org_id: int, dashboard_id: int, new_name: Optional[str] = None) -> str:
        """
        Clone a dashboard with all its widgets.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/dashboards/{id}/clone/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier to clone
            new_name: Optional name for the cloned dashboard
        
        Returns:
            Cloned dashboard details with new ID
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/clone/"
        
        data = {}
        if new_name:
            data["name"] = new_name
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Dashboard Widgets
    # ============================================================================

    @mcp.tool()
    async def list_dashboard_widgets(
        org_id: int,
        dashboard_id: Optional[int] = None,
        widget_type: Optional[str] = None,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all dashboard widgets with optional filtering.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/dashboard_widgets/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Optional filter by dashboard ID
            widget_type: Optional filter by widget type
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of dashboard widgets
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if dashboard_id:
            params["dashboard_id"] = dashboard_id
        if widget_type:
            params["widget_type"] = widget_type
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_dashboard_widget(
        org_id: int,
        dashboard_id: int,
        widget_type: str,
        config: str,
        title: str,
        description: Optional[str] = None
    ) -> str:
        """
        Create a new dashboard widget.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/dashboard_widgets/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to add widget to (REQUIRED)
            widget_type: Type of widget (REQUIRED)
            config: JSON configuration for the widget (REQUIRED)
            title: Widget title (REQUIRED)
            description: Optional widget description
        
        Returns:
            Created widget with ID
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/"
        
        try:
            config_dict = json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config parameter"})
        
        data = {
            "dashboard_id": dashboard_id,
            "widget_type": widget_type,
            "config": config_dict,
            "title": title
        }
        
        if description:
            data["description"] = description
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_dashboard_widget(org_id: int, widget_id: int) -> str:
        """
        Get detailed information about a specific widget.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/dashboard_widgets/{id}/
        
        Args:
            org_id: Organization identifier
            widget_id: Widget identifier
        
        Returns:
            JSON with widget details and configuration
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/{widget_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_dashboard_widget(
        org_id: int,
        widget_id: int,
        widget_data: str
    ) -> str:
        """
        Update a dashboard widget's configuration.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/dashboard_widgets/{id}/
        
        Args:
            org_id: Organization identifier
            widget_id: Widget identifier
            widget_data: JSON string with widget updates (config, title, description, etc.)
        
        Returns:
            Updated widget details
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/{widget_id}/"
        
        try:
            data = json.loads(widget_data) if isinstance(widget_data, str) else widget_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in widget_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_dashboard_widget(org_id: int, widget_id: int) -> str:
        """
        Delete a dashboard widget.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/dashboard_widgets/{id}/
        
        Args:
            org_id: Organization identifier
            widget_id: Widget identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/{widget_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Shared Links
    # ============================================================================

    @mcp.tool()
    async def list_shared_links(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all shared dashboard links for the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/shared_links/
        
        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of shared links
        """
        endpoint = f"organization/{org_id}/shared_links/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_shared_link(
        org_id: int,
        dashboard_id: int,
        expires_at: Optional[str] = None,
        password: Optional[str] = None
    ) -> str:
        """
        Create a shared link for a dashboard with optional expiration and password protection.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/shared_links/
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to share (REQUIRED)
            expires_at: Optional expiration date (ISO format)
            password: Optional password protection
        
        Returns:
            Created shared link with URL
        """
        endpoint = f"organization/{org_id}/shared_links/"
        
        data = {"dashboard_id": dashboard_id}
        if expires_at:
            data["expires_at"] = expires_at
        if password:
            data["password"] = password
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_shared_link(org_id: int, link_id: int) -> str:
        """
        Get details of a specific shared link.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/shared_links/{id}/
        
        Args:
            org_id: Organization identifier
            link_id: Shared link identifier
        
        Returns:
            JSON with shared link details
        """
        endpoint = f"organization/{org_id}/shared_links/{link_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_shared_link(
        org_id: int,
        link_id: int,
        link_data: str
    ) -> str:
        """
        Update a shared link's settings.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/shared_links/{id}/
        
        Args:
            org_id: Organization identifier
            link_id: Shared link identifier
            link_data: JSON string with link updates (expires_at, password, etc.)
        
        Returns:
            Updated shared link details
        """
        endpoint = f"organization/{org_id}/shared_links/{link_id}/"
        
        try:
            data = json.loads(link_data) if isinstance(link_data, str) else link_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in link_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_shared_link(org_id: int, link_id: int) -> str:
        """
        Delete/revoke a shared dashboard link.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/shared_links/{id}/
        
        Args:
            org_id: Organization identifier
            link_id: Shared link identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/shared_links/{link_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
