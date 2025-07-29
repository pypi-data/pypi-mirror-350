# (1) python tests/primitives_3d/test_sphere.py
# (2) python -m unittest tests/primitives_3d/test_sphere.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_3d.sphere import Sphere, Circle3D
from geo.core import Point3D, Vector3D
from geo.primitives_3d.line_3d import Line3D
from geo.primitives_3d.plane import Plane
from geo.core.precision import DEFAULT_EPSILON


class TestSphere(unittest.TestCase):

    def setUp(self):
        self.center = Point3D(0, 0, 0)
        self.radius = 5.0
        self.sphere = Sphere(self.center, self.radius)

    def test_repr_and_eq(self):
        s2 = Sphere(Point3D(0, 0, 0), 5.0)
        self.assertEqual(repr(self.sphere), "Sphere(center=Point3D(0.0, 0.0, 0.0), radius=5.0)")
        self.assertTrue(self.sphere == s2)

        s3 = Sphere(Point3D(1, 0, 0), 5.0)
        self.assertFalse(self.sphere == s3)
        self.assertFalse(self.sphere == "not a sphere")

    def test_invalid_radius(self):
        with self.assertRaises(ValueError):
            Sphere(Point3D(0, 0, 0), -1)

    def test_surface_area_volume(self):
        expected_area = 4 * math.pi * self.radius**2
        expected_volume = (4/3) * math.pi * self.radius**3
        self.assertAlmostEqual(self.sphere.surface_area, expected_area)
        self.assertAlmostEqual(self.sphere.volume, expected_volume)

    def test_contains_point(self):
        inside_point = Point3D(0, 0, 4.9)
        on_surface_point = Point3D(0, 0, 5.0)
        outside_point = Point3D(0, 0, 5.1)

        self.assertTrue(self.sphere.contains_point(inside_point))
        self.assertTrue(self.sphere.contains_point(on_surface_point))
        self.assertFalse(self.sphere.contains_point(outside_point))

        # Test on_surface_epsilon param
        self.assertTrue(self.sphere.contains_point(Point3D(0, 0, 5.0000001), on_surface_epsilon=1e-5))
        self.assertFalse(self.sphere.contains_point(Point3D(0, 0, 5.1), on_surface_epsilon=1e-5))

    def test_strictly_inside_outside_and_on_surface(self):
        inside = Point3D(0, 0, 4.9)
        on_surface = Point3D(0, 0, 5.0)
        outside = Point3D(0, 0, 5.1)

        self.assertTrue(self.sphere.strictly_inside(inside))
        self.assertFalse(self.sphere.strictly_inside(on_surface))
        self.assertFalse(self.sphere.strictly_inside(outside))

        self.assertTrue(self.sphere.on_surface(on_surface))
        self.assertFalse(self.sphere.on_surface(inside))
        self.assertFalse(self.sphere.on_surface(outside))

        self.assertTrue(self.sphere.strictly_outside(outside))
        self.assertFalse(self.sphere.strictly_outside(on_surface))
        self.assertFalse(self.sphere.strictly_outside(inside))

    def test_intersection_with_line(self):
        # Line passing through sphere center along z-axis
        line = Line3D(Point3D(0, 0, -10), Vector3D(0, 0, 1))
        points = self.sphere.intersection_with_line(line)
        self.assertEqual(len(points), 2)
        self.assertTrue(all(isinstance(p, Point3D) for p in points))

        # Line tangent to sphere (one intersection)
        line_tangent = Line3D(Point3D(5, 0, 0), Vector3D(0, 1, 0))
        points_tangent = self.sphere.intersection_with_line(line_tangent)
        self.assertEqual(len(points_tangent), 1)
        self.assertTrue(self.sphere.on_surface(points_tangent[0]))

        # Line outside sphere (no intersection)
        line_outside = Line3D(Point3D(6, 0, 0), Vector3D(0, 1, 0))
        points_outside = self.sphere.intersection_with_line(line_outside)
        self.assertEqual(len(points_outside), 0)

    def test_intersection_with_plane(self):
        # Plane passing through center, normal z-axis: intersection circle radius = sphere radius
        plane = Plane(Point3D(0, 0, 0), Vector3D(0, 0, 1))
        circle = self.sphere.intersection_with_plane(plane)
        self.assertIsInstance(circle, Circle3D)
        self.assertAlmostEqual(circle.radius, self.radius)
        self.assertTrue(circle.normal == plane.normal)

        # Plane tangent to sphere at z=5
        plane_tangent = Plane(Point3D(0, 0, 5), Vector3D(0, 0, 1))
        circle_tangent = self.sphere.intersection_with_plane(plane_tangent)
        self.assertIsInstance(circle_tangent, Circle3D)
        self.assertAlmostEqual(circle_tangent.radius, 0.0)

        # Plane far away with no intersection
        plane_far = Plane(Point3D(0, 0, 6), Vector3D(0, 0, 1))
        self.assertIsNone(self.sphere.intersection_with_plane(plane_far))

    def test_intersection_with_sphere(self):
        # Two spheres intersecting
        s1 = Sphere(Point3D(0, 0, 0), 5)
        s2 = Sphere(Point3D(6, 0, 0), 5)
        circle = s1.intersection_with_sphere(s2)
        self.assertIsInstance(circle, Circle3D)
        self.assertGreater(circle.radius, 0)
        self.assertTrue(abs(circle.normal.magnitude() - 1) < DEFAULT_EPSILON)

        # Tangent spheres (touching externally)
        s3 = Sphere(Point3D(10, 0, 0), 5)
        circle_tangent = s1.intersection_with_sphere(s3)
        self.assertIsInstance(circle_tangent, Circle3D)
        self.assertAlmostEqual(circle_tangent.radius, 0)

        # Tangent spheres (touching internally)
        s4 = Sphere(Point3D(3, 0, 0), 2)
        circle_internal_tangent = s1.intersection_with_sphere(s4)
        self.assertIsInstance(circle_internal_tangent, Circle3D)
        self.assertAlmostEqual(circle_internal_tangent.radius, 0)

        # No intersection (too far)
        s5 = Sphere(Point3D(20, 0, 0), 5)
        self.assertIsNone(s1.intersection_with_sphere(s5))

        # No intersection (one inside another without touching)
        s6 = Sphere(Point3D(0, 0, 0), 2)
        self.assertIsNone(s1.intersection_with_sphere(s6))

        # Concentric spheres
        s7 = Sphere(Point3D(0, 0, 0), 5)
        self.assertIsNone(s1.intersection_with_sphere(s7))

    def test_translate_and_scale(self):
        offset = Vector3D(1, 2, 3)
        translated = self.sphere.translate(offset)
        self.assertEqual(translated.center, self.center + offset)
        self.assertEqual(translated.radius, self.radius)

        scaled = self.sphere.scale(2)
        self.assertEqual(scaled.center, Point3D(0, 0, 0))
        self.assertEqual(scaled.radius, self.radius * 2)

        with self.assertRaises(ValueError):
            self.sphere.scale(-1)

    def test_point_from_spherical_coords(self):
        # Check point at theta=0, phi=0 (north pole)
        p = self.sphere.point_from_spherical_coords(0, 0)
        self.assertTrue(self.sphere.on_surface(p))
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 0)
        self.assertAlmostEqual(p.z, self.radius)

        # Check point at theta=pi/2, phi=pi/2 (equator point)
        p2 = self.sphere.point_from_spherical_coords(math.pi/2, math.pi/2)
        self.assertTrue(self.sphere.on_surface(p2))
        self.assertAlmostEqual(p2.x, 0, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(p2.y, self.radius, delta=DEFAULT_EPSILON)
        self.assertAlmostEqual(p2.z, 0, delta=DEFAULT_EPSILON)

        # Random point with arbitrary angles
        theta = math.pi / 4
        phi = math.pi / 3
        p3 = self.sphere.point_from_spherical_coords(theta, phi)
        self.assertTrue(self.sphere.on_surface(p3))


class TestCircle3D(unittest.TestCase):

    def setUp(self):
        self.center = Point3D(1, 2, 3)
        self.radius = 4.0
        self.normal = Vector3D(0, 0, 1)
        self.circle = Circle3D(self.center, self.radius, self.normal)

    def test_repr(self):
        expected = f"Circle3D(center={self.center}, radius={self.radius}, normal={self.normal.normalize()})"
        self.assertEqual(repr(self.circle), expected)

    def test_invalid_radius(self):
        with self.assertRaises(ValueError):
            Circle3D(self.center, -1, self.normal)

    def test_contains_point(self):
        # Point exactly on circle circumference
        point_on_circle = Point3D(self.center.x + self.radius, self.center.y, self.center.z)
        self.assertTrue(self.circle.contains_point(point_on_circle))

        # Point on plane but inside radius (not on circumference)
        point_inside = Point3D(self.center.x + self.radius / 2, self.center.y, self.center.z)
        self.assertFalse(self.circle.contains_point(point_inside))

        # Point not on plane
        point_off_plane = Point3D(self.center.x + self.radius, self.center.y, self.center.z + 0.1)
        self.assertFalse(self.circle.contains_point(point_off_plane))


if __name__ == "__main__":
    unittest.main()
