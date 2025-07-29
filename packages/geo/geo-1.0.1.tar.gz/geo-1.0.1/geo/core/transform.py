# geo/core/transform.py

"""
Provides functions for geometric transformations like translation, rotation, and scaling.

Initially, this module might contain simple functions. For more complex scenarios,
consider implementing transformation matrices.
"""

import math
from typing import Union, TypeVar
from .point import Point, Point2D, Point3D
from .vector import Vector, Vector2D, Vector3D

# Generic type for Point or Vector
GeomEntityType = TypeVar('GeomEntityType', Point, Vector, Point2D, Point3D, Vector2D, Vector3D)


def translate(entity: GeomEntityType, offset: Vector) -> GeomEntityType:
    """
    Translates a geometric entity (Point or Vector) by an offset vector.

    Args:
        entity: The Point or Vector to translate.
        offset: The Vector representing the translation.

    Returns:
        A new Point or Vector of the same type as the input entity, translated.

    Raises:
        TypeError: If the entity is not a Point or Vector, or if dimensions mismatch.
        ValueError: If dimensions of entity and offset vector do not match.
    """
    if not isinstance(entity, (Point, Vector)):
        raise TypeError(f"Translation is supported for Point and Vector types, got {type(entity)}.")
    if not isinstance(offset, Vector):
        raise TypeError(f"Offset must be a Vector type, got {type(offset)}.")

    if entity.dimension != offset.dimension:
        raise ValueError(
            f"Entity dimension ({entity.dimension}) and offset vector dimension ({offset.dimension}) must match."
        )

    if isinstance(entity, Point):
        # Point + Vector results in a new Point
        # The __add__ method in Point handles this logic and returns the correct Point subclass
        return entity + offset # type: ignore
    elif isinstance(entity, Vector):
        # Vector + Vector results in a new Vector
        # The __add__ method in Vector handles this logic and returns the correct Vector subclass
        # Note: Translating a vector typically means adding another vector if interpreting
        # it as a displacement. If interpreting as a direction, translation doesn't change it.
        # Here, we assume it's a displacement or position vector.
        return entity + offset # type: ignore
    else:
        # Should not be reached due to initial type check, but as a safeguard:
        raise TypeError(f"Unsupported entity type for translation: {type(entity)}")


def scale(entity: GeomEntityType, factors: Union[float, Vector],
            origin: Union[Point, None] = None) -> GeomEntityType:
    """
    Scales a geometric entity (Point or Vector) by given factors.

    Args:
        entity: The Point or Vector to scale.
        factors:
            - A single float for uniform scaling across all dimensions.
            - A Vector of the same dimension as the entity for non-uniform scaling.
        origin:
            - The Point about which to scale. If None, scaling is done about the
                coordinate system origin (0,0) or (0,0,0).
            - For Vectors, origin is typically ignored unless the vector is treated as a
                position vector relative to an origin. If scaling a direction vector,
                origin is usually not applicable. This implementation scales components directly.

    Returns:
        A new Point or Vector of the same type as the input entity, scaled.

    Raises:
        TypeError: If the entity is not a Point or Vector, or if factors type is invalid.
        ValueError: If dimensions mismatch or factors are invalid.
    """
    if not isinstance(entity, (Point, Vector)):
        raise TypeError(f"Scaling is supported for Point and Vector types, got {type(entity)}.")

    current_coords = entity.coords if isinstance(entity, Point) else entity.components

    scale_factors_tuple: tuple[float, ...]
    if isinstance(factors, (int, float)):
        scale_factors_tuple = tuple([float(factors)] * entity.dimension)
    elif isinstance(factors, Vector):
        if factors.dimension != entity.dimension:
            raise ValueError(
                f"Factor vector dimension ({factors.dimension}) must match entity dimension ({entity.dimension})."
            )
        scale_factors_tuple = tuple(float(f) for f in factors.components)
    else:
        raise TypeError(f"Factors must be a float or a Vector, got {type(factors)}.")

    if origin is not None:
        if not isinstance(origin, Point):
            raise TypeError(f"Origin must be a Point, got {type(origin)}.")
        if origin.dimension != entity.dimension:
            raise ValueError(
                f"Origin dimension ({origin.dimension}) must match entity dimension ({entity.dimension})."
            )

        # If origin is provided, translate to origin, scale, then translate back
        if isinstance(entity, Point):
            # Create a vector from origin to entity
            vec_to_entity = entity - origin # type: ignore
            scaled_vec_components = [
                vc * sf for vc, sf in zip(vec_to_entity.components, scale_factors_tuple)
            ]
            # Create the scaled vector relative to the origin
            if entity.dimension == 2:
                scaled_relative_vec = Vector2D(*scaled_vec_components) # type: ignore
            elif entity.dimension == 3:
                scaled_relative_vec = Vector3D(*scaled_vec_components) # type: ignore
            else:
                scaled_relative_vec = Vector(*scaled_vec_components) # type: ignore
            # Translate back by adding the origin Point
            return origin + scaled_relative_vec # type: ignore
        else: # entity is a Vector
                # For vectors (directions), origin is typically not used in simple scaling.
                # Components are scaled directly. If origin was meant for position vectors,
                # the user should handle the point-like representation.
            scaled_components = [c * sf for c, sf in zip(current_coords, scale_factors_tuple)]
            return entity.__class__(*scaled_components) # type: ignore

    else: # Scale about the coordinate system origin
        scaled_components = [c * sf for c, sf in zip(current_coords, scale_factors_tuple)]
        return entity.__class__(*scaled_components) # type: ignore


def rotate_2d(entity: Union[Point2D, Vector2D], angle_rad: float,
                origin: Union[Point2D, None] = None) -> Union[Point2D, Vector2D]:
    """
    Rotates a 2D Point or Vector counter-clockwise by a given angle around an origin.

    Args:
        entity: The Point2D or Vector2D to rotate.
        angle_rad: The angle of rotation in radians.
        origin: The Point2D about which to rotate. If None, rotation is
                performed about the coordinate system origin (0,0).
                For Vectors, origin is usually ignored if it's a direction vector.
                If it's a position vector, treat it like a point for rotation logic.

    Returns:
        A new Point2D or Vector2D, rotated.

    Raises:
        TypeError: If the entity is not a Point2D or Vector2D.
    """
    if not isinstance(entity, (Point2D, Vector2D)):
        raise TypeError(f"2D rotation is supported for Point2D and Vector2D, got {type(entity)}.")

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    if isinstance(entity, Point2D):
        ox, oy = (origin.x, origin.y) if origin else (0.0, 0.0)
        # Translate point back to origin
        px, py = entity.x - ox, entity.y - oy
        # Rotate point
        new_px = px * cos_a - py * sin_a
        new_py = px * sin_a + py * cos_a
        # Translate point back
        return Point2D(new_px + ox, new_py + oy)
    elif isinstance(entity, Vector2D):
        # For vectors (directions), rotation origin doesn't change the components if it's a free vector.
        # If the vector is a position vector, the user should rotate its corresponding point.
        # Here, we rotate the components directly, assuming it's a direction or relative vector.
        vx, vy = entity.x, entity.y
        new_vx = vx * cos_a - vy * sin_a
        new_vy = vx * sin_a + vy * cos_a
        return Vector2D(new_vx, new_vy)
    else:
        # Should not be reached
        raise TypeError(f"Unsupported entity type for 2D rotation: {type(entity)}")


def rotate_3d(entity: Union[Point3D, Vector3D],
                axis: Vector3D,
                angle_rad: float,
                origin: Union[Point3D, None] = None) -> Union[Point3D, Vector3D]:
    """
    Rotates a 3D Point or Vector by a given angle around an arbitrary axis.
    Uses Rodrigues' rotation formula.

    Args:
        entity: The Point3D or Vector3D to rotate.
        axis: The Vector3D representing the axis of rotation. Must be non-zero.
        angle_rad: The angle of rotation in radians (counter-clockwise when looking
                    down the axis vector towards the origin of the axis).
        origin: The Point3D about which to rotate.
                - If entity is Point3D: If None, rotation is about the coordinate
                    system origin (0,0,0) along an axis passing through it.
                - If entity is Vector3D: This parameter is ignored; vectors are rotated
                    about an axis passing through the coordinate system origin.

    Returns:
        A new Point3D or Vector3D, rotated.

    Raises:
        TypeError: If the entity is not Point3D/Vector3D, or axis is not Vector3D.
        ValueError: If the rotation axis is a zero vector.
    """
    if not isinstance(entity, (Point3D, Vector3D)):
        raise TypeError(f"3D rotation is supported for Point3D and Vector3D, got {type(entity)}.")
    if not isinstance(axis, Vector3D):
        raise TypeError(f"Rotation axis must be a Vector3D, got {type(axis)}.")
    if axis.is_zero_vector():
        raise ValueError("Rotation axis cannot be a zero vector.")
    # Accept origin=None as valid, otherwise check type
    if origin is not None and not isinstance(origin, Point3D):
        raise TypeError("Origin must be a Point3D")
    # If origin is None, set to origin Point3D(0,0,0)
    if origin is None:
        origin = Point3D(0, 0, 0)
    
    # Normalize the rotation axis
    k = axis.normalize() # k is a Vector3D with float components

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    one_minus_cos_a = 1.0 - cos_a

    # Vector to be rotated (v)
    v_to_rotate: Vector3D
    effective_origin: Point3D

    if isinstance(entity, Point3D):
        if origin:
            effective_origin = origin
            v_to_rotate = entity - effective_origin # Point3D - Point3D -> Vector3D
        else:
            effective_origin = Point3D(0.0, 0.0, 0.0) # System origin
            # Convert Point3D to Vector3D from system origin
            v_to_rotate = Vector3D(entity.x, entity.y, entity.z)
    elif isinstance(entity, Vector3D):
        # For vectors, rotation is always about an axis through the system origin.
        # The 'origin' parameter is effectively ignored for the vector's components.
        v_to_rotate = entity
        # effective_origin is not strictly needed for vector result, but for consistency if we returned Point
        # effective_origin = Point3D(0.0,0.0,0.0) # Not used for vector return path
    else:
        # Should be caught by initial check, but for exhaustiveness
        raise TypeError(f"Unexpected entity type {type(entity)} in rotate_3d logic.")


    # Rodrigues' rotation formula:
    # v_rot = v*cos(a) + (k x v)*sin(a) + k*(k.v)*(1-cos(a))
    
    # (k . v)
    k_dot_v = k.dot(v_to_rotate)

    # (k x v)
    k_cross_v = k.cross(v_to_rotate) # This is a Vector3D

    # Calculate each term of the formula.
    # All terms result in Vector3D objects.
    term1 = v_to_rotate * cos_a
    term2 = k_cross_v * sin_a
    term3 = k * (k_dot_v * one_minus_cos_a) # k is Vector3D, (k.v)*(1-cos_a) is scalar

    rotated_vector_part = term1 + term2 + term3

    if isinstance(entity, Point3D):
        # Translate the rotated vector part back relative to the effective_origin
        return effective_origin + rotated_vector_part # Point3D + Vector3D -> Point3D
    elif isinstance(entity, Vector3D):
        # For a vector entity, the result is the rotated vector itself
        return rotated_vector_part # This is already a Vector3D
    else:
        # Should not be reached
        raise TypeError("Internal error: entity type changed unexpectedly.")