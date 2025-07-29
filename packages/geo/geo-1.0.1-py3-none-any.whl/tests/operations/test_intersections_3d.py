# (1) python tests/operations/test_intersections_3d.py
# (2) python -m unittest tests/operations/test_intersections_3d.py (verbose output) (auto add sys.path)

import sys
import os
import random
import math
import unittest
from typing import Tuple

import matplotlib.pyplot as plt  # heavy‑weight, but imported only when DEBUG_VIS is set
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 – side‑effect adds 3‑D projection

# Add project root to sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from geo.core import Point3D, Vector3D
from geo.operations.intersections_3d import (
    sphere_sphere_intersection,
    plane_plane_intersection,
    line_triangle_intersection_moller_trumbore,
    AABB,
    SphereSphereIntersectionResult,
)
from geo.primitives_3d import Sphere, Plane, Line3D
from geo.core.precision import DEFAULT_EPSILON, is_equal, is_zero

# -----------------------------------------------------------------------------
# helpers & visual‑debug utilities
# -----------------------------------------------------------------------------

def _rand_point(rng: random.Random, bound: float = 10.0) -> Point3D:
    return Point3D(
        rng.uniform(-bound, bound), rng.uniform(-bound, bound), rng.uniform(-bound, bound)
    )


def _maybe_visualize(func):
    """Decorator: execute function only if the DEBUG_VIS env var is set."""

    def wrapper(*args, **kwargs):
        if os.getenv("DEBUG_VIS"):
            func(*args, **kwargs)

    return wrapper


@_maybe_visualize
def _vis_spheres(s1: Sphere, s2: Sphere, result: SphereSphereIntersectionResult, idx: int):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * math.pi, 30)
    v = np.linspace(0, math.pi, 15)

    def draw_sphere(sp, color, alpha=0.2):
        xs = sp.center.x + sp.radius * np.outer(np.cos(u), np.sin(v))
        ys = sp.center.y + sp.radius * np.outer(np.sin(u), np.sin(v))
        zs = sp.center.z + sp.radius * np.outer(np.ones_like(u), np.cos(v))
        ax.plot_surface(xs, ys, zs, color=color, alpha=alpha, linewidth=0)

    import numpy as np

    draw_sphere(s1, "b")
    draw_sphere(s2, "r")

    if result.type == "point":
        p = result.point
        ax.scatter([p.x], [p.y], [p.z], color="k", s=30)
    elif result.type == "circle":
        # coarse circle preview
        n = result.circle_normal
        center = result.circle_center
        r = result.circle_radius
        # construct orthonormal basis for circle plane
        if abs(n.x) < 0.9:
            v = Vector3D(1, 0, 0).cross(n).normalize()
        else:
            v = Vector3D(0, 1, 0).cross(n).normalize()
        w = n.cross(v).normalize()
        ts = np.linspace(0, 2 * math.pi, 50)
        xs, ys, zs = [], [], []
        for t in ts:
            pt = center + (math.cos(t) * r) * v + (math.sin(t) * r) * w
            xs.append(pt.x)
            ys.append(pt.y)
            zs.append(pt.z)
        ax.plot(xs, ys, zs, "k-")

    ax.set_title(f"Random sphere‑sphere #{idx}\nResult: {result.type}")
    plt.show()


# -----------------------------------------------------------------------------
# randomized / stress test cases
# -----------------------------------------------------------------------------

class TestIntersections3DRandomised(unittest.TestCase):
    RNG_SEED = 2025

    def setUp(self):
        self.rng = random.Random(self.RNG_SEED)

    # ------------------------------------------------------------------
    # Sphere – Sphere large batch
    # ------------------------------------------------------------------
    def test_sphere_sphere_random_batch(self):
        """1000 random pairs – algorithm must agree with analytic test."""
        N = 1000
        failures = []

        for i in range(N):
            c1 = _rand_point(self.rng)
            c2 = _rand_point(self.rng)
            r1 = self.rng.uniform(0.1, 5.0)
            r2 = self.rng.uniform(0.1, 5.0)
            s1, s2 = Sphere(c1, r1), Sphere(c2, r2)

            res = sphere_sphere_intersection(s1, s2)

            d = c1.distance_to(c2)

            # expected classification by distance radii relation
            if d > r1 + r2 + DEFAULT_EPSILON or d < abs(r1 - r2) - DEFAULT_EPSILON:
                expected = "none"
            elif is_zero(d) and is_equal(r1, r2):
                expected = "coincident"
            elif is_equal(d, r1 + r2) or is_equal(d, abs(r1 - r2)):
                expected = "point"
            else:
                expected = "circle"

            if res.type != expected:
                failures.append((i, expected, res.type, s1, s2))
            # optional sanity check on returned geometry
            if res.type == "point":
                self.assertTrue(s1.on_surface(res.point) and s2.on_surface(res.point))
            elif res.type == "circle":
                # distance from centers should equal x and r_intersect reasonable
                center = res.circle_center
                n = res.circle_normal
                self.assertFalse(n.is_zero_vector())
                self.assertTrue((center - c1).cross(n).magnitude() < 1e-5)  # center lies on plane through line of centers

            # visualise occasional examples
            if os.getenv("DEBUG_VIS") and i < 10:
                _vis_spheres(s1, s2, res, i)

        self.assertFalse(failures, f"{len(failures)} mismatches in {N} random tests")

    # ------------------------------------------------------------------
    # Plane – Plane random orientations
    # ------------------------------------------------------------------
    def test_plane_plane_random(self):
        for _ in range(300):
            p0 = _rand_point(self.rng)
            n1 = Vector3D(*[self.rng.uniform(-1, 1) for _ in range(3)]).normalize()
            n2 = Vector3D(*[self.rng.uniform(-1, 1) for _ in range(3)]).normalize()
            if n1.cross(n2).is_zero_vector():
                n2 = Vector3D(-n2.y, n2.x, n2.z)  # force non‑parallel
            plane1 = Plane(p0, n1)
            plane2 = Plane(_rand_point(self.rng), n2)

            line = plane_plane_intersection(plane1, plane2)
            self.assertIsNotNone(line)
            # verify that two points on the line satisfy both plane equations
            p_on = line.point_at(0.0)
            self.assertTrue(abs(plane1.signed_distance_to_point(p_on)) < 1e-6)
            self.assertTrue(abs(plane2.signed_distance_to_point(p_on)) < 1e-6)

    # ------------------------------------------------------------------
    # Möller–Trumbore stress test: many rays v random triangles
    # ------------------------------------------------------------------
    def test_ray_triangle_massive(self):
        hits = 0
        for _ in range(2000):
            # random triangle around origin
            tri = [_rand_point(self.rng, 5.0) for _ in range(3)]
            origin = _rand_point(self.rng, 10.0)
            dir_vec = Vector3D(*[self.rng.uniform(-1, 1) for _ in range(3)])
            if dir_vec.is_zero_vector():
                dir_vec = Vector3D(1, 0, 0)
            res = line_triangle_intersection_moller_trumbore(
                origin, dir_vec, *tri
            )
            # brute barycentric check when result exists
            if res is not None:
                hits += 1
                p_hit, t = res
                # barycentric coordinates using same edges
                v0, v1, v2 = tri
                # area method:
                u = ((v1 - v0).cross(v2 - v0)).magnitude()
                u0 = ((v1 - p_hit).cross(v2 - p_hit)).magnitude()
                u1 = ((v2 - p_hit).cross(v0 - p_hit)).magnitude()
                u2 = ((v0 - p_hit).cross(v1 - p_hit)).magnitude()
                self.assertTrue(abs((u0 + u1 + u2) - u) < 1e-3)
        # we just ensure algorithm never crashes and produces plausible hits
        self.assertTrue(hits > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
