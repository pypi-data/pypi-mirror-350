import math
import enum
import dataclasses
from typing import Union

from shapely.geometry.linestring import LineString
from shapely.geometry.polygon import Polygon

@enum.unique
class ArcTypeEnum(enum.Enum):
    OPEN = 'OPEN'
    CHORD = 'CHORD'
    PIE = 'PIE'

def arc(
        x: float,
        y: float,
        width: float,
        height: float,
        start_angle_deg: float,
        arc_angle_deg: float,
        arc_type: ArcTypeEnum=ArcTypeEnum.OPEN,
        num_points: int=32
) -> Union[LineString, Polygon]:
    cx = x + width / 2
    cy = y + height / 2
    rx = width / 2
    ry = height / 2

    start_rad = math.radians(start_angle_deg)
    end_rad = math.radians(start_angle_deg + arc_angle_deg)

    # Normalize angle range for clockwise or counter-clockwise
    angle_step = (end_rad - start_rad) / num_points

    points = [
        (
            cx + rx * math.cos(start_rad + i * angle_step),
            cy - ry * math.sin(start_rad + i * angle_step)
        )
        for i in range(num_points + 1)
    ]

    if arc_type == ArcTypeEnum.OPEN:
        return LineString(points)

    if arc_type == ArcTypeEnum.CHORD:
        # Add straight line from end to start to close with a chord
        return LineString(points + [points[0]])

    if arc_type == ArcTypeEnum.PIE:
        # Add center and return as filled sector
        return Polygon([ (cx, cy) ] + points + [ (cx, cy) ])

    raise ValueError(f"Unsupported arc type: {arc_type}")

@dataclasses.dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float

    @property
    def max_x(self) -> float:
        return self.x + self.width

    @property
    def max_y(self) -> float:
        return self.y + self.height

    def add(self, new_x: float, new_y: float) -> None:
        # Expand bounds to include point (px, py)
        self.x = min(self.x, new_x)
        self.y =  min(self.y, new_y)
        self.width = max(self.max_x, new_x) - self.x
        self.height = max(self.max_y, new_y) - self.y


    def add_rectangle(self, rect: 'Rectangle') -> None:
        x1 = min(self.x, rect.x)
        x2 = max(self.max_x, rect.max_x)
        y1 = min(self.y, rect.y)
        y2 = max(self.max_y, rect.max_y)

        self.x = x1
        self.y = y1
        self.width = x2 - x1
        self.height =  y2 - y1


    def to_polygon(self) -> Polygon:
        return Polygon([
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
            (self.x, self.y)  # Close the polygon
        ])
