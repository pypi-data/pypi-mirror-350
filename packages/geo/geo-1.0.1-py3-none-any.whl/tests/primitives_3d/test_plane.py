# (1) python tests/primitives_3d/test_plane.py
# (2) python -m unittest tests/primitives_3d/test_plane.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_3d.plane import Plane
from geo.core import Point3D, Vector3D
from geo.primitives_3d.line_3d import Line3D
from geo.core.precision import DEFAULT_EPSILON

class TestPlane(unittest.TestCase):

    def test_init_point_normal(self):
        p = Point3D(1, 2, 3)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)
        self.assertEqual(plane.point_on_plane, p)
        self.assertEqual(plane.normal, n.normalize())
        self.assertAlmostEqual(plane.d_coeff, n.dot(Vector3D(*p)), delta=DEFAULT_EPSILON)

    def test_init_three_points(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 0, 0)
        p3 = Point3D(0, 1, 0)
        plane = Plane(p1, p2, p3)
        expected_normal = Vector3D(0, 0, 1)
        self.assertEqual(plane.normal, expected_normal)
        self.assertTrue(plane.contains_point(p1))
        self.assertTrue(plane.contains_point(p2))
        self.assertTrue(plane.contains_point(p3))

    def test_init_collinear_points_raises(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(1, 1, 1)
        p3 = Point3D(2, 2, 2)
        with self.assertRaises(ValueError):
            Plane(p1, p2, p3)

    def test_init_zero_normal_raises(self):
        p = Point3D(0, 0, 0)
        zero_vector = Vector3D(0, 0, 0)
        with self.assertRaises(ValueError):
            Plane(p, zero_vector)

    def test_init_invalid_args_raises(self):
        p = Point3D(0, 0, 0)
        with self.assertRaises(TypeError):
            Plane(p, "invalid_arg")

    def test_repr_and_eq(self):
        p = Point3D(1, 2, 3)
        n = Vector3D(0, 0, 1)
        plane1 = Plane(p, n)
        plane2 = Plane(p, n)
        plane3 = Plane(p, -n)
        self.assertIn("Plane", repr(plane1))
        self.assertEqual(plane1, plane2)
        self.assertEqual(plane1, plane3)
        self.assertNotEqual(plane1, "not_a_plane")

    def test_signed_distance_and_distance_to_point(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        point_above = Point3D(0, 0, 5)
        point_below = Point3D(0, 0, -5)
        point_on_plane = Point3D(1, 2, 0)

        self.assertAlmostEqual(plane.signed_distance_to_point(point_above), 5, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(plane.signed_distance_to_point(point_below), -5, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(plane.signed_distance_to_point(point_on_plane), 0, delta=DEFAULT_EPSILON)

        self.assertAlmostEqual(plane.distance_to_point(point_above), 5, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(plane.distance_to_point(point_below), 5, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(plane.distance_to_point(point_on_plane), 0, delta=DEFAULT_EPSILON)

    def test_contains_point(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        point_on_plane = Point3D(1, 1, 0)
        point_near_plane = Point3D(1, 1, 1e-12)
        point_off_plane = Point3D(1, 1, 1)

        self.assertTrue(plane.contains_point(point_on_plane))
        self.assertTrue(plane.contains_point(point_near_plane, epsilon=1e-10))
        self.assertFalse(plane.contains_point(point_off_plane))

    def test_project_point(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        point = Point3D(1, 2, 3)
        projected = plane.project_point(point)
        self.assertTrue(plane.contains_point(projected))
        self.assertAlmostEqual(projected.z, 0, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(projected.x, point.x, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(projected.y, point.y, delta=DEFAULT_EPSILON)

    def test_intersection_with_line_intersects(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        line_origin = Point3D(0, 0, 1)
        line_dir = Vector3D(0, 0, -1)
        line = Line3D(line_origin, line_dir)

        intersect_point = plane.intersection_with_line(line)
        self.assertIsNotNone(intersect_point)
        self.assertTrue(plane.contains_point(intersect_point))
        self.assertAlmostEqual(intersect_point.z, 0, delta=DEFAULT_EPSILON)

    def test_intersection_with_line_parallel_no_intersect(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        line_origin = Point3D(0, 0, 1)
        line_dir = Vector3D(1, 0, 0)  # Parallel to plane, in xy plane
        line = Line3D(line_origin, line_dir)

        intersect_point = plane.intersection_with_line(line)
        self.assertIsNone(intersect_point)

    def test_intersection_with_line_on_plane(self):
        p = Point3D(0, 0, 0)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)

        line_origin = Point3D(1, 1, 0)
        line_dir = Vector3D(1, 0, 0)  # Line lies on the plane
        line = Line3D(line_origin, line_dir)

        intersect_point = plane.intersection_with_line(line)
        self.assertIsNone(intersect_point)

    def test_get_coefficients(self):
        p = Point3D(1, 2, 3)
        n = Vector3D(0, 0, 1)
        plane = Plane(p, n)
        A, B, C, D = plane.get_coefficients()
        self.assertAlmostEqual(A, n.x, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(B, n.y, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(C, n.z, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(D, n.dot(Vector3D(*p)), delta=DEFAULT_EPSILON)

if __name__ == "__main__":
    unittest.main()
