# XGIC Dev Container CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**XGIC Dev Container CLI** (`xgic.cli.dev`) provides Docker Compose orchestration and Dev Container–oriented helpers for the modular [XGIC CLI](https://github.com/xgic/cli).

Architecture: [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md).

| Package | Role |
|---------|------|
| [xgic/cli](https://github.com/xgic/cli) | Thin core framework (`xgic`) |
| **This repo** | Dev Container / Compose library (`xgic.cli.dev`) |
| [xgic/payload-cms-cli](https://github.com/xgic/payload-cms-cli) | Payload CMS product module |

## Status

**0.1.0 — library extract.** `DockerComposeController` and related helpers. Domain lifecycle subcommands (`up`/`down`/`check`/…) land in later releases. Depends on `xgic-cli` for environment detection.

## Requirements

- Python **3.14+**
- `xgic-cli` ≥ 0.2.0

## Install (development)

Until the core package is published to PyPI, install core from a sibling checkout:

```bash
python -m pip install -e ../cli
python -m pip install -e ".[dev]"
```

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

Product-specific config (for example Payload CMS `create-payload-config.json`) lives in **payload-cms-cli**, not here.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.
