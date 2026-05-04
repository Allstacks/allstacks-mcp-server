"""AI & Analytics - AI-powered reports, insights, and code analysis"""

import json
from typing import Optional


def register_tools(mcp, api_client):
    """Register all AI and analytics tools with the MCP server"""

    # ============================================================================
    # AI Reports
    # ============================================================================

    @mcp.tool()
    async def list_ai_reports(
        org_id: int,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        ordering: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> str:
        """
        List AI-generated reports for analysis and insights.

        From OpenAPI: GET /api/v1/organization/{org_id}/ai_reports/

        AI Reports provide automated analysis of project health, team performance,
        and risk factors using machine learning.

        Args:
            org_id: Organization identifier
            project_id: Optional filter by project
            status: Optional filter by status (pending, completed, failed)
            ordering: Optional ordering field
            limit: Number of results per page (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            JSON array of AI reports with summaries and insights
        """
        endpoint = f"organization/{org_id}/ai_reports/"

        params = {"limit": limit, "offset": offset}

        if project_id:
            params["project_id"] = project_id
        if status:
            params["status"] = status
        if ordering:
            params["ordering"] = ordering

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_ai_report(
        org_id: int, report_type: str, project_id: int, config: Optional[str] = None
    ) -> str:
        """
        Generate a new AI report for a project.

        From OpenAPI: POST /api/v1/organization/{org_id}/ai_reports/

        Args:
            org_id: Organization identifier
            report_type: Type of report to generate (REQUIRED)
            project_id: Project to analyze (REQUIRED)
            config: Optional JSON string with report configuration

        Returns:
            Created report with ID and generation status
        """
        endpoint = f"organization/{org_id}/ai_reports/"

        data = {"report_type": report_type, "project_id": project_id}

        if config:
            try:
                data["config"] = (
                    json.loads(config) if isinstance(config, str) else config
                )
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON in config parameter"})

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_ai_report(org_id: int, report_id: int) -> str:
        """
        Get detailed AI report results and insights.

        From OpenAPI: GET /api/v1/organization/{org_id}/ai_reports/{id}/

        Args:
            org_id: Organization identifier
            report_id: Report identifier

        Returns:
            JSON with complete report including AI-generated insights, recommendations, and data
        """
        endpoint = f"organization/{org_id}/ai_reports/{report_id}/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def delete_ai_report(org_id: int, report_id: int) -> str:
        """
        Delete an AI report.

        From OpenAPI: DELETE /api/v1/organization/{org_id}/ai_reports/{id}/

        Args:
            org_id: Organization identifier
            report_id: Report identifier

        Returns:
            Deletion confirmation
        """
        endpoint = f"organization/{org_id}/ai_reports/{report_id}/"

        result = await api_client.request("DELETE", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def regenerate_ai_report(org_id: int, report_id: int) -> str:
        """
        Regenerate an existing AI report with latest data.

        From OpenAPI: POST /api/v1/organization/{org_id}/ai_reports/{id}/regenerate/

        Args:
            org_id: Organization identifier
            report_id: Report identifier

        Returns:
            Updated report generation status
        """
        endpoint = f"organization/{org_id}/ai_reports/{report_id}/regenerate/"

        result = await api_client.request("POST", endpoint)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Action AI & Code Query
    # ============================================================================

    @mcp.tool()
    async def query_code(
        org_id: int, project_id: int, query: str, file_patterns: Optional[str] = None
    ) -> str:
        """
        Query codebase using natural language with Action AI.

        From OpenAPI: POST /api/v1/organization/{org_id}/action_ai/code_query/

        Use AI to search and understand code patterns, functions, and architecture
        across your codebase.

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            query: Natural language query about the code (REQUIRED)
            file_patterns: Optional comma-separated file patterns to search (*.py, *.js, etc.)

        Returns:
            JSON with AI-analyzed code results and explanations
        """
        endpoint = f"organization/{org_id}/action_ai/code_query/"

        data = {"project_id": project_id, "query": query}

        if file_patterns:
            data["file_patterns"] = file_patterns

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def create_metric_with_ai(
        org_id: int, project_id: int, description: str, context: Optional[str] = None
    ) -> str:
        """
        Use AI to create a custom metric configuration from natural language description.

        From OpenAPI: POST /api/v1/organization/{org_id}/action_ai/metric_builder/

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            description: Natural language description of desired metric (REQUIRED)
            context: Optional additional context or examples

        Returns:
            JSON with AI-generated metric configuration ready to use
        """
        endpoint = f"organization/{org_id}/action_ai/metric_builder/"

        data = {"project_id": project_id, "description": description}

        if context:
            data["context"] = context

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def ai_metric_builder(
        project_id: int,
        prompt: str,
        previous_config: Optional[str] = None,
        stream: bool = False,
        data_source: Optional[str] = None,
    ) -> str:
        """
        Run the AI metric builder (chart builder agent): natural language to a Metrics V2 chart/metric config.

        From API: POST /api/v1/project/{project_id}/actionai/ai-metric-builder/

        **Request body (what you send):**
        - ``prompt`` (required): one-shot string, or the API also accepts a list of strings for multi-turn
          content; a single string is wrapped to a one-element list by the API.
        - ``previous_config`` (optional): JSON object (pass here as a JSON *string*); prior chart/metric
          config to refine in a follow-up turn.
        - ``stream`` (optional): when true, the HTTP response is SSE (progress events), not a single JSON
          document; this client returns ``{"raw_body": "<SSE payload>"}`` instead of parsing JSON.
        - ``data_source`` (optional): one of ``"default"``, ``"investment_hours"``, ``"rnd_velocity"``.

        **Response shape (what you get back):**
        - ``stream`` false: JSON from the builder describing the **metric/chart definition** (filters,
          dimensions, metric selection, view metadata), not the full Metrics V2 **data** response. Use the
          object that matches the **inner** ``config`` for ``POST .../metrics_v2/metrics``.
        - ``stream`` true: ``{"raw_body": "..."}`` with raw SSE text; parse until you have the final config.

        **Getting actual data (required next step):** Call ``get_project_metrics_v2_data`` with the same
        ``project_id`` and the inner ``config`` as a JSON string. The MCP tool sends the API body
        ``{"config", "get_count_only", "variables"}``.

        Args:
            project_id: Project identifier (path)
            prompt: Raw question or instruction for the metric builder (REQUIRED)
            previous_config: Optional JSON string of a prior chart/metric config to refine
            stream: If true, request SSE streaming (returns raw response body under raw_body)
            data_source: Optional data source override for the builder

        Returns:
            JSON from the metric builder (config-oriented), or with stream=true a JSON object with key
            raw_body (SSE text). Use ``get_project_metrics_v2_data`` next to retrieve metric data.
        """
        endpoint = f"project/{project_id}/actionai/ai-metric-builder/"

        data: dict = {"prompt": prompt}

        if previous_config is not None:
            try:
                data["previous_config"] = json.loads(previous_config)
            except json.JSONDecodeError:
                return json.dumps(
                    {"error": "Invalid JSON in previous_config parameter"}
                )

        if stream:
            data["stream"] = True

        if data_source is not None:
            data["data_source"] = data_source

        result = await api_client.request(
            "POST",
            endpoint,
            data=data,
            timeout_seconds=120.0,
            expect_json=not stream,
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def analyze_patterns(
        org_id: int,
        project_id: int,
        pattern_type: str,
        time_range: Optional[str] = None,
    ) -> str:
        """
        Analyze development patterns and anomalies using AI.

        From OpenAPI: POST /api/v1/organization/{org_id}/action_ai/pattern_analysis/

        Args:
            org_id: Organization identifier
            project_id: Project identifier
            pattern_type: Type of pattern to analyze (deployment, commit, review, etc.) (REQUIRED)
            time_range: Optional time range (last_week, last_month, last_quarter)

        Returns:
            JSON with detected patterns, anomalies, and insights
        """
        endpoint = f"organization/{org_id}/action_ai/pattern_analysis/"

        data = {"project_id": project_id, "pattern_type": pattern_type}

        if time_range:
            data["time_range"] = time_range

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Developer Experience & Surveys
    # ============================================================================

    @mcp.tool()
    async def list_surveys(
        org_id: int, project_id: Optional[int] = None, status: Optional[str] = None
    ) -> str:
        """
        List developer experience surveys and their results.

        From OpenAPI: GET /api/v1/organization/{org_id}/surveys/

        Args:
            org_id: Organization identifier
            project_id: Optional filter by project
            status: Optional filter by status (active, completed, draft)

        Returns:
            JSON array of surveys with participation and response data
        """
        endpoint = f"organization/{org_id}/surveys/"

        params = {}
        if project_id:
            params["project_id"] = project_id
        if status:
            params["status"] = status

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_survey_results(org_id: int, survey_id: int) -> str:
        """
        Get detailed survey results and analytics.

        From OpenAPI: GET /api/v1/organization/{org_id}/surveys/{id}/results/

        Args:
            org_id: Organization identifier
            survey_id: Survey identifier

        Returns:
            JSON with aggregated survey responses, trends, and insights
        """
        endpoint = f"organization/{org_id}/surveys/{survey_id}/results/"

        result = await api_client.request("GET", endpoint)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_developer_experience_score(
        org_id: int,
        project_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """
        Get developer experience (DX) score and breakdown.

        From OpenAPI: GET /api/v1/organization/{org_id}/developer_experience/score/

        Args:
            org_id: Organization identifier
            project_id: Project identifier (query parameter)
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            JSON with DX score, component scores, and trends
        """
        endpoint = f"organization/{org_id}/developer_experience/score/"

        params = {"project_id": project_id}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # AI Tool Usage (Cursor, Q, etc.)
    # ============================================================================

    @mcp.tool()
    async def get_ai_tool_usage(
        org_id: int,
        project_id: int,
        tool_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """
        Get AI coding tool usage statistics (Cursor, Amazon Q, Copilot, etc.).

        From OpenAPI: GET /api/v1/organization/{org_id}/ai_tool_usage/

        Track adoption and usage patterns of AI coding assistants.

        Args:
            org_id: Organization identifier
            project_id: Project identifier (query parameter)
            tool_name: Optional filter by specific tool (cursor, q, copilot, etc.)
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            JSON with usage statistics, adoption trends, and productivity correlation
        """
        endpoint = f"organization/{org_id}/ai_tool_usage/"

        params = {"project_id": project_id}
        if tool_name:
            params["tool_name"] = tool_name
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_ai_tool_impact(
        org_id: int, project_id: int, user_id: Optional[int] = None
    ) -> str:
        """
        Analyze the impact of AI tools on developer productivity.

        From OpenAPI: GET /api/v1/organization/{org_id}/ai_tool_usage/impact/

        Args:
            org_id: Organization identifier
            project_id: Project identifier (query parameter)
            user_id: Optional filter by specific user

        Returns:
            JSON with productivity impact analysis, before/after comparison
        """
        endpoint = f"organization/{org_id}/ai_tool_usage/impact/"

        params = {"project_id": project_id}
        if user_id:
            params["user_id"] = user_id

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    # ============================================================================
    # Insights & Recommendations
    # ============================================================================

    @mcp.tool()
    async def get_insights(
        org_id: int, project_id: int, category: Optional[str] = None
    ) -> str:
        """
        Get AI-generated insights and recommendations for a project.

        From OpenAPI: GET /api/v1/organization/{org_id}/insights/

        Args:
            org_id: Organization identifier
            project_id: Project identifier (query parameter)
            category: Optional category filter (performance, quality, delivery, team)

        Returns:
            JSON array of insights with severity, recommendations, and actionable steps
        """
        endpoint = f"organization/{org_id}/insights/"

        params = {"project_id": project_id}
        if category:
            params["category"] = category

        result = await api_client.request("GET", endpoint, params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dismiss_insight(
        org_id: int, insight_id: int, reason: Optional[str] = None
    ) -> str:
        """
        Dismiss an insight as not relevant or already addressed.

        From OpenAPI: POST /api/v1/organization/{org_id}/insights/{id}/dismiss/

        Args:
            org_id: Organization identifier
            insight_id: Insight identifier
            reason: Optional reason for dismissal

        Returns:
            Confirmation of dismissal
        """
        endpoint = f"organization/{org_id}/insights/{insight_id}/dismiss/"

        data = {}
        if reason:
            data["reason"] = reason

        result = await api_client.request("POST", endpoint, data=data)
        return json.dumps(result, indent=2)
