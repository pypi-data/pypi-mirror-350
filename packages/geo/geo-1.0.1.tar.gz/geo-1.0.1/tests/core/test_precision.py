# (1) python tests/core/test_precision.py
# (2) python -m unittest tests/core/test_precision.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core.precision import (
    DEFAULT_EPSILON, is_equal, is_zero, is_positive, is_negative
)


class TestPrecision(unittest.TestCase):

    def test_default_epsilon(self):
        self.assertAlmostEqual(DEFAULT_EPSILON, 1e-9)

    def test_is_equal(self):
        self.assertTrue(is_equal(1.0, 1.0000000001))
        self.assertTrue(is_equal(1.0, 1.0 + DEFAULT_EPSILON / 2))
        self.assertFalse(is_equal(1.0, 1.0 + DEFAULT_EPSILON * 2))
        self.assertTrue(is_equal(0.0, 0.0))
        self.assertTrue(is_equal(-1.0, -1.0000000001))
        self.assertTrue(is_equal(1.23456789, 1.23456789))
        self.assertFalse(is_equal(1.0, 2.0))
        # Test with custom epsilon
        self.assertTrue(is_equal(1.0, 1.001, epsilon=1e-2))
        self.assertFalse(is_equal(1.0, 1.001, epsilon=1e-4))

    def test_is_zero(self):
        self.assertTrue(is_zero(0.0))
        self.assertTrue(is_zero(DEFAULT_EPSILON / 2))
        self.assertFalse(is_zero(DEFAULT_EPSILON * 2))
        self.assertTrue(is_zero(-DEFAULT_EPSILON / 2))
        self.assertFalse(is_zero(-DEFAULT_EPSILON * 2))
        self.assertFalse(is_zero(1.0))
        # Test with custom epsilon
        self.assertTrue(is_zero(0.001, epsilon=1e-2))
        self.assertFalse(is_zero(0.001, epsilon=1e-4))

    def test_is_positive(self):
        self.assertTrue(is_positive(1.0))
        self.assertTrue(is_positive(DEFAULT_EPSILON * 2))
        self.assertFalse(is_positive(DEFAULT_EPSILON / 2)) # Too close to zero
        self.assertFalse(is_positive(0.0))
        self.assertFalse(is_positive(-1.0))
        # Test with custom epsilon
        self.assertTrue(is_positive(0.001, epsilon=1e-4))
        self.assertFalse(is_positive(0.00001, epsilon=1e-4))


    def test_is_negative(self):
        self.assertTrue(is_negative(-1.0))
        self.assertTrue(is_negative(-DEFAULT_EPSILON * 2))
        self.assertFalse(is_negative(-DEFAULT_EPSILON / 2)) # Too close to zero
        self.assertFalse(is_negative(0.0))
        self.assertFalse(is_negative(1.0))
        # Test with custom epsilon
        self.assertTrue(is_negative(-0.001, epsilon=1e-4))
        self.assertFalse(is_negative(-0.00001, epsilon=1e-4))

if __name__ == '__main__':
    unittest.main()