# (1) python tests/utils/test_io.py
# (2) python -m unittest tests/utils/test_io.py (verbose output) (auto add sys.path)

import math
import unittest
import sys
import os

# For (1): Add the project root to sys.path so `geo` can be imported
# For (2): Don't need
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import tempfile
import json
from unittest import mock
from unittest.mock import patch

from geo.utils import io
from geo.core import Point2D, Point3D
from geo.primitives_2d import Polygon as Polygon2D
from geo.primitives_3d import Polyhedron


class TestGeoIO(unittest.TestCase):

    def test_parse_points_from_string_2d_and_3d(self):
        data_2d = "1,2, 3,4, 5,6"
        points_2d = io.parse_points_from_string(data_2d, point_dim=2)
        self.assertTrue(all(isinstance(p, Point2D) for p in points_2d))
        self.assertEqual(len(points_2d), 3)
        self.assertEqual((points_2d[0].x, points_2d[0].y), (1, 2))

        data_3d = "1,2,3, 4,5,6, 7,8,9"
        points_3d = io.parse_points_from_string(data_3d, point_dim=3)
        self.assertTrue(all(isinstance(p, Point3D) for p in points_3d))
        self.assertEqual(len(points_3d), 3)
        self.assertEqual(points_3d[1].z, 6)

        with self.assertRaises(ValueError):
            io.parse_points_from_string("1,2,3,4", point_dim=3)

    def test_parse_points_from_string_empty_and_invalid(self):
        # Empty string should return empty list
        result = io.parse_points_from_string("", point_dim=2)
        self.assertEqual(result, [])

        # Invalid dimension
        with self.assertRaises(ValueError):
            io.parse_points_from_string("1,2,3", point_dim=4)

        # Non-numeric values
        with self.assertRaises(ValueError):
            io.parse_points_from_string("1,2,abc", point_dim=2)

    def test_format_point_to_string(self):
        p2d = Point2D(1.1234567, 2.7654321)
        s2d = io.format_point_to_string(p2d, precision=3)
        self.assertEqual(s2d, "1.123, 2.765")

        p3d = Point3D(3.1415926, 2.7182818, 1.6180339)
        s3d = io.format_point_to_string(p3d, precision=2)
        self.assertEqual(s3d, "3.14, 2.72, 1.62")

        with self.assertRaises(TypeError):
            io.format_point_to_string("not a point")

    def test_format_point_with_zero_and_negative(self):
        p2d = Point2D(0, -0.00001)
        s = io.format_point_to_string(p2d, precision=5)
        self.assertEqual(s, "0.00000, -0.00001")

    def test_save_and_load_polyhedron_obj(self):
        vertices = [
            Point3D(0,0,0), Point3D(1,0,0), Point3D(0,1,0), Point3D(0,0,1)
        ]
        faces = [
            [0,1,2],
            [0,1,3],
            [0,2,3],
            [1,2,3]
        ]
        poly = Polyhedron(vertices, faces)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.obj")
            io.save_polyhedron_to_obj_simple(poly, file_path)
            self.assertTrue(os.path.exists(file_path))

            loaded_poly = io.load_polyhedron_from_obj_simple(file_path)
            self.assertEqual(len(loaded_poly.vertices), 4)
            self.assertEqual(len(loaded_poly.faces), 4)
            self.assertIsInstance(loaded_poly.vertices[0], Point3D)

    def test_save_polyhedron_obj_ioerror(self):
        # Mock open to throw OSError on write
        with patch("builtins.open", mock.mock_open()) as mocked_open:
            mocked_open.side_effect = OSError("disk full")
            poly = Polyhedron([], [])
            with self.assertRaises(IOError):
                io.save_polyhedron_to_obj_simple(poly, "dummy.obj")

    def test_load_polyhedron_obj_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "empty.obj")
            with open(file_path, "w") as f:
                f.write("")  # empty file
            with self.assertRaises(ValueError):
                io.load_polyhedron_from_obj_simple(file_path)

            # malformed vertex line
            file_path2 = os.path.join(tmpdir, "malformed_vertex.obj")
            with open(file_path2, "w") as f:
                f.write("v 1 2\n")  # only two coords
            with self.assertRaises(ValueError):
                io.load_polyhedron_from_obj_simple(file_path2)

            # malformed face line (less than 3 indices)
            file_path3 = os.path.join(tmpdir, "malformed_face.obj")
            with open(file_path3, "w") as f:
                f.write("v 0 0 0\nv 1 0 0\nv 0 1 0\n")
                f.write("f 1 2\n")  # only two vertices
            with self.assertRaises(ValueError):
                io.load_polyhedron_from_obj_simple(file_path3)

    def test_save_and_load_polygon2d_csv(self):
        vertices = [Point2D(1,2), Point2D(3,4), Point2D(5,6)]
        polygon = Polygon2D(vertices)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "polygon.csv")
            io.save_polygon2d_to_csv(polygon, file_path)
            self.assertTrue(os.path.exists(file_path))

            loaded_polygon = io.load_polygon2d_from_csv(file_path)
            self.assertEqual(len(loaded_polygon.vertices), 3)
            self.assertEqual((loaded_polygon.vertices[1].x, loaded_polygon.vertices[1].y), (3, 4))

    def test_save_polygon2d_csv_ioerror(self):
        with patch("builtins.open", mock.mock_open()) as mocked_open:
            mocked_open.side_effect = OSError("cannot write file")
            polygon = Polygon2D([Point2D(0,0), Point2D(1,0), Point2D(0,1)])  # at least 3 points
            with self.assertRaises(IOError):
                io.save_polygon2d_to_csv(polygon, "dummy.csv")

    def test_load_polygon2d_csv_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_file = os.path.join(tmpdir, "empty.csv")
            with open(empty_file, "w") as f:
                f.write("")
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_csv(empty_file)

            bad_file = os.path.join(tmpdir, "bad.csv")
            with open(bad_file, "w") as f:
                f.write("x,y\n1,a\n")
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_csv(bad_file)

            short_row_file = os.path.join(tmpdir, "short.csv")
            with open(short_row_file, "w") as f:
                f.write("x,y\n1\n")
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_csv(short_row_file)

    def test_save_and_load_polygon2d_json(self):
        vertices = [Point2D(7,8), Point2D(9,10), Point2D(10,7)]  # at least 3 points
        polygon = Polygon2D(vertices)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "polygon.json")
            io.save_polygon2d_to_json(polygon, file_path)
            self.assertTrue(os.path.exists(file_path))

            loaded_polygon = io.load_polygon2d_from_json(file_path)
            self.assertEqual(len(loaded_polygon.vertices), 3)
            self.assertEqual(loaded_polygon.vertices[0].x, 7)

    def test_save_polygon2d_json_ioerror(self):
        with patch("builtins.open", mock.mock_open()) as mocked_open:
            mocked_open.side_effect = OSError("cannot write file")
            polygon = Polygon2D([Point2D(0,0), Point2D(1,0), Point2D(0,1)])  # at least 3 points
            with self.assertRaises(IOError):
                io.save_polygon2d_to_json(polygon, "dummy.json")

    def test_load_polygon2d_json_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_file = os.path.join(tmpdir, "empty.json")
            with open(empty_file, "w") as f:
                f.write("")
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_json(empty_file)

            bad_file = os.path.join(tmpdir, "bad.json")
            with open(bad_file, "w") as f:
                f.write("{ bad json }")
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_json(bad_file)

            missing_keys_file = os.path.join(tmpdir, "missing_keys.json")
            with open(missing_keys_file, "w") as f:
                f.write('[{"a":1}]')
            with self.assertRaises(ValueError):
                io.load_polygon2d_from_json(missing_keys_file)

    def test_load_nonexistent_files(self):
        with self.assertRaises(FileNotFoundError):
            io.load_polygon2d_from_csv("nonexistent.csv")
        with self.assertRaises(FileNotFoundError):
            io.load_polygon2d_from_json("nonexistent.json")
        with self.assertRaises(FileNotFoundError):
            io.load_polyhedron_from_obj_simple("nonexistent.obj")


if __name__ == "__main__":
    unittest.main()
