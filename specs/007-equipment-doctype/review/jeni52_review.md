# Code Review (Second Pass) — `007-equipment-doctype` (Equipment DocType)

## Scope & Context Used

- **Feature intent:** Equipment is a polymorphic, Organization-scoped asset registry (owned by `Organization`) with assignment to `Person`, location (`Address`), documents, maintenance schedule, and strict org isolation (FR-003/FR-009).
- **Architecture / PRD:** `docs/dartwing_core/dartwing_core_arch.md` (3.11–3.14) and `docs/dartwing_core/dartwing_core_prd.md` (tasks + maintenance scheduling integration).
- **Branch spec:** `specs/007-equipment-doctype/spec.md`, `specs/007-equipment-doctype/data-model.md`, and API contract `specs/007-equipment-doctype/contracts/equipment-api.yaml`.
- **Master Plan verification:** `specs/007-equipment-doctype/review/MASTER_PLAN.md` indicates the original P1 items (permission SQL quoting, cross-tenant leak in `get_org_members`, FR-013 deactivation gap, hook ordering on delete, create-path authorization) are implemented. I validated those fixes exist in the current code.

This document lists **only the remaining current issues** after the Master Plan fixes.

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 Whitelisted list endpoints bypass Frappe permissions (and `get_equipment_by_person` can leak cross-organization equipment)

- **Where:**
  - `dartwing/dartwing_core/doctype/equipment/equipment.py:214-260` (`get_equipment_by_organization`)
  - `dartwing/dartwing_core/doctype/equipment/equipment.py:263-299` (`get_equipment_by_person`)
- **Problem:**
  - Both endpoints use `frappe.get_all(...)` which **explicitly sets `ignore_permissions=True`** in Frappe 15, i.e. it bypasses DocType permission rules and permission query conditions.
  - `get_equipment_by_organization()` *partially* compensates by checking `User Permission` for the requested Organization (so it’s not trivially open), but it still bypasses:
    - doctype-level role checks (e.g. a user with an Organization User Permission but without the “Dartwing User” role can still retrieve Equipment via this endpoint), and
    - any future additional permission logic that you may add to Equipment.
  - `get_equipment_by_person()` is worse: it checks `frappe.has_permission("Person", "read", person)` (good), but then returns **all equipment assigned to that Person across all organizations** because the query filter is only `{"assigned_to": person}` and permissions are bypassed.
    - In a multi-org reality (Person belongs to multiple orgs), this can leak equipment owned by orgs the caller does not have access to.
- **Why this blocks merge:**
  - This is an **authorization bug** in public API surface (`@frappe.whitelist()`), and it undermines the tenant isolation model this project is built on.
  - It also violates the principle “permissions are enforced centrally by Frappe” rather than duplicated ad-hoc in endpoints.
- **Concrete fix suggestion (recommended pattern):**
  1. Replace `frappe.get_all` with `frappe.get_list` (or `frappe.get_all(..., ignore_permissions=False)` is not possible, because `get_all` forces ignore_permissions).
     - Example for org endpoint:
       - Use `frappe.get_list("Equipment", filters=..., fields=..., order_by=..., limit_page_length=..., limit_start=...)`
       - This will automatically apply `permission_query_conditions` for Equipment + role-based permissions.
  2. Keep the explicit organization access check as a defense-in-depth *or* replace it with canonical permission checks:
     - Prefer: `frappe.has_permission("Organization", "read", organization)` (or a shared helper used across the codebase).
  3. Fix `get_equipment_by_person()` to constrain results to organizations the caller can access:
     - **Option A (best API design):** require an `organization` parameter and apply both filters:
       - `filters={"assigned_to": person, "owner_organization": organization}`
       - plus permission check for that organization.
     - **Option B (still safe):** compute allowed orgs from User Permission and add an IN filter:
       - `allowed_orgs = frappe.get_all("User Permission", filters={"user": user, "allow": "Organization"}, pluck="for_value")`
       - `filters={"assigned_to": person, "owner_organization": ("in", allowed_orgs)}`
     - Either way, keep `frappe.has_permission("Person", "read", person)` (or re-evaluate the Person permission model if “read person” is too broad).

### 1.2 Equipment test suite fixtures violate current DocType mandatory fields (tests will fail and provide false confidence)

- **Where:** `dartwing/dartwing_core/doctype/equipment/test_equipment.py:23-56`
- **Problem:**
  - `Person` creation in `setUpClass` omits mandatory fields:
    - `primary_email` is `reqd: 1` in `dartwing/dartwing_core/doctype/person/person.json`.
    - `source` is `reqd: 1` in `dartwing/dartwing_core/doctype/person/person.json`.
    - Depending on controller logic, other required fields may also be enforced.
  - `Org Member` creation omits mandatory `role`:
    - `role` is `reqd: 1` in `dartwing/dartwing_core/doctype/org_member/org_member.json`.
  - The same issue repeats in `test_assignment_requires_org_membership()` where the “other_person” fixture is created without required fields (`test_equipment.py:145-167`).
- **Why this blocks merge:**
  - This branch claims test coverage (“12 comprehensive test cases” per Master Plan), but the tests **won’t execute successfully** in a clean environment. That’s worse than missing tests because it creates a misleading signal for reviewers/CI.
- **Concrete fix suggestion (minimal but correct):**
  1. Update Person fixtures in tests to include mandatory fields (and ensure uniqueness):
     - Provide `primary_email` with a random/unique value (e.g. `f"test-equipment-{frappe.generate_hash(length=8)}@example.com"`).
     - Provide `source="import"` (or `"signup"` if you want to simulate real creation).
     - Provide `status="Active"` explicitly for clarity.
  2. Ensure `Org Member` fixture includes a valid `role` for the org type:
     - Create a Role Template doc in test setup (preferred for hermetic tests) with:
       - `role_name` (unique), `applies_to_org_type="Company"`, and a safe default for other required fields.
     - Then set `role=<role_template_name>` when inserting Org Member.
  3. Add at least one test that runs as a **non-Administrator** user to validate the most important security rule you added:
     - `validate_user_can_access_owner_organization()` is bypassed for Administrator/System Manager, so current tests do not verify it.
     - Use `frappe.set_user(test_user)` (or context manager) + create the relevant User Permission rows to simulate real access control.

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 API contract drift: OpenAPI enums do not match the implemented status options

- **Where:** `specs/007-equipment-doctype/contracts/equipment-api.yaml:284-285`, `:346-350`, `:417-420`
- **Problem:** Code/DocType allows `status ∈ {Active, In Repair, Retired, Lost, Stolen}` (`equipment.json`), but the OpenAPI contract still declares:
  - `enum: [Active, In Repair, Retired]`
- **Why it matters:**
  - Flutter/client generators and QA using the contract will reject valid server values, causing unnecessary client/server incompatibilities.
- **Concrete fix suggestion:**
  - Update all occurrences of `enum: [Active, In Repair, Retired]` to include `Lost` and `Stolen`, and ensure any examples/validation docs align.
  - If “Lost/Stolen” was intended as optional future scope, revert the DocType change instead (but then update tests that expect those statuses).

### 2.2 Reduce duplication in permission checks across whitelisted methods

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:186-242` and `:276-284`
- **Problem:** Organization/User Permission checks are re-implemented per method, increasing the chance of drift (as seen with the `get_all` permission bypass).
- **Concrete improvement:**
  - Create a small helper in the same module (or `dartwing/permissions/api.py` style helper) such as:
    - `_require_org_access(organization: str) -> None`
    - `_require_person_read(person: str) -> None`
  - Use these helpers consistently, and pair them with permission-aware query functions (`frappe.get_list`).

### 2.3 Messaging refers to non-existent workflow (“Equipment Transfer”)

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:47-58`
- **Problem:** Error copy says “Use Equipment Transfer if ownership needs to change.” There is no `Equipment Transfer` DocType/flow in this branch.
- **Why it matters:** Users/admins will search for a feature that doesn’t exist, turning a correct constraint into a support burden.
- **Concrete fix suggestion:**
  - Either (a) reference a real, existing process (“Contact an administrator to transfer ownership”) or (b) add the minimal “transfer” mechanism if it’s intentionally part of scope (but that’s likely a separate feature).

### 2.4 Hook ordering on `Org Member.on_update` could fail faster and avoid side effects

- **Where:** `dartwing/hooks.py` (Org Member `on_update` list)
- **Problem:** `handle_status_change` (which removes permissions) runs before `check_equipment_assignments_on_member_deactivation`. If deactivation is blocked due to equipment, you do extra permission work and log entries (even if rolled back).
- **Concrete fix suggestion:**
  - Swap the order so the equipment check runs first; treat permission propagation as the last step after validations.

---

## 3. General Feedback & Summary (Severity: LOW)

The branch is in much better shape after the Master Plan fixes: the Equipment DocType is well-aligned with the architecture (org-scoped ownership, assignment validation, deletion/deactivation guards, and improved Desk UX). The remaining work is primarily about tightening the API permission model (avoid `frappe.get_all` in whitelisted list endpoints) and fixing the test suite so it reflects the current mandatory fields and actually validates non-admin authorization behavior. Once those are corrected, this feature will be substantially closer to “merge-ready” with strong security posture and reliable regression protection.
