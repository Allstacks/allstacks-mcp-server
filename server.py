import argparse
import json
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Allstacks-MCP")

# Global variables for configuration
ALLSTACKS_API_TOKEN = ""
ALLSTACKS_BASE_URL = "https://api.allstacks.com/api/v1/"

class AllstacksAPIClient:
    """HTTP client for Allstacks API communication"""
    
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make an async HTTP request to the Allstacks API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": f"HTTP error: {e.response.text}"
                }
            except Exception as e:
                return {
                    "error": True,
                    "message": f"Request failed: {str(e)}"
                }

# Initialize the client (will be set in __main__)
api_client = None

# ==========================================
# 1. METRICS DATA RETRIEVAL ENDPOINTS (7)
# ==========================================

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


# ==========================================
# 2. SERVICE ITEMS & FILTERING ENDPOINTS (6)
# ==========================================

@mcp.tool()
async def list_service_items(
    project_id: int,
    item_types: Optional[str] = None,
    service_ids: Optional[str] = None,
    assignee_ids: Optional[str] = None,
    parent_item_ids: Optional[str] = None,
    updated_after: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> str:
    """
    List service items with comprehensive filtering.
    
    Args:
        project_id: Project identifier
        item_types: Comma-separated types (CARD,COMMIT,PULL_REQUEST)
        service_ids: Comma-separated service IDs
        assignee_ids: Comma-separated assignee user IDs
        parent_item_ids: Comma-separated parent item IDs
        updated_after: ISO date for items updated after
        status: Item status filter
        limit: Maximum items to return
        offset: Pagination offset
    
    Returns:
        JSON array of service items
    """
    endpoint = f"project/{project_id}/service_items/"
    
    params = {
        "limit": limit,
        "offset": offset
    }
    
    if item_types:
        params["item_types"] = item_types
    if service_ids:
        params["service_ids"] = service_ids
    if assignee_ids:
        params["assignee_ids"] = assignee_ids
    if parent_item_ids:
        params["parent_item_ids"] = parent_item_ids
    if updated_after:
        params["updated_after"] = updated_after
    if status:
        params["status"] = status
    
    result = await api_client.request("GET", endpoint, params=params)
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
    Get available properties for service items (for filtering).
    
    Args:
        project_id: Project identifier
        item_types: Comma-separated item types to filter
        data_types: Comma-separated prop data types
        many: Include many-valued properties
        versioned: Include versioned properties
        limit: Maximum results
        offset: Pagination offset
    
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
        params["item_types"] = item_types
    if data_types:
        params["data_types"] = data_types
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_configuration_options(
    org_id: int,
    metric: Optional[int] = None,
    item_types: Optional[str] = None
) -> str:
    """
    Get configuration options for metrics and filtering.
    
    Args:
        org_id: Organization identifier
        metric: Metric ID for metric-specific options
        item_types: Comma-separated item types
    
    Returns:
        JSON with available configuration options
    """
    endpoint = f"organization/{org_id}/configuration_options/"
    
    params = {}
    if metric:
        params["metric"] = metric
    if item_types:
        params["item_types"] = item_types
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def search_service_items(
    project_id: int,
    query: str,
    item_types: Optional[str] = None,
    limit: int = 50
) -> str:
    """
    Full-text search across service items.
    
    Args:
        project_id: Project identifier
        query: Search query string
        item_types: Optional comma-separated item types to search
        limit: Maximum results
    
    Returns:
        JSON array of matching service items
    """
    endpoint = f"project/{project_id}/service_items/search/"
    
    params = {
        "q": query,
        "limit": limit
    }
    
    if item_types:
        params["item_types"] = item_types
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_parent_service_items(
    project_id: int,
    service_item_ids: str,
    depth: int = 1
) -> str:
    """
    Get hierarchical parent items using upward link traversal.
    
    Args:
        project_id: Project identifier
        service_item_ids: Comma-separated service item IDs
        depth: Traversal depth (1-5)
    
    Returns:
        JSON with parent hierarchy
    """
    endpoint = f"project/{project_id}/service_items/parents/"
    
    params = {
        "service_item_ids": service_item_ids,
        "depth": min(max(depth, 1), 5)  # Limit depth between 1-5
    }
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_metrics_filter_sets(
    project_id: int,
    metric_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> str:
    """
    Get saved filter sets for metrics.
    
    Args:
        project_id: Project identifier
        metric_type: Optional metric type to filter
        limit: Maximum results
        offset: Pagination offset
    
    Returns:
        JSON array of filter sets
    """
    endpoint = f"project/{project_id}/metrics_filter_sets/"
    
    params = {
        "limit": limit,
        "offset": offset
    }
    
    if metric_type:
        params["metric_type"] = metric_type
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


# ==========================================
# 3. USER & TEAM MANAGEMENT ENDPOINTS (4)
# ==========================================

@mcp.tool()
async def list_service_users(
    org_id: int,
    project_id: Optional[int] = None,
    include_disabled: bool = False,
    limit: int = 100,
    offset: int = 0
) -> str:
    """
    List service users with merge handling.
    
    Args:
        org_id: Organization identifier
        project_id: Optional project filter
        include_disabled: Include disabled users
        limit: Maximum results
        offset: Pagination offset
    
    Returns:
        JSON array of users with merge status
    """
    endpoint = f"organization/{org_id}/service_users/"
    
    params = {
        "limit": limit,
        "offset": offset,
        "include_disabled": include_disabled
    }
    
    if project_id:
        params["project_id"] = project_id
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_user_mapping(
    org_id: int,
    user_keys: str,
    service_ids: str
) -> str:
    """
    Map user keys to human-readable names.
    
    Args:
        org_id: Organization identifier
        user_keys: JSON array of user_key/service_id pairs
        service_ids: Comma-separated service IDs
    
    Returns:
        JSON mapping of user keys to names
    
    Example user_keys:
    [{"user_key": "john.doe", "service_id": "123"}]
    """
    endpoint = f"organization/{org_id}/service_user/get_map/"
    
    try:
        keys_list = json.loads(user_keys) if isinstance(user_keys, str) else user_keys
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON in user_keys parameter"})
    
    data = {
        "user_keys": keys_list,
        "service_ids": service_ids.split(",") if isinstance(service_ids, str) else service_ids
    }
    
    result = await api_client.request("POST", endpoint, data=data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_user_tags(
    org_id: int,
    user_ids: Optional[str] = None,
    tag_ids: Optional[str] = None
) -> str:
    """
    Get user categorization tags.
    
    Args:
        org_id: Organization identifier
        user_ids: Optional comma-separated user IDs
        tag_ids: Optional comma-separated tag IDs
    
    Returns:
        JSON with user tags and categories
    """
    endpoint = f"organization/{org_id}/service_user/tags/"
    
    params = {}
    if user_ids:
        params["user_ids"] = user_ids
    if tag_ids:
        params["tag_ids"] = tag_ids
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_team_categories(
    org_id: int,
    include_users: bool = True
) -> str:
    """
    List team categories and hierarchies.
    
    Args:
        org_id: Organization identifier
        include_users: Include user assignments
    
    Returns:
        JSON array of team categories with hierarchy
    """
    endpoint = f"organization/{org_id}/categories/"
    
    params = {
        "include_users": include_users
    }
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


# ==========================================
# 4. ORGANIZATION & PROJECT ENDPOINTS (4)
# ==========================================

@mcp.tool()
async def get_organization_settings(org_id: int) -> str:
    """
    Get organization configuration and settings.
    
    Args:
        org_id: Organization identifier
    
    Returns:
        JSON with organization settings
    """
    endpoint = f"organization/{org_id}/settings/"
    
    result = await api_client.request("GET", endpoint)
    return json.dumps(result, indent=2)


@mcp.tool()
async def list_projects(org_id: int, include_disabled: bool = False) -> str:
    """
    List all projects in an organization.
    
    Args:
        org_id: Organization identifier
        include_disabled: Include disabled projects
    
    Returns:
        JSON array of projects
    """
    endpoint = f"organization/{org_id}/projects/"
    
    params = {
        "include_disabled": include_disabled
    }
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_project_services(
    project_id: int,
    include_disabled: bool = False
) -> str:
    """
    Get connected services for a project.
    
    Args:
        project_id: Project identifier
        include_disabled: Include disabled services
    
    Returns:
        JSON array of connected services
    """
    endpoint = f"project/{project_id}/services/"
    
    params = {
        "include_disabled": include_disabled
    }
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_enabled_work_bundles(
    project_id: int,
    service_ids: Optional[str] = None
) -> str:
    """
    List enabled work bundles for a project.
    
    Args:
        project_id: Project identifier
        service_ids: Optional comma-separated service IDs
    
    Returns:
        JSON array of work bundles
    """
    endpoint = f"project/{project_id}/work_bundles/"
    
    params = {
        "enabled": True
    }
    
    if service_ids:
        params["service_ids"] = service_ids
    
    result = await api_client.request("GET", endpoint, params=params)
    return json.dumps(result, indent=2)


# ==========================================
# 5. AI & ANALYTICS ENDPOINTS (4)
# ==========================================

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


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Allstacks MCP Server - AI-ready interface to Allstacks API'
    )
    parser.add_argument(
        '--api-token', '-t',
        required=True,
        help='API token for authentication'
    )
    parser.add_argument(
        '--base-url', '-u',
        default='https://api.allstacks.com/api/v1/',
        help='Base URL for the API (default: https://api.allstacks.com/api/v1/)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the API client with provided parameters
    ALLSTACKS_API_TOKEN = args.api_token
    ALLSTACKS_BASE_URL = args.base_url
    api_client = AllstacksAPIClient(ALLSTACKS_API_TOKEN, ALLSTACKS_BASE_URL)
    
    # Run the MCP server
    mcp.run(transport='stdio')
