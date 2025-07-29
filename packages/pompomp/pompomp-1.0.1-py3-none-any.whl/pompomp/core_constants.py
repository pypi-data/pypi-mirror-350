"""
Constants and default values used across the pompomp project.

This module defines default filenames, directory names, template metadata, and
Oh My Posh documentation URLs. These values are used to standardize behavior
and simplify file access throughout the project.
"""
PROJECT_NAME = "pompomp"

# Encoding
YAML_ENCODING = "utf-8"

# Default filenames
DEFAULT_ICONS_FILENAME = "icons.yml"
DEFAULT_MAIN_THEME_LAYOUT_FILENAME = "__main__.yml"
DEFAULT_PALETTE_FILENAME = "palette.yml"
TEMPLATES_METADATA_FILENAME = "meta.yml"
PREVIEW_TMP_FILE = f"{PROJECT_NAME}-preview.yml"

# Default directory names
DEFAULT_CORE_DIRNAME = "core"
DEFAULT_LAYOUTS_DIRNAME = "layouts"
DEFAULT_SHARED_DIRNAME = "shared"
DEFAULT_THEME_DIRNAME = "default"
TEMPLATES_DIRNAME = "templates"

# Layout shortcuts
LAYOUT_SHORTCUTS_MAP = {
    "1": "1_line",
    "1-line": "1_line",
    "1l": "1_line",
    "2": "2_lines",
    "2-lines": "2_lines",
    "2l": "2_lines",
}

# Schema style tags
STYLE_TAGS = {
    "bold": "b",
    "underline": "u",
    "overline": "o",
    "italic": "i",
    "strikethrough": "s",
    "dim": "d",
    "blink": "f",
    "reversed": "r",
}
STYLE_ALIASES = {v: k for k, v in
                 STYLE_TAGS.items()}  # Bijective reverse mapping for short names ; could be different in the future
VALID_STYLES = set(STYLE_TAGS) | set(STYLE_ALIASES)  # Used to validate any allowed style (long or short)

# Metadata skeleton
TEMPLATES_METADATA_SKELETON = """name: [THEME_NAME]
version: "1.0.0"
description: [DESCRIPTION]
created: [CREATED_DATE]
authors:
  - name: [AUTHOR_NAME]
    email: [AUTHOR_EMAIL]
tags: [TAGS]
"""

# External documentation
OMP_SEGMENTS_DOC_URL = "https://ohmyposh.dev/docs/configuration/segment"
OMP_TEMPLATES_DOC_URL = "https://ohmyposh.dev/docs/configuration/templates"
