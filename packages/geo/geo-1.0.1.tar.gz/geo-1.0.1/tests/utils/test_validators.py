# (1) python tests/utils/test_validators.py
# (2) python -m unittest tests/utils/test_validators.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.utils.validators import (
    validate_non_negative,
    validate_positive,
    validate_list_of_points,
    validate_polygon_vertices,
)
from geo.core import Point2D, Point3D


class TestValidators(unittest.TestCase):
    # ------------------------------------------------------------------ #
    # validate_non_negative                                              #
    # ------------------------------------------------------------------ #
    def test_validate_non_negative_valid(self):
        # Zero and positive should pass
        validate_non_negative(0)
        validate_non_negative(1e9)
        validate_non_negative(3.14159)

    def test_validate_non_negative_errors(self):
        # Negative value
        with self.assertRaises(ValueError):
            validate_non_negative(-1, name="radius")

        # NaN / infinity
        for bad in (math.nan, math.inf, -math.inf):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_non_negative(bad)

        # Non-numeric types
        with self.assertRaises(TypeError):
            validate_non_negative("5")  # type: ignore[arg-type]

        with self.assertRaises(TypeError):
            validate_non_negative([], name="value")  # type: ignore[arg-type]

    # ------------------------------------------------------------------ #
    # validate_positive                                                  #
    # ------------------------------------------------------------------ #
    def test_validate_positive_valid(self):
        validate_positive(1)
        validate_positive(0.0001)

    def test_validate_positive_errors(self):
        for bad in (0, -0.1, -10):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_positive(bad)

        for bad in (math.nan, math.inf, -math.inf):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_positive(bad)

        with self.assertRaises(TypeError):
            validate_positive(None)  # type: ignore[arg-type]

    # ------------------------------------------------------------------ #
    # validate_list_of_points                                            #
    # ------------------------------------------------------------------ #
    def test_validate_list_of_points_valid(self):
        pts2 = [Point2D(0, 0), Point2D(1, 1)]
        validate_list_of_points(pts2, min_points=2)

        pts3 = [Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0)]
        validate_list_of_points(pts3, min_points=3, point_type=Point3D)

    def test_validate_list_of_points_not_sequence(self):
        with self.assertRaises(TypeError):
            validate_list_of_points("not a list")  # type: ignore[arg-type]

    def test_validate_list_of_points_too_few(self):
        with self.assertRaises(ValueError):
            validate_list_of_points([Point2D(0, 0)], min_points=2)

    def test_validate_list_of_points_wrong_type(self):
        pts_mixed = [Point2D(0, 0), "bad", Point2D(1, 1)]  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            validate_list_of_points(pts_mixed)

        pts_wrong = [Point2D(0, 0), Point2D(1, 1)]
        with self.assertRaises(TypeError):
            validate_list_of_points(pts_wrong, point_type=Point3D)

    # ------------------------------------------------------------------ #
    # validate_polygon_vertices                                          #
    # ------------------------------------------------------------------ #
    def test_validate_polygon_vertices_valid(self):
        vertices = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)]
        # should not raise
        validate_polygon_vertices(vertices)

    def test_validate_polygon_vertices_errors(self):
        # fewer than 3 vertices
        with self.assertRaises(ValueError):
            validate_polygon_vertices([Point2D(0, 0), Point2D(1, 0)])

        # wrong point type
        bad = [Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0)]
        with self.assertRaises(TypeError):
            validate_polygon_vertices(bad)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
