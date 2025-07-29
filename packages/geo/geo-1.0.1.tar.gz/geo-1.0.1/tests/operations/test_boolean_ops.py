# (1) python tests/operations/test_boolean_ops.py
# (2) python -m unittest tests/operations/test_boolean_ops.py (verbose output) (auto add sys.path)

"""
1. Convex clipping (`clip_polygon_sutherland_hodgman`)
2. 2-D Shapely boolean ops (`union`, `intersection`, `difference`)
3. 3-D Trimesh boolean ops (same trio)

All optional back-ends are auto-detected and their suites are skipped if the
library isn't available, so the file can run in any environment.
"""

from __future__ import annotations

import math
import os
import sys
import unittest
from typing import List, Optional

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from geo.core.precision import DEFAULT_EPSILON as EPS, is_equal  # noqa: E402
from geo.core import Point2D, Point3D  # noqa: E402
from geo.primitives_2d import Polygon  # noqa: E402
from geo.primitives_3d import Polyhedron  # noqa: E402
from geo.operations import boolean_ops as bop  # noqa: E402


# Helper utilities

def _poly_equal(p1: Polygon, p2: Polygon, tol: float = EPS) -> bool:  # noqa: D401
    """Return *True* if two polygons are vertex-wise equal up to rotation."""
    if p1.num_vertices != p2.num_vertices:
        return False
    n = p1.num_vertices
    for shift in range(n):
        if all(
            is_equal(p1.vertices[i].x, p2.vertices[(i + shift) % n].x, tol)
            and is_equal(p1.vertices[i].y, p2.vertices[(i + shift) % n].y, tol)
            for i in range(n)
        ):
            return True
    return False


def _area(polys: List[Polygon]) -> float:
    return sum(p.area for p in polys)


def _volume(polys: List[Polyhedron]) -> float:
    return sum(p.volume() for p in polys)


# 0. SUTHERLAND–HODGMAN CLIPPING (always available)

class TestSutherlandHodgman(unittest.TestCase):
    """Edge-cases for convex clipping."""

    def setUp(self) -> None:
        # Subject square (0,0)→(4,4)
        self.sub_sq = Polygon([
            Point2D(0, 0), Point2D(4, 0), Point2D(4, 4), Point2D(0, 4)
        ])
        # Convex triangle for partial clip
        self.clip_tri = Polygon([
            Point2D(1, 1), Point2D(3, 1), Point2D(2, 3)
        ])
        if self.clip_tri.signed_area() < 0:
            self.clip_tri = Polygon(list(reversed(self.clip_tri.vertices)))

    def test_subject_inside_clip_bigger(self):
        big_clip = Polygon([
            Point2D(-1, -1), Point2D(5, -1), Point2D(5, 5), Point2D(-1, 5)
        ])
        res = bop.clip_polygon_sutherland_hodgman(self.sub_sq, big_clip)
        self.assertIsNotNone(res)
        self.assertTrue(_poly_equal(res, self.sub_sq))

    def test_subject_outside(self):
        clip = Polygon([
            Point2D(5, 5), Point2D(6, 5), Point2D(6, 6), Point2D(5, 6)
        ])
        res = bop.clip_polygon_sutherland_hodgman(self.sub_sq, clip)
        self.assertIsNone(res)

    def test_partial_overlap(self):
        res = bop.clip_polygon_sutherland_hodgman(self.sub_sq, self.clip_tri)
        self.assertIsNotNone(res)
        if res:
            self.assertAlmostEqual(res.area, self.clip_tri.area, places=6)

    def test_vertex_on_edge(self):
        # Clip so that a subject vertex lies on clip edge
        clip = Polygon([Point2D(0, 0), Point2D(4, 0), Point2D(2, 3)])
        if clip.signed_area() < 0:
            clip = Polygon(list(reversed(clip.vertices)))
        res = bop.clip_polygon_sutherland_hodgman(self.sub_sq, clip)
        self.assertIsNotNone(res)
        if res:
            # area should be equal to clip triangle (base 4, height 3) => 6
            self.assertAlmostEqual(res.area, 6.0, places=6)

    def test_clockwise_subject(self):
        cw_subject = Polygon(list(reversed(self.sub_sq.vertices)))
        res = bop.clip_polygon_sutherland_hodgman(cw_subject, self.clip_tri)
        self.assertIsNotNone(res)
        if res:
            self.assertAlmostEqual(res.area, self.clip_tri.area, places=6)


# 1. 2-D BOOLEAN OPS (optional Shapely)

_HAS_SHAPELY = getattr(bop, "_HAS_SHAPELY", False)

@unittest.skipUnless(_HAS_SHAPELY, "Shapely not installed – skipping 2-D boolean tests")
class TestPolygonBooleanOps(unittest.TestCase):
    """Various configurations for 2-D boolean ops."""

    def setUp(self) -> None:
        self.sq1 = Polygon([
            Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2)
        ])
        self.sq2 = Polygon([
            Point2D(1, 1), Point2D(3, 1), Point2D(3, 3), Point2D(1, 3)
        ])
        self.touching = Polygon([
            Point2D(2, 0), Point2D(4, 0), Point2D(4, 2), Point2D(2, 2)
        ])

    # Overlap 1×1
    def test_union_area_overlap(self):
        res = bop.polygon_union(self.sq1, self.sq2)
        self.assertAlmostEqual(_area(res), 7.0, places=6)

    def test_intersection_area_overlap(self):
        res = bop.polygon_intersection(self.sq1, self.sq2)
        self.assertAlmostEqual(_area(res), 1.0, places=6)

    def test_difference_area_overlap(self):
        res = bop.polygon_difference(self.sq1, self.sq2)
        self.assertAlmostEqual(_area(res), 3.0, places=6)

    # Touching squares (edge-adjacent)
    def test_touching_union(self):
        res = bop.polygon_union(self.sq1, self.touching)
        self.assertAlmostEqual(_area(res), 8.0, places=6)

    def test_touching_intersection(self):
        res = bop.polygon_intersection(self.sq1, self.touching)
        self.assertAlmostEqual(_area(res), 0.0, places=6)

    def test_touching_difference(self):
        res = bop.polygon_difference(self.sq1, self.touching)
        self.assertAlmostEqual(_area(res), 4.0, places=6)  # sq1 unchanged

    # Disjoint (no overlap / touch)
    def test_disjoint_union_area(self):
        dis = Polygon([
            Point2D(5, 5), Point2D(6, 5), Point2D(6, 6), Point2D(5, 6)
        ])
        res = bop.polygon_union(self.sq1, dis)
        self.assertAlmostEqual(_area(res), 4.0 + 1.0, places=6)

# 2. 3-D BOOLEAN OPS (optional Trimesh)
_HAS_TRIMESH = getattr(bop, "_HAS_TRIMESH", False)

@unittest.skipUnless(_HAS_TRIMESH, "Trimesh not installed – skipping 3-D boolean tests")
class TestPolyhedronBooleanOps(unittest.TestCase):
    """Overlapping cubes (unit cubes, second shifted +0.5)."""

    def setUp(self) -> None:
        import trimesh  # local, under skip guard
        c1 = trimesh.creation.box(extents=(1, 1, 1))
        c2 = trimesh.creation.box(extents=(1, 1, 1), transform=trimesh.transformations.translation_matrix((0.5, 0.5, 0.5)))
        self.cube1 = Polyhedron([Point3D(*v) for v in c1.vertices], [tuple(f) for f in c1.faces])
        self.cube2 = Polyhedron([Point3D(*v) for v in c2.vertices], [tuple(f) for f in c2.faces])

    def test_intersection_volume(self):
        res = bop.polyhedron_intersection(self.cube1, self.cube2)
        self.assertTrue(res)
        self.assertAlmostEqual(_volume(res), 0.125, places=6)

    def test_difference_volume(self):
        res = bop.polyhedron_difference(self.cube1, self.cube2)
        self.assertTrue(res)
        self.assertAlmostEqual(_volume(res), 0.875, places=6)

    def test_union_volume(self):
        res = bop.polyhedron_union(self.cube1, self.cube2)
        self.assertTrue(res)
        self.assertAlmostEqual(_volume(res), 1.875, places=6)


if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)
