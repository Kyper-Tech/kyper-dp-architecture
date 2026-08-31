# 12. Glossary

Structural/metamodel terms live in the
[taxonomy](../../architecture/taxonomy.md) — the single authoring surface
for vocabulary. This section holds business/domain terms only. The mapping
to ISO/IEC 23053 vocabulary lands here once the terminology map exists
([analysis plan](../analysis-plan.md), phase 1).

- **SBOM** (Software Bill of Materials) — machine-readable inventory of
  every component inside an artifact (libraries, versions, licenses;
  SPDX or CycloneDX format). Travels with each golden artifact; enables
  fleet-wide CVE queries and per-customer compliance evidence.
- **golden** (artifact) — a release artifact accepted into the control
  plane's artifact registry: signed, scanned, SBOM attached. The only form
  tenants can pull.
