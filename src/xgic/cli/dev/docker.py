"""Docker Compose orchestration for Dev Container environments.

Product-agnostic Compose controller. Callers inject compose file, project
name, primary service, and optional profile. Payload CMS–specific defaults
and config readers live in ``xgic.cli.payload`` (xgic/payload-cms-cli).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from xgic.cli.core.environment import EnvironmentContext

DEFAULT_COMPOSE_FILE = ".devcontainer/docker-compose.yml"
DEFAULT_PROJECT_NAME = "xgic-dev"


@dataclass
class DockerComposeController:
    """Controls Docker Compose services for a dev environment."""

    env: EnvironmentContext
    compose_file: str = DEFAULT_COMPOSE_FILE
    project_name: str = DEFAULT_PROJECT_NAME
    primary_service: str | None = None

    def _run_compose(
        self,
        *args: str,
        check: bool = True,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run a docker compose command with consistent flags."""
        cmd = [
            "docker",
            "compose",
            "-f",
            self.compose_file,
            "-p",
            self.project_name,
            *args,
        ]
        return subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True,
        )

    def services_running(self, service: str | None = None) -> bool:
        """Return True if a target service (or any) appears to be up."""
        target = service or self.primary_service
        try:
            result = self._run_compose(
                "ps",
                "--services",
                "--filter",
                "status=running",
                capture_output=True,
            )
            running = {s.strip() for s in result.stdout.splitlines() if s.strip()}
            if not running:
                return False
            if target is None:
                return True
            return target in running
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def up(
        self,
        *,
        build: bool = False,
        services: list[str] | None = None,
        profile: str | None = None,
    ) -> None:
        """Start services in detached mode."""
        args: list[str] = []
        if profile:
            args.extend(["--profile", profile])
        args.extend(["up", "-d"])
        if build:
            args.append("--build")
        if services:
            args.extend(services)
        self._run_compose(*args)

    def down(self) -> None:
        """Stop services (volumes are preserved)."""
        self._run_compose("down")

    def rm_service(
        self,
        service: str,
        *,
        force: bool = True,
        stop: bool = True,
        remove_volumes: bool = False,
    ) -> None:
        """Best-effort compose rm for a single service."""
        args = ["rm"]
        if force:
            args.append("-f")
        if stop:
            args.append("-s")
        if remove_volumes:
            args.append("-v")
        args.append(service)
        self._run_compose(*args, check=False)

    def build(self, *, no_cache: bool = False) -> None:
        """Build images."""
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        self._run_compose(*args)

    def logs(self, follow: bool = True) -> None:
        """Follow logs (this blocks)."""
        args = ["logs"]
        if follow:
            args.append("-f")
        self._run_compose(*args, check=False)

    def exec(
        self, service: str, *cmd: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        """Run a command inside a service container."""
        return self._run_compose("exec", service, *cmd, check=check)

    def remove_volume(self, volume_name: str) -> bool:
        """Attempt to remove a Docker volume via top-level docker CLI."""
        try:
            result = subprocess.run(
                ["docker", "volume", "rm", "-f", volume_name],
                check=False,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def db_volume_name(self, service: str) -> str:
        """Return the conventional named volume for a DB service."""
        return f"{self.project_name}-{service}-data"
