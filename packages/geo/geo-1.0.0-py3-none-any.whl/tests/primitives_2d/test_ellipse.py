# (1) python tests/primitives_2d/test_ellipse.py
# (2) python -m unittest tests/primitives_2d/test_ellipse.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Ellipse
from geo.core import Point2D
from geo.core.precision import DEFAULT_EPSILON, is_equal


class TestEllipseBasics(unittest.TestCase):
    def test_constructor_invalid_radius(self):
        with self.assertRaises(ValueError):
            Ellipse(Point2D(0, 0), -1, 2)
        with self.assertRaises(ValueError):
            Ellipse(Point2D(0, 0), 2, -1)

    def test_zero_radii(self):
        e = Ellipse(Point2D(0, 0), 0, 0)
        self.assertEqual(e.area, 0.0)
        self.assertEqual(e.circumference(), 0.0)
        self.assertTrue(e.contains_point(Point2D(0, 0)))
        self.assertFalse(e.contains_point(Point2D(DEFAULT_EPSILON, 0)))

    def test_area_and_circumference(self):
        e = Ellipse(Point2D(0, 0), 4, 3)
        expected_area = math.pi * 4 * 3
        self.assertAlmostEqual(e.area, expected_area)
        self.assertTrue(e.circumference() > 0)  # Approximation formula used internally

    def test_equality(self):
        e1 = Ellipse(Point2D(1, 1), 3, 2)
        e2 = Ellipse(Point2D(1, 1), 3 + DEFAULT_EPSILON / 2, 2 + DEFAULT_EPSILON / 2)
        self.assertEqual(e1, e2)


class TestEllipseContainment(unittest.TestCase):
    def setUp(self):
        self.ellipse = Ellipse(Point2D(0, 0), 5, 3)

    def test_point_inside(self):
        self.assertTrue(self.ellipse.contains_point(Point2D(3, 1)))
        self.assertTrue(self.ellipse.contains_point(Point2D(0, 0)))

    def test_point_on_boundary(self):
        pt = Point2D(5, 0)  # On major axis edge
        self.assertTrue(self.ellipse.contains_point(pt))

    def test_point_outside(self):
        pt = Point2D(6, 0)
        self.assertFalse(self.ellipse.contains_point(pt))
        pt_near = Point2D(5 + DEFAULT_EPSILON * 2, 0)
        self.assertFalse(self.ellipse.contains_point(pt_near))

    def test_rotated_axes_equivalence(self):
        # Ellipse with same radius_x and radius_y is a circle
        e = Ellipse(Point2D(0, 0), 4, 4)
        self.assertTrue(e.contains_point(Point2D(2, 2)))
        self.assertFalse(e.contains_point(Point2D(4.1, 0)))


class TestEllipseBoundaryPoints(unittest.TestCase):
    def setUp(self):
        self.e = Ellipse(Point2D(0, 0), 3, 2)

    def test_boundary_extents(self):
        self.assertTrue(self.e.contains_point(Point2D(3, 0)))
        self.assertTrue(self.e.contains_point(Point2D(0, 2)))
        self.assertFalse(self.e.contains_point(Point2D(3.1, 0)))
        self.assertFalse(self.e.contains_point(Point2D(0, 2.1)))

    def test_symmetry_points(self):
        pts = [
            Point2D(-3, 0), Point2D(3, 0),
            Point2D(0, -2), Point2D(0, 2),
        ]
        for pt in pts:
            self.assertTrue(self.e.contains_point(pt))


if __name__ == "__main__":
    unittest.main()
