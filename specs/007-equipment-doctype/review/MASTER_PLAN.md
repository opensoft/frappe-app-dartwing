# MASTER ACTION PLAN: 007-Equipment-DocType (Second Pass)

**Synthesized By:** Director of Engineering
**Date:** 2025-12-14
**Branch:** `007-equipment-doctype`
**Reviews Consolidated:** opus45, jeni52, grokf1, sonn45

---

## Executive Summary

All **original P1 security issues** from the first review cycle have been successfully resolved. This second-pass synthesis consolidates findings from four reviewers who performed deep-dive analysis on the post-fix implementation.

**Key Finding:** While security vulnerabilities are addressed, **4 new HIGH-priority issues** were discovered relating to:
1. API permission bypass via `frappe.get_all()`
2. Test fixtures incompatible with current schema
3. Incomplete audit trail for initial assignments
4. Business logic gap for status-assignment validation

---

## 1. Master Action Plan (Prioritized & Consolidated)

### P1: CRITICAL — Must Fix Before Merge

| ID | Type | Source(s) | Issue Description (Consolidated) | Actionable Fix |
|:---|:-----|:----------|:---------------------------------|:---------------|
| **P1-NEW-01** | Security | jeni52, opus45 | **API Permission Bypass: `frappe.get_all()` ignores permissions.** Both `get_equipment_by_organization()` and `get_equipment_by_person()` use `frappe.get_all()` which explicitly sets `ignore_permissions=True` in Frappe 15. `get_equipment_by_person()` is particularly severe: returns ALL equipment assigned to a Person across ALL organizations, leaking equipment from orgs the caller cannot access. This violates tenant isolation per `dartwing_core_arch.md` Section 8.2.1. | **Replace `frappe.get_all()` with `frappe.get_list()` in both methods** (lines 247, 285). For `get_equipment_by_person()`, add organization filter: `user_orgs = frappe.get_all("User Permission", filters={"user": user, "allow": "Organization"}, pluck="for_value")` then use filter `{"assigned_to": person, "owner_organization": ["in", user_orgs]}`. This leverages the registered `permission_query_conditions` and enforces row-level security. |
| **P1-NEW-02** | Test Quality | jeni52 | **Test Fixtures Violate Mandatory Fields.** `test_equipment.py` fixtures create Person without `primary_email` (reqd:1) and `source` (reqd:1), and Org Member without `role` (reqd:1). Tests will fail in clean environment, providing false confidence. Per constitution.md Section 6, tests must be runnable. | **Update `setUpClass()` and all Person fixtures**: Add `primary_email=f"test-{frappe.generate_hash(length=8)}@example.com"`, `source="import"`, `status="Active"`. For Org Member, create a Role Template fixture (`role_name="Test Role"`, `applies_to_org_type="Company"`) and set `role=<role_template_name>`. |
| **P1-NEW-03** | Audit Compliance | sonn45 | **Initial Assignment Not Logged.** `_log_assignment_change()` returns early for new documents (`if self.is_new(): return`), so equipment created WITH `assigned_to` set never logs the initial assignment. Violates HIPAA/SOC2 custody tracking per `dartwing_core_arch.md` Section 8.1 (Comprehensive activity logging). | **Modify `_log_assignment_change()`**: For new docs, if `assigned_to` is set, call `self.add_comment("Info", _("Equipment initially assigned to {0}").format(self.assigned_to))` before returning. For updates, keep existing logic for change detection. |
| **P1-NEW-04** | Business Logic | sonn45 | **Assignment Allowed for Lost/Stolen/Retired Equipment.** No validation prevents assigning equipment when `status` is "Lost", "Stolen", or "Retired". Creates data inconsistency: "Who has this stolen laptop?" This is a spec gap requiring business rule clarification. | **Add status-assignment validation in `validate_assigned_person()`**: Either (a) block assignment for non-active statuses with `frappe.throw()`, or (b) warn with `frappe.msgprint(..., indicator="orange")` if tracking "last known user" is desired. Recommend option (a) as default. Document the business rule in spec.md. |

### P2: MEDIUM — Should Fix Before/Shortly After Merge

| ID | Type | Source(s) | Issue Description (Consolidated) | Actionable Fix |
|:---|:-----|:----------|:---------------------------------|:---------------|
| **P2-NEW-01** | Contract Drift | jeni52 | **OpenAPI Enum Missing Status Options.** `specs/007-equipment-doctype/contracts/equipment-api.yaml` declares `enum: [Active, In Repair, Retired]` but code now supports "Lost" and "Stolen". Flutter/client generators will reject valid server values. | Update all `status` enum declarations in `equipment-api.yaml` to include `Lost` and `Stolen`. Ensure example payloads align. |
| **P2-NEW-02** | UX | jeni52, sonn45 | **Error Message References Non-Existent Workflow.** `validate_owner_organization_immutable()` says "Use Equipment Transfer if ownership needs to change" but no such workflow exists. Creates support burden. | Change error message to: "Cannot change Equipment ownership after creation. Contact an administrator to arrange ownership transfer." Or document the planned Equipment Transfer workflow in spec.md with a TODO. |
| **P2-NEW-03** | Hook Ordering | jeni52 | **`on_update` Hook Order Risk.** `handle_status_change` (removes permissions) runs before `check_equipment_assignments_on_member_deactivation`. If deactivation is blocked, extra permission work and log entries occur (even if rolled back). | In `hooks.py` line 190-193, swap order: equipment deactivation check first, then `handle_status_change`. |
| **P2-NEW-04** | Performance | sonn45 | **Redundant `get_doc_before_save()` Calls.** `_log_assignment_change()` calls `has_value_changed()` (which internally fetches doc_before) then calls `get_doc_before_save()` again. Same pattern in `check_equipment_assignments_on_member_deactivation()`. Results in 2x DB queries per operation. | Refactor both methods: fetch `doc_before = self.get_doc_before_save()` once, then compare fields directly instead of using `has_value_changed()`. |
| **P2-NEW-05** | Robustness | sonn45 | **Missing Error Handling for `get_doc_before_save()`.** Edge cases (DB failures, race conditions) can raise exceptions instead of returning None, causing unclear error messages. | Wrap `get_doc_before_save()` calls in try-except. Log error with `frappe.log_error()` and either skip validation or use conservative approach. |
| **P2-NEW-06** | Maintainability | jeni52, opus45, sonn45 | **Permission Check Code Duplication.** Administrator/System Manager bypass pattern repeated 6+ times across `equipment.py` and `permissions/equipment.py`. Increases drift risk (as seen with `get_all` bypass). | Extract to helper: `def _is_privileged_user(user=None) -> bool` in `dartwing/permissions/helpers.py`. Use consistently across all permission-related code. |
| **P2-NEW-07** | Maintainability | sonn45 | **Raw SQL Fragility in `get_org_members()`.** Direct SQL query hardcodes "Active" status string, duplicates Person name concatenation logic, and bypasses ORM protections. Schema changes will break silently. | Refactor to use Frappe ORM: `frappe.get_all("Org Member", ...)` followed by `frappe.get_list("Person", ...)` or leverage `frappe.desk.search.search_widget()`. |
| **P2-DEFER-01** | Performance | opus45, grokf1 | **Request-Level Caching for Permission Queries.** `get_permission_query_conditions_equipment()` fetches User Permissions on every request. | Implement caching: `cache_key = f"_user_orgs_{frappe.scrub(user)}"` in `frappe.local`. Extract to shared helper in `dartwing/permissions/helpers.py`. Mark as DEFERRED — implement if performance issues arise. |
| **P2-DEFER-02** | Maintainability | opus45, grokf1 | **Hardcoded Status Strings.** Status values duplicated in `.py`, `.json`, `.js` files. | Define constants in `equipment.py`: `class EquipmentStatus: ACTIVE = "Active"...`. Mark as DEFERRED — low risk. |
| **P2-DEFER-03** | Data Integrity | opus45, grokf1 | **Missing Location Validation.** `current_location` (Address link) not validated against `owner_organization`. | Add `validate_current_location()` with warning (not throw) for flexibility. Mark as DEFERRED — may be intentionally flexible for shared facilities. |

### P3: LOW — Future Technical Debt

| ID | Type | Source(s) | Issue Description (Consolidated) | Actionable Fix |
|:---|:-----|:----------|:---------------------------------|:---------------|
| **P3-01** | Test Coverage | jeni52, opus45 | **No Tests for Non-Admin Permission Logic.** All tests run as Administrator, bypassing `validate_user_can_access_owner_organization()`. Permission fixes are untested. | Add test case using `frappe.set_user()` with a Dartwing User (no System Manager role) to verify permission enforcement. |
| **P3-02** | Code Quality | sonn45 | **Inconsistent Administrator Check Pattern.** Mix of positive (`user == "Administrator" or ...`) and negative (`user != "Administrator" and ...`) patterns reduces readability. | Standardize on positive check pattern using the helper function from P2-NEW-06. |
| **P3-03** | Security | opus45 | **Search Wildcard Handling.** `get_org_members()` uses `f"%{txt}%"` without escaping SQL wildcards (`%`, `_`). Low risk but causes unexpected search results. | Escape wildcards: `escaped_txt = txt.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")`. |
| **P3-04** | Permissions | opus45 | **Delete Permission Gap.** `Dartwing User` role has CRUD minus delete. Verify this is intentional (equipment should be Retired, not deleted). | Document in spec.md or add `"delete": 1` to `equipment.json` if users should delete. |
| **P3-05** | Code Quality | sonn45 | **Missing Type Hints.** Python 3.11+ supports type hints but Equipment controller doesn't use them extensively. | Add return type hints to public methods: `def validate_assigned_person(self) -> None:`. Low priority — developer experience enhancement. |
| **P3-DEFER** | Various | All | **Original P3 Items from First Pass.** Docstring accuracy, document type extensibility, maintenance automation, field descriptions, API helper relocation, database indexes. | See original MASTER_PLAN.md Section 3.2 for details. All remain DEFERRED. |

---

## 2. Summary & Architect Decision Log

### Synthesis Summary

The Equipment DocType implementation is **fundamentally production-ready** with all original P1 security vulnerabilities resolved. The four reviewers provided convergent feedback on the quality of fixes, with grokf1 rating the implementation "exceptionally well-architected" and sonn45 scoring it 8.5/10. However, deeper analysis revealed **4 new critical issues**:

1. **API Permission Bypass** (jeni52 + opus45): The discovery that `frappe.get_all()` explicitly ignores permissions in Frappe 15 represents a significant finding. While the original P1-02 fix added User Permission checks, these are defense-in-depth and don't leverage the framework's permission system. The recommended fix using `frappe.get_list()` is the idiomatic Frappe pattern.

2. **Test Suite Failure** (jeni52): The test fixtures created during P2-01 implementation don't account for mandatory fields added in other feature branches. This is a merge timing issue that must be addressed to ensure CI passes.

3. **Audit Trail Gap** (sonn45): The initial assignment logging oversight is subtle but compliance-critical. The fix is minimal (4 lines of code) but essential for custody tracking.

4. **Status-Assignment Validation** (sonn45): This represents a spec gap rather than a bug. The business rule must be defined: can Lost/Stolen/Retired equipment be assigned? The architecture document doesn't specify, so this requires product decision.

### Conflict Resolution Log

| Conflict | Reviewers | Resolution | Justification |
|:---------|:----------|:-----------|:--------------|
| **Permission Bypass Severity** | jeni52 rated CRITICAL (identifies `frappe.get_all` root cause), opus45 rated MEDIUM (focused on org filter fix) | **Resolved as P1-CRITICAL** | jeni52 correctly identified that `frappe.get_all()` bypasses all DocType permissions in Frappe 15. The opus45 suggested fix (adding org filter) is necessary but insufficient — must use `frappe.get_list()` to leverage `permission_query_conditions`. Per `dartwing_core_arch.md` Section 8.2.1, permissions flow through Frappe's registered hooks. |
| **Test Fixture Severity** | jeni52 rated HIGH (blocking), grokf1 did not flag, sonn45 did not flag | **Resolved as P1-CRITICAL** | jeni52 correctly identified that tests won't execute in a clean environment. Per constitution.md Section 6 (Tests required for business logic), non-functional tests are worse than no tests because they create false confidence. Tests must be runnable. |
| **Initial Assignment Logging** | sonn45 rated HIGH, other reviewers did not flag | **Resolved as P1-CRITICAL** | sonn45's deep analysis revealed a compliance gap. Per `dartwing_core_arch.md` Section 8.1 (Comprehensive activity logging for compliance), initial custody assignment is as critical as subsequent changes. The fix is minimal and must be included. |
| **Status-Assignment Validation** | sonn45 rated HIGH, other reviewers did not flag | **Resolved as P1-CRITICAL (Pending Business Rule)** | This requires product decision. However, it blocks merge because the current behavior (allowing assignment to Lost/Stolen equipment) is likely incorrect. Default to blocking assignment for non-active statuses; document the rule. |
| **Hook Ordering on `on_update`** | jeni52 rated MEDIUM | **Resolved as P2** | While the first-pass fixed `on_trash` ordering (P1-04), the same pattern issue exists in `on_update`. Less critical because permission changes are reversible, but should be fixed for consistency. |
| **`get_org_members()` SQL vs ORM** | sonn45 rated MEDIUM (refactor to ORM), jeni52 focused on permission bypass | **Resolved as P2-NEW-07** | Both reviewers identify issues with the method. The permission bypass is covered by P1-NEW-01 (using `frappe.get_list` enforces permissions). The SQL fragility is a separate maintainability concern that can be addressed in follow-up. |
| **Performance Optimizations** | sonn45 identified specific DB query duplication, opus45/grokf1 noted caching as deferred | **Resolved as P2-NEW-04 (immediate) + P2-DEFER-01 (caching)** | The redundant `get_doc_before_save()` calls are easy fixes with measurable benefit. Request-level caching is more complex and can wait for performance profiling. |

---

## 3. Implementation Checklist

### Required Before Merge (Estimated: 3-4 hours)

- [ ] **P1-NEW-01**: Replace `frappe.get_all()` with `frappe.get_list()` in API methods; add org filter to `get_equipment_by_person()`
- [ ] **P1-NEW-02**: Fix test fixtures with mandatory fields; add Role Template fixture
- [ ] **P1-NEW-03**: Log initial assignment in `_log_assignment_change()`
- [ ] **P1-NEW-04**: Add status-assignment validation (requires business rule decision)
- [ ] **P2-NEW-01**: Update OpenAPI contract with Lost/Stolen status options
- [ ] **P2-NEW-02**: Update error message for organization immutability

### Recommended Before Merge (Estimated: 1-2 hours)

- [ ] **P2-NEW-03**: Reorder `on_update` hooks
- [ ] **P2-NEW-04**: Optimize redundant `get_doc_before_save()` calls
- [ ] **P2-NEW-06**: Extract `_is_privileged_user()` helper (reduces duplication)

### Post-Merge Technical Debt

- [ ] P2-NEW-05: Error handling for `get_doc_before_save()`
- [ ] P2-NEW-07: Refactor `get_org_members()` to use ORM
- [ ] P2-DEFER-01: Request-level caching
- [ ] P2-DEFER-02: Status constants
- [ ] P2-DEFER-03: Location validation
- [ ] P3-01 through P3-05: Various low-priority items

---

## 4. Verification of Original P1 Fixes

All reviewers independently verified that the original 5 P1 critical issues have been successfully resolved:

| Original Issue | Status | Verification Notes |
|:---------------|:-------|:-------------------|
| P1-01: SQL Injection | **FIXED** | Line 47: `frappe.db.escape(o)` without extra quotes |
| P1-02: Cross-Tenant API | **FIXED** | Auth checks at lines 186-197, 228-241, 276-283 (but see P1-NEW-01 for remaining gap) |
| P1-03: FR-013 Deactivation | **FIXED** | `check_equipment_assignments_on_member_deactivation()` at line 345 |
| P1-04: Hook Ordering (`on_trash`) | **FIXED** | Equipment check before permission removal in hooks.py:185-188 |
| P1-05: Create Authorization | **FIXED** | `validate_user_can_access_owner_organization()` at line 127 |

---

## 5. Quality Metrics

| Metric | Score | Notes |
|:-------|:------|:------|
| **Security Posture** | 8/10 | Original vulnerabilities fixed; P1-NEW-01 is defense-in-depth gap |
| **Code Quality** | 8.5/10 | Well-structured; minor duplication and optimization opportunities |
| **Test Coverage** | 6/10 | Tests exist but have fixture issues and don't cover permissions |
| **API Contract Alignment** | 7/10 | OpenAPI needs update for new status options |
| **Frappe Idiom Adherence** | 7/10 | Good overall; should use `frappe.get_list()` instead of `get_all()` |
| **Overall Merge Readiness** | **Not Ready** | 4 P1 issues must be resolved first |

---

## 6. Appendix: Files Requiring Changes

### P1 Critical Fixes

| File | Lines | Change |
|:-----|:------|:-------|
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 247, 285 | Replace `frappe.get_all()` with `frappe.get_list()` |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 276-298 | Add organization filter to `get_equipment_by_person()` |
| `dartwing/dartwing_core/doctype/equipment/test_equipment.py` | 23-56 | Fix Person and Org Member fixtures with mandatory fields |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 34-52 | Log initial assignments for new equipment |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | 95-125 | Add status-assignment validation |

### P2 Medium Fixes

| File | Change |
|:-----|:-------|
| `specs/007-equipment-doctype/contracts/equipment-api.yaml` | Add Lost/Stolen to status enums |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | Update immutability error message |
| `dartwing/hooks.py` | Reorder `on_update` hooks for Org Member |
| `dartwing/dartwing_core/doctype/equipment/equipment.py` | Optimize `get_doc_before_save()` usage |
| `dartwing/permissions/helpers.py` | Add `_is_privileged_user()` helper (new file or add to existing) |

---

**End of Master Plan (Second Pass)**

**Next Steps:**
1. Obtain business rule decision for status-assignment validation (P1-NEW-04)
2. Implement all P1 fixes
3. Run full test suite to verify
4. Implement recommended P2 fixes
5. Merge to main
6. Create follow-up tickets for deferred items
