"""
Handler to resolve [icons:...] DSL blocks.

Resolves references to icons defined in `icons.yml`, allowing access to either
the `glyph` (default) or the `code` (e.g., U+E725) for any icon in the `icons:` section.

Supported formats:
    [icons:family.name] → returns the icon's glyph
    [icons:family.name.code] → returns the icon's Unicode code

Examples:
    [icons:prompt.folder] → 
    [icons:git.branch_icon.code] → U+E725

Raises:
    - ValueError if the path format is invalid
    - KeyError if the family, name, or attribute is not found in icons.yml
"""
import re
from typing import Any

from pompomp.constants import DEFAULT_THEME_DIRNAME
from pompomp.dsl.handlers.palette import resolve_palette
from pompomp.loaders.icons_loader import load_icons

RE_ICONS = re.compile(r"^(?P<family>[^.]+)\.(?P<name>[^.]+)(?:\.(?P<attr>glyph|code))?$")


def resolve_icons(value: str, trace: bool = False, *_args, theme: str = DEFAULT_THEME_DIRNAME) -> Any:
    """
    Resolve an [icons:...] DSL block to its corresponding glyph or Unicode codepoint.

    Supports patterns like:
        [icons:prompt.folder] → resolves to its glyph
        [icons:prompt.folder.code] → resolves to its Unicode code
        [icons:prompt.folder, palette:roles.line] → resolves to a styled glyph

    Args:
        value (str): DSL icon reference in the form 'family.name[.attr]'.
        trace (bool): If True, prints the resolved result.
        *_args: Unused (for DSL handler signature compatibility).
        theme (str): The theme name used to load the icons.yml file.

    Returns:
        str: The resolved glyph or styled glyph if palette is provided.

    Raises:
        ValueError: If the icon path format is invalid.
        KeyError: If the icon or its attribute is missing in the theme.
    """
    # Split the value by "," to capture palette if present
    parts = [p.strip() for p in value.split(",")]
    icon_ref = parts[0]

    # Resolve icon family and name
    match = RE_ICONS.match(icon_ref)
    if not match:
        raise ValueError(f"Invalid icons path: '{icon_ref}' (expected format: family.name[.attr])")

    family = match.group("family")
    name = match.group("name")
    attr = match.group("attr") or "glyph"

    icons = load_icons(theme)

    try:
        data = icons.icons[family][name]
    except KeyError:
        raise KeyError(f"Missing icon entry: '{family}.{name}' in theme: '{theme}'")

    if attr not in data:
        raise KeyError(f"Attribute '{attr}' not found for icon: '{family}.{name}' in theme: '{theme}'")

    glyph_or_code = data[attr]

    styles = []
    for part in parts[1:]:
        if part.startswith("palette:"):
            resolved_color = resolve_palette(part.split(":", 1)[1], trace=trace, theme=theme)
            styles.append(resolved_color)

    if trace:
        print(f"[TRACE] [icons] {family}.{name}.{attr} → {glyph_or_code}")

    if styles:
        return f"<{styles[0]}>{glyph_or_code}</>"

    return glyph_or_code
