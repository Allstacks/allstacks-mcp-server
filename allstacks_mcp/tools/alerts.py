"""Alerts & Monitoring Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all alert and monitoring-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_service_item_alerts(
        project_id: int,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None,
        active_only: bool = True
    ) -> str:
        """
        Get alerts for service items.
        
        Args:
            project_id: Project identifier
            alert_type: Optional alert type filter
            severity: Optional severity (low, medium, high, critical)
            active_only: Only show active alerts
        
        Returns:
            JSON array of alerts
        """
        endpoint = f"project/{project_id}/alerts/"
        
        params = {"active_only": active_only}
        if alert_type:
            params["alert_type"] = alert_type
        if severity:
            params["severity"] = severity
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_deliverable_risks(
        project_id: int,
        risk_threshold: str = "medium",
        include_mitigations: bool = True
    ) -> str:
        """
        Get deliverable risk assessment.
        
        Args:
            project_id: Project identifier
            risk_threshold: Minimum risk level (low, medium, high)
            include_mitigations: Include mitigation suggestions
        
        Returns:
            JSON with risk assessment
        """
        endpoint = f"project/{project_id}/deliverable_risks/"
        
        params = {
            "risk_threshold": risk_threshold,
            "include_mitigations": include_mitigations
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_health(
        org_id: int,
        service_ids: Optional[str] = None
    ) -> str:
        """
        Get health status of integrated services.
        
        Args:
            org_id: Organization identifier
            service_ids: Optional comma-separated service IDs
        
        Returns:
            JSON with service health metrics
        """
        endpoint = f"organization/{org_id}/service_health/"
        
        params = {}
        if service_ids:
            params["service_ids"] = service_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_error_logs(
        org_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        service_id: Optional[int] = None,
        limit: int = 100
    ) -> str:
        """
        Get error logs for debugging.
        
        Args:
            org_id: Organization identifier
            start_date: Optional start date
            end_date: Optional end date
            service_id: Optional service filter
            limit: Maximum logs to return
        
        Returns:
            JSON array of error logs
        """
        endpoint = f"organization/{org_id}/error_logs/"
        
        params = {"limit": limit}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if service_id:
            params["service_id"] = service_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_audit_log(
        org_id: int,
        user_id: Optional[int] = None,
        action_type: Optional[str] = None,
        start_date: Optional[str] = None,
        limit: int = 100
    ) -> str:
        """
        Get audit log of user actions.
        
        Args:
            org_id: Organization identifier
            user_id: Optional user filter
            action_type: Optional action type filter
            start_date: Optional start date
            limit: Maximum entries
        
        Returns:
            JSON array of audit log entries
        """
        endpoint = f"organization/{org_id}/audit_log/"
        
        params = {"limit": limit}
        if user_id:
            params["user_id"] = user_id
        if action_type:
            params["action_type"] = action_type
        if start_date:
            params["start_date"] = start_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

