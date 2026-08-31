---
id: ADR-0007
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA-01]
---
# Model states the S3-compatible contract; products are per-tenant-class bindings
## Context
Cloud tenants use GCS or S3; on-prem tenants need a self-run store with weaker posture.
## Decision
Object store element carries the contract only. architecture/bindings/storage.yaml maps
tenant class -> product -> availability posture. Per-tenant resolution in tenant registry.
## Consequences
Product swaps touch bindings + ADR, never the model. On-prem product still TBD.
## Rejected alternatives
Product names as components.
