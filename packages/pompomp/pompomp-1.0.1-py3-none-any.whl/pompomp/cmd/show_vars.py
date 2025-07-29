"""
CLI command: `show-vars` : List all available Oh My Posh template variables.

This command displays the variables usable in prompt templates and DSL blocks, grouped by:
- Global variables (.UserName, .HostName, etc.)
- Segment context (.Segment.Index, etc.)
- Dynamic variables (.Env.XYZ, .Segments.Contains, etc.)
- Segment-specific variables (per segment like 'git', 'python', etc.)

Options:
    --segment, -s TEXT        Filter variables by segment name or use 'full' to expand all.
    --keyword, -k TEXT        Filter by keyword in name or description (case-insensitive).
    --family, -f TEXT         Filter segment-specific vars by their family (e.g., "Languages").
    --list-segments, -ls      Show a summary list of segments by family.
    --with-warnings, -w       Show warnings next to segments (only with --list-segments).

Examples:
    $ pompomp show-vars
    $ pompomp show-vars -s git
    $ pompomp show-vars -k memory
    $ pompomp show-vars -ls -w
"""
import typer

from pompomp.cmd.console import box, console, Panel, Table, escape
from pompomp.constants import OMP_SEGMENTS_DOC_URL
from pompomp.dsl.template_vars import (
    TEMPLATE_GLOBAL_VARS,
    TEMPLATE_SEGMENT_CONTEXT,
    TEMPLATE_DYNAMIC_VARS,
    SEGMENT_SPECIFIC_VARS,
    SEGMENT_TO_FAMILY,
    OMP_ALL_SEGMENT_FAMILIES,
)


def should_include(var: dict, keyword: str | None) -> bool:
    return not keyword or keyword.lower() in (var["name"].lower() + var["description"].lower())


def render_group(title: str, items: list[dict], keyword: str | None = None, width=None) -> None:
    table = Table(title=title, show_lines=True, box=box.SIMPLE_HEAD, width=width)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Description", style="white")

    rendered = False
    for var in items:
        if should_include(var, keyword):
            table.add_row(var["name"], var["type"], var["description"])
            rendered = True

    if rendered:
        console.print(table)


def render_segment(title: str, items: list[dict], keyword: str | None = None, family: str | None = None,
                   width=None) -> None:
    table = Table(title=title, show_lines=True, box=box.SIMPLE_HEAD, width=width)
    table.add_column("Family", style="dim", no_wrap=True)
    table.add_column("Segment", style="yellow", no_wrap=True)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Description", style="white")

    rendered = False
    for var in items:
        family_name = SEGMENT_TO_FAMILY.get(var["segment"], "Unknown")
        if (not family or family_name.lower() == family.lower()) and should_include(var, keyword):
            table.add_row(
                family_name,
                var["segment"],
                var["name"],
                var["type"],
                var["description"]
            )
            rendered = True

    if rendered:
        console.print(table)


def _family_matches(family_name: str, family_filter: str | None) -> bool:
    if not family_filter:
        return True
    return family_name.lower() == family_filter.lower()


def _segment_matches(family_name: str, seg_name: str, description: str, warning: str, keyword: str | None) -> bool:
    if not keyword:
        return True
    combined = f"{family_name} {seg_name} {description} {warning}".lower()
    return keyword.lower() in combined


def _build_row(family_name: str, seg_data: dict, seg_name: str, with_warnings: bool) -> list[str]:
    segment_name = seg_data.get("name", seg_name)
    description = seg_data.get("description", "")
    warning = seg_data.get("warning", "")
    row = [family_name, segment_name, description]
    if with_warnings:
        row.append(warning)
    return row


def render_segments_list(with_warnings: bool, keyword: str | None = None, family: str | None = None) -> None:
    table = Table(title="Available Segments", show_lines=True, box=box.SIMPLE_HEAD)
    table.add_column("Family", style="dim", no_wrap=True)
    table.add_column("Segment", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    if with_warnings:
        table.add_column("Warning", style="yellow")

    for source in OMP_ALL_SEGMENT_FAMILIES:
        family_name = source.get("meta", {}).get("name", "Unknown Family")
        if not _family_matches(family_name, family):
            continue
        for seg_key, seg_data in source.items():
            if seg_key == "meta":
                continue
            if not _segment_matches(family_name, seg_key, seg_data.get("description", ""), seg_data.get("warning", ""),
                                    keyword):
                continue
            row = _build_row(family_name, seg_data, seg_key, with_warnings)
            table.add_row(*row)

    console.print(table)


def show_vars(
        segment: str = typer.Option(
            None,
            "--segment", "-s",
            help="Show only variables for a specific segment (e.g. git), or 'full' to expand all segment-specific groups."
        ),
        keyword: str = typer.Option(
            None,
            "--keyword", "-k",
            help="Filter variables by keyword in name or description (case-insensitive)."
        ),
        family: str = typer.Option(
            None,
            "--family", "-f",
            help="Filter segment-specific variables by family name (case-insensitive)."
        ),
        list_segments: bool = typer.Option(
            False,
            "--list-segments", "-ls",
            help="List all segments with their family, description, and optionally warning."
        ),
        with_warnings: bool = typer.Option(
            False,
            "--with-warnings", "-w",
            help="Display warnings when listing segments (only applies with --list-segments)."
        )
) -> None:
    if list_segments:
        render_segments_list(with_warnings, keyword, family)
        return

    if family:
        render_segment(
            f"Segment-Specific (Family: {family})",
            [
                {"segment": k, "name": v["name"], "type": v["type"], "description": v["description"]}
                for k, lst in SEGMENT_SPECIFIC_VARS.items()
                for v in lst
            ],
            keyword,
            family
        )

    elif segment is None:
        render_group("Global Variables", TEMPLATE_GLOBAL_VARS, keyword)
        render_group("Segment Context", TEMPLATE_SEGMENT_CONTEXT, keyword)
        render_group("Dynamic Variables", TEMPLATE_DYNAMIC_VARS, keyword)
        segment_list = ", ".join(SEGMENT_SPECIFIC_VARS.keys())
        render_segment(
            f"Segment-Specific (tip: use --segment full to isolate or one of the segments in {escape(f'[{segment_list}]')})",
            [
                {"segment": k, "name": v["name"], "type": v["type"], "description": v["description"]}
                for k, lst in SEGMENT_SPECIFIC_VARS.items()
                for v in lst
            ],
            keyword
        )

    elif segment.lower() == "full":
        for seg_name, seg_vars in SEGMENT_SPECIFIC_VARS.items():
            render_group(f"Segment: {seg_name}", seg_vars, keyword)

    else:
        matches = {
            k: v for k, v in SEGMENT_SPECIFIC_VARS.items()
            if k == segment or k.startswith(f"{segment}.")
        }
        if not matches:
            console.print(f"[bold red]\u274c Unknown segment:[/] '{segment}'")
            console.print(f"Available: {', '.join(SEGMENT_SPECIFIC_VARS)}")
            raise typer.Exit(code=1)

        render_segment(f"Matched Segment(s): {', '.join(matches)}", [
            {"segment": k, "name": v["name"], "type": v["type"], "description": v["description"]}
            for k, lst in matches.items()
            for v in lst
        ], keyword)

    console.print(Panel.fit(
        f"[bold blue]More info:[/bold blue]\n{OMP_SEGMENTS_DOC_URL}",
        title="[yellow]OMP Reference",
        border_style="dim"
    ))
