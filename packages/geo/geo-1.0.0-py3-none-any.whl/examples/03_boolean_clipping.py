"""Clip a square by a triangle and compare union / intersection via Shapely backend."""
from geo.core import Point2D
from geo.primitives_2d import Polygon
from geo.operations.boolean_ops import (
    clip_polygon_sutherland_hodgman, polygon_union, polygon_intersection
)

square = Polygon([
    Point2D(0, 0), Point2D(4, 0), Point2D(4, 4), Point2D(0, 4)
])
tri = Polygon([
    Point2D(1, 1), Point2D(3, 1), Point2D(2, 3)
])

clipped = clip_polygon_sutherland_hodgman(square, tri)
print("Clipped poly vertices:")
for v in clipped.vertices:
    print("  ", v)

# If Shapely available
try:
    union = polygon_union(square, tri)
    inter = polygon_intersection(square, tri)
    print("union area =", sum(p.area for p in union))
    print("intersection area =", sum(p.area for p in inter))
except NotImplementedError:
    print("Install shapely for full boolean demo → pip install shapely")