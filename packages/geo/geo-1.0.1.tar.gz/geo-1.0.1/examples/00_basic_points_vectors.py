"""Minimal tour of Point2D / Vector2D / transformations."""
from geo.core import Point2D, Vector2D

p = Point2D(1, 2)
q = Point2D(4, -1)

print("p =", p, "  q =", q)
print("distance(p, q) =", p.distance_to(q))

v = q - p  # Vector from p→q
print("vector v =", v, "  length =", v.magnitude())
print("normalised v =", v.normalize())

# simple affine combo
mid = p.midpoint(q)
print("mid-point =", mid)