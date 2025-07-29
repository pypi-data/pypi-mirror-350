# geo/primitives_2d/rectangle.py

"""
Defines a Rectangle primitive in 2D space.
"""

import math
from typing import List, Optional, Union

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, DEFAULT_EPSILON
from .polygon import Polygon

class Rectangle(Polygon):
    """
    Represents a rectangle in 2D space.
    Can be initialized with two opposite corner points, or with a corner, width, height, and angle.
    Inherits from Polygon. Vertices are ordered counter-clockwise by default.
    """

    def __init__(self, p1: Point2D, p2_or_width: Union[Point2D, float],
                 height: Optional[float] = None, angle_rad: float = 0.0):
        """
        Initializes a Rectangle.

        Method 1: Two opposite corner points.
            Args:
                p1: First corner Point2D.
                p2_or_width: Opposite corner Point2D.
                height: Must be None.
                angle_rad: Must be 0.0 (ignored).

        Method 2: A corner point, width, height, and rotation angle.
            Args:
                p1: The bottom-left corner (before rotation) Point2D.
                p2_or_width: The width (float).
                height: The height (float).
                angle_rad: Rotation angle in radians, CCW from x-axis.

        Raises:
            ValueError: If arguments are inconsistent or width/height are non-positive.
        """
        self.p1 = p1  # Store reference point for rotated case

        if isinstance(p2_or_width, Point2D) and height is None:
            # ── Axis-aligned rectangle from two opposite corners ──
            p3 = p2_or_width
            if p1 == p3:
                raise ValueError("Corner points of a rectangle cannot be identical.")

            min_x, max_x = (p1.x, p3.x) if p1.x < p3.x else (p3.x, p1.x)
            min_y, max_y = (p1.y, p3.y) if p1.y < p3.y else (p3.y, p1.y)

            bl = Point2D(min_x, min_y)
            br = Point2D(max_x, min_y)
            tr = Point2D(max_x, max_y)
            tl = Point2D(min_x, max_y)

            vertices = [bl, br, tr, tl]  # CCW order
            super().__init__(vertices)

            self._width = max_x - min_x
            self._height = max_y - min_y
            self._angle_rad = 0.0

        elif isinstance(p2_or_width, (int, float)) and height is not None:
            # ── Rotated rectangle from base point, width, height, and angle ──
            width = float(p2_or_width)

            if width <= 0 or height <= 0:
                raise ValueError("Rectangle width and height must be positive.")

            self._width = width
            self._height = height
            self._angle_rad = angle_rad

            # Local rectangle before rotation
            local_p1 = Point2D(0, 0)
            local_p2 = Point2D(width, 0)
            local_p3 = Point2D(width, height)
            local_p4 = Point2D(0, height)

            vertices_local = [local_p1, local_p2, local_p3, local_p4]
            rotated_vertices = []

            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            for p_local in vertices_local:
                rot_x = p_local.x * cos_a - p_local.y * sin_a
                rot_y = p_local.x * sin_a + p_local.y * cos_a
                final_x = rot_x + self.p1.x
                final_y = rot_y + self.p1.y
                rotated_vertices.append(Point2D(final_x, final_y))

            super().__init__(rotated_vertices)

        else:
            raise ValueError("Invalid arguments for Rectangle constructor.")

    @property
    def width(self) -> float:
        """Returns the width of the rectangle."""
        if hasattr(self, '_width'):
            return self._width
        return self.vertices[0].distance_to(self.vertices[1])

    @property
    def height(self) -> float:
        """Returns the height of the rectangle."""
        if hasattr(self, '_height'):
            return self._height
        return self.vertices[1].distance_to(self.vertices[2])

    @property
    def angle(self) -> float:
        """Returns the rotation angle in radians from x-axis."""
        if hasattr(self, '_angle_rad'):
            return self._angle_rad
        edge_vec = self.vertices[1] - self.vertices[0]
        return edge_vec.angle() if not edge_vec.is_zero_vector() else 0.0

    @property
    def area(self) -> float:
        """Returns the area of the rectangle."""
        if hasattr(self, '_width') and hasattr(self, '_height'):
            return self._width * self._height
        return super().area  # Shoelace method

    @property
    def diagonal_length(self) -> float:
        """Returns the diagonal length of the rectangle."""
        if hasattr(self, '_width') and hasattr(self, '_height'):
            return math.hypot(self._width, self._height)
        return self.vertices[0].distance_to(self.vertices[2])

    def is_square(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if the rectangle is a square."""
        if self.num_vertices != 4:
            return False
        return is_equal(self.width, self.height, epsilon)
