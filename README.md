# XGIC Dev Container CLI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/xgic-dev-cli.svg)](https://pypi.org/project/xgic-dev-cli/)
[![Python](https://img.shields.io/pypi/pyversions/xgic-dev-cli.svg)](https://pypi.org/project/xgic-dev-cli/)
[![CI](https://github.com/xgic/dev-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/xgic/dev-cli/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/xgic/dev-cli)](https://github.com/xgic/dev-cli/releases)

**Product-agnostic Docker Compose and Dev Container lifecycle for the modular [XGIC CLI](https://github.com/xgic/cli).**

Namespace: **`xgic.cli.dev`** · Console entry: **`xgic`** (plugins via entry points) · Brand: **XGIC CLI only** ([ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md))

Standards hub: [xgic/ai](https://github.com/xgic/ai)

---

## Vision

Environment orchestration should be **predictable, documented, and AI-operable**. This package owns the **generic** lifecycle that every XGIC Dev Container product needs—`up`, `down`, `check`, logs, shell—without embedding Payload-specific or other product logic.

Humans get a stable command map. AI agents get the same map in [AGENTS.md](AGENTS.md) instead of inventing Make targets or host-global installs.

---

## Why this module exists

| Benefit | Detail |
|---------|--------|
| **Separation of concerns** | Core CLI stays thin; product commands live in domain modules |
| **Reuse across products** | Same lifecycle for Payload, GitLab tooling, and future stacks |
| **Configuration over hard-coding** | Compose file, project, service, and profile via flags or env |
| **Safe defaults for agents** | Destructive actions require explicit confirmation (`--yes`) |
| **Open-source rigor** | Apache-2.0, Python 3.14+, PyPI release discipline |

---

## Ecosystem

| Package | Role |
|---------|------|
| [xgic/cli](https://github.com/xgic/cli) | Thin core framework (`xgic`) |
| **This repo** | Dev Container / Docker Compose lifecycle (`xgic.cli.dev`) |
| [xgic/payload-cms-cli](https://github.com/xgic/payload-cms-cli) | Payload product commands (`xgic payload …`) |
| [xgic/payload-cms-dev](https://github.com/xgic/payload-cms-dev) | Payload Dev Container **image producer** |
| [xgic/payload-cms](https://github.com/xgic/payload-cms) | Payload **end-user template** (consumes GHCR image) |

---

## Quick start

### Install (PyPI)

```bash
uv pip install "xgic-dev-cli>=0.2.1"
xgic --help
xgic up --help
```

### Development (editable monorepo layout)

```bash
uv pip install -e ../cli
uv pip install -e ".[dev]"
xgic --help
xgic up --help
```

### Typical session

```bash
export XGIC_COMPOSE_FILE=.devcontainer/docker-compose.yml
export XGIC_COMPOSE_PROJECT=my-project
export XGIC_PRIMARY_SERVICE=app

xgic up --profile postgres
xgic check
xgic logs
xgic down
```

---

## Console commands

Registered on the core `xgic` entrypoint:

| Command | Purpose |
|---------|---------|
| `xgic up` | Start Compose services (detached) |
| `xgic down` | Stop services (volumes preserved) |
| `xgic build [--no-cache]` | Build or rebuild images |
| `xgic logs` | Follow service logs |
| `xgic shell` | Shell in primary service (`--service` if unset) |
| `xgic clean --yes` | Destructive: volumes + `.devcontainer/.env` |
| `xgic check [--json]` | Services + environment diagnostic |
| `xgic env [--json]` | Environment status (no secret regeneration) |

### Common flags / environment

| Flag | Env var | Default |
|------|---------|---------|
| `--compose-file` | `XGIC_COMPOSE_FILE` | `.devcontainer/docker-compose.yml` |
| `--project` | `XGIC_COMPOSE_PROJECT` | Compose file `name:` (else `xgic-dev`) |
| `--service` | `XGIC_PRIMARY_SERVICE` | `devcontainer.json` `service` (else none) |
| `--profile` | `XGIC_COMPOSE_PROFILE` | (none; used by `up`) |

**Note:** Payload-specific env regenerate / setup lives in **[payload-cms-cli](https://github.com/xgic/payload-cms-cli)** (`xgic payload env`, `xgic payload setup`, …).

---

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

---

## Requirements

- Python **3.14+**
- `xgic-cli` ≥ 0.2.1
- Docker / Docker Compose on the host when running lifecycle commands

---

## Publishing

Follow [python-package-release.md](https://github.com/xgic/ai/blob/main/docs/python-package-release.md).

Publish **after** `xgic-cli` for stack releases. Tags: `vX.Y.ZrcN` → TestPyPI; `vX.Y.Z` → PyPI.

---

## Working with AI assistants

- Prefer documented `xgic` lifecycle commands over ad-hoc `docker compose` one-liners in agent prompts.  
- Point agents at [AGENTS.md](AGENTS.md) and the hub [catalog](https://github.com/xgic/ai/blob/main/docs/ecosystem/catalog.md).  
- Public issues/PRs: [BASE-STANDARDS public-safe gate](https://github.com/xgic/ai/blob/main/docs/BASE-STANDARDS-FOR-ORCHESTRATED-REPOS.md).

---

## Contributing

PRs with human UI review only. Conventional Commits; labels required. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).  
Copyright form: `Copyright 2026 XGIC`.

---

**XGIC** — Modular CLI architecture for open-source developer platforms: thin core, domain modules, AI-operable commands.
