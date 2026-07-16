"""Lifecycle commands: up, down, build, logs, shell, clean."""

from __future__ import annotations

import contextlib
from pathlib import Path

from xgic.cli.app import CommandContext
from xgic.cli.dev.context import make_docker, resolve_profile
from xgic.cli.utils.output import print_info, print_success, print_warning

ENV_FILE = Path(".devcontainer/.env")


def run_up(ctx: CommandContext) -> int:
    """Start compose services in detached mode."""
    docker = make_docker(ctx.env, ctx.args)
    profile = resolve_profile(ctx.args)
    print_info("Starting services...")
    docker.up(profile=profile)
    print_success("Services are up (detached)")
    return 0


def run_down(ctx: CommandContext) -> int:
    """Stop services (volumes preserved)."""
    docker = make_docker(ctx.env, ctx.args)
    print_info("Stopping services...")
    docker.down()
    print_success("Services stopped (volumes preserved)")
    return 0


def run_build(ctx: CommandContext) -> int:
    """Build compose images."""
    docker = make_docker(ctx.env, ctx.args)
    no_cache = bool(getattr(ctx.args, "no_cache", False))
    print_info("Building services" + (" (no cache)" if no_cache else "") + "...")
    docker.build(no_cache=no_cache)
    print_success("Build complete")
    return 0


def run_logs(ctx: CommandContext) -> int:
    """Follow logs for all services (blocks until interrupted)."""
    docker = make_docker(ctx.env, ctx.args)
    print_info("Following logs (press Ctrl+C to exit)...")
    docker.logs(follow=True)
    return 0


def run_shell(ctx: CommandContext) -> int:
    """Open an interactive shell in the primary service."""
    docker = make_docker(ctx.env, ctx.args)
    service = docker.primary_service
    if not service:
        print_warning(
            "No primary service set. Pass --service NAME or set "
            "XGIC_PRIMARY_SERVICE."
        )
        return 1
    print_info(f"Opening shell in service {service!r} (type 'exit' to leave)...")
    try:
        docker.exec(service, "bash")
    except Exception:
        print_info("Shell session ended or failed to attach.")
    return 0


def run_clean(ctx: CommandContext) -> int:
    """Full environment cleanup (volumes + .env). Extremely destructive."""
    docker = make_docker(ctx.env, ctx.args)
    yes = bool(getattr(ctx.args, "yes", False))

    print_warning(
        "This will delete Docker volumes AND the generated .env file "
        f"(if present at {ENV_FILE})."
    )
    if not yes:
        print_warning("Re-run with --yes only if you are absolutely sure.")
        return 1

    print_info("Performing full cleanup...")
    try:
        docker.down(remove_volumes=True)
    except Exception:
        with contextlib.suppress(Exception):
            docker.down()

    if ENV_FILE.exists():
        ENV_FILE.unlink()
        print_success(f"Removed {ENV_FILE}")

    print_success(
        "Full cleanup complete. You will need to re-initialize the environment."
    )
    return 0
