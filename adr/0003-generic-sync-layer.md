---
id: ADR-0003
status: proposed
date: 2026-08-31
affects: [KYP-T-SYNC-01, KYP-E]
---
# Decouple edge from tenant through a generic sync layer, not a named message broker
## Context
Edge sites lose WAN for days; neither side may depend on the other's service addresses.
## Decision
A boundary component with message transport, artifact transfer, offline queue and traffic
priority per link class. Whether one or two products implement it is a binding decision.
## Consequences
Model bundles too large for a bus need artifact transfer; both sides store-and-forward.
## Rejected alternatives
Direct service calls; naming a broker at component level.
