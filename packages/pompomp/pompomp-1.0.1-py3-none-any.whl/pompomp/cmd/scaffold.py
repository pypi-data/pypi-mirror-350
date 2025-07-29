"""
CLI command: `scaffold` : Create a new theme or palette from a template.

This command bootstraps a new theme folder under `templates/`, either by:
- cloning the full base theme (`--new-theme`)
- copying only `palette.yml` and `meta.yml` (`--new-palette`)

Options:
    --new-theme            Create a full theme (default files, layouts, icons)
    --new-palette          Create only palette.yml + meta.yml
    --theme-name TEXT      Required name of the new theme
    --base-theme TEXT      Source theme to copy from (default: "default")
    --author-name TEXT     Required author name
    --author-email TEXT    Optional author email (must be valid)
    --description TEXT     Optional description for the theme
    --tags TEXT            Optional comma- or semicolon-separated tags
    --force                Overwrite existing files if they exist
    --hard                 Wipe theme folder before copying (requires --force)
    --verbose              Enable verbose output
"""
import os
import shutil
import stat
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

import typer
from ruamel.yaml import YAML

from pompomp.cmd.console import console
from pompomp.constants import (
    DEFAULT_LAYOUTS_DIRNAME,
    DEFAULT_PALETTE_FILENAME,
    DEFAULT_SHARED_DIRNAME,
    TEMPLATES_METADATA_FILENAME,
    TEMPLATES_METADATA_SKELETON,
    DEFAULT_THEME_DIRNAME,
    YAML_ENCODING,
)
from pompomp.helpers import (
    normalize_author_name,
    replace_placeholders,
    is_valid_email,
)
from pompomp.helpers.scaffold import resolve_scaffold_targets
from pompomp.models.meta import ThemeMeta

yaml = YAML()
yaml.preserve_quotes = True


def _verbose_print(message: str, verbose: bool, style: str = "") -> None:
    if verbose:
        console.print(f"[{style}]{message}[/{style}]")


def _handle_remove_error(func: Callable[[str], None], path: str, _exc_info: tuple) -> None:
    os.chmod(path, stat.S_IWRITE)
    try:
        func(path)
    except Exception as e:
        console.print(f"[red]⚠️ Failed to delete: {path} → {e}[/red]")


def _copy_structure(
        dst: Path,
        src: Path,
        force: bool,
        hard: bool,
        paths: list[tuple[Path, Path]],
        mode: str,
        verbose: bool
) -> None:
    _prepare_destination(dst, hard, mode, verbose)
    _perform_copy(dst, src, paths, mode, force, verbose)


def _prepare_destination(dst: Path, hard: bool, mode: str, verbose: bool) -> None:
    if dst.exists():
        _verbose_print(
            f"⚠️ Skipping existing {mode} '{dst.name}' files. Use `--force` to overwrite or `--hard` to wipe completely.",
            True,
            "yellow",
        )
    else:
        dst.mkdir(parents=True)

    if hard and dst.exists():
        _verbose_print(f"⚠️ Hard mode enabled. Removing existing {mode} '{dst.name}'...", verbose, "yellow")
        shutil.rmtree(dst, onerror=_handle_remove_error)
        dst.mkdir(parents=True)


def _perform_copy(dst: Path, src: Path, paths: list[tuple[Path, Path]], mode: str, force: bool, verbose: bool) -> None:
    if mode == "palette":
        for src_path, target_path in paths:
            _safe_copy(src_path, target_path, force, verbose)
    else:
        for item in src.rglob("*"):
            target = dst / item.relative_to(src)
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                _safe_copy(item, target, force, verbose)


def _safe_copy(src: Path, dst: Path, force: bool, verbose: bool) -> None:
    if not dst.exists():
        _verbose_print(f"➕ Adding missing file: {dst}", verbose, "green")
        _copy_file(src, dst, force)
    elif force:
        _verbose_print(f"🔄 Overwriting file: {dst}", verbose, "cyan")
        _copy_file(src, dst, force)


def _copy_file(src: Path, dst: Path, force: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or force:
        shutil.copy2(src, dst)


def _update_palette_meta(path: Path, theme: str, author: str, from_base_theme: bool = False, force: bool = False,
                         verbose: bool = False) -> None:
    if not path.exists():
        return
    with path.open("r", encoding=YAML_ENCODING) as f:
        data = yaml.load(f)

    if (not from_base_theme) or (from_base_theme and force):
        _verbose_print(f"🔄 Overwriting metadata in palette.yml (force={force})", verbose, "cyan")
        data.setdefault("meta", {})
        data["meta"]["name"] = theme
        data["meta"]["author"] = normalize_author_name(author)

    with path.open("w", encoding=YAML_ENCODING) as f:
        yaml.dump(data, f)


def _write_meta_file(dst: Path, meta: ThemeMeta, verbose: bool = False) -> None:
    tags = [t.strip() for t in meta.tags.replace(";", ",").split(",") if t.strip()] if meta.tags else [meta.theme_name]
    content = replace_placeholders(
        TEMPLATES_METADATA_SKELETON,
        THEME_NAME=f'"{meta.theme_name}"',
        AUTHOR_NAME=f'"{normalize_author_name(meta.author_name)}"',
        AUTHOR_EMAIL=f'"{str(meta.author_email).lower()}"' if meta.author_email else '""',
        DESCRIPTION=f'"{meta.description}"' if meta.description else '""',
        CREATED_DATE=f'"{datetime.now():%Y-%m-%d}"',
        TAGS="\n  - " + "\n  - ".join(f'"{t}"' for t in tags),
    )
    (dst / TEMPLATES_METADATA_FILENAME).write_text(content, encoding=YAML_ENCODING)
    _verbose_print(f"📝 Wrote meta file: {dst / TEMPLATES_METADATA_FILENAME}", verbose, "green")


def _create_full_theme(dst: Path, src: Path, meta: ThemeMeta, force: bool, hard: bool,
                       verbose: bool) -> None:
    _verbose_print(f"📂 Source path: {src}", verbose, "yellow")
    _verbose_print(f"📁 Destination path: {dst}", verbose, "yellow")

    paths = [(item, dst / item.relative_to(src)) for item in src.rglob("*")]

    for src_path, target_path in paths:
        _verbose_print(f"➡️  Copy planned: {src_path} → {target_path}", verbose, "cyan")

    _copy_structure(dst, src, force, hard, paths, mode="theme", verbose=verbose)
    _write_meta_file(dst, meta, verbose)
    console.print(f"[bold green]✅ Theme created at:[/bold green] {dst.resolve()}")


def _create_palette_only(dst: Path, src: Path, meta: ThemeMeta, force: bool, hard: bool,
                         from_base_theme: bool, verbose: bool) -> None:
    shared_dst = dst / DEFAULT_SHARED_DIRNAME
    layouts_dst = dst / DEFAULT_LAYOUTS_DIRNAME

    _verbose_print(f"📂 Source path: {src}", verbose, "yellow")
    _verbose_print(f"📁 Destination path: {dst}", verbose, "yellow")

    paths = [
        (src / DEFAULT_SHARED_DIRNAME / DEFAULT_PALETTE_FILENAME, shared_dst / DEFAULT_PALETTE_FILENAME),
        (src / DEFAULT_LAYOUTS_DIRNAME / TEMPLATES_METADATA_FILENAME, layouts_dst / TEMPLATES_METADATA_FILENAME),
    ]

    for src_path, target_path in paths:
        if src_path.exists():
            _verbose_print(f"➡️  Copy planned: {src_path} → {target_path}", verbose, "cyan")
        else:
            _verbose_print(f"❌ Path not found: {src_path}", verbose, "red")

    _copy_structure(dst, src, force, hard, paths, mode="palette", verbose=verbose)

    _update_palette_meta(
        shared_dst / DEFAULT_PALETTE_FILENAME,
        meta.theme_name,
        meta.author_name,
        from_base_theme,
        force,
        verbose,
    )
    _write_meta_file(dst, meta, verbose)
    console.print(f"[bold green]✅ Palette created at:[/bold green] {dst.resolve()}")


def scaffold(
        new_theme: bool = typer.Option(False, "--new-theme", help="Create a full theme based on a template"),
        new_palette: bool = typer.Option(False, "--new-palette", help="Create only palette.yml and layouts/meta.yml"),
        theme_name: Optional[str] = typer.Option(None, help="Name of the new theme to create"),
        base_theme: str = typer.Option(DEFAULT_THEME_DIRNAME, "--base-theme", help="Base theme to copy from"),
        author_name: str = typer.Option(None, help="Author name"),
        author_email: Optional[str] = typer.Option(None, help="Author email (optional)"),
        description: Optional[str] = typer.Option(None, help="Theme description (optional)"),
        tags: Optional[str] = typer.Option(None, help="Comma- or semicolon-separated tags"),
        force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
        hard: bool = typer.Option(False, "--hard", help="Delete theme directory before copying (requires --force)"),
        verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
) -> None:
    if not any([new_theme, new_palette]):
        raise typer.BadParameter("You must choose either --new-theme or --new-palette")
    if new_theme and new_palette:
        raise typer.BadParameter("You can't combine --new-theme and --new-palette")
    if hard and not force:
        raise typer.BadParameter("--hard requires --force")
    if not theme_name:
        raise typer.BadParameter("--theme-name is required")
    if not author_name:
        raise typer.BadParameter("--author-name is required")
    if author_email and not is_valid_email(author_email):
        raise typer.BadParameter("--author-email is not a valid email address")

    slug, dst, src = resolve_scaffold_targets(theme_name, base_theme)

    if not src.exists():
        console.print(f"[red]❌ The base theme '{base_theme}' does not exist in 'templates/'.[/red]")
        raise typer.Exit(code=1)

    meta = ThemeMeta(theme_name, author_name, author_email, description, tags)

    if new_theme:
        _create_full_theme(dst, src, meta, force, hard, verbose)
    elif new_palette:
        _create_palette_only(dst, src, meta, force, hard, base_theme != DEFAULT_THEME_DIRNAME, verbose)
