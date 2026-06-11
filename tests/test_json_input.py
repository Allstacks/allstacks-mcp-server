"""Unit tests for the shared JSON-input parameter helper."""

import unittest

from allstacks_mcp._json_input import (
    _coerce_json_array,
    _coerce_json_object,
    _coerce_json_value,
    parse_json_input,
)


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


class CoerceJsonInputTests(unittest.TestCase):
    def test_coerce_json_object_accepts_dict(self):
        value = {"metric": "Velocity"}
        self.assertIs(_coerce_json_object(value), value)

    def test_coerce_json_value_accepts_dict(self):
        value = {"metric": "Velocity"}
        self.assertIs(_coerce_json_value(value), value)

    def test_coerce_json_value_accepts_list(self):
        value = [1, 2, 3]
        self.assertIs(_coerce_json_value(value), value)

    def test_coerce_json_object_parses_string(self):
        self.assertEqual(
            _coerce_json_object('{"metric": "Velocity"}'), {"metric": "Velocity"}
        )

    def test_coerce_json_object_rejects_array(self):
        with self.assertRaises(ValueError):
            _coerce_json_object("[1, 2]")

    def test_coerce_json_object_rejects_invalid_json_with_details(self):
        with self.assertRaises(ValueError) as cm:
            _coerce_json_object("not json")
        self.assertIn("Invalid JSON string:", str(cm.exception))

    def test_coerce_json_value_accepts_array(self):
        self.assertEqual(_coerce_json_value("[1, 2]"), [1, 2])

    def test_coerce_json_value_rejects_scalars(self):
        for value in (123, True, None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _coerce_json_value(value)

    def test_coerce_json_array_accepts_array(self):
        value = ["email", "slack"]
        self.assertIs(_coerce_json_array(value), value)

    def test_coerce_json_array_rejects_object(self):
        with self.assertRaises(ValueError):
            _coerce_json_array('{"channel": "email"}')


if __name__ == "__main__":
    unittest.main()
