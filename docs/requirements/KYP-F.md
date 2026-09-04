# Requirements — Product factory (KYP-F)

Purpose: where Kyper builds, tests and signs the platform and the shared
models; the origin of everything the control plane distributes
([ADR-0022](../../adr/0022-product-factory-plane.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-F-01 | The factory MUST have no relation to any tenant plane: it cannot reach a tenant, and no tenant depends on it. | [ADR-0022](../../adr/0022-product-factory-plane.md) |
| REQ-KYP-F-02 | Every artifact leaving the factory MUST be signed, scanned and carry an SBOM before it enters the control plane's golden registry. | [ADR-0022](../../adr/0022-product-factory-plane.md) |
| REQ-KYP-F-03 | Customer data MUST NOT enter the factory, except as a consented extract exported by the tenant into an isolated enclave, never copied into a workspace or registry, and destroyed at expiry. | [ADR-0022](../../adr/0022-product-factory-plane.md), [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-F-04 | Shared models MUST be trained on synthetic, public or consented data only; never on one customer's data without that customer's consent. | [ADR-0022](../../adr/0022-product-factory-plane.md) |
| REQ-KYP-F-05 | Signing keys MUST live in factory trust and never leave it; signing is an act of the factory, not of the control plane or a tenant. | [ADR-0022](../../adr/0022-product-factory-plane.md) |
| REQ-KYP-F-06 | The reference environment MUST keep the shape of a real tenant, or a release tested there is not tested. | — |

Quality: [Q-05](../arc42/10-quality-requirements.md) (promotion integrity).
