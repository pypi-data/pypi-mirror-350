import math
from dataclasses import dataclass
from typing import Optional, List, Tuple

from javaobj import JavaObject
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point

from .Color import Color
from .HasLevel import HasLevel
from .Renderable import Renderable
from .TextStyle import TextStyle, Alignment
from .Level import Level
from .ModelBase import ModelBase
from ..AssetManager import AssetManager

DIMENSION_LINE_MARK_END = (
    'M -5 5',
    'L 5 -5',
    'M 0 5',
    'L 0 -5'
)

VERTICAL_DIMENSION_LINE_DISC = Point(0, 0).buffer(1.5)
VERTICAL_DIMENSION_LINE = Point(0, 0).buffer(5)
DEFAULT_TEXT_STYLE = TextStyle(18, False, False, Alignment.CENTER)

@dataclass
class DimensionLine(ModelBase, Renderable, HasLevel):
    identifier: str
    x_start: float
    y_start: float
    elevation_start: float
    x_end: float
    y_end: float
    elevation_end: float
    offset: float
    end_mark_size: float
    pitch: float
    length_style: TextStyle
    color: Color
    is_visible_in_3d: bool
    level: Optional[Level] = None

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'DimensionLine':
        return cls(
            identifier=o.id,
            x_start=o.xStart,
            y_start=o.yStart,
            elevation_start=o.elevationStart,
            x_end=o.xEnd,
            y_end=o.yEnd,
            elevation_end=o.elevationEnd,
            offset=o.offset,
            end_mark_size=o.endMarkSize,
            pitch=o.pitch,
            color=Color.from_argb_interger(int(o.color)) if o.color else Color.from_rgba(0,0,0,255),
            is_visible_in_3d=o.visibleIn3D,
            length_style=TextStyle.from_javaobj(o.lengthStyle, asset_manager) if o.lengthStyle else DEFAULT_TEXT_STYLE,
            level=Level.from_javaobj(o.level, asset_manager) if o.level else None
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'DimensionLine':
        text_style = data.get('textStyle')
        level_identifier = data.get('@level')
        elevation_end = data.get('@elevationEnd', '0.0')
        elevation_start = data.get('@elevationStart', '0.0')

        color = data.get('@color')
        return cls(
            identifier=data.get('@id'),
            x_start=cls.required_float(data.get('@xStart')),
            y_start=cls.required_float(data.get('@yStart')),
            elevation_start=cls.required_float(elevation_start),
            x_end=cls.required_float(data.get('@xEnd')),
            y_end=cls.required_float(data.get('@yEnd')),
            elevation_end=cls.required_float(elevation_end),
            offset=cls.required_float(data.get('@offset')),
            end_mark_size=cls.required_float(data.get('@endMarkSize', '10.0')),
            pitch=cls.required_float(data.get('@pitch', '0.0')),
            color=Color.from_hexa(color) if color else Color.from_rgba(0,0,0,255),
            is_visible_in_3d=data.get('@visibleIn3D', 'false') == 'true',
            length_style=TextStyle.from_xml_dict(text_style, asset_manager) if text_style else DEFAULT_TEXT_STYLE,
            level=Level.from_identifier(level_identifier) if level_identifier else None
        )


    @property
    def is_elevation_dimension_line(self) -> bool:
        return self.x_start == self.x_end and self.y_start == self.y_end and self.elevation_start != self.elevation_end

    @property
    def length(self) -> float:
        delta_x = self.x_end - self.x_start
        delta_y = self.y_end - self.y_start
        delta_elevation = self.elevation_end - self.elevation_start
        return math.sqrt(delta_x * delta_x + delta_y * delta_y + delta_elevation * delta_elevation)

    @property
    def points(self) -> List[Tuple[float, float]]:
        angle = self.pitch if self.is_elevation_dimension_line else math.atan2(self.y_end - self.y_start, self.x_end - self.x_start)
        dx = -math.sin(angle) * self.offset
        dy = math.cos(angle) * self.offset
        return [
            (self.x_start, self.y_start),
            (self.x_start + dx, self.y_start + dy),
            (self.x_end + dx, self.y_end + dy),
            (self.x_end, self.y_end)
        ]

    @property
    def geometry(self) -> Polygon:
        return Polygon(self.points)

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True

        if self.level and level:
            dimension_line_level_elevation = self.level.elevation
            level_elevation = level.elevation
            at_same_level = dimension_line_level_elevation == level_elevation and self.level.elevation_index < level.elevation_index
            in_same_level = dimension_line_level_elevation < level_elevation < dimension_line_level_elevation + max(self.elevation_start, self.elevation_end)
            return at_same_level or in_same_level

        return False
