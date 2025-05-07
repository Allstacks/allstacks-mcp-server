import argparse
import json
from typing import Any
import httpx
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Allstacks-MCP")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

ALLSTACKS_API_TOKEN = "example"
ALLSTACKS_BASE_URL = "https://api.allstacks.com/api/v1/"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool()
async def getOrganizationInvestments(org_id: int) -> str:
    """Get current investments for an organization.

    Args:
        org_id: The organization ID
    """
    # Construct the URL with the org_id parameter
    url = f"{ALLSTACKS_BASE_URL}organization/{org_id}/ai_summary/currentInvestments"
    
    # Set up headers with the API token
    headers = {
        "Authorization": f"Bearer {ALLSTACKS_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request using requests library
        response = requests.post(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data
            data = response.json()
            return json.dumps(data, indent=2)
        else:
            # Handle error responses
            error_text = response.text
            return f"Error {response.status_code}: {error_text}"
    except Exception as e:
        # Handle any exceptions that occur during the request
        return f"Failed to get organization investments: {str(e)}"

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run server with API token and base URL')
    parser.add_argument('--api-token', '-t', required=True, help='API token for authentication')
    parser.add_argument('--base-url', '-u', default='https://api.allstacks.com/api/v1/', help='Base URL for the API (default: https://api.allstacks.com/api/v1/)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize and run the server with the provided parameters
    ALLSTACKS_API_TOKEN = args.api_token
    ALLSTACKS_BASE_URL = args.base_url
    
    # Pass parameters to your mcp module
    mcp.run(transport='stdio')