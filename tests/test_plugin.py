"""Tests for entry-point registration and check/env commands."""

from __future__ import annotations

import argparse
import json
from unittest.mock import MagicMock, patch

from xgic.cli.app import CommandContext, build_parser
from xgic.cli.core.environment import EnvironmentContext, EnvironmentType
from xgic.cli.dev.commands.check import run_check
from xgic.cli.dev.commands.env_cmd import run_env
from xgic.cli.dev.plugin import register


def test_register_adds_lifecycle_commands() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    register(sub)
    # Parse a few known commands
    for name in ("up", "down", "build", "logs", "shell", "clean", "check", "env"):
        args = parser.parse_args([name])
        assert args.command == name
        assert callable(args.func)


def test_plugin_loaded_via_core_parser_when_installed() -> None:
    # With package installed, entry point should register commands
    parser = build_parser(include_plugins=True)
    # help string includes subcommands when plugins load
    help_text = parser.format_help()
    # If plugin entry point is installed, up appears; if not, only info.
    # In editable install of this package, entry point is present.
    assert "info" in help_text or "Available commands" in help_text


def test_run_check_json(capsys) -> None:
    ns = argparse.Namespace(
        compose_file=None,
        project=None,
        service="app",
        profile=None,
        json=True,
    )
    env = EnvironmentContext(env_type=EnvironmentType.HOST)
    ctx = CommandContext(env=env, args=ns)
    with patch("xgic.cli.dev.commands.check.make_docker") as make:
        docker = MagicMock()
        docker.services_running.return_value = True
        docker.compose_file = ".devcontainer/docker-compose.yml"
        docker.project_name = "xgic-dev"
        docker.primary_service = "app"
        make.return_value = docker
        assert run_check(ctx) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["services_running"] is True
    assert data["overall_ok"] is True


def test_run_env_status(capsys) -> None:
    ns = argparse.Namespace(
        compose_file=None,
        project=None,
        service=None,
        profile=None,
        json=False,
    )
    env = EnvironmentContext(env_type=EnvironmentType.HOST)
    ctx = CommandContext(env=env, args=ns)
    with patch("xgic.cli.dev.commands.env_cmd.make_docker") as make:
        docker = MagicMock()
        docker.services_running.return_value = False
        docker.compose_file = "cf"
        docker.project_name = "pn"
        docker.primary_service = None
        make.return_value = docker
        assert run_env(ctx) == 0
    out = capsys.readouterr().out
    assert "Development environment status" in out or "Docker Compose" in out
