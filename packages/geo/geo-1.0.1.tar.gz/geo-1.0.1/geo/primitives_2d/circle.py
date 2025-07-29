# geo/primitives_2d/circle.py

"""
Defines a Circle primitive in 2D space.
"""
import math
from typing import Optional, List

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, is_zero, is_positive, DEFAULT_EPSILON
from .line import Line2D # For intersection methods

class Circle:
    """
    Represents a circle in 2D space, defined by a center point and a radius.
    """
    def __init__(self, center: Point2D, radius: float):
        """
        Initializes a Circle.

        Args:
            center: The center Point2D of the circle.
            radius: The radius of the circle. Must be non-negative.

        Raises:
            ValueError: If the radius is negative.
        """
        if radius < 0:
            raise ValueError("Circle radius cannot be negative.")
        self.center = center
        self.radius = radius

    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return False
        return self.center == other.center and is_equal(self.radius, other.radius)

    @property
    def area(self) -> float:
        """Calculates the area of the circle."""
        return math.pi * self.radius**2

    @property
    def circumference(self) -> float:
        """Calculates the circumference (perimeter) of the circle."""
        return 2 * math.pi * self.radius

    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is inside or on the boundary of the circle.

        Args:
            point: The Point2D to check.
            epsilon: Tolerance for floating point comparisons (for boundary).

        Returns:
            True if the point is contained within or on the circle, False otherwise.
        """
        distance_sq = self.center.distance_to(point)**2
        radius_sq = self.radius**2
        return math.sqrt(distance_sq) <= math.sqrt(radius_sq) + epsilon # Add epsilon for points very close to boundary

    def on_boundary(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies exactly on the boundary of the circle.
        """
        return is_equal(self.center.distance_to(point), self.radius, epsilon)

    def intersection_with_line(self, line: Line2D, epsilon: float = DEFAULT_EPSILON) -> List[Point2D]:
        """
        Calculates the intersection points of this circle with a Line2D.

        Args:
            line: The Line2D to intersect with.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            A list of intersection Point2Ds.
            - Empty list if no intersection.
            - One point if the line is tangent to the circle.
            - Two points if the line secants the circle.
        """
        # Algorithm:
        # 1. Find the closest point on the line to the circle's center.
        #    Let C be circle center, P_line be a point on the line, D_line be line direction.
        #    Vector from P_line to C: V = C - P_line
        #    Projection of V onto D_line: t = V.dot(D_line) (since D_line is normalized)
        #    Closest point on line M = P_line + t * D_line
        # 2. Calculate distance from circle center C to M (dist_CM).
        # 3. Compare dist_CM with radius R:
        #    - If dist_CM > R: No intersection.
        #    - If dist_CM == R (approx): One intersection (tangent), M is the point.
        #    - If dist_CM < R: Two intersections.
        #      Distance from M to intersection points along the line:
        #      offset = sqrt(R^2 - dist_CM^2)
        #      Intersection points: M +/- offset * D_line

        intersections: List[Point2D] = []

        # Vector from a point on the line (line.p1) to the circle's center
        cp_vec = self.center - line.p1
        
        # Project cp_vec onto the line's direction vector
        # t_closest is the parameter along the line from line.p1 to the closest point
        t_closest = cp_vec.dot(line.direction)
        
        # Closest point on the line to the circle's center
        closest_point_on_line = line.p1 + line.direction * t_closest
        
        dist_center_to_closest_sq = self.center.distance_to(closest_point_on_line)**2
        radius_sq = self.radius**2

        if dist_center_to_closest_sq > radius_sq + epsilon and not is_equal(dist_center_to_closest_sq, radius_sq, epsilon):
            return [] # No intersection (line is too far)

        if is_equal(dist_center_to_closest_sq, radius_sq, epsilon):
            # Tangent: one intersection point
            intersections.append(closest_point_on_line)
            return intersections
        
        # Two intersection points
        # dist_center_to_closest_sq < radius_sq
        # Use Pythagoras: offset_sq = radius_sq - dist_center_to_closest_sq
        offset_sq = radius_sq - dist_center_to_closest_sq
        if offset_sq < 0: # Should not happen if previous checks are correct, but for safety
            offset_sq = 0
        
        offset_along_line = math.sqrt(offset_sq)

        p1 = closest_point_on_line + line.direction * offset_along_line
        p2 = closest_point_on_line - line.direction * offset_along_line
        
        intersections.append(p1)
        # Avoid adding duplicate point if offset_along_line is zero (though covered by tangent case)
        if not p1.__eq__(p2): # Use __eq__ for Point2D comparison with tolerance
                intersections.append(p2)
        return intersections

    def intersection_with_circle(self, other: 'Circle', epsilon: float = DEFAULT_EPSILON) -> List[Point2D]:
        """
        Calculates the intersection points of this circle with another circle.

        Args:
            other: The other Circle to intersect with.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            A list of intersection Point2Ds.
            - Empty list if no intersection (circles are separate or one contains another without touching).
            - One point if circles are tangent.
            - Two points if circles intersect at two distinct points.
            - Potentially infinite if circles are coincident (returns empty list for now).
        """
        # Distance between centers
        d = self.center.distance_to(other.center)
        r1 = self.radius
        r2 = other.radius
        intersections: List[Point2D] = []

        if is_zero(d, epsilon) and is_equal(r1, r2, epsilon):
            # Coincident circles - infinite intersections, return empty for simplicity
            return []
        
        # No intersection cases:
        if d > r1 + r2 + epsilon:  # Circles are separate
            return []
        if d < abs(r1 - r2) - epsilon:  # One circle contains another without touching
            return []

        # Tangent cases:
        if is_equal(d, r1 + r2, epsilon) or is_equal(d, abs(r1 - r2), epsilon):
            # One intersection point
            # The intersection point lies on the line connecting the centers.
            # Vector from self.center to other.center
            center_to_center_vec = (other.center - self.center)
            if center_to_center_vec.is_zero_vector(): # Should be caught by coincident case
                if is_equal(r1,0) and is_equal(r2,0): return [self.center] # Both are points
                # This case implies d=0, but r1 != r2, handled by containment check.
                # If d=0, r1=r2 -> coincident.
                # If d=0, r1!=r2, one inside other, if abs(r1-r2) = 0 -> r1=r2, so this is complex.
                # Let's assume d > 0 for tangent point calculation here if not coincident.
                # If d=0 and tangent, it means r1=0 or r2=0 and the other radius is also 0.
                # Handled by the d=0, r1=r2 case mostly.
                # If one radius is 0 (it's a point) and it's on the other circle's boundary.
                if is_equal(r1,0) and is_equal(other.center.distance_to(self.center), r2):
                    return [self.center]
                if is_equal(r2,0) and is_equal(self.center.distance_to(other.center), r1):
                    return [other.center]
                return [] # Should not be easily reachable if d=0 and not coincident

            # Point is r1 along the normalized vector from self.center towards other.center
            # (or away if internally tangent)
            # If d = r1 + r2 (external tangency)
            # If d = abs(r1 - r2) (internal tangency)
            # The intersection point P = C1 + (C2-C1) * (r1/d)
            # This formula for the intersection point might be slightly off for internal tangency scaling.
            # A more robust way:
            # The intersection point is on the line connecting the centers.
            # P = C1 + dir_vec * r1 (if externally tangent, dir_vec from C1 to C2)
            # P = C1 + dir_vec * r1 (if internally tangent, C2 inside C1, dir_vec from C1 to C2)
            # P = C1 - dir_vec * r1 (if internally tangent, C1 inside C2, dir_vec from C1 to C2)
            
            # Let's use geometry.
            # The point of tangency P is such that C1, C2, P are collinear.
            # If C1=C2, already handled (coincident or one contains other).
            vec_c1_c2 = (other.center - self.center).normalize()
            tangent_point = self.center + vec_c1_c2 * r1
            
            # Verify this point is also on the other circle
            if other.on_boundary(tangent_point, epsilon):
                intersections.append(tangent_point)
            else: # Try the other direction for internal tangency if r1 > r2 and d = r1 - r2
                tangent_point_alt = self.center - vec_c1_c2 * r1
                if other.on_boundary(tangent_point_alt, epsilon):
                        intersections.append(tangent_point_alt)
                # This logic for tangency point can be tricky.
                # A common method is to find the radical axis (which is tangent line here)
                # and intersect it with line of centers.
                # For now, this simplified approach for a single tangent point.
                # If d = abs(r1-r2), P = C1 + (r1/d)*(C2-C1) if r1>r2, or C2 + (r2/d)*(C1-C2) if r2>r1
                # This is equivalent to scaling.
                if is_equal(d,0): # Should be caught if r1=r2 (coincident) or one is point
                    if is_equal(r1,r2): return [] # Coincident
                    # One is a point, and it's the center of the other, and tangent means radius of other is 0.
                    if (is_equal(r1,0) and is_equal(r2,0)) : return [self.center]

            return intersections


        # Two intersection points case:
        # Using the cosine rule to find angles, or by finding the radical axis.
        # The radical axis for two circles (x-x1)^2 + (y-y1)^2 = r1^2 and (x-x2)^2 + (y-y2)^2 = r2^2
        # is 2(x2-x1)x + 2(y2-y1)y = (r1^2 - r2^2) - (x1^2 - y1^2) + (x2^2 - y2^2)
        # This is a line. Intersect this line with one of the circles.

        # Simpler geometric approach:
        # d^2 = distance between centers squared
        d_sq = d**2
        r1_sq = r1**2
        r2_sq = r2**2

        # Distance from self.center to the midpoint of the common chord (on the line of centers)
        # a = (r1^2 - r2^2 + d^2) / (2*d)
        if is_zero(d): return [] # Should be caught by coincident or containment

        a = (r1_sq - r2_sq + d_sq) / (2 * d)

        # Half-length of the common chord (h)
        # h^2 = r1^2 - a^2
        h_sq = r1_sq - a*a
        if h_sq < -epsilon : # No real solution for h, means no intersection (or tangent, already handled)
            return []
        if h_sq < 0: h_sq = 0 # Clamp due to precision
        
        h = math.sqrt(h_sq)

        # Midpoint of the common chord (P_mid)
        # P_mid = C1 + a * (C2-C1)/d
        vec_c1_c2_norm = (other.center - self.center).normalize()
        p_mid = self.center + vec_c1_c2_norm * a

        # Direction perpendicular to the line of centers
        perp_vec = Vector2D(-vec_c1_c2_norm.y, vec_c1_c2_norm.x)

        i1 = p_mid + perp_vec * h
        i2 = p_mid - perp_vec * h
        
        intersections.append(i1)
        if not i1.__eq__(i2): # Avoid duplicate for tangent case where h might be zero
            intersections.append(i2)
        
        return intersections