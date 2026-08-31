# Requirements — Control plane (KYP-C)

No areas yet (components sit directly in the plane); requirements at plane
level until that changes.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-C-01 | The control plane MUST never initiate a connection into a tenant; every delivery path is tenant-pull. | ADR-0001 |
| REQ-KYP-C-02 | The control plane MUST hold no credentials into any customer environment. | ADR-0001 |
| REQ-KYP-C-03 | Golden artifacts MUST be signed and carry an SBOM before any tenant can pull them. | — |
| REQ-KYP-C-04 | The tenant registry MUST be the single authority for per-tenant resolution: class, binding resolution, siteClass per site, ingestion mode, enabled modules, version pins. | ADR-0013 (proposed) |
| REQ-KYP-C-05 | Staff access MUST enter only via the staff identity federation. | — |
| REQ-KYP-C-06 | Tenant lifecycle (provision, suspend, offboard with data export) — GAP, requirements to be defined with the lifecycle decision. | — |

Quality: [Q-02](../arc42/10-quality-requirements.md) (blast radius).
