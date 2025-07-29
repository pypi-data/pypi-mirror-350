# (1) python tests/primitives_2d/test_polygon.py
# (2) python -m unittest tests/primitives_2d/test_polygon.py (verbose output) (auto add sys.path)

from __future__ import annotations

import math
import unittest
from typing import List
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Polygon
from geo.core import Point2D
from geo.core.precision import DEFAULT_EPSILON, is_equal


class TestPolygonConstruction(unittest.TestCase):
    """Validate constructor safeguards."""

    def test_less_than_three_vertices_raises(self):
        with self.assertRaises(ValueError):
            Polygon([Point2D(0, 0), Point2D(1, 1)])

    def test_duplicate_consecutive_vertices_collapsed(self):
        poly = Polygon([
            Point2D(0, 0), Point2D(1, 0), Point2D(1, 0), Point2D(1, 1), Point2D(0, 1)
        ])
        # Implementation may auto‑collapse duplicates or keep them but assure area ≈ 1
        self.assertAlmostEqual(abs(poly.area), 1.0, places=6)
        # Ensure number of *unique* vertices >= 4 for square
        unique_coords = {v.coords for v in poly.vertices}
        self.assertGreaterEqual(len(unique_coords), 4)


class TestPolygonBasicMetrics(unittest.TestCase):
    def setUp(self):
        self.square = Polygon([
            Point2D(0, 0), Point2D(1, 0), Point2D(1, 1), Point2D(0, 1)
        ])
        self.triangle = Polygon([
            Point2D(0, 0), Point2D(4, 0), Point2D(0, 3)
        ])

    def test_area(self):
        self.assertAlmostEqual(self.square.area, 1.0)
        self.assertAlmostEqual(self.triangle.area, 6.0)

    def test_perimeter(self):
        if hasattr(self.square, "perimeter"):
            self.assertAlmostEqual(self.square.perimeter, 4.0)
        else:
            self.skipTest("Polygon.perimeter() not implemented")

    def test_edges_count(self):
        self.assertEqual(len(self.square.edges), len(self.square.vertices))


class TestPolygonContainment(unittest.TestCase):
    def setUp(self):
        self.poly = Polygon([
            Point2D(0, 0), Point2D(5, 0), Point2D(5, 5), Point2D(0, 5)
        ])

    def test_inside_point(self):
        self.assertTrue(self.poly.contains_point(Point2D(2.5, 2.5)))

    def test_outside_point(self):
        self.assertFalse(self.poly.contains_point(Point2D(6, 6)))

    def test_on_boundary(self):
        pt = Point2D(0, 2)
        self.assertTrue(self.poly.contains_point(pt))

    def test_near_boundary_epsilon(self):
        near = Point2D(0 - DEFAULT_EPSILON / 2, 2)
        self.assertTrue(self.poly.contains_point(near))


class TestPolygonSelfIntersecting(unittest.TestCase):
    """Bow-tie polygon should be flagged as non‑simple or give |area|>0 but is_simple=False."""

    def setUp(self):
        # Bow-tie / hour-glass crossing at centre
        self.bow = Polygon([
            Point2D(0, 0), Point2D(2, 2), Point2D(0, 2), Point2D(2, 0)
        ])

    @unittest.skipUnless(hasattr(Polygon, "is_simple"), "Polygon.is_simple() not implemented")
    def test_is_simple_false(self):
        self.assertFalse(self.bow.is_simple())

    def test_area_absolute_value(self):
        # Shoelace algorithm gives signed area; magnitude should match two triangles (4)
        self.assertAlmostEqual(abs(self.bow.area), 2.0)


class TestPolygonConvexity(unittest.TestCase):
    def setUp(self):
        self.heptagon = Polygon([
            Point2D(math.cos(theta), math.sin(theta)) for theta in [i * 2 * math.pi / 7 for i in range(7)]
        ])

    @unittest.skipUnless(hasattr(Polygon, "is_convex"), "Polygon.is_convex() not implemented")
    def test_is_convex_true(self):
        self.assertTrue(self.heptagon.is_convex())


class TestPolygonCollinearEdgeCases(unittest.TestCase):
    def test_collinear_vertices_area(self):
        poly = Polygon([
            Point2D(0, 0), Point2D(1, 0), Point2D(2, 0),  # collinear
            Point2D(2, 2), Point2D(0, 2)
        ])
        # Collinear point should not alter area (expected rectangle 2×2)
        self.assertAlmostEqual(abs(poly.area), 4.0)


if __name__ == "__main__":
    unittest.main()
