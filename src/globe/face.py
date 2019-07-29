from __future__ import annotations
from typing import List, Generator, Union
import json
from src.globe.point import Point


def _id_generator() -> Generator[int, None, None]:
    _face_count = 0
    while True:
        yield _face_count
        _face_count += 1


_id = _id_generator()


class Face:
    def __init__(
            self,
            point1: Point,
            point2: Point,
            point3: Point,
            register: bool = True):
        self.id = next(_id)
        self.points = [
            point1,
            point2,
            point3
        ]
        self.centroid: Point = self.get_centroid(True)
        if register:
            point1.register_face(self)
            point2.register_face(self)
            point3.register_face(self)

    def __repr__(self) -> str:
        return json.dumps(
            {'id': self.id, 'points': [x.__str__() for x in self.points]})

    def __str__(self) -> str:
        return "Face({})".format(self.__repr__())

    def get_other_points(self, point1: Point) -> List[Point]:
        other: List[Point] = []
        for p in self.points:
            if p != point1:
                other.append(p)
        return other

    def find_third_point(self, point1: Point, point2: Point)\
            -> Union[Point, None]:
        for p in self.points:
            if p != point1 and p != point2:
                return p
        return None

    def is_adjacent_to(self, face2: Face) -> bool:
        """
        Count the number of common points, if there are 2/3 common points
        then the faces are adjacent
        """
        count = len(set(self.points) & set(face2.points))
        assert count in range(4)
        return count == 2

    def get_centroid(self, clear: bool = False) -> Point:
        """Get the centroid of the triangle"""
        if self.centroid and not clear:
            return self.centroid
        x = (self.points[0].x + self.points[1].x + self.points[2].x) / 3
        y = (self.points[0].y + self.points[1].y + self.points[2].y) / 3
        z = (self.points[0].z + self.points[1].z + self.points[2].z) / 3
        centroid = Point(x, y, z)
        self.centroid = centroid
        return centroid
