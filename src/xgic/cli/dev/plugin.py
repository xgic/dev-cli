"""Register ``xgic.cli.dev`` subcommands on the core ``xgic`` CLI."""

from __future__ import annotations

import argparse

from xgic.cli.dev.commands.check import run_check
from xgic.cli.dev.commands.env_cmd import run_env
from xgic.cli.dev.commands.lifecycle import (
    run_build,
    run_clean,
    run_down,
    run_logs,
    run_shell,
    run_up,
)


def _common_parent() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "--compose-file",
        metavar="PATH",
        help="Compose file path (or XGIC_COMPOSE_FILE)",
    )
    parent.add_argument(
        "--project",
        metavar="NAME",
        help="Compose project name (or XGIC_COMPOSE_PROJECT)",
    )
    parent.add_argument(
        "--service",
        metavar="NAME",
        help="Primary compose service (or XGIC_PRIMARY_SERVICE)",
    )
    parent.add_argument(
        "--profile",
        metavar="NAME",
        help="Compose profile for up (or XGIC_COMPOSE_PROFILE)",
    )
    return parent


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Entry point: ``xgic.cli.commands`` → register Dev Container commands."""
    parent = _common_parent()

    up = subparsers.add_parser(
        "up",
        parents=[parent],
        help="Start Docker Compose services (detached)",
    )
    up.set_defaults(func=run_up)

    down = subparsers.add_parser(
        "down",
        parents=[parent],
        help="Stop Docker Compose services (volumes preserved)",
    )
    down.set_defaults(func=run_down)

    build = subparsers.add_parser(
        "build",
        parents=[parent],
        help="Build or rebuild compose services",
    )
    build.add_argument(
        "--no-cache",
        action="store_true",
        help="Build without cache",
    )
    build.set_defaults(func=run_build)

    logs = subparsers.add_parser(
        "logs",
        parents=[parent],
        help="Follow logs for compose services",
    )
    logs.set_defaults(func=run_logs)

    shell = subparsers.add_parser(
        "shell",
        parents=[parent],
        help="Open a shell in the primary service",
    )
    shell.set_defaults(func=run_shell)

    clean = subparsers.add_parser(
        "clean",
        parents=[parent],
        help="[DANGER] Full cleanup (volumes + .devcontainer/.env)",
    )
    clean.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation and proceed",
    )
    clean.set_defaults(func=run_clean)

    check = subparsers.add_parser(
        "check",
        parents=[parent],
        help="Diagnostic: compose services + environment context",
    )
    check.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    check.set_defaults(func=run_check)

    env_p = subparsers.add_parser(
        "env",
        parents=[parent],
        help="Inspect development environment status",
    )
    env_p.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    env_p.set_defaults(func=run_env)
