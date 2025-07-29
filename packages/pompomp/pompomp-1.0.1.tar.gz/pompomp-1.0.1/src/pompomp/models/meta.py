"""
Data model for theme metadata.

Defines the `ThemeMeta` dataclass used to store basic information
about a theme, such as name, author, contact, and description.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ThemeMeta:
    """
    Represents metadata associated with a Pompomp theme.

    Attributes:
        theme_name: Name of the theme.
        author_name: Name of the theme's author.
        author_email: Contact email of the author.
        description: Short description of the theme.
        tags: Comma-separated tags describing the theme.
    """
    theme_name: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
