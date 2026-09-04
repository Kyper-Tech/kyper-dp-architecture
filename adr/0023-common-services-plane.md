---
id: ADR-0023
status: proposed
date: 2026-08-31
affects: [KYP-S, KYP-T]
amends: [ADR-0001, ADR-0002, ADR-0007, ADR-0013, ADR-0018]
---
# Common services: a fifth plane for shared capacity, opt-in per tenant, design open

## Context
GPUs sit idle in per-tenant silos. Some customers will accept shared
capacity and shared-model inference for the economics; others never will.
The platform needs a home for the shared offering that leaves the silo
fully intact for every tenant that declines it.

## Decision
A fifth plane, common services (KYP-S), Kyper operated.

### Purpose
Common services offers what is uneconomic to run per tenant — scarce
compute and the serving of shared models — to tenants that choose to join
the shared network, without changing anything for tenants that do not.

### Opt-in
Participation is opt-in per tenant and recorded in the tenant registry.
The default is not opted in. A tenant that has not opted in never has a
workload placed in common services and never has a request routed there.
Opting in is a customer decision with contractual weight, not a platform
default.

### Direction
Common services never initiates into a tenant. An opted-in tenant reaches
it outbound, and receives the result on the connection it opened.

### Capabilities
Two capabilities are intended and named here, not designed:

- a shared capacity pool — hardware assigned to one tenant's workload at a
  time, for training and batch work;
- shared-model inference — factory-built shared models
  ([ADR-0022](0022-product-factory-plane.md)) served to many tenants.

Their risk profiles differ enough that each is designed in its own ADR.
Software reaches common services the way it reaches a tenant: pulled from
the control plane's golden registry.

### Open — to be investigated before either capability is built
- The isolation model for each capability: exclusive assignment and
  attestation for the pool; per-request isolation and batching posture for
  inference.
- The instancing dimension. Jurisdiction is expected, which brings the
  residency decision forward.
- Which tenant classes may opt in; on-prem tenants are likely excluded, as
  their data would otherwise leave the premises.
- The blast-radius statement for a compromise of the plane.
- Classification of request data in flight, which zones (at rest) do not
  cover.
- Observability without request content.
- The relation kind for a tenant invoking a service across a plane
  boundary, which the taxonomy does not yet have.

## Consequences
- Silo tenancy ([ADR-0002](0002-tenant-per-customer.md)) becomes the
  default with one named, opt-in exception.
- For an opted-in tenant, the multi-tenancy answer in a security review
  becomes two-tier: silo for everything at rest, shared with controls for
  work in flight. For a tenant that declines, nothing changes.
- The tenant registry record
  ([ADR-0013](0013-tenant-registry-record-schema.md)) gains opt-in and
  acceptable-jurisdiction fields.
- Metering per tenant (REQ-KYP-T-OPS-05) becomes load-bearing: shared
  capacity must be attributable to be billable.

## Rejected alternatives
- Shared capacity inside each tenant: defeats the purpose.
- Shared capacity inside the control plane: the control plane holds no
  customer data and must stay that way.
- Designing the isolation rules in this ADR: they need investigation, and
  the two capabilities must not share one argument.
