import dataclasses
from typing import Optional
from zoneinfo import ZoneInfo
from javaobj import JavaObject
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


@dataclasses.dataclass
class Compass(ModelBase):
    x: float
    y: float
    diameter: float
    visible: bool
    north_direction: float
    latitude: float
    longitude: float
    time_zone: Optional[ZoneInfo]

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Compass':
        return cls(
            x=o.x,
            y=o.y,
            diameter=o.diameter,
            visible=o.visible,
            north_direction=o.northDirection,
            latitude=o.latitude,
            longitude=o.longitude,
            time_zone=ZoneInfo(o.timeZone.ID)
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Compass':
        time_zone = data.get('@timeZone')
        if not time_zone:
            raise ValueError('TimeZone is required')

        return cls(
            x=cls.required_float(data.get('@x')),
            y=cls.required_float(data.get('@y')),
            diameter=cls.required_float(data.get('@diameter')),
            visible=True,
            north_direction=cls.required_float(data.get('@northDirection')),
            latitude=cls.required_float(data.get('@latitude')),
            longitude=cls.required_float(data.get('@longitude')),
            time_zone=ZoneInfo(time_zone)
        )
