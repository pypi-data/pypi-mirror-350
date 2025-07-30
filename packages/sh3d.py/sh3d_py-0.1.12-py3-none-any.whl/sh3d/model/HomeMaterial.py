import dataclasses
from typing import Optional
from javaobj import JavaObject
from .HomeTexture import HomeTexture
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


@dataclasses.dataclass
class HomeMaterial(ModelBase):
    name: str
    color: Optional[int]
    texture: Optional[HomeTexture]
    shininess: Optional[float]

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'HomeMaterial':
        return cls(
            name=o.name,
            color=o.color,
            texture=HomeTexture.from_javaobj(o.texture, asset_manager) if o.texture else None,
            shininess=o.shininess,
        )
