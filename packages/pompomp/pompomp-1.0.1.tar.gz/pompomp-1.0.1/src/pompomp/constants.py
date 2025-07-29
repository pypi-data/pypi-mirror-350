"""
Resolve and validate template paths used by pompomp.

This module ensures that the user's template root exists; otherwise it prompts for a reset.
It also defines derived paths for the default theme, layouts, shared assets, and preview file.
"""
import tempfile
from importlib.resources import files
from pathlib import Path

from pompomp.core_constants import *  # Import shared constants
from pompomp.exceptions import TemplatesRootNotFound
from pompomp.helpers import (
    get_user_templates_root,
    load_pompomp_config,
    update_user_templates_path,
)

try:
    PROJECT_USER_ROOT = get_user_templates_root()
    if not (PROJECT_USER_ROOT / TEMPLATES_DIRNAME).exists():
        raise TemplatesRootNotFound(f"User templates root invalid: {PROJECT_USER_ROOT}")
except TemplatesRootNotFound as e:
    from pompomp.cmd.console import Prompt, console  # Avoid circular import
    user_path = load_pompomp_config().templates_root.user
    console.print(f"[bold red]❌ User templates directory not found:[/bold red] {user_path}")
    if Prompt.ask("Do you want to reset your configuration?", choices=["y", "n"], default="y") == "y":
        update_user_templates_path(None)
        PROJECT_USER_ROOT = get_user_templates_root()
    else:
        raise TemplatesRootNotFound(f"User templates root invalid: {user_path}")

PROJECT_ROOT = PROJECT_USER_ROOT if PROJECT_USER_ROOT.exists() else files(PROJECT_NAME)

# Derived paths
TEMPLATES_ROOT = PROJECT_ROOT / TEMPLATES_DIRNAME
TEMPLATE_DEFAULT_ROOT = TEMPLATES_ROOT / DEFAULT_THEME_DIRNAME

TEMPLATE_DEFAULT_LAYOUTS_DIR = TEMPLATE_DEFAULT_ROOT / DEFAULT_LAYOUTS_DIRNAME
TEMPLATE_DEFAULT_SHARED_DIR = TEMPLATE_DEFAULT_ROOT / DEFAULT_SHARED_DIRNAME
TEMPLATE_DEFAULT_CORE_DIR = TEMPLATE_DEFAULT_ROOT / DEFAULT_CORE_DIRNAME

TEMPLATE_DEFAULT_MAIN_LAYOUT = TEMPLATE_DEFAULT_LAYOUTS_DIR / DEFAULT_MAIN_THEME_LAYOUT_FILENAME
TEMPLATE_DEFAULT_PALETTE = TEMPLATE_DEFAULT_SHARED_DIR / DEFAULT_PALETTE_FILENAME
TEMPLATE_DEFAULT_ICONS = TEMPLATE_DEFAULT_SHARED_DIR / DEFAULT_ICONS_FILENAME

TEMPLATE_PREVIEW_TEMP_PATH = Path(tempfile.gettempdir()) / PREVIEW_TMP_FILE
