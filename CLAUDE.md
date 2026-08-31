# Kyper architecture repo — instructions for Claude Code

## What this repo is
Source of truth for the Kyper platform architecture: element taxonomy, LikeC4
model, ADRs, arc42 narrative. CI renders and publishes a static site. Notion is
a portal that only LINKS here; Linear holds tasks. This repo never writes to
either.

## Read first, in this order
1. docs/design-brief.md      — the architecture (v13) and every decision behind it
2. architecture/taxonomy.md  — kinds, relation kinds, axes, KYP-ID scheme
3. adr/                      — accepted decisions; never re-open one without a new ADR
4. docs/analysis-plan.md     — the standards-conformance work plan (Linear project)

## Hard rules
- Model files may use only kinds and relation kinds declared in
  architecture/model/spec.likec4. Adding a kind requires an ADR first.
- Product names (S3, GCS, MinIO, Keycloak, Argo, Airflow...) NEVER appear in
  architecture/model/. They live in architecture/bindings/*.yaml keyed by
  KYP-ID x tenant class. The model states contracts, not products.
- Environments (nonprod, prod), tenants and site classes are AXES expressed as
  metadata — never elements, never duplicated subtrees.
- Every element carries metadata.kypId (unique). Every structural change cites
  an ADR id in metadata.adr on the affected element(s).
- One authoring surface per fact: model/decision facts here; analysis findings
  in Notion; tasks in Linear. Other tools link, never restate.
- A new kind of store is a KIND only if its boundary rule differs (see
  registry). Different technology = metadata.class, not a kind.
- Run the gate before proposing any commit:
    npx likec4 build architecture/model -o site   &&   python3 scripts/check_adr_links.py
- LikeC4 syntax and CLI flags change between versions. Before using any
  construct not already present in this repo, verify it at https://likec4.dev/docs
  and pin the likec4 version in package.json.

## Placement rules (the architecture's consistency principles)
1. State lives in the data layer; behaviour lives above it. Serving and
   application hold no durable state.
2. Every producer-to-runtime handoff goes through a registry (model registry,
   artifact repo, catalog for data). No direct paths.
3. Every trust boundary is a named component: OT gateway (in), public ingress
   (out), sync layer (edge), staff federation (control plane).
4. Cross-cutting concerns (identity, secrets, keys, audit, admission, backup,
   metering, network policy) exist once, in platform bands, and are consumed —
   never re-implemented inside an area.
5. One scheduler per tenant environment; edge schedules only what must survive
   disconnection. Edge never trains, never owns the catalog.
6. Environments are instances of the environment container, not components.

## Rejected options — do not propose these again
- three environments (dev / stage / prod)          -> ADR-0005
- dev space and ML space as sibling subsystems     -> ADR-0008 (profiles of one workspace)
- source repo / artifact repo / model registry inside a space -> ADR-0004
- product names at component level                 -> ADR-0007
- "message broker" as the named edge boundary      -> ADR-0003 (generic sync layer)
- CI writing registers or diagrams into Notion     -> ADR-0009

## Working conventions
- Branch per Linear issue: KYP-<n>-<slug>. PR description names the finding
  row or ADR it resolves.
- New decision: copy adr/template.md to adr/NNNN-title.md, status "proposed";
  flip to "accepted" in the merging PR. Add the affected KYP-IDs to `affects:`.
- Diagrams are views in architecture/model/views/. Never hand-draw a diagram
  that the model can render.
- Keep docs/design-brief.md accurate: it is the narrative the portal links to.
