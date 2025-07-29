"""
DSL Schema : Defines supported DSL blocks, their behavior, and usage metadata.

This module documents each supported DSL directive (e.g., [inc:...], [if ...], etc.)
including its expected structure, behavior, examples, and specific rules.

"""

ALLOWED_COLOR_KEYWORDS = ["transparent", "parentBackground", "parentForeground"]

DSL_SCHEMA_INFO = {
    "var": {
        "description": "Inject a Go-template variable. Transforms `[.Var]` into `{{ .Var }}`.",
        "example": "[.UserName]",
        "expected": "Go-template variable expression: {{ .UserName }}",
        "notes": [
            "Matches any `.VariableName` starting with a capital letter (e.g. `.Shell`, `.Env.ENV`, etc.).",
            "The variable must be wrapped in brackets like `[.XXX]` to be processed.",
            "Whitespace is ignored: `[ .Shell ]` → `{{ .Shell }}`.",
            "This transformation happens early in the DSL preprocessing pipeline.",
            "Does not resolve variables, just transforms them to OMP-compatible syntax."
        ]
    },
    "ui": {
        "description": "Render a UI glyph or icon (e.g. powerline symbol) with optional styling.",
        "example": "[ui:divider.right_half_circle_thick, transparent]",
        "expected": "Styled glyph or codepoint, e.g. '<transparent></>'",
        "notes": [
            "Uses glyph definitions from `icons.yml` (resolved by theme).",
            "Supports access to `.glyph` or `.code` explicitly: e.g. [ui:x.y.z.code].",
            "Optional styling accepts up to two values: a foreground and/or background.",
            "Styling values can be:",
            "  - Literal keywords: transparent, parentBackground, ...",
            "  - Palette references: palette:roles.line",
            "  - Raw hex values: #FF00FF",
            "If no style is provided, only the raw glyph/code is returned.",
            "If invalid or missing, raises KeyError with precise info."
        ]
    },
    "style": {
        "description": "Apply one or more inline text styles using pseudo-HTML tags.",
        "example": "[bold, underline: Hello]",
        "expected": "Text wrapped in tags, e.g. <b><u>Hello</u></b>",
        "notes": [
            "Supports both short (e.g. b, u) and long (e.g. bold, underline) style names.",
            "Valid styles include:",
            "  - bold (b), italic (i), underline (u), overline (o)",
            "  - strikethrough (s), dim (d), blink (f), reversed (r)",
            "Multiple styles are applied in the order written (left to right).",
            "Each style wraps the next: [b,u: X] → <b><u>X</u></b>",
            "Whitespace around style names and commas is ignored.",
            "Invalid style names are silently skipped (or logged if trace=True).",
            "The content can include nested DSL blocks like [.Var] or [ui:...]."
        ]
    },
    "inc": {
        "description": "Include a YAML file from the templates directory and inject its contents (entire or a specific key).",
        "example": "[inc:shared.omp.os_properties]",
        "expected": "dict or value (depending on usage)",
        "notes": [
            "Path is relative to 'templates/<theme>' with fallback to 'default'.",
            "Only YAML files (.yml) are supported.",
            "If used in a key like 'properties', the file must contain that key.",
            "If used standalone, the file must contain a single top-level key.",
            "Raises FileNotFoundError or KeyError if the target is missing."
        ]
    },
    "inc_var": {
        "description": "Include another file like `[inc:]`, but with `${...}` variable substitution from `meta.yml`.",
        "example": "[inc_var:shared.envs.${Environment}]",
        "expected": "Interpolated `[inc:...]` block (then resolved like a normal include)",
        "notes": [
            "Reads variables from the current theme’s `meta.yml` file located at `templates/<theme>/layouts/meta.yml`.",
            "Performs `${Variable}` substitution using values from this file.",
            "Once interpolated, downgrades to a standard `[inc:...]` block and resolves it normally.",
            "Supports chaining with other blocks like [inc_var:shared.snippets.${Shell}]",
            "Raises `KeyError` if a referenced meta variable is missing.",
            "Raises `FileNotFoundError` or `KeyError` if the final include path is invalid.",
            "This preprocessing happens early in the transformation pipeline, before any other includes are resolved."
        ]
    },
    "if": {
        "description": "Conditional rendering using Go-template compatible logic. Supports basic comparisons and logical operators.",
        "example": "[if .UserName == 'root']... [else]... [end]",
        "expected": "Go-template block ({{ if ... }}...{{ else }}...{{ end }})",
        "notes": [
            "Supports basic comparisons: ==, !=, <, <=, >, >= or their literal forms (eq, ne, lt, le, gt, ge).",
            "Also supports 'contains' (e.g. [if .Env.ENV contains 'PROD']) and 'not'.",
            "Logical combinations are supported: [if .A > 0 and .B < 5]",
            "Conditions are auto-transformed to Go-template syntax used by Oh My Posh.",
            "⚠️ Version 1 only supports flat conditions. Nested expressions like:",
            "    [if .A > 0 and (.B < 2 or .C == 5)]",
            "  are not guaranteed to be transformed correctly.",
            "  You can write them manually in Go syntax if needed:",
            "    {{ if and (gt .A 0) (or (lt .B 2) (eq .C 5)) }}",
            "Else/End are optional: [if .X]... [end] or [if .X]... [else]... [end]"
        ]
    },
    "icons": {
        "description": "Resolve an icon from `icons.yml`, returning either the glyph or the Unicode code.",
        "example": "[icons:prompt.folder.code]",
        "expected": "Glyph or codepoint (e.g.,  or U+E725)",
        "notes": [
            "The syntax must follow 'family.name[.attr]'.",
            "Default attribute is 'glyph' if omitted.",
            "Examples:",
            "  - [icons:prompt.folder] → returns the glyph",
            "  - [icons:prompt.folder.code] → returns the Unicode code",
            "Icons are loaded from the active theme, with fallback to `default` if needed.",
            "Raises ValueError if the format is invalid.",
            "Raises KeyError if the icon or attribute is missing in the theme."
        ]
    },
}
