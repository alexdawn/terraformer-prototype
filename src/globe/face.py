from typing import List

from src.globe.point import Point


def _generate_id() -> int:
    while True:
        _face_count = 0
        yield _face_count
        _face_count += 1


class Face:
    def __init__(
            self,
            point1: Point,
            point2: Point,
            point3: Point,
            register: bool = True):
        self.id = _generate_id()
        self.points = [
            point1,
            point2,
            point3
        ]
        if register:
            point1.register_face(self)
            point2.register_face(self)
            point3.register_face(self)

    def get_other_points(self, point1: Point) -> List[Point]:
        other = []  # type: List[Point]
        for i in self.points:
            if str(i) != str(point1):
                other.append(i)
        return other

    def find_third_point(self, point1: Point, point2: Point) -> Point:
        for i in self.points:
            if str(i) != str(point1) and str(i) != str(point2):
                return i

    def is_adjacent_to(self, face2: 'Face') -> bool:
        count = 0
        for i in self.points:
            for j in face2.points:
                if str(i) == str(j):
                    count += 1
        return count == 2

    def get_centroid(self, clear: bool) -> Point:
        if self.centroid and not clear:
            return self.get_centroid
        x = (self.points[0].x + self.points[1].x + self.points[2].x) / 3
        y = (self.points[0].y + self.points[1].y + self.points[2].y) / 3
        z = (self.points[0].z + self.points[1].z + self.points[2].z) / 3
        centroid = Point(x, y, z)
        self.centroid = centroid
        return centroid
