"""
Handler for resolving [palette:...] DSL blocks.

Supports resolving theme colors and roles via [palette:section.key] syntax.

Examples:
    [palette:colors.cyan] → resolves to hex from `palette.colors`
    [palette:roles.accent_5] → resolves role → color indirection

Functions:
    - resolve_palette(value, trace, target_key, theme) → str
"""
from pompomp.constants import DEFAULT_THEME_DIRNAME
from pompomp.loaders.palette_loader import load_palette


def resolve_palette(value: str, trace: bool = False, target_key: str | None = None,
                    theme: str = DEFAULT_THEME_DIRNAME) -> str:
    """
    Resolve a [palette:...] DSL block into a final hex color code.

    Supports:
        - [palette:colors.cyan] → resolves directly from `palette.colors`
        - [palette:roles.accent_5] → resolves indirection from `palette.roles` → `palette.colors`

    Args:
        value (str): DSL path (e.g., 'colors.red' or 'roles.primary_bg')
        trace (bool): If True, prints resolution trace.
        target_key (str, optional): Unused (for DSL signature compatibility).
        theme (str): The current theme name.

    Returns:
        str: The resolved hex color (e.g., '#FFB86C').

    Raises:
        ValueError: If the path format or section is invalid.
        KeyError: If the key is not found in the palette.
    """
    if "." not in value:
        raise ValueError(f"Invalid palette path '{value}': expected 'section.key' (e.g., 'roles.accent_5')")

    section, key = value.split(".", 1)
    palette = load_palette(theme)

    resolved = None
    if section == "colors":
        resolved = palette.colors.get(key)
    elif section == "roles":
        role = palette.roles.get(key)
        resolved = palette.colors.get(role)
    else:
        raise ValueError(f"Unknown palette section '{section}', must be 'roles' or 'colors'")

    if resolved is None:
        raise KeyError(f"Unable to resolve [palette:{value}] in theme '{theme}'")

    if trace:
        print(f"[TRACE] [palette:{value}] => {resolved}")

    return resolved
