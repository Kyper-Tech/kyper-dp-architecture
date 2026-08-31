# 7. Deployment View

> Skeleton — to be filled. Deployment is instancing of the model along its
> axes, never a duplicated subtree:

- Instancing rules per plane: [design brief — planes](../design-brief.md#planes).
- Axes: `env ∈ {nonprod, prod}`, `tenantClass ∈ {cloud-gcp, cloud-aws, onprem}`,
  `siteClass ∈ {connected, remote}` — [taxonomy](../../architecture/taxonomy.md).
- Contract → product resolution per tenant class:
  [bindings](../../architecture/bindings/storage.yaml)
  ([ADR-0007](../../adr/0007-object-store-contract-bindings.md)); per-tenant
  resolution lives in the control-plane tenant registry.
