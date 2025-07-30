import dataclasses
from typing import Optional, List, Tuple
from javaobj import JavaObject
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon

from .Color import Color
from .HasLevel import HasLevel
from .Renderable import Renderable
from .TextStyle import TextStyle, Alignment
from .Level import Level
from .ModelBase import ModelBase
from ..AssetManager import AssetManager

DEFAULT_TEXT_STYLE = TextStyle(
    font_size=18.0,
    bold=False,
    italic=False,
    alignment=Alignment.CENTER
)


@dataclasses.dataclass
class Label(ModelBase, Renderable, HasLevel):
    identifier: str
    text: str
    x: float
    y: float
    color: Color
    angle: float
    elevation: float
    style: TextStyle
    outline_color: Optional[Color] = None
    pitch: Optional[float] = None

    level: Optional[Level] = None

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Label':
        return cls(
            identifier=o.id,
            text=o.text,
            x=o.x,
            y=o.y,
            style=TextStyle.from_javaobj(o.style, asset_manager) if o.style else DEFAULT_TEXT_STYLE,
            color=Color.from_argb_interger(o.color) if o.color else Color.from_rgba(0, 0, 0, 255),
            outline_color=Color.from_argb_interger(o.outlineColor) if o.outlineColor else None,
            angle=o.angle,
            pitch=o.pitch,
            elevation=o.elevation,
            level=Level.from_javaobj(o.level, asset_manager) if o.level else None,
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Label':
        text_style = data.get('textStyle')
        color = data.get('@color')
        outline_color = data.get('@outlineColor')
        level_identifier = data.get('@level')
        pitch = data.get('@pitch')

        return cls(
            identifier=data.get('@id'),
            text=data.get('text'),
            x=float(data.get('@x')),
            y=float(data.get('@y')),
            style=TextStyle.from_xml_dict(text_style, asset_manager) if text_style else DEFAULT_TEXT_STYLE,
            color=Color.from_hexa(color) if color else Color.from_rgba(0, 0, 0, 255),
            outline_color=Color.from_hexa(outline_color) if outline_color else None,
            angle=float(data.get('@angle', '0.0')),
            pitch=float(pitch) if pitch else None,
            elevation=float(data.get('@elevation', '0.0')),
            level=Level.from_identifier(level_identifier) if level_identifier else None,
        )

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True

        if self.level and level:
            label_level_elevation = self.level.elevation
            level_elevation = level.elevation
            at_same_level = label_level_elevation == level_elevation and self.level.elevation_index < level.elevation_index
            in_same_level = label_level_elevation < level_elevation < label_level_elevation + self.elevation
            return at_same_level or in_same_level

        return False

    @property
    def points(self) -> List[Tuple[float, float]]:
        return [(self.x, self.y)]

    @property
    def geometry(self) -> Polygon:
        return Point(self.x, self.y).buffer(self.style.font_size)
