---
id: ADR-0002
status: proposed
date: 2026-08-31
affects: [KYP-T]
---
# One tenant-plane deployment per customer (silo model) with shared Kyper-operated planes

Amended by [ADR-0023](0023-common-services-plane.md): silo is the default;
common services is an opt-in exception.

## Context
Industrial customers require data sovereignty and isolation; some are on-prem.
## Decision
Silo tenancy: full tenant plane per customer. Shared planes are Kyper-operated and
hold no customer data (control, product factory), with one exception: common services,
which opted-in tenants may use under rules still to be decided
([ADR-0023](0023-common-services-plane.md)). Silo remains the default.
## Consequences
Cost is multiplicative per tenant; idle-scale and environment count matter ([ADR-0005](0005-two-environments.md)).
Tenant registry records tenant class -> substrate -> availability posture.
Multi-tenancy answers in a security review become two-tier for opted-in tenants:
silo for everything at rest, shared with controls for work in flight.
## Rejected alternatives
Pooled multi-tenant data or serving as the default model.
