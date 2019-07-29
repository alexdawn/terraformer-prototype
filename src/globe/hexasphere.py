from __future__ import annotations
import json
from typing import Dict, List

from src.globe.tile import Tile
from src.globe.face import Face
from src.globe.point import Point


class Isohedron:
    def get_corners(self):
        tao = 1.61803399
        size = 1000
        return [
            Point(size, tao * size, 0),
            Point(-size, tao * size, 0),
            Point(size, -tao * size, 0),
            Point(-size, -tao * size, 0),
            Point(0, size, tao * size),
            Point(0, -size, tao * size),
            Point(0, size, -tao * size),
            Point(0, -size, -tao * size),
            Point(tao * size, 0, size),
            Point(-tao * size, 0, size),
            Point(tao * size, 0, -size),
            Point(-tao * size, 0, -size)
        ]

    def get_faces(self, corners):
        return [
            Face(corners[0], corners[1], corners[4], False),
            Face(corners[1], corners[9], corners[4], False),
            Face(corners[4], corners[9], corners[5], False),
            Face(corners[5], corners[9], corners[3], False),
            Face(corners[2], corners[3], corners[7], False),
            Face(corners[3], corners[2], corners[5], False),
            Face(corners[7], corners[10], corners[2], False),
            Face(corners[0], corners[8], corners[10], False),
            Face(corners[0], corners[4], corners[8], False),
            Face(corners[8], corners[2], corners[10], False),
            Face(corners[8], corners[4], corners[5], False),
            Face(corners[8], corners[5], corners[2], False),
            Face(corners[1], corners[0], corners[6], False),
            Face(corners[11], corners[1], corners[6], False),
            Face(corners[3], corners[9], corners[11], False),
            Face(corners[6], corners[10], corners[7], False),
            Face(corners[3], corners[11], corners[7], False),
            Face(corners[11], corners[6], corners[7], False),
            Face(corners[6], corners[0], corners[10], False),
            Face(corners[9], corners[1], corners[11], False)
        ]


class Hexsphere:
    def __init__(self, radius: float, number_of_divisions: int,
                 hex_size: float):
        self.radius = radius
        corners = Isohedron().get_corners()
        assert len(corners) == 12
        points = {corner: corners[i] for i, corner in enumerate(corners)}
        faces = Isohedron().get_faces(corners)
        assert len(faces) == 20
        faces = self.set_faces(faces, number_of_divisions, points)
        points = self.project_points(points, radius)
        self.set_tiles(points, hex_size)

    def set_faces(self, faces: List[Face], number_of_divisions: int, points: Dict[Point, Point]):
        def get_point_if_exists(point: Point) -> Point:
            """Check if a suitable point already exists and use it
            otherwise create one"""
            for p in points.keys():
                if point.common_point(p):
                    print("Point already exists!")
                    return p
            else:
                print("Create point")
                points[point] = point
                return point
        new_faces: List[Face] = []
        for i, f in enumerate(faces):
            print("On isohedral face {} it has points:".format(i))
            for p in f.points:
                print("\t{}".format(p))
            prev = None
            bottom = [f.points[0]]
            left = f.points[0].subdivide(
                f.points[1], number_of_divisions, get_point_if_exists)
            right = f.points[0].subdivide(
                f.points[2], number_of_divisions, get_point_if_exists)
            for i in range(1, number_of_divisions+1):
                prev = bottom
                bottom = left[i].subdivide(
                    right[i], i, get_point_if_exists)
                for j in range(i):
                    print("On division {} {}".format(i, j))
                    nf = Face(prev[j], bottom[j], bottom[j + 1])
                    print(nf)
                    new_faces.append(nf)
                    if j > 0:  # handle inverse triangles
                        nf = Face(prev[j - 1], prev[j], bottom[j])
                        new_faces.append(nf)
        return new_faces

    def project_points(self, points: Dict[Point, Point], radius: float) -> Dict[Point, Point]:
        new_points: Dict[Point, Point] = {}
        for p in points.keys():
            np = points[p].project(radius)
            new_points[np] = np
        return new_points

    def set_tiles(self, points: Dict[Point, Point], hex_size) -> None:
        self.tiles: List[Tile] = []
        self.tile_lookup: Dict[Tile, Tile] = {}
        for i, p in enumerate(points.keys()):
            print("On point {}". format(i))
            new_tile = Tile(points[p], hex_size)
            self.tiles.append(new_tile)
            self.tile_lookup[new_tile] = new_tile
        for t in self.tiles:
            _self = self
            t.neighbours = [_self.tile_lookup[item] for item in t.neighbour_ids]

    def to_json(self) -> str:
        return json.dumps({
            "radius": self.radius,
            "tiles": [tile.to_json() for tile in self.tiles]
        })

    def __repr__(self) -> str:
        return self.to_json()

    def __str__(self) -> str:
        return json.dumps({
            "radius": self.radius,
            "tiles": [str(tile) for tile in self.tiles]
        })

    def to_object_file(self) -> str:
        obj_v: List[Point] = []
        obj_f: List[List[Face]] = []
        obj_text = "# vertices \n"
        vertex_index_map: Dict[Point, Face] = {}

        for t in self.tiles:
            f: List[Face] = []
            for p in t.boundary:
                index = vertex_index_map[p]
                if index is None:
                    obj_v.append(p)
                    index = len(obj_v)
                    vertex_index_map[p] = index
                f.append(index)
            obj_f.append(f)
        for v in obj_v:
            obj_text += 'v {} {} {}\n'.format(v.x, v.y, v.z)
        obj_text += '\n# faces\n'
        for i in obj_f:
            obj_text += "f {}\n".format(
                ' '.join([str(f) for f in i]))
        return obj_text
