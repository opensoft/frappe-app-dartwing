# Implementation Plan: Background Job Engine

**Branch**: `011-background-job-engine` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/011-background-job-engine/spec.md`
**PRD Reference**: C-16 (Section 5.10)

## Summary

The Background Job Engine provides guaranteed asynchronous task execution for Dartwing. It extends Frappe's built-in background jobs infrastructure with:
- Real-time progress tracking via Socket.IO
- Intelligent retry with error classification (transient vs permanent)
- Multi-tenant job isolation scoped to Organization
- Dead letter queue for failed job review
- Operational metrics for monitoring

This is a foundational platform feature that blocks C-04 (Offline-First), C-10 (Notifications), C-24 (Fax Engine), and C-25 (Maintenance Scheduler).

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.background_jobs, Redis/RQ, Socket.IO
**Storage**: MariaDB 10.6+ via Frappe ORM (job metadata persistence)
**Testing**: pytest with frappe.test_runner
**Target Platform**: Linux server (Frappe deployment)
**Project Type**: Backend service extension (Frappe app module)
**Performance Goals**:
- Job submission acknowledgment < 1 second
- Progress updates visible within 2 seconds
- 100+ concurrent jobs per organization
**Constraints**:
- Must integrate with existing Frappe background jobs (not replace)
- Multi-tenant isolation via Organization scoping
- 30-day job metadata retention
**Scale/Scope**: Multi-organization SaaS, unlimited job types

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Single Source of Truth | PASS | Job metadata stored in single Background Job doctype |
| 2. Technology Stack | PASS | Python 3.11+, Frappe 15.x, MariaDB 10.6+ |
| 3. Architecture Patterns | PASS | Repository pattern for job access, extends Frappe doctype system |
| 4. Cross-Platform Requirements | PASS | Backend service - all clients access via REST API |
| 5. Security & Compliance | PASS | Organization-scoped isolation, audit logging for state transitions |
| 6. Code Quality Standards | PASS | Tests required for job engine logic |
| 7. Naming Conventions | PASS | Doctypes: BackgroundJob, JobType; fields: snake_case |
| 8. API Design | PASS | Whitelisted methods via `/api/method/dartwing.jobs.*` |
| 9. Offline-First | N/A | Backend service - offline handled by sync layer |
| 10. AI Integration | N/A | Not an AI feature |
| 11. Parallel Development | PASS | Branch 011 created, will push after planning |

**Gate Result**: PASS - No violations, proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/011-background-job-engine/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── api.md           # REST API specification
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   ├── doctype/
│   │   ├── background_job/
│   │   │   ├── background_job.json      # Job metadata doctype
│   │   │   ├── background_job.py        # Job controller
│   │   │   └── test_background_job.py   # Unit tests
│   │   ├── job_type/
│   │   │   ├── job_type.json            # Job type configuration
│   │   │   └── job_type.py              # Job type controller
│   │   └── job_execution_log/
│   │       ├── job_execution_log.json   # Audit log doctype
│   │       └── job_execution_log.py     # Log controller
│   ├── background_jobs/
│   │   ├── __init__.py
│   │   ├── engine.py                    # Core job engine
│   │   ├── executor.py                  # Job execution logic
│   │   ├── retry.py                     # Retry policy & error classification
│   │   ├── progress.py                  # Progress tracking via Socket.IO
│   │   ├── metrics.py                   # Operational metrics
│   │   └── dead_letter.py               # Dead letter queue handling
│   └── api/
│       └── jobs.py                      # Whitelisted API methods
├── hooks.py                             # Register background job hooks

dartwing/tests/
├── unit/
│   ├── test_job_engine.py
│   ├── test_retry_policy.py
│   └── test_error_classification.py
└── integration/
    ├── test_job_submission.py
    ├── test_job_progress.py
    └── test_multi_tenant_isolation.py
```

**Structure Decision**: Extends dartwing_core module with new doctypes (BackgroundJob, JobType, JobExecutionLog) and a dedicated background_jobs package for engine logic. API exposed via dartwing_core/api/jobs.py with @frappe.whitelist() methods.

## Complexity Tracking

No constitution violations requiring justification.
