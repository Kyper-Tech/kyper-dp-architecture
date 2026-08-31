# Requirements — Edge site services (KYP-E-SITE)

Boundary rule: always present when edge is deployed.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-E-SITE-01 | The update agent MUST apply only signed bundles pulled through the sync layer; no other update path exists. | ADR-0001, ADR-0003 |
| REQ-KYP-E-SITE-02 | Devices MUST enroll via identity + attestation before exchanging anything with the tenant plane. | — |
| REQ-KYP-E-SITE-03 | Time sync MUST bound clock skew so event ordering and alert timestamps stay trustworthy across disconnections. | — |
| REQ-KYP-E-SITE-04 | Neither side MUST hold a service address of the other; all exchange is via the sync layer. | ADR-0003 |

Quality: [Q-01](../arc42/10-quality-requirements.md) (disconnection).
