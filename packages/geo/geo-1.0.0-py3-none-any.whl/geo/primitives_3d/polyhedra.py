# geo/primitives_3d/polyhedra.py

"""
Defines a base Polyhedron class and potentially common polyhedra types.
"""
import math
from typing import List, Sequence, Tuple

from geo.core import Point3D, Vector3D
from geo.core.precision import is_zero
from .plane import Plane

class Polyhedron:
    """
    Represents a polyhedron defined by a list of vertices and a list of faces.
    Each face is a list of indices referencing the vertices list.
    Vertices of a face are assumed to be ordered CCW when viewed from outside.
    """

    def __init__(self, vertices: Sequence[Point3D], faces: Sequence[Sequence[int]]):
        """
        Initializes a Polyhedron.

        Args:
            vertices: A sequence of Point3D objects.
            faces: A sequence of sequences of integers. Each inner sequence represents
                   a face, with integers being indices into the `vertices` list.
                   Example: [[0, 1, 2], [0, 2, 3]] for a tetrahedron with 4 vertices.

        Raises:
            ValueError: If face indices are out of bounds or faces are malformed.
        """
        self.vertices = tuple(vertices)

        # Validate faces
        validated_faces = []
        for i, face_indices in enumerate(faces):
            if len(face_indices) < 3:
                raise ValueError(f"Face {i} has fewer than 3 vertices: {face_indices}")
            for v_idx in face_indices:
                if not (0 <= v_idx < len(self.vertices)):
                    raise ValueError(
                        f"Vertex index {v_idx} in face {i} is out of bounds "
                        f"(num_vertices={len(self.vertices)})."
                    )
            validated_faces.append(tuple(face_indices))
        self.faces = list(validated_faces)

        # Ensure face winding is consistent and normals point outward,
        # assuming the origin (0,0,0) is inside the polyhedron.
        self._ensure_outward_normals()

    def _ensure_outward_normals(self):
        """
        Ensures all faces have outward-pointing normals by
        checking if the normal points toward the origin. If so,
        the vertex order is reversed.
        """
        origin = Point3D(0, 0, 0)
        for i, face_indices in enumerate(self.faces):
            pts = [self.vertices[idx] for idx in face_indices]
            # Compute normal
            v1 = pts[1] - pts[0]
            v2 = pts[2] - pts[0]
            normal = v1.cross(v2).normalize()
            # Vector from a face point to origin
            vec_to_origin = origin - pts[0]
            # If normal points inward (dot product positive), reverse order
            if normal.dot(vec_to_origin) > 0:
                self.faces[i] = tuple(reversed(face_indices))

    def __repr__(self) -> str:
        return f"Polyhedron(num_vertices={len(self.vertices)}, num_faces={len(self.faces)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polyhedron):
            return False
        if len(self.vertices) != len(other.vertices) or len(self.faces) != len(other.faces):
            return False
        # Basic equality: does not handle isomorphism or reordering
        return self.vertices == other.vertices and self.faces == other.faces

    @property
    def num_vertices(self) -> int:
        return len(self.vertices)

    @property
    def num_faces(self) -> int:
        return len(self.faces)

    @property
    def num_edges(self) -> int:
        """Calculates the number of unique edges in the polyhedron."""
        edge_set = set()
        for face_indices in self.faces:
            num_v_in_face = len(face_indices)
            for i in range(num_v_in_face):
                v1_idx = face_indices[i]
                v2_idx = face_indices[(i + 1) % num_v_in_face]
                # Store edge with smaller index first to ensure uniqueness
                edge = tuple(sorted((v1_idx, v2_idx)))
                edge_set.add(edge)
        return len(edge_set)

    def get_face_points(self, face_index: int) -> List[Point3D]:
        """Returns the Point3D objects for a given face index."""
        if not (0 <= face_index < self.num_faces):
            raise IndexError("Face index out of bounds.")
        return [self.vertices[v_idx] for v_idx in self.faces[face_index]]

    def get_face_normal(self, face_index: int) -> Vector3D:
        """
        Calculates the normal vector of a given face.
        Assumes face vertices are ordered CCW from outside.
        Uses a robust method by checking vertex triplets to find a non-collinear set.
        
        Raises:
            ValueError: If all triplets are collinear and face is degenerate.
        """
        face_pts = self.get_face_points(face_index)
        n = len(face_pts)

        # Try to find any triplet of non-collinear points to compute normal
        for i in range(n):
            p0 = face_pts[i]
            p1 = face_pts[(i + 1) % n]
            p2 = face_pts[(i + 2) % n]

            v1 = p1 - p0
            v2 = p2 - p0
            normal = v1.cross(v2)
            if not normal.is_zero_vector():
                return normal.normalize()

        # If all triplets collinear, face is degenerate
        raise ValueError(f"Face {face_index} is degenerate: all vertices are collinear.")

    def surface_area(self) -> float:
        """
        Calculates the total surface area of the polyhedron.
        Sums the area of each face by triangulating polygonal faces from the first vertex.
        """
        total_area = 0.0
        for i in range(self.num_faces):
            face_pts = self.get_face_points(i)
            if len(face_pts) < 3:
                continue  # Should not happen with validation

            p0 = face_pts[0]
            face_area_sum = 0.0
            for j in range(1, len(face_pts) - 1):
                p1 = face_pts[j]
                p2 = face_pts[j + 1]

                v1 = p1 - p0
                v2 = p2 - p0
                triangle_area = 0.5 * v1.cross(v2).magnitude()
                face_area_sum += triangle_area
            total_area += face_area_sum
        return total_area

    def volume(self) -> float:
        """
        Calculates the volume of the polyhedron.
        Uses the sum of signed volumes of tetrahedra formed by origin and each face triangle.
        Triangulates faces if needed.

        Returns:
            Absolute volume (non-negative).

        Note:
            The reference origin (0,0,0) is assumed for signed volume calculations.
            If polyhedron does not contain origin, volume is still correct by absolute value.
        """
        total_volume = 0.0

        for face_indices in self.faces:
            face_verts = [self.vertices[idx] for idx in face_indices]

            # Triangulate the face from its first vertex
            p0_face = face_verts[0]
            for i in range(1, len(face_verts) - 1):
                p1_face = face_verts[i]
                p2_face = face_verts[i + 1]

                # Use Points as vectors for volume calculation
                v0 = Vector3D(p0_face.x, p0_face.y, p0_face.z)
                v1 = Vector3D(p1_face.x, p1_face.y, p1_face.z)
                v2 = Vector3D(p2_face.x, p2_face.y, p2_face.z)

                signed_tetra_vol = v0.dot(v1.cross(v2)) / 6.0
                total_volume += signed_tetra_vol

        return abs(total_volume)  # Volume should be positive

    def contains_point(self, point: Point3D) -> bool:
        ray_dir = Vector3D(1, 0, 0)  # Positive X direction
        intersections = 0
        for face_indices in self.faces:
            face_pts = [self.vertices[i] for i in face_indices]
            if ray_intersects_polygon(point, ray_dir, face_pts):
                intersections += 1
        return (intersections % 2) == 1


# Helper
def ray_intersects_polygon(ray_origin: Point3D, ray_dir: Vector3D, polygon_pts: list[Point3D], eps=1e-9) -> bool:
    """
    Return True if ray intersects polygon (convex).
    """

    # 1. Compute plane normal
    p0, p1, p2 = polygon_pts[:3]
    edge1 = p1 - p0
    edge2 = p2 - p0
    normal = edge1.cross(edge2)

    denom = normal.dot(ray_dir)
    if abs(denom) < eps:
        # Ray is parallel to polygon plane
        return False

    d = normal.dot(Vector3D(p0.x, p0.y, p0.z))
    t = (d - normal.dot(Vector3D(ray_origin.x, ray_origin.y, ray_origin.z))) / denom
    if t < 0:
        # Intersection behind ray origin
        return False

    intersect_point = ray_origin + ray_dir * t

    # Check if intersect_point lies inside polygon using barycentric method or ray casting 2D

    # Project polygon and point to 2D plane for point-in-polygon test:
    # Choose projection plane by ignoring coordinate with largest abs component of normal
    nx, ny, nz = abs(normal.x), abs(normal.y), abs(normal.z)
    if nx > ny and nx > nz:
        # Project to yz plane
        proj_pts = [(p.y, p.z) for p in polygon_pts]
        proj_p = (intersect_point.y, intersect_point.z)
    elif ny > nz:
        # Project to xz plane
        proj_pts = [(p.x, p.z) for p in polygon_pts]
        proj_p = (intersect_point.x, intersect_point.z)
    else:
        # Project to xy plane
        proj_pts = [(p.x, p.y) for p in polygon_pts]
        proj_p = (intersect_point.x, intersect_point.y)

    # Ray casting 2D point-in-polygon test
    inside = False
    n = len(proj_pts)
    j = n - 1
    for i in range(n):
        xi, yi = proj_pts[i]
        xj, yj = proj_pts[j]
        if ((yi > proj_p[1]) != (yj > proj_p[1])) and (proj_p[0] < (xj - xi) * (proj_p[1] - yi) / (yj - yi + eps) + xi):
            inside = not inside
        j = i

    return inside
