"""
Basic Input/Output utility functions for simple geometry data formats.
These are basic and can be expanded significantly.
"""
from typing import List, Sequence, Union, TextIO
import csv
import os
import json

from geo.core import Point2D, Point3D
from geo.primitives_2d import Polygon as Polygon2D
from geo.primitives_3d import Polyhedron

def parse_points_from_string(data_string: str, 
                              delimiter: str = ',', 
                              point_dim: int = 2) -> list[Union[Point2D, Point3D]]:
    """
    Parses a string of coordinates into a list of Point2D or Point3D objects.
    Supports 2D and 3D points; validates for supported dimensions.
    """
    if point_dim not in (2, 3):
        raise ValueError(f"Unsupported point dimension: {point_dim}. Supported dimensions are 2 and 3.")

    parts = [p.strip() for p in data_string.replace('\n', delimiter).split(delimiter) if p.strip()]

    try:
        coords_flat = [float(part) for part in parts]
    except ValueError as e:
        raise ValueError(f"Invalid numeric value found in data string: {e}")

    if len(coords_flat) % point_dim != 0:
        raise ValueError(
            f"Total number of coordinates ({len(coords_flat)}) is not divisible by point dimension ({point_dim}).")

    points = []
    for i in range(0, len(coords_flat), point_dim):
        chunk = coords_flat[i:i + point_dim]
        if point_dim == 2:
            points.append(Point2D(*chunk))
        elif point_dim == 3:
            points.append(Point3D(*chunk))
    return points


def format_point_to_string(point: Union[Point2D, Point3D], delimiter: str = ', ', precision: int = 6) -> str:
    """Formats a Point2D or Point3D object into a string."""
    format_str = f"{{:.{precision}f}}"
    if isinstance(point, Point2D):
        return delimiter.join([format_str.format(point.x), format_str.format(point.y)])
    elif isinstance(point, Point3D):
        return delimiter.join([format_str.format(point.x), format_str.format(point.y), format_str.format(point.z)])
    raise TypeError("Input must be a Point2D or Point3D object.")

def save_polyhedron_to_obj_simple(polyhedron: Polyhedron,
                                  file_path: str | os.PathLike,
                                  precision: int = 6,
                                  encoding: str = "utf-8") -> None:
    """Saves a Polyhedron object to a simple OBJ file format."""
    fmt = f"{{:.{precision}f}}"
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(f"# Simple OBJ export from geo\n")
            f.write(f"# Vertices: {polyhedron.num_vertices}\n")
            f.write(f"# Faces: {polyhedron.num_faces}\n\n")

            for vertex in polyhedron.vertices:
                f.write(f"v {fmt.format(vertex.x)} {fmt.format(vertex.y)} {fmt.format(vertex.z)}\n")
            f.write("\n")

            for face in polyhedron.faces:
                f.write("f " + " ".join(str(i + 1) for i in face) + "\n")
    except OSError as e:
        raise IOError(f"Failed to write OBJ file: {e}")

def load_polyhedron_from_obj_simple(file_path: str | os.PathLike, encoding: str = "utf-8") -> Polyhedron:
    """Loads a Polyhedron from a simplified OBJ file (vertices and faces only)."""
    vertices: list[Point3D] = []
    faces: list[list[int]] = []

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                cmd = parts[0].lower()

                if cmd == 'v':
                    if len(parts) < 4:
                        raise ValueError(f"Malformed vertex line {line_num}: '{line}'")
                    try:
                        x, y, z = map(float, parts[1:4])
                        vertices.append(Point3D(x, y, z))
                    except ValueError:
                        raise ValueError(f"Invalid vertex in line {line_num}: '{line}'")

                elif cmd == 'f':
                    if len(parts) < 4:
                        raise ValueError(f"Malformed face line {line_num}: '{line}'")
                    indices = []
                    for token in parts[1:]:
                        idx_str = token.split('/')[0]
                        try:
                            idx = int(idx_str)
                            idx = idx - 1 if idx > 0 else len(vertices) + idx
                            indices.append(idx)
                        except ValueError:
                            raise ValueError(f"Invalid index in face line {line_num}: '{line}'")
                    faces.append(indices)
    except FileNotFoundError:
        raise FileNotFoundError(f"OBJ file not found: {file_path}")
    except OSError as e:
        raise IOError(f"Error reading OBJ file: {e}")

    if not vertices:
        raise ValueError("OBJ file contains no vertices.")

    return Polyhedron(vertices, faces)

def save_polygon2d_to_csv(polygon: Polygon2D, file_path: str | os.PathLike, delimiter: str = ',', encoding: str = "utf-8") -> None:
    """Saves a 2D Polygon's vertices to a CSV file (x,y per line)."""
    try:
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(['x', 'y'])
            for vertex in polygon.vertices:
                writer.writerow([vertex.x, vertex.y])
    except OSError as e:
        raise IOError(f"Failed to write CSV file: {e}")

def load_polygon2d_from_csv(file_path: str | os.PathLike, delimiter: str = ',', encoding: str = "utf-8") -> Polygon2D:
    """Loads a 2D Polygon from a CSV file."""
    vertices: list[Point2D] = []
    try:
        with open(file_path, 'r', newline='', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader, None)
            if header is None:
                raise ValueError("CSV file is empty or missing header.")
            for i, row in enumerate(reader):
                if len(row) < 2:
                    raise ValueError(f"Row {i + 1} has fewer than 2 columns: {row}")
                try:
                    x, y = float(row[0]), float(row[1])
                    vertices.append(Point2D(x, y))
                except ValueError:
                    raise ValueError(f"Invalid numeric data in row {i + 1}: {row}")
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    except OSError as e:
        raise IOError(f"Error reading CSV file: {e}")

    if not vertices:
        raise ValueError("No vertices found in CSV file.")
    return Polygon2D(vertices)

def save_polygon2d_to_json(polygon: Polygon2D, file_path: str | os.PathLike, encoding: str = "utf-8") -> None:
    """Saves a 2D Polygon to a JSON file with a list of point dictionaries."""
    data = [{'x': v.x, 'y': v.y} for v in polygon.vertices]
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        raise IOError(f"Failed to write JSON file: {e}")

def load_polygon2d_from_json(file_path: str | os.PathLike, encoding: str = "utf-8") -> Polygon2D:
    """Loads a 2D Polygon from a JSON file containing a list of point dictionaries."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        vertices = [Point2D(p['x'], p['y']) for p in data if 'x' in p and 'y' in p]
        if not vertices:
            raise ValueError("No valid vertices found in JSON file.")
        return Polygon2D(vertices)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Invalid JSON format: {e}")
