import unittest
from typing import Any, Dict, cast

import numpy as np

from midas.util.dict_util import (  # replace with actual module name
    bool_from_dict,
    convert,
    convert_list,
    convert_val,
    set_default_bool,
    set_default_float,
    set_default_int,
    strtobool,
    tobool,
    update,
)


class TestDictUtils(unittest.TestCase):
    def test_update(self):
        a = {"a": 1, "b": {"x": 1}}
        b = {"b": {"y": 2}, "c": 3}
        result = update(a, b)
        self.assertEqual(result, {"a": 1, "b": {"x": 1, "y": 2}, "c": 3})

    def test_convert_basic(self):
        d = {
            "a": np.int32(5),
            "b": np.float64(3.14),
            "c": np.array([1, 2, 3]),
            "d": None,
        }
        converted = convert(d.copy())
        self.assertEqual(converted["a"], 5)
        self.assertEqual(converted["b"], 3.14)
        for x, y in zip(converted["c"], [1, 2, 3]):
            self.assertEqual(x, y)
        self.assertIsNone(converted["d"])

    def test_convert_nested(self):
        d = {
            "a": {"b": np.int16(2)},
            "c": [np.float32(1.2), {"d": np.int64(4)}],
        }
        result = convert(d.copy())
        self.assertEqual(result["a"]["b"], 2)
        self.assertIsInstance(
            result["c"][0], float, msg=f"Got type {type(result['c'][0])}"
        )
        self.assertEqual(result["c"][0], 1.2)
        self.assertEqual(result["c"][1]["d"], 4)

    def test_convert_list(self):
        arr = [1, np.float32(2.5), {"x": np.int64(3)}]
        result = convert_list(arr)
        self.assertEqual(result, [1, 2.5, {"x": 3}])

    def test_convert_val(self):
        self.assertEqual(convert_val(np.int32(5)), 5)
        self.assertEqual(convert_val(np.float64(3.14)), 3.14)
        self.assertEqual(convert_val("True"), True)
        self.assertEqual(convert_val("5"), 5)
        self.assertEqual(convert_val("3.14"), 3.14)
        self.assertEqual(convert_val("some string"), "some string")
        self.assertIsNone(convert_val("None"))
        self.assertEqual(convert_val(None), None)

    def test_strtobool(self):
        true_vals = ["y", "yes", "t", "true", "on", "1"]
        false_vals = ["n", "no", "f", "false", "off", "0"]
        for val in true_vals:
            self.assertTrue(strtobool(val))
        for val in false_vals:
            self.assertFalse(strtobool(val))
        with self.assertRaises(ValueError):
            strtobool("maybe")

    def test_tobool(self):
        self.assertTrue(tobool(True))
        self.assertFalse(tobool(False))
        self.assertTrue(tobool(1))
        self.assertFalse(tobool(0))
        self.assertTrue(tobool(0.1))
        self.assertFalse(tobool(0.0))
        self.assertTrue(tobool("yes"))
        self.assertFalse(tobool("no"))
        with self.assertRaises(ValueError):
            tobool(cast(Any, None))

    def test_bool_from_dict(self):
        d: Dict[str, Any] = {"a": "yes", "b": "no"}
        self.assertTrue(bool_from_dict(d, "a"))
        self.assertFalse(bool_from_dict(d, "b"))
        self.assertEqual(bool_from_dict(d, "c", default=True), True)

    def test_set_default_bool(self):
        d: Dict[str, Any] = {"x": "yes"}
        set_default_bool(d, "x", default=False)
        set_default_bool(d, "y", default=True)
        self.assertEqual(d["x"], "yes")
        self.assertEqual(d["y"], True)

    def test_set_default_float(self):
        d = {"x": "3.14"}
        set_default_float(d, "x")
        set_default_float(d, "y", 1.5)
        self.assertEqual(d["x"], 3.14)
        self.assertEqual(d["y"], 1.5)

    def test_set_default_int(self):
        d = {"x": "42"}
        set_default_int(d, "x")
        set_default_int(d, "y", 10)
        self.assertEqual(d["x"], 42)
        self.assertEqual(d["y"], 10)


if __name__ == "__main__":
    unittest.main()
