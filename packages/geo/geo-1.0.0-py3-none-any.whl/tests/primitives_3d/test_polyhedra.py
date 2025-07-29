# (1) python tests/primitives_3d/test_polyhedra.py
# (2) python -m unittest tests/primitives_3d/test_polyhedra.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_3d.polyhedra import Polyhedron
from geo.core import Point3D, Vector3D

class TestPolyhedron(unittest.TestCase):

    def setUp(self):
        # Define a cube centered at origin with side length 2
        # Vertices of cube (8 points)
        self.cube_vertices = [
            Point3D(-1, -1, -1),
            Point3D(1, -1, -1),
            Point3D(1, 1, -1),
            Point3D(-1, 1, -1),
            Point3D(-1, -1, 1),
            Point3D(1, -1, 1),
            Point3D(1, 1, 1),
            Point3D(-1, 1, 1)
        ]
        # Faces by vertex indices (each face has 4 vertices)
        self.cube_faces = [
            [0, 1, 2, 3],  # Bottom face (z = -1)
            [4, 5, 6, 7],  # Top face (z = +1)
            [0, 1, 5, 4],  # Front face (y = -1)
            [2, 3, 7, 6],  # Back face (y = +1)
            [1, 2, 6, 5],  # Right face (x = +1)
            [0, 3, 7, 4]   # Left face (x = -1)
        ]
        self.cube = Polyhedron(self.cube_vertices, self.cube_faces)

    def test_basic_properties(self):
        self.assertEqual(self.cube.num_vertices, 8)
        self.assertEqual(self.cube.num_faces, 6)
        self.assertEqual(self.cube.num_edges, 12)  # Cube has 12 edges

    def test_face_points(self):
        face0_points = self.cube.get_face_points(0)
        self.assertEqual(len(face0_points), 4)
        self.assertTrue(all(isinstance(p, Point3D) for p in face0_points))

    def test_face_normal(self):
        # Bottom face normal points down (0,0,-1)
        normal = self.cube.get_face_normal(0)
        expected = Vector3D(0, 0, -1)
        self.assertAlmostEqual(normal.x, expected.x, places=6)
        self.assertAlmostEqual(normal.y, expected.y, places=6)
        self.assertAlmostEqual(normal.z, expected.z, places=6)

        # Top face normal points up (0,0,1)
        normal_top = self.cube.get_face_normal(1)
        expected_top = Vector3D(0, 0, 1)
        self.assertAlmostEqual(normal_top.x, expected_top.x, places=6)
        self.assertAlmostEqual(normal_top.y, expected_top.y, places=6)
        self.assertAlmostEqual(normal_top.z, expected_top.z, places=6)

    def test_surface_area(self):
        # Cube with side length 2 has surface area 6 * 2*2 = 24
        area = self.cube.surface_area()
        self.assertAlmostEqual(area, 24.0, places=6)

    def test_volume(self):
        # Cube side length 2 has volume 2^3 = 8
        vol = self.cube.volume()
        self.assertAlmostEqual(vol, 8.0, places=6)

    def test_contains_point_inside(self):
        inside_point = Point3D(0, 0, 0)
        self.assertTrue(self.cube.contains_point(inside_point))

    def test_contains_point_outside(self):
        outside_point = Point3D(3, 0, 0)
        self.assertFalse(self.cube.contains_point(outside_point))

    def test_contains_point_on_surface(self):
        surface_point = Point3D(1, 0, 0)  # On right face plane
        self.assertTrue(self.cube.contains_point(surface_point))

    def test_invalid_face_indices(self):
        # Creating a polyhedron with invalid face index should raise ValueError
        with self.assertRaises(ValueError):
            Polyhedron(self.cube_vertices, [[0, 1, 8]])  # 8 out of range

    def test_face_too_small(self):
        # Face with less than 3 vertices should raise error
        with self.assertRaises(ValueError):
            Polyhedron(self.cube_vertices, [[0, 1]])  # Only two vertices

if __name__ == '__main__':
    unittest.main()
