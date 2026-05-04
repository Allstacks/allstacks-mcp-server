"""Metrics Data Retrieval Endpoints - Main multi-dimension time series API"""

import json
from typing import Optional

from ..metrics_v2_payload import build_metrics_v2_post_body


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
        time_zone: str = "UTC",
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

        params = {"aggregation": aggregation, "time_zone": time_zone}

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
    async def get_project_metrics_v2_data(
        project_id: int,
        config: str,
        get_count_only: bool = False,
        variables: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Fetch Metrics V2 data for a project (Work Item Table / Data Explorer).

        From API: POST /api/v1/project/{project_id}/metrics_v2/metrics

        **Request body:** ``{"config": {...}, "get_count_only": false, "variables": {}}``. Pass
        ``config`` as JSON of either the **inner** config object or the full envelope (keys only
        ``config``, ``get_count_only``, ``variables``). Optional query ``use_cache`` (default true).

        **Response:** JSON with ``results``, ``ignored_filters``, ``next``, ``previous``. Count-only:
        ``{"count", "ignored_filters"}``. Cached responses may include ``from_cache``. If ``config.as_csv``
        is true, CSV is returned as ``raw_body`` by this client.

        After ``ai_metric_builder``, pass the inner config as this ``config`` string.

        Args:
            project_id: Project identifier
            config: JSON string — inner config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string of variables for ``{{var}}`` substitution
            use_cache: Query param; false bypasses response cache

        Returns:
            JSON string, or ``{"raw_body": "..."}`` for CSV
        """
        endpoint = f"project/{project_id}/metrics_v2/metrics"
        params = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        result = await api_client.request(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_org_metrics_v2_data(
        org_id: int,
        config: str,
        get_count_only: bool = False,
        variables: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Fetch Metrics V2 data for an organization (cross-project scope).

        From API: POST /api/v1/organization/{org_id}/metrics_v2/metrics

        Same request wrapper as ``get_project_metrics_v2_data``.

        Args:
            org_id: Organization identifier
            config: JSON string — inner config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string of variables dict
            use_cache: Query param; false bypasses cache

        Returns:
            JSON string, or ``{"raw_body": "..."}`` for CSV
        """
        endpoint = f"organization/{org_id}/metrics_v2/metrics"
        params = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        result = await api_client.request(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_org_metrics_v2_capitalization_data(
        org_id: int,
        config: str,
        get_count_only: bool = False,
        variables: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Fetch Metrics V2 capitalization query data for an organization (SOC 1 certified engine).

        From API: POST /api/v1/organization/{org_id}/metrics_v2_capitalization/metrics

        Same request wrapper as ``get_org_metrics_v2_data``. Use to preview or validate capitalization
        metric configs; generated CSV reports use ``send_v2_capitalization_report``.

        Args:
            org_id: Organization identifier
            config: JSON string — inner capitalization config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string of variables dict
            use_cache: Query param; false bypasses cache

        Returns:
            JSON string, or ``{"raw_body": "..."}`` for CSV
        """
        endpoint = f"organization/{org_id}/metrics_v2_capitalization/metrics"
        params = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        result = await api_client.request(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_org_templates(org_id: int, tag: str) -> str:
        """
        List predefined Metrics V2 configuration templates for an organization.

        From API: GET /api/v1/organization/{org_id}/metrics_v2/templates/?tag=<tag>

        Args:
            org_id: Organization identifier
            tag: Template tag (e.g. devex, contributors, dora, individual_scorecard)

        Returns:
            JSON with template names and embedded config objects
        """
        endpoint = f"organization/{org_id}/metrics_v2/templates/"
        params = {"tag": tag}
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_individual_scorecard_templates(
        org_id: int, tag: str
    ) -> str:
        """
        List individual scorecard Metrics V2 templates for an organization.

        From API: GET /api/v1/organization/{org_id}/metrics_v2/individual-scorecard-templates/?tag=<tag>

        Args:
            org_id: Organization identifier
            tag: Template tag (required)

        Returns:
            JSON with templates and embedded configs
        """
        endpoint = f"organization/{org_id}/metrics_v2/individual-scorecard-templates/"
        params = {"tag": tag}
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_allstacks_labels(
        project_id: int,
        search: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> str:
        """
        Get Allstacks labels available for Metrics V2 filtering.

        From API: GET /api/v1/project/{project_id}/metrics_v2/allstacks-labels/

        Args:
            project_id: Project identifier
            search: Optional search term
            limit: Optional max results

        Returns:
            JSON object (e.g. ``allstacks_labels`` and related fields)
        """
        endpoint = f"project/{project_id}/metrics_v2/allstacks-labels/"
        params = {}
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        result = await api_client.request("GET", endpoint, params=params or None)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_user_tags(
        project_id: int,
        search: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> str:
        """
        Get user tags available for Metrics V2 filtering.

        From API: GET /api/v1/project/{project_id}/metrics_v2/user-tags/

        Args:
            project_id: Project identifier
            search: Optional search term
            limit: Optional max results

        Returns:
            JSON object (e.g. ``user_tags`` and related fields)
        """
        endpoint = f"project/{project_id}/metrics_v2/user-tags/"
        params = {}
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        result = await api_client.request("GET", endpoint, params=params or None)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_v2_item_props(
        project_id: int, item_types: Optional[str] = None, search: Optional[str] = None
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
        insight_keys: Optional[str] = None,
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
        time_zone: str = "UTC",
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
            config_dict = (
                json.loads(metrics_config)
                if isinstance(metrics_config, str)
                else metrics_config
            )
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
