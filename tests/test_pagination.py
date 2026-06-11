"""Unit tests for list response pagination helpers."""

import unittest

from allstacks_mcp._pagination import cap_list_payload


class CapListPayloadTests(unittest.TestCase):
    def test_caps_top_level_list(self):
        payload = [{"id": i} for i in range(30)]
        capped = cap_list_payload(payload, limit=10, offset=0)
        self.assertEqual(len(capped), 10)

    def test_applies_offset_on_top_level_list(self):
        payload = [{"id": i} for i in range(30)]
        capped = cap_list_payload(payload, limit=10, offset=5)
        self.assertEqual([row["id"] for row in capped], list(range(5, 15)))

    def test_leaves_correctly_paged_results_unchanged(self):
        payload = {"count": 30, "results": [{"id": i} for i in range(10)]}
        self.assertIs(cap_list_payload(payload, limit=10), payload)

    def test_caps_oversized_results_wrapper(self):
        payload = {"count": 30, "results": [{"id": i} for i in range(30)]}
        capped = cap_list_payload(payload, limit=10, offset=0)
        self.assertEqual(len(capped["results"]), 10)
        self.assertEqual(capped["count"], 30)


if __name__ == "__main__":
    unittest.main()
