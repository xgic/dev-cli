"""Health check command (product-agnostic)."""

from __future__ import annotations

import json

from xgic.cli.app import CommandContext
from xgic.cli.dev.context import make_docker
from xgic.cli.utils.output import print_info, print_success, print_warning


def run_check(ctx: CommandContext) -> int:
    """Lightweight compose + environment health check."""
    docker = make_docker(ctx.env, ctx.args)
    services_ok = docker.services_running()
    use_json = bool(getattr(ctx.args, "json", False))

    if use_json:
        result = {
            "services_running": services_ok,
            "compose_file": docker.compose_file,
            "project_name": docker.project_name,
            "primary_service": docker.primary_service,
            "environment": ctx.env.describe(),
            "overall_ok": services_ok,
        }
        print(json.dumps(result, indent=2))
        return 0 if services_ok else 1

    print_info("Running environment health checks...")

    if services_ok:
        print_success("Docker Compose services: running")
    else:
        print_warning(
            "Docker Compose services: not all services appear to be running"
        )
        print_info("Suggestion: Run `xgic up` to start services.")

    print_info(f"Compose file: {docker.compose_file}")
    print_info(f"Project: {docker.project_name}")
    if docker.primary_service:
        print_info(f"Primary service: {docker.primary_service}")
    print_info("Environment context: " + ctx.env.describe())

    if services_ok:
        print_success("Basic environment check passed")
        return 0
    return 1
