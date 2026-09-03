# Requirements — Edge orchestration (KYP-E-ORCH, optional)

Boundary rule: schedules only what must survive disconnection.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-E-ORCH-01 | Local schedules MUST cover only work that must survive disconnection; everything else belongs to the tenant scheduler. | — |
| REQ-KYP-E-ORCH-02 | Buffer flush MUST drain store-and-forward on reconnect, honoring the sync layer's traffic priority. | [ADR-0003](../../adr/0003-generic-sync-layer.md) |
| REQ-KYP-E-ORCH-03 | Edge MUST never schedule training. | — |

Quality: [Q-01](../arc42/10-quality-requirements.md) (disconnection).
