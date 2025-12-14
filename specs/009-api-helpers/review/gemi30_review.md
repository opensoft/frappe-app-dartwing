# Code Review: 009-api-helpers

**Reviewer:** gemi30
**Module:** dartwing_core
**Date:** 2025-12-14

## Context

- **Feature:** Feature 9: API Helpers (Whitelisted Methods)
- **Purpose:** Implement standardized, whitelisted API endpoints (`get_user_organizations`, `get_org_members`, `get_concrete_doc`) to support Flutter and external clients, ensuring proper permission enforcement and data formatting.

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### [Security/Design] Bypass of Permission System via Raw SQL

**File:** `dartwing/dartwing_core/api/organization_api.py`

**Issue:** Both `get_user_organizations` (lines 60-84) and `get_org_members` (lines 158-183) use raw `frappe.db.sql` queries. While `get_org_members` checks for `Organization` read permission, the raw SQL query bypasses any potential row-level permissions defined on `Org Member` or `Role Template`, and misses standard Frappe formatter features. It also manually constructs joins which Frappe's ORM handles natively.

**Fix Suggestion:** Replace raw SQL with `frappe.get_list` or `frappe.get_all`. This ensures the core permission engine runs (if configured) and simplifies the code significantly.

**Recommended Rewrite for `get_org_members`:**

```python
def get_org_members(organization: str, limit: int = 20, offset: int = 0, status: Optional[str] = None) -> dict:
    # ... validation logic ...

    filters = {"organization": organization}
    if status:
        filters["status"] = status

    # Use ORM with dot-notation for joins
    members = frappe.get_list(
        "Org Member",
        filters=filters,
        fields=[
            "name", "person", "member_name", "organization", "role",
            "status", "start_date", "end_date",
            "person.primary_email as person_email",  # Join Person
            "role.is_supervisor"                     # Join Role Template
        ],
        order_by="start_date desc",
        limit_page_length=limit,
        start=offset
    )

    # ... rest of logic ...
```

**Why this is blocking:** Security best practices in Frappe dictate using the ORM whenever possible to avoid accidental permission bypasses and SQL injection risks (though your current SQL parameterization is safe from injection).

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### [Maintainability] Use `frappe.get_list` for Organization Query

**File:** `dartwing/dartwing_core/api/organization_api.py`

**Issue:** `get_user_organizations` also uses complex SQL to join `Organization` and `Role Template`.

**Suggestion:** Refactor to use `frappe.get_list` on `Org Member` with fetched fields from parent.

```python
memberships = frappe.get_list(
    "Org Member",
    filters={"person": person},
    fields=[
        "organization", "role", "status",
        "organization.org_name", "organization.org_type", "organization.logo",
        "organization.linked_doctype", "organization.linked_name",
        "role.is_supervisor"
    ]
)
```

This reduces 25 lines of SQL string to ~5 lines of Python and is more readable.

### [Performance] Optimize `validate_links`

**File:** `dartwing/dartwing_core/doctype/organization/organization.py`

**Issue:** `validate_links` calls `frappe.db.exists` (line 199) and then `frappe.get_doc` (line 207). `get_doc` implies `exists`.

**Suggestion:** Just try to `get_doc` and catch `DoesNotExistError`. This saves one database query.

### [Code Quality] Use Constants for Field Names

**File:** `dartwing/dartwing_core/doctype/organization/organization.py`

**Suggestion:** The keys in `ORG_FIELD_MAP` (e.g., "family_name") are string literals. Consider defining these as constants at the top of the file or on the concrete classes to avoid typo-induced bugs.

---

## 3. General Feedback & Summary (Severity: LOW)

**Summary:**
The code is well-structured, follows the project's architectural guidelines, and includes comprehensive tests. The use of a thread-safe validation cache for `ORG_FIELD_MAP` is a nice meaningful optimization. The `Audit Trail` logging implementation is consistent and thorough. The primary area for improvement is shifting from raw SQL to Frappe's ORM (`get_list`) to better align with the "Low Code" philosophy and ensure robust security inheritance.

**Positives:**

- Excellent docstrings and strict typing.
- Good use of `@frappe.whitelist` and `logging`.
- Comprehensive test suite covering edge cases (pagination, permissions, null links).

**Future Technical Debt:**

- Consider adding a `get_permission_query_conditions` hook for `Org Member` to strictly enforce that users can only fetch members for orgs they belong to at the database level, reinforcing the application-level check.
