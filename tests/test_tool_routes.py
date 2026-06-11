"""Verify URL templates for tools whose routes were known to be incorrect.

These guard against regressions of the route-drift fixes called out in the
MCP test findings.
"""

import asyncio
import unittest

from mcp.server.fastmcp import FastMCP

from allstacks_mcp.tools import (
    ai_analytics,
    alerts,
    forecasting,
    metrics,
    org_projects,
    risk_management,
    work_bundles,
)


class _RecordingClient:
    """Captures the request kwargs for assertion without making HTTP calls."""

    def __init__(self):
        self.last = None

    async def request(self, method, endpoint, params=None, data=None, **kwargs):
        self.last = {
            "method": method,
            "endpoint": endpoint,
            "params": params,
            "data": data,
        }
        if endpoint.endswith("projects/"):
            return [{"id": i} for i in range(30)]
        return {"ok": True}

    async def request_text(
        self,
        method,
        endpoint,
        params=None,
        data=None,
        response_format="json",
        **kwargs,
    ):
        self.last = {
            "method": method,
            "endpoint": endpoint,
            "params": params,
            "data": data,
            "response_format": response_format,
        }
        return f"format={response_format}"


def _run(coro):
    return asyncio.run(coro)


class ToolRouteTests(unittest.TestCase):
    def _build(self, register):
        mcp = FastMCP("Test")
        client = _RecordingClient()
        register(mcp, client)
        return mcp, client

    def test_list_ai_reports_uses_hyphenated_route(self):
        mcp, client = self._build(ai_analytics.register_tools)
        _run(mcp.call_tool("list_ai_reports", {"org_id": 7}))
        self.assertEqual(client.last["method"], "GET")
        self.assertEqual(client.last["endpoint"], "organization/7/ai-reports/")

    def test_get_ai_report_uses_hyphenated_route(self):
        mcp, client = self._build(ai_analytics.register_tools)
        _run(mcp.call_tool("get_ai_report", {"org_id": 7, "report_id": 42}))
        self.assertEqual(client.last["endpoint"], "organization/7/ai-reports/42/")

    def test_get_project_services_uses_singular_route(self):
        mcp, client = self._build(org_projects.register_tools)
        _run(mcp.call_tool("get_project_services", {"project_id": 49816}))
        self.assertEqual(client.last["endpoint"], "project/49816/service/")

    def test_get_project_configuration_uses_configuration_options(self):
        mcp, client = self._build(org_projects.register_tools)
        _run(mcp.call_tool("get_project_configuration", {"project_id": 49816}))
        self.assertEqual(
            client.last["endpoint"], "project/49816/configuration_options/"
        )

    def test_get_project_uses_flat_project_route(self):
        mcp, client = self._build(org_projects.register_tools)
        _run(mcp.call_tool("get_project", {"project_id": 49816}))
        self.assertEqual(client.last["endpoint"], "project/49816/")

    def test_list_projects_forwards_toon_response_format(self):
        mcp, client = self._build(org_projects.register_tools)
        result = _run(
            mcp.call_tool("list_projects", {"org_id": 7, "response_format": "toon"})
        )
        self.assertEqual(client.last["endpoint"], "organization/7/projects/")
        text = result[0][0].text if isinstance(result, tuple) else result[0].text
        self.assertNotIn('"id"', text)
        self.assertIn("id", text)

    def test_list_projects_forwards_limit(self):
        mcp, client = self._build(org_projects.register_tools)
        _run(mcp.call_tool("list_projects", {"org_id": 7, "limit": 10}))
        self.assertEqual(client.last["params"]["limit"], 10)

    def test_list_work_bundles_uses_initial_route(self):
        mcp, client = self._build(work_bundles.register_tools)
        _run(mcp.call_tool("list_work_bundles", {"project_id": 49816}))
        self.assertEqual(client.last["endpoint"], "project/49816/work_bundles/initial/")

    def test_time_series_tools_forward_toon_response_format(self):
        mcp, client = self._build(metrics.register_tools)
        _run(
            mcp.call_tool(
                "get_gmdts_data",
                {
                    "project_id": 49816,
                    "metric_type": "Velocity",
                    "response_format": "toon",
                },
            )
        )
        self.assertEqual(
            client.last["endpoint"], "project/49816/generated_metric_data/Velocity"
        )
        self.assertEqual(client.last["response_format"], "toon")

    def test_get_population_benchmark_route_has_no_trailing_slash(self):
        # The Django route regex (metric/(?P<metric_type>.+)$) captures a trailing
        # slash into metric_type and the view rejects it as an invalid type.
        mcp, client = self._build(metrics.register_tools)
        _run(mcp.call_tool("get_population_benchmark", {"metric_type": "CycleTime"}))
        self.assertEqual(
            client.last["endpoint"], "population-benchmarks/metric/CycleTime"
        )

    def test_get_population_benchmark_strips_trailing_slash(self):
        mcp, client = self._build(metrics.register_tools)
        _run(mcp.call_tool("get_population_benchmark", {"metric_type": "CycleTime/"}))
        self.assertEqual(
            client.last["endpoint"], "population-benchmarks/metric/CycleTime"
        )

    def test_list_project_risk_definitions_uses_risk_definitions_route(self):
        mcp, client = self._build(risk_management.register_tools)
        _run(mcp.call_tool("list_project_risk_definitions", {"project_id": 49816}))
        self.assertEqual(client.last["endpoint"], "project/49816/risk_definitions/")


class DeadToolRemovalTests(unittest.TestCase):
    """Tools that targeted nonexistent endpoints must not be re-registered."""

    def _names(self, register) -> set:
        mcp = FastMCP("Test")

        class _NoopClient:
            async def request(self, *a, **kw):
                return {}

        register(mcp, _NoopClient())
        return {t.name for t in asyncio.run(mcp.list_tools())}

    def test_dead_tools_unregistered(self):
        ai_names = self._names(ai_analytics.register_tools)
        op_names = self._names(org_projects.register_tools)
        alert_names = self._names(alerts.register_tools)
        forecast_names = self._names(forecasting.register_tools)

        risk_names = self._names(risk_management.register_tools)
        for name, present_in in [
            ("get_project_time_periods", op_names),
            ("get_time_periods_by_type", op_names),
            ("update_project_configuration", op_names),
            ("get_velocity_data", forecast_names),
            ("list_active_alerts", alert_names),
            ("get_developer_experience_score", ai_names),
            ("get_insights", ai_names),
            # Renamed to list_project_risk_definitions; the old name described
            # active risks but the URL returns definitions.
            ("get_project_risks", risk_names),
        ]:
            self.assertNotIn(name, present_in, f"{name} should be removed")


if __name__ == "__main__":
    unittest.main()
