import math
from collections import defaultdict
from typing import List, Dict, Optional, Tuple, TypeVar, Callable
from functools import cached_property, reduce
from pathlib import Path
import skia
from shapely.geometry.linestring import LineString
from sh3d.model.BackgroundImage import BackgroundImage
from sh3d.model.Color import Color
from sh3d.model.DimensionLine import DimensionLine
from sh3d.model.HasLevel import HasLevel
from sh3d.model.Home import Home
from sh3d.model.HomePieceOfFurniture import HomePieceOfFurniture
from sh3d.model.Label import Label
from sh3d.model.Level import Level
from sh3d.model.Polyline import Polyline, ArrowStyle, CapStyle
from sh3d.model.TextStyle import TextStyle
from sh3d.model.TextureImage import TextureImage
from sh3d.model.Wall import Wall
from sh3d.model.Room import Room
from sh3d.model.Renderable import Renderable
from sh3d.geometry import Rectangle


L = TypeVar('L', bound=HasLevel)


class HomeRenderer:
    home: Home
    def __init__(self, home: Home):
        self.home = home

    @cached_property
    def plan_bounds(self) -> Rectangle:
        items_bounds = self.get_items_bounds(self.home.selectable_viewable_items)
        bounds = items_bounds if items_bounds else Rectangle(0,0, 1000, 1000)
        background_images = [level.background_image for level in self.home.levels if level.background_image]
        if self.home.background_image:
            background_images.append(self.home.background_image)

        for background_image in background_images:
            bounds.add(-background_image.x_origin, -background_image.y_origin)  # Same
            bounds.add(
                background_image.image_info.width * background_image.scale -background_image.x_origin,
                background_image.image_info.height * background_image.scale - background_image.y_origin
            )

        return bounds

    def _union_paths(self, paths: List[skia.Path]) -> skia.Path:
        return reduce(lambda acc, p: skia.Op(acc, p, skia.PathOp.kUnion_PathOp), paths)

    @staticmethod
    def points_to_path(points: List[Tuple[float, float]], closed_path: bool = True, transform: Optional[skia.Matrix]=None) -> skia.Path:
        path = skia.Path()

        if not points:
            return path

        # Move to first point
        path.moveTo(*points[0])

        # Draw lines to the rest
        for pt in points[1:]:
            path.lineTo(*pt)

        if closed_path:
            path.close()

        # Apply transform if provided
        if transform:
            # Assume `transform` is a 3x3 or 2D compatible Skia matrix
            path.transform(transform)

        return path

    @staticmethod
    def path_string_to_skia_path(path_string: str) -> skia.Path:
        path = skia.Path()
        last_x = 0.0
        last_y = 0.0
        char_to_command: Dict[str, Callable[..., None]] = {
            'M': path.moveTo,
            'm': path.rMoveTo,
            'L': path.lineTo,
            'l': path.rLineTo,  # noqa: E741
            'H': lambda *args: path.lineTo(last_x, args[1]),
            'h': lambda *args: path.lineTo(last_x + args[0], args[1]),
            'V': lambda *args: path.lineTo(args[0], last_y),
            'v': lambda *args: path.lineTo(args[0], last_y + args[1]),
            'C': path.cubicTo,
            'c': path.rCubicTo,
            'Q': path.quadTo,
            'q': path.rQuadTo,
            'A': path.arcTo,
            'a': path.rArcTo,
            'Z': path.close
        }
        chunks = path_string.split()
        command: Optional[Callable[..., None]] = None
        command_args: List[float] = []
        chunks_count = len(chunks)
        for index, chunk in enumerate(chunks):
            command_found = char_to_command.get(chunk)
            if command_found:
                if command is not None:
                    command(*command_args)
                    command_args = []
            if command_found:
                command = command_found
            elif command is not None:
                command_args.append(float(chunk.replace(',', '')))

                if index == chunks_count - 1:
                    command(*command_args)
                    command_args = []

        return path

    @staticmethod
    def accumulate_non_overlapping_paths(paths: List[skia.Path]) -> List[skia.Path]:
        """
        Given a list of skia.Path objects, returns a list of non-overlapping paths,
        where each subsequent path is clipped (difference) from the union of the previous ones.
        """
        result_paths = []
        accumulated = skia.Path()

        for path in paths:
            if not accumulated.isEmpty():
                path = skia.Op(path, accumulated, skia.PathOp.kDifference_PathOp)
            result_paths.append(path)
            accumulated = skia.Op(accumulated, path, skia.PathOp.kUnion_PathOp)

        return result_paths

    def get_items_bounds(self, items: List[Renderable]) -> Optional[Rectangle]:
        bounds: Optional[Rectangle] = None
        for item in items:
            bound = self.get_item_bound(item)
            if not bounds:
                bounds = bound
            else:
                bounds.add_rectangle(bound)

        return bounds

    @staticmethod
    def get_item_bound(item: Renderable) -> Rectangle:
        (minx, miny, maxx, maxy) = item.geometry.bounds

        return Rectangle(
            x=minx,
            y=miny,
            width=maxx - minx,
            height=maxy - miny
        )

    @staticmethod
    def is_viewable_at_level(has_level: HasLevel, level: Optional[Level]=None) -> bool:
        if not has_level.level:
            return True
        return has_level.level.is_visible and has_level.is_at_level(level)

    def get_drawable_items_at_level(self, items: List[L], level: Optional[Level]=None) -> List[L]:
        items_at_level: List[L] = []
        for wall in items:
            if self.is_viewable_at_level(wall, level):
                items_at_level.append(wall)
        return items_at_level

    def get_wall_areas_at_level(self, level: Optional[Level]=None) -> List[Tuple[List[Wall], skia.Path]]:
        return self.get_wall_areas(self.get_drawable_items_at_level(self.home.walls, level))

    def get_wall_areas(self, walls: List[Wall]) -> List[Tuple[List[Wall], skia.Path]]:
        """
        Groups walls by pattern and computes the unioned area for each group.
        Returns a dict mapping pattern identifier (e.g. name or hash) to shapely geometry.
        """
        if not walls:
            return []

        # Determine if all walls share the same pattern
        first_pattern = walls[0].pattern
        same_pattern = all(wall.pattern == first_pattern for wall in walls)

        wall_areas: List[Tuple[List['Wall'], skia.Path]] = []

        if same_pattern:
            # All use same pattern
            wall_areas.append((walls, self.get_items_area(walls)))
        else:
            # Sort walls by their pattern
            sorted_walls: Dict[TextureImage, List[Wall]] = defaultdict(list)
            for wall in walls:
                pattern = wall.pattern
                if not pattern:
                    raise NotImplementedError('IMPLEMENT DEFAULT PATTERN FOR NO PATTERN SET')
                sorted_walls[pattern].append(wall)
            for pattern_walls in sorted_walls.values():
                wall_areas.append((pattern_walls, self.get_items_area(pattern_walls)))

        return wall_areas

    def get_items_area(self, items: List[Renderable]) -> skia.Path:
        paths = []
        for item in items:
            paths.append(self.points_to_path(item.points, closed_path=True, transform=None))

        return self._union_paths(paths)

    def render(self, level: Optional[Level] = None, plan_scale: float = 1.0) -> None:
        self._paint_background(level)
        self._paint_background_image(level, plan_scale)
        self._paint_rooms(level, plan_scale)
        self._paint_walls(level, plan_scale)
        self._paint_dimension_lines(level, plan_scale)
        self._paint_furniture(level, plan_scale)
        self._paint_polylines(level, plan_scale)
        self._paint_labels(level, plan_scale)

    def _paint_background(self, _level: Optional[Level]=None) -> None:
        self.drawn_background('#FFFFFF')

    def _paint_background_image(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        if level and level.background_image and not level.background_image.invisible:
            self.drawn_background_image(level.background_image, plan_scale)
        elif self.home.background_image and not self.home.background_image.invisible:
            self.drawn_background_image(self.home.background_image, plan_scale)

    def _paint_rooms(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        rooms = self.get_drawable_items_at_level(self.home.rooms, level)
        self.drawn_rooms(rooms, plan_scale)
        # Paint room names and area
        color = Color.from_rgba(0, 0, 0, 255)
        for room in rooms:
            if room.name:
                self.drawn_text(
                    room.name,
                    room.x_center + room.name_x_offset,
                    room.y_center + room.name_y_offset,
                    room.name_angle,
                    room.name_style,
                    color
                )

            if room.is_area_visible and room.area:
                area_text = '{:.2f} m²'.format(room.area / 10000)
                self.drawn_text(
                    area_text,
                    room.x_center + room.area_x_offset,
                    room.y_center + room.area_y_offset,
                    room.area_angle,
                    room.area_style,
                    color
                )


    def _paint_walls(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        wall_areas: List[Tuple[List[Wall], skia.Path]] = self.get_wall_areas_at_level(level)
        for walls, area in wall_areas:
            wall_pattern = walls[0].pattern
            self.drawn_walls(walls, area, plan_scale, wall_pattern)

    def _paint_dimension_lines(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        self.drawn_dimension_lines(self.get_drawable_items_at_level(self.home.dimension_lines, level), plan_scale)

    def _paint_furniture(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        self.drawn_furniture(self.get_drawable_items_at_level(self.home.furniture, level), self.get_drawable_items_at_level(self.home.walls, level), plan_scale)

    def _paint_polylines(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        polylines = self.get_drawable_items_at_level(self.home.polylines, level)
        self.drawn_polylines(polylines, plan_scale)

        # Drawn polyine arrows
        for polyline in polylines:
            coordinates = polyline.polyline_path.coords if isinstance(polyline.polyline_path, LineString) else polyline.polyline_path.exterior.coords

            if polyline.is_closed_path or len(coordinates) < 2:
                # Stop here, closed path has no arrows
                return

            # Arrows
            arrow_delta = polyline.thickness / 2 if polyline.cap_style != CapStyle.BUTT else 0

            if polyline.start_arrow_style and polyline.start_arrow_style != ArrowStyle.NONE:
                first_point = coordinates[0]
                second_point = coordinates[1]
                angle_at_start = math.atan2(first_point[1] - second_point[1], first_point[0] - second_point[0])
                self.drawn_arrow(first_point, angle_at_start, polyline.start_arrow_style, polyline.thickness, polyline.color, arrow_delta)

            if polyline.end_arrow_style and polyline.end_arrow_style != ArrowStyle.NONE:
                before_last_point = coordinates[-2]
                last_point = coordinates[-1]
                angle_at_end = math.atan2(last_point[1] - before_last_point[1], last_point[0] - before_last_point[0])
                self.drawn_arrow(last_point, angle_at_end, polyline.end_arrow_style, polyline.thickness, polyline.color, arrow_delta)

    def _paint_labels(self, level: Optional[Level]=None, plan_scale: float = 1.0) -> None:
        self.drawn_labels(self.get_drawable_items_at_level(self.home.labels, level), plan_scale)

    def drawn_walls(self, walls: List[Wall], area: skia.Path, plan_scale: float, wall_pattern: TextureImage) -> None:
        raise NotImplementedError

    def drawn_dimension_lines(self, dimension_lines: List[DimensionLine], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_polylines(self, polylines: List[Polyline], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_background(self, color: str) -> None:
        raise NotImplementedError

    def drawn_background_image(self, background_image: BackgroundImage, plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_rooms(self, rooms: List[Room], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_furniture(self, furniture: List[HomePieceOfFurniture], walls:List[Wall], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_arrow(self, point: Tuple[float, float], angle: float, arrow_style: ArrowStyle, thickness: float, color: Color, delta: float) -> None:
        raise NotImplementedError

    def drawn_labels(self, labels: List[Label], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_text(self, text: str, x: float, y: float, angle: float, style: TextStyle, color: Color, outline_color: Optional[Color] = None) -> None:
        raise NotImplementedError

    def plot(self, level: Optional[Level] = None) -> bytes:
        raise NotImplementedError

    def save_to_file(self, path: Path, level: Optional[Level] = None) -> None:
        raise NotImplementedError
