"""Attainment & Goals Endpoints (7 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all attainment and goals-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_attainment_metrics(
        org_id: int,
        start_date: str,
        end_date: str,
        team_ids: Optional[str] = None,
        metric_types: Optional[str] = None
    ) -> str:
        """
        Get attainment metrics for goals and OKRs.
        
        Args:
            org_id: Organization identifier
            start_date: Period start date
            end_date: Period end date
            team_ids: Optional comma-separated team IDs
            metric_types: Optional comma-separated metric types
        
        Returns:
            JSON with attainment metrics
        """
        endpoint = f"organization/{org_id}/attainment/metrics/"
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        if team_ids:
            params["team_ids"] = team_ids
        if metric_types:
            params["metric_types"] = metric_types
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_attainment_goals(
        org_id: int,
        period: Optional[str] = None,
        status: Optional[str] = None,
        owner_ids: Optional[str] = None,
        include_archived: bool = False
    ) -> str:
        """
        List attainment goals and objectives.
        
        Args:
            org_id: Organization identifier
            period: Optional period filter (Q1_2024, H1_2024, etc.)
            status: Optional status filter (active, completed, at_risk)
            owner_ids: Optional comma-separated owner IDs
            include_archived: Include archived goals
        
        Returns:
            JSON array of attainment goals
        """
        endpoint = f"organization/{org_id}/attainment/goals/"
        
        params = {
            "include_archived": include_archived
        }
        
        if period:
            params["period"] = period
        if status:
            params["status"] = status
        if owner_ids:
            params["owner_ids"] = owner_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_attainment_goal(
        org_id: int,
        name: str,
        target_value: float,
        metric_type: str,
        period: str,
        team_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> str:
        """
        Create a new attainment goal.
        
        Args:
            org_id: Organization identifier
            name: Goal name
            target_value: Target value to achieve
            metric_type: Metric type for measurement
            period: Goal period (Q1_2024, H1_2024, etc.)
            team_id: Optional team assignment
            description: Optional description
        
        Returns:
            Created goal with ID
        """
        endpoint = f"organization/{org_id}/attainment/goals/"
        
        data = {
            "name": name,
            "target_value": target_value,
            "metric_type": metric_type,
            "period": period
        }
        
        if team_id:
            data["team_id"] = team_id
        if description:
            data["description"] = description
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_attainment_progress(
        org_id: int,
        goal_id: int,
        include_history: bool = True,
        include_projections: bool = True
    ) -> str:
        """
        Get progress tracking for an attainment goal.
        
        Args:
            org_id: Organization identifier
            goal_id: Goal identifier
            include_history: Include historical progress
            include_projections: Include future projections
        
        Returns:
            JSON with goal progress and projections
        """
        endpoint = f"organization/{org_id}/attainment/goals/{goal_id}/progress/"
        
        params = {
            "include_history": include_history,
            "include_projections": include_projections
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_attainment_widget_data(
        org_id: int,
        widget_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Get data for an attainment widget.
        
        Args:
            org_id: Organization identifier
            widget_id: Widget identifier
            start_date: Optional start date override
            end_date: Optional end date override
        
        Returns:
            JSON with widget data
        """
        endpoint = f"organization/{org_id}/attainment/widgets/{widget_id}/data/"
        
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_attainment_widget(
        org_id: int,
        dashboard_id: int,
        goal_ids: str,
        widget_type: str = "progress_bar",
        title: str = "Goal Progress"
    ) -> str:
        """
        Create an attainment tracking widget.
        
        Args:
            org_id: Organization identifier
            dashboard_id: Dashboard to add widget to
            goal_ids: Comma-separated goal IDs to track
            widget_type: Widget visualization type (progress_bar, gauge, trend_line)
            title: Widget title
        
        Returns:
            Created widget with ID
        """
        endpoint = f"organization/{org_id}/attainment/widgets/"
        
        data = {
            "dashboard_id": dashboard_id,
            "goal_ids": [int(x) for x in goal_ids.split(",")],
            "widget_type": widget_type,
            "title": title
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_attainment_report(
        org_id: int,
        period: str,
        format_type: str = "summary",
        team_breakdown: bool = True,
        include_recommendations: bool = True
    ) -> str:
        """
        Generate comprehensive attainment report.
        
        Args:
            org_id: Organization identifier
            period: Report period (Q1_2024, H1_2024, FY_2024)
            format_type: Report format (summary, detailed, executive)
            team_breakdown: Include team-level breakdown
            include_recommendations: Include AI recommendations
        
        Returns:
            JSON with attainment report
        """
        endpoint = f"organization/{org_id}/attainment/report/"
        
        data = {
            "period": period,
            "format_type": format_type,
            "team_breakdown": team_breakdown,
            "include_recommendations": include_recommendations
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

