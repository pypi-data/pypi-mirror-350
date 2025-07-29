"""Ear‑clipping and Delaunay examples."""
from geo.core import Point2D
from geo.primitives_2d import Polygon
from geo.operations.triangulation import (
    triangulate_simple_polygon_ear_clipping, delaunay_triangulation_points_2d
)
import matplotlib.pyplot as plt

poly = Polygon([
    Point2D(0, 0), Point2D(4, 0), Point2D(5, 2), Point2D(3, 4), Point2D(1, 3)
])
triangles = triangulate_simple_polygon_ear_clipping(poly)
print("Ear-clipping output:", len(triangles), "triangles")

pts = [Point2D(x, y) for x, y in [(0,0),(4,0),(5,2),(3,4),(1,3)]]
tris = delaunay_triangulation_points_2d(pts)
print("Delaunay produced", len(tris), "triangles")

# crude plot
for t in tris:
    xs = [t.p1.x, t.p2.x, t.p3.x, t.p1.x]
    ys = [t.p1.y, t.p2.y, t.p3.y, t.p1.y]
    plt.plot(xs, ys, "k-")
plt.scatter([p.x for p in pts], [p.y for p in pts])
plt.gca().set_aspect("equal", adjustable="box")
plt.show()