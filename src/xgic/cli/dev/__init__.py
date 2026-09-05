"""XGIC CLI Dev Container module (``xgic.cli.dev``)."""

from xgic.cli.dev.docker import DockerComposeController

__version__ = "0.2.1rc1"

__all__ = [
    "DockerComposeController",
    "__version__",
]
