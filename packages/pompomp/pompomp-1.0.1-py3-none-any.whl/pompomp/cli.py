"""
Main CLI entrypoint for the pompomp application.

This module uses Typer to define and register all CLI subcommands,
including options like --version, and commands such as
- info
- show-palette
- generate
- convert
- and more...

It also displays metadata and routes subcommands to their handlers.
"""

from typing import Optional

import typer

from pompomp import meta
from pompomp.cmd import (
    convert,
    generate,
    list_templates,
    scaffold,
    set_meta,
    show_icons,
    show_meta,
    show_palette,
    show_schema,
    show_vars,
)
# noinspection PyShadowingBuiltins
from pompomp.cmd.console import Table, console, rprint as print

app = typer.Typer(add_completion=False)


def _version_callback(value: bool) -> None:
    if value:
        print(f"[light_salmon1]{meta.__app_name__}[/] v{meta.__version__}")
        raise typer.Exit()


@app.callback()
def main(
        _version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


@app.command(help="Display basic or full metadata about the pompomp project")
def info(
        full: bool = typer.Option(
            False,
            "--full",
            "-f",
            help="Show full information about the application.",
        ),
) -> None:
    print(meta.__logo__)

    if full:
        _data = [
            ("Name", meta.__app_name__),
            ("Version", meta.__version__),
            ("Description", meta.__description__),
            ("Author", meta.__author__),
            ("Email", meta.__email__),
            ("URL", meta.__url__),
            ("Keywords", ", ".join(meta.__keywords__)),
            ("Classifiers", "\n".join(meta.__classifiers__)),
            ("License Type", meta.__license_type__),
            ("License", meta.__license__),
            ("", ""),
        ]

        table = Table(show_header=False, show_lines=False, title=None, box=None)
        table.add_column(justify="right")
        table.add_column(justify="left")

        for row in _data:
            table.add_row(f"[light_salmon1]{row[0]}[/]", row[1])

        console.print(table)
        return

    _version_callback(True)


# Register all CLI subcommands
app.command(help="List all icons available in the current theme")(show_icons)
app.command(help="Show the current theme palette with color previews")(show_palette)
app.command(help="List all supported DSL blocks and their behaviors")(show_schema)
app.command(help="Show all official OMP template variables")(show_vars)
app.command(help="Create a layout YAML file from predefined blueprints")(scaffold)
app.command(help="Convert a theme or config file between YAML, JSON, and TOML formats")(convert)
app.command(help="Generate an OMP-compatible theme from a pompomp DSL input file")(generate)
app.command(help="List all available templates")(list_templates)
app.command(help="Update meta variables inside templates/<theme>/layouts/meta.yml")(set_meta)
app.command(help="Show all meta variables inside templates/<theme>/layouts/meta.yml")(show_meta)

if __name__ == "__main__":
    app()
