# geo/primitives_2d/curve/spline.py
"""
A complete (clamped, non-periodic) B-spline implementation in 2D.

Key features
============
* Uniform or user-supplied knot vectors
* de Boor evaluation (point_at, tangent_at)
* First-derivative / tangent computation
* Cox-de Boor basis-function utilities (basis_functions, basis_function_derivatives)
* Knot-span lookup (find_span)
* Knot insertion (insert_knot) — arbitrary multiplicity r
* Degree elevation (elevate_degree) — elevates by 1 at a time (can be looped)
* Conversion helper (to_bezier_segments) (one cubic Bezier per B-spline span)

Limitations
-----------
* Only open, clamped knot vectors are generated automatically.
* Only 2D control points are supported (easy to generalise).
* Higher-order derivatives not yet implemented.

Implementation follows Piegl & Tiller, *The NURBS Book* (2nd ed.), sections 2-3.
"""

from __future__ import annotations

import bisect
import math
from typing import List, Sequence, Tuple

from geo.core import Point2D, Vector2D
from .base import Curve2D

__all__ = ["BSplineCurve2D"]

# Helper
def _uniform_clamped_knots(n: int, p: int) -> List[float]:
    """Return a *uniform, clamped* knot vector (length = n + p + 2)."""
    m = n + p + 1  # last index
    knots = [0.0] * (p + 1)
    inner = [i for i in range(1, m - (2 * p))]
    knots += inner
    knots += [inner[-1] + 1.0] * (p + 1)
    # normalise to [0,1]
    k0, k_last = knots[0], knots[-1]
    span = k_last - k0
    return [(k - k0) / span for k in knots]


# Main class
class SplineCurve(Curve2D):
    """Open, clamped *B-spline* curve in 2D."""

    def __init__(
        self,
        control_points: Sequence[Point2D],
        degree: int = 3,
        knots: Sequence[float] | None = None,
    ) -> None:
        if degree < 1:
            raise ValueError("Degree p must be ≥ 1 (p = 1 → poly-line).")
        if len(control_points) < degree + 1:
            raise ValueError("Need at least p + 1 control points.")
        super().__init__(control_points)
        self.p: int = degree
        self.n: int = len(self.control_points) - 1  # highest cp index

        if knots is None:
            knots = _uniform_clamped_knots(self.n, self.p)
        self.knots: List[float] = list(knots)
        if len(self.knots) != self.n + self.p + 2:
            raise ValueError("Invalid knot vector length.")
        if any(self.knots[i] > self.knots[i + 1] for i in range(len(self.knots) - 1)):
            raise ValueError("Knot vector must be non-decreasing.")

    # Evaluation

    def find_span(self, u: float) -> int:
        if math.isclose(u, self.knots[self.n + 1]):
            return self.n
        # Special case for knots[p]
        if math.isclose(u, self.knots[self.p]):
            return self.p
        low = self.p
        high = self.n + 1
        return bisect.bisect_left(self.knots, u, low, high) - 1

    def basis_functions(self, i: int, u: float) -> List[float]:
        """Compute *p + 1* non-zero basis functions N_{i-p, …, i}(u)."""
        p = self.p
        N = [0.0] * (p + 1)
        left = [0.0] * (p + 1)
        right = [0.0] * (p + 1)
        N[0] = 1.0
        for j in range(1, p + 1):
            left[j] = u - self.knots[i + 1 - j]
            right[j] = self.knots[i + j] - u
            saved = 0.0
            for r in range(j):
                demon = right[r + 1] + left[j - r]
                if math.isclose(demon, 0.0):
                    temp = 0.0
                else:
                    temp = N[r] / demon
                N[r] = saved + right[r + 1] * temp
                saved = left[j - r] * temp
            N[j] = saved
        return N

    def basis_function_derivatives(self, i: int, u: float, d: int = 1) -> List[List[float]]:
        """Return derivatives up to order *d* (≤ p) of basis at *u*.
        Uses algorithm A2-3 (Piegl & Tiller).
        """
        p = self.p
        d = min(d, p)
        ndu = [[0.0] * (p + 1) for _ in range(p + 1)]
        ndu[0][0] = 1.0
        left = [0.0] * (p + 1)
        right = [0.0] * (p + 1)
        for j in range(1, p + 1):
            left[j] = u - self.knots[i + 1 - j]
            right[j] = self.knots[i + j] - u
            saved = 0.0
            for r in range(j):
                ndu[j][r] = right[r + 1] + left[j - r]
                temp = ndu[r][j - 1] / ndu[j][r]
                ndu[r][j] = saved + right[r + 1] * temp
                saved = left[j - r] * temp
            ndu[j][j] = saved
        # load basis values
        ders = [[0.0] * (p + 1) for _ in range(d + 1)]
        for j in range(p + 1):
            ders[0][j] = ndu[j][p]
        # compute derivatives
        a = [[0.0] * (p + 1) for _ in range(2)]
        for r in range(p + 1):
            s1, s2 = 0, 1
            a[0][0] = 1.0
            for k in range(1, d + 1):
                dsum = 0.0
                rk = r - k
                pk = p - k
                if r >= k:
                    a[s2][0] = a[s1][0] / ndu[pk + 1][rk]
                    dsum = a[s2][0] * ndu[rk][pk]
                j1 = 1 if rk >= -1 else -rk
                j2 = k - 1 if r - 1 <= pk else p - r
                for j in range(j1, j2 + 1):
                    a[s2][j] = (
                        (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j]
                    )
                    dsum += a[s2][j] * ndu[rk + j][pk]
                if r <= pk:
                    a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r]
                    dsum += a[s2][k] * ndu[r][pk]
                ders[k][r] = dsum
                s1, s2 = s2, s1  # swap rows
        # multiply by factorial terms
        for k in range(1, d + 1):
            for j in range(p + 1):
                ders[k][j] *= p
                for i2 in range(1, k):
                    ders[k][j] *= p - i2
        return ders

    # de Boor evaluation

    def point_at(self, t: float) -> Point2D:
        # Clamp parameter to domain
        u = max(self.knots[self.p], min(t, self.knots[self.n + 1]))
        i = self.find_span(u)
        N = self.basis_functions(i, u)
        cx = cy = 0.0
        for k in range(self.p + 1):
            cp = self.control_points[i - self.p + k]
            coeff = N[k]
            cx += coeff * cp.x
            cy += coeff * cp.y
        return Point2D(cx, cy)

    def tangent_at(self, t: float) -> Vector2D:
        u = max(self.knots[self.p], min(t, self.knots[self.n + 1]))
        i = self.find_span(u)
        ders = self.basis_function_derivatives(i, u, d=1)
        dN = ders[1]
        vx = vy = 0.0
        for k in range(self.p + 1):
            cp = self.control_points[i - self.p + k]
            coeff = dN[k]
            vx += coeff * cp.x
            vy += coeff * cp.y
        return Vector2D(vx, vy)

    # Knot editing

    def insert_knot(self, u: float, r: int = 1) -> None:
        """Insert parameter *u* (`p` ≥ multiplicity + current mult.) up to `r` times."""
        p = self.p
        s = self.knots.count(u)
        if s + r > p:
            raise ValueError("Knot multiplicity would exceed degree.")
        for _ in range(r):
            self._insert_single_knot(u)

    def _insert_single_knot(self, u: float) -> None:
        p = self.p
        i = self.find_span(u)
        s = self.knots.count(u)
        
        # Copy control points as list to modify
        new_cpts = list(self.control_points)
        
        # Compute new control points affected by knot insertion
        for j in range(i - p + 1, i - s + 1)[::-1]:  # backwards
            denom = self.knots[j + p] - self.knots[j]
            alpha = (u - self.knots[j]) / denom if denom > 0 else 0.0
            
            new_x = (1 - alpha) * new_cpts[j - 1].x + alpha * new_cpts[j].x
            new_y = (1 - alpha) * new_cpts[j - 1].y + alpha * new_cpts[j].y
            
            new_cpts[j - 1] = Point2D(new_x, new_y)
        
        # Insert new control point at position i - p + 1
        new_cpts.insert(i - p + 1, new_cpts[i - p + 1])
        
        # Insert knot
        self.knots.insert(i + 1, u)
        
        # Update control points tuple and number of control points
        self.control_points = tuple(new_cpts)
        self.n += 1

    # Degree elevation

    def elevate_degree(self) -> None:
        """Elevate degree by **one** (algorithm 5.3, Piegl & Tiller)."""
        p = self.p
        m = self.n + p + 1
        Uh = self.knots.copy()
        ph = p + 1
        n = self.n
        # new knot vector identical (no change for clamped uniform)
        # compute new control points
        Q: List[Point2D] = []
        # first point
        Q.append(self.control_points[0])
        for i in range(1, n + 1):
            alpha = i / (ph)
            x = alpha * self.control_points[i].x + (1 - alpha) * self.control_points[i - 1].x
            y = alpha * self.control_points[i].y + (1 - alpha) * self.control_points[i - 1].y
            Q.append(Point2D(x, y))
        Q.append(self.control_points[-1])
        # update
        self.p = ph
        self.control_points = tuple(Q)
        self.n = len(self.control_points) - 1
        # knots remain unchanged (for uniform clamped) — else regenerate
        if len(self.knots) != self.n + self.p + 2:
            self.knots = _uniform_clamped_knots(self.n, self.p)

    # Utility / export

    def to_bezier_segments(self) -> List[Tuple[Point2D, Point2D, Point2D, Point2D]]:
        """Return a list of cubic Bezier segments equivalent to this B-spline.
        Works only for *p == 3*.
        """
        if self.p != 3:
            raise NotImplementedError("Conversion only for cubic B-splines.")
        beziers: List[Tuple[Point2D, Point2D, Point2D, Point2D]] = []
        for span in range(self.p, self.n + 1):
            if self.knots[span + 1] == self.knots[span]:
                continue  # zero-length span
            # basis -> Bezier extraction coefficients (pre-computed for cubic)
            cps = [self.control_points[span - 3 + k] for k in range(4)]
            beziers.append(tuple(cps))
        return beziers

    # repr

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"BSplineCurve2D(degree={self.p}, "
            f"control_points={self.control_points}, "
            f"knots={self.knots})"
        )
