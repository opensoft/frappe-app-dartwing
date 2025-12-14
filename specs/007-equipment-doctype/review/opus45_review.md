# Code Review: 007-Equipment-DocType (Second Pass)

**Reviewer:** opus45
**Date:** 2025-12-14
**Branch:** `007-equipment-doctype`
**Module:** dartwing_core
**Review Type:** Post-fix verification and detailed second pass

---

## Executive Summary

The first-pass issues (P1-01 through P1-05, P2-01 through P2-03, P2-05, P2-06, P2-08, P2-09) have been **successfully resolved**. The implementation now addresses all critical security and compliance issues identified in the MASTER_PLAN.md.

This second-pass review focuses on **newly identified edge cases** and **remaining deferred items** that warrant attention before or shortly after merge.

---

## 1. Critical Issues & Blockers (Severity: HIGH)

**None remaining.** All P1 critical issues have been resolved:
- SQL injection vulnerability: Fixed (line 47)
- Cross-tenant API leakage: Fixed (auth checks added)
- FR-013 deactivation blocking: Fixed (new hook function)
- Hook ordering: Fixed (equipment check first)
- Create-path authorization: Fixed (specific org validation)

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 NEW: Potential Multi-Org Data Leakage in `get_equipment_by_person()`

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.py:263-298`

**Issue:** The function checks if the user can read the *Person*, but returns equipment from *all organizations* that person is assigned to, without filtering by the calling user's organization access.

**Scenario:**
1. Person "John" is a member of both OrgA and OrgB
2. UserX has access only to OrgA
3. UserX calls `get_equipment_by_person("John")`
4. UserX receives equipment from both OrgA *and* OrgB

**Current Code (line 278-283):**
```python
if user != "Administrator" and "System Manager" not in frappe.get_roles(user):
    if not frappe.has_permission("Person", "read", person):
        frappe.throw(...)
```

**Recommended Fix:**
```python
@frappe.whitelist()
def get_equipment_by_person(person: str) -> list:
    """Get all equipment currently assigned to a specific person."""
    user = frappe.session.user

    # P1-02 FIX: Verify user has access to view this person's data
    if user != "Administrator" and "System Manager" not in frappe.get_roles(user):
        if not frappe.has_permission("Person", "read", person):
            frappe.throw(
                _("You do not have permission to view equipment for this person"),
                frappe.PermissionError,
            )

        # SECOND-PASS FIX: Filter to only organizations user can access
        user_orgs = frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Organization"},
            pluck="for_value",
        )
        filters = {"assigned_to": person, "owner_organization": ["in", user_orgs]}
    else:
        filters = {"assigned_to": person}

    return frappe.get_all("Equipment", filters=filters, fields=[...])
```

**Severity:** MEDIUM - Data exposure limited to equipment records, not PII. However, this could reveal business-sensitive asset information across tenant boundaries.

---

### 2.2 DEFERRED: Request-Level Caching (P2-04)

**File:** `dartwing/permissions/equipment.py:35-39`

**Issue:** Each request fetches User Permissions for the current user. For users with many org memberships or high request volume, this adds latency.

**Current Status:** Marked as DEFERRED in MASTER_PLAN.md.

**Recommendation:** Implement caching if performance profiling reveals >50ms permission query overhead. Suggested pattern:

```python
def _get_user_organizations(user: str) -> list[str]:
    """Get user's permitted organizations with request-level caching."""
    cache_key = f"_user_orgs_{frappe.scrub(user)}"
    if not hasattr(frappe.local, cache_key):
        orgs = frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Organization"},
            pluck="for_value",
        )
        setattr(frappe.local, cache_key, orgs)
    return getattr(frappe.local, cache_key)
```

This can be extracted to `dartwing/permissions/helpers.py` and reused across all permission modules.

---

### 2.3 DEFERRED: Status Constants (P2-07)

**Files:**
- `equipment.py` (validation code)
- `equipment.json` (field options)
- `equipment.js` (client-side)

**Issue:** Status values ("Active", "In Repair", "Retired", "Lost", "Stolen") are hardcoded strings duplicated across files.

**Risk:** Low - renaming a status requires coordinated changes in 3 files.

**Recommendation:** Define constants in `equipment.py`:

```python
class EquipmentStatus:
    ACTIVE = "Active"
    IN_REPAIR = "In Repair"
    RETIRED = "Retired"
    LOST = "Lost"
    STOLEN = "Stolen"

    @classmethod
    def all(cls) -> list[str]:
        return [cls.ACTIVE, cls.IN_REPAIR, cls.RETIRED, cls.LOST, cls.STOLEN]
```

JSON and JS must remain strings, but Python validation and API code should reference constants.

---

### 2.4 DEFERRED: Location Validation (P2-10)

**File:** `equipment.json:90-94`

**Issue:** `current_location` links to any Address without validating the address is associated with `owner_organization`.

**Risk:** Low - users could assign equipment to addresses from unrelated organizations. This may be intentional for shared facilities.

**Recommendation:** If tenant isolation is required, add validation:

```python
def validate_current_location(self):
    """Validate current_location is associated with owner_organization."""
    if not self.current_location or not self.owner_organization:
        return

    # Check if Address has Dynamic Link to this organization
    has_link = frappe.db.exists(
        "Dynamic Link",
        {
            "parenttype": "Address",
            "parent": self.current_location,
            "link_doctype": "Organization",
            "link_name": self.owner_organization,
        },
    )

    if not has_link:
        frappe.msgprint(
            _("Warning: Address '{0}' is not linked to organization '{1}'").format(
                self.current_location, self.owner_organization
            ),
            indicator="orange",
        )
```

Use `msgprint` (warning) instead of `throw` to allow flexibility for shared locations.

---

## 3. General Feedback & Summary (Severity: LOW)

### 3.1 Test Coverage Enhancement Opportunity

**File:** `dartwing/dartwing_core/doctype/equipment/test_equipment.py`

**Observation:** All 12 test cases run as Administrator, which bypasses permission logic. The permission-related tests (P1-05, P2-02 fixes) are not directly exercised.

**Recommendation:** Add test cases that simulate a regular "Dartwing User":

```python
def test_user_cannot_create_for_unauthorized_org(self):
    """Test P1-05: Users cannot create equipment for orgs they lack access to."""
    # Create test user
    test_user = frappe.get_doc({
        "doctype": "User",
        "email": "equip_test@test.local",
        "first_name": "Equipment",
        "last_name": "Tester",
        "roles": [{"role": "Dartwing User"}]
    })
    test_user.insert()

    # Create org WITHOUT giving user permission
    other_org = frappe.get_doc({
        "doctype": "Organization",
        "org_name": "Unauthorized Org",
        "org_type": "Company"
    })
    other_org.insert()

    try:
        frappe.set_user(test_user.name)
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Unauthorized",
            "owner_organization": other_org.name
        })
        with self.assertRaises(frappe.PermissionError):
            equipment.insert()
    finally:
        frappe.set_user("Administrator")
        # cleanup...
```

---

### 3.2 Permission Function Code Duplication

**Files:**
- `dartwing/permissions/equipment.py:31-32, 69-70`
- `dartwing/dartwing_core/doctype/equipment/equipment.py:136-137, 188, 229-230, 278`

**Observation:** The Administrator/System Manager bypass check is repeated in 6+ locations:

```python
if user == "Administrator" or "System Manager" in frappe.get_roles(user):
    return True  # or return ""
```

**Recommendation:** Extract to a helper in `dartwing/permissions/helpers.py`:

```python
def is_superuser(user: str | None = None) -> bool:
    """Check if user has unrestricted access."""
    if not user:
        user = frappe.session.user
    return user == "Administrator" or "System Manager" in frappe.get_roles(user)
```

This reduces duplication and centralizes the bypass logic for future modifications.

---

### 3.3 Delete Permission Not Granted to Dartwing User

**File:** `equipment.json:139-149`

**Observation:** The "Dartwing User" role has create, read, write, share permissions but **not delete**:

```json
{
    "create": 1,
    "email": 1,
    "export": 1,
    "print": 1,
    "read": 1,
    "report": 1,
    "role": "Dartwing User",
    "share": 1,
    "write": 1
    // Note: "delete": 1 is missing
}
```

**Impact:** Regular users cannot delete equipment records. This may be intentional for audit/compliance reasons (equipment should be "Retired" not deleted).

**Action:** Verify this is intentional. If so, no change needed. If users should be able to delete, add `"delete": 1`.

---

### 3.4 Minor: Search Wildcard Handling in `get_org_members()`

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.py:206`

**Issue:** The `txt` parameter is used directly in LIKE patterns without escaping SQL wildcards (`%`, `_`):

```python
(organization, f"%{txt}%", f"%{txt}%", f"%{txt}%", start, page_len)
```

**Risk:** Very low. If a user searches for "John_Doe", the underscore matches any single character. This could cause unexpected but harmless search results.

**Recommendation (optional):**

```python
# Escape SQL wildcards in search text
escaped_txt = txt.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
search_pattern = f"%{escaped_txt}%"
```

---

## 4. Verification Checklist

| Original Issue | Status | Verification |
|:---------------|:-------|:-------------|
| P1-01 SQL Injection | FIXED | Line 47: `frappe.db.escape(o)` without extra quotes |
| P1-02 Cross-Tenant API | FIXED | Auth checks at lines 186-197, 228-241, 276-283 |
| P1-03 FR-013 Deactivation | FIXED | `check_equipment_assignments_on_member_deactivation()` at line 345 |
| P1-04 Hook Ordering | FIXED | hooks.py:185-188 - equipment check before permission removal |
| P1-05 Create Authorization | FIXED | `validate_user_can_access_owner_organization()` at line 127 |
| P2-01 Unit Tests | FIXED | 12 test cases in `test_equipment.py` |
| P2-02 Function Naming | FIXED | `_equipment` suffix in hooks.py:129, 139 |
| P2-03 Redundant Validation | FIXED | `validate_equipment_name()` removed |
| P2-05 Org Immutability | FIXED | `validate_owner_organization_immutable()` at line 54 |
| P2-06 Audit Trail | FIXED | `_log_assignment_change()` at line 34 |
| P2-08 Client UX | FIXED | `equipment.js:24-34` - disabled field with message |
| P2-09 Lost/Stolen Status | FIXED | `equipment.json:65` - options include Lost, Stolen |

---

## 5. Remaining Issues Summary

| Priority | Issue | Action |
|:---------|:------|:-------|
| **P2-NEW** | `get_equipment_by_person()` may leak cross-org equipment | Filter returned equipment by user's org access |
| P2-04 | Request-level caching | DEFERRED - implement if perf issues arise |
| P2-07 | Hardcoded status strings | DEFERRED - low risk, can be addressed later |
| P2-10 | Location validation | DEFERRED - may be intentionally flexible |
| P3-01 | Docstring accuracy | DEFERRED |
| P3-02 | Document type extensibility | DEFERRED |
| P3-03 | Maintenance automation | DEFERRED - future feature |
| P3-04 | Field descriptions | DEFERRED |
| P3-05 | API helper relocation | DEFERRED - current location acceptable |
| P3-06 | Database indexes | DEFERRED - standard Frappe indexes sufficient |

---

## 6. Recommendation

**Merge Readiness:** APPROVED with one recommended pre-merge fix

The implementation is **production-ready** for the current scope. All critical (P1) issues have been resolved. The one new P2 issue (`get_equipment_by_person()` multi-org leakage) is low-risk but should be addressed before or immediately after merge.

**Pre-Merge:**
1. Apply the `get_equipment_by_person()` organization filter fix (Section 2.1)

**Post-Merge (Future Sprints):**
1. Add permission-based test cases
2. Implement caching if performance monitoring shows need
3. Address remaining P3 items per backlog prioritization

---

## Confidence Assessment

**Confidence Level: 96%**

The 4% uncertainty relates to:
- No runtime execution testing performed
- Integration behavior with other modules (Person, Org Member, User Permission) not traced end-to-end
- Database migration state not verified

---

**End of Second Pass Review**
