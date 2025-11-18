# Dartwing API Documentation

## Overview

Dartwing is a Family/Organization Management System built on the Frappe Framework. It provides RESTful API endpoints to manage family and organizational entities.

## Current Implementation

**Status**: v0.1.0 - Early Development  
**Module**: Family Manager  
**Framework**: Frappe

### What's Implemented

✅ **Family Organization CRUD API** - Full create, read, update, delete operations  
✅ **Search & Filtering** - Query families by name or description  
✅ **Statistics** - Aggregate data about families  

### What's Planned (Not Yet Implemented)

❌ ERPNext Integration (accounting)  
❌ Frappe Health Integration (healthcare)  
❌ Frappe Drive Integration (document management)  

## Data Model

### Family DocType

Manages family and organizational entities.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization_name` | Data | Yes | Unique name of the organization |
| `organization_type` | Select | Yes | Type: Family, Business, Non-Profit, Other |
| `description` | Text | No | Optional description |
| `status` | Select | Yes | Status: Active, Inactive, Archived |
| `created_date` | Date | Auto | Auto-populated creation date |

**Permissions:**
- System Manager: Full access
- All: Full access

**Features:**
- Auto-naming by organization_name field
- Rename allowed
- Change tracking enabled

## API Endpoints

All endpoints are accessible via HTTP POST to:
```
POST /api/method/dartwing.api.family.<method_name>
```

### Authentication

All endpoints require Frappe authentication (API key/secret or session).

---

### 1. Create Family

**Endpoint:** `dartwing.api.family.create_family`

**Description:** Create a new family/organization.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `organization_name` | string | Yes | - | Name of the organization |
| `organization_type` | string | No | "Family" | Type: Family, Business, Non-Profit, Other |
| `description` | string | No | null | Optional description |
| `status` | string | No | "Active" | Status: Active, Inactive, Archived |

**Response:**
```json
{
  "success": true,
  "message": "Family organization created successfully",
  "data": {
    "name": "Smith Family",
    "organization_name": "Smith Family",
    "organization_type": "Family",
    "description": "The Smith family organization",
    "status": "Active",
    "created_date": "2025-01-17"
  }
}
```

**Errors:**
- Organization name is required
- Family organization already exists
- Failed to create family organization

---

### 2. Get Family

**Endpoint:** `dartwing.api.family.get_family`

**Description:** Retrieve a specific family/organization by name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family organization |

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Smith Family",
    "organization_name": "Smith Family",
    "organization_type": "Family",
    "description": "The Smith family organization",
    "status": "Active",
    "created_date": "2025-01-17"
  }
}
```

**Errors:**
- Family name is required
- Family organization not found

---

### 3. Get All Families

**Endpoint:** `dartwing.api.family.get_all_families`

**Description:** List all families with optional filtering and pagination.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filters` | dict/JSON | No | {} | Filter criteria (e.g., `{"status": "Active"}`) |
| `fields` | list/JSON | No | Default fields | Fields to return |
| `limit_start` | int | No | 0 | Pagination offset |
| `limit_page_length` | int | No | 20 | Number of records per page |

**Default Fields:**
- `name`
- `organization_name`
- `organization_type`
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
      "organization_name": "Smith Family",
      "organization_type": "Family",
      "status": "Active",
      "created_date": "2025-01-17"
    },
    {
      "name": "Acme Corp",
      "organization_name": "Acme Corp",
      "organization_type": "Business",
      "status": "Active",
      "created_date": "2025-01-16"
    }
  ]
}
```

**Example Filters:**
```json
// Active families only
{"status": "Active"}

// Business organizations
{"organization_type": "Business"}

// Multiple conditions
{"status": "Active", "organization_type": "Family"}
```

---

### 4. Update Family

**Endpoint:** `dartwing.api.family.update_family`

**Description:** Update an existing family/organization.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family organization |
| `organization_type` | string | No | Updated type |
| `description` | string | No | Updated description |
| `status` | string | No | Updated status |

**Note:** The `organization_name` field cannot be updated via this endpoint (use Frappe's rename feature).

**Response:**
```json
{
  "success": true,
  "message": "Family organization updated successfully",
  "data": {
    "name": "Smith Family",
    "organization_name": "Smith Family",
    "organization_type": "Family",
    "description": "Updated description",
    "status": "Inactive",
    "created_date": "2025-01-17"
  }
}
```

**Errors:**
- Family name is required
- Family organization not found
- Failed to update family organization

---

### 5. Delete Family

**Endpoint:** `dartwing.api.family.delete_family`

**Description:** Delete a family/organization.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the family organization |

**Response:**
```json
{
  "success": true,
  "message": "Family organization deleted successfully"
}
```

**Errors:**
- Family name is required
- Family organization not found
- Failed to delete family organization

---

### 6. Search Families

**Endpoint:** `dartwing.api.family.search_families`

**Description:** Search for families by name or description.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search term |
| `limit` | int | No | 20 | Maximum results |

**Response:**
```json
{
  "success": true,
  "count": 1,
  "data": [
    {
      "name": "Smith Family",
      "organization_name": "Smith Family",
      "organization_type": "Family",
      "status": "Active",
      "description": "The Smith family organization"
    }
  ]
}
```

**Errors:**
- Search query is required
- Failed to search family organizations

---

### 7. Get Family Statistics

**Endpoint:** `dartwing.api.family.get_family_stats`

**Description:** Get aggregate statistics about all families.

**Parameters:** None

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
    },
    "by_type": {
      "Family": 8,
      "Business": 5,
      "Non-Profit": 2
    }
  }
}
```

**Errors:**
- Failed to get family statistics

---

## Usage Examples

### Using cURL

```bash
# Create a family
curl -X POST https://your-site.com/api/method/dartwing.api.family.create_family \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Johnson Family",
    "organization_type": "Family",
    "description": "Johnson family organization",
    "status": "Active"
  }'

# Get all families
curl -X POST https://your-site.com/api/method/dartwing.api.family.get_all_families \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {"status": "Active"},
    "limit_page_length": 10
  }'

# Search families
curl -X POST https://your-site.com/api/method/dartwing.api.family.search_families \
  -H "Authorization: token your-api-key:your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Johnson",
    "limit": 5
  }'
```

### Using Python (frappe.client)

```python
import frappe

# Create a family
result = frappe.call(
    "dartwing.api.family.create_family",
    organization_name="Johnson Family",
    organization_type="Family",
    description="Johnson family organization",
    status="Active"
)

# Get all families
families = frappe.call(
    "dartwing.api.family.get_all_families",
    filters={"status": "Active"},
    limit_page_length=10
)

# Search families
results = frappe.call(
    "dartwing.api.family.search_families",
    query="Johnson",
    limit=5
)
```

### Using JavaScript (Frappe Frontend)

```javascript
// Create a family
frappe.call({
    method: 'dartwing.api.family.create_family',
    args: {
        organization_name: 'Johnson Family',
        organization_type: 'Family',
        description: 'Johnson family organization',
        status: 'Active'
    },
    callback: function(r) {
        if (r.message.success) {
            console.log('Created:', r.message.data);
        }
    }
});

// Get all families
frappe.call({
    method: 'dartwing.api.family.get_all_families',
    args: {
        filters: JSON.stringify({status: 'Active'}),
        limit_page_length: 10
    },
    callback: function(r) {
        if (r.message.success) {
            console.log('Families:', r.message.data);
        }
    }
});
```

## Error Handling

All endpoints follow a consistent error handling pattern:

**Success Response:**
```json
{
  "success": true,
  "message": "...",
  "data": {...}
}
```

**Error Response:**
Frappe will throw an exception that returns:
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

## Development

### Module Structure

```
dartwing/
├── __init__.py
├── hooks.py                    # Frappe app hooks
├── modules.txt                 # Registered modules
├── patches.txt                 # Database patches
├── api/
│   ├── __init__.py
│   └── family.py              # Family API endpoints
├── config/
│   └── __init__.py
├── doctype/
│   └── family/
│       ├── __init__.py
│       ├── family.json        # DocType definition
│       └── family.py          # Document controller
└── public/                    # Static assets (empty)
```

### Testing

Test the API using Frappe's test framework or manually via:

```bash
# Using bench console
bench --site your-site.localhost console

# Then in Python console
frappe.call('dartwing.api.family.create_family', 
            organization_name='Test Family')
```

## License

Apache 2.0 - See [LICENSE](./LICENSE) for details.

## Support

- GitHub: [opensoft/frappe-app-dartwing](https://github.com/opensoft/frappe-app-dartwing)
- Issues: [GitHub Issues](https://github.com/opensoft/frappe-app-dartwing/issues)
