# Requirements — Control plane (KYP-C)

Purpose: answers Kyper's questions about the fleet (what each tenant runs,
where trustworthy software comes from, who releases what when, is everyone
alive) while sitting in no runtime path and holding no customer data.

No areas yet (components sit directly in the plane); requirements at plane
level until that changes.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-C-01 | The control plane MUST never initiate a connection into a tenant; every delivery path is tenant-pull. | [ADR-0001](../../adr/0001-plane-structure.md) |
| REQ-KYP-C-02 | The control plane MUST hold no credentials into any customer environment. | [ADR-0001](../../adr/0001-plane-structure.md) |
| REQ-KYP-C-03 | Golden artifacts MUST be signed and carry an SBOM before any tenant can pull them. | — |
| REQ-KYP-C-04 | The tenant registry MUST be the single authority for per-tenant resolution: class, binding resolution, siteClass per site, ingestion mode, enabled modules, version pins. | [ADR-0013](../../adr/0013-tenant-registry-record-schema.md) (proposed) |
| REQ-KYP-C-05 | Staff access MUST enter only via the staff identity federation. | — |
| REQ-KYP-C-06 | Tenant lifecycle (provision, suspend, offboard) — GAP. Offboarding MUST cover data export, secure deletion of customer data across every store and backup, and a published exit procedure. Requirements to be defined with the lifecycle decision. | — |
| REQ-KYP-C-07 | The control plane MUST NOT receive or store customer data or anything derived from it (logs, payloads, model weights); fleet health receives aggregated status only. Exception only by explicit customer consent, scoped to named data, a stated purpose and a duration, recorded in the tenant registry, with every transfer audited. Consent is never a default and never survives its duration. | — |

Quality: [Q-02](../arc42/10-quality-requirements.md) (blast radius).
