"""Unit tests for the shared JSON-input parameter helper."""

import unittest

from allstacks_mcp._json_input import parse_json_input


class ParseJsonInputTests(unittest.TestCase):
    def test_passes_dict_through(self):
        value = {"a": 1, "b": [2, 3]}
        self.assertEqual(parse_json_input(value), value)

    def test_passes_list_through(self):
        value = [{"a": 1}, {"b": 2}]
        self.assertEqual(parse_json_input(value), value)

    def test_decodes_json_string(self):
        self.assertEqual(parse_json_input('{"a": 1}'), {"a": 1})
        self.assertEqual(parse_json_input("[1, 2, 3]"), [1, 2, 3])

    def test_invalid_json_raises_with_name(self):
        with self.assertRaises(ValueError) as cm:
            parse_json_input("not json", name="config")
        self.assertIn("config", str(cm.exception))

    def test_unsupported_type_raises_with_name(self):
        with self.assertRaises(ValueError) as cm:
            parse_json_input(123, name="payload")  # type: ignore[arg-type]
        self.assertIn("payload", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
