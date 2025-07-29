# geo/primitives_3d/cylinder.py

"""
Defines a Cylinder primitive in 3D space.
"""

import math
from typing import Tuple, Optional

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from .plane import Plane  # For cap planes


class Cylinder:
    """
    Represents a finite right circular cylinder in 3D space.
    Defined by the center of its base, its axis direction, radius, and height.
    """

    def __init__(
        self,
        base_center: Point3D,
        axis_direction: Vector3D,
        radius: float,
        height: float,
    ):
        """
        Initializes a Cylinder.

        Args:
            base_center: The Point3D at the center of the cylinder's base cap.
            axis_direction: The Vector3D representing the direction of the cylinder's axis.
                            Will be normalized. Must not be a zero vector.
            radius: The radius of the cylinder. Must be non-negative.
            height: The height of the cylinder along its axis. Must be non-negative.

        Raises:
            ValueError: If axis_direction is zero, or if radius/height are negative.
        """
        if axis_direction.is_zero_vector():
            raise ValueError("Cylinder axis direction cannot be a zero vector.")
        if radius < 0:
            raise ValueError("Cylinder radius cannot be negative.")
        if height < 0:
            raise ValueError("Cylinder height cannot be negative.")

        self.base_center = base_center
        self.axis_direction = axis_direction.normalize()
        self.radius = radius
        self.height = height

        self.top_center = self.base_center + self.axis_direction * self.height

    def __repr__(self) -> str:
        return (
            f"Cylinder(base_center={self.base_center}, axis={self.axis_direction}, "
            f"radius={self.radius}, height={self.height})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cylinder):
            return False

        # Check if axes and centers match (consider flipped axis with swapped centers)
        axis_equal_direct = (
            self.axis_direction == other.axis_direction and self.base_center == other.base_center
        )
        axis_equal_flipped = (
            self.axis_direction == -other.axis_direction and self.base_center == other.top_center
        )
        axis_and_center_equal = axis_equal_direct or axis_equal_flipped

        return (
            axis_and_center_equal
            and is_equal(self.radius, other.radius, epsilon=DEFAULT_EPSILON)
            and is_equal(self.height, other.height, epsilon=DEFAULT_EPSILON)
        )

    @property
    def volume(self) -> float:
        """Calculates the volume of the cylinder: pi * r^2 * h."""
        return math.pi * self.radius**2 * self.height

    @property
    def lateral_surface_area(self) -> float:
        """Calculates the lateral surface area (side) of the cylinder: 2 * pi * r * h."""
        return 2 * math.pi * self.radius * self.height

    @property
    def base_area(self) -> float:
        """Calculates the area of one circular cap of the cylinder: pi * r^2."""
        return math.pi * self.radius**2

    @property
    def total_surface_area(self) -> float:
        """Calculates the total surface area: 2 * base_area + lateral_surface_area."""
        return 2 * self.base_area + self.lateral_surface_area

    def get_cap_planes(self) -> Tuple[Plane, Plane]:
        """
        Returns the two planes of the cylinder caps.
        
        The base cap's normal points opposite to the axis direction (outward from volume),
        and the top cap's normal points along the axis direction.
        """
        base_plane = Plane(self.base_center, -self.axis_direction)  # Normal points outward from base
        top_plane = Plane(self.top_center, self.axis_direction)  # Normal points outward from top
        return base_plane, top_plane

    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is inside or on the boundary of the cylinder.

        Steps:
        1. Project point onto the cylinder's axis. Check if projection is between base and top (with epsilon tolerance).
        2. Calculate distance from point to the axis. Check if it's within radius (with epsilon tolerance).

        Args:
            point: The point to test.
            epsilon: Tolerance for boundary checks.

        Returns:
            True if point is inside or on the boundary, False otherwise.
        """
        vec_base_to_point = point - self.base_center
        dist_along_axis = vec_base_to_point.dot(self.axis_direction)

        if not (-epsilon <= dist_along_axis <= self.height + epsilon):
            return False  # Outside height range

        point_on_axis = self.base_center + self.axis_direction * dist_along_axis

        radial_distance = point.distance_to(point_on_axis)
        return radial_distance <= self.radius + epsilon

    def distance_to_axis(self, point: Point3D) -> float:
        """
        Calculates the shortest distance from a given point to the cylinder's axis line.

        Args:
            point: The point to measure distance from.

        Returns:
            The shortest distance from point to the axis line.
        """
        vec_base_to_point = point - self.base_center
        proj_length = vec_base_to_point.dot(self.axis_direction)
        point_on_axis = self.base_center + self.axis_direction * proj_length
        return point.distance_to(point_on_axis)

    def get_lateral_surface_point(self, angle_radians: float, height_fraction: float) -> Point3D:
        """
        Returns a point on the lateral surface of the cylinder given an angle around
        the axis and a height fraction along the axis.

        Args:
            angle_radians: Angle around the axis in radians (0 aligned with some reference).
            height_fraction: Fraction between 0 (base) and 1 (top) along the axis height.

        Returns:
            A Point3D on the lateral surface of the cylinder.
        """
        if not 0 <= height_fraction <= 1:
            raise ValueError("height_fraction must be between 0 and 1")

        # Find an arbitrary perpendicular vector to axis_direction
        # We'll generate two orthogonal vectors perpendicular to axis_direction:
        axis = self.axis_direction
        if abs(axis.x) < 1e-8 and abs(axis.y) < 1e-8:
            # Axis close to z-axis
            perp1 = Vector3D(1, 0, 0)
        else:
            perp1 = Vector3D(-axis.y, axis.x, 0).normalize()
        perp2 = axis.cross(perp1)

        # Calculate point on circle
        lateral_point = (
            self.base_center
            + axis * (height_fraction * self.height)
            + perp1 * (self.radius * math.cos(angle_radians))
            + perp2 * (self.radius * math.sin(angle_radians))
        )
        return lateral_point

    def project_point_onto_axis(self, point: Point3D) -> float:
        """
        Projects a point onto the cylinder's axis and returns the scalar distance along the axis
        from the base_center.

        Args:
            point: The point to project.

        Returns:
            Scalar projection length along the axis from base_center.
        """
        vec_base_to_point = point - self.base_center
        return vec_base_to_point.dot(self.axis_direction)
