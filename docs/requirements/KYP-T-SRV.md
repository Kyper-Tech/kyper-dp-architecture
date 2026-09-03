# Requirements — Serving (KYP-T-SRV)

Boundary rule: stateless; models in from registry, predictions out to
storage.

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-SRV-01 | The model runtime MUST load only promoted, signed model-registry entries; admission verifies before load. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-SRV-02 | Every prediction MUST be written to the predictions store labelled with its environment. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |
| REQ-KYP-T-SRV-03 | Serving components MUST hold no durable state; restart loses nothing but in-flight requests. | — |
| REQ-KYP-T-SRV-04 | All inference MUST enter through the inference gateway; no direct model-runtime access. | — |
| REQ-KYP-T-SRV-05 | The drift monitor MUST read prod-labelled predictions via the query engine only. | [ADR-0006](../../adr/0006-shared-zoned-data-layer.md) |

Quality: [Q-05](../arc42/10-quality-requirements.md) (promotion integrity),
[Q-07](../arc42/10-quality-requirements.md) (workload isolation).
