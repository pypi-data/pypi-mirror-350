# geo/operations/convex_hull.py

"""
Robust 2D / 3D convex-hull utilities with optional visualisation helpers.

Public API
==========
convex_hull_2d_monotone_chain(points)   →   List[Point2D]
convex_hull_3d(points)                   →   Polyhedron | raises NotImplementedError
plot_convex_hull_2d(points, hull=None, *, ax=None, show=True)
plot_convex_hull_3d(points, hull=None, *, ax=None, show=True)

Design notes
------------
* 2D  -  Andrew monotone chain O(n log n) with extra guards:
  • Deduplication of identical points.
  • Removal of on-edge collinear points inside edges (toggle via keep_collinear).
  • Graceful handling for < 3 unique points (returns copy of unique set).

* 3D  -  Delegates to scipy.spatial.ConvexHull when available.
  The returned hull is converted to geo.primitives_3d.Polyhedron.
  If SciPy is missing an informative NotImplementedError is raised.

* Visualisation  -  Lightweight wrappers around matplotlib
  (auto-installed in most scientific stacks).  They are optional and only
  imported on demand - the core hull code has zero plotting deps.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple, Optional

from geo.core import Point2D, Point3D
from geo.core.precision import DEFAULT_EPSILON, is_zero
from geo.primitives_2d import Polygon
from geo.primitives_3d import Polyhedron

__all__ = [
    "convex_hull_2d_monotone_chain",
    "convex_hull_3d",
    "plot_convex_hull_2d",
    "plot_convex_hull_3d",
]


# Helpers

def _cross(o: Point2D, a: Point2D, b: Point2D) -> float:
    """2D signed area of the triangle o-a-b (twice the actual area)."""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def _dedup(points: Sequence[Point2D]) -> List[Point2D]:
    """Return points without duplicates (lexicographic order)."""
    seen: set[Tuple[float, float]] = set()
    out: List[Point2D] = []
    for p in sorted(points, key=lambda q: (q.x, q.y)):
        key = (p.x, p.y)
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


# 2‑D convex hull (Monotone Chain)


def convex_hull_2d_monotone_chain(
    points: Sequence[Point2D], *, keep_collinear: bool = False
) -> List[Point2D]:
    """Andrew monotone-chain convex hull.

    Parameters
    ----------
    points
        The input point cloud (any iterable).
    keep_collinear
        False (default) removes collinear points on edges of the hull,
        returning the minimal vertex set. True keeps them.
    """
    uniq = _dedup(points)
    if len(uniq) <= 2:
        return uniq.copy()

    lower: List[Point2D] = []
    for p in uniq:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= (
            DEFAULT_EPSILON if keep_collinear else 0.0
        ):
            lower.pop()
        lower.append(p)

    upper: List[Point2D] = []
    for p in reversed(uniq):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= (
            DEFAULT_EPSILON if keep_collinear else 0.0
        ):
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    return hull


# 3‑D convex hull (SciPy backend)

try:
    from scipy.spatial import ConvexHull as _SciHull
    import numpy as _np

    _HAS_SCIPY = True
except ModuleNotFoundError:  # pragma: no cover – SciPy optional
    _HAS_SCIPY = False


def _require_scipy() -> None:
    if not _HAS_SCIPY:
        raise NotImplementedError(
            "convex_hull_3d requires SciPy ≥1.3.  Install via `pip install scipy`."
        )


def convex_hull_3d(points: Sequence[Point3D]) -> Polyhedron:
    """Compute the 3‑D convex hull using *SciPy*.

    Returns a :class:`~geo.primitives_3d.Polyhedron` whose vertices are the
    unique points of points and faces given by the SciPy simplices
    (oriented CCW seen from outside).
    """
    _require_scipy()

    if len(points) < 4:
        raise ValueError("Need ≥4 non-coplanar points for a 3-D hull.")

    pts = _np.array([[p.x, p.y, p.z] for p in points])
    hull = _SciHull(pts)

    vertices = [Point3D(*pts[i]) for i in hull.vertices]  # unique vertices (order arbitrary)
    faces = [tuple(int(v) for v in simplex) for simplex in hull.simplices]
    return Polyhedron(vertices, faces)


# Optional visualisation (matplotlib)

def _mpl_axes_2d(ax=None):
    import matplotlib.pyplot as plt  # lazy import

    if ax is None:
        fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")
    return ax


def plot_convex_hull_2d(
    points: Sequence[Point2D],
    hull: Optional[Sequence[Point2D]] = None,
    *,
    ax=None,
    show: bool = True,
    point_kwargs=None,
    hull_kwargs=None,
):
    """Quick matplotlib visualisation of a 2D hull."""
    import matplotlib.pyplot as plt  # lazy import

    point_kwargs = {"s": 20, "color": "tab:blue", "zorder": 2} | (point_kwargs or {})
    hull_kwargs = {"linewidth": 1.5, "color": "tab:red", "zorder": 3} | (hull_kwargs or {})

    ax = _mpl_axes_2d(ax)
    xs, ys = zip(*[(p.x, p.y) for p in points])
    ax.scatter(xs, ys, **point_kwargs)

    if hull is None:
        hull = convex_hull_2d_monotone_chain(points)
    if hull:
        hx, hy = zip(*[(p.x, p.y) for p in hull + [hull[0]]])
        ax.plot(hx, hy, **hull_kwargs)
    if show:
        plt.show()
    return ax


def plot_convex_hull_3d(
    points: Sequence[Point3D],
    hull: Optional[Polyhedron] = None,
    *,
    ax=None,
    show: bool = True,
):
    """Matplotlib 3D plot of point cloud and its convex hull triangles."""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 – side-effect import
    import matplotlib.pyplot as plt  # lazy import
    import matplotlib as mpl

    if hull is None:
        try:
            hull = convex_hull_3d(points)
        except NotImplementedError:
            raise  # propagate if SciPy missing

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    # plot points
    xs, ys, zs = zip(*[(p.x, p.y, p.z) for p in points])
    ax.scatter(xs, ys, zs, color="tab:blue", s=10)

    # plot hull faces
    verts = [(v.x, v.y, v.z) for v in hull.vertices]
    poly3d = [[verts[idx] for idx in face] for face in hull.faces]
    coll = mpl.art3d.Poly3DCollection(poly3d, alpha=0.2, facecolor="tab:red")
    ax.add_collection3d(coll)

    ax.set_box_aspect([1, 1, 1])
    if show:
        plt.show()
    return ax
