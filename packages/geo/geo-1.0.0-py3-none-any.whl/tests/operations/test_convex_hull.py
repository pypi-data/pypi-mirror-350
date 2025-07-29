# (1) python tests/operations/test_convex_hull.py
# (2) python -m unittest tests/operations/test_convex_hull.py (verbose output) (auto add sys.path)

import unittest
import os
import sys
import math
import random
import matplotlib.pyplot as plt

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core import Point2D, Point3D
from geo.operations.convex_hull import convex_hull_2d_monotone_chain, convex_hull_3d

try:
    import scipy.spatial  # ensure scipy is available for 3D tests
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

class TestConvexHull2D(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(convex_hull_2d_monotone_chain([]), [])

    def test_single_point(self):
        p = Point2D(0, 0)
        self.assertEqual(convex_hull_2d_monotone_chain([p]), [p])

    def test_two_points(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(1, 1)
        result = convex_hull_2d_monotone_chain([p1, p2])
        self.assertEqual(result, [p1, p2])

    def test_triangle(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(1, 0)
        p3 = Point2D(0, 1)
        hull = convex_hull_2d_monotone_chain([p1, p2, p3])
        self.assertEqual(set(hull), {p1, p2, p3})

    def test_collinear_points(self):
        points = [Point2D(x, 0) for x in range(5)]
        hull = convex_hull_2d_monotone_chain(points)
        self.assertEqual(hull, [Point2D(0, 0), Point2D(4, 0)])

    def test_square(self):
        square = [Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,1)]
        hull = convex_hull_2d_monotone_chain(square)
        self.assertEqual(set(hull), set(square))

    def test_duplicate_points(self):
        square = [Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,1)]
        duplicate = square + [Point2D(1,0), Point2D(0,0)]
        hull = convex_hull_2d_monotone_chain(duplicate)
        self.assertEqual(set(hull), set(square))


@unittest.skipUnless(SCIPY_AVAILABLE, "Requires SciPy")
class TestConvexHull3D(unittest.TestCase):

    def test_cube(self):
        cube = [
            Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0), Point3D(0,1,0),
            Point3D(0,0,1), Point3D(1,0,1), Point3D(1,1,1), Point3D(0,1,1)
        ]
        hull = convex_hull_3d(cube)
        self.assertEqual(len(hull.vertices), 8)
        self.assertGreaterEqual(hull.num_faces, 6)

    def test_tetrahedron(self):
        tetra = [
            Point3D(0,0,0), Point3D(1,0,0), Point3D(0,1,0), Point3D(0,0,1)
        ]
        hull = convex_hull_3d(tetra)
        self.assertEqual(len(hull.vertices), 4)
        self.assertGreaterEqual(hull.num_faces, 4)


class TestConvexHullExtended(unittest.TestCase):

    def generate_circle_points(self, num_points=100, radius=1.0, noise=0.0):
        return [
            Point2D(
                radius * math.cos(theta) + random.uniform(-noise, noise),
                radius * math.sin(theta) + random.uniform(-noise, noise)
            ) for theta in [2 * math.pi * i / num_points for i in range(num_points)]
        ]

    def test_convex_hull_random_circle_points(self):
        points = self.generate_circle_points(num_points=100, radius=5.0, noise=0.1)
        hull = convex_hull_2d_monotone_chain(points)
        self.assertTrue(len(hull) > 0)

        # Visualize
        plt.figure()
        x = [p.x for p in points]
        y = [p.y for p in points]
        hx = [p.x for p in hull] + [hull[0].x]
        hy = [p.y for p in hull] + [hull[0].y]
        plt.plot(x, y, 'o', label='Points')
        plt.plot(hx, hy, 'r-', label='Convex Hull')
        plt.legend()
        plt.title("Convex Hull of Noisy Circle")
        plt.show()

    def test_convex_hull_random_cloud(self):
        random.seed(42)
        points = [Point2D(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(200)]
        hull = convex_hull_2d_monotone_chain(points)
        self.assertTrue(len(hull) > 0)

        # Visualize
        plt.figure()
        x = [p.x for p in points]
        y = [p.y for p in points]
        hx = [p.x for p in hull] + [hull[0].x]
        hy = [p.y for p in hull] + [hull[0].y]
        plt.plot(x, y, 'o', label='Points')
        plt.plot(hx, hy, 'g-', label='Convex Hull')
        plt.legend()
        plt.title("Convex Hull of Random Cloud")
        plt.show()

    def test_convex_hull_3d_random_cube(self):
        try:
            points = [
                Point3D(x, y, z)
                for x in (0, 1) for y in (0, 1) for z in (0, 1)
            ]
            hull = convex_hull_3d(points)
            self.assertTrue(hull is not None)
            self.assertTrue(hull.num_faces > 0)
        except ImportError:
            self.skipTest("SciPy not available for 3D convex hull")


if __name__ == '__main__':
    unittest.main()
