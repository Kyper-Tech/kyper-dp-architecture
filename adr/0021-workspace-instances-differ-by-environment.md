---
id: ADR-0021
status: proposed
date: 2026-08-31
affects: [KYP-T-DEVWS, KYP-T-MLWS, KYP-T-DATAWS, KYP-T-DATA-25]
---
# Workspace instances differ per environment in purpose and grants, not in size

## Context
Workspaces are environment-scoped, but nothing says what distinguishes one
environment's instance from another's. Read as copies differing only in
quota, a production workspace is pointless: model development does not need
one, since a model is developed once and promoted through the registry to
nonprod serving and then to prod serving
([ADR-0004](0004-registries-only-handoff.md)).

The production instance exists for a different reason. Someone has to
operate on production — investigate a failing pipeline, inspect production
data, run a corrective job — and that needs elevated grants that
development must not have.

## Decision
Workspace instances are environment-scoped and differ by purpose:

- **nonprod instance — development.** Model development, pipeline
  development, application development. Reads per
  [ADR-0006](0006-shared-zoned-data-layer.md); writes only to its own
  sandbox. No production writes of any kind.
- **prod instance — production operation.** Investigating and correcting
  production work, with elevated grants including writes where the user's
  identity permits. Not a development environment: model and pipeline
  development do not happen here.

Grants are per user, not per instance. Two users in the same instance may
hold different scopes; the instance sets the ceiling, the grant sets the
actual scope.

The curated-zone rule is unchanged and the prod instance is not a way
around it: curated stays writable only by the prod orchestration identity.
A curated change is made by promoting a pipeline, or under a break-glass
grant that is named, expiring and audited (KYP-T-DATA-25,
KYP-T-TRUST-05) — never by a user writing curated directly from a
workspace.

## Consequences
- The production workspace is a privileged surface and needs the tightest
  access review of any workspace; it is where a security review will look
  first.
- Break-glass is now an explicit, audited path rather than an informal
  one, which is what makes elevated production access defensible.
- Development and production operation cannot be conflated: a developer
  cannot acquire production write capability by moving work into a
  workspace, because the instance sets the ceiling.
- Access review has to cover both the instance ceiling and the per-user
  grants, since either alone tells only half the story.

## Rejected alternatives
- Workspace instances as identical copies differing by quota: makes the
  production instance pointless and hides the grant difference that is the
  real reason to have one.
- One cross-environment workspace: leaves production operation with no home
  and forces either a permanently elevated single workspace or ad-hoc
  access outside the architecture.
- Allowing direct curated writes from the production workspace: destroys
  the single-writer rule that the environment boundary rests on.
