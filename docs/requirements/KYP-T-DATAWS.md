# Requirements — Data workspace (KYP-T-DATAWS)

Boundary rule: ephemeral, nothing durable; hands off only to source and
artifact repos; raw and curated reads under audited grants, for pipeline
development only ([ADR-0015](../../adr/0015-data-engineering-workspace.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-DATAWS-01 | A pipeline run MUST be reproducible from a source-repo commit plus an environment image digest alone. | [ADR-0004](../../adr/0004-registries-only-handoff.md), [ADR-0015](../../adr/0015-data-engineering-workspace.md) |
| REQ-KYP-T-DATAWS-02 | Pipeline artifacts (transform images, contract and quality definitions) MUST reach the scheduler only as promoted artifact-repo entries; no live-edited definitions. | [ADR-0015](../../adr/0015-data-engineering-workspace.md) |
| REQ-KYP-T-DATAWS-03 | A data engineer MUST be able to develop against raw and curated data; every raw read is granted per classification and recorded in the audit trail. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md), [ADR-0015](../../adr/0015-data-engineering-workspace.md) |
| REQ-KYP-T-DATAWS-04 | Pipeline test runs MUST write only to the environment's sandbox zone. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-DATAWS-05 | Losing a workspace instance MUST cost at most uncommitted work. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |

Quality: [Q-03](../arc42/10-quality-requirements.md) (zone enforcement),
[Q-04](../arc42/10-quality-requirements.md) (workspace loss).
