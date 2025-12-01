# Dartwing API Documentation

## Overview

Dartwing is a Family/Organization Management System built on the Frappe Framework. It provides RESTful API endpoints to manage family entities and members.

## Current Implementation

**Status**: v0.1.0 - Early Development
**Module**: Dartwing Core
**Framework**: Frappe

### What's Implemented

✅ **Family CRUD API** - Full create, read, update, delete operations
✅ **Family Member Management** - Add, update, delete members within families
✅ **Search & Filtering** - Query families by name or description
✅ **Statistics** - Aggregate data about families

### What's Planned (Not Yet Implemented)

❌ Organization linking (multi-tenant isolation)
❌ Permission-based access control
❌ Real-time sync endpoints
❌ ERPNext Integration (accounting)
❌ Frappe Health Integration (healthcare)
❌ Frappe Drive Integration (document management)

## Data Model

### Family DocType

Manages family entities.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `family_name` | Data | Yes | Unique name of the family |
| `slug` | Data | Auto | URL-friendly identifier (auto-generated) |
| `description` | Text | No | Optional description |
| `tags` | Data | No | Optional tags |
| `contact_email` | Data | No | Contact email address |
| `contact_phone` | Data | No | Contact phone number |
| `status` | Select | Yes | Status: Active, Inactive, Archived |
| `created_date` | Date | Auto | Auto-populated creation date |
| `members` | Table | No | Child table of Family Members |

### Family Member (Child Table)

Members within a family.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `full_name` | Data | Yes | Full name of the member |
| `relationship` | Select | No | Parent, Child, Spouse, Sibling, Other |
| `email` | Data | No | Email address |
| `phone` | Data | No | Phone number |
| `date_of_birth` | Date | No | Date of birth |
| `status` | Select | No | Active, Inactive |
| `notes` | Small Text | No | Additional notes |

**Permissions:**
- System Manager: Full access
- Family Manager: Full access

## API Endpoints

All endpoints are accessible via HTTP POST to:
```
POST /api/method/dartwing.api.v1.<method_name>
```

### Authentication

All endpoints require Frappe authentication (API key/secret or session).

---

## Family Endpoints

### 1. Create Family

**Endpoint:** `dartwing.api.v1.create_family`

**Description:** Create a new family with optional members.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `family_name` | string | Yes | - | Name of the family |
| `description` | string | No | null | Optional description |
| `status` | string | No | "Active" | Status: Active, Inactive, Archived |
| `members` | array | No | [] | Array of member objects |

**Response:**
```json
{
  "success": true,
  "message": "Family created successfully",
  "data": {
    "name": "Smith Family",
    "family_name": "Smith Family",
    "slug": "smith-family",
    "description": "The Smith family",
    "status": "Active",
    "created_date": "2025-01-17",
    "members": []
  }
}
```

---

### 2. Get Family

**Endpoint:** `dartwing.api.v1.get_family`

**Description:** Retrieve a specific family by name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family |

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Smith Family",
    "family_name": "Smith Family",
    "slug": "smith-family",
    "description": "The Smith family",
    "status": "Active",
    "created_date": "2025-01-17",
    "members": [...]
  }
}
```

---

### 3. Get All Families

**Endpoint:** `dartwing.api.v1.get_all_families`

**Description:** List all families with optional filtering and pagination.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filters` | dict/JSON | No | {} | Filter criteria |
| `fields` | list/JSON | No | Default fields | Fields to return |
| `limit_start` | int | No | 0 | Pagination offset |
| `limit_page_length` | int | No | 20 | Records per page |

**Default Fields:**
- `name`
- `family_name`
- `status`
- `created_date`

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "name": "Smith Family",
      "family_name": "Smith Family",
      "status": "Active",
      "created_date": "2025-01-17"
    }
  ]
}
```

---

### 4. Update Family

**Endpoint:** `dartwing.api.v1.update_family`

**Description:** Update an existing family.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family |
| `family_name` | string | No | Updated name |
| `description` | string | No | Updated description |
| `status` | string | No | Updated status |
| `members` | array | No | Updated members array |

---

### 5. Delete Family

**Endpoint:** `dartwing.api.v1.delete_family`

**Description:** Delete a family.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family |

**Response:**
```json
{
  "success": true,
  "message": "Family deleted successfully"
}
```

---

### 6. Search Families

**Endpoint:** `dartwing.api.v1.search_families`

**Description:** Search for families by name or description.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search term |
| `limit` | int | No | 20 | Maximum results |

---

### 7. Get Family Statistics

**Endpoint:** `dartwing.api.v1.get_family_stats`

**Description:** Get aggregate statistics about all families.

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 15,
    "by_status": {
      "active": 12,
      "inactive": 2,
      "archived": 1
    }
  }
}
```

---

## Family Member Endpoints

### 8. Add Family Member

**Endpoint:** `dartwing.api.v1.add_family_member`

**Description:** Add a member to a family.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `family` | string | Yes | Family name |
| `full_name` | string | Yes | Member's full name |
| `relationship` | string | No | Parent, Child, Spouse, Sibling, Other |
| `email` | string | No | Email address |
| `phone` | string | No | Phone number |
| `date_of_birth` | date | No | Date of birth |
| `status` | string | No | Active, Inactive |
| `notes` | string | No | Additional notes |

**Response:**
```json
{
  "success": true,
  "message": "Member added",
  "data": {
    "name": "abc123xyz",
    "full_name": "John Smith",
    "relationship": "Parent",
    "email": "john@example.com"
  }
}
```

---

### 9. Update Family Member

**Endpoint:** `dartwing.api.v1.update_family_member`

**Description:** Update a family member by child table name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `family` | string | Yes | Family name |
| `member_name` | string | Yes | Child table row name |
| `full_name` | string | No | Updated name |
| `relationship` | string | No | Updated relationship |
| `email` | string | No | Updated email |
| `phone` | string | No | Updated phone |
| `date_of_birth` | date | No | Updated DOB |
| `status` | string | No | Updated status |
| `notes` | string | No | Updated notes |

---

### 10. Delete Family Member

**Endpoint:** `dartwing.api.v1.delete_family_member`

**Description:** Remove a member from a family.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `family` | string | Yes | Family name |
| `member_name` | string | Yes | Child table row name |

**Response:**
```json
{
  "success": true,
  "message": "Member deleted"
}
```

---

## Usage Examples

### Using cURL

```bash
# Create a family
curl -X POST https://your-site.com/api/method/dartwing.api.v1.create_family \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "family_name": "Johnson Family",
    "description": "Johnson family",
    "status": "Active"
  }'

# Add a member
curl -X POST https://your-site.com/api/method/dartwing.api.v1.add_family_member \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "family": "Johnson Family",
    "full_name": "John Johnson",
    "relationship": "Parent",
    "email": "john@example.com"
  }'

# Get all families
curl -X POST https://your-site.com/api/method/dartwing.api.v1.get_all_families \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {"status": "Active"},
    "limit_page_length": 10
  }'
```

### Using Python

```python
import frappe

# Create a family
result = frappe.call(
    "dartwing.api.v1.create_family",
    family_name="Johnson Family",
    description="Johnson family",
    status="Active"
)

# Add a member
member = frappe.call(
    "dartwing.api.v1.add_family_member",
    family="Johnson Family",
    full_name="John Johnson",
    relationship="Parent",
    email="john@example.com"
)

# Get all families
families = frappe.call(
    "dartwing.api.v1.get_all_families",
    filters={"status": "Active"},
    limit_page_length=10
)
```

### Using JavaScript

```javascript
// Create a family
frappe.call({
    method: 'dartwing.api.v1.create_family',
    args: {
        family_name: 'Johnson Family',
        description: 'Johnson family',
        status: 'Active'
    },
    callback: function(r) {
        if (r.message.success) {
            console.log('Created:', r.message.data);
        }
    }
});

// Add a member
frappe.call({
    method: 'dartwing.api.v1.add_family_member',
    args: {
        family: 'Johnson Family',
        full_name: 'John Johnson',
        relationship: 'Parent'
    },
    callback: function(r) {
        if (r.message.success) {
            console.log('Added:', r.message.data);
        }
    }
});
```

## Error Handling

All endpoints follow a consistent pattern:

**Success Response:**
```json
{
  "success": true,
  "message": "...",
  "data": {...}
}
```

**Error Response:**
Frappe throws exceptions that return:
```json
{
  "exc_type": "ValidationError",
  "exception": "Error message here"
}
```

Common error types:
- `ValidationError` - Invalid input or business logic violation
- `DoesNotExistError` - Requested resource not found
- `DuplicateEntryError` - Unique constraint violation

## Module Structure

```
dartwing/
├── __init__.py
├── hooks.py                    # Frappe app hooks
├── modules.txt                 # Registered modules
├── patches.txt                 # Database patches
├── api/
│   ├── __init__.py
│   ├── v1.py                   # Family API endpoints (current)
│   └── utils.py                # API helpers
├── dartwing_core/
│   └── doctype/
│       ├── family/             # Family DocType
│       └── family_member/      # Family Member child table
└── fixtures/
    └── role.json               # Role fixtures
```

## License

Apache 2.0 - See [LICENSE](./LICENSE) for details.
