"""Organization and Project Management Tools"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all organization and project management tools with the MCP server"""
    
    # ============================================================================
    # Organization Management
    # ============================================================================
    
    @mcp.tool()
    async def list_organizations() -> str:
        """
        List all organizations accessible to the current user.
        
        From OpenAPI: GET /api/v1/organization/
        
        Returns:
            JSON array of organizations with metadata
        """
        endpoint = "organization/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_organization(org_id: int) -> str:
        """
        Get detailed information about a specific organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with organization details, settings, and configuration
        """
        endpoint = f"organization/{org_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_organization(org_id: int, org_data: str) -> str:
        """
        Update organization settings.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/
        
        Args:
            org_id: Organization identifier
            org_data: JSON string with organization updates
        
        Returns:
            Updated organization details
        """
        endpoint = f"organization/{org_id}/"
        
        try:
            data = json.loads(org_data) if isinstance(org_data, str) else org_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in org_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_organization_settings(org_id: int) -> str:
        """
        Get organization settings and configuration.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/settings/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with organization settings
        """
        endpoint = f"organization/{org_id}/settings/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_organization_settings(org_id: int, settings: str) -> str:
        """
        Update organization settings.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/settings/
        
        Args:
            org_id: Organization identifier
            settings: JSON string with settings updates
        
        Returns:
            Updated settings
        """
        endpoint = f"organization/{org_id}/settings/"
        
        try:
            data = json.loads(settings) if isinstance(settings, str) else settings
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in settings parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_employee_list(
        org_id: int,
        include_disabled_users: int = 0
    ) -> str:
        """
        List employees in the organization with filtering options.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/employee_list/
        
        Args:
            org_id: Organization identifier
            include_disabled_users: Include disabled users (0 = no, 1 = yes) (default: 0)
        
        Returns:
            JSON array of employees
        """
        endpoint = f"organization/{org_id}/employee_list/"
        
        params = {"include_disabled_users": include_disabled_users}
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_error_logs(
        org_id: int,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        Get error logs for the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/error_logs/
        
        Args:
            org_id: Organization identifier
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of error logs
        """
        endpoint = f"organization/{org_id}/error_logs/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Projects
    # ============================================================================

    @mcp.tool()
    async def list_projects(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all projects in the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/projects/
        
        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of projects with metadata
        """
        endpoint = f"organization/{org_id}/projects/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_project(org_id: int, project_data: str) -> str:
        """
        Create a new project in the organization.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/projects/
        
        Args:
            org_id: Organization identifier
            project_data: JSON string with project configuration (name, description, etc.)
        
        Returns:
            Created project details
        """
        endpoint = f"organization/{org_id}/projects/"
        
        try:
            data = json.loads(project_data) if isinstance(project_data, str) else project_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in project_data parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project(org_id: int, project_id: int) -> str:
        """
        Get detailed information about a specific project.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/projects/{id}/
        
        Args:
            org_id: Organization identifier
            project_id: Project identifier
        
        Returns:
            JSON with project details and configuration
        """
        endpoint = f"organization/{org_id}/projects/{project_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_project(org_id: int, project_id: int, project_data: str) -> str:
        """
        Update project settings and configuration.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/projects/{id}/
        
        Args:
            org_id: Organization identifier
            project_id: Project identifier
            project_data: JSON string with project updates
        
        Returns:
            Updated project details
        """
        endpoint = f"organization/{org_id}/projects/{project_id}/"
        
        try:
            data = json.loads(project_data) if isinstance(project_data, str) else project_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in project_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project_configuration(project_id: int) -> str:
        """
        Get project configuration details.
        
        From OpenAPI: GET /api/v1/project/{project_id}/configuration/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON with project configuration
        """
        endpoint = f"project/{project_id}/configuration/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_project_configuration(project_id: int, config_data: str) -> str:
        """
        Update project configuration.
        
        From OpenAPI: POST /api/v1/project/{project_id}/configuration/
        
        Args:
            project_id: Project identifier
            config_data: JSON string with configuration updates
        
        Returns:
            Updated configuration
        """
        endpoint = f"project/{project_id}/configuration/"
        
        try:
            data = json.loads(config_data) if isinstance(config_data, str) else config_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config_data parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project_services(project_id: int) -> str:
        """
        Get services configured for a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/services/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of project services (Jira, GitHub, Bitbucket, etc.)
        """
        endpoint = f"project/{project_id}/services/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_project_service_users(
        project_id: int,
        service_id: int,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List service users for a specific service in the project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/service/{service_id}/service_users/
        
        Args:
            project_id: Project identifier
            service_id: Service identifier
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of service users
        """
        endpoint = f"project/{project_id}/service/{service_id}/service_users/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Slots Configuration
    # ============================================================================

    @mcp.tool()
    async def get_project_slots(project_id: int) -> str:
        """
        Fetch all slots with their associated configurations and templates.
        
        From OpenAPI: GET /api/v1/project/{project_id}/slots/
        
        Slots are placeholders for configurable metrics/widgets in the project.
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of slots with configurations
        """
        endpoint = f"project/{project_id}/slots/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_slot_configuration(project_id: int, slot_type: str) -> str:
        """
        Get configuration for a specific slot type.
        
        From OpenAPI: GET /api/v1/project/{project_id}/slots/{slot_type}/
        
        Args:
            project_id: Project identifier
            slot_type: Slot type identifier
        
        Returns:
            JSON with slot configuration
        """
        endpoint = f"project/{project_id}/slots/{slot_type}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_slot_configuration(
        project_id: int,
        slot_type: str,
        slot_config: str
    ) -> str:
        """
        Update a slot's configuration or template.
        
        From OpenAPI: POST /api/v1/project/{project_id}/slots/{slot_type}/
        
        Args:
            project_id: Project identifier
            slot_type: Slot type identifier
            slot_config: JSON string with slot configuration
        
        Returns:
            Updated slot configuration
        """
        endpoint = f"project/{project_id}/slots/{slot_type}/"
        
        try:
            data = json.loads(slot_config) if isinstance(slot_config, str) else slot_config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in slot_config parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Time Periods
    # ============================================================================

    @mcp.tool()
    async def get_project_time_periods(project_id: int) -> str:
        """
        Get configured time periods for the project (sprints, releases, quarters).
        
        From OpenAPI: GET /api/v1/project/{project_id}/time_periods/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON with time period configuration
        """
        endpoint = f"project/{project_id}/time_periods/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_time_periods_by_type(project_id: int, period_type: str) -> str:
        """
        Get time periods of a specific type.
        
        From OpenAPI: GET /api/v1/project/{project_id}/time_periods/{type}/
        
        Args:
            project_id: Project identifier
            period_type: Period type (sprint, release, quarter, etc.)
        
        Returns:
            JSON array of time periods
        """
        endpoint = f"project/{project_id}/time_periods/{period_type}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_calendars(org_id: int) -> str:
        """
        Get organization calendars for planning and holiday scheduling.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/calendars/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON array of calendars
        """
        endpoint = f"organization/{org_id}/calendars/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_calendar(org_id: int, calendar_data: str) -> str:
        """
        Create a new organization calendar.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/calendars/
        
        Args:
            org_id: Organization identifier
            calendar_data: JSON string with calendar configuration
        
        Returns:
            Created calendar details
        """
        endpoint = f"organization/{org_id}/calendars/"
        
        try:
            data = json.loads(calendar_data) if isinstance(calendar_data, str) else calendar_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in calendar_data parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_calendar(org_id: int, calendar_id: int) -> str:
        """
        Get a specific calendar.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/calendars/{id}/
        
        Args:
            org_id: Organization identifier
            calendar_id: Calendar identifier
        
        Returns:
            JSON with calendar details
        """
        endpoint = f"organization/{org_id}/calendars/{calendar_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_calendar(org_id: int, calendar_id: int, calendar_data: str) -> str:
        """
        Update a calendar.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/calendars/{id}/
        
        Args:
            org_id: Organization identifier
            calendar_id: Calendar identifier
            calendar_data: JSON string with calendar updates
        
        Returns:
            Updated calendar details
        """
        endpoint = f"organization/{org_id}/calendars/{calendar_id}/"
        
        try:
            data = json.loads(calendar_data) if isinstance(calendar_data, str) else calendar_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in calendar_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_calendar(org_id: int, calendar_id: int) -> str:
        """
        Delete an organization calendar.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/calendars/{id}/
        
        Args:
            org_id: Organization identifier
            calendar_id: Calendar identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/calendars/{calendar_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
