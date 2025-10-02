"""Milestones & Pinned Milestones Endpoints (6 tools)"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all milestone-related tools with the MCP server"""
    
    @mcp.tool()
    async def list_milestones(
        project_id: int,
        include_completed: bool = False,
        milestone_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> str:
        """
        List all milestones for a project.
        
        Args:
            project_id: Project identifier
            include_completed: Include completed milestones
            milestone_type: Optional type filter (release, sprint, custom)
            start_date: Optional start date filter
            end_date: Optional end date filter
            limit: Maximum results
        
        Returns:
            JSON array of milestones
        """
        endpoint = f"project/{project_id}/milestones/"
        
        params = {
            "include_completed": include_completed,
            "limit": limit
        }
        
        if milestone_type:
            params["milestone_type"] = milestone_type
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_pinned_milestones(
        org_id: int,
        project_ids: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> str:
        """
        Get pinned milestones for organization or specific projects.
        
        Args:
            org_id: Organization identifier
            project_ids: Optional comma-separated project IDs
            user_id: Optional user filter for personal pins
        
        Returns:
            JSON array of pinned milestones
        """
        endpoint = f"organization/{org_id}/pinned_milestones/"
        
        params = {}
        if project_ids:
            params["project_ids"] = project_ids
        if user_id:
            params["user_id"] = user_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def pin_milestone(
        org_id: int,
        milestone_id: int,
        project_id: int,
        scope: str = "organization"
    ) -> str:
        """
        Pin a milestone for visibility.
        
        Args:
            org_id: Organization identifier
            milestone_id: Milestone to pin
            project_id: Project containing the milestone
            scope: Pin scope (organization, project, personal)
        
        Returns:
            JSON with pin confirmation
        """
        endpoint = f"organization/{org_id}/pinned_milestones/"
        
        data = {
            "milestone_id": milestone_id,
            "project_id": project_id,
            "scope": scope
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def unpin_milestone(
        org_id: int,
        milestone_id: int,
        project_id: int
    ) -> str:
        """
        Unpin a previously pinned milestone.
        
        Args:
            org_id: Organization identifier
            milestone_id: Milestone to unpin
            project_id: Project containing the milestone
        
        Returns:
            JSON with unpin confirmation
        """
        endpoint = f"organization/{org_id}/pinned_milestones/{milestone_id}/"
        
        params = {
            "project_id": project_id
        }
        
        result = await api_client.request("DELETE", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_milestone_report(
        project_id: int,
        milestone_id: int,
        include_metrics: bool = True,
        include_risks: bool = True,
        include_dependencies: bool = True
    ) -> str:
        """
        Generate comprehensive milestone report.
        
        Args:
            project_id: Project identifier
            milestone_id: Milestone identifier
            include_metrics: Include performance metrics
            include_risks: Include risk assessment
            include_dependencies: Include dependency analysis
        
        Returns:
            JSON with milestone report data
        """
        endpoint = f"project/{project_id}/milestones/{milestone_id}/report/"
        
        params = {
            "include_metrics": include_metrics,
            "include_risks": include_risks,
            "include_dependencies": include_dependencies
        }
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_milestone(
        project_id: int,
        name: str,
        target_date: str,
        milestone_type: str = "custom",
        description: Optional[str] = None,
        owner_id: Optional[int] = None,
        work_item_ids: Optional[str] = None
    ) -> str:
        """
        Create a new milestone.
        
        Args:
            project_id: Project identifier
            name: Milestone name
            target_date: Target completion date (YYYY-MM-DD)
            milestone_type: Type of milestone (release, sprint, custom)
            description: Optional description
            owner_id: Optional owner user ID
            work_item_ids: Optional comma-separated work item IDs
        
        Returns:
            Created milestone with ID
        """
        endpoint = f"project/{project_id}/milestones/"
        
        data = {
            "name": name,
            "target_date": target_date,
            "milestone_type": milestone_type
        }
        
        if description:
            data["description"] = description
        if owner_id:
            data["owner_id"] = owner_id
        if work_item_ids:
            data["work_item_ids"] = [int(x) for x in work_item_ids.split(",")]
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

