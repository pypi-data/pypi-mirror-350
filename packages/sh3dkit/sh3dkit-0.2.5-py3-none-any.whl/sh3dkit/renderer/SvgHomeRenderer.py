import base64
import math
from pathlib import Path
from typing import List, Optional, Tuple, Type, Dict, Literal
import svg
import skia
from shapely.geometry.linestring import LineString

from sh3d.model.BackgroundImage import BackgroundImage
from sh3d.model.Color import Color
from sh3d.model.DimensionLine import DimensionLine, DIMENSION_LINE_MARK_END, VERTICAL_DIMENSION_LINE_DISC, VERTICAL_DIMENSION_LINE
from sh3d.model.Home import Home
from sh3d.model.HomeDoorOrWindow import HomeDoorOrWindow
from sh3d.model.HomePieceOfFurniture import HomePieceOfFurniture
from sh3d.model.Label import Label
from sh3d.model.Level import Level
from sh3d.model.Polyline import Polyline, ArrowStyle
from sh3d.model.Room import Room
from sh3d.model.TextStyle import TextStyle, Alignment
from sh3d.model.TextureImage import TextureImage
from sh3d.model.Wall import Wall

from sh3dkit.renderer.HomeRenderer import HomeRenderer



class SvgHomeRenderer(HomeRenderer):
    elements: List[svg.Element]
    definitions: Dict[str, svg.Element]

    _alignment_to_svg: Dict[Alignment, Literal['start', 'middle', 'end']] = {
        Alignment.LEFT: 'start',
        Alignment.CENTER: 'middle',
        Alignment.RIGHT: 'end'
    }

    def __init__(self, home: Home):
        super().__init__(home)
        self.elements = []
        self.definitions = {}

    @staticmethod
    def path_string_to_path_data(path: str) -> List[svg.PathData]:
        char_to_command: Dict[str, Type[svg.PathData]] = {
            'M': svg.MoveTo,
            'm': svg.MoveToRel,
            'L': svg.LineTo,
            'l': svg.LineToRel,  # noqa: E741
            'H': svg.HorizontalLineTo,
            'h': svg.HorizontalLineToRel,
            'V': svg.VerticalLineTo,
            'v': svg.VerticalLineToRel,
            'C': svg.CubicBezier,
            'c': svg.CubicBezierRel,
            'S': svg.SmoothCubicBezier,
            's': svg.SmoothCubicBezierRel,
            'Q': svg.QuadraticBezier,
            'q': svg.QuadraticBezierRel,
            'T': svg.SmoothQuadraticBezier,
            't': svg.SmoothQuadraticBezierRel,
            'A': svg.Arc,
            'a': svg.ArcRel,
            'Z': svg.ClosePath
        }
        chunks = path.split()
        command: Optional[Type[svg.PathData]] = None
        command_args: List[float] = []
        commands = []
        chunks_count = len(chunks)
        for index, chunk in enumerate(chunks):
            command_found = char_to_command.get(chunk)
            if command_found:
                if command is not None:
                    commands.append(command(*command_args))
                    command_args = []
            if command_found:
                command = command_found
            elif command is not None:
                command_args.append(float(chunk.replace(',', '')))

                if index == chunks_count - 1:
                    commands.append(command(*command_args))
                    command_args = []

        return commands

    @staticmethod
    def _skia_path_to_svg_d(path: skia.Path) -> List[svg.PathData]:
        d: List[svg.PathData] = []
        for verb, pts in path:

            if verb == skia.Path.Verb.kMove_Verb:
                point1, = pts
                d.append(svg.M(point1.x(), point1.y()))
            elif verb == skia.Path.Verb.kLine_Verb:
                point1, point2 = pts
                d.append(svg.L(point2.x(), point2.y()))
            elif verb == skia.Path.Verb.kQuad_Verb:
                point1, point2, point3 = pts
                d.append(svg.Q(point2.x(), point2.y(), point3.x(), point3.y()))
            elif verb == skia.Path.Verb.kCubic_Verb:
                point1, point2, point3, point4 = pts
                d.append(svg.C(point2.x(), point2.y(), point3.x(), point3.y(), point4.x(), point4.y()))
            elif verb == skia.Path.Verb.kClose_Verb:
                d.append(svg.Z())
        return d

    def drawn_walls(self, walls: List[Wall], area: skia.Path, plan_scale: float, wall_pattern: TextureImage) -> None:
        # Embed wall pattern if not yet done
        if wall_pattern.name not in self.definitions:
            self.definitions[wall_pattern.name] = svg.Pattern(
                id=wall_pattern.name,
                patternUnits='userSpaceOnUse',
                width=wall_pattern.width,
                height=wall_pattern.height,
                elements=[
                    svg.Image(
                        href='data:image/png;base64,{}'.format(base64.b64encode(wall_pattern.image.data).decode()),
                        x=0,
                        y=0,
                        width=wall_pattern.width,
                        height=wall_pattern.height
                    )
                ]
            )

        # Wall outline
        path = self._skia_path_to_svg_d(area)
        wall_path = svg.Path(
            d=path,
            stroke_width=1,
            stroke='black',
            fill_opacity=0
        )
        self.elements.append(wall_path)

        # Drawn walls fill
        wall_fills = self.accumulate_non_overlapping_paths(
            [self.points_to_path(wall.points, closed_path=True, transform=None) for wall in walls]
        )

        for wall_fill in wall_fills:
            # First color
            wall_path = svg.Path(
                d=self._skia_path_to_svg_d(wall_fill),
                stroke_width=0,
                fill='#FFFFFF',
            )
            self.elements.append(wall_path)

            # Then pattern

            wall_path = svg.Path(
                d=self._skia_path_to_svg_d(wall_fill),
                stroke_width=0,
                fill='url(#{})'.format(wall_pattern.name),
            )
            self.elements.append(wall_path)

    def drawn_background(self, color: str) -> None:
        self.elements.append(svg.Rect(
            x=self.plan_bounds.x,
            y=self.plan_bounds.y,
            width=self.plan_bounds.width,
            height=self.plan_bounds.height,
            fill=color
        ))

    def drawn_background_image(self, background_image: BackgroundImage, plan_scale: float) -> None:
        self.elements.append(svg.Image(
            href='data:image/png;base64,{}'.format(base64.b64encode(background_image.image.data).decode()),
            x=0,
            y=0,
            width=background_image.image_info.width,
            height=background_image.image_info.height,
            transform=[
                svg.Translate(
                    x=-background_image.x_origin,
                    y=-background_image.y_origin,
                ),
                svg.Scale(
                    x=background_image.scale
                )
            ]
        ))

    def drawn_rooms(self, rooms: List[Room], plan_scale: float) -> None:
        for room in rooms:
            room_polygon = svg.Polygon(
                class_=['room'],
                id=room.identifier,
                points=[coord for point in room.geometry.exterior.coords for coord in point],
                stroke="black",
                fill="#808080",
                stroke_width=1,
            )

            self.elements.append(room_polygon)


    def drawn_dimension_lines(self, dimension_lines: List[DimensionLine], plan_scale: float) -> None:
        mark_end = self.path_string_to_skia_path(' '.join(DIMENSION_LINE_MARK_END))
        mark_end_width = mark_end.getBounds().width()

        extension_line_stroke = [20 / plan_scale, 5 / plan_scale, 5 / plan_scale, 5 / plan_scale]
        for dimension_line in dimension_lines:
            mark_end_scale = dimension_line.end_mark_size / mark_end_width
            dimension_line_stroke = 0.5 / mark_end_scale / plan_scale

            if dimension_line.is_elevation_dimension_line:
                angle = (dimension_line.pitch + 2 * math.pi) % (2 * math.pi)
            else:
                angle = math.atan2(dimension_line.y_end - dimension_line.y_start, dimension_line.x_end - dimension_line.x_start)

            transformations: List[svg.Transform] = [
                svg.Translate(dimension_line.x_start, dimension_line.y_start),
                svg.Rotate(math.degrees(angle)),
                svg.Translate(0, dimension_line.offset)
            ]

            is_horizontal_dimension_line = dimension_line.elevation_start == dimension_line.elevation_end

            if is_horizontal_dimension_line:
                main_line = svg.Line(
                    x1=0,
                    y1=0,
                    x2=dimension_line.length,
                    y2=0,
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    stroke_width=dimension_line_stroke,
                    transform=transformations
                )

                self.elements.append(main_line)

                end_mark = svg.Path(
                    d=self._skia_path_to_svg_d(mark_end),
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    transform=transformations + [svg.Scale(mark_end_scale, mark_end_scale)]
                )
                self.elements.append(end_mark)
                end_mark = svg.Path(
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    d=self._skia_path_to_svg_d(mark_end),
                    transform=transformations + [
                        svg.Translate(dimension_line.length / mark_end_scale, 0),
                        svg.Scale(mark_end_scale, mark_end_scale)
                    ]
                )
                self.elements.append(end_mark)

                line = svg.Line(
                    x1=0,
                    y1=-dimension_line.offset,
                    x2=0,
                    y2=0,
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    stroke_width=1 / plan_scale,
                    stroke_linecap='square',
                    stroke_dasharray=extension_line_stroke,  # type:ignore[arg-type]
                    transform=transformations
                )

                self.elements.append(line)

                line = svg.Line(
                    x1=dimension_line.length,
                    y1=-dimension_line.offset,
                    x2=dimension_line.length,
                    y2=0,
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    stroke_width=1 / plan_scale,
                    stroke_linecap='square',
                    stroke_dasharray=extension_line_stroke,  # type:ignore[arg-type]
                    transform=transformations
                )

                self.elements.append(line)

            else:
                disc = svg.Polygon(
                    points=[coord for point in VERTICAL_DIMENSION_LINE_DISC.exterior.coords for coord in point],
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    transform=transformations + [svg.Scale(mark_end_scale, mark_end_scale)]
                )
                self.elements.append(disc)

                line_polygon = svg.Polygon(
                    points=[coord for point in VERTICAL_DIMENSION_LINE.exterior.coords for coord in
                            point],
                    stroke=dimension_line.color.hex,
                    stroke_opacity=dimension_line.color.alpha_float,
                    fill_opacity=0,
                    transform=transformations + [svg.Scale(mark_end_scale, mark_end_scale)]
                )
                self.elements.append(line_polygon)

                if abs(dimension_line.offset) > (dimension_line.end_mark_size / 2):
                    y2_multiplier = -1
                    if dimension_line.offset > -1:
                        y2_multiplier = 0 if dimension_line.offset == 0 else 1

                    line = svg.Line(
                        x1=0,
                        y1=-dimension_line.offset,
                        x2=0,
                        y2=-dimension_line.end_mark_size / 2 * y2_multiplier,
                        stroke=dimension_line.color.hex,
                        stroke_opacity=dimension_line.color.alpha_float,
                        stroke_width=1 / plan_scale,
                        stroke_linecap='square',
                        stroke_dasharray=extension_line_stroke,  # type:ignore[arg-type]
                        transform=transformations
                    )

                    self.elements.append(line)
            resolution_scale = 1.0
            # Dimensional line text
            dimension_line_text = '{:.3f}'.format(dimension_line.length / 100)
            font = skia.Font(skia.Typeface.MakeDefault(), dimension_line.length_style.font_size)
            text_metrics = font.getMetrics()
            text_width = font.measureText(dimension_line_text, skia.TextEncoding.kUTF8)

            text_transformations: List[svg.Transform] = []
            if not is_horizontal_dimension_line:
                text_transformations.append(svg.Rotate(math.degrees(math.pi / 2 if angle > math.pi else -math.pi / 2)))

                if (dimension_line.offset <= 0) ^ (angle <= math.pi):
                    text_x = -(text_width / 2) - mark_end_width / 2 - 5 / plan_scale / resolution_scale
                else:
                    text_x = mark_end_width / 2 + 5 / plan_scale / resolution_scale

                text_y = text_metrics.fCapHeight / 2
            else:
                text_x = dimension_line.length / 2

                if dimension_line.offset <= 0:
                    text_y = -text_metrics.fDescent - 1
                else:
                    text_y = text_metrics.fCapHeight / 2 + mark_end_width / 2 + 5 / plan_scale / resolution_scale

            text_transformations.append(svg.Translate(text_x, text_y))

            text = svg.Text(
                text=dimension_line_text,
                x=0,
                y=0,
                font_family="Arial",
                fill=dimension_line.color.hex,
                fill_opacity=dimension_line.color.alpha_float,
                font_size=dimension_line.length_style.font_size,
                transform=transformations + text_transformations,
                text_anchor=self._alignment_to_svg.get(dimension_line.length_style.alignment, 'middle')
            )

            self.elements.append(text)




    def drawn_furniture(self, furniture: List[HomePieceOfFurniture], walls: List[Wall], plan_scale: float) -> None:
        for item in furniture:
            # Embed images
            identifier = 'icon_{}'.format(item.icon.image.content_digest.digest.hex())
            if identifier not in self.definitions:
                image = svg.Image(
                    href='data:image/png;base64,{}'.format(base64.b64encode(item.icon.image.data).decode()),
                    width=item.icon.width,
                    height=item.icon.height
                )
                self.definitions[identifier] = svg.Symbol(
                    id=identifier,
                    viewBox=svg.ViewBoxSpec(
                        min_x=0,
                        min_y=0,
                        width=item.icon.width,
                        height=item.icon.height
                    ),
                    elements=[image]
                )

            if not isinstance(item, HomeDoorOrWindow):
                # Display background rect only when not window or door
                furniture_rect = svg.Polygon(
                    id=item.identifier,
                    stroke_width=1,
                    stroke='#5c5959',
                    fill='white',
                    fill_opacity=0 if isinstance(item, HomeDoorOrWindow) else 100,
                    points=[coord for point in item.geometry.exterior.coords for coord in point]
                )

                self.elements.append(furniture_rect)
            icon_geometry = item.geometry

            if isinstance(item, HomeDoorOrWindow):
                # Sashes
                for sash in item.sashes:
                    sash_polygon = svg.Polygon(
                        id=item.identifier,
                        stroke_width=1,
                        fill_opacity=0,
                        stroke='black',
                        points=[coord for point in sash.geometry.exterior.coords for coord in point]
                    )
                    self.elements.append(sash_polygon)

                # Match wall
                matched_wall: Optional[Wall] = None
                max_area = 0.0
                for wall in walls:
                    if item.geometry.intersects(wall.geometry):
                        intersection = item.geometry.intersection(wall.geometry)
                        area = intersection.area
                        if area > max_area:
                            max_area = area
                            matched_wall = wall

                if matched_wall:
                    door_or_window_geometry = item.geometry.intersection(matched_wall.geometry)
                    icon_geometry = door_or_window_geometry
                    furniture_wall_rect = svg.Polygon(
                        id=item.identifier,
                        stroke_width=1,
                        fill='white',
                        stroke='black',
                        points=[coord for point in door_or_window_geometry.exterior.coords for coord in point]
                    )

                    self.elements.append(furniture_wall_rect)

            minx, miny, maxx, maxy = icon_geometry.bounds

            icon = svg.Use(
                href='#{}'.format(identifier),
                x=minx,
                y=miny,
                width=maxx - minx,
                height=maxy - miny
            )

            self.elements.append(icon)

    def drawn_polylines(self, polylines: List[Polyline], plan_scale: float) -> None:
        for polyline in polylines:
            # Standard path
            if isinstance(polyline.polyline_path, LineString):
                coordinates = polyline.polyline_path.coords
                polyline_poly = svg.Polyline(
                    id=polyline.identifier,
                    stroke_width=polyline.thickness,
                    stroke=polyline.color.hex,
                    stroke_opacity=polyline.color.alpha_float,
                    fill='none',
                    stroke_linecap=polyline.cap_style.value.lower() if polyline.cap_style else None,
                    stroke_linejoin=polyline.join_style.value.lower() if polyline.join_style else None,
                    stroke_dasharray=polyline.dash_pattern,
                    points=[coord for point in coordinates for coord in point]
                )
                self.elements.append(polyline_poly)
            else:
                coordinates = polyline.polyline_path.exterior.coords
                polygon_poly = svg.Polygon(
                    id=polyline.identifier,
                    stroke_width=polyline.thickness,
                    stroke=polyline.color.hex,
                    stroke_opacity=polyline.color.alpha_float,
                    fill='none',
                    stroke_linejoin=polyline.join_style.value.lower() if polyline.join_style else None,
                    stroke_dasharray=polyline.dash_pattern,
                    points=[coord for point in coordinates for coord in point]
                )

                self.elements.append(polygon_poly)


    def drawn_arrow(self, point: Tuple[float, float], angle: float, arrow_style: ArrowStyle, thickness: float, color: Color, delta: float) -> None:
        scale = math.pow(thickness, 0.66) * 2
        transforms = [
            svg.Translate(point[0], point[1]),
            svg.Rotate(math.degrees(angle)),
            svg.Translate(delta, 0),
            svg.Scale(scale, scale)
        ]

        if arrow_style == ArrowStyle.DISC:
            self.elements.append(svg.Ellipse(
                fill=color.hex,
                fill_opacity=color.alpha_float,
                cx=-1.5,
                cy=0,
                rx=2,
                ry=2,
                transform=transforms
            ))
        elif arrow_style in [ArrowStyle.OPEN, ArrowStyle.DELTA]:
            if arrow_style == ArrowStyle.OPEN:
                transforms.append(svg.Scale(0.9, 0.9))
            else:
                transforms.append(svg.Translate(1.65, 0))
            arrow = svg.Path(
                stroke=color.hex if arrow_style == ArrowStyle.OPEN else None,
                stroke_opacity=color.alpha_float if arrow_style == ArrowStyle.OPEN else None,
                fill=color.hex if arrow_style.DELTA else 'none',
                fill_opacity=color.alpha_float,
                stroke_width=(thickness/ scale / 0.9) if arrow_style == ArrowStyle.OPEN else None,
                stroke_linecap='butt',
                stroke_linejoin='miter',
                d=[
                    svg.MoveTo(-5, -2),
                    svg.LineTo(0, 0),
                    svg.LineTo(-5, 2)
                ],
                transform=transforms
            )
            self.elements.append(arrow)

    def drawn_labels(self, labels: List[Label], plan_scale: float) -> None:
        for label in labels:
            self.drawn_text(label.text, label.x, label.y, label.angle, label.style, label.color, label.outline_color)

    def drawn_text(self, text: str, x: float, y: float, angle: float, style: TextStyle, color: Color, outline_color: Optional[Color] = None) -> None:
        lines = text.split('\n')
        line_height = style.font_size * 1.2
        group = svg.G(
            transform=[
                svg.Translate(x, y),
                svg.Rotate(math.degrees(angle))
            ]
        )
        svg_lines: List[svg.Element] = []
        for i, line in enumerate(reversed(lines)):
            dy = -i * line_height


            svg_line = svg.Text(
                text=line,
                x=0,
                y=dy,
                font_family="Arial",
                fill=color.hex,
                fill_opacity=color.alpha_float,
                stroke=outline_color.hex if outline_color else None,
                stroke_opacity=outline_color.alpha_float if outline_color else None,
                font_size=style.font_size,
                text_anchor=self._alignment_to_svg.get(style.alignment, 'middle')
            )

            svg_lines.append(svg_line)

        group.elements = svg_lines
        self.elements.append(group)

    def plot(self, level: Optional[Level] = None) -> bytes:
        self.render(level)

        canvas = svg.SVG(
            viewBox=svg.ViewBoxSpec(self.plan_bounds.x, self.plan_bounds.y, self.plan_bounds.width,
                                    self.plan_bounds.height),
            data={'version': self.home.version},
            width=self.plan_bounds.width,
            height=self.plan_bounds.height,
            elements=self.elements + list(self.definitions.values()),
        )

        # Reset
        self.elements = []
        self.definitions = {}

        return canvas.as_str().encode('UTF-8')

    def save_to_file(self, path: Path, level: Optional[Level] = None) -> None:
        content = self.plot(level)

        with path.open('wb') as f:
            f.write(content)
