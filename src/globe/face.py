from typing import List
import json
import globe.point as point


def _id_generator() -> int:
    _face_count = 0
    while True:
        yield _face_count
        _face_count += 1


_id = _id_generator()


class Face:
    def __init__(
            self,
            point1,
            point2,
            point3,
            register: bool = True):
        self.id = next(_id)
        self.points = [
            point1,
            point2,
            point3
        ]
        self.centroid = None
        if register:
            point1.register_face(self)
            point2.register_face(self)
            point3.register_face(self)

    def __repr__(self):
        return json.dumps(
            {'id': self.id, 'points': [x.__str__() for x in self.points]})

    def __str__(self):
        return "Face({})".format(self.__repr__())

    def get_other_points(self, point1) -> List:
        other = []  # type: List
        for i in self.points:
            if i != point1:
                other.append(i)
        return other

    def find_third_point(self, point1, point2):
        for i in self.points:
            if i != point1 and i != point2:
                return i

    def is_adjacent_to(self, face2: 'Face') -> bool:
        """
        Count the number of common points, if there are 2/3 common points
        then the faces are adjacent
        """
        count = len(set(self.points) & set(face2.points))
        assert count in range(4)
        return count == 2

    def get_centroid(self, clear: bool = False):
        """Get the centroid of the triangle"""
        if self.centroid and not clear:
            return self.centroid
        x = (self.points[0].x + self.points[1].x + self.points[2].x) / 3
        y = (self.points[0].y + self.points[1].y + self.points[2].y) / 3
        z = (self.points[0].z + self.points[1].z + self.points[2].z) / 3
        centroid = point.Point(x, y, z)
        self.centroid = centroid
        return centroid
