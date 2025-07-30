import dataclasses
import decimal
import math
from functools import cached_property
from typing import Optional, List, Tuple
from javaobj import JavaObject
from shapely.geometry import Polygon

from .Color import Color
from .HasLevel import HasLevel
from .Level import Level
from .Content import Content
from .Renderable import Renderable
from .TextStyle import TextStyle
from .HomeMaterial import HomeMaterial
from .HomeTexture import HomeTexture
from .ModelBase import ModelBase
from .TextureImage import TextureImage
from ..AssetManager import AssetManager

@dataclasses.dataclass
class HomePieceOfFurniture(ModelBase, Renderable, HasLevel):
    identifier: str
    name_visible: bool
    name_x_offset: float
    name_y_offset: float
    name_angle: float
    width: float
    depth: float
    height: float
    elevation: float
    movable: bool
    is_door_or_window: bool
    back_face_shown: bool
    resizable: bool
    deformable: bool
    texturable: bool
    is_visible: bool
    x: float
    y: float
    angle: float
    is_model_mirrored: bool
    height_in_plan: float
    name_style: Optional[TextStyle] = None
    description: Optional[str] = None
    icon: Optional[TextureImage] = None
    plan_icon: Optional[TextureImage] = None
    model: Optional[Content] = None
    model_materials: Optional[List[HomeMaterial]] = None
    color: Optional[Color] = None
    texture: Optional[HomeTexture] = None
    shininess: Optional[float] = None
    model_rotation: Optional[List[List[float]]] = None
    staircase_cut_out_shape: Optional[str] = None
    price: Optional[decimal.Decimal] = None
    value_added_tax_percentage: Optional[decimal.Decimal] = None
    currency: Optional[str] = None
    catalog_id: Optional[str] = None
    name: Optional[str] = None
    level: Optional[Level] = None

    @cached_property
    def geometry(self) -> Polygon:
        svg_x = self.x - (self.width / 2)
        svg_y = self.y - (self.depth / 2)

        height = self.depth

        corners = [
            (svg_x, svg_y),  # top-left
            (svg_x + self.width, svg_y),  # top-right
            (svg_x + self.width, svg_y + height),  # bottom-right
            (svg_x, svg_y + height)  # bottom-left
        ]

        def rotate(px, py):
            dx = px - self.x
            dy = py - self.y
            cos_a = math.cos(self.angle)
            sin_a = math.sin(self.angle)
            return (
                self.x + dx * cos_a - dy * sin_a,
                self.y + dx * sin_a + dy * cos_a
            )

        rotated_corners = [rotate(px, py) for (px, py) in corners]
        return Polygon(rotated_corners)

    @property
    def points(self) -> List[Tuple[float, float]]:
        return list(self.geometry.exterior.coords)

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True

        if self.level and level:
            piece_level_elevation = self.level.elevation
            level_elevation = level.elevation
            if piece_level_elevation == level_elevation and self.level.elevation_index < level.elevation_index:
                return True

            if piece_level_elevation < level_elevation and self._is_top_at_level(level):
                return True

        return False

    def _is_top_at_level(self, level: Level) -> bool:
        if not self.level:
            return False
        top_elevation = self.level.elevation + self.elevation + self.height_in_plan
        if self.staircase_cut_out_shape:
            return top_elevation >= level.elevation

        return top_elevation > level.elevation


    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'HomePieceOfFurniture':
        icon_content = asset_manager.get_asset_by_uri(o.icon.url.file) if o.icon else None
        plan_icon_content = asset_manager.get_asset_by_uri(o.planIcon.url.file) if o.planIcon else None

        return cls(
            identifier=o.id,
            catalog_id=o.catalogId,
            name=o.name,
            name_visible=o.nameVisible,
            name_x_offset=o.nameXOffset,
            name_y_offset=o.nameYOffset,
            name_style=TextStyle.from_javaobj(o.nameStyle, asset_manager) if o.nameStyle else None,
            name_angle=o.nameAngle,
            description=o.description,
            height_in_plan=o.heightInPlan,
            icon=TextureImage.from_content(icon_content) if icon_content else None,
            plan_icon=TextureImage.from_content(plan_icon_content) if plan_icon_content else None,
            model=asset_manager.get_asset_by_uri(o.model.url.file) if o.model else None,
            width=o.width,
            depth=o.depth,
            height=o.height,
            elevation=o.elevation,
            movable=o.movable,
            is_door_or_window=o.doorOrWindow,
            model_materials=[HomeMaterial.from_javaobj(hmo, asset_manager) for hmo in o.modelMaterials] if o.modelMaterials else None,
            color=Color.from_argb_interger(o.color) if o.color else None,
            texture=HomeTexture.from_javaobj(o.texture, asset_manager) if o.texture else None,
            shininess=o.shininess,
            model_rotation=o.modelRotation,
            staircase_cut_out_shape=o.staircaseCutOutShape,
            back_face_shown=o.backFaceShown,
            resizable=o.resizable,
            deformable=o.deformable,
            texturable=o.texturable,
            price=o.price,
            value_added_tax_percentage=o.valueAddedTaxPercentage,
            currency=o.currency,
            is_visible=o.visible,
            x=o.x,
            y=o.y,
            angle=o.angle,
            is_model_mirrored=o.modelMirrored,
            level=Level.from_javaobj(o.level, asset_manager) if o.level else None
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'HomePieceOfFurniture':
        icon = data.get('@icon')
        model = data.get('@model')
        level_identifier = data.get('@level')

        return cls(
            identifier=cls.required_str(data.get('@id')),
            catalog_id=data.get('@catalogId'),
            name=data.get('@name'),
            name_visible=True,
            name_x_offset=0.0,
            name_y_offset=0.0,
            name_style=None,
            name_angle=0.0,
            description=None,
            height_in_plan=cls.required_float(data.get('@heightInPlan', '-infinity')),
            icon=TextureImage.from_content(asset_manager.get_asset(icon)) if icon else None,
            plan_icon=None,
            model=asset_manager.get_asset(model) if model else None,
            width=cls.required_float(data.get('@width')),
            depth=cls.required_float(data.get('@depth')),
            height=cls.required_float(data.get('@height')),
            elevation=0.0,
            movable=False,
            is_door_or_window=False,
            model_materials=None,
            color=None,
            texture=None,
            shininess=0.0,
            model_rotation=None,
            staircase_cut_out_shape=None,
            back_face_shown=False,
            resizable=False,
            deformable=False,
            texturable=False,
            price=None,
            value_added_tax_percentage=None,
            currency=None,
            is_visible=True,
            x=cls.required_float(data.get('@x')),
            y=cls.required_float(data.get('@y')),
            angle=cls.required_float(data.get('@angle', '0.0')),
            is_model_mirrored=False,
            level=Level.from_identifier(level_identifier) if level_identifier else None
        )
