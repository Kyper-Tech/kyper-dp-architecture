---
id: ADR-0004
status: proposed
date: 2026-08-31
affects: [KYP-T-REG, KYP-T-DEVWS, KYP-T-MLWS]
---
# Registries are the only handoff between producers and runtimes; spaces hold nothing durable
## Context
Source repo, artifact repo and model registry were scattered inside dev/ML spaces.
## Decision
A per-tenant registries band (source, artifact, model, experiments). Workspaces are
ephemeral; CI/CD is the only actor moving a registry entry into a runtime.
## Consequences
Losing a workspace costs only uncommitted work. Catalog stays in data management as the
data registry — accepted asymmetry.
## Rejected alternatives
Registries inside spaces; direct workspace->runtime deploy paths.
