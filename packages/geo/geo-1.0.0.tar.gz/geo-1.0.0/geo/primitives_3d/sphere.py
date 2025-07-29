# geo/primitives_3d/sphere.py

"""
Defines a Sphere primitive in 3D space.
"""
import math
from typing import List, Optional, Tuple, Union

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from .line_3d import Line3D  # For intersection
from .plane import Plane  # For intersection


class Circle3D:
    """
    Represents a circle in 3D space, defined by a center point, radius, and plane normal.
    """
    def __init__(self, center: Point3D, radius: float, normal: Vector3D):
        if radius < 0:
            raise ValueError("Circle radius cannot be negative.")
        self.center = center
        self.radius = radius
        self.normal = normal.normalize()

    def __repr__(self) -> str:
        return f"Circle3D(center={self.center}, radius={self.radius}, normal={self.normal})"

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Check if a point lies on the circumference of the circle (within epsilon tolerance).
        """
        # Check if point lies on the plane of the circle within epsilon
        plane_to_point = (point - self.center).dot(self.normal)
        if not is_equal(plane_to_point, 0.0, epsilon):
            return False

        # Check distance to center vs radius
        dist = self.center.distance_to(point)
        return is_equal(dist, self.radius, epsilon)


class Sphere:
    """Represents a sphere in 3D space, defined by a center point and a radius."""

    def __init__(self, center: Point3D, radius: float):
        if radius < 0:
            raise ValueError("Sphere radius cannot be negative.")
        self.center = center
        self.radius = radius

    def __repr__(self) -> str:
        return f"Sphere(center={self.center}, radius={self.radius})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sphere):
            return False
        return self.center == other.center and is_equal(self.radius, other.radius)

    @property
    def surface_area(self) -> float:
        """Calculates the surface area of the sphere: 4 * pi * r^2."""
        return 4 * math.pi * self.radius**2

    @property
    def volume(self) -> float:
        """Calculates the volume of the sphere: (4/3) * pi * r^3."""
        return (4/3) * math.pi * self.radius**3

    def contains_point(self, point: Point3D, on_surface_epsilon: Optional[float] = None) -> bool:
        """
        Checks if a point is inside or on the boundary of the sphere.

        Args:
            point: The Point3D to check.
            on_surface_epsilon: If provided, checks if the point is on the surface
                                within this epsilon. Otherwise, checks if inside or on surface.
        Returns:
            True if condition met, False otherwise.
        """
        dist = self.center.distance_to(point)
        if on_surface_epsilon is not None:
            # Check if point is on surface within epsilon
            return is_equal(dist, self.radius, on_surface_epsilon)
        # Default: inside or on surface (allowing slight floating errors)
        return dist <= self.radius + DEFAULT_EPSILON

    def strictly_inside(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is strictly inside the sphere (excluding surface within epsilon).
        """
        dist = self.center.distance_to(point)
        return dist < self.radius - epsilon

    def strictly_outside(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is strictly outside the sphere (excluding surface within epsilon).
        """
        dist = self.center.distance_to(point)
        return dist > self.radius + epsilon

    def on_surface(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if a point lies exactly on the surface of the sphere within epsilon."""
        dist = self.center.distance_to(point)
        return is_equal(dist, self.radius, epsilon)

    def intersection_with_line(self, line: Line3D) -> List[Point3D]:
        """
        Calculates intersection points of the sphere with a Line3D.
        Algorithm: Solve (X-C).(X-C) = r^2 where X = L0 + t*L_dir.
        This leads to a quadratic equation in t: at^2 + bt + c = 0.
        """
        intersections: List[Point3D] = []

        oc = line.origin - self.center  # Vector from sphere center to line origin
        l_dir = line.direction  # Normalized direction vector of the line

        a = l_dir.dot(l_dir)  # Should be 1.0 as l_dir is normalized
        b = 2 * l_dir.dot(oc)
        c = oc.dot(oc) - self.radius**2

        discriminant = b**2 - 4*a*c

        if discriminant < -DEFAULT_EPSILON:  # No real roots
            return []
        elif is_zero(discriminant):  # One root (tangent)
            t = -b / (2*a)
            intersections.append(line.point_at(t))
        else:  # Two distinct roots
            sqrt_discriminant = math.sqrt(discriminant)
            t1 = (-b + sqrt_discriminant) / (2*a)
            t2 = (-b - sqrt_discriminant) / (2*a)
            intersections.append(line.point_at(t1))
            p2 = line.point_at(t2)
            if not intersections[0] == p2:
                intersections.append(p2)
        return intersections

    def intersection_with_plane(self, plane: Plane) -> Optional[Circle3D]:
        """
        Calculates the intersection of the sphere with a Plane.
        Returns a Circle3D if intersection is a circle,
        or a Circle3D with radius 0 if tangent,
        or None if no intersection.
        """
        signed_dist = plane.signed_distance_to_point(self.center)
        dist = abs(signed_dist)

        if dist > self.radius + DEFAULT_EPSILON:
            return None  # No intersection

        # Center of the intersection circle is projection of sphere center onto plane
        circle_center = plane.project_point(self.center)

        if is_equal(dist, self.radius):
            # Tangent: circle radius zero
            return Circle3D(circle_center, 0.0, plane.normal)

        radius_sq = self.radius**2 - signed_dist**2
        radius = math.sqrt(radius_sq) if radius_sq > 0 else 0.0

        return Circle3D(circle_center, radius, plane.normal)

    def intersection_with_sphere(self, other: "Sphere") -> Optional[Circle3D]:
        """
        Calculates the intersection of this sphere with another sphere.
        Returns a Circle3D representing the circle of intersection,
        or None if no intersection or spheres are tangent at a point.

        Reference: https://mathworld.wolfram.com/Sphere-SphereIntersection.html
        """
        d = self.center.distance_to(other.center)
        r1, r2 = self.radius, other.radius

        # No intersection if centers too far apart or one inside the other without touching
        if d > r1 + r2 + DEFAULT_EPSILON:
            return None  # Separate spheres
        if d < abs(r1 - r2) - DEFAULT_EPSILON:
            return None  # One sphere inside the other without intersection

        # Tangent spheres (one touching at a single point)
        if is_equal(d, r1 + r2) or is_equal(d, abs(r1 - r2)):
            # Intersection is a single point, radius zero circle
            # Calculate point on line between centers at proportion
            if d == 0:
                # Concentric spheres
                return None
            t = r1 / (r1 + r2) if d > 0 else 0.5
            center_point = Point3D(
                self.center.x + t * (other.center.x - self.center.x),
                self.center.y + t * (other.center.y - self.center.y),
                self.center.z + t * (other.center.z - self.center.z),
            )
            # Normal vector is the line between centers
            normal = (other.center - self.center).normalize() if d > 0 else Vector3D(1, 0, 0)
            return Circle3D(center_point, 0.0, normal)

        # Calculate circle radius and center for intersecting spheres
        # See sphere-sphere intersection formula:
        # h = (r1^2 - r2^2 + d^2) / (2d)
        h = (r1**2 - r2**2 + d**2) / (2 * d)
        # Intersection circle radius
        radius = math.sqrt(r1**2 - h**2)

        # Center of intersection circle along line from self.center to other.center
        direction = (other.center - self.center).normalize()
        circle_center = Point3D(
            self.center.x + direction.x * h,
            self.center.y + direction.y * h,
            self.center.z + direction.z * h,
        )

        return Circle3D(circle_center, radius, direction)

    def translate(self, offset: Vector3D) -> "Sphere":
        """
        Returns a new Sphere translated by the given vector.
        """
        new_center = self.center + offset
        return Sphere(new_center, self.radius)

    def scale(self, factor: float) -> "Sphere":
        """
        Returns a new Sphere scaled by the given factor relative to the origin.
        """
        if factor < 0:
            raise ValueError("Scale factor must be non-negative.")
        new_center = Point3D(self.center.x * factor,
                             self.center.y * factor,
                             self.center.z * factor)
        new_radius = self.radius * factor
        return Sphere(new_center, new_radius)

    def point_from_spherical_coords(self, theta: float, phi: float) -> Point3D:
        """
        Returns a point on the sphere surface given spherical coordinates.
        theta: azimuthal angle in radians [0, 2*pi]
        phi: polar angle in radians [0, pi]
        """
        x = self.center.x + self.radius * math.sin(phi) * math.cos(theta)
        y = self.center.y + self.radius * math.sin(phi) * math.sin(theta)
        z = self.center.z + self.radius * math.cos(phi)
        return Point3D(x, y, z)
