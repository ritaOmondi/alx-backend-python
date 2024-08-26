#!/usr/bin/env python3
"""
This module contains the TestAccessNestedMap class, which is used to
test the access_nested_map function from the utils module.
"""

import unittest
from parameterized import parameterized

from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Test case class for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test the access_nested_map function with different input parameters.

        Args:
            nested_map (dict): The nested map to be accessed.
            path (tuple): The path to the desired value in the nested map.
            expected (any): The expected value to be returned by access_nested_map.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == '__main__':
    unittest.main()
