# Research: User Permission Propagation

**Feature**: 005-user-permission-propagation
**Date**: 2025-12-13

## 1. Frappe User Permission System

### Decision: Use Frappe's Built-in User Permission DocType

**Rationale**: Frappe provides a native `User Permission` doctype that enables row-level access control. This is the standard mechanism for restricting users to specific records.

**Alternatives Considered**:
- Custom permission table: Rejected - would bypass Frappe's permission system and require reimplementing list filtering
- Role-based only: Rejected - doesn't provide organization-level isolation

### User Permission Structure

```python
# Creating a User Permission
frappe.get_doc({
    "doctype": "User Permission",
    "user": "user@example.com",      # Frappe User email
    "allow": "Organization",          # DocType being restricted
    "for_value": "ORG-2025-00001",   # Specific record name
    "apply_to_all_doctypes": 0,      # Only apply to specified doctype
    "applicable_for": "Organization"  # Explicit application
}).insert(ignore_permissions=True)
```

### Key Behaviors

1. **Automatic Filtering**: When User Permission exists for a doctype, Frappe automatically filters list views
2. **Link Field Propagation**: Records with Link fields to a restricted doctype inherit the restriction
3. **Multiple Permissions**: User can have multiple User Permissions for same doctype (OR logic)

## 2. Permission Query Conditions Pattern

### Decision: Use `permission_query_conditions` Hook

**Rationale**: Frappe's `permission_query_conditions` hook is the standard way to add SQL WHERE conditions to list queries. This enables complex filtering logic beyond simple User Permissions.

**Pattern**:
```python
# hooks.py
permission_query_conditions = {
    "Organization": "dartwing.permissions.organization.get_permission_query_conditions",
    "Family": "dartwing.permissions.family.get_permission_query_conditions",
    "Company": "dartwing.permissions.company.get_permission_query_conditions",
    # ... etc
}

# dartwing/permissions/organization.py
def get_permission_query_conditions(user):
    """
    Returns SQL WHERE clause fragment for Organization list queries.
    Called automatically by Frappe for list views.
    """
    if "System Manager" in frappe.get_roles(user):
        return ""  # No restriction for System Manager

    # Get user's permitted organizations
    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"  # No access - return impossible condition

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabOrganization`.`name` IN ({org_list})"
```

### Concrete Type Pattern

For concrete types (Family, Company, etc.), filter by their `organization` Link field:

```python
# dartwing/permissions/family.py
def get_permission_query_conditions(user):
    if "System Manager" in frappe.get_roles(user):
        return ""

    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabFamily`.`organization` IN ({org_list})"
```

## 3. Has Permission Hook Pattern

### Decision: Use `has_permission` Hook

**Rationale**: The `has_permission` hook provides single-document access control, complementing the list-level `permission_query_conditions`.

**Pattern**:
```python
# hooks.py
has_permission = {
    "Organization": "dartwing.permissions.organization.has_permission",
    "Family": "dartwing.permissions.family.has_permission",
    # ... etc
}

# dartwing/permissions/organization.py
def has_permission(doc, ptype, user):
    """
    Check if user has permission to access specific Organization.
    Called for single document operations (read, write, etc).
    """
    if "System Manager" in frappe.get_roles(user):
        return True

    return frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Organization", "for_value": doc.name}
    )
```

## 4. Doc Events for Permission Propagation

### Decision: Use `doc_events` Hook on Org Member

**Rationale**: Permission creation/removal should trigger on Org Member lifecycle events. Using `doc_events` is the standard Frappe pattern.

**Pattern**:
```python
# hooks.py
doc_events = {
    "Org Member": {
        "after_insert": "dartwing.permissions.helpers.create_user_permissions",
        "on_trash": "dartwing.permissions.helpers.remove_user_permissions",
        "on_update": "dartwing.permissions.helpers.handle_status_change"
    }
}
```

### Implementation Logic

```python
# dartwing/permissions/helpers.py
import frappe

def create_user_permissions(doc, method):
    """Create User Permissions when Org Member is created."""
    # Get the Frappe User from Person
    user = frappe.db.get_value("Person", doc.person, "frappe_user")

    if not user:
        # Log skip event (FR-007, FR-012)
        log_permission_event("skip", doc, reason="Person has no linked Frappe User")
        return

    # Get Organization details
    org = frappe.get_doc("Organization", doc.organization)

    # Create permission for Organization
    create_permission(user, "Organization", doc.organization)
    log_permission_event("create", doc, user=user, doctype="Organization")

    # Create permission for concrete type if it exists
    if org.linked_doctype and org.linked_name:
        create_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event("create", doc, user=user, doctype=org.linked_doctype)

def remove_user_permissions(doc, method):
    """Remove User Permissions when Org Member is deleted."""
    user = frappe.db.get_value("Person", doc.person, "frappe_user")

    if not user:
        return  # Nothing to remove

    org = frappe.get_doc("Organization", doc.organization)

    # Remove permission for Organization
    delete_permission(user, "Organization", doc.organization)
    log_permission_event("remove", doc, user=user, doctype="Organization")

    # Remove permission for concrete type
    if org.linked_doctype and org.linked_name:
        delete_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event("remove", doc, user=user, doctype=org.linked_doctype)

def handle_status_change(doc, method):
    """Handle Org Member status changes (FR-009)."""
    if doc.has_value_changed("status"):
        if doc.status == "Inactive":
            remove_user_permissions(doc, method)
        elif doc.status == "Active" and doc.get_doc_before_save().status == "Inactive":
            create_user_permissions(doc, method)

def create_permission(user, allow, for_value):
    """Create a User Permission if it doesn't exist."""
    if not frappe.db.exists("User Permission", {
        "user": user,
        "allow": allow,
        "for_value": for_value
    }):
        frappe.get_doc({
            "doctype": "User Permission",
            "user": user,
            "allow": allow,
            "for_value": for_value,
            "apply_to_all_doctypes": 0
        }).insert(ignore_permissions=True)

def delete_permission(user, allow, for_value):
    """Delete a User Permission."""
    frappe.db.delete("User Permission", {
        "user": user,
        "allow": allow,
        "for_value": for_value
    })
```

## 5. Audit Logging Pattern

### Decision: Use Frappe's Built-in Logging with Custom Logger

**Rationale**: FR-012 requires logging all permission lifecycle events. Using `frappe.logger` provides structured logging that integrates with Frappe's log infrastructure.

**Pattern**:
```python
# dartwing/utils/permission_logger.py
import frappe
from frappe.utils import now_datetime

def get_permission_logger():
    return frappe.logger("permission_audit", allow_site=True)

def log_permission_event(event_type, org_member_doc, **kwargs):
    """
    Log permission lifecycle event for audit trail.

    Args:
        event_type: "create", "remove", or "skip"
        org_member_doc: The Org Member document triggering the event
        **kwargs: Additional context (user, doctype, reason)
    """
    logger = get_permission_logger()

    log_data = {
        "timestamp": str(now_datetime()),
        "event": event_type,
        "org_member": org_member_doc.name,
        "person": org_member_doc.person,
        "organization": org_member_doc.organization,
        **kwargs
    }

    logger.info(f"PERMISSION_{event_type.upper()}: {log_data}")
```

### Log Events Captured

| Event | Description | Additional Data |
|-------|-------------|-----------------|
| create | User Permission created | user, doctype, for_value |
| remove | User Permission removed | user, doctype, for_value |
| skip | Permission creation skipped | reason |

## 6. System Manager Bypass

### Decision: Check Roles Early in Permission Functions

**Rationale**: System Manager role should bypass all permission checks per FR-006. Checking early avoids unnecessary database queries.

**Pattern**:
```python
def get_permission_query_conditions(user):
    # Early exit for System Manager
    if "System Manager" in frappe.get_roles(user):
        return ""  # Empty string = no restriction

    # ... normal permission logic
```

## 7. Dartwing Admin Scope

### Decision: Admin Access via Org Member with Supervisor Role

Per clarification, Dartwing Admin scope is determined by Org Member records where the user has a supervisor/admin-level Role Template.

**Pattern**:
```python
def is_org_admin(user, organization):
    """Check if user is an admin for the given organization."""
    person = frappe.db.get_value("User", user, "person")
    if not person:
        return False

    return frappe.db.exists("Org Member", {
        "person": person,
        "organization": organization,
        "status": "Active",
        "role": ["in", get_admin_roles()]  # Roles with is_supervisor=1
    })

def get_admin_roles():
    """Get Role Templates that have is_supervisor=True."""
    return frappe.get_all(
        "Role Template",
        filters={"is_supervisor": 1},
        pluck="name"
    )
```

## 8. Duplicate Prevention (FR-008)

### Decision: Unique Constraint on Org Member

**Rationale**: FR-008 requires preventing duplicate Org Member records for same person + organization. This should be enforced at the DocType level.

**Implementation**: This is Feature 3's responsibility but should be documented here for reference:
```json
// org_member.json
{
  "unique_constraint": [
    ["person", "organization"]
  ]
}
```

Or in controller:
```python
def validate(self):
    if frappe.db.exists("Org Member", {
        "person": self.person,
        "organization": self.organization,
        "name": ["!=", self.name]
    }):
        frappe.throw(_("This person is already a member of this organization"))
```

## 9. Cascade Delete on Organization Deletion

### Decision: Remove Org Members and Permissions Before Organization Delete

**Rationale**: When an Organization is deleted, all associated Org Members should be removed, which will trigger permission cleanup through doc_events.

**Note**: This is handled by Organization's on_trash hook (Feature 4), which should:
1. Find all Org Members for the organization
2. Delete each Org Member (triggering permission removal via doc_events)
3. Then proceed with Organization deletion

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Permission Storage | Frappe User Permission | Native, automatic list filtering |
| List Filtering | permission_query_conditions hook | Standard Frappe pattern |
| Doc Access | has_permission hook | Standard Frappe pattern |
| Event Triggers | doc_events on Org Member | Clean separation, automatic |
| Logging | frappe.logger with custom module | Structured, integrated |
| Admin Bypass | Role check early in functions | Performance, clarity |
| Duplicate Prevention | Unique constraint on DocType | Database-level enforcement |
