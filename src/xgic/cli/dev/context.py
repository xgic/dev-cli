"""Build a DockerComposeController from CLI args / environment."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from xgic.cli.core.environment import EnvironmentContext
from xgic.cli.dev.docker import (
    DEFAULT_COMPOSE_FILE,
    DEFAULT_PROJECT_NAME,
    DockerComposeController,
)

ENV_COMPOSE_FILE = "XGIC_COMPOSE_FILE"
ENV_COMPOSE_PROJECT = "XGIC_COMPOSE_PROJECT"
ENV_PRIMARY_SERVICE = "XGIC_PRIMARY_SERVICE"
ENV_COMPOSE_PROFILE = "XGIC_COMPOSE_PROFILE"

DEFAULT_DEVCONTAINER_JSON = Path(".devcontainer/devcontainer.json")
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,62}$")


def resolve_compose_file(args: argparse.Namespace) -> str:
    return (
        getattr(args, "compose_file", None)
        or os.environ.get(ENV_COMPOSE_FILE)
        or DEFAULT_COMPOSE_FILE
    )


def _is_compose_safe_name(name: str) -> bool:
    return bool(name and _SAFE_NAME.fullmatch(name))


def compose_name_from_file(compose_path: Path) -> str | None:
    """Parse top-level ``name:`` from a Compose file (best-effort)."""
    if not compose_path.is_file():
        return None
    try:
        for line in compose_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or not stripped.startswith("name:"):
                continue
            raw = stripped.split(":", 1)[1].strip().strip("\"'")
            if raw and _is_compose_safe_name(raw):
                return raw
    except OSError:
        return None
    return None


def primary_service_from_devcontainer(
    path: Path = DEFAULT_DEVCONTAINER_JSON,
) -> str | None:
    """Read ``service`` from ``.devcontainer/devcontainer.json`` if present."""
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    raw = data.get("service")
    if isinstance(raw, str) and raw.strip() and _is_compose_safe_name(raw.strip()):
        return raw.strip()
    return None


def resolve_project_name(args: argparse.Namespace) -> str:
    named = getattr(args, "project", None) or os.environ.get(ENV_COMPOSE_PROJECT)
    if isinstance(named, str) and named.strip() and _is_compose_safe_name(named.strip()):
        return named.strip()
    compose_file = resolve_compose_file(args)
    from_file = compose_name_from_file(Path(compose_file))
    if from_file:
        return from_file
    return DEFAULT_PROJECT_NAME


def resolve_primary_service(args: argparse.Namespace) -> str | None:
    named = getattr(args, "service", None) or os.environ.get(ENV_PRIMARY_SERVICE)
    if isinstance(named, str) and named.strip():
        return named.strip()
    return primary_service_from_devcontainer()


def resolve_profile(args: argparse.Namespace) -> str | None:
    return getattr(args, "profile", None) or os.environ.get(ENV_COMPOSE_PROFILE)


def make_docker(
    env: EnvironmentContext, args: argparse.Namespace
) -> DockerComposeController:
    """Construct a controller from CommandContext-compatible args."""
    return DockerComposeController(
        env=env,
        compose_file=resolve_compose_file(args),
        project_name=resolve_project_name(args),
        primary_service=resolve_primary_service(args),
    )
