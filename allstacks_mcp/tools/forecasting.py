"""Forecasting & Planning - Project delivery predictions and capacity planning"""

import json
from typing import Optional

from .._json_input import JsonObjectInput, JsonValueInput, parse_json_input


def register_tools(mcp, api_client):
    """Register all forecasting-related tools with the MCP server"""

    @mcp.tool()
    async def get_forecast_v3(
        project_id: int,
        work_bundle_ids: Optional[str] = None,
        service_item_ids: Optional[str] = None,
        confidence_level: int = 80,
        time_zone: str = "UTC",
        response_format: str = "json",
    ) -> str:
        """
        Get v3 forecast data for work items with probability distributions.

        From OpenAPI: GET /api/v1/forecasting/{project_id}/v3/

        Monte Carlo simulation-based forecasting for work bundles or service items.

        Args:
            project_id: Project identifier
            work_bundle_ids: Optional comma-separated work bundle IDs to forecast
            service_item_ids: Optional comma-separated service item IDs to forecast
            confidence_level: Confidence percentage (50-95) (default: 80)
            time_zone: Timezone string (default: UTC)
            response_format: Output encoding: json (default) or toon

        Returns:
            Forecast completion dates, probability distributions, and confidence intervals
        """
        endpoint = f"forecasting/{project_id}/v3/"

        params: dict[str, object] = {
            "confidence_level": confidence_level,
            "time_zone": time_zone,
        }
        if work_bundle_ids:
            params["work_bundle_ids[]"] = work_bundle_ids.split(",")
        if service_item_ids:
            params["service_item_ids[]"] = service_item_ids.split(",")

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_forecasting_config(project_id: int) -> str:
        """
        Get forecasting configuration for a project.

        From OpenAPI: GET /api/v1/forecasting/{project_id}/config/

        Args:
            project_id: Project identifier

        Returns:
            JSON with forecasting configuration settings
        """
        endpoint = f"forecasting/{project_id}/config/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_forecasting_config(
        project_id: int, config_data: JsonObjectInput
    ) -> str:
        """
        Update forecasting configuration for a project.

        From OpenAPI: POST /api/v1/forecasting/{project_id}/config/

        Args:
            project_id: Project identifier
            config_data: JSON string or object with configuration updates

        Returns:
            Updated forecasting configuration
        """
        endpoint = f"forecasting/{project_id}/config/"

        try:
            data = parse_json_input(config_data, name="config_data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_item_types_for_forecasting(org_id: int) -> str:
        """
        Get item types available for forecasting in the organization.

        From OpenAPI: GET /api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/

        Returns types of work items that can be forecast.

        Args:
            org_id: Organization identifier

        Returns:
            JSON array of available item types for forecasting
        """
        endpoint = f"organization/{org_id}/forecasting/item_types_for_forecasting/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_forecasting_history(
        project_id: int,
        work_bundle_id: Optional[int] = None,
        service_item_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        response_format: str = "json",
    ) -> str:
        """
        Get historical forecasting data to track forecast accuracy over time.

        From OpenAPI: GET /api/v1/forecasting/{project_id}/history/

        Args:
            project_id: Project identifier
            work_bundle_id: Optional work bundle ID to filter history
            service_item_id: Optional service item ID to filter history
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            response_format: Output encoding: json (default) or toon

        Returns:
            Historical forecast snapshots
        """
        endpoint = f"forecasting/{project_id}/history/"

        params: dict[str, object] = {"limit": limit, "offset": offset}
        if work_bundle_id:
            params["work_bundle_id"] = work_bundle_id
        if service_item_id:
            params["service_item_id"] = service_item_id

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def analyze_chart_data(
        data: JsonValueInput, analysis_type: str = "trends"
    ) -> str:
        """
        Analyze chart data for patterns, trends, and insights using AI.

        From OpenAPI: POST /api/v1/charts/analyze

        Args:
            data: JSON string or object of chart data to analyze
            analysis_type: Type of analysis to perform (trends, anomalies, patterns)

        Returns:
            JSON with AI-generated analysis results
        """
        endpoint = "charts/analyze"

        try:
            data_dict = parse_json_input(data, name="data")
        except ValueError as e:
            return json.dumps({"error": str(e)})

        request_data: dict[str, object] = {
            "data": data_dict,
            "analysis_type": analysis_type,
        }

        result = await api_client.request("POST", endpoint, data=request_data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_chart_analysis(chart_id: int, project_id: int) -> str:
        """
        Get AI analysis for a specific chart configuration.

        From OpenAPI: POST /api/v1/charts/analysis/

        Args:
            chart_id: Chart identifier
            project_id: Project context

        Returns:
            JSON with AI-generated chart insights
        """
        endpoint = "charts/analysis/"

        data: dict[str, object] = {"chart_id": chart_id, "project_id": project_id}

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_capacity_planning(
        org_id: int,
        start_date: str,
        end_date: str,
        project_ids: Optional[str] = None,
        response_format: str = "json",
    ) -> str:
        """
        Get resource capacity planning data across projects.

        From OpenAPI: GET /api/v1/organization/{org_id}/forecasting/capacity/

        Args:
            org_id: Organization identifier
            start_date: Start date for capacity planning (ISO format)
            end_date: End date for capacity planning (ISO format)
            project_ids: Optional comma-separated project IDs to include
            response_format: Output encoding: json (default) or toon

        Returns:
            Capacity allocation and availability
        """
        endpoint = f"organization/{org_id}/forecasting/capacity/"

        params: dict[str, object] = {"start_date": start_date, "end_date": end_date}
        if project_ids:
            params["project_ids[]"] = project_ids.split(",")

        return await api_client.request_text(
            "GET", endpoint, params=params, response_format=response_format
        )

    @mcp.tool()
    async def get_scenario_analysis(
        project_id: int, work_bundle_ids: str, scenarios: JsonValueInput
    ) -> str:
        """
        Run what-if scenario analysis for forecasting.

        From OpenAPI: POST /api/v1/forecasting/{project_id}/scenarios/

        Compare multiple forecasting scenarios with different assumptions.

        Args:
            project_id: Project identifier
            work_bundle_ids: Comma-separated work bundle IDs to analyze
            scenarios: JSON string or array of scenario configurations (velocity adjustments, capacity changes, etc.)

        Returns:
            JSON with comparative scenario analysis
        """
        endpoint = f"forecasting/{project_id}/scenarios/"

        try:
            scenarios_list = parse_json_input(scenarios, name="scenarios")
        except ValueError as e:
            return json.dumps({"error": str(e)})
        if not isinstance(scenarios_list, list):
            return json.dumps({"error": "scenarios must be a JSON array"})

        data: dict[str, object] = {
            "work_bundle_ids": work_bundle_ids,
            "scenarios": scenarios_list,
        }

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)
