# geo/operations/intersections_3d.py

"""
Functions for 3D intersection detection.
Includes complex or specific intersection algorithms beyond primitive methods.

Intersections covered:
- Sphere-Sphere (point, circle, none)
- Plane-Plane (line or none)
- Line-Triangle (Möller-Trumbore)
- AABB-Point, AABB-AABB, AABB-Sphere

Assumes right-handed coordinate system and standard geometric conventions.
"""

import math
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, Union

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from geo.primitives_3d import Sphere, Plane as Plane3D, Line3D

# Configure logger for optional debugging
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class SphereSphereIntersectionResult:
    """Result for sphere-sphere intersection."""
    type: str  # 'none', 'point', 'circle', 'coincident'
    point: Optional[Point3D] = None
    circle_center: Optional[Point3D] = None
    circle_radius: Optional[float] = None
    circle_normal: Optional[Vector3D] = None

def sphere_sphere_intersection(
    s1: Sphere, s2: Sphere, epsilon: float = DEFAULT_EPSILON
) -> SphereSphereIntersectionResult:
    """
    Calculate intersection between two spheres.

    Returns:
        SphereSphereIntersectionResult:
          - type 'none' if no intersection.
          - type 'point' with point attribute if tangent.
          - type 'circle' with center, radius, and normal if intersect in circle.
          - type 'coincident' if spheres are coincident.
    """
    d = s1.center.distance_to(s2.center)
    r1, r2 = s1.radius, s2.radius

    # No intersection cases
    if d > r1 + r2 + epsilon:
        return SphereSphereIntersectionResult(type='none')
    if d < abs(r1 - r2) - epsilon:
        return SphereSphereIntersectionResult(type='none')
    if is_zero(d, epsilon) and not is_equal(r1, r2, epsilon):
        return SphereSphereIntersectionResult(type='none')

    # Coincident spheres (infinite intersection)
    if is_zero(d, epsilon) and is_equal(r1, r2, epsilon):
        if is_zero(r1):
            # Both spheres degenerate to same point
            return SphereSphereIntersectionResult(type='point', point=s1.center)
        return SphereSphereIntersectionResult(type='coincident')

    # Tangent spheres (one intersection point)
    if is_equal(d, r1 + r2, epsilon) or is_equal(d, abs(r1 - r2), epsilon):
        if is_zero(d, epsilon):  # Degenerate to single point
            return SphereSphereIntersectionResult(type='point', point=s1.center)
        vec_c1_to_c2 = (s2.center - s1.center).normalize()
        tangent_point = s1.center + vec_c1_to_c2 * r1

        if s2.on_surface(tangent_point, epsilon * 2):
            return SphereSphereIntersectionResult(type='point', point=tangent_point)
        else:
            # Alternate tangent point (rare)
            if not is_zero(d):
                tangent_point_alt = s1.center + (s2.center - s1.center) * (r1 / d)
                if s2.on_surface(tangent_point_alt, epsilon * 2):
                    return SphereSphereIntersectionResult(type='point', point=tangent_point_alt)
            return SphereSphereIntersectionResult(type='none')

    # Intersection is a circle
    if is_zero(d, epsilon):
        return SphereSphereIntersectionResult(type='none')  # Should be handled above

    x = (d**2 - r2**2 + r1**2) / (2 * d)
    r_intersect_sq = r1**2 - x**2

    if r_intersect_sq < -epsilon:
        return SphereSphereIntersectionResult(type='none')
    if r_intersect_sq < 0:
        r_intersect_sq = 0

    circle_radius = math.sqrt(r_intersect_sq)
    vec_c1_to_c2_norm = (s2.center - s1.center).normalize()
    circle_center = s1.center + vec_c1_to_c2_norm * x

    return SphereSphereIntersectionResult(
        type='circle',
        circle_center=circle_center,
        circle_radius=circle_radius,
        circle_normal=vec_c1_to_c2_norm,
    )


def plane_plane_intersection(
    plane1: Plane3D, plane2: Plane3D, epsilon: float = DEFAULT_EPSILON, debug: bool = False
) -> Optional[Line3D]:
    """
    Compute the intersection line of two planes.

    Returns:
        Line3D if planes intersect in a line.
        None if planes are parallel or coincident (no unique line).

    If debug=True, logs warnings if numerical inconsistencies occur.
    """
    n1 = plane1.normal
    n2 = plane2.normal

    line_direction = n1.cross(n2)

    if line_direction.is_zero_vector(epsilon):
        # Parallel or coincident planes
        if plane2.contains_point(plane1.point_on_plane, epsilon):
            return None  # Coincident
        else:
            return None  # Parallel and distinct

    d1 = plane1.d_coeff
    d2 = plane2.d_coeff
    line_dir_mag_sq = line_direction.magnitude_squared()

    term1 = n2 * d1
    term2 = n1 * d2
    numerator_vec_part = term1 - term2

    point_on_line_vec = numerator_vec_part.cross(line_direction) / line_dir_mag_sq
    point_on_line = Point3D(point_on_line_vec.x, point_on_line_vec.y, point_on_line_vec.z)

    if debug:
        if not plane1.contains_point(point_on_line, epsilon * 10) or not plane2.contains_point(point_on_line, epsilon * 10):
            logger.warning(f"Calculated point {point_on_line} not on both planes within tolerance.")

    return Line3D(point_on_line, line_direction.normalize())


def line_triangle_intersection_moller_trumbore(
    ray_origin: Point3D,
    ray_direction: Vector3D,
    tri_v0: Point3D,
    tri_v1: Point3D,
    tri_v2: Point3D,
    epsilon: float = DEFAULT_EPSILON,
    cull_back_faces: bool = False,
) -> Optional[Tuple[Point3D, float]]:
    """
    Möller-Trumbore ray-triangle intersection.

    Args:
        ray_origin: Ray or line origin.
        ray_direction: Direction vector (not necessarily normalized).
        tri_v0, tri_v1, tri_v2: Triangle vertices.
        epsilon: Numerical tolerance.
        cull_back_faces: Ignore intersections with back faces if True.

    Returns:
        Tuple of (intersection_point, t_parameter) if intersection occurs.
        None otherwise.
    """
    edge1 = tri_v1 - tri_v0
    edge2 = tri_v2 - tri_v0

    h_vec = ray_direction.cross(edge2)
    determinant = edge1.dot(h_vec)

    if -epsilon < determinant < epsilon:
        return None  # Parallel or no intersection

    if cull_back_faces and determinant < 0:
        return None

    inv_det = 1.0 / determinant
    s_vec = ray_origin - tri_v0
    u = inv_det * s_vec.dot(h_vec)

    if u < -epsilon or u > 1.0 + epsilon:
        return None

    q_vec = s_vec.cross(edge1)
    v = inv_det * ray_direction.dot(q_vec)

    if v < -epsilon or (u + v) > 1.0 + epsilon:
        return None

    t = inv_det * edge2.dot(q_vec)

    intersection_point = ray_origin + ray_direction * t
    return intersection_point, t


@dataclass(frozen=True)
class AABB:
    """Axis-Aligned Bounding Box."""
    min_pt: Point3D
    max_pt: Point3D

    def contains_point(self, point: Point3D) -> bool:
        """Check if point is inside or on boundary of AABB."""
        return (
            self.min_pt.x <= point.x <= self.max_pt.x and
            self.min_pt.y <= point.y <= self.max_pt.y and
            self.min_pt.z <= point.z <= self.max_pt.z
        )

    def intersects_aabb(self, other: "AABB") -> bool:
        """Check if this AABB intersects with another AABB."""
        return (
            self.min_pt.x <= other.max_pt.x and self.max_pt.x >= other.min_pt.x and
            self.min_pt.y <= other.max_pt.y and self.max_pt.y >= other.min_pt.y and
            self.min_pt.z <= other.max_pt.z and self.max_pt.z >= other.min_pt.z
        )

    def intersects_sphere(
        self, sphere_center: Point3D, sphere_radius: float, epsilon: float = DEFAULT_EPSILON
    ) -> bool:
        """
        Check if AABB intersects a sphere.
        Finds closest point on AABB to sphere center, then checks distance.
        """
        closest_x = max(self.min_pt.x, min(sphere_center.x, self.max_pt.x))
        closest_y = max(self.min_pt.y, min(sphere_center.y, self.max_pt.y))
        closest_z = max(self.min_pt.z, min(sphere_center.z, self.max_pt.z))

        closest_point = Point3D(closest_x, closest_y, closest_z)

        # Use squared distance to avoid sqrt
        diff = sphere_center - closest_point
        distance_sq = diff.magnitude_squared()

        return distance_sq <= sphere_radius**2 + epsilon