---
id: ADR-0009
status: proposed
date: 2026-08-31
affects: []
---
# Taxonomy + arc42 + LikeC4 model-as-code, validated and published by CI
## Context
Diagrams and decisions drift when they are drawn by hand and stored apart from
the model. A non-git audience (business, DS) also needs to reach the narrative.
## Decision
Git is the single authoring surface for the model, the decisions and the
narrative. CI validates them and publishes a static site, which is how the
non-git audience reads them. Linear holds tasks and cites the ADR or
requirement it implements.

No external tool holds a copy of anything authored here. If a portal is
introduced later, it links to the published site and never mirrors it; that
choice is a separate decision.
## Consequences
No custom sync code, and no second place where a fact can go stale. The
published site carries the whole narrative, so it has to stay readable on
its own.
## Rejected alternatives
CI writing registers or diagrams into an external portal via API: no native
sync, so it drifts.
