"""Dashboards & Widgets Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all dashboard-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_dashboards(
        org_id: int,
        project_id: Optional[int] = None
    ) -> str:
        """
        List dashboards for organization or project.
        
        Args:
            org_id: Organization identifier
            project_id: Optional project filter
        
        Returns:
            JSON array of dashboards
        """
        if project_id:
            endpoint = f"project/{project_id}/dashboards/"
        else:
            endpoint = f"organization/{org_id}/dashboards/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_dashboard_widgets(
        org_id: int,
        dashboard_id: Optional[int] = None,
        widget_type: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Get dashboard widgets and their configurations.
        
        Args:
            org_id: Organization identifier
            dashboard_id: Optional specific dashboard
            widget_type: Optional widget type filter
            limit: Maximum results
        
        Returns:
            JSON array of dashboard widgets
        """
        endpoint = f"organization/{org_id}/dashboard_widgets/"
        
        params = {"limit": limit}
        if dashboard_id:
            params["dashboard_id"] = dashboard_id
        if widget_type:
            params["widget_type"] = widget_type
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_dashboard_widget(
        org_id: int,
        dashboard_id: int,
        widget_type: str,
        config: str,
        title: str
    ) -> str:
        """
        Create a new dashboard widget.
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to add widget to
            widget_type: Type of widget (chart, table, metric)
            config: JSON configuration for the widget
            title: Widget title
        
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
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_shared_links(org_id: int) -> str:
        """
        Get shared dashboard links for an organization.
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON array of shared links
        """
        endpoint = f"organization/{org_id}/shared_links/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_shared_link(
        org_id: int,
        dashboard_id: int,
        expires_at: Optional[str] = None,
        password: Optional[str] = None
    ) -> str:
        """
        Create a shared link for a dashboard.
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to share
            expires_at: Optional expiration date
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

