---
id: ADR-0001
status: accepted
date: 2026-08-31
affects: [KYP-C, KYP-T, KYP-E]
---
# Split the platform into control, tenant and edge planes with pull-only trust downward
## Context
Per-customer deployments must scale operationally and serve air-gapped industrial sites.
## Decision
Three planes. Control plane never initiates into a tenant; tenants pull config and artifacts.
Edge pulls from tenant through a boundary. No inbound credentials held by Kyper.
## Consequences
Fleet management is a first-class control-plane concern; every delivery path is pull/async.
## Rejected alternatives
Push-based CI into customer clusters; fully distributed (no core) model.
