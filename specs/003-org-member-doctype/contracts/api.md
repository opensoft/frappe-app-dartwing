# API Contract: Org Member DocType

**Feature**: 003-org-member-doctype
**Date**: 2025-12-12

## Overview

This document defines the API contracts for Org Member management. All endpoints follow Frappe's standard patterns and are accessible via `/api/method/dartwing.dartwing_core.doctype.org_member.org_member.{method}`.

---

## Standard Frappe Resource API

### Create Org Member

```
POST /api/resource/Org Member
```

**Request Body**:
```json
{
  "person": "PERSON-2025-00001",
  "organization": "ORG-2025-00001",
  "role": "Employee",
  "status": "Active",
  "start_date": "2025-12-12"
}
```

**Response (201 Created)**:
```json
{
  "data": {
    "name": "abc123xyz",
    "person": "PERSON-2025-00001",
    "organization": "ORG-2025-00001",
    "role": "Employee",
    "status": "Active",
    "start_date": "2025-12-12",
    "end_date": null,
    "member_name": "John Doe",
    "organization_name": "Acme Corp",
    "organization_type": "Company"
  }
}
```

**Error Responses**:

- `400 Bad Request` - Validation error (duplicate membership, invalid role for org type)
- `403 Forbidden` - Permission denied
- `404 Not Found` - Person, Organization, or Role Template not found

---

## Custom Whitelist Methods

### get_members_for_organization

Get all members of an organization with optional status filter.

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.get_members_for_organization
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| organization | string | Yes | Organization document name |
| status | string | No | Filter by status (Active/Inactive/Pending). Default: all statuses |
| include_inactive | boolean | No | Include inactive members. Default: false |

**Request**:
```json
{
  "organization": "ORG-2025-00001",
  "status": "Active"
}
```

**Response (200 OK)**:
```json
{
  "message": [
    {
      "name": "abc123xyz",
      "person": "PERSON-2025-00001",
      "member_name": "John Doe",
      "role": "Manager",
      "is_supervisor": 1,
      "status": "Active",
      "start_date": "2025-01-15"
    },
    {
      "name": "def456uvw",
      "person": "PERSON-2025-00002",
      "member_name": "Jane Smith",
      "role": "Employee",
      "is_supervisor": 0,
      "status": "Active",
      "start_date": "2025-03-01"
    }
  ]
}
```

---

### get_organizations_for_person

Get all organizations a person belongs to.

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.get_organizations_for_person
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| person | string | Yes | Person document name |
| status | string | No | Filter by membership status. Default: "Active" |

**Request**:
```json
{
  "person": "PERSON-2025-00001"
}
```

**Response (200 OK)**:
```json
{
  "message": [
    {
      "name": "abc123xyz",
      "organization": "ORG-2025-00001",
      "organization_name": "Acme Corp",
      "organization_type": "Company",
      "role": "Manager",
      "is_supervisor": 1,
      "status": "Active",
      "start_date": "2025-01-15"
    },
    {
      "name": "ghi789rst",
      "organization": "ORG-2025-00003",
      "organization_name": "Smith Family",
      "organization_type": "Family",
      "role": "Parent",
      "is_supervisor": 1,
      "status": "Active",
      "start_date": "2024-06-01"
    }
  ]
}
```

---

### add_member_to_organization

Add a new member or reactivate an existing inactive membership.

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.add_member_to_organization
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| person | string | Yes | Person document name |
| organization | string | Yes | Organization document name |
| role | string | Yes | Role Template name |
| status | string | No | Initial status. Default: "Active" |
| start_date | string | No | Start date (YYYY-MM-DD). Default: today |

**Request**:
```json
{
  "person": "PERSON-2025-00003",
  "organization": "ORG-2025-00001",
  "role": "Employee"
}
```

**Response (200 OK)** - New membership:
```json
{
  "message": {
    "name": "jkl012mno",
    "action": "created",
    "person": "PERSON-2025-00003",
    "organization": "ORG-2025-00001",
    "role": "Employee",
    "status": "Active",
    "start_date": "2025-12-12"
  }
}
```

**Response (200 OK)** - Reactivated membership:
```json
{
  "message": {
    "name": "abc123xyz",
    "action": "reactivated",
    "person": "PERSON-2025-00003",
    "organization": "ORG-2025-00001",
    "role": "Employee",
    "status": "Active",
    "start_date": "2025-12-12",
    "previous_status": "Inactive"
  }
}
```

**Error Responses**:

- `400 Bad Request`:
  ```json
  {
    "exc_type": "ValidationError",
    "message": "Person is already an active member of this organization"
  }
  ```

  ```json
  {
    "exc_type": "ValidationError",
    "message": "Role 'Employee' is not valid for Family organizations"
  }
  ```

---

### deactivate_member

Deactivate a member (set status to Inactive).

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.deactivate_member
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| member | string | Yes | Org Member document name |
| end_date | string | No | End date (YYYY-MM-DD). Default: today |

**Request**:
```json
{
  "member": "abc123xyz",
  "end_date": "2025-12-31"
}
```

**Response (200 OK)**:
```json
{
  "message": {
    "name": "abc123xyz",
    "status": "Inactive",
    "end_date": "2025-12-31"
  }
}
```

**Error Response** - Last supervisor:
```json
{
  "exc_type": "ValidationError",
  "message": "Cannot deactivate: at least one supervisor must remain in the organization"
}
```

---

### change_member_role

Change a member's assigned role.

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.change_member_role
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| member | string | Yes | Org Member document name |
| new_role | string | Yes | New Role Template name |

**Request**:
```json
{
  "member": "abc123xyz",
  "new_role": "Manager"
}
```

**Response (200 OK)**:
```json
{
  "message": {
    "name": "abc123xyz",
    "previous_role": "Employee",
    "role": "Manager"
  }
}
```

**Error Responses**:

- `400 Bad Request` - Role not valid for org type:
  ```json
  {
    "exc_type": "ValidationError",
    "message": "Role 'Owner' is not valid for Family organizations"
  }
  ```

- `400 Bad Request` - Would leave no supervisors:
  ```json
  {
    "exc_type": "ValidationError",
    "message": "Cannot change role: at least one supervisor must remain in the organization"
  }
  ```

---

### check_is_last_supervisor

Check if a member is the last supervisor in their organization.

```
POST /api/method/dartwing.dartwing_core.doctype.org_member.org_member.check_is_last_supervisor
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| member | string | Yes | Org Member document name |

**Request**:
```json
{
  "member": "abc123xyz"
}
```

**Response (200 OK)**:
```json
{
  "message": {
    "is_last_supervisor": true,
    "supervisor_count": 1,
    "member_role_is_supervisor": true
  }
}
```

---

## Error Codes Reference

| Code | Description |
|------|-------------|
| `DUPLICATE_MEMBERSHIP` | Person is already a member of the organization |
| `INVALID_ROLE_FOR_ORG_TYPE` | Role does not match organization type |
| `LAST_SUPERVISOR` | Cannot remove/deactivate last supervisor |
| `PERSON_NOT_FOUND` | Referenced Person does not exist |
| `ORGANIZATION_NOT_FOUND` | Referenced Organization does not exist |
| `ROLE_NOT_FOUND` | Referenced Role Template does not exist |
| `MEMBER_NOT_FOUND` | Org Member document does not exist |
| `INVALID_STATUS_TRANSITION` | Invalid status change (e.g., Inactive to Pending) |
