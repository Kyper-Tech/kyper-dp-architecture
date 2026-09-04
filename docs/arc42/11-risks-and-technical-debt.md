# 11. Risks and Technical Debt

The trade-offs themselves, with their controls and evidence, are in the
[accepted costs](../design-brief.md#accepted-costs) table. What follows is
what is not yet settled. Most are commitments to enforce when the
components are built, not defects failing today.

## Accepted residual risk

- **Shared object storage is separated between environments by
  authorization only.** The bucket is reachable from non-production; no
  workload holds standing permission and every access is scoped per request
  and audited, but a compromised mediator or a scope-evaluation defect
  exposes the whole bucket. Accepted knowingly
  ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md)) — **Risk owner: the CTO.** Conditions that keep it acceptable: the mediator's own
  hardening and change control, and an audit trail that can answer "did any
  non-production identity ever read production-only objects". Escape valve:
  per-environment analytical stores for a tenant class or contract that
  requires physical separation.

## To be addressed

- **Recovery targets for self-run stores.** Managed object storage carries
  its own durability for cloud tenants. The catalog, the operational
  database, the indexes and the whole on-prem case have no RPO or RTO.
  Open: [Q-06](10-quality-requirements.md).
- **Query-engine isolation.** No query engine exists yet. When one is
  introduced, production application queries and nonprod exploration must
  be isolated, with a stated target.
  Open: [Q-07](10-quality-requirements.md).
- **Raw-zone reads from the ML and data workspaces.** Model and pipeline
  development need real data, so the audited-grant machinery is the
  control, not a formality. It has to exist when the workspaces do
  ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md),
  [ADR-0012](../../adr/0012-split-dev-ml-workspaces.md),
  [ADR-0015](../../adr/0015-data-engineering-workspace.md)).
- **Audit-trail integrity.** The object-store contract now requires
  immutability, but storage immutability alone is not tamper evidence: the
  audit trail (KYP-T-TRUST-05) must be append-only and verifiable in its
  own right, because it is what evidences that the zoning controls
  operated.

## Declared gaps

- **Tenant lifecycle** — KYP-C-FLEET-04 carries `status 'gap'`, and
  REQ-KYP-C-06 has no requirements yet. It must cover provision, suspend,
  offboard with data export, secure deletion across every store and
  backup, and a published exit procedure.
- **Business continuity and disaster recovery** — no policy, no
  availability targets, no statement on geographically resilient hosting,
  and no test interval. Until these exist the resiliency questions in a
  customer security review have no answer. Open decision in the
  [design brief](../design-brief.md#open-decisions).

Findings from the standards conformance work are classified and tracked per
the [analysis plan](../analysis-plan.md); this section carries only what the
architecture itself leaves open.
