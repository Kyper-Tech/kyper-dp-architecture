---
id: ADR-0016
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA-03, KYP-T-APP-01]
---
# Add the owns relation kind for operational stores

## Context
store.class operational is defined as "owned by exactly one application",
but no relation kind can express that access: readsVia requires a mediating
service, publishesTo means versioned records. The dependency was invisible
in every diagram (the operational database had zero relations), and an
owner metadata key proved a dead end — metadata does not render and its
endpoint is not checked.

## Decision
A seventh relation kind:

    owns : service -> store

The single owner of an operational store accesses it directly, reads and
writes, no mediation. Constraints: the target's store.class MUST be
operational; exactly one owns relation per operational store; every
operational store has one.

The owner metadata key is removed (the relation is the single surface for
this fact).

## Consequences
- Direct-access dependencies render in diagrams and are checkable
  (endpoints, cardinality) by the gate later.
- Catalog mediation stays the analytical rule; owns is scoped to
  operational stores only — it is not a general bypass.

## Rejected alternatives
- owner metadata: invisible in diagrams, endpoint unchecked.
- Stretching readsVia or publishesTo: breaks their signatures and meanings.
