---
id: ADR-0017
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA-10, KYP-T-DATA-11, KYP-E-RT]
---
# Customer systems integrate through named boundaries, at exactly one altitude per source

## Context
Customer systems (historians, PLCs, cloud APIs) are touched from two
altitudes: tenant connectors ingest (push or pull, [ADR-0001](0001-three-planes-pull-only.md)) and sites
read plant systems locally for inference. Three defects follow today:
the external kind exists but no relation kind can reach it, so none of
this is drawable; the edge side has no named boundary for plant reads
(placement rule 3 violation at the seam IEC 62443 probes first); and
nothing forbids ingesting one source from both altitudes at once, which
would break lineage and double-count data.

## Decision
1. Customer systems are modeled as external elements.
2. New relation kind: integrates : external <-> boundary. An external
   touches the platform only through a named boundary; internal components
   never reference an external directly. Both sides reference the boundary,
   the same discipline boundaries already impose. Push vs pull is not a
   different arrow — it is the source's ingestion mode in the tenant
   registry.
3. The edge inference runtime gains a named boundary: Site OT gateway,
   mirroring the tenant OT gateway, for local plant reads.
4. One source, one path. Each customer source is ingested at exactly one
   altitude: at the site when data feeds local inference or the siteClass
   is remote; at the tenant otherwise (cloud systems, APIs, connected
   plants without edge). The altitude is recorded per source in the tenant
   registry.
5. Credentials follow the accessor. Tenant-ingested sources: credentials
   in that tenant's Secrets, audited ([ADR-0001](0001-three-planes-pull-only.md)). Site-ingested sources:
   credentials held at that site, scoped to it — a compromised site
   exposes one plant's sources, not the tenant's.

## Consequences
- Trust rule 3 (brief) becomes drawable: external -> boundary -> ingestion.
- One seam pattern at both altitudes: data contracts, named boundary,
  scoped credentials, audit. Parameters differ per altitude; the measures
  do not (placement rule 4).
- The tenant registry record ([ADR-0013](0013-tenant-registry-record-schema.md)) grows a per-source entry:
  source id, ingestion altitude, mode (push | pull), owning site if any.
- Model changes on acceptance: integrates in spec + taxonomy §4 and
  Appendix A; Site OT gateway element; first external elements.

## Rejected alternatives
- Direct component -> external relations: unbounded seams; every
  integration would invent its own trust story.
- A separate security regime for cloud-reachable sources ("cloud edge"):
  re-implements cross-cutting concerns, violating placement rule 4.
- Single-altitude ingestion only: forbids either disconnected sites
  (tenant-only) or edge-less customers (site-only).
