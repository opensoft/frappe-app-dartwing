# Architecture Critique: Dartwing Core Module

**Date:** November 2025
**Reviewer:** Antigravity Agent (Gemi)
**Status:** Comprehensive Review against PRD v2.0

## Executive Summary

The **Dartwing Core** architecture provides a solid, scalable foundation for the "Universal Platform" vision. The move to a **Hybrid Organization Model** (Thin Reference + Concrete Types) is a critical architectural win that solves the "God Object" problem while maintaining a unified identity layer.

**Verdict:** The architecture is **Strategically Sound** and **Feature-Complete**, but **Implementation Risk is High** in specific areas (Sync, AI Merge, Global Search).

- **Sound:** The core data model, authentication (Keycloak), and multi-tenancy approach are industry-standard and robust.
- **Risky:** The PRD promises "AI Smart Merge" and "Sub-second Global Search" which require significant infrastructure complexity that is under-specified in the current architecture document.

## Strengths

1.  **Hybrid Organization Model (C-01):**

    - _Why it's good:_ Decoupling the "Identity" (`Organization`) from the "Implementation" (`Family`, `Company`) allows for infinite extensibility. You can add a `DAO` or `GovernmentAgency` type later without touching the core schema.
    - _Benefit:_ Solves the "Sparse Table" problem and ensures strict type safety for vertical-specific logic.

2.  **Unified "Person" Identity (C-03):**

    - _Why it's good:_ Separating `User` (Login) from `Person` (Profile) and linking them allows one human to have multiple roles across different organizations without duplicating their profile data.
    - _Benefit:_ Enables the "Personal vs Business Identity" requirement elegantly.

3.  **API-First Design (C-06, C-19):**
    - _Why it's good:_ Forcing all logic through `@frappe.whitelist()` ensures that the Flutter mobile app and the Web UI are always in sync. The "UI Generation" from DocTypes is a massive productivity booster.

## Weaknesses & Critical Risks

### 1. "AI Smart Merge" Risk (High Severity)

The PRD (C-04) and Sync Spec mention "AI Smart Merge" for conflict resolution.

- **The Risk:** AI (LLMs) are non-deterministic. If an AI "hallucinates" during a merge (e.g., inventing a phone number or dropping a paragraph from a note), it causes **silent data corruption**.
- **Mitigation:**
  - **Strict Confidence Thresholds:** Only auto-merge if AI confidence > 98%.
  - **Original Retention:** Always keep the conflicting versions in a `Version` history so a human can rollback an AI merge.
  - **Human Fallback:** The default should be "Ask the User", with AI only as a suggestion, unless the conflict is trivial (e.g., whitespace).

### 2. Global Search Scalability (C-09) (Medium Severity)

The PRD promises "Sub-second search across millions of records".

- **The Risk:** The architecture lists MariaDB/PostgreSQL. Standard SQL `LIKE` queries or even Full-Text indexes will choke on multi-tenant data at scale, especially with complex permission filtering.
- **Mitigation:** The architecture _must_ explicitly include a dedicated search engine (OpenSearch, Meilisearch, or Elasticsearch) in the stack. SQL is not enough for this requirement.

### 3. Compliance Mode Infrastructure (C-13) (Medium Severity)

The PRD promises "HIPAA/SOC2 Mode" with "Object Lock" and "Encryption".

- **The Risk:** These are infrastructure-level features, not just code. You cannot "code" S3 Object Lock in Python; it must be provisioned at the bucket level.
- **Mitigation:** The architecture needs an **Infrastructure-as-Code (IaC)** component (Terraform/Pulumi) to provision separate, compliant infrastructure for Enterprise tenants.

## Feature Implementation Analysis (Easy vs Hard)

| Feature                   | Difficulty | Implementation Analysis                                                                                                                      |
| :------------------------ | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| **C-01 Multi-Tenancy**    | **Easy**   | **Why:** The Hybrid model makes this straightforward. Frappe's permission system handles the isolation well.                                 |
| **C-02 One-Click Create** | **Easy**   | **Why:** It's just a transaction wrapper around creating two DocTypes.                                                                       |
| **C-06 UI Generation**    | **Easy**   | **Why:** Frappe metadata is rich. Mapping it to Flutter widgets is a solved problem in this framework.                                       |
| **C-17 Role Permissions** | **Easy**   | **Why:** Frappe's Role/UserPermission system is mature and powerful.                                                                         |
| **C-25 Task Scheduler**   | **Easy**   | **Why:** Frappe's background jobs (RQ) are reliable.                                                                                         |
| **C-04 Offline Sync**     | **Hard**   | **Why:** "Offline-First" is always hard. Handling schema changes, large initial syncs, and delta calculations requires a very robust engine. |
| **C-09 Global Search**    | **Hard**   | **Why:** Requires syncing data to a search engine + enforcing permissions at query time (which is very hard in search engines).              |
| **C-13 Compliance Mode**  | **Hard**   | **Why:** Requires deep infrastructure integration (AWS/Azure APIs) and rigorous audit logging that cannot be bypassed.                       |
| **C-24 Fax-over-IP**      | **Medium** | **Why:** The logic is simple (API call to Telnyx), but reliability (retries, webhooks, PDF rendering) adds complexity.                       |

## Robustness & Reliability Improvements

### 1. Explicit Search Engine Requirement

**Recommendation:** Add **Meilisearch** or **OpenSearch** to the official stack for C-09.

- **Why:** To support "Sub-second search" with typo-tolerance and faceting. SQL cannot do this well.

### 2. "Safe" AI Merge Protocol

**Recommendation:** Update the Sync Spec to mandate **"Human-in-the-loop"** for AI merges by default.

- **Change:** The AI should produce a _suggested_ merged document, but present it to the user as "Review Conflicts" unless the confidence is near-perfect. Silent AI merges are too dangerous for business data.

### 3. Infrastructure-Aware Architecture

**Recommendation:** Add a section on **Tenant Provisioning**.

- **Why:** For C-13 (Compliance), creating a new Organization might need to trigger a Terraform script to spin up a dedicated S3 bucket with Object Lock enabled. This "Control Plane" logic needs to be part of the Core architecture.

### 4. Hook Reliability (Reconciliation)

**Recommendation:** As noted in previous critiques, the "Reconciliation Job" is critical.

- **Addition:** Add a **"Transaction Outbox"** pattern for the hooks. Instead of just firing logic in `after_insert`, write an event to an `Outbox` table. A background worker processes the Outbox. This guarantees that if the hook logic fails (e.g., external API down), it can be retried without losing the event.

## Conclusion

Dartwing Core is well-positioned to be the "Operating System" for these applications. The **Hybrid Model** is a major success. The primary challenges are now **Operational**: scaling search, ensuring sync reliability, and managing the infrastructure complexity of the Compliance features.
