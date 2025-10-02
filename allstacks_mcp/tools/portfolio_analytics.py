"""Portfolio Analytics Endpoints (7 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all portfolio analytics-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_portfolio_health(
        org_id: int,
        portfolio_id: int,
        include_trends: bool = True
    ) -> str:
        """
        Get health metrics for a portfolio.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            include_trends: Include trend analysis
        
        Returns:
            JSON with portfolio health metrics
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/health/"
        
        params = {
            "include_trends": include_trends
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_portfolio_timeline(
        org_id: int,
        portfolio_id: int,
        view_type: str = "gantt",
        include_dependencies: bool = True
    ) -> str:
        """
        Get timeline view of portfolio items.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            view_type: Timeline view type (gantt, roadmap, calendar)
            include_dependencies: Include dependency links
        
        Returns:
            JSON with timeline data
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/timeline/"
        
        params = {
            "view_type": view_type,
            "include_dependencies": include_dependencies
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_portfolio_allocation(
        org_id: int,
        portfolio_id: int,
        breakdown_by: str = "project",
        include_capacity: bool = True
    ) -> str:
        """
        Get resource allocation across portfolio.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            breakdown_by: Allocation breakdown (project, team, skill)
            include_capacity: Include capacity analysis
        
        Returns:
            JSON with allocation data
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/allocation/"
        
        params = {
            "breakdown_by": breakdown_by,
            "include_capacity": include_capacity
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_portfolio_dependencies(
        org_id: int,
        portfolio_id: int,
        include_external: bool = True,
        include_risks: bool = True
    ) -> str:
        """
        Get dependency map for portfolio items.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            include_external: Include external dependencies
            include_risks: Include dependency risks
        
        Returns:
            JSON with dependency graph
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/dependencies/"
        
        params = {
            "include_external": include_external,
            "include_risks": include_risks
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def compare_portfolios(
        org_id: int,
        portfolio_ids: str,
        metrics: Optional[str] = None,
        period: Optional[str] = None
    ) -> str:
        """
        Compare multiple portfolios side by side.
        
        Args:
            org_id: Organization identifier
            portfolio_ids: Comma-separated portfolio IDs to compare
            metrics: Optional comma-separated metrics to compare
            period: Optional time period for comparison
        
        Returns:
            JSON with portfolio comparison
        """
        endpoint = f"organization/{org_id}/portfolios/compare/"
        
        params = {
            "portfolio_ids": portfolio_ids
        }
        
        if metrics:
            params["metrics"] = metrics
        if period:
            params["period"] = period
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_portfolio_forecast(
        org_id: int,
        portfolio_id: int,
        forecast_months: int = 3,
        confidence_level: int = 80,
        include_scenarios: bool = True
    ) -> str:
        """
        Get forecasted completion for portfolio items.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            forecast_months: Months to forecast ahead
            confidence_level: Confidence percentage (50-95)
            include_scenarios: Include best/worst case scenarios
        
        Returns:
            JSON with portfolio forecast
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/forecast/"
        
        params = {
            "forecast_months": forecast_months,
            "confidence_level": confidence_level,
            "include_scenarios": include_scenarios
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def export_portfolio_report(
        org_id: int,
        portfolio_id: int,
        report_type: str = "executive",
        format: str = "json",
        include_charts: bool = True
    ) -> str:
        """
        Export comprehensive portfolio report.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            report_type: Type of report (executive, detailed, status)
            format: Export format (json, csv, pdf)
            include_charts: Include chart data
        
        Returns:
            JSON with report data or download URL
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/export/"
        
        params = {
            "report_type": report_type,
            "format": format,
            "include_charts": include_charts
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

