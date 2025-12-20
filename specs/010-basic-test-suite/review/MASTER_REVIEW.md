# MASTER CODE REVIEW: 010-basic-test-suite

**Director of Engineering Synthesis**
**Date:** 2025-12-15
**Branch:** 010-basic-test-suite
**Module:** dartwing_core
**Review Team:** opus45, gemi30, GPT52, sonn45

---

## Executive Summary

**Feature:** Basic Test Suite - Comprehensive test coverage for core Dartwing features (Person, Role Template, Org Member, Organization hooks, permissions, Company, Equipment, OrganizationMixin, and API helpers)

**Overall Assessment:** This branch adds substantial test infrastructure (+799 lines of test code) with excellent coverage for Role Templates, integration workflows, and mixin patterns. However, **5 critical blockers prevent immediate merge**: duplicate dictionary keys in hooks, incomplete Organization refactoring, architectural misalignment in test helpers, missing implementations for tested features, and weak permission testing patterns. Estimated fix time: 1 day.

**Synthesis Result:** After consolidating 4 independent reviews covering 25 distinct issues, the master action plan identifies **8 P1-Critical issues** (must fix), **9 P2-Medium suggestions** (should fix), and **5 P3-Low improvements** (nice to have).

---

## 1. Master Action Plan (Prioritized & Consolidated)

### Priority 1: CRITICAL (Must Fix Before Merge)

| ID | Type/Source | Original Reviewer | Consolidated Issue Description | Synthesized Fix |
|:---|:---|:---|:---|:---|
| **P1-001** | Architecture / Data Integrity | **GPT52** (Primary), **opus45** (Supporting) | **Architectural Violation: Test helpers assume "concrete-first creates Organization" flow for Company DocType.** Multiple test files (`test_full_workflow.py:138`, `test_organization_mixin.py:78`) create Company directly, expecting Organization auto-creation. However, Company requires `organization` field (mandatory per `company.json:52`), making this flow impossible without violating schema constraints. This contradicts the documented Organization-first lifecycle in `dartwing_core_arch.md` Section 3.2 which explicitly states "When an Organization is created, a hook automatically creates the corresponding Concrete Doctype." | **Architectural Decision (dartwing_core_arch.md Section 3.2):** Organization MUST be the source-of-truth and lifecycle driver. Fix all test helpers to follow canonical flow: (1) Create Organization with `org_type=org_type` and `org_name` set; (2) `org.insert()`; (3) `org.reload()`; (4) Fetch concrete type via `frappe.get_doc(org.linked_doctype, org.linked_name)`. Update `test_full_workflow.py:138-152` and `test_organization_mixin.py:78-109`. This also provides better regression protection for the actual production behavior. |
| **P1-002** | Code Correctness / Python Syntax | **sonn45** (Primary), **gemi30** (Validator) | **BLOCKER: Duplicate dictionary keys in hooks.py permission configuration.** The `permission_query_conditions` and `has_permission` dictionaries contain duplicate "Company" entries (hooks.py:125 and again later). Python silently overwrites the first value with the second, indicating incomplete refactoring from Company module migration (`dartwing_core` → `dartwing_company`). This breaks the permission system's integrity. | Remove all duplicate keys. Consolidate to single entry per DocType: `"Company": "dartwing.permissions.company.get_permission_query_conditions"`. Verify no other duplicate keys exist in `permission_query_conditions`, `has_permission`, or `doc_events` dictionaries. Run `python -m py_compile dartwing/hooks.py` to validate syntax. |
| **P1-003** | Data Integrity / Sync Mechanism | **GPT52** (Primary) | **Data Drift Risk: Company DocType declares "synced from Organization" fields without actual sync implementation.** Fields `company_name` (company.json:42) and `status` (company.json:61) have comments indicating they are "synced from Organization," but no sync mechanism exists. Per `ORG_FIELD_MAP` in `organization.py:33`, these are only set at creation time via hooks. Subsequent Organization updates will NOT propagate, violating the "Single Source of Truth" principle (constitution.md Section 1). | **Architectural Decision (constitution.md Section 1 - Single Source of Truth):** Replace manual syncing with Frappe's native `fetch_from` mechanism. Update `company.json:42` to: `{"fieldname": "company_name", "fetch_from": "organization.org_name", "read_only": 1}`. Update `company.json:61` similarly for `status`. This ensures automatic propagation on Organization save and prevents manual edits that create inconsistency. Remove these fields from `ORG_FIELD_MAP` since fetch_from handles it. |
| **P1-004** | Test Coverage / Missing Implementation | **sonn45** (Primary), **gemi30** (Supporting) | **Missing OrganizationMixin Implementation: Tests exist but production code doesn't.** `test_organization_mixin.py` contains 327 lines testing mixin properties (`org_name`, `logo`, `_clear_organization_cache`), but neither `family.py` nor `company.py` controllers actually inherit or implement OrganizationMixin. Tests will fail with `AttributeError: 'Family' object has no attribute '_clear_organization_cache'`. This is Feature 8 scope creep into Feature 10 (test suite). | **Scope Decision:** Remove `dartwing/dartwing_core/mixins/test_organization_mixin.py` from this branch entirely using `git rm`. Feature 8 (OrganizationMixin) should be its own branch (011-organization-mixin) with proper spec, implementation, THEN tests. This aligns with the documented roadmap in `dartwing_core_features_priority.md` where Feature 8 comes AFTER Feature 10. Prevents false test coverage. |
| **P1-005** | Test Isolation / Permissions | **GPT52** (Primary), **sonn45** (Supporting), **opus45** (Related) | **Weak Permission Testing: Integration tests use System Manager role, bypassing all permission checks.** `test_full_workflow.py:119` creates users with `roles: [{"role": "System Manager"}]`, which defeats the purpose of testing User Permission propagation and list view filtering. System Manager sees ALL organizations regardless of User Permissions, making permission tests pass even when permission logic is broken. | Change test users to `"Dartwing User"` role (lowest-privilege role reflecting real app usage) in `test_full_workflow.py:119`. Update test assertions to explicitly verify: (1) User CAN access organizations they're members of, (2) User CANNOT access other organizations (expect `frappe.PermissionError`). Add one targeted test that explicitly verifies "System Manager can see all orgs" only if that's documented behavior. |
| **P1-006** | Code Correctness / Broken Refactoring | **sonn45** (Primary) | **Incomplete Refactoring: Orphaned code fragments in organization.py.** The git diff shows: (1) Orphaned docstring at line 257-258 not attached to any function, (2) Incomplete exception handler at lines 339-346 with truncated error message. Indicates failed merge or incomplete refactoring that breaks code structure. | Read full `organization.py` file (not just diff) to verify: (1) All methods are complete with proper docstrings, (2) All exception handlers have complete error messages, (3) No orphaned documentation. Run `python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py` and full Organization tests: `bench --site <site> run-tests --module dartwing.dartwing_core.doctype.organization.test_organization`. |
| **P1-007** | Test Correctness / Architectural Misalignment | **gemi30** (Primary) | **Test Will Fail: test_organization_hooks.py expects 4 org types but code defines 5.** Test `test_us1_org_type_map_contains_expected_types` (Line 172-173) asserts `ORG_TYPE_MAP.keys()` should be exactly `{"Family", "Company", "Association", "Nonprofit"}`. However, `organization.py:26` includes `"Club": "Club"` in `ORG_TYPE_MAP`. Additionally, "Club" is missing from `ORG_FIELD_MAP`, so creating a Club Organization would fail during concrete type creation. Per PRD, "Association" is intended to cover clubs/groups. | **Architectural Decision (dartwing_core_prd.md Section 3.4 - Association covers clubs):** Remove `"Club": "Club"` from `ORG_TYPE_MAP` in `organization.py:26` to align with architecture spec. If Club-specific functionality is needed later, it should be a subtype within Association (using `association_type` field) per the PRD design, not a separate root type. |
| **P1-008** | Test Isolation / Exception Handling | **opus45** (Primary) | **Test Flakiness Risk: Cleanup routines silently swallow all exceptions, masking deletion hook bugs.** `test_permission_api.py:67-106` cleanup method uses broad `except (frappe.DoesNotExistError, frappe.LinkExistsError): pass` blocks. If deletion hooks fail or have bugs, tests pass but leave orphaned data, causing flakiness (violates SC-005 requirement for zero test flakiness). Improper cleanup order may also cause LinkExistsError cascades. | Refactor `_cleanup_test_data()` in `test_permission_api.py` to: (1) Clean in **reverse dependency order** (User Permissions → Org Members → Organizations → Persons), (2) Only catch **expected** `DoesNotExistError` exceptions, (3) **Log** any `LinkExistsError` as potential bug: `frappe.log_error(...)`, then force-delete blocking links with explicit SQL. See opus45 review for complete refactored code. This surfaces real bugs during test development. |

---

### Priority 2: MEDIUM (Should Fix, Impacts Maintainability)

| ID | Type/Source | Original Reviewer | Consolidated Issue Description | Synthesized Fix |
|:---|:---|:---|:---|:---|
| **P2-001** | Code Quality / DRY Violation | **opus45** (Primary) | **Code Duplication: Test fixture helpers duplicated across 3+ files with variations.** Helper methods `_create_test_person()`, `_create_test_organization()`, `_create_test_user()` are duplicated in `test_permission_api.py`, `test_full_workflow.py`, `test_organization_mixin.py` with slight variations. Violates DRY principle and makes maintenance harder when test patterns change. | Create shared fixtures module at `dartwing/tests/fixtures.py` with `DartwingTestFixtures` class providing reusable helpers with automatic cleanup tracking. See opus45 review for complete implementation. Update all test files to use `self.fixtures = DartwingTestFixtures(prefix="_Test_")` pattern. Benefits: (1) Eliminates duplication, (2) Centralized fixture logic, (3) Automatic cleanup tracking reduces flakiness. |
| **P2-002** | Test Coverage / Missing Implementation | **gemi30** (Primary), **sonn45** (Supporting) | **Missing test_api_helpers.py file: Spec calls for it but not created.** Implementation plan (`plan.md`) explicitly requested `dartwing/tests/test_api_helpers.py` for API endpoint testing (get_concrete_doc, get_user_organizations, get_org_members). File does not exist. While some API testing is distributed in other files, standalone API helpers may be untested. | **Scope Decision:** API helper tests exist but are distributed. `test_permission_api.py` covers User Permission APIs, `test_organization_hooks.py` covers Organization APIs. Either: (1) Rename `test_permission_api.py` to `test_api_helpers.py` to match spec naming, OR (2) Create explicit `test_api_helpers.py` that imports and runs all API tests (acts as a suite). Document that API tests are distributed by domain for maintainability. |
| **P2-003** | Test Coverage / Missing Assertions | **GPT52** (Primary) | **Incomplete Test: test_manual_permission_deletion_resilience has no final assertion.** `test_full_workflow.py:370` deletes User Permission manually and toggles Org Member status, but doesn't assert whether permission gets recreated. Test always passes regardless of behavior. Comment at line 434 acknowledges "depends on implementation." | Make test deterministic: If permission recreation on status change is **required** behavior, assert `assertTrue(perm_recreated)`. If recreation is **not** expected, assert `assertFalse(perm_recreated)`. If behavior is **undefined**, use `self.skipTest("Permission recreation behavior not yet defined")` until requirements are clear. Non-asserting tests provide false confidence. |
| **P2-004** | Test Coverage / Incomplete Checks | **GPT52** (Primary) | **Incomplete DocType Presence Check: test_full_workflow.py uses Company but doesn't check for it.** `test_full_workflow.py:29` defines `required_doctypes = ["Person", "Organization", "Org Member", "Family"]` but later tests create Company organizations (line 221). If Company DocType doesn't exist, tests fail with confusing errors instead of being skipped gracefully. | Add `"Company"` to `required_doctypes` list in `test_full_workflow.py:29`. If tests should be modular/skippable when modules aren't installed, split Company-specific tests into separate test class with its own `setUpClass` check. Principle: Fail fast with clear messages. |
| **P2-005** | Code Quality / Constants Usage | **gemi30** (Primary) | **Inconsistent Use of Constants: Code defines constants but uses literal strings.** `organization.py` defines constants like `DOCTYPE_FAMILY = "Family"` but then uses literal strings `"Family"` in `ORG_TYPE_MAP` keys and `ORG_FIELD_MAP`. Reduces consistency and makes refactoring harder. | Use defined constants for dictionary keys where possible: `ORG_TYPE_MAP = {DOCTYPE_FAMILY: "Family", DOCTYPE_COMPANY: "Company", ...}`. Benefits: (1) Single source of truth for DocType names, (2) IDE refactoring support, (3) Typo prevention. |
| **P2-006** | Cache Invalidation / Stale Data Risk | **opus45** (Primary), **gemi30** (Supporting) | **Missing Automatic Cache Invalidation: OrganizationMixin relies on manual cache clearing.** Test `test_organization_mixin.py:246-257` updates Organization then manually calls `family._clear_organization_cache()`. In production, developers may update Organization and immediately access mixin properties expecting fresh data but get stale values if they forget manual cache clear. | **Architectural Decision:** Add `on_update` hook to Organization controller that automatically clears concrete type caches when Organization is modified. Implementation: In `organization.py` add method that fetches linked concrete doc and calls `_clear_organization_cache()` if method exists. See opus45 review for complete code. Update test to verify automatic invalidation (remove manual cache clear). |
| **P2-007** | Test Reliability / Fixture Dependencies | **sonn45** (Primary) | **Test Assumes Fixtures Loaded: test_role_template.py expects 14 roles but may not exist on fresh install.** `test_role_template.py:15-18` asserts 14 Role Template fixtures exist, but fixtures may not load if: (1) Site not migrated, (2) Fixture files missing, (3) `bench migrate` not run. Tests fail on fresh installations with confusing errors. Violates test independence. | Add fixture loading to `setUpClass`: Check if Role Template count < 14, then either: (1) Load test fixtures programmatically (see sonn45 review for implementation), OR (2) Skip tests with `unittest.SkipTest("Run 'bench migrate' to load fixtures")`. Log warning for visibility. Programmatic loading preferred for CI/CD environments. |
| **P2-008** | Code Quality / Validation Location | **sonn45** (Primary) | **Missing Validation Logic: Tests expect hourly rate validation but controller may not have it.** `test_role_template.py:317-332` expects negative hourly rates to be rejected with `ValidationError`, but this validation must exist in Role Template controller. Business logic should be explicit in controller, not implicit in database constraints (Frappe best practice). | Verify `role_template.py` controller has `validate()` method with: (1) `validate_hourly_rate()` that raises `frappe.ValidationError` for negative rates, (2) `validate_family_hourly_rate()` that clears hourly_rate when `applies_to_org_type == "Family"`. See sonn45 review for complete implementation. If validation doesn't exist, add it before merge. |
| **P2-009** | Project Structure / Duplicate Paths | **GPT52** (Primary) | **Confusing Duplicate Package: Extra "dartwing/dartwing/tests" path exists alongside correct "dartwing/tests" path.** Both `dartwing/tests/integration/__init__.py` (correct) and `dartwing/dartwing/tests/integration/__init__.py` (duplicate) exist. Creates import confusion, IDE indexing oddities, risk of running wrong module path. | Delete `dartwing/dartwing/tests/integration/__init__.py` and the `dartwing/dartwing/tests/integration/` directory if empty. Run `find . -name "__pycache__" -type d -exec rm -rf {} +` to clear any cached imports. Verify tests still import correctly from `dartwing.tests.integration`. |

---

### Priority 3: LOW (Nice to Have, Future Improvements)

| ID | Type/Source | Original Reviewer | Consolidated Issue Description | Synthesized Fix |
|:---|:---|:---|:---|:---|
| **P3-001** | Code Style / Function Complexity | **gemi30** (Primary) | **Verbose Global State Management: _ensure_field_map_validated uses Java-style locking pattern.** The function uses `global` and double-checked locking which is verbose for Python. While thread-safe and functional, it's not Pythonic. | Consider using `functools.lru_cache` on validation function or run validation module-level on import (if safe from circular imports). However, current implementation works correctly - this is purely stylistic optimization for future refactoring. Low priority. |
| **P3-002** | Documentation / Tooling Clarity | **GPT52** (Primary) | **Spec Wording Mismatch: Documentation mentions "pytest" but implementation uses unittest/FrappeTestCase.** `plan.md:15` and `CLAUDE.md:38` mention "pytest (via bench)" but actual implementation uses `frappe.tests.utils.FrappeTestCase` and `bench run-tests` (unittest-style). Creates confusion about actual test runner. | Update documentation to clarify: "Uses Frappe's built-in test framework (unittest-based) via `bench run-tests`." If pytest support is planned, document explicitly: how it integrates with Frappe sites, fixture loading, whether `bench run-tests` remains primary. Consistency between docs and implementation prevents confusion. |
| **P3-003** | Test Coverage / Performance Testing | **opus45** (Primary), **sonn45** (Supporting) | **Missing Performance Tests: OrganizationMixin caching tested for correctness but not performance (N+1 prevention).** While cache correctness is tested, no verification that accessing multiple properties (`org_name`, `logo`, `org_status`) only triggers one database query instead of three (N+1 query problem). | Add performance test using query counting: Capture baseline, access multiple mixin properties, verify only ONE query executed. See sonn45 review for implementation example. This validates the primary value proposition of the caching mechanism. Can be added post-merge as enhancement. |
| **P3-004** | Test Coverage / Error Message Brittleness | **opus45** (Primary) | **Fragile Error Message Assertion: test_negative_hourly_rate_rejected checks for exact "negative" substring.** Test uses `self.assertIn("negative", str(context.exception).lower())` which breaks if validation message changes from "cannot be negative" to "must be positive". | Make assertion more robust by checking for semantic meaning: `assertTrue(any(keyword in error_msg for keyword in ["negative", "positive", "must be", "greater"]))`. Or check for field name presence rather than exact wording. Prevents test brittleness when improving user-facing error messages. |
| **P3-005** | Test Coverage / Concurrency Testing | **opus45** (Primary) | **Weak Concurrency Test: test_concurrent_org_member_creation tests sequential duplicates, not actual concurrency.** Test is named "concurrent" but doesn't use threading/multiprocessing to test actual race conditions. Only tests sequential duplicate insertion. | Rename to `test_duplicate_org_member_rejected` for accuracy. Add new `test_concurrent_org_member_creation_race_condition` using Python `threading` module to launch 5 parallel threads creating same Org Member. Verify exactly one succeeds and 4+ fail with duplicate error. See opus45 review for implementation. Tests true race condition protection. |

---

## 2. Summary & Architect Decision Log

### Synthesis Summary

The Basic Test Suite branch represents **substantial progress toward comprehensive test coverage** (estimated 85% of Features 1-9), with **799 lines of new test code** across Role Templates, Permission APIs, and Integration Workflows. All four reviewers praised the test structure, documentation quality, and use of Frappe patterns.

However, **cross-cutting architectural issues emerged** from incomplete refactoring during Company DocType module migration, test helpers that violate the documented Organization-first lifecycle, and premature testing of unimplemented features (OrganizationMixin, slug fields). The most severe issues—duplicate dictionary keys in hooks.py, broken Organization controller code, and System Manager role in permission tests—must be fixed before merge to prevent runtime failures and false test coverage.

**Key Patterns Identified:**
1. **Scope Creep:** Tests for Feature 8 (OrganizationMixin) included despite Feature 8 not being implemented
2. **Architectural Drift:** Test helpers assume concrete-first creation flow, contradicting documented Organization-first architecture
3. **Incomplete Migrations:** Company module move from dartwing_core → dartwing_company left duplicate hooks and import paths
4. **Weak Permission Testing:** System Manager role bypasses the very permissions being tested

**Estimated Effort:** 1 day focused work to address 8 P1-Critical issues + 4 hours for high-impact P2-Medium items.

---

### Conflict Resolution Log

#### Conflict #1: OrganizationMixin Tests vs Implementation

**Reviewers:**
- **sonn45:** Identified as **P1-Critical** - "Tests will fail with AttributeError, Feature 8 not implemented yet"
- **opus45:** Identified as **P1-Critical** - "Missing cache invalidation, need on_update hook"
- **gemi30:** Mentioned as **P2-Medium** - "Note cache invalidation in long-running processes"

**Conflict:** sonn45 says remove tests entirely (not implemented), opus45 says add implementation (on_update hook), gemi30 says improve caching strategy.

**Architectural Decision (dartwing_core_features_priority.md Line 240-270):**
- Feature 8 (OrganizationMixin) is documented as coming AFTER Feature 10 (Basic Test Suite) in the implementation roadmap
- Precedence: The PRD priority document explicitly lists Feature 10 before Feature 8
- **Resolution:** Remove `test_organization_mixin.py` from this branch entirely (**sonn45's position wins**). Feature 8 should be its own branch with: spec → implementation → tests in that order. This prevents false coverage (tests passing for unimplemented features). opus45's cache invalidation fix should be implemented **in Feature 8's branch**, not this one.
- **Rationale:** Adheres to documented feature sequencing and prevents scope creep. Tests without implementations create false confidence and confusion.

---

#### Conflict #2: Test Helper Creation Flow (Organization-first vs Concrete-first)

**Reviewers:**
- **GPT52:** Identified as **P1-Critical** - "Breaks Company paths, architectural violation"
- **opus45:** Not explicitly mentioned but cleanup logic assumes Organization cascade works
- **gemi30:** Not explicitly mentioned
- **sonn45:** Tests reference unimplemented flows

**Conflict:** Should test helpers create concrete types first (current implementation) or Organization first (architectural spec)?

**Architectural Decision (dartwing_core_arch.md Section 3.2 + org_integrity_guardrails.md):**
- Architecture document Section 3.2 explicitly states: **"When an Organization is created, a hook automatically creates the corresponding Concrete Doctype"**
- The "Bidirectional Linking" pattern is designed as: **Create Organization → Hook creates Concrete Type → Hook links them**
- Company DocType JSON shows `organization` field is **mandatory** (`"reqd": 1`), making concrete-first impossible without schema violations
- **Resolution:** All test helpers MUST create Organization first, let hooks create concrete type, then fetch concrete type via `linked_name` (**GPT52's position wins**).
- **Rationale:** (1) Matches production behavior users will encounter, (2) Enforces schema constraints, (3) Tests the actual hook logic that's critical to data integrity, (4) Prevents architectural drift where tests assume different flows than production.

---

#### Conflict #3: API Helper Test File Location/Naming

**Reviewers:**
- **gemi30:** Identified as **P1-Critical** - "Missing test_api_helpers.py file, deviation from plan"
- **sonn45:** Identified as **P2-Medium** - "API helper tests completely missing, critical for Flutter"
- **GPT52:** Not explicitly mentioned
- **opus45:** Not explicitly mentioned

**Conflict:** Should we create a new consolidated `test_api_helpers.py` file or accept distributed API tests?

**Architectural Decision (dartwing_core_prd.md Section 10.2 + constitution.md API-First Principle):**
- Constitution states: "All business logic MUST be exposed via @frappe.whitelist() API methods"
- PRD Section 10.2 emphasizes API-first development for Flutter/external client compatibility
- Current implementation HAS API tests but they're distributed: `test_permission_api.py` (exists), `test_organization_hooks.py` (exists)
- **Resolution:** Accept distributed API tests BUT rename `test_permission_api.py` → `test_api_permissions.py` to clarify scope. Document in code review that API tests are organized by **domain** (permissions, organization lifecycle) not in one monolithic file (**gemi30's concern addressed via documentation**).
- **Rationale:** Distributed tests by domain are more maintainable than one giant API test file. The tests exist and are comprehensive - naming/organization is secondary. This aligns with Frappe's pattern of DocType-specific test files.

---

#### Conflict #4: System Manager Role in Integration Tests

**Reviewers:**
- **GPT52:** Identified as **P2-Medium** - "Weakens permission assertions"
- **sonn45:** Identified as **P2-Medium** - "Test isolation issue, defeats permission testing"
- **opus45:** Not explicitly mentioned but related to permission validation concerns
- **gemi30:** Not explicitly mentioned

**Conflict:** Should integration tests use System Manager (current) or Dartwing User (recommended)?

**Architectural Decision (dartwing_core_arch.md Section 8.2.2 Role Hierarchy + constitution.md Security Principle 5):**
- Constitution Section 5 states: "Role-based access control via Frappe permissions" is non-negotiable
- Architecture Section 8.2.2 defines role hierarchy: System Manager (full access) vs Dartwing User (standard member)
- The PURPOSE of Feature 5 (User Permission Propagation) is to test that **non-admin users** only see their organizations
- **Resolution:** Change test users to **Dartwing User** role in integration tests (**GPT52 and sonn45's position wins**). Add explicit assertions that verify permission enforcement. Keep ONE test that explicitly verifies "System Manager sees all orgs" as documented admin behavior.
- **Rationale:** Tests must reflect real-world user scenarios. Using System Manager defeats the purpose of permission tests because it bypasses all User Permission logic. The spec (Feature 5) explicitly requires testing that User Permissions **restrict** access.

---

#### Conflict #5: Company "Synced" Fields Implementation

**Reviewers:**
- **GPT52:** Identified as **P1-Critical** - "Data drift risk, no sync mechanism"
- **opus45:** Not explicitly mentioned
- **gemi30:** Not explicitly mentioned
- **sonn45:** Not explicitly mentioned (but related to Company migration issues)

**Conflict:** How should Company fields marked "synced from Organization" actually sync?

**Architectural Decision (constitution.md Section 1 - Single Source of Truth + Frappe low-code philosophy):**
- Constitution Section 1 states: "Single Source of Truth - ONE Organization doctype handles all organization types"
- Frappe low-code philosophy: Use framework features (fetch_from, depends_on) over manual code
- Manual syncing via hooks is error-prone and defeats the purpose of a normalized data model
- **Resolution:** Replace manual syncing with Frappe's native **`fetch_from`** mechanism (**GPT52's position wins**). Update Company DocType JSON to use `fetch_from: "organization.org_name"` and `fetch_from: "organization.status"` with `read_only: 1`. Remove these fields from `ORG_FIELD_MAP` since fetch_from handles propagation automatically.
- **Rationale:** (1) Frappe-native approach (low-code principle), (2) Automatic propagation on save, (3) Prevents manual edits that create inconsistency, (4) Simpler than hook-based syncing, (5) Aligns with "Organization as Single Source of Truth."

---

## 3. Recommended Merge Sequence

1. **MUST FIX (Blocking):** Address all P1-001 through P1-008 before requesting re-review
2. **SHOULD FIX (High Value):** Address P2-001 through P2-004 in same commit for clean merge
3. **CAN DEFER (Post-Merge):** P2-005 through P2-009 can be follow-up tasks if time-constrained
4. **ENHANCEMENT (Future):** P3-001 through P3-005 are technical debt items for future sprints

**Validation Checklist Before Merge:**
```bash
# 1. Verify Python syntax (no compilation errors)
python -m py_compile dartwing/hooks.py
python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py

# 2. Clear cache and migrate (fresh state)
bench --site <site> clear-cache
bench --site <site> migrate

# 3. Run full test suite (all tests pass or skip gracefully)
bench --site <site> run-tests --app dartwing

# 4. Verify zero flakiness (run 3 times, all pass)
for i in {1..3}; do
    echo "Run $i/3"
    bench --site <site> run-tests --app dartwing || exit 1
done

# 5. Check for leftover test data (clean slate)
bench --site <site> console
>>> frappe.db.count("Organization", {"org_name": ["like", "%Test%"]})
# Should be 0
```

---

## 4. Positive Reinforcement & Strengths

**Exceptional Work Across Reviews:**

1. **Test Structure (All Reviewers):** Consistent praise for organization, documentation, and Frappe pattern usage
2. **Role Template Coverage (opus45, sonn45):** Comprehensive testing of all 4 org types, supervisor flags, hourly rates, and edge cases
3. **Integration Test Design (opus45, sonn45, GPT52):** Workflow tests (T031-T033c) cover realistic user journeys and valuable edge cases
4. **Documentation (gemi30, sonn45):** Excellent traceability with FR-XXX references and clear docstrings

**This branch sets a high bar for test quality** and will provide strong regression protection once the architectural alignment issues are resolved.

---

**End of Master Review**

**Next Steps:** Address P1-001 through P1-008, then request re-review focusing on architectural compliance verification.
