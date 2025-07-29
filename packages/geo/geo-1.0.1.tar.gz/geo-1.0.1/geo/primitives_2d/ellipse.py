# geo/primitives_2d/ellipse.py

"""
Defines an Ellipse primitive in 2D space.
"""

import math
from typing import Tuple

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON

class Ellipse:
    """
    Represents an ellipse in 2D space.
    Defined by a center, semi-major axis length (a), semi-minor axis length (b),
    and a rotation angle for the major axis relative to the x-axis.
    We assume a >= b. If b > a, they are swapped.
    """
    def __init__(self, center: Point2D, semi_major_axis: float, semi_minor_axis: float, angle_rad: float = 0.0):
        """
        Initializes an Ellipse.

        Args:
            center: The center Point2D of the ellipse.
            semi_major_axis: Length of the semi-major axis (a).
            semi_minor_axis: Length of the semi-minor axis (b).
            angle_rad: Rotation angle of the major axis in radians, counter-clockwise from positive x-axis.

        Raises:
            ValueError: If semi-major or semi-minor axes are negative.
        """
        if semi_major_axis < 0 or semi_minor_axis < 0:
            raise ValueError("Ellipse axes lengths cannot be negative.")

        self.center = center
        # Ensure a >= b
        if semi_major_axis < semi_minor_axis:
            self.a = semi_minor_axis  # semi-major axis
            self.b = semi_major_axis  # semi-minor axis
            self.angle_rad = angle_rad + math.pi / 2 # Adjust angle if swapped
        else:
            self.a = semi_major_axis
            self.b = semi_minor_axis
            self.angle_rad = angle_rad
        
        # Normalize angle to [0, 2*pi) or (-pi, pi] if preferred
        self.angle_rad = self.angle_rad % (2 * math.pi)


    def __repr__(self) -> str:
        return (f"Ellipse(center={self.center}, a={self.a}, b={self.b}, "
                f"angle_rad={self.angle_rad:.4f})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ellipse):
            return False
        # Normalize angles before comparison for equivalence
        angle1_norm = self.angle_rad % math.pi # Ellipse has pi symmetry for its orientation
        angle2_norm = other.angle_rad % math.pi
        
        # Check if axes are swapped but represent the same ellipse
        same_axes = is_equal(self.a, other.a) and is_equal(self.b, other.b)
        swapped_axes = is_equal(self.a, other.b) and is_equal(self.b, other.a)

        if same_axes:
            return self.center == other.center and is_equal(angle1_norm, angle2_norm)
        elif swapped_axes: # If axes are swapped, angle needs to differ by pi/2
            # This case should be handled by the constructor ensuring a >= b.
            # If a constructor always enforces a>=b, then only same_axes needed.
            # However, if direct comparison of two Ellipse objects is needed where one might
            # have been constructed with a<b and angle adjusted, this is complex.
            # Assuming constructor normalizes (a>=b), this swapped_axes check is mostly redundant
            # unless comparing to an Ellipse that bypassed this normalization somehow.
            # For now, rely on constructor's a>=b normalization.
            return self.center == other.center and is_equal(angle1_norm, (angle2_norm + math.pi/2) % math.pi)

        return False


    @property
    def area(self) -> float:
        """Calculates the area of the ellipse."""
        return math.pi * self.a * self.b

    @property
    def linear_eccentricity(self) -> float:
        """
        Calculates the linear eccentricity (c), distance from center to each focus.
        c = sqrt(a^2 - b^2)
        Returns 0 if a < b (which shouldn't happen if constructor enforces a>=b).
        """
        if self.a < self.b: # Should not occur with constructor logic
            return 0.0
        return math.sqrt(self.a**2 - self.b**2)

    @property
    def eccentricity(self) -> float:
        """
        Calculates the eccentricity (e) of the ellipse.
        e = c / a = sqrt(1 - (b/a)^2)
        Returns 0 if a is zero.
        """
        if is_zero(self.a):
            return 0.0
        return self.linear_eccentricity / self.a
    
    def get_foci(self) -> Tuple[Point2D, Point2D]:
        """
        Calculates the two foci of the ellipse.
        Foci lie along the major axis, at distance c from the center.
        """
        if is_zero(self.a) and is_zero(self.b): # Degenerate ellipse (a point)
            return self.center, self.center
        if is_equal(self.a, self.b): # Circle, foci coincide at center
            return self.center, self.center

        c = self.linear_eccentricity
        
        # Direction of the major axis
        cos_angle = math.cos(self.angle_rad)
        sin_angle = math.sin(self.angle_rad)
        
        major_axis_direction = Vector2D(cos_angle, sin_angle)
        
        f1 = self.center + major_axis_direction * c
        f2 = self.center - major_axis_direction * c
        
        return f1, f2

    def circumference(self) -> float:
        """
        Calculates the circumference (perimeter) of the ellipse.
        This uses Ramanujan's approximation, which is quite accurate.
        C approx = pi * [3(a+b) - sqrt((3a+b)(a+3b))]
        """
        if is_zero(self.a) and is_zero(self.b): return 0.0
        if is_equal(self.a, self.b): # It's a circle
            return 2 * math.pi * self.a

        # Ramanujan's approximation
        h = ((self.a - self.b)**2) / ((self.a + self.b)**2)
        # C = math.pi * (self.a + self.b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
        # Simpler Ramanujan approximation:
        # C ≈ π [ 3(a+b) - √((3a+b)(a+3b)) ]
        term1 = 3 * (self.a + self.b)
        term2_factor1 = 3 * self.a + self.b
        term2_factor2 = self.a + 3 * self.b
        if term2_factor1 < 0 or term2_factor2 < 0: # Should not happen with a,b >=0
            # This indicates an issue, likely a or b became effectively negative
            # Fallback or error
            # For now, if a or b is very small, it might lead to issues.
            # Fallback to circle if a or b is zero and the other is not.
            if is_zero(self.b) and self.a > 0: return 4 * self.a # Degenerate ellipse (line segment) approx
            if is_zero(self.a) and self.b > 0: return 4 * self.b # Should not happen with a>=b
            return 0.0 # Or raise error

        term2 = math.sqrt(term2_factor1 * term2_factor2)
        return math.pi * (term1 - term2)


    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is inside or on the boundary of the ellipse.
        The point is transformed to the ellipse's local coordinate system (where it's axis-aligned).
        Then, (x/a)^2 + (y/b)^2 <= 1 within a numerical tolerance.
        """
        # Handle degenerate ellipse cases
        if self.a < epsilon or self.b < epsilon:
            if self.a < epsilon and self.b < epsilon:  # Point-like ellipse
                return point == self.center
            if self.a < epsilon:  # Vertical segment (b > 0)
                return math.isclose(point.x, self.center.x, abs_tol=epsilon) and \
                    abs(point.y - self.center.y) <= self.b + epsilon
            if self.b < epsilon:  # Horizontal segment (a > 0)
                return math.isclose(point.y, self.center.y, abs_tol=epsilon) and \
                    abs(point.x - self.center.x) <= self.a + epsilon
            return False  # Fallback, should not reach

        # Translate point so ellipse center is at origin
        translated_point = point - self.center

        # Rotate point by -self.angle_rad to align ellipse with axes
        cos_angle = math.cos(-self.angle_rad)
        sin_angle = math.sin(-self.angle_rad)

        local_x = translated_point.x * cos_angle - translated_point.y * sin_angle
        local_y = translated_point.x * sin_angle + translated_point.y * cos_angle

        # Check the ellipse equation
        # (local_x / self.a)^2 + (local_y / self.b)^2 <= 1
        if is_zero(self.a) or is_zero(self.b): # Avoid division by zero for degenerate
            # This case should ideally be handled by the a < epsilon or b < epsilon check above.
            # If a or b is zero, it's a line segment or a point.
            # If a=0, b=0, it's a point, check point == center.
            if is_zero(self.a) and is_zero(self.b): return point == self.center
            # If one is zero, it's a line segment.
            # e.g. if b=0, then local_y must be zero, and abs(local_x) <= a
            if is_zero(self.b):
                return is_zero(local_y, epsilon) and (abs(local_x) <= self.a + epsilon)
            if is_zero(self.a): # Should not happen if a >= b and b > 0
                return is_zero(local_x, epsilon) and (abs(local_y) <= self.b + epsilon)
            return False # Should not be reached

        val = (local_x / self.a)**2 + (local_y / self.b)**2
        return val <= 1.0 + 0.75*epsilon # Add epsilon for points very close to boundary

    # Intersection methods (e.g., with Line2D) are more complex for ellipses
    # and are omitted for this initial version.