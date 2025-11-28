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

- **Universal Organization Model:** Single doctype handles families, companies, nonprofits, and clubs
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
  "fields": [
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
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
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
    }
  ]
}
```

#### Company (Concrete)

```json
{
  "doctype": "Company",
  "module": "Dartwing Company",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "read_only": 1
    },
    {
      "fieldname": "tax_id",
      "label": "Tax ID / EIN",
      "fieldtype": "Data"
    },
    {
      "fieldname": "entity_type",
      "label": "Entity Type",
      "fieldtype": "Select",
      "options": "C-Corp\nLLC\n..."
    },
    {
      "fieldname": "jurisdiction_country",
      "label": "Jurisdiction",
      "fieldtype": "Link",
      "options": "Country"
    }
  ]
}
```

#### Club (Concrete)

```json
{
  "doctype": "Club",
  "module": "Dartwing Associations",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization Ref",
      "fieldtype": "Link",
      "options": "Organization",
      "read_only": 1
    },
    {
      "fieldname": "membership_tiers",
      "label": "Membership Tiers",
      "fieldtype": "Table",
      "options": "Organization Membership Tier"
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

### 3.6 Role Template Doctype

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

### 3.7 Org Member Doctype

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
      "link_fieldname": "organization",
      "group": "Family"
    },
    {
      "link_doctype": "Employment Record",
      "link_fieldname": "organization",
      "group": "Company"
    }
  ]
}
```

### 3.8 Family Relationship Doctype

```json
{
  "doctype": "Family Relationship",
  "istable": 0,
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Family",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
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

### 3.9 Employment Record Doctype

```json
{
  "doctype": "Employment Record",
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "employee",
      "label": "Employee",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "organization",
      "label": "Company",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
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

### 3.10 Equipment Doctype

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

### 3.11 Employee Skill (Child Table)

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

### 3.12 Equipment Document (Child Table)

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

### 3.13 Equipment Maintenance (Child Table)

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

---

## 11. Advanced Features & Operations

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

Complete Frappe JSON definitions for core doctypes are maintained in the dartwing_core repository. Key doctypes include:

- Organization
- Person
- Org Member
- Role Template
- Family Relationship
- Employment Record
- Equipment
- Equipment Document (child table)
- Equipment Maintenance (child table)
- Organization Officer (child table)
- Organization Member Partner (child table)
- Organization Membership Tier (child table)
- Employee Skill (child table)

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
