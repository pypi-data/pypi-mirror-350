# (1) python tests/primitives_2d/test_line.py
# (2) python -m unittest tests/primitives_2d/test_line.py (verbose output) (auto add sys.path)

from __future__ import annotations

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.primitives_2d import Line2D, Segment2D, Ray2D
from geo.core import Point2D, Vector2D
from geo.core.precision import DEFAULT_EPSILON, is_equal

# ---------------------------------------------------------------------------
# LINE 2D
# ---------------------------------------------------------------------------
class TestLine2DConstruction(unittest.TestCase):
    """Constructor validation for Line2D."""

    def test_two_point_constructor(self):
        p1, p2 = Point2D(0, 0), Point2D(1, 1)
        line = Line2D(p1, p2)
        self.assertEqual(line.p1, p1)
        self.assertTrue(is_equal(line.direction.x, 2 ** -0.5))
        self.assertTrue(is_equal(line.direction.y, 2 ** -0.5))

    def test_point_and_vector_constructor(self):
        p = Point2D(0, 0)
        v = Vector2D(0, 3)
        line = Line2D(p, v)
        self.assertEqual(line.p1, p)
        self.assertTrue(is_equal(line.direction.x, 0))
        self.assertTrue(is_equal(line.direction.y, 1))

    def test_identical_points_raises(self):
        p = Point2D(1, 1)
        with self.assertRaises(ValueError):
            Line2D(p, p)

    def test_zero_vector_raises(self):
        p = Point2D(0, 0)
        with self.assertRaises(ValueError):
            Line2D(p, Vector2D(0, 0))


class TestLine2DBehaviour(unittest.TestCase):
    """General behaviour and relations between lines."""

    def setUp(self):
        self.line = Line2D(Point2D(0, 0), Point2D(2, 2))  # y = x

    def test_point_at(self):
        p = self.line.point_at(3.0)
        self.assertTrue(self.line.contains_point(p))

    def test_contains_point_noise(self):
        noisy = Point2D(1 + 1e-10, 1 - 1e-10)
        self.assertTrue(self.line.contains_point(noisy))

    def test_parallel_and_perpendicular(self):
        parallel = Line2D(Point2D(0, 1), Vector2D(1, 1))
        perpendicular = Line2D(Point2D(0, 0), Vector2D(-1, 1))  # slope -1
        self.assertTrue(self.line.is_parallel_to(parallel))
        self.assertTrue(self.line.is_perpendicular_to(perpendicular))

    def test_intersection(self):
        other = Line2D(Point2D(0, 1), Vector2D(1, -1))  # y = -x + 1
        ip = self.line.intersection_with(other)
        self.assertEqual(ip, Point2D(0.5, 0.5))

    def test_distance_to_point(self):
        d = self.line.distance_to_point(Point2D(1, 0))
        self.assertAlmostEqual(d, 1 / math.sqrt(2), places=6)

    def test_near_parallel_tolerance(self):
        base = Line2D(Point2D(0, 0), Vector2D(1, 0))
        off = Line2D(Point2D(0, 1), Vector2D(1, DEFAULT_EPSILON / 10))
        self.assertTrue(base.is_parallel_to(off))

# ---------------------------------------------------------------------------
# SEGMENT 2D
# ---------------------------------------------------------------------------
class TestSegment2DBasic(unittest.TestCase):
    """Constructor and basic properties."""

    def setUp(self):
        self.seg = Segment2D(Point2D(0, 0), Point2D(3, 4))  # length 5

    def test_length_midpoint_direction(self):
        self.assertEqual(self.seg.length, 5)
        self.assertEqual(self.seg.midpoint, Point2D(1.5, 2))
        self.assertEqual(self.seg.direction_vector, Vector2D(3, 4))

    def test_contains_point(self):
        self.assertTrue(self.seg.contains_point(Point2D(1.5, 2)))
        self.assertFalse(self.seg.contains_point(Point2D(4, 5)))

    def test_to_line(self):
        line = self.seg.to_line()
        self.assertTrue(line.contains_point(self.seg.p1))
        self.assertTrue(line.contains_point(self.seg.p2))

    def test_zero_length_segment_raises(self):
        p = Point2D(1, 1)
        with self.assertRaises(ValueError):
            Segment2D(p, p)


class TestSegment2DIntersections(unittest.TestCase):
    """Segment–segment intersection edge‑cases."""

    def test_simple_cross(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(3, 3))
        s2 = Segment2D(Point2D(0, 3), Point2D(3, 0))
        ip = s1.intersection_with_segment(s2)
        self.assertEqual(ip, Point2D(1.5, 1.5))

    def test_collinear_overlap(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(4, 0))
        s2 = Segment2D(Point2D(2, 0), Point2D(6, 0))

        from geo.operations import segment_segment_intersection_detail  # type: ignore
        itype, result = segment_segment_intersection_detail(s1, s2)

        self.assertEqual(itype, "overlap")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(p, Point2D) for p in result))

        expected = Segment2D(Point2D(2, 0), Point2D(4, 0))
        self.assertTrue(
            (result[0] == expected.p1 and result[1] == expected.p2) or
            (result[0] == expected.p2 and result[1] == expected.p1),
            f"Expected overlapping segment {expected}, got {result}"
        )

    def test_disjoint_parallel(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(1, 0))
        s2 = Segment2D(Point2D(0, 1), Point2D(1, 1))
        self.assertIsNone(s1.intersection_with_segment(s2))

    def setUp(self):
        # Example: horizontal segment from (0, 0) to (4, 0)
        self.seg = Segment2D(Point2D(0, 0), Point2D(4, 0))

    def test_distance_to_point_inside_projection(self):
        p = Point2D(1, 2)
        d = self.seg.distance_to_point(p := Point2D(1, 2))
        self.assertAlmostEqual(d, 2)

# ---------------------------------------------------------------------------
# RAY 2D
# ---------------------------------------------------------------------------
class TestRay2D(unittest.TestCase):
    """Construction and behaviour for Ray2D."""

    def test_constructor_zero_vector_raises(self):
        with self.assertRaises(ValueError):
            Ray2D(Point2D(0, 0), Vector2D(0, 0))

    def test_point_at(self):
        ray = Ray2D(Point2D(0, 0), Vector2D(1, 1))
        p = ray.point_at(math.sqrt(2))
        self.assertEqual(p, Point2D(1.0, 1.0))

    def test_point_at_negative_raises(self):
        ray = Ray2D(Point2D(0, 0), Vector2D(1, 0))
        with self.assertRaises(ValueError):
            ray.point_at(-0.1)

    def test_equality_normalises_direction(self):
        r1 = Ray2D(Point2D(0, 0), Vector2D(2, 0))
        r2 = Ray2D(Point2D(0, 0), Vector2D(1, 0))
        self.assertEqual(r1, r2)


if __name__ == "__main__":
    unittest.main()
