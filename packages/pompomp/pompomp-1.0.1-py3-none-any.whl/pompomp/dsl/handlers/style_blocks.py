import re

from pompomp.core_constants import STYLE_TAGS, STYLE_ALIASES

VALID_STYLES = set(STYLE_TAGS) | set(STYLE_ALIASES)

RE_STYLE_BLOCK = re.compile(r"\[([\w\s,]+): (.+?)]", re.DOTALL)


def resolve_styles(value: str, trace: bool = False) -> str:
    """
    Handler to resolve [style] blocks like [b,u: content] into styled pseudo-HTML tags.

    Transforms DSL inline style blocks into encapsulated tags for rendering.
    Supports both short (`b`, `i`, `u`, etc.) and long (`bold`, `italic`, `underline`, etc.) style names.

    Recognized styles:
        - b / bold → <b>
        - i / italic → <i>
        - u / underline → <u>
        - o / overline → <o>
        - s / strikethrough → <s>
        - d / dim → <d>
        - f / blink → <f>
        - r / reversed → <r>

    Syntax:
        [b,i: Hello]         → <b><i>Hello</i></b>
        [italic,underline: X] → <i><u>X</u></i>
        [blink: [.Shell]]     → <f>{{ .Shell }}</f>

    Invalid styles are ignored with an optional warning in trace mode.

    Args:
        value (str): Input string containing one or more [b,u: ...] blocks.
        trace (bool): Whether to print trace warnings for unknown styles.

    Returns:
        str: Transformed string with style tags applied.
    """

    def replace(match):
        raw_keys = re.split(r"\s*,\s*", match.group(1).strip())
        content = match.group(2).strip()

        applied = []
        for k in raw_keys:
            if k in VALID_STYLES:
                tag = STYLE_TAGS.get(k, k) if k in STYLE_TAGS else STYLE_TAGS[STYLE_ALIASES[k]]
                applied.append(tag)
            else:
                if trace:
                    print(f"[STYLE][WARN] Unknown style: {k}")

        for tag in applied:
            content = f"<{tag}>{content}</{tag}>"
        return content

    return RE_STYLE_BLOCK.sub(replace, value)
