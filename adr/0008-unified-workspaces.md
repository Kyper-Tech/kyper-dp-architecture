---
id: ADR-0008
status: accepted
date: 2026-08-31
affects: [KYP-T-WS]
---
# One workspace subsystem with dev and ML profiles
## Context
Dev space and ML space shared session, jobs, environment and scratch anatomy.
## Decision
Single workspaces area; profiles differ only in data scope, publish target and compute quota.
## Consequences
Analyst profile becomes cheap. ML profile's raw-read is a trust-level difference to defend
in security reviews.
## Rejected alternatives
Two sibling subsystems.
