# Requirements — Dev workspace (KYP-T-DEVWS)

Boundary rule: ephemeral, nothing durable; hands off only to source/artifact
repos; curated-zone data scope ([ADR-0012](../../adr/0012-split-dev-ml-workspaces.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-DEVWS-01 | A build MUST be reproducible from a source-repo commit plus an environment image digest alone. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-DEVWS-02 | Code and build artifacts MUST leave the workspace only via source repo (commits) and artifact repo (images, packages). | [ADR-0012](../../adr/0012-split-dev-ml-workspaces.md) |
| REQ-KYP-T-DEVWS-03 | Data access MUST be curated-zone only, via the catalog; no raw-zone path exists. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md), [ADR-0012](../../adr/0012-split-dev-ml-workspaces.md) |
| REQ-KYP-T-DEVWS-04 | Losing a workspace instance MUST cost at most uncommitted work. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |

Quality: [Q-04](../arc42/10-quality-requirements.md) (workspace loss).
