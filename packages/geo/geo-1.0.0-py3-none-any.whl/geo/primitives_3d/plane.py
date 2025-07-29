# geo/primitives_3d/plane.py

"""
Defines a Plane primitive in 3D space.
"""

# geo/primitives_3d/plane.py

"""
Defines a Plane primitive in 3D space.
"""

from typing import Optional, Union, Tuple, TYPE_CHECKING

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON

if TYPE_CHECKING:
    from .line_3d import Line3D

class Plane:
    """
    Represents an infinite plane in 3D space.

    A plane can be defined by a point on the plane and a normal vector,
    or by three non-collinear points.

    The plane equation is: n · (P - P0) = 0, where n is the normal,
    P0 is a point on the plane, and P is any point (x,y,z) on the plane.

    This can be written as:
        Ax + By + Cz = D,
    where (A, B, C) is the normal vector n,
    and D = n · P0 (note: this is the plane constant in this form).
    """

    def __init__(
        self,
        point_on_plane: Point3D,
        normal_or_p2: Union[Vector3D, Point3D],
        p3: Optional[Point3D] = None
    ):
        """
        Initializes a Plane.

        Method 1: Point and Normal
            Args:
                point_on_plane: A Point3D on the plane.
                normal_or_p2: The normal Vector3D to the plane.
                p3: Must be None.

        Method 2: Three non-collinear points
            Args:
                point_on_plane (p1): The first Point3D.
                normal_or_p2 (p2): The second Point3D.
                p3: The third Point3D.

        Raises:
            ValueError: If the normal vector is zero, or if the three points are collinear.
            TypeError: If arguments are inconsistent.
        """
        self.point_on_plane = point_on_plane

        if isinstance(normal_or_p2, Vector3D) and p3 is None:
            if normal_or_p2.is_zero_vector():
                raise ValueError("Plane normal vector cannot be a zero vector.")
            self.normal = normal_or_p2.normalize()
        elif isinstance(normal_or_p2, Point3D) and isinstance(p3, Point3D):
            p1 = point_on_plane
            p2 = normal_or_p2
            # Calculate normal from three points p1, p2, p3
            v1 = p2 - p1
            v2 = p3 - p1
            calculated_normal = v1.cross(v2)
            if calculated_normal.is_zero_vector():
                raise ValueError("The three points are collinear and cannot define a plane.")
            self.normal = calculated_normal.normalize()
        else:
            raise TypeError(
                "Invalid arguments for Plane constructor. "
                "Use (Point3D, Vector3D) or (Point3D, Point3D, Point3D)."
            )

        # D constant for plane equation Ax + By + Cz = D
        # Note: Different from standard form Ax + By + Cz + D = 0,
        # here D = n · P0
        self.d_coeff = self.normal.dot(
            Vector3D(self.point_on_plane.x, self.point_on_plane.y, self.point_on_plane.z)
        )

    def __repr__(self) -> str:
        return f"Plane(point_on_plane={self.point_on_plane}, normal={self.normal})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Plane):
            return False

        dot = self.normal.dot(other.normal)
        if not is_equal(abs(dot), 1.0):
            return False
        return other.contains_point(self.point_on_plane)

    def signed_distance_to_point(self, point: Point3D) -> float:
        """
        Calculates the signed distance from a point to the plane.

        Distance = n · (P - P0) / |n|. Since |n|=1, Distance = n · (P - P0).
        Positive if the point is on the side of the normal, negative otherwise.
        """
        vec_to_point = point - self.point_on_plane
        return self.normal.dot(vec_to_point)

    def distance_to_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> float:
        """Calculates the shortest (unsigned) distance from a point to the plane."""
        return abs(self.signed_distance_to_point(point))

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point lies on the plane.

        This is true if the signed distance from the point to the plane is close to zero.
        """
        return is_zero(self.signed_distance_to_point(point), epsilon)

    def project_point(self, point: Point3D) -> Point3D:
        """
        Projects a point onto the plane.

        P_proj = P - (n · (P - P0)) * n
        """
        signed_dist = self.signed_distance_to_point(point)
        projected_point = point - (self.normal * signed_dist)
        return projected_point

    def intersection_with_line(self, line: 'Line3D') -> Optional[Point3D]:
        """
        Calculates the intersection point of this plane with a Line3D.

        Args:
            line: The Line3D to intersect with.

        Returns:
            The intersection Point3D, or None if the line is parallel to the plane
            and not on the plane. If the line lies on the plane, it also returns None
            as there is no single intersection point (infinite intersections).
        """
        n_dot_l_dir = self.normal.dot(line.direction)

        if is_zero(n_dot_l_dir):
            # Line is parallel to the plane.
            # Check if the line's origin point is on the plane.
            if self.contains_point(line.origin):
                return None  # Line lies on the plane (infinite intersections)
            else:
                return None  # Line is parallel and not on the plane (no intersection)

        n_dot_l0 = self.normal.dot(
            Vector3D(line.origin.x, line.origin.y, line.origin.z)
        )
        t = (self.d_coeff - n_dot_l0) / n_dot_l_dir

        return line.point_at(t)

    def get_coefficients(self) -> Tuple[float, float, float, float]:
        """
        Returns the coefficients (A, B, C, D) of the plane equation:
            Ax + By + Cz = D
        """
        return (self.normal.x, self.normal.y, self.normal.z, self.d_coeff)
