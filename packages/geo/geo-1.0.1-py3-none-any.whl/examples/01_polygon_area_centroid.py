"""Create a polygon & compute derived properties."""
from geo.core import Point2D
from geo.primitives_2d import Polygon

square = Polygon([
    Point2D(0, 0), Point2D(3, 0), Point2D(3, 3), Point2D(0, 3)
])
print("square area =", square.area)
print("square centroid =", square.centroid())