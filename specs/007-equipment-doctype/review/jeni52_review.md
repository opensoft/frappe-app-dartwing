# Code Review — `007-equipment-doctype` (Equipment DocType)

## Scope & Context Used

- **Branch goal (per priority list):** Implement **Feature 7: Equipment DocType** — organization-scoped asset management with assignment, location, documents, and maintenance schedule, filtered by Organization permissions. See `docs/dartwing_core/wip/dartwing_core_features_priority.md`.
- **Architecture alignment:** `docs/dartwing_core/dartwing_core_arch.md` (notably section **3.11–3.14**) and `docs/dartwing_core/dartwing_core_prd.md` (Tasks domain + “equipment maintenance integration”).
- **Spec alignment:** `specs/007-equipment-doctype/spec.md` and `specs/007-equipment-doctype/data-model.md`.
- **Process note:** `007-equipment-doctype` is currently **not ahead of `main` by commits** (`git diff main...HEAD` is empty). The changes appear to be **working tree/untracked additions** plus edits to `dartwing/hooks.py` and `CLAUDE.md`. This review covers the *feature implementation as present in the workspace*.

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 Broken SQL in `get_permission_query_conditions()` (will break list queries + permission filtering)

- **Where:** `dartwing/permissions/equipment.py:45-47`
- **Problem:** `frappe.db.escape()` already returns a quoted string (e.g. `'ORG-0001'`). Wrapping it again produces `''ORG-0001''`, which leads to invalid SQL and/or unexpected behavior.
- **Why this blocks merge:** Permission query conditions are executed for list view queries and API list calls; if they error, **Equipment becomes unusable** (and may impact any route that touches `Equipment`).
- **Concrete fix suggestion (match existing patterns like `dartwing/permissions/company.py`):**
  - Replace the IN clause construction with:
    - `org_list = ", ".join(frappe.db.escape(org) for org in orgs)`
    - `return f"\`tabEquipment\`.\`owner_organization\` IN ({org_list})"`
  - Add an Administrator bypass (consistent with other permission modules), e.g.:
    - `if user == "Administrator": return ""`

### 1.2 Authorization gap in `get_org_members()` (potential cross-tenant data leak)

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:119-152`
- **Problem:** This is a whitelisted method used by Desk to populate the `assigned_to` link query, but it **does not verify** that the caller has access to the requested `organization`. A malicious caller can call:
  - `/api/method/dartwing.dartwing_core.doctype.equipment.equipment.get_org_members?organization=<other_org>`
  and potentially enumerate `Person` records belonging to organizations they shouldn’t see.
- **Why this blocks merge:** This violates org isolation expectations (Constitution “Security & Compliance” + spec FR-003/FR-009). It’s a direct tenant data exposure risk.
- **Concrete fix suggestion:**
  - Before running the SQL, enforce that the current user has Organization access:
    - If `user == "Administrator"` or `"System Manager" in roles`: allow.
    - Else require a `User Permission` row for `{user, allow="Organization", for_value=organization}` (or equivalent `frappe.has_permission("Organization", "read", organization)` if you standardize on it).
  - On failure, raise a permission error (`frappe.throw(_("Not permitted"), frappe.PermissionError)`).

### 1.3 FR-013 not fully implemented: deactivation is not blocked (only deletion is blocked)

- **Where:** `dartwing/hooks.py:180-187` and `dartwing/dartwing_core/doctype/equipment/equipment.py:231-253`
- **Problem:** `check_equipment_assignments_on_member_removal()` states it applies to “deleted or deactivated”, but it’s only registered on **`on_trash`** for `Org Member`. Spec FR-013 requires blocking **deactivation** *as well as* removal.
- **Why this blocks merge:** This is a spec compliance gap: an Org Member can be made inactive while still assigned equipment, leaving inconsistent data states and undermining enforcement.
- **Concrete fix suggestion (two viable patterns):**
  1. **Hook approach:** Register an additional `on_update` handler for `Org Member` that checks when `status` changes away from Active, and blocks if assigned equipment exists.
  2. **Model approach (preferred for correctness):** Put the enforcement in `Org Member`’s controller (`validate()` / `on_trash`) so it applies regardless of how updates happen (Desk/API/background jobs), and keep the query helper in an equipment utility module.

### 1.4 Hook ordering risk on `Org Member.on_trash` (side effects before validation)

- **Where:** `dartwing/hooks.py:182-185`
- **Problem:** `remove_user_permissions` runs *before* the equipment assignment check. If the equipment check throws, you rely on transaction rollback to restore removed permissions.
- **Why this blocks merge:** In Frappe, deletes can include multiple operations and commits may occur in helper code; relying on implicit rollback for cross-module side effects is fragile.
- **Concrete fix suggestion:**
  - Reorder the `on_trash` list to run the equipment check **first**, then remove user permissions:
    - `check_equipment_assignments_on_member_removal`
    - `remove_user_permissions`

### 1.5 Create-path authorization is too weak: “has any org permission” ≠ “can create equipment for this org”

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:93-117`
- **Problem:** `validate_user_has_organization()` only ensures the user has *some* Organization User Permission, but does not ensure they can create Equipment for the selected `owner_organization`.
- **Why this blocks merge:** Even if standard permission hooks usually catch this, this validation reads as the enforcement mechanism for FR-001/FR-003 create behavior; right now it can pass for a user who has org access to A but creates equipment for B.
- **Concrete fix suggestion:**
  - Replace this validation with `validate_user_can_access_owner_organization()`:
    - Require `owner_organization` set.
    - Check `User Permission` exists for `(user, allow="Organization", for_value=self.owner_organization)` for non-admin users.
  - If you want to keep the “must belong to at least one org” rule, enforce it as a *secondary* check only when `owner_organization` is empty (but `owner_organization` is already `reqd` in the DocType).

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 Align permission module style with existing patterns

- **Where:** `dartwing/permissions/equipment.py`
- Recommend matching `dartwing/permissions/company.py` conventions for:
  - Optional `user: str | None = None` argument + defaulting to session user.
  - Administrator bypass (your other permission modules already treat Administrator specially).
  - Avoiding SQL string pitfalls; consider using `frappe.qb` when possible for composability.

### 2.2 Consider moving “API helpers” out of DocType module

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:155-209`
- `get_equipment_by_organization()` / `get_equipment_by_person()` are API-style endpoints. Per repo guidelines (see `AGENTS.md`), whitelisted endpoints typically live under `dartwing/api/…` and DocType controllers focus on validations and document rules.
- Suggested pattern:
  - Keep only `Document` class + document lifecycle enforcement in the controller.
  - Move list/query API helpers into `dartwing/api/equipment.py` (or an equivalent core API module) and reuse the same permission model.

### 2.3 Reduce redundancy: rely on DocType metadata where it already enforces rules

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:29-60` and `dartwing/dartwing_core/doctype/equipment/equipment.json`
- `equipment_name` is already `reqd: 1` in `equipment.json`, and `serial_number` is already `unique: 1`.
- If you keep server-side checks for better UX, consider standardizing them:
  - For uniqueness: catch `frappe.UniqueValidationError` / `DuplicateEntryError` and present a user-friendly message rather than pre-querying.
  - For required fields: let Frappe’s required-field handling drive UX unless you need custom messaging/logic.

### 2.4 Prefer query builder / ORM patterns for maintainability

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.py:140-152`
- The SQL is parameterized (good), but long-term maintainability improves if you use:
  - `frappe.qb` (query builder) for joins and conditions, and/or
  - `frappe.get_list` where feasible.
- If you keep SQL, add minimal hardening:
  - Normalize empty `filters` (handle `filters is None`).
  - Consider `IFNULL(p.last_name, '') LIKE %s` so last-name search behaves consistently.

### 2.5 Performance guardrails: indexing + pagination patterns

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.json` and list APIs
- For SC-002 (“1000 items in 2s”) and long-term scaling:
  - Ensure DB indexes on common predicates: `owner_organization`, `assigned_to`, `status`, `equipment_type` (consider `search_index: 1` for Link/Select fields you filter on).
  - Ensure list endpoints always paginate (Frappe REST does; your custom methods should also document `limit_start/limit_page_length` if used externally).

### 2.6 Minor Desk script resilience

- **Where:** `dartwing/dartwing_core/doctype/equipment/equipment.js:10-17`
- Clearing `assigned_to` based on `__onload.owner_organization` can behave unexpectedly on new docs or after multiple org changes.
- Consider tracking prior org in a local variable on `frm` (e.g., `frm._last_owner_org`) or using `frm.doc.owner_organization` change detection directly, so the behavior is deterministic.

---

## 3. General Feedback & Summary (Severity: LOW)

The feature implementation is directionally solid: the DocType schema matches the spec and architecture (organization-scoped ownership, assignment to Person via Org Member validation, child tables for documents and maintenance, and hooks for deletion safety). The strongest parts are the explicit spec-driven validations and the attempt to integrate with the existing Organization User Permission model. Before merge, address the permission query SQL bug and the missing authorization check in `get_org_members()`—those are high-risk and will either break core functionality or violate tenant isolation. After that, tightening FR-013 deactivation enforcement and aligning API placement/style with existing repo conventions will make the feature more robust and easier to maintain. Future technical debt worth scheduling: add minimal automated tests for permission filtering and assignment/deactivation edge cases (even if the initial spec didn’t request them, the project constitution does).

