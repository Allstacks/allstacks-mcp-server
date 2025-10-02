"""Forecasting & Planning Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all forecasting-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_forecast_v3(
        project_id: int,
        work_bundle_ids: Optional[str] = None,
        service_item_ids: Optional[str] = None,
        confidence_level: int = 80
    ) -> str:
        """
        Get v3 forecast data for work items.
        
        Args:
            project_id: Project identifier
            work_bundle_ids: Optional comma-separated work bundle IDs
            service_item_ids: Optional comma-separated service item IDs
            confidence_level: Confidence percentage (50-95)
        
        Returns:
            JSON with forecast data and dates
        """
        endpoint = f"forecasting/{project_id}/v3/"
        
        params = {"confidence_level": confidence_level}
        if work_bundle_ids:
            params["work_bundle_ids"] = work_bundle_ids
        if service_item_ids:
            params["service_item_ids"] = service_item_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_slots(
        org_id: int,
        start_date: str,
        end_date: str,
        project_ids: Optional[str] = None
    ) -> str:
        """
        Get resource slots/capacity for planning.
        
        Args:
            org_id: Organization identifier
            start_date: Start date for slots
            end_date: End date for slots
            project_ids: Optional comma-separated project IDs
        
        Returns:
            JSON with slot/capacity data
        """
        endpoint = f"organization/{org_id}/slots/"
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        if project_ids:
            params["project_ids"] = project_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def analyze_chart_data(
        data: str,
        analysis_type: str = "trends"
    ) -> str:
        """
        Analyze chart data for patterns and insights.
        
        Args:
            data: JSON string of chart data
            analysis_type: Type of analysis (trends, anomalies, patterns)
        
        Returns:
            JSON with analysis results
        """
        endpoint = "charts/analyze"
        
        try:
            data_dict = json.loads(data) if isinstance(data, str) else data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in data parameter"})
        
        request_data = {
            "data": data_dict,
            "analysis_type": analysis_type
        }
        
        result = await api_client.request("POST", endpoint, data=request_data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_chart_analysis(
        chart_id: int,
        project_id: int
    ) -> str:
        """
        Get AI analysis for a specific chart.
        
        Args:
            chart_id: Chart identifier
            project_id: Project context
        
        Returns:
            JSON with chart analysis
        """
        endpoint = "charts/analysis/"
        
        data = {
            "chart_id": chart_id,
            "project_id": project_id
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_company_metrics(
        org_id: int,
        metric_types: Optional[str] = None
    ) -> str:
        """
        Get company-level metrics configuration.
        
        Args:
            org_id: Organization identifier
            metric_types: Optional comma-separated metric types
        
        Returns:
            JSON with company metrics
        """
        endpoint = f"organization/{org_id}/company_metrics/"
        
        params = {}
        if metric_types:
            params["metric_types"] = metric_types
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

