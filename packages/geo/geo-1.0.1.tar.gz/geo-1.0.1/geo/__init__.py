# geo/__init__.py

"""
geo

A Python package for computational geometry.
Provides primitives, operations, and utilities for 2D and 3D geometric tasks.
"""

__version__ = "0.1.2"

# Import key classes and functions from submodules for easier access
# For example: from .core import Point2D, Vector3D
# This makes them available as: import geo
# then: geo.Point2D(...)

# From core module
from .core import (
    DEFAULT_EPSILON,
    is_equal,
    is_zero,
    is_positive,
    is_negative,
    Point, Point2D, Point3D,
    Vector, Vector2D, Vector3D,
    translate, rotate_2d, rotate_3d, scale
)

# From primitives_2d module
from .primitives_2d import (
    Line2D, Segment2D, Ray2D,
    Circle,
    Ellipse,
    Polygon,
    Triangle,
    Rectangle,
    Curve2D, # Base class for curves
    BezierCurve,
    SplineCurve,
)

# From primitives_3d module
from .primitives_3d import (
    Plane, # Renamed to avoid conflict with other 'Plane' if any, or use Plane3D
    Line3D, Segment3D, Ray3D,
    Circle3D, Sphere,
    Cube,
    Cylinder,
    Cone,
    Polyhedron,
)

# From operations module
# Import specific, commonly used operations. Users can also import from submodules directly.
from .operations import (
    # 2D Intersections
    IntersectionType,
    segment_segment_intersection_detail,
    line_polygon_intersections,
    segment_contains_point_collinear,
    segment_circle_intersections,

    # Measurements
    closest_point_on_segment_to_point,
    distance_segment_segment_2d,
    closest_points_segments_2d,
    signed_angle_between_vectors_2d,
    distance_point_line_3d,
    distance_point_plane,
    distance_line_line_3d,

    # Containment
    check_point_left_of_line,
    is_polygon_simple,
    point_on_polygon_boundary,
    point_in_convex_polygon_2d,
    point_in_polyhedron_convex,

    # 3D Intersections
    sphere_sphere_intersection,
    plane_plane_intersection,
    line_triangle_intersection_moller_trumbore,
    SphereSphereIntersectionResult,
    AABB,

    # Convex Hull
    convex_hull_2d_monotone_chain,
    convex_hull_3d,
    plot_convex_hull_2d,
    plot_convex_hull_3d,

    # Triangulation
    triangulate_simple_polygon_ear_clipping,
    delaunay_triangulation_points_2d,
    constrained_delaunay_triangulation,
    tetrahedralise,
    
    # Boolean Operations (example)
    clip_polygon_sutherland_hodgman,
    polygon_union,
    polygon_intersection,
    polygon_difference,
    polyhedron_union,
    polyhedron_intersection,
    polyhedron_difference,
)

# From utils module (if there are high-level utilities to expose)
from .utils import (
    validate_non_negative,
    validate_positive,
    validate_list_of_points,
    validate_polygon_vertices,
    parse_points_from_string,
    format_point_to_string,
    save_polyhedron_to_obj_simple,
    load_polyhedron_from_obj_simple,
    save_polygon2d_to_csv,
    load_polygon2d_from_csv,
)


# Define __all__ for `from geo import *`
# It's generally better for users to import specific items, but __all__ can be defined.
__all__ = [
    # Core
    'DEFAULT_EPSILON', 'is_equal', 'is_zero', 'is_positive', 'is_negative',
    'Point', 'Point2D', 'Point3D',
    'Vector', 'Vector2D', 'Vector3D',
    'translate', 'rotate_2d', 'rotate_3d', 'scale',

    # Primitives 2D
    'Line2D', 'Segment2D', 'Ray2D',
    'Circle', 'Ellipse', 'Polygon', 'Triangle', 'Rectangle',
    'Curve2D', 'BezierCurve', 'SplineCurve',

    # Primitives 3D
    'Plane', 'Line3D', 'Segment3D', 'Ray3D',
    'Circle3D', 'Sphere', 'Cube', 'Cylinder', 'Cone', 'Polyhedron',

    # Operations
    'IntersectionType', 'segment_segment_intersection_detail', 'line_polygon_intersections',
    'segment_contains_point_collinear', 'segment_circle_intersections',
    'closest_point_on_segment_to_point', 'distance_segment_segment_2d', 'closest_points_segments_2d',
    'signed_angle_between_vectors_2d', 'distance_point_line_3d',
    'distance_point_plane', 'distance_line_line_3d',
    'check_point_left_of_line', 'is_polygon_simple', 'point_on_polygon_boundary',
    'point_in_convex_polygon_2d', 'point_in_polyhedron_convex',
    'sphere_sphere_intersection', 'plane_plane_intersection',
    'line_triangle_intersection_moller_trumbore',
    'SphereSphereIntersectionResult', 'AABB',
    'convex_hull_2d_monotone_chain', 'convex_hull_3d', 
    'plot_convex_hull_2d', 'plot_convex_hull_3d',
    'triangulate_simple_polygon_ear_clipping', 'delaunay_triangulation_points_2d',
    'constrained_delaunay_triangulation', 'tetrahedralise',
    'clip_polygon_sutherland_hodgman', 'polygon_union',
    'polygon_intersection', 'polygon_difference',
    'polyhedron_union', 'polyhedron_intersection', 'polyhedron_difference',
    
    # Utils
    'validate_non_negative', 'validate_positive', 'validate_list_of_points',
    'validate_polygon_vertices',
    'parse_points_from_string', 'format_point_to_string',
    'save_polyhedron_to_obj_simple', 'load_polyhedron_from_obj_simple',
    'save_polygon2d_to_csv', 'load_polygon2d_from_csv',

    # Version
    '__version__',
]