"""Organization & Project Endpoints (4 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all organization and project-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_organization_settings(org_id: int) -> str:
        """
        Get organization configuration and settings.
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with organization settings
        """
        endpoint = f"organization/{org_id}/settings/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_projects(org_id: int, include_disabled: bool = False) -> str:
        """
        List all projects in an organization.
        
        Args:
            org_id: Organization identifier
            include_disabled: Include disabled projects
        
        Returns:
            JSON array of projects
        """
        endpoint = f"organization/{org_id}/projects/"
        
        params = {
            "include_disabled": include_disabled
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project_services(
        project_id: int,
        include_disabled: bool = False
    ) -> str:
        """
        Get connected services for a project.
        
        Args:
            project_id: Project identifier
            include_disabled: Include disabled services
        
        Returns:
            JSON array of connected services
        """
        endpoint = f"project/{project_id}/services/"
        
        params = {
            "include_disabled": include_disabled
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_enabled_work_bundles(
        project_id: int,
        service_ids: Optional[str] = None
    ) -> str:
        """
        List enabled work bundles for a project.
        
        Args:
            project_id: Project identifier
            service_ids: Optional comma-separated service IDs
        
        Returns:
            JSON array of work bundles
        """
        endpoint = f"project/{project_id}/work_bundles/"
        
        params = {
            "enabled": True
        }
        
        if service_ids:
            params["service_ids"] = service_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

