# Implementation Plan: Role Template DocType

**Branch**: `002-role-template-doctype` | **Date**: 2025-12-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-role-template-doctype/spec.md`

## Summary

Create a Role Template DocType that defines organization-type-specific roles (Family, Company, Nonprofit, Association) with supervisor flags and conditional hourly rate fields. Include seed data fixtures for 14 predefined roles across all organization types (4 Family + 4 Company + 3 Nonprofit + 3 Association). Role filtering in Org Member forms will use the organization's `org_type` field to display only relevant roles.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 16.x backend)
**Primary Dependencies**: Frappe Framework 16.x, frappe.model.document, frappe.fixtures
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with frappe test runner (`bench --site [site] run-tests`)
**Target Platform**: Frappe/ERPNext server (Linux)
**Project Type**: Frappe DocType module (dartwing_core)
**Performance Goals**: Role filtering < 500ms, fixture loading < 5s
**Constraints**: Must integrate with existing Organization DocType; read-only for non-System Managers
**Scale/Scope**: ~15 seed records, minimal runtime queries (reference data)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Single Source of Truth | ✅ PASS | Role Template is a single DocType for all org types; uses `applies_to_org_type` field |
| 2. Technology Stack | ✅ PASS | Using Frappe 16.x with Python 3.11+, MariaDB |
| 3. Architecture Patterns | ✅ PASS | Standard Frappe doctype system for data models |
| 4. Cross-Platform Requirements | ✅ PASS | DocType accessible via REST API for Flutter clients |
| 5. Security & Compliance | ✅ PASS | Role-based access control; System Manager for write, all users for read |
| 6. Code Quality Standards | ✅ PASS | Complete field definitions, tests required |
| 7. Naming Conventions | ✅ PASS | DocType: "Role Template" (PascalCase), fields: snake_case |
| 8. API Design | ✅ PASS | Standard `/api/resource/Role Template` CRUD |
| 9. Offline-First | ✅ PASS | Reference data can be cached client-side |
| 10. AI Integration | N/A | No AI features in this DocType |

**Gate Result**: ✅ ALL GATES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/002-role-template-doctype/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── role-template-api.yaml
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
dartwing/
└── dartwing_core/
    └── doctype/
        └── role_template/
            ├── __init__.py
            ├── role_template.json      # DocType definition
            ├── role_template.py        # Controller with validation hooks
            └── test_role_template.py   # Unit tests

dartwing/
└── fixtures/
    └── role_template.json              # Seed data (15 roles)
```

**Structure Decision**: Standard Frappe DocType structure within existing `dartwing_core` module. Fixtures in app-level `dartwing/fixtures/` for automatic loading on install.

## Risks & Decisions

### Risk 1: Organization org_type Mismatch

**Risk**: The existing Organization DocType uses "Club" but spec requires "Association"
**Impact**: HIGH - Role filtering will fail if org_type values don't match
**Mitigation**: Update Organization DocType's `org_type` options from "Club" to "Association" as part of this feature, or create a migration

**Decision**: Update Organization DocType to use "Association" instead of "Club" (aligns with clarification that Club is a subtype of Association)

### Risk 2: Seed Data Idempotency

**Risk**: Running fixtures multiple times could create duplicates or fail on unique constraint
**Impact**: MEDIUM - Deployment issues
**Mitigation**: Use `role_name` as fixture key; Frappe fixtures are idempotent by name

**Decision**: Use standard Frappe fixture format with `name` field matching `role_name`

### Risk 3: Deletion Prevention Without Org Member

**Risk**: FR-008 requires preventing deletion when referenced by Org Member, but Org Member doesn't exist yet
**Impact**: LOW - Feature 3 will add Org Member
**Mitigation**: Implement `on_trash` hook with conditional check; will become active when Org Member exists

**Decision**: Implement the validation hook now; it will return early if Org Member DocType doesn't exist

### Assumptions Validated

| Assumption | Validation | Status |
|------------|------------|--------|
| Organization DocType exists with org_type | Confirmed in organization.json | ✅ |
| org_type uses Select field | Confirmed: "Family\nCompany\nClub\nNonprofit" | ⚠️ Needs "Club"→"Association" update |
| Frappe fixture system available | Standard Frappe feature | ✅ |
| System Manager role exists | Standard Frappe role | ✅ |

### Trade-offs

| Decision | Chosen Approach | Alternative Rejected | Rationale |
|----------|-----------------|---------------------|-----------|
| Role naming | Unique across all org types | Unique per org_type | Simpler queries, clearer admin experience, prevents confusion |
| Hourly rate field | Conditional via `depends_on` | Separate DocType per org type | Keeps single DocType; shows for Company/Nonprofit/Association, hidden for Family |
| Supervisor flag | Simple boolean | Permission level integer | Boolean covers known use cases; can extend later |
| Fixture format | JSON in dartwing/fixtures | Python fixtures or migration | Standard Frappe approach, automatic loading |

## Complexity Tracking

> No Constitution Check violations - table not required

## Phase 0 Output Reference

See [research.md](./research.md) for:
- Frappe fixture best practices
- `depends_on` conditional field patterns
- Link field filtering patterns
- Deletion prevention hooks

## Phase 1 Output Reference

See:
- [data-model.md](./data-model.md) - Role Template entity definition
- [contracts/role-template-api.yaml](./contracts/role-template-api.yaml) - REST API contract
- [quickstart.md](./quickstart.md) - Developer setup guide
