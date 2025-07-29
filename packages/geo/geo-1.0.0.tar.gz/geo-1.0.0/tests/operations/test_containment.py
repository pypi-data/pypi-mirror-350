# (1) python tests/operations/test_containment.py
# (2) python -m unittest tests/operations/test_containment.py (verbose output) (auto add sys.path)

import unittest
import os
import sys

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core.precision import DEFAULT_EPSILON
from geo.core import Point2D, Point3D, Vector2D
from geo.primitives_2d import Polygon, Segment2D
from geo.primitives_3d import Polyhedron
from geo.operations import containment

class TestContainment(unittest.TestCase):

    def setUp(self):
        # Common points for tests
        self.p0 = Point2D(0, 0)
        self.p1 = Point2D(1, 0)
        self.p2 = Point2D(1, 1)
        self.p3 = Point2D(0, 1)
        self.p_outside = Point2D(2, 2)
        self.p_on_edge = Point2D(0.5, 0)
        self.p_vertex = Point2D(1, 0)

        # Square polygon CCW
        self.square = Polygon([self.p0, self.p1, self.p2, self.p3])

        # Triangle polygon CCW
        self.triangle = Polygon([self.p0, self.p1, self.p2])

        # Concave polygon (arrow shape)
        self.concave = Polygon([
            Point2D(0,0), Point2D(2,1), Point2D(0,2), Point2D(1,1)
        ])

    # --- check_point_left_of_line ---
    def test_check_point_left_of_line(self):
        val = containment.check_point_left_of_line(Point2D(0,1), Point2D(0,0), Point2D(1,0))
        self.assertGreater(val, 0)

        val = containment.check_point_left_of_line(Point2D(0,-1), Point2D(0,0), Point2D(1,0))
        self.assertLess(val, 0)

        val = containment.check_point_left_of_line(Point2D(0.5, 0), Point2D(0,0), Point2D(1,0))
        self.assertAlmostEqual(val, 0)

    # --- is_polygon_simple ---
    def test_is_polygon_simple_simple_polygon(self):
        self.assertTrue(containment.is_polygon_simple(self.square))
        self.assertTrue(containment.is_polygon_simple(self.triangle))

    def test_is_polygon_simple_self_intersecting(self):
        bowtie = Polygon([Point2D(0,0), Point2D(2,2), Point2D(0,2), Point2D(2,0)])
        self.assertFalse(containment.is_polygon_simple(bowtie))

    def test_is_polygon_simple_adjacent_edges_touching_only_at_vertex(self):
        poly = Polygon([Point2D(0,0), Point2D(2,0), Point2D(1,1), Point2D(2,2), Point2D(0,2)])
        self.assertTrue(containment.is_polygon_simple(poly))

    def test_is_polygon_simple_overlapping_adjacent_edges(self):
        vertices = [Point2D(0,0), Point2D(2,0), Point2D(1,0), Point2D(0,1)]
        poly = Polygon(vertices)
        self.assertFalse(containment.is_polygon_simple(poly))

    # --- point_on_polygon_boundary ---
    def test_point_on_polygon_boundary_true(self):
        self.assertTrue(containment.point_on_polygon_boundary(self.p_vertex, self.square))
        self.assertTrue(containment.point_on_polygon_boundary(self.p_on_edge, self.square))

    def test_point_on_polygon_boundary_false(self):
        self.assertFalse(containment.point_on_polygon_boundary(self.p_outside, self.square))
        self.assertFalse(containment.point_on_polygon_boundary(Point2D(0.5, 0.5), self.square))

    # --- point_in_convex_polygon_2d ---
    def test_point_in_convex_polygon_2d_inside(self):
        self.assertTrue(containment.point_in_convex_polygon_2d(Point2D(0.5,0.5), self.square))

    def test_point_in_convex_polygon_2d_outside(self):
        self.assertFalse(containment.point_in_convex_polygon_2d(self.p_outside, self.square))

    def test_point_in_convex_polygon_2d_on_edge(self):
        self.assertTrue(containment.point_in_convex_polygon_2d(self.p_on_edge, self.square))

    def test_point_in_convex_polygon_2d_vertex(self):
        self.assertTrue(containment.point_in_convex_polygon_2d(self.p_vertex, self.square))

    def test_point_in_convex_polygon_2d_concave_polygon(self):
        inside_concavity = Point2D(1, 1.2)
        self.assertFalse(containment.point_in_convex_polygon_2d(inside_concavity, self.concave))

    # --- point_in_polyhedron_convex ---
    def test_point_in_polyhedron_convex_inside_and_outside(self):
        cube_vertices = [
            Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0), Point3D(0,1,0),
            Point3D(0,0,1), Point3D(1,0,1), Point3D(1,1,1), Point3D(0,1,1),
        ]

        class MockPolyhedron(Polyhedron):
            def __init__(self, verts):
                self._verts = verts
            def get_face_points(self, i):
                faces = [
                    [self._verts[0], self._verts[1], self._verts[2], self._verts[3]],
                    [self._verts[4], self._verts[5], self._verts[6], self._verts[7]],
                    [self._verts[0], self._verts[1], self._verts[5], self._verts[4]],
                    [self._verts[1], self._verts[2], self._verts[6], self._verts[5]],
                    [self._verts[2], self._verts[3], self._verts[7], self._verts[6]],
                    [self._verts[3], self._verts[0], self._verts[4], self._verts[7]],
                ]
                return faces[i]
            @property
            def num_faces(self):
                return 6

        poly = MockPolyhedron(cube_vertices)

        from geo.primitives_3d import Plane as Plane3D

        orig_signed_distance = Plane3D.signed_distance_to_point
        def mock_signed_distance_to_point(self, point):
            if point.x < 0 or point.x > 1 or point.y < 0 or point.y > 1 or point.z < 0 or point.z > 1:
                return 1.0
            return -1.0

        Plane3D.signed_distance_to_point = mock_signed_distance_to_point

        inside_point = Point3D(0.5, 0.5, 0.5)
        outside_point = Point3D(1.5, 0.5, 0.5)

        self.assertTrue(containment.point_in_polyhedron_convex(inside_point, poly))
        self.assertFalse(containment.point_in_polyhedron_convex(outside_point, poly))

        Plane3D.signed_distance_to_point = orig_signed_distance


if __name__ == '__main__':
    unittest.main()