---
id: ADR-0006
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA, KYP-T-DATA-03, KYP-T-DATA-04, KYP-T-DATA-07, KYP-T-DATA-22, KYP-T-DATA-25]
---
# One data layer: sharing follows store class, access follows purpose

## Context
Copying the whole data layer per environment multiplies per-tenant cost and
is unnecessary for most of it. But "one shared data layer" overstates the
case: an application's operational state and the stores that serve runtimes
are shared with nothing. Separately, a customer security review asks
directly whether production data is used in non-production (CAIQ DG-06.1,
ISO/IEC 27001 A.8.33), and that question is about testing software — not
about the analytics the customer engaged us to perform.

## Decision

### Sharing follows store.class
- analytical (object store, tables) — one shared instance, zoned. Not
  copied per environment; this is where the cost argument applies.
- operational (application database) — one instance per environment.
- online (indexes, feature and vector stores, predictions) — one instance
  per environment, since they serve per-environment runtimes.
- timeseries — the primary takes ingestion writes, consumers read through
  a read-only path, and nonprod writes go to a separate instance. Which
  topology provides that is a binding decision, not a model element.

`shared` metadata therefore belongs on individual stores, never on the
data layer as a whole.

### Zones, in the shared analytical stores
raw, curated, and one sandbox per environment.
- curated is writable only by the prod orchestration identity
- nonprod writes only to its own sandbox
- every cross-zone grant is audited

### Access follows purpose, not environment
1. **Analytics and model development on the tenant's own data** is what the
   platform is for. It uses real curated and raw data, governed by
   classification and audited grants
   ([ADR-0012](0012-split-dev-ml-workspaces.md),
   [ADR-0015](0015-data-engineering-workspace.md)). Synthetic data is not a
   substitute: a model for this customer's plant cannot be developed on
   invented values.
2. **Developing and testing the platform's own software** is a different
   purpose and does not need real customer data. It uses synthetic data or
   masked derivatives carrying no re-identifying fields. Real production
   data for this purpose requires customer consent naming the datasets,
   stating the purpose and carrying an expiry, recorded in the tenant
   registry with every access audited.
   - Serving and pipeline development: synthetic; where a real read is
     unavoidable it is read-only against an immutable source.
   - Application development: a masked dump into that environment's own
     operational database; unmasked only under consent.

### Limits that hold regardless
- Nonprod never writes the curated zone.
- Development reads are read-only against sources that cannot be modified
  — the same principle as the object store's immutability row and the
  time-series read path.
- Data under consent stays in the tenant plane, is not copied to another
  environment or tenant, and is deleted when the consent expires.

## Consequences
- The environment boundary is authorization correctness rather than
  infrastructure; the cross-zone grant log is the standing evidence.
- The shared failure domain covers the analytical stores only. Managed
  object storage mitigates it for cloud tenants; catalog, query engine and
  the rest stay self-run.
- The query engine needs workload isolation between the prod application
  and nonprod exploration.
- DG-06.1 has a precise answer: production data serves the analytics the
  customer engaged us for, and is not used to test our software except
  under the customer's documented, expiring authorization.
- Someone must produce and maintain the synthetic and masked datasets.
  Without them the default is unusable, consent becomes routine, and the
  exception turns into a habit.
- The tenant registry record
  ([ADR-0013](0013-tenant-registry-record-schema.md)) grows a consents
  section.

## Rejected alternatives
- Copying the analytical stores per environment: multiplies per-tenant
  cost, which this decision and [ADR-0005](0005-two-environments.md) exist
  to avoid.
- Treating the whole data layer as shared: false for operational and
  online stores, and it answers DG-06.1 with a bare "yes".
- Synthetic data for model development: not a substitute for real plant
  data, and it would forbid the platform's own purpose.
