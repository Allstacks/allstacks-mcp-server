"""Verify MCP tool input schemas accept client-pre-parsed JSON objects."""

import asyncio
import json
import unittest

from mcp.server.fastmcp import FastMCP

from allstacks_mcp.tools import alerts, metrics, org_projects


class _MetricsClient:
    def __init__(self):
        self.last = None

    async def request_text(self, method, endpoint, params=None, data=None, **kwargs):
        self.last = {
            "method": method,
            "endpoint": endpoint,
            "params": params,
            "data": data,
        }
        return "{}"


class _ProjectsClient:
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
            return [{"id": i, "name": f"project-{i}"} for i in range(30)]
        return {"ok": True}


def _run(coro):
    return asyncio.run(coro)


def _tool_text(result) -> str:
    content = result[0] if isinstance(result, tuple) else result
    return content[0].text


class JsonObjectToolSignatureTests(unittest.TestCase):
    def test_get_project_metrics_v2_data_schema_is_object_not_string(self):
        mcp = FastMCP("Test")
        metrics.register_tools(mcp, _MetricsClient())
        tools = _run(mcp.list_tools())
        tool = next(t for t in tools if t.name == "get_project_metrics_v2_data")
        config_schema = tool.inputSchema["properties"]["config"]
        self.assertEqual(config_schema.get("type"), "object")
        self.assertNotIn("anyOf", config_schema)

    def test_get_project_metrics_v2_data_accepts_pre_parsed_dict(self):
        mcp = FastMCP("Test")
        client = _MetricsClient()
        metrics.register_tools(mcp, client)
        _run(
            mcp.call_tool(
                "get_project_metrics_v2_data",
                {
                    "project_id": 1,
                    "config": {"views": [], "filters": {}},
                },
            )
        )
        self.assertIsInstance(client.last["data"]["config"], dict)

    def test_get_project_metrics_v2_data_accepts_json_string(self):
        mcp = FastMCP("Test")
        client = _MetricsClient()
        metrics.register_tools(mcp, client)
        _run(
            mcp.call_tool(
                "get_project_metrics_v2_data",
                {"project_id": 1, "config": '{"views": []}'},
            )
        )
        self.assertEqual(client.last["data"]["config"], {"views": []})

    def test_subscribe_to_alert_channels_schema_is_array(self):
        mcp = FastMCP("Test")
        alerts.register_tools(mcp, _MetricsClient())
        tools = _run(mcp.list_tools())
        tool = next(t for t in tools if t.name == "subscribe_to_alert")
        channels_schema = tool.inputSchema["properties"]["channels"]
        self.assertEqual(channels_schema.get("type"), "array")


class ListProjectsPaginationTests(unittest.TestCase):
    def test_list_projects_forwards_limit_param(self):
        mcp = FastMCP("Test")
        client = _ProjectsClient()
        org_projects.register_tools(mcp, client)
        _run(mcp.call_tool("list_projects", {"org_id": 7, "limit": 10}))
        self.assertEqual(client.last["params"]["limit"], 10)

    def test_list_projects_caps_oversized_list_response(self):
        mcp = FastMCP("Test")
        client = _ProjectsClient()
        org_projects.register_tools(mcp, client)
        result = _run(mcp.call_tool("list_projects", {"org_id": 7, "limit": 10}))
        payload = json.loads(_tool_text(result))
        self.assertEqual(len(payload), 10)


if __name__ == "__main__":
    unittest.main()
