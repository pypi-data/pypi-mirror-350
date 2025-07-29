"""
Functions for polygon triangulation and other forms of triangulation.
"""
from typing import List, Sequence, Tuple

from geo.core import Point2D, Point3D, Vector2D
from geo.core.precision import is_zero, DEFAULT_EPSILON
from geo.primitives_2d import Polygon, Triangle
from .containment import check_point_left_of_line


def triangulate_simple_polygon_ear_clipping(polygon: Polygon, ensure_ccw: bool = True) -> List[Triangle]:
    """
    Triangulates a simple 2D polygon using the Ear Clipping (Ear Cutting) method.
    Assumes the polygon is simple (no self-intersections).
    Vertices should be ordered (e.g., counter-clockwise for this implementation).

    Args:
        polygon: The simple Polygon to triangulate.
        ensure_ccw: If True, ensures polygon vertices are CCW. If False, assumes they are.

    Returns:
        A list of Triangle objects that form the triangulation.
        Returns empty list if polygon has < 3 vertices or is degenerate.
    """
    if polygon.num_vertices < 3:
        return []

    original_vertices = list(polygon.vertices)

    if ensure_ccw:
        signed_area = polygon.signed_area()
        if is_zero(signed_area):
            return []  # Degenerate (collinear)
        if signed_area < 0:  # Clockwise
            original_vertices.reverse()

    remaining_indices = list(range(len(original_vertices)))
    triangles: List[Triangle] = []

    num_remaining = len(remaining_indices)
    current_iteration = 0
    max_iterations = num_remaining * num_remaining  # Heuristic to avoid infinite loops

    while num_remaining > 2 and current_iteration < max_iterations:
        found_ear = False
        for i in range(num_remaining):
            idx_prev = remaining_indices[(i - 1) % num_remaining]
            idx_curr = remaining_indices[i]
            idx_next = remaining_indices[(i + 1) % num_remaining]

            p_prev = original_vertices[idx_prev]
            p_curr = original_vertices[idx_curr]
            p_next = original_vertices[idx_next]

            # Check convexity: cross product > epsilon means convex vertex for CCW polygon
            v_prev_curr = p_curr - p_prev
            v_curr_next = p_next - p_curr
            cross_product_z = v_prev_curr.x * v_curr_next.y - v_prev_curr.y * v_curr_next.x

            if cross_product_z <= DEFAULT_EPSILON:
                continue  # Not a convex vertex or collinear

            # Check if any other vertex lies inside the ear triangle
            is_ear = True
            for j in range(num_remaining):
                idx_other = remaining_indices[j]
                if idx_other in (idx_prev, idx_curr, idx_next):
                    continue
                p_other = original_vertices[idx_other]

                # Check if point p_other lies inside or on boundary of triangle
                # Using left-of-line tests
                if (
                    check_point_left_of_line(p_other, p_prev, p_curr) < -DEFAULT_EPSILON or
                    check_point_left_of_line(p_other, p_curr, p_next) < -DEFAULT_EPSILON or
                    check_point_left_of_line(p_other, p_next, p_prev) < -DEFAULT_EPSILON
                ):
                    continue  # Outside or on right side of at least one edge

                # p_other is inside or on boundary => not an ear
                is_ear = False
                break

            if is_ear:
                triangles.append(Triangle(p_prev, p_curr, p_next))
                remaining_indices.pop(i)
                num_remaining -= 1
                found_ear = True
                break  # Restart scan

        current_iteration += 1
        if not found_ear and num_remaining > 2:
            # Could not find an ear - polygon might be non-simple or numerical issues
            break

    # If original polygon was a triangle and no triangles were added, add it
    if len(original_vertices) == 3 and not triangles and not is_zero(Polygon(original_vertices).signed_area()):
        triangles.append(Triangle(*original_vertices))

    return triangles


def delaunay_triangulation_points_2d(points: Sequence[Point2D]) -> List[Triangle]:
    """
    Computes the Delaunay triangulation of a set of 2D points.

    Args:
        points: Sequence of Point2D objects.

    Returns:
        List of Triangle objects forming the Delaunay triangulation.

    Raises:
        ValueError if fewer than 3 points are provided.
    """
    from scipy.spatial import Delaunay

    if len(points) < 3:
        raise ValueError("At least 3 points are required for Delaunay triangulation.")

    coords = [(p.x, p.y) for p in points]
    delaunay = Delaunay(coords)

    triangles = []
    for simplex in delaunay.simplices:
        tri = Triangle(points[simplex[0]], points[simplex[1]], points[simplex[2]])
        triangles.append(tri)

    return triangles


def constrained_delaunay_triangulation(polygon: Polygon) -> List[Triangle]:
    """
    Placeholder for Constrained Delaunay Triangulation that preserves polygon edges.
    Not implemented.

    Args:
        polygon: Polygon to triangulate.

    Raises:
        NotImplementedError
    """
    raise NotImplementedError("Constrained Delaunay Triangulation not implemented.")


def tetrahedralise(points: Sequence[Point3D]) -> List[Tuple[Point3D, Point3D, Point3D, Point3D]]:
    """
    Computes the 3D Delaunay tetrahedralization of a set of 3D points.

    Args:
        points: Sequence of Point3D objects.

    Returns:
        List of tetrahedra, each represented by a tuple of four Point3D vertices.

    Raises:
        ValueError if fewer than 4 points are provided.
    """
    from scipy.spatial import Delaunay

    if len(points) < 4:
        raise ValueError("At least 4 points are required for 3D tetrahedralization.")

    coords = [(p.x, p.y, p.z) for p in points]
    delaunay = Delaunay(coords)

    tetrahedra = []
    for simplex in delaunay.simplices:
        tetra = tuple(points[i] for i in simplex)
        tetrahedra.append(tetra)

    return tetrahedra
