# geo/utils/validators.py

"""
Input validation helper functions for the geometry package.
"""
from typing import Any, Sequence, Union, Type
from collections.abc import Sequence as ABCSequence
import numbers
import math

from geo.core import Point2D, Point3D


def validate_non_negative(value: Union[int, float], name: str = "Value") -> None:
    """
    Validates if a numeric value is non-negative.

    Args:
        value: The numeric value to check.
        name: The name of the value (for error messages).

    Raises:
        ValueError: If the value is negative.
        TypeError: If the value is not numeric.
    """
    if not isinstance(value, numbers.Real):
        raise TypeError(f"{name} must be a numeric value (int or float). Got {type(value)}.")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{name} cannot be NaN or infinite. Got {value}.")
    if value < 0:
        raise ValueError(f"{name} cannot be negative. Got {value}.")


def validate_positive(value: Union[int, float], name: str = "Value") -> None:
    """
    Validates if a numeric value is strictly positive.

    Args:
        value: The numeric value to check.
        name: The name of the value (for error messages).

    Raises:
        ValueError: If the value is not positive.
        TypeError: If the value is not numeric.
    """
    if not isinstance(value, numbers.Real):
        raise TypeError(f"{name} must be a numeric value (int or float). Got {type(value)}.")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{name} cannot be NaN or infinite. Got {value}.")
    if value <= 0:
        raise ValueError(f"{name} must be strictly positive. Got {value}.")


def validate_list_of_points(points: Sequence[Any], 
                            min_points: int = 0, 
                            point_type: Union[Type[Point2D], Type[Point3D], None] = None,
                            name: str = "Point list") -> None:
    """
    Validates if the input is a sequence of Point2D or Point3D objects.

    Args:
        points: The sequence to validate.
        min_points: Minimum number of points required in the sequence.
        point_type: Expected type of points (Point2D or Point3D). If None, allows either.
        name: Name of the list (for error messages).

    Raises:
        TypeError: If `points` is not a sequence or contains non-Point objects.
        ValueError: If the number of points is less than `min_points`.
    """
    if isinstance(points, str) or not isinstance(points, ABCSequence):
        raise TypeError(f"{name} must be a sequence (e.g., list or tuple), not a string or unrelated type. Got {type(points)}.")
    if len(points) < min_points:
        raise ValueError(f"{name} must contain at least {min_points} points. Got {len(points)}.")

    for i, p in enumerate(points):
        if point_type:
            if not isinstance(p, point_type):
                raise TypeError(
                    f"Element {i} in {name} must be a {point_type.__name__}. Got {type(p)}."
                )
        elif not isinstance(p, (Point2D, Point3D)):
            raise TypeError(
                f"Element {i} in {name} must be a Point2D or Point3D object. Got {type(p)}."
            )


def validate_polygon_vertices(vertices: Sequence[Any], 
                                point_type: Type[Point2D] = Point2D, 
                                name: str = "Polygon vertices") -> None:
    """
    Validates vertices for a Polygon. Specifically for 2D polygons.

    Args:
        vertices: Sequence of potential vertices.
        point_type: Expected type of point (default Point2D).
        name: Name for error messages.

    Raises:
        TypeError: If vertices is not a sequence or elements are not of point_type.
        ValueError: If fewer than 3 vertices are provided.
    """
    validate_list_of_points(vertices, min_points=3, point_type=point_type, name=name)
