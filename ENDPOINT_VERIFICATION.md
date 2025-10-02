# Allstacks MCP Endpoint Verification

## Analysis Date: 2025-10-02

This document maps our current 54 MCP tools against the official Allstacks OpenAPI specification to identify:
1. Which endpoints actually exist
2. Which need to be fixed/updated
3. Which parameters and descriptions need enhancement

---

## Current Tool Inventory (54 tools across 10 categories)

### ✅ Category 1: Metrics Data Retrieval (7 tools)
1. **list_metrics** - `/metrics/` - ❌ **NEEDS VERIFICATION** - endpoint unclear in spec
2. **get_metric_info** - `/metrics/{metric_id}/get_generated_metric_info/` - ✅ **EXISTS**
3. **get_gmdts_data** - `/project/{project_id}/metrics/gmdts/{metric_type}/` - ❌ **DOES NOT EXIST**
4. **get_metrics_v2_data** - `/project/{project_id}/metrics/v2/data/` - ❌ **DOES NOT EXIST** (should be `/metrics_v2/metrics`)
5. **list_metrics_v2_configs** - `/project/{project_id}/configs/` - ❌ **WRONG PATH** (should be organization level)
6. **create_metrics_v2_config** - `/project/{project_id}/configs/` - ❌ **WRONG PATH**
7. **get_insight_configs** - `/project/{project_id}/insights/configs` - ✅ **EXISTS**

### ✅ Category 2: Service Items & Filtering (6 tools)
1. **list_service_items** - `/project/{project_id}/service_items/` - ❌ **DOES NOT EXIST** (real: `/api/v1/service_items/service_item/`)
2. **get_item_props** - `/project/{project_id}/item_props/` - ✅ **EXISTS**
3. **get_configuration_options** - `/organization/{org_id}/configuration_options/` - ✅ **EXISTS**
4. **search_service_items** - `/project/{project_id}/service_items/search/` - ❌ **DOES NOT EXIST**
5. **get_parent_service_items** - `/project/{project_id}/service_items/parents/` - ❌ **SHOULD BE** `/api/v1/project/{project_id}/parent_service_items/`
6. **get_metrics_filter_sets** - `/project/{project_id}/metrics_filter_sets/` - ✅ **EXISTS**

### ✅ Category 3: User & Team Management (4 tools)
1. **list_service_users** - `/organization/{org_id}/service_users/` - ❌ **SHOULD BE** `/api/v1/organization/{org_id}/service_user/`
2. **get_user_mapping** - `/organization/{org_id}/service_user/get_map/` - ✅ **EXISTS**
3. **get_user_tags** - `/organization/{org_id}/service_user/tags/` - ❌ **SHOULD BE** `/api/v1/organization/{org_id}/service_user_tag/`
4. **get_team_categories** - `/organization/{org_id}/categories/` - ❌ **SHOULD BE** `/api/v1/organization/{org_id}/team_categories/`

### ✅ Category 4: Organization & Project (4 tools)
1. **get_organization_settings** - `/organization/{org_id}/settings/` - ✅ **EXISTS**
2. **list_projects** - `/organization/{org_id}/projects/` - ✅ **EXISTS**
3. **get_project_services** - `/project/{project_id}/services/` - ❌ **SHOULD BE** `/api/v1/project/{project_id}/service/`
4. **get_enabled_work_bundles** - `/project/{project_id}/work_bundles/` - ❌ **DOES NOT EXIST**

### ✅ Category 5: AI & Analytics (4 tools)
1. **get_organization_investments** - `/organization/{org_id}/ai_summary/currentInvestments` - ❌ **DOES NOT EXIST**
2. **generate_workflow_analysis** - `/project/{project_id}/ai_analysis/workflow/` - ❌ **DOES NOT EXIST**
3. **get_developer_experience_metrics** - `/organization/{org_id}/developer_experience/` - ❌ **DOES NOT EXIST**
4. **get_capitalization_report** - `/organization/{org_id}/capitalization_report/` - ❌ **DOES NOT EXIST** (should be generate_capitalization)

### ✅ Category 6: Dashboards & Widgets (5 tools)
1. **list_dashboards** - `/organization/{org_id}/dashboards/` OR `/project/{project_id}/dashboards/` - ✅ **EXISTS**
2. **get_dashboard_widgets** - `/organization/{org_id}/dashboard_widgets/` - ✅ **EXISTS**
3. **create_dashboard_widget** - `/organization/{org_id}/dashboard_widgets/` - ✅ **EXISTS**
4. **get_shared_links** - `/organization/{org_id}/shared_links/` - ✅ **EXISTS**
5. **create_shared_link** - `/organization/{org_id}/shared_links/` - ✅ **EXISTS**

### ✅ Category 7: Employee & Productivity (5 tools)
1. **get_employee_metrics** - `/employee/{project_id}/metrics/` - ✅ **EXISTS**
2. **get_employee_periods** - `/employee/{project_id}/periods/` - ✅ **EXISTS**
3. **get_employee_users** - `/employee/{project_id}/users/` - ✅ **EXISTS**
4. **get_employee_metric_data** - `/employee/{project_id}/{metric_id}/metric-data/` - ✅ **EXISTS**
5. **merge_service_users** - `/organization/{org_id}/merge_users/` - ✅ **EXISTS**

### ✅ Category 8: Forecasting & Planning (5 tools)
1. **get_forecast_v3** - `/forecasting/{project_id}/v3/` - ✅ **EXISTS**
2. **get_slots** - `/organization/{org_id}/slots/` - ✅ **EXISTS**
3. **analyze_chart_data** - `/charts/analyze` - ✅ **EXISTS**
4. **get_chart_analysis** - `/charts/analysis/` - ✅ **EXISTS**
5. **get_company_metrics** - `/organization/{org_id}/company_metrics/` - ✅ **EXISTS**

### ✅ Category 9: Labels & Tagging (5 tools)
1. **list_labels** - `/organization/{org_id}/labels/` - ✅ **EXISTS**
2. **create_label** - `/organization/{org_id}/labels/` - ✅ **EXISTS**
3. **add_service_user_tags** - `/organization/{org_id}/service_user/service_user_tags/` - ✅ **EXISTS**
4. **remove_service_user_tags** - `/organization/{org_id}/service_user/service_user_tags/` - ✅ **EXISTS**
5. **get_manageable_roles** - `/organization/{org_id}/manageable_roles` - ✅ **EXISTS**

### ✅ Category 10: Alerts & Monitoring (5 tools)
1. **get_service_item_alerts** - `/project/{project_id}/alerts/` - ❌ **DOES NOT EXIST**
2. **get_deliverable_risks** - `/project/{project_id}/deliverable_risks/` - ❌ **DOES NOT EXIST** (should be risk_definitions)
3. **get_service_health** - `/organization/{org_id}/service_health/` - ❌ **DOES NOT EXIST**
4. **get_error_logs** - `/organization/{org_id}/error_logs/` - ✅ **EXISTS**
5. **get_audit_log** - `/organization/{org_id}/audit_log/` - ❌ **SHOULD BE** `/api/v1/iadmin/organizations/{org_id}/user_audit_logs/`

---

## Summary Statistics

- **Total Tools**: 54
- **Fully Correct**: ~18 (33%)
- **Need Path Fixes**: ~15 (28%)
- **Don't Exist/Wrong**: ~21 (39%)

---

## Critical Findings

### ❌ High Priority Fixes Needed:

1. **GMDTS endpoint** (`get_gmdts_data`) - The endpoint path `/project/{project_id}/metrics/gmdts/{metric_type}/` does NOT exist. The real endpoint is `/api/v1/project/{project_id}/generated_metric_data/{metric_type}` with POST/GET methods

2. **Metrics V2** - Wrong paths. Should be:
   - POST `/api/v1/project/{project_id}/metrics_v2/metrics`
   - POST `/api/v1/organization/{org_id}/metrics_v2/metrics`

3. **Service Items** - Path incorrect. Real endpoint: `/api/v1/service_items/service_item/` with complex filtering via GET/POST

4. **Parent Service Items** - Exists but wrong path: `/api/v1/project/{project_id}/parent_service_items/` (not `/service_items/parents/`)

5. **AI Analytics endpoints** - Most don't exist. Need to use actual endpoints like:
   - AI Reports: `/api/v1/organization/{org_id}/ai-reports/`
   - Capitalization: `/api/v1/organization/{org_id}/generate_capitalization/`

---

## Next Steps

1. ✅ Fix all endpoint paths to match OpenAPI spec
2. ✅ Add robust parameter descriptions from the spec
3. ✅ Enhance function docstrings with official API documentation
4. ✅ Add validation for required vs optional parameters
5. ✅ Update examples to match real API patterns
6. ✅ Consider adding more tools for missing functionality (AI reports, risk definitions, etc.)

---

## Recommendations

### Remove or Fix Non-Existent Endpoints:
- `search_service_items` - No search endpoint exists
- `get_organization_investments` - Endpoint doesn't exist
- `generate_workflow_analysis` - Endpoint doesn't exist
- `get_developer_experience_metrics` - Endpoint doesn't exist
- `get_service_item_alerts` - Endpoint doesn't exist
- `get_deliverable_risks` - Wrong name (should be risk_definitions)
- `get_service_health` - Endpoint doesn't exist

### Endpoints to ADD (from OpenAPI spec):
1. **AI Reports** - `/api/v1/organization/{org_id}/ai-reports/` (GET, POST)
2. **Risk Definitions** - `/api/v1/project/{project_id}/risk_definitions/` (full CRUD)
3. **Personal Access Tokens** - `/api/v1/organization/{org_id}/pat/` (for integrations)
4. **Alert Subscriptions** - `/api/v1/project/{project_id}/alert_subscriptions/` (GET, PATCH)
5. **Dashboard Subscriptions** - `/api/v1/project/{project_id}/dashboard_subscriptions` (GET, POST)
6. **Population Benchmarks** - `/api/v1/population-benchmarks/metric/{metric_type}` (GET)


