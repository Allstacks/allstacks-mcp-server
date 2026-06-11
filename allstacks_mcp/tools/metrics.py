"""Metrics V2 data retrieval endpoints."""

import json
from typing import Optional

from .._json_input import JsonInput
from ..metrics_v2_payload import build_metrics_v2_post_body


def register_tools(mcp, api_client):
    """Register all metrics-related tools with the MCP server"""

    @mcp.tool()
    async def get_project_metrics_v2_data(
        project_id: int,
        config: JsonInput,
        get_count_only: bool = False,
        variables: Optional[JsonInput] = None,
        use_cache: bool = True,
        response_format: str = "json",
    ) -> str:
        """
        Fetch Metrics V2 data for a project (Work Item Table / Data Explorer).

        From API: POST /api/v1/project/{project_id}/metrics_v2/metrics

        **Request body:** ``{"config": {...}, "get_count_only": false, "variables": {}}``. Pass
        ``config`` as the **inner** config object or the full envelope (keys only ``config``,
        ``get_count_only``, ``variables``). Either form may be a JSON string or the already-parsed
        object. Optional query ``use_cache`` (default true).

        **Response:** JSON with ``results``, ``ignored_filters``, ``next``, ``previous``. Count-only:
        ``{"count", "ignored_filters"}``. Cached responses may include ``from_cache``. If ``config.as_csv``
        is true, CSV is returned as ``raw_body`` by this client.

        After ``ai_metric_builder``, pass the inner config as this ``config``.

        Args:
            project_id: Project identifier
            config: JSON string or object — inner config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string or object of variables for ``{{var}}`` substitution
            use_cache: Query param; false bypasses response cache
            response_format: Output encoding: json (default) or toon

        Returns:
            Encoded response string, or ``{"raw_body": "..."}`` JSON for CSV
        """
        endpoint = f"project/{project_id}/metrics_v2/metrics"
        params: dict[str, object] = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        return await api_client.request_text(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
            response_format=response_format,
        )

    @mcp.tool()
    async def get_org_metrics_v2_data(
        org_id: int,
        config: JsonInput,
        get_count_only: bool = False,
        variables: Optional[JsonInput] = None,
        use_cache: bool = True,
        response_format: str = "json",
    ) -> str:
        """
        Fetch Metrics V2 data for an organization (cross-project scope).

        From API: POST /api/v1/organization/{org_id}/metrics_v2/metrics

        Same request wrapper as ``get_project_metrics_v2_data``.

        Args:
            org_id: Organization identifier
            config: JSON string or object — inner config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string or object of variables dict
            use_cache: Query param; false bypasses cache
            response_format: Output encoding: json (default) or toon

        Returns:
            Encoded response string, or ``{"raw_body": "..."}`` JSON for CSV
        """
        endpoint = f"organization/{org_id}/metrics_v2/metrics"
        params: dict[str, object] = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        return await api_client.request_text(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
            response_format=response_format,
        )

    @mcp.tool()
    async def get_org_metrics_v2_capitalization_data(
        org_id: int,
        config: JsonInput,
        get_count_only: bool = False,
        variables: Optional[JsonInput] = None,
        use_cache: bool = True,
        response_format: str = "json",
    ) -> str:
        """
        Fetch Metrics V2 capitalization query data for an organization (SOC 1 certified engine).

        From API: POST /api/v1/organization/{org_id}/metrics_v2_capitalization/metrics

        Same request wrapper as ``get_org_metrics_v2_data``. Use to preview or validate capitalization
        metric configs; generated CSV reports use ``send_v2_capitalization_report``.

        Args:
            org_id: Organization identifier
            config: JSON string or object — inner capitalization config or full envelope
            get_count_only: If true, request only row count
            variables: Optional JSON string or object of variables dict
            use_cache: Query param; false bypasses cache
            response_format: Output encoding: json (default) or toon

        Returns:
            Encoded response string, or ``{"raw_body": "..."}`` JSON for CSV
        """
        endpoint = f"organization/{org_id}/metrics_v2_capitalization/metrics"
        params: dict[str, object] = {"use_cache": str(use_cache).lower()}

        try:
            body = build_metrics_v2_post_body(config, get_count_only, variables)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        inner_config = body.get("config")
        expect_json = not (
            isinstance(inner_config, dict) and bool(inner_config.get("as_csv"))
        )

        return await api_client.request_text(
            "POST",
            endpoint,
            params=params,
            data=body,
            timeout_seconds=120.0 if not expect_json else 60.0,
            expect_json=expect_json,
            response_format=response_format,
        )

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
        params: dict[str, object] = {"tag": tag}
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
        params: dict[str, object] = {"tag": tag}
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
        params: dict[str, object] = {}
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
        params: dict[str, object] = {}
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

        params: dict[str, object] = {}
        if item_types:
            params["item_types[]"] = item_types.split(",")
        if search:
            params["search"] = search

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)
