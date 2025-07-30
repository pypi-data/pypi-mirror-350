import dataclasses
import math
from functools import cached_property
from typing import Union, TYPE_CHECKING, List
from javaobj import JavaObject
from shapely.geometry.linestring import LineString
from shapely.geometry.polygon import Polygon
from shapely.affinity import rotate, translate

from sh3d.AssetManager import AssetManager
from sh3d.geometry import arc, ArcTypeEnum
from .Renderable import Renderable, PointType
from .ModelBase import ModelBase

if TYPE_CHECKING:
    from .HomeDoorOrWindow import HomeDoorOrWindow


@dataclasses.dataclass
class Sash(Renderable):
    door_or_window: 'HomeDoorOrWindow'
    x_axis: float
    y_axis: float
    width: float
    start_angle: float
    end_angle: float

    @cached_property
    def geometry(self) -> Union[LineString, Polygon]:
        model_mirrored_sign = -1 if self.door_or_window.is_model_mirrored else 1

        # Compute arc positioning and size
        x_axis = model_mirrored_sign * self.x_axis * self.door_or_window.width
        y_axis = self.y_axis * self.door_or_window.depth
        sash_width = self.width * self.door_or_window.width

        # Convert start angle to degrees
        start_angle_deg = math.degrees(self.start_angle)

        if self.door_or_window.is_model_mirrored:
            start_angle_deg = 180 - start_angle_deg

        # Compute extent angle
        extent_angle_deg = model_mirrored_sign * math.degrees(
            self.end_angle - self.start_angle
        )

        # Create arc shape (as Polygon for PIE)
        arc_shape = arc(
            x=x_axis - sash_width,
            y=y_axis - sash_width,
            width=2 * sash_width,
            height=2 * sash_width,
            start_angle_deg=start_angle_deg,
            arc_angle_deg=extent_angle_deg,
            arc_type=ArcTypeEnum.PIE
        )

        # Apply transformation: translate to (x, y), rotate, then align center
        shape = translate(arc_shape, xoff=model_mirrored_sign * -self.door_or_window.width / 2,
                          yoff=-self.door_or_window.depth / 2)
        shape = rotate(shape, angle=self.door_or_window.angle, origin=(0, 0), use_radians=True)
        return translate(shape, xoff=self.door_or_window.x, yoff=self.door_or_window.y)

    @property
    def points(self) -> List[PointType]:
        return list(self.geometry.exterior.coords)

    @points.setter
    def points(self, points: List[PointType]) -> None:
        raise NotImplementedError

    @classmethod
    def from_javaobj(cls, door_or_window: 'HomeDoorOrWindow', o: JavaObject, _asset_manager: AssetManager) -> 'Sash':
        return cls(
            door_or_window=door_or_window,
            x_axis=o.xAxis,
            y_axis=o.yAxis,
            width=o.width,
            start_angle=o.startAngle,
            end_angle=o.endAngle,
        )

    @classmethod
    def from_xml_dict(cls, door_or_window: 'HomeDoorOrWindow', data: dict, _asset_manager: AssetManager) -> 'Sash':
        return cls(
            door_or_window=door_or_window,
            x_axis=ModelBase.required_float(data.get('@xAxis')),
            y_axis=ModelBase.required_float(data.get('@yAxis')),
            width=ModelBase.required_float(data.get('@width')),
            start_angle=ModelBase.required_float(data.get('@startAngle')),
            end_angle=ModelBase.required_float(data.get('@endAngle'))
        )
