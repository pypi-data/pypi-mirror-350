"""
Defines the Icons model for accessing UI glyphs and symbols.

This module provides:
- `IconsKey` enum to reference top-level icon sections.
- `Icons` dataclass for structured access to nested icon dictionaries.
- A `get()` method for retrieving glyphs by exact key.
"""
from dataclasses import dataclass
from enum import StrEnum


class IconsKey(StrEnum):
    UI = "ui"
    ICONS = "icons"


@dataclass
class Icons:
    """
    Represents a resolved icon collection including UI elements and symbolic icons.

    Attributes:
        name: The theme name.
        ui: Nested dictionary of UI icons (e.g. box, divider).
        icons: Dictionary of general icons (e.g. OS, git, lang, prompt).
    """

    name: str
    ui: dict
    icons: dict

    def get(self, key: str) -> str | None:
        """
        Resolves a glyph character from a given icon key (exact match only).

        Args:
            key: The exact key to search for in all sections.

        Returns:
            The glyph character if found, or None.
        """
        for section in (self.ui, self.icons):
            for group in section.values():
                if isinstance(group, dict) and key in group:
                    return group[key].get("glyph")
        return None
