"""Employee Performance & Productivity Analytics"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all employee-related tools with the MCP server"""

    @mcp.tool()
    async def get_employee_metrics(project_id: int, item_id: int) -> str:
        """
        Retrieve metrics configuration and overview data for a specific employee in a project.

        From OpenAPI: GET /api/v1/employee/{project_id}/metrics/

        This endpoint provides the necessary context for displaying employee-specific metrics.

        Args:
            project_id: Project identifier (required in URL path)
            item_id: ID of the employee (ServiceUsers ID) (required query parameter)

        Returns:
            JSON with employee metrics configuration including:
            - Start and end dates for the analysis period
            - Employee name and project details
            - Available metrics with configuration and categories
        """
        endpoint = f"employee/{project_id}/metrics/"

        params: dict[str, object] = {"item_id": item_id}

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_employee_periods(project_id: int, item_id: int) -> str:
        """
        Get time periods available for employee metrics analysis.

        From OpenAPI: GET /api/v1/employee/{project_id}/periods/

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID) - query parameter

        Returns:
            JSON with available time periods for the employee
        """
        endpoint = f"employee/{project_id}/periods/"

        params: dict[str, object] = {"item_id": item_id}

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_project_employees(
        project_id: int,
        include_disabled_users: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        Retrieve a list of employees (service users) for a specific project with their
        organizational relationships and service assignments.

        From OpenAPI: GET /api/v1/employee/{project_id}/users/

        Args:
            project_id: Project identifier
            include_disabled_users: Include disabled users in results (0 = no, 1 = yes) (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Employees with:
            - Employee ID, name, and email
            - Cohort leadership status (has children)
            - Service count (number of services assigned)
            - Results sorted alphabetically by name
        """
        endpoint = f"employee/{project_id}/users/"

        params: dict[str, object] = {"include_disabled_users": include_disabled_users}

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_employee_cohort_data(
        project_id: int,
        item_id: int,
        metric_type: str,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC",
        response_format: str = "json",
    ) -> str:
        """
        Get cohort comparison data for an employee metric.

        From OpenAPI: GET /api/v1/employee/{project_id}/cohort/{item_id}/{metric_type}

        Compare an individual's metrics against their cohort/team.

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID)
            metric_type: Metric type to retrieve
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
            response_format: Output encoding: json (default) or toon

        Returns:
            Cohort comparison data
        """
        endpoint = f"employee/{project_id}/cohort/{item_id}/{metric_type}"

        params: dict[str, object] = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_employee_metric_data(
        project_id: int,
        item_id: int,
        metric_type: str,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC",
        grouping: Optional[str] = None,
        response_format: str = "json",
    ) -> str:
        """
        Get detailed metric data for a specific employee.

        From OpenAPI: GET /api/v1/employee/{project_id}/metric/{item_id}/{metric_type}

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID)
            metric_type: Metric type to retrieve
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
            grouping: Optional grouping parameter
            response_format: Output encoding: json (default) or toon

        Returns:
            Employee metric time series data
        """
        endpoint = f"employee/{project_id}/metric/{item_id}/{metric_type}"

        params: dict[str, object] = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if grouping:
            params["grouping"] = grouping

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_employee_work_items(
        project_id: int,
        item_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC",
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        Get work items (cards, commits, PRs) associated with an employee.

        From OpenAPI: GET /api/v1/employee/{project_id}/work_items/{item_id}

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID)
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Work items with details
        """
        endpoint = f"employee/{project_id}/work_items/{item_id}"

        params: dict[str, object] = {
            "time_zone": time_zone,
            "limit": limit,
            "offset": offset,
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_employee_timeline(
        project_id: int,
        item_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC",
        response_format: str = "json",
    ) -> str:
        """
        Get timeline of activities for an employee.

        From OpenAPI: GET /api/v1/employee/{project_id}/timeline/{item_id}

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID)
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
            response_format: Output encoding: json (default) or toon

        Returns:
            Timeline events
        """
        endpoint = f"employee/{project_id}/timeline/{item_id}"

        params: dict[str, object] = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_employee_summary(
        project_id: int,
        item_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC",
    ) -> str:
        """
        Get summary statistics for an employee's performance.

        From OpenAPI: GET /api/v1/employee/{project_id}/summary/{item_id}

        Args:
            project_id: Project identifier
            item_id: Employee (ServiceUsers ID)
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)

        Returns:
            JSON with summary statistics
        """
        endpoint = f"employee/{project_id}/summary/{item_id}"

        params: dict[str, object] = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)
