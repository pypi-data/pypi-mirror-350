"""Random scatter -> convex hull with matplotlib visualisation."""
import random, math
import matplotlib.pyplot as plt
from geo.core import Point2D
from geo.operations.convex_hull import convex_hull_2d_monotone_chain

random.seed(0)
pts = [Point2D(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(200)]
hull = convex_hull_2d_monotone_chain(pts)

plt.scatter([p.x for p in pts], [p.y for p in pts], s=10, label="points")
hx = [p.x for p in hull] + [hull[0].x]
hy = [p.y for p in hull] + [hull[0].y]
plt.plot(hx, hy, "r-", label="convex hull")
plt.axis("equal")
plt.legend()
plt.show()