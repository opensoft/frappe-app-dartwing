# Codex Critique: Dartwing Core Architecture

**Scope reviewed:** `dartwing_core_arch.md`, `dartwing_auth_arch.md`, `additional_features.md`, `architecture_critique.md`, `claud_core_arch_critique.md`

## What Works Well
- Hybrid Organization model (thin `Organization` + concrete types) is documented end to end with hooks, mixins, and permission hooks, avoiding the original single-table bloat while keeping `Link -> Organization` ergonomics.
- API-first mandate (`@frappe.whitelist` everywhere) ensures Flutter, Builder, and external clients use one contract; Riverpod + feature-first Flutter structure is sane for multi-platform.
- Keycloak-centric auth is described clearly (PKCE, short-lived tokens, personal vs business identity separation) and uses Social Login Key to avoid reinventing SSO.
- Permissions strategy cascades from Organization to concrete doctypes with query conditions; role hierarchy is defined and maps cleanly to Keycloak groups.
- Naming series, concrete doctypes, and child tables are explicitly enumerated, reducing guesswork for implementers.

## Risks / Gaps That Need Change (ordered by impact)
1. **Org type drift can corrupt links:** `org_type` is mutable and there is no guard against changing it after creation. Changing a Family to Company would orphan the concrete record and break hooks.  
2. **Lifecycle is non-atomic:** `after_insert` creates the concrete record; if that insert fails, the Organization persists without a concrete. There is no retry/idempotency guard or reconciliation job.  
3. **Person/identity model is underspecified:** Core docs reference `Person` and user mapping but never define the doctype fields, unique constraints, or how personal vs business identities map to Frappe Users. This blocks permission correctness and invite flows.  
4. **Permission leakage risk for multi-org users:** Strategy relies on `User Permission` creation from Org Member, but there is no enforcement that all access paths (custom RPCs, Socket.IO, background jobs) apply the same filters. Concrete doctypes lack explicit `user_permission_doctypes` and the auth doc omits claim-to-role mapping failure handling.  
5. **Hierarchy and delegation missing:** No parent/child Organization or cross-org delegation (subsidiaries, chapters, multi-household families), yet roadmap targets enterprise/nonprofit cases that require it.  
6. **Offline sync not designed:** Architecture promises offline/real-time sync but provides no protocol (conflict resolution, tombstones, pagination, retry/backoff, partial sync). This is a high-complexity area and a likely failure point for mobile.  
7. **Soft-delete/compliance story thin:** Hooks hard-delete concrete types; audit logging is listed but no retention/erasure model for HIPAA/GDPR is specified.  
8. **Keycloak operational fallback absent:** Keycloak is the only auth path; no "lite" mode or documented health/degradation behavior (token introspection latency, cache, fail-open vs fail-closed).  
9. **Performance safeguards missing:** No indexing plan on common predicates (`organization`, `org_type`, `linked_doctype/name`) or API rate limits per tenant; real-time sync and Equipment/Org Member lists will suffer at scale.

## Recommended Changes (with rationale)
1. **Lock `org_type` after creation and add migration guard.** Prevents orphaned concrete records; add validation in `Organization.validate` and a background reconciliation to create missing concretes for legacy rows.  
2. **Make concrete creation atomic/idempotent.** Move creation into `before_insert` or wrap `after_insert` in a transaction-like pattern with retry + `db_set` only after success; add a cron job to heal missing links. Prevents dangling Organizations and improves operational safety.  
3. **Publish the `Person` contract.** Document required fields (`user`, `keycloak_user_id`, `primary_email`, PII flags), uniqueness, and how invitations map to Org Member + User Permission creation. Without it, role propagation and personal/business separation are speculative.  
4. **Strengthen permission enforcement.** Add `user_permission_doctypes` on concrete doctypes, document a shared permission utility used by REST, Socket.IO, and background jobs, and define behavior when Keycloak group sync fails. This closes gaps for multi-org accounts and non-list API entry points.  
5. **Add Organization hierarchy + scoped queries.** Introduce `parent_organization` (and `parent_company`) with recursive permission-aware queries. Enterprise/nonprofit use cases depend on this to model subsidiaries/chapters without schema hacks.  
6. **Write the offline/real-time sync spec.** Define conflict strategy (e.g., LWW with audit trail or CRDT), delta feeds, pagination, retry/backoff, attachment handling, and a minimal test matrix. This is required before mobile ships to avoid data loss.  
7. **Adopt soft-delete/audit policy.** Replace hard deletes with cancel/archival for concretes, specify retention windows, and codify "right to be forgotten" flows. Aligns HIPAA/GDPR claims with actual behavior.  
8. **Plan Keycloak resiliency and "lite" mode.** Document caching of introspection, circuit-breaker behavior, and a fallback auth path (Frappe local auth) for small/self-hosted installs. Reduces operational fragility and broadens deployability.  
9. **Add performance guardrails.** Specify indexes on `organization`, `org_type`, and `linked_*`; outline rate limits per tenant and pagination defaults for high-churn doctypes (Org Member, Equipment). Keeps latency targets (<200 ms simple queries) realistic at 10k+ org scale.

## Quick Wins (low effort, high value)
- Ship `org_type` immutability and backfill script now.  
- Publish Person doctype and add `user_permission_doctypes` to concrete doctypes.  
- Add indexes and enforce pagination defaults in API helpers.  
- Draft the sync conflict policy before implementing offline queues.
