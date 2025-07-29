"""
CLI command: `set-meta` : Update meta.yml in a theme's layout folder.

This command updates one or more metadata keys (e.g. `line_mode`)
inside `templates/<theme>/layouts/meta.yml`.

Examples:
    pompomp set-meta --set line_mode=2 --theme pompomp
"""
from pathlib import Path

import typer
from ruamel.yaml import YAML

# noinspection PyShadowingBuiltins
from pompomp.cmd.console import rprint as print, console, Table, box
from pompomp.constants import (
    TEMPLATES_ROOT,
    DEFAULT_THEME_DIRNAME,
    DEFAULT_LAYOUTS_DIRNAME,
    TEMPLATES_METADATA_FILENAME,
    LAYOUT_SHORTCUTS_MAP,
    YAML_ENCODING,
)
from pompomp.helpers.meta import update_meta_key

yaml = YAML()
yaml.preserve_quotes = True


def _resolve_line_mode(value: str) -> str:
    normalized = value.lower().strip()
    if normalized not in LAYOUT_SHORTCUTS_MAP:
        valid = ", ".join(sorted(LAYOUT_SHORTCUTS_MAP))
        print(f"[bold red]❌ Invalid line_mode:[/] '{value}'\n[dim]Allowed values:[/] {valid}")
        raise typer.Exit(code=1)
    return LAYOUT_SHORTCUTS_MAP[normalized]


def _load_meta_file(theme: str) -> Path:
    path = TEMPLATES_ROOT / theme / DEFAULT_LAYOUTS_DIRNAME / TEMPLATES_METADATA_FILENAME
    if not path.exists():
        print(f"[bold red]❌ meta.yml not found for theme:[/] {theme} → {path}")
        raise typer.Exit(code=1)
    return path


def set_meta(
        _set: list[str] = typer.Option(..., "--set", help="Meta key=value pair to set (repeatable)"),
        theme: str = typer.Option(DEFAULT_THEME_DIRNAME, "--theme", "-t", help="Target theme to update")
) -> None:
    path = _load_meta_file(theme)

    for entry in _set:
        if "=" not in entry:
            print(f"[bold red]❌ Invalid --set format:[/] '{entry}' (expected key=value)")
            raise typer.Exit(code=1)

        key, value = map(str.strip, entry.split("=", 1))

        if key == "line_mode":
            value = _resolve_line_mode(value)

        update_meta_key(path, key, value)


def show_meta(
        theme: str = typer.Option(DEFAULT_THEME_DIRNAME, "--theme", "-t", help="Theme to inspect")
) -> None:
    path = _load_meta_file(theme)

    try:
        with path.open("r", encoding=YAML_ENCODING) as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"[bold red]❌ Failed to read meta.yml:[/] {e}")
        raise typer.Exit(code=1)

    if not data:
        print(f"[yellow]⚠️ meta.yml is empty or malformed in theme '{theme}'.[/yellow]")
        raise typer.Exit()

    table = Table(title=f"Meta configuration for theme: [bold]{theme}[/bold]",
                  show_lines=True, box=box.SIMPLE_HEAD, width=console.width / 3)
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console.print(table)
