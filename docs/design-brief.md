# Kyper platform architecture — design brief (v13, 2026-08-31)

Component level, capability names only. Products are bindings, not components
([ADR-0007](../adr/0007-object-store-contract-bindings.md)): the model states
the contract a component promises; the concrete product fulfilling it per
tenant class lives in [architecture/bindings/](../architecture/bindings/),
keyed by KYP-ID x tenant class.

## Planes
| Plane | Instances | Operated by | Network direction |
|---|---|---|---|
| Control | 1 | Kyper | never initiates into a tenant |
| Tenant | one per customer | Kyper-managed, customer-owned data | pulls from control |
| Edge | 0..N per tenant, per site | tenant plane | exchanges with tenant only via sync layer |

Pull-only downward. No inbound path from control plane into a tenant. (ADR-0001, ADR-0002)

## Control plane (thin by design; SaaS-lens analysis pending)
- Fleet config — tenant registry + desired state per tenant
- Artifact registry — golden: signed, with SBOM
- Release control
- Staff identity federation
- Fleet health aggregation
- Tenant lifecycle — GAP: provision, suspend, offboard with data export

The tenant registry carries: tenant class -> storage substrate -> availability
posture; site connectivity classes; ingestion mode (push | pull); enabled
modules; version pins.

## Tenant plane
### Environment container — instantiated as nonprod and prod (ADR-0005)

| Area | Contains | Rule |
|---|---|---|
| Dev workspace | Sessions, build/test jobs, environment images, scratch | Ephemeral (ADR-0004). Publishes only to source + artifact repos; curated data only. (ADR-0012) |
| ML workspace | Notebook sessions, training jobs, environment images, scratch | Ephemeral (ADR-0004). Publishes only to model registry + experiments; raw reads under audited grants. (ADR-0012) |
| Serving | Model runtime, retrieval, inference gateway, drift monitor | Stateless: models in from registry, predictions out to storage. |
| Application | App runtime, API gateway, alerting (authority), public ingress | Stateless; the only public entry point. |
| Orchestration | Ingest, transform, scoring, retraining trigger, idle scale | One scheduler per environment; owns all recurring work incl. scale-to-zero. |

### Data layer — shared across environments, zoned (ADR-0006)

| Band | Contains |
|---|---|
| Ingestion | OT gateway (boundary), connectors, data contracts, streams |
| Storage | Object store (S3 contract, ADR-0007), tables, operational database, indexes (vector, feature), predictions (env-labelled) |
| Data management | Catalog, query engine, lineage, quality, env zones, classification, retention + tiering, access policy |

Zone rules:
- curated zone: writable only by the prod orchestration identity
- nonprod: reads curated/raw per classification; writes only to its own sandbox
- every cross-zone grant is audited

Catalog stays in data management — it IS the data access path (accepted asymmetry).

### Per-tenant, cross-environment bands

| Band | Contains | Rule |
|---|---|---|
| Registries | Source repo, artifact repo, model registry, experiments | The only handoff seam. Immutable, versioned; CI/CD alone moves an entry into a runtime. (ADR-0004) |
| Trust services | Identity (human, workload, device), secrets, keys, admission, audit trail, network policy | Exist once per tenant; consumed, never re-implemented. |
| Operation services | CI/CD, observability (+ outbound log shipper), synthetics, incidents/SLOs, scanning, backup + DR, metering | Exist once per tenant; consumed, never re-implemented. |

## Sync layer (boundary between tenant and edge) — ADR-0003
Message transport · Artifact transfer · Offline queue · Traffic priority per link class.
Neither plane holds an address of a service in the other.

## Edge plane — optional, per site

| Area | Contains | Rule |
|---|---|---|
| Runtime | Inference, preprocess/filter, store-and-forward, local alerting | Alerting is a replica: acks sync upward, tenant alerting authoritative (ADR-0010). |
| Site services | Update agent, device identity + attestation, time sync, network services | Always present when edge is deployed. |
| Application *(optional)* | Operator UI, local API | Deployed only at some sites. |
| Orchestration *(optional)* | Local schedules, buffer flush | Schedules only what must survive disconnection. |

Edge never trains, never holds the catalog. Store-and-forward is the one
intentional co-location of state and behaviour outside the data layer.

## Contracts (the seam pattern)
Data contract at ingestion (schema, semantics, quality thresholds, delivery; violations
quarantine; breaking change = new version). Model contract = registry entry (schemas,
evaluation thresholds met, per-target variants incl. quantized edge bundles). Deploy
contract = signed, scanned artifact verified by admission.

## Accepted costs
Shared data layer = shared failure domain across envs (mitigated for cloud tenants by managed
object storage; catalog/db/indexes/query engine remain self-run). Query engine needs
workload isolation between prod app and nonprod exploration. No formal stage env: full-scale
rehearsal = nonprod run against curated read-only.

## Open decisions
- Request-response vs batch inference (blocks online feature path) — oldest open fork
- Semantic layer above query engine (only if >1 consumer defines same KPI)
- Availability targets per stateful component; DR targets (RPO/RTO) per tenant class
- Tenant lifecycle (provision/suspend/offboard with data export) in control plane
- Analyst workspace (own area vs a home inside dev workspace)
- Federated learning across tenants (future option; keep compatible, do not build)

## Standards to map against (see docs/analysis-plan.md)
ISO/IEC 23053 (vocabulary), ISO/IEC 5338/42001/23894/5259, CNCF CNAI + Data-on-K8s AI
whitepaper, AWS Well-Architected ML Lens + SaaS Lens, Google MLOps practitioners guide,
IIC IIRA v1.10 (tiers, gateway pattern = sync layer), IEC 62443 zones/conduits, OpenInfra
Edge-AI whitepaper (applied in v13: site services, local preprocessing/alerting, traffic priority).
