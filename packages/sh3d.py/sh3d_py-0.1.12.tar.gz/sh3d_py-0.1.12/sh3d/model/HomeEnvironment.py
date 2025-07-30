import dataclasses
from typing import Optional
from javaobj import JavaObject
from .HomeTexture import HomeTexture
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


@dataclasses.dataclass
class HomeEnvironment(ModelBase):
    observer_camera_elevation_adjusted: bool
    ground_color: int
    ground_texture: Optional['HomeTexture']
    sky_color: int
    sky_texture: Optional['HomeTexture']
    light_color: int
    ceiling_light_color: int
    walls_alpha: float
    subpart_size_under_light: float
    all_levels_visible: bool
    photo_width: int
    photo_height: int
    photo_aspect_ratio_name: Optional[str]
    photo_quality: int
    video_width: int
    video_aspect_ratio_name: Optional[str]
    video_quality: int
    video_frame_rate: int

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'HomeEnvironment':
        return cls(
            observer_camera_elevation_adjusted=o.observerCameraElevationAdjusted,
            ground_color=o.groundColor,
            ground_texture=HomeTexture.from_javaobj(o.groundTexture, asset_manager) if o.groundTexture else None,
            sky_color=o.skyColor,
            sky_texture=HomeTexture.from_javaobj(o.skyTexture, asset_manager) if o.skyTexture else None,
            light_color=o.lightColor,
            ceiling_light_color=o.ceilingLightColor,
            walls_alpha=o.wallsAlpha,
            subpart_size_under_light=o.subpartSizeUnderLight,
            all_levels_visible=o.allLevelsVisible,
            photo_width=o.photoWidth,
            photo_height=o.photoHeight,
            photo_aspect_ratio_name=o.photoAspectRatioName,
            photo_quality=o.photoQuality,
            video_width=o.videoWidth,
            video_aspect_ratio_name=o.videoAspectRatioName,
            video_quality=o.videoQuality,
            video_frame_rate=o.videoFrameRate
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'HomeEnvironment':
        ground_texture = data.get('@groundTexture')
        sky_texture = data.get('@skyTexture')

        return cls(
            observer_camera_elevation_adjusted=False,
            ground_color=data.get('@groundColor'),
            ground_texture=HomeTexture.from_xml_dict(ground_texture, asset_manager) if ground_texture else None,
            sky_color=data.get('@skyColor'),
            sky_texture=HomeTexture.from_xml_dict(sky_texture, asset_manager) if sky_texture else None,
            light_color=data.get('@lightColor'),
            ceiling_light_color=data.get('@ceillingLightColor'),
            walls_alpha=0.0,
            subpart_size_under_light=0.0,
            all_levels_visible=True,
            photo_width=cls.required_int(data.get('@photoWidth')),
            photo_height=cls.required_int(data.get('@photoHeight')),
            photo_aspect_ratio_name=data.get('@photoAspectRatio'),
            photo_quality=data.get('@photoQuality'),
            video_width=data.get('@videoWidth'),
            video_aspect_ratio_name=data.get('@videoAspectRatio'),
            video_quality=data.get('@videoQuality'),
            video_frame_rate=data.get('@videoFrameRate')
        )
