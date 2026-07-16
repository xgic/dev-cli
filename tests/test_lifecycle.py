"""Tests for lifecycle command handlers (mocked compose)."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

from xgic.cli.app import CommandContext
from xgic.cli.core.environment import EnvironmentContext, EnvironmentType
from xgic.cli.dev.commands.lifecycle import (
    run_clean,
    run_down,
    run_shell,
    run_up,
)


def _ctx(**kwargs: object) -> CommandContext:
    defaults: dict[str, object] = {
        "compose_file": None,
        "project": None,
        "service": None,
        "profile": None,
        "no_cache": False,
        "yes": False,
    }
    defaults.update(kwargs)
    ns = argparse.Namespace(**defaults)
    env = EnvironmentContext(env_type=EnvironmentType.HOST)
    return CommandContext(env=env, args=ns)


def test_run_up_calls_docker_up() -> None:
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        docker = MagicMock()
        make.return_value = docker
        ctx = _ctx(profile="postgres")
        assert run_up(ctx) == 0
        docker.up.assert_called_once_with(profile="postgres")


def test_run_down_calls_docker_down() -> None:
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        docker = MagicMock()
        make.return_value = docker
        assert run_down(_ctx()) == 0
        docker.down.assert_called_once_with()


def test_run_shell_requires_service() -> None:
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        docker = MagicMock()
        docker.primary_service = None
        make.return_value = docker
        assert run_shell(_ctx()) == 1
        docker.exec.assert_not_called()


def test_run_shell_with_service() -> None:
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        docker = MagicMock()
        docker.primary_service = "app"
        make.return_value = docker
        assert run_shell(_ctx(service="app")) == 0
        docker.exec.assert_called_once_with("app", "bash")


def test_run_clean_requires_yes() -> None:
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        make.return_value = MagicMock()
        assert run_clean(_ctx(yes=False)) == 1


def test_run_clean_with_yes(tmp_path: Path, monkeypatch) -> None:
    env_dir = tmp_path / ".devcontainer"
    env_dir.mkdir()
    env_file = env_dir / ".env"
    env_file.write_text("SECRET=1")
    monkeypatch.chdir(tmp_path)
    with patch("xgic.cli.dev.commands.lifecycle.make_docker") as make:
        docker = MagicMock()
        make.return_value = docker
        assert run_clean(_ctx(yes=True)) == 0
        docker.down.assert_called_with(remove_volumes=True)
        assert not env_file.exists()
