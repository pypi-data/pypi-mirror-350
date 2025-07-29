# geo/primitives_2d/line.py

"""
Defines Line, Segment, and Ray primitives in 2D space.
"""
import math
from typing import Optional, Union

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON

class Line2D:
    """
    Represents an infinite line in 2D space.
    A line can be defined by two distinct points or by a point and a direction vector.
    """

    def __init__(self, p1: Point2D, p2_or_direction: Union[Point2D, Vector2D]):
        """
        Initializes a Line2D.

        Args:
            p1: The first Point2D on the line.
            p2_or_direction:
                - If Point2D: A second distinct Point2D on the line.
                - If Vector2D: The direction Vector2D of the line.

        Raises:
            ValueError: If p1 and p2 are the same point, or if direction vector is zero.
        """
        self.p1 = p1
        if isinstance(p2_or_direction, Point2D):
            if p1 == p2_or_direction:
                raise ValueError("Cannot define a line with two identical points.")
            self.direction = (p2_or_direction - p1).normalize()
        elif isinstance(p2_or_direction, Vector2D):
            if p2_or_direction.is_zero_vector():
                raise ValueError("Cannot define a line with a zero direction vector.")
            self.direction = p2_or_direction.normalize()
        else:
            raise TypeError("Second argument must be a Point2D or a Vector2D.")

    def __repr__(self) -> str:
        return f"Line2D(p1={self.p1}, direction={self.direction})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line2D):
            return False
        # Check if directions are parallel and if a point from one line lies on the other
        if not (self.direction == other.direction or self.direction == -other.direction):
            return False
        return self.contains_point(other.p1)

    def point_at(self, t: float) -> Point2D:
        """
        Returns a point on the line at parameter t.
        P(t) = p1 + t * direction

        Args:
            t: The parameter.

        Returns:
            The Point2D on the line corresponding to t.
        """
        return self.p1 + (self.direction * t)

    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the line.

        Args:
            point: The Point2D to check.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            True if the point is on the line, False otherwise.
        """
        if point == self.p1:
            return True
        vec_to_point = point - self.p1
        if vec_to_point.is_zero_vector(): # Should be caught by point == self.p1
            return True
        # Check if vec_to_point is parallel to self.direction
        # Cross product of 2D vectors (v1.x*v2.y - v1.y*v2.x) should be zero if parallel
        cross_product = self.direction.x * vec_to_point.y - self.direction.y * vec_to_point.x
        return is_zero(cross_product, epsilon)

    def is_parallel_to(self, other: 'Line2D', epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if this line is parallel to another line.
        Parallel lines have direction vectors that are scalar multiples of each other.
        Their 2D cross product (z-component) is zero.
        """
        cross_product = self.direction.x * other.direction.y - self.direction.y * other.direction.x
        return is_zero(cross_product, epsilon)

    def is_perpendicular_to(self, other: 'Line2D', epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if this line is perpendicular to another line.
        Perpendicular lines have direction vectors whose dot product is zero.
        """
        dot_product = self.direction.dot(other.direction)
        return is_zero(dot_product, epsilon)

    def intersection_with(self, other: 'Line2D', epsilon: float = DEFAULT_EPSILON) -> Optional[Point2D]:
        """
        Calculates the intersection point with another line.

        Args:
            other: The other Line2D.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            The intersection Point2D, or None if lines are parallel (or coincident).
            If lines are coincident, this method returns None as there isn't a single intersection point.
        """
        if self.is_parallel_to(other, epsilon):
            return None  # Parallel or coincident lines

        # Line 1: P = A + t*u  (self.p1, self.direction)
        # Line 2: Q = B + s*v  (other.p1, other.direction)
        # A.x + t*u.x = B.x + s*v.x
        # A.y + t*u.y = B.y + s*v.y
        # t*u.x - s*v.x = B.x - A.x
        # t*u.y - s*v.y = B.y - A.y
        # Using Cramer's rule or substitution:
        # Denominator = u.x*v.y - u.y*v.x (which is -self.direction.cross(other.direction))
        
        a = self.p1
        u = self.direction
        b = other.p1
        v = other.direction

        denominator = u.x * v.y - u.y * v.x # This is -u.cross(v)

        if is_zero(denominator, epsilon): # Should be caught by is_parallel_to
            return None

        # t = ((b.x - a.x) * v.y - (b.y - a.y) * v.x) / denominator
        t_num = (b.x - a.x) * v.y - (b.y - a.y) * v.x
        t = t_num / denominator

        return self.point_at(t)

    def distance_to_point(self, point: Point2D) -> float:
        """
        Calculates the shortest distance from a point to this line.
        Distance = |(AP x d)| / |d|, where AP is vector from point on line to the given point,
        d is direction vector. For 2D, |(AP x d)| is |AP.x*d.y - AP.y*d.x|.
        Since d is normalized, |d|=1. So distance = |AP x d|.
        """
        ap = point - self.p1
        # The cross product in 2D (scalar result)
        cross_product_mag = ap.x * self.direction.y - ap.y * self.direction.x
        return abs(cross_product_mag)


class Segment2D:
    """
    Represents a line segment in 2D space, defined by two distinct endpoints.
    """
    def __init__(self, p1: Point2D, p2: Point2D):
        """
        Initializes a Segment2D.

        Args:
            p1: The first endpoint.
            p2: The second endpoint.

        Raises:
            ValueError: If p1 and p2 are the same point.
        """
        if p1 == p2:
            raise ValueError("Cannot define a segment with two identical points.")
        self.p1 = p1
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Segment2D(p1={self.p1}, p2={self.p2})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Segment2D):
            return False
        return (self.p1 == other.p1 and self.p2 == other.p2) or \
                (self.p1 == other.p2 and self.p2 == other.p1)

    @property
    def length(self) -> float:
        """Returns the length of the segment."""
        return self.p1.distance_to(self.p2)

    @property
    def midpoint(self) -> Point2D:
        """Returns the midpoint of the segment."""
        return Point2D((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2)

    @property
    def direction_vector(self) -> Vector2D:
        """Returns the direction vector from p1 to p2 (not necessarily normalized)."""
        return self.p2 - self.p1

    def to_line(self) -> Line2D:
        """Converts the segment to an infinite Line2D."""
        return Line2D(self.p1, self.p2)

    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the segment within a given epsilon tolerance.
        Considers the point to be 'on' the segment if:
        - It lies approximately on the line (collinear within epsilon).
        - It projects within or near the segment bounds.
        """
        # 1. Check for collinearity
        # Create vectors from p1 to point and p1 to p2
        vec_p1_point = point - self.p1
        vec_p1_p2 = self.p2 - self.p1

        if vec_p1_p2.is_zero_vector():  # Degenerate segment
            return point == self.p1

        # Cross product = area of parallelogram; divide by length to get perpendicular distance
        cross = vec_p1_p2.x * vec_p1_point.y - vec_p1_p2.y * vec_p1_point.x
        seg_len = vec_p1_p2.magnitude()

        # Handle degenerate segments (shouldn’t occur due to constructor, but just in case)
        if seg_len == 0:
            return (point - self.p1).magnitude() <= epsilon

        distance = abs(cross) / seg_len
        if distance > epsilon:
            return False

        # Dot product: projection must lie between p1 and p2 (with epsilon slack)
        dot = vec_p1_point.dot(vec_p1_p2)
        if dot < -epsilon:
            return False
        if dot > vec_p1_p2.magnitude_squared() + epsilon:
            return False

        return True

    def intersection_with_segment(self, other: 'Segment2D', epsilon: float = DEFAULT_EPSILON) -> Optional[Point2D]:
        """
        Calculates the intersection point with another segment.

        Args:
            other: The other Segment2D.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            The intersection Point2D, or None if they do not intersect or overlap.
            If segments overlap along a line, this method currently returns None.
            Handling of overlapping segments can be complex and is omitted for simplicity.
        """
        line1 = self.to_line()
        line2 = other.to_line()

        intersection_point = line1.intersection_with(line2, epsilon)

        if intersection_point is None:
            # Lines are parallel. Check for collinear overlap (more complex, not fully handled here)
            # For simplicity, if lines are parallel, segments don't intersect unless collinear and overlapping
            if line1.is_parallel_to(line2) and line1.contains_point(other.p1):
                # Collinear. Now check for overlap.
                # This part is tricky and can have multiple cases (no overlap, partial, one contains other)
                # For now, return None for collinear overlaps to keep it simple.
                # A full implementation would check if endpoints of one are on the other segment.
                pass # Fall through to return None for parallel/collinear without single point intersection
            return None

        # Check if the intersection point lies on both segments
        if self.contains_point(intersection_point, epsilon) and \
            other.contains_point(intersection_point, epsilon):
            return intersection_point
        
        return None

    def distance_to_point(self, point: Point2D) -> float:
        """Calculates the shortest distance from a point to this segment."""
        # Vector from p1 to p2
        line_vec = self.p2 - self.p1
        # Vector from p1 to the point
        p1_to_point_vec = point - self.p1

        if line_vec.is_zero_vector(): # Should be caught by constructor
            return self.p1.distance_to(point)

        # Project p1_to_point_vec onto line_vec
        # t = dot(p1_to_point_vec, line_vec) / dot(line_vec, line_vec)
        line_mag_sq = line_vec.magnitude_squared()
        t = p1_to_point_vec.dot(line_vec) / line_mag_sq

        if t < 0.0:
            # Closest point is p1
            return self.p1.distance_to(point)
        elif t > 1.0:
            # Closest point is p2
            return self.p2.distance_to(point)
        else:
            # Closest point is on the segment, project point onto the line
            projection = self.p1 + line_vec * t
            return projection.distance_to(point)


class Ray2D:
    """
    Represents a ray in 2D space, starting at an origin and extending infinitely
    in a given direction.
    """
    def __init__(self, origin: Point2D, direction: Vector2D):
        """
        Initializes a Ray2D.

        Args:
            origin: The starting Point2D of the ray.
            direction: The Vector2D indicating the ray's direction. Must be non-zero.

        Raises:
            ValueError: If the direction vector is a zero vector.
        """
        if direction.is_zero_vector():
            raise ValueError("Ray direction cannot be a zero vector.")
        self.origin = origin
        self.direction = direction.normalize() # Store normalized direction

    def __repr__(self) -> str:
        return f"Ray2D(origin={self.origin}, direction={self.direction})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ray2D):
            return False
        return self.origin == other.origin and self.direction == other.direction

    def point_at(self, t: float) -> Point2D:
        """
        Returns a point on the ray at parameter t.
        P(t) = origin + t * direction.
        Note: For a ray, t must be non-negative.

        Args:
            t: The parameter (must be >= 0).

        Returns:
            The Point2D on the ray.

        Raises:
            ValueError: If t is negative.
        """
        if t < 0:
            # Or silently return origin for t=0, or clamp t.
            # Raising error is stricter for "point on ray" definition.
            raise ValueError("Parameter t must be non-negative for a ray.")
        return self.origin + (self.direction * t)

    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the ray.
        The point must be collinear with the ray's line and on the positive side
        of the origin along the ray's direction.
        """
        if point == self.origin:
            return True
        
        vec_to_point = point - self.origin
        if vec_to_point.is_zero_vector(): # Should be caught by point == self.origin
            return True

        # 1. Check for collinearity (cross product with direction should be zero)
        cross_product = self.direction.x * vec_to_point.y - self.direction.y * vec_to_point.x
        if not is_zero(cross_product, epsilon):
            return False

        # 2. Check if the point is in the direction of the ray (dot product should be non-negative)
        dot_product = self.direction.dot(vec_to_point)
        return dot_product >= -epsilon # Allow for slight numerical errors around origin

    def to_line(self) -> Line2D:
        """Converts the ray to an infinite Line2D."""
        return Line2D(self.origin, self.direction)

    # Intersection methods (e.g., with Line, Segment, other Ray) can be added.
    # They would typically involve finding the intersection with the underlying line
    # and then checking if the parameter 't' is non-negative.