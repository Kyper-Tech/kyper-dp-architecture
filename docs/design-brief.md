# Kyper platform architecture — design brief

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
store" means "keeps objects, with ranged reads, multipart upload and
per-zone access control", and which product provides it — and which
protocol it speaks — depends on where the tenant runs.

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
| Edge | 0..N per tenant, one per location (a deployment = a site) | tenant plane | exchanges with tenant only via sync layer |

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
   compromising it grants access to zero customer networks. ([ADR-0001](../adr/0001-three-planes-pull-only.md))
2. **Tenant <-> edge (sync).** Neither side dials the other; both meet at
   the sync layer. Sites connect outbound to it, pushing telemetry and
   alert acks up and fetching signed bundles down. Nothing on the tenant
   side ever connects into a site. ([ADR-0003](../adr/0003-generic-sync-layer.md))
3. **Tenant -> customer systems (ingestion).** Push or pull, per tenant.
   In pull mode the tenant's connectors DO dial out to the customer's
   system, wherever it is hosted, with credentials held in that tenant's
   Secrets and every use audited. ([ADR-0001](../adr/0001-three-planes-pull-only.md))
4. **Site -> customer systems (local ingestion).** A site reads plant
   systems on the local network; that is why it exists. Credentials for
   those reads are held at the site and scoped to it, so a compromised
   site exposes one plant's sources, never the tenant's. Proposed in
   [ADR-0017](../adr/0017-customer-system-integration-seam.md): a named
   boundary for these reads (site OT gateway), and the rule that each
   source is ingested at exactly one altitude — site or tenant, never
   both.

## Control plane (thin by design; SaaS-lens analysis pending)

The control plane is how Kyper operates the fleet: it answers what each
tenant should run, where trustworthy software comes from, who gets which
release when, whether every tenant is alive, which tenants a CVE affects,
and who at Kyper may act. Customer workloads never touch it — those live
entirely in the tenant planes. Deliberately thin: it sits in no runtime
path and holds no customer data ([REQ-KYP-C-07](requirements/KYP-C.md)), so a control-plane outage
means "no updates today", never a production stop.

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
### Environment container — instantiated as nonprod and prod ([ADR-0005](../adr/0005-two-environments.md))

| Area | Contains | Rule |
|---|---|---|
| Dev workspace | Sessions, build/test jobs, environment images, scratch | Ephemeral ([ADR-0004](../adr/0004-registries-only-handoff.md)). Publishes only to source + artifact repos; curated data only. ([ADR-0012](../adr/0012-split-dev-ml-workspaces.md)) |
| ML workspace | Notebook sessions, training jobs, environment images, scratch | Ephemeral ([ADR-0004](../adr/0004-registries-only-handoff.md)). Publishes only to model registry + experiments; raw reads under audited grants. ([ADR-0012](../adr/0012-split-dev-ml-workspaces.md)) |
| Data workspace | Sessions, pipeline build/test jobs, environment images, scratch | Ephemeral ([ADR-0004](../adr/0004-registries-only-handoff.md)). Publishes only to source + artifact repos; raw + curated reads under audited grants, for pipeline development. ([ADR-0015](../adr/0015-data-engineering-workspace.md)) |
| Serving | Model runtime, retrieval, inference gateway, drift monitor | Stateless: models in from registry, predictions out to storage. |
| Application | App runtime, API gateway, alerting (authority), public ingress | Stateless; the only public entry point. |
| Orchestration | Ingest, transform, scoring, retraining trigger, idle scale | One scheduler per environment; owns all recurring work incl. scale-to-zero. |

### Data layer — analytical stores shared and zoned, the rest per environment ([ADR-0006](../adr/0006-shared-zoned-data-layer.md))

| Group | Contains |
|---|---|
| Ingestion | OT gateway (boundary), connectors, data contracts, streams |
| Storage | Shared and zoned: object store (object-store contract, [ADR-0007](../adr/0007-object-store-contract-bindings.md)), tables. Per environment: operational database, indexes (vector, feature), predictions |
| Data management | Catalog, query engine, lineage, quality, env zones, classification, retention + tiering, access policy |

Zone rules:
- curated zone: writable only by the prod orchestration identity
- nonprod: reads curated/raw per classification; writes only to its own sandbox
- every cross-zone grant is audited

Catalog stays in data management — it IS the data access path (accepted asymmetry).

### Per-tenant, cross-environment bands

| Band | Contains | Rule |
|---|---|---|
| Registries | Source repo, artifact repo, model registry, experiments | The only handoff seam. Immutable, versioned; CI/CD alone moves an entry into a runtime. ([ADR-0004](../adr/0004-registries-only-handoff.md)) |
| Trust services | Identity (human, workload, device), secrets, keys, admission, audit trail, network policy | Exist once per tenant; consumed, never re-implemented. |
| Operation services | CI/CD, observability (+ outbound log shipper), synthetics, incidents/SLOs, scanning, backup + DR, metering | Exist once per tenant; consumed, never re-implemented. |

## Sync layer (boundary between tenant and edge) — [ADR-0003](../adr/0003-generic-sync-layer.md)
Message transport · Artifact transfer · Offline queue · Traffic priority per siteClass.
Neither plane holds an address of a service in the other.

## Edge plane — optional, per site

The edge plane brings inference to where the data is born: plants and
sites that may lose connectivity for days. It adds to serving, never
replaces it — the tenant plane's serving area always runs inference; a
site additionally scores locally when latency or a dead WAN demands it.
Both runtimes consume the same promoted models from the tenant's model
registry, in per-target variants (quantized bundles for edge). Training,
retraining and batch scoring stay in the tenant plane, always.

A site is one deployment of this plane at one location, classed by
siteClass (connected | remote).
The site is only what Kyper deploys: customer systems at the same
location are externals, not parts of the site, even though the site reads
them locally (trust rule 4).

| Area | Contains | Rule |
|---|---|---|
| Inference runtime | Inference, preprocess/filter, store-and-forward, local alerting | Alerting is a replica: acks sync upward, tenant alerting authoritative ([ADR-0010](../adr/0010-alerting-authority.md)). |
| Site management | Update agent, device identity + attestation, time sync, network services | Always present when edge is deployed. |
| Application *(optional)* | Operator UI, local API | Deployed only at some sites. |
| Orchestration *(optional)* | Local schedules, buffer flush | Schedules only what must survive disconnection. |

Edge never trains, never holds the catalog. Store-and-forward is the one
intentional co-location of state and behaviour outside the data layer.

## Contracts (the seam pattern)

Every handoff is governed by a contract rather than by convention: a data
contract at ingestion, a model contract as a registry entry, a deploy
contract verified by admission. Each is enforced by a named component, and
a breaking change is always a new version. Detail in
[crosscutting concepts](arc42/08-crosscutting-concepts.md).

## Accepted costs

These are deliberate trade-offs, not oversights. Each is acceptable only
because a named control holds it in place — and a security or compliance
review will ask for evidence that the control actually operated, not that
it exists. So each row names both. A row whose evidence column is open is
a gap until the target is set, not an accepted cost.

| Accepted cost | What makes it acceptable | Evidence |
|---|---|---|
| The analytical stores are shared across environments ([ADR-0006](../adr/0006-shared-zoned-data-layer.md)) | Zoning: the curated zone is writable only by the prod orchestration identity; nonprod writes only its own sandbox; access policy enforces on the catalog, the query engine and the operational database. Operational and online stores are per environment, so they are not exposed at all | Cross-zone grant log in the audit trail; scenario [Q-03](arc42/10-quality-requirements.md) |
| Therefore one failure domain spans environments, for the analytical stores | Managed object storage for cloud tenants; catalog and query engine stay self-run | Per-store DR posture ([ADR-0014](../adr/0014-data-layer-storage-layers.md), proposed). **Open:** RPO/RTO per tenant class ([Q-06](arc42/10-quality-requirements.md)) |
| One query engine serves the prod application and nonprod exploration | Workload isolation between the two | **Open:** isolation target not yet set ([Q-07](arc42/10-quality-requirements.md)) |
| No formal stage environment ([ADR-0005](../adr/0005-two-environments.md)) | Full-scale rehearsal is a nonprod run against curated data, read-only | Nonprod cannot write curated by construction (same control as row 1) |

The compliance reading of these rows — which criterion each answers, and
what an auditor would be shown — belongs in
[risks and technical debt](arc42/11-risks-and-technical-debt.md).

## Open decisions
- Request-response vs batch inference (blocks online feature path) — oldest open fork
- Semantic layer above query engine (only if >1 consumer defines same KPI)
- Business continuity and disaster recovery — TBD, not yet addressed:
  availability targets per stateful component; RPO/RTO per tenant class;
  whether geographically resilient hosting is offered; and the interval at
  which recovery plans are tested. Until these exist, the resiliency
  questions in a customer security review have no answer.
- Tenant lifecycle in the control plane (KYP-C-FLEET-04, `status 'gap'`) —
  provision, suspend, and offboard. Offboarding must cover data export,
  secure deletion of customer data across every store and backup, and a
  published exit procedure a customer can be shown; none of it exists yet.
- Analyst workspace (own area vs a home inside dev workspace)
- Control-plane residency. Today one control plane serves all tenants.
  That is defensible because it holds no customer data (REQ-KYP-C-07):
  only desired state, signed releases and health summaries. The open
  question is whether a jurisdiction forces a split anyway — a customer
  contract demanding in-country metadata, transfer rules catching audit
  or consent records, or critical-infrastructure rules covering the plant
  locations stored in the tenant registry. If triggered, the prepared
  shape is: tenant registry and fleet health per jurisdiction, golden
  artifacts global or mirrored. Distance and latency are not triggers —
  the control plane sits in no runtime path.
- Federated learning across tenants (future option; keep compatible, do not build)

## Standards to map against (see [docs/analysis-plan.md](analysis-plan.md))
ISO/IEC 23053 (vocabulary), ISO/IEC 5338/42001/23894/5259, CNCF CNAI + Data-on-K8s AI
whitepaper, AWS Well-Architected ML Lens + SaaS Lens, Google MLOps practitioners guide,
IIC IIRA v1.10 (tiers, gateway pattern = sync layer), IEC 62443 zones/conduits, OpenInfra
Edge-AI whitepaper (already applied: site management, local preprocessing and alerting,
traffic priority per siteClass).
