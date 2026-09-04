# 6. Runtime View

> Skeleton — to be filled with LikeC4 dynamic views once the scenarios are
> chosen. Candidate scenarios:

1. Data contract violation at ingestion → quarantine
   ([design brief — contracts](../design-brief.md#contracts-the-seam-pattern)).
2. Model promotion: workspace → model registry → serving runtime
   ([ADR-0004](../../adr/0004-registries-only-handoff.md)).
3. Edge disconnection and reconnect: store-and-forward, local alerting,
   ack reconciliation ([ADR-0010](../../adr/0010-alerting-authority.md)).
4. Tenant pulls a platform release from the control plane
   ([ADR-0001](../../adr/0001-plane-structure.md)).

Rule: runtime interaction semantics belong here as dynamic views — the
static model states dependencies only.
