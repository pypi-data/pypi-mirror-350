from .golang_cleaner import clean_golang_template
from .icons import resolve_icons
from .inc import resolve_include
from .palette import resolve_palette
from .style_blocks import resolve_styles
from .ui import resolve_ui
from .vars import resolve_template_var

__all__ = [
    "resolve_include", "resolve_palette", "resolve_ui",
    "resolve_template_var", "resolve_icons", "clean_golang_template",
    "resolve_styles"
]
