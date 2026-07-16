"""Build a DockerComposeController from CLI args / environment."""

from __future__ import annotations

import argparse
import os

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


def resolve_compose_file(args: argparse.Namespace) -> str:
    return (
        getattr(args, "compose_file", None)
        or os.environ.get(ENV_COMPOSE_FILE)
        or DEFAULT_COMPOSE_FILE
    )


def resolve_project_name(args: argparse.Namespace) -> str:
    return (
        getattr(args, "project", None)
        or os.environ.get(ENV_COMPOSE_PROJECT)
        or DEFAULT_PROJECT_NAME
    )


def resolve_primary_service(args: argparse.Namespace) -> str | None:
    return getattr(args, "service", None) or os.environ.get(ENV_PRIMARY_SERVICE)


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
