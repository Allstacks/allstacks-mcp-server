"""Unit tests for Metrics V2 POST body construction."""

import json
import unittest

from allstacks_mcp.metrics_v2_payload import build_metrics_v2_post_body


class BuildMetricsV2PostBodyTests(unittest.TestCase):
    def test_inner_config_only_wraps(self):
        inner = {
            "views": [{"dimensions": [{"property": "id"}]}],
            "filters": {"default": {"item_type": "CARD"}},
        }
        body = build_metrics_v2_post_body(json.dumps(inner))
        self.assertEqual(
            body,
            {"config": inner, "get_count_only": False, "variables": {}},
        )

    def test_full_envelope_passthrough(self):
        inner = {"views": []}
        envelope = {"config": inner, "get_count_only": True, "variables": {"a": 1}}
        body = build_metrics_v2_post_body(json.dumps(envelope))
        self.assertEqual(body["config"], inner)
        self.assertTrue(body["get_count_only"])
        self.assertEqual(body["variables"], {"a": 1})

    def test_inner_plus_tool_get_count_only(self):
        inner = {"views": []}
        body = build_metrics_v2_post_body(json.dumps(inner), get_count_only=True)
        self.assertTrue(body["get_count_only"])

    def test_envelope_get_count_false_but_tool_true(self):
        envelope = {"config": {"views": []}, "get_count_only": False, "variables": {}}
        body = build_metrics_v2_post_body(json.dumps(envelope), get_count_only=True)
        self.assertTrue(body["get_count_only"])

    def test_variables_string_override(self):
        inner = {"views": []}
        body = build_metrics_v2_post_body(json.dumps(inner), variables='{"x": 1}')
        self.assertEqual(body["variables"], {"x": 1})

    def test_invalid_json_raises(self):
        with self.assertRaises(ValueError):
            build_metrics_v2_post_body("not json")

    def test_views_only_dict_wrapped_as_inner_config(self):
        inner = {"views": [], "filters": {}}
        body = build_metrics_v2_post_body(json.dumps(inner))
        self.assertEqual(body["config"], inner)


if __name__ == "__main__":
    unittest.main()
