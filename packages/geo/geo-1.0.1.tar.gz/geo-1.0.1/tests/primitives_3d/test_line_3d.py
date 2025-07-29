# (1) python tests/primitives_3d/test_line_3d.py
# (2) python -m unittest tests/primitives_3d/test_line_3d.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_3d.line_3d import Line3D, Segment3D, Ray3D
from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, DEFAULT_EPSILON

def points_equal(p1: Point3D, p2: Point3D, epsilon=DEFAULT_EPSILON) -> bool:
    return is_equal(p1.x, p2.x, epsilon) and is_equal(p1.y, p2.y, epsilon) and is_equal(p1.z, p2.z, epsilon)

def vectors_equal(v1: Vector3D, v2: Vector3D, epsilon=DEFAULT_EPSILON) -> bool:
    return is_equal(v1.x, v2.x, epsilon) and is_equal(v1.y, v2.y, epsilon) and is_equal(v1.z, v2.z, epsilon)


class TestLine3D(unittest.TestCase):

    def setUp(self):
        self.p1 = Point3D(0, 0, 0)
        self.p2 = Point3D(1, 1, 1)
        self.v1 = Vector3D(1, 1, 1)
        self.v_zero = Vector3D(0, 0, 0)

    def test_init_with_vector(self):
        line = Line3D(self.p1, self.v1)
        self.assertTrue(vectors_equal(line.direction, self.v1.normalize()))

        with self.assertRaises(ValueError):
            Line3D(self.p1, self.v_zero)

        with self.assertRaises(TypeError):
            Line3D(self.p1, 123)

    def test_init_with_two_points(self):
        line = Line3D(self.p1, self.p2)
        expected_dir = (self.p2 - self.p1).normalize()
        self.assertTrue(vectors_equal(line.direction, expected_dir))

        with self.assertRaises(ValueError):
            Line3D(self.p1, self.p1)

    def test_equality(self):
        line1 = Line3D(self.p1, self.p2)
        line2 = Line3D(self.p2, self.p1)
        line3 = Line3D(self.p1, Vector3D(-1, -1, -1))
        line4 = Line3D(Point3D(0, 1, 0), Vector3D(1, 1, 1))

        self.assertEqual(line1, line2)
        self.assertEqual(line1, line3)
        self.assertNotEqual(line1, line4)

    def test_point_at(self):
        line = Line3D(self.p1, self.v1)
        p = line.point_at(2.0)
        expected = self.p1 + self.v1.normalize() * 2.0
        self.assertTrue(points_equal(p, expected))

    def test_contains_point(self):
        line = Line3D(self.p1, self.v1)
        p_on_line = Point3D(2, 2, 2)
        p_not_on_line = Point3D(1, 0, 0)

        self.assertTrue(line.contains_point(p_on_line))
        self.assertFalse(line.contains_point(p_not_on_line))

    def test_distance_to_point(self):
        line = Line3D(self.p1, self.v1)
        p = Point3D(1, 0, 0)
        dist = line.distance_to_point(p)
        expected = ((p - self.p1).cross(self.v1.normalize())).magnitude()
        self.assertAlmostEqual(dist, expected, places=6)

    def test_project_point(self):
        line = Line3D(self.p1, self.v1)
        p = Point3D(1, 0, 0)
        proj = line.project_point(p)
        self.assertTrue(line.contains_point(proj))
        dist_proj = proj.distance_to(p)
        for t in [-1, 0, 1, 2]:
            candidate = line.point_at(t)
            self.assertLessEqual(dist_proj, candidate.distance_to(p) + DEFAULT_EPSILON)


class TestSegment3D(unittest.TestCase):

    def setUp(self):
        self.p1 = Point3D(0, 0, 0)
        self.p2 = Point3D(2, 0, 0)
        self.p_mid = Point3D(1, 0, 0)
        self.p_outside = Point3D(3, 0, 0)

    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            Segment3D(self.p1, self.p1)

    def test_equality(self):
        seg1 = Segment3D(self.p1, self.p2)
        seg2 = Segment3D(self.p2, self.p1)
        seg3 = Segment3D(self.p1, Point3D(0, 1, 0))

        self.assertEqual(seg1, seg2)
        self.assertNotEqual(seg1, seg3)

    def test_length_and_midpoint(self):
        seg = Segment3D(self.p1, self.p2)
        self.assertAlmostEqual(seg.length, 2.0, places=6)
        self.assertTrue(points_equal(seg.midpoint, self.p_mid))

    def test_direction_vector(self):
        seg = Segment3D(self.p1, self.p2)
        expected_dir = Vector3D(2, 0, 0)
        self.assertTrue(vectors_equal(seg.direction_vector, expected_dir))

    def test_to_line(self):
        seg = Segment3D(self.p1, self.p2)
        line = seg.to_line()
        self.assertTrue(line.contains_point(self.p1))
        self.assertTrue(line.contains_point(self.p2))

    def test_contains_point(self):
        seg = Segment3D(self.p1, self.p2)
        self.assertTrue(seg.contains_point(self.p_mid))
        self.assertFalse(seg.contains_point(self.p_outside))

    def test_distance_to_point(self):
        seg = Segment3D(self.p1, self.p2)
        p_above = Point3D(1, 1, 0)
        dist = seg.distance_to_point(p_above)
        self.assertAlmostEqual(dist, 1.0, places=6)

        p_before = Point3D(-1, 0, 0)
        dist_before = seg.distance_to_point(p_before)
        self.assertAlmostEqual(dist_before, 1.0, places=6)

        p_after = Point3D(3, 0, 0)
        dist_after = seg.distance_to_point(p_after)
        self.assertAlmostEqual(dist_after, 1.0, places=6)


class TestRay3D(unittest.TestCase):

    def setUp(self):
        self.origin = Point3D(0, 0, 0)
        self.dir = Vector3D(1, 0, 0)
        self.zero_vec = Vector3D(0, 0, 0)

    def test_init(self):
        ray = Ray3D(self.origin, self.dir)
        self.assertTrue(vectors_equal(ray.direction, self.dir.normalize()))

        with self.assertRaises(ValueError):
            Ray3D(self.origin, self.zero_vec)

    def test_equality(self):
        ray1 = Ray3D(self.origin, self.dir)
        ray2 = Ray3D(self.origin, self.dir)
        ray3 = Ray3D(Point3D(1, 0, 0), self.dir)
        ray4 = Ray3D(self.origin, Vector3D(0, 1, 0))

        self.assertEqual(ray1, ray2)
        self.assertNotEqual(ray1, ray3)
        self.assertNotEqual(ray1, ray4)

    def test_point_at(self):
        ray = Ray3D(self.origin, self.dir)
        p = ray.point_at(3.0)
        expected = self.origin + self.dir.normalize() * 3.0
        self.assertTrue(points_equal(p, expected))

        with self.assertRaises(ValueError):
            ray.point_at(-1.0)

    def test_contains_point(self):
        ray = Ray3D(self.origin, self.dir)
        p_on_ray = Point3D(5, 0, 0)
        p_before_origin = Point3D(-1, 0, 0)
        p_not_on_ray = Point3D(0, 1, 0)

        self.assertTrue(ray.contains_point(p_on_ray))
        self.assertFalse(ray.contains_point(p_before_origin))
        self.assertFalse(ray.contains_point(p_not_on_ray))

    def test_to_line(self):
        ray = Ray3D(self.origin, self.dir)
        line = ray.to_line()
        self.assertTrue(line.contains_point(self.origin))
        self.assertTrue(vectors_equal(line.direction, self.dir.normalize()))


if __name__ == "__main__":
    unittest.main()
