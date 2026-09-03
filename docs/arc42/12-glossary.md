# 12. Glossary

Structural/metamodel terms live in the
[taxonomy](../../architecture/taxonomy.md) — the single authoring surface
for vocabulary. This section holds business/domain terms only. The mapping
to ISO/IEC 23053 vocabulary lands here once the terminology map exists
([analysis plan](../analysis-plan.md), phase 1).

- **CVE** (Common Vulnerabilities and Exposures) — the public catalog of
  known security flaws, each with an id such as CVE-2021-44228 (Log4Shell).
  "Which tenants does a CVE affect" is answered by joining the tenant
  registry (what each tenant runs) with the SBOMs of those versions.
- **golden** (artifact) — a release artifact accepted into the control
  plane's artifact registry: signed, scanned, SBOM attached. The only form
  tenants can pull.
- **OT** (operational technology) — the plant-floor systems the platform
  ingests from: PLCs, SCADA, historians. Customer-owned; reached only
  through a named boundary.
- **SBOM** (Software Bill of Materials) — machine-readable inventory of
  every component inside an artifact (libraries, versions, licenses;
  SPDX or CycloneDX format). Travels with each golden artifact; enables
  fleet-wide CVE queries and per-customer compliance evidence.
