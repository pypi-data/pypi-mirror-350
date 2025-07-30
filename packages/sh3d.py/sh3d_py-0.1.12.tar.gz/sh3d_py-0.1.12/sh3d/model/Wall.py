import dataclasses
import math
from functools import cached_property
from typing import Optional, Dict, List

from javaobj import JavaObject

from shapely.geometry.polygon import Polygon
from .Baseboard import BaseBoard
from .HasLevel import HasLevel
from .HomeTexture import HomeTexture
from .Level import Level
from .Renderable import Renderable, PointType, PointTypeEditable
from .TextureImage import TextureImage
from .ModelBase import ModelBase
from ..AssetManager import AssetManager

_wall_cache: Dict[str, 'Wall'] = {}



@dataclasses.dataclass
class Wall(ModelBase, Renderable, HasLevel):
    identifier: str
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    thickness: float
    left_side_shininess: float = 0.0
    right_side_shininess: float = 0.0
    symmetric: bool = True
    pattern: Optional[TextureImage] = None
    top_color: Optional[int] = None
    arc_extent: Optional[float] = None
    height: Optional[float] = None
    height_at_end: Optional[float] = None
    left_side_color: Optional[int] = None
    left_side_texture: Optional[HomeTexture] = None
    right_side_color: Optional[int] = None
    right_side_texture: Optional[HomeTexture] = None
    wall_at_start: Optional['Wall'] = None
    wall_at_end: Optional['Wall'] = None
    level: Optional[Level] = None
    left_side_baseboard: Optional[BaseBoard] = None
    right_side_baseboard: Optional[BaseBoard] = None

    _arc_circle_center_cache: Optional[PointTypeEditable] = None
    _points_cache: Optional[List[PointTypeEditable]] = None
    _points_including_baseboards_cache: Optional[List[PointTypeEditable]] = None

    def is_at_level(self, level: Level) -> bool:
        if self.level == level:
            return True
        if self.level and level:
            this_level_elevation = self.level.elevation
            level_elevation = level.elevation
            at_elevation = this_level_elevation == level_elevation and self.level.elevation_index < level.elevation_index
            at_level = this_level_elevation < level_elevation < this_level_elevation + self.get_wall_maximum_height()
            return at_elevation or at_level

        return False

    @cached_property
    def geometry(self) -> Polygon:
        return Polygon(self.points)

    def get_wall_maximum_height(self) -> float:
        if not self.height:
            return 0.0
        if self.height and self.height_at_end:
            return max(self.height, self.height_at_end)

        return self.height

    def is_trapezoidal(self) -> bool:
        if not self.height or not self.height_at_end:
            return False

        return self.height != self.height_at_end

    @property
    def points(self) -> List[PointType]:
        return self.get_points(include_baseboards=False)

    @points.setter
    def points(self, points: List[PointType]) -> None:
        raise NotImplementedError

    def get_points(self, include_baseboards: bool) -> List[PointType]:
        if include_baseboards and (self.left_side_baseboard or self.right_side_baseboard):
            if not self._points_including_baseboards_cache:
                self._points_including_baseboards_cache = self._get_shape_points(include_baseboards)
            return self._points_including_baseboards_cache

        if not self._points_cache:
            self._points_cache = self._get_shape_points(include_baseboards=False)
        return self._points_cache

    def get_arc_circle_center(self) -> PointType:
        if not self.arc_extent:
            raise ValueError('arc_extent is not set')
        if self._arc_circle_center_cache:
            return self._arc_circle_center_cache
        distance = math.dist([self.x_start, self.y_start], [self.x_end, self.y_end])
        if abs(self.arc_extent) > math.pi:
            angle_to_center = -(math.pi + self.arc_extent) / 2
        else:
            angle_to_center = (math.pi - self.arc_extent) / 2

        center_offset = -math.tan(angle_to_center) * distance / 2

        x_mid = (self.x_start + self.x_end) / 2
        y_mid = (self.y_start + self.y_end) / 2

        base_angle = math.atan2(self.x_start - self.x_end, self.y_end - self.y_start)
        self._arc_circle_center_cache = [x_mid + center_offset * math.cos(base_angle), y_mid + center_offset * math.sin(base_angle)]

        return self._arc_circle_center_cache

    def _compute_round_wall_shape_point(
            self,
            wall_points: List[PointType],
            angle: float,
            index: int,
            angle_delta: float,
            arc_circle_center: PointType,
            exterior_arc_radius: float,
            interior_arc_radius: float
    ) -> None:
        cos = math.cos(angle)
        sin = math.sin(angle)

        interior_arc_point = [
            arc_circle_center[0] + interior_arc_radius * cos,
            arc_circle_center[1] - interior_arc_radius * sin
        ]


        exterior_arc_point = [
            arc_circle_center[0] + exterior_arc_radius * cos,
            arc_circle_center[1] - exterior_arc_radius * sin
        ]

        if angle_delta > 0:
            wall_points.insert(index, interior_arc_point)
            wall_points.insert(len(wall_points) - index, exterior_arc_point)
        else:
            wall_points.insert(index, exterior_arc_point)
            wall_points.insert(len(wall_points) - index, interior_arc_point)

    def _get_unjoined_shape_points(self, include_baseboards: bool) -> List[PointType]:
        epsilon = 1e-10

        if (
                self.arc_extent and
                self.arc_extent != 0 and
                (self.x_start - self.x_end) ** 2 + (self.y_start - self.y_end) ** 2 > epsilon
        ):

            arc_center = self.get_arc_circle_center()
            start_angle = math.atan2(arc_center[1] - self.y_start, arc_center[0] - self.x_start)
            start_angle += 2 * math.atan2(self.y_start - self.y_end, self.x_end - self.x_start)

            arc_radius = math.dist(arc_center, [self.x_start, self.y_start])
            exterior_radius = arc_radius + self.thickness / 2
            interior_radius = max(0.0, arc_radius - self.thickness / 2)
            arc_length = exterior_radius * abs(self.arc_extent)
            angle_delta = self.arc_extent / math.sqrt(arc_length) if arc_length != 0 else 0
            angle_steps = int(self.arc_extent / angle_delta) if angle_delta != 0 else 0

            if include_baseboards:
                if angle_delta > 0:
                    if self.left_side_baseboard:
                        exterior_radius += self.left_side_baseboard.thickness
                    if self.right_side_baseboard:
                        interior_radius -= self.right_side_baseboard.thickness
                else:
                    if self.left_side_baseboard:
                        interior_radius -= self.left_side_baseboard.thickness
                    if self.right_side_baseboard:
                        exterior_radius += self.right_side_baseboard.thickness

            wall_points: List[PointType] = []

            if self.symmetric:
                if abs(self.arc_extent - angle_steps * angle_delta) > 1e-6:
                    angle_steps += 1
                    angle_delta = self.arc_extent / angle_steps
                for i in range(angle_steps + 1):
                    angle = start_angle + self.arc_extent - i * angle_delta
                    self._compute_round_wall_shape_point(
                        wall_points, angle, i, angle_delta,
                        arc_center, exterior_radius, interior_radius)
            else:
                i = 0
                angle = self.arc_extent

                def _step_condition(a: float) -> bool:
                    return a >= angle_delta * 0.1 if angle_delta > 0 else a <= -angle_delta * 0.1

                while _step_condition(angle):
                    self._compute_round_wall_shape_point(
                        wall_points, start_angle + angle, i, angle_delta,
                        arc_center, exterior_radius, interior_radius)
                    angle -= angle_delta
                    i += 1
                self._compute_round_wall_shape_point(
                    wall_points, start_angle, i, angle_delta,
                    arc_center, exterior_radius, interior_radius)

            return wall_points

        angle = math.atan2(self.y_end - self.y_start, self.x_end - self.x_start)
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        left_thickness = self.thickness / 2
        if include_baseboards and self.left_side_baseboard:
            left_thickness += self.left_side_baseboard.thickness
        left_dx = sin_a * left_thickness
        left_dy = cos_a * left_thickness

        right_thickness = self.thickness / 2
        if include_baseboards and self.right_side_baseboard:
            right_thickness += self.right_side_baseboard.thickness
        right_dx = sin_a * right_thickness
        right_dy = cos_a * right_thickness

        return [
            [self.x_start + left_dx, self.y_start - left_dy],
            [self.x_end + left_dx, self.y_end - left_dy],
            [self.x_end - right_dx, self.y_end + right_dy],
            [self.x_start - right_dx, self.y_start + right_dy]
        ]

    def _compute_intersection(
            self,
            point1: PointTypeEditable,
            point2: PointTypeEditable,
            point3: PointTypeEditable,
            point4: PointTypeEditable,
            limit: float
    ) -> None:
        try:
            alpha1 = (point2[1] - point1[1]) / (point2[0] - point1[0])
        except ZeroDivisionError:
            alpha1 = float('inf') if point2[1] >= point1[1] else -float('inf')

        try:
            alpha2 = (point4[1] - point3[1]) / (point4[0] - point3[0])
        except ZeroDivisionError:
            alpha2 = float('inf') if point4[1] >= point3[1] else -float('inf')

        if alpha1 != alpha2:
            x = point1[0]
            y = point1[1]

            # First line vertical
            if math.isinf(alpha1) and not math.isinf(alpha2):
                x = point1[0]
                beta2 = point4[1] - alpha2 * point4[0]
                y = alpha2 * x + beta2

            # Second line vertical
            elif math.isinf(alpha2) and not math.isinf(alpha1):
                x = point3[0]
                beta1 = point2[1] - alpha1 * point2[0]
                y = alpha1 * x + beta1

            # Neither vertical
            elif not math.isinf(alpha1) and not math.isinf(alpha2):
                same_signum = math.copysign(1, alpha1) == math.copysign(1, alpha2)
                if (abs(alpha1 - alpha2) > 1E-5 and
                        (not same_signum or (max(abs(alpha1), abs(alpha2)) / min(abs(alpha1), abs(alpha2))) > 1.004)):
                    beta1 = point2[1] - alpha1 * point2[0]
                    beta2 = point4[1] - alpha2 * point4[0]
                    x = (beta2 - beta1) / (alpha1 - alpha2)
                    y = alpha1 * x + beta1

            # Only update point1 if the new intersection is within the limit
            if (point1[0] - x) ** 2 + (point1[1] - y) ** 2 < limit * limit:
                point1[0] = x
                point1[1] = y

    def _get_shape_points(self, include_baseboards: bool) -> List[PointType]:
        epsilon = 0.01
        wall_points = self._get_unjoined_shape_points(include_baseboards)
        left_start = 0
        wall_points_len = len(wall_points)
        right_start = wall_points_len - 1
        left_end = wall_points_len // 2 - 1
        right_end = wall_points_len// 2

        if self.wall_at_start:
            wall_start = self.wall_at_start
            start_points = wall_start._get_unjoined_shape_points(include_baseboards)
            start_left_start = 0
            start_right_start = len(start_points) - 1
            start_left_end = len(start_points) // 2 - 1
            start_right_end = len(start_points) // 2

            joined_at_end = (
                    wall_start.wall_at_end == self and
                    (wall_start.wall_at_start != self or
                     (wall_start.x_end == self.x_start and wall_start.y_end == self.y_start))
            )
            joined_at_start = (
                    wall_start.wall_at_start == self and
                    (wall_start.wall_at_end != self or
                     (wall_start.x_start == self.x_start and wall_start.y_start == self.y_start))
            )

            start_cache = wall_start._points_including_baseboards_cache if include_baseboards else wall_start._points_cache

            limit = 2 * max(self.thickness, wall_start.thickness)

            if joined_at_end:
                self._compute_intersection(wall_points[left_start], wall_points[left_start + 1],
                                          start_points[start_left_end], start_points[start_left_end - 1], limit)
                self._compute_intersection(wall_points[right_start], wall_points[right_start - 1],
                                          start_points[start_right_end], start_points[start_right_end + 1], limit)

                if start_cache:
                    if (abs(wall_points[left_start][0] - start_cache[start_left_end][0]) < epsilon and
                            abs(wall_points[left_start][1] - start_cache[start_left_end][1]) < epsilon):
                        wall_points[left_start] = start_cache[start_left_end]
                    if (abs(wall_points[right_start][0] - start_cache[start_right_end][0]) < epsilon and
                            abs(wall_points[right_start][1] - start_cache[start_right_end][1]) < epsilon):
                        wall_points[right_start] = start_cache[start_right_end]

            elif joined_at_start:
                self._compute_intersection(wall_points[left_start], wall_points[left_start + 1],
                                          start_points[start_right_start], start_points[start_right_start - 1], limit)
                self._compute_intersection(wall_points[right_start], wall_points[right_start - 1],
                                          start_points[start_left_start], start_points[start_left_start + 1], limit)

                if start_cache:
                    if (abs(wall_points[left_start][0] - start_cache[start_right_start][0]) < epsilon and
                            abs(wall_points[left_start][1] - start_cache[start_right_start][1]) < epsilon):
                        wall_points[left_start] = start_cache[start_right_start]
                    if (abs(wall_points[right_start][0] - start_cache[start_left_start][0]) < epsilon and
                            abs(wall_points[right_start][1] - start_cache[start_left_start][1]) < epsilon):
                        wall_points[right_start] = start_cache[start_left_start]

        if self.wall_at_end:
            wall_end = self.wall_at_end
            end_points = wall_end._get_unjoined_shape_points(include_baseboards)
            end_left_start = 0
            end_right_start = len(end_points) - 1
            end_left_end = len(end_points) // 2 - 1
            end_right_end = len(end_points) // 2

            joined_at_start = (
                    wall_end.wall_at_start == self and
                    (wall_end.wall_at_end != self or
                     (wall_end.x_start == self.x_end and wall_end.y_start == self.y_end))
            )

            joined_at_end = (
                    wall_end.wall_at_end == self and
                    (wall_end.wall_at_start != self or
                     (wall_end.x_end == self.x_end and wall_end.y_end == self.y_end))
            )

            end_cache = wall_end._points_including_baseboards_cache if include_baseboards else wall_end._points_cache

            limit = 2 * max(self.thickness, wall_end.thickness)

            if joined_at_start:
                self._compute_intersection(wall_points[left_end], wall_points[left_end - 1],
                                          end_points[end_left_start], end_points[end_left_start + 1], limit)
                self._compute_intersection(wall_points[right_end], wall_points[right_end + 1],
                                          end_points[end_right_start], end_points[end_right_start - 1], limit)

                if end_cache:
                    if (abs(wall_points[left_end][0] - end_cache[end_left_start][0]) < epsilon and
                            abs(wall_points[left_end][1] - end_cache[end_left_start][1]) < epsilon):
                        wall_points[left_end] = end_cache[end_left_start]
                    if (abs(wall_points[right_end][0] - end_cache[end_right_start][0]) < epsilon and
                            abs(wall_points[right_end][1] - end_cache[end_right_start][1]) < epsilon):
                        wall_points[right_end] = end_cache[end_right_start]

            elif joined_at_end:
                self._compute_intersection(wall_points[left_end], wall_points[left_end - 1],
                                          end_points[end_right_end], end_points[end_right_end + 1], limit)
                self._compute_intersection(wall_points[right_end], wall_points[right_end + 1],
                                          end_points[end_left_end], end_points[end_left_end - 1], limit)

                if end_cache:
                    if (abs(wall_points[left_end][0] - end_cache[end_right_end][0]) < epsilon and
                            abs(wall_points[left_end][1] - end_cache[end_right_end][1]) < epsilon):
                        wall_points[left_end] = end_cache[end_right_end]
                    if (abs(wall_points[right_end][0] - end_cache[end_left_end][0]) < epsilon and
                            abs(wall_points[right_end][1] - end_cache[end_left_end][1]) < epsilon):
                        wall_points[right_end] = end_cache[end_left_end]


        return wall_points

    @classmethod
    def from_identifier(cls, identifier: str) -> 'Wall':
        wall = _wall_cache.get(identifier)
        if not wall:
            raise ValueError('Identifier not found in cache')
        return wall

    @classmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'Wall':
        wall_identifier = o.id

        if wall_identifier in _wall_cache:
            return _wall_cache[wall_identifier]

        # First pass: create partially initialized object
        wall = cls(
            identifier=wall_identifier,
            x_start=o.xStart,
            y_start=o.yStart,
            x_end=o.xEnd,
            y_end=o.yEnd,
            thickness=getattr(o, 'thickness', 0.0)
        )

        pattern = getattr(o, 'pattern', None)
        height = getattr(o, 'height', None)
        arc_extent = getattr(o, 'arcExtent', None)
        level = getattr(o, 'level', None)

        _wall_cache[wall_identifier] = wall
        # Second pass: populate fields
        wall.arc_extent = arc_extent.value if arc_extent else None
        wall.height = height.value if height else None
        wall.height_at_end = getattr(o, 'heightAtEnd', None)
        wall.left_side_color = getattr(o, 'leftSideColor', None)
        wall.left_side_texture = getattr(o, 'leftSideTexture', None)
        wall.left_side_shininess = getattr(o, 'leftSideShininess', 0.0)
        wall.left_side_baseboard = getattr(o, 'leftSideBaseboard', None)
        wall.right_side_color = getattr(o, 'rightSideColor', None)
        wall.right_side_texture = getattr(o, 'rightSideTexture', None)
        wall.right_side_shininess = getattr(o, 'rightSideShininess', 0.0)
        wall.right_side_baseboard = getattr(o, 'rightSideBaseboard', None)
        wall.pattern = TextureImage.from_javaobj(pattern, asset_manager) if pattern else None
        wall.top_color = getattr(o, 'topColor', None)
        wall.symmetric = getattr(o, 'symmetric', True)

        wall_at_start = getattr(o, 'wallAtStart', None)
        wall_at_end = getattr(o, 'wallAtEnd', None)

        wall.wall_at_start = cls.from_javaobj(wall_at_start, asset_manager) if wall_at_start else None
        wall.wall_at_end = cls.from_javaobj(wall_at_end, asset_manager) if wall_at_end else None

        wall.level = Level.from_javaobj(level, asset_manager) if level else None

        return wall

    @classmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'Wall':
        pattern = data.get('@pattern')
        level_identifier = data.get('@level')
        wall_identifier = cls.required_str(data.get('@id'))

        if wall_identifier in _wall_cache:
            return _wall_cache[wall_identifier]

        # First pass: create partially initialized object
        wall = cls(
            identifier=wall_identifier,
            x_start=cls.required_float(data.get('@xStart')),
            y_start=cls.required_float(data.get('@yStart')),
            x_end=cls.required_float(data.get('@xEnd')),
            y_end=cls.required_float(data.get('@yEnd')),
            thickness=float(data.get('@thickness', '0.0'))
        )

        _wall_cache[wall_identifier] = wall

        # Second pass: populate fields
        wall.height = cls.required_float(data.get('@height'))
        wall.pattern = TextureImage.from_str(pattern, asset_manager) if pattern else None

        wall_at_start = data.get('@wallAtStart')
        wall_at_end = data.get('@wallAtEnd')
        wall.wall_at_start = _wall_cache.get(wall_at_start) if wall_at_start else None
        wall.wall_at_end = _wall_cache.get(wall_at_end) if wall_at_end else None

        wall.level = Level.from_identifier(level_identifier) if level_identifier else None

        return wall
