# Research: Organization Bidirectional Hooks

**Feature**: 004-org-bidirectional-hooks
**Date**: 2025-12-13

## Overview

This document captures research findings for implementing bidirectional hooks between Organization and concrete type doctypes in Frappe.

---

## 1. Frappe Document Hooks

### Decision
Use `after_insert` hook for concrete type creation and `on_trash` hook for cascade deletion.

### Rationale
- `after_insert` fires after the document is committed to the database, ensuring the Organization record exists before creating the concrete type
- `on_trash` fires before deletion, allowing cascade delete of the concrete type before Organization removal
- These hooks are part of Frappe's standard document lifecycle and are well-tested

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| `before_insert` | Organization doesn't have a `name` yet, cannot link concrete type |
| `validate` | Runs before save, same issue as before_insert |
| `on_update` | Would fire on every update, not just creation |
| Database triggers | Bypasses Frappe's permission system and logging |

### Implementation Pattern
```python
# hooks.py registration
doc_events = {
    "Organization": {
        "after_insert": "dartwing_core.doctype.organization.organization.create_concrete_type",
        "on_trash": "dartwing_core.doctype.organization.organization.delete_concrete_type"
    }
}
```

---

## 2. Org Type to Doctype Mapping

### Decision
Use a static dictionary mapping `org_type` Select values to concrete doctype names.

### Rationale
- Simple, explicit, and easy to validate
- No runtime lookup overhead
- Easy to extend when adding new org types
- Type safety through explicit mapping

### Implementation Pattern
```python
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Nonprofit": "Nonprofit",
    "Association": "Association"
}
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Dynamic lookup via doctype metadata | Adds complexity, runtime overhead |
| Convention-based (org_type == doctype) | Fragile if naming conventions change |
| Configuration file | Over-engineered for static mapping |

---

## 3. Atomic Transaction Handling

### Decision
Rely on Frappe's implicit transaction management within hook execution context.

### Rationale
- Frappe wraps document operations in database transactions automatically
- If concrete type creation fails, the entire transaction (including Organization insert) rolls back
- No explicit transaction management code needed
- Consistent with Frappe patterns

### Implementation Pattern
```python
def create_concrete_type(doc, method):
    concrete = frappe.new_doc(ORG_TYPE_MAP[doc.org_type])
    concrete.organization = doc.name
    concrete.flags.ignore_permissions = True
    concrete.insert()  # Fails here = entire transaction rolls back

    doc.db_set("linked_doctype", concrete.doctype, update_modified=False)
    doc.db_set("linked_name", concrete.name, update_modified=False)
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Explicit `frappe.db.begin()`/`commit()` | Interferes with Frappe's transaction management |
| Two-phase commit | Over-engineered for single-database operation |
| Eventual consistency with background job | Adds complexity, harder to test, violates atomicity requirement |

---

## 4. System Privilege Execution

### Decision
Use `flags.ignore_permissions = True` on concrete type document operations.

### Rationale
- User already has permission to create Organization (the trigger)
- Concrete type creation is an internal system operation, not user-initiated
- Prevents confusing permission errors when user lacks explicit permission on concrete type
- Aligns with clarification decision from spec

### Implementation Pattern
```python
concrete.flags.ignore_permissions = True
concrete.insert()

# For deletion
frappe.delete_doc(
    doc.linked_doctype,
    doc.linked_name,
    force=True,
    ignore_permissions=True
)
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Run as Administrator user | Adds complexity, audit trail confusion |
| Require user permissions on all types | Poor UX, permission error messages confusing |
| Custom permission check | Over-engineered for system operation |

---

## 5. Audit Logging Strategy

### Decision
Use `frappe.logger()` with structured log messages for hook execution audit trail.

### Rationale
- Built into Frappe framework
- Configurable log levels and destinations
- Can be forwarded to external logging systems
- Supports structured data for parsing

### Implementation Pattern
```python
import frappe
from frappe.utils.logger import get_logger

logger = get_logger("dartwing_core.hooks")

def create_concrete_type(doc, method):
    try:
        # ... creation logic ...
        logger.info(f"Created {concrete.doctype} {concrete.name} for Organization {doc.name}")
    except Exception as e:
        logger.error(f"Failed to create concrete type for Organization {doc.name}: {str(e)}")
        raise
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Custom audit doctype | Over-engineered for hook logging |
| Print statements | Not production-appropriate |
| External logging service direct | Adds dependency, network latency |

---

## 6. Org Type Immutability Enforcement

### Decision
Use Frappe's `set_only_once` field attribute plus server-side validation in `validate()` method.

### Rationale
- `set_only_once` provides UI-level protection in Frappe Desk
- Server-side validation catches API-based attempts to modify
- Defense in depth: both UI and API protected

### Implementation Pattern
```python
# In organization.json
{
    "fieldname": "org_type",
    "set_only_once": 1,
    ...
}

# In organization.py
def validate(self):
    if not self.is_new() and self.has_value_changed("org_type"):
        frappe.throw(_("Organization type cannot be changed after creation"))
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Only `set_only_once` | API can bypass UI attribute |
| Only server validation | Missing immediate UI feedback |
| Read-only field | Doesn't allow initial value setting |

---

## 7. API Method Design

### Decision
Provide two whitelisted methods: `get_concrete_doc()` and `get_organization_with_details()`.

### Rationale
- Separate methods for different use cases
- `get_concrete_doc()` for callers who only need concrete type data
- `get_organization_with_details()` for callers who need merged view
- Follows single responsibility principle

### Implementation Pattern
```python
@frappe.whitelist()
def get_concrete_doc(organization: str) -> dict:
    """Return just the concrete type document."""
    org = frappe.get_doc("Organization", organization)
    if not org.linked_doctype or not org.linked_name:
        return None
    return frappe.get_doc(org.linked_doctype, org.linked_name).as_dict()

@frappe.whitelist()
def get_organization_with_details(organization: str) -> dict:
    """Return Organization merged with concrete type fields."""
    org = frappe.get_doc("Organization", organization)
    result = org.as_dict()
    if org.linked_doctype and org.linked_name:
        concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
        result["concrete_type"] = concrete.as_dict()
    return result
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Single method with parameters | Adds complexity, harder to document |
| GraphQL | Not in current tech stack |
| Virtual fields on Organization | Frappe doesn't support computed nested objects |

---

## 8. Graceful Cascade Delete Handling

### Decision
Check for concrete type existence before attempting delete; proceed silently if not found.

### Rationale
- Prevents errors when data is already out of sync
- Allows manual cleanup without blocking Organization deletion
- Logs warning for visibility but doesn't fail operation

### Implementation Pattern
```python
def delete_concrete_type(doc, method):
    if doc.linked_doctype and doc.linked_name:
        if frappe.db.exists(doc.linked_doctype, doc.linked_name):
            frappe.delete_doc(
                doc.linked_doctype,
                doc.linked_name,
                force=True,
                ignore_permissions=True
            )
            logger.info(f"Cascade deleted {doc.linked_doctype} {doc.linked_name}")
        else:
            logger.warning(f"Concrete type {doc.linked_doctype} {doc.linked_name} not found during cascade delete")
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Throw error if not found | Blocks cleanup of inconsistent data |
| Always attempt delete | Generates unnecessary errors in logs |
| Background reconciliation only | Leaves orphaned Organizations |

---

## Summary of Decisions

| Area | Decision |
|------|----------|
| Hook Events | `after_insert` for create, `on_trash` for delete |
| Type Mapping | Static dictionary `ORG_TYPE_MAP` |
| Transactions | Rely on Frappe's implicit transaction management |
| Permissions | `ignore_permissions=True` for system operations |
| Logging | `frappe.logger()` with structured messages |
| Immutability | `set_only_once` + server-side validation |
| API Design | Two separate whitelisted methods |
| Error Handling | Graceful handling with logging |
