---
id: ADR-0019
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA-01]
---
# Requirements for the on-prem object store; no product selected yet

## Context
[ADR-0007](0007-object-store-contract-bindings.md) left the onprem product
for the object-store contract open, and
[ADR-0011](0011-onprem-object-store-seaweedfs.md) proposed binding a
specific product before the criteria were settled. Meanwhile the contract
profile in
[architecture/bindings/storage.yaml](../architecture/bindings/storage.yaml)
gained an immutability (WORM) row, which audit archives depend on. On-prem
footprints are small and edge-adjacent, and the team operating them is not
a storage team.

## Decision
No on-prem object store product is selected. The binding stays `TBD` with
`status: not-selected`, and a candidate is admitted only against the
criteria below.

Beyond every `required` row of the `object-store` contract profile, an
on-prem candidate must satisfy:

1. Object immutability (WORM): objects or prefixes can be made immutable
   for a stated retention period, so audit archives cannot be altered or
   deleted early.
2. Access control granular enough to carry the curated-zone write rule
   ([ADR-0006](0006-shared-zoned-data-layer.md)) in the store's own IAM,
   rather than relying on access policy mediation (KYP-T-DATA-25) to
   compensate for what the store cannot express.
3. Operable by a team that is not a storage team.
4. A licence and roadmap that permit shipping inside a customer-deployed
   product.

A local object store may be run for application development. That is a
developer convenience, not a binding, and nothing in the architecture may
assume it exists or behaves any particular way.

## Consequences
- On-prem tenants have no production object store binding; this is an open
  decision with stated criteria, not an oversight.
- Requirement 1 excludes any candidate that cannot provide WORM, before
  operability or cost are discussed.
- Requirement 2 makes store-native zone enforcement the expectation;
  a candidate that needs access policy to compensate is weaker, and that
  weakness must be argued explicitly rather than assumed acceptable.
- The object store provides no block storage in any case: the operational
  database (KYP-T-DATA-03) needs a separate CSI.

## Rejected alternatives
- Selecting a product now: the criteria, in particular immutability, were
  settled after the candidates were discussed.
