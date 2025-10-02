"""Alerts & Monitoring - Risk alerts and notification management"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all alerts and monitoring tools with the MCP server"""
    
    # ============================================================================
    # Alert Rules & Configuration
    # ============================================================================
    
    @mcp.tool()
    async def list_alert_rules(
        org_id: int,
        project_id: Optional[int] = None,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List all alert rules configured for the organization or project.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/alert_rules/
        
        Alert rules define conditions that trigger notifications when metrics
        exceed thresholds or patterns are detected.
        
        Args:
            org_id: Organization identifier
            project_id: Optional filter by project
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of alert rules with conditions and actions
        """
        endpoint = f"organization/{org_id}/alert_rules/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if project_id:
            params["project_id"] = project_id
        if ordering:
            params["ordering"] = ordering
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_alert_rule(
        org_id: int,
        name: str,
        condition: str,
        alert_type: str,
        project_id: Optional[int] = None,
        enabled: bool = True
    ) -> str:
        """
        Create a new alert rule for monitoring metrics and conditions.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/alert_rules/
        
        Args:
            org_id: Organization identifier
            name: Alert rule name (REQUIRED)
            condition: JSON string defining alert conditions (REQUIRED)
            alert_type: Type of alert (metric_threshold, pattern_detection, etc.) (REQUIRED)
            project_id: Optional project to scope the alert to
            enabled: Whether the alert is active (default: True)
        
        Returns:
            Created alert rule with ID
        """
        endpoint = f"organization/{org_id}/alert_rules/"
        
        try:
            condition_dict = json.loads(condition) if isinstance(condition, str) else condition
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in condition parameter"})
        
        data = {
            "name": name,
            "condition": condition_dict,
            "alert_type": alert_type,
            "enabled": enabled
        }
        
        if project_id:
            data["project_id"] = project_id
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_alert_rule(org_id: int, rule_id: int) -> str:
        """
        Get detailed information about a specific alert rule.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/alert_rules/{id}/
        
        Args:
            org_id: Organization identifier
            rule_id: Alert rule identifier
        
        Returns:
            JSON with alert rule details, conditions, and history
        """
        endpoint = f"organization/{org_id}/alert_rules/{rule_id}/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_alert_rule(
        org_id: int,
        rule_id: int,
        rule_data: str
    ) -> str:
        """
        Update an alert rule's configuration.
        
        From OpenAPI: PUT/PATCH /api/v1/organization/{org_id}/alert_rules/{id}/
        
        Args:
            org_id: Organization identifier
            rule_id: Alert rule identifier
            rule_data: JSON string with rule updates (name, condition, enabled, etc.)
        
        Returns:
            Updated alert rule details
        """
        endpoint = f"organization/{org_id}/alert_rules/{rule_id}/"
        
        try:
            data = json.loads(rule_data) if isinstance(rule_data, str) else rule_data
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in rule_data parameter"})
        
        result = await api_client.request("PATCH", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_alert_rule(org_id: int, rule_id: int) -> str:
        """
        Delete an alert rule.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/alert_rules/{id}/
        
        Args:
            org_id: Organization identifier
            rule_id: Alert rule identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/alert_rules/{rule_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Active Alerts & Notifications
    # ============================================================================

    @mcp.tool()
    async def list_active_alerts(
        org_id: int,
        project_id: Optional[int] = None,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        List currently active/triggered alerts across the organization.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/alerts/active/
        
        Args:
            org_id: Organization identifier
            project_id: Optional filter by project
            alert_type: Optional filter by alert type
            severity: Optional filter by severity (low, medium, high, critical)
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of active alerts with timestamps and details
        """
        endpoint = f"organization/{org_id}/alerts/active/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if project_id:
            params["project_id"] = project_id
        if alert_type:
            params["alert_type"] = alert_type
        if severity:
            params["severity"] = severity
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_alert_history(
        org_id: int,
        rule_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """
        Get historical alert data and trigger events.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/alerts/history/
        
        Args:
            org_id: Organization identifier
            rule_id: Optional filter by specific alert rule
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of historical alert events
        """
        endpoint = f"organization/{org_id}/alerts/history/"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if rule_id:
            params["rule_id"] = rule_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def acknowledge_alert(org_id: int, alert_id: int, note: Optional[str] = None) -> str:
        """
        Acknowledge an active alert to mark it as reviewed.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/alerts/{id}/acknowledge/
        
        Args:
            org_id: Organization identifier
            alert_id: Alert identifier
            note: Optional note about the acknowledgment
        
        Returns:
            Acknowledged alert details
        """
        endpoint = f"organization/{org_id}/alerts/{alert_id}/acknowledge/"
        
        data = {}
        if note:
            data["note"] = note
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def resolve_alert(org_id: int, alert_id: int, resolution: Optional[str] = None) -> str:
        """
        Mark an alert as resolved with optional resolution notes.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/alerts/{id}/resolve/
        
        Args:
            org_id: Organization identifier
            alert_id: Alert identifier
            resolution: Optional resolution notes
        
        Returns:
            Resolved alert details
        """
        endpoint = f"organization/{org_id}/alerts/{alert_id}/resolve/"
        
        data = {}
        if resolution:
            data["resolution"] = resolution
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Notification Preferences
    # ============================================================================

    @mcp.tool()
    async def get_notification_preferences(org_id: int) -> str:
        """
        Get notification preferences for alerts.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/notification_preferences/
        
        Args:
            org_id: Organization identifier
        
        Returns:
            JSON with notification channel preferences (email, slack, etc.)
        """
        endpoint = f"organization/{org_id}/notification_preferences/"
        
        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def update_notification_preferences(org_id: int, preferences: str) -> str:
        """
        Update notification preferences for alerts.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/notification_preferences/
        
        Args:
            org_id: Organization identifier
            preferences: JSON string with notification preferences
        
        Returns:
            Updated preferences
        """
        endpoint = f"organization/{org_id}/notification_preferences/"
        
        try:
            data = json.loads(preferences) if isinstance(preferences, str) else preferences
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in preferences parameter"})
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Alert Subscriptions
    # ============================================================================

    @mcp.tool()
    async def list_alert_subscriptions(
        org_id: int,
        user_id: Optional[int] = None
    ) -> str:
        """
        List alert subscriptions for users.
        
        From OpenAPI: GET /api/v1/organization/{org_id}/alert_subscriptions/
        
        Args:
            org_id: Organization identifier
            user_id: Optional filter by specific user
        
        Returns:
            JSON array of alert subscriptions
        """
        endpoint = f"organization/{org_id}/alert_subscriptions/"
        
        params = {}
        if user_id:
            params["user_id"] = user_id
        
        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def subscribe_to_alert(
        org_id: int,
        rule_id: int,
        user_id: int,
        channels: str
    ) -> str:
        """
        Subscribe a user to an alert rule.
        
        From OpenAPI: POST /api/v1/organization/{org_id}/alert_subscriptions/
        
        Args:
            org_id: Organization identifier
            rule_id: Alert rule ID to subscribe to (REQUIRED)
            user_id: User ID to subscribe (REQUIRED)
            channels: JSON string array of notification channels (email, slack, etc.) (REQUIRED)
        
        Returns:
            Created subscription details
        """
        endpoint = f"organization/{org_id}/alert_subscriptions/"
        
        try:
            channels_list = json.loads(channels) if isinstance(channels, str) else channels
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in channels parameter"})
        
        data = {
            "rule_id": rule_id,
            "user_id": user_id,
            "channels": channels_list
        }
        
        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def unsubscribe_from_alert(org_id: int, subscription_id: int) -> str:
        """
        Unsubscribe from an alert rule.
        
        From OpenAPI: DELETE /api/v1/organization/{org_id}/alert_subscriptions/{id}/
        
        Args:
            org_id: Organization identifier
            subscription_id: Subscription identifier
        
        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/alert_subscriptions/{subscription_id}/"
        
        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)
