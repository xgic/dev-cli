"""Tests for Compose identity resolution."""

from __future__ import annotations

import argparse
from pathlib import Path

from xgic.cli.dev.context import (
    compose_name_from_file,
    primary_service_from_devcontainer,
    resolve_primary_service,
    resolve_project_name,
)


def _args(**kwargs: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "compose_file": None,
        "project": None,
        "service": None,
        "profile": None,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_compose_name_from_file(tmp_path: Path) -> None:
    compose = tmp_path / "docker-compose.yml"
    compose.write_text("# comment\nname: xgic-wagtail\nservices: {}\n")
    assert compose_name_from_file(compose) == "xgic-wagtail"


def test_compose_name_from_file_missing() -> None:
    assert compose_name_from_file(Path("no-such-compose.yml")) is None


def test_resolve_project_prefers_flag(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".devcontainer").mkdir()
    (tmp_path / ".devcontainer" / "docker-compose.yml").write_text(
        "name: xgic-wagtail\n"
    )
    assert resolve_project_name(_args(project="from-flag")) == "from-flag"


def test_resolve_project_reads_compose_name(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".devcontainer").mkdir()
    (tmp_path / ".devcontainer" / "docker-compose.yml").write_text(
        "name: xgic-wagtail\n"
    )
    assert resolve_project_name(_args()) == "xgic-wagtail"


def test_primary_service_from_devcontainer(tmp_path: Path) -> None:
    path = tmp_path / "devcontainer.json"
    path.write_text('{"name": "XGIC Wagtail", "service": "xgic-wagtail"}\n')
    assert primary_service_from_devcontainer(path) == "xgic-wagtail"


def test_resolve_primary_service_flag_wins(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    dc = tmp_path / ".devcontainer"
    dc.mkdir()
    (dc / "devcontainer.json").write_text('{"service": "xgic-wagtail"}\n')
    assert resolve_primary_service(_args(service="from-flag")) == "from-flag"


def test_resolve_primary_service_from_devcontainer(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    dc = tmp_path / ".devcontainer"
    dc.mkdir()
    (dc / "devcontainer.json").write_text('{"service": "xgic-wagtail"}\n')
    assert resolve_primary_service(_args()) == "xgic-wagtail"
