"""Environment status command (product-agnostic; no product secrets)."""

from __future__ import annotations

import json
from pathlib import Path

from xgic.cli.app import CommandContext
from xgic.cli.dev.context import make_docker
from xgic.cli.utils.output import print_info, print_success

ENV_FILE = Path(".devcontainer/.env")


def run_env(ctx: CommandContext) -> int:
    """Inspect development environment status (no regenerate in this module)."""
    docker = make_docker(ctx.env, ctx.args)
    env_file_exists = ENV_FILE.exists()
    services_ok = docker.services_running()
    use_json = bool(getattr(ctx.args, "json", False))

    if use_json:
        print(
            json.dumps(
                {
                    "env_file_exists": env_file_exists,
                    "env_file": str(ENV_FILE),
                    "services_running": services_ok,
                    "compose_file": docker.compose_file,
                    "project_name": docker.project_name,
                    "primary_service": docker.primary_service,
                    "environment": ctx.env.describe(),
                },
                indent=2,
            )
        )
        return 0

    print_info("Development environment status:")
    if env_file_exists:
        print_success(f".env file exists at {ENV_FILE}")
    else:
        print_info(f".env file not found at {ENV_FILE}")

    if services_ok:
        print_success("Compose services: appear to be running")
    else:
        print_info("Compose services: not detected as running")

    print_info(f"Compose file: {docker.compose_file}")
    print_info(f"Project: {docker.project_name}")
    print_info("Environment context: " + ctx.env.describe())
    return 0
