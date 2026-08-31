---
id: ADR-0011
status: accepted
date: 2026-08-31
affects: [KYP-T-DATA-01, KYP-T-DATA-25]
---
# Bind the on-prem object store contract to SeaweedFS

## Context
ADR-0007 left the onprem product for the s3-object-api contract TBD. On-prem
tenant footprints are small and operationally constrained (edge-adjacent);
the team operating them is not a storage team. The contract profile in
architecture/bindings/storage.yaml defines what the product must satisfy.

## Decision
SeaweedFS is the onprem binding for KYP-T-DATA-01. It satisfies the
profile's required rows (object CRUD, ranged reads, multipart, presigned
URLs, encryption at rest) with one compensation: its IAM is coarser than
S3/RGW, so the curated-zone write rule (ADR-0006) is enforced by dedicated
per-zone identities plus mediation by the access policy component
(KYP-T-DATA-25) — not by store-native policy documents.

## Consequences
- Zone enforcement correctness shifts partly from the store to platform
  components; the access-policy grant log becomes the audit evidence.
- The object store provides no block storage: the operational database
  (KYP-T-DATA-03) needs a separate block CSI. Postgres cannot run on object
  storage; S3-backed Postgres engines are managed/commercial only.
- SeaweedFS community/maintainer concentration is a monitored risk; the
  contract profile keeps a swap to another S3-wire product a bindings-only
  change.

## Rejected alternatives
- MinIO: AGPL plus the 2025 community-edition feature removals make it a
  licensing and roadmap risk inside a customer-shipped product.
- Ceph RGW: strongest IAM row and block/FS double-duty, but operationally
  too heavy for the target on-prem footprints.
- Raw PVCs: block/filesystem volumes expose no object API, presigned URLs
  or IAM — they cannot satisfy s3-object-api; every candidate runs on PVCs.
