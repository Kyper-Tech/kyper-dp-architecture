# Requirements — how and where

One file per area, named by the area's KYP-ID (`KYP-T-DATAWS.md`).
Functional requirements live here; quality (non-functional) requirements
live in [arc42 §10](../arc42/10-quality-requirements.md) as measurable
scenarios — these files link to their rows, never restate them.

## Scheme
- `REQ-<KYP-ID>-<nn>` — the requirement id extends the KYP-ID join key:
  ADRs, Linear issues and test plans cite requirements by this id.
- Each requirement: one MUST-statement about what the area always does,
  optionally `satisfied-by:` ADR ids and `verified-by:` (test, review,
  gate) once known.

## Boundaries (what does NOT belong here)
- What someone should do next sprint -> Linear (the issue cites the REQ).
- Why a requirement is satisfied this way -> the ADR (cited, not
  paraphrased).
- How well / how fast / how resilient -> a quality scenario in arc42 §10.
- Analysis findings -> Notion register (links back by REQ id).

## Files

Tenant plane:
- [KYP-T-DEVWS](KYP-T-DEVWS.md) — dev workspace
- [KYP-T-MLWS](KYP-T-MLWS.md) — ML workspace
- [KYP-T-DATAWS](KYP-T-DATAWS.md) — data workspace
- [KYP-T-SRV](KYP-T-SRV.md) — serving
- [KYP-T-APP](KYP-T-APP.md) — application
- [KYP-T-ORCH](KYP-T-ORCH.md) — orchestration
- [KYP-T-DATA](KYP-T-DATA.md) — data layer
- [KYP-T-REG](KYP-T-REG.md) — registries
- [KYP-T-TRUST](KYP-T-TRUST.md) — trust services
- [KYP-T-OPS](KYP-T-OPS.md) — operation services

Edge plane:
- [KYP-E-RT](KYP-E-RT.md) — inference runtime
- [KYP-E-SITE](KYP-E-SITE.md) — site management
- [KYP-E-APP](KYP-E-APP.md) — application (optional)
- [KYP-E-ORCH](KYP-E-ORCH.md) — orchestration (optional)

Control plane (no areas yet — plane level):
- [KYP-C](KYP-C.md) — control plane
