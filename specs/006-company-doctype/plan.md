# Implementation Plan: Company DocType

**Branch**: `006-company-doctype` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-company-doctype/spec.md`

## Summary

Implement the Company DocType as a concrete organization type in the Dartwing hybrid organization model. The Company DocType will be automatically created when an Organization with `org_type="Company"` is created, maintaining bidirectional linking. It includes fields for legal entity information (tax ID, entity type, jurisdiction), child tables for officers/directors and LLC/partnership members, and address references.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.fixtures
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with Frappe test framework
**Target Platform**: Frappe server (Linux)
**Project Type**: Frappe DocType module (dartwing_company)
**Performance Goals**: Company record creation < 5 seconds, legal info entry < 2 minutes
**Constraints**: Must integrate with existing Organization hooks, respect User Permissions
**Scale/Scope**: Standard business application scale (thousands of companies per instance)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **1. Single Source of Truth** | PASS | Company is a concrete type linked 1:1 to Organization; not a separate org system |
| **2. Technology Stack** | PASS | Using Frappe 15.x, Python 3.11+, MariaDB - all compliant |
| **3. Architecture Patterns** | PASS | Following Frappe doctype system for data models |
| **4. Cross-Platform Requirements** | PASS | DocType accessible via REST API from all clients |
| **5. Security & Compliance** | PASS | Role-based access via Frappe permissions, User Permission inheritance from Organization |
| **6. Code Quality Standards** | PASS | Complete field definitions in JSON, tests required |
| **7. Naming Conventions** | PASS | DocType PascalCase (Company), fieldnames snake_case (tax_id, entity_type) |
| **8. API Design** | PASS | Standard `/api/resource/Company` plus custom whitelist methods |
| **9. Offline-First** | N/A | Backend DocType - offline handled by Flutter client |
| **10. AI Integration** | N/A | Not applicable to this feature |

**Gate Result**: PASS - No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/006-company-doctype/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   ├── doctype/
│   │   ├── organization/
│   │   │   ├── organization.json      # Update ORG_TYPE_MAP
│   │   │   └── organization.py        # Add Company creation logic
│   │   ├── organization_officer/      # NEW - shared child table
│   │   │   ├── organization_officer.json
│   │   │   └── organization_officer.py
│   │   └── organization_member_partner/  # NEW - shared child table
│   │       ├── organization_member_partner.json
│   │       └── organization_member_partner.py
│   ├── fixtures/                      # Seed data for Role Templates
│   └── mixins/
│       └── organization_mixin.py      # Shared mixin for concrete org types
├── hooks.py                           # App-level hooks (permission_query_conditions registered here)
├── dartwing_company/                  # NEW module
│   ├── __init__.py
│   ├── doctype/
│   │   └── company/
│   │       ├── company.json           # DocType definition
│   │       ├── company.py             # Controller with OrganizationMixin
│   │       ├── company.js             # Client script for entity_type warnings
│   │       └── test_company.py        # Unit tests
│   ├── permissions.py                 # Permission query conditions
│   └── api.py                         # Whitelist API methods
└── tests/
    └── integration/
        └── test_company_integration.py  # Integration tests
```

**Structure Decision**: Creating a new `dartwing_company` Frappe module to house the Company DocType, following the existing pattern where `dartwing_core` hosts Organization and shared doctypes. The child tables (Organization Officer, Organization Member Partner) belong in `dartwing_core` as they're shared with Nonprofit.

## Complexity Tracking

> No Constitution violations requiring justification. Complexity is appropriate for the feature scope.

| Component | Complexity | Justification |
|-----------|------------|---------------|
| Company DocType | Low | Standard Frappe DocType with fields and child tables |
| Organization hooks | Low | Extending existing after_insert pattern |
| Child tables | Low | Standard Frappe child table pattern |
| Permission inheritance | Medium | Using existing User Permission system, no custom logic needed |
