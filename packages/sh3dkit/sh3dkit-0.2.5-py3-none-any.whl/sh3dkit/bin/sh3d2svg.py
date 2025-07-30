#!/usr/bin/python
import re
from pathlib import Path
from typing import Optional, List
import click
from sh3d.FileLoader import FileLoader
from sh3d.model.Level import Level
from sh3dkit.renderer.SvgHomeRenderer import SvgHomeRenderer


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='output.svg', help='Output SVG file path.')
@click.option('--level-name', '-l', default=None, help='What level name to render, if not specified all are rendered into separate files automatically.')
def main(input_file: str, output: str, level_name: Optional[str] = None) -> None:
    input_path = Path(input_file)
    output_path = Path(output)
    with FileLoader(input_path) as file_loader:
        render_levels: List[Level] = []
        if level_name:
            level_by_name = {l.name: l for l in file_loader.home.levels}
            found_level = level_by_name.get(level_name)
            if not found_level:
                click.echo("Error: requested Level not found!", err=True)
                click.echo('Valid Level names are: {}'.format(list(level_by_name.keys())))
                raise click.BadParameter(level_name)
            render_levels.append(found_level)
        else:
            render_levels.extend(file_loader.home.levels)

        svg_home_renderer = SvgHomeRenderer(file_loader.home)
        if render_levels:
            for level in render_levels:
                level.is_visible = True  # Force level to be always visible
                sanitized_level_name = re.sub(r'[^A-Za-z0-9_.-]', '_', level.name)
                modified_path = output_path.parent.joinpath('{}_{}'.format(output_path.stem, sanitized_level_name + output_path.suffix))
                click.echo(f'Rendering {input_file} to {modified_path}')
                svg_home_renderer.save_to_file(modified_path, level)
        else:
            click.echo(f'Rendering {input_file} to {output}')
            svg_home_renderer.save_to_file(output_path)


if __name__ == '__main__':
    main()
