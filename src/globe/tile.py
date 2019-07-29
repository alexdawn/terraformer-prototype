from __future__ import annotations
import math
import json
from typing import Dict, List
from src.globe.point import Point
from src.globe.face import Face


def vector(p1: Point, p2: Point) -> Point:
    return Point(p2.x - p1.x,
                 p2.y - p1.y,
                 p2.z - p1.z)


def calculate_surface_normal(p1: Point, p2: Point, p3: Point) -> Point:
    u = vector(p1, p2)
    v = vector(p1, p3)
    return Point(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x
    )


def pointing_away_from_origin(p: Point, v: Point) -> bool:
    return ((p.x * v.x) >= 0) and ((p.y * v.y) >= 0) and ((p.z * v.z) >= 0)


def normalize_vector(v: Point) -> Point:
    magnitude = math.sqrt(
        math.pow(v.x, 2)
        + math.pow(v.y, 2)
        + math.pow(v.z, 2)
    )
    return Point(
        v.x / magnitude,
        v.y / magnitude,
        v.z / magnitude
    )


class Tile:
    def __init__(self, centre_point: Point, hex_size: float = 1):
        hex_size = max(0.01, min(1.0, hex_size))
        self.centre_point = centre_point
        self.faces: List[Face] = centre_point.get_ordered_faces()
        self.boundary: List[Point] = []
        self.neighbour_ids: List[Point] = []
        self.neighbours: List[Tile] = []
        neighbour_hash: Dict[Point, int] = {}
        for f in self.faces:
            centroid_point = f.get_centroid()
            self.boundary.append(
                centroid_point.segment(self.centre_point, hex_size))
            other_points = f.get_other_points(self.centre_point)
            for other in other_points:
                neighbour_hash[other] = 1
        self.neighbour_ids = list(neighbour_hash.keys())
        normal = calculate_surface_normal(*self.boundary[:3])
        if not pointing_away_from_origin(self.centre_point, normal):
            self.boundary.reverse()

    def get_lat_long(self, radius: float, boundary_num: int)\
            -> Dict[str, float]:
        point = self.centre_point
        if(type(boundary_num) == int and boundary_num < len(self.boundary)):
            point = self.boundary[boundary_num]
        phi = math.acos(point.y / radius)
        theta = ((math.atan2(point.x, point.z) + math.pi + math.pi / 2) %
                 (math.pi * 2) - math.pi)
        # theta is a hack, since I want to rotate by Math.PI/2 to start.
        return {
            "lat": 180 * phi / math.pi - 90,
            "lon": 180 * theta / math.pi
        }

    def scaled_boundary(self, scale: float) -> List[Point]:
        scale = max(0, min(1, scale))
        ret: List[Point] = []
        for p in self.boundary:
            ret.append(self.centre_point.segment(p, 1 - scale))
        return ret

    def to_json(self) -> str:
        return json.dumps({
            'centre_point': str(self.centre_point),
            'boundary': [str(point) for point in self.boundary]
        })

    def __repr__(self) -> str:
        return str(self.to_json())

    def __str__(self) -> str:
        return "Tile({})".format(self.__repr__())
