# API Contracts: Organization Bidirectional Hooks

**Feature**: 004-org-bidirectional-hooks
**Date**: 2025-12-13

## Overview

This document defines the API contracts for the Organization bidirectional hooks feature. All endpoints follow Frappe's standard REST API patterns and are exposed via `@frappe.whitelist()` decorated methods.

---

## Endpoints

### 1. Get Concrete Document

Retrieves only the concrete type document for a given Organization.

**Endpoint**: `POST /api/method/dartwing.dartwing_core.doctype.organization.organization.get_concrete_doc`

**Request**:
```json
{
  "organization": "ORG-2025-00001"
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organization | string | Yes | Organization name/ID |

**Response (200 OK)**:
```json
{
  "message": {
    "name": "FAM-00001",
    "doctype": "Family",
    "organization": "ORG-2025-00001",
    "family_nickname": "The Smiths",
    "primary_residence": "ADDR-00001",
    "parental_controls_enabled": 0,
    "screen_time_limit_minutes": null,
    "creation": "2025-12-13 10:00:00",
    "modified": "2025-12-13 10:00:00",
    "owner": "Administrator"
  }
}
```

**Response (Organization Not Found - 404)**:
```json
{
  "exc_type": "DoesNotExistError",
  "exception": "Organization ORG-2025-99999 not found"
}
```

**Response (No Linked Concrete Type - 200 OK)**:
```json
{
  "message": null
}
```

---

### 2. Get Organization with Details

Retrieves Organization merged with its concrete type details in a single request.

**Endpoint**: `POST /api/method/dartwing.dartwing_core.doctype.organization.organization.get_organization_with_details`

**Request**:
```json
{
  "organization": "ORG-2025-00001"
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organization | string | Yes | Organization name/ID |

**Response (200 OK - Family type)**:
```json
{
  "message": {
    "name": "ORG-2025-00001",
    "doctype": "Organization",
    "org_name": "Smith Family",
    "org_type": "Family",
    "logo": null,
    "status": "Active",
    "linked_doctype": "Family",
    "linked_name": "FAM-00001",
    "creation": "2025-12-13 10:00:00",
    "modified": "2025-12-13 10:00:00",
    "owner": "Administrator",
    "concrete_type": {
      "name": "FAM-00001",
      "doctype": "Family",
      "organization": "ORG-2025-00001",
      "family_nickname": "The Smiths",
      "primary_residence": "ADDR-00001",
      "parental_controls_enabled": 0,
      "screen_time_limit_minutes": null
    }
  }
}
```

**Response (200 OK - Company type)**:
```json
{
  "message": {
    "name": "ORG-2025-00002",
    "doctype": "Organization",
    "org_name": "Acme Corp",
    "org_type": "Company",
    "logo": "/files/acme-logo.png",
    "status": "Active",
    "linked_doctype": "Company",
    "linked_name": "CO-00001",
    "creation": "2025-12-13 11:00:00",
    "modified": "2025-12-13 11:00:00",
    "owner": "Administrator",
    "concrete_type": {
      "name": "CO-00001",
      "doctype": "Company",
      "organization": "ORG-2025-00002",
      "legal_name": "Acme Corporation Inc.",
      "tax_id": "12-3456789",
      "entity_type": "C-Corp",
      "jurisdiction_country": "United States",
      "jurisdiction_state": "Delaware"
    }
  }
}
```

**Response (Organization Not Found - 404)**:
```json
{
  "exc_type": "DoesNotExistError",
  "exception": "Organization ORG-2025-99999 not found"
}
```

**Performance Requirement**: Response within 500ms under normal load.

---

## Standard CRUD Operations

The following standard Frappe REST API endpoints are affected by the bidirectional hooks:

### Create Organization

**Endpoint**: `POST /api/resource/Organization`

**Request**:
```json
{
  "org_name": "New Organization",
  "org_type": "Family"
}
```

**Behavior**:
1. Organization record created
2. `after_insert` hook fires
3. Family record auto-created with `organization` = new Organization name
4. Organization's `linked_doctype` = "Family", `linked_name` = Family record name
5. Hook execution logged

**Response (201 Created)**:
```json
{
  "data": {
    "name": "ORG-2025-00003",
    "org_name": "New Organization",
    "org_type": "Family",
    "status": "Active",
    "linked_doctype": "Family",
    "linked_name": "FAM-00002"
  }
}
```

**Response (Invalid org_type - 417)**:
```json
{
  "exc_type": "ValidationError",
  "exception": "Invalid org_type: InvalidType. Must be one of: Family, Company, Nonprofit, Association"
}
```

---

### Update Organization

**Endpoint**: `PUT /api/resource/Organization/{name}`

**Request (Allowed - modifying org_name)**:
```json
{
  "org_name": "Updated Name"
}
```

**Response (200 OK)**:
```json
{
  "data": {
    "name": "ORG-2025-00001",
    "org_name": "Updated Name",
    "org_type": "Family"
  }
}
```

**Request (Blocked - attempting to change org_type)**:
```json
{
  "org_type": "Company"
}
```

**Response (417 Expectation Failed)**:
```json
{
  "exc_type": "ValidationError",
  "exception": "Organization type cannot be changed after creation"
}
```

---

### Delete Organization

**Endpoint**: `DELETE /api/resource/Organization/{name}`

**Behavior**:
1. `on_trash` hook fires
2. Linked concrete type record deleted (cascade)
3. Organization record deleted
4. Hook execution logged

**Response (202 Accepted)**:
```json
{
  "message": "ok"
}
```

**Response (Blocked by references - 417)**:
```json
{
  "exc_type": "LinkExistsError",
  "exception": "Cannot delete Organization ORG-2025-00001: linked to Org Member OM-00001"
}
```

---

## Error Codes

| HTTP Status | Frappe Exception | Description |
|-------------|------------------|-------------|
| 200 | - | Success |
| 201 | - | Created |
| 202 | - | Accepted (delete) |
| 404 | DoesNotExistError | Resource not found |
| 403 | PermissionError | User lacks permission |
| 417 | ValidationError | Validation failed (e.g., invalid org_type, immutable field change) |
| 417 | LinkExistsError | Cannot delete due to references |
| 500 | - | Internal server error |

---

## Authentication

All endpoints require authentication via:
- Session cookie (Frappe Desk)
- API Key + Secret header (`Authorization: token api_key:api_secret`)
- OAuth2 Bearer token (`Authorization: Bearer <token>`)

---

## Rate Limits

Standard Frappe rate limits apply. No custom rate limiting for this feature.

---

## Audit Log Format

Hook executions are logged with the following structure:

```
[INFO] dartwing_core.hooks: Created Family FAM-00001 for Organization ORG-2025-00001
[INFO] dartwing_core.hooks: Cascade deleted Family FAM-00001 for Organization ORG-2025-00001
[ERROR] dartwing_core.hooks: Failed to create concrete type for Organization ORG-2025-00001: <error message>
[WARNING] dartwing_core.hooks: Concrete type Family FAM-00001 not found during cascade delete
```
