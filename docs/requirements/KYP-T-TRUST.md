# Requirements — Trust services (KYP-T-TRUST)

Boundary rule: exist once per tenant; consumed, never re-implemented.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-TRUST-01 | Every human, workload and device MUST have a platform identity; no shared accounts. | — |
| REQ-KYP-T-TRUST-02 | Secrets MUST be fetched at runtime under a workload identity with short-lived leases; every fetch is an audit event. Credentials into customer systems exist only in this tenant's plane. | [ADR-0001](../../adr/0001-plane-structure.md) |
| REQ-KYP-T-TRUST-03 | Admission MUST verify signature and scan status before any artifact or model runs. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-TRUST-04 | The audit trail MUST be append-only and tamper-evident; retention per compliance scope. | — |
| REQ-KYP-T-TRUST-05 | Network policy MUST be default-deny between areas; allowed flows mirror declared model relations. | — |
| REQ-KYP-T-TRUST-06 | Workloads MUST authenticate as workload identities, never with a user's credentials. Where a human initiated the work, their identity is propagated as request context and the mediating service resolves the effective scope (instance ceiling ∩ user grant); the audit trail records both the workload and the user it acted for. | [ADR-0021](../../adr/0021-workspace-instances-differ-by-environment.md) |
| REQ-KYP-T-TRUST-07 | Humans MUST hold no data-plane permissions. A person's data entitlements exist only in the access-policy layer; the only principals holding permissions on a store are workload identities. Emergency access uses the break-glass grant, never a direct permission. | [ADR-0021](../../adr/0021-workspace-instances-differ-by-environment.md) |
| REQ-KYP-T-TRUST-08 | Each workspace instance MUST have its own workload identity, never shared with another instance, holding only the permissions of that instance's ceiling — so the ceiling holds even if policy evaluation fails. | [ADR-0021](../../adr/0021-workspace-instances-differ-by-environment.md) |

Quality: [Q-02](../arc42/10-quality-requirements.md),
[Q-03](../arc42/10-quality-requirements.md),
[Q-05](../arc42/10-quality-requirements.md).
