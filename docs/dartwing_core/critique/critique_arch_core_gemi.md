# Architecture Critique: Dartwing Core (v2 - Hybrid Model)

**Date:** November 2025
**Reviewer:** Antigravity Agent
**Status:** Updated after Hybrid Model Refactoring

## Executive Summary

The refactored Dartwing architecture represents a significant maturation from the initial "Universal Organization" concept. By adopting a **Hybrid Architecture (Thin Reference + Concrete Types)**, the system effectively mitigates the "God Object" risk while retaining the benefits of a unified identity layer.

The addition of explicit specifications for **Offline Sync** and **Organization Integrity Guardrails** demonstrates a high level of architectural rigor. The primary remaining risks have shifted from _data modeling_ flaws to _implementation complexity_—specifically regarding bidirectional hook maintenance and distributed synchronization.

## Strengths

### 1. Hybrid Data Model (Major Improvement)

- **Best of Both Worlds:** The decision to split `Organization` into a thin shell and concrete 1:1 extensions (`Family`, `Company`, etc.) is the correct architectural choice. It solves the "sparse table" problem and allows for strict type safety (e.g., Payroll linking only to Companies) while maintaining polymorphic linking for shared entities (Tasks, Notes).
- **Future Proof:** Adding a new organization type (e.g., `DAOs` in 2028) no longer requires modifying the core `Organization` schema, adhering to the Open-Closed Principle.

### 2. Robust Integrity Guardrails

- **Self-Healing:** The inclusion of a "Reconciliation Job" and "Atomic Creation" logic in `org_integrity_guardrails.md` shows proactive thinking about data consistency.
- **Immutability:** Enforcing `org_type` immutability is a critical decision that simplifies downstream logic significantly.

### 3. Detailed Sync Specification

- **Deterministic Behavior:** The `offline_real_time_sync_spec.md` moves beyond vague promises to a concrete protocol (Change Feeds, Write Queues, Tombstones).
- **Conflict Strategy:** Explicitly defining "Last-Write-Wins" with an audit trail as the default, while allowing for CRDT-like field-level merges for high-value data, is a pragmatic approach.

## Weaknesses & Risks

### 1. Hook Complexity & Race Conditions (Medium)

- **Risk:** The bidirectional linking (Organization ↔ Concrete Type) relies heavily on server-side hooks (`after_insert`, `on_trash`). In a high-concurrency environment, or during bulk imports, these hooks could fail or race, leading to "Orphaned" organizations or "Headless" concrete types.
- **Mitigation:** The proposed "Reconciliation Job" is essential. Ensure it is idempotent and performant.

### 2. Permission Model Complexity (Medium)

- **Risk:** The permission flow (`User` → `Org Member` → `Organization` → `Concrete Type`) is sophisticated but complex to debug. A misconfiguration in the `User Permission` propagation could leave a user unable to see their own Family details.
- **Mitigation:** Automated permission testing (as suggested in the PRD) is mandatory. Visual tools to "Explain Permissions" for a given user/doc pair would be valuable.

### 3. Offline Sync Implementation (High)

- **Risk:** While the _spec_ is good, the _implementation_ of a reliable offline sync engine in Flutter + Frappe is non-trivial. Handling large initial syncs (pagination), binary assets (attachments), and schema changes (migrations) will be pain points.
- **Mitigation:** Build a "Sync Simulator" test suite that introduces network lag, drops packets, and creates conflicts to verify the system's resilience before production.

## Recommendations

1.  **Implement "Dry Run" for Reconciliation:** The integrity repair job should have a mode where it only reports issues without fixing them, to allow operators to verify logic before auto-healing.
2.  **Sync Protocol Versioning:** The Sync Spec should include a version handshake. If the server schema changes, older clients must know to force a full re-sync rather than applying incompatible deltas.
3.  **Performance Benchmarking for Hooks:** Test the `after_insert` hook latency. If creating an Organization takes 2s because of multiple DB roundtrips, it will degrade the user experience. Consider moving non-critical hook logic to background jobs.
4.  **Developer Experience (DX):** With the Hybrid model, developers need to know _which_ ID to use. Clear guidelines (e.g., "Always link to Concrete ID for domain logic, Organization ID for generic features") should be enforced via linter rules or code review checklists.

## Conclusion

The architecture is now in a **highly robust state**. The structural flaws have been resolved. The focus must now shift to **execution quality**—specifically the reliability of the sync engine and the correctness of the permission hooks.
