"""Metrics Data Retrieval Endpoints (7 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all metrics-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_metrics(org_id: Optional[int] = None) -> str:
        """
        List all available metric types and their definitions.
        
        Args:
            org_id: Optional organization ID for org-specific metrics
        
        Returns:
            JSON array of available metrics with descriptions
        """
        endpoint = "metrics/"
        params = {"org_id": org_id} if org_id else {}
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metric_info(metric_id: int) -> str:
        """
        Get detailed information about a specific metric.
        
        Args:
            metric_id: The metric identifier
        
        Returns:
            JSON with metric configuration and metadata
        """
        endpoint = f"metrics/{metric_id}/get_generated_metric_info/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_gmdts_data(
        project_id: int,
        metric_type: str,
        start_date: str,
        end_date: str,
        dimensions: Optional[str] = None,
        filters: Optional[str] = None,
        aggregation: str = "sum",
        group_by: Optional[str] = None,
        limit: int = 1000
    ) -> str:
        """
        Fetch Generated Metric Data Time Series (GMDTS) data.
        
        Args:
            project_id: Project identifier
            metric_type: Type of metric (from list_metrics)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            dimensions: Comma-separated dimensions (user_name,service_id,series_id)
            filters: JSON string of filters {"service_ids": [], "user_ids": []}
            aggregation: Aggregation method (sum, avg, count, min, max)
            group_by: Group by period (day, week, month)
            limit: Maximum results to return
        
        Returns:
            JSON formatted time series data
        """
        endpoint = f"project/{project_id}/metrics/gmdts/{metric_type}/"
        
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "aggregation": aggregation,
            "limit": limit
        }
        
        if dimensions:
            params["dimensions"] = dimensions
        if group_by:
            params["group_by"] = group_by
        if filters:
            params["filters"] = filters
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_data(
        project_id: int,
        config: str
    ) -> str:
        """
        Fetch data using Metrics V2 configuration (Work Item Table/Data Explorer).
        
        Args:
            project_id: Project identifier
            config: JSON string of Metrics V2 configuration with:
                - pagination: {limit, offset}
                - filters: {default: {}, advanced_filters: {}}
                - views: [{dimensions: [...]}]
                - sort: [{key, desc}]
        
        Returns:
            JSON formatted results with data and metadata
        
        Example config:
        {
            "pagination": {"limit": 100, "offset": 0},
            "filters": {
                "default": {"item_type": "CARD"},
                "advanced_filters": {
                    "type": "and",
                    "children": [
                        {"prop": "status", "operation": "equals", "value": "Done"}
                    ]
                }
            },
            "views": [{
                "dimensions": [
                    {"property": "id", "header": "ID"},
                    {"property": "item_name", "header": "Name"},
                    {"property": "story_points", "header": "Points"}
                ]
            }]
        }
        """
        endpoint = f"project/{project_id}/metrics/v2/data/"
        
        try:
            config_dict = json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config parameter"})
        
        result = await api_client.request("POST", endpoint, data={"config": config_dict})
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_metrics_v2_configs(project_id: int) -> str:
        """
        List saved Metrics V2 configurations for a project.
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of saved configurations
        """
        endpoint = f"project/{project_id}/configs/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_metrics_v2_config(
        project_id: int,
        name: str,
        config: str,
        description: Optional[str] = None
    ) -> str:
        """
        Create a new Metrics V2 configuration.
        
        Args:
            project_id: Project identifier
            name: Configuration name
            config: JSON string of configuration
            description: Optional description
        
        Returns:
            Created configuration with ID
        """
        endpoint = f"project/{project_id}/configs/"
        
        try:
            config_dict = json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config parameter"})
        
        data = {
            "name": name,
            "config": config_dict,
            "description": description
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_insight_configs(
        project_id: int,
        metric_types: Optional[str] = None,
        insight_keys: Optional[str] = None
    ) -> str:
        """
        Get insight configurations that dictate GMDTS parameters.
        
        Args:
            project_id: Project identifier
            metric_types: Comma-separated metric types to filter
            insight_keys: Comma-separated insight keys to filter
        
        Returns:
            JSON array of insight configurations
        """
        endpoint = f"project/{project_id}/insights/configs"
        
        params = {}
        if metric_types:
            params["metric_types"] = metric_types
        if insight_keys:
            params["insight_keys"] = insight_keys
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

