# (1) python tests/primitives_2d/curve/test_bezier.py
# (2) python -m unittest tests/primitives_2d/curve/test_bezier.py (verbose output) (auto add sys.path)

import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from geo.core import Point2D, Vector2D
from geo.primitives_2d.curve.bezier import BezierCurve

class TestBezierCurve(unittest.TestCase):

    def test_invalid_control_points(self):
        with self.assertRaises(ValueError):
            BezierCurve([])
        with self.assertRaises(ValueError):
            BezierCurve([Point2D(0, 0)])

    def test_linear_bezier(self):
        p0 = Point2D(0, 0)
        p1 = Point2D(1, 1)
        curve = BezierCurve([p0, p1])
        self.assertEqual(curve.degree, 1)
        self.assertEqual(curve.point_at(0.0), p0)
        self.assertEqual(curve.point_at(1.0), p1)
        self.assertEqual(curve.point_at(0.5), Point2D(0.5, 0.5))
        self.assertEqual(curve.tangent_at(0.3), p1 - p0)

    def test_quadratic_bezier(self):
        p0 = Point2D(0, 0)
        p1 = Point2D(1, 2)
        p2 = Point2D(2, 0)
        curve = BezierCurve([p0, p1, p2])
        self.assertEqual(curve.degree, 2)
        pt = curve.point_at(0.5)
        self.assertTrue(isinstance(pt, Point2D))
        tangent = curve.tangent_at(0.5)
        self.assertTrue(isinstance(tangent, Vector2D))

    def test_cubic_bezier(self):
        p0 = Point2D(0, 0)
        p1 = Point2D(1, 3)
        p2 = Point2D(2, 3)
        p3 = Point2D(3, 0)
        curve = BezierCurve([p0, p1, p2, p3])
        pt = curve.point_at(0.25)
        pt_casteljau = curve.point_at(0.25, use_casteljau=True)
        self.assertAlmostEqual(pt.x, pt_casteljau.x, places=10)
        self.assertAlmostEqual(pt.y, pt_casteljau.y, places=10)

    def test_tangent_zero_degree(self):
        # Should be replaced with a 2-point zero vector curve
        curve = BezierCurve([Point2D(0, 0), Point2D(0, 0)])
        self.assertEqual(curve.tangent_at(0.5), Vector2D(0.0, 0.0))

    def test_extrapolation(self):
        p0 = Point2D(0, 0)
        p1 = Point2D(1, 1)
        curve = BezierCurve([p0, p1])
        pt_low = curve.point_at(-0.5)
        pt_high = curve.point_at(1.5)
        self.assertTrue(isinstance(pt_low, Point2D))
        self.assertTrue(isinstance(pt_high, Point2D))

    def test_derivative_curve(self):
        p0 = Point2D(0, 0)
        p1 = Point2D(2, 2)
        p2 = Point2D(4, 0)
        curve = BezierCurve([p0, p1, p2])
        deriv = curve.derivative_curve()
        self.assertEqual(deriv.degree, 1)
        t0 = curve.tangent_at(0.3)
        t1 = deriv.point_at(0.3)
        self.assertAlmostEqual(t0.x, t1.x, places=10)
        self.assertAlmostEqual(t0.y, t1.y, places=10)

    def test_repr(self):
        curve = BezierCurve([Point2D(0, 0), Point2D(1, 1)])
        self.assertIn("BezierCurve", repr(curve))

if __name__ == '__main__':
    unittest.main()
