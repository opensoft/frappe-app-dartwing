# Implementation Plan: Basic Test Suite

**Branch**: `010-basic-test-suite` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-basic-test-suite/spec.md`

## Summary

This feature consolidates and completes the existing test coverage for Dartwing core features. The codebase already has substantial test infrastructure (`test_person.py`, `test_organization_hooks.py`, `test_permission_propagation.py`), but requires additional tests for Role Template, API helpers, and OrganizationMixin to achieve 80% coverage of Features 1-9. The implementation will extend the existing Frappe test patterns (FrappeTestCase, fixtures, cleanup utilities) rather than introducing new testing frameworks.

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 15.x backend)
**Primary Dependencies**: Frappe Framework 15.x, frappe.tests.utils, pytest (via bench)
**Storage**: MariaDB 10.6+ via Frappe ORM (test database)
**Testing**: Frappe's built-in test framework (`bench run-tests`), FrappeTestCase base class
**Target Platform**: Linux server (development/CI environment)
**Project Type**: Single Frappe app with modular test organization
**Performance Goals**: Full test suite execution under 5 minutes
**Constraints**: Tests must use Frappe's transaction rollback for isolation; no external dependencies
**Scale/Scope**: ~50-60 test cases covering 9 core features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| 1. Single Source of Truth | PASS | Tests verify Organization polymorphism, not duplicate structures |
| 2. Technology Stack | PASS | Python 3.11+, Frappe 15.x, MariaDB - no new technologies |
| 3. Architecture Patterns | PASS | Using existing FrappeTestCase patterns |
| 4. Cross-Platform Requirements | N/A | Backend tests only |
| 5. Security & Compliance | PASS | Permission tests validate RBAC |
| 6. Code Quality Standards | PASS | Tests enforce doctype validation, required fields |
| 7. Naming Conventions | PASS | test_*.py files, snake_case functions |
| 8. API Design | PASS | Tests validate @frappe.whitelist() methods |
| 9. Offline-First | N/A | Backend tests only |
| 10. AI Integration | N/A | Not applicable to test suite |
| 11. Parallel Development | PASS | Branch pushed immediately |

## Project Structure

### Documentation (this feature)

```text
specs/010-basic-test-suite/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (test entities)
├── quickstart.md        # Phase 1 output (test execution guide)
└── contracts/           # Phase 1 output (test coverage matrix)
```

### Source Code (repository root)

```text
dartwing/
├── dartwing/
│   ├── dartwing_core/
│   │   ├── doctype/
│   │   │   ├── person/
│   │   │   │   └── test_person.py          # [EXISTS] Person DocType tests
│   │   │   ├── organization/
│   │   │   │   └── test_organization.py    # [EXISTS] Basic org tests
│   │   │   ├── org_member/
│   │   │   │   └── test_org_member.py      # [EXISTS] Org Member tests
│   │   │   └── role_template/
│   │   │       └── test_role_template.py   # [NEW] Role Template tests
│   │   │
│   │   └── mixins/
│   │       └── test_organization_mixin.py  # [NEW] OrganizationMixin tests
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_organization_hooks.py      # [EXISTS] Bidirectional hooks
│       ├── test_permission_propagation.py  # [EXISTS] User Permission lifecycle
│       ├── test_permission_helpers.py      # [EXISTS] Permission query conditions
│       ├── test_permission_api.py          # [EXISTS] Permission API tests
│       ├── test_person_api.py              # [EXISTS] Person API tests
│       ├── test_api_helpers.py             # [NEW] API helper tests (get_concrete_doc, etc.)
│       └── integration/
│           └── test_full_workflow.py       # [NEW] End-to-end workflow test
```

**Structure Decision**: Extending existing test organization. DocType-specific tests live in doctype folders; cross-cutting tests in `dartwing/tests/`. New files marked with [NEW].

## Test Coverage Gap Analysis

Based on spec requirements vs. existing tests:

| Feature | Requirement | Existing Coverage | Gap |
|---------|-------------|-------------------|-----|
| Person DocType (FR-001) | Email/keycloak uniqueness, deletion prevention | test_person.py (comprehensive) | None |
| Organization Hooks (FR-002) | Concrete type creation, cascade delete | test_organization_hooks.py (comprehensive) | None |
| Org Member (FR-003) | Person+org uniqueness, role filtering | test_org_member.py (partial) | Role filtering tests |
| Permission Propagation (FR-004) | Auto creation/removal | test_permission_propagation.py (comprehensive) | None |
| Permission Filtering (FR-005) | List view filtering | test_permission_helpers.py | None |
| API Helpers (FR-006) | get_concrete_doc, get_user_organizations | test_person_api.py (partial) | get_org_members, get_user_organizations |
| OrganizationMixin (FR-007) | Property accessors, update methods | None | Full implementation needed |
| Test Isolation (FR-008) | Setup/teardown | Implemented via TEST_PREFIX pattern | None |
| Role Template Seed Data (FR-012) | Verify fixtures exist | None | Full implementation needed |

## Complexity Tracking

No constitution violations requiring justification. The implementation adds 4 new test files while leveraging existing patterns.

## Implementation Phases

### Phase 2: Test Implementation (via /speckit.tasks)

Tasks will be generated to:
1. Create `test_role_template.py` - Role Template validation and seed data tests
2. Create `test_organization_mixin.py` - Mixin property accessor tests
3. Create `test_api_helpers.py` - API endpoint tests for Flutter integration
4. Extend `test_org_member.py` - Add role filtering validation tests
5. Create `test_full_workflow.py` - Integration test covering complete user flow
6. Update test runner configuration for CI readiness

### Test Execution Commands

```bash
# Run all Dartwing tests
bench --site <site> run-tests --app dartwing

# Run specific test module
bench --site <site> run-tests --app dartwing --module dartwing.tests.test_api_helpers

# Run with verbose output
bench --site <site> run-tests --app dartwing -v

# Run tests matching pattern
bench --site <site> run-tests --app dartwing -k "test_role"
```
