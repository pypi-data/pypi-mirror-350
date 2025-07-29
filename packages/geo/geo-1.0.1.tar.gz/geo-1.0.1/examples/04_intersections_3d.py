"""Demonstrate 3‑D intersection helpers."""
from geo.core import Point3D, Vector3D
from geo.primitives_3d import Sphere, Plane
from geo.operations.intersections_3d import (
    sphere_sphere_intersection, plane_plane_intersection, line_triangle_intersection_moller_trumbore
)
from geo.primitives_3d import Line3D

s1 = Sphere(Point3D(0, 0, 0), 2)
s2 = Sphere(Point3D(3, 0, 0), 2)
print("Sphere–sphere →", sphere_sphere_intersection(s1, s2).type)

pl1 = Plane(Point3D(0, 0, 0), Vector3D(0, 0, 1))
pl2 = Plane(Point3D(0, 0, 1), Vector3D(1, 0, 1))
print("Plane–plane line =", plane_plane_intersection(pl1, pl2))

orig = Point3D(0, 0, 5)
dir = Vector3D(0, 0, -1)
tri = (
    Point3D(-1, -1, 0), Point3D(1, -1, 0), Point3D(0, 1, 0)
)
print("Ray-triangle hit:", line_triangle_intersection_moller_trumbore(orig, dir, *tri))