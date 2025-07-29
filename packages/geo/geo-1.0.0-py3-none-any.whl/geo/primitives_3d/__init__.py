# geo/primitives_3d/__init__.py

"""
Primitives_3D module for the geometry package.

This module provides classes for various 3D geometric primitives.
"""

from .plane import Plane
from .line_3d import Line3D, Segment3D, Ray3D
from .sphere import Circle3D, Sphere
from .cube import Cube
from .cylinder import Cylinder
from .cone import Cone
from .polyhedra import Polyhedron # Basic Polyhedron class

__all__ = [
    'Plane',
    'Line3D',
    'Segment3D',
    'Ray3D',
    'Circle3D',
    'Sphere',
    'Cube',
    'Cylinder',
    'Cone',
    'Polyhedron',
]