# geo/operations/boolean_ops.py

"""
Comprehensive boolean operations module including:

1. Convex polygon clipping via Sutherland-Hodgman (clip_polygon_sutherland_hodgman).
2. 2D polygon boolean operations backed by Shapely (auto-skipped if Shapely missing).
3. 3D polyhedron boolean operations backed by Trimesh (auto-skipped if Trimesh missing).

The API is stable:
```python
clip_polygon_sutherland_hodgman(subject, clip)
polygon_union(a, b)
polygon_intersection(a, b)
polygon_difference(a, b)
polyhedron_union(a, b)
polyhedron_intersection(a, b)
polyhedron_difference(a, b)
```
"""

from __future__ import annotations

from typing import List, Optional

from geo.core.precision import DEFAULT_EPSILON, is_zero
from geo.core import Point2D, Point3D
from geo.primitives_2d import Polygon
from geo.primitives_3d import Polyhedron

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _dedup_consecutive(points: List[Point2D], tol: float = DEFAULT_EPSILON) -> List[Point2D]:
    """Remove consecutive duplicates (incl. closing repeat)."""
    if not points:
        return []
    uniq = [points[0]]
    for pt in points[1:]:
        if (pt - uniq[-1]).magnitude() > tol:
            uniq.append(pt)
    if len(uniq) > 2 and (uniq[0] - uniq[-1]).magnitude() <= tol:
        uniq.pop()
    return uniq

# ---------------------------------------------------------------------------
# 0. Convex clipping – Sutherland–Hodgman
# ---------------------------------------------------------------------------

def _is_left(p: Point2D, a: Point2D, b: Point2D) -> float:
    """Return positive if *p* is left of the line *ab*."""
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x)


def clip_polygon_sutherland_hodgman(subject: Polygon, clip: Polygon) -> Optional[Polygon]:
    """Clip *subject* (any polygon, CW or CCW) against **convex** *clip* (CCW).

    Returns clipped polygon or *None* if empty.
    """
    if subject.num_vertices < 3 or clip.num_vertices < 3:
        return None

    # Ensure clip polygon is CCW (required by algorithm)
    if clip.signed_area() < 0:
        clip = Polygon(list(reversed(clip.vertices)))

    output = list(subject.vertices)
    for i in range(clip.num_vertices):
        cp1 = clip.vertices[i]
        cp2 = clip.vertices[(i + 1) % clip.num_vertices]
        input_list = output
        output = []
        if not input_list:
            break
        s = input_list[-1]
        for e in input_list:
            inside_e = _is_left(e, cp1, cp2) >= -DEFAULT_EPSILON
            inside_s = _is_left(s, cp1, cp2) >= -DEFAULT_EPSILON
            if inside_e:
                if not inside_s:
                    # Compute intersection
                    seg = e - s
                    clip_vec = cp2 - cp1
                    denom = seg.x * clip_vec.y - seg.y * clip_vec.x
                    if not is_zero(denom, DEFAULT_EPSILON):
                        t = ((cp1 - s).x * clip_vec.y - (cp1 - s).y * clip_vec.x) / denom
                        output.append(s + seg * t)
                output.append(e)
            elif inside_s:
                seg = e - s
                clip_vec = cp2 - cp1
                denom = seg.x * clip_vec.y - seg.y * clip_vec.x
                if not is_zero(denom, DEFAULT_EPSILON):
                    t = ((cp1 - s).x * clip_vec.y - (cp1 - s).y * clip_vec.x) / denom
                    output.append(s + seg * t)
            s = e
    output = _dedup_consecutive(output)
    return Polygon(output) if len(output) >= 3 else None

# ---------------------------------------------------------------------------
# 1. 2‑D BOOLEAN OPS (Shapely)
# ---------------------------------------------------------------------------

try:
    from shapely.geometry import Polygon as _ShPoly  # type: ignore
    from shapely.ops import unary_union
    
    _HAS_SHAPELY = True
except ImportError:  # pragma: no cover
    _HAS_SHAPELY = False


def _to_shapely(poly: Polygon) -> "_ShPoly":
    return _ShPoly([(v.x, v.y) for v in poly.vertices])


def _from_shapely(geom) -> List[Polygon]:
    def _ring_to_pts(ring) -> List[Point2D]:
        return [Point2D(x, y) for x, y in list(ring.coords)[:-1]]

    def _convert_single_polygon(g) -> Polygon:
        exterior = _ring_to_pts(g.exterior)
        if len(exterior) < 3:
            return None
        interiors = [_ring_to_pts(ring) for ring in g.interiors if len(ring.coords) > 3]
        poly = Polygon(exterior)
        for hole in interiors:
            poly.add_hole(hole)
        return poly

    if geom.is_empty:
        return []
    elif geom.geom_type == "Polygon":
        poly = _convert_single_polygon(geom)
        return [poly] if poly else []
    elif geom.geom_type == "MultiPolygon":
        return [p for g in geom.geoms for p in _from_shapely(g)]
    elif geom.geom_type == "GeometryCollection":
        return [p for g in geom.geoms for p in _from_shapely(g)]
    else:
        return []

def _apply_shapely_op(a: Polygon, b: Polygon, op: str) -> List[Polygon]:
    if not _HAS_SHAPELY:
        raise NotImplementedError("Shapely not available")
    s1, s2 = map(_to_shapely, (a, b))
    op_func = {
        "union": lambda x, y: unary_union([x, y]),
        "intersection": lambda x, y: x.intersection(y),
        "difference": lambda x, y: x.difference(y),
    }[op]
    result = op_func(s1, s2)
    return _from_shapely(result)


def polygon_union(a: Polygon, b: Polygon) -> List[Polygon]:
    return _apply_shapely_op(a, b, "union")


def polygon_intersection(a: Polygon, b: Polygon) -> List[Polygon]:
    return _apply_shapely_op(a, b, "intersection")


def polygon_difference(a: Polygon, b: Polygon) -> List[Polygon]:
    return _apply_shapely_op(a, b, "difference")

# ---------------------------------------------------------------------------
# 2. 3‑D BOOLEAN OPS (Trimesh)
# ---------------------------------------------------------------------------

try:
    import trimesh
    import numpy as np
    _HAS_TRIMESH = True
except ImportError:  # pragma: no cover
    _HAS_TRIMESH = False


def _poly_to_tm(poly: Polyhedron) -> "trimesh.Trimesh":  # type: ignore[name-defined]
    verts = np.array([[v.x, v.y, v.z] for v in poly.vertices])
    faces = np.array(poly.faces)
    mesh = trimesh.Trimesh(verts, faces, process=False, validate=False)
    mesh.process(validate=True)
    return mesh


def _tm_to_poly(mesh: "trimesh.Trimesh") -> Polyhedron:  # type: ignore[name-defined]
    verts = [Point3D(*v) for v in mesh.vertices]
    faces = [tuple(map(int, f)) for f in mesh.faces]
    return Polyhedron(verts, faces)


def _tm_boolean(a: Polyhedron, b: Polyhedron, op: str) -> List[Polyhedron]:
    if not _HAS_TRIMESH:
        raise NotImplementedError("Trimesh not available")

    def ensure_watertight(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        if not mesh.is_watertight:
            mesh = mesh.fill_holes()
        return mesh

    m1, m2 = map(_poly_to_tm, (a, b))
    m1 = ensure_watertight(m1)
    m2 = ensure_watertight(m2)

    fn = {
        "union": trimesh.boolean.union,
        "intersection": trimesh.boolean.intersection,
        "difference": trimesh.boolean.difference,
    }[op]

    try:
        res = fn([m1, m2], engine="scad")
    except Exception:
        res = fn([m1, m2])

    meshes = (
        [res]
        if isinstance(res, trimesh.Trimesh)
        else list(res.geometry.values()) if isinstance(res, trimesh.Scene) else res  # type: ignore[arg-type]
    )
    return [_tm_to_poly(m) for m in meshes if isinstance(m, trimesh.Trimesh)]

def polyhedron_union(a: Polyhedron, b: Polyhedron) -> List[Polyhedron]:
    return _tm_boolean(a, b, "union")

def polyhedron_intersection(a: Polyhedron, b: Polyhedron) -> List[Polyhedron]:
    return _tm_boolean(a, b, "intersection")

def polyhedron_difference(a: Polyhedron, b: Polyhedron) -> List[Polyhedron]:
    return _tm_boolean(a, b, "difference")
