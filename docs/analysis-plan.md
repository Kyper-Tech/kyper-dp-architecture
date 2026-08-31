# Standards conformance analysis — plan (Linear project)

Exit criterion: every register row classified (gap / decision-needed / accepted-deviation /
validated) — not every source exhausted.

## Phase 0 — Baseline and sources (~1d)
1. Component register with KYP-IDs (generated from model; mirrored as text IDs in Notion).
2. Acquire sources, record versions.
   - ISO/IEC 23053: https://www.iso.org/standard/74438.html
   - JTC 1/SC 42 catalogue (5338, 5259, 23894, 42001): https://www.iso.org/committee/6794475.html
   - IIRA v1.10: https://www.iiconsortium.org/wp-content/uploads/sites/2/2022/11/IIRA-v1.10.pdf
   - CNCF CNAI: https://tag-runtime.cncf.io/wgs/cnaiwg/whitepapers/cloudnativeai/
   - CNCF data-on-K8s AI (2026): https://www.cncf.io/report-whitepaper/2026/07/08/the-cncf-data-storage-in-cloud-native-ai-white-paper/
   - AWS ML Lens: https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html
   - AWS SaaS Lens: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html
   - Google MLOps guide: https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf
   Prereqs: ISO 42010 concepts before IIRA (https://www.iso-architecture.org/ieee-1471/cm/);
   AWS SaaS fundamentals before SaaS Lens
   (https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/saas-architecture-fundamentals.html);
   base WAF before ML Lens (https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html).

## Phase 1 — Structural and vocabulary mapping (~1-2d)
3. Terminology map: KYP-ID -> 23053 term -> IIRA functional domain. Mark residuals both ways.
4. Tier mapping vs IIRA edge/platform/enterprise + gateway-mediated connectivity; delta list.

## Phase 2 — Capability gap passes (~2-3d)
5. Google MLOps capabilities vs workspaces/registries/orchestration: present/conditional/absent + justification.
   Second opinion: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/mlops-maturity-model
6. CNCF CNAI stack shape vs tenant plane; data-on-K8s paper vs storage row and shared-data decision.
7. SaaS Lens vs control plane and tenancy (lifecycle, isolation, tiering, metering) — densest findings expected.

## Phase 3 — Review instruments (~2-3d)
8. ML Lens review, six phases x pillars per subsystem, timeboxed; findings as risks/decisions, never components.
9. IEC 62443 zone-and-conduit model over OT gateway, network policy, sync layer, edge
   (https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards).

## Phase 4 — Consolidation (~1-2d)
10. Single findings register with four classifications, priority, owner.
11. One architecture revision; everything else becomes ADRs (https://adr.github.io).
12. External artifact: conformance map + zone model (security-questionnaire annex).

Dependencies: 3-7 parallelizable; 8-9 depend on 3; 10 gates 11-12.
