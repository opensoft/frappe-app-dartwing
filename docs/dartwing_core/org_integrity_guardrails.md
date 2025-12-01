# Organization Integrity Guardrails

**Objective:** Prevent org_type drift, ensure concrete creation is atomic, and provide healing for orphaned Organizations.

## Guardrail 1: org_type Immutability
- Block changes to `org_type` after insert.
- Implementation (controller validate):
  - If `not self.is_new()` and `self.has_value_changed("org_type")`: `frappe.throw("Organization type cannot be changed after creation")`.
- Tests:
  - Attempt to change `org_type` → expect ValidationError.
  - Fresh insert with valid `org_type` → passes.

## Guardrail 2: Atomic Concrete Creation
- Create concrete record before setting forward refs; only set `linked_doctype`/`linked_name` after successful insert.
- Recommended flow:
  - Use `before_insert` to determine `ORG_TYPE_MAP` target.
  - In `after_insert`, wrap creation in try/except; on failure, roll back and throw to prevent dangling Organizations.
  - Mark creation idempotent: if `linked_doctype`/`linked_name` already set, skip.
- Retry strategy:
  - On transient DB errors, retry once with backoff; otherwise bubble up.

### Pseudocode
```python
ORG_TYPE_MAP = {...}

def validate(self):
    if not self.is_new() and self.has_value_changed("org_type"):
        frappe.throw("Organization type cannot be changed after creation")
    if self.org_type not in ORG_TYPE_MAP:
        frappe.throw(f"Invalid org_type: {self.org_type}")

def after_insert(self):
    if self.linked_doctype and self.linked_name:
        return  # idempotent
    concrete_doctype = ORG_TYPE_MAP[self.org_type]
    try:
        concrete = frappe.new_doc(concrete_doctype)
        concrete.organization = self.name
        concrete.flags.ignore_permissions = True
        concrete.insert()
        self.db_set("linked_doctype", concrete_doctype, update_modified=False)
        self.db_set("linked_name", concrete.name, update_modified=False)
    except Exception:
        frappe.db.rollback()
        frappe.throw("Failed to create concrete record; Organization not saved.")
```

## Guardrail 3: Reconciliation Job
- Daily scheduled job to heal missing concrete links.
- Steps:
  - Query Organizations where `linked_doctype`/`linked_name` is null.
  - For each, validate `org_type` and create missing concrete as above.
  - Log successes/failures; emit site log or email alert.
- CLI patch helper:
  - `bench execute dartwing_core.organization_repair.heal_missing_concretes`

## Documentation & Ops
- Document behavior in `dartwing_core_arch.md` and release notes.
- Provide a short runbook: how to rerun reconciliation, how to diagnose org_type change attempts, and where errors surface (Error Log).
