# (1) python tests/primitives_3d/test_cone.py
# (2) python -m unittest tests/primitives_3d/test_cone.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_3d.cone import Cone
from geo.core import Point3D, Vector3D
from geo.primitives_3d.plane import Plane
from geo.core.precision import is_equal, DEFAULT_EPSILON

class TestCone(unittest.TestCase):

    def setUp(self):
        # Simple cone along z-axis from (0,0,0) base to (0,0,3) apex with radius 1
        self.apex = Point3D(0, 0, 3)
        self.base_center = Point3D(0, 0, 0)
        self.radius = 1.0
        self.cone = Cone(self.apex, self.base_center, self.radius)

    def test_cone_creation_valid(self):
        self.assertEqual(self.cone.apex, self.apex)
        self.assertEqual(self.cone.base_center, self.base_center)
        self.assertAlmostEqual(self.cone.base_radius, self.radius)
        self.assertAlmostEqual(self.cone.height, 3.0)
        self.assertTrue(isinstance(self.cone.axis_direction, Vector3D))

    def test_cone_creation_invalid(self):
        # Apex == base_center with nonzero radius -> error
        with self.assertRaises(ValueError):
            Cone(self.base_center, self.base_center, 1.0)
        # Negative radius -> error
        with self.assertRaises(ValueError):
            Cone(self.apex, self.base_center, -0.5)
        # Apex == base_center with zero radius (point cone) allowed
        cone_point = Cone(self.base_center, self.base_center, 0.0)
        self.assertEqual(cone_point.height, 0.0)
        self.assertEqual(cone_point.base_radius, 0.0)

    def test_properties(self):
        # volume = (1/3)*pi*r^2*h = (1/3)*pi*1*1*3 = pi
        self.assertAlmostEqual(self.cone.volume, math.pi, places=7)
        # slant_height = sqrt(h^2 + r^2) = sqrt(9+1) = sqrt(10)
        self.assertAlmostEqual(self.cone.slant_height, math.sqrt(10), places=7)
        # lateral_surface_area = pi*r*slant_height
        self.assertAlmostEqual(
            self.cone.lateral_surface_area, math.pi * 1 * math.sqrt(10), places=7)
        # base_area = pi*r^2
        self.assertAlmostEqual(self.cone.base_area, math.pi * 1**2, places=7)
        # total_surface_area = base_area + lateral_surface_area
        self.assertAlmostEqual(
            self.cone.total_surface_area,
            self.cone.base_area + self.cone.lateral_surface_area,
            places=7)

    def test_get_base_plane(self):
        plane = self.cone.get_base_plane()
        self.assertIsInstance(plane, Plane)
        # Base plane normal should be opposite axis_direction
        self.assertTrue(
            is_equal(plane.normal.x, -self.cone.axis_direction.x, DEFAULT_EPSILON) and
            is_equal(plane.normal.y, -self.cone.axis_direction.y, DEFAULT_EPSILON) and
            is_equal(plane.normal.z, -self.cone.axis_direction.z, DEFAULT_EPSILON)
        )

    def test_contains_point_inside(self):
        # Point exactly at apex
        self.assertTrue(self.cone.contains_point(self.apex))
        # Point on axis halfway between base and apex
        mid_point = Point3D(0, 0, 1.5)
        self.assertTrue(self.cone.contains_point(mid_point))
        # Point inside radius at mid height
        inside_point = Point3D(0.2, 0.2, 1.5)
        self.assertTrue(self.cone.contains_point(inside_point))
        # Point on base circle
        base_edge_point = Point3D(1.0, 0, 0)
        self.assertTrue(self.cone.contains_point(base_edge_point))
        # Point slightly outside radius at mid height
        outside_point = Point3D(1.0, 0, 1.5)
        self.assertFalse(self.cone.contains_point(outside_point))

    def test_contains_point_outside(self):
        # Point below base plane
        below_base = Point3D(0, 0, -0.1)
        self.assertFalse(self.cone.contains_point(below_base))
        # Point above apex
        above_apex = Point3D(0, 0, 3.1)
        self.assertFalse(self.cone.contains_point(above_apex))
        # Far away point
        far_point = Point3D(10, 10, 10)
        self.assertFalse(self.cone.contains_point(far_point))

    def test_equality_and_repr(self):
        cone2 = Cone(self.apex, self.base_center, self.radius)
        self.assertEqual(self.cone, cone2)
        self.assertIn("Cone", repr(self.cone))

    def test_degenerate_point_cone_contains(self):
        point_cone = Cone(self.base_center, self.base_center, 0.0)
        self.assertTrue(point_cone.contains_point(self.base_center))
        self.assertFalse(point_cone.contains_point(Point3D(0,0,0.1)))

    def test_degenerate_disk_cone_contains(self):
        # Apex == base_center, radius > 0 => should raise error on construction (your code)
        # But if modified to allow, test points on disk plane
        with self.assertRaises(ValueError):
            Cone(self.base_center, self.base_center, 1.0)

if __name__ == "__main__":
    unittest.main()
