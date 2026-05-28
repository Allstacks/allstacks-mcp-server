"""Tests for MCP API discovery resources and category mappings."""

import asyncio
import json
import unittest

from mcp.server.fastmcp import FastMCP

from allstacks_mcp.tools import (
    ai_analytics,
    alerts,
    dashboards,
    discovery,
    employee,
    forecasting,
    labels,
    metrics,
    org_projects,
    risk_management,
    service_items,
    users_teams,
    work_bundles,
)


class _DiscoveryClient:
    def __init__(self):
        self.schema_calls = 0

    async def get_openapi_schema(self):
        self.schema_calls += 1
        return {"openapi": "3.0.3", "paths": {"/api/v1/projects/": {}}}

    async def request(self, *args, **kwargs):
        return {"ok": True}


def _run(coro):
    return asyncio.run(coro)


def _tool_text(call_result) -> str:
    content = call_result[0] if isinstance(call_result, tuple) else call_result
    return content[0].text


class DiscoveryTests(unittest.TestCase):
    def _build_discovery(self):
        mcp = FastMCP("Test")
        client = _DiscoveryClient()
        discovery.register_tools(mcp, client)
        return mcp, client

    def test_get_openapi_schema_tool_fetches_runtime_schema(self):
        mcp, client = self._build_discovery()

        result = _run(mcp.call_tool("get_openapi_schema", {}))

        self.assertEqual(json.loads(_tool_text(result))["openapi"], "3.0.3")
        self.assertEqual(client.schema_calls, 1)

    def test_openapi_schema_resources_fetch_runtime_schema(self):
        mcp, client = self._build_discovery()

        resources = {str(resource.uri) for resource in _run(mcp.list_resources())}
        self.assertIn("allstacks://openapi", resources)
        self.assertIn("schema://api", resources)

        contents = _run(mcp.read_resource("allstacks://openapi"))
        self.assertEqual(
            json.loads(contents[0].content)["paths"], {"/api/v1/projects/": {}}
        )
        self.assertEqual(client.schema_calls, 1)

    def test_tool_categories_include_expected_domains(self):
        mcp, _client = self._build_discovery()

        result = _run(mcp.call_tool("list_tool_categories", {}))
        categories = json.loads(_tool_text(result))

        self.assertIn("metrics", categories)
        self.assertIn("allocations", categories)
        self.assertIn("delivery", categories)
        self.assertIn("ai_impact", categories)
        self.assertIn("get_project_metrics_v2_data", categories["metrics"])
        self.assertIn(
            "get_org_metrics_v2_capitalization_data", categories["allocations"]
        )
        self.assertIn("get_forecast_v3", categories["delivery"])
        self.assertIn("get_ai_tool_impact", categories["ai_impact"])

    def test_tool_categories_match_registered_tools(self):
        mcp = FastMCP("Test")
        client = _DiscoveryClient()
        for register in (
            discovery.register_tools,
            metrics.register_tools,
            service_items.register_tools,
            users_teams.register_tools,
            org_projects.register_tools,
            ai_analytics.register_tools,
            dashboards.register_tools,
            employee.register_tools,
            forecasting.register_tools,
            labels.register_tools,
            alerts.register_tools,
            work_bundles.register_tools,
            risk_management.register_tools,
        ):
            register(mcp, client)

        registered = {tool.name for tool in _run(mcp.list_tools())}
        categorized = {
            tool_name
            for tool_names in discovery.TOOL_CATEGORIES.values()
            for tool_name in tool_names
        }

        self.assertEqual(registered - categorized, set())
        self.assertEqual(categorized - registered, set())


if __name__ == "__main__":
    unittest.main()
