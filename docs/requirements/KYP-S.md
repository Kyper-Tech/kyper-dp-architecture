# Requirements — Common services (KYP-S)

Purpose: shared capacity and shared-model inference for tenants that choose
to join the shared network, without changing anything for tenants that do
not ([ADR-0023](../../adr/0023-common-services-plane.md)). Design open;
these requirements bound what any design must satisfy.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-S-01 | No workload MUST be placed and no request routed to common services for a tenant that has not opted in. The default is not opted in; opt-in is recorded in the tenant registry. | [ADR-0023](../../adr/0023-common-services-plane.md), [ADR-0013](../../adr/0013-tenant-registry-record-schema.md) |
| REQ-KYP-S-02 | Common services MUST never initiate into a tenant; an opted-in tenant reaches it outbound. | [ADR-0023](../../adr/0023-common-services-plane.md), [ADR-0001](../../adr/0001-plane-structure.md) |
| REQ-KYP-S-03 | Shared capacity MUST be metered and attributable per tenant. | [ADR-0023](../../adr/0023-common-services-plane.md) |
| REQ-KYP-S-04 | No capability MUST be built before its isolation model is decided in an ADR of its own. | [ADR-0023](../../adr/0023-common-services-plane.md) |

Quality: [Q-08](../arc42/10-quality-requirements.md) (blast radius, open).
