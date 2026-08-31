# Kyper platform architecture — design brief (v13, 2026-08-31)

Component level, capability names only. Products are bindings, not components.

## Planes
| Plane | Instances | Operated by | Network direction |
|---|---|---|---|
| Control | 1 | Kyper | never initiates into a tenant |
| Tenant | one per customer | Kyper-managed, customer-owned data | pulls from control |
| Edge | 0..N per tenant, per site | tenant plane | exchanges with tenant only via sync layer |

Pull-only downward. No inbound path from control plane into a tenant. (ADR-0001, ADR-0002)

## Control plane (thin by design; SaaS-lens analysis pending)
Fleet config (tenant registry + desired state) · Artifact registry (golden, signed, SBOM) ·
Release control · Staff identity federation · Fleet health aggregation · Tenant lifecycle (GAP).
Tenant registry carries: tenant class -> storage substrate -> availability posture; site
connectivity classes; enabled modules; version pins.

## Tenant plane
### Environment container — instantiated as nonprod and prod (ADR-0005)
Holds: Workspaces, Serving, Application, Orchestration.

Workspaces (one subsystem, profiles dev / ML; analyst profile later) — ADR-0008
  Sessions · Jobs · Environments (pinned images) · Scratch runtime
  Profile differences are policy only: data scope, publish target, compute quota.
  Spaces hold nothing durable (ADR-0004).
Serving — Model runtime · Retrieval · Inference gateway · Drift monitor (stateless)
Application — App runtime · API gateway · Alerting (authority) · Public ingress
Orchestration — Ingest · Transform · Scoring · Retraining trigger · Idle scale
  (one scheduler per environment; owns all recurring work incl. scale-to-zero)

### Data layer — shared across environments, zoned (ADR-0006)
Ingestion — OT gateway (boundary) · Connectors · Contracts · Streams
Storage — Object store (S3-compatible contract, ADR-0007) · Tables · Operational database ·
          Indexes (vector, feature) · Predictions (env-labelled)
Data management — Catalog · Query engine · Lineage · Quality · Env zones ·
          Classification · Retention + tiering · Access policy
Zone rules: curated zone writable only by prod orchestration identity; nonprod reads
curated/raw per classification, writes only its sandbox; every cross-zone grant audited.
Catalog stays in data management (it IS the data access path) — accepted asymmetry.

### Per-tenant, cross-environment bands
Registries (the only handoff seam) — Source repo · Artifact repo · Model registry ·
  Experiments/evaluation records. Immutable, versioned. CI/CD is the only actor that
  moves a registry entry into a runtime.
Trust services — Identity (human, workload, device) · Secrets · Keys · Admission ·
  Audit trail · Network policy
Operation services — CI/CD · Observability (+ outbound log shipper) · Synthetics ·
  Incidents/SLOs · Scanning · Backup + DR · Metering

## Sync layer (boundary between tenant and edge) — ADR-0003
Message transport · Artifact transfer · Offline queue · Traffic priority per link class.
Neither plane holds an address of a service in the other.

## Edge plane — optional, per site
Runtime — Inference · Preprocess/filter · Store-and-forward · Local alerting (replica; acks
  sync upward, tenant alerting authoritative — ADR-0010)
Site services — Update agent · Device identity + attestation · Time sync · Network services
Optional (dashed) — Application (operator UI, local API) · Orchestration (local schedules,
  buffer flush). Edge never trains, never holds the catalog. Store-and-forward is the one
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
- Analyst workspace profile
- Federated learning across tenants (future option; keep compatible, do not build)

## Standards to map against (see docs/analysis-plan.md)
ISO/IEC 23053 (vocabulary), ISO/IEC 5338/42001/23894/5259, CNCF CNAI + Data-on-K8s AI
whitepaper, AWS Well-Architected ML Lens + SaaS Lens, Google MLOps practitioners guide,
IIC IIRA v1.10 (tiers, gateway pattern = sync layer), IEC 62443 zones/conduits, OpenInfra
Edge-AI whitepaper (applied in v13: site services, local preprocessing/alerting, traffic priority).
