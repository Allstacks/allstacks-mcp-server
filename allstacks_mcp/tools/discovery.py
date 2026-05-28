"""API discovery tools and resources."""

import json
from typing import Any


TOOL_CATEGORIES: dict[str, tuple[str, ...]] = {
    "api_discovery": (
        "get_openapi_schema",
        "list_tool_categories",
    ),
    "metrics": (
        "list_metrics",
        "get_metric_details",
        "get_metric_info",
        "get_generated_metric",
        "get_gmdts_data",
        "get_project_metrics_v2_data",
        "get_org_metrics_v2_data",
        "get_metrics_v2_org_templates",
        "get_metrics_v2_individual_scorecard_templates",
        "get_metrics_v2_allstacks_labels",
        "get_metrics_v2_user_tags",
        "get_metrics_v2_item_props",
        "get_project_metrics_list",
        "get_insight_configs",
        "get_population_benchmark",
        "get_company_metrics",
        "create_company_metrics",
        "delete_company_metrics",
        "get_company_available_metrics",
    ),
    "allocations": (
        "get_org_metrics_v2_capitalization_data",
        "send_v2_capitalization_report",
        "get_capitalization_report_config",
        "save_capitalization_report_config",
        "list_generated_capitalization_reports",
        "get_generated_capitalization_report",
        "delete_generated_capitalization_report",
    ),
    "delivery": (
        "list_service_items",
        "get_service_item_property_keys",
        "get_service_items_for_metric",
        "get_parent_service_items",
        "get_service_item_types",
        "get_initial_service_items",
        "get_service_item_estimation_method",
        "set_service_item_estimation_method",
        "add_service_item_notes",
        "delete_service_item_notes",
        "get_item_props",
        "get_item_props_by_type",
        "get_configuration_options",
        "get_metrics_filter_sets",
        "create_metrics_filter_set",
        "get_metrics_filter_set",
        "update_metrics_filter_set",
        "delete_metrics_filter_set",
        "get_forecast_v3",
        "get_forecasting_config",
        "update_forecasting_config",
        "get_item_types_for_forecasting",
        "get_forecasting_history",
        "analyze_chart_data",
        "get_chart_analysis",
        "get_capacity_planning",
        "get_scenario_analysis",
        "list_work_bundles",
        "create_work_bundle",
        "get_work_bundle",
        "update_work_bundle",
        "delete_work_bundle",
        "add_items_to_work_bundle",
        "remove_items_from_work_bundle",
        "get_work_bundle_forecast",
        "get_work_bundle_metrics",
        "clone_work_bundle",
        "mark_work_bundle_complete",
        "reopen_work_bundle",
    ),
    "ai_impact": (
        "list_ai_reports",
        "create_ai_report",
        "get_ai_report",
        "delete_ai_report",
        "regenerate_ai_report",
        "query_code",
        "create_metric_with_ai",
        "ai_metric_builder",
        "analyze_patterns",
        "list_surveys",
        "get_survey_results",
        "get_ai_tool_usage",
        "get_ai_tool_impact",
        "dismiss_insight",
    ),
    "organizations_projects": (
        "list_organizations",
        "get_organization",
        "update_organization",
        "get_organization_settings",
        "update_organization_settings",
        "get_error_logs",
        "list_projects",
        "create_project",
        "get_project",
        "update_project",
        "get_project_configuration",
        "get_project_services",
        "list_project_service_users",
        "get_project_slots",
        "get_slot_configuration",
        "update_slot_configuration",
        "get_calendars",
        "create_calendar",
        "get_calendar",
        "update_calendar",
        "delete_calendar",
    ),
    "people_teams": (
        "get_employee_list",
        "get_employee_metrics",
        "get_employee_periods",
        "list_project_employees",
        "get_employee_cohort_data",
        "get_employee_metric_data",
        "get_employee_work_items",
        "get_employee_timeline",
        "get_employee_summary",
        "list_org_users",
        "get_org_user",
        "update_org_user",
        "get_manageable_roles",
        "list_org_user_invites",
        "create_user_invite",
        "get_user_invite",
        "update_user_invite",
        "delete_user_invite",
        "resend_user_invite",
        "list_project_users",
        "list_service_users_v2",
        "list_team_tags",
        "get_team_tag",
        "add_team_tag",
        "remove_team_tag",
        "list_personal_access_tokens",
        "create_personal_access_token",
        "get_personal_access_token",
        "delete_personal_access_token",
    ),
    "dashboards": (
        "list_org_dashboards",
        "create_org_dashboard",
        "get_dashboard_names",
        "get_org_dashboard",
        "update_org_dashboard",
        "delete_org_dashboard",
        "clear_dashboard_widgets",
        "clone_dashboard",
        "list_dashboard_widgets",
        "create_dashboard_widget",
        "get_dashboard_widget",
        "update_dashboard_widget",
        "delete_dashboard_widget",
        "list_shared_links",
        "create_shared_link",
        "get_shared_link",
        "update_shared_link",
        "delete_shared_link",
    ),
    "labels_tagging": (
        "list_labels",
        "create_label",
        "get_label",
        "update_label",
        "delete_label",
        "list_label_families",
        "create_label_family",
        "get_label_family",
        "update_label_family",
        "delete_label_family",
        "bulk_assign_labels",
        "bulk_remove_labels",
        "get_service_item_labels",
        "assign_service_item_label",
        "remove_service_item_label",
    ),
    "alerts_monitoring": (
        "list_alert_rules",
        "create_alert_rule",
        "get_alert_rule",
        "update_alert_rule",
        "delete_alert_rule",
        "get_alert_history",
        "acknowledge_alert",
        "resolve_alert",
        "get_notification_preferences",
        "update_notification_preferences",
        "list_alert_subscriptions",
        "subscribe_to_alert",
        "unsubscribe_from_alert",
    ),
    "risk_management": (
        "list_risk_definitions",
        "create_risk_definition",
        "get_risk_definition",
        "update_risk_definition",
        "delete_risk_definition",
        "list_project_risk_definitions",
        "get_service_item_risks",
        "acknowledge_risk",
        "resolve_risk",
        "get_risk_trends",
        "run_risk_assessment",
        "get_risk_summary",
    ),
}


def _json_response(value: Any) -> str:
    return json.dumps(value, indent=2)


async def _openapi_schema_json(api_client) -> str:
    schema = await api_client.get_openapi_schema()
    return _json_response(schema)


def register_tools(mcp, api_client):
    """Register API discovery tools and resources with the MCP server"""

    @mcp.tool()
    async def get_openapi_schema() -> str:
        """
        Fetch the published OpenAPI schema for the configured Allstacks API.

        The schema is retrieved at runtime using the same authentication as API
        tools, so it reflects the product API rather than a packaged snapshot.

        Returns:
            JSON OpenAPI document.
        """
        return await _openapi_schema_json(api_client)

    @mcp.tool()
    async def list_tool_categories() -> str:
        """
        List lightweight tool category mappings for API discovery.

        Returns:
            JSON object mapping product domains to MCP tool names.
        """
        return _json_response(TOOL_CATEGORIES)

    @mcp.resource(
        "allstacks://openapi",
        name="allstacks_openapi_schema",
        description="Published Allstacks OpenAPI schema fetched at runtime.",
        mime_type="application/json",
    )
    async def allstacks_openapi_schema() -> str:
        return await _openapi_schema_json(api_client)

    @mcp.resource(
        "schema://api",
        name="api_schema",
        description="Allstacks API schema alias for MCP clients that discover schema resources.",
        mime_type="application/json",
    )
    async def api_schema() -> str:
        return await _openapi_schema_json(api_client)
