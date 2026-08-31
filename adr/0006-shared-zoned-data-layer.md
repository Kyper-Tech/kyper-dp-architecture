---
id: ADR-0006
status: accepted
date: 2026-08-31
affects: [KYP-T-DATA, KYP-T-DATA-22, KYP-T-DATA-25]
---
# One data layer shared across environments, protected by zoning and access policy
## Context
Data is not copied per environment.
## Decision
Zones: raw, curated (writable only by prod orchestration identity), per-env sandbox.
Nonprod reads per classification; writes only to its sandbox; grants audited; predictions
env-labelled.
## Consequences
Environment boundary becomes authorization correctness; shared failure domain across envs
(managed object storage mitigates for cloud tenants); query engine needs workload isolation.
## Rejected alternatives
Per-environment data copies.
