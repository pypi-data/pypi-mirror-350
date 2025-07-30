import enum
from typing import Optional, List, Union
from dataclasses import dataclass
from functools import cached_property
import numpy as np
from javaobj import JavaObject
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString

from .Color import Color
from .HasLevel import HasLevel
from .Renderable import Renderable, PointType
from .Level import Level
from .ModelBase import ModelBase
from ..AssetManager import AssetManager

@enum.unique
class CapStyle(enum.Enum):
    BUTT = 'BUTT'
    SQUARE = 'SQUARE'
    ROUND = 'ROUND'


@enum.unique
class JoinStyle(enum.Enum):
    BEVEL = 'BEVEL'
    MITER = 'MITER'
    ROUND = 'ROUND'
    CURVED = 'CURVED'

@enum.unique
class ArrowStyle(enum.Enum):
    NONE = 'NONE'
    DELTA = 'DELTA'
    OPEN = 'OPEN'
    DISC = 'DISC'

@enum.unique
class DashStyle(enum.Enum):
    SOLID = 'SOLID'
    DOT = 'DOT'
    DASH = 'DASH'
    DASH_DOT = 'DASH_DOT'
    DASH_DOT_DOT = 'DASH_DOT_DOT'
    CUSTOMIZED = 'CUSTOMIZED'


    @property
    def dash_pattern(self) -> Optional[List[float]]:
        return {
            DashStyle.SOLID: [1.0, 0.0],
            DashStyle.DOT: [1.0, 1.0],
            DashStyle.DASH: [4.0, 2.0],
            DashStyle.DASH_DOT: [8.0, 2.0, 2.0, 2.0],
            DashStyle.DASH_DOT_DOT: [8.0, 2.0, 2.0, 2.0, 2.0, 2.0],
        }.get(self)




@dataclass
class Polyline(ModelBase, Renderable, HasLevel):
    identifier: str

    thickness: float
    cap_style_name: str
    join_style_name: str
    dash_style_name: str
    dash_pattern: List[float]
    dash_offset: float
    start_arrow_style_name: str
    end_arrow_style_name: str
    is_closed_path: bool
    color: Color
    elevation: float
    points: List[PointType]
    cap_style: CapStyle = CapStyle.BUTT
    join_style: JoinStyle = JoinStyle.MITER
    dash_style: DashStyle = DashStyle.SOLID
    start_arrow_style: ArrowStyle = ArrowStyle.NONE
    end_arrow_style: ArrowStyle = ArrowStyle.NONE
    level: Optional[Level] = None

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Polyline':
        return cls(
            identifier=o.id,
            points=o.points,
            thickness=o.thickness,
            cap_style=CapStyle(o.capStyleName) if o.capStyleName else CapStyle.BUTT,
            cap_style_name=o.capStyleName,
            join_style=JoinStyle(o.joinStyleName) if o.joinStyleName else JoinStyle.MITER,
            join_style_name=o.joinStyleName,
            dash_style=DashStyle(o.dashStyleName) if o.dashStyleName else DashStyle.SOLID,
            dash_style_name=o.dashStyleName,
            dash_pattern=o.dashPattern if o.dashPattern else DashStyle(o.dashStyleName).dash_pattern if o.dashStyleName else None,
            dash_offset=o.dashOffset,
            start_arrow_style=ArrowStyle(o.startArrowStyleName) if o.startArrowStyleName else None,
            start_arrow_style_name=o.startArrowStyleName,
            end_arrow_style=ArrowStyle(o.endArrowStyleName) if o.endArrowStyleName else None,
            end_arrow_style_name=o.endArrowStyleName,
            is_closed_path=o.closedPath,
            color=Color.from_argb_interger(o.color) if o.color else None,
            elevation=o.elevation,
            level=Level.from_javaobj(o.level, asset_manager) if o.level else None
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Polyline':
        points = data.get('point')
        cap_style_name = data.get('@capStyle')
        join_style_name = data.get('@joinStyle')
        dash_style_name = data.get('@dashStyle')
        dash_pattern = data.get('@dashPattern')
        start_arrow_style_name = data.get('@startArrowStyle')
        end_arrow_style_name = data.get('@endArrowStyle')
        color = data.get('@color')
        level_identifier = data.get('@level')
        return cls(
            identifier=data.get('@id'),
            points=[[float(point.get('@x')), float(point.get('@y'))] for point in points],
            thickness=cls.required_float(data.get('@thickness')),
            cap_style=CapStyle(cap_style_name) if cap_style_name else CapStyle.BUTT,
            cap_style_name=cap_style_name,
            join_style=JoinStyle(join_style_name) if join_style_name else JoinStyle.MITER,
            join_style_name=join_style_name,
            dash_style=DashStyle(dash_style_name) if dash_style_name else DashStyle.SOLID,
            dash_style_name=dash_style_name,
            dash_pattern=dash_pattern if dash_pattern else DashStyle(dash_style_name).dash_pattern if dash_style_name else None,
            dash_offset=data.get('@dashOffset'),
            start_arrow_style=ArrowStyle(start_arrow_style_name) if start_arrow_style_name else None,
            start_arrow_style_name=start_arrow_style_name,
            end_arrow_style=ArrowStyle(end_arrow_style_name) if end_arrow_style_name else None,
            end_arrow_style_name=end_arrow_style_name,
            is_closed_path=data.get('@closedPath', False),
            color=Color.from_hexa(color) if color else None,
            elevation=data.get('@elevation'),
            level=Level.from_identifier(level_identifier) if level_identifier else None
        )


    @cached_property
    def polyline_path(self) -> Union[LineString | Polygon]:

        points = self.points
        n = len(points)
        path_points = []

        if self.join_style == JoinStyle.CURVED:
            def cubic_bezier(p0: np.ndarray, c1: np.ndarray, c2: np.ndarray, p1: np.ndarray, steps: int =20) -> np.ndarray:
                t = np.linspace(0, 1, steps)
                curve = (1 - t)[:, None] ** 3 * p0 + \
                        3 * (1 - t)[:, None] ** 2 * t[:, None] * c1 + \
                        3 * (1 - t)[:, None] * t[:, None] ** 2 * c2 + \
                        t[:, None] ** 3 * p1
                return curve

            limit = n if self.is_closed_path else n - 1
            for i in range(limit):
                prev_idx = (i - 1) % n
                next_idx = (i + 1) % n
                next_next_idx = (i + 2) % n

                prev = np.array(points[prev_idx])
                curr = np.array(points[i])
                next_pt = np.array(points[next_idx])
                next_next = np.array(points[next_next_idx])

                v1 = (next_pt - prev) / 3.625 if i != 0 or self.is_closed_path else np.zeros(2)
                v2 = (curr - next_next) / 3.625 if i != n - 2 or self.is_closed_path else np.zeros(2)

                control1 = curr + v1
                control2 = next_pt + v2
                bezier = cubic_bezier(curr, control1, control2, next_pt)

                path_points.extend(bezier.tolist())

            if self.is_closed_path:
                path_points.append(path_points[0])  # close it manually
            return LineString(path_points)

        if self.is_closed_path:
            return Polygon(points)

        return LineString(points)

    @property
    def geometry(self) -> Polygon:
        cap_style = {
            CapStyle.ROUND: 'round',
            CapStyle.SQUARE: 'square',
            CapStyle.BUTT: 'flat'
        }.get(self.cap_style, 'round')

        join_style = {
            JoinStyle.ROUND: 'round',
            JoinStyle.MITER: 'mitre',
            JoinStyle.BEVEL: 'bevel'
        }.get(self.join_style, 'round')

        return self.polyline_path.buffer(self.thickness, cap_style=cap_style, join_style=join_style)

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True

        if self.level and level:
            dimension_line_level_elevation = self.level.elevation
            level_elevation = level.elevation
            return dimension_line_level_elevation == level_elevation and self.level.elevation_index < level.elevation_index

        return False
