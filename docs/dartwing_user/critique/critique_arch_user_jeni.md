# Critique – Dartwing User Architecture (jeni)

Sources reviewed: `docs/dartwing_core/dartwing_core_arch.md`, `docs/dartwing_user/dartwing_user_arch.md`, `docs/dartwing_user/dartwing_user_prd.md`. Note: `dartwing_user_executive_summary.md` is missing from the repo.

## Overall take
- Strong identity chain and owner-only access model set the right privacy posture, but several high-risk features (travel mode, digital will, vault, AI voice) need clearer enforcement hooks, key handling, and provider fail-safes to be production-ready.
- The module is ambitious: the doc covers most PRD features at the data/API layer, yet multiple P1/P2 items only have sketches (no data model or service plan), and some integrations are stubbed.
- Cross-org semantics ride on Core’s `Org Member` guardrails, but privacy, data-classification, and travel-mode filters are not wired through to consuming modules, leaving policy enforcement largely aspirational.

## Strengths
- Clean identity chain (Keycloak → Person → User Profile) with automatic profile creation and consistent owner-only permission philosophy (`dartwing_user/permissions.py`), aligning with the “personal ≠ organizational” principle.
- Comprehensive data model coverage for core security/privacy features (User Profile/Device/Session/Block, Privacy Setting, Digital Will, Vault Item, Verification Record, AI Voice Profile, Notification Preference), reducing future schema churn.
- Service-layer pattern is well-articulated (DeviceTrustService, TravelModeService, PrivacyService, VaultService, etc.) with background jobs scheduled for hygiene (trust score recalcs, session cleanup, will inactivity checks).
- Flutter client plan mirrors backend features with feature-first structure and Riverpod providers, easing alignment between API surface and UI screens.
- Audit logging and security events catalogue provide a baseline for compliance, and encryption helpers for vault items recognize E2E requirements.

## Weak points and gaps
- **Policy enforcement not wired:** Travel mode and privacy settings return filtered data in helpers but lack integration into API/query layers for other modules (tasks/messages/files), so sensitive data could still leak. No concrete data-type taxonomy for `Privacy Setting`.
- **Security stubs:** `DeviceTrustService` stubs MFA/OS update checks, and push-to-approve flow depends on `push_token` but omits rate-limits/expiry and trusted-device selection rules. No attestation or jailbreak/root detection.
- **Vault key handling unclear:** Encryption helper derives keys from user password but storage/rotation/salt persistence and client-side key custody are unspecified, risking server-side key exposure and lockout scenarios.
- **Digital will & duress flows:** Decoy data/trustee notifications are described but lack access scoping to concrete data sets and tamper-evident audit. No escalation/appeal flow or replay protection for trustee requests.
- **Cross-org search/feed:** Only a pattern is shown; no index strategy, per-org permission filters, or rate limits, making P1 features U-19/U-20 high-risk for data bleed and performance.
- **Missing/partial features vs PRD:** Passkeys (U-24), Contact auto-match (U-21), Achievements (U-26), Reputation scoring logic (U-27), AI Memory pipeline (U-28), Health/Wearable integrations (U-29/U-30) lack schemas/services. Daily briefing (U-10) and Unified activity feed (U-20) are only lightly sketched.
- **Docs/process gaps:** Missing `dartwing_user_executive_summary.md`; owner-only permissions are defined but not shown as registered in `hooks.py` for all doctypes; Person `after_insert` hook calls `frappe.db.commit()` (side effects inside hooks can mask partial failures).

## PRD alignment and implementation difficulty
Ease levels assume current architecture with modest hardening. “Support” refers to presence of schema/service/API.

| ID   | Feature                               | Ease | Notes |
| ---- | ------------------------------------- | ---- | ----- |
| U-01 | User Profile & Preferences            | Easy | Schema/UI/providers exist; add bio/pronouns/calendar fields from PRD. |
| U-02 | Multi-Org Management                  | Medium | Org list/switch implied; needs fast org context cache, badges, leave-org flow. |
| U-03 | Device Trust & Management             | Medium | Device/Session services exist; trust algo stubs + push-approve hardening needed. |
| U-04 | Global Block List                     | Easy | Doctype/API pattern present; need directory/message hooks and invite guard. |
| U-05 | Personal Shortcuts                    | Medium | Doctype defined; execution engine, voice trigger, import/export not specified. |
| U-06 | Travel Mode                           | Hard | Helper exists but no global data-classification enforcement or decoy routing. |
| U-07 | Push-to-Approve Login                 | Medium | Pending-device flow present; add MFA fallback, expiry, and rate-limits. |
| U-08 | Digital Will & Succession             | Hard | Schema/jobs exist; access-scoping, consent/audit, and dispute handling missing. |
| U-09 | AI Voice Profile                      | Hard | Schema + provider stub; needs storage/PII controls, fraud checks, watermark verify. |
| U-10 | Daily AI Briefing                     | Medium | Service stub only; requires data feeds (tasks/events/news), caching, SLAs. |
| U-11 | Live Location Sharing                 | Medium | Doctype present; needs throttling, precision controls, and recipient permissioning. |
| U-12 | Identity Verification                 | Medium | Verification Record + Persona stub; webhook security, badge exposure rules needed. |
| U-13 | Personal Vault                        | Hard | Schema/encryption helper exist; key mgmt, E2E flows, virus scanning, share tokens TBD. |
| U-14 | Emergency Contacts                    | Easy | Child table present; visibility controls already noted. |
| U-15 | Notification Preferences              | Medium | Doctype listed; delivery fan-out + channel fallback logic absent. |
| U-16 | Privacy Dashboard                     | Medium | Dashboard API/service present; needs data-type taxonomy and org-scoped filters. |
| U-17 | Data Export & Portability             | Medium | Queue/export pattern shown; scope of data sets and redaction rules unspecified. |
| U-18 | Account Deletion                      | Medium | PrivacyService schedule/cancel pattern; dependency checks and tombstoning policies needed. |
| U-19 | Cross-Org Search                      | Hard | Pattern only; requires indexing, permission-safe queries, pagination, abuse protection. |
| U-20 | Unified Activity Feed                 | Hard | No concrete source list or aggregation; needs event schema and dedupe rules. |
| U-21 | Contact Auto-Match                    | Hard | Not modeled; requires matching service, conflict resolution, privacy impact review. |
| U-22 | Smart Invitations                     | Medium | User Invite doctype/API; needs template variants, throttling, and prefill validation. |
| U-23 | Biometric Unlock                      | Easy | Flutter service included; ensure platform fallback and server-side flag storage. |
| U-24 | Passkey Support                       | Hard | Not covered; add WebAuthn/Platform Auth flows and binding to Keycloak. |
| U-25 | Session Management                    | Easy | User Session model + APIs present; ensure revoke-on-device changes. |
| U-26 | Achievements & Gamification           | Hard | Not modeled; requires event schema and reward engine. |
| U-27 | Reputation Score                      | Hard | Schema present but scoring inputs/decay not defined; risk of bias and abuse. |
| U-28 | Personal AI Memory                    | Hard | Doctype exists but capture/retention/purging pipeline missing. |
| U-29 | Health Data Integration               | Hard | Not modeled; needs consent, PHI handling, provider SDKs. |
| U-30 | Wearable Device Sync                  | Hard | Not modeled; depends on platform-specific collectors and throttling. |

## Recommendations to harden and simplify implementation
- **Enforce privacy/travel mode centrally:** Define a data-type taxonomy (financial/medical/business/personal AI/vault) and inject privacy/travel-mode filters into shared query helpers used by other modules. Add integration tests that assert hidden data stays hidden under travel/duress.
- **Ship real trust and approval controls:** Implement MFA lookups via Keycloak Admin API, OS-version allowlists, jailbreak/root detection, push-approval expiry + rate-limits, and device attestation where supported. Backfill trust factors for existing devices.
- **Vault key strategy:** Move to client-held keys with per-item salts stored server-side; document recovery flows and rotation; block server-side decrypt paths. Add AV scanning, size limits, and share-token TTL signing.
- **Digital will/duress guardrails:** Require trustee verification + multi-party approval, sign requests with short-lived tokens, and scope data release to explicit collections. Add irreversible audit events and cancellation/appeal flow.
- **Cross-org search/feed safety:** Add an indexing plan (per-org indices), mandatory org filters, pagination, abuse throttles, and event schemas for feeds. Provide a shared “permission-aware search” utility that all endpoints must use.
- **Permission registration and testing:** Register `has_permission`/`get_permission_query_conditions` for all User doctypes in `hooks.py`; add unit tests for owner-only enforcement and cross-org leakage.
- **Reduce hook side effects:** Remove commits from `Person.after_insert`; handle failures gracefully and queue profile creation if needed.
- **Fill missing PRD items:** Add passkey/WebAuthn design, contact auto-match approach, gamification schema, reputation scoring inputs/decay, AI memory lifecycle, and health/wearable integration plan—or explicitly de-scope in roadmap.

## Will the current architecture enable clear implementation?
- For P0 foundations (profile, org switcher, devices, sessions, notifications, deletion/export), the architecture is mostly sufficient with hardening.
- P1 security/privacy (travel mode, push approve, privacy dashboard, vault, cross-org features) require additional enforcement layers, clear data taxonomy, and real integrations to avoid regressions.
- P2 AI/voice/health/gamification items need new design work; implementing them now would be brittle without clarified data flows, consent models, and provider contracts.

