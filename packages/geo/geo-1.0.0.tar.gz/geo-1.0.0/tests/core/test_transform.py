# (1) python tests/core/test_transform.py
# (2) python -m unittest tests/core/test_transform.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point2D, Point3D, Vector2D, Vector3D
from geo.core import translate, scale, rotate_2d, rotate_3d
from geo.core.precision import is_equal

class TestTransform(unittest.TestCase):

    def test_translate_point2d(self):
        p = Point2D(1, 2)
        offset = Vector2D(3, -1)
        translated_p = translate(p, offset)
        self.assertIsInstance(translated_p, Point2D)
        self.assertEqual(translated_p, Point2D(4, 1))

    def test_translate_vector2d(self):
        v = Vector2D(1, 2)
        offset = Vector2D(3, -1)
        # Translating a vector (as a displacement) means adding another vector
        translated_v = translate(v, offset)
        self.assertIsInstance(translated_v, Vector2D)
        self.assertEqual(translated_v, Vector2D(4, 1))

    def test_translate_point3d(self):
        p = Point3D(1, 2, 3)
        offset = Vector3D(3, -1, 0.5)
        translated_p = translate(p, offset)
        self.assertIsInstance(translated_p, Point3D)
        self.assertEqual(translated_p, Point3D(4, 1, 3.5))

    def test_translate_vector3d(self):
        v = Vector3D(1, 2, 3)
        offset = Vector3D(3, -1, 0.5)
        translated_v = translate(v, offset)
        self.assertIsInstance(translated_v, Vector3D)
        self.assertEqual(translated_v, Vector3D(4, 1, 3.5))

    def test_translate_errors(self):
        p2d = Point2D(1,1)
        v3d = Vector3D(1,1,1)
        with self.assertRaises(ValueError): # Dimension mismatch
            translate(p2d, v3d)
        with self.assertRaises(TypeError): # Invalid offset type
            translate(p2d, Point2D(1,1)) # type: ignore


    def test_scale_point2d_uniform(self):
        p = Point2D(2, 3)
        scaled_p = scale(p, 2.0) # Scale about origin
        self.assertEqual(scaled_p, Point2D(4, 6))

        origin = Point2D(1, 1)
        scaled_p_origin = scale(p, 2.0, origin=origin)
        # P' = O + factor * (P - O)
        # P-O = (1, 2)
        # factor*(P-O) = (2, 4)
        # O + (2,4) = (1,1) + (2,4) = (3,5)
        self.assertEqual(scaled_p_origin, Point2D(3, 5))

    def test_scale_point2d_non_uniform(self):
        p = Point2D(2, 3)
        factors = Vector2D(2, 0.5)
        scaled_p = scale(p, factors) # Scale about origin
        self.assertEqual(scaled_p, Point2D(4, 1.5))

        origin = Point2D(1, 2)
        # P-O = (1, 1)
        # Scaled P-O = (1*2, 1*0.5) = (2, 0.5)
        # O + Scaled P-O = (1,2) + (2,0.5) = (3, 2.5)
        scaled_p_origin = scale(p, factors, origin=origin)
        self.assertEqual(scaled_p_origin, Point2D(3, 2.5))

    def test_scale_vector2d(self):
        v = Vector2D(2, 3)
        # For vectors (directions), origin is usually ignored.
        scaled_v_uniform = scale(v, 2.0)
        self.assertEqual(scaled_v_uniform, Vector2D(4, 6))
        
        scaled_v_non_uniform = scale(v, Vector2D(0.5, 3))
        self.assertEqual(scaled_v_non_uniform, Vector2D(1, 9))

        # Test with origin (should be ignored for vector scaling in current impl)
        scaled_v_origin_ignored = scale(v, 2.0, origin=Point2D(10,10))
        self.assertEqual(scaled_v_origin_ignored, Vector2D(4,6))


    def test_scale_point3d(self):
        p = Point3D(1,2,3)
        scaled_p_uniform = scale(p, 3.0)
        self.assertEqual(scaled_p_uniform, Point3D(3,6,9))

        factors = Vector3D(2, 0.5, 1)
        scaled_p_non_uniform = scale(p, factors)
        self.assertEqual(scaled_p_non_uniform, Point3D(2, 1, 3))

        origin = Point3D(0,1,0)
        # P-O = (1,1,3)
        # Scaled P-O = (1*2, 1*0.5, 3*1) = (2, 0.5, 3)
        # O + Scaled P-O = (0,1,0) + (2,0.5,3) = (2, 1.5, 3)
        scaled_p_origin = scale(p, factors, origin=origin)
        self.assertEqual(scaled_p_origin, Point3D(2, 1.5, 3))

    def test_scale_errors(self):
        p2d = Point2D(1,1)
        v3d_factors = Vector3D(1,1,1)
        with self.assertRaises(ValueError): # Dimension mismatch for factors
            scale(p2d, v3d_factors)
        with self.assertRaises(TypeError): # Invalid factors type
            scale(p2d, Point2D(1,1)) # type: ignore
        with self.assertRaises(TypeError): # Invalid origin type
            scale(p2d, 2.0, origin=Vector2D(1,1)) # type: ignore


    def test_rotate_2d_point(self):
        p = Point2D(1, 0)
        # Rotate 90 deg CCW around origin -> (0, 1)
        rotated_p1 = rotate_2d(p, math.pi / 2)
        self.assertEqual(rotated_p1, Point2D(0, 1))

        # Rotate 180 deg CCW around origin -> (-1, 0)
        rotated_p2 = rotate_2d(p, math.pi)
        self.assertEqual(rotated_p2, Point2D(-1, 0))

        # Rotate point (2,1) by 90 deg CCW around origin (1,1)
        # P=(2,1), O=(1,1) => P-O = (1,0)
        # Rotated P-O = (0,1)
        # O + Rotated P-O = (1,1) + (0,1) = (1,2)
        p_complex = Point2D(2,1)
        origin = Point2D(1,1)
        rotated_p_origin = rotate_2d(p_complex, math.pi/2, origin=origin)
        self.assertEqual(rotated_p_origin, Point2D(1,2))

    def test_rotate_2d_vector(self):
        v = Vector2D(1, 0)
        # Rotate 90 deg CCW -> (0, 1) (origin ignored for vectors)
        rotated_v1 = rotate_2d(v, math.pi / 2, origin=Point2D(10,10))
        self.assertEqual(rotated_v1, Vector2D(0, 1))


    def test_rotate_3d_point_simple_axis(self):
        p = Point3D(1, 0, 0) # Point on x-axis

        # Rotate around Z-axis by 90 deg (pi/2)
        # (1,0,0) -> (0,1,0)
        axis_z = Vector3D(0, 0, 1)
        rotated_p_z = rotate_3d(p, axis_z, math.pi / 2)
        self.assertEqual(rotated_p_z, Point3D(0, 1, 0))

        # Rotate (0,1,0) around X-axis by 90 deg (pi/2)
        # (0,1,0) -> (0,0,1)
        p_on_y = Point3D(0,1,0)
        axis_x = Vector3D(1,0,0)
        rotated_p_x = rotate_3d(p_on_y, axis_x, math.pi/2)
        self.assertEqual(rotated_p_x, Point3D(0,0,1))

        # Rotate (0,0,1) around Y-axis by 90 deg (pi/2)
        # (0,0,1) -> (1,0,0)
        p_on_z = Point3D(0,0,1)
        axis_y = Vector3D(0,1,0)
        rotated_p_y = rotate_3d(p_on_z, axis_y, math.pi/2)
        self.assertEqual(rotated_p_y, Point3D(1,0,0))

    def test_rotate_3d_point_with_origin(self):
        # Point P(2,1,0), Axis Z(0,0,1), Angle 90 deg, Origin O(1,1,0)
        # P-O = (1,0,0)
        # Rotated (P-O) around Z-axis by 90 deg = (0,1,0)
        # O + Rotated(P-O) = (1,1,0) + (0,1,0) = (1,2,0)
        p = Point3D(2,1,0)
        axis = Vector3D(0,0,1)
        angle = math.pi/2
        origin = Point3D(1,1,0)
        rotated_p = rotate_3d(p, axis, angle, origin=origin)
        self.assertEqual(rotated_p, Point3D(1,2,0))

    def test_rotate_3d_vector(self):
        # Vector V(1,0,0), Axis Z(0,0,1), Angle 90 deg
        # Result should be (0,1,0) (origin is ignored for vector rotation)
        v = Vector3D(1,0,0)
        axis = Vector3D(0,0,1)
        angle = math.pi/2
        rotated_v = rotate_3d(v, axis, angle, origin=Point3D(10,20,30))
        self.assertEqual(rotated_v, Vector3D(0,1,0))

    def test_rotate_3d_identity(self):
        p = Point3D(1,2,3)
        axis = Vector3D(1,1,1) # Any non-zero axis
        # Rotate by 0 angle
        rotated_p_zero_angle = rotate_3d(p, axis, 0.0)
        self.assertEqual(rotated_p_zero_angle, p)
        # Rotate by 2*pi angle
        rotated_p_2pi_angle = rotate_3d(p, axis, 2 * math.pi)
        self.assertEqual(rotated_p_2pi_angle, p)

    def test_rotate_3d_errors(self):
        p3d = Point3D(1,1,1)
        v_axis = Vector3D(0,0,1)
        angle = math.pi/2
        with self.assertRaises(TypeError): # Invalid entity
            rotate_3d(Vector2D(1,0), v_axis, angle) # type: ignore
        with self.assertRaises(TypeError): # Invalid axis
            rotate_3d(p3d, Point3D(0,0,1), angle) # type: ignore
        with self.assertRaises(ValueError): # Zero axis
            rotate_3d(p3d, Vector3D(0,0,0), angle)
        with self.assertRaises(TypeError): # Invalid origin
            rotate_3d(p3d, v_axis, angle, origin=Vector3D(0,0,0)) # type: ignore


if __name__ == '__main__':
    unittest.main()