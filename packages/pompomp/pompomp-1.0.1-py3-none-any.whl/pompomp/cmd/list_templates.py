"""
CLI command to list available templates in the "templates/" directory.

Each template must contain a "meta.yml" file with structured metadata.
If missing or invalid, the template is skipped with a warning.

Supports:
- Standard view: shows Name, Version, Authors, Description, and Tags.
- Raw view (--raw): shows technical folder names with meta.yml presence info.

This helps explore and select available themes for use in other commands.

Options:
    --raw, -r       Show only folder names (technical view), skip metadata parsing
"""
from pathlib import Path

import typer

from pompomp.cmd.console import box, console, Table
from pompomp.constants import TEMPLATES_ROOT, TEMPLATES_METADATA_FILENAME
from pompomp.loaders.metadata_loader import load_template_metadata, TemplateMetadata


def _list_raw_templates(template_dirs: list[Path]) -> None:
    """Print raw folder names, highlighting missing meta.yml."""
    console.print("[bold]✨ Available Templates (Raw View):[/bold]\n")
    for folder in sorted(template_dirs):
        meta_file = folder / TEMPLATES_METADATA_FILENAME
        if meta_file.exists():
            console.print(f"- [green]{folder.name}[/green]")
        else:
            console.print(f"- [yellow]{folder.name}[/yellow] [dim](no meta.yml found)[/dim]")


def _list_full_templates(template_dirs: list[Path]) -> None:
    """Print full table of templates with metadata."""
    table = Table(title="Available Templates", box=box.SIMPLE_HEAD, show_lines=True)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Folder", style="green", no_wrap=True)
    table.add_column("Version", style="dim", no_wrap=True)
    table.add_column("Authors", style="yellow", no_wrap=True)
    table.add_column("Description", style="dim")
    table.add_column("Tags", style="dim")

    for folder in sorted(template_dirs):
        try:
            metadata: TemplateMetadata = load_template_metadata(folder / TEMPLATES_METADATA_FILENAME)
            authors = "- " + "\n- ".join(a.name for a in (metadata.authors or [])) if metadata.authors else "-"
            tags = ", ".join(metadata.tags) if metadata.tags else "-"
            desc = metadata.description or "-"

            table.add_row(
                metadata.name,
                folder.name,
                metadata.version or "-",
                authors,
                desc,
                tags,
            )
        except FileNotFoundError:
            console.print(f"[bold yellow]⚠️ No {TEMPLATES_METADATA_FILENAME} found in:[/bold yellow] {folder.name}")
        except Exception as e:
            console.print(f"[bold red]❌ Failed to load:[/bold red] {folder.name} ({e})")

    console.print(table)


def list_templates(
        raw: bool = typer.Option(
            False, "--raw", "-r", help="Only output technical template names (folders)."
        )
) -> None:
    """List available templates (themes) installed locally."""
    template_dirs = [p for p in Path(TEMPLATES_ROOT).iterdir() if p.is_dir()]

    if not template_dirs:
        console.print("[bold red]❌ No templates found in[/bold red] templates/ directory.")
        raise typer.Exit(code=1)

    console.print(f"[dim]📁 All templates are listed from:[/dim] {TEMPLATES_ROOT}\n")
    if raw:
        _list_raw_templates(template_dirs)
    else:
        _list_full_templates(template_dirs)
