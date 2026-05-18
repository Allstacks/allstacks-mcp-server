"""Live smoke test for repointed tool URLs.

The unit tests in ``test_tool_routes.py`` verify that each tool *builds* the
correct URL. This module verifies that the deployed API actually answers at
those URLs — i.e. that the URL contract this MCP server ships has not drifted
from production.

The harness is **opt-in**. It only runs when every environment variable
below is set; otherwise the whole module is skipped. There are no embedded
credentials and no defaults that point at production.

Required environment variables (HTTP Basic auth, matches ``server.py``):

- ``ALLSTACKS_MCP_LIVE_USERNAME``
- ``ALLSTACKS_MCP_LIVE_PASSWORD``
- ``ALLSTACKS_MCP_LIVE_BASE_URL``  (e.g. ``https://app.allstacks.com/api/v1/``)
- ``ALLSTACKS_MCP_LIVE_ORG_ID``
- ``ALLSTACKS_MCP_LIVE_PROJECT_ID``

Run only this module:

    ALLSTACKS_MCP_LIVE_USERNAME=... ALLSTACKS_MCP_LIVE_PASSWORD=... \
    ALLSTACKS_MCP_LIVE_BASE_URL=... ALLSTACKS_MCP_LIVE_ORG_ID=... \
    ALLSTACKS_MCP_LIVE_PROJECT_ID=... \
    uv run python -m unittest tests.test_live_routes
"""

import asyncio
import os
import unittest

from allstacks_mcp.client import AllstacksAPIClient

_REQUIRED_ENV = (
    "ALLSTACKS_MCP_LIVE_USERNAME",
    "ALLSTACKS_MCP_LIVE_PASSWORD",
    "ALLSTACKS_MCP_LIVE_BASE_URL",
    "ALLSTACKS_MCP_LIVE_ORG_ID",
    "ALLSTACKS_MCP_LIVE_PROJECT_ID",
)


def _missing_env() -> list:
    return [name for name in _REQUIRED_ENV if not os.environ.get(name)]


def _run(coro):
    return asyncio.run(coro)


def _assert_ok(test: unittest.TestCase, result, route: str) -> None:
    """Fail the test when the client returned an error envelope or a 404.

    Authorization-restricted endpoints (403) are tolerated — the goal here is
    to lock in URL correctness, not entitlements.
    """
    test.assertIsInstance(
        result, (dict, list), f"{route}: expected JSON, got {type(result).__name__}"
    )
    if isinstance(result, dict) and result.get("error"):
        status = result.get("status_code")
        test.assertNotEqual(
            status,
            404,
            f"{route}: 404 from deployed API — URL has drifted ({result.get('message')})",
        )
        test.assertNotIn(
            status,
            (None,),
            f"{route}: transport error reaching API ({result.get('message')})",
        )
        if status not in (401, 403):
            test.fail(f"{route}: unexpected error envelope {result}")


@unittest.skipUnless(
    not _missing_env(),
    f"Live route smoke tests skipped — set {', '.join(_REQUIRED_ENV)} to enable",
)
class LiveRouteSmokeTests(unittest.TestCase):
    """Hit each URL repointed in this PR plus a baseline known-good route.

    These should all answer 2xx, 401, or 403 — never 404. A 404 means the
    URL template in the tool no longer matches the deployed API.
    """

    @classmethod
    def setUpClass(cls):
        cls.client = AllstacksAPIClient(
            username=os.environ["ALLSTACKS_MCP_LIVE_USERNAME"],
            password=os.environ["ALLSTACKS_MCP_LIVE_PASSWORD"],
            base_url=os.environ["ALLSTACKS_MCP_LIVE_BASE_URL"],
        )
        cls.org_id = int(os.environ["ALLSTACKS_MCP_LIVE_ORG_ID"])
        cls.project_id = int(os.environ["ALLSTACKS_MCP_LIVE_PROJECT_ID"])

    def test_baseline_list_projects(self):
        route = f"organization/{self.org_id}/projects/"
        result = _run(self.client.request("GET", route, params={"limit": 1}))
        _assert_ok(self, result, route)

    def test_list_ai_reports_hyphenated_route(self):
        route = f"organization/{self.org_id}/ai-reports/"
        result = _run(self.client.request("GET", route, params={"limit": 1}))
        _assert_ok(self, result, route)

    def test_get_project_services_singular_route(self):
        route = f"project/{self.project_id}/service/"
        result = _run(self.client.request("GET", route))
        _assert_ok(self, result, route)

    def test_get_project_configuration_options_route(self):
        route = f"project/{self.project_id}/configuration_options/"
        result = _run(self.client.request("GET", route))
        _assert_ok(self, result, route)

    def test_get_project_flat_route(self):
        route = f"project/{self.project_id}/"
        result = _run(self.client.request("GET", route))
        _assert_ok(self, result, route)

    def test_list_work_bundles_initial_route(self):
        route = f"project/{self.project_id}/work_bundles/initial/"
        result = _run(self.client.request("GET", route))
        _assert_ok(self, result, route)

    def test_list_project_risk_definitions_route(self):
        route = f"project/{self.project_id}/risk_definitions/"
        result = _run(self.client.request("GET", route))
        _assert_ok(self, result, route)


if __name__ == "__main__":
    unittest.main()
