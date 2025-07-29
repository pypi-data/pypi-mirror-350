"""
Handler for resolving [ui:...] DSL blocks.

This module handles the transformation of UI directives in the DSL,
typically used to render visual glyphs (e.g. powerline symbols) with optional
styling (foreground, background, transparency).

Features:
- Supports both `.glyph` and `.code` attributes.
- Allows inline styling via `transparent`, raw hex, or palette-based roles.
- Compatible with multi-level icon resolution (e.g. ui.divider.right_half_circle_thick).

Example usages:
    [ui:divider.right_half_circle_thick]
    [ui:divider.right_half_circle_thick.code]
    [ui:divider.right_half_circle_thick, transparent]
    [ui:divider.right_half_circle_thick, palette:roles.line, transparent]

Functions:
    - resolve_ui(value, trace, target_key, theme) → str
"""
from typing import Optional

from pompomp.constants import DEFAULT_THEME_DIRNAME
from pompomp.dsl.handlers.palette import resolve_palette
from pompomp.dsl.schema import ALLOWED_COLOR_KEYWORDS
from pompomp.loaders.icons_loader import load_icons


def resolve_ui(value: str, trace: bool = False, target_key: Optional[str] = None,
               theme: str = DEFAULT_THEME_DIRNAME) -> str:
    """
    Resolve a [ui:...] DSL block into a styled icon or glyph.

    This handler supports rendering of icons defined in icons.yml, with optional color or palette-based styles.

    Examples:
        [ui:divider.right_half_circle_thick] → ''
        [ui:divider.right_half_circle_thick.code] → 'U+E0B4'
        [ui:divider.right_half_circle_thick, transparent] → '<transparent></>'
        [ui:divider.right_half_circle_thick, palette:roles.line, transparent] → '<#hex,transparent></>'

    Args:
        value (str): The full DSL string to resolve, including icon path and optional styles.
        trace (bool): If True, prints resolution trace logs.
        target_key (str, optional): Not used here (DSL handler interface compatibility).
        theme (str): Theme name to use for icon resolution.

    Returns:
        str: A styled icon string, or plain glyph/code if no style provided.

    Raises:
        KeyError: If the requested icon or attribute is not found.
    """
    parts = [p.strip() for p in value.split(",")]
    icon_ref = parts[0].removeprefix("ui:")
    style_parts = parts[1:]

    attr = "glyph"
    if icon_ref.endswith(".glyph"):
        icon_ref = icon_ref.rsplit(".", 1)[0]
    elif icon_ref.endswith(".code"):
        icon_ref = icon_ref.rsplit(".", 1)[0]
        attr = "code"

    icons = load_icons(theme)

    try:
        data = _resolve_icon_data(icons, icon_ref)
    except KeyError:
        raise KeyError(f"UI icon not found: ui.{icon_ref}")

    if attr not in data:
        raise KeyError(f"Attribute '{attr}' not found for UI icon: ui.{icon_ref}")

    content = data[attr]
    styles = [_resolve_style(s, trace, theme) for s in style_parts[:2]]

    if styles and styles[0]:
        style_tag = ",".join(filter(None, styles))
        return f"<{style_tag}>{content}</>"

    return content


def _resolve_icon_data(icons, icon_ref: str) -> dict:
    """
    Resolve an icon reference path into its corresponding icon dictionary.

    Supports two-level or three-level access:
    - ui.family.group.key
    - ui.group.key (fallback for legacy/simple icons)

    Args:
        icons: The loaded Icons instance for the current theme.
        icon_ref (str): A dot-delimited path to the icon.

    Returns:
        dict: The dictionary containing glyph and code for the specified icon.

    Raises:
        KeyError: If the icon reference is invalid or missing.
    """
    try:
        family, group, key = icon_ref.split(".", 2)
        return icons.ui[family][group][key]
    except ValueError:
        group, key = icon_ref.split(".", 1)
        return icons.ui[group][key]


def _resolve_style(style: str, trace: bool, theme: str) -> Optional[str]:
    """
    Resolve a style element in a [ui:...] block.

    Supports:
    - Literal keywords: transparent, parentBackground, etc.
    - Palette references: palette:roles.line, etc.
    - Raw hex or named styles (returned as-is).

    Args:
        style (str): The style string to interpret.
        trace (bool): Whether to print trace logs (unused here).
        theme (str): Current theme name for palette resolution.

    Returns:
        Optional[str]: The resolved style or None if empty.
    """
    if style in ALLOWED_COLOR_KEYWORDS:
        return style
    if style.startswith("palette:"):
        return resolve_palette(style[len("palette:"):], trace=trace, theme=theme)
    return style or None
