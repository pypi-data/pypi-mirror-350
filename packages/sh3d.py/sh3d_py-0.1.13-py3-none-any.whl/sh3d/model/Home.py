import dataclasses
from functools import cached_property
from typing import List, TypeVar, Tuple, Optional
from javaobj import JavaObject

from .HasLevel import HasLevel
from .Level import Level
from .BackgroundImage import BackgroundImage
from .HomePieceOfFurniture import HomePieceOfFurniture
from .HomeDoorOrWindow import HomeDoorOrWindow
from .Polyline import Polyline
from .Room import Room
from .Wall import Wall
from .Renderable import Renderable
from .DimensionLine import DimensionLine
from .Label import Label
from .HomeEnvironment import HomeEnvironment
from .Compass import Compass
from .ModelBase import ModelBase
from ..AssetManager import AssetManager


L = TypeVar('L', bound=HasLevel)

@dataclasses.dataclass
class Home(ModelBase):
    levels: List[Level]  # Implemented
    furniture: List[HomePieceOfFurniture]  # Implemented
    rooms: List[Room]  # Implemented
    walls: List[Wall]  # Implemented
    dimension_lines: List[DimensionLine]  # Implemented
    labels: List[Label] # Implemented
    polylines: List[Polyline]  # Implemented
    wall_height: float
    name: str
    environment: HomeEnvironment  # Ignored, not needed for SVG
    compass: Compass  # Not really needed?
    version: int
    background_image: Optional[BackgroundImage] = None  # Implemented

    @cached_property
    def selectable_viewable_items(self) -> List[Renderable]:
        renderable = self.walls + self.rooms + self.dimension_lines + self.labels + self.polylines
        viewable_items: List[Renderable] = [item for item in renderable if not item.level or item.level.is_visible]

        for furniture in self.furniture:
            if furniture.is_visible and (not furniture.level or furniture.level.is_visible):
                viewable_items.append(furniture)

                if isinstance(furniture, HomeDoorOrWindow):
                    for sash in furniture.sashes:
                        viewable_items.append(sash)

        return viewable_items

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Home':
        walls = [Wall.from_javaobj(wo, asset_manager) for wo in o.walls]
        if hasattr(o, 'furnitureWithDoorsAndWindows'):
            furniture_obj = o.furnitureWithDoorsAndWindows
        else:
            furniture_obj = o.furniture

        furniture = []
        for hpofo in furniture_obj:
            if hpofo.classdesc.name == 'com.eteks.sweethome3d.model.HomeDoorOrWindow':
                furniture.append(HomeDoorOrWindow.from_javaobj(hpofo, asset_manager))
            else:
                furniture.append(HomePieceOfFurniture.from_javaobj(hpofo, asset_manager))

        return cls(
            levels=[Level.from_javaobj(lo, asset_manager) for lo in o.levels],
            furniture=furniture,
            rooms=[Room.from_javaobj(ro, asset_manager) for ro in o.rooms],
            walls=walls,
            dimension_lines=[DimensionLine.from_javaobj(dlo, asset_manager) for dlo in o.dimensionLines],
            polylines=[Polyline.from_javaobj(po, asset_manager) for po in o.polylines],
            labels=[Label.from_javaobj(lo, asset_manager) for lo in o.labels],
            wall_height=o.wallHeight,
            name=o.name,
            background_image=BackgroundImage.from_javaobj(o.backgroundImage, asset_manager) if o.backgroundImage else None,
            environment=HomeEnvironment.from_javaobj(o.environment, asset_manager),
            compass=Compass.from_javaobj(o.compass, asset_manager),
            version=o.version
        )

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Home':
        background_image = data.get('backgroundImage')
        dimension_line = data.get('dimensionLine', [])
        compass = data.get('compass')

        if not compass:
            raise ValueError('compass is not provided')

        if not isinstance(dimension_line, list):
            dimension_line = [dimension_line]
        label = data.get('label', [])
        if not isinstance(label, list):
            label = [label]

        wall = data.get('wall', [])
        if not isinstance(wall, list):
            wall = [wall]

        level = data.get('level', [])
        if not isinstance(level, list):
            level = [level]

        # Levels needs to be processed first to fill in cache
        levels = [Level.from_xml_dict(le, asset_manager) for le in level]

        door_or_window = data.get('doorOrWindow',[])
        if not isinstance(door_or_window, list):
            door_or_window = [door_or_window]
        piece_of_furniture = data.get('pieceOfFurniture',[])
        if not isinstance(piece_of_furniture, list):
            piece_of_furniture = [piece_of_furniture]

        polyline = data.get('polyline', [])
        if not isinstance(polyline, list):
            polyline = [polyline]

        furniture = [HomeDoorOrWindow.from_xml_dict(dow, asset_manager) for dow in door_or_window]
        furniture += [HomePieceOfFurniture.from_xml_dict(hpofo, asset_manager) for hpofo in piece_of_furniture]

        # Stitch together walls
        walls: List[Tuple[Wall, str, str]] = []
        for wo in wall:
            wall_at_start_identifier = wo.get('@wallAtStart')
            wall_at_end_identifier = wo.get('@wallAtEnd')
            walls.append((Wall.from_xml_dict(wo, asset_manager), wall_at_start_identifier, wall_at_end_identifier))

        # Loop over created walls and set wall_at_start/end correctly
        for wall, wall_at_start_identifier, wall_at_end_identifier in walls:
            if wall_at_start_identifier and not wall.wall_at_start:
                wall.wall_at_start = Wall.from_identifier(wall_at_start_identifier)

            if wall_at_end_identifier and not wall.wall_at_end:
                wall.wall_at_end = Wall.from_identifier(wall_at_end_identifier)

        return cls(
            levels=levels,
            labels=[Label.from_xml_dict(lo, asset_manager) for lo in label],
            furniture=furniture,
            rooms=[Room.from_xml_dict(ro, asset_manager) for ro in data.get('room')],
            walls=[w[0] for w in walls],
            dimension_lines=[DimensionLine.from_xml_dict(dl, asset_manager) for dl in dimension_line],
            polylines=[Polyline.from_xml_dict(po, asset_manager) for po in polyline],
            wall_height=cls.required_float(data.get('@wallHeight')),
            name=cls.required_str(data.get('@name')),
            background_image=BackgroundImage.from_xml_dict(data.get('backgroundImage'), asset_manager) if background_image else None,
            environment=HomeEnvironment.from_xml_dict(data.get('environment'), asset_manager),
            compass=Compass.from_xml_dict(compass, asset_manager),
            version=cls.required_int(data.get('@version')),
        )
