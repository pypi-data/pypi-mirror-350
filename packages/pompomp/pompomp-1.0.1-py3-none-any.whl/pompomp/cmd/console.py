"""
Rich console utilities and pre-imported components for consistent terminal rendering.

This module re-exports selected components from the `rich` library,

Exports:
- box
- rprint
- console
- Panel
- Syntax
- Table
- Text
"""
from rich import box
from rich import print as rprint
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

console = Console()

__all__ = [
    "Panel", "Prompt", "Syntax", "Table", "Text",
    "box", "console", "escape", "rprint"
]
