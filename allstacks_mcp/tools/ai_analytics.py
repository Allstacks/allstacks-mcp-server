"""AI & Analytics Endpoints (4 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all AI and analytics-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_organization_investments(org_id: int) -> str:
        """
        Get current investment analysis for an organization.
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with investment summary and breakdown
        """
        endpoint = f"organization/{org_id}/ai_summary/currentInvestments"
        
        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def generate_workflow_analysis(
        project_id: int,
        analysis_type: str = "patterns",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Generate AI-powered workflow analysis report.
        
        Args:
            project_id: Project identifier
            analysis_type: Type of analysis (patterns, bottlenecks, recommendations)
            start_date: Optional start date for analysis
            end_date: Optional end date for analysis
        
        Returns:
            JSON with AI-generated analysis
        """
        endpoint = f"project/{project_id}/ai_analysis/workflow/"
        
        data = {
            "analysis_type": analysis_type
        }
        
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_developer_experience_metrics(
        org_id: int,
        project_id: Optional[int] = None,
        period: str = "last_30_days"
    ) -> str:
        """
        Get developer experience (DevEx) metrics and survey results.
        
        Args:
            org_id: Organization identifier
            project_id: Optional project filter
            period: Time period (last_7_days, last_30_days, last_quarter)
        
        Returns:
            JSON with DevEx metrics and insights
        """
        endpoint = f"organization/{org_id}/developer_experience/"
        
        params = {
            "period": period
        }
        
        if project_id:
            params["project_id"] = project_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_capitalization_report(
        org_id: int,
        start_date: str,
        end_date: str,
        report_type: str = "standard"
    ) -> str:
        """
        Get R&D capitalization report for financial analysis.
        
        Args:
            org_id: Organization identifier
            start_date: Report start date (YYYY-MM-DD)
            end_date: Report end date (YYYY-MM-DD)
            report_type: Type of report (standard, detailed, summary)
        
        Returns:
            JSON with capitalization data and breakdowns
        """
        endpoint = f"organization/{org_id}/capitalization_report/"
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "report_type": report_type
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

