# geo/primitives_2d/curve/base.py

"""
Defines a base class for 2D curves in a parametric form C(t), typically with t ∈ [0, 1].
"""
from abc import ABC, abstractmethod
from typing import List, Sequence, Iterator

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal


class Curve2D(ABC):
    """
    Abstract base class for a 2D parametric curve.
    A curve is typically defined by C(t), where t is a parameter in [0, 1].
    """
    def __init__(self, control_points: Sequence[Point2D]):
        if not control_points:
            raise ValueError("A curve must have at least one control point.")
        for i, pt in enumerate(control_points):
            if not isinstance(pt, Point2D):
                raise TypeError(f"Expected Point2D at index {i}, got {type(pt).__name__}.")
        self.control_points: tuple[Point2D, ...] = tuple(control_points)

    @abstractmethod
    def point_at(self, t: float) -> Point2D:
        """
        Calculates the point on the curve at parameter t.
        Args:
            t (float): The parameter (typically in the range [0, 1]).
        Returns:
            Point2D: The point on the curve.
        """
        pass

    @abstractmethod
    def tangent_at(self, t: float) -> Vector2D:
        """
        Calculates the (non-normalized) tangent vector to the curve at parameter t.
        If the tangent is undefined (e.g., cusp), a zero vector or exception may be returned/raised.

        Args:
            t (float): The parameter.

        Returns:
            Vector2D: The tangent vector.
        """
        pass

    def derivative_at(self, t: float) -> Vector2D:
        """
        Alias for tangent_at, representing the first derivative C'(t).
        """
        return self.tangent_at(t)

    def length(self, t0: float = 0.0, t1: float = 1.0, num_segments: int = 100) -> float:
        """
        Approximates the curve length from t0 to t1 using numerical integration.

        Args:
            t0 (float): Starting parameter.
            t1 (float): Ending parameter.
            num_segments (int): Number of segments for numerical approximation.

        Returns:
            float: Approximate curve length.

        Raises:
            ValueError: If num_segments is not positive.
        """
        if is_equal(t0, t1):
            return 0.0
        if num_segments <= 0:
            raise ValueError("Number of segments must be positive for length calculation.")

        # Ensure t0 <= t1
        if t0 > t1:
            t0, t1 = t1, t0

        total_length = 0.0
        dt = (t1 - t0) / num_segments
        prev_point = self.point_at(t0)

        for i in range(1, num_segments + 1):
            current_t = t0 + i * dt
            current_point = self.point_at(current_t)
            total_length += prev_point.distance_to(current_point)
            prev_point = current_point
        
        return total_length

    def __len__(self) -> int:
        """
        Returns the number of control points.
        """
        return len(self.control_points)

    def __iter__(self) -> Iterator[Point2D]:
        """
        Allows iteration over control points.
        """
        return iter(self.control_points)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(control_points={self.control_points})"