"""
CLI command: `show-palette` : Preview a theme's palette with colors and contrast rendering.

Displays a styled table showing the mapping of palette roles to color names and hex values,
with optional color preview and dynamic contrast adjustment for readability.

Options:
    --theme, -t TEXT      Theme name to preview (default: 'default')
    --contrast, -c INT    Contrast threshold for font color (0–255, default: 151)
"""
import typer

from pompomp.cmd.console import box, console, Table, Text
from pompomp.helpers.colors import get_contrast_color
from pompomp.loaders.palette_loader import load_palette
from pompomp.models.palette import ALIAS_MAP


def show_palette(
        theme: str = typer.Option(
            "default",
            "--theme", "-t",
            help="Theme name to preview (default: 'default')"
        ),
        contrast: int = typer.Option(
            151,
            "--contrast", "-c",
            min=0,
            max=255,
            help="Contrast threshold for font color (default: 151)"
        )
) -> None:
    palette = load_palette(theme)

    if palette.meta.get("name", "").lower() != theme.lower() and theme.lower() != "default":
        console.print(
            f"[bold yellow]⚠️ Theme '{theme}' not found. "
            f"Using fallback: '{palette.meta.get('name', 'default')}'[/]\n"
        )

    table = Table(title=f"🎨 Palette: {palette.meta.get('name', theme)}", show_lines=True, box=box.SIMPLE_HEAD)

    table.add_column("Role", style="bold")
    table.add_column("Alias", style="green")
    table.add_column("Color Name")
    table.add_column("Hex", justify="center")
    table.add_column("Preview", justify="center")

    for role, color_name in palette.roles.items():
        hex_code = palette.colors.get(color_name, None)
        if hex_code is None:
            hex_code = "[red]❌ missing[/]"
            preview = "N/A"
        else:
            font_color = get_contrast_color(hex_code, threshold=contrast)
            preview = Text(hex_code, style=f"{font_color} on {hex_code}")

        aliases = [a for a, r in ALIAS_MAP.items() if r == role]
        alias_str = ", ".join(aliases) if aliases else ""

        table.add_row(role, alias_str, color_name, hex_code, preview)

    console.print(table)
