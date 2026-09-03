---
id: ADR-0018
status: proposed
date: 2026-08-31
affects: [KYP-T-TRUST-01, KYP-T-TRUST-02, KYP-E-SITE-02]
---
# Customer users federate to the customer's IdP, per tenant, never through the control plane

## Context
Application users are the customer's people. The customer already runs an
identity provider and expects their users to sign in with it. The control
plane holds no customer data (REQ-KYP-C-07) and no credentials into a
customer environment (REQ-KYP-C-02), so it cannot be in the login path.
The model already separates staff identity (KYP-C-TRUST-01, Kyper's own
people) from tenant identity (KYP-T-TRUST-01), but nothing states how
customer users reach the platform, and disconnected sites have no answer
at all.

## Decision
1. End-user identity is a tenant-plane concern. Each tenant's identity
   service (KYP-T-TRUST-01) federates to that customer's IdP. The control
   plane is not in the path and never sees an end user.
2. The customer IdP is an external system reached through a named boundary
   in the tenant trust band, following the seam pattern of ADR-0017.
   Components never address the IdP directly.
3. Kyper stores no customer passwords. What the tenant stores — subject
   identifiers, group and role claims, sessions — is customer data and
   stays in that tenant.
4. IdP client secrets live in that tenant's Secrets (KYP-T-TRUST-02),
   audited on every use. They are credentials into a customer environment,
   so REQ-KYP-C-02 keeps them out of the control plane.
5. Tenants without a usable IdP fall back to local identities in the
   tenant identity service. Federation is a per-tenant mode, not a
   platform-wide assumption.
6. Sites must authenticate operators with the WAN down, when the customer
   IdP is unreachable. Offline login uses short-lived cached assertions or
   site-scoped local identities, bounded by the site's clock discipline
   (REQ-KYP-E-SITE-03); revocations reconcile on reconnect, tenant
   identity authoritative — the same replica pattern as alerting
   (ADR-0010).
7. The tenant registry records only the federation mode (federated |
   local), never endpoints, client ids or secrets — the same minimal
   treatment as ingestion mode.

## Consequences
- REQ-KYP-C-07 holds unchanged: no end user, and no user identifier, ever
  reaches the control plane.
- Staff federation and customer federation stay separate seams. A staff
  identity compromise reaches no customer user; a customer IdP compromise
  reaches one tenant.
- Offline login is a bounded exception with a reconciliation obligation,
  and it widens the window in which a revoked user can still act at a
  site. That window is a contract parameter, not a default.
- Model changes on acceptance: a customer identity federation boundary in
  the tenant trust band, and the customer IdP as an external.

## Rejected alternatives
- One central IdP in the control plane serving all tenants: puts customer
  identities in the control plane, breaking REQ-KYP-C-07, and makes one
  compromise cross-tenant.
- Kyper-managed passwords per tenant: password storage liability with no
  benefit over federation.
- Reusing the staff federation boundary (KYP-C-TRUST-01): mixes Kyper
  staff and customer users in one trust seam.
- Requiring connectivity for every login: makes a dead WAN a production
  stop at the site, contradicting the edge plane's reason to exist.
