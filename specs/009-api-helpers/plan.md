# Implementation Plan: API Helpers (Whitelisted Methods)

**Branch**: `009-api-helpers` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-api-helpers/spec.md`

## Summary

Implement four whitelisted API methods (`get_user_organizations`, `get_organization_with_details`, `get_concrete_doc`, `get_org_members`) that enable the Flutter client to retrieve organization data, concrete type details, and member information through standardized REST endpoints. All methods enforce permission checks and return consistent response formats.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.permissions
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with Frappe test framework
**Target Platform**: Frappe backend serving Flutter (iOS, Android, Web, Desktop) + external clients
**Project Type**: Web application (Frappe backend + Flutter frontend)
**Performance Goals**: <500ms response time, 1000 concurrent users
**Constraints**: All methods must use `@frappe.whitelist()`, permission checks required
**Scale/Scope**: Up to 50 organizations per user, 100+ members per organization

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| API-First Development | PASS | All methods exposed via `@frappe.whitelist()` |
| Single Source of Truth | PASS | Uses existing Organization doctype pattern |
| Technology Stack | PASS | Python 3.11+, Frappe 15.x, MariaDB |
| Security & Compliance | PASS | Permission checks enforced, audit logging |
| API Design | PASS | Custom methods via `/api/method/dartwing.*`, pagination via limit/offset |
| Naming Conventions | PASS | snake_case for methods/fields, PascalCase for doctypes |
| Code Quality Standards | PASS | Tests required for business logic |

**Gate Result**: PASS - All constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/009-api-helpers/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   ├── doctype/
│   │   ├── organization/
│   │   │   └── organization.py     # Extend with get_concrete_doc, get_organization_with_details
│   │   └── org_member/
│   │       └── org_member.py       # Existing doctype
│   └── api/
│       └── organization_api.py     # NEW: get_user_organizations, get_org_members
├── hooks.py                        # Register any new hooks if needed
└── tests/
    └── test_organization_api.py    # NEW: All API tests (unit + integration in single file per Frappe convention)
```

**Structure Decision**: Backend-only implementation in `dartwing_core` module. API methods go in either:
1. `dartwing_core/doctype/organization/organization.py` - for methods tied to Organization document
2. `dartwing_core/api/organization_api.py` - for standalone API methods not tied to a specific document

## Complexity Tracking

> No violations - structure follows existing patterns.

| Item | Decision | Rationale |
|------|----------|-----------|
| API location | Split between doctype controller and api module | `get_concrete_doc` and `get_organization_with_details` are document-centric, `get_user_organizations` and `get_org_members` are query-centric |
| Response format | Frappe standard dict with `message` key | Consistent with existing Frappe API patterns |
