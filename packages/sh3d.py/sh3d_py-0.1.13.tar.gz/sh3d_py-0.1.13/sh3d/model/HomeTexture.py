import dataclasses
from javaobj import JavaObject
from .Content import Content
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


@dataclasses.dataclass(frozen=True)
class HomeTexture(ModelBase):
    name: str
    image: Content
    width: float
    height: float
    left_to_right_oriented: bool

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'HomeTexture':
        return cls(
            name=o.name,
            image=asset_manager.get_texture(o.name),
            width=o.width,
            height=o.height,
            left_to_right_oriented=o.left_to_right_oriented
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'HomeTexture':
        raise NotImplementedError
        #return cls(
        #    name=data.get('@name'),
        #    image=None,
        #    width=float(data.get('@width')),
        #    height=float(data.get('@height')),
        #    left_to_right_oriented=False
        #)
