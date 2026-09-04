---
id: ADR-0022
status: proposed
date: 2026-08-31
affects: [KYP-F, KYP-C-FLEET-02]
amends: [ADR-0001, ADR-0004, ADR-0005, ADR-0012, ADR-0018]
---
# The product factory: a fourth plane where Kyper builds, tests and signs the product

## Context
The platform is built, tested and signed by Kyper before the control plane
ships it. That work needs a plane of its own. Kyper's engineers are not a
customer's people, the product is not a customer's workload, and shared
models are derived from no customer's data — so none of it belongs in a
tenant, and the control plane deliberately holds nothing but fleet
metadata and finished artifacts.

## Decision
A fourth plane, the product factory (KYP-F): one instance, Kyper operated.

### Purpose
The factory is where the platform and the shared models are developed,
tested against a tenant-shaped reference environment, and turned into
golden artifacts: signed, scanned, with an SBOM. It is the origin of
everything the control plane distributes.

### Areas
- Product workspaces — development of the platform and of shared models.
  Ephemeral, nothing durable, publishing only to the factory's registries
  ([ADR-0004](0004-registries-only-handoff.md)).
- Factory registries — source repo, artifact repo, model registry,
  experiments.
- Reference environment — a tenant-shaped environment on synthetic data,
  where the product is tested before release. Not a tenant; holds no
  customer data.
- Factory operations — CI/CD, build, scanning.
- Factory trust — staff identity, secrets, and the signing keys that make
  an artifact golden.

### Boundaries
The factory's only outbound path is publishing golden artifacts into the
control plane's registry (KYP-C-FLEET-02). It has no relation to any tenant
plane in either direction: it cannot reach a tenant, and no tenant depends
on it. Tenants receive the product from the control plane by pull
([ADR-0001](0001-plane-structure.md)).

### Customer data
Customer data does not enter the factory. Work that needs real data
happens inside the tenant, in its production workspace
([ADR-0021](0021-workspace-instances-differ-by-environment.md)), where the
data already is.

Where that is impossible, a customer may consent to an extract, exported by
the tenant — never pulled by the factory — under the consent shape of
[ADR-0006](0006-shared-zoned-data-layer.md): named datasets, stated
purpose, an expiry, recorded and audited. It lands in an isolated enclave,
is never copied into a workspace or a registry, and is destroyed at expiry.

Shared models are trained on synthetic, public or consented data only;
never on one customer's data without that customer's consent
(REQ-KYP-T-MLWS-06).

## Consequences
- The factory holds the source and the signing keys, with a signed path to
  every tenant. It is the highest-value target in the architecture and
  needs the strongest controls of any plane.
- Golden artifacts have a producer, so "signed, scanned, SBOM attached"
  (REQ-KYP-C-03) is a property of a modeled path rather than a promise.
- The reference environment must keep the shape of a real tenant, or
  testing there proves nothing.
- Kyper engineers have no standing access to customer data. Reproducing a
  customer-specific defect is harder as a result, and consent is the
  pressure valve; it must not become routine.

## Rejected alternatives
- Building the product in the control plane: mixes fleet operation with
  development, and puts source and signing keys in the plane every tenant
  pulls from.
- Building it in a tenant: couples the product to one customer, next to
  that customer's data.
- The factory pulling data from tenants under consent: any factory-initiated
  path into a tenant is the inbound access ADR-0001 removes.
