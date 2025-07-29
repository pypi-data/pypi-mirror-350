# geo/operations/intersections_2d.py

"""
Functions for 2D intersection detection.
"""
from typing import List, Optional, Tuple, Union, Literal

from geo.core import Point2D, Vector2D
from geo.core.precision import is_equal, is_zero, DEFAULT_EPSILON
from geo.primitives_2d import Line2D, Segment2D, Polygon, Circle

IntersectionType = Literal["none", "point", "overlap", "collinear_no_overlap"]

def segment_segment_intersection_detail(
    seg1: Segment2D, seg2: Segment2D, epsilon: float = DEFAULT_EPSILON
) -> Tuple[IntersectionType, Optional[Union[Point2D, Tuple[Point2D, Point2D]]]]:
    """
    Determines the intersection of two 2D line segments with more detail.

    Args:
        seg1: The first Segment2D.
        seg2: The second Segment2D.
        epsilon: Tolerance for floating point comparisons.

    Returns:
        A tuple:
        - IntersectionType: "none", "point", "overlap", "collinear_no_overlap".
        - Optional[Union[Point2D, Tuple[Point2D, Point2D]]]:
            - If "point", the intersection Point2D.
            - If "overlap", a tuple of two Point2Ds representing the overlapping segment.
            - None otherwise.
    """
    p1, p2 = seg1.p1, seg1.p2
    p3, p4 = seg2.p1, seg2.p2

    v12 = p2 - p1  # Vector for seg1
    v34 = p4 - p3  # Vector for seg2

    denom = v12.x * v34.y - v12.y * v34.x

    v13 = p3 - p1  # Vector from p1 to p3

    if is_zero(denom, epsilon):  # Lines are parallel
        # Check for collinearity
        if not is_zero(v13.x * v12.y - v13.y * v12.x, epsilon):
            return "none", None  # Parallel and non-collinear

        # Collinear case: check for overlap
        v12_mag_sq = v12.magnitude_squared()
        if is_zero(v12_mag_sq):  # seg1 is a point
            if seg2.contains_point(p1, epsilon):
                return "point", p1
            return "none", None

        t_p3_on_l1 = (p3 - p1).dot(v12) / v12_mag_sq
        t_p4_on_l1 = (p4 - p1).dot(v12) / v12_mag_sq

        min_t_s2 = min(t_p3_on_l1, t_p4_on_l1)
        max_t_s2 = max(t_p3_on_l1, t_p4_on_l1)

        overlap_start_t = max(0.0, min_t_s2)
        overlap_end_t = min(1.0, max_t_s2)

        if overlap_start_t <= overlap_end_t + epsilon:
            overlap_p_start = p1 + v12 * overlap_start_t
            overlap_p_end = p1 + v12 * overlap_end_t

            if is_equal(overlap_start_t, overlap_end_t, epsilon) or overlap_p_start == overlap_p_end:
                if seg1.contains_point(overlap_p_start, epsilon) and seg2.contains_point(overlap_p_start, epsilon):
                    return "point", overlap_p_start
                else:
                    return "collinear_no_overlap", None
            else:
                return "overlap", (overlap_p_start, overlap_p_end)
        else:
            return "collinear_no_overlap", None

    # Lines are not parallel, calculate intersection point
    t_num = v13.x * v34.y - v13.y * v34.x
    u_num = v13.x * v12.y - v13.y * v12.x

    t = t_num / denom

    v31 = p1 - p3
    u_numerator = v31.x * v12.y - v31.y * v12.x
    u = u_numerator / (-denom)

    if (-epsilon <= t <= 1.0 + epsilon) and (-epsilon <= u <= 1.0 + epsilon):
        intersection_point = p1 + v12 * t
        if seg1.contains_point(intersection_point, epsilon) and seg2.contains_point(intersection_point, epsilon):
            return "point", intersection_point
        else:
            return "none", None
    else:
        return "none", None


def line_polygon_intersections(line: Line2D, polygon: Polygon, epsilon: float = DEFAULT_EPSILON) -> List[Point2D]:
    """
    Finds all intersection points between an infinite line and a polygon's edges.

    Args:
        line: The Line2D.
        polygon: The Polygon.
        epsilon: Tolerance for floating point comparisons.

    Returns:
        A list of unique Point2D intersection points.
    """
    intersection_points: List[Point2D] = []
    unique_points_tuples: List[Tuple[float, float]] = []

    for edge in polygon.edges:
        p1_seg, p2_seg = edge.p1, edge.p2
        seg_vec = p2_seg - p1_seg

        denom = line.direction.x * seg_vec.y - line.direction.y * seg_vec.x

        if is_zero(denom, epsilon):  # Line and segment's line are parallel
            if line.contains_point(p1_seg, epsilon):  # Collinear
                points_to_add = []
                if segment_contains_point_collinear(line.p1, line.direction, p1_seg, p1_seg, p2_seg, epsilon):
                    points_to_add.append(p1_seg)
                if segment_contains_point_collinear(line.p1, line.direction, p2_seg, p1_seg, p2_seg, epsilon):
                    points_to_add.append(p2_seg)

                for pt_add in points_to_add:
                    pt_tuple = (round(pt_add.x, 7), round(pt_add.y, 7))
                    if not any(is_equal(upt[0], pt_tuple[0], epsilon) and is_equal(upt[1], pt_tuple[1], epsilon)
                               for upt in unique_points_tuples):
                        intersection_points.append(pt_add)
                        unique_points_tuples.append(pt_tuple)
            continue

        origin_to_p1_seg = p1_seg - line.p1
        t_num = origin_to_p1_seg.x * seg_vec.y - origin_to_p1_seg.y * seg_vec.x
        t = t_num / denom

        u_num = origin_to_p1_seg.x * line.direction.y - origin_to_p1_seg.y * line.direction.x
        u = u_num / denom

        if -epsilon <= u <= 1.0 + epsilon:
            intersect_pt = p1_seg + seg_vec * u
            pt_tuple = (round(intersect_pt.x, 7), round(intersect_pt.y, 7))
            if not any(is_equal(upt[0], pt_tuple[0], epsilon) and is_equal(upt[1], pt_tuple[1], epsilon)
                       for upt in unique_points_tuples):
                intersection_points.append(intersect_pt)
                unique_points_tuples.append(pt_tuple)

    intersection_points.sort(key=lambda p: (p.x, p.y))
    return intersection_points


def segment_contains_point_collinear(line_origin: Point2D, line_dir: Vector2D,
                                    pt_to_check: Point2D,
                                    seg_p1: Point2D, seg_p2: Point2D,
                                    epsilon: float) -> bool:
    """
    Helper for line_polygon_intersections: checks if pt_to_check (known collinear with line) is on segment.

    Args:
        line_origin: Origin point of the line.
        line_dir: Direction vector of the line.
        pt_to_check: The point to check.
        seg_p1: Segment endpoint 1.
        seg_p2: Segment endpoint 2.
        epsilon: Tolerance for floating point comparisons.

    Returns:
        True if pt_to_check lies on the segment, False otherwise.
    """
    if (min(seg_p1.x, seg_p2.x) - epsilon <= pt_to_check.x <= max(seg_p1.x, seg_p2.x) + epsilon and
        min(seg_p1.y, seg_p2.y) - epsilon <= pt_to_check.y <= max(seg_p1.y, seg_p2.y) + epsilon):

        vec_sp1_sp2 = seg_p2 - seg_p1
        vec_sp1_pt = pt_to_check - seg_p1

        if vec_sp1_sp2.is_zero_vector():  # Segment is a point
            return pt_to_check == seg_p1

        dot_prod = vec_sp1_pt.dot(vec_sp1_sp2)
        if dot_prod < -epsilon:
            return False
        if dot_prod > vec_sp1_sp2.magnitude_squared() + epsilon:
            return False
        return True
    return False


def segment_circle_intersections(segment: Segment2D, circle: Circle, epsilon: float = DEFAULT_EPSILON) -> List[Point2D]:
    """
    Finds intersection points between a line segment and a circle.

    Args:
        segment: The Segment2D.
        circle: The Circle.
        epsilon: Tolerance for floating point comparisons.

    Returns:
        A list of unique Point2D intersection points.
    """
    line = segment.to_line()
    line_intersections = circle.intersection_with_line(line, epsilon)

    segment_intersections: List[Point2D] = []
    unique_points_tuples = []

    for pt in line_intersections:
        if segment.contains_point(pt, epsilon):
            pt_tuple = (round(pt.x, 7), round(pt.y, 7))
            if not any(is_equal(upt[0], pt_tuple[0], epsilon) and is_equal(upt[1], pt_tuple[1], epsilon)
                       for upt in unique_points_tuples):
                segment_intersections.append(pt)
                unique_points_tuples.append(pt_tuple)

    segment_intersections.sort(key=lambda p: (p.x, p.y))
    return segment_intersections
