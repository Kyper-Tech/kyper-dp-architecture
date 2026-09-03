# Requirements — Data layer (KYP-T-DATA)

Boundary rule: all durable state; mediated access only; shared across
environments, zoned ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-DATA-01 | All durable platform state MUST live in this area (sole exception: edge store-and-forward, [ADR-0003](../../adr/0003-generic-sync-layer.md)). | — |
| REQ-KYP-T-DATA-02 | Analytical reads MUST be catalog-mediated; no direct store access from other areas. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-DATA-03 | Zone rules MUST hold: curated writable only by prod orchestration identity; nonprod writes only its sandbox; every cross-zone grant audited. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-DATA-04 | Ingested data MUST pass a data contract; violations quarantine; breaking change = new contract version. | — |
| REQ-KYP-T-DATA-05 | Every dataset MUST carry a classification that access decisions and retention derive from. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-DATA-06 | Every store MUST declare a primary or derived DR posture; derived stores MUST be rebuildable from curated + lineage. | [ADR-0014](../../adr/0014-data-layer-storage-layers.md) (proposed) |

Quality: [Q-03](../arc42/10-quality-requirements.md),
[Q-06](../arc42/10-quality-requirements.md),
[Q-07](../arc42/10-quality-requirements.md).
