# geo/primitives_3d/line_3d.py

"""
Defines Line, Segment, and Ray primitives in 3D space.

Coordinate system assumed is a standard right-handed Cartesian system.
"""

import math
from typing import Optional, Union

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON

class Line3D:
    """
    Represents an infinite line in 3D space.
    Defined by an origin point and a direction vector (normalized).
    """
    def __init__(self, origin: Point3D, direction_or_p2: Union[Vector3D, Point3D]):
        """
        Initializes a Line3D.

        Args:
            origin: A Point3D on the line.
            direction_or_p2:
                - If Vector3D: The direction Vector3D of the line.
                - If Point3D: Another Point3D on the line (direction = p2 - origin).

        Raises:
            ValueError: If direction vector is zero or if origin and p2 are the same.
            TypeError: If second argument is not Vector3D or Point3D.
        """
        self.origin = origin
        if isinstance(direction_or_p2, Vector3D):
            if direction_or_p2.is_zero_vector():
                raise ValueError("Line direction vector cannot be zero.")
            self.direction = direction_or_p2.normalize()
        elif isinstance(direction_or_p2, Point3D):
            if origin == direction_or_p2:
                raise ValueError("Cannot define a line with two identical points.")
            self.direction = (direction_or_p2 - origin).normalize()
        else:
            raise TypeError("Second argument must be a Vector3D or Point3D.")

    def __repr__(self) -> str:
        return f"Line3D(origin={self.origin}, direction={self.direction})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line3D):
            return False
        # Check if directions are parallel (allowing opposite)
        if not (self.direction == other.direction or self.direction == -other.direction):
            return False
        # Check if a point from one line lies on the other line
        # (This is sufficient as directions are parallel)
        return self.contains_point(other.origin)

    def point_at(self, t: float) -> Point3D:
        """Returns a point on the line at parameter t: P(t) = origin + t * direction."""
        return self.origin + (self.direction * t)

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if a point lies on the line."""
        if point == self.origin:
            return True
        vec_to_point = point - self.origin
        if vec_to_point.is_zero_vector():  # Redundant but safe
            return True
        # Vector to point must be parallel to line direction (cross product == zero vector)
        cross_prod = self.direction.cross(vec_to_point)
        return cross_prod.is_zero_vector(epsilon)

    def distance_to_point(self, point: Point3D) -> float:
        """
        Calculates the shortest distance from a point to this line.
        Distance = |(P - origin) x direction| (direction is normalized).
        """
        vec_origin_to_point = point - self.origin
        cross_product_vec = vec_origin_to_point.cross(self.direction)
        return cross_product_vec.magnitude()

    def project_point(self, point: Point3D) -> Point3D:
        """Projects a point orthogonally onto this line."""
        vec_origin_to_point = point - self.origin
        t = vec_origin_to_point.dot(self.direction)  # direction normalized
        return self.origin + self.direction * t


class Segment3D:
    """Represents a finite line segment in 3D space, defined by two distinct endpoints."""

    def __init__(self, p1: Point3D, p2: Point3D):
        if p1 == p2:
            raise ValueError("Segment endpoints cannot be identical.")
        self.p1 = p1
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Segment3D(p1={self.p1}, p2={self.p2})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Segment3D):
            return False
        # Equality allows reversed endpoints
        return (self.p1 == other.p1 and self.p2 == other.p2) or \
               (self.p1 == other.p2 and self.p2 == other.p1)

    @property
    def length(self) -> float:
        """Returns the Euclidean length of the segment."""
        return self.p1.distance_to(self.p2)

    @property
    def midpoint(self) -> Point3D:
        """Returns the midpoint of the segment."""
        return Point3D(
            (self.p1.x + self.p2.x) / 2,
            (self.p1.y + self.p2.y) / 2,
            (self.p1.z + self.p2.z) / 2
        )
    
    @property
    def direction_vector(self) -> Vector3D:
        """Returns the vector from p1 to p2 (not normalized)."""
        return self.p2 - self.p1

    def to_line(self) -> Line3D:
        """Converts the segment to an infinite Line3D defined by its endpoints."""
        return Line3D(self.p1, self.p2)

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the segment.

        Algorithm:
        1. Check collinearity with the line defined by segment endpoints.
        2. Verify if point lies between p1 and p2 by projection dot products.

        Args:
            point: Point3D to check.
            epsilon: Tolerance for floating comparisons.

        Returns:
            True if point lies on or very close to the segment.
        """
        line = self.to_line()
        if not line.contains_point(point, epsilon):
            return False

        vec_p1_p2 = self.p2 - self.p1
        vec_p1_point = point - self.p1

        dot_proj = vec_p1_point.dot(vec_p1_p2)
        if dot_proj < -epsilon:
            return False  # Point lies before p1 on line
        length_sq = vec_p1_p2.magnitude_squared()
        if dot_proj > length_sq + epsilon:
            return False  # Point lies beyond p2 on line

        return True

    def project_point(self, point: Point3D) -> Point3D:
        """
        Projects a point orthogonally onto the segment.
        If projection lies outside segment, clamps to nearest endpoint.
        """
        vec_p1_p2 = self.p2 - self.p1
        vec_p1_point = point - self.p1
        length_sq = vec_p1_p2.magnitude_squared()
        if is_zero(length_sq):
            return self.p1  # Degenerate segment

        t = vec_p1_point.dot(vec_p1_p2) / length_sq

        if t < 0:
            return self.p1
        elif t > 1:
            return self.p2
        else:
            return self.p1 + vec_p1_p2 * t

    def distance_to_point(self, point: Point3D) -> float:
        """
        Calculates the shortest distance from a point to the segment.

        Uses clamped projection to find closest point on segment.
        """
        projection = self.project_point(point)
        return projection.distance_to(point)


class Ray3D:
    """Represents a ray in 3D space with origin and infinite direction."""

    def __init__(self, origin: Point3D, direction: Vector3D):
        if direction.is_zero_vector():
            raise ValueError("Ray direction cannot be a zero vector.")
        self.origin = origin
        self.direction = direction.normalize()

    def __repr__(self) -> str:
        return f"Ray3D(origin={self.origin}, direction={self.direction})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ray3D):
            return False
        return self.origin == other.origin and self.direction == other.direction

    def point_at(self, t: float) -> Point3D:
        """Returns a point on the ray: P(t) = origin + t * direction with t >= 0."""
        if t < 0:
            raise ValueError("Parameter t must be non-negative for a ray.")
        return self.origin + (self.direction * t)

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the ray.

        Algorithm:
        1. Check collinearity with the ray's direction vector.
        2. Ensure the point lies in the same direction as the ray (t >= 0).
        """
        if point == self.origin:
            return True
        
        vec_to_point = point - self.origin
        if vec_to_point.is_zero_vector():
            return True

        cross_prod = self.direction.cross(vec_to_point)
        if not cross_prod.is_zero_vector(epsilon):
            return False
        
        dot_product = self.direction.dot(vec_to_point)
        return dot_product >= -epsilon  # Allow epsilon tolerance behind origin

    def project_point(self, point: Point3D) -> Point3D:
        """
        Projects a point orthogonally onto the ray.
        If projection parameter t < 0, returns the ray origin.
        """
        vec_origin_to_point = point - self.origin
        t = vec_origin_to_point.dot(self.direction)
        if t < 0:
            return self.origin
        else:
            return self.origin + self.direction * t

    def to_line(self) -> Line3D:
        """Converts the ray to an infinite Line3D."""
        return Line3D(self.origin, self.direction)
