# Code Review — `009-api-helpers` (Dartwing Core: API Helpers)

**Nickname**: `GPT52`  
**Branch**: `009-api-helpers`  
**Module**: `dartwing_core`  

## Context I Used (per constitution)

- `bench/apps/dartwing/docs/dartwing_core/dartwing_core_arch.md`
- `bench/apps/dartwing/docs/dartwing_core/dartwing_core_prd.md` (notably API endpoints in the Organization section)
- `bench/apps/dartwing/docs/dartwing_core/wip/dartwing_core_features_priority.md` → **Feature 9: API Helpers (Whitelisted Methods)**
- `bench/apps/dartwing/.specify/memory/constitution.md`
- `bench/apps/dartwing/specs/009-api-helpers/spec.md` + `bench/apps/dartwing/specs/009-api-helpers/contracts/organization-api.yaml`

## Scope Note (important)

`git log main..HEAD` is empty at the time of review, meaning **there are no committed commits on this branch** yet. The review below is based on the **working tree diff + untracked files** currently present on `009-api-helpers`:

- Modified: `dartwing/hooks.py`, `dartwing/dartwing_core/doctype/organization/organization.py`, `CLAUDE.md`
- New: `dartwing/dartwing_core/api/organization_api.py`, `dartwing/dartwing_core/api/__init__.py`, `dartwing/tests/test_organization_api.py`, `specs/009-api-helpers/*`

---

### 1. Critical Issues & Blockers (Severity: HIGH)

1) **Test suite likely fails due to invalid `frappe.get_doc()` usage**

- **Where**: `dartwing/tests/test_organization_api.py:65`, `dartwing/tests/test_organization_api.py:80`, `dartwing/tests/test_organization_api.py:93`, `dartwing/tests/test_organization_api.py:106`, `dartwing/tests/test_organization_api.py:120`
- **What/Why**: The test uses `frappe.get_doc("Person", {"frappe_user": ...})` / `frappe.get_doc("Organization", {"org_name": ...})`. In Frappe, `get_doc(doctype, name)` expects a **document name**, not a filter dict (filters go through `frappe.db.get_value` / `frappe.get_all`).
- **Impact**: This will crash test setup before any API assertions run, making the branch unmergeable under the project’s “tests required for business logic” standard.
- **Concrete fix** (pattern to apply for each case):
  - Replace:
    - `cls.test_person = frappe.get_doc("Person", {"frappe_user": "apitest@example.com"})`
  - With:
    - `person_name = frappe.db.get_value("Person", {"frappe_user": "apitest@example.com"}, "name")`
    - `cls.test_person = frappe.get_doc("Person", person_name)`
  - Do the same for `Organization` lookups:
    - `org_name = frappe.db.get_value("Organization", {"org_name": "API Test Company"}, "name")`
    - `cls.test_company_org = frappe.get_doc("Organization", org_name)`

2) **Authorization model mismatch can yield inconsistent UI behavior (“I can see it, but can’t open it”)**

- **Where**:
  - Listing: `dartwing/dartwing_core/api/organization_api.py:49-107` (derives organizations via `Person → Org Member`)
  - Detail access: `dartwing/dartwing_core/doctype/organization/organization.py:430-478` (gates access via `frappe.has_permission("Organization", "read", org_name)`)
  - Related existing API: `dartwing/permissions/api.py:58-116` already exposes a `get_user_organizations()` that is based on **User Permission**, i.e., the same primitive `frappe.has_permission` relies on.
- **What/Why**:
  - Your list endpoint derives orgs from `Org Member`, but your detail endpoints derive access from **Frappe permissions** (likely `User Permission` propagation).
  - If User Permission propagation is delayed/broken (or membership is `Pending`/`Inactive`), a user can receive an organization in the list (because they have an `Org Member` row) but be blocked from details (because `has_permission` denies it).
- **Impact**: Flutter will render an org selector that includes orgs the user can’t actually access. This creates a correctness issue and a poor UX; it also makes incident debugging harder because “membership data” and “permission data” diverge.
- **Concrete fix options** (pick one and apply consistently across all four methods):
  - **Option A (recommended)**: Make `get_user_organizations()` list orgs using the same auth primitive as the rest of the API:
    - Base the org list on `User Permission` (or `frappe.get_list` with permissions) and *optionally* enrich with membership info by joining `Org Member` **only for those permitted orgs**.
  - **Option B**: If Org Member is the true authorization source, then stop using `frappe.has_permission("Organization", ...)` and instead:
    - Validate that the session user’s `Person` has an `Org Member` row for the org (and enforce the correct membership statuses), then proceed.
  - **Option C**: Explicitly define “visibility” vs “access”:
    - Return orgs in the list but include an `has_access` boolean based on `frappe.has_permission`, and have the client block navigation. This is workable, but typically inferior to making server-side authorization consistent.

3) **`get_org_members` returns potentially sensitive data gated only by Organization read permission**

- **Where**: `dartwing/dartwing_core/api/organization_api.py:141-212`
- **What/Why**:
  - The method returns `person_email` (`dartwing/dartwing_core/api/organization_api.py:169-170`, `dartwing/dartwing_core/api/organization_api.py:204-205`).
  - The only gate is `frappe.has_permission("Organization", "read", organization)` (`dartwing/dartwing_core/api/organization_api.py:142-145`).
  - In many RBAC models, “can view org” ≠ “can view all member emails”.
- **Impact**: Potential privacy leakage (email enumeration) to users who are regular members but not org admins, depending on how your `Organization` permission rules are configured.
- **Concrete fix**:
  - Introduce a stronger authorization check for member listing (and especially for returning emails), e.g.:
    - Require a privileged role (System Manager / Organization Admin) **or**
    - Require that the requester’s own Org Member role has `Role Template.is_supervisor = 1` for that org **or**
    - Split response fields: always return `member_name` and role/status, but only include `person_email` when privileged.
  - If you already have an “org admin” concept in Role Template or future “Org Member permissions”, enforce it here.

4) **Error semantics don’t reliably match the spec contract (401 vs 403 vs 404)**

- **Where**:
  - `dartwing/dartwing_core/api/organization_api.py:141-145` (Guest request becomes `PermissionError`, not `AuthenticationError`)
  - `dartwing/dartwing_core/doctype/organization/organization.py:430-434` and `dartwing/dartwing_core/doctype/organization/organization.py:475-478` (permission check occurs before retrieving the document)
- **What/Why**:
  - Your `specs/009-api-helpers/data-model.md` defines explicit error shapes for auth/permission/not-found.
  - `get_org_members` currently doesn’t explicitly check for `Guest` and therefore produces `PermissionError` for unauthenticated requests.
  - For the org detail helpers, the `has_permission` check is executed before `frappe.get_doc`. Depending on `has_permission` behavior, a non-existent org can incorrectly raise a permission error instead of a 404-equivalent `DoesNotExistError`.
- **Impact**: Client-side error handling becomes unreliable; contracts drift from reality; integration tests may become flaky.
- **Concrete fix** (idiomatic Frappe):
  - For org detail methods, prefer:
    - `org = frappe.get_doc("Organization", organization)` (raises `DoesNotExistError` naturally)
    - `org.check_permission("read")` (raises `PermissionError` naturally)
  - For session requirements, explicitly gate:
    - `if frappe.session.user == "Guest": frappe.throw(_("Authentication required"), frappe.AuthenticationError)`

5) **Parameter validation gaps can produce runtime exceptions or contract violations**

- **Where**: `dartwing/dartwing_core/api/organization_api.py:148-156`
- **What/Why**:
  - `limit = min(int(limit), 100)` permits `limit <= 0` (contract says min 1) and can raise `ValueError` for non-int inputs.
  - `status` is not validated to `Active/Inactive/Pending` (contract enumerates values).
  - `organization` is not validated for empty/None.
- **Impact**: Unhandled exceptions → 500s, inconsistent behavior, contract mismatch.
- **Concrete fix**:
  - Validate required args early with `frappe.ValidationError`.
  - Clamp `limit` to `[1, 100]` and validate `offset >= 0`.
  - Validate `status in {"Active","Inactive","Pending"}` if provided.

---

### 2. Suggestions for Improvement (Severity: MEDIUM)

1) **Avoid raw SQL when possible; prefer Frappe ORM / Query Builder to align with “low-code” and reduce permission footguns**

- **Where**: `dartwing/dartwing_core/api/organization_api.py:60-84` and `dartwing/dartwing_core/api/organization_api.py:158-183`
- **Why**: Raw SQL is fine when truly needed, but in Frappe it increases maintenance cost and makes it easier to bypass permission query conditions or drift from DocType metadata changes (field renames, etc.).
- **Concrete alternative**:
  - Use `frappe.qb` joins (recommended for joins) or `frappe.get_all` + batch fetch (acceptable if query count is controlled).
  - If you keep SQL, ensure you:
    - Alias columns to avoid ambiguous keys (e.g., alias `org.status AS org_status`)
    - Keep the “permission model” documented in code via clear guard conditions (not via comments, but via explicit checks).

2) **Align API module placement with repository conventions (or document the exception explicitly)**

- **Where**: new module `dartwing/dartwing_core/api/organization_api.py`
- **Observation**: `bench/apps/dartwing/AGENTS.md` recommends whitelisted APIs under `dartwing/api/<module>.py` (e.g., `dartwing/api/person.py` already follows this).
- **Suggestion**:
  - Either move org APIs under `dartwing/api/organization.py` (and keep `dartwing_core` doc helpers where they are), or
  - Explicitly standardize that “core-module APIs live under `dartwing/dartwing_core/api/`” and update AGENTS/conventions accordingly to avoid future fragmentation.

3) **Reduce drift/duplication with existing permission API endpoints**

- **Where**:
  - Existing: `dartwing/permissions/api.py:get_user_organizations` and `dartwing/permissions/api.py:get_organization_members`
  - New: `dartwing/dartwing_core/api/organization_api.py:get_user_organizations` and `dartwing/dartwing_core/api/organization_api.py:get_org_members`
- **Suggestion**:
  - If the new endpoints supersede the old ones, consider a deprecation plan (keep old endpoints but forward internally, or mark for removal in a later branch).
  - At minimum, ensure the two `get_user_organizations` variants don’t diverge in semantics (admin behavior, org filtering, response format) without an intentional “v1 vs v2” story.

4) **Logging consistency**

- **Where**:
  - `dartwing/dartwing_core/api/organization_api.py:103-105`, `dartwing/dartwing_core/api/organization_api.py:208-211`
  - `dartwing/dartwing_core/doctype/organization/organization.py:428-490`
- **Suggestion**:
  - Include the `user` in the INFO audit lines (you already have org + counts).
  - Standardize logger namespaces so searching logs for a single endpoint is straightforward (e.g., `dartwing.api.organization` vs `dartwing_core.api`).

5) **Minor cleanup to reduce noise**

- **Where**: `dartwing/dartwing_core/api/organization_api.py:152-156` (`filters` is built but unused)
- **Suggestion**: Remove unused local variables and remove SELECT columns you don’t return (e.g., `om.start_date`, `om.end_date` in `get_user_organizations`).

---

### 3. General Feedback & Summary (Severity: LOW)

The branch is directionally aligned with **Feature 9: API Helpers**: you’ve implemented the expected endpoints, enforced permissions on the Organization detail helpers, and added a dedicated test module plus an OpenAPI contract that matches the method paths. The main work left before merge is tightening correctness around test setup, making authorization semantics consistent across list vs detail endpoints, and hardening `get_org_members` (privacy gating + parameter validation + correct error types). The cleanup in `dartwing/hooks.py` is a solid fix (it resolves a syntax-breaking issue in `doc_events`). After addressing the blockers, I’d recommend adding at least one non-Administrator happy-path test that exercises the real-world permission flow (Org Member → User Permission → `has_permission`) so the Flutter integration doesn’t rely on Administrator-only behavior.

