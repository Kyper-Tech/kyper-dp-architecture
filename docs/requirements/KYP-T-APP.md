# Requirements — Application (KYP-T-APP)

Boundary rule: stateless; the only public entry point.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-APP-01 | All external traffic MUST enter through public ingress; no other component is externally reachable. | — |
| REQ-KYP-T-APP-02 | The app runtime MUST run only signed, promoted artifacts; admission verifies before start. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-APP-03 | Durable application state MUST live in the operational database (data layer), never in the runtime. | — |
| REQ-KYP-T-APP-04 | Tenant alerting MUST own escalation and suppression state, including acks synced up from edge replicas. | [ADR-0010](../../adr/0010-alerting-authority.md) |

Quality: [Q-05](../arc42/10-quality-requirements.md) (promotion integrity).
