"""Metrics Data Retrieval Endpoints - Main multi-dimension time series API"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all metrics-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_metrics(project_id: Optional[int] = None) -> str:
        """
        List all available metric types and their definitions.
        
        From OpenAPI: GET /api/v1/metrics/ - Get list of generated metrics filtered by project 
        and/or metric type.
        
        Args:
            project_id: Optional project ID to filter metrics
        
        Returns:
            JSON array of available metrics with descriptions
        """
        endpoint = "metrics/"
        params = {}
        if project_id:
            params["project_id"] = project_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metric_details(metric_id: int) -> str:
        """
        Get detailed information about a specific generated metric including configuration 
        and computed values.
        
        From OpenAPI: GET /api/v1/metrics/{id}/ - Returns detailed metric information including 
        serialized metric data and metadata.
        
        Args:
            metric_id: The metric identifier
        
        Returns:
            JSON with metric configuration and metadata
        """
        endpoint = f"metrics/{metric_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metric_info(metric_id: int) -> str:
        """
        Get detailed configuration and metadata for a specific generated metric including 
        headers, categories, and service item types.
        
        From OpenAPI: GET /api/v1/metrics/{id}/get_generated_metric_info/ - Returns comprehensive 
        metric information with value statement, description, help markup, config, metric name, 
        categories, headers, columns, and service item types.
        
        Args:
            metric_id: The metric identifier
        
        Returns:
            JSON with detailed metric configuration, help text, and structure
        """
        endpoint = f"metrics/{metric_id}/get_generated_metric_info/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_generated_metric(project_id: int, metric_type: str) -> str:
        """
        Get generated metric configuration for a specific metric type in a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/generated_metric/{metric_type}
        
        Args:
            project_id: Project identifier
            metric_type: Metric type (e.g., Velocity, CycleTime, CommitVolume)
        
        Returns:
            JSON with metric configuration
        """
        endpoint = f"project/{project_id}/generated_metric/{metric_type}"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_gmdts_data(
        project_id: int,
        metric_type: str,
        x_axis: Optional[str] = None,
        y_axis: Optional[str] = None,
        z_axis: Optional[str] = None,
        series: Optional[str] = None,
        x_axis_grouping: Optional[str] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        aggregation: str = "sum",
        time_zone: str = "UTC"
    ) -> str:
        """
        Fetch Generated Metric Data Time Series (GMDTS) data - Main multi-dimension time series API.
        
        From OpenAPI: GET/POST /api/v1/project/{project_id}/generated_metric_data/{metric_type}
        
        This is the PRIMARY metrics data endpoint supporting complex multi-dimensional queries with:
        - Cartesian dimensions (x_axis, y_axis, z_axis, series) or generic (dimension1-4)
        - Time groupings (hour, day, week, month, quarter, year, custom like "3d" or "10w")
        - Aggregations (avg, count, count_unique, min, max, sum)
        - Filtering by date ranges, services, users, work bundles, parent items
        - Team averages, trailing aggregations, show service items
        
        Args:
            project_id: Project identifier (required)
            metric_type: Type of metric - ActionsByCardType, ActiveBranches, Velocity, CycleTime, etc.
            x_axis: First dimension field (time, user_name, service_name, project_name, etc.)
            y_axis: Second dimension field
            z_axis: Third dimension field
            series: Fourth dimension (series identifier)
            x_axis_grouping: Time grouping for x_axis if time (hour, day, week, month, quarter, year, or custom like "3d")
            start_date: Unix timestamp in milliseconds for start date
            end_date: Unix timestamp in milliseconds for end date
            aggregation: Aggregation method - avg, count, count_unique, min, max, sum (default: sum)
            time_zone: Timezone for date interpretation - pytz compatible (default: UTC)
        
        Additional query parameters can be passed via POST body:
        - service_ids: Array of service IDs to filter
        - user_ids: Array of user IDs to filter  
        - parent_service_item_ids: Array of parent item IDs
        - work_bundle_ids: Array of work bundle IDs
        - show_team_average: 0/1 to show team average
        - include_disabled_users: 0/1 to include disabled users
        - show_service_items: 0/1 to show service items per data point
        - trailing_average: Custom time string for trailing average
        - trailing_aggregation: Custom time string for trailing aggregation
        
        Returns:
            JSON formatted time series data with dimensions and aggregated values
        """
        endpoint = f"project/{project_id}/generated_metric_data/{metric_type}"
        
        params = {
            "aggregation": aggregation,
            "time_zone": time_zone
        }
        
        if x_axis:
            params["x_axis"] = x_axis
        if y_axis:
            params["y_axis"] = y_axis
        if z_axis:
            params["z_axis"] = z_axis
        if series:
            params["series"] = series
        if x_axis_grouping:
            params["x_axis_grouping"] = x_axis_grouping
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project_metrics_v2_data(project_id: int, config: str) -> str:
        """
        Fetch Metrics V2 data for a project using advanced configuration (Work Item Table/Data Explorer).
        
        From OpenAPI: POST /api/v1/project/{project_id}/metrics_v2/metrics
        
        Supports complex queries with:
        - Pagination (limit, offset)
        - Advanced filters (property-based conditions with AND/OR logic)
        - Multiple views with custom dimensions
        - Sorting and grouping
        - Aggregations
        
        Args:
            project_id: Project identifier
            config: JSON string of Metrics V2 configuration
        
        Returns:
            JSON formatted results with data, metadata, and pagination info
        """
        endpoint = f"project/{project_id}/metrics_v2/metrics"
        
        try:
            config_dict = json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config parameter"})
        
        result = await api_client.request("POST", endpoint, data=config_dict)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_org_metrics_v2_data(org_id: int, config: str) -> str:
        """
        Fetch Metrics V2 data for an organization using advanced configuration.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/metrics_v2/metrics
        
        Args:
            org_id: Organization identifier
            config: JSON string of Metrics V2 configuration
        
        Returns:
            JSON formatted results with organization-wide data
        """
        endpoint = f"organization/{org_id}/metrics_v2/metrics"
        
        try:
            config_dict = json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in config parameter"})
        
        result = await api_client.request("POST", endpoint, data=config_dict)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_allstacks_labels(project_id: int) -> str:
        """
        Get Allstacks labels available for Metrics V2 filtering.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics_v2/allstacks-labels/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of available Allstacks labels for filtering
        """
        endpoint = f"project/{project_id}/metrics_v2/allstacks-labels/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_user_tags(project_id: int) -> str:
        """
        Get user tags available for Metrics V2 filtering.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics_v2/user-tags/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of user tags for filtering
        """
        endpoint = f"project/{project_id}/metrics_v2/user-tags/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_item_props(
        project_id: int,
        item_types: Optional[str] = None,
        search: Optional[str] = None
    ) -> str:
        """
        Get available item properties with item type filtering and search for Metrics V2.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics_v2/item_props/
        
        Args:
            project_id: Project identifier
            item_types: Optional comma-separated item types filter
            search: Optional search term
        
        Returns:
            JSON array of available item properties
        """
        endpoint = f"project/{project_id}/metrics_v2/item_props/"
        
        params = {}
        if item_types:
            params["item_types[]"] = item_types.split(",")
        if search:
            params["search"] = search
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_project_metrics_list(project_id: int) -> str:
        """
        Get list of available metrics for a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics/
        
        Args:
            project_id: Project identifier
        
        Returns:
            JSON array of available metrics for the project
        """
        endpoint = f"project/{project_id}/metrics/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_insight_configs(
        project_id: int,
        metric_types: Optional[str] = None,
        insight_keys: Optional[str] = None
    ) -> str:
        """
        Get insight configurations that dictate which parameters will be passed to GMDTS.
        
        From OpenAPI: GET /api/v1/project/{project_id}/insights/configs
        
        Returns insight configurations that match both metric_types and insight_keys criteria 
        when both are provided.
        
        Args:
            project_id: Project identifier
            metric_types: Comma-separated list of metric types to filter (ActionsByCardType, Velocity, etc.)
            insight_keys: Comma-separated list of specific insight keys to filter
        
        Returns:
            JSON array of insight configurations with GMDTS parameters
        """
        endpoint = f"project/{project_id}/insights/configs"
        
        params = {}
        if metric_types:
            params["metric_types"] = metric_types
        if insight_keys:
            params["insight_keys"] = insight_keys
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_population_benchmark(
        metric_type: str,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC"
    ) -> str:
        """
        Get population-benchmark data for a metric type to compare against industry standards.
        
        From OpenAPI: GET /api/v1/population-benchmarks/metric/{metric_type}
        
        Supplies population-benchmark data for comparison with your team's metrics.
        
        Args:
            metric_type: The population metric type for which data is required
            start_date: Optional unix timestamp in milliseconds - only supply data after this date (defaults to epoch)
            end_date: Optional unix timestamp in milliseconds - only supply data before this date (defaults to current time)
            time_zone: A pytz compatible timezone string (defaults to UTC)
        
        Returns:
            JSON with data array containing aggregate_value fields and metadata
        """
        endpoint = f"population-benchmarks/metric/{metric_type}"
        
        params = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_company_metrics(org_id: int) -> str:
        """
        Get company-level metrics configuration.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/company_metrics/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with company metrics configuration
        """
        endpoint = f"organization/{org_id}/company_metrics/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_company_metrics(org_id: int, metrics_config: str) -> str:
        """
        Create company metrics configuration.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/company_metrics/
        
        Args:
            org_id: Organization identifier
            metrics_config: JSON string of metrics configuration
        
        Returns:
            Created metrics configuration
        """
        endpoint = f"organization/{org_id}/company_metrics/"
        
        try:
            config_dict = json.loads(metrics_config) if isinstance(metrics_config, str) else metrics_config
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in metrics_config parameter"})
        
        result = await api_client.request("POST", endpoint, data=config_dict)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_company_metrics(org_id: int, metric_ids: str) -> str:
        """
        Delete company metrics configuration.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/company_metrics/
        
        Args:
            org_id: Organization identifier
            metric_ids: Comma-separated metric IDs to delete
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/company_metrics/"
        
        data = {"metric_ids": metric_ids}
        result = await api_client.request("DELETE", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_company_available_metrics(org_id: int) -> str:
        """
        Get all available metrics that can be configured for the company.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/company_available_metrics/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON array of available metrics
        """
        endpoint = f"organization/{org_id}/company_available_metrics/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

