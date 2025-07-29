# geo/primitives_2d/curve/bezier.py

"""
Bezier curves in 2-D.

A Bezier curve of degree n is defined by its control points
P₀ … Pₙ and is evaluated as

    B(t) = Σᵢ Pᵢ · Bᵢ,ₙ(t)          0 ≤ t ≤ 1,

where Bᵢ,ₙ(t) are the Bernstein basis polynomials.  Values of t
outside [0, 1] produce an extrapolation of the curve.
"""

import math
from typing import Sequence

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal
from .base import Curve2D

__all__ = ["BezierCurve"]


# Helper
def _bernstein(n: int, i: int, t: float) -> float:
    """
    Bᵢ,ₙ(t) = C(n, i) · tⁱ · (1 - t)ⁿ⁻ⁱ
    Returns 0 when i ∉ [0, n] to simplify calling code.
    """
    if i < 0 or i > n:
        return 0.0
    # math.comb already validates n ≥ i ≥ 0.
    coeff = math.comb(n, i)
    # No need to special-case t=0/1 – power terms are cheap & exact.
    return coeff * (t ** i) * ((1.0 - t) ** (n - i))


# Main class
class BezierCurve(Curve2D):
    """
    Arbitrary-degree 2-D Bezier curve.

    Parameters
    ----------
    control_points :
        Iterable of :class: geo.core.Point2D. At least two are required
        (a single point would be a degenerate curve; for that, use
        :class: geo.primitives_2d.curve.base.Curve2D directly or a
        degenerate curve subclass).

    Notes
    -----
    •  Degree = len(control_points) - 1
    •  point_at uses Bernstein polynomials by default; can switch
       to De Casteljau for improved numerical stability on very high
       degrees via the use_casteljau flag.
    """

    def __init__(self, control_points: Sequence[Point2D]):
        if len(control_points) < 2:
            raise ValueError(
                "BezierCurve needs at least two control points "
                "to represent a curve (one would be a single point)."
            )
        super().__init__(control_points)
        self.degree: int = len(self.control_points) - 1
        if self.degree == 0:
            # Degenerate curve – zero vector as a single-point curve
            self.control_points = (Point2D(0.0, 0.0), Point2D(0.0, 0.0))

    def point_at(self, t: float, *, use_casteljau: bool = False) -> Point2D:
        """
        Evaluate the curve at parameter t.

        Parameters
        ----------
        t : float
            Parameter value. 0 ≤ t ≤ 1 is the usual domain;
            other values extrapolate linearly.
        use_casteljau : bool, default=False
            When True, uses the recursive De Casteljau algorithm,
            which is numerically stabler for high-degree curves.

        Returns
        -------
        Point2D
        """
        if self.degree == 1:
            # Early-exit – simple linear interpolation; avoids overhead
            p0, p1 = self.control_points
            return p0 * (1.0 - t) + p1 * t

        if use_casteljau:
            return self._point_at_casteljau(t)

        n = self.degree
        sx = sy = 0.0
        for i, p in enumerate(self.control_points):
            b = _bernstein(n, i, t)
            sx += p.x * b
            sy += p.y * b
        return Point2D(sx, sy)

    def tangent_at(self, t: float) -> Vector2D:
        """
        First derivative B'(t).  Returns the zero vector for a
        degenerate (degree 0) curve.

        The derivative of a Bezier curve is itself another Bezier curve
        of degree (n-1) whose control points are n·(Pᵢ₊₁ - Pᵢ).
        """
        if self.degree == 0:
            return Vector2D(0.0, 0.0)

        if self.degree == 1:
            # Constant derivative – vector from P0 to P1
            p0, p1 = self.control_points
            return p1 - p0

        n = self.degree
        dx = dy = 0.0
        for i in range(n):
            delta = self.control_points[i + 1] - self.control_points[i]
            b = _bernstein(n - 1, i, t)
            dx += delta.x * b
            dy += delta.y * b
        return Vector2D(dx * n, dy * n)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(degree={self.degree}, "
            f"control_points={self.control_points})"
        )

    def _point_at_casteljau(self, t: float) -> Point2D:
        """
        De Casteljau evaluation (O(n²) but numerically robust).
        """
        if self.degree == 1:
            return self.point_at(t)  # linear shortcut

        # Work on a mutable copy
        pts = list(self.control_points)
        n = self.degree
        for r in range(1, n + 1):
            for i in range(n - r + 1):
                pts[i] = pts[i] * (1.0 - t) + pts[i + 1] * t
        return pts[0]

    def derivative_curve(self) -> "BezierCurve":
        """
        Returns the derivative of this Bezier curve as a new BezierCurve object.
        The resulting control points are vectors interpreted as new points.
        """
        n = len(self.control_points) - 1
        deriv_points = []
        for i in range(n):
            delta = self.control_points[i + 1] - self.control_points[i]
            # Convert the vector into a Point2D (starting from origin)
            deriv_point = Point2D(*((n * delta).components))
            deriv_points.append(deriv_point)
        return BezierCurve(deriv_points)