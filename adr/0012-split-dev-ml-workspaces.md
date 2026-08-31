---
id: ADR-0012
status: proposed
date: 2026-08-31
affects: [KYP-T-DEVWS, KYP-T-MLWS]
---
# Dev and ML are separate workspace areas

## Context
A single workspace subsystem with dev/ML profiles was considered, on the
premise that both share one anatomy (sessions, jobs, environment images,
scratch) and differ only in policy: data scope, publish target, compute
quota. The premise does not hold: the two user groups run different tooling
and different end-to-end processes — dev is build/test-centric (IDE
sessions, build pipelines), ML is experiment-loop-centric (notebook
sessions, GPU pools, experiment tracking). By the taxonomy's area test
(one area = one boundary rule) they carry different boundary rules, not one
rule with two quotas.

## Decision
Two sibling areas in the tenant plane's environment container:

- Dev workspace (KYP-T-DEVWS) — boundary rule: ephemeral, nothing durable;
  hands off exclusively to source/artifact registries; curated-zone data
  scope only.
- ML workspace (KYP-T-MLWS) — boundary rule: ephemeral, nothing durable;
  hands off exclusively to model registry and experiments; classified/raw
  reads under audited grants.

Registries remain the only producer-to-runtime handoff (ADR-0004).
Tooling differences stay out of the model — they are bindings.

## Consequences
- The ML raw-read trust difference is a named boundary between areas, not
  an intra-area policy nuance — cleaner to defend in security reviews and
  maps directly to SOC 2 CC6.1 least-privilege argumentation.
- Two anatomies to operate (sessions, jobs, images, scratch twice); a
  future analyst audience needs an explicit home rather than a cheap
  profile.
- The genuinely common parts (image pinning, scratch lifecycle) can drift
  between the two areas; keeping them aligned is an ops-band concern, not a
  structural guarantee.

## Rejected alternatives
- One workspace subsystem with dev/ML profiles: fails the area test — the
  publish targets and data scopes are two boundary contracts, and the
  raw-read trust delta hides inside a single area's policy.
- Different products per profile inside one area: does not address the
  differing handoff targets and data scopes.
