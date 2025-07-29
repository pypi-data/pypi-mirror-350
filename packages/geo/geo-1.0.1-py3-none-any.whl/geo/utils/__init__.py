# geo/utils/__init__.py

"""
Utilities sub-package for the geometry library.

Contains helper functions for validation, I/O, and other miscellaneous tasks
that are not core geometric primitives or operations but support the library.
"""

from .validators import (
    validate_non_negative,
    validate_positive,
    validate_list_of_points,
    validate_polygon_vertices,
)

from .io import (
    parse_points_from_string,
    format_point_to_string,
    save_polyhedron_to_obj_simple,
    load_polyhedron_from_obj_simple,
    save_polygon2d_to_csv,
    load_polygon2d_from_csv,
    save_polygon2d_to_json,
    load_polygon2d_from_json,
)

__all__ = [
    # Validators
    'validate_non_negative',
    'validate_positive',
    'validate_list_of_points',
    'validate_polygon_vertices',

    # I/O
    'parse_points_from_string',
    'format_point_to_string',
    'save_polyhedron_to_obj_simple',
    'load_polyhedron_from_obj_simple',
    'save_polygon2d_to_csv',
    'load_polygon2d_from_csv',
    'save_polygon2d_to_json',
    'load_polygon2d_from_json',
]