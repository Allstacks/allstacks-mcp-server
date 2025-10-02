"""Employee & Productivity Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all employee-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_employee_metrics(project_id: int) -> str:
        """
        Get employee productivity metrics for a project.
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON with employee metrics
        """
        endpoint = f"employee/{project_id}/metrics/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_employee_periods(project_id: int) -> str:
        """
        Get employee activity periods and patterns.
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON with period data
        """
        endpoint = f"employee/{project_id}/periods/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_employee_users(project_id: int) -> str:
        """
        Get employee user list with activity data.
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of employee users
        """
        endpoint = f"employee/{project_id}/users/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_employee_metric_data(
        project_id: int,
        metric_id: int,
        user_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Get detailed employee metric data.
        
        Args:
            project_id: Project identifier
            metric_id: Metric to retrieve
            user_id: Optional user filter
            start_date: Optional start date
            end_date: Optional end date
        
        Returns:
            JSON with detailed metric data
        """
        endpoint = f"employee/{project_id}/{metric_id}/metric-data/"
        
        params = {}
        if user_id:
            params["user_id"] = user_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def merge_service_users(
        org_id: int,
        primary_user_id: int,
        user_ids_to_merge: str
    ) -> str:
        """
        Merge multiple service users into one.
        
        Args:
            org_id: Organization identifier
            primary_user_id: Primary user to merge into
            user_ids_to_merge: Comma-separated IDs to merge
        
        Returns:
            JSON with merge result
        """
        endpoint = f"organization/{org_id}/merge_users/"
        
        data = {
            "primary_user_id": primary_user_id,
            "user_ids_to_merge": [int(x) for x in user_ids_to_merge.split(",")]
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

