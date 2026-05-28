"""Tests for the HTTP client's error and decoding behavior.

These cover the failure modes the MCP test report flagged:
- 4xx/5xx responses surface ``status_code`` so consumers can branch on it
- Non-JSON 2xx bodies (e.g. proxy / SSO interstitials) no longer crash the
  caller; they come back as a structured error envelope with the raw body.
"""

import asyncio
import unittest

import httpx

from allstacks_mcp.client import AllstacksAPIClient


def _run(coro):
    return asyncio.run(coro)


class ClientErrorHandlingTests(unittest.TestCase):
    def _build_client(self, transport: httpx.MockTransport) -> AllstacksAPIClient:
        client = AllstacksAPIClient("u", "p", "https://example.test/api/v1/")
        # Inject the mock transport by monkey-patching httpx.AsyncClient. The
        # AllstacksAPIClient creates its own AsyncClient per request, so we
        # patch the constructor to inject the transport.
        original = httpx.AsyncClient

        def _factory(*args, **kwargs):
            kwargs["transport"] = transport
            return original(*args, **kwargs)

        self._async_client_patch = original
        httpx.AsyncClient = _factory  # type: ignore[assignment]
        self.addCleanup(self._restore_async_client)
        return client

    def _restore_async_client(self):
        httpx.AsyncClient = self._async_client_patch  # type: ignore[assignment]

    def test_404_returns_status_code(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "not found"})

        client = self._build_client(httpx.MockTransport(handler))
        result = _run(client.request("GET", "missing/"))
        self.assertTrue(result.get("error"))
        self.assertEqual(result["status_code"], 404)

    def test_500_returns_status_code(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="boom")

        client = self._build_client(httpx.MockTransport(handler))
        result = _run(client.request("GET", "explode/"))
        self.assertTrue(result.get("error"))
        self.assertEqual(result["status_code"], 500)

    def test_200_with_html_body_returns_structured_error(self):
        """A 2xx with non-JSON body must not raise — it must surface as a
        structured error with the raw body so consumers can diagnose."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                text="<html>session expired</html>",
                headers={"Content-Type": "text/html"},
            )

        client = self._build_client(httpx.MockTransport(handler))
        result = _run(client.request("GET", "ok-but-html/"))
        self.assertTrue(result.get("error"))
        self.assertEqual(result["status_code"], 200)
        self.assertIn("<html>", result["raw_body"])

    def test_200_json_parses_normally(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"ok": True})

        client = self._build_client(httpx.MockTransport(handler))
        result = _run(client.request("GET", "good/"))
        self.assertEqual(result, {"ok": True})

    def test_default_openapi_schema_url_uses_api_schema_route(self):
        client = AllstacksAPIClient("u", "p", "https://example.test/api/v1/")
        self.assertEqual(
            client.openapi_schema_url,
            "https://example.test/api/v1/schema/",
        )

    def test_get_openapi_schema_uses_configured_absolute_url(self):
        seen_urls = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_urls.append(str(request.url))
            return httpx.Response(200, json={"openapi": "3.0.3"})

        client = self._build_client(httpx.MockTransport(handler))
        client.openapi_schema_url = "https://docs.example.test/openapi.json"

        result = _run(client.get_openapi_schema())

        self.assertEqual(result, {"openapi": "3.0.3"})
        self.assertEqual(seen_urls, ["https://docs.example.test/openapi.json"])

    def test_request_error_returns_none_status_code(self):
        """Transport-layer failures surface as a structured error with status_code=None."""

        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("network down", request=request)

        client = self._build_client(httpx.MockTransport(handler))
        result = _run(client.request("GET", "offline/"))
        self.assertTrue(result.get("error"))
        self.assertIsNone(result["status_code"])
        self.assertIn("Request failed", result["message"])


if __name__ == "__main__":
    unittest.main()
