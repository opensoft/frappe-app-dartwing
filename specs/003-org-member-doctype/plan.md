# Implementation Plan: Org Member DocType

**Branch**: `003-org-member-doctype` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-org-member-doctype/spec.md`

## Summary

Create the Org Member DocType that links Person to Organization with Role assignment. This enables multi-user functionality by establishing membership relationships with status tracking (Active/Inactive/Pending), role validation against organization type, and lifecycle management including soft-cascade on Person deletion and last-supervisor protection.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.fixtures
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with frappe.tests.IntegrationTestCase
**Target Platform**: Frappe/ERPNext server (Linux)
**Project Type**: Single Frappe app (dartwing)
**Performance Goals**: Member list retrieval <2s (SC-004), member addition <30s (SC-001)
**Constraints**: Must integrate with existing Person, Organization, Role Template doctypes
**Scale/Scope**: Supports multiple organizations per person, one membership record per (Person, Organization) pair

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Single Source of Truth | ✅ PASS | Org Member is a standalone DocType linking to existing Organization (not duplicating org data) |
| Technology Stack | ✅ PASS | Using Frappe 15.x with Python 3.11+, MariaDB 10.6+ |
| Architecture Patterns | ✅ PASS | Following Frappe doctype system for data models |
| API-First Development | ✅ PASS | Will expose whitelist methods for member management |
| Naming Conventions | ✅ PASS | DocType: OrgMember (PascalCase), fields: snake_case |
| Code Quality Standards | ✅ PASS | Will include complete field definitions and tests |
| Security & Compliance | ✅ PASS | Role-based access control via Frappe permissions |

## Project Structure

### Documentation (this feature)

```text
specs/003-org-member-doctype/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   └── doctype/
│       └── org_member/
│           ├── __init__.py
│           ├── org_member.json       # DocType definition
│           ├── org_member.py         # Controller with validation logic
│           └── test_org_member.py    # Integration tests
├── fixtures/
│   └── (no fixtures needed - Org Member records created at runtime)
└── hooks.py                          # Add doc_events for cascade handling
```

**Structure Decision**: Following existing doctype pattern in `dartwing/dartwing_core/doctype/`. Tests colocated with doctype as per existing `role_template/test_role_template.py` pattern.

## Complexity Tracking

No constitution violations requiring justification.

## Phase 0: Research Notes

### Key Findings

1. **Role Template uses `is_supervisor` flag** (not `is_admin`): The existing Role Template DocType has an `is_supervisor` boolean field to indicate admin-level roles. The spec assumed `is_admin` but we should use `is_supervisor` for consistency.

2. **Existing deletion prevention pattern**: Role Template already implements `on_trash` hook with `check_linked_org_members()` that gracefully handles missing Org Member DocType. This pattern should be maintained.

3. **Organization `org_type` is set_only_once**: The `org_type` field on Organization has `set_only_once: 1`, confirming immutability assumption in spec.

4. **Test pattern**: Uses `frappe.tests.IntegrationTestCase` with test methods prefixed by user story/phase (e.g., `test_fixture_loads_all_roles`, `test_filter_by_family_type`).

5. **Person soft-cascade**: Requires adding `doc_events` hook in `hooks.py` for Person's `on_trash` event.

### Decisions

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| Use `is_supervisor` for admin detection | Aligns with existing Role Template field | Adding new `is_admin` field (unnecessary duplication) |
| Standalone DocType (not child table) | Enables direct querying, independent permissions | Child table under Organization (limits flexibility) |
| Unique constraint on (person, organization) | Single membership record per pair; reactivation via status update | Multiple records allowing history (spec clarification chose single record) |
| Soft-cascade on Person deletion | Preserves audit history; spec clarification decision | Hard delete (loses history) or block (breaks UX) |
