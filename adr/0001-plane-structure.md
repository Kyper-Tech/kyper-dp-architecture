---
id: ADR-0001
status: proposed
date: 2026-08-31
affects: [KYP-C, KYP-F, KYP-S, KYP-T, KYP-E]
---
# Plane structure: five planes, and the trust direction across each seam

Amended by [ADR-0022](0022-product-factory-plane.md) (product factory) and
[ADR-0023](0023-common-services-plane.md) (common services): the planes are
five, not three.

## Context
Per-customer deployments must scale operationally and serve air-gapped industrial sites.
## Decision
Five planes: control, product factory, common services, tenant, edge.
Control plane never initiates into a tenant; tenants pull config and artifacts.
Edge pulls from tenant through a boundary. The control plane holds no credentials into any
customer environment; credentials that reach into one (pull-mode connectors) exist only
inside that customer's own tenant plane, stored in Secrets (KYP-T-TRUST-02) with use
recorded by Audit trail (KYP-T-TRUST-05). Ingestion mode
(push | pull) is a per-tenant fact recorded in the tenant registry — metadata, never a
model element.

The product factory publishes only to the control plane and has no relation to any
tenant ([ADR-0022](0022-product-factory-plane.md)). Common services never initiates into
a tenant; a tenant that has opted in reaches it outbound
([ADR-0023](0023-common-services-plane.md)).
## Consequences
Fleet management is a first-class control-plane concern; every delivery path is pull/async.
A control-plane compromise grants access into zero customer networks; a pull-connector
credential's blast radius is the one tenant it lives in. Pull-mode tenants add connector
credential rotation and use-audit to the Trust services area's (KYP-T-TRUST) evidence
obligations.
## Rejected alternatives
Push-based CI into customer clusters; fully distributed (no core) model;
forbidding pull-mode ingestion platform-wide (many OT historians cannot push).
