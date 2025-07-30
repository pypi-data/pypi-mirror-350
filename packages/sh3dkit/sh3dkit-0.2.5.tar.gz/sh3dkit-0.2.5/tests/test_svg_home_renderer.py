import tempfile
from pathlib import Path
from sh3d.model.Home import Home

from sh3dkit.renderer.SvgHomeRenderer import SvgHomeRenderer


def test_can_init(home: Home) -> None:
    svg_home_renderer = SvgHomeRenderer(home)
    assert isinstance(svg_home_renderer, SvgHomeRenderer)

def test_can_render(home: Home) -> None:
    svg_home_renderer = SvgHomeRenderer(home)
    svg_home_renderer.render()


def test_can_render_to_file(home: Home) -> None:
    temp = tempfile.NamedTemporaryFile()
    svg_home_renderer = SvgHomeRenderer(home)
    svg_home_renderer.save_to_file(Path(temp.name))