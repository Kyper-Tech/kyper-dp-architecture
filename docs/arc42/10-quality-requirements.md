# 10. Quality Requirements

Quality requirements are measurable scenarios: stimulus -> required
response -> measure, anchored to KYP-IDs. The quality tree's roots are the
five goals in [§1](01-introduction-and-goals.md); functional requirements
live per area in [docs/requirements/](../requirements/README.md). Where a
requirement varies by tenant class, that is a column — never a copied row.

## Scenarios

| ID | Anchors | Stimulus | Required response | Measure |
|---|---|---|---|---|
| Q-01 | KYP-E-RT, KYP-T-SYNC-01 | Edge site loses WAN | Inference and local alerting continue; telemetry buffered; alert state reconciles on reconnect ([ADR-0010](../../adr/0010-alerting-authority.md)) | survives N days disconnection (N per contract); zero acks lost |
| Q-02 | KYP-C | Control-plane compromise | No access into any customer environment or data ([ADR-0001](../../adr/0001-plane-structure.md)) | credentials reachable from control plane into tenants: zero |
| Q-03 | KYP-T-DATA-22, KYP-T-DATA-25 | Nonprod identity attempts curated-zone write | Denied and audited ([ADR-0006](../../adr/0006-shared-zoned-data-layer.md)) | unauthorized cross-zone writes: zero; every grant in audit trail |
| Q-04 | KYP-T-DEVWS, KYP-T-MLWS, KYP-T-DATAWS | Workspace instance lost | Rebuild from registries + images | loss limited to uncommitted work ([ADR-0004](../../adr/0004-registries-only-handoff.md)) |
| Q-05 | KYP-T-REG, KYP-T-TRUST-04 | Unsigned or unevaluated artifact submitted for deployment | Rejected by admission | unsigned artifacts reaching a runtime: zero |
| Q-06 | KYP-T-DATA | Store failure | Recovery per the store's declared primary/derived posture ([ADR-0014](../../adr/0014-data-layer-storage-layers.md), proposed) | RPO/RTO per tenant class — OPEN DECISION |
| Q-07 | KYP-T-DATA-06 | Nonprod exploration load spike | Prod application queries unaffected | query engine workload isolation — target TBD |
| Q-08 | KYP-S | Common-services compromise | Reach bounded to opted-in tenants' work in flight; tenants that declined are untouched ([ADR-0023](../../adr/0023-common-services-plane.md)) | blast-radius statement — OPEN, with the isolation design |

## Open

- Availability targets per stateful component; RPO/RTO per tenant class
  (Q-06) — open decisions in the [design brief](../design-brief.md#open-decisions).
- Further scenarios derived in the ML Lens review
  ([analysis plan](../analysis-plan.md), phase 3).
