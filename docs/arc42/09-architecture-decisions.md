# 9. Architecture Decisions

Decisions are ADRs in [`adr/`](../../adr/) — that directory is the single
authoring surface for decision facts. This section is an index, nothing more.
Never re-open an accepted decision without a new ADR.

| ADR | Decision | Affects |
|---|---|---|
| [ADR-0001](../../adr/0001-three-planes-pull-only.md) | Three planes; pull-only trust downward | KYP-C, KYP-T, KYP-E |
| [ADR-0002](../../adr/0002-tenant-per-customer.md) | Silo tenancy: one tenant plane per customer | KYP-T |
| [ADR-0003](../../adr/0003-generic-sync-layer.md) | Generic sync layer, not a named broker | KYP-T-SYNC-01, KYP-E |
| [ADR-0004](../../adr/0004-registries-only-handoff.md) | Registries are the only producer→runtime handoff | KYP-T-REG, KYP-T-WS |
| [ADR-0005](../../adr/0005-two-environments.md) | Two environments: nonprod and prod | KYP-T |
| [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) | One shared, zoned data layer across environments | KYP-T-DATA |
| [ADR-0007](../../adr/0007-object-store-contract-bindings.md) | Object store contract in model; products as bindings | KYP-T-DATA-01 |
| [ADR-0008](../../adr/0008-unified-workspaces.md) | One workspace subsystem, dev/ML profiles | KYP-T-WS |
| [ADR-0009](../../adr/0009-architecture-toolchain.md) | Taxonomy + arc42 + LikeC4 + CI gate; Notion links only | — |
| [ADR-0010](../../adr/0010-alerting-authority.md) | Tenant alerting authoritative; edge is a replica | KYP-T-APP-03, KYP-E-RT-04 |

Rejected options that must not be re-proposed are listed in
[CLAUDE.md](../../CLAUDE.md) ("Rejected options") with the ADR that closed
each one.

New decisions: copy [`adr/template.md`](../../adr/template.md) to
`adr/NNNN-title.md` with status `proposed`; flip to `accepted` in the merging
PR; list affected KYP-IDs in `affects:`.
