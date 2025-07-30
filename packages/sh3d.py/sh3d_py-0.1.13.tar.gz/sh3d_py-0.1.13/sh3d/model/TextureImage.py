import io
import weakref
import dataclasses
from typing import Any
from PIL import Image
from javaobj import JavaObject
from .Content import Content
from ..AssetManager import AssetManager
from .ModelBase import ModelBase


@dataclasses.dataclass(frozen=True)
class TextureImage(ModelBase):
    _instances = weakref.WeakValueDictionary()
    name: str
    image: Content
    width: float
    height: float

    def __new__(cls, name: str, *_args: Any, **_kwargs: Any) -> 'TextureImage':
        if name in cls._instances:
            return cls._instances[name]
        instance = super().__new__(cls)
        cls._instances[name] = instance
        return instance

    @classmethod
    def from_content(cls, content: Content) -> 'TextureImage':
        image_info = Image.open(io.BytesIO(content.data))
        return cls(
            name=content.content_digest.name,
            image=content,
            width=image_info.width,
            height=image_info.height
        )

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'TextureImage':
        image = asset_manager.get_pattern(o.name)
        image_info = Image.open(io.BytesIO(image.data))

        return cls(
            name=o.name,
            image=image,
            width=image_info.width,
            height=image_info.height
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'ModelBase':
        raise NotImplementedError

    @classmethod
    def from_str(cls, pattern_name: str, asset_manager: AssetManager) -> 'TextureImage':
        image = asset_manager.get_pattern(pattern_name)
        image_info = Image.open(io.BytesIO(image.data))
        return cls(
            name=pattern_name,
            image=image,
            width=image_info.width,
            height=image_info.height
        )
