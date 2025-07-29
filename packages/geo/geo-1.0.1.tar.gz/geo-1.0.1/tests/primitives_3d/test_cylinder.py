# (1) python tests/primitives_3d/test_cylinder.py
# (2) python -m unittest tests/primitives_3d/test_cylinder.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point3D, Vector3D
from geo.primitives_3d.cylinder import Cylinder
from geo.core.precision import DEFAULT_EPSILON, is_equal
from geo.primitives_3d.plane import Plane


class TestCylinder(unittest.TestCase):
    def setUp(self):
        self.base = Point3D(0, 0, 0)
        self.axis = Vector3D(0, 0, 1)
        self.radius = 2.0
        self.height = 5.0
        self.cylinder = Cylinder(self.base, self.axis, self.radius, self.height)

    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            Cylinder(self.base, Vector3D(0, 0, 0), 1.0, 1.0)  # zero axis vector

        with self.assertRaises(ValueError):
            Cylinder(self.base, self.axis, -1.0, 1.0)  # negative radius

        with self.assertRaises(ValueError):
            Cylinder(self.base, self.axis, 1.0, -1.0)  # negative height

    def test_properties(self):
        self.assertAlmostEqual(self.cylinder.volume, math.pi * self.radius ** 2 * self.height)
        self.assertAlmostEqual(self.cylinder.lateral_surface_area, 2 * math.pi * self.radius * self.height)
        self.assertAlmostEqual(self.cylinder.base_area, math.pi * self.radius ** 2)
        total_surface = 2 * self.cylinder.base_area + self.cylinder.lateral_surface_area
        self.assertAlmostEqual(self.cylinder.total_surface_area, total_surface)

    def test_top_center(self):
        expected_top = Point3D(0, 0, 5)
        self.assertEqual(self.cylinder.top_center, expected_top)

    def test_get_cap_planes(self):
        base_plane, top_plane = self.cylinder.get_cap_planes()
        self.assertIsInstance(base_plane, Plane)
        self.assertIsInstance(top_plane, Plane)
        # Base normal points opposite axis
        self.assertTrue(base_plane.normal == -self.axis.normalize())
        # Top normal points along axis
        self.assertTrue(top_plane.normal == self.axis.normalize())

    def test_contains_point_inside(self):
        # Inside point (center axis, halfway)
        p_inside = Point3D(0, 0, 2.5)
        self.assertTrue(self.cylinder.contains_point(p_inside))

    def test_contains_point_on_surface(self):
        # Point exactly on lateral surface at mid height
        p_surface = Point3D(self.radius, 0, self.height / 2)
        self.assertTrue(self.cylinder.contains_point(p_surface))

    def test_contains_point_outside_radius(self):
        p_outside = Point3D(self.radius + 1e-3, 0, self.height / 2)
        self.assertFalse(self.cylinder.contains_point(p_outside, epsilon=1e-5))

    def test_contains_point_below_base(self):
        p_below = Point3D(0, 0, -0.1)
        self.assertFalse(self.cylinder.contains_point(p_below))

    def test_contains_point_above_top(self):
        p_above = Point3D(0, 0, self.height + 0.1)
        self.assertFalse(self.cylinder.contains_point(p_above))

    def test_equality(self):
        c2 = Cylinder(self.base, self.axis, self.radius, self.height)
        self.assertEqual(self.cylinder, c2)

        # Same cylinder but axis flipped and base and top swapped
        c3 = Cylinder(self.cylinder.top_center, -self.axis, self.radius, self.height)
        self.assertEqual(self.cylinder, c3)

        # Different radius
        c4 = Cylinder(self.base, self.axis, self.radius + 0.1, self.height)
        self.assertNotEqual(self.cylinder, c4)

    def test_distance_to_axis(self):
        p = Point3D(3, 0, 2)
        dist = self.cylinder.distance_to_axis(p)
        self.assertAlmostEqual(dist, 3)

        # Point on axis has zero distance
        p_on_axis = Point3D(0, 0, 1)
        self.assertAlmostEqual(self.cylinder.distance_to_axis(p_on_axis), 0)

    def test_get_lateral_surface_point(self):
        # Angle 0, height fraction 0 -> base edge on +perp1
        p0 = self.cylinder.get_lateral_surface_point(0, 0)
        self.assertTrue(is_equal(p0.z, 0))
        dist0 = p0.distance_to(Point3D(0, 0, 0))
        self.assertTrue(is_equal(dist0, self.radius))

        # Angle pi/2, height fraction 1 -> top edge on +perp2
        p1 = self.cylinder.get_lateral_surface_point(math.pi / 2, 1)
        self.assertTrue(is_equal(p1.z, self.height))
        dist1 = p1.distance_to(Point3D(0, 0, self.height))
        self.assertTrue(is_equal(dist1, self.radius))

        # Invalid height fraction < 0 or > 1
        with self.assertRaises(ValueError):
            self.cylinder.get_lateral_surface_point(0, -0.1)
        with self.assertRaises(ValueError):
            self.cylinder.get_lateral_surface_point(0, 1.1)

    def test_project_point_onto_axis(self):
        p = Point3D(1, 0, 3)
        proj = self.cylinder.project_point_onto_axis(p)
        # Projection is dot of vector (1,0,3) onto (0,0,1) = 3
        self.assertAlmostEqual(proj, 3)

        # Point below base
        p_below = Point3D(0, 0, -1)
        proj_below = self.cylinder.project_point_onto_axis(p_below)
        self.assertAlmostEqual(proj_below, -1)


if __name__ == "__main__":
    unittest.main()
