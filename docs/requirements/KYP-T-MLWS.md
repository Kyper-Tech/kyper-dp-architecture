# Requirements — ML workspace (KYP-T-MLWS)

Boundary rule: ephemeral, nothing durable; hands off only to model registry
and experiments; classified/raw reads under audited grants ([ADR-0012](../../adr/0012-split-dev-ml-workspaces.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-MLWS-01 | A training run MUST be reproducible from a source commit, an environment image digest and a versioned data snapshot reference. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-MLWS-02 | Models MUST leave the workspace only as model-registry entries; evaluation results only as experiment records. | [ADR-0012](../../adr/0012-split-dev-ml-workspaces.md) |
| REQ-KYP-T-MLWS-03 | Every training run MUST produce an experiment record linking code, data snapshot, parameters and evaluation results. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-MLWS-04 | Every raw-zone read MUST be granted per classification and recorded in the audit trail. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-MLWS-05 | Losing a workspace instance MUST cost at most uncommitted work. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-MLWS-06 | Models MUST be trained only on this tenant's data, for this customer's purposes. Model artifacts and their derivatives (weights, gradients, evaluation data, fine-tunes) MUST never leave the tenant plane — not to the control plane, not to another tenant. Cross-tenant learning requires explicit customer consent and a new ADR. | [ADR-0002](../../adr/0002-tenant-per-customer.md) |

Quality: [Q-04](../arc42/10-quality-requirements.md) (workspace loss),
[Q-03](../arc42/10-quality-requirements.md) (zone enforcement).
