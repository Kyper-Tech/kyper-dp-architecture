# 4. Solution Strategy

> Skeleton — to be filled. The strategy in one breath, each point anchored:

1. State lives in the data layer; behaviour above it (placement rule 1).
2. Registries are the only producer→runtime handoff
   ([ADR-0004](../../adr/0004-registries-only-handoff.md)).
3. Every trust boundary is a named component (placement rule 3).
4. Cross-cutting concerns exist once, in platform bands (placement rule 4).
5. One scheduler per tenant environment; edge schedules only what must
   survive disconnection (placement rule 5).
6. Environments, tenant classes and site classes are axes — metadata, never
   elements ([taxonomy](../../architecture/taxonomy.md)).

Full placement rules: [CLAUDE.md](../../CLAUDE.md).
