# API Contracts: Company DocType

**Feature**: 006-company-doctype
**Date**: 2025-12-13

## Overview

The Company DocType exposes standard Frappe REST APIs plus custom whitelisted methods. All endpoints follow Frappe's API conventions.

---

## Standard Frappe Resource API

Base URL: `/api/resource/Company`

### List Companies

```http
GET /api/resource/Company
```

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| fields | JSON array | Fields to return, e.g., `["name","legal_name","entity_type"]` |
| filters | JSON array | Frappe filters, e.g., `[["entity_type","=","LLC"]]` |
| limit_start | integer | Pagination offset (default: 0) |
| limit_page_length | integer | Page size (default: 20, max: 500) |
| order_by | string | Sort field, e.g., `creation desc` |

**Response** (200 OK):
```json
{
  "data": [
    {
      "name": "CO-00001",
      "legal_name": "Acme Inc",
      "entity_type": "LLC",
      "organization": "ORG-2025-00001"
    }
  ]
}
```

**Notes**:
- Results automatically filtered by User Permissions (user only sees Companies for their Organizations)

---

### Get Single Company

```http
GET /api/resource/Company/{name}
```

**Response** (200 OK):
```json
{
  "data": {
    "name": "CO-00001",
    "organization": "ORG-2025-00001",
    "legal_name": "Acme Inc",
    "tax_id": "12-3456789",
    "entity_type": "LLC",
    "jurisdiction_country": "United States",
    "jurisdiction_state": "Delaware",
    "formation_date": "2020-01-15",
    "registered_address": "ADDR-00001",
    "physical_address": "ADDR-00002",
    "registered_agent": "PERSON-2025-00001",
    "officers": [
      {
        "name": "abc123",
        "person": "PERSON-2025-00002",
        "title": "CEO",
        "start_date": "2020-01-15",
        "end_date": null
      }
    ],
    "members_partners": [
      {
        "name": "def456",
        "person": "PERSON-2025-00003",
        "ownership_percent": 60.0,
        "capital_contribution": 100000.00,
        "voting_rights": 60.0
      }
    ],
    "creation": "2025-01-01 10:00:00.000000",
    "modified": "2025-01-15 14:30:00.000000",
    "owner": "admin@example.com"
  }
}
```

---

### Create Company (Indirect via Organization)

Companies are not created directly. They are auto-created when an Organization with `org_type="Company"` is created.

```http
POST /api/resource/Organization
Content-Type: application/json

{
  "org_name": "Acme Inc",
  "org_type": "Company"
}
```

**Response** (200 OK):
```json
{
  "data": {
    "name": "ORG-2025-00001",
    "org_name": "Acme Inc",
    "org_type": "Company",
    "status": "Active",
    "linked_doctype": "Company",
    "linked_name": "CO-00001"
  }
}
```

The Company record is auto-created and linked. To access it:
```http
GET /api/resource/Company/CO-00001
```

---

### Update Company

```http
PUT /api/resource/Company/{name}
Content-Type: application/json

{
  "legal_name": "Acme Corporation",
  "tax_id": "12-3456789",
  "entity_type": "C-Corp",
  "jurisdiction_country": "United States",
  "jurisdiction_state": "Delaware"
}
```

**Response** (200 OK):
```json
{
  "data": {
    "name": "CO-00001",
    "legal_name": "Acme Corporation",
    "tax_id": "12-3456789",
    "entity_type": "C-Corp",
    "...": "..."
  }
}
```

---

### Update Officers (Child Table)

To update child tables, include the full array in the update:

```http
PUT /api/resource/Company/{name}
Content-Type: application/json

{
  "officers": [
    {
      "person": "PERSON-2025-00001",
      "title": "CEO",
      "start_date": "2020-01-15"
    },
    {
      "person": "PERSON-2025-00002",
      "title": "CFO",
      "start_date": "2021-06-01"
    }
  ]
}
```

---

### Delete Company (Indirect via Organization)

Companies are deleted via cascade when their parent Organization is deleted:

```http
DELETE /api/resource/Organization/{name}
```

This triggers the `on_trash` hook which cascade-deletes the linked Company.

---

## Custom API Methods

Base URL: `/api/method/dartwing.dartwing_company.api`

### Get Company with Organization Details

Returns Company merged with parent Organization fields for convenience.

```http
GET /api/method/dartwing.dartwing_company.api.get_company_with_org_details
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| company | string | Yes | Company name (e.g., "CO-00001") |

**Response** (200 OK):
```json
{
  "message": {
    "name": "CO-00001",
    "organization": "ORG-2025-00001",
    "legal_name": "Acme Inc",
    "entity_type": "LLC",
    "org_details": {
      "org_name": "Acme Inc",
      "status": "Active",
      "logo": "/files/acme-logo.png"
    },
    "officers": [...],
    "members_partners": [...]
  }
}
```

---

### Get Companies for Current User

Returns all Companies the current user has permission to access.

```http
GET /api/method/dartwing.dartwing_company.api.get_user_companies
```

**Response** (200 OK):
```json
{
  "message": [
    {
      "name": "CO-00001",
      "legal_name": "Acme Inc",
      "entity_type": "LLC",
      "organization": "ORG-2025-00001",
      "org_name": "Acme Inc"
    },
    {
      "name": "CO-00002",
      "legal_name": "Beta Corp",
      "entity_type": "C-Corp",
      "organization": "ORG-2025-00002",
      "org_name": "Beta Corp"
    }
  ]
}
```

---

### Validate Ownership Totals

Check if ownership percentages are valid for a Company.

```http
GET /api/method/dartwing.dartwing_company.api.validate_ownership
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| company | string | Yes | Company name |

**Response** (200 OK):
```json
{
  "message": {
    "valid": false,
    "total_ownership": 105.0,
    "total_voting_rights": 100.0,
    "warnings": [
      "Total ownership (105%) exceeds 100%"
    ]
  }
}
```

---

## Error Responses

### 403 Forbidden (Permission Denied)

```json
{
  "exc_type": "PermissionError",
  "exception": "frappe.exceptions.PermissionError",
  "_server_messages": "[\"No permission to access Company CO-00001\"]"
}
```

### 404 Not Found

```json
{
  "exc_type": "DoesNotExistError",
  "exception": "frappe.exceptions.DoesNotExistError",
  "_server_messages": "[\"Company CO-99999 not found\"]"
}
```

### 417 Validation Error

```json
{
  "exc_type": "ValidationError",
  "exception": "frappe.exceptions.ValidationError",
  "_server_messages": "[\"Person is required in officers table\"]"
}
```

---

## Authentication

All API calls require authentication via one of:
1. **Session cookie** (after login to Frappe)
2. **API Key + Secret** header: `Authorization: token api_key:api_secret`
3. **OAuth2 Bearer token**: `Authorization: Bearer {access_token}`

---

## Rate Limiting

Standard Frappe rate limits apply:
- 5 requests/second per user (default)
- 200 requests/minute per user (default)

---

## OpenAPI Schema Reference

For OpenAPI 3.0 schema, see: `contracts/openapi.yaml` (generated by task T061)
