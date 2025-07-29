# (1) python tests/primitives_2d/curve/test_spline.py
# (2) python -m unittest tests/primitives_2d/curve/test_spline.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from geo.primitives_2d.curve.spline import SplineCurve, _uniform_clamped_knots
from geo.core import Point2D, Vector2D

class TestSplineCurve(unittest.TestCase):

    def test_uniform_clamped_knots_basic(self):
        knots = _uniform_clamped_knots(4, 3)
        self.assertEqual(len(knots), 4 + 3 + 2)
        self.assertAlmostEqual(knots[0], 0.0)
        self.assertAlmostEqual(knots[-1], 1.0)
        self.assertTrue(all(knots[i] <= knots[i+1] for i in range(len(knots)-1)))

    def test_init_invalid_degree(self):
        pts = [Point2D(x, 0) for x in range(4)]
        with self.assertRaises(ValueError):
            SplineCurve(pts, degree=0)

    def test_init_insufficient_control_points(self):
        pts = [Point2D(0, 0), Point2D(1, 1)]
        with self.assertRaises(ValueError):
            SplineCurve(pts, degree=3)

    def test_init_invalid_knot_length(self):
        pts = [Point2D(x, 0) for x in range(5)]
        knots = [0, 0, 0, 1, 1]  # too short for p=3, n=4 (need 9)
        with self.assertRaises(ValueError):
            SplineCurve(pts, degree=3, knots=knots)

    def test_init_nonmonotonic_knots(self):
        pts = [Point2D(x, 0) for x in range(5)]
        knots = [0, 0, 0, 0.5, 0.4, 1, 1, 1, 1]
        with self.assertRaises(ValueError):
            SplineCurve(pts, degree=3, knots=knots)

    def setUp(self):
        # Runs before each test
        self.pts = [Point2D(x, x*x) for x in range(5)]
        self.bs = SplineCurve(self.pts, degree=3)

    def test_find_span_basic(self):
        bs = self.bs
        # Lower and upper boundaries
        self.assertEqual(bs.find_span(bs.knots[bs.p]), bs.p)
        self.assertEqual(bs.find_span(bs.knots[bs.n + 1]), bs.n)

        # Pick a u strictly inside the first non-zero span (k_p , k_{p+1})
        u_mid = (bs.knots[bs.p] + bs.knots[bs.p + 1]) / 2.0
        span = bs.find_span(u_mid)

        self.assertTrue(bs.knots[span] <= u_mid < bs.knots[span + 1])
        # It should be the first non-zero span: index == p
        self.assertEqual(span, bs.p)

    def test_basis_functions_partition_of_unity(self):
        bs = self.bs
        u = (bs.knots[bs.p] + bs.knots[bs.n+1]) / 2
        i = bs.find_span(u)
        N = bs.basis_functions(i, u)
        self.assertEqual(len(N), bs.p + 1)
        self.assertAlmostEqual(sum(N), 1.0, places=12)
        self.assertTrue(all(x >= 0 for x in N))

    def test_basis_function_derivatives_order_limits(self):
        bs = self.bs
        u = (bs.knots[bs.p] + bs.knots[bs.n+1]) / 2
        i = bs.find_span(u)
        ders = bs.basis_function_derivatives(i, u, d=5)
        # d capped at degree = 3, so expect 4 rows of derivatives (0 to 3)
        self.assertEqual(len(ders), bs.p + 1)
        self.assertAlmostEqual(sum(ders[0]), 1.0, places=12)

    def test_point_at_known_points(self):
        bs = self.bs
        start = bs.point_at(bs.knots[bs.p])
        self.assertAlmostEqual(start.x, bs.control_points[0].x)
        self.assertAlmostEqual(start.y, bs.control_points[0].y)
        end = bs.point_at(bs.knots[bs.n+1])
        self.assertAlmostEqual(end.x, bs.control_points[-1].x)
        self.assertAlmostEqual(end.y, bs.control_points[-1].y)
        mid_param = (bs.knots[bs.p] + bs.knots[bs.n+1]) / 2
        mid_point = bs.point_at(mid_param)
        self.assertIsInstance(mid_point, Point2D)

    def test_point_at_clamps_out_of_domain(self):
        bs = self.bs
        below = bs.point_at(bs.knots[bs.p] - 1)
        above = bs.point_at(bs.knots[bs.n+1] + 1)
        self.assertAlmostEqual(below.x, bs.control_points[0].x)
        self.assertAlmostEqual(above.x, bs.control_points[-1].x)

    def test_tangent_at_matches_numerical_derivative(self):
        bs = self.bs
        u = (bs.knots[bs.p] + bs.knots[bs.n+1]) / 2
        tangent = bs.tangent_at(u)
        eps = 1e-6
        p1 = bs.point_at(u - eps)
        p2 = bs.point_at(u + eps)
        dx = (p2.x - p1.x) / (2 * eps)
        dy = (p2.y - p1.y) / (2 * eps)
        self.assertAlmostEqual(tangent.x, dx, delta=abs(dx)*1e-3)
        self.assertAlmostEqual(tangent.y, dy, delta=abs(dy)*1e-3)

    def test_insert_knot_multiplicity_limit(self):
        bs = self.bs
        u = bs.knots[bs.p + 1]
        max_insert = bs.p - bs.knots.count(u)
        bs.insert_knot(u, max_insert)
        with self.assertRaises(ValueError):
            bs.insert_knot(u)

    def test_insert_knot_geometry_changes(self):
        pts = [Point2D(0, 0), Point2D(1, 2), Point2D(3, 3), Point2D(4, 0)]
        bs = SplineCurve(pts, degree=2)
        
        # Choose a knot inside a non-zero span (strictly between interior knots)
        u = (bs.knots[bs.p] + bs.knots[bs.p + 1]) / 2.0
        
        # Ensure it is not already repeated p times
        existing_multiplicity = bs.knots.count(u)
        self.assertLess(existing_multiplicity, bs.p, "Knot already has full multiplicity.")

        before_pts = list(bs.control_points)
        bs.insert_knot(u)
        after_pts = bs.control_points

        # After inserting once, should gain 1 control point
        self.assertEqual(len(after_pts), len(before_pts) + 1)

        # Knot vector should grow by 1
        self.assertEqual(len(bs.knots), len(before_pts) + bs.p + 2)

        pt_before = bs.point_at(u)
        self.assertIsInstance(pt_before, Point2D)

    def test_elevate_degree_increases_degree_and_points(self):
        pts = [Point2D(x, math.sin(x)) for x in range(5)]
        bs = SplineCurve(pts, degree=2)
        old_degree = bs.p
        old_n = bs.n
        old_pts = list(bs.control_points)
        bs.elevate_degree()
        self.assertEqual(bs.p, old_degree + 1)
        self.assertEqual(bs.n, len(bs.control_points) - 1)
        self.assertEqual(len(bs.control_points), old_n + 2)
        self.assertNotEqual(bs.control_points, old_pts)

    def test_to_bezier_segments_cubic_and_error(self):
        pts = [Point2D(x, math.cos(x)) for x in range(6)]
        bs = SplineCurve(pts, degree=3)
        segments = bs.to_bezier_segments()
        self.assertIsInstance(segments, list)
        self.assertTrue(all(len(seg) == 4 for seg in segments))
        self.assertEqual(len(segments), bs.n - bs.p + 1)
        bs_deg2 = SplineCurve(pts, degree=2)
        with self.assertRaises(NotImplementedError):
            bs_deg2.to_bezier_segments()


if __name__ == "__main__":
    unittest.main()
