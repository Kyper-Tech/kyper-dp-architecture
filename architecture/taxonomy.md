# Taxonomy — v1 (changing this file requires an ADR)

This file defines every structural term the architecture may use, in
dependency order: a term is used only after the section that defines it,
except where an explicit (§n) reference points ahead. Domain/business
vocabulary (OT, golden, silo, air gap, ...) belongs in the arc42 glossary,
not here. "The model" means [architecture/model/](model/) (LikeC4).

## 1. Axes (metadata, NEVER elements)
An axis is a named dimension along which the one model is instantiated.
Axis values are metadata on elements; nothing is duplicated per value.

- env         ∈ {nonprod, prod}
- tenantClass ∈ {cloud-gcp, cloud-aws, onprem}
- siteClass   ∈ {connected, remote} — the ONLY term for site connectivity
  (never "link class" or "connectivity class")

## 2. Element kinds
Elements form two levels:
- groupings  — plane, area. They organize; they own no runtime identity.
- components — service, store, registry, boundary. Leaf elements with
  runtime identity. "Component" is the collective term, not a kind.

external belongs to neither level: it is an outside actor.

- plane    — top-level operational domain with its own trust stance and its
             own instancing rule. Exactly three exist
             (control plane, tenant plane, edge plane).
- area     — grouping of components inside exactly one plane, sharing ONE
             boundary rule
             (data layer, serving, ML workspace, trust services).
             boundary rule (of an area) — the single stated constraint on
             what may cross the area's edge: what may be read, written, or
             handed off, by whom. It is a rule, not a thing — distinct from
             the boundary kind below.
             Criteria for being an area: exactly one boundary rule;
             interacts with other areas only via declared relation kinds
             (§4); belongs to exactly one plane.
             Not areas: environments and site classes (axis values, §1),
             the sync layer (a boundary).
- service  — behaviour without durable state
             (inference gateway, scheduler, catalog, CI/CD).
- store    — durable state. Flavours via store.class metadata (§5),
             never new kinds
             (object store, tables, operational database, predictions).
- registry — immutable, versioned handoff store between producers and
             runtimes (roles, §4)
             (source repo, artifact repo, model registry, experiments).
             A kind of its own — not a store flavour —
             because its boundary rule differs: write-once entries; read
             into runtimes by CI/CD only; promotion = lifecycle-stage
             transition (e.g. candidate -> promoted; a registry stage, not
             an environment — [ADR-0005](../adr/0005-two-environments.md)).
- boundary — a trust/coupling seam reified as a named component
             (OT gateway, public ingress, sync layer, staff identity
             federation). Both sides reference the boundary; neither side
             references the other.
- external — customer-owned or third-party system the platform integrates
             with. Lives outside every plane
             (customer historian, SCADA system, customer identity provider).

## 3. Environment container and bands
Two classifications of areas — not kinds:

- environment container — the subset of a tenant plane's areas instantiated
  once per env value (§1): the workspace, serving, application and
  orchestration areas. Marked envScoped (§5).
- band — an area outside the environment container: instantiated once per
  tenant, shared across environments (registries, trust services, operation
  services). Recognizable by absent envScoped. The data layer is also
  cross-environment but is marked shared (§5) — one instance by decision
  ([ADR-0006](../adr/0006-shared-zoned-data-layer.md)), not merely one per tenant.

## 4. Relation kinds
A relation connects two elements with a declared meaning. The signature
(from -> to) is part of the definition: a relation outside its signature is
a modeling error.

Roles (producer, consumer, runtime, mediator, orchestrator, policy) are
parts a component plays in one relation — not kinds. The same service may
be a producer in one relation and a runtime in another.

- publishesTo : service -> registry | store
               producer writes a versioned artifact/record
- readsVia    : component -> service
               consumer reads state through a mediator (catalog, query engine)
- servesTo    : registry -> service
               runtime consumes a promoted entry (promotion: §2 registry)
- syncsWith   : component <-> boundary
               async exchange across a seam; never component-to-component
               across it, no service addresses cross
- owns        : service -> store
               the single owner of an operational store accesses it
               directly, reads and writes, no mediation. Target's
               store.class MUST be operational; exactly one owner per
               operational store ([ADR-0016](../adr/0016-owns-relation-kind.md))
- enforces    : service -> component
               policy applied to a target (admission -> runtimes,
               access policy -> stores)
- schedules   : service -> component
               orchestrator triggers work in a target

## 5. Controlled metadata vocabularies
Every metadata key used in the model must be listed here.

- kypId — the element's ID (§7). Mandatory on every element; unique.
- adr — comma-separated ADR ids justifying the element's structure.
- store.class ∈ {analytical, operational, online}
  analytical = catalog-mediated read; operational = owned by exactly one
  application; online = low-latency serving reads
- optional ∈ {true} — component deployed only at some sites (edge)
- envScoped ∈ {true} — area belongs to the environment container (§3);
  absent on an area = it is a band
- shared ∈ {across-envs} — one instance serves all environments (data layer)
- status ∈ {gap} — declared in the architecture but not yet designed

## 6. Instances (nouns, never elements)
An instance is one concrete deployment produced by applying a plane's
instancing rule or an axis value. Instances never appear in the model.
Every plane is a term (a class); its deployments get an instance noun,
named after the dimension the plane instantiates over (customer -> tenant,
location -> site, env value -> environment), never after the plane:

| Term (class) | Instance noun | How many |
|---|---|---|
| control plane | the control plane (singleton: class and instance coincide, so no separate noun exists) | exactly 1 |
| tenant plane | a tenant | one per customer |
| environment container (the env-scoped subset of tenant areas, §3) | an environment | two per tenant today: its nonprod and its prod |
| edge plane | a site | 0..N per tenant, one per location |

Two disambiguations:
- customer — the organization. A tenant is the deployment that serves it;
  "tenant" never means the organization.
- fleet — the set of all tenants; the control plane's object of management.

## 7. ID scheme
KYP-<plane>-<AREA>-<nn>   plane ∈ {C, T, E} (control, tenant, edge);
AREA is the area slug; nn two digits. Area-level IDs omit nn (KYP-T-DATA).
IDs are immutable; renames keep the ID. The KYP-ID is the join key across
model, ADRs, bindings, Notion registers and Linear issues.

## 8. Zones (partitions of the data layer — [ADR-0006](../adr/0006-shared-zoned-data-layer.md))
A zone is a partition of the data layer's stores carrying exactly one
access rule. Zones are never elements; zone membership is data placement.
zone ∈ {raw, curated, sandbox(env)}

- raw          — data as ingested; reads governed by data classification
- curated      — writable only by the prod orchestration identity
- sandbox(env) — one per environment; the only zone nonprod may write to

"prod orchestration identity" = the workload identity (trust services) under
which the prod environment's orchestration area runs.

## 9. Bindings (architecture/bindings/*.yaml)
A binding answers one question: which product fulfills this component's
contract, for this tenant class?

    a component (§2, keyed by its KYP-ID §7) states a contract
    a binding maps:  contract x tenantClass (§1)  ->  product + posture

- contract — the promise the component states in the model (e.g. an
  object-store contract). A capability, never a product or one vendor's
  protocol. The only thing other components may depend on.
- contract profile — the contract made explicit: `required` rows components
  may rely on, `not-relied-upon` rows they must not.
- product — a concrete technology fulfilling the contract. NEVER named in
  the model ([ADR-0007](../adr/0007-object-store-contract-bindings.md)); swapping one touches bindings + an ADR, never the
  model.
- posture — how the bound product is operated (managed-regional, self-run,
  self-run-operator). Unrelated to a plane's trust stance (§2).

Rule: a product may be bound only if it satisfies every `required` row of
the contract profile. Enforced at review time — the CI gate does not
validate bindings yet.

Bindings are per tenant class; which binding applies to one concrete tenant
is resolved in the control-plane tenant registry.

## 10. Placement rules
See CLAUDE.md "Placement rules" — normative here by reference.

## Appendix A — anchoring to standard vocabularies
This taxonomy invents a term only where it carries a rule no standard term
carries; everything else anchors to an existing vocabulary. ≈ means
"nearest standard term"; the *differs* note is what our rule adds. New
terms are admitted only under that test.

| Kyper term | ≈ standard term | Source | Differs |
|---|---|---|---|
| plane | control / data / management plane | networking, Kubernetes usage | ours adds an instancing rule per plane |
| area | grouping / package | ArchiMate grouping, UML package | exactly one boundary rule required |
| component | component | UML, C4 | collective term for the four leaf kinds |
| service | service | C4 container, ArchiMate application service | must be stateless |
| store | data store | C4, ArchiMate data object | must live in the data layer |
| registry | registry | industry term | write-once; CI/CD-only read; staged promotion |
| boundary | conduit | IEC 62443 zones & conduits | reified as a model element both sides reference |
| zone | zone | IEC 62443; raw/curated conventions | exactly one access rule per zone |
| contract | interface | UML interface, ArchiMate application interface | the only dependable surface of a component |
| contract profile | interface specification | UML | explicit required / not-relied-upon rows |
| binding | realization (the relationship) | UML/ArchiMate realization | keyed by KYP-ID x tenantClass; recorded outside the model |
| product | technology element | ArchiMate system software, UML artifact | banned from the model ([ADR-0007](../adr/0007-object-store-contract-bindings.md)) |
| servesTo | serving | ArchiMate serving | source must be a registry |
| readsVia | access (read) | ArchiMate access | must pass through a mediator service |
| publishesTo | access (write) / flow | ArchiMate | target must be registry or store; versioned |
| schedules | triggering | ArchiMate triggering | one orchestrator per environment |
| syncsWith | flow through a conduit | ArchiMate flow + IEC 62443 | may only terminate on a boundary |
| owns | access (read/write) | ArchiMate access | operational stores only; exactly one owner per store |
| enforces | — (policy application) | nearest: ArchiMate realization of a requirement | none close; kept as ours |
| axis | (architecture) viewpoint dimension | ISO/IEC/IEEE 42010 spirit | axis values are metadata, never elements |
| instance | instance specification | UML | instances never appear in the model |
| environment container, band | — | none | genuinely ours: they carry the instancing rules |

Phase 1 of [docs/analysis-plan.md](../docs/analysis-plan.md) (terminology map to ISO/IEC 23053 and IIRA)
extends this table downward from metamodel terms to the components themselves.
