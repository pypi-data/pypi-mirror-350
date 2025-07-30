import dataclasses
import io
import math
from functools import cached_property
from PIL import Image
from PIL.ImageFile import ImageFile
from javaobj import JavaObject
from .Content import Content
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


@dataclasses.dataclass
class BackgroundImage(ModelBase):
    image: Content
    scale_distance: float
    scale_distance_x_start: float
    scale_distance_y_start: float
    scale_distance_x_end: float
    scale_distance_y_end: float
    x_origin: float
    y_origin: float
    invisible: bool

    @cached_property
    def image_info(self) -> ImageFile:
        return Image.open(io.BytesIO(self.image.data))

    @cached_property
    def scale(self) -> float:
        dx = self.scale_distance_x_end - self.scale_distance_x_start
        dy = self.scale_distance_y_end - self.scale_distance_y_start
        pixel_distance = math.hypot(dx, dy)

        # Calculate the scale factor
        return self.scale_distance / pixel_distance


    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'BackgroundImage':
        image = asset_manager.get_asset_by_uri(o.image.url.file)
        if not image:
            raise ValueError('Image was not found in data')
        return cls(
            image=image,
            scale_distance=o.scaleDistance,
            scale_distance_x_start=o.scaleDistanceXStart,
            scale_distance_y_start=o.scaleDistanceYStart,
            scale_distance_x_end=o.scaleDistanceXEnd,
            scale_distance_y_end=o.scaleDistanceYEnd,
            x_origin=o.xOrigin,
            y_origin=o.yOrigin,
            invisible=o.invisible,
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'BackgroundImage':
        image = data.get('@image')
        if not image:
            raise ValueError('image is not provided')

        image_content = asset_manager.get_asset(image)
        if not image_content:
            raise ValueError('Content was not found')

        return cls(
            image=image_content,
            scale_distance=cls.required_float(data.get('@scaleDistance')),
            scale_distance_x_start=cls.required_float(data.get('@scaleDistanceXStart')),
            scale_distance_y_start=cls.required_float(data.get('@scaleDistanceYStart')),
            scale_distance_x_end=cls.required_float(data.get('@scaleDistanceXEnd')),
            scale_distance_y_end=cls.required_float(data.get('@scaleDistanceYEnd')),
            x_origin=cls.required_float(data.get('@xOrigin')),
            y_origin=cls.required_float(data.get('@yOrigin')),
            invisible=False,
        )
