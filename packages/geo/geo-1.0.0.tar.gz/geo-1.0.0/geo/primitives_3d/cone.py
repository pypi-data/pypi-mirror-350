# geo/primitives_3d/cone.py

"""
Defines a Cone primitive in 3D space.
"""
import math

from geo.core import Point3D, Vector3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from .plane import Plane # For base plane

class Cone:
    """
    Represents a finite right circular cone in 3D space.
    Defined by its apex point, the center of its circular base, and the radius of the base.
    The height and axis direction are derived from these.
    """
    def __init__(self, apex: Point3D, base_center: Point3D, base_radius: float):
        """
        Initializes a Cone.

        Args:
            apex: The apex (tip) Point3D of the cone.
            base_center: The Point3D at the center of the cone's circular base.
            base_radius: The radius of the cone's base. Must be non-negative.

        Raises:
            ValueError: If apex and base_center are the same (degenerate cone),
                        or if base_radius is negative.
        """
        if apex == base_center:
            # Allow if radius is also zero (it's a point)
            if not is_zero(base_radius):
                raise ValueError("Apex and base_center cannot be the same for a non-zero radius cone.")
        if base_radius < 0:
            raise ValueError("Cone base radius cannot be negative.")

        self.apex = apex
        self.base_center = base_center
        self.base_radius = base_radius

        vec_base_to_apex = apex - base_center
        self.height = vec_base_to_apex.magnitude()

        if is_zero(self.height) and not is_zero(self.base_radius):
            # This means apex == base_center, but radius > 0 (a disk)
            # This class represents a cone, not a disk.
            # Or, if height is zero, it's a flat disk.
            # For a "cone", height is usually positive if radius is positive.
            # Let's allow height=0 if radius=0 (point cone).
            # If height=0 and radius > 0, it's a disk. We can define axis as arbitrary or error.
            # For now, if height is zero (apex=base_center), axis is undefined unless radius is also zero.
            self.axis_direction = Vector3D(0,0,1) # Default axis if degenerate, or could be error
            if not is_zero(self.base_radius):
                    # This is a disk, not a typical cone.
                    # Could raise error or define axis based on context if needed.
                    # For simplicity, let's assume a "cone" implies some height if radius > 0.
                    # The constructor already checks apex == base_center for non-zero radius.
                    pass

        elif not is_zero(self.height):
            self.axis_direction = vec_base_to_apex.normalize()
        else: # height is zero, radius must also be zero (point cone)
            self.axis_direction = Vector3D(0,0,1) # Arbitrary axis for a point


    def __repr__(self) -> str:
        return (f"Cone(apex={self.apex}, base_center={self.base_center}, "
                f"base_radius={self.base_radius})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cone):
            return False
        return (self.apex == other.apex and
                self.base_center == other.base_center and
                is_equal(self.base_radius, other.base_radius))

    @property
    def slant_height(self) -> float:
        """Calculates the slant height of the cone."""
        if is_zero(self.base_radius) and is_zero(self.height): return 0.0
        return math.sqrt(self.height**2 + self.base_radius**2)

    @property
    def volume(self) -> float:
        """Calculates the volume of the cone: (1/3) * pi * r^2 * h."""
        return (1/3) * math.pi * self.base_radius**2 * self.height

    @property
    def lateral_surface_area(self) -> float:
        """Calculates the lateral surface area of the cone: pi * r * slant_height."""
        return math.pi * self.base_radius * self.slant_height

    @property
    def base_area(self) -> float:
        """Calculates the area of the circular base: pi * r^2."""
        return math.pi * self.base_radius**2

    @property
    def total_surface_area(self) -> float:
        """Calculates the total surface area: base_area + lateral_surface_area."""
        return self.base_area + self.lateral_surface_area

    def get_base_plane(self) -> Plane:
        """Returns the plane of the cone's base."""
        # Normal of the base plane points away from the apex, along -axis_direction
        # (or towards apex if axis_direction is from base to apex)
        # Current axis_direction is from base_center towards apex.
        # So normal of base plane is -self.axis_direction.
        if is_zero(self.height) and not is_zero(self.base_radius): # A disk
                # Axis is ill-defined, assume normal is (0,0,1) or based on context
                # This case needs careful handling for axis.
                # For now, if it's a disk, its "axis" for the plane normal would be arbitrary.
                # Let's assume the stored axis_direction is somewhat meaningful or default.
                return Plane(self.base_center, -self.axis_direction if not self.axis_direction.is_zero_vector() else Vector3D(0,0,-1))

        return Plane(self.base_center, -self.axis_direction)


    def contains_point(self, point: Point3D, epsilon: float = DEFAULT_EPSILON) -> bool:
        """
        Checks if a point is inside or on the boundary of the cone.
        1. Point must be between the base plane and a plane through the apex parallel to base.
        2. For a point P, let its projection onto the cone's axis be Q.
            The distance from P to Q (radial_dist) must be <= R_at_Q,
            where R_at_Q is the radius of the cone's cross-section at Q.
            R_at_Q = base_radius * (distance from apex to Q) / height.
        """
        if is_zero(self.height): # Cone is a disk or a point
            if is_zero(self.base_radius): # Point cone
                return point == self.apex
            else: # Disk
                base_plane = self.get_base_plane()
                if not base_plane.contains_point(point, epsilon):
                    return False
                return point.distance_to(self.base_center) <= self.base_radius + epsilon

        # Vector from base_center to the point
        vec_base_to_point = point - self.base_center
        # Projection of this vector onto the axis gives distance from base along axis
        dist_along_axis_from_base = vec_base_to_point.dot(self.axis_direction)

        # Check if point is axially between base and apex
        if not (-epsilon <= dist_along_axis_from_base <= self.height + epsilon):
            return False

        # If point is at the apex
        if is_equal(dist_along_axis_from_base, self.height, epsilon) and point == self.apex :
                return True


        # Point on the axis closest to the given 'point'
        point_on_axis = self.base_center + self.axis_direction * dist_along_axis_from_base
        
        # Radial distance of 'point' from the axis
        radial_distance = point.distance_to(point_on_axis)

        # Cone's radius at the height of 'point_on_axis'
        # Height of point_on_axis from base is dist_along_axis_from_base
        # Distance from apex to point_on_axis's plane = self.height - dist_along_axis_from_base
        dist_apex_to_point_plane = self.height - dist_along_axis_from_base
        
        # Using similar triangles: R_at_height / dist_apex_to_point_plane = base_radius / height
        # R_at_height = base_radius * dist_apex_to_point_plane / height
        if is_zero(self.height): # Should be caught earlier, but for safety
            return is_zero(radial_distance, epsilon) and is_zero(self.base_radius, epsilon) # Point at apex

        cone_radius_at_height = self.base_radius * (dist_apex_to_point_plane / self.height)
        
        return radial_distance <= cone_radius_at_height + epsilon