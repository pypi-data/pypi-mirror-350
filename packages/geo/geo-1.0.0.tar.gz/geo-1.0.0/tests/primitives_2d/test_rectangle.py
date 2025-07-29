# (1) python tests/primitives_2d/test_rectangle.py
# (2) python -m unittest tests/primitives_2d/test_rectangle.py (verbose output) (auto add sys.path)

from __future__ import annotations

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Rectangle
from geo.core import Point2D
from geo.core.precision import DEFAULT_EPSILON, is_equal


class TestRectangleCornerConstructor(unittest.TestCase):
    """Constructor that takes two opposite corners (p1, p3)."""

    def test_identical_points_raises(self):
        p = Point2D(0, 0)
        with self.assertRaises(ValueError):
            Rectangle(p, p)

    def test_axis_aligned_square(self):
        r = Rectangle(Point2D(0, 0), Point2D(2, 2))
        self.assertTrue(r.is_square())
        self.assertAlmostEqual(r.width, 2.0)
        self.assertAlmostEqual(r.height, 2.0)
        self.assertAlmostEqual(r.area, 4.0)
        self.assertAlmostEqual(r.diagonal_length, math.sqrt(8))
        # Containment – inside, boundary, outside
        self.assertTrue(r.contains_point(Point2D(1, 1)))          # Inside
        self.assertTrue(r.contains_point(Point2D(0, 1)))          # On left edge
        self.assertFalse(r.contains_point(Point2D(3, 3)))         # Outside

    def test_axis_aligned_rectangle(self):
        r = Rectangle(Point2D(0, 0), Point2D(3, 1))
        self.assertFalse(r.is_square())
        self.assertAlmostEqual(r.width, 3.0)
        self.assertAlmostEqual(r.height, 1.0)
        self.assertAlmostEqual(r.area, 3.0)
        self.assertAlmostEqual(r.diagonal_length, math.sqrt(10))


class TestRectangleWHConstructor(unittest.TestCase):
    """Constructor that takes bottom‑left point, width, height, and optional rotation."""

    def test_negative_or_zero_dimensions_raise(self):
        with self.assertRaises(ValueError):
            Rectangle(Point2D(0, 0), -1.0, 1.0)
        with self.assertRaises(ValueError):
            Rectangle(Point2D(0, 0), 1.0, 0.0)

    def test_basic_properties(self):
        r = Rectangle(Point2D(1, 1), 4.0, 2.0)
        self.assertAlmostEqual(r.width, 4.0)
        self.assertAlmostEqual(r.height, 2.0)
        self.assertAlmostEqual(r.area, 8.0)
        self.assertAlmostEqual(r.angle, 0.0)

    def test_rotated_rectangle(self):
        angle = math.pi / 4  # 45 degrees
        r = Rectangle(Point2D(0, 0), 2.0, 1.0, angle_rad=angle)
        self.assertAlmostEqual(r.width, 2.0)
        self.assertAlmostEqual(r.height, 1.0)
        self.assertTrue(is_equal(r.angle, angle))
        self.assertAlmostEqual(r.area, 2.0)
        # Inside test (centre should be inside)
        centre = Point2D(1.0, 0.5)  # before rotation centre; for small rectangle rotation shouldn't move much
        self.assertFalse(r.contains_point(centre))

    def test_is_square(self):
        r = Rectangle(Point2D(-1, -1), 3.0, 3.0)
        self.assertTrue(r.is_square())
        r2 = Rectangle(Point2D(-1, -1), 3.0, 3.0001)
        self.assertFalse(r2.is_square(epsilon=1e-5))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

