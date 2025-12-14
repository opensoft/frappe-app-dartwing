# Research: API Helpers (Whitelisted Methods)

**Date**: 2025-12-14
**Feature**: 009-api-helpers

## Executive Summary

This research documents existing implementations, design decisions, and patterns for the four API helper methods. Two methods (`get_concrete_doc`, `get_organization_with_details`) are already implemented in `organization.py`. Related methods for Org Member queries exist but need enhancement to meet spec requirements.

## Research Findings

### 1. Existing API Methods

**Decision**: Build on existing implementations rather than creating new ones.

**Rationale**: Two of the four required methods already exist in `dartwing/dartwing_core/doctype/organization/organization.py`:
- `get_concrete_doc(organization: str)` - Returns concrete type document
- `get_organization_with_details(organization: str)` - Returns Organization with nested concrete_type

Both follow Frappe patterns and include logging. Need to add explicit permission checks.

**Alternatives considered**:
- Creating new standalone API module - Rejected because methods are Organization-centric
- Complete rewrite - Rejected because existing implementations are solid

### 2. Org Member Query Methods

**Decision**: Enhance existing `get_members_for_organization` and `get_organizations_for_person` methods.

**Rationale**: The existing methods in `org_member.py` provide good foundations but need:
- `get_members_for_organization` → rename/wrap as `get_org_members` with pagination
- `get_organizations_for_person` → wrap as `get_user_organizations` to get current user's orgs

**Current limitations**:
- No pagination support (limit/offset)
- No total count returned for pagination UI
- `get_organizations_for_person` requires explicit person parameter (should derive from logged-in user)

**Alternatives considered**:
- Modifying existing methods directly - Rejected to maintain backward compatibility
- Creating completely new methods - Selected approach: new wrapper methods with pagination

### 3. Permission Model

**Decision**: Use Frappe's built-in permission system with `frappe.has_permission()` checks.

**Rationale**:
- Constitution requires permission checks on all API methods
- User Permission for Organization already implemented in Feature #5
- Methods should respect `user_permission_dependant_doctype = Organization`

**Implementation pattern**:
```python
@frappe.whitelist()
def get_organization_with_details(organization: str) -> dict:
    # Frappe automatically checks read permission via get_doc()
    # But explicit check provides clearer error messages
    if not frappe.has_permission("Organization", "read", organization):
        frappe.throw(_("Not permitted to access this organization"), frappe.PermissionError)
    ...
```

**Alternatives considered**:
- Custom permission logic - Rejected; use Frappe's proven system
- No explicit checks (rely on get_doc) - Rejected; need explicit errors for API clients

### 4. Response Format

**Decision**: Use consistent response format with Frappe's standard `as_dict()` plus wrapper for lists.

**Rationale**: Flutter client needs predictable response structure.

**Standard patterns**:

Single document:
```python
return org.as_dict()  # Direct document dict
# or with nesting:
result = org.as_dict()
result["concrete_type"] = concrete.as_dict() if concrete else None
return result
```

List with pagination:
```python
return {
    "data": [...],         # List of records
    "total_count": 150,    # Total without pagination
    "limit": 20,           # Requested limit
    "offset": 0            # Current offset
}
```

**Alternatives considered**:
- Custom wrapper class - Rejected; adds complexity without benefit
- Different formats per method - Rejected; inconsistency hurts client development

### 5. Pagination Pattern

**Decision**: Standard limit/offset pagination with total count.

**Rationale**:
- Spec requires pagination for `get_org_members()` via limit/offset (FR-006)
- Frappe uses this pattern natively (`frappe.get_all(..., limit_page_length, limit_start)`)
- Simple for Flutter client to implement

**Default values**:
- limit: 20 (reasonable for mobile lists)
- offset: 0
- max_limit: 100 (prevent abuse)

**Implementation**:
```python
@frappe.whitelist()
def get_org_members(
    organization: str,
    limit: int = 20,
    offset: int = 0,
    status: str = None
) -> dict:
    limit = min(int(limit), 100)  # Cap at 100
    offset = max(int(offset), 0)   # No negative offset

    filters = {"organization": organization}
    if status:
        filters["status"] = status

    # Get paginated results
    data = frappe.get_all("Org Member", filters=filters,
                          limit_page_length=limit, limit_start=offset)

    # Get total count (separate query)
    total_count = frappe.db.count("Org Member", filters)

    return {
        "data": data,
        "total_count": total_count,
        "limit": limit,
        "offset": offset
    }
```

**Alternatives considered**:
- Cursor-based pagination - Rejected; overkill for member lists, complex for clients
- No pagination - Rejected; spec requires it (FR-006)

### 6. Audit Logging

**Decision**: Use existing `frappe.logger` pattern established in organization.py.

**Rationale**:
- Spec requires audit logging (FR-009)
- Existing pattern in organization.py uses `frappe.logger("dartwing_core.hooks")`
- Logs include user, organization, and timestamp via Frappe's built-in log format

**Log levels**:
- INFO: Successful API calls
- WARNING: Partial data (missing concrete type)
- ERROR: Permission denied, not found

**Alternatives considered**:
- Separate audit table - Rejected; Frappe's file logs sufficient for MVP
- No logging - Rejected; spec requires it

### 7. Error Response Format

**Decision**: Use Frappe's standard exception handling with consistent error types.

**Rationale**:
- Spec requires consistent error structure (FR-010)
- Frappe exceptions translate to HTTP status codes automatically

**Error mapping**:
| Scenario | Frappe Exception | HTTP Status |
|----------|-----------------|-------------|
| Not found | `frappe.DoesNotExistError` | 404 |
| Permission denied | `frappe.PermissionError` | 403 |
| Validation error | `frappe.ValidationError` | 417 |
| Auth required | `frappe.AuthenticationError` | 401 |

**Response structure** (handled by Frappe):
```json
{
    "exc_type": "DoesNotExistError",
    "message": "Organization ORG-2025-00001 not found"
}
```

**Alternatives considered**:
- Custom error wrapper - Rejected; Frappe's pattern is well-established

## Implementation Approach

### Method Locations

| Method | Location | Type |
|--------|----------|------|
| `get_user_organizations` | `dartwing_core/api/organization_api.py` | NEW file |
| `get_organization_with_details` | `dartwing_core/doctype/organization/organization.py` | EXISTS - add permission check |
| `get_concrete_doc` | `dartwing_core/doctype/organization/organization.py` | EXISTS - add permission check |
| `get_org_members` | `dartwing_core/api/organization_api.py` | NEW wrapper |

### API Endpoint Paths

Per constitution (API Design, #8):
- `get_user_organizations`: `/api/method/dartwing.dartwing_core.api.organization_api.get_user_organizations`
- `get_organization_with_details`: `/api/method/dartwing.dartwing_core.doctype.organization.organization.get_organization_with_details`
- `get_concrete_doc`: `/api/method/dartwing.dartwing_core.doctype.organization.organization.get_concrete_doc`
- `get_org_members`: `/api/method/dartwing.dartwing_core.api.organization_api.get_org_members`

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Person DocType | Required | Feature #1 - must exist for Org Member |
| Organization DocType | Available | Already implemented |
| Org Member DocType | Required | Feature #3 - must exist |
| User Permission Propagation | Required | Feature #5 - needed for permission checks |
| Role Template DocType | Required | Feature #2 - for member role info |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Permission not enforced | High (security) | Add explicit `has_permission` checks; integration tests |
| Missing concrete type | Medium | Return null with warning log; document in edge cases |
| Large member lists | Low | Enforce max_limit=100; pagination required |

## Next Steps

1. Create `dartwing/dartwing_core/api/` directory
2. Implement `organization_api.py` with new methods
3. Add explicit permission checks to existing organization.py methods
4. Create integration tests
5. Document API in contracts/
