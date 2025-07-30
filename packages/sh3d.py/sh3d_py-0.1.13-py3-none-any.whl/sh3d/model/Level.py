import dataclasses
import weakref
from typing import Optional
from javaobj import JavaObject
from .BackgroundImage import BackgroundImage
from .ModelBase import ModelBase
from ..AssetManager import AssetManager

_level_cache = weakref.WeakValueDictionary()

@dataclasses.dataclass(unsafe_hash=True)
class Level(ModelBase):
    identifier: str
    name: str
    elevation: float
    floor_thickness: float
    height: float
    background_image: Optional[BackgroundImage]
    is_visible: bool
    is_viewable: bool
    elevation_index: int

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Level':
        identifier = o.id
        if identifier in _level_cache:
            return _level_cache[identifier]

        level = cls(
            identifier=identifier,
            name=o.name,
            elevation=o.elevation,
            floor_thickness=o.floorThickness,
            height=o.height,
            background_image=BackgroundImage.from_javaobj(o.backgroundImage, asset_manager) if o.backgroundImage else None,
            is_visible=o.visible,
            is_viewable=o.viewable,
            elevation_index=o.elevationIndex
        )

        _level_cache[identifier] = level

        return level

    @classmethod
    def from_identifier(cls, identifier: str) -> 'Level':
        wall = _level_cache.get(identifier)
        if not wall:
            raise ValueError('Identifier not found in cache')
        return wall

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Level':
        identifier = data.get('@id')
        if not identifier:
            raise ValueError('@id is required')
        background_image = data.get('backgroundImage')
        if identifier in _level_cache:
            return _level_cache[identifier]

        level = cls(
            identifier=identifier,
            name=cls.required_str(data.get('@name')),
            elevation=cls.required_float(data.get('@elevation')),
            floor_thickness=cls.required_float(data.get('@floorThickness')),
            height=cls.required_float(data.get('@height')),
            background_image=BackgroundImage.from_xml_dict(background_image, asset_manager) if background_image else None,
            is_visible=data.get('@visible', 'true') == 'true',
            is_viewable=data.get('@viewable', 'true') == 'true',
            elevation_index=cls.required_int(data.get('@elevationIndex'))
        )

        _level_cache[identifier] = level

        return level
