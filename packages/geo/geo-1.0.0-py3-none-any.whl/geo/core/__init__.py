# geo/core/__init__.py

"""
Core module for the geo package.
This module aggregates the fundamental classes and functions from its submodules, making them easily accessible from the 'core' namespace.
"""

# Import from precision first as other modules might depend on it
from .precision import (
    DEFAULT_EPSILON,
    is_equal,
    is_zero,
    is_positive,
    is_negative
)

# Import Point classes
from .point import (
    Point,
    Point2D,
    Point3D
)

# Import Vector classes
from .vector import (
    Vector,
    Vector2D,
    Vector3D
)

# Import Transformation functions/classes
from .transform import (
    translate,
    rotate_2d,
    rotate_3d,
    scale
)


__all__ = [
    # From precision.py
    'DEFAULT_EPSILON',
    'is_equal',
    'is_zero',
    'is_positive',
    'is_negative',

    # From point.py
    'Point',
    'Point2D',
    'Point3D',

    # From vector.py
    'Vector',
    'Vector2D',
    'Vector3D',

    # From transform.py
    'translate',
    'rotate_2d',
    'rotate_3d',
    'scale',
]

# Ensure that the __all__ list is complete
for module in __all__:
    if module not in globals():
        raise ImportError(f"Module {module} is not imported in __init__.py")