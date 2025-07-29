# geo/core/precision.py

"""
Handles floating-point precision issues common in geometric calculations.

Provides a default epsilon value and functions for comparing floating-point numbers with a tolerance.
"""

import math

DEFAULT_EPSILON = 1e-9  # Default tolerance for floating point comparisons

def is_equal(a: float, b: float, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if two floating-point numbers are equal within a specified tolerance.

    Args:
        a: The first float.
        b: The second float.
        epsilon: The tolerance. Defaults to DEFAULT_EPSILON.

    Returns:
        True if the absolute difference between a and b is less than epsilon, False otherwise.
    """
    return math.fabs(a - b) < epsilon

def is_zero(a: float, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a floating-point number is close enough to zero.

    Args:
        a: The float to check.
        epsilon: The tolerance. Defaults to DEFAULT_EPSILON.

    Returns:
        True if the absolute value of a is less than epsilon, False otherwise.
    """
    return math.fabs(a) < epsilon

def is_positive(a: float, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a floating-point number is definitively positive (greater than epsilon).

    Args:
        a: The float to check.
        epsilon: The tolerance. Defaults to DEFAULT_EPSILON.

    Returns:
        True if a is greater than epsilon, False otherwise.
    """
    return a > epsilon

def is_negative(a: float, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a floating-point number is definitively negative (less than -epsilon).

    Args:
        a: The float to check.
        epsilon: The tolerance. Defaults to DEFAULT_EPSILON.

    Returns:
        True if a is less than -epsilon, False otherwise.
    """
    return a < -epsilon