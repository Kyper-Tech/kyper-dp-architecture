# Requirements — Trust services (KYP-T-TRUST)

Boundary rule: exist once per tenant; consumed, never re-implemented.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-TRUST-01 | Every human, workload and device MUST have a platform identity; no shared accounts. | — |
| REQ-KYP-T-TRUST-02 | Secrets MUST be fetched at runtime under a workload identity with short-lived leases; every fetch is an audit event. Credentials into customer systems exist only in this tenant's plane. | [ADR-0001](../../adr/0001-three-planes-pull-only.md) |
| REQ-KYP-T-TRUST-03 | Admission MUST verify signature and scan status before any artifact or model runs. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-TRUST-04 | The audit trail MUST be append-only and tamper-evident; retention per compliance scope. | — |
| REQ-KYP-T-TRUST-05 | Network policy MUST be default-deny between areas; allowed flows mirror declared model relations. | — |

Quality: [Q-02](../arc42/10-quality-requirements.md),
[Q-03](../arc42/10-quality-requirements.md),
[Q-05](../arc42/10-quality-requirements.md).
