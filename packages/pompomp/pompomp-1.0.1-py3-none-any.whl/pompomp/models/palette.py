"""
Defines the Palette model used for theme customization.

This module includes:
- `PaletteKey` enum to reference palette sections.
- `ALIAS_MAP` to support alias resolution (e.g., fg → foreground).
- `Palette` dataclass which provides unified access to resolved color values.
"""
from dataclasses import dataclass
from enum import StrEnum

ALIAS_MAP = {
    "alpha": "transparent",
    "bg": "background",
    "fg": "foreground",
    "transparent": "transparent",
}


class PaletteKey(StrEnum):
    META = "meta"
    COLORS = "colors"
    ROLES = "roles"


@dataclass
class Palette:
    """
    Represents a resolved color palette with metadata, color definitions, and roles.

    Attributes:
        name: The name of the palette (usually the theme name).
        meta: Optional metadata associated with the palette.
        colors: A mapping of color names to hex or RGBA values.
        roles: A mapping of semantic roles (e.g., foreground) to color keys.
    """

    name: str
    meta: dict
    colors: dict
    roles: dict

    def get(self, key: str) -> str | None:
        """
        Resolves a color value from a given key or alias.

        The resolution order is:
        1. Apply alias (e.g., "fg" → "foreground")
        2. Look up the role in `roles` (e.g., "foreground" → "primary")
        3. Look up the color key in `colors` (e.g., "primary" → "#FF00FF")

        Args:
            key: A semantic key, such as "fg" or "background".

        Returns:
            The resolved color value as a string, or None if not found.
        """
        role = ALIAS_MAP.get(key, key)
        color_key = self.roles.get(role, role)
        return self.colors.get(color_key)
