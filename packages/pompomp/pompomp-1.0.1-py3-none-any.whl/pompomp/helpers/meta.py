"""Helper for updating a specific key in meta.yml with YAML preservation."""
from pathlib import Path

import typer
from ruamel.yaml import YAML

# noinspection PyShadowingBuiltins
from pompomp.cmd.console import rprint as print
from pompomp.core_constants import YAML_ENCODING


def update_meta_key(meta_path: Path, key: str, value: str | None) -> None:
    """
    Update a specific key in meta.yml safely, with YAML preservation.

    Args:
        meta_path: Path to the meta.yml file.
        key: Key to update (e.g., "line_mode").
        value: New value to set, or None to set it to null.
    """
    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with meta_path.open("r", encoding=YAML_ENCODING) as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"[bold red]❌ Failed to load meta.yml:[/] {e}")
        raise typer.Exit(code=1)

    data[key] = value if value is not None else None

    try:
        with meta_path.open("w", encoding=YAML_ENCODING) as f:
            yaml.dump(data, f)
        print(f"[bold green]✅ {key} updated to:[/] {value or 'null'} [dim]({meta_path})")
    except Exception as e:
        print(f"[bold red]❌ Failed to write meta.yml:[/] {e}")
        raise typer.Exit(code=1)
