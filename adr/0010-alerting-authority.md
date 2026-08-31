---
id: ADR-0010
status: proposed
date: 2026-08-31
affects: [KYP-T-APP-03, KYP-E-RT-04]
---
# Tenant alerting is authoritative; edge alerting is a disconnected-mode replica
## Context
Sites with a dead WAN link must still alarm; alert state must not fork permanently.
## Decision
Edge local alerting raises and acknowledges offline; acks sync upward; tenant alerting
owns escalation and suppression state after reconnect.
## Consequences
Reconciliation protocol required (same class as dual-scheduler rule).
## Rejected alternatives
Tenant-only alerting.
