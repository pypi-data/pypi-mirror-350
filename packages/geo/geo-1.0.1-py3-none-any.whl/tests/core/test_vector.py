# (1) python tests/core/test_vector.py
# (2) python -m unittest tests/core/test_vector.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Vector, Vector2D, Vector3D
from geo.core.precision import DEFAULT_EPSILON, is_equal

class TestVector(unittest.TestCase):

    def test_vector_generic_constructor_and_properties(self):
        v = Vector(1, 2, 3, 4)
        self.assertEqual(v.components, (1, 2, 3, 4))
        self.assertEqual(v.dimension, 4)
        self.assertEqual(v[0], 1)
        self.assertEqual(len(v), 4)
        with self.assertRaises(ValueError):
            Vector()

    def test_vector2d_constructor_and_properties(self):
        v = Vector2D(1.5, 2.5)
        self.assertEqual(v.x, 1.5)
        self.assertEqual(v.y, 2.5)
        self.assertEqual(v.components, (1.5, 2.5))
        self.assertEqual(v.dimension, 2)

    def test_vector3d_constructor_and_properties(self):
        v = Vector3D(1.0, 2.0, 3.0)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)
        self.assertEqual(v.z, 3.0)
        self.assertEqual(v.components, (1.0, 2.0, 3.0))
        self.assertEqual(v.dimension, 3)

    def test_vector_equality(self):
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(1.0, 2.0)
        v3 = Vector2D(1.0000000001, 2.0000000001)
        v4 = Vector2D(1.1, 2.0)
        from geo.core import Point2D # To test type mismatch
        p_other_type = Point2D(1.0, 2.0)


        self.assertEqual(v1, v2)
        self.assertTrue(v1 == v3)
        self.assertNotEqual(v1, v4)
        self.assertFalse(v1 == p_other_type)

        v3d1 = Vector3D(1,2,3)
        v3d2 = Vector3D(1,2,3)
        self.assertEqual(v3d1, v3d2)
        self.assertNotEqual(v1, v3d1)

    def test_vector_repr(self):
        v2d = Vector2D(1, 2)
        self.assertEqual(repr(v2d), "Vector2D(1.0, 2.0)")
        v3d = Vector3D(1, 2, 3)
        self.assertEqual(repr(v3d), "Vector3D(1.0, 2.0, 3.0)")

    def test_vector_hash(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, 2)
        v3 = Vector2D(2, 1)
        s = {v1, v2, v3}
        self.assertEqual(len(s), 2)
        self.assertIn(Vector2D(1,2), s)

    def test_magnitude(self):
        v2 = Vector2D(3, 4)
        self.assertAlmostEqual(v2.magnitude_squared(), 25.0)
        self.assertAlmostEqual(v2.magnitude(), 5.0)

        v3 = Vector3D(1, 2, 2) # mag_sq = 1+4+4=9, mag=3
        self.assertAlmostEqual(v3.magnitude_squared(), 9.0)
        self.assertAlmostEqual(v3.magnitude(), 3.0)
        
        v_zero = Vector2D(0,0)
        self.assertAlmostEqual(v_zero.magnitude_squared(), 0.0)
        self.assertAlmostEqual(v_zero.magnitude(), 0.0)


    def test_normalize(self):
        v2 = Vector2D(3, 4)
        norm_v2 = v2.normalize()
        self.assertIsInstance(norm_v2, Vector2D)
        self.assertAlmostEqual(norm_v2.x, 3/5)
        self.assertAlmostEqual(norm_v2.y, 4/5)
        self.assertAlmostEqual(norm_v2.magnitude(), 1.0)

        v3 = Vector3D(1, 2, 2)
        norm_v3 = v3.normalize()
        self.assertIsInstance(norm_v3, Vector3D)
        self.assertAlmostEqual(norm_v3.x, 1/3)
        self.assertAlmostEqual(norm_v3.y, 2/3)
        self.assertAlmostEqual(norm_v3.z, 2/3)
        self.assertAlmostEqual(norm_v3.magnitude(), 1.0)
        
        v_generic = Vector(1,1,1,1) # mag = sqrt(4) = 2
        norm_v_generic = v_generic.normalize()
        self.assertIsInstance(norm_v_generic, Vector) # Should return base Vector type
        self.assertAlmostEqual(norm_v_generic[0], 0.5)
        self.assertAlmostEqual(norm_v_generic.magnitude(), 1.0)


        with self.assertRaises(ValueError):
            Vector2D(0, 0).normalize()

    def test_is_zero_vector(self):
        self.assertTrue(Vector2D(0, 0).is_zero_vector())
        self.assertTrue(Vector3D(DEFAULT_EPSILON/2, -DEFAULT_EPSILON/2, 0).is_zero_vector())
        self.assertFalse(Vector2D(1, 0).is_zero_vector())
        self.assertFalse(Vector3D(0, DEFAULT_EPSILON*2, 0).is_zero_vector())

    def test_vector_arithmetic(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)

        # Add
        v_add = v1 + v2
        self.assertEqual(v_add, Vector2D(4, 6))
        self.assertIsInstance(v_add, Vector2D)

        # Subtract
        v_sub = v2 - v1
        self.assertEqual(v_sub, Vector2D(2, 2))
        self.assertIsInstance(v_sub, Vector2D)

        # Scalar Multiply
        v_mul_scalar = v1 * 2
        self.assertEqual(v_mul_scalar, Vector2D(2, 4))
        self.assertIsInstance(v_mul_scalar, Vector2D)
        
        v_mul_scalar_float = v1 * 0.5
        self.assertEqual(v_mul_scalar_float, Vector2D(0.5, 1.0))
        self.assertIsInstance(v_mul_scalar_float, Vector2D)


        # Reverse Scalar Multiply
        v_rmul_scalar = 2 * v1
        self.assertEqual(v_rmul_scalar, Vector2D(2, 4))

        # True Division
        v_div_scalar = v1 / 2
        self.assertEqual(v_div_scalar, Vector2D(0.5, 1.0))
        self.assertIsInstance(v_div_scalar, Vector2D) # Components become float

        with self.assertRaises(ZeroDivisionError):
            v1 / 0
        with self.assertRaises(TypeError):
            v1 * Vector2D(1,1) # Vector * Vector (use dot or cross)
        with self.assertRaises(TypeError):
            v1 + Vector3D(1,2,3) # Dimension mismatch


        # Negation
        v_neg = -v1
        self.assertEqual(v_neg, Vector2D(-1, -2))
        self.assertIsInstance(v_neg, Vector2D)
        
        v_int = Vector(1,2) # Generic vector with int components
        v_int_mul_float = v_int * 0.5
        self.assertEqual(v_int_mul_float, Vector(0.5, 1.0))
        self.assertTrue(all(isinstance(c, float) for c in v_int_mul_float.components))
        
        v_int_mul_int = v_int * 2
        self.assertEqual(v_int_mul_int, Vector(2,4))
        self.assertTrue(all(isinstance(c, int) for c in v_int_mul_int.components))


    def test_dot_product(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        self.assertAlmostEqual(v1.dot(v2), 1*3 + 2*4) # 3 + 8 = 11

        v3 = Vector3D(1, 2, 3)
        v4 = Vector3D(4, -5, 6) # 1*4 + 2*(-5) + 3*6 = 4 - 10 + 18 = 12
        self.assertAlmostEqual(v3.dot(v4), 12)

        with self.assertRaises(ValueError):
            v1.dot(v3) # Dimension mismatch

    def test_angle_between(self):
        v1 = Vector2D(1, 0)
        v2 = Vector2D(0, 1) # 90 degrees
        self.assertAlmostEqual(v1.angle_between(v2), math.pi / 2)
        self.assertAlmostEqual(v1.angle_between(v2, in_degrees=True), 90.0)

        v3 = Vector2D(1, 1)
        v4 = Vector2D(-1, 1) # Angle between (1,1) and (-1,1) is 90 deg
                                # dot = 0
        self.assertAlmostEqual(v3.angle_between(v4), math.pi / 2)
        
        v5 = Vector2D(2,0)
        self.assertAlmostEqual(v1.angle_between(v5), 0.0) # Parallel

        v6 = Vector2D(-1,0)
        self.assertAlmostEqual(v1.angle_between(v6), math.pi) # Opposite

        v7 = Vector3D(1,0,0)
        v8 = Vector3D(0,1,0)
        self.assertAlmostEqual(v7.angle_between(v8), math.pi/2)

        with self.assertRaises(ValueError):
            Vector2D(0,0).angle_between(v1)
        with self.assertRaises(ValueError):
            v1.angle_between(Vector2D(0,0))
        with self.assertRaises(ValueError):
            v1.angle_between(Vector3D(1,0,0)) # Dim mismatch

    def test_vector2d_specifics(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)

        # Cross product (scalar)
        # v1.x*v2.y - v1.y*v2.x = 1*4 - 2*3 = 4 - 6 = -2
        self.assertAlmostEqual(v1.cross(v2), -2)

        # Perpendicular
        perp_ccw = v1.perpendicular() # (-y, x) = (-2, 1)
        self.assertEqual(perp_ccw, Vector2D(-2, 1))
        self.assertAlmostEqual(v1.dot(perp_ccw), 0) # Should be orthogonal

        perp_cw = v1.perpendicular(clockwise=True) # (y, -x) = (2, -1)
        self.assertEqual(perp_cw, Vector2D(2, -1))
        self.assertAlmostEqual(v1.dot(perp_cw), 0)

        # Angle
        v_x_axis = Vector2D(1,0)
        self.assertAlmostEqual(v_x_axis.angle(), 0)
        v_45_deg = Vector2D(1,1)
        self.assertAlmostEqual(v_45_deg.angle(), math.pi/4)
        v_y_axis = Vector2D(0,1)
        self.assertAlmostEqual(v_y_axis.angle(), math.pi/2)


    def test_vector3d_specifics(self):
        v1 = Vector3D(1, 0, 0) # i
        v2 = Vector3D(0, 1, 0) # j
        v3 = Vector3D(0, 0, 1) # k

        # Cross product (vector)
        cross_ij = v1.cross(v2) # i x j = k
        self.assertEqual(cross_ij, v3)

        cross_jk = v2.cross(v3) # j x k = i
        self.assertEqual(cross_jk, v1)

        cross_ki = v3.cross(v1) # k x i = j
        self.assertEqual(cross_ki, v2)

        # Anti-commutative: j x i = -k
        self.assertEqual(v2.cross(v1), -v3)

        # Parallel vectors: v x v = 0
        self.assertTrue(v1.cross(v1).is_zero_vector())
        
        v_general1 = Vector3D(1,2,3)
        v_general2 = Vector3D(4,5,6)
        # Expected: (2*6 - 3*5, 3*4 - 1*6, 1*5 - 2*4)
        #         = (12 - 15, 12 - 6, 5 - 8)
        #         = (-3, 6, -3)
        self.assertEqual(v_general1.cross(v_general2), Vector3D(-3, 6, -3))


if __name__ == '__main__':
    unittest.main()