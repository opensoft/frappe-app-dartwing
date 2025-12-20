# Implementation Plan: OrganizationMixin Base Class

**Branch**: `008-organization-mixin` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/008-organization-mixin/spec.md`

## Summary

Enhance the existing OrganizationMixin class to add the `update_org_name()` method (FR-004) and ensure Family controller inherits from the mixin. Company already inherits from the mixin. The mixin provides read-only properties (`org_name`, `logo`, `org_status`) and `get_organization_doc()` for accessing parent Organization data from concrete types, with efficient single-query caching.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.model.document, frappe.db
**Storage**: MariaDB 10.6+ via Frappe ORM
**Testing**: pytest with Frappe test utilities
**Target Platform**: Frappe server (Linux)
**Project Type**: Single Frappe app (dartwing)
**Performance Goals**: Single-field fetches for properties, single cached query for multiple property access
**Constraints**: Must not break existing Company inheritance; Family must gain mixin without regressions
**Scale/Scope**: 4 concrete types (Family, Company, Association, Nonprofit) will inherit from mixin

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Single Source of Truth | PASS | Mixin accesses Organization doctype |
| 2. Technology Stack | PASS | Python 3.11+, Frappe 15.x, MariaDB |
| 3. Architecture Patterns | PASS | Mixin pattern for code reuse |
| 4. Cross-Platform Requirements | N/A | Backend-only feature |
| 5. Security & Compliance | PASS | Permissions delegated to Frappe |
| 6. Code Quality Standards | PASS | Tests required per spec |
| 7. Naming Conventions | PASS | snake_case for methods |
| 8. API Design | PASS | No new APIs exposed (mixin is internal) |
| 9. Offline-First | N/A | Backend-only feature |
| 10. AI Integration | N/A | No AI components |
| 11. Parallel Development | PASS | Branch pushed immediately |

**Gate Result**: PASS - No violations.

## Project Structure

### Documentation (this feature)

```text
specs/008-organization-mixin/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - no new APIs)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing_core/
│   ├── mixins/
│   │   ├── __init__.py              # Exports OrganizationMixin
│   │   └── organization_mixin.py    # MODIFY: Add update_org_name()
│   └── doctype/
│       └── family/
│           └── family.py            # MODIFY: Inherit from OrganizationMixin
└── dartwing_company/
    └── doctype/
        └── company/
            └── company.py           # NO CHANGE: Already inherits mixin

dartwing/dartwing_core/tests/
└── test_organization_mixin.py       # CREATE: Unit tests for mixin
```

**Structure Decision**: Single Frappe app structure. Mixin lives in `dartwing_core/mixins/`, consumed by concrete type controllers in their respective modules.

## Complexity Tracking

No violations to justify - implementation follows existing patterns.

## Current State Analysis

### Existing Implementation

The OrganizationMixin already exists at `dartwing/dartwing_core/mixins/organization_mixin.py` with:
- ✅ `org_name` property (FR-002)
- ✅ `logo` property (FR-002)
- ✅ `org_status` property (FR-002)
- ✅ `get_organization_doc()` method (FR-003)
- ✅ Caching via `_get_organization_cache()` (FR-009)
- ✅ Graceful None handling for missing Organization (FR-007)
- ❌ `update_org_name()` method (FR-004) - **MISSING**

### Inheritance Status

- ✅ Company inherits from OrganizationMixin (FR-006)
- ❌ Family does NOT inherit from OrganizationMixin (FR-005) - **MISSING**

## Implementation Tasks

### Task 1: Add `update_org_name()` to OrganizationMixin

Add the method to `dartwing/dartwing_core/mixins/organization_mixin.py`:
- Validate new_name is not empty (FR-008)
- Use `frappe.db.set_value()` for efficient update
- Clear cache after update
- Raise error if organization field is empty/null (Edge Case)
- Let Frappe permission system handle permission errors (Clarification)

### Task 2: Update Family to Inherit from OrganizationMixin

Modify `dartwing/dartwing_core/doctype/family/family.py`:
- Import OrganizationMixin from dartwing.dartwing_core.mixins
- Change class declaration to `class Family(Document, OrganizationMixin):`
- Verify existing Family validation logic is unaffected

### Task 3: Create Unit Tests

Create `tests/unit/test_organization_mixin.py`:
- Test `org_name` returns correct value
- Test `logo` returns correct value (and None when empty)
- Test `org_status` returns correct value
- Test `get_organization_doc()` returns document
- Test `update_org_name()` updates Organization
- Test `update_org_name("")` raises validation error
- Test all properties return None when organization is null
- Test all properties return None when Organization is deleted

### Task 4: Verify Company Inheritance (Regression Test)

Verify Company still works correctly:
- All mixin properties accessible
- `update_org_name()` works from Company instance
