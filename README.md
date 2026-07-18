# XGIC Dev Container CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**XGIC Dev Container CLI** (`xgic.cli.dev`) provides Docker Compose orchestration and Dev Container–oriented **`xgic` subcommands** for the modular [XGIC CLI](https://github.com/xgic/cli).

Architecture: [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

**Publishing to PyPI:** [python-package-release.md](https://github.com/xgic/ai/blob/main/docs/python-package-release.md)  
(publish **after** `xgic-cli` for stack releases). Tags: `vX.Y.ZrcN` → TestPyPI; `vX.Y.Z` → PyPI.

| Package | Role |
|---------|------|
| [xgic/cli](https://github.com/xgic/cli) | Thin core framework (`xgic`) |
| **This repo** | Dev Container / Docker Compose + lifecycle commands (`xgic.cli.dev`) |
| [xgic/payload-cms-cli](https://github.com/xgic/payload-cms-cli) | Payload CMS product module |

## Status

**0.2.0 — B3 lifecycle commands.** Product-agnostic Docker Compose library + registered `xgic` subcommands. Payload CMS–specific env regenerate / setup remains in **payload-cms-cli**.

## Requirements

- Python **3.14+**
- `xgic-cli` ≥ 0.2.0
- Docker / Docker Compose on the host when running lifecycle commands

## Install (development)

```bash
python -m pip install -e ../cli
python -m pip install -e ".[dev]"
xgic --help
xgic up --help
```

## Console commands (via entry point)

Installed with this package, registered on the core `xgic` entrypoint:

| Command | Purpose |
|---------|---------|
| `xgic up` | Start compose services (detached) |
| `xgic down` | Stop services (volumes preserved) |
| `xgic build [--no-cache]` | Build images |
| `xgic logs` | Follow logs |
| `xgic shell` | Shell in primary service (`--service` required if not set) |
| `xgic clean --yes` | Destructive: volumes + `.devcontainer/.env` |
| `xgic check [--json]` | Services + environment diagnostic |
| `xgic env [--json]` | Environment status (no secret regeneration) |

Common flags (or env vars):

| Flag | Env var | Default |
|------|---------|---------|
| `--compose-file` | `XGIC_COMPOSE_FILE` | `.devcontainer/docker-compose.yml` |
| `--project` | `XGIC_COMPOSE_PROJECT` | `xgic-dev` |
| `--service` | `XGIC_PRIMARY_SERVICE` | (none) |
| `--profile` | `XGIC_COMPOSE_PROFILE` | (none; used by `up`) |

## Library API

```python
from xgic.cli.core import EnvironmentContext
from xgic.cli.dev import DockerComposeController

env = EnvironmentContext.detect()
docker = DockerComposeController(
    env=env,
    compose_file=".devcontainer/docker-compose.yml",
    project_name="my-project",
    primary_service="app",
)
docker.up(profile="postgres")
```

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
