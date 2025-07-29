# (1) python tests/operations/test_measurements.py
# (2) python -m unittest tests/operations/test_measurements.py (verbose output) (auto add sys.path)

import unittest
import random
import time
import math
import os
import sys

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from geo.core import Point2D, Vector2D, Point3D, Vector3D
from geo.primitives_2d import Segment2D
from geo.primitives_3d import Segment3D, Line3D
from geo.operations.measurements import (
    closest_point_on_segment_to_point,
    distance_segment_segment_2d,
    closest_points_segments_2d,
    signed_angle_between_vectors_2d,
    distance_point_line_3d,
    distance_point_plane,
    distance_line_line_3d
)
from geo.primitives_3d import Plane as Plane3D


class TestMeasurements(unittest.TestCase):
    def test_closest_point_on_segment_to_point(self):
        seg = Segment2D(Point2D(0, 0), Point2D(10, 0))
        pt = Point2D(5, 5)
        expected = Point2D(5, 0)
        result = closest_point_on_segment_to_point(seg, pt)
        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)

    def test_distance_segment_segment_2d(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(1, 0))
        seg2 = Segment2D(Point2D(0, 1), Point2D(1, 1))
        dist = distance_segment_segment_2d(seg1, seg2)
        self.assertAlmostEqual(dist, 1.0)

    def test_closest_points_segments_2d(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(1, 0))
        seg2 = Segment2D(Point2D(0, 1), Point2D(1, 1))
        p1, p2 = closest_points_segments_2d(seg1, seg2)
        self.assertAlmostEqual(p1.distance_to(p2), 1.0)

    def test_signed_angle_between_vectors_2d(self):
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1)
        angle = signed_angle_between_vectors_2d(v1, v2)
        self.assertAlmostEqual(angle, 1.57079632679, places=5)  # ~pi/2

    def test_distance_point_line_3d(self):
        line = Line3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
        pt = Point3D(0, 1, 0)
        dist = distance_point_line_3d(pt, line)
        self.assertAlmostEqual(dist, 1.0)

    def test_distance_point_plane(self):
        plane = Plane3D(Point3D(0, 0, 0), Vector3D(0, 0, 1))
        pt = Point3D(0, 0, 5)
        dist = distance_point_plane(pt, plane)
        self.assertAlmostEqual(dist, 5.0)

    def test_distance_line_line_3d(self):
        l1 = Line3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
        l2 = Line3D(Point3D(0, 1, 1), Vector3D(0, 1, 0))
        dist, cp1, cp2 = distance_line_line_3d(l1, l2)
        self.assertAlmostEqual(dist, 1.0)
        if cp1 and cp2:
            self.assertAlmostEqual(cp1.distance_to(cp2), dist)

class TestMeasurementsEdgeCases(unittest.TestCase):
    def test_zero_length_segment(self):
        p = Point2D(1, 1)
        with self.assertRaises(ValueError):
            _ = Segment2D(p, p)  # degenerate segment

    def test_line_with_zero_direction_raises(self):
        with self.assertRaises(ValueError):
            _ = Line3D(Point3D(0, 0, 0), Vector3D(0, 0, 0))

    def test_closest_points_on_touching_segments(self):
        seg1 = Segment2D(Point2D(0, 0), Point2D(1, 0))
        seg2 = Segment2D(Point2D(1, 0), Point2D(2, 0))
        p1, p2 = closest_points_segments_2d(seg1, seg2)
        self.assertEqual(p1, Point2D(1, 0))
        self.assertEqual(p2, Point2D(1, 0))

    def test_parallel_lines_distance(self):
        l1 = Line3D(Point3D(0, 0, 0), Vector3D(1, 0, 0))
        l2 = Line3D(Point3D(0, 1, 0), Vector3D(1, 0, 0))
        dist, _, _ = distance_line_line_3d(l1, l2)
        self.assertAlmostEqual(dist, 1.0)

class TestMeasurementsPerformance(unittest.TestCase):
    def test_closest_point_performance(self):
        seg = Segment3D(Point3D(0, 0, 0), Point3D(1000, 0, 0))
        pt = Point3D(500, 10, 0)
        start_time = time.time()
        for _ in range(10000):
            _ = closest_point_on_segment_to_point(seg, pt)
        duration = time.time() - start_time
        self.assertLess(duration, 1.0)  # Should run in under 1 second

if __name__ == '__main__':
    unittest.main()
