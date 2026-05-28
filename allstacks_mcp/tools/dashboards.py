"""Dashboards & Widgets Management - Complete dashboard CRUD operations"""

import json
from typing import Optional

from .._json_input import JsonInput, parse_json_input


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
        offset: int = 0,
        response_format: str = "json",
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
            response_format: Output encoding: json (default) or toon

        Returns:
            Dashboards with metadata
        """
        endpoint = f"organization/{org_id}/dashboards/"

        params = {"limit": limit, "offset": offset}

        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def create_org_dashboard(org_id: int, dashboard_data: JsonInput) -> str:
        """
        Create a new dashboard for the organization.

        From OpenAPI: POST /api/v1/organization/{org_id}/dashboards/

        Args:
            org_id: Organization identifier
            dashboard_data: JSON string or object with dashboard configuration (name, description, etc.)

        Returns:
            Created dashboard with ID
        """
        endpoint = f"organization/{org_id}/dashboards/"

        try:
            data = parse_json_input(dashboard_data, name="dashboard_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

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
        org_id: int, dashboard_id: int, dashboard_data: JsonInput
    ) -> str:
        """
        Update a dashboard's configuration.

        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/dashboards/{id}/

        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard identifier
            dashboard_data: JSON string or object with dashboard updates

        Returns:
            Updated dashboard details
        """
        endpoint = f"organization/{org_id}/dashboards/{dashboard_id}/"

        try:
            data = parse_json_input(dashboard_data, name="dashboard_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

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
    async def clone_dashboard(
        org_id: int, dashboard_id: int, new_name: Optional[str] = None
    ) -> str:
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
        offset: int = 0,
        response_format: str = "json",
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
            response_format: Output encoding: json (default) or toon

        Returns:
            Dashboard widgets
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/"

        params = {"limit": limit, "offset": offset}

        if dashboard_id:
            params["dashboard_id"] = dashboard_id
        if widget_type:
            params["widget_type"] = widget_type
        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def create_dashboard_widget(
        org_id: int,
        dashboard_id: int,
        widget_type: str,
        config: JsonInput,
        title: str,
        description: Optional[str] = None,
    ) -> str:
        """
        Create a new dashboard widget.

        From OpenAPI: POST /api/v1/organization/{org_id}/dashboard_widgets/

        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to add widget to (REQUIRED)
            widget_type: Type of widget (REQUIRED)
            config: JSON string or object configuration for the widget (REQUIRED)
            title: Widget title (REQUIRED)
            description: Optional widget description

        Returns:
            Created widget with ID
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/"

        try:
            config_dict = parse_json_input(config, name="config")
        except ValueError as e:
            return json.dumps({"error": str(e)})

        data = {
            "dashboard_id": dashboard_id,
            "widget_type": widget_type,
            "config": config_dict,
            "title": title,
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
        org_id: int, widget_id: int, widget_data: JsonInput
    ) -> str:
        """
        Update a dashboard widget's configuration.

        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/dashboard_widgets/{id}/

        Args:
            org_id: Organization identifier
            widget_id: Widget identifier
            widget_data: JSON string or object with widget updates (config, title, description, etc.)

        Returns:
            Updated widget details
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/{widget_id}/"

        try:
            data = parse_json_input(widget_data, name="widget_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

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
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        List all shared dashboard links for the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/shared_links/

        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Shared links
        """
        endpoint = f"organization/{org_id}/shared_links/"

        params = {"limit": limit, "offset": offset}

        if ordering:
            params["ordering"] = ordering

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def create_shared_link(
        org_id: int,
        dashboard_id: int,
        expires_at: Optional[str] = None,
        password: Optional[str] = None,
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
        org_id: int, link_id: int, link_data: JsonInput
    ) -> str:
        """
        Update a shared link's settings.

        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/shared_links/{id}/

        Args:
            org_id: Organization identifier
            link_id: Shared link identifier
            link_data: JSON string or object with link updates (expires_at, password, etc.)

        Returns:
            Updated shared link details
        """
        endpoint = f"organization/{org_id}/shared_links/{link_id}/"

        try:
            data = parse_json_input(link_data, name="link_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

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
