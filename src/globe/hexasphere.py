import json
from typing import Dict, List

from globe.tile import Tile
from globe.face import Face
from globe.point import Point


class Hexsphere:
    def __init__(self, radius: float, number_of_divisions: int,
                 hex_size: float):
        self.radius = radius
        tao = 1.61803399
        size = 1000
        corners = [
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
        assert len(corners) == 12
        points = {}  # type: Dict[Point, Point]
        for i, corner in enumerate(corners):
            points[corner] = corners[i]
        faces = [
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
        ]  # type: List[Face]
        assert len(faces) == 20

        def get_point_if_exists(point: Point) -> Point:
            """Check if a suitable point already exists and use it
            otherwise create one"""
            for p in points:
                if point.common_point(p):
                    print("Point already exists!")
                    return p
            else:
                print("Create point")
                points[point] = point
                return point

        new_faces = []  # type: List[Face]
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
                    if j > 0:  #handle inverse triangles
                        nf = Face(prev[j - 1], prev[j], bottom[j])
                        new_faces.append(nf)
        faces = new_faces
        new_points = {}
        for p in points:
            np = points[p].project(radius)
            new_points[np] = np
        points = new_points
        self.tiles = []
        self.tile_lookup = {}
        for i, p in enumerate(points):
            print("On point {}". format(i))
            new_tile = Tile(points[p], hex_size)
            self.tiles.append(new_tile)
            self.tile_lookup[str(new_tile)] = new_tile
        for t in self.tiles:
            _self = self
            self.tiles[t].neighbours = [
                _self.tile_lookup[item]
                for item in self.tiles[t].neighbour_ids]

    def to_json(self):
        return json.dump({
            "radius": self.radius,
            "tiles": [tile.to_json() for tile in self.tiles]
        })

    def __repr__(self):
        return self.to_json

    def __str__(self):
        return json.dump({
            "radius": self.radius,
            "tiles": [str(tile) for tile in self.tiles]
        })

    def to_object_file():
        pass
