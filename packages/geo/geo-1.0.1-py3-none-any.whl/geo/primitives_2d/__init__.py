# geo/primitives_2d/__init__.py

"""
Primitives_2D module for the geometry package.

This module provides classes for various 2D geometric primitives.
"""

from .line import Line2D, Segment2D, Ray2D
from .circle import Circle
from .ellipse import Ellipse
from .polygon import Polygon
from .triangle import Triangle
from .rectangle import Rectangle
from .curve.base import Curve2D # Base class for curves
from .curve.bezier import BezierCurve
from .curve.spline import SplineCurve

__all__ = [
    'Line2D',
    'Segment2D',
    'Ray2D',
    'Circle',
    'Ellipse',
    'Polygon',
    'Triangle',
    'Rectangle',
    'Curve2D',
    'BezierCurve',
    'SplineCurve',
]