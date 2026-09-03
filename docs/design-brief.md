# Kyper platform architecture — design brief (v13, 2026-08-31)

This brief tells the story of the Kyper platform architecture: what the
platform is made of, how the parts relate, and which decisions gave it this
shape. Read it when you need the whole picture in one pass. The model, the
diagrams, the ADRs and the per-area requirement files carry the detail;
this document explains how they fit together.

One reading rule holds throughout: every name here is a capability, not a
product. The model states what a component promises (its contract); which
technology fulfills that promise is decided per tenant class in
[architecture/bindings/](../architecture/bindings/)
([ADR-0007](../adr/0007-object-store-contract-bindings.md)). So "object
store" means "keeps objects, speaks an S3-compatible API", and whether that
is GCS, S3 or SeaweedFS depends on where the tenant runs.

## Planes

The architecture's first cut is into three planes. A plane is the highest
level of structure: an operational domain that bundles the capabilities
which must be run and trusted together, with its own trust stance and its
own instancing rule. Nothing runs "as a plane" (planes are groupings, not
components); every component in the platform lives in exactly one of the
three.

| Plane | Instances | Operated by | Network direction |
|---|---|---|---|
| Control | 1 | Kyper | never initiates into a tenant |
| Tenant | one per customer | Kyper-managed, customer-owned data | pulls from control |
| Edge | 0..N per tenant, per site | tenant plane | exchanges with tenant only via sync layer |

Two words are used precisely throughout this brief: **edge** is the plane —
the class of thing Kyper deploys; a **site** is one deployment of that
plane at one location (taxonomy: an instance). Customer-owned systems (a
historian, an API) are never part of a site, even when they sit in the
same building — they are external systems on a separate seam.

Trust rules, one per seam:

1. **Control -> tenant (delivery).** The tenant always dials: releases and
   config flow downward, but over connections the tenant opened (agents
   poll and pull, GitOps-style). No listening endpoint and no credential
   lets the control plane reach into a customer environment, so
   compromising it grants access to zero customer networks. (ADR-0001)
2. **Tenant <-> edge (sync).** Neither side dials the other; both meet at
   the sync layer. Sites connect outbound to it, pushing telemetry and
   alert acks up and fetching signed bundles down. Nothing on the tenant
   side ever connects into a site. (ADR-0003)
3. **Tenant -> customer systems (ingestion).** Push or pull, per tenant.
   In pull mode the tenant's connectors DO dial out to the customer's
   system, wherever it is hosted, with credentials held in that tenant's
   Secrets and every use audited. (ADR-0001)

## Control plane (thin by design; SaaS-lens analysis pending)
- Fleet config — tenant registry + desired state per tenant
- Artifact registry — golden: signed, with SBOM
- Release control
- Staff identity federation
- Fleet health aggregation
- Tenant lifecycle — GAP: provision, suspend, offboard with data export

The tenant registry carries: tenant class -> storage substrate -> availability
posture; siteClass per site; ingestion mode (push | pull); enabled
modules; version pins.

## Tenant plane
### Environment container — instantiated as nonprod and prod (ADR-0005)

| Area | Contains | Rule |
|---|---|---|
| Dev workspace | Sessions, build/test jobs, environment images, scratch | Ephemeral (ADR-0004). Publishes only to source + artifact repos; curated data only. (ADR-0012) |
| ML workspace | Notebook sessions, training jobs, environment images, scratch | Ephemeral (ADR-0004). Publishes only to model registry + experiments; raw reads under audited grants. (ADR-0012) |
| Data workspace | Sessions, pipeline build/test jobs, environment images, scratch | Ephemeral (ADR-0004). Publishes only to source + artifact repos; raw + curated reads under audited grants, for pipeline development. (ADR-0015) |
| Serving | Model runtime, retrieval, inference gateway, drift monitor | Stateless: models in from registry, predictions out to storage. |
| Application | App runtime, API gateway, alerting (authority), public ingress | Stateless; the only public entry point. |
| Orchestration | Ingest, transform, scoring, retraining trigger, idle scale | One scheduler per environment; owns all recurring work incl. scale-to-zero. |

### Data layer — shared across environments, zoned (ADR-0006)

| Group | Contains |
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
Message transport · Artifact transfer · Offline queue · Traffic priority per siteClass.
Neither plane holds an address of a service in the other.

## Edge plane — optional, per site

A site is one deployment of this plane at one location, classed by
siteClass (connected | remote). The site is only what Kyper deploys:
customer systems at the same location are externals, reached through the
ingestion seam (trust rule 3), never through the site.

| Area | Contains | Rule |
|---|---|---|
| Inference runtime | Inference, preprocess/filter, store-and-forward, local alerting | Alerting is a replica: acks sync upward, tenant alerting authoritative (ADR-0010). |
| Site management | Update agent, device identity + attestation, time sync, network services | Always present when edge is deployed. |
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
Edge-AI whitepaper (applied in v13: site management, local preprocessing/alerting, traffic priority).
