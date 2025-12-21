# Verification Review (v2) — `008-organization-mixin` (`dartwing_core`)

## Verification Scope

- **Branch/spec:** `008-organization-mixin`
- **Git state:** Verified on branch `008-organization-mixin`
- **Master plan:** `specs/008-organization-mixin/review/FIX_PLAN.md` used as the master plan, enumerating P1/P2 items to be implemented and verified.

**Reference documents read:**
- `specs/008-organization-mixin/review/FIX_PLAN.md` (used as master plan substitute)
- `docs/dartwing_core/dartwing_core_arch.md` (notably 3.6 and 8.2.1)
- `docs/dartwing_core/dartwing_core_prd.md` (REQ-ORG-002 and Org model requirements)

---

# 1. Fix Verification & Regression Check (Severity: CRITICAL)

## P1 Verification (Must Fix Before Merge)

### P1-1: `update_org_name()` permission enforcement
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/mixins/organization_mixin.py:89` (normalizes input), `dartwing/dartwing_core/mixins/organization_mixin.py:114` (loads Organization doc), `dartwing/dartwing_core/mixins/organization_mixin.py:117` (explicit `org.check_permission("write")`), `dartwing/dartwing_core/mixins/organization_mixin.py:121` (`org.save()`).
- **Regression risk check:** ✅ Uses Document lifecycle (validations + hooks + audit trail). No permission bypass via `frappe.db.set_value()`.

### P1-2: Fix duplicate keys + syntax in `hooks.py`
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/hooks.py:121` (`permission_query_conditions` has a single `Company` entry), `dartwing/hooks.py:130` (`has_permission` has a single `Company` entry), `dartwing/hooks.py:174` (single `doc_events` dict; no duplicate assignment).
- **Regression risk check:** ✅ Removes silent overwrites; avoids permission hook ambiguity.

### P1-3: Negative ownership validation in `Company`
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_company/doctype/company/company.py:29` (method updated), `dartwing/dartwing_company/doctype/company/company.py:34` (rejects negative values with `frappe.throw`).
- **Regression risk check:** ✅ Error message is translatable and avoids `None` by using `mp.person or _("member")`.

### P1-4: Remove `__pycache__` from git + ignore going forward
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `.gitignore:2` contains `__pycache__/`. `git ls-files` shows no tracked `__pycache__` or `*.pyc` artifacts.
- **Regression risk check:** ✅ Prevents CI churn and noisy PR diffs.

### P1-5: Move tests to discoverable location
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/tests/unit/test_organization_mixin.py:1` exists; legacy file `dartwing/dartwing_core/tests/test_organization_mixin.py` is absent.
- **Regression risk check:** ✅ Aligns with app-level test discovery pattern (`dartwing/tests/`).

### P1-6: Family inherits `OrganizationMixin`
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/doctype/family/family.py:11` is `class Family(Document, OrganizationMixin):`.
- **Regression risk check:** ✅ No MRO conflict; consistent with Frappe mixin pattern.

## P2 Verification (Should Fix Soon)

### P2-1: Family permissions: `user_permission_dependant_doctype` + “Dartwing User”
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/doctype/family/family.json:145` sets `"user_permission_dependant_doctype": "Organization"`, and `dartwing/dartwing_core/doctype/family/family.json:130` includes role `"Dartwing User"`.
- **Architecture compliance:** ✅ Matches `docs/dartwing_core/dartwing_core_arch.md` 8.2.1 “Concrete Type Permissions (Auto-Inherited)”.

### P2-2: Mixin adoption for Association + Nonprofit
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/doctype/association/association.py:11` and `dartwing/dartwing_core/doctype/nonprofit/nonprofit.py:11` both inherit `OrganizationMixin`.

### P2-3: Type hints on mixin API
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/mixins/organization_mixin.py:39` (`Optional[Dict[str, Any]]`), `dartwing/dartwing_core/mixins/organization_mixin.py:66` (`Optional[str]`), `dartwing/dartwing_core/mixins/organization_mixin.py:83` (`Optional["Document"]`).

### P2-4: Remove manual commits from tests
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/tests/unit/test_organization_mixin.py` contains no `frappe.db.commit()` calls (search verified).

### P2-5: Introduce `CACHED_ORG_FIELDS` constant
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `dartwing/dartwing_core/mixins/organization_mixin.py:18` defines `CACHED_ORG_FIELDS`; used at `dartwing/dartwing_core/mixins/organization_mixin.py:55`.

### P2-6: Correct `research.md` guidance about `frappe.db.set_value()`
- **Status:** [SUCCESSFULLY IMPLEMENTED]
- **Evidence:** `specs/008-organization-mixin/research.md:16` and `specs/008-organization-mixin/research.md:139` explicitly state `frappe.db.set_value()` does **not** enforce permissions and recommend `get_doc()` + `check_permission()` + `save()`.

## Regression Check (New Issues Introduced By Fixes)

- **No new security regressions found** in the updated write-path: `OrganizationMixin.update_org_name()` now correctly treats Organization as the permission boundary (aligns with `docs/dartwing_core/dartwing_core_arch.md:1262` and PRD REQ-ORG-002 in `docs/dartwing_core/dartwing_core_prd.md:386`).
- **Minor doc drift:** The code sample in `docs/dartwing_core/dartwing_core_arch.md` under “Concrete Type Base Mixin” still shows `frappe.db.set_value(...)` for `update_org_name()`; the implementation is now safer (permission-checked). This mismatch can mislead future contributors.
  - **Action:** Update the doc snippet to match the current secure implementation (use `get_doc()` + `check_permission("write")` + `save()`).

---

# 2. Preemptive GitHub Copilot Issue Scan (Severity: HIGH/MEDIUM)

## Items Copilot would likely flag (and current status)

1. **Permission/validation bypass risks**
   - **Status:** ✅ Cleared. `update_org_name()` uses `check_permission("write")` and `save()` (`dartwing/dartwing_core/mixins/organization_mixin.py:114`).

2. **Missing type hints / unclear return types**
   - **Status:** ✅ Cleared for the mixin (`dartwing/dartwing_core/mixins/organization_mixin.py:9` and property annotations).

3. **Long lines / style violations in tests**
   - **Status:** ✅ Cleared. I normalized long lines in `dartwing/tests/unit/test_organization_mixin.py` to avoid common E501 flags.

4. **Potential confusion from doc mismatch**
   - **Status:** ⚠️ Still present. `docs/dartwing_core/dartwing_core_arch.md` still documents the insecure `set_value` approach for `update_org_name()` (doc-only, but high risk for copy/paste).
   - **Fix suggestion:** Update the snippet in `docs/dartwing_core/dartwing_core_arch.md` “Concrete Type Base Mixin” to mirror `OrganizationMixin.update_org_name()`’s current implementation.

5. **Docstring/API drift**
   - **Status:** ⚠️ Minor. `dartwing/dartwing_company/doctype/company/company.py:12` docstring lists only properties; it should include `get_organization_doc()` / `update_org_name()` for consistency with Family/Association/Nonprofit docstrings.
   - **Fix suggestion:** Update the docstring (no functional change).

---

# 3. Final Cleanliness & Idiomatic Frappe Check (Severity: MEDIUM)

- **Architecture alignment (Hybrid model permissions):** ✅ Family JSON now includes `user_permission_dependant_doctype` and includes “Dartwing User” permissions, consistent with `docs/dartwing_core/dartwing_core_arch.md:1262`.
- **Low-code / metadata-as-data:** Mostly good. One remaining “low-code polish” item is that multiple controllers set `status = "Active"` in Python (`dartwing/dartwing_core/doctype/family/family.py:25`, `dartwing/dartwing_core/doctype/association/association.py:25`, `dartwing/dartwing_core/doctype/nonprofit/nonprofit.py:25`). If the DocType JSON already defines defaults, prefer defaults in JSON over controller code (to keep behavior in metadata).
- **ORM usage:** ✅ All data access remains via Frappe APIs; no raw SQL introduced in production code paths.

---

# 4. Final Summary & Sign-Off (Severity: LOW)

The fix plan items (P1 and P2 from `specs/008-organization-mixin/review/FIX_PLAN.md`) verify as successfully implemented in the current codebase: permission enforcement for Organization writes is correct, hooks configuration no longer silently overwrites Company permission handlers, negative ownership validation is enforced, tests are moved into the discoverable test tree, and repo hygiene is improved via `.gitignore` and removal of bytecode artifacts. The only remaining meaningful risk is documentation drift in `docs/dartwing_core/dartwing_core_arch.md` still showing an insecure `set_value` pattern for `update_org_name()`, which should be corrected to prevent regressions via copy/paste.

FINAL VERIFICATION SIGN-OFF: This branch is ready for final QA and merging.

