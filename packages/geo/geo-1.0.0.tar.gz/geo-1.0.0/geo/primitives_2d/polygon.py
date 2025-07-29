# geo/primitives_2d/polygon.py

"""
Defines a Polygon primitive in 2D space.
"""

from typing import List, Sequence
import math

from geo.core import Point2D, Vector2D
from geo.core.precision import is_zero, is_equal, DEFAULT_EPSILON
from .line import Segment2D # For edges and intersection checks

class Polygon:
    """
    Represents a 2D polygon defined by a sequence of vertices.
    The vertices are assumed to be ordered (clockwise or counter-clockwise).
    This implementation primarily supports simple polygons (non-self-intersecting).
    """
    def __init__(self, vertices: Sequence[Point2D]):
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices.")
        self.vertices = tuple(vertices) # Store as tuple for immutability

    def __repr__(self) -> str:
        return f"Polygon(vertices={self.vertices})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polygon):
            return False
        if len(self.vertices) != len(other.vertices):
            return False
        # This requires checking for cyclic equality of vertices
        # For example, [P1,P2,P3] == [P2,P3,P1] == [P3,P1,P2]
        # And also reversed order if orientation doesn't matter for equality.
        # For now, a simple direct match (same start, same order).
        # A more robust check would involve finding a common start and direction.
        return self.vertices == other.vertices # Simplistic equality

    @property
    def num_vertices(self) -> int:
        """Returns the number of vertices in the polygon."""
        return len(self.vertices)

    @property
    def edges(self) -> List[Segment2D]:
        """
        Returns a list of Segment2D objects representing the edges of the polygon.
        """
        if self.num_vertices < 2: # Should not happen with constructor
            return []
        edges_list = []
        for i in range(self.num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.num_vertices] # Loop back to the first vertex
            edges_list.append(Segment2D(p1, p2))
        return edges_list

    @property
    def perimeter(self) -> float:
        """Calculates the perimeter of the polygon."""
        return sum(edge.length for edge in self.edges)

    @property
    def area(self) -> float:
        """
        Unsigned area of the polygon.

        * Simple polygon   →  abs(signed_area)
        * Self-intersecting →  positive cross-term sum (net enclosed area)
        """
        if self.num_vertices < 3:
            return 0.0

        s_area = self.signed_area()

        if abs(s_area) > DEFAULT_EPSILON:
            return abs(s_area)

        verts = self.vertices if s_area >= 0 else tuple(reversed(self.vertices))

        pos_sum = 0.0
        for i in range(len(verts)):
            p1 = verts[i]
            p2 = verts[(i + 1) % len(verts)]
            cross = p1.x * p2.y - p2.x * p1.y
            if cross > 0:
                pos_sum += cross

        return 0.5 * pos_sum

    def signed_area(self) -> float:
        if self.num_vertices < 3:
            return 0.0

        area_val = 0.0
        for i in range(self.num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.num_vertices]
            area_val += (p1.x * p2.y - p2.x * p1.y)
        return area_val / 2.0

    def is_clockwise(self) -> bool:
        """Checks if the polygon vertices are ordered clockwise."""
        return self.signed_area() < 0

    def is_counter_clockwise(self) -> bool:
        """Checks if the polygon vertices are ordered counter-clockwise."""
        return self.signed_area() > 0
        
    def centroid(self) -> Point2D:
        """
        Calculates the geometric centroid (center of mass) of a simple polygon.
        Formula: Cx = (1/6A) * sum_{i=0}^{n-1} (xi + x_{i+1}) * (xi*y_{i+1} - x_{i+1}*yi)
                    Cy = (1/6A) * sum_{i=0}^{n-1} (yi + y_{i+1}) * (xi*y_{i+1} - x_{i+1}*yi)
        where A is the signed area.
        """
        if self.num_vertices < 3:
            # Undefined or return average of vertices for degenerate cases
            # For a line (2 vertices) or point (1 vertex), centroid is average.
            # But polygon requires 3.
            # For now, raise error or return an arbitrary point like first vertex.
            # Or, if it's a valid (but small) polygon like a near-degenerate triangle:
            if self.num_vertices > 0:
                avg_x = sum(v.x for v in self.vertices) / self.num_vertices
                avg_y = sum(v.y for v in self.vertices) / self.num_vertices
                return Point2D(avg_x, avg_y)
            raise ValueError("Centroid calculation requires at least 3 vertices for a polygon.")


        signed_a = self.signed_area()
        if is_zero(signed_a):
            # Degenerate polygon (e.g., all points collinear).
            # Centroid can be taken as the average of vertices in this case.
            sum_x = sum(v.x for v in self.vertices)
            sum_y = sum(v.y for v in self.vertices)
            return Point2D(sum_x / self.num_vertices, sum_y / self.num_vertices)

        cx_sum = 0.0
        cy_sum = 0.0
        for i in range(self.num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.num_vertices]
            cross_term = (p1.x * p2.y - p2.x * p1.y)
            cx_sum += (p1.x + p2.x) * cross_term
            cy_sum += (p1.y + p2.y) * cross_term
        
        centroid_x = cx_sum / (6 * signed_a)
        centroid_y = cy_sum / (6 * signed_a)
        
        return Point2D(centroid_x, centroid_y)

    def is_convex(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if the polygon is convex.
        A polygon is convex if all its internal angles are <= 180 degrees.
        This can be checked by looking at the sign of the cross product of
        consecutive edge vectors. All cross products should have the same sign
        (or be zero for collinear edges).
        Assumes vertices are ordered (e.g., CCW).
        """
        if self.num_vertices < 3:
            return False # Or True for 1 or 2 points, depending on definition. Typically for polygons.
        if self.num_vertices == 3:
            return True # A triangle is always convex.

        # Get a consistent orientation (e.g., force CCW for checking)
        # For simplicity, we'll check based on the current orientation.
        # If the orientation is mixed, it's not convex.

        got_positive_turn = False
        got_negative_turn = False

        for i in range(self.num_vertices):
            p0 = self.vertices[i]
            p1 = self.vertices[(i + 1) % self.num_vertices]
            p2 = self.vertices[(i + 2) % self.num_vertices]

            # Edge vectors
            v1 = p1 - p0
            v2 = p2 - p1
            
            # 2D cross product (scalar)
            cross_product = v1.x * v2.y - v1.y * v2.x

            if cross_product > epsilon:
                got_positive_turn = True
            elif cross_product < -epsilon:
                got_negative_turn = True
            
            # If we have both positive and negative turns, it's concave.
            if got_positive_turn and got_negative_turn:
                return False
        
        # If we only got one type of turn (or all collinear, cross_product is zero), it's convex.
        # If all turns are zero (collinear points), it's degenerate but can be considered convex.
        return True


    def contains_point(self, point: Point2D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is inside, on the boundary, or outside the polygon.
        Uses the Ray Casting algorithm (even-odd rule) or Winding Number algorithm.
        This implementation uses the winding number algorithm.
        A point is inside if its winding number is non-zero.
        For simple polygons, winding number is +/-1 for inside, 0 for outside.

        Args:
            point: The Point2D to check.
            epsilon: Tolerance for floating point comparisons.

        Returns:
            True if the point is inside or on the boundary, False otherwise.
        """
        if self.num_vertices < 3:
            return False

        # First, check if point is one of the vertices
        for vertex in self.vertices:
            if point == vertex:
                return True
        
        # Check if point is on an edge
        for edge in self.edges:
            if edge.contains_point(point, epsilon):
                return True

        # Winding number algorithm
        winding_number = 0
        for i in range(self.num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.num_vertices]

            # Check if edge (p1,p2) crosses the horizontal ray from 'point' to the right.
            # Point must be between y-coordinates of edge endpoints.
            if p1.y <= point.y:
                if p2.y > point.y: # An upward crossing
                    # Calculate cross product: (p2-p1) x (point-p1)
                    # If positive, point is to the left of edge (p1,p2)
                    # (p2.x - p1.x) * (point.y - p1.y) - (p2.y - p1.y) * (point.x - p1.x)
                    # This is equivalent to checking orientation: orientation(p1, p2, point)
                    # If orientation > 0 (CCW turn from p1-p2 to p1-point), it's a valid crossing.
                    # Simplified: is_left = (p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y)
                    # If is_left > 0, increment winding number.
                    # Using (B - A) x (P - A)
                    # (bx - ax) * (py - ay) - (by - ay) * (px - ax)
                    val = (p2.x - p1.x) * (point.y - p1.y) - (p2.y - p1.y) * (point.x - p1.x)
                    if val > epsilon: # Point is to the left of upward edge
                        winding_number += 1
            elif p2.y <= point.y: # A downward crossing
                # If orientation < 0 (CW turn from p1-p2 to p1-point), it's a valid crossing.
                # If is_left < 0, decrement winding number.
                val = (p2.x - p1.x) * (point.y - p1.y) - (p2.y - p1.y) * (point.x - p1.x)
                if val < -epsilon: # Point is to the right of downward edge
                    winding_number -= 1
        
        return not is_zero(float(winding_number)) # Non-zero winding number means inside.