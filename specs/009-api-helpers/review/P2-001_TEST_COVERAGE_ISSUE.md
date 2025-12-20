# Add Comprehensive P2-001 Email Visibility Integration Tests

**Issue Type:** Enhancement
**Priority:** Medium
**Component:** Testing
**Labels:** `enhancement`, `testing`, `security`, `P2-001`, `integration-test`
**Estimated Effort:** 4-8 hours
**Branch:** Post-merge work for `009-api-helpers`

---

## Problem Statement

The P2-001 security requirement ("Supervisors can see member emails; non-supervisors can only see their own") is correctly implemented in code but lacks comprehensive automated test coverage.

**Current Test Coverage:** ✅ Administrator access only
**Missing Coverage:** ❌ Role-based supervisor access, non-supervisor restrictions, self-access

### Why This Matters

Email visibility is a **privacy/security requirement**. While the implementation has been verified through:
- ✅ Code review (confirmed correct)
- ✅ Manual testing (functionality works)
- ✅ Administrator test (validates API structure)

The **supervisor role-based access control logic is not covered by automated tests**. If this logic breaks in future refactoring, tests won't catch it.

---

## Current Implementation

**Files:**
- Implementation: `dartwing/dartwing_core/api/organization_api.py` lines 181-196, 250-253
- Current test: `dartwing/tests/test_organization_api.py` line 493 (`test_email_visibility_supervisor_only`)

**Current Test Limitation:**
```python
def test_email_visibility_supervisor_only(self):
    """Test that person_email is visible to Administrator."""
    # ...
    frappe.set_user("Administrator")  # ⚠️ Bypasses supervisor logic
    result = get_org_members(self.test_company_org.name)
    # Administrator always sees emails, so supervisor check isn't tested
```

**TODO Comment:** Lines 503-507 in `test_organization_api.py`

---

## Acceptance Criteria

### Must Have

- [ ] **Test 1: Supervisor sees all member emails**
  - User with supervisor role (`is_supervisor=1`) in organization
  - Calls `get_org_members()`
  - Assert: `person_email` field present for ALL members in response

- [ ] **Test 2: Non-supervisor sees only own email**
  - User with non-supervisor role (`is_supervisor=0`)
  - User has active membership in organization
  - Calls `get_org_members()`
  - Assert: `person_email` present ONLY for user's own record

- [ ] **Test 3: Non-supervisor cannot see other emails**
  - Same setup as Test 2
  - Assert: `person_email` field absent for other members' records

### Should Have

- [ ] **Test 4: Cache invalidation**
  - Verify supervisor status caching works correctly (60s TTL)
  - Test role change scenarios

- [ ] **Test 5: Edge cases**
  - User without Person record (edge case)
  - User with multiple roles in same org
  - Inactive member status

---

## Implementation Guidance

### Test Setup Complexity

This test requires **complete permission infrastructure**:

```python
# 1. Create Role Templates with correct flags
supervisor_role = frappe.get_doc({
    "doctype": "Role Template",
    "name": "Test Supervisor",
    "is_supervisor": 1,  # Critical flag
    "org_type": "Company"
})

non_supervisor_role = frappe.get_doc({
    "doctype": "Role Template",
    "name": "Test Employee",
    "is_supervisor": 0,  # Critical flag
    "org_type": "Company"
})

# 2. Create test users with Dartwing User role
test_user = frappe.get_doc({
    "doctype": "User",
    "email": "supervisor@test.com",
    # Must have read permission on Organization DocType
})

# 3. Create Person records linked to users
supervisor_person = frappe.get_doc({
    "doctype": "Person",
    "frappe_user": "supervisor@test.com",
    "primary_email": "supervisor@test.com"
})

# 4. Create Org Member records
supervisor_member = frappe.get_doc({
    "doctype": "Org Member",
    "person": supervisor_person.name,
    "organization": test_org.name,
    "role": "Test Supervisor",  # Links to supervisor role template
    "status": "Active"
})

# 5. Grant User Permission (CRITICAL - often forgotten!)
frappe.get_doc({
    "doctype": "User Permission",
    "user": "supervisor@test.com",
    "allow": "Organization",
    "for_value": test_org.name
}).insert()

# 6. Now test can run
frappe.set_user("supervisor@test.com")
result = get_org_members(test_org.name)
# Supervisor check logic will actually execute
```

### Key Challenges

1. **User Permission Requirement:** Users need BOTH:
   - Role-based permission (Dartwing User role)
   - User Permission for specific organization

2. **Role Template Setup:** Must have `is_supervisor` flag set correctly

3. **Test Isolation:** Careful cleanup required to avoid test pollution

4. **Fixture Reuse:** Consider creating reusable test fixtures for permission setup

---

## Proposed Test Structure

### Option A: Dedicated Integration Test File
```python
# dartwing/tests/test_email_visibility_integration.py

class TestEmailVisibilityIntegration(unittest.TestCase):
    """Integration tests for P2-001 email visibility requirement."""

    @classmethod
    def setUpClass(cls):
        # Create supervisor role template
        # Create non-supervisor role template
        # Create test users
        # Create Person records

    def setUp(self):
        # Create test organization
        # Create org members with different roles
        # Grant User Permissions

    def tearDown(self):
        # Clean up User Permissions
        # Clean up test data

    def test_supervisor_sees_all_emails(self):
        # Test 1 implementation

    def test_non_supervisor_sees_own_email_only(self):
        # Test 2 implementation

    def test_non_supervisor_cannot_see_other_emails(self):
        # Test 3 implementation
```

### Option B: Extend Existing Test File
Add tests to `test_organization_api.py` with clear section marker:

```python
# =========================================================================
# Email Visibility Integration Tests (P2-001 Security Requirement)
# =========================================================================
```

**Recommendation:** Option A (dedicated file) for better separation and maintainability.

---

## Test Scenarios Detail

### Scenario 1: Supervisor Access
```python
def test_supervisor_sees_all_emails(self):
    """Verify supervisors can see all member emails (P2-001)."""

    # Setup: Create org with 3 members (1 supervisor, 2 non-supervisors)
    # Create user with supervisor role
    # Grant User Permission

    frappe.set_user("supervisor@test.com")
    result = get_org_members(self.test_org.name)

    # Verify structure
    self.assertEqual(len(result["data"]), 3)

    # Verify ALL members have person_email field
    for member in result["data"]:
        self.assertIn("person_email", member,
            f"Supervisor should see email for member {member['name']}")
        self.assertIsNotNone(member["person_email"],
            f"Email should not be None for member {member['name']}")
```

### Scenario 2: Non-Supervisor Self-Access
```python
def test_non_supervisor_sees_own_email_only(self):
    """Verify non-supervisors can only see their own email (P2-001)."""

    # Setup: Same org with 3 members
    # Create user with non-supervisor role
    # Grant User Permission

    frappe.set_user("employee@test.com")
    result = get_org_members(self.test_org.name)

    # Find user's own record
    own_record = next(m for m in result["data"]
                     if m["person"] == self.employee_person.name)

    # Verify own email is visible
    self.assertIn("person_email", own_record,
        "Non-supervisor should see their own email")
    self.assertEqual(own_record["person_email"], "employee@test.com")
```

### Scenario 3: Non-Supervisor Restriction
```python
def test_non_supervisor_cannot_see_other_emails(self):
    """Verify non-supervisors cannot see other members' emails (P2-001)."""

    # Setup: Same org with 3 members
    # User with non-supervisor role

    frappe.set_user("employee@test.com")
    result = get_org_members(self.test_org.name)

    # Get all records EXCEPT user's own
    other_records = [m for m in result["data"]
                    if m["person"] != self.employee_person.name]

    # Verify person_email is NOT present for other members
    for member in other_records:
        self.assertNotIn("person_email", member,
            f"Non-supervisor should NOT see email for member {member['name']}")
```

---

## Code References

### Implementation Logic to Test

**File:** `dartwing/dartwing_core/api/organization_api.py`

**Lines 181-196:** Supervisor check logic
```python
if user == "Administrator":
    is_current_user_supervisor = True
else:
    current_person = frappe.db.get_value("Person", {"frappe_user": user}, "name")
    if current_person:
        is_current_user_supervisor = _is_supervisor_cached(current_person, organization)
```

**Lines 250-253:** Email inclusion logic
```python
if is_current_user_supervisor or (current_person and m.person == current_person):
    member_data["person_email"] = m.person_email
```

**Lines 56-93:** Supervisor cache implementation (with 60s TTL)

---

## Success Criteria

**Tests pass when:**
1. ✅ All 3 core scenarios pass
2. ✅ No test pollution (fixtures cleaned up properly)
3. ✅ Tests run in isolation (can run individually)
4. ✅ Tests are deterministic (no flaky failures)
5. ✅ Code coverage increases for lines 181-196, 250-253

**Definition of Done:**
- [ ] Tests implemented and passing
- [ ] Code review approved
- [ ] CI/CD pipeline passing
- [ ] TODO comment removed from `test_organization_api.py:503-507`
- [ ] Documentation updated if needed

---

## Additional Context

### Why Not Blocking for Merge (009-api-helpers)

This test gap did not block the original branch merge because:
1. ✅ Functionality is correct (verified by code review)
2. ✅ Manual testing confirmed expected behavior
3. ✅ Administrator test validates API response structure
4. ✅ Test setup complexity is significant
5. ✅ No regression risk (new feature, not refactoring)

However, **this test should be implemented before refactoring** the supervisor logic to prevent regressions.

### Risk Assessment

**Without these tests:**
- **Likelihood of future bug:** LOW (code is straightforward)
- **Impact if bug occurs:** MEDIUM (privacy violation - users see emails they shouldn't)
- **Detection time:** Could go unnoticed until user reports

**With these tests:**
- **Regression detection:** IMMEDIATE (CI/CD would catch it)
- **Refactoring confidence:** HIGH (safe to improve supervisor logic)
- **Documentation value:** Tests serve as executable specification

---

## Resources

**Related Files:**
- Implementation: `dartwing/dartwing_core/api/organization_api.py`
- Current tests: `dartwing/tests/test_organization_api.py`
- Review documentation: `specs/009-api-helpers/review/code_review_batch3_report.md`

**Frappe Documentation:**
- [User Permissions](https://frappeframework.com/docs/user/en/basics/users-and-permissions)
- [Role-Based Permissions](https://frappeframework.com/docs/user/en/basics/users-and-permissions/role-based-permissions)
- [Writing Tests](https://frappeframework.com/docs/user/en/testing)

**Security Requirement:**
- P2-001: Supervisor email visibility control
- FR-012: Audit logging for privacy-related access

---

## Comments

> **Note from Code Review (2025-12-16):**
> The TODO comment in `test_organization_api.py` (lines 503-507) documents this gap. The test was simplified to use Administrator access due to the complexity of proper permission setup. This issue captures the work needed for comprehensive coverage.

> **Implementation Note:**
> Consider creating a base test class with permission setup helpers that can be reused across test files. This would reduce the complexity burden for future permission-based tests.

---

**Created:** 2025-12-16
**Priority:** Medium (backlog for next sprint)
**Assignee:** TBD
**Milestone:** Testing Infrastructure Improvements

---

## Checklist for Implementation

- [ ] Review current test infrastructure for permission helpers
- [ ] Create Role Template fixtures (supervisor + non-supervisor)
- [ ] Create test user fixtures with proper roles
- [ ] Implement Scenario 1 (supervisor sees all)
- [ ] Implement Scenario 2 (non-supervisor sees own)
- [ ] Implement Scenario 3 (non-supervisor blocked from others)
- [ ] Add cache invalidation test (optional)
- [ ] Verify tests run in isolation
- [ ] Verify tests pass in CI/CD
- [ ] Update documentation
- [ ] Remove TODO comment from test_organization_api.py
- [ ] Code review and merge

---

**End of Issue**
