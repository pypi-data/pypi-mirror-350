# (1) python tests/primitives_3d/test_cube.py
# (2) python -m unittest tests/primitives_3d/test_cube.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point3D, Vector3D
from geo.primitives_3d.cube import Cube

class TestCube(unittest.TestCase):

    def setUp(self):
        # Standard axis-aligned cube centered at origin, side 2
        self.axis_aligned_cube = Cube(center=Point3D(0, 0, 0), side_length=2)

        # Define rotated axes: 90 degree rotation around Z
        # New axes: x' = y, y' = -x, z' = z
        x_axis = Vector3D(0, 1, 0)
        y_axis = Vector3D(-1, 0, 0)
        z_axis = Vector3D(0, 0, 1)
        self.rotated_axes = [x_axis, y_axis, z_axis]

        self.oriented_cube = Cube(center=Point3D(1, 1, 1), side_length=2, axes=self.rotated_axes)

    def test_volume_surface_area(self):
        cube = self.axis_aligned_cube
        self.assertAlmostEqual(cube.volume, 8)
        self.assertAlmostEqual(cube.surface_area, 24)

    def test_vertices_count(self):
        self.assertEqual(len(self.axis_aligned_cube.vertices), 8)
        self.assertEqual(len(self.oriented_cube.vertices), 8)

    def test_vertices_positions_axis_aligned(self):
        cube = self.axis_aligned_cube
        hs = cube.half_side
        expected = [
            Point3D(-hs, -hs, -hs),
            Point3D(-hs, -hs,  hs),
            Point3D(-hs,  hs, -hs),
            Point3D(-hs,  hs,  hs),
            Point3D( hs, -hs, -hs),
            Point3D( hs, -hs,  hs),
            Point3D( hs,  hs, -hs),
            Point3D( hs,  hs,  hs),
        ]
        for v, e in zip(cube.vertices, expected):
            self.assertAlmostEqual(v.x, e.x)
            self.assertAlmostEqual(v.y, e.y)
            self.assertAlmostEqual(v.z, e.z)

    def test_vertices_positions_oriented(self):
        cube = self.oriented_cube
        # Since cube is rotated 90 degrees about Z, vertices should match rotated positions
        # We'll check one vertex explicitly:
        # For example, vertex corresponding to (-hs, -hs, -hs) in local coords:
        hs = cube.half_side
        # local offset vector = (-hs * x_axis) + (-hs * y_axis) + (-hs * z_axis)
        offset = (cube.axes[0] * -hs) + (cube.axes[1] * -hs) + (cube.axes[2] * -hs)
        expected_vertex = cube.center + offset

        actual_vertex = cube.vertices[0]
        self.assertAlmostEqual(actual_vertex.x, expected_vertex.x)
        self.assertAlmostEqual(actual_vertex.y, expected_vertex.y)
        self.assertAlmostEqual(actual_vertex.z, expected_vertex.z)

    def test_contains_point_axis_aligned(self):
        cube = self.axis_aligned_cube
        # Inside points
        self.assertTrue(cube.contains_point(Point3D(0, 0, 0)))
        self.assertTrue(cube.contains_point(Point3D(1, 1, 1)))
        self.assertTrue(cube.contains_point(Point3D(-1, -1, -1)))
        # On boundary
        self.assertTrue(cube.contains_point(Point3D(1, 0, 0)))
        self.assertTrue(cube.contains_point(Point3D(0, -1, 0)))
        # Outside points
        self.assertFalse(cube.contains_point(Point3D(2, 0, 0)))
        self.assertFalse(cube.contains_point(Point3D(0, 0, -2)))

    def test_contains_point_oriented(self):
        cube = self.oriented_cube
        hs = cube.half_side

        # Point exactly at center
        self.assertTrue(cube.contains_point(cube.center))

        # Points inside by local coordinates (+/- hs along axes)
        # Let's build a point inside: center + 0.5 * axes[0] + (-0.5) * axes[1] + 0 * axes[2]
        inside_point = cube.center + (cube.axes[0] * 0.5 * hs) + (cube.axes[1] * -0.5 * hs)
        self.assertTrue(cube.contains_point(inside_point))

        # Point outside along one axis
        outside_point = cube.center + (cube.axes[0] * (hs + 0.1))
        self.assertFalse(cube.contains_point(outside_point))

    def test_equality(self):
        cube1 = Cube(center=Point3D(0, 0, 0), side_length=2)
        cube2 = Cube(center=Point3D(0, 0, 0), side_length=2)
        cube3 = Cube(center=Point3D(0, 0, 0), side_length=3)
        cube4 = Cube(center=Point3D(0, 0, 0), side_length=2, axes=self.rotated_axes)

        self.assertEqual(cube1, cube2)
        self.assertNotEqual(cube1, cube3)
        self.assertNotEqual(cube1, cube4)

    def test_invalid_axes(self):
        with self.assertRaises(ValueError):
            # Less than 3 axes
            Cube(center=Point3D(0, 0, 0), side_length=2, axes=[Vector3D(1,0,0)])

        with self.assertRaises(ValueError):
            # Non-unit vector axes
            Cube(center=Point3D(0, 0, 0), side_length=2, axes=[
                Vector3D(2, 0, 0),
                Vector3D(0, 1, 0),
                Vector3D(0, 0, 1),
            ])

        with self.assertRaises(ValueError):
            # Non-orthogonal axes
            Cube(center=Point3D(0, 0, 0), side_length=2, axes=[
                Vector3D(1, 0, 0),
                Vector3D(1, 0, 0),
                Vector3D(0, 0, 1),
            ])


if __name__ == "__main__":
    unittest.main()
