# 9. Architecture Decisions

Decisions are ADRs in [`adr/`](../../adr/) — that directory is the single
authoring surface for decision facts. This section is an index, nothing more.
Never re-open an accepted decision without a new ADR.

**Current state: every ADR is `proposed`**, except ADR-0011 which is
superseded. Nothing is accepted yet — the baseline is under review.
(ADR-0008 was withdrawn pre-baseline; the number is retired.)

| ADR | Decision | Affects |
|---|---|---|
| [ADR-0001](../../adr/0001-three-planes-pull-only.md) | Three planes; pull-only trust downward | KYP-C, KYP-T, KYP-E |
| [ADR-0002](../../adr/0002-tenant-per-customer.md) | Silo tenancy: one tenant plane per customer | KYP-T |
| [ADR-0003](../../adr/0003-generic-sync-layer.md) | Generic sync layer, not a named broker | KYP-T-SYNC-01, KYP-E |
| [ADR-0004](../../adr/0004-registries-only-handoff.md) | Registries are the only producer→runtime handoff | KYP-T-REG, KYP-T-DEVWS, KYP-T-MLWS |
| [ADR-0005](../../adr/0005-two-environments.md) | Two environments: nonprod and prod | KYP-T |
| [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) | Data layer: sharing follows store class, access follows purpose | KYP-T-DATA and its stores |
| [ADR-0007](../../adr/0007-object-store-contract-bindings.md) | Object store contract in model; products as bindings | KYP-T-DATA-01 |
| [ADR-0009](../../adr/0009-architecture-toolchain.md) | Taxonomy + arc42 + LikeC4 + CI gate; Notion links only | — |
| [ADR-0010](../../adr/0010-alerting-authority.md) | Tenant alerting authoritative; edge is a replica | KYP-T-APP-03, KYP-E-RT-04 |
| [ADR-0011](../../adr/0011-onprem-object-store-seaweedfs.md) *(superseded by ADR-0019)* | On-prem object store binding: SeaweedFS | KYP-T-DATA-01 |
| [ADR-0012](../../adr/0012-split-dev-ml-workspaces.md) | Dev and ML are separate workspace areas | KYP-T-DEVWS, KYP-T-MLWS |
| [ADR-0013](../../adr/0013-tenant-registry-record-schema.md) | Tenant registry record schema; instance sheets are generated | KYP-C-FLEET-01 |
| [ADR-0014](../../adr/0014-data-layer-storage-layers.md) | Layer the storage group: time-series, lakehouse, serving, operational | KYP-T-DATA, KYP-T-DATA-04 |
| [ADR-0015](../../adr/0015-data-engineering-workspace.md) | Data engineering workspace; pipeline promotion path modeled | KYP-T-DATAWS, KYP-T-ORCH, KYP-T-REG-02 |
| [ADR-0016](../../adr/0016-owns-relation-kind.md) | `owns` relation kind for operational stores | KYP-T-DATA-03, KYP-T-APP-01 |
| [ADR-0017](../../adr/0017-customer-system-integration-seam.md) | Customer systems integrate through named boundaries, one altitude per source | KYP-T-DATA-10, KYP-T-DATA-11, KYP-E-RT |
| [ADR-0018](../../adr/0018-customer-identity-federation.md) | Customer users federate to the customer's IdP, per tenant | KYP-T-TRUST-01, KYP-T-TRUST-02, KYP-E-SITE-02 |
| [ADR-0019](../../adr/0019-onprem-object-store-requirements.md) | On-prem object store requirements; no product selected | KYP-T-DATA-01 |

Rejected options that must not be re-proposed are listed in
[CLAUDE.md](../../CLAUDE.md) ("Rejected options") with the ADR that closed
each one.

New decisions: copy [`adr/template.md`](../../adr/template.md) to
`adr/NNNN-title.md` with status `proposed`; flip to `accepted` in the merging
PR; list affected KYP-IDs in `affects:`.
