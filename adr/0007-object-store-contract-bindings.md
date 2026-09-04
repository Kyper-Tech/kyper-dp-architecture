---
id: ADR-0007
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA-01]
---
# The model states capability contracts; products and their wire protocols are per-tenant-class bindings

## Context
Cloud tenants use GCS or S3; on-prem tenants need a self-run store with a
weaker posture. Naming the contract after one vendor's protocol
("S3-compatible") would put a product name — Amazon Simple Storage Service
— at the centre of the architecture, the very thing this decision exists to
prevent. It would also misdescribe an existing binding: on GCP the data
stack addresses the store natively through gs://, not through S3.

## Decision
A component states a capability contract; the contract is defined by a
profile in [architecture/bindings/](../architecture/bindings/), and each
binding names the product, the posture and the wire protocol it speaks.

For the object store (KYP-T-DATA-01) the contract is `object-store`: object
CRUD and prefix list, ranged reads, multipart upload, presigned URLs,
per-zone access control in the store's own IAM, encryption at rest, and an
S3-compatible endpoint for components that need one. S3 compatibility is
one required row, an access protocol — not the contract's identity.

Per-tenant resolution stays in the control-plane tenant registry.

## Consequences
- Product swaps touch bindings + an ADR, never the model.
- A product with a different native protocol may bind if it satisfies every
  required row, which keeps Azure Blob and future stores admissible.
- Components that hardcode an S3 SDK depend on one declared row, so that
  dependency is visible rather than assumed.

## Rejected alternatives
- Product names as components.
- Naming the contract `s3-object-api`: a product name as architecture, and
  inaccurate for the GCP binding.
- Requiring one uniform wire protocol across all tenant classes: would
  reject GCS's native path or force every binding through an
  interoperability endpoint.

Scope: common-services bindings are keyed by jurisdiction rather than tenant class ([ADR-0023](0023-common-services-plane.md)).
