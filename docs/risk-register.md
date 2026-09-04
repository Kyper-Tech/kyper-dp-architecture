# Risk register — accepted architectural risks

The accepted costs in the [design brief](design-brief.md#accepted-costs)
are risks the architecture carries on purpose. This register is what the
risk owner signs for each one: the risk, the treatment chosen, the controls,
what remains after them, the conditions under which the acceptance holds,
and when it is reviewed. An entry is **accepted** only when signed with all
conditions met; **accepted with conditions outstanding** when signed on the
design while a named condition is still open; **open** otherwise.

Review cadence for every entry: annually, and on any listed trigger. A
trigger review may confirm, tighten, or withdraw the acceptance; withdrawal
invokes the entry's fallback.

Owner for all entries: **the CTO**. Signature and date are recorded per
entry below when the acceptance is made.

---

## RISK-01 — Shared analytical stores: environment separation by authorization only

**Risk.** The analytical stores (object store, tables) are shared across
environments. Non-production workloads can reach the shared bucket that
holds production data. Separation is authorization, not network: a
compromised mediator (catalog or query engine) or a defect in scope
evaluation exposes the whole bucket to non-production.

**Source.** [ADR-0006](../adr/0006-shared-zoned-data-layer.md).

**Treatment.** Mitigate and accept the residual. Avoidance is available and
kept live as the fallback.

**Controls.**
- Zoning: curated writable only by the prod orchestration identity;
  nonprod writes only its own sandbox; every cross-zone grant audited.
- Every read of shared data is mediated; no workload holds standing
  permission on a shared store; credentials are short-lived and scoped per
  request to the effective grant (instance ceiling ∩ user grant).
- Operational and online stores are per environment and not exposed.
- The gate rejects any modeled relation from an env-scoped area straight
  to a shared store.

**Residual.** Mediator compromise or scope-evaluation defect exposes the
entire shared bucket to non-production. Blast radius: the bucket.

**Conditions of acceptance.**
1. The mediator is hardened and under privileged-access review.
2. Change control on the scope-evaluation logic, with review records.
3. Credential lifetimes and revocation measured and reported.
4. The audit trail can answer directly: *did any non-production identity
   ever read production-only objects?*
5. The cross-zone grant log is retained for the compliance scope.

**Fallback.** Per-environment analytical stores for a tenant class or a
contract that requires physical separation; the class rule permits it at
the cost of a second lakehouse per tenant.

**Triggers.** Mediator security incident; a customer contract requiring
physical separation; an audit finding on environment separation; a new
jurisdiction; any change to the scope-evaluation logic.

**Status.** Open — awaiting signature.
**Accepted by:** ______ (CTO) **Date:** ______ **Next review:** ______

---

## RISK-02 — One failure domain across environments for the analytical stores

**Risk.** Because the analytical stores are shared, a failure there affects
both environments at once. Cloud tenants inherit managed durability for
object storage; on-prem tenants and the self-run components (catalog,
query engine) carry the failure domain without it.

**Source.** [ADR-0006](../adr/0006-shared-zoned-data-layer.md),
[ADR-0014](../adr/0014-data-layer-storage-layers.md) (proposed).

**Treatment.** Mitigate and accept the residual.

**Controls.**
- Managed object storage for cloud tenant classes.
- A declared DR posture per store — primary or derived — with backup
  following the posture (REQ-KYP-T-OPS-03).
- Derived stores rebuildable from curated plus lineage.

**Residual.** Recovery is unquantified: no RPO or RTO per tenant class, so
neither the loss window nor the time to recover is a commitment. On-prem
carries the domain with no managed durability behind it.

**Conditions of acceptance.**
1. RPO and RTO set per tenant class
   ([Q-06](arc42/10-quality-requirements.md)) — **outstanding**, part of
   the BC/DR open decision.
2. Every store has a declared DR posture.
3. Restores are exercised on a stated interval, not assumed.

**Fallback.** None short of per-environment analytical stores (RISK-01's
fallback), which also splits the failure domain.

**Triggers.** Any data-loss incident; the BC/DR decision landing; a
contract stating recovery commitments; a tenant class added.

**Status.** Open — cannot be signed as fully accepted until condition 1 is
met; may be signed *with conditions outstanding* on the design.
**Accepted by:** ______ (CTO) **Date:** ______ **Next review:** ______

---

## RISK-03 — No formal stage environment

**Risk.** Releases are rehearsed in non-production against curated data,
read-only, rather than in a dedicated stage. Rehearsal proves only as much
as non-production resembles production; a defect that manifests only under
production shape, scale or configuration reaches production untested.

**Source.** [ADR-0005](../adr/0005-two-environments.md).

**Treatment.** Mitigate and accept the residual. Avoidance available per
contract.

**Controls.**
- Full-scale rehearsal against real curated data, read-only.
- Non-production cannot write curated by construction (RISK-01's zoning).
- Stage available as configuration for a tenant whose contract demands it
  (ADR-0005).

**Residual.** Production-only conditions — scale, configuration drift
between environments — are untested before release.

**Conditions of acceptance.**
1. Non-production tracks production shape: configuration parity is
   evidenced, and drift between the environments is monitored.
2. The rehearsal is a release-gate step, recorded per release.

**Fallback.** A stage environment by configuration, per contract, at the
cost ADR-0005 avoided.

**Triggers.** A production incident attributable to environment
divergence; a contract requiring a formal stage; a change to the
environment count.

**Status.** Open — awaiting signature.
**Accepted by:** ______ (CTO) **Date:** ______ **Next review:** ______
