# sh3dkit

**sh3dkit** is a flexible and extensible Python library and command-line interface (CLI) toolset for working with `.sh3d` files, commonly used by Sweet Home 3D. It provides an easy way to render, visualize, and convert `.sh3d` files into other formats such as SVG, while offering an architecture to add support for additional renderers in the future.

## Key Features:
- **Render .sh3d files**: Extracts and visualizes floor plans and 3D home designs from `.sh3d` files.
- **Format Conversion**: Convert `.sh3d` files into various output formats, including SVG, and with the potential for more formats in the future.
- **Extensible**: Built with flexibility in mind, allowing for easy addition of new rendering engines (e.g., Matplotlib, custom formats).
- **CLI and Library**: Provides both a command-line interface (CLI) and a Python library for use in automated workflows or custom applications.
- **Easy Integration**: Installable via `pip` and ready to use in your Python projects.

Whether you're an architect, a designer, or a developer working with home design data, `sh3dkit` enables efficient processing of Sweet Home 3D project files for your own needs.

## CLI

Currently only convertion into SVG is supported by using sh3d2svg command provided in `sh3dkit/bin/sh3d2svg.py`, it usage is:

```bash
Usage: sh3d2svg [OPTIONS] INPUT_FILE

Options:
  -o, --output TEXT      Output SVG file path.
  -l, --level-name TEXT  What level name to render, if not specified all are
                         rendered into separate files automatically.
  --help                 Show this message and exit.
```

## API

Single renderer interface is provided for implementation in `sh3dkit/renderer/HomeRenderer.py`, SVG renderer used by `sh3d2svg` command is implemented in `sh3dkit/renderer/SvgHomeRenderer.py`.
"Only" these functions are required to be implemented to get your custom renderer working:

```python
from typing import List, Tuple, Optional
from pathlib import Path
import skia
from sh3d.model.Wall import Wall
from sh3d.model.TextureImage import TextureImage
from sh3d.model.DimensionLine import DimensionLine
from sh3d.model.Polyline import Polyline, ArrowStyle
from sh3d.model.BackgroundImage import BackgroundImage
from sh3d.model.Room import Room
from sh3d.model.Color import Color
from sh3d.model.TextStyle import TextStyle
from sh3d.model.Label import Label
from sh3d.model.HomePieceOfFurniture import HomePieceOfFurniture
from sh3dkit.renderer.HomeRenderer import HomeRenderer


class MyCustomHomeRenderer(HomeRenderer):

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

    def drawn_furniture(self, furniture: List[HomePieceOfFurniture], walls: List[Wall], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_arrow(self, point: Tuple[float, float], angle: float, arrow_style: ArrowStyle, thickness: float, color: Color, delta: float) -> None:
        raise NotImplementedError

    def drawn_labels(self, labels: List[Label], plan_scale: float) -> None:
        raise NotImplementedError

    def drawn_text(self, text: str, x: float, y: float, angle: float, style: TextStyle, color: Color, outline_color: Optional[Color] = None) -> None:
        raise NotImplementedError

    def save_to_file(self, path: Path) -> None:
        raise NotImplementedError
```

Objects `Wall`, `DimensionLine`, `Polyline`, `Room`, `Label`, `HomePieceOfFurniture`, `HomeDoorOrWindow(HomePieceOfFurniture)`  implement `Renderable` that provides properties `points` and `geometry`, where `points` are List of tuples containing x, y coordinates and `geometry` returns shapely shape.