"""Service Items & Work Items Endpoints - Core data retrieval"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all service items-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_service_items(
        item_type: Optional[str] = None,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List service items (work items, commits, pull requests, etc.) with comprehensive filtering.
        
        From OpenAPI: GET/POST /api/v1/service_items/service_item/
        
        Retrieve and manage service items with filtering, pagination, and risk assessment capabilities.
        Supports both GET and POST methods (POST for complex filters that exceed URL length limits).
        
        Args:
            item_type: Optional filter by service item type (CARD, COMMIT, PULL_REQUEST, etc.)
            ordering: Optional ordering field
            limit: Number of results to return per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of service items with metadata
        """
        endpoint = "service_items/service_item/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if item_type:
            params["item_type"] = item_type
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_item_property_keys(item_type: str) -> str:
        """
        Get available property keys for a specific service item type for building filters.
        
        From OpenAPI: GET /api/v1/service_items/service_item/get_property_keys/
        
        Args:
            item_type: Service item type (CARD, COMMIT, PULL_REQUEST, etc.) - MANDATORY
        
        Returns:
            JSON array of available property keys for the item type
        """
        endpoint = "service_items/service_item/get_property_keys/"
        
        params = {"item_type": item_type}
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_items_for_metric(
        metric: str,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        Get service items for use on metric pages with metric-specific context.
        
        From OpenAPI: GET/POST /api/v1/service_items/{metric}/
        
        Args:
            metric: Metric type identifier
            ordering: Optional ordering field
            limit: Number of results per page
            offset: Pagination offset
        
        Returns:
            JSON array of service items relevant to the metric
        """
        endpoint = f"service_items/{metric}/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_parent_service_items(
        project_id: int,
        parent_service_item_ids: Optional[str] = None,
        parent_service_item_types: Optional[str] = None,
        parent_service_item_groups: Optional[str] = None,
        service_id: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        time_zone: str = "UTC",
        parent_service_item_name: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: str = "desc",
        pin_filter: Optional[int] = None,
        estimation_method_override: Optional[str] = None,
        fields: Optional[str] = None
    ) -> str:
        """
        Return parent service items (epics, milestones, features) for a project with detailed metadata.
        
        From OpenAPI: GET/POST /api/v1/project/{project_id}/parent_service_items/
        
        Returns parent service items with optional fields like forecasting data, risk counts, velocity trends, etc.
        
        Args:
            project_id: Project identifier (required)
            parent_service_item_ids: Comma-separated list of parent service item IDs to return
            parent_service_item_types: Comma-separated types of parent service item to return
            parent_service_item_groups: Comma-separated groups of parent service item to return
            service_id: Filter by service ID
            offset: Pagination offset
            limit: Pagination limit
            time_zone: Timezone for date offsets in forecast and scope data (default: UTC)
            parent_service_item_name: Search filter for partial matches on name and human readable ID
            order_by: Order by field (id, name) - defaults to id, service, key, group, start date, end date, item id
            order_direction: Order direction - 'asc' or 'desc' (default: desc)
            pin_filter: Filter for pinned (1) or unpinned (0) milestones
            estimation_method_override: Estimation method (Count, Story Points, Time Estimate (Hours))
            fields: Comma-separated fields to return (available_estimation_methods, child_milestones, 
                    completed_work, completion_date, delivery_slippage, item_estimation_method, 
                    first_work_date, forecast_time_series, forecasted_completion_date, 
                    item_human_readable_id, last_forecasted_on, last_work_date, pinned_to_project, 
                    risk_count, risks, scope_creep_percentage, scope_time_series, scope_trend, 
                    service_item_count, state, team_priority, total_work, unestimated_item_ids, 
                    unestimated_work, url, velocity, notes, velocity_time_series, velocity_trend)
        
        Returns:
            JSON with service_item_count and list of parent service items with requested fields
        """
        endpoint = f"project/{project_id}/parent_service_items/"
        
        params = {"time_zone": time_zone, "order_direction": order_direction}
        
        # Handle array parameters - API expects fields[]=value format
        if parent_service_item_ids:
            params["parent_service_item_ids[]"] = parent_service_item_ids.split(",")
        if parent_service_item_types:
            params["parent_service_item_types[]"] = parent_service_item_types.split(",")
        if parent_service_item_groups:
            params["parent_service_item_groups[]"] = parent_service_item_groups.split(",")
        if service_id:
            params["service_id"] = service_id
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if parent_service_item_name:
            params["parent_service_item_name"] = parent_service_item_name
        if order_by:
            params["order_by"] = order_by
        if pin_filter is not None:
            params["pin_filter"] = pin_filter
        if estimation_method_override:
            params["estimation_method_override"] = estimation_method_override
        if fields:
            # Convert comma-separated fields to array format
            params["fields[]"] = fields.split(",")
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_item_types(project_id: int, service_item_types: Optional[str] = None) -> str:
        """
        Get an object of all container service item types for a project with their counts.
        
        From OpenAPI: GET /api/v1/project/{project_id}/service_items/types/
        
        Args:
            project_id: Project identifier
            service_item_types: Optional comma-separated list of service item types to return
        
        Returns:
            JSON object with service item types and their counts
        """
        endpoint = f"project/{project_id}/service_items/types/"
        
        params = {}
        if service_item_types:
            params["service_item_types[]"] = service_item_types.split(",")
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_initial_service_items(
        project_id: int,
        service_item_limit: int = 3,
        group_limit: Optional[int] = None,
        group_offset: int = 0
    ) -> str:
        """
        Return recent service items for a project by type-group-service combination.
        
        From OpenAPI: GET /api/v1/project/{project_id}/service_items/initial/
        
        Args:
            project_id: Project identifier
            service_item_limit: Number of items to return for each combination (default: 3)
            group_limit: Optional number of groups to return
            group_offset: Offset for groups (default: 0)
        
        Returns:
            JSON with grouped service items
        """
        endpoint = f"project/{project_id}/service_items/initial/"
        
        params = {
            "service_item_limit": service_item_limit,
            "group_offset": group_offset
        }
        
        if group_limit is not None:
            params["group_limit"] = group_limit
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_item_estimation_method(
        project_id: int,
        service_item_ids: Optional[str] = None
    ) -> str:
        """
        Return service item estimation methods.
        
        From OpenAPI: GET /api/v1/project/{project_id}/service_items/estimation_method/
        
        Args:
            project_id: Project identifier
            service_item_ids: Optional comma-separated list of service item IDs to filter
        
        Returns:
            JSON with estimation methods for service items
        """
        endpoint = f"project/{project_id}/service_items/estimation_method/"
        
        params = {}
        if service_item_ids:
            params["service_item_ids[]"] = service_item_ids.split(",")
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def set_service_item_estimation_method(
        project_id: int,
        service_item_ids: str,
        estimation_method: str
    ) -> str:
        """
        Set service item estimation method for specific items.
        
        From OpenAPI: POST /api/v1/project/{project_id}/service_items/estimation_method/
        
        Args:
            project_id: Project identifier
            service_item_ids: Comma-separated list of service items IDs (MANDATORY)
            estimation_method: Estimation method to set (MANDATORY)
        
        Returns:
            JSON confirmation of estimation method update
        """
        endpoint = f"project/{project_id}/service_items/estimation_method/"
        
        data = {
            "service_item_ids": service_item_ids,
            "estimation_method": estimation_method
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def add_service_item_notes(
        project_id: int,
        milestone_item_id: int,
        notes: str
    ) -> str:
        """
        Add notes to a service item (milestone).
        
        From OpenAPI: POST /api/v1/project/{project_id}/service_item/{milestone_item_id}/notes
        
        Args:
            project_id: Project identifier
            milestone_item_id: Service item/milestone ID
            notes: Notes text to add
        
        Returns:
            JSON confirmation
        """
        endpoint = f"project/{project_id}/service_item/{milestone_item_id}/notes"
        
        data = {"notes": notes}
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_service_item_notes(project_id: int, milestone_item_id: int) -> str:
        """
        Delete notes from a service item (milestone).
        
        From OpenAPI: DELETE /api/v1/project/{project_id}/service_item/{milestone_item_id}/notes
        
        Args:
            project_id: Project identifier
            milestone_item_id: Service item/milestone ID
        
        Returns:
            JSON confirmation
        """
        endpoint = f"project/{project_id}/service_item/{milestone_item_id}/notes"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_item_props(
        project_id: int,
        item_types: Optional[str] = None,
        data_types: Optional[str] = None,
        many: bool = False,
        versioned: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        Get available properties for service items for advanced filtering.
        
        From OpenAPI: GET /api/v1/project/{project_id}/item_props/
        
        Args:
            project_id: Project identifier
            item_types: Optional comma-separated item types to filter
            data_types: Optional comma-separated prop data types
            many: Include many-valued properties (default: False)
            versioned: Include versioned properties (default: False)
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of available properties with metadata
        """
        endpoint = f"project/{project_id}/item_props/"
        
        params = {
            "limit": limit,
            "offset": offset,
            "many": many,
            "versioned": versioned
        }
        
        if item_types:
            params["item_types[]"] = item_types.split(",")
        if data_types:
            params["data_types[]"] = data_types.split(",")
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_item_props_by_type(project_id: int, item_type: str) -> str:
        """
        Get properties for a specific item type.
        
        From OpenAPI: GET /api/v1/project/{project_id}/item_props/{item_type}/
        
        Args:
            project_id: Project identifier
            item_type: Specific item type to get properties for
        
        Returns:
            JSON with properties for the specified item type
        """
        endpoint = f"project/{project_id}/item_props/{item_type}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_configuration_options(
        org_id: int,
        metric: Optional[str] = None,
        item_types: Optional[str] = None,
        data_types: Optional[str] = None
    ) -> str:
        """
        Get configuration options for metrics and filtering.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/configuration_options/
        
        Args:
            org_id: Organization identifier
            metric: Optional metric enum value (ActionsByCardType, Velocity, etc.)
            item_types: Optional comma-separated item types (CARD, COMMIT, PULL_REQUEST, etc.)
            data_types: Optional comma-separated data types to filter results (boolean, date, datetime, duration, number, string, user, work_bundle, etc.)
        
        Returns:
            JSON with available configuration options including property groups with data types, grouping options, axis settings
        """
        endpoint = f"organization/{org_id}/configuration_options/"
        
        params = {}
        if metric:
            params["metric"] = metric
        if item_types:
            params["item_types[]"] = item_types.split(",")
        if data_types:
            params["data_types[]"] = data_types.split(",")
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_filter_sets(
        project_id: int,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> str:
        """
        Get saved filter sets for metrics.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics_filter_sets/
        
        Args:
            project_id: Project identifier
            search: Optional search term
            limit: Maximum results (default: 20)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of filter sets
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if search:
            params["search"] = search
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_metrics_filter_set(
        project_id: int,
        name: Optional[str] = None,
        filter_set: str = "{}"
    ) -> str:
        """
        Create a new metrics filter set.
        
        From OpenAPI: POST /api/v1/project/{project_id}/metrics_filter_sets/
        
        Args:
            project_id: Project identifier
            name: Optional name for the filter set
            filter_set: JSON string of filter configuration (required)
        
        Returns:
            Created filter set with ID
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/"
        
        try:
            filter_dict = json.loads(filter_set) if isinstance(filter_set, str) else filter_set
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in filter_set parameter"})
        
        data = {
            "filter_set": filter_dict
        }
        if name:
            data["name"] = name
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_metrics_filter_set(project_id: int, filter_set_id: int) -> str:
        """
        Get a specific metrics filter set.
        
        From OpenAPI: GET /api/v1/project/{project_id}/metrics_filter_sets/{id}/
        
        Args:
            project_id: Project identifier
            filter_set_id: Filter set ID
        
        Returns:
            JSON with filter set details
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/{filter_set_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_metrics_filter_set(
        project_id: int,
        filter_set_id: int,
        name: Optional[str] = None,
        filter_set: Optional[str] = None
    ) -> str:
        """
        Update a metrics filter set.
        
        From OpenAPI: PUT/PATCH /api/v1/project/{project_id}/metrics_filter_sets/{id}/
        
        Args:
            project_id: Project identifier
            filter_set_id: Filter set ID
            name: Optional new name
            filter_set: Optional JSON string of updated filter configuration
        
        Returns:
            Updated filter set
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/{filter_set_id}/"
        
        data = {}
        if name:
            data["name"] = name
        if filter_set:
            try:
                data["filter_set"] = json.loads(filter_set) if isinstance(filter_set, str) else filter_set
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON in filter_set parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_metrics_filter_set(project_id: int, filter_set_id: int) -> str:
        """
        Delete a metrics filter set.
        
        From OpenAPI: DELETE /api/v1/project/{project_id}/metrics_filter_sets/{id}/
        
        Args:
            project_id: Project identifier
            filter_set_id: Filter set ID
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"project/{project_id}/metrics_filter_sets/{filter_set_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
