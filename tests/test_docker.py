"""Unit tests for DockerComposeController (mocked subprocess)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from xgic.cli.core.environment import EnvironmentContext, EnvironmentType
from xgic.cli.dev.docker import DockerComposeController


@pytest.fixture
def mock_env() -> EnvironmentContext:
    return EnvironmentContext(env_type=EnvironmentType.HOST)


@pytest.fixture
def controller(mock_env: EnvironmentContext) -> DockerComposeController:
    return DockerComposeController(
        env=mock_env,
        project_name="test-project",
        primary_service="app",
    )


class TestDockerComposeController:
    def test_services_running_primary(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "app\nother"
            mock_run.return_value = mock_result
            assert controller.services_running() is True

    def test_services_running_false_when_empty(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = ""
            mock_run.return_value = mock_result
            assert controller.services_running() is False

    def test_up_with_profile_and_services(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.up(profile="postgres", services=["postgres"], build=True)
            mock_run.assert_called_with(
                "--profile",
                "postgres",
                "up",
                "-d",
                "--build",
                "postgres",
            )

    def test_down(self, controller: DockerComposeController) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.down()
            mock_run.assert_called_with("down")

    def test_down_remove_volumes(self, controller: DockerComposeController) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.down(remove_volumes=True)
            mock_run.assert_called_with("down", "-v")

    def test_rm_service(self, controller: DockerComposeController) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.rm_service("postgres", force=True, stop=True)
            mock_run.assert_called_with(
                "rm", "-f", "-s", "postgres", check=False
            )

    def test_remove_volume(self, controller: DockerComposeController) -> None:
        with patch("xgic.cli.dev.docker.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            assert controller.remove_volume("test-volume") is True
            called_cmd = mock_run.call_args[0][0]
            assert called_cmd[0:4] == ["docker", "volume", "rm", "-f"]

    def test_db_volume_name(self, controller: DockerComposeController) -> None:
        assert controller.db_volume_name("postgres") == "test-project-postgres-data"
