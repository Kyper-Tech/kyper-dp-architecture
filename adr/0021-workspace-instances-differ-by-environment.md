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

### Credentials and authorization are separate
Sessions and jobs authenticate as a **workload identity** scoped to the
workspace instance. They never run with a user's credentials, so no human
secret reaches a runtime and a job can safely outlive the session that
started it.

Authorization is evaluated per user. The user's identity travels with the
request as context — a claim, not a credential — and the mediating service
(catalog, query engine) computes the effective scope:

    effective scope = instance ceiling ∩ the user's own grant

This is why access is catalog-mediated and direct store connections are
forbidden ([ADR-0006](0006-shared-zoned-data-layer.md)): a direct
connection carries only the workload identity, loses the user context, and
collapses every user to the instance ceiling.

Detached work has no live user. A scheduled job runs at its workload
identity's own scope, with the submitting user recorded and the data scope
fixed at submission.

The audit trail records both: which workload acted, and on whose behalf.

### The ceiling is technical, not policy
Three rules make the ceiling hold rather than merely describe it:

1. **One workload identity per workspace instance**, never shared between
   instances. Sharing one merges the ceilings.
2. **The instance's workload identity does not possess permissions beyond
   its ceiling.** A development instance holds no write permission on
   production data at all, rather than holding it and being denied by
   policy. The ceiling then survives a policy-evaluation bug, because the
   principal making the call cannot perform the operation.
3. **Humans hold no data-plane permissions.** A person's entitlements
   exist only in the access-policy layer, which the mediating service
   consults. If a human held direct permissions on a store, their session
   could act as themselves instead of as the instance's workload identity
   and step over the ceiling entirely. This is the rule the whole scheme
   rests on.

The effect: the same person, in a development instance, cannot write
production data even when entitled to write it elsewhere, because the
principal making the request has no such permission. In a production
instance the same person can, because there the workload identity does.

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
- The mediating service becomes a per-user enforcement point, not just an
  abstraction: it must accept and evaluate propagated user context, and a
  gap there silently grants every user the instance ceiling.
- Revoking a user's grant takes effect at the next mediated request, but a
  detached job keeps the scope it was submitted with until it ends.
- Provisioning must create a distinct workload identity per workspace
  instance and grant it only its ceiling; getting this wrong is silent,
  since everything keeps working while the ceiling is gone.
- Granting a person direct permissions on a store — however convenient in
  an incident — breaks the ceiling for every instance at once. Emergency
  access goes through the break-glass grant, not through a direct
  permission.

## Rejected alternatives
- Workspace instances as identical copies differing by quota: makes the
  production instance pointless and hides the grant difference that is the
  real reason to have one.
- One cross-environment workspace: leaves production operation with no home
  and forces either a permanently elevated single workspace or ad-hoc
  access outside the architecture.
- Allowing direct curated writes from the production workspace: destroys
  the single-writer rule that the environment boundary rests on.
