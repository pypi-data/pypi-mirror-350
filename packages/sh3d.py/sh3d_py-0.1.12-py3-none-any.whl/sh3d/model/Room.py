from dataclasses import dataclass
from functools import cached_property
from typing import Optional, List
from javaobj import JavaObject
from shapely.geometry.polygon import Polygon

from .HasLevel import HasLevel
from .Renderable import Renderable, PointType
from .TextStyle import TextStyle, Alignment
from .HomeTexture import HomeTexture
from .Level import Level
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


DEFAULT_ROOM_TEXT_STYLE = TextStyle(
    font_size=24,
    bold=False,
    italic=False,
    alignment=Alignment.CENTER
)

@dataclass
class Room(ModelBase, Renderable, HasLevel):
    identifier: str
    name_x_offset: float
    name_y_offset: float
    is_area_visible: bool
    area_x_offset: float
    area_y_offset: float
    name_angle: float
    area_angle: float
    floor_visible: bool
    floor_shininess: float
    ceiling_visible: bool
    ceiling_shininess: float
    name_style: TextStyle
    area_style: TextStyle
    points: List[PointType]
    name: Optional[str] = None
    floor_color: Optional[int] = None
    floor_texture: Optional[HomeTexture] = None
    ceiling_color: Optional[int] = None
    ceiling_texture: Optional[HomeTexture] = None
    level: Optional[Level] = None

    @cached_property
    def x_center(self) -> float:
        x_coords = [p[0] for p in self.points]
        x_min = min(x_coords)
        x_max = max(x_coords)
        return (x_min + x_max) / 2

    @cached_property
    def y_center(self) -> float:
        y_coords = [p[1] for p in self.points]
        y_min = min(y_coords)
        y_max = max(y_coords)
        return (y_min + y_max) / 2


    @cached_property
    def area(self) -> float:
        return self.geometry.area

    @cached_property
    def geometry(self) -> Polygon:
        return Polygon(self.points)

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True

        if not self.level or not level:
            return False

        return self.level.elevation == level.elevation and self.level.elevation_index < level.elevation_index

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Room':
        return cls(
            identifier=o.id,
            name=o.name.strip() if o.name else None,
            name_x_offset=o.nameXOffset,
            name_y_offset=o.nameYOffset,
            name_style=TextStyle.from_javaobj(o.nameStyle, asset_manager) if o.nameStyle else DEFAULT_ROOM_TEXT_STYLE,
            name_angle=o.nameAngle,
            points=o.points,
            is_area_visible=o.areaVisible,
            area_x_offset=o.areaXOffset,
            area_y_offset=o.areaYOffset,
            area_style=TextStyle.from_javaobj(o.areaStyle, asset_manager) if o.areaStyle else DEFAULT_ROOM_TEXT_STYLE,
            area_angle=o.areaAngle,
            floor_visible=o.floorVisible,
            floor_color=o.floorColor,
            floor_texture=HomeTexture.from_javaobj(o.floorTexture, asset_manager) if o.floorTexture else None,
            floor_shininess=o.floorShininess,
            ceiling_visible=o.ceilingVisible,
            ceiling_color=o.ceilingColor,
            ceiling_texture=HomeTexture.from_javaobj(o.ceilingTexture, asset_manager) if o.ceilingTexture else None,
            ceiling_shininess=o.ceilingShininess,
            level=Level.from_javaobj(o.level, asset_manager) if o.level else None
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Room':
        level_identifier = data.get('@level')
        points = data.get('point')
        return cls(
            identifier=cls.required_str(data.get('@id')),
            name=data.get('@name'),
            name_x_offset=0.0,
            name_y_offset=-40.0,
            name_style=DEFAULT_ROOM_TEXT_STYLE,
            name_angle=0.0,
            points=[[float(point.get('@x')), float(point.get('@y'))] for point in points],
            is_area_visible=data.get('@areaVisible') == 'true',
            area_x_offset=0.0,
            area_y_offset=0.0,
            area_style=DEFAULT_ROOM_TEXT_STYLE,
            area_angle=0.0,
            floor_visible=True,
            floor_color=0,
            floor_texture=None,
            floor_shininess=0.0,
            ceiling_visible=False,
            ceiling_color=0,
            ceiling_texture=None,
            ceiling_shininess=0.0,
            level=Level.from_identifier(level_identifier) if level_identifier else None
        )
