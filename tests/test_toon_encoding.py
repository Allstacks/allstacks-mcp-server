"""Tests for token-efficient response encoding."""

import json
import unittest

from allstacks_mcp.toon import encode_toon


class ToonEncodingTests(unittest.TestCase):
    def test_repeated_object_arrays_encode_as_tables(self):
        payload = {
            "count": 2,
            "results": [
                {"id": 1, "name": "Alpha", "active": True},
                {"id": 2, "name": "Beta", "active": False},
            ],
        }

        self.assertEqual(
            encode_toon(payload),
            "count: 2\nresults[2]{id,name,active}:\n1,Alpha,true\n2,Beta,false",
        )

    def test_strings_with_delimiters_are_quoted(self):
        payload = [{"id": 1, "name": "Alpha, Inc."}]

        self.assertEqual(encode_toon(payload), '[1]{id,name}:\n1,"Alpha, Inc."')

    def test_toon_is_smaller_for_repeated_metric_rows(self):
        payload = {
            "results": [
                {
                    "date": f"2026-05-{day:02d}",
                    "project_id": 10,
                    "metric_type": "Velocity",
                    "aggregate_value": day * 3,
                }
                for day in range(1, 32)
            ]
        }

        json_chars = len(json.dumps(payload, indent=2))
        toon_chars = len(encode_toon(payload))

        self.assertLess(toon_chars, json_chars * 0.5)


if __name__ == "__main__":
    unittest.main()
