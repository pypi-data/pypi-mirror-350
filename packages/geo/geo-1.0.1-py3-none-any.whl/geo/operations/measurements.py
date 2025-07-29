# geo/operations/measurements.py
"""
High-level geometric measurement helpers that complement the methods
already available on the primitive classes.
"""
from __future__ import annotations

import math
from typing import Optional, Sequence, Tuple, Union

from geo.core import Point2D, Point3D, Vector2D, Vector3D
from geo.core.precision import DEFAULT_EPSILON, is_equal, is_zero
from geo.primitives_2d import Line2D, Segment2D
from geo.primitives_3d import Line3D, Plane as Plane3D, Segment3D
from geo.operations.intersections_2d import segment_segment_intersection_detail

__all__: Sequence[str] = (
    "closest_point_on_segment_to_point",
    "distance_segment_segment_2d",
    "closest_points_segments_2d",
    "signed_angle_between_vectors_2d",
    "distance_point_line_3d",
    "distance_point_plane",
    "distance_line_line_3d",
)


# Generic helpers

def _closest_point_parameter(p: Union[Point2D, Point3D],
                             a: Union[Point2D, Point3D],
                             b: Union[Point2D, Point3D]) -> float:
    """Parameter t in a + t·(b-a) of the orthogonal projection of p.
    Returns t without clamping to [0, 1].
    """
    ab = b - a  # type: ignore[operator]
    if ab.is_zero_vector(DEFAULT_EPSILON):  # degenerate segment
        return 0.0
    return (p - a).dot(ab) / ab.magnitude_squared()  # type: ignore[operator]



# 2‑D & 3‑D helpers

def closest_point_on_segment_to_point(
    segment: Union[Segment2D, Segment3D],
    point: Union[Point2D, Point3D],
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> Union[Point2D, Point3D]:
    """Return the point on *segment* closest to *point* (inclusive ends)."""
    t = _closest_point_parameter(point, segment.p1, segment.p2)
    if t <= 0.0:
        return segment.p1
    if t >= 1.0:
        return segment.p2
    return segment.p1 + (segment.p2 - segment.p1) * t  # type: ignore[operator]


def distance_segment_segment_2d(
    seg1: Segment2D,
    seg2: Segment2D,
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> float:
    """Shortest distance between two *closed* 2D segments (0 if they touch)."""
    itype, _ = segment_segment_intersection_detail(seg1, seg2, epsilon)
    if itype in {"point", "overlap"}:
        return 0.0
    # endpoints to opposite segment distances
    dists = (
        seg2.distance_to_point(seg1.p1),
        seg2.distance_to_point(seg1.p2),
        seg1.distance_to_point(seg2.p1),
        seg1.distance_to_point(seg2.p2),
    )
    return min(dists)


def closest_points_segments_2d(
    seg1: Segment2D,
    seg2: Segment2D,
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> Tuple[Point2D, Point2D]:
    """Pair of closest points (p_on_seg1, p_on_seg2) for two 2D segments."""
    itype, data = segment_segment_intersection_detail(seg1, seg2, epsilon)
    if itype == "point":
        assert isinstance(data, Point2D)
        return data, data
    if itype == "overlap":
        assert isinstance(data, tuple) and len(data) == 2
        return data[0], data[0]  # any point on the overlap is equally valid

    # otherwise compute candidates (projection of each end onto the other seg)
    cands: list[Tuple[float, Point2D, Point2D]] = []
    for p in (seg1.p1, seg1.p2):
        q = closest_point_on_segment_to_point(seg2, p, epsilon=epsilon)  # type: ignore[arg-type]
        cands.append((p.distance_to(q), p, q))
    for p in (seg2.p1, seg2.p2):
        q = closest_point_on_segment_to_point(seg1, p, epsilon=epsilon)  # type: ignore[arg-type]
        cands.append((p.distance_to(q), q, p))
    # return the minimum‑distance pair
    cands.sort(key=lambda t: t[0])
    return cands[0][1], cands[0][2]


def signed_angle_between_vectors_2d(v1: Vector2D, v2: Vector2D) -> float:
    """Signed angle v1 → v2 in radians (CCW positive, range (-π, π])."""
    if v1.is_zero_vector(DEFAULT_EPSILON) or v2.is_zero_vector(DEFAULT_EPSILON):
        return 0.0
    dot = v1.dot(v2)
    cross = v1.x * v2.y - v1.y * v2.x
    return math.atan2(cross, dot)


# Thin wrappers around primitive methods (3‑D)

def distance_point_line_3d(point: Point3D, line: Line3D) -> float:
    """Alias for line.distance_to_point(point) kept for API symmetry."""
    return line.distance_to_point(point)


def distance_point_plane(point: Point3D, plane: Plane3D) -> float:
    """Alias for plane.distance_to_point(point) kept for API symmetry."""
    return plane.distance_to_point(point)


# 3‑D line‑line minimal distance

def distance_line_line_3d(
    line1: Line3D,
    line2: Line3D,
    *,
    epsilon: float = DEFAULT_EPSILON,
) -> Tuple[float, Optional[Point3D], Optional[Point3D]]:
    """Shortest distance between two 3D infinite lines plus closest points.

    * Parallel lines - returns the perpendicular distance, points None.
    * Intersecting lines - distance 0, identical closest points.
    * Skew lines - distance > 0 and the unique closest points on each line.
    """
    d1, d2 = line1.direction, line2.direction
    p1, p2 = line1.origin, line2.origin

    n = d1.cross(d2)
    if n.is_zero_vector(epsilon):  # ‖d1×d2‖ ≈ 0 → parallel
        return line2.distance_to_point(p1), None, None

    w0 = p1 - p2
    denom = n.magnitude()
    distance = abs(w0.dot(n)) / denom

    # solve for the parameters of the closest points (see geometric derivation)
    b = d1.dot(d2)
    d = d1.dot(w0)
    e = d2.dot(w0)
    denom_param = 1.0 - b * b

    # numerical safety – denom_param should not be zero here (lines not parallel)
    if is_zero(denom_param, epsilon):
        return distance, None, None

    s = (b * e - d) / denom_param
    t = (e - b * d) / denom_param

    cp1 = p1 + d1 * s  # type: ignore[operator]
    cp2 = p2 + d2 * t  # type: ignore[operator]

    return distance, cp1, cp2
