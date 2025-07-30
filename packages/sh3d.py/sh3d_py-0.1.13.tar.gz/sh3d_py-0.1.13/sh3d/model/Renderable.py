from functools import cached_property
from typing import List, Tuple, Union
from shapely.geometry.base import BaseGeometry

PointTypeFixed = Tuple[float, float]
PointTypeEditable = List[float]

PointType = Union[PointTypeFixed, PointTypeEditable]

class Renderable:
    identifier: str
    points: List[PointType]

    @cached_property
    def geometry(self) -> BaseGeometry:
        raise NotImplementedError
