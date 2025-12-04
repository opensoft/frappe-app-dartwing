# Dartwing Core - First 10 Features to Implement

**Purpose:** Prioritized implementation order for core features to build a functional foundation.

**Date:** December 1, 2025

---

## Current State

**Already Implemented:**
- Organization DocType (basic shell)
- Family DocType (basic)
- Family Member DocType (child table)

**Not Yet Implemented:**
- Person DocType
- Org Member DocType
- Role Template DocType
- Organization hooks (bidirectional linking)
- Permission system
- Keycloak integration

---

## Priority Order

### Feature 1: Person DocType

**Priority:** P1 - CRITICAL (Foundation)
**Blocks:** Org Member, Employment Record, Family Relationship, all user flows
**Architecture Reference:** `docs/dartwing_core/person_doctype_contract.md`

**Why First:**
- Person is the identity layer - every user interaction requires it
- Org Member links Person to Organization
- Cannot implement permissions without Person → User linkage

**Required Fields:**
```
- primary_email (Data, reqd, unique)
- keycloak_user_id (Data, unique, nullable)
- frappe_user (Link → User, unique when set)
- first_name, last_name (Data)
- mobile_no (Data, optional)
- personal_org (Link → Organization)
- is_minor (Check)
- consent_captured (Check)
- consent_timestamp (Datetime)
- source (Select: signup/invite/import)
- status (Select: Active/Inactive/Merged)
```

**Acceptance Criteria:**
- [ ] DocType JSON created with all required fields
- [ ] Uniqueness constraints enforced (email, keycloak_id, frappe_user)
- [ ] Deletion prevented when linked to Org Member
- [ ] Basic tests for duplicate email rejection

---

### Feature 2: Role Template DocType

**Priority:** P1 - CRITICAL (Foundation)
**Blocks:** Org Member (needs role reference)
**Architecture Reference:** Section 3.7

**Why Second:**
- Org Member requires a role assignment
- Roles are org-type specific (Family vs Company roles differ)
- Enables conditional field visibility based on role

**Required Fields:**
```
- role_name (Data, reqd, unique)
- applies_to_org_type (Select: Family/Company/Nonprofit/Association)
- is_supervisor (Check)
- default_hourly_rate (Currency, depends_on Company)
```

**Seed Data Required:**
```
Family: Parent, Child, Guardian, Extended Family
Company: Owner, Manager, Employee, Contractor
Nonprofit: Board Member, Volunteer, Staff
Association: President, Member, Honorary
```

**Acceptance Criteria:**
- [ ] DocType JSON created
- [ ] Seed data fixtures created
- [ ] Roles filtered by org_type in UI

---

### Feature 3: Org Member DocType

**Priority:** P1 - CRITICAL (Foundation)
**Depends On:** Person, Role Template, Organization
**Blocks:** Permission propagation, all org-specific features
**Architecture Reference:** Section 3.8

**Why Third:**
- Links Person to Organization with a role
- Required for any multi-user functionality
- Permission system depends on Org Member

**Required Fields:**
```
- person (Link → Person, reqd)
- organization (Link → Organization, reqd)
- role (Link → Role Template, reqd)
- start_date (Date, default: Today)
- end_date (Date)
- status (Select: Active/Inactive/Pending)
```

**Acceptance Criteria:**
- [ ] DocType JSON created
- [ ] Unique constraint: (person, organization) pair
- [ ] Role filtered by org_type of linked organization
- [ ] Status workflow (Pending → Active → Inactive)

---

### Feature 4: Organization Bidirectional Hooks

**Priority:** P1 - CRITICAL (Foundation)
**Depends On:** Organization, Family (existing)
**Architecture Reference:** Section 3.6

**Why Fourth:**
- Ensures Organization ↔ Concrete Type integrity
- Auto-creates concrete type when Organization is created
- Cascades delete to concrete type

**Implementation:**
```python
# dartwing_core/doctype/organization/organization.py
def after_insert(doc):
    """Create concrete type based on org_type."""

def on_trash(doc):
    """Cascade delete to concrete type."""
```

**Acceptance Criteria:**
- [ ] Creating Organization auto-creates Family/Company/etc
- [ ] linked_doctype and linked_name populated automatically
- [ ] Deleting Organization cascades to concrete type
- [ ] get_concrete_doc() API helper works

---

### Feature 5: User Permission Propagation

**Priority:** P1 - CRITICAL (Security)
**Depends On:** Person, Org Member, Organization
**Architecture Reference:** `person_doctype_contract.md` - Permission Propagation

**Why Fifth:**
- Security foundation - users should only see their org's data
- Multi-org users need scoped access
- Required before any real user testing

**Implementation:**
```python
# On Org Member creation:
# 1. Create User Permission for Organization
# 2. Create User Permission for concrete type (Family/Company)
# 3. On Org Member deletion, remove User Permissions
```

**Acceptance Criteria:**
- [ ] Creating Org Member creates User Permission
- [ ] User can only see Organizations they belong to
- [ ] List views filtered by User Permission
- [ ] Permission helper functions in dartwing_core/permissions/

---

### Feature 6: Company DocType (Concrete Type)

**Priority:** P2 - HIGH (Core Feature)
**Depends On:** Organization hooks working
**Architecture Reference:** Section 3.4

**Why Sixth:**
- Family already exists, Company is next most common org type
- Required for B2B use cases
- Has more complex fields (tax_id, entity_type, jurisdiction)

**Required Fields:**
```
- organization (Link → Organization, reqd, read_only)
- entity_type (Select: LLC/Corporation/Partnership/Sole Prop)
- tax_id (Data)
- jurisdiction (Data)
- officers (Table → Organization Officer)
- partners (Table → Organization Member Partner)
```

**Acceptance Criteria:**
- [ ] DocType JSON created in dartwing_company module
- [ ] Auto-created when Organization with org_type=Company is made
- [ ] Bidirectional link maintained
- [ ] OrganizationMixin inherited

---

### Feature 7: Equipment DocType

**Priority:** P2 - HIGH (Core Feature)
**Depends On:** Organization
**Architecture Reference:** Section 3.5

**Why Seventh:**
- Required for asset management across all org types
- Simple enough to implement quickly
- Demonstrates polymorphic Organization pattern

**Required Fields:**
```
- equipment_name (Data, reqd)
- organization (Link → Organization, reqd)
- equipment_type (Select: Vehicle/Electronics/Furniture/etc)
- serial_number (Data)
- status (Select: Active/In Repair/Retired)
- documents (Table → Equipment Document)
- maintenance (Table → Equipment Maintenance)
```

**Acceptance Criteria:**
- [ ] DocType JSON with child tables
- [ ] Linked to Organization (polymorphic)
- [ ] Filtered by User Permission

---

### Feature 8: OrganizationMixin Base Class

**Priority:** P2 - HIGH (Code Quality)
**Depends On:** Organization, Family, Company
**Architecture Reference:** Section 3.6

**Why Eighth:**
- Reduces code duplication across concrete types
- Provides consistent API for accessing parent Organization
- Should be implemented before more concrete types added

**Implementation:**
```python
# dartwing_core/mixins/organization_mixin.py
class OrganizationMixin:
    @property
    def org_name(self): ...
    @property
    def logo(self): ...
    @property
    def org_status(self): ...
    def get_organization_doc(self): ...
    def update_org_name(self, new_name): ...
```

**Acceptance Criteria:**
- [ ] Mixin class created
- [ ] Family controller inherits mixin
- [ ] Company controller inherits mixin
- [ ] Properties work correctly

---

### Feature 9: API Helpers (Whitelisted Methods)

**Priority:** P2 - HIGH (Flutter Integration)
**Depends On:** All core DocTypes
**Architecture Reference:** Section 3.6, 10.2

**Why Ninth:**
- Flutter client needs clean API endpoints
- Cannot build mobile app without these
- Standardizes data access patterns

**Required Methods:**
```python
@frappe.whitelist()
def get_concrete_doc(organization: str) -> dict

@frappe.whitelist()
def get_organization_with_details(organization: str) -> dict

@frappe.whitelist()
def get_user_organizations() -> list

@frappe.whitelist()
def get_org_members(organization: str) -> list
```

**Acceptance Criteria:**
- [ ] All methods implemented and tested
- [ ] Permissions enforced in each method
- [ ] Response format documented

---

### Feature 10: Basic Test Suite

**Priority:** P2 - HIGH (Quality)
**Depends On:** All above features
**Architecture Reference:** AGENTS.md testing guidelines

**Why Tenth:**
- Validates all features work together
- Catches regressions early
- Required before any deployment

**Required Tests:**
```python
# tests/test_person.py
- test_duplicate_email_rejected
- test_person_creates_frappe_user (when configured)

# tests/test_organization.py
- test_organization_creates_concrete_type
- test_cascade_delete_to_concrete

# tests/test_org_member.py
- test_org_member_creates_user_permission
- test_role_filtered_by_org_type

# tests/test_permissions.py
- test_user_sees_only_own_orgs
- test_list_view_filtering
```

**Acceptance Criteria:**
- [ ] All tests passing
- [ ] Test coverage for core flows
- [ ] CI integration ready

---

## Implementation Order Summary

| Order | Feature | Priority | Est. Effort | Depends On |
|-------|---------|----------|-------------|------------|
| 1 | Person DocType | P1 | 1 day | None |
| 2 | Role Template DocType | P1 | 0.5 day | None |
| 3 | Org Member DocType | P1 | 1 day | Person, Role Template |
| 4 | Organization Hooks | P1 | 0.5 day | Organization |
| 5 | User Permission Propagation | P1 | 1 day | Person, Org Member |
| 6 | Company DocType | P2 | 1 day | Org Hooks |
| 7 | Equipment DocType | P2 | 0.5 day | Organization |
| 8 | OrganizationMixin | P2 | 0.5 day | Family, Company |
| 9 | API Helpers | P2 | 1 day | All DocTypes |
| 10 | Basic Test Suite | P2 | 1.5 days | All Features |

**Total Estimated Effort:** ~8.5 days

---

## Dependencies Diagram

```
                    ┌──────────────────┐
                    │   Role Template  │
                    │     (Feature 2)  │
                    └────────┬─────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│      Person      │─────────┼────────▶│    Org Member    │
│   (Feature 1)    │         │         │   (Feature 3)    │
└──────────────────┘         │         └────────┬─────────┘
                             │                  │
                    ┌────────▼─────────┐        │
                    │   Organization   │        │
                    │    (existing)    │        │
                    └────────┬─────────┘        │
                             │                  │
              ┌──────────────┼──────────────┐   │
              ▼              ▼              ▼   ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────────┐
        │  Family  │  │ Company  │  │ User Permissions │
        │(existing)│  │(Feature 6)│  │   (Feature 5)    │
        └──────────┘  └──────────┘  └──────────────────┘
```

---

## Next Steps After These 10

After completing these foundational features:

1. **Keycloak Integration** - SSO and OAuth2 flows
2. **Family Relationship DocType** - Family-specific relationships
3. **Employment Record DocType** - Company-specific employment
4. **Socket.IO Real-time Sync** - Live updates
5. **Flutter Client Scaffolding** - Mobile app foundation
