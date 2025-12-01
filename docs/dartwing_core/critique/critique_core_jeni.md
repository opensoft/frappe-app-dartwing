# Critique: Dartwing Core Architecture vs PRD

Scope reviewed: `dartwing_core_arch.md`, `dartwing_core_prd.md`

## Strengths
- Hybrid Organization model (thin Organization + concrete types) with documented hooks, mixins, and permission hooks addresses the god-object risk while preserving `Link -> Organization` ergonomics.
- API-first mandate (`@frappe.whitelist`), feature-first Flutter structure, and Keycloak-based auth are coherent with multi-client consumption and SSO requirements.
- Clear capability coverage in PRD (C-01…C-25) with dependency graph; core features like invitations, offline/real-time, UI generation, and plugin/module system are explicitly called out.
- Security/permissions are at least scoped conceptually (org-level isolation, role templates, user permissions), and naming series plus doc listings reduce ambiguity.
- Compliance ambitions (HIPAA/SOC2/GDPR, audit trail, data residency) and offline/real-time goals are explicitly stated, giving targets for implementation.

## Gaps & Risks (architecture vs PRD needs)
- org_type immutability and atomic creation are implied but not enforced in code; missing reconciliation for orphaned Organizations (REQ-ORG-004/011).
- Offline/real-time sync lacks concrete protocol (change feed, batch upsert, tombstones, conflict policy, attachment handling) tied to C-04/C-05; “AI Smart Merge” is aspirational without spec.
- UI auto-generation (C-06/C-19) is described but no schema/renderer contract is defined (field widgets, validation mapping, conditional logic, offline forms).
- Permissions not fully hardened: `user_permission_doctypes` not specified per concrete type; Socket.IO and background jobs could bypass org filters; field-level constraints for sensitive modules (health, billing) are unspecified.
- Compliance features (C-13/C-20/C-21) lack data retention, soft-delete strategy, audit scope, and encryption/key management details; no residency-aware storage routing.
- Integrations/marketplace (C-15) and unified storage (C-07) list many targets but lack degraded-mode behavior, rate limits, and error handling; risk of brittle user experience.
- Billing/usage metering (C-12) not mapped to data model or events; no per-org quotas or backpressure strategy.
- Performance/SLO enforcement not backed by indices, caching strategy, or rate limiting; <400ms context switching and <200ms API goals are ungrounded.

## PRD Feature Implementability (ease vs difficulty)
**Easier**
- C-01/C-02/C-03 (org creation, invitations), C-17 (basic RBAC), C-18 (theming), C-19 (navigation) — architecture supports, needs org immutability guard and permission helpers.
- C-14/C-16 (plugin system, background jobs) — Frappe hooks/scheduler give a base; needs job monitoring/retry policy.
- C-23/C-25 (exports, reminders) — achievable as doctypes + jobs.

**Moderate**
- C-04/C-05 (offline + real-time): requires defined sync protocol, delta feeds, conflict rules, attachment flow.
- C-06 (UI generation): needs a DocType→Flutter renderer contract, widget mapping, and client override points.
- C-07 (unified storage) and C-10 (notifications): require provider abstraction, quotas, and per-org policy.
- C-12 (billing/metering): needs event hooks and per-feature meters; align with feature flags (C-22).
- C-09 (search): feasible with OpenSearch/DB, but must enforce org ACLs in index and queries.

**Hard / High-Risk**
- C-11/C-13/C-20/C-21 (white-label + compliance/audit/residency): require multi-region storage, key management, immutable logs, and provable retention/erasure workflows.
- C-15 (40+ integrations marketplace): operationally heavy; needs adapter framework, health checks, and fallback UX.
- C-24 (fax primitive) at scale: carrier failover, retries, deliverability receipts, billing integration.
- “AI Smart Merge” conflict resolution: needs deterministic rules and human fallback UI; risk of silent data loss.

## Recommendations to strengthen architecture
1) Enforce org integrity: make `org_type` immutable post-insert; ensure atomic concrete creation with idempotency and add a reconciliation job for missing links.
2) Publish sync spec (tie to C-04/C-05): change feed API, batch upsert, tombstones, conflict policy (LWW + audit, optional human review), attachment flow, retry/backoff, and test matrix.
3) Define UI generation contract: DocType→widget mapping, validation, conditional visibility, offline form caching, and extension points for module-specific overrides.
4) Harden permissions: set `user_permission_doctypes` on concretes; shared permission utilities for REST, Socket.IO, and jobs; field-level controls for sensitive data; tests for multi-org users.
5) Compliance/residency plan: retention/soft-delete, audit scope (what is logged), key management, residency-aware storage and search indices, and BAA/GDPR flows.
6) Metering and feature flags: map meters to events (fax pages, storage, API calls, seats), set per-org quotas, and integrate with C-22 flags; add backpressure behavior.
7) Observability/performance: define SLOs and back them with indexes on `organization`, `modified`, `org_type`; per-org rate limits; metrics for sync lag, job failures, notification/queue health.
8) Integrations/marketplace and storage: provide adapter framework with health checks, retries, and degraded-mode UX; for storage, define provider failover and virus-scan policy.

## Verdict
- The architecture aligns conceptually with the PRD, but several critical features (offline/sync, UI auto-generation, compliance, metering) need concrete specs and enforcement to be safely shippable. Addressing org integrity, sync protocol, permissions, and compliance/metering details will materially reduce implementation risk and make the PRD goals achievable. 
