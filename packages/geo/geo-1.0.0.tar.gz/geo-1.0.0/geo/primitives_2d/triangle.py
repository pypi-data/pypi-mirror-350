# geo/primitives_2d/triangle.py

"""
Defines a Triangle primitive in 2D space.
"""
import math
from typing import Tuple, List, Optional

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from .polygon import Polygon
from .line import Line2D, Segment2D
from .circle import Circle


class Triangle(Polygon):
    """
    Represents a triangle in 2D space, defined by three vertices.
    Inherits from Polygon.
    """
    def __init__(self, p1: Point2D, p2: Point2D, p3: Point2D):
        """
        Initializes a Triangle.

        Args:
            p1, p2, p3: The three Point2D vertices of the triangle.

        Raises:
            ValueError: If the three points are collinear (form a degenerate triangle).
        """
        super().__init__([p1, p2, p3])
        # Check for collinearity (signed area would be zero)
        if is_zero(super().signed_area()):
            raise ValueError("Vertices are collinear, cannot form a non-degenerate triangle.")
        
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    @property
    def area(self) -> float:
        """
        Calculates the area of the triangle.
        Overrides Polygon.area for potential direct calculation, though Shoelace is fine.
        Area = 0.5 * |x1(y2−y3) + x2(y3−y1) + x3(y1−y2)|
        """
        # Using the inherited Polygon.area which uses Shoelace formula is generally good.
        return super().area # Or implement the direct formula:
        # return 0.5 * abs(self.p1.x * (self.p2.y - self.p3.y) + \
        #                  self.p2.x * (self.p3.y - self.p1.y) + \
        #                  self.p3.x * (self.p1.y - self.p2.y))

    @property
    def side_lengths(self) -> Tuple[float, float, float]:
        """Returns the lengths of the three sides (a, b, c).
        a: length of side opposite p1 (segment p2-p3)
        b: length of side opposite p2 (segment p1-p3)
        c: length of side opposite p3 (segment p1-p2)
        """
        len_a = self.p2.distance_to(self.p3) # side opposite p1
        len_b = self.p1.distance_to(self.p3) # side opposite p2
        len_c = self.p1.distance_to(self.p2) # side opposite p3
        return len_a, len_b, len_c

    @property
    def angles_rad(self) -> Tuple[float, float, float]:
        """
        Returns the three internal angles of the triangle in radians.
        (angle_at_p1, angle_at_p2, angle_at_p3)
        Uses the Law of Cosines: c^2 = a^2 + b^2 - 2ab*cos(C)
        => cos(C) = (a^2 + b^2 - c^2) / (2ab)
        """
        a, b, c = self.side_lengths
        
        if is_zero(a) or is_zero(b) or is_zero(c): # Degenerate
            return (0.0, 0.0, 0.0) # Or handle error

        # Angle at p1 (opposite side a)
        cos_alpha = (b**2 + c**2 - a**2) / (2 * b * c)
        # Angle at p2 (opposite side b)
        cos_beta  = (a**2 + c**2 - b**2) / (2 * a * c)
        # Angle at p3 (opposite side c)
        cos_gamma = (a**2 + b**2 - c**2) / (2 * a * b)

        # Clamp values to [-1, 1] due to potential floating point inaccuracies
        alpha = math.acos(max(-1.0, min(1.0, cos_alpha)))
        beta  = math.acos(max(-1.0, min(1.0, cos_beta)))
        gamma = math.acos(max(-1.0, min(1.0, cos_gamma))) # Or gamma = math.pi - alpha - beta for precision

        return alpha, beta, gamma

    @property
    def angles_deg(self) -> Tuple[float, float, float]:
        """Returns the three internal angles in degrees."""
        return tuple(math.degrees(rad) for rad in self.angles_rad)

    def is_equilateral(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if the triangle is equilateral."""
        a, b, c = self.side_lengths
        return is_equal(a, b, epsilon) and is_equal(b, c, epsilon)

    def is_isosceles(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if the triangle is isosceles."""
        if self.is_equilateral(epsilon): # Equilateral is also isosceles
            return True
        a, b, c = self.side_lengths
        return is_equal(a, b, epsilon) or \
                is_equal(b, c, epsilon) or \
                is_equal(a, c, epsilon)

    def is_right(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if the triangle is a right-angled triangle."""
        angles = self.angles_rad
        right_angle = math.pi / 2
        return any(is_equal(angle, right_angle, epsilon) for angle in angles)
    
    @property
    def circumcircle(self) -> Optional[Circle]:
        """
        Calculates the circumcircle of the triangle (the circle passing through all three vertices).
        Returns None if the triangle is degenerate (vertices are collinear),
        though the constructor should prevent this.
        """
        # Using formula for circumcenter coordinates:
        # D = 2 * (x1(y2 - y3) + x2(y3 - y1) + x3(y1 - y2))
        # This D is 4 * signed_area_of_triangle. If D is zero, points are collinear.
        
        D_val = 2 * (self.p1.x * (self.p2.y - self.p3.y) + \
                        self.p2.x * (self.p3.y - self.p1.y) + \
                        self.p3.x * (self.p1.y - self.p2.y))

        if is_zero(D_val):
            return None # Collinear points, no unique circumcircle (or infinite radius)

        p1_sq = self.p1.x**2 + self.p1.y**2
        p2_sq = self.p2.x**2 + self.p2.y**2
        p3_sq = self.p3.x**2 + self.p3.y**2

        center_x = (1/D_val) * (p1_sq * (self.p2.y - self.p3.y) + \
                                p2_sq * (self.p3.y - self.p1.y) + \
                                p3_sq * (self.p1.y - self.p2.y))
        
        center_y = (1/D_val) * (p1_sq * (self.p3.x - self.p2.x) + \
                                p2_sq * (self.p1.x - self.p3.x) + \
                                p3_sq * (self.p2.x - self.p1.x))
        
        center = Point2D(center_x, center_y)
        radius = center.distance_to(self.p1)
        
        return Circle(center, radius)

    @property
    def incircle(self) -> Optional[Circle]:
        """
        Calculates the incircle of the triangle (the largest circle contained within the triangle).
        Returns None if the triangle is degenerate.
        Incenter Ix = (a*x1 + b*x2 + c*x3) / (a+b+c)
        Incenter Iy = (a*y1 + b*y2 + c*y3) / (a+b+c)
        Inradius r = Area / s, where s is semi-perimeter (a+b+c)/2.
        """
        a, b, c = self.side_lengths # a=p2p3, b=p1p3, c=p1p2
        perimeter_val = a + b + c

        if is_zero(perimeter_val): # Degenerate
            return None

        # Incenter coordinates
        # Note: a is length of side p2-p3 (opposite p1), b is p1-p3 (opposite p2), c is p1-p2 (opposite p3)
        center_x = (a * self.p1.x + b * self.p2.x + c * self.p3.x) / perimeter_val
        center_y = (a * self.p1.y + b * self.p2.y + c * self.p3.y) / perimeter_val
        center = Point2D(center_x, center_y)

        # Inradius
        area_val = self.area
        semi_perimeter = perimeter_val / 2.0
        if is_zero(semi_perimeter): # Degenerate
            return None
        
        radius = area_val / semi_perimeter
        
        return Circle(center, radius)