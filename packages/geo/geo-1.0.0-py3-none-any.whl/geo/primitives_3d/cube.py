# geo/primitives_3d/cube.py

"""
Defines a Cube primitive in 3D space.
Supports both axis-aligned and non-axis-aligned cubes.
A cube is a specific type of Polyhedron (hexahedron).
"""

import math
from typing import List, Optional

from geo.core import Point3D, Vector3D
from .polyhedra import Polyhedron  # To potentially represent it as a Polyhedron

class Cube:
    """
    Represents a cube in 3D space.

    - Axis-aligned cube defined by center and side_length.
    - Optionally, a rotation matrix (3 orthonormal Vector3D axes) can define
      a non-axis-aligned cube (oriented cube).
    """

    def __init__(
        self,
        center: Point3D,
        side_length: float,
        axes: Optional[List[Vector3D]] = None,
    ):
        """
        Initializes a Cube.

        Args:
            center: The center Point3D of the cube.
            side_length: The length of each side of the cube. Must be positive.
            axes: Optional list of 3 orthonormal Vector3D axes defining the cube orientation.
                  If None, cube is axis-aligned with standard axes (x,y,z).

        Raises:
            ValueError: If side_length is non-positive or axes are invalid.
        """
        if side_length <= 0:
            raise ValueError("Cube side length must be positive.")
        self.center = center
        self.side_length = side_length
        self.half_side = side_length / 2.0

        if axes is not None:
            if len(axes) != 3:
                raise ValueError("Axes must be a list of 3 Vector3D objects.")
            # Check orthonormality: each axis unit length and perpendicular
            for i in range(3):
                if not math.isclose(axes[i].magnitude(), 1.0, abs_tol=1e-9):
                    raise ValueError("Axes must be unit vectors.")
                for j in range(i + 1, 3):
                    if not math.isclose(axes[i].dot(axes[j]), 0.0, abs_tol=1e-9):
                        raise ValueError("Axes must be mutually perpendicular.")
            self.axes = axes
        else:
            # Default to standard x,y,z axes unit vectors
            self.axes = [
                Vector3D(1, 0, 0),
                Vector3D(0, 1, 0),
                Vector3D(0, 0, 1),
            ]

        # Compute vertices once for convenience
        self._vertices = self._compute_vertices()

    def __repr__(self) -> str:
        return f"Cube(center={self.center}, side_length={self.side_length}, axes={self.axes})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cube):
            return False
        if not self.center == other.center:
            return False
        if not math.isclose(self.side_length, other.side_length, abs_tol=1e-9):
            return False
        # Compare axes component-wise with tolerance
        for a1, a2 in zip(self.axes, other.axes):
            for c1, c2 in zip((a1.x, a1.y, a1.z), (a2.x, a2.y, a2.z)):
                if not math.isclose(c1, c2, abs_tol=1e-9):
                    return False
        return True

    @property
    def volume(self) -> float:
        """Calculates the volume of the cube."""
        return self.side_length ** 3

    @property
    def surface_area(self) -> float:
        """Calculates the surface area of the cube."""
        return 6 * (self.side_length ** 2)

    def _compute_vertices(self) -> List[Point3D]:
        """
        Computes the 8 vertices of the cube based on center, half_side, and axes.

        Vertices are calculated by starting from the center and adding or subtracting half_side
        times each axis vector to reach corners.
        """
        hs = self.half_side
        c = self.center
        ax, ay, az = self.axes

        # Each vertex corresponds to one combination of +/- half_side on each axis
        vertices = []
        for dx in (-hs, hs):
            for dy in (-hs, hs):
                for dz in (-hs, hs):
                    offset = (ax * dx) + (ay * dy) + (az * dz)
                    vertex = c + offset
                    vertices.append(vertex)
        return vertices

    @property
    def vertices(self) -> List[Point3D]:
        """Returns the precomputed vertices."""
        return self._vertices

    @property
    def faces_as_vertex_indices(self) -> List[List[int]]:
        """
        Returns the 6 faces of the cube, each as a list of vertex indices.
        Vertices are ordered CCW when viewed from outside.
        Vertex order in self.vertices is:
            index = (dx_index * 4) + (dy_index * 2) + dz_index
            with dx, dy, dz in (-hs, hs) ordering

        The cube is built as a rectangular parallelepiped, but the order is consistent.
        """
        # The 8 vertices are ordered as:
        # 0: (-,-,-), 1: (-,-,+), 2: (-,+,-), 3: (-,+,+),
        # 4: (+,-,-), 5: (+,-,+), 6: (+,+,-), 7: (+,+,+)
        # But our code above generates in nested loops dx,dy,dz which is different order:
        # We'll reorder vertices to standard:
        # From our _compute_vertices order (dx, dy, dz):
        # Index in nested loops: 0..7 with dx varies slowest, dz fastest:
        # Actually, our loop is dx in (-hs,hs), dy in (-hs,hs), dz in (-hs,hs)
        # So order generated is:
        # 0:(-,-,-), 1:(-,-,+), 2:(-,+,-), 3:(-,+,+), 4:(+,-,-), 5:(+,-,+), 6:(+,+,-), 7:(+,+,+)
        # Which matches above.

        return [
            [0, 4, 6, 2],  # Left face (-x)
            [1, 3, 7, 5],  # Right face (+x)
            [0, 1, 5, 4],  # Bottom face (-y)
            [2, 6, 7, 3],  # Top face (+y)
            [0, 2, 3, 1],  # Back face (-z)
            [4, 5, 7, 6],  # Front face (+z)
        ]

    def to_polyhedron(self) -> Polyhedron:
        """Converts this Cube to a Polyhedron object."""
        return Polyhedron(self.vertices, self.faces_as_vertex_indices)

    def contains_point(self, point: Point3D, epsilon: float = 1e-9) -> bool:
        """
        Checks if a point is inside or on the boundary of the cube.

        For axis-aligned cubes (default axes), this is a simple bounding box check.

        For oriented cubes, transform point into cube's local axes coords,
        then check if within [-half_side, half_side] along each axis.
        """
        # Vector from center to point
        vec = point - self.center

        # Project vector onto each axis
        for axis in self.axes:
            dist = vec.dot(axis)
            if dist < -self.half_side - epsilon or dist > self.half_side + epsilon:
                return False
        return True
