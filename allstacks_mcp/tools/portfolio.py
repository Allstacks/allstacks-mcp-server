"""Portfolio & Deliverables Endpoints (5 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all portfolio-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_portfolios(
        org_id: int,
        include_archived: bool = False,
        limit: int = 100
    ) -> str:
        """
        List all portfolios in an organization.
        
        Args:
            org_id: Organization identifier
            include_archived: Include archived portfolios
            limit: Maximum results to return
        
        Returns:
            JSON array of portfolios
        """
        endpoint = f"organization/{org_id}/portfolios/"
        
        params = {
            "include_archived": include_archived,
            "limit": limit
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_portfolio_details(
        org_id: int,
        portfolio_id: int,
        include_items: bool = True
    ) -> str:
        """
        Get detailed information about a specific portfolio.
        
        Args:
            org_id: Organization identifier
            portfolio_id: Portfolio identifier
            include_items: Include portfolio items in response
        
        Returns:
            JSON with portfolio details and items
        """
        endpoint = f"organization/{org_id}/portfolios/{portfolio_id}/"
        
        params = {
            "include_items": include_items
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_portfolio(
        org_id: int,
        name: str,
        description: str,
        owner_id: int,
        project_ids: Optional[str] = None
    ) -> str:
        """
        Create a new portfolio.
        
        Args:
            org_id: Organization identifier
            name: Portfolio name
            description: Portfolio description
            owner_id: Portfolio owner user ID
            project_ids: Optional comma-separated project IDs to include
        
        Returns:
            Created portfolio with ID
        """
        endpoint = f"organization/{org_id}/portfolios/"
        
        data = {
            "name": name,
            "description": description,
            "owner_id": owner_id
        }
        
        if project_ids:
            data["project_ids"] = [int(x) for x in project_ids.split(",")]
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_deliverables(
        project_id: int,
        status: Optional[str] = None,
        owner_ids: Optional[str] = None,
        include_completed: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List deliverables for a project.
        
        Args:
            project_id: Project identifier
            status: Optional status filter (planned, in_progress, at_risk, completed)
            owner_ids: Optional comma-separated owner IDs
            include_completed: Include completed deliverables
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            JSON array of deliverables
        """
        endpoint = f"project/{project_id}/deliverables/"
        
        params = {
            "include_completed": include_completed,
            "limit": limit,
            "offset": offset
        }
        
        if status:
            params["status"] = status
        if owner_ids:
            params["owner_ids"] = owner_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_deliverable_status(
        project_id: int,
        deliverable_id: int,
        include_history: bool = True
    ) -> str:
        """
        Get detailed status of a specific deliverable.
        
        Args:
            project_id: Project identifier
            deliverable_id: Deliverable identifier
            include_history: Include status history
        
        Returns:
            JSON with deliverable status and history
        """
        endpoint = f"project/{project_id}/deliverables/{deliverable_id}/status/"
        
        params = {
            "include_history": include_history
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

