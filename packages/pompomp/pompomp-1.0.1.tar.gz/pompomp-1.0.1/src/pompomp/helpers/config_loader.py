"""Handles loading, resolving, and updating the Pompomp YAML configuration.

This module provides functions to:
- Load and validate the main `pompomp.yml` configuration file.
- Resolve packaged and user template root paths.
- Prompt the user to initialize their template directory.
- Update the configuration dynamically.

Relies on:
- `PompompConfig` model (pydantic)
- `ruamel.yaml` for YAML parsing with quote preservation
"""
from importlib.resources import files
from pathlib import Path
from shutil import copytree, copyfile

from ruamel.yaml import YAML

from pompomp.cmd.console import Prompt, console
from pompomp.core_constants import *
from pompomp.exceptions import PompompConfigError, TemplatesRootNotFound
from pompomp.models.config import PompompConfig

yaml = YAML()
yaml.preserve_quotes = True

CONFIG_FILE = files(PROJECT_NAME) / f"{PROJECT_NAME}.yml"
DEFAULT_CONFIG_FILE = files(PROJECT_NAME) / f"{PROJECT_NAME}.conf.yml"


def ensure_config_exists() -> None:
    """
    Ensure that the main 'pompomp.yml' configuration file exists.
    If not, create it from 'pompomp.conf.yml'.
    """
    if not Path(str(CONFIG_FILE)).exists():
        copyfile(str(DEFAULT_CONFIG_FILE), str(CONFIG_FILE))


ensure_config_exists()


def load_pompomp_config() -> PompompConfig:
    """
    Load and parse the `pompomp.yml` configuration file.

    Returns:
        Parsed configuration object.

    Raises:
        PompompConfigError: If the file is missing or malformed.
    """
    try:
        with CONFIG_FILE.open("r", encoding=YAML_ENCODING) as f:
            raw = yaml.load(f) or {}
        return PompompConfig(**raw)
    except FileNotFoundError:
        raise PompompConfigError(f"Missing '{PROJECT_NAME}.yml' in package.")
    except Exception as e:
        raise PompompConfigError(f"Invalid configuration format: {e}")


def get_user_templates_root() -> Path:
    """
    Resolve the user's templates directory.

    If not configured, prompts the user to initialize it and updates the config.

    Returns:
        Path to the user templates root.

    Raises:
        TemplatesRootNotFound: If the resolved path does not exist.
    """
    config = load_pompomp_config()
    user = config.templates_root.user

    if not user:
        user_path = prompt_init_user_templates_path()
    else:
        user_path = Path(user)

    user_templates_dir = user_path / TEMPLATES_DIRNAME
    if not user_templates_dir.is_dir():
        raise TemplatesRootNotFound(f"User templates path does not exist: {user_templates_dir}")

    return user_path


def get_project_templates_root() -> Path:
    """
    Return the path to the packaged templates root.
    """
    config = load_pompomp_config()
    return files(PROJECT_NAME) / config.templates_root.packaged  # type: ignore


def update_user_templates_path(path: Path | None) -> None:
    """
    Update the 'templates_root.user' field in pompomp.yml config.

    Args:
        path: New user templates root, or None to reset.
    """
    with CONFIG_FILE.open("r", encoding=YAML_ENCODING) as f:
        data = yaml.load(f) or {}

    data.setdefault("templates_root", {})
    data["templates_root"]["user"] = str(path.resolve()) if path else None

    with CONFIG_FILE.open("w", encoding=YAML_ENCODING) as f:  # type: ignore
        yaml.dump(data, f)


def prompt_init_user_templates_path() -> Path:
    """
    Prompt the user to define the root location for user workspace,
    and scaffold the default template structure inside it.

    Returns:
        Path to the initialized user root.
    """
    console.print("[bold yellow]⚠️  Your user templates directory is not configured yet.[/bold yellow]")
    path_str = Prompt.ask(
        "Where do you want to initialize the local Pompomp workspace?",
        default=str(Path.home() / f".{PROJECT_NAME}")
    )
    user_root = Path(path_str).expanduser().resolve()

    # Ensure user root exists
    user_root.mkdir(parents=True, exist_ok=True)

    # Create the 'templates/default' structure
    default_target = user_root / TEMPLATES_DIRNAME
    default_target.mkdir(parents=True, exist_ok=True)

    # Copy packaged template into it
    packaged_path = get_project_templates_root()
    copytree(packaged_path, default_target, dirs_exist_ok=True)

    update_user_templates_path(user_root)
    console.print(f"[bold green]✅ Default theme copied to:[/bold green] {default_target}")
    return user_root
