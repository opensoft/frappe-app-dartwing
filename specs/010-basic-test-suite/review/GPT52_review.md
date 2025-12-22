# GPT52 Code Review — `010-basic-test-suite` (`dartwing_core`)

## Context I Used

- Standards: `bench/apps/dartwing/.specify/memory/constitution.md`
- Architecture/product references: `bench/apps/dartwing/docs/dartwing_core/dartwing_core_arch.md`, `bench/apps/dartwing/docs/dartwing_core/dartwing_core_prd.md`, `bench/apps/dartwing/docs/dartwing_core/org_integrity_guardrails.md`, `bench/apps/dartwing/docs/dartwing_core/person_doctype_contract.md`
- Feature mapping: `bench/apps/dartwing/docs/dartwing_core/wip/dartwing_core_features_priority.md#L306` → **Feature 10: Basic Test Suite**
- Branch diff scope reviewed: `main..HEAD` for `010-basic-test-suite`

---

# 1. Critical Issues & Blockers (Severity: HIGH)

## 1.1 Integration tests assume unsupported “concrete-first creates Organization” flow (breaks Company paths)

**Where**
- `dartwing/tests/integration/test_full_workflow.py:138` (helper `_create_test_organization`)
- `dartwing/tests/integration/test_full_workflow.py:221` (creates Company via helper in `test_multi_org_membership_workflow`)
- `dartwing/dartwing_core/mixins/test_organization_mixin.py:78` (helper `_create_test_company`)
- `dartwing/dartwing_core/mixins/test_organization_mixin.py:315` (Company mixin test depends on `_create_test_company`)

**Why this is a blocker**
- `Company` requires `organization` (`dartwing/dartwing_company/doctype/company/company.json:52` shows `"reqd": 1`). Creating a `Company` document “first” without an `Organization` will fail mandatory validation in Frappe.
- Even if you bypass mandatory checks, the project’s own architecture positions **Organization as the source-of-truth** and the lifecycle driver (Organization → concrete) (see `bench/apps/dartwing/docs/dartwing_core/org_integrity_guardrails.md` and `bench/apps/dartwing/docs/dartwing_core/dartwing_core_arch.md`).
- Result: at least the Company branches in the new “full workflow” suite and the new mixin suite are expected to fail (or silently test the wrong behavior if later weakened with ignore_mandatory/force flags).

**Concrete fix options (pick one; Option A is the cleanest)**

**Option A (Recommended): Make tests follow the canonical flow (Organization-first)**
- Update `dartwing/tests/integration/test_full_workflow.py:138`:
  - Replace “create concrete first” with:
    1. Create `Organization` with `org_type=org_type` and `org_name` set.
    2. `org.insert(ignore_permissions=True)`
    3. `org.reload()` and fetch concrete via `org.linked_doctype` + `org.linked_name`.
  - This also exercises the real production behavior you want to protect from regressions.
- Update `dartwing/dartwing_core/mixins/test_organization_mixin.py:78`:
  - Don’t create `Company` directly. Instead:
    1. Create `Organization` with `org_type="Company"`.
    2. Fetch the created `Company` via `org.linked_name`.
    3. Use that `Company` instance to test the mixin.

**Option B: Implement concrete-first bidirectional linking for Company (and make schema consistent)**
- If you intentionally want “creating `Company` creates `Organization`”, then you need to implement it the same way `Family` now does:
  - Add `after_insert` to `dartwing/dartwing_company/doctype/company/company.py` mirroring the `Family.after_insert` pattern in `dartwing/dartwing_core/doctype/family/family.py:28`.
  - Decide whether `company.organization` should remain mandatory:
    - If mandatory stays `1`, “Company-first” cannot work without `ignore_mandatory` (not desirable for production).
    - If you relax it to allow insert, ensure Organization creation is **atomic** and consistent with guardrails (rollback on failure; idempotency).

**Option C: Keep tests concrete-first but pass an Organization explicitly**
- This is the least aligned with the architecture, but would make tests pass:
  - Create an `Organization` first, then create `Company(organization=org.name, company_name=...)`.
  - This does *not* validate the auto-creation logic and is weaker coverage than A/B.

---

## 1.2 `Company` DocType adds “synced from Organization” fields without actual sync mechanism (data drift risk)

**Where**
- `dartwing/dartwing_company/doctype/company/company.json:42` (`company_name` described as “synced from Organization”)
- `dartwing/dartwing_company/doctype/company/company.json:61` (`status` described as “synced from Organization”)

**Why this is a blocker**
- As implemented, these fields will only be set at creation time by Organization hooks (via `ORG_FIELD_MAP` in `dartwing/dartwing_core/doctype/organization/organization.py:33`), and then can drift:
  - If Organization name/status changes, the Company’s `company_name`/`status` will remain stale unless you add propagation logic.
  - Users can also edit `status` directly (it is not `read_only`), creating inconsistency against the “Single Source of Truth” principle stated in `bench/apps/dartwing/.specify/memory/constitution.md`.
- This is exactly the kind of subtle correctness problem that tends to *pass tests* but cause inconsistent UI/behavior later.

**Concrete fix (Frappe-native / low-code)**
- Prefer **`fetch_from` + read-only** instead of manual syncing:
  - In `dartwing/dartwing_company/doctype/company/company.json:42` set:
    - `fetch_from: "organization.org_name"`
    - `read_only: 1`
  - In `dartwing/dartwing_company/doctype/company/company.json:61` set:
    - `fetch_from: "organization.status"`
    - `read_only: 1`
- Keep `in_list_view` / `in_standard_filter` if you need those columns.
- If you *must* store denormalized values (e.g., for performance), then add a single authoritative propagation point:
  - Update `Organization` controller to propagate on save (and enforce immutability rules), but this is heavier than fetch_from and easier to get wrong.

---

## 1.3 Accidental extra “tests package” path likely to confuse imports and reviewers

**Where**
- `dartwing/dartwing/tests/integration/__init__.py:1` (note the extra `dartwing/dartwing/…` nesting)

**Why this is a blocker**
- The repo already has the correct test package at `dartwing/tests/integration/__init__.py` (and the new workflow test is correctly placed under `dartwing/tests/integration/`).
- Having a second, similarly named `dartwing.dartwing.tests.integration` package is confusing and increases the chance of running the wrong module path, IDE indexing oddities, or future accidental duplication.

**Concrete fix**
- Delete `dartwing/dartwing/tests/integration/__init__.py` and the now-empty `dartwing/dartwing/tests/integration/` directory if nothing else lives there.

---

# 2. Suggestions for Improvement (Severity: MEDIUM)

## 2.1 “Workflow” test user is a `System Manager`, weakening permission assertions

**Where**
- `dartwing/tests/integration/test_full_workflow.py:108` (`roles: [{"role": "System Manager"}]`)
- `dartwing/tests/integration/test_full_workflow.py:268` (note acknowledges System Manager may see all orgs)

**Suggestion**
- For permission propagation and list filtering, use the lowest-privilege role(s) that reflect real application use (e.g., `Dartwing User`) and rely on `User Permission` + hook query conditions to enforce scoping.
- Keep a single targeted test that *explicitly* verifies “admin-style roles can see all” only if that’s intended and documented.

## 2.2 Incomplete test: “manual permission deletion resilience” has no assertion

**Where**
- `dartwing/tests/integration/test_full_workflow.py:370` (`test_manual_permission_deletion_resilience`)

**Suggestion**
- Either:
  - Make it deterministic: assert that toggling status recreates permission (if that is required behavior), or
  - Convert it into an explicit expectation: `assertFalse(perm_recreated)` (if recreation is *not* expected), or
  - Skip it with a clear reason until the intended behavior is implemented (preferred over a non-asserting test that always passes).

## 2.3 Add DocType presence checks for every DocType the module actually uses

**Where**
- `dartwing/tests/integration/test_full_workflow.py:29` (`required_doctypes` omits `Company` but later uses it)

**Suggestion**
- If the suite is meant to be modular and skippable when modules aren’t installed, include all doctypes used by tests (e.g. `Company`) or split tests so Company paths are conditionally skipped.

## 2.4 Make test data isolation more consistent across new tests

**Where**
- `dartwing/tests/integration/test_full_workflow.py:45` (cleanup uses `TEST_PREFIX`)
- `dartwing/dartwing_core/mixins/test_organization_mixin.py:18` (cleanup uses `TEST_PREFIX`)

**Suggestion**
- The prefix pattern is good. Two improvements to reduce flakiness:
  - Avoid `except Exception: pass` in cleanup unless you log what failed (otherwise broken cascades can be masked).
  - Prefer deleting root documents only (Organization / concrete type) and let cascades handle children. You already mostly do this—keep it consistent.

## 2.5 Align spec wording (“pytest”) with actual runner usage

**Where**
- `CLAUDE.md:38` (mentions `pytest (via bench)`)
- `specs/010-basic-test-suite/plan.md:15` (mentions `pytest (via bench)`)

**Suggestion**
- The implementation uses `frappe.tests.utils.FrappeTestCase` and `bench run-tests` (unittest-style). If pytest is not actually used/required, avoid implying it’s the primary runner.
- If you *do* intend pytest, keep it explicit: how it runs with sites, how fixtures are loaded, and whether `bench run-tests` remains the supported path.

---

# 3. General Feedback & Summary (Severity: LOW)

The branch direction is right: you’re consolidating on `FrappeTestCase`, adding higher-level integration coverage, and tying the branch back to the documented “Feature 10: Basic Test Suite”. The main gaps are correctness and architectural alignment in the new tests—specifically around the Organization/concrete creation flow and the new “synced” fields in `Company` which currently have no real sync mechanism. Once the Company path is fixed and the workflow tests become deterministic (assertions, privilege level), this will be a strong regression safety net for the core multi-tenant model.

