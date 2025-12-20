# Quickstart: API Helpers (Whitelisted Methods)

**Feature**: 009-api-helpers
**Date**: 2025-12-14

## Overview

This feature provides four whitelisted API methods for Flutter client integration:

1. `get_user_organizations()` - List user's organizations
2. `get_organization_with_details(organization)` - Get org with concrete type
3. `get_concrete_doc(organization)` - Get concrete type only
4. `get_org_members(organization, ...)` - List org members with pagination

## Prerequisites

- Frappe 15.x installed
- dartwing app installed
- Features #1-#5 implemented (Person, Role Template, Org Member, Org Hooks, User Permissions)
- At least one Organization with concrete type created

## Quick Test (via Frappe Console)

```bash
cd ~/frappe-bench
bench --site your-site.local console
```

```python
import frappe

# Login as test user
frappe.set_user("test@example.com")

# Test get_user_organizations
from dartwing.dartwing_core.api.organization_api import get_user_organizations
result = get_user_organizations()
print(result)

# Test get_organization_with_details
from dartwing.dartwing_core.doctype.organization.organization import get_organization_with_details
result = get_organization_with_details("ORG-2025-00001")
print(result)

# Test get_concrete_doc
from dartwing.dartwing_core.doctype.organization.organization import get_concrete_doc
result = get_concrete_doc("ORG-2025-00001")
print(result)

# Test get_org_members
from dartwing.dartwing_core.api.organization_api import get_org_members
result = get_org_members("ORG-2025-00001", limit=10, offset=0)
print(result)
```

## API Usage (HTTP)

All endpoints use POST with JSON body. Include session cookie for authentication.

### Get User's Organizations

```bash
curl -X POST 'http://localhost:8000/api/method/dartwing.dartwing_core.api.organization_api.get_user_organizations' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: sid=YOUR_SESSION_ID'
```

Response:
```json
{
  "message": {
    "data": [
      {
        "name": "ORG-2025-00001",
        "org_name": "Smith Family",
        "org_type": "Family",
        "status": "Active",
        "role": "Parent",
        "is_supervisor": 1
      }
    ],
    "total_count": 1
  }
}
```

### Get Organization with Details

```bash
curl -X POST 'http://localhost:8000/api/method/dartwing.dartwing_core.doctype.organization.organization.get_organization_with_details' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: sid=YOUR_SESSION_ID' \
  -d '{"organization": "ORG-2025-00001"}'
```

Response:
```json
{
  "message": {
    "name": "ORG-2025-00001",
    "org_name": "Smith Family",
    "org_type": "Family",
    "concrete_type": {
      "name": "FAM-00001",
      "family_name": "Smith Family",
      "parental_controls_enabled": 1
    }
  }
}
```

### Get Concrete Doc

```bash
curl -X POST 'http://localhost:8000/api/method/dartwing.dartwing_core.doctype.organization.organization.get_concrete_doc' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: sid=YOUR_SESSION_ID' \
  -d '{"organization": "ORG-2025-00001"}'
```

Response:
```json
{
  "message": {
    "name": "FAM-00001",
    "family_name": "Smith Family",
    "parental_controls_enabled": 1
  }
}
```

### Get Organization Members

```bash
curl -X POST 'http://localhost:8000/api/method/dartwing.dartwing_core.api.organization_api.get_org_members' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: sid=YOUR_SESSION_ID' \
  -d '{"organization": "ORG-2025-00001", "limit": 20, "offset": 0, "status": "Active"}'
```

Response:
```json
{
  "message": {
    "data": [
      {
        "name": "OM-00001",
        "person": "PER-00001",
        "member_name": "John Smith",
        "role": "Parent",
        "status": "Active",
        "is_supervisor": 1
      }
    ],
    "total_count": 2,
    "limit": 20,
    "offset": 0
  }
}
```

## Flutter Usage

```dart
// Using Dio for HTTP requests
final dio = Dio();
dio.options.baseUrl = 'http://localhost:8000';
dio.options.headers['Cookie'] = 'sid=$sessionId';

// Get user's organizations
Future<List<Organization>> getUserOrganizations() async {
  final response = await dio.post(
    '/api/method/dartwing.dartwing_core.api.organization_api.get_user_organizations',
  );
  final data = response.data['message']['data'] as List;
  return data.map((e) => Organization.fromJson(e)).toList();
}

// Get organization with details
Future<OrganizationWithDetails> getOrganizationWithDetails(String orgId) async {
  final response = await dio.post(
    '/api/method/dartwing.dartwing_core.doctype.organization.organization.get_organization_with_details',
    data: {'organization': orgId},
  );
  return OrganizationWithDetails.fromJson(response.data['message']);
}

// Get org members with pagination
Future<PaginatedMembers> getOrgMembers(
  String orgId, {
  int limit = 20,
  int offset = 0,
  String? status,
}) async {
  final response = await dio.post(
    '/api/method/dartwing.dartwing_core.api.organization_api.get_org_members',
    data: {
      'organization': orgId,
      'limit': limit,
      'offset': offset,
      if (status != null) 'status': status,
    },
  );
  return PaginatedMembers.fromJson(response.data['message']);
}
```

## Error Handling

All methods throw Frappe exceptions that translate to HTTP errors:

| Error | HTTP Status | When |
|-------|-------------|------|
| `AuthenticationError` | 401 | Not logged in |
| `PermissionError` | 403 | User lacks Organization access |
| `DoesNotExistError` | 404 | Organization not found |
| `ValidationError` | 417 | Invalid parameters |

```dart
try {
  final org = await getOrganizationWithDetails('ORG-2025-00001');
} on DioException catch (e) {
  if (e.response?.statusCode == 403) {
    // Handle permission denied
  } else if (e.response?.statusCode == 404) {
    // Handle not found
  }
}
```

## Running Tests

```bash
cd ~/frappe-bench
bench --site your-site.local run-tests --app dartwing --module dartwing_core.api.test_organization_api
```

## File Locations

| File | Purpose |
|------|---------|
| `dartwing/dartwing_core/api/organization_api.py` | New API methods |
| `dartwing/dartwing_core/doctype/organization/organization.py` | Existing methods |
| `dartwing/dartwing_core/api/test_organization_api.py` | API tests |
| `specs/009-api-helpers/contracts/organization-api.yaml` | OpenAPI spec |
