# (1) python tests/operations/test_intersections_2d.py
# (2) python -m unittest tests/operations/test_intersections_2d.py (verbose output) (auto add sys.path)

import unittest
import math
import os
import sys

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point2D, Vector2D
from geo.primitives_2d import Line2D, Segment2D, Polygon, Circle
from geo.operations.intersections_2d import (
    segment_segment_intersection_detail,
    line_polygon_intersections,
    segment_circle_intersections,
)

class TestIntersections2D(unittest.TestCase):

    def test_segment_segment_intersection_detail_point(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(2, 2))
        seg2 = Segment2D(Point2D(0, 2), Point2D(2, 0))
        itype, result = segment_segment_intersection_detail(seg1, seg2)
        self.assertEqual(itype, "point")
        self.assertAlmostEqual(result.x, 1.0)
        self.assertAlmostEqual(result.y, 1.0)

    def test_segment_segment_intersection_detail_no_intersection(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(1, 1))
        seg2 = Segment2D(Point2D(2, 2), Point2D(3, 3))
        itype, result = segment_segment_intersection_detail(seg1, seg2)
        self.assertIn(itype, ("none", "collinear_no_overlap"))
        self.assertIsNone(result)

    def test_segment_segment_intersection_detail_overlap(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(3, 3))
        seg2 = Segment2D(Point2D(1, 1), Point2D(4, 4))
        itype, result = segment_segment_intersection_detail(seg1, seg2)
        self.assertEqual(itype, "overlap")
        self.assertIsInstance(result, tuple)
        self.assertTrue(all(isinstance(pt, Point2D) for pt in result))

    def test_segment_segment_intersection_detail_collinear_no_overlap(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(1, 1))
        seg2 = Segment2D(Point2D(2, 2), Point2D(3, 3))
        itype, result = segment_segment_intersection_detail(seg1, seg2)
        self.assertEqual(itype, "collinear_no_overlap")
        self.assertIsNone(result)

    def test_line_polygon_intersections_simple_square(self):
        square = Polygon([
            Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2)
        ])
        line = Line2D(Point2D(1, -1), Vector2D(0, 1))
        intersections = line_polygon_intersections(line, square)
        self.assertEqual(len(intersections), 2)
        self.assertTrue(any(abs(pt.y - 0) < 1e-7 for pt in intersections))
        self.assertTrue(any(abs(pt.y - 2) < 1e-7 for pt in intersections))

    def test_line_polygon_intersections_parallel_no_intersection(self):
        triangle = Polygon([
            Point2D(0, 0), Point2D(1, 0), Point2D(0.5, 1)
        ])
        line = Line2D(Point2D(0, 2), Vector2D(1, 0))  # Above triangle, parallel
        intersections = line_polygon_intersections(line, triangle)
        self.assertEqual(len(intersections), 0)

    def test_segment_circle_intersections_no_intersection(self):
        seg = Segment2D(Point2D(0, 0), Point2D(1, 0))
        circle = Circle(Point2D(5, 5), 1)
        intersections = segment_circle_intersections(seg, circle)
        self.assertEqual(len(intersections), 0)

    def test_segment_circle_intersections_two_points(self):
        seg = Segment2D(Point2D(-2, 0), Point2D(2, 0))
        circle = Circle(Point2D(0, 0), 1)
        intersections = segment_circle_intersections(seg, circle)
        self.assertEqual(len(intersections), 2)
        xs = sorted(pt.x for pt in intersections)
        self.assertAlmostEqual(xs[0], -1)
        self.assertAlmostEqual(xs[1], 1)

    def test_segment_circle_intersections_tangent(self):
        seg = Segment2D(Point2D(-1, 1), Point2D(1, 1))
        circle = Circle(Point2D(0, 0), 1)
        intersections = segment_circle_intersections(seg, circle)
        self.assertEqual(len(intersections), 1)
        self.assertAlmostEqual(intersections[0].x, 0)
        self.assertAlmostEqual(intersections[0].y, 1)

if __name__ == "__main__":
    unittest.main()
