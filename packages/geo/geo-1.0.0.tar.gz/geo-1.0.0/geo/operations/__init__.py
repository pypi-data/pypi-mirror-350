# geo/operations/__init__.py

"""
Operations module for the geometry package.

This module provides functions for various geometric operations and algorithms,
such as intersection detection, measurements, containment checks, etc.
"""

from .intersections_2d import (
    IntersectionType,
    segment_segment_intersection_detail,
    line_polygon_intersections,
    segment_contains_point_collinear,
    segment_circle_intersections,
)
from .measurements import (
    closest_point_on_segment_to_point,
    distance_segment_segment_2d,
    closest_points_segments_2d,
    signed_angle_between_vectors_2d,
    distance_point_line_3d,
    distance_point_plane,
    distance_line_line_3d,
)
from .containment import (
    check_point_left_of_line,
    is_polygon_simple,
    point_on_polygon_boundary,
    point_in_convex_polygon_2d,
    point_in_polyhedron_convex,
)
from .intersections_3d import (
    sphere_sphere_intersection,
    plane_plane_intersection,
    line_triangle_intersection_moller_trumbore,
    SphereSphereIntersectionResult,
    AABB,
)
from .convex_hull import (
    convex_hull_2d_monotone_chain,
    convex_hull_3d,
    plot_convex_hull_2d,
    plot_convex_hull_3d,
)
from .triangulation import (
    triangulate_simple_polygon_ear_clipping,
    delaunay_triangulation_points_2d,
    constrained_delaunay_triangulation,
    tetrahedralise,

)
from .boolean_ops import (
    # Placeholders or stubs for boolean operations
    clip_polygon_sutherland_hodgman, # Example of a specific clipping
    polygon_union,
    polygon_intersection,
    polygon_difference,
    polyhedron_union,
    polyhedron_intersection,
    polyhedron_difference,
)


__all__ = [
    # From intersections_2d.py
    'IntersectionType',
    'segment_segment_intersection_detail',
    'line_polygon_intersections',
    'segment_contains_point_collinear',
    'segment_circle_intersections',

    # From measurements.py
    'closest_point_on_segment_to_point',
    'distance_segment_segment_2d',
    'closest_points_segments_2d',
    'signed_angle_between_vectors_2d',
    'distance_point_line_3d',
    'distance_point_plane',
    'distance_line_line_3d',

    # From containment.py
    'check_point_left_of_line',
    'is_polygon_simple',
    'point_on_polygon_boundary',
    'point_in_convex_polygon_2d',
    'point_in_polyhedron_convex',

    # From intersections_3d.py
    'sphere_sphere_intersection',
    'plane_plane_intersection',
    'line_triangle_intersection_moller_trumbore',
    'SphereSphereIntersectionResult',
    'AABB',

    # From convex_hull.py
    'convex_hull_2d_monotone_chain',
    'convex_hull_3d',
    'plot_convex_hull_2d',
    'plot_convex_hull_3d',

    # From triangulation.py
    'triangulate_simple_polygon_ear_clipping',
    'delaunay_triangulation_points_2d',
    'constrained_delaunay_triangulation',
    'tetrahedralise',

    # From boolean_ops.py
    'clip_polygon_sutherland_hodgman',
    'polygon_union',
    'polygon_intersection',
    'polygon_difference',
    'polyhedron_union',
    'polyhedron_intersection',
    'polyhedron_difference',
]