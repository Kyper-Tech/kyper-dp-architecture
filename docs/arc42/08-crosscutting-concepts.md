# 8. Crosscutting Concepts

> Skeleton — to be filled. Cross-cutting concerns exist once, in platform
> bands, and are consumed — never re-implemented inside an area (placement
> rule 4):

- Trust services band (KYP-T-TRUST): identity, secrets, keys, admission,
  audit, network policy.
- Operation services band (KYP-T-OPS): CI/CD, observability, synthetics,
  incidents/SLOs, scanning, backup+DR, metering.
- The contract seam pattern (data / model / deploy contracts):
  [design brief — contracts](../design-brief.md#contracts-the-seam-pattern).
- Zoning and access policy across environments:
  [ADR-0006](../../adr/0006-shared-zoned-data-layer.md).
