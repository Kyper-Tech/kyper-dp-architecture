# Requirements — Operation services (KYP-T-OPS)

Boundary rule: exist once per tenant; consumed, never re-implemented.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-OPS-01 | CI/CD MUST be the only actor moving registry entries into runtimes. | ADR-0004 |
| REQ-KYP-T-OPS-02 | Every artifact MUST pass scanning before promotion; failing artifacts cannot promote. | — |
| REQ-KYP-T-OPS-03 | Backup MUST follow each store's declared DR posture; restores are exercised, not assumed. | ADR-0014 (proposed) |
| REQ-KYP-T-OPS-04 | Observability MUST cover every component; logs ship outbound via the log shipper (pull-only rules hold). | ADR-0001 |
| REQ-KYP-T-OPS-05 | Per-tenant resource usage MUST be metered per environment. | ADR-0002 |

Quality: [Q-06](../arc42/10-quality-requirements.md) (DR).
