from typing import List, Tuple, Any
from javaobj import JavaObject
from .HomeMaterial import HomeMaterial
from .HomePieceOfFurniture import HomePieceOfFurniture
from .HomeTexture import HomeTexture
from .Level import Level
from .Sash import Sash
from .TextStyle import TextStyle
from .TextureImage import TextureImage
from ..AssetManager import AssetManager

DEFAULT_CUT_OUT_SHAPE: str = 'M0,0 v1 h1 v-1 z'


class HomeDoorOrWindow(HomePieceOfFurniture):
    sashes: List[Sash]
    wall_thickness: float
    width_depth_deformable: bool
    bound_to_wall: bool
    cut_out_shape: str
    wall_cut_out_on_both_sides: bool
    wall_distance: float
    wall_width: float
    wall_left: float
    wall_height: float
    wall_top: float

    @property
    def points(self) -> List[Tuple[float, float]]:
        raise NotImplementedError

    def __init__(
        self,
        sashes: List[Sash],
        cut_out_shape: str,
        *args: Any,
        wall_thickness: float = 0.0,
        width_depth_deformable: bool = False,
        bound_to_wall: bool = False,
        wall_cut_out_on_both_sides: bool = False,
        wall_distance: float = 0.0,
        wall_width: float = 1.0,
        wall_left: float = 0.0,
        wall_height: float = 1.0,
        wall_top: float = 0.0,
       **kwargs: Any
    ):
        self.sashes = sashes
        self.wall_thickness = wall_thickness
        self.width_depth_deformable = width_depth_deformable
        self.bound_to_wall = bound_to_wall
        self.cut_out_shape = cut_out_shape
        self.wall_cut_out_on_both_sides = wall_cut_out_on_both_sides
        self.wall_distance = wall_distance
        self.wall_width = wall_width
        self.wall_left = wall_left
        self.wall_height = wall_height
        self.wall_top = wall_top
        super().__init__(*args, **kwargs)

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'HomeDoorOrWindow':
        door_or_window = cls(
            # HomeDoorOrWindow
            sashes=[], # Is set later after class init
            wall_thickness=o.wallThickness,
            width_depth_deformable=o.widthDepthDeformable,
            bound_to_wall=o.boundToWall,
            cut_out_shape=o.cutOutShape if o.cutOutShape else DEFAULT_CUT_OUT_SHAPE,
            wall_cut_out_on_both_sides=o.wallCutOutOnBothSides,
            wall_distance=o.wallDistance,
            wall_width=o.wallWidth,
            wall_left=o.wallLeft,
            wall_height=o.wallHeight,
            wall_top=o.wallTop,

            # HomePieceOfFurniture
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
            icon=TextureImage.from_content(asset_manager.get_asset_by_uri(o.icon.url.file)) if o.icon else None,
            plan_icon=TextureImage.from_content(asset_manager.get_asset_by_uri(o.planIcon.url.file)) if o.planIcon else None,
            model=asset_manager.get_asset_by_uri(o.model.url.file) if o.model else None,
            width=o.width,
            depth=o.depth,
            height=o.height,
            elevation=o.elevation,
            movable=o.movable,
            is_door_or_window=o.doorOrWindow,
            model_materials=[HomeMaterial.from_javaobj(hmo, asset_manager) for hmo in
                             o.modelMaterials] if o.modelMaterials else None,
            color=o.color,
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

        door_or_window.sashes = [Sash.from_javaobj(door_or_window, sash, asset_manager) for sash in o.sashes]

        return door_or_window

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'HomeDoorOrWindow':
        icon = data.get('@icon')
        icon_content = asset_manager.get_asset(icon) if icon else None

        model = data.get('@model')
        level_identifier = data.get('@level')
        sash = data.get('sash', [])

        if not isinstance(sash, list):
            sash = [sash]

        door_or_window = cls(
            # HomeDoorOrWindow
            sashes=[],  # Is set later after class init
            wall_thickness=cls.required_float(data.get('@wallThickness')),
            width_depth_deformable=data.get('@widthDepthDeformable') == 'true',
            bound_to_wall=data.get('@boundToWall') == 'true',
            cut_out_shape=data.get('@cutOutShape', DEFAULT_CUT_OUT_SHAPE),
            wall_cut_out_on_both_sides=data.get('@wallCutOutOnBothSides') == 'true',
            wall_distance=cls.required_float(data.get('@wallDistance', '0.0')),
            wall_width=cls.required_float(data.get('@wallWidth', '1.0')),
            wall_left=cls.required_float(data.get('@wallLeft', '0.0')),
            wall_height=cls.required_float(data.get('@wallHeight', '1.0')),
            wall_top=cls.required_float(data.get('@wallTop', '0.0')),

            # HomePieceOfFurniture
            identifier=data.get('@id'),
            catalog_id=data.get('@catalogId'),
            name=data.get('@name'),
            name_visible=True,
            name_x_offset=0.0,
            name_y_offset=0.0,
            name_style=None,
            name_angle=0.0,
            description=None,
            height_in_plan=cls.required_float(data.get('@heightInPlan', '-infinity')),
            icon=TextureImage.from_content(icon_content) if icon_content else None,
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

        door_or_window.sashes = [Sash.from_xml_dict(door_or_window, sash, asset_manager) for sash in sash]

        return door_or_window
