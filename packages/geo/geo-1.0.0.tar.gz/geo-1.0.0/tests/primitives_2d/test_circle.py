# (1) python tests/primitives_2d/test_circle.py
# (2) python -m unittest tests/primitives_2d/test_circle.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Circle, Line2D
from geo.core import Point2D, Vector2D
from geo.core.precision import DEFAULT_EPSILON, is_equal


class TestCircleBasics(unittest.TestCase):
    """Constructor, repr, equality, basic properties."""

    def test_constructor_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            Circle(Point2D(0, 0), -1)

    def test_zero_radius(self):
        c = Circle(Point2D(1, 1), 0)
        self.assertEqual(c.area, 0.0)
        self.assertEqual(c.circumference, 0.0)
        # Only the centre is contained
        self.assertTrue(c.contains_point(Point2D(1, 1)))
        self.assertFalse(c.contains_point(Point2D(1, 1 + DEFAULT_EPSILON * 10)))
        # on_boundary should regard the centre as boundary when r==0
        self.assertTrue(c.on_boundary(Point2D(1, 1)))

    def test_area_circumference_formulae(self):
        r = 3.5
        c = Circle(Point2D(0, 0), r)
        self.assertAlmostEqual(c.area, math.pi * r ** 2)
        self.assertAlmostEqual(c.circumference, 2 * math.pi * r)

    def test_equality_with_tolerance(self):
        c1 = Circle(Point2D(0, 0), 2.0)
        c2 = Circle(Point2D(0, 0), 2.0 + DEFAULT_EPSILON / 2)
        self.assertEqual(c1, c2)


class TestCircleContainment(unittest.TestCase):
    def setUp(self):
        self.circle = Circle(Point2D(0, 0), 5)

    def test_contains_point_inside(self):
        self.assertTrue(self.circle.contains_point(Point2D(3, 4)))  # distance 5, on boundary
        self.assertTrue(self.circle.contains_point(Point2D(0, 0)))  # centre
        self.assertTrue(self.circle.on_boundary(Point2D(3, 4)))

    def test_contains_point_outside(self):
        self.assertFalse(self.circle.contains_point(Point2D(6, 0)))
        # Just outside boundary but within epsilon → still True due to tolerance
        self.assertTrue(self.circle.contains_point(Point2D(5 + DEFAULT_EPSILON / 2, 0)))


class TestCircleLineIntersection(unittest.TestCase):
    """Secant, tangent, and disjoint cases."""

    def setUp(self):
        self.circle = Circle(Point2D(0, 0), 5)
        self.horizontal_center = Line2D(Point2D(-10, 0), Point2D(10, 0))  # Through centre
        self.horizontal_top_tangent = Line2D(Point2D(-10, 5), Vector2D(1, 0))
        self.horizontal_above = Line2D(Point2D(-10, 6), Vector2D(1, 0))

    def test_secant_two_points(self):
        pts = self.circle.intersection_with_line(self.horizontal_center)
        self.assertEqual(len(pts), 2)
        # Points should be (-5,0) and (5,0) regardless of ordering
        xs = sorted(p.x for p in pts)
        self.assertTrue(is_equal(xs[0], -5) and is_equal(xs[1], 5))
        self.assertTrue(all(is_equal(p.y, 0) for p in pts))

    def test_tangent_one_point(self):
        pts = self.circle.intersection_with_line(self.horizontal_top_tangent)
        self.assertEqual(len(pts), 1)
        self.assertAlmostEqual(pts[0].x, 0.0)
        self.assertAlmostEqual(pts[0].y, 5.0)

    def test_no_intersection_disjoint(self):
        self.assertEqual(self.circle.intersection_with_line(self.horizontal_above), [])


class TestCircleCircleIntersection(unittest.TestCase):
    """Validate circle‑circle intersection helper in Circle.intersection_with_circle"""

    def test_two_points(self):
        c1 = Circle(Point2D(0, 0), 5)
        c2 = Circle(Point2D(8, 0), 5)
        pts = c1.intersection_with_circle(c2)
        self.assertEqual(len(pts), 2)
        # y coordinates should be symmetric
        self.assertAlmostEqual(pts[0].y, -pts[1].y)
        self.assertTrue(all(is_equal(p.x, 4) for p in pts))

    def test_tangent_external(self):
        c1 = Circle(Point2D(0, 0), 5)
        c2 = Circle(Point2D(10, 0), 5)
        pts = c1.intersection_with_circle(c2)
        self.assertEqual(len(pts), 1)
        self.assertAlmostEqual(pts[0].x, 5.0)
        self.assertAlmostEqual(pts[0].y, 0.0)

    def test_tangent_internal(self):
        c1 = Circle(Point2D(0, 0), 5)
        c2 = Circle(Point2D(0, 0), 2)
        # Internal tangency when radius difference equals distance (here d=0, handled as containment)
        # Shift c2 a bit to make them internally tangent at (3,0)
        c2 = Circle(Point2D(3, 0), 2)
        pts = c1.intersection_with_circle(c2)
        self.assertEqual(len(pts), 1)
        self.assertAlmostEqual(pts[0].x, 5.0)
        self.assertAlmostEqual(pts[0].y, 0.0)

    def test_disjoint(self):
        c1 = Circle(Point2D(0, 0), 5)
        c2 = Circle(Point2D(20, 0), 5)
        self.assertEqual(c1.intersection_with_circle(c2), [])

    def test_contained_no_intersection(self):
        big = Circle(Point2D(0, 0), 5)
        small = Circle(Point2D(1, 1), 1)
        self.assertEqual(big.intersection_with_circle(small), [])

    def test_coincident_returns_empty(self):
        c1 = Circle(Point2D(0, 0), 5)
        c2 = Circle(Point2D(0, 0), 5)
        self.assertEqual(c1.intersection_with_circle(c2), [])

    def test_point_circle_tangent(self):
        point_circle = Circle(Point2D(5, 0), 0)
        big = Circle(Point2D(0, 0), 5)
        pts = big.intersection_with_circle(point_circle)
        self.assertEqual(pts, [Point2D(5, 0)])


if __name__ == "__main__":
    unittest.main()
