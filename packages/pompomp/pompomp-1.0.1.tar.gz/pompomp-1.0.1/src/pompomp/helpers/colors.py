"""Color-related helpers for contrast detection and color preview rendering.

This module includes:
- A luminance-based contrast calculator (`get_contrast_color`) to determine
  whether to use black or white text over a given hex background.
- A color highlighter (`highlight_hex_colors`) that styles hex codes in YAML previews using `rich.Text`.
"""
import re

from rich.text import Text

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}")


def get_contrast_color(hex_color: str, threshold: int = 151) -> str:
    """
    Return 'black' or 'white' depending on which offers the better contrast
    against the given background hex color (using luminance).

    Args:
        hex_color: A string hex code (e.g., '#FFB86C')
        threshold: Contrast threshold between 0 and 255 (default: 151)

    Returns:
        Either 'black' or 'white' based on optimal contrast.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "white"  # fallback just in case...

    r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "black" if luminance > threshold else "white"


def highlight_hex_colors(yaml_text: str, contrast: int = 151) -> list[Text]:
    """
    Highlight all #RRGGBB values in a YAML text with background and contrast-aware foreground.

    Args:
        yaml_text: The rendered YAML as a string.
        contrast: Contrast threshold (default: 151)

    Returns:
        List of rich.Text lines with highlighted hex values.
    """
    result = []

    for line in yaml_text.splitlines():
        segments = []
        last_index = 0

        for match in HEX_COLOR_RE.finditer(line):
            start, end = match.span()
            hex_code = match.group()
            font_color = get_contrast_color(hex_code, threshold=contrast)

            if start > last_index:
                segments.append(line[last_index:start])

            segments.append(Text(hex_code, style=f"{font_color} on {hex_code}"))
            last_index = end

        if last_index < len(line):
            segments.append(line[last_index:])

        result.append(Text.assemble(*segments) if segments else Text(line))

    return result
