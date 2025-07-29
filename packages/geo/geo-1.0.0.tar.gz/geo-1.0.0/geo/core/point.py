# geo/core/point.py

"""
Defines Point classes in 2D and 3D space.
"""

import math
from typing import Union, Sequence, TypeVar, Generic
from .precision import is_equal, DEFAULT_EPSILON

# Type variable for Point coordinates
TCoord = TypeVar('TCoord', int, float)

class Point(Generic[TCoord]):
    """
    A base class for a point in N-dimensional space.
    Not intended for direct instantiation for specific dimensions,
    but provides common functionality.
    """
    _coords: Sequence[TCoord]

    def __init__(self, *coords: TCoord):
        """
        Initializes a Point with the given coordinates.

        Args:
            *coords: A sequence of numeric coordinates.

        Raises:
            ValueError: If no coordinates are provided.
        """
        if not coords:
            raise ValueError("Cannot create a Point with no coordinates.")
        self._coords = tuple(coords) # Store as tuple for immutability

    @property
    def coords(self) -> Sequence[TCoord]:
        """Returns the coordinates of the point as a tuple."""
        return self._coords

    @property
    def dimension(self) -> int:
        """Returns the dimension of the point."""
        return len(self._coords)

    def __getitem__(self, index: int) -> TCoord:
        """Allows accessing coordinates by index (e.g., p[0])."""
        return self._coords[index]

    def __len__(self) -> int:
        """Returns the dimension of the point."""
        return self.dimension

    def __eq__(self, other: object) -> bool:
        """
        Checks if two points are equal by comparing their coordinates.
        Uses `is_equal` for floating-point comparisons.
        """
        if not isinstance(other, Point) or self.dimension != other.dimension:
            return False
        return all(is_equal(s_coord, o_coord)
                    for s_coord, o_coord in zip(self._coords, other._coords))

    def __ne__(self, other: object) -> bool:
        """Checks if two points are not equal."""
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """Returns a string representation of the point."""
        return f"{self.__class__.__name__}({', '.join(map(str, self._coords))})"

    def __hash__(self) -> int:
        """
        Computes a hash for the point.
        Note: Due to floating point precision, points that are 'is_equal'
        might not have the same hash if their float representations differ slightly.
        For dictionary keys with floating point coords, consider custom handling or
        rounding to a certain precision if exact matches are needed for 'close' points.
        """
        # A simple hash, can be improved.
        # For floats, this can be tricky due to precision.
        # Consider rounding to a fixed number of decimal places for hashing if needed.
        return hash((self.__class__.__name__, self._coords))

    def distance_to(self, other: 'Point[TCoord]') -> float:
        """
        Calculates the Euclidean distance to another point.

        Args:
            other: The other Point object.

        Returns:
            The Euclidean distance.

        Raises:
            ValueError: If the points have different dimensions.
        """
        if self.dimension != other.dimension:
            raise ValueError("Points must have the same dimension to calculate distance.")
        return math.sqrt(sum((s_coord - o_coord)**2
                                for s_coord, o_coord in zip(self._coords, other.coords)))

    def midpoint(self, other: 'Point[TCoord]') -> 'Point[TCoord]':
        """
        Calculates the midpoint between this point and another.

        Args:
            other: Another Point object of the same dimension.

        Returns:
            A new Point object representing the midpoint.
        """
        if self.dimension != other.dimension:
            raise ValueError("Points must have the same dimension to calculate midpoint.")
        mid_coords = tuple((s + o) / 2 for s, o in zip(self.coords, other.coords))
        return self.__class__(*mid_coords)  # type: ignore

    # Operations with vectors
    def __add__(self, other: object) -> 'Point[TCoord]':
        """
        Adds a Vector to a Point, or adds two Points component-wise (e.g. during interpolation).
        """
        from .vector import Vector  # Local import to avoid circular dependency
        if isinstance(other, Vector) and self.dimension == other.dimension:
            new_coords = tuple(pc + vc for pc, vc in zip(self.coords, other.components))
            return self.__class__(*new_coords)  # type: ignore
        elif isinstance(other, Point) and self.dimension == other.dimension:
            new_coords = tuple(a + b for a, b in zip(self.coords, other.coords))
            return self.__class__(*new_coords)  # type: ignore
        raise TypeError(f"Can only add a Vector or Point of the same dimension to a Point. Got {type(other)}")

    def __sub__(self, other: object) -> Union['Vector', 'Point']:
        """
        Subtracts another Point or a Vector from this Point.
        - Point - Point = Vector
        - Point - Vector = Point
        """
        from .vector import Vector  # Local import to avoid circular dependency
        if isinstance(other, Point):
            if self.dimension != other.dimension:
                raise ValueError("Points must have the same dimension for subtraction.")
            vec_components = tuple(s_coord - o_coord for s_coord, o_coord in zip(self.coords, other.coords))
            if self.dimension == 2:
                from .vector import Vector2D
                return Vector2D(*vec_components)  # type: ignore
            elif self.dimension == 3:
                from .vector import Vector3D
                return Vector3D(*vec_components)  # type: ignore
            else:
                return Vector(*vec_components)  # type: ignore
        elif isinstance(other, Vector):
            if self.dimension != other.dimension:
                raise TypeError(f"Can only subtract a Vector of the same dimension from a Point. Got {type(other)}")
            new_coords = tuple(pc - vc for pc, vc in zip(self.coords, other.components))
            return self.__class__(*new_coords)  # type: ignore
        return NotImplemented


class Point2D(Point[float]):
    """Represents a point in 2D space."""

    def __init__(self, x: float, y: float):
        """
        Initializes a 2D point.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
        """
        super().__init__(float(x), float(y))

    @property
    def x(self) -> float:
        """Returns the x-coordinate."""
        return self._coords[0]

    @property
    def y(self) -> float:
        """Returns the y-coordinate."""
        return self._coords[1]

    # Example of a 2D specific method
    def to_polar(self) -> tuple[float, float]:
        """
        Converts Cartesian coordinates to polar coordinates.

        Returns:
            A tuple (r, theta) where r is the radius and theta is the angle in radians.
            Angle is in the range (-pi, pi].
        """
        r = math.sqrt(self.x**2 + self.y**2)
        theta = math.atan2(self.y, self.x)
        return r, theta

    @classmethod
    def from_polar(cls, r: float, theta: float) -> 'Point2D':
        """
        Creates a Point2D from polar coordinates.

        Args:
            r: The radius.
            theta: The angle in radians.

        Returns:
            A new Point2D object.
        """
        if r < 0:
            raise ValueError("Radius 'r' in polar coordinates cannot be negative.")
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return cls(x, y)

    def __mul__(self, scalar: float) -> 'Point2D':
        if isinstance(scalar, (int, float)):
            return Point2D(self.x * scalar, self.y * scalar)
        raise TypeError("Can only multiply Point2D by a scalar")

    def __rmul__(self, scalar: float) -> 'Point2D':
        return self.__mul__(scalar)
    

class Point3D(Point[float]):
    """Represents a point in 3D space."""

    def __init__(self, x: float, y: float, z: float):
        """
        Initializes a 3D point.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
            z: The z-coordinate.
        """
        super().__init__(float(x), float(y), float(z))

    @property
    def x(self) -> float:
        """Returns the x-coordinate."""
        return self._coords[0]

    @property
    def y(self) -> float:
        """Returns the y-coordinate."""
        return self._coords[1]

    @property
    def z(self) -> float:
        """Returns the z-coordinate."""
        return self._coords[2]

    # Example of a 3D specific method
    def to_spherical(self) -> tuple[float, float, float]:
        """
        Converts Cartesian coordinates to spherical coordinates (ISO 80000-2:2019 convention).
        r: radial distance
        theta: inclination (polar angle, angle from positive z-axis), range [0, pi]
        phi: azimuth (angle from positive x-axis in xy-plane), range (-pi, pi]

        Returns:
            A tuple (r, theta, phi).
        """
        r = self.distance_to(Point3D(0, 0, 0)) # Magnitude
        if is_equal(r, 0.0):
            return 0.0, 0.0, 0.0 # Origin

        theta = math.acos(self.z / r)  # Polar angle (inclination)
        phi = math.atan2(self.y, self.x)    # Azimuthal angle
        return r, theta, phi

    @classmethod
    def from_spherical(cls, r: float, theta: float, phi: float) -> 'Point3D':
        """
        Creates a Point3D from spherical coordinates (ISO 80000-2:2019 convention).

        Args:
            r: Radial distance (must be non-negative).
            theta: Inclination (polar angle from positive z-axis), in radians [0, pi].
            phi: Azimuth (angle from positive x-axis in xy-plane), in radians.

        Returns:
            A new Point3D object.
        """
        if r < 0:
            raise ValueError("Radial distance 'r' cannot be negative.")
        if not (0 <= theta <= math.pi + DEFAULT_EPSILON): # allow for slight precision errors around pi
                # Check if theta is slightly outside [0, pi] due to precision
            if not (is_equal(theta, 0.0) or is_equal(theta, math.pi)):
                raise ValueError(f"Inclination 'theta' must be in the range [0, pi]. Got {theta}")
            elif theta < 0:
                theta = 0.0
            elif theta > math.pi:
                theta = math.pi


        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return cls(x, y, z)
