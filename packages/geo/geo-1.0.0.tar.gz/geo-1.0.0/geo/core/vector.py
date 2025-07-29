# geo/core/vector.py

"""
Defines Vector classes in 2D and 3D space.
"""

import math
from typing import Union, Sequence, TypeVar, Generic, overload, cast, TYPE_CHECKING
from .precision import is_equal, is_zero, DEFAULT_EPSILON

if TYPE_CHECKING:
    from .point import Point # For type hinting and operations

# Type variable for Vector components
TComponent = TypeVar('TComponent', int, float)

class Vector(Generic[TComponent]):
    """
    A base class for a vector in N-dimensional space.
    Provides common vector operations.
    """
    _components: Sequence[TComponent]

    def __init__(self, *components: TComponent):
        """
        Initializes a Vector with the given components.

        Args:
            *components: A sequence of numeric components.

        Raises:
            ValueError: If no components are provided.
        """
        if not components:
            raise ValueError("Cannot create a Vector with no components.")
        self._components = tuple(components) # Store as tuple for immutability

    @property
    def components(self) -> Sequence[TComponent]:
        """Returns the components of the vector as a tuple."""
        return self._components

    @property
    def dimension(self) -> int:
        """Returns the dimension of the vector."""
        return len(self._components)

    def __getitem__(self, index: int) -> TComponent:
        """Allows accessing components by index (e.g., v[0])."""
        return self._components[index]

    def __len__(self) -> int:
        """Returns the dimension of the vector."""
        return self.dimension

    def __eq__(self, other: object) -> bool:
        """
        Checks if two vectors are equal by comparing their components.
        Uses `is_equal` for floating-point comparisons.
        """
        if not isinstance(other, Vector) or self.dimension != other.dimension:
            return False
        return all(is_equal(s_comp, o_comp)
                    for s_comp, o_comp in zip(self._components, other._components))

    def __ne__(self, other: object) -> bool:
        """Checks if two vectors are not equal."""
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """Returns a string representation of the vector."""
        return f"{self.__class__.__name__}({', '.join(map(str, self._components))})"

    def __hash__(self) -> int:
        """
        Computes a hash for the vector.
        Similar to Point, hashing floats can be tricky.
        """
        return hash((self.__class__.__name__, self._components))

    def magnitude_squared(self) -> float:
        """Calculates the squared magnitude (length) of the vector."""
        return sum(c**2 for c in self._components) # type: ignore

    def magnitude(self) -> float:
        """Calculates the magnitude (length) of the vector."""
        return math.sqrt(self.magnitude_squared())

    def normalize(self) -> 'Vector[float]':
        """
        Returns a new unit vector in the same direction as this vector.

        Returns:
            A new Vector with magnitude 1.

        Raises:
            ValueError: If the vector is a zero vector (cannot normalize).
        """
        mag = self.magnitude()
        if is_zero(mag):
            raise ValueError("Cannot normalize a zero vector.")
        # Ensure the new vector components are floats
        normalized_components = tuple(float(c) / mag for c in self._components)

        # Return an instance of the correct subclass (Vector2D, Vector3D, or Vector)
        if isinstance(self, Vector2D):
            return Vector2D(*cast(Sequence[float], normalized_components)) # type: ignore
        elif isinstance(self, Vector3D):
            return Vector3D(*cast(Sequence[float], normalized_components)) # type: ignore
        else:
            return Vector(*cast(Sequence[float], normalized_components)) # type: ignore


    def is_zero_vector(self, epsilon: float = DEFAULT_EPSILON) -> bool:
        """Checks if the vector is a zero vector (all components are close to zero)."""
        return all(is_zero(c, epsilon) for c in self._components) # type: ignore

    # Vector arithmetic
    def __add__(self, other: 'Vector[TComponent]') -> 'Vector[TComponent]':
        """Adds another vector to this vector, returning a new vector."""
        if not isinstance(other, Vector) or self.dimension != other.dimension:
            raise TypeError(f"Can only add a Vector of the same dimension. Got {type(other)}")
        new_components = tuple(s_comp + o_comp for s_comp, o_comp in zip(self.components, other.components))
        return self.__class__(*new_components) # type: ignore

    def __sub__(self, other: 'Vector[TComponent]') -> 'Vector[TComponent]':
        """Subtracts another vector from this vector, returning a new vector."""
        if not isinstance(other, Vector) or self.dimension != other.dimension:
            raise TypeError(f"Can only subtract a Vector of the same dimension. Got {type(other)}")
        new_components = tuple(s_comp - o_comp for s_comp, o_comp in zip(self.components, other.components))
        return self.__class__(*new_components) # type: ignore

    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        """Multiplies the vector by a scalar, returning a new vector (Vector * scalar)."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented # Let Python try __rmul__ or raise TypeError
        new_components = tuple(c * scalar for c in self.components) # type: ignore
        return self.__class__(*new_components) # type: ignore

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        """Multiplies the vector by a scalar (scalar * Vector)."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> 'Vector[float]':
        """Divides the vector by a scalar, returning a new vector with float components."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if is_zero(float(scalar)):
            raise ZeroDivisionError("Cannot divide vector by zero.")
        new_components = tuple(float(c) / scalar for c in self.components) # type: ignore
            # Return an instance of the correct subclass (Vector2D, Vector3D, or Vector)
        if isinstance(self, Vector2D):
            return Vector2D(*cast(Sequence[float], new_components)) # type: ignore
        elif isinstance(self, Vector3D):
            return Vector3D(*cast(Sequence[float], new_components)) # type: ignore
        else:
            return Vector(*cast(Sequence[float], new_components)) # type: ignore


    def __neg__(self) -> 'Vector[TComponent]':
        """Negates the vector, returning a new vector."""
        new_components = tuple(-c for c in self.components) # type: ignore
        return self.__class__(*new_components) # type: ignore

    def dot(self, other: 'Vector[TComponent]') -> float:
        """
        Calculates the dot product with another vector.

        Args:
            other: The other Vector object.

        Returns:
            The dot product.

        Raises:
            ValueError: If the vectors have different dimensions.
        """
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension for dot product.")
        return sum(s_comp * o_comp for s_comp, o_comp in zip(self.components, other.components)) # type: ignore

    def angle_between(self, other: 'Vector[TComponent]', in_degrees: bool = False) -> float:
        """
        Calculates the angle between this vector and another vector.

        Args:
            other: The other Vector object.
            in_degrees: If True, returns the angle in degrees. Otherwise, in radians.

        Returns:
            The angle in radians or degrees.

        Raises:
            ValueError: If either vector is a zero vector or dimensions mismatch.
        """
        if self.is_zero_vector() or other.is_zero_vector():
            raise ValueError("Cannot calculate angle with a zero vector.")
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension to calculate angle.")

        dot_product = self.dot(other)
        mag_product = self.magnitude() * other.magnitude()

        # Clamp the cosine value to [-1, 1] to avoid domain errors with acos
        # due to potential floating point inaccuracies.
        cos_theta = max(-1.0, min(1.0, dot_product / mag_product))

        angle_rad = math.acos(cos_theta)

        return math.degrees(angle_rad) if in_degrees else angle_rad


class Vector2D(Vector[float]):
    """Represents a vector in 2D space."""

    def __init__(self, x: float, y: float):
        """
        Initializes a 2D vector.

        Args:
            x: The x-component.
            y: The y-component.
        """
        super().__init__(float(x), float(y))

    @property
    def x(self) -> float:
        """Returns the x-component."""
        return self._components[0]

    @property
    def y(self) -> float:
        """Returns the y-component."""
        return self._components[1]

    def cross(self, other: 'Vector2D') -> float:
        """
        Calculates the 2D cross product (magnitude of the 3D cross product's z-component).
        This is a scalar value: self.x * other.y - self.y * other.x.
        It's useful for determining orientation or signed area.

        Args:
            other: The other Vector2D object.

        Returns:
            The scalar result of the 2D cross product.
        """
        if not isinstance(other, Vector2D):
            raise TypeError("Cross product is defined for two Vector2D instances.")
        return self.x * other.y - self.y * other.x

    def perpendicular(self, clockwise: bool = False) -> 'Vector2D':
        """
        Returns a 2D vector perpendicular to this one.
        By default, returns the counter-clockwise perpendicular vector (-y, x).

        Args:
            clockwise: If True, returns the clockwise perpendicular vector (y, -x).

        Returns:
            A new Vector2D perpendicular to this one.
        """
        if clockwise:
            return Vector2D(self.y, -self.x)
        return Vector2D(-self.y, self.x)

    def angle(self) -> float:
        """
        Calculates the angle of the vector with respect to the positive x-axis.
        The angle is in radians, in the range (-pi, pi].
        """
        return math.atan2(self.y, self.x)


class Vector3D(Vector[float]):
    """Represents a vector in 3D space."""

    def __init__(self, x: float, y: float, z: float):
        """
        Initializes a 3D vector.

        Args:
            x: The x-component.
            y: The y-component.
            z: The z-component.
        """
        super().__init__(float(x), float(y), float(z))

    @property
    def x(self) -> float:
        """Returns the x-component."""
        return self._components[0]

    @property
    def y(self) -> float:
        """Returns the y-component."""
        return self._components[1]

    @property
    def z(self) -> float:
        """Returns the z-component."""
        return self._components[2]

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """
        Calculates the 3D cross product with another vector.

        Args:
            other: The other Vector3D object.

        Returns:
            A new Vector3D representing the cross product.
        """
        if not isinstance(other, Vector3D):
            raise TypeError("3D Cross product is defined for two Vector3D instances.")
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    