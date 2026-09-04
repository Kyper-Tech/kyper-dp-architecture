---
id: ADR-0014
status: proposed
date: 2026-08-31
affects: [KYP-T-DATA, KYP-T-DATA-04]
---
# Layer the data layer's storage group: time-series, lakehouse, serving, operational

## Context
Telemetry is the platform's primary data shape, but the storage group gives
it no home: raw sensor data has only a generic object store to land in, and
vector search hides inside an undifferentiated "Indexes" store. Access
patterns in the group differ by orders of magnitude (ingest-rate appends vs
batch analytics vs millisecond similarity lookups) yet are not named.

## Decision
Storage is organized into four layers by access pattern. No new kinds —
stores differ by store.class (taxonomy §5), extended with one value:

- timeseries — high-rate append, time-windowed reads, native downsampling
  and retention.

Layers and stores:
1. Hot / landing — Time-series store (new, KYP-T-DATA-08,
   class timeseries, contract timeseries-query): telemetry lands here in
   the raw zone; owns retention and downsampling. It comes with a read-path
   mediating service: non-production reaches the read path, never the
   store ([ADR-0006](0006-shared-zoned-data-layer.md), network separation).
2. Curated / multimodal lakehouse — Object store + Tables (unchanged,
   analytical). The system of record for every modality: downsampled
   telemetry history, documents (manuals, reports), images, and offline
   feature tables — all in the curated zone, all under data contracts,
   classification and lineage like any other curated data.
3. Serving / online — Vector store (new, KYP-T-DATA-09, class online,
   contract vector-search); Feature store (rename of Indexes, keeps
   KYP-T-DATA-04, class online, contract feature-serving); Predictions
   (unchanged). Vector and feature stores are DERIVED projections of the
   lakehouse — chunking/embedding pipelines materialize curated documents
   into the vector store; feature pipelines materialize offline feature
   tables into the feature store. They hold no facts of their own and are
   rebuildable from curated + lineage.
4. Operational — Operational database (unchanged).

Flows: orchestration compacts hot -> curated on the TS store's retention
schedule; chunking/embedding and feature pipelines (scheduled, per
environment) materialize curated -> serving; all analytical reads stay
catalog-mediated. Zones ([ADR-0006](0006-shared-zoned-data-layer.md)) apply across all layers.

Products (Timescale/QuestDB/Influx; Qdrant/Milvus/pgvector) are bindings
per tenant class with contract profiles written before binding ([ADR-0007](0007-object-store-contract-bindings.md)).

## Consequences
- DR posture differs per layer and must not be averaged:
  - Operational database: primary state -> classic backup with
    point-in-time recovery. Nothing here is rebuildable.
  - Time-series store: PRIMARY until compaction has landed the data in
    curated -> backup, or an explicitly accepted loss window (an RPO
    decision per tenant class — already an open decision in the brief).
  - Lakehouse (object store + tables): system of record -> full backup/DR
    (the ops band's Backup + DR component).
  - Predictions: written facts -> backup (re-scoring is possible but is a
    policy decision, not an assumption).
  - Vector + feature stores ONLY: derived -> rebuild from curated instead
    of restore; valid only if lineage from every entry back to its curated
    source exists, so lineage (KYP-T-DATA-20) becomes load-bearing for
    exactly these two.
- Chunking/embedding is a scheduled pipeline like any other (one scheduler
  per environment, placement rule 5) — not a side effect inside serving.
- Two new stores and one class value: model, taxonomy §5, bindings and the
  gate's class vocabulary change together in the accepting PR.
- Contract profiles needed for timeseries-query, vector-search and
  feature-serving before any product is bound; the vector profile must
  decide on filtered/hybrid search in its required rows.
- On-prem cost: three more self-run stateful products per tenant unless
  bindings collapse them (e.g. one product fulfilling postgres-wire +
  timeseries-query + vector-search is admissible if it satisfies every
  required row of each profile).

## Rejected alternatives
- New store kinds per technology: boundary rules do not differ; class
  covers it (taxonomy §2 store).
- Keeping vector inside a generic Indexes store: contract cannot be
  profiled, so bindings cannot be validated.
- Landing telemetry directly in the object store: loses windowed reads,
  retention and downsampling at ingest rate.
