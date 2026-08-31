# 1. Introduction and Goals

## What Kyper is

Kyper is an industrial AI platform delivered as one managed deployment per
customer. It ingests OT/plant data, manages it in a governed data layer,
supports model development and training, serves models and applications, and
extends inference to factory sites that may lose WAN connectivity for days.

The full narrative lives in the [design brief](../design-brief.md) (v13) —
this section states only the goals and their drivers.

## Top quality goals

| Priority | Goal | Driver | Anchored by |
|---|---|---|---|
| 1 | Data sovereignty and isolation per customer | Industrial customers; some on-prem, some air-gap-adjacent | silo tenancy ([ADR-0002](../../adr/0002-tenant-per-customer.md)) |
| 2 | Delivery is pull-only: the control plane never initiates into a tenant | No *central* credentials into customer environments — data ingestion may be push or pull per tenant, but those connector credentials live inside that tenant's own plane, never in the control plane | pull-only planes ([ADR-0001](../../adr/0001-three-planes-pull-only.md)); OT gateway + connectors (KYP-T-DATA) |
| 3 | Site autonDLH -ction | Edge sites lose WAN for days but must keep inferring and alarming | sync layer ([ADR-0003](../../adr/0003-generic-sync-layer.md)), edge alerting replica ([ADR-0010](../../adr/0010-alerting-authority.md)) |
| 4 | Per-tenant cost that scales with tenant count | Cost is multiplicative in the silo model | two environments ([ADR-0005](../../adr/0005-two-environments.md)), shared zoned data layer ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md)) |
| 5 | Provable promotion integrity | Only reviewed, signed, evaluated artifacts reach runtimes | registries-only handoff ([ADR-0004](../../adr/0004-registries-only-handoff.md)) |

## Stakeholders

| Stakeholder | Concern | Where it is addressed |
|---|---|---|
| Customer (data owner) | Sovereignty, isolation, export on offboarding | tenant plane; lifecycle gap tracked in [design brief — open decisions](../design-brief.md#open-decisions) |
| Plant / OT operations | Local inference and alerting despite dead WAN | edge plane, [ADR-0010](../../adr/0010-alerting-authority.md) |
| Data scientists / developers | One workspace, dev and ML profiles | [ADR-0008](../../adr/0008-unified-workspaces.md) |
| Kyper operations | Operate a fleet of tenant silos from one control plane | control plane ([ADR-0001](../../adr/0001-three-planes-pull-only.md)) |
| Security reviewers | Trust boundaries as named components; zone model | placement rules in [CLAUDE.md](../../CLAUDE.md); [analysis plan](../analysis-plan.md) phase 3 |
| Business / non-git audience | Discoverable narrative without Git access | Notion portal, links only ([ADR-0009](../../adr/0009-architecture-toolchain.md)) |
