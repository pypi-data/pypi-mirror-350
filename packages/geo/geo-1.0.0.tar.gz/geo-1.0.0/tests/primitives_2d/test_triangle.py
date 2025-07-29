# (1) python tests/primitives_2d/test_triangle.py
# (2) python -m unittest tests/primitives_2d/test_triangle.py (verbose output) (auto add sys.path)

from __future__ import annotations

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Triangle
from geo.core import Point2D
from geo.core.precision import DEFAULT_EPSILON, is_equal


class TestTriangleConstructor(unittest.TestCase):
    def test_collinear_points_raises(self):
        with self.assertRaises(ValueError):
            Triangle(Point2D(0, 0), Point2D(1, 1), Point2D(2, 2))

    def test_duplicate_points_raises(self):
        p = Point2D(0, 0)
        with self.assertRaises(ValueError):
            Triangle(p, p, Point2D(1, 0))


class TestTriangleMetrics(unittest.TestCase):
    def setUp(self):
        # Classic 3‑4‑5 right triangle
        self.t = Triangle(Point2D(0, 0), Point2D(4, 0), Point2D(0, 3))

    def test_area(self):
        self.assertAlmostEqual(self.t.area, 6.0)

    def test_centroid(self):
        c = self.t.centroid()
        self.assertAlmostEqual(c.x, 4/3)
        self.assertAlmostEqual(c.y, 1.0)

    def test_side_lengths(self):
        if hasattr(self.t, "side_lengths"):
            a, b, c = sorted(self.t.side_lengths)  # type: ignore[attr-defined]
            self.assertTrue(is_equal(a, 3))
            self.assertTrue(is_equal(b, 4))
            self.assertTrue(is_equal(c, 5))
        else:
            self.skipTest("Triangle.side_lengths not implemented")

    def test_perimeter(self):
        if hasattr(self.t, "perimeter"):
            self.assertAlmostEqual(self.t.perimeter, 12.0)  # 3+4+5
        else:
            self.skipTest("Triangle.perimeter not implemented")

    def test_is_right(self):
        if hasattr(self.t, "is_right"):
            self.assertTrue(self.t.is_right())
        else:
            self.skipTest("Triangle.is_right() not implemented")


class TestTriangleContainsPoint(unittest.TestCase):
    def setUp(self):
        self.t = Triangle(Point2D(0, 0), Point2D(5, 0), Point2D(0, 5))

    def test_inside(self):
        self.assertTrue(self.t.contains_point(Point2D(1, 1)))

    def test_boundary(self):
        self.assertTrue(self.t.contains_point(Point2D(0, 2)))
        self.assertTrue(self.t.contains_point(Point2D(2.5, 2.5)))

    def test_outside(self):
        self.assertFalse(self.t.contains_point(Point2D(3, 3.1)))

    def test_near_boundary_epsilon(self):
        near = Point2D(0, -DEFAULT_EPSILON/2)
        self.assertTrue(self.t.contains_point(near))


class TestTriangleSpecialTypes(unittest.TestCase):
    def test_equilateral_properties(self):
        t = Triangle(Point2D(0, 0), Point2D(1, 0), Point2D(0.5, math.sqrt(3)/2))
        if hasattr(t, "is_equilateral"):
            self.assertTrue(t.is_equilateral())
        if hasattr(t, "is_isosceles"):
            self.assertTrue(t.is_isosceles())
        if hasattr(t, "is_scalene"):
            self.assertFalse(t.is_scalene())


if __name__ == "__main__":
    unittest.main()
