---
id: ADR-0005
status: proposed
date: 2026-08-31
affects: [KYP-T]
---
# Two environments per tenant: nonprod and prod
## Context
Three environments multiply per-tenant cost; stage's rehearsal role is covered elsewhere.
## Decision
Environment container instantiated as nonprod and prod. Stage available as configuration
for tenants whose contract demands it.
## Consequences
Full-scale rehearsal = nonprod run against curated read-only. Environments are an axis
(metadata), never elements.
## Rejected alternatives
dev/stage/prod.
