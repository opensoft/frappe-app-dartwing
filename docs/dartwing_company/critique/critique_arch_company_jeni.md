# Critique: Dartwing Company Architecture

Scope reviewed: `dartwing_core/dartwing_core_arch.md`, `dartwing_company_arch.md`, `dartwing_company_executive_summary.md`, `dartwing_company_prd.md`

## Strengths
- Clear overlay strategy on ERPNext/HRMS/CRM/Health/Drive; avoids forking core apps and leans on links/hooks.
- Modular structure (ops, crm, hr, healthcare, integrations, api) aligns with feature groupings and makes ownership boundaries explicit.
- Multi-tenant awareness: org-scoped settings/feature flags, and reliance on dartwing_core’s hybrid org model.
- API-first and event-driven mindset matches Flutter/external client needs; integration diagrams show intended data flow.
- Dependency matrix lists required vs optional modules, setting expectations for the stack.

## Weaknesses / Gaps
- Missing concrete schemas: no JSON/controller detail for key doctypes (Dispatch Job, Conversation*, Appointment, Ticket, Vault, Workflow, etc.), so integration promises are not enforceable.
- Permissions under-specified: only sample query; no `user_permission_doctypes`, no Socket.IO/job enforcement, no PHI separation for healthcare mode.
- Offline/real-time sync undefined: PRD promises offline forms/mobile ops, but there is no delta feed, conflict policy, or attachment/tombstone handling for company doctypes.
- Optional dependency ambiguity: many features assume ERPNext/HRMS/CRM/Health, yet they’re marked “optional”; no degraded-mode behavior or preflight checks.
- Operational risk: ambitious AI (Receptionist, Growth, RAG) plus routing/geo/Stripe without sequencing, SLOs, or error budgets.
- Multi-tenancy depth: no hierarchy/parent-org support, shared resources, per-tenant rate limits, or Drive namespace isolation.
- Testing/rollout not covered: no seed data, migrations, sandbox flags, or rollout plan per org/tenant.

## PRD Feature Fit (ease vs difficulty)
**Easier**
- CRM-01 Client Portal: portal scaffolding exists; depends on solid auth/permissions.
- CRM-02 Document Vault: Drive integration makes this straightforward with audit trails.
- CRM-03 Appointment Booker: calendar + Stripe + Contact/Deal links are feasible.
- OPS-03 Workflow Builder: engine/builder folders exist; avoid clashing with Frappe Workflow.
- OPS-08 Broadcast Alerts: broadcaster in place; add provider limits and org rate limits.
- OPS-06 Status Boards: mostly composed views over ERPNext/CRM data.

**Moderate**
- OPS-02 Universal Inbox: channel abstraction exists; needs identity matching, dedupe, and backpressure.
- OPS-05 Mobile Forms: builder/render present; offline schema/versioning still undefined.
- OPS-07 Knowledge Base: indexing + embeddings + ACL; harder with PHI.
- CRM-04 Tickets / CRM-06 SLA: requires clock source, pause rules, and multi-channel triggers.
- HR-01 Shift Scheduler / HR-02 Geo Clock-In: HRMS sync outlined; must add geofence validation and tamper resistance.

**Hard / High-Risk**
- OPS-01 AI Receptionist: real-time voice latency, call control, fallback scripting, compliance recording.
- OPS-04 Smart Dispatch: accurate geocode/drive-time, qualification blocking, optimization scalability.
- OPS-12 Ask Anything: vector search with strict ACL; risk of leakage.
- CRM-07 Growth Orchestrator: depends on leadgen quality, ICP UX, and CRM ROI tracking.
- Healthcare overlay: PHI segregation, consent, audit retention; needs dedicated role model.

## Recommendations
1) Publish doctype schemas/controllers: define Dispatch Job, Conversation*, Appointment, Ticket, Vault, Workflow, etc., with links to Organization/Company/Customer/Employee and indexes on `organization`, `customer`, `status`, `assigned_to`, `modified`.
2) Harden permissions: add `user_permission_doctypes` to all org-scoped doctypes; use shared permission helpers across REST, Socket.IO, background jobs; define health-mode roles/PHI access.
3) Define degraded modes: for each optional dependency, specify feature gating, UI messaging, and startup checks; fail closed when required apps are absent.
4) Add offline/sync spec for company doctypes: align with core sync (change feed, batch upsert, tombstones, conflict rules, attachments).
5) Sequence delivery: waves—(a) Portal + Vault + Appointments + basic Tickets; (b) Inbox + Workflow + Broadcast; (c) Dispatch + Geo Clock-In; (d) AI Receptionist + Growth + Ask Anything—with dependency readiness gates.
6) Observability/safety: per-org rate limits for inbox/broadcast; DLQ for channel failures; metrics on assignment success, SLA breaches, sync lag; alerting on spikes.
7) Multi-tenancy/hierarchy: add parent_org support (aligned with dartwing_core guardrails), org-aware search indices, and Drive folder namespaces per tenant.
8) Compliance: define retention/soft-delete for conversations/voice/tickets; audit logs for Vault and health data; consent tracking for Patient/Contact flows.

## Implementability Verdict
- With published schemas, stricter permissions, and a sync/degraded-mode plan, the architecture can deliver the “easy” and many “moderate” PRD features. High-risk items (AI Receptionist, Smart Dispatch optimization, global search with ACLs, healthcare PHI) require deeper technical design, performance SLOs, and compliance models before committing. Strengthening data models, permission enforcement, and rollout sequencing will materially reduce delivery risk and make the PRD achievable. 
