# Business Logic Guide

This document explains where to place business logic in the Dartwing Frappe app.

## Overview

Business logic in Frappe apps is organized by purpose and scope, not centralized in one location. This guide helps you determine where to put your code.

## Decision Tree

```
Is it document-level logic (validation, calculations)?
├─ YES → DocType Controller (dartwing/doctype/<name>/<name>.py)
└─ NO  → Is it an external API endpoint?
         ├─ YES → API Module (dartwing/api/<module>.py)
         └─ NO  → Is it reusable across multiple DocTypes?
                  ├─ YES → Utils Module (dartwing/utils/<module>.py)
                  └─ NO  → Is it background processing?
                           ├─ YES → Tasks Module (dartwing/tasks.py)
                           └─ NO  → Custom module in dartwing/<name>.py
```

## 1. DocType Controllers

**Location:** `dartwing/doctype/<doctype_name>/<doctype_name>.py`

**Purpose:** Business logic specific to a DocType (document/database model)

**Use for:**
- Field validation
- Auto-calculations
- Status transitions
- Permissions checks
- Related document creation/updates
- Business rules enforcement

### Example: `dartwing/doctype/family/family.py`

```python
import frappe
from frappe.model.document import Document

class Family(Document):
    """Family Organization Document"""
    
    # VALIDATION - Before save
    def validate(self):
        """Called before every save"""
        self.validate_organization_name()
        self.calculate_member_count()
        
    def validate_organization_name(self):
        """Business rule: Organization name must be unique"""
        if not self.organization_name:
            frappe.throw("Organization Name is required")
            
    # AUTO-CALCULATION
    def calculate_member_count(self):
        """Auto-calculate number of members"""
        self.member_count = frappe.db.count("Family Member", {
            "family": self.name
        })
    
    # LIFECYCLE HOOKS
    def before_insert(self):
        """Called before creating a new document"""
        if not self.created_date:
            self.created_date = frappe.utils.today()
            
    def after_insert(self):
        """Called after creating a new document"""
        self.create_default_roles()
        
    def on_update(self):
        """Called after updating the document"""
        self.notify_members_of_change()
        
    def before_submit(self):
        """Called before submitting (if submittable)"""
        self.validate_ready_for_submission()
        
    def on_submit(self):
        """Called after submission"""
        self.lock_for_editing()
        
    def on_cancel(self):
        """Called when canceling a submitted document"""
        self.reverse_submissions()
        
    def on_trash(self):
        """Called before deleting"""
        self.cleanup_related_records()
        
    # CUSTOM METHODS
    def create_default_roles(self):
        """Custom business logic"""
        # Create admin role for creator
        pass
        
    def notify_members_of_change(self):
        """Send notifications"""
        pass
```

### Available Lifecycle Hooks

| Hook | When Called | Use For |
|------|-------------|---------|
| `validate()` | Before every save | Validation, calculations |
| `before_insert()` | Before creating new | Set defaults, generate IDs |
| `after_insert()` | After creating new | Create related docs, notifications |
| `before_save()` | Before insert or update | Common save logic |
| `after_save()` | After insert or update | Post-save actions |
| `on_update()` | After update | Update related docs |
| `before_submit()` | Before submission | Final validation |
| `on_submit()` | After submission | Lock, create GL entries |
| `on_cancel()` | On cancellation | Reverse transactions |
| `before_rename()` | Before renaming | Validation |
| `after_rename()` | After renaming | Update references |
| `on_trash()` | Before deletion | Cleanup |
| `after_delete()` | After deletion | Final cleanup |

## 2. API Modules

**Location:** `dartwing/api/<module>.py`

**Purpose:** REST API endpoints and external integrations

**Use for:**
- HTTP API endpoints
- External service integrations
- Stateless operations
- Batch operations
- Search/query endpoints

### Example: `dartwing/api/family.py`

```python
import frappe
from frappe import _

@frappe.whitelist()
def create_family(organization_name, organization_type="Family"):
    """
    API endpoint to create a family
    Accessible at: /api/method/dartwing.api.family.create_family
    """
    # Validation
    if not organization_name:
        frappe.throw(_("Organization Name is required"))
    
    # Business logic
    family = frappe.get_doc({
        "doctype": "Family",
        "organization_name": organization_name,
        "organization_type": organization_type
    })
    family.insert()
    
    return {
        "success": True,
        "data": family.as_dict()
    }

@frappe.whitelist()
def bulk_update_status(family_names, new_status):
    """Batch operation"""
    for name in family_names:
        doc = frappe.get_doc("Family", name)
        doc.status = new_status
        doc.save()
    
    frappe.db.commit()
    return {"success": True, "updated": len(family_names)}
```

## 3. Utils Modules

**Location:** `dartwing/utils/<module>.py`

**Purpose:** Reusable business logic not tied to specific DocTypes

**Use for:**
- Validation functions
- Data transformations
- Calculations
- External service clients
- Common business rules
- Helper functions

### Example: `dartwing/utils/validation.py`

```python
import frappe
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        frappe.throw(f"Invalid email: {email}")
    return True

def validate_phone(phone):
    """Validate phone number"""
    # Business logic
    pass

def check_duplicate(doctype, field, value, exclude=None):
    """Check for duplicate values"""
    filters = {field: value}
    if exclude:
        filters["name"] = ["!=", exclude]
    
    if frappe.db.exists(doctype, filters):
        frappe.throw(f"Duplicate {field}: {value}")
    return False
```

### Example: `dartwing/utils/notifications.py`

```python
import frappe

def send_family_notification(family_name, message):
    """Send notification to all family members"""
    members = frappe.get_all("Family Member", 
        filters={"family": family_name},
        fields=["email"]
    )
    
    for member in members:
        frappe.sendmail(
            recipients=[member.email],
            subject=f"Update for {family_name}",
            message=message
        )

def send_sms(phone, message):
    """Send SMS via external service"""
    # Integration with SMS service
    pass
```

### Example: `dartwing/utils/calculations.py`

```python
def calculate_age(birth_date):
    """Calculate age from birth date"""
    from datetime import date
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

def calculate_family_size(family_name):
    """Calculate total family size"""
    return frappe.db.count("Family Member", {"family": family_name})
```

## 4. Tasks Module

**Location:** `dartwing/tasks.py`

**Purpose:** Background jobs and scheduled tasks

**Use for:**
- Scheduled tasks (hourly, daily, weekly)
- Long-running operations
- Batch processing
- Cleanup jobs
- Data synchronization

### Example: `dartwing/tasks.py`

```python
import frappe
from frappe.utils import now_datetime, add_days

def daily_cleanup():
    """Run daily cleanup tasks"""
    cleanup_expired_sessions()
    send_reminder_emails()

def cleanup_expired_sessions():
    """Delete old sessions"""
    threshold = add_days(now_datetime(), -30)
    frappe.db.delete("Session", {
        "created": ["<", threshold]
    })

def send_reminder_emails():
    """Send reminder emails to families"""
    families = frappe.get_all("Family", 
        filters={"status": "Active"},
        fields=["name", "organization_name"]
    )
    
    for family in families:
        # Send reminder
        pass

def hourly_sync():
    """Sync data every hour"""
    pass
```

**Register in hooks.py:**
```python
scheduler_events = {
    "daily": [
        "dartwing.tasks.daily_cleanup"
    ],
    "hourly": [
        "dartwing.tasks.hourly_sync"
    ]
}
```

## 5. Custom Modules

**Location:** `dartwing/<module_name>.py` or `dartwing/<domain>/<module>.py`

**Purpose:** Domain-specific business logic modules

**Use for:**
- Payment processing
- Report generation
- Complex calculations
- External integrations
- Domain models

### Example: `dartwing/payments.py`

```python
import frappe

def process_payment(family_name, amount, payment_method):
    """Process family payment"""
    # Validate
    family = frappe.get_doc("Family", family_name)
    if family.status != "Active":
        frappe.throw("Cannot process payment for inactive family")
    
    # Create payment record
    payment = frappe.get_doc({
        "doctype": "Family Payment",
        "family": family_name,
        "amount": amount,
        "payment_method": payment_method,
        "status": "Pending"
    })
    payment.insert()
    
    # Process with payment gateway
    result = charge_payment_gateway(amount, payment_method)
    
    if result.success:
        payment.status = "Completed"
        payment.transaction_id = result.transaction_id
        payment.save()
    
    return payment

def charge_payment_gateway(amount, method):
    """External payment gateway integration"""
    # API call to payment provider
    pass
```

## 6. Reports

**Location:** `dartwing/report/<report_name>/` (created via bench)

**Purpose:** Custom reports with business logic

### Create Report:
```bash
bench --site mysite new-report "Family Statistics"
```

### Example: `dartwing/report/family_statistics/family_statistics.py`

```python
import frappe

def execute(filters=None):
    """Report business logic"""
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Family", "fieldname": "family", "width": 200},
        {"label": "Members", "fieldname": "members", "width": 100},
        {"label": "Status", "fieldname": "status", "width": 100}
    ]

def get_data(filters):
    # Business logic to fetch and calculate data
    return frappe.db.sql("""
        SELECT 
            name as family,
            member_count as members,
            status
        FROM `tabFamily`
        WHERE status = %(status)s
    """, filters, as_dict=1)
```

## Best Practices

### 1. Keep DocType Controllers Focused
✅ **DO:**
```python
class Family(Document):
    def validate(self):
        self.validate_name()
        self.calculate_totals()
```

❌ **DON'T:**
```python
class Family(Document):
    def validate(self):
        # Sending emails in validate is wrong
        self.send_welcome_email()  
```

### 2. Use Utils for Reusable Logic
✅ **DO:**
```python
# dartwing/utils/validation.py
def validate_email(email):
    # Reusable validation

# Use in multiple DocTypes
from dartwing.utils.validation import validate_email
```

❌ **DON'T:**
```python
# Copy-paste validation in every DocType
class Family(Document):
    def validate_email(self, email):
        # Duplicated code
```

### 3. Keep API Endpoints Thin
✅ **DO:**
```python
@frappe.whitelist()
def create_family(data):
    # Delegate to DocType
    family = frappe.get_doc({
        "doctype": "Family",
        **data
    })
    family.insert()
    return family
```

❌ **DON'T:**
```python
@frappe.whitelist()
def create_family(data):
    # Too much logic in API
    # Validation, calculation, etc.
    # This should be in DocType
```

### 4. Use Tasks for Background Work
✅ **DO:**
```python
# Run async
frappe.enqueue("dartwing.tasks.send_bulk_emails", 
               family_names=names)
```

❌ **DON'T:**
```python
# Block API response
for family in families:
    send_email(family)  # Slow!
```

## Summary

| Type | Location | Purpose | Example |
|------|----------|---------|---------|
| **Document Logic** | `doctype/<name>/<name>.py` | Validation, lifecycle | Family.validate() |
| **API Endpoints** | `api/<module>.py` | External access | create_family() |
| **Reusable Utils** | `utils/<module>.py` | Shared functions | validate_email() |
| **Background Jobs** | `tasks.py` | Scheduled tasks | daily_cleanup() |
| **Custom Modules** | `<module>.py` | Domain logic | process_payment() |
| **Reports** | `report/<name>/` | Custom reports | family_statistics |

## Quick Reference

**I need to...**

- **Validate a field** → DocType Controller `validate()`
- **Calculate a value** → DocType Controller `validate()`
- **Create related docs** → DocType Controller `after_insert()`
- **Expose API endpoint** → `api/<module>.py`
- **Reusable validation** → `utils/validation.py`
- **Send notifications** → `utils/notifications.py`
- **Process payments** → Custom module `payments.py`
- **Schedule daily job** → `tasks.py` + hooks.py
- **Generate report** → `report/<name>/`

## Resources

- [Frappe Controller Hooks](https://frappeframework.com/docs/user/en/api/document)
- [Whitelisted Methods](https://frappeframework.com/docs/user/en/api/rest)
- [Background Jobs](https://frappeframework.com/docs/user/en/api/background-jobs)

## License

Apache 2.0 - See [LICENSE](./LICENSE)
