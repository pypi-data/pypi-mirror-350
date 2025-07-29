# (1) python tests/core/test_point.py
# (2) python -m unittest tests/core/test_point.py (verbose output) (auto add sys.path)

import unittest
import math
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point, Point2D, Point3D, Vector2D, Vector3D
from geo.core.precision import DEFAULT_EPSILON, is_equal

class TestPoint(unittest.TestCase):

    def test_point_generic_constructor_and_properties(self):
        p = Point(1, 2, 3, 4)
        self.assertEqual(p.coords, (1, 2, 3, 4))
        self.assertEqual(p.dimension, 4)
        self.assertEqual(p[0], 1)
        self.assertEqual(len(p), 4)
        with self.assertRaises(ValueError):
            Point() # No coordinates

    def test_point2d_constructor_and_properties(self):
        p = Point2D(1.5, 2.5)
        self.assertEqual(p.x, 1.5)
        self.assertEqual(p.y, 2.5)
        self.assertEqual(p.coords, (1.5, 2.5))
        self.assertEqual(p.dimension, 2)
        self.assertEqual(p[0], 1.5)
        self.assertEqual(p[1], 2.5)
        self.assertEqual(len(p), 2)

    def test_point3d_constructor_and_properties(self):
        p = Point3D(1.0, 2.0, 3.0)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
        self.assertEqual(p.z, 3.0)
        self.assertEqual(p.coords, (1.0, 2.0, 3.0))
        self.assertEqual(p.dimension, 3)
        self.assertEqual(p[0], 1.0)
        self.assertEqual(p[1], 2.0)
        self.assertEqual(p[2], 3.0)
        self.assertEqual(len(p), 3)

    def test_point_equality(self):
        p1_2d = Point2D(1.0, 2.0)
        p2_2d = Point2D(1.0, 2.0)
        p3_2d = Point2D(1.0000000001, 2.0000000001) # Close enough
        p4_2d = Point2D(1.1, 2.0)
        p_other_type = Vector2D(1.0, 2.0)

        self.assertEqual(p1_2d, p2_2d)
        self.assertTrue(p1_2d == p3_2d) # Uses is_equal
        self.assertNotEqual(p1_2d, p4_2d)
        self.assertFalse(p1_2d == p_other_type) # Type mismatch

        p1_3d = Point3D(1,2,3)
        p2_3d = Point3D(1,2,3)
        self.assertEqual(p1_3d, p2_3d)
        self.assertNotEqual(p1_2d, p1_3d) # Dimension mismatch

    def test_point_repr(self):
        p2d = Point2D(1, 2)
        self.assertEqual(repr(p2d), "Point2D(1.0, 2.0)") # Floats due to Point2D(Point[float])
        p3d = Point3D(1, 2, 3)
        self.assertEqual(repr(p3d), "Point3D(1.0, 2.0, 3.0)")

    def test_point_hash(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(1, 2)
        p3 = Point2D(2, 1)
        s = {p1, p2, p3}
        self.assertEqual(len(s), 2) # p1 and p2 should hash to same if equal
        self.assertIn(p1, s)
        self.assertIn(Point2D(1,2), s) # Test with new equal instance

    def test_distance_to(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0)

        p3 = Point3D(0, 0, 0)
        p4 = Point3D(1, 2, 2) # dist = sqrt(1+4+4) = sqrt(9) = 3
        self.assertAlmostEqual(p3.distance_to(p4), 3.0)

        with self.assertRaises(ValueError):
            p1.distance_to(p3) # Dimension mismatch

    def test_point_vector_addition_subtraction(self):
        p1 = Point2D(1, 1)
        v1 = Vector2D(2, 3)
        p_res_add = p1 + v1
        self.assertIsInstance(p_res_add, Point2D)
        self.assertEqual(p_res_add, Point2D(3, 4))

        p_res_sub_vec = p1 - v1
        self.assertIsInstance(p_res_sub_vec, Point2D)
        self.assertEqual(p_res_sub_vec, Point2D(-1, -2))

        p2 = Point2D(5, 5)
        v_res_sub_point = p2 - p1
        self.assertIsInstance(v_res_sub_point, Vector2D)
        self.assertEqual(v_res_sub_point, Vector2D(4, 4))
        
        p3d1 = Point3D(1,1,1)
        v3d1 = Vector3D(1,2,3)
        p3d_res_add = p3d1 + v3d1
        self.assertEqual(p3d_res_add, Point3D(2,3,4))

        p3d2 = Point3D(0,0,0)
        v3d_res_sub_point = p3d1 - p3d2
        self.assertEqual(v3d_res_sub_point, Vector3D(1,1,1))

        with self.assertRaises(TypeError):
            p1 + Vector3D(1,2,3) # Dimension mismatch for add
        with self.assertRaises(ValueError):
                Point2D(1,1) - Point3D(1,2,3) # Dimension mismatch for sub

    def test_point2d_polar_conversion(self):
        # Cartesian to Polar
        p1 = Point2D(1, 1) # r = sqrt(2), theta = pi/4
        r, theta = p1.to_polar()
        self.assertAlmostEqual(r, math.sqrt(2))
        self.assertAlmostEqual(theta, math.pi / 4)

        p2 = Point2D(-1, 0) # r = 1, theta = pi
        r, theta = p2.to_polar()
        self.assertAlmostEqual(r, 1)
        self.assertAlmostEqual(theta, math.pi)
        
        p_origin = Point2D(0,0)
        r, theta = p_origin.to_polar()
        self.assertAlmostEqual(r, 0)
        self.assertAlmostEqual(theta, 0) # atan2(0,0) is often 0

        # Polar to Cartesian
        p_from_polar1 = Point2D.from_polar(math.sqrt(2), math.pi / 4)
        self.assertEqual(p_from_polar1, Point2D(1,1))

        p_from_polar2 = Point2D.from_polar(2, math.pi) # x = -2, y = 0
        self.assertEqual(p_from_polar2, Point2D(-2,0))
        
        with self.assertRaises(ValueError):
            Point2D.from_polar(-1, 0) # Negative radius

    def test_point3d_spherical_conversion(self):
        # Cartesian to Spherical (r, theta_inclination, phi_azimuth)
        # theta_inclination from +z [0, pi], phi_azimuth from +x in xy-plane (-pi, pi]
        p1 = Point3D(1, 1, math.sqrt(2)) # r = sqrt(1+1+2) = 2.
                                            # z = r*cos(theta) => sqrt(2) = 2*cos(theta) => cos(theta)=sqrt(2)/2 => theta=pi/4
                                            # y/x = tan(phi) => 1/1 = tan(phi) => phi=pi/4
        r, theta, phi = p1.to_spherical()
        self.assertAlmostEqual(r, 2.0)
        self.assertAlmostEqual(theta, math.pi / 4)
        self.assertAlmostEqual(phi, math.pi / 4)

        p_z_axis = Point3D(0, 0, 5) # r=5, theta=0, phi=0 (atan2(0,0) is 0)
        r, theta, phi = p_z_axis.to_spherical()
        self.assertAlmostEqual(r, 5.0)
        self.assertAlmostEqual(theta, 0.0)
        self.assertAlmostEqual(phi, 0.0)

        p_neg_z_axis = Point3D(0,0,-3) # r=3, theta=pi, phi=0
        r, theta, phi = p_neg_z_axis.to_spherical()
        self.assertAlmostEqual(r, 3.0)
        self.assertAlmostEqual(theta, math.pi)
        self.assertAlmostEqual(phi, 0.0)
        
        p_origin = Point3D(0,0,0)
        r, theta, phi = p_origin.to_spherical()
        self.assertAlmostEqual(r,0)
        self.assertAlmostEqual(theta,0)
        self.assertAlmostEqual(phi,0)


        # Spherical to Cartesian
        p_from_spher1 = Point3D.from_spherical(2.0, math.pi / 4, math.pi / 4)
        self.assertEqual(p_from_spher1, Point3D(1, 1, math.sqrt(2)))

        p_from_spher_z = Point3D.from_spherical(5.0, 0.0, 0.0) # Any phi for theta=0 is on z-axis
        self.assertEqual(p_from_spher_z, Point3D(0,0,5))
        
        p_from_spher_z_phi = Point3D.from_spherical(5.0, 0.0, math.pi/2) # phi ignored if theta=0
        self.assertEqual(p_from_spher_z_phi, Point3D(0,0,5))


        with self.assertRaises(ValueError):
            Point3D.from_spherical(-1, 0, 0) # Negative radius
        with self.assertRaises(ValueError):
            Point3D.from_spherical(1, -math.pi/2, 0) # Theta out of range [0, pi]
        with self.assertRaises(ValueError):
            Point3D.from_spherical(1, math.pi * 1.5, 0) # Theta out of range

        # Test theta clamping for values very close to 0 or pi
        p_near_pi = Point3D.from_spherical(1.0, math.pi + DEFAULT_EPSILON/10, 0.0)
        self.assertAlmostEqual(p_near_pi.z, -1.0) # cos(pi) = -1
        p_near_zero = Point3D.from_spherical(1.0, -DEFAULT_EPSILON/10, 0.0)
        self.assertAlmostEqual(p_near_zero.z, 1.0) # cos(0) = 1