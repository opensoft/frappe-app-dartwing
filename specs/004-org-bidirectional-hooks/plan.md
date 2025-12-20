# Implementation Plan: Organization Bidirectional Hooks

**Branch**: `004-org-bidirectional-hooks` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-org-bidirectional-hooks/spec.md`

## Summary

Implement server-side hooks that automatically create and manage the bidirectional relationship between Organization and its concrete type records (Family, Company, Association, Nonprofit). When an Organization is created, the corresponding concrete type record is auto-created with proper linkage. When an Organization is deleted, the concrete type is cascade-deleted. The implementation uses Frappe document hooks (`after_insert`, `on_trash`) and provides whitelisted API methods for retrieving Organization data with nested concrete type details.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.utils.logger
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with Frappe test fixtures
**Target Platform**: Frappe server (Linux)
**Project Type**: Backend module (dartwing_core Frappe app)
**Performance Goals**: Retrieval within 500ms, 100 concurrent Organization creations without corruption
**Constraints**: Atomic transactions, system-privilege execution for hooks, audit logging required
**Scale/Scope**: Supports all four org types (Family, Company, Association, Nonprofit)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Single Source of Truth | PASS | Uses existing Organization doctype with org_type field |
| Technology Stack | PASS | Python 3.11+, Frappe 15.x, MariaDB 10.6+ |
| Architecture Patterns | PASS | Uses Frappe doctype system and document hooks |
| API-First | PASS | Whitelisted methods exposed via `/api/method/` |
| Security & Compliance | PASS | Audit logging for hook executions, system privilege execution |
| Code Quality | PASS | Will include tests for business logic |
| Naming Conventions | PASS | snake_case for fieldnames, PascalCase for doctypes |
| API Design | PASS | Uses `/api/method/dartwing.{module}.{method}` pattern |

**Constitution Check Result**: PASS - No violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/004-org-bidirectional-hooks/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
└── dartwing_core/
    ├── dartwing_core/
    │   ├── doctype/
    │   │   └── organization/
    │   │       ├── organization.json      # Doctype definition (existing)
    │   │       └── organization.py        # Controller with hooks + API methods
    │   └── hooks.py                       # Frappe hooks registration
    └── tests/
        └── test_organization_hooks.py     # Hook behavior tests
```

**Structure Decision**: Single Frappe app module (dartwing_core) with hooks implemented directly in the Organization doctype controller (`organization.py`). This keeps hook logic co-located with the doctype for simplicity and discoverability.

## Complexity Tracking

> No constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
