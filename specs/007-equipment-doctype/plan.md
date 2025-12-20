# Implementation Plan: Equipment DocType

**Branch**: `007-equipment-doctype` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-equipment-doctype/spec.md`

## Summary

Implement the Equipment DocType as a polymorphic asset management entity linked to Organization. Equipment tracks physical assets with serial numbers, status, location, documents, and maintenance schedules. The implementation follows the established patterns from Company DocType (Feature 6) using `user_permission_dependant_doctype` for Organization-scoped access control.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.fixtures
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with frappe test runner
**Target Platform**: Frappe/ERPNext server (Linux)
**Project Type**: Frappe app module (backend doctypes)
**Performance Goals**: Equipment list loads within 2 seconds for 1000 items per organization
**Constraints**: Must integrate with existing User Permission system; equipment filtered by Organization access
**Scale/Scope**: Up to 1000 equipment items per organization; supports all org types (Family, Company, Nonprofit, Association)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Single Source of Truth | PASS | Equipment links to Organization (polymorphic), not to concrete types |
| 2. Technology Stack | PASS | Using Frappe 15.x, Python 3.11+, MariaDB |
| 3. Architecture Patterns | PASS | Following Frappe doctype patterns; repository via Frappe ORM |
| 4. Cross-Platform Requirements | N/A | Backend-only feature; API serves all clients |
| 5. Security & Compliance | PASS | Using User Permission system via Organization link; audit via Frappe's built-in logging |
| 6. Code Quality Standards | PASS | Will include doctype JSON definitions and tests |
| 7. Naming Conventions | PASS | DocType: PascalCase (Equipment, Equipment Document); fields: snake_case |
| 8. API Design | PASS | Using /api/resource/Equipment for CRUD; custom methods via /api/method/ |
| 9. Offline-First | N/A | Backend feature; offline handled by client |
| 10. AI Integration | N/A | Not applicable to this feature |
| 11. Parallel Development Governance | PASS | Branch created and will be pushed immediately |

## Project Structure

### Documentation (this feature)

```text
specs/007-equipment-doctype/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   └── doctype/
│       ├── equipment/
│       │   ├── __init__.py
│       │   ├── equipment.json          # DocType definition
│       │   ├── equipment.py            # Controller with validation
│       │   └── test_equipment.py       # Unit tests (optional - for future/manual testing)
│       ├── equipment_document/
│       │   ├── __init__.py
│       │   ├── equipment_document.json # Child table definition
│       │   └── equipment_document.py
│       └── equipment_maintenance/
│           ├── __init__.py
│           ├── equipment_maintenance.json # Child table definition
│           └── equipment_maintenance.py
├── permissions/
│   └── equipment.py                    # Permission query conditions
├── hooks.py                            # Register permission hooks
└── tests/
    └── integration/
        └── test_equipment_integration.py

tests/
├── integration/
│   └── test_equipment_permissions.py   # Permission integration tests
└── unit/
    └── test_equipment_validation.py    # Validation unit tests
```

**Structure Decision**: Equipment DocType placed in `dartwing_core` module (not a separate module) since:
1. Equipment is a generic asset tied to Organization (like Org Member)
2. Child tables (Equipment Document, Equipment Maintenance) are Equipment-specific (not shared)
3. Follows pattern from architecture doc Section 3.11 which places Equipment in dartwing_core

## Complexity Tracking

> No Constitution Check violations requiring justification.

| Decision | Rationale |
|----------|-----------|
| Place in dartwing_core | Equipment is generic across all org types; follows architecture doc |
| Two child tables | Equipment Document and Equipment Maintenance are Equipment-specific, not shared with other doctypes |
| No separate module | Unlike Company which has domain-specific concerns, Equipment is a utility doctype |
