"""
CLI command: `show-icons` : Preview available icons from the current theme.

Displays a styled table showing all icons grouped by family (e.g., 'ui', 'icons'),
with optional filtering by family/subgroup and DSL-usable key format.

Options:
    --family, -f TEXT     Filter by icon family or subgroup (e.g. 'ui.divider', 'icons.git')
    --dsl-names, -d       Show only canonical DSL keys (e.g. 'divider.right_half_circle')
"""
import typer

from pompomp.cmd.console import box, console, Table
from pompomp.loaders.icons_loader import load_icons


def resolve_families(icons, family: str):
    family_top, _, _ = family.partition(".")
    families = []
    if family_top in ("all", "ui"):
        families.append(("ui", icons.ui))
    if family_top in ("all", "icons"):
        families.append(("icons", icons.icons))
    return family_top, family.partition(".")[2], families


def collect_group_rows(group: dict, family_name: str, group_name: str, dsl_names: bool):
    rows = []
    for key, entry in group.items():
        show_key = key if dsl_names else f"{group_name}.{key}"
        rows.append((family_name, show_key, entry.get("glyph", ""), entry.get("code", "")))
    return rows


def collect_icon_rows(icons, family: str, dsl_names: bool):
    """Build rows for the table of icons, based on family/subgroup filtering."""
    family_top, family_group, families = resolve_families(icons, family)
    rows = []

    for family_name, family_dict in families:
        if family_top != "all" and family_name != family_top:
            continue
        for group_name, group in family_dict.items():
            if family_group and group_name != family_group:
                continue
            rows.extend(collect_group_rows(group, family_name, group_name, dsl_names))

    return rows


def show_icons(
    family: str = typer.Option(
        "all",
        "--family", "-f",
        help="Filter by family or sub-group (e.g. 'icons', 'icons.os' or 'ui.divider')"
    ),
    dsl_names: bool = typer.Option(
        False,
        "--dsl-names", "-d",
        help="Show only DSL-usable names (canonical names)"
    ),
):
    """
    Display available icons grouped by family, with optional DSL filtering.
    """
    icons = load_icons("default")
    rows = collect_icon_rows(icons, family, dsl_names)

    table = Table(
        title="🔤 Icons Available in Theme",
        show_lines=False,
        box=box.SIMPLE_HEAD
    )
    table.add_column("Family", style="cyan")
    table.add_column("Key", style="green")
    table.add_column("Glyph", style="bold", justify="center")
    table.add_column("Code", style="dim", justify="center")

    for row in rows:
        table.add_row(*row)

    console.print(table)
