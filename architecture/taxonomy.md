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
             CI/CD only, promotion by lifecycle-stage transition (a registry
             stage, e.g. candidate -> promoted — not an environment; ADR-0005).
- boundary — a named trust/coupling seam (OT gateway, public ingress, sync layer, staff
             federation). Both sides may reference it; neither side references the other.
- external — customer-owned or third-party system the platform integrates with.
- band     — not a kind: shorthand for an area outside the environment
             container — instantiated once per tenant, shared across
             environments (registries, trust services, operation services).
             Recognizable by the absence of envScoped metadata.

## Relation kinds
Role nouns below (producer, runtime, mediator, orchestrator) are roles a
component plays in one relation — not kinds. The same service may be a
producer in one relation and a runtime in another.

- publishesTo  — producer writes a versioned artifact/record into a registry or store
- readsVia     — consumer reads state through a mediating service (catalog, query engine)
- servesTo     — runtime consumes a promoted artifact from a registry
- syncsWith    — exchange across a boundary (async, both directions, no service addresses)
- enforces     — policy/gate applied to a target (admission -> runtimes, access policy -> stores)
- schedules    — orchestrator triggers work in a target

## Axes (metadata, NEVER elements)
- env        ∈ {nonprod, prod}
- tenantClass ∈ {cloud-gcp, cloud-aws, onprem}
- siteClass  ∈ {connected, remote} — the ONLY term for site connectivity
  (do not write "link class" or "connectivity class")

Instances along the axes (nouns, not kinds):
- tenant      — one instantiation of the tenant plane, for one customer
- environment — one instantiation of the environment container, per env value
- site        — one instantiation of the edge plane, at one location
- fleet       — all tenants, as the control plane's object of management

## Controlled metadata vocabularies
- store.class ∈ {analytical, operational, online}
  analytical = catalog-mediated read; operational = owned by exactly one application;
  online = low-latency serving reads
- optional ∈ {true} — component deployed only at some sites (edge)
- envScoped ∈ {true} — area instantiated per environment (it is inside the
  environment container); absent = per-tenant, cross-environment (a band)
- shared ∈ {across-envs} — one instance serves all environments (data layer)
- status ∈ {gap} — declared in the architecture but not yet designed

## Zones (data layer partitions — ADR-0006)
A zone is a partition of the data layer carrying exactly one access rule.
Zones are NEVER elements. zone ∈ {raw, curated, sandbox-<env>}.
- raw      — as ingested; reads per classification
- curated  — writable only by the prod orchestration identity
- sandbox  — per-environment; the only zone nonprod may write to

## Bindings (architecture/bindings/*.yaml)
A binding answers one question: which product fulfills this component's
contract, for this tenant class?

    component (KYP-ID) x tenantClass  ->  product + posture

Terms in that formula:
- contract — the promise the component states in the model (e.g. an
  S3-compatible object API). The only thing other components may depend on.
- contract profile — the contract made explicit: `required` rows components
  may rely on, `not-relied-upon` rows they must not. A product may bind
  only if it satisfies every required row.
- product — a concrete technology fulfilling the contract. NEVER named in
  the model (ADR-0007); swapping one touches bindings + an ADR, never the model.
- posture — how the bound product is operated (managed-regional, self-run,
  self-run-operator).

Bindings are per tenant *class*; which binding applies to one concrete
tenant is resolved in the control-plane tenant registry.

## ID scheme
KYP-<plane>-<AREA>-<nn>   plane ∈ {C, T, E}; AREA is the area slug; nn two digits.
Area-level IDs omit nn (KYP-T-DATA). IDs are immutable; renames keep the ID.
The KYP-ID is the join key across model, ADRs, Notion registers and Linear issues.

## Placement rules
See CLAUDE.md "Placement rules" — normative here by reference.
