# Master Fix Plan v2.0: Background Job Engine (011-background-job-engine)

**Created By:** Director of Engineering / Lead Developer
**Date:** 2025-12-16
**Version:** 2.0 (Post-Review Iteration)
**Branch:** `011-background-job-engine`
**Module:** `dartwing_core`

---

## Overview

This document provides a detailed implementation plan for all **new issues** identified in MASTER_REVIEW.md v2.0, following verification that all original P1/P2 items from v1.0 have been successfully implemented.

**Status Summary:**
- Original P1 (8 tasks): ✅ ALL VERIFIED COMPLETE
- Original P2 (8 tasks): ✅ ALL VERIFIED COMPLETE (P2-001 deferred by design)
- **NEW P1 (3 tasks): 🔄 IN PROGRESS**
- **NEW P2 (3 tasks): ⏳ PENDING APPROVAL**
- **NEW P3 (6 tasks): ⏳ DEFERRED TO POST-MERGE**

**Execution Rule:** Execute P1 fixes first. Wait for approval before proceeding to P2 or P3.

---

## P1: Critical Issues (3 Tasks) - APPROVED FOR IMPLEMENTATION

### Task 1: Add Socket.IO Permission Validation

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-NEW-001 |
| **Source Reviewer** | sonn45 |
| **Severity** | CRITICAL - Security |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/progress.py` |

**Problem:** `publish_job_progress()` (lines 101-128) and `publish_job_status_changed()` (lines 131-167) broadcast Socket.IO events without validating:
1. The organization exists in the database
2. The job belongs to the claimed organization

An attacker could spoof organization IDs to receive cross-tenant job updates, violating multi-tenant isolation.

**Plan:**
1. Add `_validate_broadcast_params(job_id, organization)` helper function
2. Call validation at start of both broadcast functions
3. Silently return on validation failure (don't expose validation to attackers)

**Implementation:**
```python
def _validate_broadcast_params(job_id: str, organization: str) -> bool:
    """
    Validate job exists and belongs to claimed organization.

    Returns False (invalid) if:
    - Organization doesn't exist
    - Job doesn't exist
    - Job belongs to a different organization
    """
    if not frappe.db.exists("Organization", organization):
        return False
    job_org = frappe.db.get_value("Background Job", job_id, "organization")
    return job_org == organization
```

**Compliance Note:**
- Architecture Section 8.2.1 requires "Permission Query Hook" for all data access
- PRD C-01 mandates "Complete data isolation between Organizations (no data leakage)"

---

### Task 2: Fix Orphaned Dependent Jobs

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-NEW-002 |
| **Source Reviewer** | sonn45 |
| **Severity** | CRITICAL - Functional |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/executor.py` |

**Problem:** In `_check_dependency()` (lines 93-131), when a parent job is still in progress, the function returns `False` without setting `next_retry_at`. The job remains in "Queued" status forever without being re-picked by the scheduler.

**Plan:**
1. Add import for `add_to_date` from `frappe.utils`
2. Set `next_retry_at` to 30 seconds in future when dependency is pending
3. Commit the change so scheduler can pick it up

**Implementation:**
```python
# When parent is still in progress (Pending/Queued/Running):
if parent_status in ["Pending", "Queued", "Running"]:
    # Parent still in progress - schedule retry
    job.next_retry_at = add_to_date(now_datetime(), seconds=30)
    job.save(ignore_permissions=True)
    frappe.db.commit()
    return False
```

**Compliance Note:**
- PRD C-16 explicitly requires "guaranteed execution with progress UI"
- Jobs silently stuck in Queued status violates this requirement

---

### Task 3: Fix JSON Serialization Instability

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-NEW-003 |
| **Source Reviewer** | gemi30 |
| **Severity** | CRITICAL - Stability |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** Line 362 uses `json.dumps(params, sort_keys=True)` which crashes with `TypeError` if `params` contains `datetime`, `date`, or `Decimal` objects (common in Frappe job parameters).

**Plan:**
1. Replace `json.dumps()` with `frappe.as_json()` which handles Frappe-specific types
2. Ensure `sort_keys=True` is passed for deterministic hashing

**Implementation:**
```python
def generate_job_hash(job_type: str, organization: str, params: dict) -> str:
    """
    Generate unique hash for duplicate detection.

    Uses frappe.as_json() for stable serialization of Frappe types
    (datetime, date, Decimal, etc.).
    """
    params_json = frappe.as_json(params, sort_keys=True)
    content = f"{job_type}:{organization}:{params_json}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]
```

**Compliance Note:**
- `frappe.as_json()` is the idiomatic Frappe pattern per Architecture Doc
- Handles datetime, date, Decimal, and other Frappe-specific types

---

## P2: Medium Issues (3 Tasks) - PENDING APPROVAL

### Task 4: Document RQ Cancellation Limitation (P2-001)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-001 |
| **Status** | DEFERRED - GitHub Issue #34 tracks implementation |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Plan:** Add explicit documentation to `cancel_job()` docstring noting that cancellation is cooperative via `is_canceled()` polling, not immediate RQ job termination.

---

### Task 5: Remove Premature Commit (P2-002)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-002 |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Plan:** Remove explicit `frappe.db.commit()` from `_enqueue_job()` line 525. The `enqueue_after_commit=True` parameter already handles transaction boundary.

---

### Task 6: Add Redis Failure Handling (P2-003)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-003 |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Plan:** Wrap Redis lock acquisition in try/except and throw user-friendly error on Redis connection failure.

---

## P3: Low Priority (6 Tasks) - DEFERRED TO POST-MERGE

| Task | Issue ID | Description |
|------|----------|-------------|
| 7 | P3-001 | Refactor `submit_job()` complexity |
| 8 | P3-002 | Add return type hints to public API |
| 9 | P3-003 | Add rate limit window cap (max 24 hours) |
| 10 | P3-004 | Add progress update throttling |
| 11 | P3-005 | Extract magic numbers to config |
| 12 | P3-006 | Include `retry_attempt` in job history |

---

## Verification of Original FIX_PLAN v1.0 Items

### P1 Original (All 8 VERIFIED ✅)

| Task | Issue | Status | Evidence |
|------|-------|--------|----------|
| 1 | SQL Injection | ✅ VERIFIED | Parameterized queries in metrics.py |
| 2 | SIGALRM Timeout | ✅ VERIFIED | ThreadPoolExecutor in executor.py |
| 3 | User Field Reference | ✅ VERIFIED | Person→Org Member chain in engine.py |
| 4 | Database Indexes | ✅ VERIFIED | Indexes in background_job.json |
| 5 | Duplicate Race Condition | ✅ VERIFIED | Distributed lock in engine.py |
| 6 | Cancel Race Condition | ✅ VERIFIED | SELECT FOR UPDATE in engine.py |
| 7 | Scheduler Hooks | ✅ VERIFIED | Hooks present in hooks.py |
| 8 | State Machine Cleanup | ✅ VERIFIED | Terminal deletion in cleanup.py |

### P2 Original (All 8 VERIFIED ✅)

| Task | Issue | Status | Evidence |
|------|-------|--------|----------|
| 9 | RQ Cancel | ⏸️ DEFERRED | GitHub Issue #34 |
| 10 | enqueue_after_commit | ✅ VERIFIED | Present at line 551 |
| 11 | Duplicate hooks.py Keys | ✅ VERIFIED | No duplicates |
| 12 | Falsy Config Values | ✅ VERIFIED | `is not None` checks |
| 13 | Batched Cleanup | ✅ VERIFIED | Batch commits in cleanup.py |
| 14 | Progress Commit | ✅ VERIFIED | Documented as eventual |
| 15 | Org Field on Log | ✅ VERIFIED | Field with fetch_from |
| 16 | Socket.IO Room Scoping | ✅ VERIFIED | `room=f"org:{organization}"` |

---

## Execution Log

### P1 Execution (2025-12-16)

| Task | Start | End | Status |
|------|-------|-----|--------|
| Task 3 (JSON) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |
| Task 1 (Socket.IO) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |
| Task 2 (Orphaned Jobs) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |

### Changes Made

**engine.py (P1-NEW-003):**
- `generate_job_hash()`: Replaced `json.dumps(params, sort_keys=True)` with `frappe.as_json(params, sort_keys=True)`
- Added docstring noting Frappe type handling

**progress.py (P1-NEW-001):**
- Added `_validate_broadcast_params(job_id, organization)` helper function
- Added validation call at start of `publish_job_progress()`
- Added validation call at start of `publish_job_status_changed()`

**executor.py (P1-NEW-002):**
- Added import: `add_to_date` from `frappe.utils`
- In `_check_dependency()`: Added `next_retry_at` scheduling when parent is still in progress
- Prevents orphaned jobs that would wait forever

---

### P2 Execution (2025-12-16)

| Task | Start | End | Status |
|------|-------|-----|--------|
| Task 4 (RQ Doc) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |
| Task 5 (Commit) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |
| Task 6 (Redis) | 2025-12-16 | 2025-12-16 | ✅ COMPLETE |

### P2 Changes Made

**engine.py (P2-001, P2-002, P2-003):**
- `cancel_job()`: Added docstring noting cooperative cancellation via `is_canceled()` and GitHub Issue #34
- `_enqueue_job()`: Removed explicit `frappe.db.commit()`, added docstring explaining why
- `_deduplication_lock()`: Wrapped lock acquisition in try/except with user-friendly error message

---

*Plan approved by user on 2025-12-16*
*P1 execution completed on 2025-12-16*
*P2 execution completed on 2025-12-16*
*Reference: MASTER_REVIEW.md v2.0*
