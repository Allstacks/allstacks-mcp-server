"""Verify URL templates for tools whose routes were known to be incorrect.

These guard against regressions of the route-drift fixes called out in the
MCP test findings.
"""

import asyncio
import unittest

from mcp.server.fastmcp import FastMCP

from allstacks_mcp.tools import ai_analytics, org_projects


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
        return {"ok": True}


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


if __name__ == "__main__":
    unittest.main()
