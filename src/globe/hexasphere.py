import json
from typing import Dict, List

from src.globe.tile import Tile
from src.globe.face import Face
from src.globe.point import Point


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
            Point(0, -size, -tao * size),
            Point(tao * size, 0, size),
            Point(-tao * size, 0, size),
            Point(tao * size, 0, -size),
            Point(-tao * size, 0, -size)
        ]
        assert len(corners) == 12
        points = {}  # type: Dict[Point, Point]
        # not sure if this is going to be hashable?
        for i, corner in enumerate(corners):
            points[corner] = corners[i]
        # where does this get populated?
        faces = []  # type: List[Face]

        def get_point_if_exists(self, point: Point) -> Point:
            if points[point]:
                return points[point]
            else:
                points[point] = point
                return point

        new_faces = []  # type: List[Face]
        for f in faces:
            prev = None
            bottom = [f.points[0]]
            left = f.points[0].subdivide(
                faces[f].points[1], number_of_divisions, get_point_if_exists)
            right = f.points[0].subdivide(
                faces[f].points[2], number_of_divisions, get_point_if_exists)
            for i in range(number_of_divisions):
                prev = bottom
                bottom = left[i].subdivide(
                    right[i], i, get_point_if_exists)
                for j in range(i):
                    nf = Face(prev[j], bottom[j], bottom[j + 1])
                    new_faces.append(nf)
                    if j > 0:
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
        for p in points:
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

    def to_object_file():
        pass
