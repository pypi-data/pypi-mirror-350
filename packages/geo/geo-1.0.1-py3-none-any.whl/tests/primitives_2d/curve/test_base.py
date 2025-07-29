# (1) python tests/primitives_2d/curve/test_base.py
# (2) python -m unittest tests/primitives_2d/curve/test_base.py (verbose output) (auto add sys.path)

from __future__ import annotations

import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from geo.primitives_2d.curve.base import Curve2D
from geo.core import Point2D, Vector2D


class DummyCurve(Curve2D):
    """
    A simple linear curve for testing: C(t) = (1 - t) * P0 + t * P1
    """

    def point_at(self, t: float) -> Point2D:
        p0, p1 = self.control_points
        x = (1 - t) * p0.x + t * p1.x
        y = (1 - t) * p0.y + t * p1.y
        return Point2D(x, y)

    def tangent_at(self, t: float) -> Vector2D:
        p0, p1 = self.control_points
        return Vector2D(p1.x - p0.x, p1.y - p0.y)


class TestCurve2D(unittest.TestCase):

    def setUp(self):
        self.p0 = Point2D(0, 0)
        self.p1 = Point2D(3, 4)
        self.curve = DummyCurve([self.p0, self.p1])

    def test_control_points_storage(self):
        self.assertEqual(len(self.curve), 2)
        self.assertEqual(self.curve.control_points[0], self.p0)

    def test_point_at(self):
        self.assertEqual(self.curve.point_at(0), self.p0)
        self.assertEqual(self.curve.point_at(1), self.p1)
        mid = self.curve.point_at(0.5)
        self.assertAlmostEqual(mid.x, 1.5)
        self.assertAlmostEqual(mid.y, 2.0)

    def test_tangent_at(self):
        tangent = self.curve.tangent_at(0.5)
        self.assertEqual(tangent.x, 3)
        self.assertEqual(tangent.y, 4)

    def test_derivative_alias(self):
        d = self.curve.derivative_at(0.3)
        self.assertEqual(d, self.curve.tangent_at(0.3))

    def test_length(self):
        length = self.curve.length()
        self.assertAlmostEqual(length, 5.0, places=3)

    def test_length_partial(self):
        length_half = self.curve.length(0.0, 0.5)
        self.assertAlmostEqual(length_half, 2.5, delta=0.05)

    def test_length_reversed_bounds(self):
        length = self.curve.length(1.0, 0.0)
        self.assertAlmostEqual(length, 5.0, places=3)

    def test_length_same_bounds(self):
        self.assertEqual(self.curve.length(0.5, 0.5), 0.0)

    def test_repr(self):
        rep = repr(self.curve)
        self.assertIn("DummyCurve", rep)
        self.assertIn("control_points", rep)

    def test_invalid_constructor_empty(self):
        with self.assertRaises(ValueError):
            DummyCurve([])

    def test_invalid_control_point_type(self):
        with self.assertRaises(TypeError):
            DummyCurve([self.p0, "not a point"])

    def test_iter_and_len(self):
        pts = list(self.curve)
        self.assertEqual(pts, [self.p0, self.p1])
        self.assertEqual(len(self.curve), 2)

    def test_length_invalid_segments(self):
        with self.assertRaises(ValueError):
            self.curve.length(num_segments=0)

    # ---------- Additional edge-case tests ----------

    def test_point_at_out_of_bounds(self):
        p_neg = self.curve.point_at(-0.1)
        p_overshoot = self.curve.point_at(1.1)
        self.assertIsInstance(p_neg, Point2D)
        self.assertIsInstance(p_overshoot, Point2D)

    def test_zero_length_curve(self):
        curve = DummyCurve([Point2D(1, 1), Point2D(1, 1)])
        self.assertAlmostEqual(curve.length(), 0.0)
        tangent = curve.tangent_at(0.5)
        self.assertEqual(tangent, Vector2D(0, 0))

    def test_small_parameter_interval(self):
        l = self.curve.length(0.0, 1e-10, num_segments=10)
        self.assertAlmostEqual(l, 0.0, places=6)

    def test_length_high_resolution(self):
        l = self.curve.length(num_segments=10000)
        self.assertAlmostEqual(l, 5.0, places=4)

    def test_curve2d_is_abstract(self):
        with self.assertRaises(TypeError):
            Curve2D([self.p0])  # Cannot instantiate abstract class


if __name__ == '__main__':
    unittest.main()
