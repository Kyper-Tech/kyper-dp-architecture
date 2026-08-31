# Taxonomy — v1 (changing this file requires an ADR)

## Element kinds
Two levels. Groupings (plane, area) organize and own no runtime identity.
Components (service, store, registry, boundary) are the leaf elements that
exist at runtime. "Component" is the collective term for the leaf kinds —
it is not a kind itself. external is neither: it is an outside actor.

- plane    — top-level operational domain with its own trust posture and instancing rule
             (control, tenant, edge). Exactly three exist.
- area     — grouping of components inside a plane sharing ONE boundary rule and one
             interface discipline. Owns no runtime identity. Criteria: exactly one stated
             boundary rule; interacts with other areas only via declared relation kinds;
             appears in exactly one plane. Not areas: environments, site classes (axes),
             sync layer (boundary).
- service  — behaviour without durable state (serving, gateways, schedulers, catalog service).
- store    — durable state in the data layer. Flavours via metadata.class, never new kinds.
- registry — immutable, versioned handoff store between producers and runtimes. A kind (not a
             store flavour) because its boundary rule differs: write-once entries, read by
             CI/CD only, promotion by stage transition.
- boundary — a named trust/coupling seam (OT gateway, public ingress, sync layer, staff
             federation). Both sides may reference it; neither side references the other.
- external — customer-owned or third-party system the platform integrates with.

## Relation kinds
- publishesTo  — producer writes a versioned artifact/record into a registry or store
- readsVia     — consumer reads state through a mediating service (catalog, query engine)
- servesTo     — runtime consumes a promoted artifact from a registry
- syncsWith    — exchange across a boundary (async, both directions, no service addresses)
- enforces     — policy/gate applied to a target (admission -> runtimes, access policy -> stores)
- schedules    — orchestrator triggers work in a target

## Axes (metadata, NEVER elements)
- env        ∈ {nonprod, prod}
- tenantClass ∈ {cloud-gcp, cloud-aws, onprem}
- siteClass  ∈ {connected, remote}

## Controlled metadata vocabularies
- store.class ∈ {analytical, operational, online}
  analytical = catalog-mediated read; operational = owned by exactly one application;
  online = low-latency serving reads
- optional ∈ {true} — component deployed only at some sites (edge)

## ID scheme
KYP-<plane>-<AREA>-<nn>   plane ∈ {C, T, E}; AREA is the area slug; nn two digits.
Area-level IDs omit nn (KYP-T-DATA). IDs are immutable; renames keep the ID.
The KYP-ID is the join key across model, ADRs, Notion registers and Linear issues.

## Placement rules
See CLAUDE.md "Placement rules" — normative here by reference.
