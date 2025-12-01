# Critique: Dartwing Family Architecture

Scope reviewed: `dartwing_core/dartwing_core_arch.md`, `dartwing_family_arch.md`, `dartwing_family_executive_summary.md`, `dartwing_family_prd.md`

## Strengths
- Comprehensive data model with rich DocType coverage (relationships, chores/rewards, finance, custody, medical, location, integrations); strong age-aware logic and COPPA awareness baked into Family Member controller.
- Clear activation model keyed off `Organization.org_type = Family`, with fixtures and scheduler jobs defined; aligns with dartwing_core hybrid org model.
- Privacy and safety-first framing (age-based minimization, COPPA, guardian validation) and explicit real-time + offline ambitions.
- Modular adapter strategy for integrations (home automation, retail, education, telematics) keeps external dependencies decoupled.
- Role mapping and permission profiles per age category provide a foundation for least-privilege defaults.

## Weaknesses / Gaps
- Permission enforcement thin: relies on custom permission manager but lacks `user_permission_doctypes`, list filters for all doctypes, and Socket.IO/job enforcement; PHI and sensitive data (medical, location) need stricter role separation.
- Offline/real-time sync undefined at module level: PRD promises offline-first and conflict resolution, but no change-feed/batch-upsert/tombstone spec for family doctypes; relies on core docs implicitly.
- Integration burden high: 20+ integrations listed without sequencing, error handling, or degraded-mode behavior; risk of brittle UX when adapters fail.
- Multi-tenant controls need depth: no hierarchy/linked families, no per-tenant rate limits/backpressure for real-time or location feeds, no Drive namespace strategy for shared assets.
- Compliance details missing: COPPA/GDPR/PHI retention, soft-delete policies, consent logging, and audit trails for voice/location/medical not fully specified.
- Operational safety: schedulers (age check, allowance, geofence, grade sync) lack idempotency/alerting docs; background jobs could cross-org leak without shared permission guard.

## PRD Feature Fit (ease vs difficulty)
**Easier**
- Chore management and rewards: DocTypes and controllers exist; needs modest validation and UI.
- Allowance tracking: Config/payment DocTypes present; implement payout hooks and audit.
- Calendar/events: Family calendars, reminders, transportation requests outlined.
- Age-based permissions: Controller logic and profiles already mapped to roles.

**Moderate**
- Location sharing/geofences/check-ins: Needs rate limits, storage strategy, and alert flows; must harden permission checks.
- Custody scheduling: Rules and relationships exist; requires conflict detection and calendar overlays.
- Home automation/retail/education adapters: Design patterns exist but need concrete adapter implementations and error handling.
- Voice assistant (family VA): Depends on VA module; child-safe filters and consent must be enforced in-app.
- Offline sync for core flows: Requires applying a defined sync protocol to Family doctypes.

**Hard / High-Risk**
- 20+ third-party integrations at once: operational and support load; many APIs with differing auth/rate limits.
- Real-time + offline across sensitive data (location/medical): conflict handling, ACL, and retention must be precise to avoid leakage.
- Teen driving/vehicle telemetry: Safety implications; needs anomaly detection, rate capping, and clear consent.
- COPPA/PHI compliance end-to-end: Must prove auditability, data minimization, and retention/erasure flows.

## Recommendations
1) Harden permissions: add `user_permission_doctypes` to all family-scoped doctypes; use shared permission utilities across REST, Socket.IO, and jobs; separate roles for medical/location/voice data; ensure org filter in all list queries.
2) Define offline/sync spec for Family doctypes: align with core sync (change feed, batch upsert, tombstones, conflict policy, attachment handling) and document client responsibilities.
3) Sequence integrations: ship in waves (core chores/allowance/calendar → location/geofence → custody → selected adapters → voice/telemetry). Add degraded-mode behavior and health checks for each adapter.
4) Compliance and retention: document COPPA/GDPR/PHI policies, retention windows, soft-delete for sensitive records, consent logs for voice/location/medical, and audit access to vault/drive assets.
5) Observability/safety: add per-org rate limits for location/real-time events; DLQ for scheduler failures; metrics/alerts for sync lag, geofence checks, allowance payouts, and adapter errors.
6) Multi-tenancy depth: consider parent/linked families for blended/extended scenarios; namespace Drive/storage per family; add per-tenant search indices if using vector DB for knowledge/voice.

## Implementability Verdict
- Core family flows (chores, allowance, calendar, age-based permissions) are well supported and should be straightforward. Location/custody and basic adapters are achievable with added permission and rate-limit hardening. High-risk areas (mass integrations, vehicle telemetry, voice/PHI handling, offline+real-time for sensitive data) need concrete sync/ACL/compliance design and phased rollout to avoid leakage and operational instability. 
