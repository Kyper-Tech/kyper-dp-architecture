---
id: ADR-0009
status: accepted
date: 2026-08-31
affects: []
---
# Taxonomy + arc42 + LikeC4 model-as-code + CI render gate; Notion links, never mirrors
## Context
Diagram/decision drift; non-git audience (business, DS) needs discoverability.
## Decision
Git is the authoring surface for model, decisions, narrative. CI validates and publishes a
static site. Notion is a portal (narrative pages, findings register, links); Linear holds
tasks. Coarse stable facts may be summarized in Notion with a source link and as-of date;
fine-grained volatile facts are reference-only.
## Consequences
No custom sync code. Portal updated as part of the ADR-merge ritual.
## Rejected alternatives
CI writing registers/diagrams into Notion via API (no native sync -> drift).
