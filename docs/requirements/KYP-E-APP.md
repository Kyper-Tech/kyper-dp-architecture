# Requirements — Edge application (KYP-E-APP, optional)

Boundary rule: deployed only at some sites (optional).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-E-APP-01 | Operator UI and local API MUST function fully disconnected. | [ADR-0003](../../adr/0003-generic-sync-layer.md) |
| REQ-KYP-E-APP-02 | Edge application components MUST hold no durable state beyond the runtime's store-and-forward buffer. | — |
| REQ-KYP-E-APP-03 | Local API access MUST use device/site identities; no tenant-plane credentials cached at edge. | [ADR-0001](../../adr/0001-plane-structure.md) |

Quality: [Q-01](../arc42/10-quality-requirements.md) (disconnection).
