# Dartwing Framework

**Architecture & Product Requirements Document**

Version 1.0 | November 2025

_A Flutter + Frappe Low-Code Application Framework_

---

## Table of Contents

1. Executive Summary
2. Architecture Overview
3. Core Data Model
4. Flutter Client Architecture
5. Authentication Architecture
6. AI Persona Architecture
7. Modular Application Architecture
8. Security Architecture
9. Implementation Roadmap
10. Technical Specifications
11. Advanced Features & Operations
12. Developer Ecosystem

- Appendix A: Doctype JSON Reference
- Appendix B: Flutter Package Dependencies
- Appendix C: Glossary

---

## Documentation Structure

### Context Hierarchy (Read in this order)

1. **Always read**: `docs/README.md`, `docs/architecture.md`, `docs/overview.md` (project-wide)
2. **Current context**: When working on specific modules, also read `docs/[module-name]/` and submodules
3. **Full scan**: `docs/**/*.md` (all docs when comprehensive understanding needed)

### Instructions for Agents

- Start with project root docs for architecture understanding
- When given module name (ex: "dartwing_core"), prioritize `docs/dartwing_core/` + root docs
- Reference specific docs paths in responses: `[docs/dartwing_core/organization.md]`
- For Flutter work, also read `lib/README.md` if present
- For Frappe doctypes, check `docs/doctypes/` for field definitions

### Repository Structure

```
dartwing/
├── docs/
│   ├── README.md              # Project overview
│   ├── architecture.md        # This document
│   ├── overview.md            # High-level system overview
│   ├── dartwing_core/         # Core module docs
│   │   ├── organization.md
│   │   ├── person.md
│   │   └── equipment.md
│   ├── dartwing_hr/           # HR module docs
│   ├── dartwing_family/       # Family module docs
│   ├── dartwing_comms/        # Communications module docs
│   ├── dartwing_ai/           # AI module docs
│   ├── dartwing_fax/          # Fax module docs
│   └── doctypes/              # Doctype field definitions
├── dartwing_core/             # Frappe app: core doctypes
├── dartwing_flutter/          # Flutter monorepo
│   ├── lib/
│   │   ├── README.md          # Flutter architecture
│   │   ├── core/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   └── services/
│   └── pubspec.yaml
├── constitution.md            # Project principles (for spec-kit)
└── .specify/                  # spec-kit artifacts (if using)
    └── specs/
```

---

## 1. Executive Summary

Dartwing is a comprehensive application framework combining Flutter for cross-platform mobile/web/desktop frontends with Frappe as the backend, enabling rapid low-code development of business applications. The framework provides a unified data model, AI-powered personas, and seamless integration across all platforms.

### 1.1 Vision Statement

One framework. Every platform. Any organization type. Dartwing eliminates the need for separate CRM, HRIS, family-management, church-management, HOA, and club-membership systems by providing a single, unified architecture that adapts to any organizational structure.

### 1.2 Key Differentiators

- **Universal Organization Model:** Hybrid architecture with unified identity layer and type-specific concrete implementations
- **Cross-Platform Native:** Flutter provides true native performance on iOS, Android, Web, and Desktop
- **AI-First Design:** Built-in AI personas for sales, support, and automation
- **Low-Code Development:** Frappe's doctype system enables rapid app building
- **Multi-Tenant Architecture:** Supports B2B, B2C, and hybrid deployment models

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

Dartwing follows a three-tier architecture with clear separation between presentation, business logic, and data layers.

| Layer          | Technology              | Responsibility                               |
| -------------- | ----------------------- | -------------------------------------------- |
| Presentation   | Flutter (Dart)          | UI/UX, State Management, Platform Adaptation |
| API Gateway    | Frappe REST / Socket.IO | Authentication, Rate Limiting, Routing       |
| Business Logic | Frappe (Python)         | Workflows, Validations, Permissions          |
| Data Layer     | MariaDB / PostgreSQL    | Persistence, Transactions, Indexing          |
| Authentication | Keycloak                | SSO, OAuth2, OIDC, Realm Management          |

### 2.2 Client Architecture (Three Access Patterns)

Dartwing serves three distinct client types, all communicating through the **same REST API layer**:

| Client Type             | Technology                             | Communication Method                                    |
| ----------------------- | -------------------------------------- | ------------------------------------------------------- |
| **Flutter Apps**        | Flutter (Mobile, Desktop, Web)         | REST API (`/api/resource/`, `/api/method/`) + Socket.IO |
| **External Websites**   | Any framework (React, Vue, vanilla JS) | REST API (same endpoints)                               |
| **Frappe Builder Site** | Frappe Builder                         | `frappe.call()` → REST API internally                   |

[See `docs/dartwing_core/socket_io_scaling_spec.md` for Socket.IO horizontal scaling architecture with Redis pub/sub adapter.]

**API-First Principle:** All business logic MUST be exposed via `@frappe.whitelist()` decorated Python methods. This ensures:

- Flutter mobile/desktop apps can access all functionality
- Third-party websites can integrate via standard REST calls
- Frappe Builder pages use the same backend logic via `frappe.call()`
- No duplicate logic across client types

**Frappe Builder Note:** While Frappe Builder appears to be "internal," it actually uses `frappe.call()` which wraps HTTP requests to `/api/method/` endpoints. This means Frappe Builder websites consume the exact same API as external clients.

### 2.3 Component Diagram

The framework consists of these primary components:

- **DartwingFone:** Flutter mobile application for end users
- **Dartwing Web:** Flutter web application for browser access
- **Dartwing Desktop:** Flutter desktop apps (macOS, Windows, Linux)
- **Dartwing Core:** Frappe app containing core doctypes and business logic
- **Dartwing AI:** AI persona engine for sales, support, automation
- **Dartwing Sync:** Real-time synchronization service

---

## 3. Core Data Model

### 3.1 Hybrid Organization Model (Thin Reference + Concrete Types)

Dartwing uses a **Hybrid Architecture** to solve the "God Object" problem while maintaining the benefits of a unified `Organization` entity.

1.  **Organization (Thin Reference):** A lightweight shell that holds shared identity (Name, Logo, Status) and acts as the target for all foreign keys (Invoices, Tasks, Notes).
2.  **Concrete Types:** Separate 1:1 linked doctypes (`Family`, `Company`, `Club`, `Nonprofit`) that hold domain-specific data and validation logic.

| Doctype          | Role                    | Fields                                                      |
| :--------------- | :---------------------- | :---------------------------------------------------------- |
| **Organization** | Polymorphic Identity    | `name`, `org_type`, `logo`, `linked_doctype`, `linked_name` |
| **Family**       | Concrete Implementation | `nickname`, `residence`, `parental_controls`                |
| **Company**      | Concrete Implementation | `tax_id`, `entity_type`, `jurisdiction`                     |
| **Club**         | Concrete Implementation | `membership_tiers`, `dues`, `amenities`                     |
| **Nonprofit**    | Concrete Implementation | `tax_exempt_status`, `board_members`, `mission`             |

```
┌─────────────────────────────────────────────────────────────────┐
│                         Organization                             │
│  ┌───────────┬──────────┬────────┬─────────────────────────┐    │
│  │ org_name  │ org_type │ status │ linked_doctype/name     │    │
│  └───────────┴──────────┴────────┴─────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ 1:1 Link (maintained by hooks)
          ┌─────────────────┼─────────────────┬─────────────────┐
          ▼                 ▼                 ▼                 ▼
     ┌─────────┐      ┌──────────┐      ┌─────────┐      ┌───────────┐
     │ Family  │      │ Company  │      │  Club   │      │ Nonprofit │
     ├─────────┤      ├──────────┤      ├─────────┤      ├───────────┤
     │nickname │      │ tax_id   │      │ tiers[] │      │ 501c_type │
     │residence│      │ officers │      │ dues    │      │ board[]   │
     │         │      │ partners │      │         │      │ mission   │
     └─────────┘      └──────────┘      └─────────┘      └───────────┘
```

### 3.2 Implementation Pattern (Bidirectional Linking)

To ensure data integrity, we use Frappe server-side hooks to maintain the relationship:

- **Creation:** When an `Organization` is created, a hook automatically creates the corresponding Concrete Doctype (e.g., `Family`) and links them.
- **Linking:** The `Organization` record stores the `linked_doctype` and `linked_name` for easy retrieval.
- **Validation:** Concrete doctypes (e.g., `Payroll Run`) link directly to `Company` to enforce type safety. Generic doctypes (e.g., `Task`) link to `Organization` for polymorphism.

### 3.3 Organization Doctype JSON (Thin Shell)

```json
{
  "doctype": "Organization",
  "name": "Organization",
  "module": "Dartwing Core",
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "ORG-.YYYY.-",
      "default": "ORG-.YYYY.-",
      "hidden": 1
    },
    {
      "fieldname": "org_name",
      "label": "Organization Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "org_type",
      "label": "Organization Type",
      "fieldtype": "Select",
      "reqd": 1,
      "set_only_once": 1,
      "options": "Family\nCompany\nNonprofit\nClub/Association"
    },
    { "fieldname": "logo", "label": "Logo", "fieldtype": "Attach Image" },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "default": "Active",
      "options": "Active\nInactive\nDissolved"
    },
    {
      "fieldname": "section_link",
      "fieldtype": "Section Break",
      "label": "Concrete Implementation"
    },
    {
      "fieldname": "linked_doctype",
      "label": "Linked Doctype",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "linked_name",
      "label": "Linked Name",
      "fieldtype": "Data",
      "read_only": 1
    }
  ]
}
```

### 3.4 Concrete Doctype JSONs

#### Family (Concrete)

```json
{
  "doctype": "Family",
  "module": "Dartwing Family",
  "autoname": "FAM-.#####",
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "family_nickname",
      "label": "Family Nickname",
      "fieldtype": "Data"
    },
    {
      "fieldname": "primary_residence",
      "label": "Primary Residence",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "section_parental",
      "fieldtype": "Section Break",
      "label": "Parental Controls"
    },
    {
      "fieldname": "parental_controls_enabled",
      "label": "Enable Parental Controls",
      "fieldtype": "Check"
    },
    {
      "fieldname": "screen_time_limit_minutes",
      "label": "Daily Screen Time Limit (minutes)",
      "fieldtype": "Int",
      "depends_on": "eval:doc.parental_controls_enabled"
    }
  ]
}
```

#### Company (Concrete)

```json
{
  "doctype": "Company",
  "module": "Dartwing Company",
  "autoname": "CO-.#####",
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "section_legal",
      "fieldtype": "Section Break",
      "label": "Legal Entity Information"
    },
    {
      "fieldname": "legal_name",
      "label": "Legal Entity Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "tax_id",
      "label": "Tax ID / EIN / Unified Social Credit Code",
      "fieldtype": "Data"
    },
    {
      "fieldname": "entity_type",
      "label": "Entity Type",
      "fieldtype": "Select",
      "options": "\nC-Corp\nS-Corp\nLLC\nLimited Partnership (LP)\nGeneral Partnership\nLLP\nWFOE (China)\nBenefit Corporation\nCooperative"
    },
    { "fieldname": "column_break_legal", "fieldtype": "Column Break" },
    {
      "fieldname": "jurisdiction_country",
      "label": "Country of Formation",
      "fieldtype": "Link",
      "options": "Country"
    },
    {
      "fieldname": "jurisdiction_state",
      "label": "State / Province",
      "fieldtype": "Data"
    },
    {
      "fieldname": "formation_date",
      "label": "Date of Formation",
      "fieldtype": "Date"
    },
    {
      "fieldname": "section_addresses",
      "fieldtype": "Section Break",
      "label": "Addresses"
    },
    {
      "fieldname": "registered_address",
      "label": "Registered Address",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "physical_address",
      "label": "Principal / Physical Address",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "registered_agent",
      "label": "Registered Agent",
      "fieldtype": "Link",
      "options": "Person"
    },
    {
      "fieldname": "section_officers",
      "fieldtype": "Section Break",
      "label": "Officers & Directors"
    },
    {
      "fieldname": "officers",
      "label": "Officers & Directors",
      "fieldtype": "Table",
      "options": "Organization Officer"
    },
    {
      "fieldname": "section_ownership",
      "fieldtype": "Section Break",
      "label": "Ownership / Members / Partners",
      "depends_on": "eval:['LLC','Limited Partnership (LP)','LLP','General Partnership'].includes(doc.entity_type)"
    },
    {
      "fieldname": "members_partners",
      "label": "Members / Partners",
      "fieldtype": "Table",
      "options": "Organization Member Partner"
    }
  ]
}
```

#### Club (Concrete)

```json
{
  "doctype": "Club",
  "module": "Dartwing Associations",
  "autoname": "CLB-.#####",
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "section_membership",
      "fieldtype": "Section Break",
      "label": "Membership Configuration"
    },
    {
      "fieldname": "membership_tiers",
      "label": "Membership Tiers",
      "fieldtype": "Table",
      "options": "Organization Membership Tier"
    },
    {
      "fieldname": "default_dues_amount",
      "label": "Default Annual Dues",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "section_amenities",
      "fieldtype": "Section Break",
      "label": "Amenities & Facilities"
    },
    {
      "fieldname": "amenities",
      "label": "Amenities",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "clubhouse_address",
      "label": "Clubhouse Address",
      "fieldtype": "Link",
      "options": "Address"
    }
  ]
}
```

#### Nonprofit (Concrete)

```json
{
  "doctype": "Nonprofit",
  "module": "Dartwing Nonprofit",
  "autoname": "NPO-.#####",
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "section_taxexempt",
      "fieldtype": "Section Break",
      "label": "Tax-Exempt Status"
    },
    {
      "fieldname": "tax_exempt_status",
      "label": "Tax-Exempt Status",
      "fieldtype": "Select",
      "options": "\n501(c)(3)\n501(c)(4)\n501(c)(6)\n501(c)(7)\nOther"
    },
    {
      "fieldname": "ein",
      "label": "EIN",
      "fieldtype": "Data"
    },
    {
      "fieldname": "determination_date",
      "label": "IRS Determination Date",
      "fieldtype": "Date"
    },
    {
      "fieldname": "column_break_tax", "fieldtype": "Column Break"
    },
    {
      "fieldname": "fiscal_year_end",
      "label": "Fiscal Year End",
      "fieldtype": "Select",
      "options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember"
    },
    {
      "fieldname": "mission_statement",
      "label": "Mission Statement",
      "fieldtype": "Text"
    },
    {
      "fieldname": "section_board",
      "fieldtype": "Section Break",
      "label": "Board of Directors"
    },
    {
      "fieldname": "board_members",
      "label": "Board Members",
      "fieldtype": "Table",
      "options": "Organization Officer"
    },
    {
      "fieldname": "section_addresses",
      "fieldtype": "Section Break",
      "label": "Addresses"
    },
    {
      "fieldname": "registered_address",
      "label": "Registered Address",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "mailing_address",
      "label": "Mailing Address",
      "fieldtype": "Link",
      "options": "Address"
    }
  ]
}
```

### 3.5 Child Doctypes

#### Organization Officer (Child Table)

```json
{
  "doctype": "Organization Officer",
  "istable": 1,
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    { "fieldname": "title", "label": "Title", "fieldtype": "Data", "reqd": 1 },
    { "fieldname": "start_date", "label": "Start Date", "fieldtype": "Date" },
    { "fieldname": "end_date", "label": "End Date", "fieldtype": "Date" }
  ]
}
```

#### Organization Member Partner (Child Table)

```json
{
  "doctype": "Organization Member Partner",
  "istable": 1,
  "fields": [
    {
      "fieldname": "person",
      "label": "Member / Partner",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "ownership_percent",
      "label": "% Ownership",
      "fieldtype": "Percent"
    },
    {
      "fieldname": "capital_contribution",
      "label": "Capital Contribution",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "voting_rights",
      "label": "Voting Rights %",
      "fieldtype": "Percent"
    }
  ]
}
```

#### Organization Membership Tier (Child Table)

```json
{
  "doctype": "Organization Membership Tier",
  "istable": 1,
  "fields": [
    {
      "fieldname": "tier_name",
      "label": "Tier Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "annual_fee",
      "label": "Annual Fee",
      "fieldtype": "Currency"
    },
    { "fieldname": "benefits", "label": "Benefits", "fieldtype": "Small Text" }
  ]
}
```

### 3.6 Server-Side Hooks Implementation

The hybrid model requires server-side hooks to maintain the bidirectional relationship between `Organization` and its concrete types.

[See also: `docs/dartwing_core/org_integrity_guardrails.md` for immutability + reconciliation details.]

#### hooks.py Configuration

```python
# dartwing_core/hooks.py

doc_events = {
    "Organization": {
        "after_insert": "dartwing_core.doctype.organization.organization.create_concrete_type",
        "on_trash": "dartwing_core.doctype.organization.organization.delete_concrete_type"
    }
}
```

#### Organization Controller

```python
# dartwing_core/doctype/organization/organization.py

import frappe
from frappe.model.document import Document

# Maps org_type Select value to concrete Doctype name
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Nonprofit": "Nonprofit",
    "Club/Association": "Club"
}

class Organization(Document):
    def validate(self):
        if self.org_type and self.org_type not in ORG_TYPE_MAP:
            frappe.throw(f"Invalid org_type: {self.org_type}")

        # Prevent org_type change after creation (defense in depth with set_only_once)
        if not self.is_new() and self.has_value_changed("org_type"):
            frappe.throw(_("Organization type cannot be changed after creation"))

def create_concrete_type(doc, method):
    """
    Hook: after_insert
    Creates the corresponding concrete type record and links it back.
    """
    concrete_doctype = ORG_TYPE_MAP.get(doc.org_type)
    if not concrete_doctype:
        frappe.throw(f"Unknown org_type: {doc.org_type}")

    # Create the concrete type with back-reference
    concrete = frappe.new_doc(concrete_doctype)
    concrete.organization = doc.name
    concrete.flags.ignore_permissions = True
    concrete.insert()

    # Update Organization with forward reference (without triggering hooks)
    doc.db_set("linked_doctype", concrete_doctype, update_modified=False)
    doc.db_set("linked_name", concrete.name, update_modified=False)

def delete_concrete_type(doc, method):
    """
    Hook: on_trash
    Cascades delete to the concrete type record.
    """
    if doc.linked_doctype and doc.linked_name:
        if frappe.db.exists(doc.linked_doctype, doc.linked_name):
            frappe.delete_doc(
                doc.linked_doctype,
                doc.linked_name,
                force=True,
                ignore_permissions=True
            )

@frappe.whitelist()
def get_concrete_doc(organization: str) -> dict:
    """
    API helper to fetch the concrete type document in one call.

    Usage (JavaScript):
        frappe.call({
            method: 'dartwing_core.doctype.organization.organization.get_concrete_doc',
            args: { organization: 'ORG-2025-00001' }
        })

    Usage (Python):
        from dartwing_core.doctype.organization.organization import get_concrete_doc
        family_doc = get_concrete_doc('ORG-2025-00001')
    """
    org = frappe.get_doc("Organization", organization)
    if not org.linked_doctype or not org.linked_name:
        return None
    return frappe.get_doc(org.linked_doctype, org.linked_name).as_dict()

@frappe.whitelist()
def get_organization_with_details(organization: str) -> dict:
    """
    Returns Organization merged with its concrete type fields.
    Useful for Flutter/API consumers who want a single payload.
    """
    org = frappe.get_doc("Organization", organization)
    result = org.as_dict()

    if org.linked_doctype and org.linked_name:
        concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
        result["concrete_type"] = concrete.as_dict()

    return result
```

#### Concrete Type Base Mixin

```python
# dartwing_core/mixins/organization_mixin.py

import frappe

class OrganizationMixin:
    """
    Shared functionality for all concrete organization types.
    Inherit this in Family, Company, Club, Nonprofit controllers.
    """

    @property
    def org_name(self):
        """Fetch org_name from parent Organization."""
        return frappe.db.get_value("Organization", self.organization, "org_name")

    @property
    def logo(self):
        """Fetch logo from parent Organization."""
        return frappe.db.get_value("Organization", self.organization, "logo")

    @property
    def org_status(self):
        """Fetch status from parent Organization."""
        return frappe.db.get_value("Organization", self.organization, "status")

    def get_organization_doc(self):
        """Return the full parent Organization document."""
        return frappe.get_doc("Organization", self.organization)

    def update_org_name(self, new_name: str):
        """Update org_name on the parent Organization."""
        frappe.db.set_value("Organization", self.organization, "org_name", new_name)
```

#### Example: Family Controller Using Mixin

```python
# dartwing_family/doctype/family/family.py

from frappe.model.document import Document
from dartwing_core.mixins.organization_mixin import OrganizationMixin

class Family(Document, OrganizationMixin):
    def validate(self):
        # Family-specific validation
        if self.screen_time_limit_minutes and self.screen_time_limit_minutes < 0:
            frappe.throw("Screen time limit cannot be negative")

    def get_family_members(self):
        """Return all Org Members for this family's organization."""
        return frappe.get_all(
            "Org Member",
            filters={"organization": self.organization, "status": "Active"},
            fields=["person", "role", "start_date"]
        )
```

### 3.7 Role Template Doctype

```json
{
  "doctype": "Role Template",
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "role_name",
      "label": "Role Name",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "applies_to_org_type",
      "label": "Applies To",
      "fieldtype": "Select",
      "reqd": 1,
      "options": "Family\nCompany\nNonprofit\nClub/Association"
    },
    {
      "fieldname": "is_supervisor",
      "label": "Is Supervisor?",
      "fieldtype": "Check"
    },
    {
      "fieldname": "default_hourly_rate",
      "label": "Default Hourly Rate",
      "fieldtype": "Currency",
      "depends_on": "eval:doc.applies_to_org_type=='Company'"
    }
  ]
}
```

### 3.8 Org Member Doctype
[See `docs/dartwing_core/person_doctype_contract.md` for Person identity/linkage and invite flow requirements.]

```json
{
  "doctype": "Org Member",
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
    },
    {
      "fieldname": "role",
      "label": "Role",
      "fieldtype": "Link",
      "options": "Role Template",
      "reqd": 1
    },
    {
      "fieldname": "start_date",
      "label": "Member Since",
      "fieldtype": "Date",
      "default": "Today"
    },
    { "fieldname": "end_date", "label": "End Date", "fieldtype": "Date" },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "default": "Active",
      "options": "Active\nInactive\nPending"
    }
  ],
  "links": [
    {
      "link_doctype": "Family Relationship",
      "link_fieldname": "family",
      "group": "Family"
    },
    {
      "link_doctype": "Employment Record",
      "link_fieldname": "company",
      "group": "Company"
    }
  ]
}
```

### 3.9 Family Relationship Doctype

```json
{
  "doctype": "Family Relationship",
  "istable": 0,
  "module": "Dartwing Family",
  "autoname": "hash",
  "fields": [
    {
      "fieldname": "family",
      "label": "Family",
      "fieldtype": "Link",
      "options": "Family",
      "reqd": 1,
      "description": "Links to concrete Family type (enforces type safety)"
    },
    {
      "fieldname": "person_a",
      "label": "Person A",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "person_b",
      "label": "Person B",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "relationship",
      "label": "Relationship (A → B)",
      "fieldtype": "Select",
      "reqd": 1,
      "options": "Parent\nChild\nSpouse\nSibling\nGrandparent\nGrandchild\nGuardian\nOther"
    }
  ]
}
```

### 3.10 Employment Record Doctype

```json
{
  "doctype": "Employment Record",
  "module": "Dartwing HR",
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "EMP-.YYYY.-",
      "default": "EMP-.YYYY.-",
      "hidden": 1
    },
    {
      "fieldname": "employee",
      "label": "Employee",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "company",
      "label": "Company",
      "fieldtype": "Link",
      "options": "Company",
      "reqd": 1,
      "description": "Links to concrete Company type (enforces type safety)"
    },
    {
      "fieldname": "department",
      "label": "Department",
      "fieldtype": "Link",
      "options": "Department"
    },
    {
      "fieldname": "supervisor",
      "label": "Reports To",
      "fieldtype": "Link",
      "options": "Person"
    },
    { "fieldname": "hire_date", "label": "Hire Date", "fieldtype": "Date" },
    {
      "fieldname": "termination_date",
      "label": "Termination Date",
      "fieldtype": "Date"
    },
    {
      "fieldname": "hourly_rate",
      "label": "Hourly Rate",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "skills",
      "label": "Skills",
      "fieldtype": "Table",
      "options": "Employee Skill"
    }
  ]
}
```

### 3.11 Equipment Doctype

```json
{
  "doctype": "Equipment",
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "equipment_name",
      "label": "Name / Description",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "serial_number",
      "label": "Serial Number",
      "fieldtype": "Data",
      "unique": 1
    },
    {
      "fieldname": "owner_organization",
      "label": "Owner Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "Person"
    },
    {
      "fieldname": "current_location",
      "label": "Current Location",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "manuals",
      "label": "Manuals & Docs",
      "fieldtype": "Table",
      "options": "Equipment Document"
    },
    {
      "fieldname": "maintenance_schedule",
      "label": "Maintenance Schedule",
      "fieldtype": "Table",
      "options": "Equipment Maintenance"
    }
  ]
}
```

### 3.12 Employee Skill (Child Table)

```json
{
  "doctype": "Employee Skill",
  "istable": 1,
  "fields": [
    { "fieldname": "skill", "label": "Skill", "fieldtype": "Data", "reqd": 1 },
    {
      "fieldname": "proficiency",
      "label": "Proficiency",
      "fieldtype": "Select",
      "options": "Beginner\nIntermediate\nAdvanced\nExpert"
    }
  ]
}
```

### 3.13 Equipment Document (Child Table)

```json
{
  "doctype": "Equipment Document",
  "istable": 1,
  "fields": [
    { "fieldname": "document_type", "label": "Type", "fieldtype": "Data" },
    { "fieldname": "file", "label": "File", "fieldtype": "Attach" }
  ]
}
```

### 3.14 Equipment Maintenance (Child Table)

```json
{
  "doctype": "Equipment Maintenance",
  "istable": 1,
  "fields": [
    { "fieldname": "task", "label": "Task", "fieldtype": "Data" },
    {
      "fieldname": "frequency",
      "label": "Frequency",
      "fieldtype": "Select",
      "options": "Daily\nWeekly\nMonthly\nQuarterly\nYearly"
    },
    { "fieldname": "next_due", "label": "Next Due", "fieldtype": "Date" }
  ]
}
```

---

## 4. Flutter Client Architecture

### 4.1 State Management

Dartwing uses Riverpod 2.0 for state management, providing:

- Compile-time safety and automatic disposal
- Provider scoping for multi-tenant support
- AsyncNotifier for API state management
- Code generation for reduced boilerplate

### 4.2 Project Structure

The Flutter project follows a feature-first architecture:

```
lib/
├── core/           # Shared utilities, constants, extensions, theme
├── data/           # API clients, repositories, DTOs
├── domain/         # Entity models, use cases, repository interfaces
├── presentation/   # Screens, widgets, providers
└── services/       # Platform services (auth, storage, notifications)
```

### 4.3 Frappe Integration Layer

A dedicated Frappe client library handles all backend communication:

- **FrappeClient:** HTTP client with automatic token refresh
- **DoctypeRepository<T>:** Generic CRUD operations for any doctype
- **SocketService:** Real-time updates via Socket.IO
- **OfflineSync:** Queue-based offline operation handling

### 4.4 Platform Adaptations

| Platform | Adaptations                       | Special Features                           |
| -------- | --------------------------------- | ------------------------------------------ |
| iOS      | Cupertino widgets, iOS navigation | Push notifications, HealthKit, CallKit     |
| Android  | Material Design 3, back gesture   | FCM, Health Connect, Work Profile          |
| Web      | Responsive layout, keyboard nav   | PWA support, Web Push, OAuth redirect      |
| Desktop  | Window management, menus          | System tray, file associations, deep links |

---

## 5. Authentication Architecture

### 5.1 Keycloak Integration

Dartwing uses Keycloak as the identity provider, enabling SSO across all applications. The integration supports OAuth2/OIDC flows with PKCE for mobile apps.

### 5.2 Personal vs Business Identity

A key architectural decision is the separation of personal and business identities:

- **Personal Account:** User's private identity, never accessible by employers
- **Business Account:** Linked to organization, subject to org policies
- **Invitation Flow:** Users create personal account first, then receive org invitations

### 5.3 Multi-Factor Authentication

- Email OTP verification
- SMS verification (Twilio integration)
- TOTP authenticator apps
- Biometric (Face ID, fingerprint) for mobile

### 5.4 Integration Token Management

External integrations (Twilio, Stripe, Google, etc.) require secure credential storage and proactive token refresh.

[See `docs/dartwing_core/integration_token_management_spec.md` for OAuth2 token lifecycle, encryption strategy, and proactive refresh scheduler.]

---

---

## 6. AI Persona Architecture

### 6.1 Persona Types

Dartwing includes built-in AI personas that adapt to organizational context:

- **Sales Persona:** Lead qualification, product recommendations, quote generation
- **Support Persona:** Ticket triage, FAQ responses, escalation management
- **Admin Persona:** Workflow automation, report generation, data validation
- **Custom Personas:** User-defined personas with specific knowledge bases

### 6.2 Knowledge Vault

Each Organization has an associated Knowledge Vault containing documents, FAQs, product information, and procedures. AI personas query this vault to provide contextually accurate responses.

### 6.3 Tool Registry

AI personas can execute registered tools—API calls, database queries, workflow triggers—based on user requests. Tools are registered per-organization and subject to role-based permissions.

### 6.4 Voice & Interaction Layer

- **Voice-First Interface:** Native Flutter voice capabilities allow users to interact via natural language (e.g., "Add a meeting with John tomorrow").
- **Local LLM Support:** Privacy-focused option for Family orgs to run smaller LLMs (e.g., Llama 3 8B) on local hardware/edge devices.
- **Meeting Assistant:** Automated transcription and summarization of meetings with action item extraction into the `Task` doctype.

---

## 7. Modular Application Architecture

### 7.1 Core Modules

| Module          | Description                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| dartwing_core   | Organization, Person, Org Member, Role Template, Equipment doctypes                                        |
| dartwing_hr     | Employment Record, Skills, Departments, Payroll integration                                                |
| dartwing_family | Family Relationship, shared calendars, allowance tracking, Chore Gamification, Meal Planning, Family Vault |
| dartwing_comms  | Virtual phone numbers, SMS/Voice, Fax management, Unified Inbox, Smart Routing, Broadcast System           |
| dartwing_ai     | AI Personas, Knowledge Vault, Tool Registry, LLM integration                                               |
| dartwing_fax    | HIPAA-compliant fax handling, patient mapping, audit logs                                                  |

### 7.2 Module Loading

Modules are loaded dynamically based on organization type and subscription tier. The Flutter client discovers available modules via API and loads corresponding UI components.

---

## 8. Security Architecture

### 8.1 Data Security

- **Encryption at Rest:** AES-256 for all stored data
- **Encryption in Transit:** TLS 1.3 for all API communication
- **Zero Trust Files:** File storage with per-file encryption keys
- **Audit Logging:** Comprehensive activity logging for compliance

### 8.2 Role-Based Access Control

Permissions cascade from Organization → Role Template → Org Member. Frappe's built-in permission system is extended with custom permission rules for complex multi-org scenarios.

#### 8.2.1 Hybrid Model Permissions Strategy

The hybrid Organization model requires careful permission handling to ensure users can only access their own organizations and concrete types.

**Permission Flow:**
```
User → Org Member → Organization → Concrete Type (Family/Company/Club/Nonprofit)
```

**Implementation:**

1. **Document-Level Permissions on Organization:**
```python
# When user becomes Org Member, add user_permission
def on_org_member_insert(doc, method):
    frappe.get_doc({
        "doctype": "User Permission",
        "user": frappe.db.get_value("Person", doc.person, "user"),
        "allow": "Organization",
        "for_value": doc.organization,
        "apply_to_all_doctypes": 0,
        "applicable_for": "Organization"
    }).insert(ignore_permissions=True)
```

2. **Concrete Type Permissions (Auto-Inherited):**

Each concrete type inherits access via its `organization` Link field. Add this permission rule to each concrete doctype:

```json
// In Family, Company, Club, Nonprofit doctype JSON
"permissions": [
    {
        "role": "System Manager",
        "read": 1, "write": 1, "create": 1, "delete": 1
    },
    {
        "role": "Dartwing User",
        "read": 1, "write": 1,
        "if_owner": 0
    }
],
"restrict_to_domain": "",
"user_permission_dependant_doctype": "Organization"
```

3. **Permission Query Hook (for list views):**

```python
# dartwing_core/permissions.py

def get_permission_query_conditions(user):
    """
    Called by Frappe to filter list queries.
    Returns SQL WHERE clause fragment.
    """
    if "System Manager" in frappe.get_roles(user):
        return ""

    # Get all organizations this user has access to
    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"  # No access

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabOrganization`.`name` IN ({org_list})"

def has_permission(doc, ptype, user):
    """
    Called for single document permission checks.
    """
    if "System Manager" in frappe.get_roles(user):
        return True

    return frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Organization", "for_value": doc.name}
    )
```

4. **Concrete Type Permission Hooks:**

```python
# dartwing_family/permissions.py

def get_permission_query_conditions_family(user):
    """Filter Family list by user's accessible Organizations."""
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

5. **Register Permission Hooks:**

```python
# dartwing_core/hooks.py

permission_query_conditions = {
    "Organization": "dartwing_core.permissions.get_permission_query_conditions",
    "Family": "dartwing_family.permissions.get_permission_query_conditions_family",
    "Company": "dartwing_company.permissions.get_permission_query_conditions_company",
    "Club": "dartwing_associations.permissions.get_permission_query_conditions_club",
    "Nonprofit": "dartwing_nonprofit.permissions.get_permission_query_conditions_nonprofit",
}

has_permission = {
    "Organization": "dartwing_core.permissions.has_permission",
}
```

#### 8.2.2 Role Hierarchy

| Frappe Role | Access Level | Description |
|-------------|--------------|-------------|
| System Manager | Full | Platform administrators |
| Dartwing Admin | Multi-Org | Can manage multiple organizations |
| Organization Admin | Single-Org | Full access to one organization |
| Dartwing User | Member | Standard member access |
| Dartwing Guest | Read-Only | Limited read access (e.g., family member without account) |

### 8.3 Compliance Support

- **HIPAA:** PHI handling, BAAs, audit trails
- **GDPR:** Data portability, right to erasure, consent management
- **SOC 2:** Security controls and monitoring
- **Multi-Jurisdiction:** Data residency requirements (US, EU, China)

---

## 9. Implementation Roadmap

### 9.1 Phase 1: Foundation (Q1 2026)

1. Core doctypes (Organization, Person, Org Member)
2. Flutter project scaffolding with Riverpod
3. Keycloak integration with PKCE flows
4. Basic Frappe API client
5. iOS and Android builds

### 9.2 Phase 2: Core Features (Q2 2026)

1. Role Template and conditional field visibility
2. Family and Company org_type implementations
3. Equipment management
4. Real-time sync via Socket.IO
5. Web and Desktop builds

### 9.3 Phase 3: AI & Communications (Q3 2026)

1. AI Persona engine integration
2. Knowledge Vault implementation
3. Virtual phone numbers (Twilio)
4. Fax management module
5. HIPAA compliance features

### 9.4 Phase 4: Scale & Polish (Q4 2026)

1. Nonprofit and Club org_types
2. Multi-jurisdiction support
3. Advanced analytics and reporting
4. App store submissions
5. Enterprise deployment options

---

## 10. Technical Specifications

### 10.1 Technology Stack

| Component          | Technology | Version |
| ------------------ | ---------- | ------- |
| Frontend Framework | Flutter    | 3.24+   |
| Frontend Language  | Dart       | 3.5+    |
| Backend Framework  | Frappe     | 15.x    |
| Backend Language   | Python     | 3.11+   |
| Database           | MariaDB    | 10.6+   |
| Identity Provider  | Keycloak   | 24.x    |
| Cache/Queue        | Redis      | 7.x     |
| State Management   | Riverpod   | 2.5+    |

### 10.2 API Design Principles

1. **RESTful Resources:** Standard HTTP methods for CRUD operations
2. **Frappe API Convention:** Use /api/resource/{doctype} endpoints
3. **RPC Methods:** Custom whitelisted methods via /api/method/{path}
4. **Pagination:** Limit/offset with total count in response
5. **Filtering:** Frappe filters syntax for flexible queries
6. **Versioning:** API version in header, not URL path

### 10.3 Performance Requirements

- **API Response Time:** < 200ms for simple queries, < 1s for complex reports
- **App Launch Time:** < 3s cold start, < 1s warm start
- **Offline Capability:** Full read access, queued write operations
- **Sync Latency:** < 500ms for real-time updates
- **Concurrent Users:** Support 10,000+ concurrent connections per instance

### 10.4 Observability

Production systems require comprehensive metrics, structured logging, and alerting.

[See `docs/dartwing_core/observability_spec.md` for Prometheus metrics, structured logging format, and alert definitions.]

---

## 11. Advanced Features & Operations

[Offline/real-time sync behavior is detailed in `docs/dartwing_core/offline_real_time_sync_spec.md`.]

[Background job queue isolation and retry strategies are detailed in `docs/dartwing_core/background_job_isolation_spec.md`.]

### 11.1 Business & Operations

- **Geofencing & Location Tracking:**
  - _Business:_ Auto-clock-in/out, asset tracking.
  - _Family:_ Child arrival/departure alerts (school/home).
- **Visual Workflow Builder:** Flutter-based drag-and-drop UI for designing approval processes and automations.
- **White-Labeling:** Tenant-specific branding (Logo, Colors) dynamically applied to the Flutter app.

### 11.2 Developer Ecosystem

- **Plugin Marketplace:** Platform for third-party developers to build and sell modules.
- **Webhooks & Zapier:** First-class support for outgoing webhooks and integration with external low-code tools.
- **Data Sovereignty:** One-click "Export All My Data" (JSON/CSV) feature.

---

## Appendix A: Doctype JSON Reference

Complete Frappe JSON definitions are organized by module:

### Core Module (dartwing_core)
| Doctype | Type | Description |
|---------|------|-------------|
| Organization | Parent | Thin reference shell for polymorphic identity |
| Person | Parent | Individual human identity |
| Org Member | Parent | Links Person to Organization with role |
| Role Template | Parent | Role definitions per org_type |
| Equipment | Parent | Assets owned by organizations |
| Equipment Document | Child Table | Attached documents for Equipment |
| Equipment Maintenance | Child Table | Maintenance schedules for Equipment |
| Organization Officer | Child Table | Officers/Directors (used by Company, Nonprofit) |
| Organization Member Partner | Child Table | LLC/Partnership ownership (used by Company) |
| Employee Skill | Child Table | Skills for Employment Record |

### Concrete Organization Types
| Doctype | Module | Naming Series |
|---------|--------|---------------|
| Family | dartwing_family | FAM-.##### |
| Company | dartwing_company | CO-.##### |
| Club | dartwing_associations | CLB-.##### |
| Nonprofit | dartwing_nonprofit | NPO-.##### |

### Type-Specific Doctypes
| Doctype | Module | Links To |
|---------|--------|----------|
| Family Relationship | dartwing_family | Family (concrete) |
| Employment Record | dartwing_hr | Company (concrete) |
| Organization Membership Tier | dartwing_associations | Club (child table) |

---

## Appendix B: Flutter Package Dependencies

Core packages required for the Flutter client:

- flutter_riverpod, riverpod_annotation, riverpod_generator
- dio, retrofit, json_serializable
- flutter_secure_storage, hive_flutter
- socket_io_client
- flutter_appauth (OAuth/OIDC)
- go_router
- freezed, freezed_annotation

---

## Appendix C: Glossary

- **Doctype:** Frappe's equivalent of a database table with metadata and logic
- **org_type:** The classification of an Organization (Family/Company/Nonprofit/Club)
- **Role Template:** Reusable role definitions filtered by org_type
- **depends_on:** Frappe field attribute for conditional visibility
- **Knowledge Vault:** Organization-specific document repository for AI context
- **DartwingFone:** The mobile application component of Dartwing
- **@frappe.whitelist():** Python decorator that exposes a method via REST API
- **frappe.call():** JavaScript function that makes AJAX requests to whitelisted methods
- **PKCE:** Proof Key for Code Exchange - OAuth2 extension for mobile apps
- **Socket.IO:** Real-time bidirectional event-based communication library
