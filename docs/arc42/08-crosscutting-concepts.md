# 8. Crosscutting Concepts

Concerns that exist once and are consumed, never re-implemented inside an
area (placement rule 4).

## The contract seam pattern

Wherever something crosses from one responsibility to another, the handoff
is governed by a contract rather than by convention. The same shape recurs
at three seams: what is promised is explicit, a version is what changes, and
one named component refuses whatever does not conform.

| Seam | Contract | States | Enforced by | On violation |
|---|---|---|---|---|
| Ingestion — customer systems to the data layer | Data contract | Schema, semantics, quality thresholds, delivery expectations | Data contracts (KYP-T-DATA-12), quality (KYP-T-DATA-21) | Quarantine; the data does not enter the raw zone silently |
| Promotion — producer to runtime | Model contract, as a registry entry | Input and output schemas, evaluation thresholds met, per-target variants including quantized edge bundles | Model registry (KYP-T-REG-03) | Not promotable; the runtime has nothing to consume |
| Deployment — registry to runtime | Deploy contract | Signed, scanned artifact with an SBOM | Admission (KYP-T-TRUST-04) | Refused at admission; the artifact does not run |

Rules that hold at all three:

- A breaking change is a new version, never an edit in place. Registries
  are write-once ([ADR-0004](../../adr/0004-registries-only-handoff.md)),
  and a data contract's consumers are entitled to the version they were
  built against.
- The contract is the only thing the far side may depend on. Anything not
  stated is not promised, and depending on it is a defect.
- Enforcement is a named component, not a review step, so a violation is a
  runtime fact rather than a matter of discipline.

Distinct from *capability contracts* (taxonomy §9), which state what a
component promises so that a product can be bound to it per tenant class.
Those are about substitutability; these are about handoffs.

## Identity, secrets and trust

Trust services band (KYP-T-TRUST): identity for humans, workloads and
devices; secrets; keys; admission; audit trail; network policy. Consumed
by every area; re-implemented by none. Customer users federate to the
customer's own IdP per tenant
([ADR-0018](../../adr/0018-customer-identity-federation.md)); Kyper staff
enter only through the control plane's staff federation.

## Operations

Operation services band (KYP-T-OPS): CI/CD, observability, synthetics,
incidents and SLOs, scanning, backup and DR, metering.

## Zoning and data access

Zones partition the analytical stores and carry the environment boundary as
authorization rather than infrastructure; access follows purpose, not
environment ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md)).
