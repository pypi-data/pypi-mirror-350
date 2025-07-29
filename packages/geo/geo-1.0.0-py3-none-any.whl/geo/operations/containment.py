# geo/operations/containment.py

"""
Functions for 2D and 3D containment checks.
Many basic containment checks are methods of the primitive classes.
This module can house more complex checks or those involving multiple entities.
"""
from typing import List

from geo.core import Point2D, Vector2D, Point3D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from geo.primitives_2d import Polygon, Segment2D, Line2D
from geo.primitives_3d import Polyhedron, Plane as Plane3D
from .intersections_2d import segment_segment_intersection_detail  # For polygon simplicity check


def check_point_left_of_line(point: Point2D, line_p1: Point2D, line_p2: Point2D) -> float:
    """
    Returns > 0 if `point` is left of the directed line from line_p1 to line_p2,
    < 0 if right, and 0 if collinear.
    """
    return (line_p2.x - line_p1.x) * (point.y - line_p1.y) - (line_p2.y - line_p1.y) * (point.x - line_p1.x)


def is_polygon_simple(polygon: Polygon, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a polygon is simple (i.e., edges do not intersect except at shared vertices).
    """
    num_edges = len(polygon.edges)
    if num_edges < 3:
        return True  # Polygon with fewer than 3 edges trivially simple

    edges = polygon.edges

    for i in range(num_edges):
        edge1 = edges[i]
        for j in range(i + 1, num_edges):
            edge2 = edges[j]

            # Check adjacency: edges sharing exactly one vertex and consecutive in order
            is_adjacent = False
            # Shared vertices between edge1=(v_i, v_i+1), edge2=(v_j, v_j+1)
            shared_vertices = {
                polygon.vertices[i],
                polygon.vertices[(i + 1) % num_edges]
            } & {
                polygon.vertices[j],
                polygon.vertices[(j + 1) % num_edges]
            }
            if len(shared_vertices) == 1:
                # Adjacent if edges are consecutive in polygon indexing or first and last edge
                if j == (i + 1) % num_edges or (i == 0 and j == num_edges - 1):
                    is_adjacent = True

            intersection_type, intersect_data = segment_segment_intersection_detail(edge1, edge2, epsilon)

            if is_adjacent:
                if intersection_type == "point":
                    pt = intersect_data
                    assert isinstance(pt, Point2D)
                    # Intersection point must be the shared vertex
                    shared_vertex = next(iter(shared_vertices))
                    if not pt == shared_vertex:
                        # Adjacent edges intersecting at a point other than shared vertex means not simple
                        return False
                elif intersection_type == "overlap":
                    # Adjacent edges overlapping means degenerate polygon
                    return False
                # "none" or "collinear_no_overlap" is okay for adjacent edges
            else:
                # Non-adjacent edges must not intersect or overlap
                if intersection_type in ("point", "overlap"):
                    return False

    return True


def point_on_polygon_boundary(point: Point2D, polygon: Polygon, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Returns True if point lies exactly on any edge of the polygon.
    """
    if polygon.num_vertices < 2:
        return False

    for edge in polygon.edges:
        if edge.contains_point(point, epsilon):
            return True
    return False


def point_in_convex_polygon_2d(point: Point2D, polygon: Polygon, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a point is inside or on the boundary of a convex polygon.
    Assumes vertices are ordered CCW.

    The point must be left of or on every directed edge.
    """
    if polygon.num_vertices < 3:
        return False  # Not a valid polygon for containment

    if point_on_polygon_boundary(point, polygon, epsilon):
        return True

    for i in range(polygon.num_vertices):
        p1 = polygon.vertices[i]
        p2 = polygon.vertices[(i + 1) % polygon.num_vertices]

        cross_val = check_point_left_of_line(point, p1, p2)
        if cross_val < -epsilon:  # Point is to the right of an edge (outside)
            return False

    return True


def point_in_polyhedron_convex(point: Point3D, polyhedron: Polyhedron, epsilon: float = DEFAULT_EPSILON) -> bool:
    """
    Checks if a point is inside or on the boundary of a convex polyhedron.

    The point must lie on the non-positive side of all face planes (normals point outward).
    """
    if polyhedron.num_faces == 0:
        return False

    for i in range(polyhedron.num_faces):
        face_points = polyhedron.get_face_points(i)
        if len(face_points) < 3:
            continue  # Skip degenerate faces

        face_normal = polyhedron.get_face_normal(i)
        if face_normal.is_zero_vector():
            # Degenerate face normal, skip or handle separately
            continue

        plane_of_face = Plane3D(face_points[0], face_normal)
        signed_dist = plane_of_face.signed_distance_to_point(point)
        if signed_dist > epsilon:  # Outside face plane
            return False

    return True
