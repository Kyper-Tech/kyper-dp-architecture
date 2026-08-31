---
id: ADR-0002
status: proposed
date: 2026-08-31
affects: [KYP-T]
---
# One tenant-plane deployment per customer (silo model) with a shared control plane
## Context
Industrial customers require data sovereignty and isolation; some are on-prem.
## Decision
Silo tenancy: full tenant plane per customer. Shared control plane only.
## Consequences
Cost is multiplicative per tenant; idle-scale and environment count matter (ADR-0005).
Tenant registry records tenant class -> substrate -> availability posture.
## Rejected alternatives
Pooled multi-tenant data/serving.
