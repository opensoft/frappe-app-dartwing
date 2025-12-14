# Implementation Plan: User Permission Propagation

**Branch**: `005-user-permission-propagation` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-user-permission-propagation/spec.md`

## Summary

Implement automatic User Permission propagation when Org Member records are created/deleted/modified. This is the security foundation enabling multi-org data isolation - users only see data from Organizations they belong to. The system creates User Permissions for both the Organization and its concrete type (Family/Company/Association/Nonprofit), handles edge cases like missing User links, and provides permission query condition functions for list filtering and has_permission functions for single document access checks.

Key capabilities:
- Automatic User Permission creation on Org Member insert
- Automatic User Permission removal on Org Member delete or status change to Inactive
- Permission query condition functions for Organization and all concrete types
- System Manager bypass for administrative access
- Audit logging for all permission lifecycle events

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.permissions
**Storage**: MariaDB 10.6+ (via Frappe ORM)
**Testing**: pytest with frappe.tests.utils
**Target Platform**: Frappe Server (Linux), accessible via REST API from Flutter clients
**Project Type**: Frappe App (dartwing_core module)
**Performance Goals**: Permission creation <1s synchronous (SC-002), permission checks <50ms latency (SC-006)
**Constraints**: API-first (all logic via @frappe.whitelist()), audit logging for compliance (FR-012)
**Scale/Scope**: All users with Org Member records; scales with number of org memberships

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Single Source of Truth | PASS | User Permission is Frappe's standard permission mechanism; no parallel system |
| Technology Stack | PASS | Python/Frappe backend, MariaDB storage per constitution |
| Architecture Patterns | PASS | Using Frappe doctype hooks and permission system |
| API-First Development | PASS | Permission functions callable via API; no UI-only logic |
| Security & Compliance | PASS | Audit logging for permission events (FR-012), role-based access |
| Code Quality Standards | PASS | Will include complete field definitions and tests |
| Naming Conventions | PASS | Functions: snake_case, hooks registered per Frappe convention. DocType display name: "Org Member" (with space); folder: `org_member`; class: `OrgMember` |
| Cross-Platform Requirements | N/A | Backend security layer; clients consume filtered data |
| Offline-First | N/A | Backend permission logic; offline handled by Flutter clients |

**Gate Result**: PASS - No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/005-user-permission-propagation/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── permissions-api.yaml  # Permission helper API endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   └── doctype/
│       └── org_member/              # Feature 3 dependency - DocType must exist
│           ├── __init__.py          # (not created by this feature)
│           ├── org_member.json      # (not created by this feature)
│           └── org_member.py        # (not modified - hooks registered in dartwing/hooks.py)
│
├── permissions/
│   ├── __init__.py
│   ├── organization.py              # Organization permission query conditions
│   ├── family.py                    # Family permission query conditions
│   ├── company.py                   # Company permission query conditions
│   ├── association.py               # Association permission query conditions
│   ├── nonprofit.py                 # Nonprofit permission query conditions
│   └── helpers.py                   # Shared permission utilities
│
├── utils/
│   └── permission_logger.py         # Audit logging for permission events
│
├── hooks.py                         # Register permission hooks
│
└── tests/
    ├── test_permission_propagation.py    # Permission create/remove tests
    ├── test_permission_query.py          # List filtering tests
    └── test_permission_access.py         # Single doc access tests
```

**Structure Decision**: Following established dartwing_core module pattern. Permission logic centralized in `dartwing/permissions/` module with separate files per doctype for maintainability. Hooks registered in `dartwing/hooks.py` following Frappe convention.

## Dependencies

This feature depends on:
- **Feature 1: Person DocType** - Person.frappe_user field for User lookup
- **Feature 3: Org Member DocType** - Org Member record triggers permission propagation
- **Organization DocType** - Existing, with linked_doctype/linked_name fields

## Risks & Decisions

### Risk 1: Missing Person.frappe_user Link
**Risk**: Person record may not have a linked Frappe User at time of Org Member creation
**Impact**: MEDIUM - Permission cannot be created without User
**Mitigation**: FR-007 specifies skip gracefully and log; no error thrown

**Decision**: Check for frappe_user before creating User Permission; log skip event for debugging

### Risk 2: Orphaned User Permissions
**Risk**: If Org Member deletion fails mid-process, User Permissions may remain
**Impact**: LOW - User has extra access until cleanup
**Mitigation**: Delete User Permissions before Org Member in on_trash hook

**Decision**: Use frappe.db.delete for atomic permission removal

### Risk 3: Multi-Org Performance
**Risk**: Users with many organizations may have slow permission queries
**Impact**: LOW - IN clause with many values can be slow
**Mitigation**: Index on User Permission (user, allow, for_value); Frappe provides this by default

**Decision**: Monitor query performance; add index if needed

## Complexity Tracking

> No Constitution Check violations - table not required

## Phase 0 Output Reference

See [research.md](./research.md) for:
- Frappe User Permission system patterns
- permission_query_conditions hook patterns
- has_permission hook patterns
- Audit logging best practices in Frappe

## Phase 1 Output Reference

See:
- [data-model.md](./data-model.md) - User Permission entity usage (Frappe built-in)
- [contracts/permissions-api.yaml](./contracts/permissions-api.yaml) - Permission helper API endpoints
- [quickstart.md](./quickstart.md) - Developer setup guide
