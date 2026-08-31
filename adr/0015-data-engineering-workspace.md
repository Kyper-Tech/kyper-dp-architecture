---
id: ADR-0015
status: proposed
date: 2026-08-31
affects: [KYP-T-ORCH, KYP-T-REG-02]
---
# Data engineering gets its own workspace and a modeled pipeline promotion path

## Context
Data engineering half-exists in the architecture: its runtime (the
orchestration scheduler), and its machinery (connectors, contracts,
quality) are modeled, but the practice is not. Nowhere to develop
pipelines: by the boundary-rule test (ADR-0012), a data engineer publishes
to source/artifact repos (like dev) while reading raw data under audited
grants (like ML) — a third distinct rule that neither existing workspace
admits. And no registry edge feeds the scheduler: pipelines reach their
runtime by an unmodeled path, violating registries-only handoff (ADR-0004)
exactly as the app-runtime path does.

## Decision
1. A third workspace area in the environment container:
   Data workspace (KYP-T-DATAWS) — boundary rule: ephemeral, nothing
   durable; hands off only to source and artifact repos (pipeline code,
   transform images, contract and quality-rule definitions); reads raw and
   curated under audited grants, for pipeline development only.
   Anatomy mirrors the other workspaces: sessions, pipeline build/test
   jobs, environment images, scratch.
2. The pipeline promotion path is modeled: promoted pipeline artifacts flow
   from the artifact repo (KYP-T-REG-02) to the orchestration scheduler via
   servesTo, closing the ADR-0004 gap for pipelines. Contract and quality
   definitions ride the same path — versioned artifacts, never edited live.

## Consequences
- Three workspace anatomies to operate; the ADR-0012 consequence
  ("a future analyst audience needs an explicit home") now has a pattern:
  each audience with a distinct boundary rule gets an area, and the
  analyst decision (open in the brief) should reuse it.
- The scheduler becomes a runtime in the taxonomy-role sense: it consumes
  promoted entries; live-edited DAGs are structurally impossible.
- Raw-read grants extend to a second workspace; the audited-grant machinery
  (access policy, audit trail) covers both identically.

## Rejected alternatives
- Fold into ML workspace: wrong publish target (model registry is closed
  to pipeline artifacts by ML's own boundary rule).
- Fold into dev workspace: wrong data scope (curated-only forbids
  raw -> curated pipeline development).
- Widen dev workspace's rule to cover both: recreates the one-area,
  two-rules ambiguity that ADR-0012 removed.
