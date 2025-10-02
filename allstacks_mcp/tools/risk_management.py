"""Risk Management - Risk definitions and risk assessment"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all risk management tools with the MCP server"""
    
    # ============================================================================
    # Risk Definitions
    # ============================================================================
    
    @mcp.tool()
    async def list_risk_definitions(
        org_id: int,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all risk definitions configured for the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/risk_definitions/
        
        Risk definitions specify conditions and thresholds that identify potential
        project risks (delays, quality issues, resource problems, etc.).
        
        Args:
            org_id: Organization identifier
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of risk definitions with conditions and severity levels
        """
        endpoint = f"organization/{org_id}/risk_definitions/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_risk_definition(
        org_id: int,
        name: str,
        description: str,
        condition: str,
        severity: str,
        risk_type: str
    ) -> str:
        """
        Create a new risk definition.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/risk_definitions/
        
        Args:
            org_id: Organization identifier
            name: Risk definition name (REQUIRED)
            description: Description of what the risk identifies (REQUIRED)
            condition: JSON string defining risk detection conditions (REQUIRED)
            severity: Risk severity (low, medium, high, critical) (REQUIRED)
            risk_type: Type of risk (delivery, quality, resource, technical_debt, etc.) (REQUIRED)
        
        Returns:
            Created risk definition with ID
        """
        endpoint = f"organization/{org_id}/risk_definitions/"
        
        try:
            condition_dict = json.loads(condition) if isinstance(condition, str) else condition
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in condition parameter"})
        
        data = {
            "name": name,
            "description": description,
            "condition": condition_dict,
            "severity": severity,
            "risk_type": risk_type
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_risk_definition(org_id: int, definition_id: int) -> str:
        """
        Get detailed information about a specific risk definition.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/risk_definitions/{id}/
        
        Args:
            org_id: Organization identifier
            definition_id: Risk definition identifier
        
        Returns:
            JSON with risk definition details, conditions, and usage statistics
        """
        endpoint = f"organization/{org_id}/risk_definitions/{definition_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_risk_definition(
        org_id: int,
        definition_id: int,
        definition_data: str
    ) -> str:
        """
        Update a risk definition's configuration.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/risk_definitions/{id}/
        
        Args:
            org_id: Organization identifier
            definition_id: Risk definition identifier
            definition_data: JSON string with definition updates (name, condition, severity, etc.)
        
        Returns:
            Updated risk definition details
        """
        endpoint = f"organization/{org_id}/risk_definitions/{definition_id}/"
        
        try:
            data = json.loads(definition_data) if isinstance(definition_data, str) else definition_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in definition_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_risk_definition(org_id: int, definition_id: int) -> str:
        """
        Delete a risk definition.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/risk_definitions/{id}/
        
        Args:
            org_id: Organization identifier
            definition_id: Risk definition identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/risk_definitions/{definition_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Risk Assessment & Active Risks
    # ============================================================================

    @mcp.tool()
    async def get_project_risks(
        project_id: int,
        risk_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        """
        Get active risks identified for a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/risks/
        
        Args:
            project_id: Project identifier
            risk_type: Optional filter by risk type (delivery, quality, resource, technical_debt)
            severity: Optional filter by severity (low, medium, high, critical)
            status: Optional filter by status (active, resolved, acknowledged)
        
        Returns:
            JSON array of active risks with details and affected service items
        """
        endpoint = f"project/{project_id}/risks/"
        
        params = {}
        if risk_type:
            params["risk_type"] = risk_type
        if severity:
            params["severity"] = severity
        if status:
            params["status"] = status
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_service_item_risks(project_id: int, service_item_id: int) -> str:
        """
        Get risks associated with a specific service item.
        
        From OpenAPI: GET /api/v1/project/{project_id}/service_items/{service_item_id}/risks/
        
        Args:
            project_id: Project identifier
            service_item_id: Service item identifier
        
        Returns:
            JSON array of risks affecting the service item
        """
        endpoint = f"project/{project_id}/service_items/{service_item_id}/risks/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def acknowledge_risk(
        project_id: int,
        risk_id: int,
        note: Optional[str] = None
    ) -> str:
        """
        Acknowledge a risk as reviewed.
        
        From OpenAPI: POST /api/v1/project/{project_id}/risks/{id}/acknowledge/
        
        Args:
            project_id: Project identifier
            risk_id: Risk identifier
            note: Optional acknowledgment note
        
        Returns:
            Acknowledged risk details
        """
        endpoint = f"project/{project_id}/risks/{risk_id}/acknowledge/"
        
        data = {}
        if note:
            data["note"] = note
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def resolve_risk(
        project_id: int,
        risk_id: int,
        resolution: Optional[str] = None
    ) -> str:
        """
        Mark a risk as resolved.
        
        From OpenAPI: POST /api/v1/project/{project_id}/risks/{id}/resolve/
        
        Args:
            project_id: Project identifier
            risk_id: Risk identifier
            resolution: Optional resolution notes
        
        Returns:
            Resolved risk details
        """
        endpoint = f"project/{project_id}/risks/{risk_id}/resolve/"
        
        data = {}
        if resolution:
            data["resolution"] = resolution
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_risk_trends(
        project_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        time_zone: str = "UTC"
    ) -> str:
        """
        Get historical risk trends for a project.
        
        From OpenAPI: GET /api/v1/project/{project_id}/risks/trends/
        
        Args:
            project_id: Project identifier
            start_date: Optional unix timestamp in milliseconds
            end_date: Optional unix timestamp in milliseconds
            time_zone: Timezone string (default: UTC)
        
        Returns:
            JSON with risk count trends over time by type and severity
        """
        endpoint = f"project/{project_id}/risks/trends/"
        
        params = {"time_zone": time_zone}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def run_risk_assessment(project_id: int) -> str:
        """
        Trigger a manual risk assessment scan for a project.
        
        From OpenAPI: POST /api/v1/project/{project_id}/risks/assess/
        
        Re-evaluates all risk definitions against current project data.
        
        Args:
            project_id: Project identifier
        
        Returns:
            Assessment status and newly identified risks
        """
        endpoint = f"project/{project_id}/risks/assess/"
        
        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_risk_summary(org_id: int, project_ids: Optional[str] = None) -> str:
        """
        Get risk summary across organization or specific projects.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/risks/summary/
        
        Args:
            org_id: Organization identifier
            project_ids: Optional comma-separated project IDs to filter
        
        Returns:
            JSON with aggregated risk counts by type, severity, and project
        """
        endpoint = f"organization/{org_id}/risks/summary/"
        
        params = {}
        if project_ids:
            params["project_ids"] = project_ids
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

