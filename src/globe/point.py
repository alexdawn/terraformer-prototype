import math
import json
from itertools import product
from typing import Dict, List, Any, Callable


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.faces = []  # type: List

    def __repr__(self) -> Dict[str, Any]:
        return json.dumps({
            "coordinates": (self.x, self.y, self.z),
            "faces": [f.__repr__() for f in self.faces]
        })

    def __str__(self) -> str:
        return "Point({}, {}, {})".format(
            round(self.x, 2),
            round(self.y, 2),
            round(self.z, 2))

    def common_point(self, test: 'Point') -> bool:
        return self.x == test.x and self.y == test.y and self.z == test.z

    def subdivide(self, point: 'Point', count: int, check_point: Callable)\
            -> List['Point']:
        segments = []  # type: List[Point]
        segments.append(self)
        for i in range(1, count+1):
            np = Point(
                self.x * (1 - (i / count+1)) + point.x * (i / count+1),
                self.y * (1 - (i / count+1)) + point.y * (i / count+1),
                self.z * (1 - (i / count+1)) + point.z * (i / count+1)
                )
            print(np)
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
                              math.pow(self.y, 2) +
                              math.pow(self.z, 2))
        ratio = radius / magnitude

        self.x = self.x * ratio * percent
        self.y = self.y * ratio * percent
        self.z = self.z * ratio * percent
        return self

    def register_face(self, face) -> None:
        self.faces.append(face)

    def get_ordered_faces(self) -> List:
        working_array = self.faces.copy()
        assert len(working_array) == 3  # some vertices might have 5 faces?
        ret = []  # type: List
        print([x.is_adjacent_to(y)
               for x, y in product(working_array, working_array)])
        for i in range(len(self.faces)):
            if i == 0:
                ret.append(working_array.pop(i))
            else:
                print("Finding next faces {}".format(i))
                hit = False  # type: bool
                j = 0  # type: int
                while j < len(working_array) and not hit:
                    print("Trial {}".format(j))
                    if working_array[j].is_adjacent_to(ret[i - 1]):
                        print("HIT!")
                        hit = True
                        ret.append(working_array.pop(j))
                    j += 1
                assert hit
        return ret

    def find_common_face(self, other: 'Point', not_this_face):
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
