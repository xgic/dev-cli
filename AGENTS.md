# AI Agent Instructions — XGIC Dev Container CLI

Public repository. Follow https://github.com/xgic/ai for multi-repo standards.

## Product

- **Package:** `xgic.cli.dev` (distribution `xgic-dev-cli`)  
- **Depends on:** `xgic-cli` (thin core)  
- **Architecture:** [ADR-0005](https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md)

## Scope

- Docker Compose controller and Dev Container–oriented orchestration helpers  
- Future: lifecycle/check/env CLI subcommands registered on `xgic` via entry points  

## Out of scope

- Payload CMS project creation / product commands → https://github.com/xgic/payload-cms-cli  
- Thin CLI framework / env detection → https://github.com/xgic/cli  

## Rules

- Public-safe content only  
- Human UI review before merge to `main`  
- Dedicated issue-number branches; Conventional Commits  
- Labels required on issues/PRs  
- Python 3.14+; Apache-2.0; root `CODEOWNERS` (`@xgic`)  
