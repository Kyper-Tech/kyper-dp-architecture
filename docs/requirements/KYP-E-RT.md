# Requirements — Edge inference runtime (KYP-E-RT)

Boundary rule: alerting is a replica; acks sync upward, tenant alerting
authoritative (ADR-0010). Edge never trains, never owns the catalog.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-E-RT-01 | Inference MUST continue through WAN loss for the contracted disconnection window. | ADR-0003 |
| REQ-KYP-E-RT-02 | Store-and-forward MUST lose no telemetry up to its declared buffer capacity; overflow policy is explicit (drop-oldest vs block). | ADR-0003 |
| REQ-KYP-E-RT-03 | Local alerting MUST raise and acknowledge offline; acks sync upward on reconnect; tenant alerting owns escalation after reconcile. | ADR-0010 |
| REQ-KYP-E-RT-04 | Preprocessing MUST reduce telemetry to the traffic priority of the site's siteClass. | ADR-0003 |

Quality: [Q-01](../arc42/10-quality-requirements.md) (disconnection).
