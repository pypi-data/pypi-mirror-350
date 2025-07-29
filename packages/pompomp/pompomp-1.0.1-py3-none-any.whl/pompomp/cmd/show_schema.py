"""
CLI command: `show-schema` : Display DSL schema definitions.

This command lets you explore the available DSL block types (e.g., [inc:], [palette:], [if ...])
and style tags usable in inline DSL strings.

Options:
    --mode, -m TEXT     Show specific schema section: "style-tags", "blocks", or "all" (default).
"""
import typer

from pompomp.cmd.console import box, console, Table, escape
from pompomp.core_constants import STYLE_TAGS, STYLE_ALIASES
from pompomp.dsl.schema import DSL_SCHEMA_INFO


def _show_style_tags() -> None:
    # Build (short, full) pairs from both directions to future-proof against non-bijective mappings.
    # This ensures all valid style aliases are shown, even if not symmetrically defined.
    style_rows = set()
    for full, short in STYLE_TAGS.items():
        style_rows.add((short, full))
    for short, full in STYLE_ALIASES.items():
        style_rows.add((short, full))

    tag_table = Table(title="🎨 Style Tags", show_lines=True, box=box.HORIZONTALS)
    tag_table.add_column("Short", style="cyan")
    tag_table.add_column("Full name", style="dim")

    for short, full in sorted(style_rows):
        tag_table.add_row(short, full)
    console.print(tag_table)

def show_schema(
        mode: str = typer.Option(
            "all",
            "--mode", "-m",
            help="Show specific part of DSL schema: style-tags, blocks, or all"
        )
):
    if mode in ("all", "style-tags"):
        _show_style_tags()

    if mode in ("all", "blocks"):
        block_table = Table(title="📦 DSL Blocks", show_lines=True, box=box.SIMPLE_HEAD)
        block_table.add_column("Key", style="cyan")
        block_table.add_column("Details", style="green")

        for prefix, meta in DSL_SCHEMA_INFO.items():
            block_table.add_row(prefix, f"[bold yellow]Description:[/bold yellow] {meta["description"]}")
            block_table.add_row("", f"[bold yellow]Example:[/bold yellow] {escape(meta['example'])}")
            block_table.add_row("", f"[bold yellow]Returns:[/bold yellow] {meta['expected']}")

            notes = meta.get("notes", [])
            for i, note in enumerate(notes):
                prefix_label = "Notes:" if i == 0 else ""
                block_table.add_row("", f"[bold yellow]{prefix_label} -[/bold yellow] {escape(note)}")
            block_table.add_row("", "")

        console.print(block_table)
