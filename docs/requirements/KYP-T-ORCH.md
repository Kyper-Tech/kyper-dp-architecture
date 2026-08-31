# Requirements — Orchestration (KYP-T-ORCH)

Boundary rule: one scheduler per environment; owns all recurring work.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-ORCH-01 | Exactly one scheduler per environment MUST own all recurring work, including idle scale-to-zero. | ADR-0005 |
| REQ-KYP-T-ORCH-02 | The scheduler MUST execute only pipelines promoted through the artifact repo; no live-edited definitions. | ADR-0015 |
| REQ-KYP-T-ORCH-03 | Curated-zone writes MUST happen only under the prod orchestration identity. | ADR-0006 |
| REQ-KYP-T-ORCH-04 | Retraining MUST be triggered by schedule or drift signal, never manually inside a runtime. | — |

Quality: [Q-03](../arc42/10-quality-requirements.md) (zone enforcement).
