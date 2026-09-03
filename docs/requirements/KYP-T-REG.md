# Requirements — Registries (KYP-T-REG)

Boundary rule: the only handoff seam; write-once entries, read into
runtimes by CI/CD only, promotion by lifecycle stage ([ADR-0004](../../adr/0004-registries-only-handoff.md)).

| ID | Requirement | satisfied-by |
|---|---|---|
| REQ-KYP-T-REG-01 | Entries MUST be immutable and versioned; a change is a new version, never an edit. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-REG-02 | Promotion MUST be a recorded lifecycle-stage transition (e.g. candidate -> promoted). | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-REG-03 | Only CI/CD moves a registry entry into a runtime; producers cannot deploy directly. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |
| REQ-KYP-T-REG-04 | Every artifact running in any runtime MUST be traceable to exactly one registry entry. | [ADR-0004](../../adr/0004-registries-only-handoff.md) |

Quality: [Q-05](../arc42/10-quality-requirements.md) (promotion integrity).
