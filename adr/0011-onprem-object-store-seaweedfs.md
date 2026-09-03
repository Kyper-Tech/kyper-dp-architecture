---
id: ADR-0011
status: superseded-by ADR-0019
date: 2026-08-31
affects: [KYP-T-DATA-01]
---
# Bind the on-prem object store contract to SeaweedFS

Superseded by [ADR-0019](0019-onprem-object-store-requirements.md), which
states the requirements an on-prem object store must satisfy instead of
naming a product. Kept as the record of what was considered.

## Context
[ADR-0007](0007-object-store-contract-bindings.md) left the onprem product
for the object-store contract open. On-prem tenant footprints are small and
operationally constrained (edge-adjacent); the team operating them is not a
storage team. SeaweedFS is light to operate and sufficient for application
development.

## Decision
Not adopted. SeaweedFS was proposed as the onprem binding for
KYP-T-DATA-01 on the strength of its operability, with the acknowledged
compensation that its IAM is coarser than S3-class, so the curated-zone
write rule ([ADR-0006](0006-shared-zoned-data-layer.md)) would have to be
carried by dedicated per-zone identities plus mediation by the access
policy component (KYP-T-DATA-25).

## Consequences
Superseded before adoption, so none took effect. The reasoning that ended
it: the contract profile later gained an immutability (WORM) row for audit
archives, and a product had been proposed before the criteria were
settled. Those criteria now live in
[ADR-0019](0019-onprem-object-store-requirements.md).
