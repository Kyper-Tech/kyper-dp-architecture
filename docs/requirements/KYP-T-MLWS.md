# Requirements — ML workspace (KYP-T-MLWS)

Boundary rule: ephemeral, nothing durable; hands off only to model registry
and experiments; classified/raw reads under audited grants (ADR-0012).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-MLWS-01 | A training run MUST be reproducible from a source commit, an environment image digest and a versioned data snapshot reference. | ADR-0004 |
| REQ-KYP-T-MLWS-02 | Models MUST leave the workspace only as model-registry entries; evaluation results only as experiment records. | ADR-0012 |
| REQ-KYP-T-MLWS-03 | Every training run MUST produce an experiment record linking code, data snapshot, parameters and evaluation results. | ADR-0004 |
| REQ-KYP-T-MLWS-04 | Every raw-zone read MUST be granted per classification and recorded in the audit trail. | ADR-0006 |
| REQ-KYP-T-MLWS-05 | Losing a workspace instance MUST cost at most uncommitted work. | ADR-0004 |

Quality: [Q-04](../arc42/10-quality-requirements.md) (workspace loss),
[Q-03](../arc42/10-quality-requirements.md) (zone enforcement).
