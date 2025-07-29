# tests/conftest.py
# `pytest` to run

"""
Pytest configuration for the geo project.
Provides common fixtures and test setup.
"""

import sys
import os
import pytest
import math

# Ensure the project root (directory containing the 'geo' package) is in sys.path
# Assuming conftest.py is in the 'tests/' directory, which is a subdirectory of the project root.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now that sys.path is configured, we can import from the 'geo' package
from geo.core import (
    Point2D, Point3D,
    Vector2D, Vector3D,
    DEFAULT_EPSILON as CORE_DEFAULT_EPSILON # Import the original default
)
from geo.primitives_2d import (
    Polygon as Polygon2D,
    Triangle as Triangle2D,
    Rectangle as Rectangle2D,
    Circle as Circle2D,
    Segment2D,
    Line2D,
    Ray2D
)
from geo.primitives_3d import (
    Polyhedron,
    Cube,
    Sphere,
    Plane as Plane3D, # Alias to avoid potential name clashes
    Line3D,
    Segment3D,
    Ray3D,
    Cylinder,
    Cone
)
from geo.core import precision as geo_precision_module # For monkeypatching

# --- Core Fixtures ---

@pytest.fixture(scope="session")
def default_test_epsilon() -> float:
    """Provides a consistent epsilon value for tests (1e-8)."""
    return 1e-8

@pytest.fixture(autouse=True)
def set_custom_default_epsilon_for_geo_module(monkeypatch, default_test_epsilon: float):
    """
    Sets the geo.core.precision.DEFAULT_EPSILON to a custom value (1e-8)
    for the duration of each test function.
    This ensures that internal calculations within the geo package use this
    epsilon if they rely on the global DEFAULT_EPSILON.
    """
    original_epsilon = geo_precision_module.DEFAULT_EPSILON
    monkeypatch.setattr(geo_precision_module, "DEFAULT_EPSILON", default_test_epsilon)
    yield # Test runs with the patched epsilon
    # Restore original epsilon after test (though monkeypatch handles this for its scope)
    monkeypatch.setattr(geo_precision_module, "DEFAULT_EPSILON", original_epsilon)


@pytest.fixture
def p2d_origin() -> Point2D:
    """A 2D point at the origin (0,0)."""
    return Point2D(0.0, 0.0)

@pytest.fixture
def p2d_one_one() -> Point2D:
    """A 2D point at (1,1)."""
    return Point2D(1.0, 1.0)

@pytest.fixture
def p2d_generic() -> Point2D:
    """A generic 2D point (3,4)."""
    return Point2D(3.0, 4.0)

@pytest.fixture
def p3d_origin() -> Point3D:
    """A 3D point at the origin (0,0,0)."""
    return Point3D(0.0, 0.0, 0.0)

@pytest.fixture
def p3d_one_one_one() -> Point3D:
    """A 3D point at (1,1,1)."""
    return Point3D(1.0, 1.0, 1.0)

@pytest.fixture
def p3d_generic() -> Point3D:
    """A generic 3D point (1,2,3)."""
    return Point3D(1.0, 2.0, 3.0)

@pytest.fixture
def v2d_zero() -> Vector2D:
    """A 2D zero vector (0,0)."""
    return Vector2D(0.0, 0.0)

@pytest.fixture
def v2d_i() -> Vector2D:
    """A 2D unit vector along the x-axis (1,0)."""
    return Vector2D(1.0, 0.0)

@pytest.fixture
def v2d_j() -> Vector2D:
    """A 2D unit vector along the y-axis (0,1)."""
    return Vector2D(0.0, 1.0)

@pytest.fixture
def v3d_zero() -> Vector3D:
    """A 3D zero vector (0,0,0)."""
    return Vector3D(0.0, 0.0, 0.0)

@pytest.fixture
def v3d_i() -> Vector3D:
    """A 3D unit vector along the x-axis (1,0,0)."""
    return Vector3D(1.0, 0.0, 0.0)

@pytest.fixture
def v3d_j() -> Vector3D:
    """A 3D unit vector along the y-axis (0,1,0)."""
    return Vector3D(0.0, 1.0, 0.0)

@pytest.fixture
def v3d_k() -> Vector3D:
    """A 3D unit vector along the z-axis (0,0,1)."""
    return Vector3D(0.0, 0.0, 1.0)


# --- 2D Primitives Fixtures ---

@pytest.fixture
def unit_square_polygon_2d(p2d_origin: Point2D) -> Polygon2D:
    """A unit square Polygon2D with bottom-left at origin, CCW vertices."""
    return Polygon2D([
        p2d_origin,
        Point2D(1.0, 0.0),
        Point2D(1.0, 1.0),
        Point2D(0.0, 1.0)
    ])

@pytest.fixture
def simple_triangle_2d() -> Triangle2D:
    """A simple Triangle2D: (0,0), (1,0), (0,1)."""
    return Triangle2D(Point2D(0,0), Point2D(1,0), Point2D(0,1))

@pytest.fixture
def unit_circle_2d_at_origin(p2d_origin: Point2D) -> Circle2D:
    """A unit Circle2D centered at the origin."""
    return Circle2D(center=p2d_origin, radius=1.0)

@pytest.fixture
def segment_2d_horizontal(p2d_origin: Point2D) -> Segment2D:
    """A horizontal Segment2D from (0,0) to (5,0)."""
    return Segment2D(p2d_origin, Point2D(5.0, 0.0))

@pytest.fixture
def line_2d_xaxis(p2d_origin: Point2D, v2d_i: Vector2D) -> Line2D:
    """A Line2D representing the x-axis."""
    return Line2D(p2d_origin, v2d_i)

@pytest.fixture
def ray_2d_positive_x(p2d_origin: Point2D, v2d_i: Vector2D) -> Ray2D:
    """A Ray2D starting at origin along the positive x-axis."""
    return Ray2D(p2d_origin, v2d_i)


# --- 3D Primitives Fixtures ---

@pytest.fixture
def unit_cube_vertices_faces() -> tuple[list[Point3D], list[list[int]]]:
    """Provides vertices and quad faces for a unit cube [0,0,0]-[1,1,1]."""
    vertices = [
        Point3D(0.0, 0.0, 0.0),  # 0
        Point3D(1.0, 0.0, 0.0),  # 1
        Point3D(1.0, 1.0, 0.0),  # 2
        Point3D(0.0, 1.0, 0.0),  # 3
        Point3D(0.0, 0.0, 1.0),  # 4
        Point3D(1.0, 0.0, 1.0),  # 5
        Point3D(1.0, 1.0, 1.0),  # 6
        Point3D(0.0, 1.0, 1.0)   # 7
    ]
    # Faces (quads), CCW when viewed from outside
    faces = [
        [0, 3, 2, 1],  # Bottom face (-Z)
        [4, 5, 6, 7],  # Top face (+Z)
        [0, 4, 7, 3],  # Left face (-X)
        [1, 2, 6, 5],  # Right face (+X)
        [0, 1, 5, 4],  # Back face (-Y)
        [3, 7, 6, 2]   # Front face (+Y)
    ]
    return vertices, faces

@pytest.fixture
def unit_cube_polyhedron(unit_cube_vertices_faces: tuple[list[Point3D], list[list[int]]]) -> Polyhedron:
    """A unit Polyhedron cube based on quad faces."""
    vertices, faces = unit_cube_vertices_faces
    return Polyhedron(vertices, faces)

@pytest.fixture
def unit_cube_polyhedron_triangulated(unit_cube_vertices_faces: tuple[list[Point3D], list[list[int]]]) -> Polyhedron:
    """A unit Polyhedron cube with triangulated faces."""
    vertices, _ = unit_cube_vertices_faces
    # Triangulated faces for a cube (12 triangles)
    # Each quad [v0, v1, v2, v3] becomes [v0, v1, v2] and [v0, v2, v3] (example triangulation)
    faces_tri = [
        [0,1,2], [0,2,3], # Bottom (-Z)
        [4,7,6], [4,6,5], # Top (+Z) (Reversed for CCW: [4,5,6], [4,6,7]) -> [4,5,6], [4,6,7]
        [0,3,7], [0,7,4], # Left (-X)
        [1,2,6], [1,6,5], # Right (+X)
        [0,4,5], [0,5,1], # Back (-Y)
        [3,2,6], [3,6,7]  # Front (+Y)
    ]
    # Let's use a more standard triangulation for the cube based on the quad faces:
    # Quad [a,b,c,d] -> Triangles [a,b,c], [a,c,d]
    quad_faces = [
        [0, 3, 2, 1], [4, 5, 6, 7], [0, 4, 7, 3],
        [1, 2, 6, 5], [0, 1, 5, 4], [3, 7, 6, 2]
    ]
    tri_faces_final = []
    for qf in quad_faces:
        tri_faces_final.append([qf[0], qf[1], qf[2]])
        tri_faces_final.append([qf[0], qf[2], qf[3]])

    return Polyhedron(vertices, tri_faces_final)


@pytest.fixture
def unit_cube_primitive() -> Cube:
    """A unit Cube primitive centered at (0.5,0.5,0.5) with side length 1."""
    return Cube(center=Point3D(0.5, 0.5, 0.5), side_length=1.0)

@pytest.fixture
def unit_sphere_at_origin(p3d_origin: Point3D) -> Sphere:
    """A unit Sphere centered at the origin."""
    return Sphere(center=p3d_origin, radius=1.0)

@pytest.fixture
def xy_plane_3d(p3d_origin: Point3D, v3d_k: Vector3D) -> Plane3D:
    """A Plane3D representing the XY plane (normal along Z-axis)."""
    return Plane3D(point_on_plane=p3d_origin, normal_or_p2=v3d_k)

@pytest.fixture
def line_3d_xaxis(p3d_origin: Point3D, v3d_i: Vector3D) -> Line3D:
    """A Line3D representing the X-axis."""
    return Line3D(origin=p3d_origin, direction_or_p2=v3d_i)

@pytest.fixture
def segment_3d_generic() -> Segment3D:
    """A generic Segment3D."""
    return Segment3D(Point3D(0,0,0), Point3D(1,2,3))

@pytest.fixture
def ray_3d_positive_z(p3d_origin: Point3D, v3d_k: Vector3D) -> Ray3D:
    """A Ray3D starting at origin along the positive Z-axis."""
    return Ray3D(origin=p3d_origin, direction=v3d_k)