import math
import json
from typing import Dict, List, Any, Callable
from src.globe.face import Face


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.faces = []  # type: List[Face]

    def __repr__(self) -> Dict[str, Any]:
        return {
            "coordinates": tuple(self.x, self.y, self.z),
            "faces": self.faces.__repr__()
        }

    def __str__(self) -> str:
        return "Point({}, {}, {})".format(self.x, self.y, self.z)

    def __getitem__(self, i: int) -> Face:
        return self.faces[i]

    def subdivide(self, point: 'Point', count: int, check_point: Callable)\
            -> List['Point']:
        segments = []  # type: List[Point]
        segments.append(self)
        for i in range(count):
            np = Point(
                self.x * (1 - (i / count)) + point.x * (i / count),
                self.y * (1 - (i / count)) + point.y * (i / count),
                self.z * (1 - (i / count)) + point.z * (i / count)
                )
            np = check_point(np)
            segments.append(np)
        return segments

    def segment(self, point: 'Point', percent: float) -> 'Point':
        percent = max(0.01, min(1.0, percent))
        x = point.x * (1 - percent) + self.x * percent
        y = point.y * (1 - percent) + self.y * percent
        z = point.z * (1 - percent) + self.z * percent
        return Point(x, y, z)

    def midpoint(self, point: 'Point') -> 'Point':
        return self.segment(point, 0.5)

    def project(self, radius: float, percent: float = 1.0) -> 'Point':
        percent = max(0.0, min(1.0, percent))
        magnitude = math.sqrt(math.pow(self.x, 2) +
                              math.pow(self.y, 2),
                              math.pow(self.z, 2))
        ratio = radius / magnitude

        self.x = self.x * ratio * percent
        self.y = self.y * ratio * percent
        self.z = self.z * ratio * percent
        return self

    def register_face(self, face) -> None:
        self.faces.append(face)

    def get_ordered_faces(self) -> List[Face]:
        working_array = self.faces.copy()
        ret = []  # type: List[Face]
        for i in range(len(self.faces)):
            if i == 0:
                ret.append(working_array[i])
                working_array.pop(i)
            else:
                hit = False  # type: bool
                j = 0  # type: int
                while j < len(working_array) and not hit:
                    if working_array[j].is_adjacent_to(ret[i - 1]):
                        hit = True
                        ret.append(working_array[j])
                        working_array.pop(j)
                    j += 1
        return ret

    def find_common_face(self, other: 'Point', not_this_face: Face) -> Face:
        for i in self.faces:
            for j in other.faces:
                if i == j and i.id != not_this_face.id:
                    return i
        return None

    def to_json(self) -> str:
        return json.dumps({
            'x': self.x,
            'y': self.y,
            'z': self.z
        })
