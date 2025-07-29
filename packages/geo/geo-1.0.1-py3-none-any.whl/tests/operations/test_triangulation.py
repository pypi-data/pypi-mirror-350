# (1) python tests/operations/test_triangulation.py
# (2) python -m unittest tests/operations/test_triangulation.py (verbose output) (auto add sys.path)

import unittest
import math
import numpy as np
import os
import sys

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point2D, Point3D
from geo.primitives_2d import Polygon, Triangle
from geo.operations import triangulation


class TestTriangulation(unittest.TestCase):

    def test_ear_clipping_basic_triangle(self):
        pts = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]
        poly = Polygon(pts)
        tris = triangulation.triangulate_simple_polygon_ear_clipping(poly)
        self.assertEqual(len(tris), 1)
        tri = tris[0]
        self.assertIsInstance(tri, Triangle)
        verts = [tri.p1, tri.p2, tri.p3]
        for p in pts:
            self.assertIn(p, verts)

    def test_ear_clipping_square(self):
        pts = [Point2D(0, 0), Point2D(1, 0), Point2D(1, 1), Point2D(0, 1)]
        poly = Polygon(pts)
        tris = triangulation.triangulate_simple_polygon_ear_clipping(poly)
        self.assertEqual(len(tris), 2)
        for tri in tris:
            self.assertIsInstance(tri, Triangle)

    def test_ear_clipping_concave_polygon(self):
        pts = [
            Point2D(0, 0), Point2D(2, 0), Point2D(2, 2),
            Point2D(1, 1), Point2D(0, 2)
        ]
        poly = Polygon(pts)
        tris = triangulation.triangulate_simple_polygon_ear_clipping(poly)
        self.assertGreaterEqual(len(tris), 3)  # Number of triangles depends on polygon shape
        for tri in tris:
            self.assertIsInstance(tri, Triangle)

    def test_delaunay_triangulation_basic(self):
        pts = [
            Point2D(0, 0), Point2D(1, 0), Point2D(0, 1),
            Point2D(1, 1), Point2D(0.5, 0.5)
        ]
        tris = triangulation.delaunay_triangulation_points_2d(pts)
        self.assertTrue(len(tris) > 0)
        for tri in tris:
            self.assertIsInstance(tri, Triangle)

    def test_delaunay_triangulation_too_few_points(self):
        pts = [Point2D(0, 0), Point2D(1, 0)]
        with self.assertRaises(ValueError):
            triangulation.delaunay_triangulation_points_2d(pts)

    def test_constrained_delaunay_triangulation_not_implemented(self):
        pts = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]
        poly = Polygon(pts)
        with self.assertRaises(NotImplementedError):
            triangulation.constrained_delaunay_triangulation(poly)

    def test_tetrahedralise_basic(self):
        pts = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(0, 1, 0),
            Point3D(0, 0, 1),
            Point3D(1, 1, 1),
        ]
        tets = triangulation.tetrahedralise(pts)
        self.assertIsInstance(tets, list)
        self.assertGreater(len(tets), 0)
        for tet in tets:
            self.assertIsInstance(tet, tuple)
            self.assertEqual(len(tet), 4)
            for p in tet:
                self.assertIsInstance(p, Point3D)

    def test_tetrahedralise_too_few_points(self):
        pts = [Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0)]
        with self.assertRaises(ValueError):
            triangulation.tetrahedralise(pts)


if __name__ == "__main__":
    unittest.main()
