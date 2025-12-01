# PRD – Dartwing Core

**The Universal Platform That Powers Every Dartwing Application**

| Field | Value |
|-------|-------|
| Version | 2.0 |
| Date | November 2025 |
| Status | Draft |
| Module | dartwing_core |

---

# Section 1: Executive Summary & Vision

## 1.1 Purpose

This document defines every shippable, customer-facing feature of **Dartwing Core** — the foundational platform inherited by all vertical applications including DartwingFax, DartwingFamily, DartwingLegal, DartwingHealth, and future modules.

Dartwing Core functions as the "iOS + AWS" layer: a complete runtime environment providing multi-tenancy, authentication, offline sync, real-time collaboration, and compliance infrastructure that vertical modules consume without reimplementation.

## 1.2 Vision Statement

> **One framework. Every platform. Any organization type.**

Dartwing eliminates the need for separate CRM, HRIS, family-management, church-management, HOA, and club-membership systems by providing a single, unified architecture that adapts to any organizational structure.

## 1.3 Key Differentiators

| Differentiator | Description |
|----------------|-------------|
| **Universal Organization Model** | Hybrid architecture with unified identity layer and type-specific concrete implementations (Family, Company, Club, Nonprofit) |
| **Cross-Platform Native** | Flutter provides true native performance on iOS, Android, Web, and Desktop from a single codebase |
| **AI-First Design** | Built-in AI personas, smart routing, and LLM integration with optional local/edge processing for privacy |
| **Low-Code Development** | Frappe's doctype system enables rapid app building; new verticals ship in ≤8 weeks |
| **Offline-First Architecture** | Full native apps work 100% offline with deterministic sync and conflict resolution |
| **Multi-Tenant Isolation** | Complete data isolation between Organizations with <400ms context switching |
| **Compliance-Ready** | One toggle enables HIPAA, SOC2, GDPR modes with signed BAA, Object Lock, encryption, and audit trails |

## 1.4 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend Framework | Flutter | 3.24+ |
| Frontend Language | Dart | 3.5+ |
| Backend Framework | Frappe | 15.x |
| Backend Language | Python | 3.11+ |
| Database | MariaDB | 10.6+ |
| Identity Provider | Keycloak | 24.x |
| Cache/Queue | Redis | 7.x |
| State Management | Riverpod | 2.5+ |
| Real-Time | Socket.IO | Latest |

## 1.5 Target Metrics

| Metric | Target |
|--------|--------|
| New vertical MVP launch time | ≤8 weeks |
| Lines of code for new module | ~1,800 typical |
| API response time (simple queries) | <200ms |
| API response time (complex reports) | <1s |
| App cold start | <3s |
| App warm start | <1s |
| Real-time sync latency | <500ms |
| Concurrent connections per instance | 10,000+ |
| Uptime | 99.99% |
| Security incidents (multi-tenancy/sync) | 0 |
| Mobile app rating | ≥4.8 |

## 1.6 Document Structure

This PRD is organized into the following sections:

1. Executive Summary & Vision (this section)
2. Feature Catalog (prioritized list with tiers)
3. Organization & Multi-Tenancy System
4. Identity & Authentication
5. Offline-First & Real-Time Sync
6. UI Generation & Navigation
7. File Storage & Documents
8. Notifications & Communication
9. Compliance & Security
10. Plugin & Module System
11. Integrations & Marketplace
12. AI & Voice Features
13. Developer Experience
14. Acceptance Criteria & Success Metrics
15. Architecture Cross-Reference & Known Issues

---

*End of Section 1*
# Section 2: Feature Catalog

## 2.1 Feature Summary

Dartwing Core provides 25 foundational features organized into 8 capability domains. All features are inherited automatically by vertical modules (DartwingFax, DartwingFamily, etc.).

## 2.2 Complete Feature Catalog

| ID | Feature Name | Description (Customer Benefit) | Status | Tier | Domain |
|----|--------------|-------------------------------|--------|------|--------|
| C-01 | Multi-Tenant Organizations | Unlimited "Companies" and "Families" per account with full data isolation and <400ms context switching | Live | Free | Organization |
| C-02 | One-Click Organization Creation | Any user creates a Company or Family in ≤3 seconds | Live | Free | Organization |
| C-03 | Invite Members (Adults, Children, Guests) | Email invite + QR-code child invite + time-limited guest access + auto-join flow for new users | Live | Free | Organization |
| C-04 | Offline-First Mobile Apps | Full native iOS/Android apps work 100% offline (forms, lists, signatures, camera) with background sync | Live | Free | Sync |
| C-05 | Real-Time Collaboration | Live cursors, comments, @mentions, and presence across web + mobile via Socket.IO | Live | Free | Sync |
| C-06 | Automatic Native UI Generation | Every Frappe DocType instantly becomes beautiful, native Flutter forms, lists, kanban, calendars — zero code | Live | Free | UI |
| C-07 | Unified File Storage | One API works with Google Drive, SharePoint, OneDrive, Dropbox, or S3 + automatic virus scanning | Live | Free/Pro | Storage |
| C-08 | Electronic Signature & Annotation | Legally-binding e-signature (draw/type/upload) + highlight, stamp, redact — reusable in every app | Live | Free | Documents |
| C-09 | Global Full-Text + Metadata Search | Sub-second search across millions of documents, faxes, notes, appliances, etc. | Live | Pro | Search |
| C-10 | Real-Time Notifications Engine | Push, SMS, email, in-app — rule-based (keywords, assignees, urgency) | Live | Free/Pro | Notifications |
| C-11 | White-Label & Custom Domain | app.yourbrand.com, email@yourbrand.com, custom logo/color, remove all Dartwing branding | Live | Enterprise | Branding |
| C-12 | Per-Organization Billing & Usage Metering | Meter fax pages, storage, API calls, seats → Stripe/Lemon Squeezy billing | Live | Pro | Billing |
| C-13 | Compliance-Ready Mode (HIPAA/SOC2/GDPR) | One toggle enables signed BAA, Object Lock, encryption, audit trail, data residency | Live | Pro/Enterprise | Compliance |
| C-14 | Plugin / Module System | Install DartwingFax, DartwingFamily, DartwingLegal, etc. as simple plugins on the same instance | Live | Free | Platform |
| C-15 | 40+ Pre-Built Integrations Marketplace | Salesforce, QuickBooks, Google Workspace, Microsoft 365, Slack, Zapier, DocuSign, etc. — one-click connect | Live | Pro/Enterprise | Integrations |
| C-16 | Background Job Engine | OCR, fax sending, PDF generation, AI tasks, reminders — guaranteed execution with progress UI | Live | Free | Platform |
| C-17 | Role & Permission System (Row + Field Level) | Permissions scoped to Company/Family + department + location + custom roles | Live | Free | Security |
| C-18 | Theme & Branding Engine | Per-organization colors, logos, fonts, dark mode — instantly applied everywhere | Live | Free | Branding |
| C-19 | Navigation & Routing Framework | Dynamic sidebar, bottom nav, deep linking, role-based menus — same code works web + mobile | Live | Free | UI |
| C-20 | Immutable 7-Year Audit Trail | Every action (create/edit/delete/upload) logged forever with S3 Object Lock | Live | Pro | Compliance |
| C-21 | Data Residency Selection | Customer picks US / EU / Canada / Australia region at signup | Live | Enterprise | Compliance |
| C-22 | Feature Flags Per Organization | Turn any feature on/off instantly for one Company/Family or globally | Live | Pro | Platform |
| C-23 | Emergency Binder / Export Generator | One-tap beautiful PDF export of all critical data (used by Family → instantly reusable in Health/Legal) | Live | Free | Documents |
| C-24 | Fax-over-IP Engine (Reusable Primitive) | Any app can call `DartwingFax.send("+15551234", pdf)` — no extra code | Live | Pro | Communications |
| C-25 | Maintenance & Reminder Scheduler | Recurring tasks with push/email/SMS reminders and one-tap "Done" (started in Family → now used everywhere) | Live | Free | Tasks |

## 2.3 Features by Domain

### Organization Domain (C-01, C-02, C-03)

Core multi-tenancy and membership management enabling unlimited organizations per user with complete data isolation.

**Key Capabilities:**
- Hybrid Organization model (thin reference + concrete types)
- Four org_types: Family, Company, Club/Association, Nonprofit
- Bidirectional linking between Organization and concrete doctypes
- Member invitation via email, QR code, or direct link
- Guest access with time-limited permissions
- Child/minor member support with parental controls

### Sync Domain (C-04, C-05)

Offline-first architecture with deterministic sync and real-time collaboration.

**Key Capabilities:**
- Full offline CRUD operations with local queue
- Background sync with exponential backoff
- Three-tier conflict resolution: AI Smart Merge → Human Fallback → Last-Write-Wins
- Socket.IO channels scoped to `sync:<doctype>:<org>`
- Live presence indicators and cursors
- Delta-based sync with 30-day change log retention

### UI Domain (C-06, C-19)

Automatic native UI generation from Frappe doctypes with consistent navigation.

**Key Capabilities:**
- DocType → Flutter form/list/kanban/calendar rendering
- Conditional field visibility via `depends_on`
- Platform-adaptive widgets (Cupertino on iOS, Material on Android)
- Dynamic sidebar and bottom navigation
- Deep linking with role-based menu filtering
- Responsive layouts for web/tablet/phone

### Storage Domain (C-07)

Unified file storage abstraction across multiple cloud providers.

**Key Capabilities:**
- Single API for Google Drive, SharePoint, OneDrive, Dropbox, S3
- Automatic virus scanning on upload
- Per-file encryption keys (Zero Trust Files)
- Attachment upload before metadata (sync-safe)
- Storage usage metering per organization

### Documents Domain (C-08, C-23)

Electronic signatures, annotations, and document export.

**Key Capabilities:**
- Legally-binding e-signatures (draw/type/upload)
- Annotation tools: highlight, stamp, redact
- PDF generation with templating
- Emergency Binder one-tap export
- Document versioning and history

### Search Domain (C-09)

Global full-text and metadata search across all content.

**Key Capabilities:**
- Sub-second search across millions of records
- Full-text indexing of documents, faxes, notes
- Metadata filtering (date, type, assignee, tags)
- Saved searches and search history
- Organization-scoped results

### Notifications Domain (C-10)

Multi-channel notification engine with rule-based routing.

**Key Capabilities:**
- Push notifications (iOS/Android)
- SMS via Twilio
- Email with templates
- In-app notification center
- Rule-based triggers (keywords, assignees, urgency, escalation)

### Branding Domain (C-11, C-18)

White-labeling and per-organization theming.

**Key Capabilities:**
- Custom domains (app.yourbrand.com)
- Custom email domains (email@yourbrand.com)
- Logo, colors, fonts per organization
- Dark mode support
- Complete Dartwing branding removal (Enterprise)

### Compliance Domain (C-13, C-20, C-21)

Enterprise compliance features for regulated industries.

**Key Capabilities:**
- HIPAA mode with signed BAA support
- SOC 2 controls and monitoring
- GDPR data portability and right to erasure
- Immutable audit trail with S3 Object Lock (7-year retention)
- Data residency selection (US/EU/Canada/Australia)
- Encryption at rest (AES-256) and in transit (TLS 1.3)

### Platform Domain (C-14, C-16, C-22)

Core platform infrastructure for extensibility.

**Key Capabilities:**
- Plugin/module installation system
- Background job engine with guaranteed execution
- Progress UI for long-running tasks
- Feature flags per organization or global
- Job monitoring and retry logic

### Security Domain (C-17)

Role-based access control with row and field level permissions.

**Key Capabilities:**
- Permissions scoped to Organization + Role Template
- Row-level security via User Permission
- Field-level visibility via `depends_on`
- Department and location-based filtering
- Custom role creation

### Billing Domain (C-12)

Usage metering and subscription management.

**Key Capabilities:**
- Per-organization metering (fax pages, storage, API calls, seats)
- Stripe integration
- Lemon Squeezy integration
- Usage dashboards
- Billing alerts and limits

### Integrations Domain (C-15)

Pre-built connectors and integration marketplace.

**Key Capabilities:**
- 40+ one-click integrations
- Salesforce, QuickBooks, Google Workspace, Microsoft 365
- Slack, Zapier, DocuSign
- Webhook support (outgoing)
- OAuth2 connection management

### Communications Domain (C-24)

Reusable communication primitives.

**Key Capabilities:**
- Fax-over-IP engine callable from any module
- Simple API: `DartwingFax.send("+15551234", pdf)`
- Multi-carrier abstraction (Telnyx, Bandwidth, SignalWire)
- Delivery tracking and receipts

### Tasks Domain (C-25)

Recurring task and reminder management.

**Key Capabilities:**
- Maintenance scheduling (daily/weekly/monthly/quarterly/yearly)
- Multi-channel reminders (push/email/SMS)
- One-tap completion
- Overdue tracking and escalation
- Equipment maintenance integration

## 2.4 Tier Definitions

| Tier | Description | Features Included |
|------|-------------|-------------------|
| **Free** | Core functionality for all users | C-01, C-02, C-03, C-04, C-05, C-06, C-08, C-14, C-16, C-17, C-18, C-19, C-23, C-25 |
| **Pro** | Advanced features for growing teams | C-07 (full), C-09, C-10 (full), C-12, C-13, C-15, C-20, C-22, C-24 |
| **Enterprise** | White-label, compliance, data residency | C-11, C-13 (full), C-15 (full), C-21 |

## 2.5 Feature Dependencies

```
C-01 (Organizations) ──┬── C-02 (One-Click Create)
                       ├── C-03 (Invite Members)
                       ├── C-17 (Permissions)
                       ├── C-12 (Billing)
                       └── C-22 (Feature Flags)

C-04 (Offline) ────────┬── C-05 (Real-Time)
                       └── C-16 (Background Jobs)

C-06 (UI Generation) ──┬── C-19 (Navigation)
                       └── C-18 (Theming)

C-13 (Compliance) ─────┬── C-20 (Audit Trail)
                       └── C-21 (Data Residency)

C-14 (Plugins) ────────┬── C-15 (Integrations)
                       └── C-24 (Fax Engine)
```

---

*End of Section 2*
# Section 3: Organization & Multi-Tenancy System

## 3.1 Overview

The Organization system is the foundation of Dartwing's multi-tenancy architecture. It enables unlimited organizations per user account with complete data isolation, sub-400ms context switching, and type-specific functionality through a hybrid model design.

**Related Features:** C-01, C-02, C-03, C-17

## 3.2 Hybrid Organization Model

Dartwing uses a **Hybrid Architecture** to solve the "God Object" problem while maintaining the benefits of a unified `Organization` entity.

### Design Pattern

1. **Organization (Thin Reference):** A lightweight shell holding shared identity (Name, Logo, Status) that acts as the target for all foreign keys
2. **Concrete Types:** Separate 1:1 linked doctypes (`Family`, `Company`, `Club`, `Nonprofit`) holding domain-specific data and validation logic

### Architecture Diagram

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
     │parental │      │ partners │      │amenities│      │ mission   │
     └─────────┘      └──────────┘      └─────────┘      └───────────┘
```

## 3.3 Organization Types

| Type | Module | Naming Series | Primary Use Cases |
|------|--------|---------------|-------------------|
| **Family** | dartwing_family | FAM-.##### | Households, personal life management, parental controls |
| **Company** | dartwing_company | CO-.##### | Businesses, LLCs, corporations, partnerships |
| **Club/Association** | dartwing_associations | CLB-.##### | HOAs, sports clubs, membership organizations |
| **Nonprofit** | dartwing_nonprofit | NPO-.##### | 501(c)(3), foundations, charities |

## 3.4 Feature Requirements

### C-01: Multi-Tenant Organizations

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-ORG-001 | Must | Users can belong to unlimited Organizations simultaneously |
| REQ-ORG-002 | Must | Complete data isolation between Organizations (no data leakage) |
| REQ-ORG-003 | Must | Context switching between Organizations completes in <400ms |
| REQ-ORG-004 | Must | Organization type (org_type) is immutable after creation |
| REQ-ORG-005 | Must | Bidirectional linking between Organization and concrete type maintained by server hooks |
| REQ-ORG-006 | Should | Organization deletion cascades to concrete type |
| REQ-ORG-007 | Should | Soft-delete support with status = "Dissolved" |

### C-02: One-Click Organization Creation

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-ORG-010 | Must | Organization creation completes in ≤3 seconds |
| REQ-ORG-011 | Must | Creating Organization auto-creates corresponding concrete type |
| REQ-ORG-012 | Must | Creator automatically added as Org Member with admin role |
| REQ-ORG-013 | Must | User Permission automatically created for creator |
| REQ-ORG-014 | Should | Organization creation wizard with type-specific fields |
| REQ-ORG-015 | Could | Template organizations for quick setup |

### C-03: Invite Members

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-ORG-020 | Must | Email invitation with secure token |
| REQ-ORG-021 | Must | QR code invitation for in-person onboarding (especially children) |
| REQ-ORG-022 | Must | Time-limited guest access with configurable expiration |
| REQ-ORG-023 | Must | Auto-join flow for new users (creates Person + Frappe User) |
| REQ-ORG-024 | Must | Invitation tracks status: Pending, Accepted, Expired, Revoked |
| REQ-ORG-025 | Should | Bulk invitation via CSV upload |
| REQ-ORG-026 | Should | Invitation reminders (automated re-send) |
| REQ-ORG-027 | Could | Invitation approval workflow for sensitive organizations |

## 3.5 Data Model

### Organization Doctype (Thin Shell)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| naming_series | Select | Yes | ORG-.YYYY.- |
| org_name | Data | Yes | Display name |
| org_type | Select | Yes | Family, Company, Nonprofit, Club/Association (set_only_once) |
| logo | Attach Image | No | Organization logo |
| status | Select | Yes | Active, Inactive, Dissolved (default: Active) |
| linked_doctype | Data | No | Auto-set: Family, Company, Club, Nonprofit |
| linked_name | Data | No | Auto-set: concrete document name |

### Concrete Type Fields

#### Family (dartwing_family)

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Back-reference (reqd, read_only) |
| family_nickname | Data | Casual family name |
| primary_residence | Link → Address | Main home address |
| parental_controls_enabled | Check | Enable child restrictions |
| screen_time_limit_minutes | Int | Daily limit (depends_on parental_controls) |

#### Company (dartwing_company)

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Back-reference |
| legal_name | Data | Official legal entity name |
| tax_id | Data | EIN / Tax ID |
| entity_type | Select | C-Corp, S-Corp, LLC, LP, LLP, WFOE, etc. |
| jurisdiction_country | Link → Country | Country of formation |
| jurisdiction_state | Data | State/Province |
| formation_date | Date | Date of incorporation |
| registered_address | Link → Address | Registered agent address |
| physical_address | Link → Address | Principal place of business |
| registered_agent | Link → Person | Registered agent contact |
| officers | Table → Organization Officer | Officers & Directors |
| members_partners | Table → Organization Member Partner | LLC/Partnership ownership |

#### Club (dartwing_associations)

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Back-reference |
| membership_tiers | Table → Organization Membership Tier | Tier definitions |
| default_dues_amount | Currency | Default annual dues |
| amenities | Small Text | Facilities description |
| clubhouse_address | Link → Address | Primary facility |

#### Nonprofit (dartwing_nonprofit)

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Back-reference |
| tax_exempt_status | Select | 501(c)(3), 501(c)(4), 501(c)(6), 501(c)(7), Other |
| ein | Data | Employer Identification Number |
| determination_date | Date | IRS determination letter date |
| fiscal_year_end | Select | Month (January-December) |
| mission_statement | Text | Organization mission |
| board_members | Table → Organization Officer | Board of Directors |
| registered_address | Link → Address | Official address |
| mailing_address | Link → Address | Correspondence address |

### Org Member Doctype

Links Person to Organization with role assignment.

| Field | Type | Description |
|-------|------|-------------|
| person | Link → Person | The individual |
| organization | Link → Organization | The organization |
| role | Link → Role Template | Assigned role |
| start_date | Date | Membership start (default: Today) |
| end_date | Date | Membership end (optional) |
| status | Select | Active, Inactive, Pending |

### Role Template Doctype

| Field | Type | Description |
|-------|------|-------------|
| role_name | Data | Unique role identifier |
| applies_to_org_type | Select | Family, Company, Nonprofit, Club/Association |
| is_supervisor | Check | Has supervisory permissions |
| default_hourly_rate | Currency | For Company type (depends_on) |

## 3.6 Server-Side Implementation

### Hook Configuration

```python
# dartwing_core/hooks.py
doc_events = {
    "Organization": {
        "after_insert": "dartwing_core.doctype.organization.organization.create_concrete_type",
        "on_trash": "dartwing_core.doctype.organization.organization.delete_concrete_type"
    }
}
```

### Integrity Guardrails

| Rule | Enforcement |
|------|-------------|
| org_type immutability | `set_only_once` field attribute + validate hook |
| Bidirectional link integrity | Server hooks maintain both directions |
| Cascade delete | on_trash hook deletes concrete type |
| Permission propagation | after_insert creates User Permission |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/resource/Organization` | POST | Create organization (triggers concrete type creation) |
| `/api/resource/Organization/{name}` | GET | Get organization with linked_doctype/linked_name |
| `/api/method/dartwing_core.organization.get_concrete_doc` | GET | Fetch concrete type document |
| `/api/method/dartwing_core.organization.get_organization_with_details` | GET | Merged Organization + concrete type payload |

## 3.7 Permission Model

### Permission Flow

```
User → Org Member → Organization → Concrete Type (Family/Company/Club/Nonprofit)
```

### Implementation

1. **Document-Level Permissions:** When Org Member created, add User Permission for Organization
2. **Concrete Type Inheritance:** Concrete types inherit access via `user_permission_dependant_doctype: Organization`
3. **Permission Query Hook:** Filter list views by user's accessible Organizations
4. **Role Hierarchy:**

| Frappe Role | Access Level | Description |
|-------------|--------------|-------------|
| System Manager | Full | Platform administrators |
| Dartwing Admin | Multi-Org | Can manage multiple organizations |
| Organization Admin | Single-Org | Full access to one organization |
| Dartwing User | Member | Standard member access |
| Dartwing Guest | Read-Only | Limited read access |

## 3.8 User Experience

### Organization Switcher

```
┌─────────────────────────────────────┐
│  Current: Smith Family              │
│  ─────────────────────────────────  │
│  🏠 Smith Family          ✓        │
│  🏢 Acme Corporation               │
│  🏢 Tech Startup LLC               │
│  ⛳ Riverside Golf Club            │
│  ─────────────────────────────────  │
│  [+ Create New Organization]        │
└─────────────────────────────────────┘
```

### Organization Creation Flow

```
Step 1: Select Type
┌─────────────────────────────────────┐
│  What type of organization?         │
│                                     │
│  [🏠 Family]  [🏢 Company]          │
│  [🏛 Nonprofit] [⛳ Club]           │
└─────────────────────────────────────┘

Step 2: Basic Info (type-specific)
┌─────────────────────────────────────┐
│  Organization Name: [____________]  │
│  (Type-specific fields appear)      │
│                                     │
│  [Cancel]              [Create →]   │
└─────────────────────────────────────┘

Step 3: Invite Members (optional)
┌─────────────────────────────────────┐
│  Invite your first members          │
│                                     │
│  [email@example.com        ] [Add]  │
│                                     │
│  [Skip for now]    [Send Invites]   │
└─────────────────────────────────────┘
```

## 3.9 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-ORG-01 | User can create Organization in ≤3 seconds | Performance test |
| AC-ORG-02 | Concrete type auto-created with correct back-reference | Integration test |
| AC-ORG-03 | org_type change after creation fails | Unit test |
| AC-ORG-04 | User can switch organizations in <400ms | Performance test |
| AC-ORG-05 | Data from Org A never visible in Org B context | Security test |
| AC-ORG-06 | Invitation email delivered within 30 seconds | Integration test |
| AC-ORG-07 | QR code scans and joins correctly on mobile | E2E test |
| AC-ORG-08 | Guest access expires at configured time | Unit test |
| AC-ORG-09 | Organization deletion cascades to concrete type | Integration test |
| AC-ORG-10 | User Permission created on Org Member insert | Integration test |

## 3.10 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Doctype JSON schemas | Architecture Doc, Section 3 |
| Server hooks implementation | Architecture Doc, Section 3.6 |
| Permission hooks | Architecture Doc, Section 8.2.1 |
| Org integrity guardrails | `docs/dartwing_core/org_integrity_guardrails.md` |

---

*End of Section 3*
# Section 4: Identity & Authentication

## 4.1 Overview

Dartwing uses **Keycloak** as the central Identity Provider (IdP) for all authentication, enabling Single Sign-On (SSO) across Flutter mobile apps, web apps, desktop apps, Frappe backend, and third-party integrations.

**Related Features:** C-03, C-13, C-17

## 4.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **Single Source of Truth** | Keycloak manages all user identities |
| **SSO Everywhere** | One login works across all Dartwing applications |
| **API-First** | All auth flows work via standard OAuth2/OIDC protocols |
| **Personal/Business Separation** | Users have distinct personal and organizational identities |
| **Zero Trust** | Every request is authenticated, tokens are short-lived |

## 4.3 Architecture

### High-Level Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                         │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│  Flutter Mobile │  Flutter Web    │  Flutter Desktop│  External Websites    │
│  (iOS/Android)  │  (PWA)          │  (macOS/Win/Lin)│  (React/Vue/etc)      │
└────────┬────────┴────────┬────────┴────────┬────────┴───────────┬───────────┘
         │                 │                 │                     │
         │         OAuth2 + PKCE / OIDC      │                     │
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEYCLOAK SERVER                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │    Clients      │  │  Identity       │  │  User           │             │
│  │ - dartwing-app  │  │  Providers      │  │  Federation     │             │
│  │ - frappe-api    │  │ - Google        │  │ - LDAP          │             │
│  │ - web-portal    │  │ - Apple         │  │ - SAML          │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ Token Validation / User Info
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRAPPE BACKEND                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Social Login Key (OIDC Client)                     │  │
│  │  - Validates tokens from Keycloak                                     │  │
│  │  - Creates/maps Frappe User from Keycloak identity                   │  │
│  │  - Syncs roles/permissions from Keycloak groups                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.4 Person Identity Model

The `Person` doctype is the canonical identity record linking Keycloak identity to Dartwing data.

### Person Doctype Contract

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| primary_email | Data | Yes | Yes | Main email address |
| keycloak_user_id | Data | No | Yes | Keycloak `sub` claim (nullable for local auth) |
| frappe_user | Link → User | No | Yes | Linked Frappe User account |
| first_name | Data | Yes | No | Given name |
| last_name | Data | No | No | Family name |
| mobile_no | Data | No | No | Phone with country-aware validation |
| personal_org | Link → Organization | No | No | Auto-created personal Family org |
| is_minor | Check | No | No | Under 18 flag |
| consent_captured | Check | No | No | Privacy consent obtained |
| consent_timestamp | Datetime | No | No | When consent was captured |
| source | Select | No | No | signup, invite, import |
| status | Select | No | No | Active, Inactive, Merged |

### Identity Constraints

| Constraint | Enforcement |
|------------|-------------|
| Email uniqueness | Database unique constraint |
| Keycloak ID uniqueness | Database unique constraint |
| Frappe User uniqueness | Database unique constraint |
| No deletion with Org Member links | Validate hook (use deactivate/merge instead) |
| Auto-create Frappe User | On insert if keycloak_user_id present and site config allows |

## 4.5 Authentication Flows

### 4.5.1 Authorization Code Flow with PKCE (Mobile/Web Apps)

Primary flow for Flutter mobile, web, and desktop apps.

```
┌──────────┐                              ┌──────────┐                              ┌──────────┐
│  Flutter │                              │ Keycloak │                              │  Frappe  │
│   App    │                              │  Server  │                              │  Backend │
└────┬─────┘                              └────┬─────┘                              └────┬─────┘
     │ 1. Generate code_verifier + code_challenge                                        │
     │                                         │                                         │
     │ 2. Open browser/webview                 │                                         │
     │────────────────────────────────────────►│                                         │
     │    GET /auth?response_type=code         │                                         │
     │        &client_id=dartwing-mobile       │                                         │
     │        &code_challenge={challenge}      │                                         │
     │        &code_challenge_method=S256      │                                         │
     │                                         │                                         │
     │ 3. User authenticates                   │                                         │
     │◄────────────────────────────────────────│                                         │
     │    Redirect with ?code={auth_code}      │                                         │
     │                                         │                                         │
     │ 4. Exchange code for tokens             │                                         │
     │────────────────────────────────────────►│                                         │
     │    POST /token with code_verifier       │                                         │
     │                                         │                                         │
     │◄────────────────────────────────────────│                                         │
     │    {access_token, refresh_token, id_token}                                        │
     │                                         │                                         │
     │ 5. Call Frappe API with Bearer token    │                                         │
     │─────────────────────────────────────────┼────────────────────────────────────────►│
     │                                         │ 6. Validate token with Keycloak         │
     │◄────────────────────────────────────────┼─────────────────────────────────────────│
     │    {data}                               │                                         │
```

### 4.5.2 Client Credentials Flow (Service-to-Service)

For backend services, background jobs, and integrations.

### 4.5.3 Social Login Providers

| Provider | Enabled | Trust Email | Scopes |
|----------|---------|-------------|--------|
| Google | Yes | Yes | openid, profile, email |
| Apple | Yes | Yes | openid, name, email |
| Facebook | Yes | No | email, public_profile |
| Microsoft | Yes | Yes | openid, profile, email |

## 4.6 Feature Requirements

### Authentication Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-AUTH-001 | Must | PKCE required for all public clients (S256 method) |
| REQ-AUTH-002 | Must | Access tokens expire in 5 minutes |
| REQ-AUTH-003 | Must | Refresh tokens valid for 30 days |
| REQ-AUTH-004 | Must | Tokens stored in platform secure storage (Keychain/Keystore) |
| REQ-AUTH-005 | Must | Automatic token refresh before expiration |
| REQ-AUTH-006 | Must | SSO session idle timeout: 30 minutes |
| REQ-AUTH-007 | Must | SSO session max lifespan: 10 hours |
| REQ-AUTH-008 | Should | Offline tokens for background sync |
| REQ-AUTH-009 | Should | Biometric unlock for mobile apps |

### Multi-Factor Authentication Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-MFA-001 | Must | Email OTP verification |
| REQ-MFA-002 | Must | TOTP authenticator app support |
| REQ-MFA-003 | Should | SMS OTP via Twilio |
| REQ-MFA-004 | Should | WebAuthn/FIDO2 support |
| REQ-MFA-005 | Should | Recovery codes (one-time use) |
| REQ-MFA-006 | Could | Organization-enforced MFA policies |

### Personal vs Business Identity Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-ID-001 | Must | Personal account created with personal email |
| REQ-ID-002 | Must | Personal Family organization auto-created at signup |
| REQ-ID-003 | Must | Business identity linked to same Person record |
| REQ-ID-004 | Must | Company has no access to personal org data |
| REQ-ID-005 | Should | Business email can be added as secondary identity |
| REQ-ID-006 | Should | Person merge for duplicate detection |

## 4.7 Token Lifecycle

| Token Type | Lifespan | Purpose | Storage |
|------------|----------|---------|---------|
| Access Token | 5 minutes | API authorization | Secure Storage |
| Refresh Token | 30 days | Obtain new access tokens | Secure Storage |
| ID Token | 5 minutes | User identity claims | Secure Storage |
| Offline Token | 30 days | Background refresh without user | Secure Storage |

### Token Refresh Flow

```
┌─────────────────────────────────┐
│   App Makes API Request         │
└─────────────┬───────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Access Token    │───── Valid ────────────────────┐
    │ Expired?        │                                │
    └────────┬────────┘                                │
             │ Yes                                     │
             ▼                                         │
    ┌─────────────────┐                                │
    │ Refresh Token   │───── Missing ──► Login Screen │
    │ Exists?         │                                │
    └────────┬────────┘                                │
             │ Yes                                     │
             ▼                                         │
    ┌─────────────────┐                                │
    │ Call Keycloak   │───── Fail ─────► Login Screen │
    │ /token endpoint │                                │
    └────────┬────────┘                                │
             │ Success                                 │
             ▼                                         │
    ┌─────────────────┐                                │
    │ Store new       │                                │
    │ access token    │◄───────────────────────────────┘
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Make API call   │
    └─────────────────┘
```

## 4.8 Signup & Invitation Flows

### Personal Signup Flow

1. User signs up with personal email (required)
2. Keycloak creates user, sends verification email
3. On first login callback:
   - Create Person with `primary_email`, `keycloak_user_id`
   - Create Frappe User with default roles (`Dartwing User`)
   - Create personal Organization (org_type = Family)
   - Link via `personal_org`
   - Add Org Member for personal org
   - Add User Permission for that org

### Business Invitation Flow

1. Org Admin invites email address
2. System looks up Person by `primary_email`
3. If Person exists:
   - Add Org Member with invited role
   - Add User Permission for organization
   - Send invitation email with deep link
4. If Person missing:
   - Create stub Person with status=Pending
   - Send Keycloak invitation email
5. On accept:
   - Set `keycloak_user_id` if not set
   - Map/create `frappe_user`
   - Activate Org Member
   - Add User Permission

### Identity Merge Flow

When duplicate Persons detected (same email or Keycloak ID):

1. Identify winner and loser records
2. Re-link all Org Members to winner
3. Re-link all documents to winner
4. Audit the merge action
5. Soft-delete loser (status = Merged)

## 4.9 Keycloak Configuration

### Realm Settings

| Setting | Value |
|---------|-------|
| registrationAllowed | true |
| registrationEmailAsUsername | true |
| verifyEmail | true |
| resetPasswordAllowed | true |
| loginWithEmailAllowed | true |
| duplicateEmailsAllowed | false |
| sslRequired | external |
| accessTokenLifespan | 300 (5 min) |
| ssoSessionIdleTimeout | 1800 (30 min) |
| ssoSessionMaxLifespan | 36000 (10 hours) |
| offlineSessionIdleTimeout | 2592000 (30 days) |

### Brute Force Protection

| Setting | Value |
|---------|-------|
| bruteForceProtected | true |
| failureFactor | 5 |
| permanentLockout | false |
| maxFailureWaitSeconds | 900 (15 min) |
| waitIncrementSeconds | 60 |

### Client Configuration

| Client | Type | PKCE | Redirect URIs |
|--------|------|------|---------------|
| dartwing-mobile | Public | S256 Required | io.dartwing.app://callback |
| dartwing-web | Public | S256 Required | https://app.dartwing.io/callback |
| frappe-backend | Confidential | N/A | /api/method/frappe.integrations.oauth2_logins.custom |

## 4.10 Frappe Integration

### Social Login Key Configuration

| Field | Value |
|-------|-------|
| provider_name | Keycloak |
| client_id | frappe-backend |
| base_url | https://auth.dartwing.io/realms/dartwing-prod |
| authorize_url | /protocol/openid-connect/auth |
| access_token_url | /protocol/openid-connect/token |
| api_endpoint | /protocol/openid-connect/userinfo |
| user_id_property | sub |
| user_email_property | email |

### Role Mapping

Keycloak groups map to Frappe roles via custom hook:

| Keycloak Group | Frappe Role |
|----------------|-------------|
| /dartwing/admins | System Manager |
| /dartwing/org-admins | Organization Admin |
| /dartwing/users | Dartwing User |

## 4.11 Security Considerations

| Concern | Mitigation |
|---------|------------|
| Token theft | Short-lived access tokens (5 min), secure storage |
| PKCE bypass | S256 method required, no fallback |
| Token in URL | Never pass tokens in query parameters |
| CORS attacks | Whitelist specific origins only |
| Brute force | Account lockout after 5 failures |
| Session hijacking | HTTPS only, secure cookies |

## 4.12 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-AUTH-01 | PKCE flow completes successfully on iOS | E2E test |
| AC-AUTH-02 | PKCE flow completes successfully on Android | E2E test |
| AC-AUTH-03 | Token refresh works before expiration | Unit test |
| AC-AUTH-04 | Expired refresh token redirects to login | Integration test |
| AC-AUTH-05 | Social login (Google) creates Person + User | Integration test |
| AC-AUTH-06 | MFA prompt appears when enabled | E2E test |
| AC-AUTH-07 | Personal org created on signup | Integration test |
| AC-AUTH-08 | Business invitation adds Org Member | Integration test |
| AC-AUTH-09 | Brute force lockout activates after 5 failures | Security test |
| AC-AUTH-10 | Logout clears all tokens and Keycloak session | E2E test |

## 4.13 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Full auth architecture | dartwing-auth-architecture.md |
| Person doctype contract | `docs/dartwing_core/person_doctype_contract.md` |
| Flutter AuthService | Architecture Doc, Section 6.2 |
| Keycloak configuration | Auth Architecture, Section 3 |

---

*End of Section 4*
# Section 5: Offline-First & Real-Time Sync

## 5.1 Overview

Dartwing implements an **offline-first architecture** ensuring full functionality without network connectivity, combined with **real-time collaboration** when online. This enables users to work seamlessly in low-connectivity environments while maintaining instant updates when connected.

**Related Features:** C-04, C-05, C-16

## 5.2 Design Goals

| Goal | Description |
|------|-------------|
| **100% Offline Capability** | All critical features work without network (forms, lists, signatures, camera) |
| **Deterministic Sync** | Predictable conflict handling with clear resolution paths |
| **Bounded Payloads** | Delta-based sync with pagination to prevent memory issues |
| **Org-Scoped Access** | Permission enforcement identical across REST, Socket.IO, and jobs |
| **Sub-500ms Updates** | Real-time changes propagate within 500ms when online |

## 5.3 Architecture

### Sync Flow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FLUTTER CLIENT                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Local SQLite   │  │  Sync Queue     │  │  Socket.IO      │             │
│  │  (Offline DB)   │  │  (Pending Ops)  │  │  (Real-Time)    │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                │                                            │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │   ONLINE?               │
                    └────────────┬────────────┘
                          Yes    │    No
                    ┌────────────┴────────────┐
                    ▼                         ▼
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│       FRAPPE BACKEND            │  │       LOCAL ONLY                │
│  ┌─────────────────┐            │  │  - Queue writes locally         │
│  │  Change Feed    │            │  │  - Read from SQLite             │
│  │  /sync.feed     │            │  │  - Show sync pending indicator  │
│  └─────────────────┘            │  │                                 │
│  ┌─────────────────┐            │  └─────────────────────────────────┘
│  │  Batch Upsert   │            │
│  │  /sync.upsert   │            │
│  └─────────────────┘            │
│  ┌─────────────────┐            │
│  │  Socket.IO      │            │
│  │  sync:<dt>:<org>│            │
│  └─────────────────┘            │
└─────────────────────────────────┘
```

## 5.4 Feature Requirements

### C-04: Offline-First Mobile Apps

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-SYNC-001 | Must | All CRUD operations work offline with local queue |
| REQ-SYNC-002 | Must | Local SQLite database for offline data storage |
| REQ-SYNC-003 | Must | Sync queue persisted durably (survives app restart) |
| REQ-SYNC-004 | Must | Background sync when connectivity restored |
| REQ-SYNC-005 | Must | Visual indicator for pending sync operations |
| REQ-SYNC-006 | Must | Attachment upload before metadata record |
| REQ-SYNC-007 | Should | Exponential backoff on sync failures (5xx, network errors) |
| REQ-SYNC-008 | Should | Stop retry after N attempts, surface error to user |
| REQ-SYNC-009 | Should | Delta retention: 30-day change log |
| REQ-SYNC-010 | Should | Full resync trigger for clients >30 days behind |

### C-05: Real-Time Collaboration

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-RT-001 | Must | Socket.IO connection for real-time updates |
| REQ-RT-002 | Must | Channel scoping: `sync:<doctype>:<org>` |
| REQ-RT-003 | Must | Org membership verified before channel subscription |
| REQ-RT-004 | Must | Connection dropped on role/org permission change |
| REQ-RT-005 | Must | Real-time updates propagate within 500ms |
| REQ-RT-006 | Should | Live presence indicators (who's viewing document) |
| REQ-RT-007 | Should | Live cursors for collaborative editing |
| REQ-RT-008 | Should | @mentions with instant notification |
| REQ-RT-009 | Could | Typing indicators |

## 5.5 API Specification

### Change Feed Endpoint

**Endpoint:** `GET /api/method/dartwing_core.sync.feed`

**Purpose:** Retrieve changes since last sync point

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| doctype | string | Yes | Doctype to fetch changes for |
| since | string | Yes | Timestamp or watermark from last sync |
| limit | int | No | Records per page (default: 100, max: 500) |
| org | string | Yes | Organization name for filtering |

**Response:**

```json
{
  "rows": [
    {
      "name": "DOC-00001",
      "modified": "2025-11-28T10:30:00Z",
      "docstatus": 0,
      "data": { /* full document fields */ },
      "deleted": false
    }
  ],
  "next_since": "2025-11-28T10:30:00Z",
  "has_more": true
}
```

### Batch Upsert Endpoint

**Endpoint:** `POST /api/method/dartwing_core.sync.upsert_batch`

**Purpose:** Submit queued offline operations

**Request Body:**

```json
{
  "operations": [
    {
      "doctype": "Task",
      "name": null,
      "data": { "title": "New Task", "status": "Open" },
      "client_ts": "2025-11-28T10:25:00Z",
      "op": "insert"
    },
    {
      "doctype": "Task",
      "name": "TASK-00001",
      "data": { "status": "Completed" },
      "client_ts": "2025-11-28T10:26:00Z",
      "op": "update"
    }
  ]
}
```

**Response:**

```json
{
  "results": [
    {
      "status": "success",
      "server_ts": "2025-11-28T10:30:05Z",
      "resolved_doc": { /* created document */ }
    },
    {
      "status": "conflict",
      "server_ts": "2025-11-28T10:30:06Z",
      "server_doc": { /* current server version */ },
      "client_doc": { /* submitted version */ }
    }
  ]
}
```

### Socket.IO Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| subscribe | Client → Server | `{ channel: "sync:Task:ORG-001" }` | Subscribe to changes |
| unsubscribe | Client → Server | `{ channel: "sync:Task:ORG-001" }` | Unsubscribe |
| delta | Server → Client | `{ name, modified, data, deleted }` | Document change |
| presence | Server → Client | `{ user, document, action }` | User presence update |

## 5.6 Conflict Resolution

### Three-Tier Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONFLICT DETECTED                            │
│        (server modified > client modified, values differ)        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TIER 1: AI SMART MERGE                         │
│  - LLM analyzes server_doc and client_doc                       │
│  - Returns merged JSON or null if uncertain                     │
│  - Success: Submit merged version with force=True               │
└─────────────────────────────┬───────────────────────────────────┘
                              │ Fail/Null
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TIER 2: HUMAN RESOLUTION                       │
│  - Display "Sync Conflict" banner                               │
│  - Show side-by-side diff                                       │
│  - Field-level picker for each conflict                         │
│  - User submits resolved version with force=True                │
└─────────────────────────────┬───────────────────────────────────┘
                              │ Disabled/Bypass
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TIER 3: LAST-WRITE-WINS                        │
│  - Accept latest timestamp blindly                              │
│  - Log overwrite in Version history                             │
│  - Used for low-value, high-velocity data only                  │
│  - Deletes (tombstones) always win over updates                 │
└─────────────────────────────────────────────────────────────────┘
```

### Conflict Resolution UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    ⚠️ SYNC CONFLICT                              │
│                                                                  │
│  This document was modified on another device.                   │
│                                                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐               │
│  │   SERVER VERSION    │  │   YOUR VERSION      │               │
│  ├─────────────────────┤  ├─────────────────────┤               │
│  │ Title: Buy groceries│  │ Title: Buy groceries│               │
│  │ Status: ○ Open      │  │ Status: ● Completed │  ◄─ Conflict │
│  │ Due: Nov 28         │  │ Due: Nov 28         │               │
│  │ Notes: eggs, milk   │  │ Notes: eggs, bread  │  ◄─ Conflict │
│  └─────────────────────┘  └─────────────────────┘               │
│                                                                  │
│  Choose which values to keep:                                    │
│                                                                  │
│  Status:  ○ Open (Server)   ● Completed (Yours)                 │
│  Notes:   ○ eggs, milk      ○ eggs, bread      ○ Custom: [___] │
│                                                                  │
│  [Cancel]                              [Resolve & Sync]          │
└─────────────────────────────────────────────────────────────────┘
```

## 5.7 Client Implementation

### Local Storage Architecture

| Storage | Technology | Purpose |
|---------|------------|---------|
| Document cache | SQLite (sqflite) | Offline document storage |
| Sync queue | SQLite | Pending operations (durable) |
| Sync metadata | Hive | Watermarks, sync state |
| Attachments | File system | Cached files |

### Sync Queue Entry

```dart
class SyncQueueEntry {
  final String id;           // UUID
  final String doctype;
  final String? documentName;
  final Map<String, dynamic> data;
  final DateTime clientTs;
  final SyncOperation op;    // insert, update, delete
  final int retryCount;
  final SyncStatus status;   // pending, syncing, conflict, failed
}
```

### Client Responsibilities

| Responsibility | Implementation |
|----------------|----------------|
| Maintain local queue | Durable SQLite storage with client_ts |
| Replay writes in order | FIFO processing, pause on conflict |
| Handle 409 Conflict | Surface conflict UI or defer |
| Apply incoming deltas | Idempotent application, ignore older than local |
| Attachments | Upload first, then send metadata with file reference |

## 5.8 Permission Enforcement

### Consistent Enforcement

| Access Path | Enforcement Point |
|-------------|-------------------|
| REST API | Permission query hook on feed/upsert |
| Socket.IO | Verify org membership before subscribe |
| Background Jobs | Shared permission utility on delta emit |

### Permission Checks

```python
# Shared utility used by REST, Socket.IO, and jobs
def check_org_access(user: str, org: str, doctype: str) -> bool:
    """
    Verify user has access to organization for specified doctype.
    """
    return frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Organization", "for_value": org}
    )
```

## 5.9 Observability

### Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| sync_queue_depth | Pending operations count | >1000 |
| conflict_rate | Conflicts per 1000 syncs | >5% |
| sync_5xx_rate | Server error rate | >1% |
| avg_delta_size | Average sync payload bytes | >1MB |
| sync_lag | `now - next_since` | >5 minutes |

### Logging

| Log Type | Contents |
|----------|----------|
| Request trace | Trace ID, org, doctype, operation |
| Sync audit | User, document, action, timestamp |
| Error log | Rejected upserts with reason |
| Conflict log | Both versions, resolution method |

### Alerts

| Condition | Severity | Action |
|-----------|----------|--------|
| Spike in conflicts | Warning | Investigate concurrent edits |
| Sustained lag >5 min | Critical | Check backend health |
| Failure to advance next_since | Critical | Possible sync deadlock |

## 5.10 Background Job Engine (C-16)

### Guaranteed Execution

| Feature | Description |
|---------|-------------|
| Job queue | Redis-backed with persistence |
| Retry logic | Exponential backoff, max 5 retries |
| Progress tracking | Real-time progress updates via Socket.IO |
| Timeout handling | Configurable per job type |
| Dead letter queue | Failed jobs for manual review |

### Common Job Types

| Job Type | Trigger | Typical Duration |
|----------|---------|------------------|
| OCR processing | Document upload | 5-30 seconds |
| Fax sending | API call | 30-120 seconds |
| PDF generation | Export request | 2-10 seconds |
| AI classification | Document upload | 3-15 seconds |
| Bulk sync | Full resync | 1-30 minutes |

### Progress UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Processing document...                                          │
│                                                                  │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░  35%                      │
│                                                                  │
│  ✓ Uploaded document                                            │
│  ✓ OCR extraction complete                                      │
│  ⟳ AI classification in progress...                             │
│  ○ Routing to inbox                                             │
│                                                                  │
│  [Cancel]                                                        │
└─────────────────────────────────────────────────────────────────┘
```

## 5.11 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-SYNC-01 | Create document offline, appears after sync | E2E test |
| AC-SYNC-02 | Update document offline, syncs correctly | E2E test |
| AC-SYNC-03 | Delete document offline, syncs correctly | E2E test |
| AC-SYNC-04 | Conflict detected when server version newer | Integration test |
| AC-SYNC-05 | AI merge resolves simple conflicts automatically | Integration test |
| AC-SYNC-06 | Human resolution UI shows correct diff | E2E test |
| AC-SYNC-07 | Real-time update received within 500ms | Performance test |
| AC-SYNC-08 | Socket unsubscribed on permission revocation | Security test |
| AC-SYNC-09 | Pagination continues until has_more=false | Integration test |
| AC-SYNC-10 | Full resync triggered for >30 day gap | Integration test |
| AC-SYNC-11 | Background job shows progress in UI | E2E test |
| AC-SYNC-12 | Failed job retries with exponential backoff | Unit test |

## 5.12 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Full sync specification | `docs/dartwing_core/offline_real_time_sync_spec.md` |
| Permission enforcement | Architecture Doc, Section 8.2 |
| Socket.IO configuration | Architecture Doc, Section 2.3 |
| Background jobs | Frappe documentation |

---

*End of Section 5*
# Section 6: UI Generation & Navigation

## 6.1 Overview

Dartwing's **Automatic Native UI Generation** transforms Frappe DocTypes into beautiful, native Flutter interfaces without manual coding. Combined with the **Navigation & Routing Framework**, this enables rapid development of cross-platform applications with consistent UX.

**Related Features:** C-06, C-18, C-19

## 6.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **Zero-Code UI** | Every DocType becomes native UI automatically |
| **Platform Adaptive** | iOS uses Cupertino, Android uses Material Design 3 |
| **Responsive** | Same code works across phone, tablet, web, desktop |
| **Consistent Navigation** | Dynamic menus adapt to role and organization type |
| **Deep Linkable** | Every screen accessible via URL/deep link |

## 6.3 Architecture

### DocType to Flutter Rendering Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRAPPE BACKEND                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    DocType JSON                              ││
│  │  - Field definitions                                         ││
│  │  - Validation rules                                          ││
│  │  - depends_on conditions                                     ││
│  │  - Permissions                                               ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │ GET /api/resource/{doctype}/meta
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FLUTTER CLIENT                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  DocType Parser                              ││
│  │  - Parse field metadata                                      ││
│  │  - Resolve depends_on expressions                            ││
│  │  - Build field widget map                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │               Widget Factory                                 ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           ││
│  │  │  Form   │ │  List   │ │ Kanban  │ │Calendar │           ││
│  │  │ Builder │ │ Builder │ │ Builder │ │ Builder │           ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘           ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Platform Adapter                                ││
│  │  iOS: Cupertino  │  Android: Material  │  Web: Adaptive    ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 6.4 Feature Requirements

### C-06: Automatic Native UI Generation

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-UI-001 | Must | All Frappe field types render as appropriate Flutter widgets |
| REQ-UI-002 | Must | Form view auto-generated from DocType metadata |
| REQ-UI-003 | Must | List view auto-generated with sortable columns |
| REQ-UI-004 | Must | Kanban view for DocTypes with status field |
| REQ-UI-005 | Must | Calendar view for DocTypes with date fields |
| REQ-UI-006 | Must | `depends_on` expressions evaluated for conditional visibility |
| REQ-UI-007 | Must | Field-level permissions respected (read_only, hidden) |
| REQ-UI-008 | Must | Validation rules enforced on client side |
| REQ-UI-009 | Should | Section and column breaks render correctly |
| REQ-UI-010 | Should | Child tables render as expandable/inline editors |
| REQ-UI-011 | Should | Link fields provide search/autocomplete |
| REQ-UI-012 | Could | Custom field renderers via plugin system |

### C-18: Theme & Branding Engine

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-THEME-001 | Must | Per-organization primary and accent colors |
| REQ-THEME-002 | Must | Logo displayed in app bar and splash screen |
| REQ-THEME-003 | Must | Dark mode support (follows system or manual toggle) |
| REQ-THEME-004 | Must | Theme changes apply instantly without restart |
| REQ-THEME-005 | Should | Custom fonts per organization |
| REQ-THEME-006 | Should | Theme preview before applying |
| REQ-THEME-007 | Could | CSS-level customization for web |

### C-19: Navigation & Routing Framework

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-NAV-001 | Must | Dynamic sidebar with role-based menu items |
| REQ-NAV-002 | Must | Bottom navigation for mobile (≤5 primary destinations) |
| REQ-NAV-003 | Must | Deep linking to any screen via URL |
| REQ-NAV-004 | Must | Back navigation works correctly across platforms |
| REQ-NAV-005 | Must | Organization switcher accessible from navigation |
| REQ-NAV-006 | Should | Breadcrumb navigation for nested views |
| REQ-NAV-007 | Should | Recent items quick access |
| REQ-NAV-008 | Should | Search from navigation bar |
| REQ-NAV-009 | Could | Customizable menu order per user |

## 6.5 Field Type Mapping

### Frappe to Flutter Widget Mapping

| Frappe Field Type | Flutter Widget | Notes |
|-------------------|----------------|-------|
| Data | TextField | Single line text |
| Text | TextField (multiline) | Expandable |
| Small Text | TextField (3 lines) | Fixed height |
| Text Editor | Rich text editor | HTML support |
| Int | TextField (numeric) | Integer only |
| Float | TextField (numeric) | Decimal allowed |
| Currency | CurrencyField | With currency symbol |
| Percent | Slider or TextField | 0-100 range |
| Check | Switch or Checkbox | Boolean |
| Select | Dropdown | Single selection |
| Link | Autocomplete | Search linked doctype |
| Dynamic Link | Autocomplete | Doctype selected first |
| Date | DatePicker | Platform native |
| Datetime | DateTimePicker | Platform native |
| Time | TimePicker | Platform native |
| Duration | DurationPicker | Hours:Minutes:Seconds |
| Attach | FilePicker | Upload/capture |
| Attach Image | ImagePicker | With preview |
| Signature | SignaturePad | Draw signature |
| Geolocation | MapPicker | Lat/Long selection |
| Color | ColorPicker | With preview |
| Rating | StarRating | 1-5 stars |
| Table | ChildTableEditor | Inline editing |
| Section Break | Divider + Header | Collapsible |
| Column Break | Row layout | Side-by-side |
| Tab Break | TabBar | Tabbed sections |

## 6.6 Conditional Field Visibility

### depends_on Expression Evaluation

The `depends_on` attribute controls field visibility based on document state.

**Supported Expressions:**

| Expression | Example | Description |
|------------|---------|-------------|
| Simple equality | `eval:doc.status=='Open'` | Field shown when status is Open |
| Inequality | `eval:doc.amount>1000` | Field shown when amount exceeds 1000 |
| Boolean check | `eval:doc.is_active` | Field shown when is_active is truthy |
| Negation | `eval:!doc.is_archived` | Field shown when not archived |
| Array includes | `eval:['A','B'].includes(doc.type)` | Field shown for types A or B |
| Compound | `eval:doc.status=='Open' && doc.priority=='High'` | Multiple conditions |

### Flutter Implementation

```dart
class DependsOnEvaluator {
  bool evaluate(String expression, Map<String, dynamic> doc) {
    // Parse 'eval:' prefix
    if (expression.startsWith('eval:')) {
      final expr = expression.substring(5);
      return _evaluateExpression(expr, doc);
    }
    return true; // Default visible
  }
}
```

## 6.7 View Types

### Form View

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Task Details                                    [Save] [⋮]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BASIC INFORMATION                                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Title *                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Complete quarterly report                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Status                          Priority                       │
│  ┌──────────────────┐           ┌──────────────────┐           │
│  │ In Progress    ▼ │           │ High           ▼ │           │
│  └──────────────────┘           └──────────────────┘           │
│                                                                  │
│  Due Date                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📅 November 30, 2025                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ASSIGNMENT                                                     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Assigned To                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔍 John Smith                                      ✕     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### List View

```
┌─────────────────────────────────────────────────────────────────┐
│  Tasks                                      [+ New] [🔍] [⋮]    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔍 Search tasks...                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  All (24)  Open (12)  In Progress (8)  Completed (4)           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ○ Complete quarterly report                    🔴 High   │  │
│  │   Due: Nov 30 • John Smith                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ○ Review marketing materials                   🟡 Medium │  │
│  │   Due: Dec 5 • Sarah Johnson                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ✓ Update team calendar                         🟢 Low    │  │
│  │   Completed: Nov 25 • Mike Wilson                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Kanban View

```
┌─────────────────────────────────────────────────────────────────┐
│  Tasks - Kanban                              [List] [Kanban ✓]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OPEN (5)        IN PROGRESS (3)    REVIEW (2)     DONE (8)    │
│  ──────────────  ────────────────   ───────────    ──────────  │
│  ┌────────────┐  ┌────────────┐     ┌───────────┐  ┌─────────┐ │
│  │ Task A     │  │ Task D     │     │ Task G    │  │ Task I  │ │
│  │ 🔴 High    │  │ 🟡 Medium  │     │ 🔴 High   │  │ ✓       │ │
│  │ Nov 28     │  │ Nov 30     │     │ Dec 1     │  │ Nov 25  │ │
│  └────────────┘  └────────────┘     └───────────┘  └─────────┘ │
│  ┌────────────┐  ┌────────────┐     ┌───────────┐  ┌─────────┐ │
│  │ Task B     │  │ Task E     │     │ Task H    │  │ Task J  │ │
│  │ 🟡 Medium  │  │ 🟢 Low     │     │ 🟡 Medium │  │ ✓       │ │
│  │ Dec 5      │  │ Dec 10     │     │ Dec 3     │  │ Nov 24  │ │
│  └────────────┘  └────────────┘     └───────────┘  └─────────┘ │
│  ┌────────────┐  ┌────────────┐                    ┌─────────┐ │
│  │ Task C     │  │ Task F     │                    │ ...     │ │
│  │ 🟢 Low     │  │ 🔴 High    │                    │         │ │
│  │ Dec 15     │  │ Nov 29     │                    │         │ │
│  └────────────┘  └────────────┘                    └─────────┘ │
│                                                                  │
│  [Drag cards to change status]                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Calendar View

```
┌─────────────────────────────────────────────────────────────────┐
│  Tasks - Calendar                    [< Nov 2025 >] [Month ▼]   │
├─────────────────────────────────────────────────────────────────┤
│  Sun     Mon     Tue     Wed     Thu     Fri     Sat           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  26      27      28      29      30      1       2              │
│          ┌─────┐ ┌─────┐         ┌─────┐                        │
│          │ 2   │ │🔴1  │         │ 3   │                        │
│          └─────┘ └─────┘         └─────┘                        │
│                                                                  │
│  3       4       5       6       7       8       9              │
│  ┌─────┐         ┌─────┐                 ┌─────┐                │
│  │🟡1  │         │ 2   │                 │ 1   │                │
│  └─────┘         └─────┘                 └─────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 6.8 Navigation Structure

### Mobile Navigation (Bottom Nav + Drawer)

```
┌─────────────────────────────────────────────────────────────────┐
│  ≡  Smith Family                              🔔 👤             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      [Main Content Area]                        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   🏠        📋        📅        💬        ⚙️                   │
│  Home     Tasks    Calendar   Chat    Settings                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Desktop/Web Navigation (Sidebar)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏠 Dartwing                                              🔔  👤 John Smith │
├──────────────────────┬──────────────────────────────────────────────────────┤
│                      │                                                       │
│  Smith Family    ▼   │                                                       │
│  ──────────────────  │                                                       │
│                      │              [Main Content Area]                      │
│  📊 Dashboard        │                                                       │
│  📋 Tasks            │                                                       │
│  📅 Calendar         │                                                       │
│  📁 Documents        │                                                       │
│  👥 Members          │                                                       │
│                      │                                                       │
│  ──────────────────  │                                                       │
│  MODULES             │                                                       │
│  ──────────────────  │                                                       │
│  📠 Fax              │                                                       │
│  💰 Budget           │                                                       │
│  🏥 Health           │                                                       │
│                      │                                                       │
│  ──────────────────  │                                                       │
│  ⚙️ Settings         │                                                       │
│  ❓ Help             │                                                       │
│                      │                                                       │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

### Deep Linking Routes

| Route Pattern | Screen | Example |
|---------------|--------|---------|
| `/` | Dashboard | Home screen |
| `/:doctype` | List view | `/Task` |
| `/:doctype/:name` | Form view | `/Task/TASK-00001` |
| `/:doctype/:name/edit` | Edit mode | `/Task/TASK-00001/edit` |
| `/:doctype/new` | Create form | `/Task/new` |
| `/settings` | Settings | App settings |
| `/org/:org` | Org dashboard | `/org/ORG-001` |

## 6.9 Platform Adaptations

| Platform | Navigation | Widgets | Special Features |
|----------|------------|---------|------------------|
| **iOS** | Tab bar, swipe back | CupertinoTextField, CupertinoButton | Haptic feedback, pull-to-refresh |
| **Android** | Bottom nav, back button | Material TextField, ElevatedButton | Edge-to-edge, predictive back |
| **Web** | Sidebar, breadcrumbs | Material (responsive) | Keyboard shortcuts, hover states |
| **Desktop** | Sidebar, menu bar | Material (dense) | Window management, system tray |

## 6.10 Theme Configuration

### Organization Theme Settings

| Setting | Type | Description |
|---------|------|-------------|
| primary_color | Color | Main brand color |
| accent_color | Color | Secondary/action color |
| logo_url | URL | Organization logo |
| logo_dark_url | URL | Logo for dark mode |
| font_family | String | Custom font name |
| dark_mode | Select | auto, light, dark |

### Theme Application

```dart
// Theme applied at organization context switch
final theme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: org.primaryColor,
    secondary: org.accentColor,
    brightness: org.darkMode == 'dark' ? Brightness.dark : Brightness.light,
  ),
  fontFamily: org.fontFamily,
);
```

## 6.11 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-UI-01 | DocType renders as form without code | Integration test |
| AC-UI-02 | All field types render correctly | Visual regression |
| AC-UI-03 | depends_on hides/shows fields correctly | Unit test |
| AC-UI-04 | List view displays with sorting | E2E test |
| AC-UI-05 | Kanban drag-and-drop updates status | E2E test |
| AC-UI-06 | Calendar shows items on correct dates | E2E test |
| AC-UI-07 | Theme changes apply instantly | E2E test |
| AC-UI-08 | Dark mode works correctly | Visual regression |
| AC-UI-09 | Deep link opens correct screen | E2E test |
| AC-UI-10 | Navigation adapts to platform | Visual regression |
| AC-UI-11 | Sidebar shows role-appropriate items | Integration test |
| AC-UI-12 | Organization switcher works | E2E test |

## 6.12 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Flutter project structure | Architecture Doc, Section 4.2 |
| Riverpod state management | Architecture Doc, Section 4.1 |
| go_router configuration | Flutter codebase |
| Platform adaptations | Architecture Doc, Section 4.4 |

---

*End of Section 6*
# Section 7: File Storage & Documents

## 7.1 Overview

Dartwing provides **Unified File Storage** with a single API abstraction across multiple cloud providers, combined with **Electronic Signature & Annotation** capabilities and **Document Export** features that work consistently across all vertical modules.

**Related Features:** C-07, C-08, C-23

## 7.2 Architecture

### Storage Abstraction Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUTTER CLIENT                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   Storage Service                            ││
│  │  upload() • download() • delete() • list() • getUrl()       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FRAPPE BACKEND                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Storage Router                               ││
│  │  Route to configured provider per organization               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   AWS S3    │      │Google Drive │      │  SharePoint │     │
│  │   Adapter   │      │   Adapter   │      │   Adapter   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  OneDrive   │      │   Dropbox   │      │    Local    │     │
│  │   Adapter   │      │   Adapter   │      │   Adapter   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## 7.3 Feature Requirements

### C-07: Unified File Storage

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-STOR-001 | Must | Single API for all storage operations |
| REQ-STOR-002 | Must | Support AWS S3 as default provider |
| REQ-STOR-003 | Must | Support Google Drive integration |
| REQ-STOR-004 | Must | Support SharePoint/OneDrive integration |
| REQ-STOR-005 | Must | Support Dropbox integration |
| REQ-STOR-006 | Must | Automatic virus scanning on upload |
| REQ-STOR-007 | Must | Per-organization storage configuration |
| REQ-STOR-008 | Must | Pre-signed URLs for secure download |
| REQ-STOR-009 | Should | Per-file encryption keys (Zero Trust) |
| REQ-STOR-010 | Should | Storage usage metering per organization |
| REQ-STOR-011 | Should | Automatic thumbnail generation for images |
| REQ-STOR-012 | Should | File type validation and restrictions |
| REQ-STOR-013 | Could | CDN integration for faster delivery |
| REQ-STOR-014 | Could | Deduplication for identical files |

### C-08: Electronic Signature & Annotation

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-SIGN-001 | Must | Draw signature with finger/stylus |
| REQ-SIGN-002 | Must | Type signature with font selection |
| REQ-SIGN-003 | Must | Upload signature image |
| REQ-SIGN-004 | Must | Save signature for reuse |
| REQ-SIGN-005 | Must | Legally-binding signature with timestamp |
| REQ-SIGN-006 | Must | Signature audit trail |
| REQ-SIGN-007 | Must | Highlight annotation tool |
| REQ-SIGN-008 | Must | Stamp/badge annotation |
| REQ-SIGN-009 | Must | Redaction tool (permanent removal) |
| REQ-SIGN-010 | Should | Text annotation/comments |
| REQ-SIGN-011 | Should | Shape annotations (arrows, boxes) |
| REQ-SIGN-012 | Should | Multi-page PDF navigation |
| REQ-SIGN-013 | Could | Collaborative annotation (real-time) |

### C-23: Emergency Binder / Export Generator

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-EXPORT-001 | Must | One-tap PDF export of critical data |
| REQ-EXPORT-002 | Must | Beautiful, professional formatting |
| REQ-EXPORT-003 | Must | Configurable sections to include |
| REQ-EXPORT-004 | Must | Secure PDF with optional password |
| REQ-EXPORT-005 | Should | Include attached documents |
| REQ-EXPORT-006 | Should | Export to cloud storage |
| REQ-EXPORT-007 | Should | Scheduled automatic exports |
| REQ-EXPORT-008 | Could | Print-ready layout options |

## 7.4 Storage Provider Configuration

### Provider Settings per Organization

| Provider | Required Settings | Optional Settings |
|----------|-------------------|-------------------|
| **AWS S3** | bucket, region, access_key, secret_key | endpoint (for S3-compatible) |
| **Google Drive** | client_id, client_secret, refresh_token | folder_id |
| **SharePoint** | tenant_id, client_id, client_secret, site_url | library_name |
| **OneDrive** | client_id, client_secret, refresh_token | folder_path |
| **Dropbox** | access_token | folder_path |
| **Local** | base_path | max_size_mb |

### Storage Configuration Doctype

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Target organization |
| provider | Select | aws_s3, google_drive, sharepoint, onedrive, dropbox, local |
| is_default | Check | Default for new uploads |
| config | JSON | Provider-specific settings (encrypted) |
| max_file_size_mb | Int | Maximum file size limit |
| allowed_extensions | Data | Comma-separated list (e.g., pdf,doc,jpg) |
| virus_scan_enabled | Check | Enable ClamAV scanning |

## 7.5 File Operations API

### Upload Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Client     │     │   Backend    │     │  Virus Scan  │     │   Storage    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │                    │
       │  1. Request upload URL                  │                    │
       │───────────────────►│                    │                    │
       │                    │                    │                    │
       │  2. Pre-signed URL │                    │                    │
       │◄───────────────────│                    │                    │
       │                    │                    │                    │
       │  3. Upload directly to storage          │                    │
       │─────────────────────────────────────────┼───────────────────►│
       │                    │                    │                    │
       │  4. Confirm upload │                    │                    │
       │───────────────────►│                    │                    │
       │                    │  5. Scan file      │                    │
       │                    │───────────────────►│                    │
       │                    │                    │                    │
       │                    │  6. Scan result    │                    │
       │                    │◄───────────────────│                    │
       │                    │                    │                    │
       │  7. File record created                 │                    │
       │◄───────────────────│                    │                    │
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/method/dartwing_core.storage.get_upload_url` | POST | Get pre-signed upload URL |
| `/api/method/dartwing_core.storage.confirm_upload` | POST | Confirm upload and create File record |
| `/api/method/dartwing_core.storage.get_download_url` | GET | Get pre-signed download URL |
| `/api/method/dartwing_core.storage.delete_file` | DELETE | Delete file from storage |
| `/api/method/dartwing_core.storage.list_files` | GET | List files for document |

### File Doctype

| Field | Type | Description |
|-------|------|-------------|
| file_name | Data | Original filename |
| file_url | Data | Storage URL or key |
| file_size | Int | Size in bytes |
| file_type | Data | MIME type |
| is_private | Check | Requires authentication |
| attached_to_doctype | Link | Parent doctype |
| attached_to_name | Data | Parent document name |
| storage_provider | Select | Which provider stores this file |
| virus_scan_status | Select | pending, clean, infected, error |
| checksum | Data | SHA-256 hash |

## 7.6 Electronic Signature

### Signature Capture UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Sign Document                                           [Done] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Draw]  [Type]  [Upload]                                       │
│  ━━━━━━                                                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                                                              ││
│  │                                                              ││
│  │                    [Draw signature here]                     ││
│  │                                                              ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Clear]                                                        │
│                                                                  │
│  ☑ Save this signature for future use                          │
│                                                                  │
│  By signing, you agree to the terms and conditions.             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Signature Record Doctype

| Field | Type | Description |
|-------|------|-------------|
| document_doctype | Data | Signed document type |
| document_name | Data | Signed document name |
| signer | Link → Person | Who signed |
| signature_image | Attach Image | Signature capture |
| signature_type | Select | draw, type, upload |
| signed_at | Datetime | Timestamp |
| ip_address | Data | Signer's IP |
| user_agent | Data | Browser/device info |
| certificate_hash | Data | Digital certificate |

### Signature Validation

| Check | Description |
|-------|-------------|
| Identity verification | Signer authenticated via Keycloak |
| Timestamp | Server-side timestamp (not client) |
| Document hash | SHA-256 of document at signing time |
| Audit trail | Immutable record in audit log |
| Certificate | Optional PKI certificate attachment |

## 7.7 Annotation Tools

### Annotation Types

| Tool | Icon | Description | Behavior |
|------|------|-------------|----------|
| Highlight | 🖍️ | Yellow highlight | Semi-transparent overlay |
| Redact | ⬛ | Permanent removal | Black box, removes underlying data |
| Stamp | 🔖 | Badge/label | APPROVED, REJECTED, CONFIDENTIAL, etc. |
| Text | 💬 | Comment | Sticky note with text |
| Arrow | ➜ | Pointer | Draw attention to area |
| Rectangle | ▢ | Box | Outline area |
| Freehand | ✏️ | Drawing | Free-form markup |

### Annotation UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Document Viewer                          [Save] [Print] [⋮]    │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  🖍️  ⬛  🔖  💬  ➜  ▢  ✏️  │  Page 1 of 5  │  ◀  ▶  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │    INVOICE                        ┌─────────────────────┐ │  │
│  │                                   │ 🔖 APPROVED         │ │  │
│  │    Invoice #: 12345               └─────────────────────┘ │  │
│  │    Date: Nov 28, 2025                                     │  │
│  │                                                            │  │
│  │    ┌──────────────────────────────────────────────────┐   │  │
│  │    │ █████████████████████████ (Highlighted)          │   │  │
│  │    └──────────────────────────────────────────────────┘   │  │
│  │                                                            │  │
│  │    Total: $1,234.56                                       │  │
│  │                                                            │  │
│  │    ┌─────────────────────┐                                │  │
│  │    │ ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛ │ (Redacted)                    │  │
│  │    └─────────────────────┘                                │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Annotations (3)                                          [+]   │
│  ─────────────────────────────────────────────────────────────  │
│  • Highlight on page 1 - John Smith, Nov 28                     │
│  • Stamp "APPROVED" on page 1 - Sarah Johnson, Nov 28           │
│  • Redaction on page 1 - John Smith, Nov 28                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Annotation Record Doctype

| Field | Type | Description |
|-------|------|-------------|
| document_doctype | Data | Annotated document type |
| document_name | Data | Annotated document name |
| page_number | Int | Page containing annotation |
| annotation_type | Select | highlight, redact, stamp, text, arrow, rectangle, freehand |
| coordinates | JSON | Position and size `{x, y, width, height}` |
| content | Data | Text content (for text, stamp) |
| color | Color | Annotation color |
| created_by | Link → User | Who created |
| created_at | Datetime | When created |

## 7.8 Emergency Binder / Export

### Export Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│  Generate Emergency Binder                              [×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Select sections to include:                                    │
│                                                                  │
│  ☑ Family Members & Emergency Contacts                          │
│  ☑ Medical Information                                          │
│  ☑ Insurance Policies                                           │
│  ☑ Important Documents (Wills, Deeds)                           │
│  ☐ Financial Accounts                                           │
│  ☑ Pet Information                                              │
│  ☐ Vehicle Information                                          │
│  ☑ Home Systems & Passwords                                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Security Options:                                              │
│  ☑ Password protect PDF                                         │
│    Password: [••••••••••••]                                     │
│                                                                  │
│  Output:                                                        │
│  ○ Download PDF                                                 │
│  ● Save to Google Drive                                         │
│  ○ Email to: [_______________________]                          │
│                                                                  │
│  [Cancel]                              [Generate Binder]        │
└─────────────────────────────────────────────────────────────────┘
```

### Export Template System

| Template | Org Type | Sections |
|----------|----------|----------|
| Family Emergency Binder | Family | Contacts, Medical, Insurance, Documents, Pets |
| Business Continuity | Company | Contacts, Procedures, Accounts, Vendors |
| Patient Records | Health | Demographics, Conditions, Medications, Providers |
| Legal Matter Summary | Legal | Case Info, Parties, Documents, Timeline |

### Generated PDF Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    SMITH FAMILY                                  │
│                  Emergency Binder                                │
│                                                                  │
│              Generated: November 28, 2025                        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TABLE OF CONTENTS                                              │
│  ─────────────────────────────────────────────────────────────  │
│  1. Emergency Contacts ........................... 2            │
│  2. Family Members .............................. 4             │
│  3. Medical Information ......................... 6             │
│  4. Insurance Policies .......................... 10            │
│  5. Important Documents ......................... 14            │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. EMERGENCY CONTACTS                                          │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Primary Emergency Contact:                                     │
│  Name: Jane Smith                                               │
│  Relationship: Spouse                                           │
│  Phone: (555) 123-4567                                          │
│  ...                                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 7.9 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-STOR-01 | File uploads to configured S3 bucket | Integration test |
| AC-STOR-02 | File uploads to Google Drive | Integration test |
| AC-STOR-03 | Virus scan blocks infected file | Integration test |
| AC-STOR-04 | Pre-signed URL expires after timeout | Unit test |
| AC-STOR-05 | Storage usage metered correctly | Integration test |
| AC-SIGN-01 | Drawn signature saves correctly | E2E test |
| AC-SIGN-02 | Typed signature renders with font | E2E test |
| AC-SIGN-03 | Signature audit record created | Integration test |
| AC-SIGN-04 | Saved signature available for reuse | E2E test |
| AC-ANNOT-01 | Highlight annotation saves position | E2E test |
| AC-ANNOT-02 | Redaction permanently removes data | Security test |
| AC-ANNOT-03 | Stamp appears at correct location | E2E test |
| AC-EXPORT-01 | Emergency binder PDF generates | E2E test |
| AC-EXPORT-02 | Password-protected PDF requires password | Unit test |
| AC-EXPORT-03 | Export includes selected sections only | Integration test |

## 7.10 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Storage configuration | Site config / Organization settings |
| Virus scanning | ClamAV integration |
| PDF generation | ReportLab / WeasyPrint |
| Signature legal compliance | UETA/ESIGN compliance docs |

---

*End of Section 7*
# Section 8: Notifications & Communication

## 8.1 Overview

Dartwing provides a **Real-Time Notifications Engine** delivering alerts across multiple channels (push, SMS, email, in-app) with rule-based routing, combined with a **Fax-over-IP Engine** as a reusable primitive and a **Maintenance & Reminder Scheduler** for recurring tasks.

**Related Features:** C-10, C-24, C-25

## 8.2 Architecture

### Notification Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      EVENT TRIGGER                               │
│  Document Created/Updated • Mention • Deadline • Rule Match      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION ENGINE                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Rule Evaluator                            ││
│  │  - Match event against notification rules                   ││
│  │  - Determine recipients and channels                        ││
│  │  - Apply user preferences                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │    Push     │      │    Email    │      │     SMS     │     │
│  │   (FCM/APNs)│      │  (SendGrid) │      │  (Twilio)   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    In-App Center                             ││
│  │  - Notification list with read/unread state                 ││
│  │  - Deep links to source documents                           ││
│  │  - Badge count management                                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 8.3 Feature Requirements

### C-10: Real-Time Notifications Engine

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-NOTIF-001 | Must | Push notifications to iOS (APNs) and Android (FCM) |
| REQ-NOTIF-002 | Must | Email notifications with templates |
| REQ-NOTIF-003 | Must | SMS notifications via Twilio |
| REQ-NOTIF-004 | Must | In-app notification center |
| REQ-NOTIF-005 | Must | Rule-based notification triggers |
| REQ-NOTIF-006 | Must | @mention notifications |
| REQ-NOTIF-007 | Must | User notification preferences (opt-out per channel) |
| REQ-NOTIF-008 | Must | Organization-level notification settings |
| REQ-NOTIF-009 | Should | Keyword-based triggers |
| REQ-NOTIF-010 | Should | Urgency/priority escalation |
| REQ-NOTIF-011 | Should | Quiet hours / Do Not Disturb |
| REQ-NOTIF-012 | Should | Notification grouping/batching |
| REQ-NOTIF-013 | Could | Voice call alerts for critical events |
| REQ-NOTIF-014 | Could | Slack/Teams integration |

### C-24: Fax-over-IP Engine

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-FAX-001 | Must | Simple API: `DartwingFax.send(number, pdf)` |
| REQ-FAX-002 | Must | Multi-carrier abstraction (Telnyx, Bandwidth, SignalWire) |
| REQ-FAX-003 | Must | Delivery tracking and status updates |
| REQ-FAX-004 | Must | Retry on failure with exponential backoff |
| REQ-FAX-005 | Must | Delivery receipt / confirmation |
| REQ-FAX-006 | Should | Inbound fax receiving |
| REQ-FAX-007 | Should | Cover page generation |
| REQ-FAX-008 | Should | Fax queue management |
| REQ-FAX-009 | Could | Fax number provisioning |

### C-25: Maintenance & Reminder Scheduler

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-REMIND-001 | Must | Recurring task scheduling (daily/weekly/monthly/quarterly/yearly) |
| REQ-REMIND-002 | Must | Multi-channel reminders (push/email/SMS) |
| REQ-REMIND-003 | Must | One-tap task completion |
| REQ-REMIND-004 | Must | Overdue tracking and alerts |
| REQ-REMIND-005 | Should | Escalation for missed reminders |
| REQ-REMIND-006 | Should | Custom recurrence patterns |
| REQ-REMIND-007 | Should | Equipment maintenance integration |
| REQ-REMIND-008 | Could | Calendar integration (Google, Outlook) |

## 8.4 Notification Rules

### Notification Rule Doctype

| Field | Type | Description |
|-------|------|-------------|
| name | Data | Rule identifier |
| organization | Link → Organization | Scope (null = global) |
| enabled | Check | Active status |
| event_type | Select | created, updated, deleted, assigned, mentioned, deadline, custom |
| doctype_filter | Link → DocType | Apply to specific doctype |
| field_conditions | JSON | Field value conditions |
| keyword_triggers | Data | Comma-separated keywords |
| recipients | Select | owner, assigned_to, mentioned, role, custom |
| recipient_roles | Table MultiSelect | If recipients = role |
| recipient_custom | Data | Custom recipient logic |
| channels | MultiSelect | push, email, sms, in_app |
| priority | Select | low, normal, high, urgent |
| template | Link → Notification Template | Message template |

### Example Rules

| Rule | Event | Condition | Recipients | Channels |
|------|-------|-----------|------------|----------|
| New Task Assignment | Task.created | assigned_to is set | assigned_to | push, email |
| High Priority Alert | Task.updated | priority = High | owner, assigned_to | push, sms |
| Deadline Approaching | Task | due_date within 24h | assigned_to | push, email |
| Mention Notification | Any | @mention detected | mentioned user | push, in_app |
| Keyword Alert | Fax.created | contains "URGENT" | fax_admin role | push, sms |

### Notification Template Doctype

| Field | Type | Description |
|-------|------|-------------|
| name | Data | Template identifier |
| subject | Data | Email/push title (supports variables) |
| body_text | Text | Plain text body |
| body_html | Text Editor | HTML body for email |
| push_body | Data | Short push notification text |
| variables | Table | Available template variables |

### Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{doc.name}}` | Document name | TASK-00001 |
| `{{doc.title}}` | Document title field | Complete report |
| `{{doc.owner}}` | Document owner | John Smith |
| `{{user.full_name}}` | Current user name | Sarah Johnson |
| `{{org.org_name}}` | Organization name | Acme Corp |
| `{{link}}` | Deep link to document | dartwing://Task/TASK-00001 |

## 8.5 Notification Center UI

### Mobile Notification Center

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Notifications                              [Mark All Read]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TODAY                                                          │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ● Task Assigned                                   2m ago │  │
│  │   You've been assigned "Complete quarterly report"       │  │
│  │   by Sarah Johnson                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ● @Mentioned                                      15m ago│  │
│  │   John Smith mentioned you in a comment on               │  │
│  │   "Q3 Budget Review"                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ○ Deadline Reminder                               1h ago │  │
│  │   "Update team calendar" is due tomorrow                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  YESTERDAY                                                      │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ○ Fax Received                                   Yesterday│  │
│  │   New fax from +1 (555) 123-4567                         │  │
│  │   3 pages • Classified as "Invoice"                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### User Notification Preferences

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Notification Settings                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CHANNELS                                                       │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Push Notifications                              [━━━━━━●]  ON  │
│  Email Notifications                             [━━━━━━●]  ON  │
│  SMS Notifications                               [●━━━━━━]  OFF │
│                                                                  │
│  QUIET HOURS                                                    │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Enable Quiet Hours                              [━━━━━━●]  ON  │
│  From: [10:00 PM]  To: [7:00 AM]                               │
│                                                                  │
│  NOTIFICATION TYPES                                             │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Task Assignments              Push ☑  Email ☑  SMS ☐          │
│  @Mentions                     Push ☑  Email ☑  SMS ☐          │
│  Deadline Reminders            Push ☑  Email ☑  SMS ☑          │
│  Fax Received                  Push ☑  Email ☐  SMS ☐          │
│  Comments                      Push ☐  Email ☑  SMS ☐          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 8.6 Fax-over-IP Engine

### API Usage

```python
# Simple fax sending from any module
from dartwing_core.fax import DartwingFax

# Send a fax
result = DartwingFax.send(
    to="+15551234567",
    pdf="/path/to/document.pdf",
    organization="ORG-001",
    cover_page=True,
    callback_url="https://api.dartwing.io/fax/callback"
)

# Returns
{
    "fax_id": "FAX-2025-00001",
    "status": "queued",
    "estimated_delivery": "2025-11-28T10:35:00Z"
}
```

### Carrier Abstraction

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fax Router                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Organization Fax Settings:                                  ││
│  │  - Primary carrier: Telnyx                                  ││
│  │  - Failover: Bandwidth → SignalWire                         ││
│  │  - Numbers: [+1-555-FAX-0001, +1-555-FAX-0002]              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   Telnyx    │      │  Bandwidth  │      │ SignalWire  │     │
│  │   Adapter   │      │   Adapter   │      │   Adapter   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Fax Status Flow

```
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Queued │───►│Sending │───►│Delivered│   │ Failed │   │Cancelled│
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
                  │              ▲              ▲
                  │              │              │
                  └──────────────┴──────────────┘
                        (Retry on failure)
```

## 8.7 Maintenance & Reminder Scheduler

### Scheduled Task Doctype

| Field | Type | Description |
|-------|------|-------------|
| title | Data | Task description |
| organization | Link → Organization | Owner organization |
| assigned_to | Link → Person | Responsible person |
| recurrence | Select | once, daily, weekly, monthly, quarterly, yearly |
| recurrence_day | Int | Day of week (1-7) or month (1-31) |
| next_due | Date | Next occurrence date |
| reminder_before | Int | Hours before due to remind |
| reminder_channels | MultiSelect | push, email, sms |
| linked_equipment | Link → Equipment | For equipment maintenance |
| last_completed | Datetime | Last completion timestamp |
| status | Select | active, paused, completed |

### Reminder Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULER (Cron Job)                          │
│  Runs every 15 minutes                                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. Find tasks where:                                           │
│     - next_due - reminder_before <= now                         │
│     - status = active                                           │
│     - reminder not yet sent for this occurrence                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. For each task:                                              │
│     - Create Notification via Notification Engine               │
│     - Mark reminder as sent for this occurrence                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. On task completion:                                         │
│     - Update last_completed                                     │
│     - Calculate next_due based on recurrence                    │
│     - Reset reminder_sent flag                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Reminder UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Upcoming Reminders                                      [+ New]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TODAY                                                          │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔄 Change HVAC filter                           Due Today │  │
│  │    Monthly • Living Room HVAC                            │  │
│  │                                          [Done ✓] [Skip] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  THIS WEEK                                                      │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔄 Water indoor plants                          Due Fri  │  │
│  │    Weekly • All Plants                                   │  │
│  │                                          [Done ✓] [Skip] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔄 Review family budget                         Due Sat  │  │
│  │    Monthly • Family Finances                             │  │
│  │                                          [Done ✓] [Skip] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 8.8 Channel Integrations

### Push Notifications

| Platform | Service | Configuration |
|----------|---------|---------------|
| iOS | APNs | Team ID, Key ID, Auth Key |
| Android | FCM | Server Key, Project ID |

### Email

| Provider | Configuration |
|----------|---------------|
| SendGrid | API Key, From Address |
| Mailgun | API Key, Domain |
| SMTP | Host, Port, Username, Password |

### SMS

| Provider | Configuration |
|----------|---------------|
| Twilio | Account SID, Auth Token, From Number |
| Vonage | API Key, API Secret, From Number |

## 8.9 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-NOTIF-01 | Push notification delivered to iOS | E2E test |
| AC-NOTIF-02 | Push notification delivered to Android | E2E test |
| AC-NOTIF-03 | Email notification uses template | Integration test |
| AC-NOTIF-04 | SMS delivered via Twilio | Integration test |
| AC-NOTIF-05 | In-app notification appears in center | E2E test |
| AC-NOTIF-06 | @mention triggers notification | Integration test |
| AC-NOTIF-07 | Quiet hours suppresses notifications | Unit test |
| AC-NOTIF-08 | User preferences respected | Integration test |
| AC-FAX-01 | Fax sent via Telnyx | Integration test |
| AC-FAX-02 | Failover to Bandwidth works | Integration test |
| AC-FAX-03 | Delivery callback received | Integration test |
| AC-REMIND-01 | Recurring task created with next_due | Unit test |
| AC-REMIND-02 | Reminder sent at correct time | Integration test |
| AC-REMIND-03 | One-tap completion updates next_due | E2E test |
| AC-REMIND-04 | Overdue task shows alert | E2E test |

## 8.10 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Fax module details | dartwing-fax-prd.md |
| Background job execution | Section 5 (C-16) |
| Real-time events | Section 5 (Socket.IO) |

---

*End of Section 8*
# Section 9: Compliance & Security

## 9.1 Overview

Dartwing provides enterprise-grade **Compliance-Ready Mode** with one-toggle enablement for HIPAA, SOC 2, and GDPR requirements, combined with **Immutable Audit Trails**, **Data Residency Selection**, and a comprehensive **Role & Permission System** with row and field-level controls.

**Related Features:** C-13, C-17, C-20, C-21

## 9.2 Compliance Framework

### Supported Compliance Standards

| Standard | Scope | Key Requirements |
|----------|-------|------------------|
| **HIPAA** | Healthcare (US) | PHI protection, BAA, audit controls, encryption |
| **SOC 2** | Enterprise | Security controls, monitoring, incident response |
| **GDPR** | EU Data | Data portability, right to erasure, consent |
| **HITECH** | Healthcare (US) | Breach notification, enhanced penalties |
| **UETA/ESIGN** | Electronic Signatures | Legal validity of e-signatures |

### Compliance Mode Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 COMPLIANCE CONFIGURATION                         │
│                                                                  │
│  Organization Settings:                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ☑ HIPAA Mode Enabled                                       ││
│  │  ☑ SOC 2 Controls Active                                    ││
│  │  ☑ GDPR Compliance                                          ││
│  │  Data Region: [US-East ▼]                                   ││
│  │  BAA Status: ✓ Signed (Expires: Dec 2026)                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  ENCRYPTION     │  │  AUDIT TRAIL    │  │  DATA RESIDENCY │
│  AES-256 at rest│  │  S3 Object Lock │  │  Region-locked  │
│  TLS 1.3 transit│  │  7-year retain  │  │  storage        │
│  Per-file keys  │  │  Immutable logs │  │  Local backups  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## 9.3 Feature Requirements

### C-13: Compliance-Ready Mode

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-COMP-001 | Must | One-toggle HIPAA mode enablement |
| REQ-COMP-002 | Must | Business Associate Agreement (BAA) tracking |
| REQ-COMP-003 | Must | PHI handling controls and tagging |
| REQ-COMP-004 | Must | Encryption at rest (AES-256) |
| REQ-COMP-005 | Must | Encryption in transit (TLS 1.3) |
| REQ-COMP-006 | Must | Access logging for all PHI access |
| REQ-COMP-007 | Must | Automatic session timeout |
| REQ-COMP-008 | Should | SOC 2 control monitoring |
| REQ-COMP-009 | Should | GDPR consent management |
| REQ-COMP-010 | Should | Data portability export |
| REQ-COMP-011 | Should | Right to erasure workflow |
| REQ-COMP-012 | Could | Compliance dashboard and reports |

### C-17: Role & Permission System

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-PERM-001 | Must | Role-based access control (RBAC) |
| REQ-PERM-002 | Must | Organization-scoped permissions |
| REQ-PERM-003 | Must | Row-level security via User Permission |
| REQ-PERM-004 | Must | Field-level visibility (read_only, hidden) |
| REQ-PERM-005 | Must | Permission inheritance through concrete types |
| REQ-PERM-006 | Should | Department-based filtering |
| REQ-PERM-007 | Should | Location-based filtering |
| REQ-PERM-008 | Should | Custom role creation |
| REQ-PERM-009 | Should | Permission audit reports |
| REQ-PERM-010 | Could | Temporary elevated permissions |

### C-20: Immutable Audit Trail

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-AUDIT-001 | Must | Log all create/update/delete operations |
| REQ-AUDIT-002 | Must | Log all document views (for PHI) |
| REQ-AUDIT-003 | Must | Log authentication events |
| REQ-AUDIT-004 | Must | Immutable storage (S3 Object Lock) |
| REQ-AUDIT-005 | Must | 7-year minimum retention |
| REQ-AUDIT-006 | Must | Tamper-evident logging |
| REQ-AUDIT-007 | Should | Real-time audit stream |
| REQ-AUDIT-008 | Should | Audit search and filtering |
| REQ-AUDIT-009 | Should | Export for compliance auditors |
| REQ-AUDIT-010 | Could | Anomaly detection alerts |

### C-21: Data Residency Selection

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-RESID-001 | Must | Region selection at organization signup |
| REQ-RESID-002 | Must | US region (us-east, us-west) |
| REQ-RESID-003 | Must | EU region (eu-west, eu-central) |
| REQ-RESID-004 | Should | Canada region |
| REQ-RESID-005 | Should | Australia region |
| REQ-RESID-006 | Should | Data never leaves selected region |
| REQ-RESID-007 | Could | Multi-region replication for DR |

## 9.4 Permission System Architecture

### Permission Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION LAYERS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Frappe Role                                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  System Manager > Dartwing Admin > Org Admin > User > Guest ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 2: Organization Scope                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  User Permission: Allow "Organization" for "ORG-001"        ││
│  │  → Access limited to that organization's data               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 3: Role Template                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Org Member has Role "Family Admin" or "Employee"           ││
│  │  → Additional doctype-level permissions                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 4: Field-Level                                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  depends_on, read_only, hidden                              ││
│  │  → Individual field visibility/editability                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Role Definitions

| Role | Level | Capabilities |
|------|-------|--------------|
| **System Manager** | Platform | Full access to all organizations and settings |
| **Dartwing Admin** | Multi-Org | Can manage multiple organizations |
| **Organization Admin** | Single-Org | Full access within one organization |
| **Dartwing User** | Member | Standard member access based on Role Template |
| **Dartwing Guest** | Limited | Read-only access to specific documents |

### Permission Query Implementation

```python
# dartwing_core/permissions.py

def get_permission_query_conditions(user):
    """
    Filter queries to user's accessible organizations.
    Called by Frappe on all list queries.
    """
    if "System Manager" in frappe.get_roles(user):
        return ""  # No filter for admins

    # Get user's organizations
    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"  # No access

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabOrganization`.`name` IN ({org_list})"
```

## 9.5 Audit Trail System

### Audit Log Doctype

| Field | Type | Description |
|-------|------|-------------|
| timestamp | Datetime | Event time (server UTC) |
| user | Link → User | Who performed action |
| action | Select | create, read, update, delete, login, logout, export |
| doctype | Data | Affected document type |
| document_name | Data | Affected document |
| organization | Link → Organization | Organization context |
| ip_address | Data | Client IP |
| user_agent | Data | Browser/device info |
| old_value | JSON | Previous state (for updates) |
| new_value | JSON | New state (for creates/updates) |
| is_phi | Check | PHI access flag |
| checksum | Data | SHA-256 of log entry |
| previous_checksum | Data | Chain to previous entry |

### Audit Event Types

| Event | Trigger | Logged Data |
|-------|---------|-------------|
| Document Create | after_insert hook | New document values |
| Document Read | custom API wrapper | Document accessed |
| Document Update | on_update hook | Before/after values |
| Document Delete | on_trash hook | Deleted document |
| Login | auth callback | User, IP, success/fail |
| Logout | logout handler | User, session duration |
| Export | export API | What was exported |
| Permission Change | role assignment | Old/new permissions |
| PHI Access | PHI field access | Document, fields accessed |

### Immutable Storage

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUDIT STORAGE                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  S3 Object Lock (WORM)                       ││
│  │  - Governance mode for 7 years                              ││
│  │  - Objects cannot be deleted or modified                    ││
│  │  - Legal hold capability                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  Chain Integrity                             ││
│  │  Each log entry contains:                                   ││
│  │  - SHA-256 checksum of current entry                        ││
│  │  - SHA-256 checksum of previous entry                       ││
│  │  → Tamper detection via chain verification                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Audit Viewer UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Audit Log                                    [Export] [Filter] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Filters:                                                       │
│  [All Actions ▼] [All Users ▼] [Last 7 days ▼] [🔍 Search]     │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  Nov 28, 2025 10:45:23 AM                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 📝 UPDATE   Patient Record PAT-00123         🔒 PHI      │  │
│  │    User: Dr. Sarah Johnson                               │  │
│  │    Changed: diagnosis, medications                        │  │
│  │    IP: 192.168.1.100                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Nov 28, 2025 10:42:15 AM                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 👁 READ     Patient Record PAT-00123         🔒 PHI      │  │
│  │    User: Dr. Sarah Johnson                               │  │
│  │    IP: 192.168.1.100                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Nov 28, 2025 10:30:00 AM                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🔑 LOGIN    john.smith@acme.com                          │  │
│  │    IP: 203.0.113.45                                      │  │
│  │    Device: iPhone 15 Pro / Safari                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Load More...]                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 9.6 Encryption Architecture

### Encryption Layers

| Layer | Method | Key Management |
|-------|--------|----------------|
| **At Rest (Database)** | AES-256 | Database-level encryption |
| **At Rest (Files)** | AES-256-GCM | Per-file keys in KMS |
| **In Transit** | TLS 1.3 | Certificate rotation |
| **Backups** | AES-256 | Separate backup keys |

### Key Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    KEY HIERARCHY                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Master Key (HSM-protected)                                 ││
│  │  └── Organization Key                                       ││
│  │      └── Data Encryption Key (rotates monthly)              ││
│  │          └── Per-File Keys                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Key Storage: AWS KMS / Azure Key Vault / HashiCorp Vault       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 9.7 HIPAA-Specific Controls

### PHI Tagging

| PHI Element | Auto-Detection | Handling |
|-------------|----------------|----------|
| Patient Name | Yes (NER) | Encrypted, access logged |
| Date of Birth | Yes (Pattern) | Encrypted, access logged |
| SSN | Yes (Pattern) | Encrypted, masked display |
| Medical Record Number | Yes (Pattern) | Encrypted, access logged |
| Phone/Fax | Yes (Pattern) | Encrypted |
| Email | Yes (Pattern) | Encrypted |
| Address | Yes (NER) | Encrypted |
| Account Numbers | Yes (Pattern) | Encrypted, masked |
| Biometric | Manual tag | Encrypted |
| Photos | Manual tag | Encrypted |

### HIPAA Compliance Checklist

| Control | Implementation | Status |
|---------|----------------|--------|
| Access Controls | Role-based + MFA | ✓ |
| Audit Controls | Immutable logging | ✓ |
| Integrity Controls | Checksums, WORM | ✓ |
| Transmission Security | TLS 1.3 | ✓ |
| Encryption | AES-256 at rest | ✓ |
| BAA Management | Tracking doctype | ✓ |
| Breach Notification | Alert system | ✓ |
| Workforce Training | Training module | Planned |

## 9.8 Data Residency

### Available Regions

| Region Code | Location | Provider | Compliance |
|-------------|----------|----------|------------|
| us-east-1 | Virginia, USA | AWS | HIPAA, SOC 2 |
| us-west-2 | Oregon, USA | AWS | HIPAA, SOC 2 |
| eu-west-1 | Ireland | AWS | GDPR, SOC 2 |
| eu-central-1 | Frankfurt | AWS | GDPR, SOC 2 |
| ca-central-1 | Montreal | AWS | PIPEDA |
| ap-southeast-2 | Sydney | AWS | Privacy Act |

### Region Lock Implementation

```python
# Enforced at storage router level
class StorageRouter:
    def get_bucket(self, organization):
        region = frappe.db.get_value("Organization", organization, "data_region")
        return REGION_BUCKETS[region]
    
    def validate_region(self, organization, target_region):
        current = frappe.db.get_value("Organization", organization, "data_region")
        if current != target_region:
            frappe.throw("Data cannot be transferred outside configured region")
```

## 9.9 GDPR Compliance

### Data Subject Rights

| Right | Implementation |
|-------|----------------|
| **Right to Access** | Data export API, one-click download |
| **Right to Rectification** | Standard edit workflows |
| **Right to Erasure** | Deletion workflow with audit |
| **Right to Portability** | JSON/CSV export |
| **Right to Object** | Consent withdrawal |
| **Right to Restrict** | Processing pause |

### Consent Management

```
┌─────────────────────────────────────────────────────────────────┐
│  Privacy & Consent                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Your Data Rights                                               │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  [📥 Download My Data]  [🗑️ Delete My Account]                  │
│                                                                  │
│  Consent Settings                                               │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ☑ Essential cookies (required)                                 │
│  ☑ Analytics to improve service                                 │
│  ☐ Marketing communications                                     │
│  ☐ Third-party integrations                                     │
│                                                                  │
│  [Save Preferences]                                             │
│                                                                  │
│  Consent History                                                │
│  ─────────────────────────────────────────────────────────────  │
│  Nov 1, 2025 - Accepted Terms of Service                        │
│  Nov 1, 2025 - Opted in to Analytics                            │
│  Nov 15, 2025 - Opted out of Marketing                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 9.10 Security Controls

### Authentication Security

| Control | Implementation |
|---------|----------------|
| Password Policy | Min 12 chars, complexity requirements |
| MFA | Required for admin roles |
| Session Timeout | 30 min idle, 10 hour max |
| Brute Force Protection | 5 attempts, 15 min lockout |
| Token Security | Short-lived (5 min), secure storage |

### Network Security

| Control | Implementation |
|---------|----------------|
| TLS | 1.3 only, strong ciphers |
| CORS | Whitelist-only origins |
| CSP | Strict content security policy |
| Rate Limiting | Per-IP and per-user limits |
| DDoS Protection | CloudFlare / AWS Shield |

### Application Security

| Control | Implementation |
|---------|----------------|
| Input Validation | Server-side validation on all inputs |
| SQL Injection | Parameterized queries (Frappe ORM) |
| XSS | Output encoding, CSP |
| CSRF | Token validation |
| File Upload | Type validation, virus scanning |

## 9.11 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-COMP-01 | HIPAA mode enables all required controls | Integration test |
| AC-COMP-02 | BAA tracking creates valid record | Unit test |
| AC-COMP-03 | PHI auto-tagged on ingest | Integration test |
| AC-PERM-01 | User cannot access other org's data | Security test |
| AC-PERM-02 | Role permissions enforced on API | Integration test |
| AC-PERM-03 | Field-level permissions work | Unit test |
| AC-AUDIT-01 | All CRUD operations logged | Integration test |
| AC-AUDIT-02 | PHI access logged separately | Integration test |
| AC-AUDIT-03 | Audit logs immutable (Object Lock) | Security test |
| AC-AUDIT-04 | Chain integrity verifiable | Unit test |
| AC-RESID-01 | Data stored in selected region only | Infrastructure test |
| AC-RESID-02 | Cross-region transfer blocked | Security test |
| AC-GDPR-01 | Data export includes all user data | Integration test |
| AC-GDPR-02 | Account deletion removes all data | Integration test |
| AC-SEC-01 | TLS 1.3 enforced | Security scan |
| AC-SEC-02 | SQL injection blocked | Penetration test |

## 9.12 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Permission implementation | Architecture Doc, Section 8.2.1 |
| Keycloak security | dartwing-auth-architecture.md |
| PHI detection | dartwing-fax-prd.md, Module R |
| Encryption configuration | Infrastructure docs |

---

*End of Section 9*
# Section 10: Plugin & Module System

## 10.1 Overview

Dartwing's **Plugin / Module System** enables vertical applications (DartwingFax, DartwingFamily, DartwingLegal, etc.) to be installed as plugins on the same instance, with **Feature Flags** providing granular control over functionality at the organization or global level.

**Related Features:** C-14, C-22

## 10.2 Architecture

### Module Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DARTWING INSTANCE                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    DARTWING CORE                             ││
│  │  Organization • Person • Auth • Sync • Notifications        ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  dartwing   │      │  dartwing   │      │  dartwing   │     │
│  │    _fax     │      │   _family   │      │   _legal    │     │
│  │             │      │             │      │             │     │
│  │ • Fax Send  │      │ • Chores    │      │ • Cases     │     │
│  │ • Fax Recv  │      │ • Calendar  │      │ • Documents │     │
│  │ • AI Class  │      │ • Budget    │      │ • Billing   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   FLUTTER CLIENT                             ││
│  │  Module loader dynamically enables UI based on installed    ││
│  │  modules and organization settings                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 10.3 Feature Requirements

### C-14: Plugin / Module System

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-MOD-001 | Must | Modules installable via Frappe bench |
| REQ-MOD-002 | Must | Module discovery API for Flutter client |
| REQ-MOD-003 | Must | Per-organization module enablement |
| REQ-MOD-004 | Must | Module dependencies declared and validated |
| REQ-MOD-005 | Must | Module provides doctypes, APIs, and UI components |
| REQ-MOD-006 | Must | Modules inherit Core features (auth, sync, notifications) |
| REQ-MOD-007 | Should | Hot-reload module updates without restart |
| REQ-MOD-008 | Should | Module versioning and compatibility checks |
| REQ-MOD-009 | Should | Module marketplace listing |
| REQ-MOD-010 | Could | Third-party module support |

### C-22: Feature Flags Per Organization

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-FLAG-001 | Must | Global feature flags (all organizations) |
| REQ-FLAG-002 | Must | Per-organization feature overrides |
| REQ-FLAG-003 | Must | Instant flag changes without deployment |
| REQ-FLAG-004 | Must | Boolean, percentage, and variant flags |
| REQ-FLAG-005 | Should | A/B testing support |
| REQ-FLAG-006 | Should | Flag audit history |
| REQ-FLAG-007 | Should | Gradual rollout percentages |
| REQ-FLAG-008 | Could | User segment targeting |

## 10.4 Module Definition

### Module Manifest (hooks.py)

```python
# dartwing_fax/hooks.py

app_name = "dartwing_fax"
app_title = "Dartwing Fax"
app_publisher = "Dartwing Inc"
app_description = "Enterprise fax management for Dartwing"
app_version = "1.0.0"
app_color = "#3498db"
app_icon = "📠"

# Core dependency
required_apps = ["dartwing_core"]

# Module metadata for discovery
dartwing_module = {
    "name": "dartwing_fax",
    "title": "Fax",
    "icon": "📠",
    "color": "#3498db",
    "description": "Send, receive, and manage faxes with AI classification",
    "category": "communication",
    "tier": "pro",
    "org_types": ["Company", "Family", "Nonprofit"],  # Compatible org types
    "features": [
        {
            "id": "fax_send",
            "name": "Send Fax",
            "description": "Send faxes to any number",
            "flag": "fax.send_enabled"
        },
        {
            "id": "fax_receive",
            "name": "Receive Fax",
            "description": "Receive inbound faxes",
            "flag": "fax.receive_enabled"
        },
        {
            "id": "fax_ai",
            "name": "AI Classification",
            "description": "Automatic fax classification and routing",
            "flag": "fax.ai_enabled",
            "tier": "pro"
        }
    ],
    "navigation": [
        {
            "label": "Fax",
            "icon": "📠",
            "route": "/fax",
            "children": [
                {"label": "Inbox", "route": "/fax/inbox"},
                {"label": "Sent", "route": "/fax/sent"},
                {"label": "Numbers", "route": "/fax/numbers"}
            ]
        }
    ]
}
```

### Module Doctype

| Field | Type | Description |
|-------|------|-------------|
| name | Data | Module identifier (e.g., dartwing_fax) |
| title | Data | Display name |
| icon | Data | Emoji or icon class |
| color | Color | Brand color |
| description | Text | Module description |
| version | Data | Installed version |
| category | Select | communication, productivity, compliance, etc. |
| tier | Select | free, pro, enterprise |
| status | Select | installed, enabled, disabled |
| compatible_org_types | MultiSelect | Family, Company, Nonprofit, Club |

### Organization Module Doctype

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Target organization |
| module | Link → Module | Enabled module |
| enabled | Check | Active for this org |
| enabled_at | Datetime | When enabled |
| enabled_by | Link → User | Who enabled |
| settings | JSON | Module-specific org settings |

## 10.5 Module Discovery API

### Endpoint: Get Available Modules

```
GET /api/method/dartwing_core.modules.get_available_modules
```

**Response:**
```json
{
  "modules": [
    {
      "name": "dartwing_fax",
      "title": "Fax",
      "icon": "📠",
      "description": "Send, receive, and manage faxes",
      "version": "1.0.0",
      "tier": "pro",
      "installed": true,
      "enabled_for_org": true,
      "features": [
        {
          "id": "fax_send",
          "name": "Send Fax",
          "enabled": true
        },
        {
          "id": "fax_ai",
          "name": "AI Classification",
          "enabled": false,
          "reason": "Requires Pro tier"
        }
      ]
    },
    {
      "name": "dartwing_family",
      "title": "Family",
      "icon": "👨‍👩‍👧‍👦",
      "description": "Family life management",
      "version": "1.0.0",
      "tier": "free",
      "installed": true,
      "enabled_for_org": false,
      "reason": "Only available for Family org type"
    }
  ]
}
```

### Endpoint: Enable Module for Organization

```
POST /api/method/dartwing_core.modules.enable_module
Content-Type: application/json

{
  "organization": "ORG-001",
  "module": "dartwing_fax"
}
```

## 10.6 Feature Flags

### Feature Flag Doctype

| Field | Type | Description |
|-------|------|-------------|
| flag_key | Data | Unique identifier (e.g., fax.ai_enabled) |
| name | Data | Display name |
| description | Text | What this flag controls |
| flag_type | Select | boolean, percentage, variant |
| default_value | Data | Default state |
| global_override | Data | Global setting (overrides default) |
| is_internal | Check | Hidden from org admins |

### Organization Feature Flag Doctype

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Target organization |
| flag | Link → Feature Flag | The flag |
| value | Data | Organization-specific value |
| updated_at | Datetime | Last change |
| updated_by | Link → User | Who changed |

### Flag Resolution Logic

```python
def get_flag_value(flag_key: str, organization: str = None) -> any:
    """
    Resolve feature flag value with priority:
    1. Organization override (if exists)
    2. Global override (if set)
    3. Default value
    """
    flag = frappe.get_doc("Feature Flag", flag_key)
    
    # Check org override first
    if organization:
        org_flag = frappe.db.get_value(
            "Organization Feature Flag",
            {"organization": organization, "flag": flag_key},
            "value"
        )
        if org_flag is not None:
            return parse_flag_value(org_flag, flag.flag_type)
    
    # Check global override
    if flag.global_override:
        return parse_flag_value(flag.global_override, flag.flag_type)
    
    # Return default
    return parse_flag_value(flag.default_value, flag.flag_type)
```

### Feature Flag Types

| Type | Values | Use Case |
|------|--------|----------|
| **Boolean** | true/false | Simple on/off features |
| **Percentage** | 0-100 | Gradual rollouts |
| **Variant** | A/B/C... | A/B testing |

### Flag Evaluation API

```
GET /api/method/dartwing_core.flags.evaluate
?flags=fax.ai_enabled,fax.bulk_send,notifications.sms
&organization=ORG-001
```

**Response:**
```json
{
  "flags": {
    "fax.ai_enabled": true,
    "fax.bulk_send": false,
    "notifications.sms": true
  }
}
```

## 10.7 Flutter Module Loader

### Module Discovery Flow

```dart
class ModuleLoader {
  Future<List<DartwingModule>> loadModules() async {
    // 1. Fetch available modules from API
    final response = await api.getAvailableModules();
    
    // 2. Filter to enabled modules for current org
    final enabledModules = response.modules
        .where((m) => m.enabledForOrg)
        .toList();
    
    // 3. Load Flutter components for each module
    final loadedModules = <DartwingModule>[];
    for (final module in enabledModules) {
      final flutterModule = await _loadFlutterModule(module.name);
      if (flutterModule != null) {
        loadedModules.add(flutterModule);
      }
    }
    
    return loadedModules;
  }
  
  Future<DartwingModule?> _loadFlutterModule(String name) async {
    // Module registry maps name to Flutter implementation
    return ModuleRegistry.get(name);
  }
}
```

### Module Interface

```dart
abstract class DartwingModule {
  String get name;
  String get title;
  String get icon;
  
  /// Navigation items to add to sidebar/menu
  List<NavigationItem> get navigationItems;
  
  /// Routes this module provides
  List<GoRoute> get routes;
  
  /// Providers this module registers
  List<Override> get providers;
  
  /// Called when module is loaded
  Future<void> initialize();
  
  /// Called when entering this module's context
  Future<void> onEnter();
  
  /// Called when leaving this module's context
  Future<void> onExit();
}
```

### Dynamic Navigation

```dart
class NavigationBuilder {
  List<NavigationItem> buildNavigation(
    List<DartwingModule> modules,
    Organization org,
    User user,
  ) {
    final items = <NavigationItem>[];
    
    // Add core navigation
    items.addAll(coreNavigation);
    
    // Add module navigation
    for (final module in modules) {
      // Check if module is compatible with org type
      if (!module.supportsOrgType(org.orgType)) continue;
      
      // Check user permissions for module
      if (!user.hasModuleAccess(module.name)) continue;
      
      items.addAll(module.navigationItems);
    }
    
    return items;
  }
}
```

## 10.8 Module Administration UI

### Module Management Screen

```
┌─────────────────────────────────────────────────────────────────┐
│  Modules & Features                                      [?]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INSTALLED MODULES                                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 📠 Fax                                    v1.0.0   PRO   │  │
│  │    Send, receive, and manage faxes with AI                │  │
│  │                                                            │  │
│  │    Features:                                               │  │
│  │    ☑ Send Fax                              [━━━━━━●] ON   │  │
│  │    ☑ Receive Fax                           [━━━━━━●] ON   │  │
│  │    ☐ AI Classification                     [●━━━━━━] OFF  │  │
│  │      ↳ Requires Pro subscription                          │  │
│  │                                                            │  │
│  │    [Configure] [Disable Module]                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 👨‍👩‍👧‍👦 Family                                 v1.0.0   FREE  │  │
│  │    Family life management and coordination                │  │
│  │                                             [Enabled ✓]   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  AVAILABLE MODULES                                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ⚖️ Legal                                  v1.0.0   PRO   │  │
│  │    Legal case and matter management                       │  │
│  │                                              [Enable →]   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Feature Flag Admin

```
┌─────────────────────────────────────────────────────────────────┐
│  Feature Flags                               [+ New Flag]       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔍 [Search flags...]                                           │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  FLAG                        DEFAULT    GLOBAL    ORG COUNT     │
│  ─────────────────────────────────────────────────────────────  │
│  fax.ai_enabled              false      true      3 overrides   │
│  fax.bulk_send               false      false     0 overrides   │
│  notifications.sms           true       true      1 override    │
│  experimental.voice_ui       false      false     12 overrides  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Selected: fax.ai_enabled                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Type: Boolean                                            │  │
│  │  Default: false                                           │  │
│  │  Global Override: true                                    │  │
│  │                                                            │  │
│  │  Organization Overrides:                                  │  │
│  │  • ORG-001 (Acme Corp): false                            │  │
│  │  • ORG-015 (Beta Testers): true                          │  │
│  │  • ORG-022 (Test Org): false                             │  │
│  │                                                            │  │
│  │  [Edit] [View History]                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 10.9 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-MOD-01 | Module installed via bench command | Integration test |
| AC-MOD-02 | Module appears in discovery API | Integration test |
| AC-MOD-03 | Module enablement per organization works | Integration test |
| AC-MOD-04 | Module navigation appears when enabled | E2E test |
| AC-MOD-05 | Module routes accessible when enabled | E2E test |
| AC-MOD-06 | Module hidden when disabled | E2E test |
| AC-MOD-07 | Org type compatibility enforced | Unit test |
| AC-FLAG-01 | Boolean flag evaluates correctly | Unit test |
| AC-FLAG-02 | Org override takes precedence | Unit test |
| AC-FLAG-03 | Global override applies when no org override | Unit test |
| AC-FLAG-04 | Flag changes apply without restart | Integration test |
| AC-FLAG-05 | Percentage rollout distributes correctly | Statistical test |

## 10.10 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| Frappe app structure | Frappe documentation |
| Module hooks | hooks.py specification |
| Flutter module loading | Architecture Doc, Section 7.2 |

---

*End of Section 10*
# Section 11: Integrations & Marketplace

## 11.1 Overview

Dartwing provides **40+ Pre-Built Integrations** through a unified marketplace, enabling one-click connections to popular business applications. The integration framework supports OAuth2 connections, webhook automation, and bi-directional data sync.

**Related Features:** C-15

## 11.2 Architecture

### Integration Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                     INTEGRATION LAYER                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  Connection Manager                          ││
│  │  - OAuth2 token management                                  ││
│  │  - API key storage (encrypted)                              ││
│  │  - Connection health monitoring                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   Adapter Registry                           ││
│  ├─────────────┬─────────────┬─────────────┬───────────────────┤│
│  │ CRM         │ Accounting  │ Productivity│ Communication     ││
│  │ • Salesforce│ • QuickBooks│ • Google WS │ • Slack           ││
│  │ • HubSpot   │ • Xero      │ • Microsoft │ • Teams           ││
│  │ • Pipedrive │ • FreshBooks│ • Notion    │ • Discord         ││
│  └─────────────┴─────────────┴─────────────┴───────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   Sync Engine                                ││
│  │  - Bi-directional data mapping                              ││
│  │  - Conflict resolution                                      ││
│  │  - Scheduled sync jobs                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   Webhook Handler                            ││
│  │  - Incoming webhook processing                              ││
│  │  - Outgoing webhook dispatch                                ││
│  │  - Zapier/Make.com compatibility                            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 11.3 Feature Requirements

### C-15: Pre-Built Integrations Marketplace

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-INT-001 | Must | OAuth2 connection flow for supported apps |
| REQ-INT-002 | Must | Secure credential storage (encrypted) |
| REQ-INT-003 | Must | One-click connect from marketplace UI |
| REQ-INT-004 | Must | Connection status monitoring |
| REQ-INT-005 | Must | Disconnect and re-authorize flow |
| REQ-INT-006 | Should | Bi-directional data sync |
| REQ-INT-007 | Should | Field mapping configuration |
| REQ-INT-008 | Should | Sync scheduling (real-time, hourly, daily) |
| REQ-INT-009 | Should | Webhook support (incoming and outgoing) |
| REQ-INT-010 | Should | Zapier integration |
| REQ-INT-011 | Could | Custom integration builder |
| REQ-INT-012 | Could | Integration analytics and logs |

## 11.4 Integration Categories

### Category: CRM & Sales

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **Salesforce** | Enterprise | Bi-directional | Contacts, Accounts, Opportunities, Tasks |
| **HubSpot** | Pro | Bi-directional | Contacts, Companies, Deals, Tickets |
| **Pipedrive** | Pro | Bi-directional | Persons, Organizations, Deals |
| **Zoho CRM** | Pro | Bi-directional | Leads, Contacts, Accounts |

### Category: Accounting & Finance

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **QuickBooks Online** | Pro | Bi-directional | Invoices, Customers, Payments |
| **Xero** | Pro | Bi-directional | Invoices, Contacts, Bills |
| **FreshBooks** | Pro | Bi-directional | Clients, Invoices, Expenses |
| **Wave** | Free | Export only | Invoice export |

### Category: Productivity & Workspace

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **Google Workspace** | Free | Bi-directional | Drive, Calendar, Contacts, Gmail |
| **Microsoft 365** | Pro | Bi-directional | OneDrive, Outlook, Calendar, Teams |
| **Notion** | Pro | Bi-directional | Databases, Pages |
| **Airtable** | Pro | Bi-directional | Bases, Records |

### Category: Communication

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **Slack** | Pro | Bi-directional | Notifications, Commands, Channels |
| **Microsoft Teams** | Pro | Bi-directional | Notifications, Channels, Meetings |
| **Discord** | Free | Outgoing | Webhooks, Notifications |
| **Twilio** | Pro | Bi-directional | SMS, Voice, Fax |

### Category: Document & Signature

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **DocuSign** | Enterprise | Bi-directional | Send for signature, Status tracking |
| **Adobe Sign** | Enterprise | Bi-directional | Signature requests, Templates |
| **PandaDoc** | Pro | Bi-directional | Documents, Proposals |
| **HelloSign** | Pro | Bi-directional | Signature requests |

### Category: Cloud Storage

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **Google Drive** | Free | Bi-directional | File sync, Folder mapping |
| **Dropbox** | Free | Bi-directional | File sync, Sharing |
| **OneDrive** | Pro | Bi-directional | File sync, SharePoint |
| **Box** | Enterprise | Bi-directional | File sync, Governance |

### Category: Automation

| Integration | Tier | Sync Direction | Key Features |
|-------------|------|----------------|--------------|
| **Zapier** | Pro | Bi-directional | Triggers, Actions |
| **Make (Integromat)** | Pro | Bi-directional | Scenarios, Modules |
| **n8n** | Pro | Bi-directional | Workflows, Self-hosted |
| **Power Automate** | Enterprise | Bi-directional | Flows, Connectors |

## 11.5 Data Model

### Integration Doctype

| Field | Type | Description |
|-------|------|-------------|
| name | Data | Integration identifier (e.g., salesforce) |
| title | Data | Display name |
| category | Select | crm, accounting, productivity, etc. |
| icon | Attach Image | Integration logo |
| description | Text | What this integration does |
| tier | Select | free, pro, enterprise |
| auth_type | Select | oauth2, api_key, basic, webhook |
| oauth_config | JSON | OAuth2 settings (client_id, scopes, etc.) |
| supported_entities | JSON | What data types can sync |
| documentation_url | Data | Link to integration docs |

### Organization Integration Doctype

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Owner organization |
| integration | Link → Integration | The integration |
| status | Select | connected, disconnected, error |
| credentials | JSON | Encrypted tokens/keys |
| settings | JSON | Integration-specific settings |
| last_sync | Datetime | Last successful sync |
| sync_status | Select | idle, syncing, error |
| error_message | Text | Last error if any |
| connected_at | Datetime | When connected |
| connected_by | Link → User | Who connected |

### Sync Mapping Doctype

| Field | Type | Description |
|-------|------|-------------|
| org_integration | Link → Organization Integration | Parent connection |
| dartwing_doctype | Link → DocType | Local doctype |
| external_entity | Data | Remote entity name |
| direction | Select | push, pull, bidirectional |
| field_mappings | JSON | Field-to-field mappings |
| filters | JSON | Sync filters |
| sync_frequency | Select | realtime, hourly, daily, manual |
| enabled | Check | Active sync |

## 11.6 OAuth2 Flow

### Connection Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Flutter    │     │   Frappe     │     │   Provider   │
│   Client     │     │   Backend    │     │  (e.g. Slack)│
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │ 1. Click "Connect" │                    │
       │───────────────────►│                    │
       │                    │                    │
       │ 2. OAuth URL       │                    │
       │◄───────────────────│                    │
       │                    │                    │
       │ 3. Open browser/webview                 │
       │────────────────────────────────────────►│
       │                    │                    │
       │ 4. User authorizes │                    │
       │◄────────────────────────────────────────│
       │    (redirect with code)                 │
       │                    │                    │
       │ 5. Exchange code   │                    │
       │───────────────────►│                    │
       │                    │ 6. Token request   │
       │                    │───────────────────►│
       │                    │                    │
       │                    │ 7. Access token    │
       │                    │◄───────────────────│
       │                    │                    │
       │                    │ 8. Store encrypted │
       │                    │    credentials     │
       │                    │                    │
       │ 9. Connection ready│                    │
       │◄───────────────────│                    │
```

### Token Refresh

```python
class IntegrationManager:
    def get_access_token(self, org_integration: str) -> str:
        """
        Get valid access token, refreshing if needed.
        """
        doc = frappe.get_doc("Organization Integration", org_integration)
        credentials = self.decrypt_credentials(doc.credentials)
        
        # Check if token is expired
        if self.is_token_expired(credentials):
            # Refresh the token
            new_tokens = self.refresh_token(
                doc.integration,
                credentials['refresh_token']
            )
            
            # Update stored credentials
            doc.credentials = self.encrypt_credentials(new_tokens)
            doc.save()
            
            return new_tokens['access_token']
        
        return credentials['access_token']
```

## 11.7 Webhook System

### Incoming Webhooks

```
POST /api/method/dartwing_core.webhooks.receive
?integration=slack&organization=ORG-001&secret=abc123
```

**Processing Flow:**
1. Validate webhook signature/secret
2. Parse payload based on integration type
3. Route to appropriate handler
4. Execute configured actions
5. Return acknowledgment

### Outgoing Webhooks

| Event | Trigger | Payload |
|-------|---------|---------|
| document.created | After insert | Full document data |
| document.updated | After update | Changed fields |
| document.deleted | After delete | Document reference |
| fax.received | Inbound fax | Fax metadata |
| task.completed | Task done | Task details |

### Webhook Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│  Configure Webhook                                       [Save] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Webhook URL *                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ https://hooks.zapier.com/hooks/catch/123456/abcdef/         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Events to Send                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ Document Created                                             │
│  ☑ Document Updated                                             │
│  ☐ Document Deleted                                             │
│  ☑ Fax Received                                                 │
│  ☐ Task Completed                                               │
│                                                                  │
│  Filter by DocType                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Task, Fax Document                               [+ Add]    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Authentication                                                 │
│  ○ None                                                         │
│  ● Header: [X-Webhook-Secret] = [••••••••]                     │
│  ○ Basic Auth: [username] / [password]                         │
│                                                                  │
│  [Test Webhook]                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 11.8 Integration Marketplace UI

### Marketplace Browser

```
┌─────────────────────────────────────────────────────────────────┐
│  Integrations                                    [Connected: 5] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔍 [Search integrations...]                                    │
│                                                                  │
│  All  CRM  Accounting  Productivity  Communication  Storage     │
│  ━━━                                                            │
│                                                                  │
│  CONNECTED                                                      │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ [Slack]     │ │ [Google]    │ │ [QuickBooks]│              │
│  │ ✓ Connected │ │ ✓ Connected │ │ ✓ Connected │              │
│  │ [Manage]    │ │ [Manage]    │ │ [Manage]    │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                  │
│  AVAILABLE                                                      │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ [Salesforce]│ │ [HubSpot]   │ │ [DocuSign]  │              │
│  │ CRM         │ │ CRM         │ │ Signatures  │              │
│  │ ENTERPRISE  │ │ PRO         │ │ ENTERPRISE  │              │
│  │ [Connect]   │ │ [Connect]   │ │ [Connect]   │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ [Zapier]    │ │ [Dropbox]   │ │ [Xero]      │              │
│  │ Automation  │ │ Storage     │ │ Accounting  │              │
│  │ PRO         │ │ FREE        │ │ PRO         │              │
│  │ [Connect]   │ │ [Connect]   │ │ [Connect]   │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Management

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Slack Integration                          [Disconnect]      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STATUS                                                         │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ● Connected                                                    │
│  Connected: Nov 15, 2025 by John Smith                         │
│  Workspace: Acme Corp                                           │
│  Last Sync: 2 minutes ago                                       │
│                                                                  │
│  CONFIGURATION                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Default Channel for Notifications                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ #dartwing-alerts                                       ▼   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Send notifications for:                                        │
│  ☑ New fax received                                             │
│  ☑ Task assigned to me                                          │
│  ☐ Document comments                                            │
│  ☑ Urgent alerts                                                │
│                                                                  │
│  SYNC SETTINGS                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ☑ Sync Slack users to Dartwing contacts                        │
│     Frequency: [Daily ▼]                                        │
│     Last sync: Nov 28, 2025 6:00 AM                             │
│                                                                  │
│  [Save Settings]                [Sync Now]                      │
│                                                                  │
│  ACTIVITY LOG                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  • Nov 28 10:45 - Notification sent: New fax received           │
│  • Nov 28 10:30 - Notification sent: Task assigned              │
│  • Nov 28 06:00 - User sync completed: 24 contacts updated      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 11.9 Zapier Integration

### Zapier Triggers (Dartwing → Zapier)

| Trigger | Description |
|---------|-------------|
| New Document | When a document is created in any doctype |
| Updated Document | When a document is modified |
| New Fax Received | When an inbound fax arrives |
| Task Completed | When a task is marked done |
| New Organization Member | When someone joins the org |

### Zapier Actions (Zapier → Dartwing)

| Action | Description |
|--------|-------------|
| Create Document | Create a new document in any doctype |
| Update Document | Modify an existing document |
| Send Fax | Send a fax via Dartwing |
| Create Task | Create a new task |
| Add Comment | Add a comment to a document |

### Zapier App Configuration

```json
{
  "platformVersion": "1.0.0",
  "app": {
    "name": "Dartwing",
    "key": "dartwing",
    "authentication": {
      "type": "oauth2",
      "oauth2Config": {
        "authorizeUrl": "https://auth.dartwing.io/oauth/authorize",
        "accessTokenUrl": "https://auth.dartwing.io/oauth/token",
        "scope": "read write"
      }
    },
    "triggers": {
      "new_document": {
        "display": {"label": "New Document"},
        "operation": {
          "perform": "$func$zapier_triggers.new_document$"
        }
      }
    },
    "actions": {
      "create_document": {
        "display": {"label": "Create Document"},
        "operation": {
          "perform": "$func$zapier_actions.create_document$"
        }
      }
    }
  }
}
```

## 11.10 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-INT-01 | OAuth2 connection completes successfully | E2E test |
| AC-INT-02 | Credentials stored encrypted | Security test |
| AC-INT-03 | Token refresh works automatically | Integration test |
| AC-INT-04 | Disconnect removes credentials | Integration test |
| AC-INT-05 | Bi-directional sync creates/updates records | Integration test |
| AC-INT-06 | Field mapping applies correctly | Unit test |
| AC-INT-07 | Webhook received and processed | Integration test |
| AC-INT-08 | Outgoing webhook fires on event | Integration test |
| AC-INT-09 | Zapier trigger sends data | Integration test |
| AC-INT-10 | Zapier action creates document | Integration test |
| AC-INT-11 | Connection error displayed to user | E2E test |
| AC-INT-12 | Integration logs events correctly | Integration test |

## 11.11 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| OAuth2 implementation | dartwing-auth-architecture.md |
| Credential encryption | Section 9 (Security) |
| Background sync jobs | Section 5 (C-16) |

---

*End of Section 11*
# Section 12: AI & Voice Features

## 12.1 Overview

Dartwing provides **AI-First Design** with built-in AI personas, intelligent document processing, voice-first interfaces, and support for both cloud and local LLM deployments. These features are foundational capabilities inherited by all vertical modules.

**Related Features:** AI Persona Architecture (Architecture Doc Section 6), Additional Features Document

## 12.2 Architecture

### AI System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI LAYER                                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  AI Router                                   ││
│  │  Route requests to appropriate LLM based on:                ││
│  │  - Task type (classification, generation, extraction)       ││
│  │  - Privacy requirements (cloud vs local)                    ││
│  │  - Organization settings                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   Cloud     │      │   Local     │      │   Edge      │     │
│  │   LLM       │      │   LLM       │      │   LLM       │     │
│  │             │      │             │      │             │     │
│  │ • OpenAI    │      │ • Ollama    │      │ • On-device │     │
│  │ • Anthropic │      │ • Llama 3   │      │ • CoreML    │     │
│  │ • Gemini    │      │ • Mistral   │      │ • ONNX      │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  Knowledge Vault                             ││
│  │  Per-organization document repository for AI context        ││
│  │  - RAG indexing with embeddings                             ││
│  │  - Semantic search                                          ││
│  │  - Document chunking and vectorization                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  Tool Registry                               ││
│  │  AI can execute registered tools:                           ││
│  │  - API calls, database queries, workflow triggers           ││
│  │  - Role-based permission checks                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 12.3 Feature Requirements

### AI Persona System

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-AI-001 | Must | Built-in AI personas (Sales, Support, Admin) |
| REQ-AI-002 | Must | Organization-scoped AI context |
| REQ-AI-003 | Must | Knowledge Vault per organization |
| REQ-AI-004 | Must | Tool execution with permission checks |
| REQ-AI-005 | Should | Custom persona creation |
| REQ-AI-006 | Should | Persona behavior configuration |
| REQ-AI-007 | Could | Multi-persona conversations |

### Document AI

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-DOCAI-001 | Must | OCR for scanned documents |
| REQ-DOCAI-002 | Must | Document classification |
| REQ-DOCAI-003 | Must | Entity extraction (NER) |
| REQ-DOCAI-004 | Must | PHI detection for healthcare |
| REQ-DOCAI-005 | Should | Handwriting recognition (ICR) |
| REQ-DOCAI-006 | Should | Table extraction |
| REQ-DOCAI-007 | Should | Form field mapping |
| REQ-DOCAI-008 | Could | Multi-language support |

### Voice Interface

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-VOICE-001 | Should | Voice command input |
| REQ-VOICE-002 | Should | Natural language task creation |
| REQ-VOICE-003 | Should | Voice-to-text transcription |
| REQ-VOICE-004 | Could | Meeting transcription and summarization |
| REQ-VOICE-005 | Could | Voice response output |
| REQ-VOICE-006 | Could | Multi-language voice support |

### Local LLM Support

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-LOCAL-001 | Should | Ollama integration for self-hosted LLM |
| REQ-LOCAL-002 | Should | On-device inference for sensitive data |
| REQ-LOCAL-003 | Could | Model selection per organization |
| REQ-LOCAL-004 | Could | Hybrid cloud/local routing |

## 12.4 AI Persona Types

### Built-in Personas

| Persona | Purpose | Capabilities |
|---------|---------|--------------|
| **Sales Assistant** | Lead qualification, recommendations | Query CRM, generate quotes, schedule meetings |
| **Support Agent** | Ticket triage, FAQ responses | Search knowledge base, create tickets, escalate |
| **Admin Assistant** | Workflow automation, reporting | Run reports, trigger workflows, data validation |
| **Family Helper** | Family coordination (Family org type) | Schedule management, reminders, recommendations |

### Persona Configuration

```python
# Example: Sales Persona Configuration
{
    "name": "sales_assistant",
    "display_name": "Sales Assistant",
    "avatar": "👔",
    "description": "Helps with lead qualification and sales processes",
    "system_prompt": """You are a helpful sales assistant for {org_name}.
Your role is to help qualify leads, answer product questions, and 
assist with the sales process. You have access to the CRM data and 
can create quotes and schedule meetings.""",
    "available_tools": [
        "search_crm",
        "create_quote",
        "schedule_meeting",
        "send_email_draft"
    ],
    "knowledge_sources": [
        "product_catalog",
        "pricing_sheets",
        "sales_playbook"
    ],
    "org_types": ["Company"],
    "roles_required": ["Sales User", "Sales Manager"]
}
```

## 12.5 Knowledge Vault

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE VAULT                               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Document Ingestion                                          ││
│  │  PDF, DOCX, TXT, HTML, MD → Chunks → Embeddings             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Vector Database (per Organization)                          ││
│  │  • pgvector / Pinecone / Weaviate                           ││
│  │  • Embedding model: text-embedding-3-small                  ││
│  │  • Chunk size: 512 tokens with 50 token overlap             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  RAG Query Pipeline                                          ││
│  │  1. Embed user query                                        ││
│  │  2. Semantic search (top-k similar chunks)                  ││
│  │  3. Rerank results                                          ││
│  │  4. Inject context into LLM prompt                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Knowledge Source Doctype

| Field | Type | Description |
|-------|------|-------------|
| organization | Link → Organization | Owner organization |
| name | Data | Source identifier |
| title | Data | Display name |
| source_type | Select | document, webpage, database, api |
| source_url | Data | URL or file path |
| refresh_frequency | Select | manual, daily, weekly |
| last_indexed | Datetime | Last indexing time |
| chunk_count | Int | Number of chunks |
| status | Select | pending, indexed, error |

## 12.6 Tool Registry

### Tool Definition

```python
@frappe.whitelist()
def register_ai_tool(tool_config: dict):
    """
    Register a tool that AI personas can execute.
    """
    return frappe.get_doc({
        "doctype": "AI Tool",
        "name": tool_config["name"],
        "description": tool_config["description"],
        "parameters_schema": json.dumps(tool_config["parameters"]),
        "handler_method": tool_config["handler"],
        "required_permissions": tool_config.get("permissions", []),
        "org_types": tool_config.get("org_types", [])
    }).insert()

# Example tool registration
register_ai_tool({
    "name": "create_task",
    "description": "Create a new task in the system",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title"},
            "due_date": {"type": "string", "format": "date"},
            "assigned_to": {"type": "string", "description": "Person name"}
        },
        "required": ["title"]
    },
    "handler": "dartwing_core.ai.tools.create_task",
    "permissions": ["Dartwing User"]
})
```

### Tool Execution Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User       │     │   AI Engine  │     │   Tool       │
│   Request    │     │              │     │   Handler    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │ "Schedule meeting" │                    │
       │───────────────────►│                    │
       │                    │                    │
       │                    │ Parse intent       │
       │                    │ Select tool        │
       │                    │ Extract parameters │
       │                    │                    │
       │                    │ Check permissions  │
       │                    │───────────────────►│
       │                    │                    │
       │                    │                    │ Validate user
       │                    │                    │ has permission
       │                    │◄───────────────────│
       │                    │                    │
       │                    │ Execute tool       │
       │                    │───────────────────►│
       │                    │                    │
       │                    │                    │ Create calendar
       │                    │                    │ event
       │                    │◄───────────────────│
       │                    │                    │
       │ "Done! Meeting     │                    │
       │  scheduled for..." │                    │
       │◄───────────────────│                    │
```

## 12.7 Document AI Pipeline

### Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  DOCUMENT AI PIPELINE                            │
│                                                                  │
│  ┌─────────────┐                                                │
│  │  Document   │                                                │
│  │  Upload     │                                                │
│  └──────┬──────┘                                                │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────┐     ┌─────────────┐                            │
│  │  OCR        │────►│  Text       │                            │
│  │  (Tesseract)│     │  Extraction │                            │
│  └─────────────┘     └──────┬──────┘                            │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │Classification│     │   Entity    │     │    PHI     │       │
│  │  (LLM)      │     │  Extraction │     │  Detection │       │
│  │             │     │    (NER)    │     │            │       │
│  │ Invoice,    │     │ Names,Dates │     │ SSN, DOB,  │       │
│  │ Contract,   │     │ Amounts,    │     │ MRN, etc.  │       │
│  │ Resume...   │     │ Addresses   │     │            │       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Structured Output                                           ││
│  │  - document_type: "Invoice"                                 ││
│  │  - confidence: 0.95                                         ││
│  │  - entities: {vendor: "Acme", amount: "$1,234.56", ...}    ││
│  │  - phi_detected: false                                      ││
│  │  - suggested_routing: "accounting_inbox"                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Classification Categories

| Category | Description | Typical Routing |
|----------|-------------|-----------------|
| Invoice | Bills, invoices | Accounting |
| Contract | Legal agreements | Legal |
| Resume | Job applications | HR |
| Medical Record | Patient records | Clinical |
| Prescription | Rx orders | Pharmacy |
| Lab Results | Laboratory reports | Provider |
| Correspondence | Letters, memos | General inbox |
| Form | Structured forms | By form type |

## 12.8 Voice Interface

### Voice Command Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOICE INTERFACE                               │
│                                                                  │
│  ┌──────────────┐                                               │
│  │  🎤 Tap to   │  User: "Add a meeting with John tomorrow     │
│  │    speak     │         at 2pm about the quarterly review"   │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Speech-to-Text (Whisper / Platform Native)                 ││
│  │  → "Add a meeting with John tomorrow at 2pm about the       ││
│  │     quarterly review"                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Intent Recognition (LLM)                                   ││
│  │  Intent: create_calendar_event                              ││
│  │  Entities:                                                  ││
│  │    - attendee: "John" → John Smith (from contacts)         ││
│  │    - date: "tomorrow" → 2025-11-29                         ││
│  │    - time: "2pm" → 14:00                                   ││
│  │    - subject: "quarterly review"                           ││
│  └─────────────────────────────────────────────────────────────┘│
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Confirmation                                               ││
│  │  "I'll create a meeting with John Smith tomorrow at 2:00   ││
│  │   PM titled 'Quarterly Review'. Should I send an invite?"  ││
│  │                                                             ││
│  │  [Yes, send invite]  [Edit details]  [Cancel]              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Supported Voice Commands

| Command Pattern | Action | Example |
|-----------------|--------|---------|
| "Add/Create [task/meeting/reminder]" | Create entity | "Add a task to review the budget" |
| "Show/Find [documents/tasks/contacts]" | Search | "Show my tasks due this week" |
| "Send [fax/email] to [contact]" | Communication | "Send a fax to Dr. Smith" |
| "What's my [schedule/inbox/status]" | Query | "What's on my calendar today?" |
| "Mark [task] as [done/complete]" | Update | "Mark the expense report as done" |

## 12.9 Local LLM Configuration

### Ollama Integration

```python
# AI Provider Configuration
ai_providers = {
    "cloud": {
        "openai": {
            "api_key": "${OPENAI_API_KEY}",
            "models": ["gpt-4o", "gpt-4o-mini"],
            "default_model": "gpt-4o-mini"
        },
        "anthropic": {
            "api_key": "${ANTHROPIC_API_KEY}",
            "models": ["claude-3-5-sonnet"],
            "default_model": "claude-3-5-sonnet"
        }
    },
    "local": {
        "ollama": {
            "base_url": "http://localhost:11434",
            "models": ["llama3:8b", "mistral:7b"],
            "default_model": "llama3:8b"
        }
    }
}

# Organization can override
{
    "ai_provider": "local",  # Use local for privacy
    "ai_model": "llama3:8b",
    "fallback_to_cloud": false  # Never send to cloud
}
```

### Privacy-First AI Routing

```python
def route_ai_request(request, organization):
    """
    Route AI request based on privacy requirements.
    """
    org_settings = get_org_ai_settings(organization)
    
    # Check if request contains PHI
    if request.contains_phi or org_settings.hipaa_mode:
        if org_settings.local_llm_available:
            return LocalLLMProvider(org_settings.local_model)
        else:
            # PHI but no local LLM - must redact or reject
            if org_settings.allow_redacted_cloud:
                return CloudLLMProvider(redact_phi(request))
            else:
                raise PrivacyError("Cannot process PHI without local LLM")
    
    # No PHI concerns - use configured preference
    if org_settings.ai_provider == "local":
        return LocalLLMProvider(org_settings.local_model)
    else:
        return CloudLLMProvider(org_settings.cloud_model)
```

## 12.10 AI Chat Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  AI Assistant                                            [⚙️]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🤖 Hi! I'm your Dartwing assistant. I can help you:      │  │
│  │    • Create and manage tasks                              │  │
│  │    • Search documents and faxes                          │  │
│  │    • Schedule meetings                                    │  │
│  │    • Answer questions about your data                    │  │
│  │                                                            │  │
│  │    What would you like to do?                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 👤 Find all invoices from Acme Corp this month           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🤖 I found 3 invoices from Acme Corp in November:        │  │
│  │                                                            │  │
│  │    📄 INV-2025-0892 - $1,234.56 - Nov 5                  │  │
│  │    📄 INV-2025-0915 - $567.89 - Nov 12                   │  │
│  │    📄 INV-2025-0943 - $2,100.00 - Nov 22                 │  │
│  │                                                            │  │
│  │    Total: $3,902.45                                       │  │
│  │                                                            │  │
│  │    [View All] [Export to Excel] [Create Report]          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Type a message...                              [🎤] [📎] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 12.11 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-AI-01 | AI persona responds with org-specific context | Integration test |
| AC-AI-02 | Knowledge Vault retrieves relevant chunks | Unit test |
| AC-AI-03 | Tool execution respects permissions | Security test |
| AC-AI-04 | Document classification accuracy >90% | ML evaluation |
| AC-AI-05 | Entity extraction identifies key fields | ML evaluation |
| AC-AI-06 | PHI detection catches all PHI types | Security test |
| AC-AI-07 | Voice command creates task correctly | E2E test |
| AC-AI-08 | Voice-to-text accuracy >95% | ML evaluation |
| AC-AI-09 | Local LLM processes without cloud | Integration test |
| AC-AI-10 | PHI requests routed to local only | Security test |
| AC-AI-11 | AI chat responds within 3 seconds | Performance test |
| AC-AI-12 | Meeting assistant extracts action items | Integration test |

## 12.12 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| AI Persona Architecture | Architecture Doc, Section 6 |
| Document AI (Fax) | dartwing-fax-prd.md, Module B |
| PHI Detection | dartwing-fax-prd.md, Module R |
| Background processing | Section 5 (C-16) |

---

*End of Section 12*
# Section 13: Developer Experience

## 13.1 Overview

Dartwing provides a comprehensive **Developer Ecosystem** enabling rapid development of vertical modules and third-party integrations. The platform supports both internal developers building Dartwing modules and external developers creating custom solutions.

**Related Features:** C-14 (Plugin System), Architecture Doc Section 11

## 13.2 Development Goals

| Goal | Target |
|------|--------|
| New vertical MVP launch time | ≤8 weeks |
| Lines of code for new module | ~1,800 typical |
| API documentation coverage | 100% |
| Time to first API call | <30 minutes |
| Developer satisfaction score | >4.5/5 |

## 13.3 Feature Requirements

### API & Documentation

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-DEV-001 | Must | RESTful API for all operations |
| REQ-DEV-002 | Must | OpenAPI/Swagger documentation |
| REQ-DEV-003 | Must | API authentication via OAuth2/API keys |
| REQ-DEV-004 | Must | Rate limiting with clear headers |
| REQ-DEV-005 | Should | Interactive API explorer |
| REQ-DEV-006 | Should | SDK for common languages (Python, JS, Dart) |
| REQ-DEV-007 | Should | Webhook documentation and testing |
| REQ-DEV-008 | Could | GraphQL endpoint |

### Developer Portal

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-PORTAL-001 | Must | API key management |
| REQ-PORTAL-002 | Must | Usage dashboards |
| REQ-PORTAL-003 | Should | Sandbox environment |
| REQ-PORTAL-004 | Should | Sample code and tutorials |
| REQ-PORTAL-005 | Should | Community forum |
| REQ-PORTAL-006 | Could | Partner program |

### Data Export & Portability

| Requirement | Priority | Description |
|-------------|----------|-------------|
| REQ-EXPORT-001 | Must | One-click full data export |
| REQ-EXPORT-002 | Must | Export formats: JSON, CSV |
| REQ-EXPORT-003 | Should | Scheduled automatic exports |
| REQ-EXPORT-004 | Should | Incremental export (changes only) |
| REQ-EXPORT-005 | Could | Direct database access (Enterprise) |

## 13.4 API Design

### API Conventions

| Aspect | Convention |
|--------|------------|
| Base URL | `https://api.dartwing.io/v1` |
| Authentication | Bearer token or API key |
| Content-Type | `application/json` |
| Pagination | `limit`, `offset`, `total_count` |
| Filtering | Frappe filter syntax |
| Errors | Standard HTTP codes + JSON detail |
| Versioning | URL path (`/v1/`) |

### Standard Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/resource/{doctype}` | GET | List documents |
| `/api/resource/{doctype}` | POST | Create document |
| `/api/resource/{doctype}/{name}` | GET | Get document |
| `/api/resource/{doctype}/{name}` | PUT | Update document |
| `/api/resource/{doctype}/{name}` | DELETE | Delete document |
| `/api/method/{path}` | POST | Execute custom method |

### API Response Format

```json
{
  "data": {
    "name": "TASK-00001",
    "title": "Complete quarterly report",
    "status": "Open",
    "due_date": "2025-11-30",
    "created": "2025-11-28T10:30:00Z",
    "modified": "2025-11-28T10:30:00Z"
  },
  "meta": {
    "doctype": "Task",
    "permissions": {
      "read": true,
      "write": true,
      "delete": false
    }
  }
}
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": [
      {
        "field": "title",
        "message": "This field is required"
      }
    ]
  },
  "request_id": "req_abc123"
}
```

### Rate Limiting

| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 60 | 10,000 |
| Pro | 300 | 100,000 |
| Enterprise | 1,000 | Unlimited |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 295
X-RateLimit-Reset: 1732800000
```

## 13.5 Authentication Options

### OAuth2 (Recommended for Apps)

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp...
```

### API Key (For Server-to-Server)

```
Authorization: token api_key:api_secret
```

### API Key Generation

```
┌─────────────────────────────────────────────────────────────────┐
│  API Keys                                          [+ New Key]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Production API Key                                       │  │
│  │  Created: Nov 1, 2025 • Last used: 2 hours ago           │  │
│  │                                                            │  │
│  │  Key: ••••••••••••••••d8f4                                │  │
│  │  Secret: ••••••••••••••••9a2c                             │  │
│  │                                                            │  │
│  │  Permissions:                                              │  │
│  │  ☑ Read all documents                                     │  │
│  │  ☑ Write tasks and events                                 │  │
│  │  ☐ Delete documents                                       │  │
│  │  ☐ Admin operations                                       │  │
│  │                                                            │  │
│  │  [Regenerate Secret]  [Revoke Key]                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Development API Key                                      │  │
│  │  Created: Nov 15, 2025 • Sandbox only                    │  │
│  │                                                            │  │
│  │  Key: ••••••••••••••••b7e2                                │  │
│  │                                                            │  │
│  │  [Regenerate Secret]  [Revoke Key]                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 13.6 SDK Overview

### Python SDK

```python
from dartwing import DartwingClient

# Initialize client
client = DartwingClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    base_url="https://api.dartwing.io"
)

# List tasks
tasks = client.get_list("Task", filters={"status": "Open"}, limit=10)

# Create task
new_task = client.create("Task", {
    "title": "Review proposal",
    "due_date": "2025-12-01",
    "assigned_to": "john@example.com"
})

# Update task
client.update("Task", "TASK-00001", {"status": "Completed"})

# Delete task
client.delete("Task", "TASK-00001")

# Call custom method
result = client.call("dartwing_fax.send_fax", {
    "to": "+15551234567",
    "document": "DOC-00001"
})
```

### JavaScript/TypeScript SDK

```typescript
import { DartwingClient } from '@dartwing/sdk';

const client = new DartwingClient({
  apiKey: 'your_api_key',
  apiSecret: 'your_api_secret',
});

// List tasks
const tasks = await client.getList('Task', {
  filters: { status: 'Open' },
  limit: 10,
});

// Create task
const newTask = await client.create('Task', {
  title: 'Review proposal',
  due_date: '2025-12-01',
});

// Real-time subscription
client.subscribe('Task', 'ORG-001', (event) => {
  console.log('Task updated:', event);
});
```

### Dart/Flutter SDK

```dart
import 'package:dartwing_sdk/dartwing_sdk.dart';

final client = DartwingClient(
  apiKey: 'your_api_key',
  apiSecret: 'your_api_secret',
);

// List tasks
final tasks = await client.getList<Task>(
  filters: {'status': 'Open'},
  limit: 10,
);

// Create task
final newTask = await client.create<Task>(Task(
  title: 'Review proposal',
  dueDate: DateTime(2025, 12, 1),
));
```

## 13.7 Developer Portal

### Portal Features

```
┌─────────────────────────────────────────────────────────────────┐
│  Dartwing Developer Portal                         [Dashboard]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ 📖 Docs    │ │ 🔑 API Keys│ │ 📊 Usage   │ │ 🧪 Sandbox │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                                                                  │
│  QUICK START                                                    │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  1. Get your API key                         [Generate Key →]   │
│  2. Install the SDK                                             │
│     pip install dartwing-sdk                                    │
│  3. Make your first API call                 [View Tutorial →]  │
│                                                                  │
│  API USAGE (Last 30 days)                                       │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Requests: 45,678 / 100,000                              │  │
│  │  ████████████████████░░░░░░░░░░░░░░░░░░  45%             │  │
│  │                                                            │  │
│  │  Errors: 23 (0.05%)                                       │  │
│  │  Avg Response Time: 145ms                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  RECENT API CALLS                                               │
│  ─────────────────────────────────────────────────────────────  │
│  GET /api/resource/Task             200  145ms  10 min ago     │
│  POST /api/resource/Task            201   89ms  15 min ago     │
│  GET /api/resource/Organization     200  123ms  20 min ago     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### API Explorer

```
┌─────────────────────────────────────────────────────────────────┐
│  API Explorer                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Endpoint                                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ GET ▼ │ /api/resource/Task                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Parameters                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  filters    [{"status": "Open"}                        ]        │
│  limit      [10                                        ]        │
│  offset     [0                                         ]        │
│  fields     [["name", "title", "status", "due_date"]   ]        │
│                                                                  │
│  Headers                                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Authorization: Bearer ••••••••••••token                        │
│                                                                  │
│  [Send Request]                                                 │
│                                                                  │
│  Response (200 OK - 145ms)                                      │
│  ─────────────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ {                                                           ││
│  │   "data": [                                                 ││
│  │     {                                                       ││
│  │       "name": "TASK-00001",                                ││
│  │       "title": "Complete quarterly report",                ││
│  │       "status": "Open",                                    ││
│  │       "due_date": "2025-11-30"                             ││
│  │     }                                                       ││
│  │   ]                                                         ││
│  │ }                                                           ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Copy as cURL]  [Copy as Python]  [Copy as JavaScript]        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 13.8 Data Export

### Export API

```
POST /api/method/dartwing_core.export.full_export
{
  "organization": "ORG-001",
  "format": "json",  // or "csv"
  "doctypes": ["Task", "Person", "Organization"],  // optional, default all
  "include_files": true  // include attachments
}

Response:
{
  "export_id": "EXP-2025-00123",
  "status": "processing",
  "estimated_completion": "2025-11-28T11:00:00Z",
  "download_url": null  // populated when complete
}
```

### Export Status

```
GET /api/method/dartwing_core.export.status?export_id=EXP-2025-00123

Response:
{
  "export_id": "EXP-2025-00123",
  "status": "completed",
  "download_url": "https://exports.dartwing.io/EXP-2025-00123.zip",
  "expires_at": "2025-12-05T11:00:00Z",
  "size_bytes": 15234567,
  "record_count": {
    "Task": 156,
    "Person": 24,
    "Organization": 1
  }
}
```

### Export UI

```
┌─────────────────────────────────────────────────────────────────┐
│  Data Export                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Export your organization's data for backup or migration.       │
│                                                                  │
│  FORMAT                                                         │
│  ─────────────────────────────────────────────────────────────  │
│  ○ JSON (recommended for reimport)                              │
│  ● CSV (spreadsheet compatible)                                 │
│                                                                  │
│  DATA TO INCLUDE                                                │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ All data (recommended)                                       │
│  ☐ Select specific types:                                       │
│     ☑ Tasks        ☑ Contacts       ☑ Documents                │
│     ☑ Faxes        ☑ Calendar       ☐ Audit Logs               │
│                                                                  │
│  ☑ Include file attachments                                     │
│                                                                  │
│  SCHEDULE                                                       │
│  ─────────────────────────────────────────────────────────────  │
│  ○ One-time export now                                          │
│  ● Scheduled: [Weekly ▼] on [Sunday ▼] at [2:00 AM ▼]          │
│     Destination: [Google Drive ▼]                               │
│                                                                  │
│  [Start Export]                                                 │
│                                                                  │
│  RECENT EXPORTS                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  Nov 24, 2025 - 14.5 MB - CSV - [Download]                     │
│  Nov 17, 2025 - 13.8 MB - JSON - [Download]                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 13.9 Module Development Guide

### Creating a New Module

```bash
# 1. Create Frappe app
bench new-app dartwing_legal

# 2. Add to Dartwing site
bench --site dartwing.local install-app dartwing_legal

# 3. Configure as Dartwing module (hooks.py)
# See Section 10 for module manifest format

# 4. Create doctypes
bench --site dartwing.local new-doctype "Legal Case"

# 5. Create Flutter module
# Add to dartwing_flutter/lib/modules/legal/
```

### Module Checklist

| Step | Description | Status |
|------|-------------|--------|
| 1 | Define `dartwing_module` in hooks.py | ☐ |
| 2 | Set `required_apps = ["dartwing_core"]` | ☐ |
| 3 | Create doctypes with `organization` link | ☐ |
| 4 | Add permission hooks (Section 9) | ☐ |
| 5 | Create navigation items | ☐ |
| 6 | Implement Flutter module interface | ☐ |
| 7 | Add feature flags for module features | ☐ |
| 8 | Write API tests | ☐ |
| 9 | Write E2E tests | ☐ |
| 10 | Documentation | ☐ |

## 13.10 Acceptance Criteria

| ID | Criteria | Test Method |
|----|----------|-------------|
| AC-DEV-01 | API documentation 100% complete | Manual review |
| AC-DEV-02 | First API call in <30 minutes | User testing |
| AC-DEV-03 | SDK installs without errors | Integration test |
| AC-DEV-04 | SDK CRUD operations work | Integration test |
| AC-DEV-05 | API Explorer sends valid requests | E2E test |
| AC-DEV-06 | Rate limiting enforced correctly | Load test |
| AC-DEV-07 | Full export completes successfully | Integration test |
| AC-DEV-08 | Export includes all requested data | Unit test |
| AC-DEV-09 | New module template works | Integration test |
| AC-DEV-10 | Webhook testing tool works | E2E test |

## 13.11 Architecture Cross-Reference

| Component | Reference Document |
|-----------|-------------------|
| API conventions | Frappe REST API docs |
| Module system | Section 10 |
| Authentication | Section 4 |
| Permissions | Section 9 |

---

*End of Section 13*
# Section 14: Acceptance Criteria & Success Metrics

## 14.1 Overview

This section consolidates all acceptance criteria from individual feature sections and defines the success metrics that determine whether Dartwing Core has achieved its objectives.

## 14.2 Global Acceptance Criteria

These criteria must be true for Dartwing Core to be considered complete and production-ready.

| ID | Criteria | Priority | Test Method |
|----|----------|----------|-------------|
| GAC-01 | New vertical module can ship production-ready MVP in ≤8 weeks | Must | Measured |
| GAC-02 | All features work identically for both Company and Family tenants | Must | Integration test |
| GAC-03 | Zero security incidents related to multi-tenancy or offline sync | Must | Security audit |
| GAC-04 | Mobile app rating ≥4.8 on App Store and Google Play | Must | App store metrics |
| GAC-05 | 99.99% uptime across all regions | Must | Monitoring |
| GAC-06 | API response time <200ms for simple queries | Must | Performance test |
| GAC-07 | API response time <1s for complex reports | Must | Performance test |
| GAC-08 | App cold start <3 seconds | Must | Performance test |
| GAC-09 | Real-time sync latency <500ms | Must | Performance test |
| GAC-10 | Support 10,000+ concurrent connections per instance | Must | Load test |

## 14.3 Feature-Level Acceptance Criteria Summary

### Organization & Multi-Tenancy (Section 3)

| ID | Criteria | Status |
|----|----------|--------|
| AC-ORG-01 | User can create Organization in ≤3 seconds | ☐ |
| AC-ORG-02 | Concrete type auto-created with correct back-reference | ☐ |
| AC-ORG-03 | org_type change after creation fails | ☐ |
| AC-ORG-04 | User can switch organizations in <400ms | ☐ |
| AC-ORG-05 | Data from Org A never visible in Org B context | ☐ |
| AC-ORG-06 | Invitation email delivered within 30 seconds | ☐ |
| AC-ORG-07 | QR code scans and joins correctly on mobile | ☐ |
| AC-ORG-08 | Guest access expires at configured time | ☐ |
| AC-ORG-09 | Organization deletion cascades to concrete type | ☐ |
| AC-ORG-10 | User Permission created on Org Member insert | ☐ |

### Identity & Authentication (Section 4)

| ID | Criteria | Status |
|----|----------|--------|
| AC-AUTH-01 | PKCE flow completes successfully on iOS | ☐ |
| AC-AUTH-02 | PKCE flow completes successfully on Android | ☐ |
| AC-AUTH-03 | Token refresh works before expiration | ☐ |
| AC-AUTH-04 | Expired refresh token redirects to login | ☐ |
| AC-AUTH-05 | Social login (Google) creates Person + User | ☐ |
| AC-AUTH-06 | MFA prompt appears when enabled | ☐ |
| AC-AUTH-07 | Personal org created on signup | ☐ |
| AC-AUTH-08 | Business invitation adds Org Member | ☐ |
| AC-AUTH-09 | Brute force lockout activates after 5 failures | ☐ |
| AC-AUTH-10 | Logout clears all tokens and Keycloak session | ☐ |

### Offline-First & Real-Time Sync (Section 5)

| ID | Criteria | Status |
|----|----------|--------|
| AC-SYNC-01 | Create document offline, appears after sync | ☐ |
| AC-SYNC-02 | Update document offline, syncs correctly | ☐ |
| AC-SYNC-03 | Delete document offline, syncs correctly | ☐ |
| AC-SYNC-04 | Conflict detected when server version newer | ☐ |
| AC-SYNC-05 | AI merge resolves simple conflicts automatically | ☐ |
| AC-SYNC-06 | Human resolution UI shows correct diff | ☐ |
| AC-SYNC-07 | Real-time update received within 500ms | ☐ |
| AC-SYNC-08 | Socket unsubscribed on permission revocation | ☐ |
| AC-SYNC-09 | Pagination continues until has_more=false | ☐ |
| AC-SYNC-10 | Full resync triggered for >30 day gap | ☐ |
| AC-SYNC-11 | Background job shows progress in UI | ☐ |
| AC-SYNC-12 | Failed job retries with exponential backoff | ☐ |

### UI Generation & Navigation (Section 6)

| ID | Criteria | Status |
|----|----------|--------|
| AC-UI-01 | DocType renders as form without code | ☐ |
| AC-UI-02 | All field types render correctly | ☐ |
| AC-UI-03 | depends_on hides/shows fields correctly | ☐ |
| AC-UI-04 | List view displays with sorting | ☐ |
| AC-UI-05 | Kanban drag-and-drop updates status | ☐ |
| AC-UI-06 | Calendar shows items on correct dates | ☐ |
| AC-UI-07 | Theme changes apply instantly | ☐ |
| AC-UI-08 | Dark mode works correctly | ☐ |
| AC-UI-09 | Deep link opens correct screen | ☐ |
| AC-UI-10 | Navigation adapts to platform | ☐ |
| AC-UI-11 | Sidebar shows role-appropriate items | ☐ |
| AC-UI-12 | Organization switcher works | ☐ |

### File Storage & Documents (Section 7)

| ID | Criteria | Status |
|----|----------|--------|
| AC-STOR-01 | File uploads to configured S3 bucket | ☐ |
| AC-STOR-02 | File uploads to Google Drive | ☐ |
| AC-STOR-03 | Virus scan blocks infected file | ☐ |
| AC-STOR-04 | Pre-signed URL expires after timeout | ☐ |
| AC-STOR-05 | Storage usage metered correctly | ☐ |
| AC-SIGN-01 | Drawn signature saves correctly | ☐ |
| AC-SIGN-02 | Typed signature renders with font | ☐ |
| AC-SIGN-03 | Signature audit record created | ☐ |
| AC-SIGN-04 | Saved signature available for reuse | ☐ |
| AC-ANNOT-01 | Highlight annotation saves position | ☐ |
| AC-ANNOT-02 | Redaction permanently removes data | ☐ |
| AC-ANNOT-03 | Stamp appears at correct location | ☐ |
| AC-EXPORT-01 | Emergency binder PDF generates | ☐ |
| AC-EXPORT-02 | Password-protected PDF requires password | ☐ |
| AC-EXPORT-03 | Export includes selected sections only | ☐ |

### Notifications & Communication (Section 8)

| ID | Criteria | Status |
|----|----------|--------|
| AC-NOTIF-01 | Push notification delivered to iOS | ☐ |
| AC-NOTIF-02 | Push notification delivered to Android | ☐ |
| AC-NOTIF-03 | Email notification uses template | ☐ |
| AC-NOTIF-04 | SMS delivered via Twilio | ☐ |
| AC-NOTIF-05 | In-app notification appears in center | ☐ |
| AC-NOTIF-06 | @mention triggers notification | ☐ |
| AC-NOTIF-07 | Quiet hours suppresses notifications | ☐ |
| AC-NOTIF-08 | User preferences respected | ☐ |
| AC-FAX-01 | Fax sent via Telnyx | ☐ |
| AC-FAX-02 | Failover to Bandwidth works | ☐ |
| AC-FAX-03 | Delivery callback received | ☐ |
| AC-REMIND-01 | Recurring task created with next_due | ☐ |
| AC-REMIND-02 | Reminder sent at correct time | ☐ |
| AC-REMIND-03 | One-tap completion updates next_due | ☐ |
| AC-REMIND-04 | Overdue task shows alert | ☐ |

### Compliance & Security (Section 9)

| ID | Criteria | Status |
|----|----------|--------|
| AC-COMP-01 | HIPAA mode enables all required controls | ☐ |
| AC-COMP-02 | BAA tracking creates valid record | ☐ |
| AC-COMP-03 | PHI auto-tagged on ingest | ☐ |
| AC-PERM-01 | User cannot access other org's data | ☐ |
| AC-PERM-02 | Role permissions enforced on API | ☐ |
| AC-PERM-03 | Field-level permissions work | ☐ |
| AC-AUDIT-01 | All CRUD operations logged | ☐ |
| AC-AUDIT-02 | PHI access logged separately | ☐ |
| AC-AUDIT-03 | Audit logs immutable (Object Lock) | ☐ |
| AC-AUDIT-04 | Chain integrity verifiable | ☐ |
| AC-RESID-01 | Data stored in selected region only | ☐ |
| AC-RESID-02 | Cross-region transfer blocked | ☐ |
| AC-GDPR-01 | Data export includes all user data | ☐ |
| AC-GDPR-02 | Account deletion removes all data | ☐ |
| AC-SEC-01 | TLS 1.3 enforced | ☐ |
| AC-SEC-02 | SQL injection blocked | ☐ |

### Plugin & Module System (Section 10)

| ID | Criteria | Status |
|----|----------|--------|
| AC-MOD-01 | Module installed via bench command | ☐ |
| AC-MOD-02 | Module appears in discovery API | ☐ |
| AC-MOD-03 | Module enablement per organization works | ☐ |
| AC-MOD-04 | Module navigation appears when enabled | ☐ |
| AC-MOD-05 | Module routes accessible when enabled | ☐ |
| AC-MOD-06 | Module hidden when disabled | ☐ |
| AC-MOD-07 | Org type compatibility enforced | ☐ |
| AC-FLAG-01 | Boolean flag evaluates correctly | ☐ |
| AC-FLAG-02 | Org override takes precedence | ☐ |
| AC-FLAG-03 | Global override applies when no org override | ☐ |
| AC-FLAG-04 | Flag changes apply without restart | ☐ |
| AC-FLAG-05 | Percentage rollout distributes correctly | ☐ |

### Integrations & Marketplace (Section 11)

| ID | Criteria | Status |
|----|----------|--------|
| AC-INT-01 | OAuth2 connection completes successfully | ☐ |
| AC-INT-02 | Credentials stored encrypted | ☐ |
| AC-INT-03 | Token refresh works automatically | ☐ |
| AC-INT-04 | Disconnect removes credentials | ☐ |
| AC-INT-05 | Bi-directional sync creates/updates records | ☐ |
| AC-INT-06 | Field mapping applies correctly | ☐ |
| AC-INT-07 | Webhook received and processed | ☐ |
| AC-INT-08 | Outgoing webhook fires on event | ☐ |
| AC-INT-09 | Zapier trigger sends data | ☐ |
| AC-INT-10 | Zapier action creates document | ☐ |
| AC-INT-11 | Connection error displayed to user | ☐ |
| AC-INT-12 | Integration logs events correctly | ☐ |

### AI & Voice Features (Section 12)

| ID | Criteria | Status |
|----|----------|--------|
| AC-AI-01 | AI persona responds with org-specific context | ☐ |
| AC-AI-02 | Knowledge Vault retrieves relevant chunks | ☐ |
| AC-AI-03 | Tool execution respects permissions | ☐ |
| AC-AI-04 | Document classification accuracy >90% | ☐ |
| AC-AI-05 | Entity extraction identifies key fields | ☐ |
| AC-AI-06 | PHI detection catches all PHI types | ☐ |
| AC-AI-07 | Voice command creates task correctly | ☐ |
| AC-AI-08 | Voice-to-text accuracy >95% | ☐ |
| AC-AI-09 | Local LLM processes without cloud | ☐ |
| AC-AI-10 | PHI requests routed to local only | ☐ |
| AC-AI-11 | AI chat responds within 3 seconds | ☐ |
| AC-AI-12 | Meeting assistant extracts action items | ☐ |

### Developer Experience (Section 13)

| ID | Criteria | Status |
|----|----------|--------|
| AC-DEV-01 | API documentation 100% complete | ☐ |
| AC-DEV-02 | First API call in <30 minutes | ☐ |
| AC-DEV-03 | SDK installs without errors | ☐ |
| AC-DEV-04 | SDK CRUD operations work | ☐ |
| AC-DEV-05 | API Explorer sends valid requests | ☐ |
| AC-DEV-06 | Rate limiting enforced correctly | ☐ |
| AC-DEV-07 | Full export completes successfully | ☐ |
| AC-DEV-08 | Export includes all requested data | ☐ |
| AC-DEV-09 | New module template works | ☐ |
| AC-DEV-10 | Webhook testing tool works | ☐ |

## 14.4 Success Metrics

### Business Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Active Organizations (Companies + Families) | 15,000+ by Q4 2026 | Database count |
| Consumer Families | 2,000+ by Q4 2026 | Database count |
| Monthly Fax Pages | 75 million by Q4 2026 | Usage metering |
| Average New Vertical Launch Time | ≤6 weeks | Project tracking |
| Lines of Code per New Module | <2,000 average | Code analysis |
| Customer Churn Rate | <2% monthly | Billing data |
| Net Promoter Score (NPS) | >50 | Survey |

### Product Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Mobile App Rating (iOS) | ≥4.8 | App Store |
| Mobile App Rating (Android) | ≥4.8 | Play Store |
| Daily Active Users (DAU) | 60% of registered | Analytics |
| Feature Adoption Rate | >40% within 30 days | Analytics |
| Time to Value (first meaningful action) | <5 minutes | Analytics |
| Support Ticket Volume | <0.5 per user/month | Support system |

### Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.99% | Monitoring |
| API Response Time (p50) | <100ms | APM |
| API Response Time (p95) | <250ms | APM |
| API Response Time (p99) | <500ms | APM |
| Error Rate | <0.1% | APM |
| Sync Conflict Rate | <1% | Logging |
| Security Incidents | 0 | Security audit |
| Data Breach Incidents | 0 | Security audit |

### Developer Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Documentation Coverage | 100% | Automated check |
| Time to First API Call | <30 minutes | User testing |
| Third-Party Integrations | 40+ | Marketplace count |
| Developer Portal MAU | 500+ | Analytics |
| SDK Downloads (monthly) | 1,000+ | Package managers |

## 14.5 Quality Gates

### Phase Gate Criteria

| Phase | Gate Criteria |
|-------|---------------|
| **Alpha** | All Must-have requirements implemented, >70% AC passing |
| **Beta** | All Must + Should requirements implemented, >90% AC passing |
| **RC** | All requirements implemented, 100% AC passing, security audit passed |
| **GA** | RC criteria + 2 weeks stable in production, NPS >40 |

### Release Criteria

| Criterion | Required For Release |
|-----------|---------------------|
| All critical bugs resolved | Yes |
| All Must-have AC passing | Yes |
| Security scan clean | Yes |
| Performance targets met | Yes |
| Documentation complete | Yes |
| Rollback plan tested | Yes |

## 14.6 Monitoring & Alerting

### Key Dashboards

| Dashboard | Contents |
|-----------|----------|
| **Executive** | Business metrics, user growth, revenue |
| **Operations** | Uptime, error rates, response times |
| **Security** | Auth failures, audit events, compliance status |
| **Product** | Feature usage, user flows, conversion |

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Uptime | <99.95% | <99.9% |
| Error Rate | >0.5% | >1% |
| API p95 Latency | >500ms | >1000ms |
| Sync Conflict Rate | >2% | >5% |
| Failed Login Rate | >5% | >10% |
| Queue Depth | >1000 | >5000 |

---

*End of Section 14*
# Section 15: Architecture Cross-Reference & Known Issues

## 15.1 Overview

This section provides a comprehensive cross-reference between PRD features and architecture documentation, identifies known architectural constraints, documents potential issues, and outlines the implementation roadmap.

## 15.2 Document Cross-Reference

### PRD to Architecture Mapping

| PRD Section | Architecture Document | Specific Section |
|-------------|----------------------|------------------|
| Section 3: Organization | dartwing-architecture.md | Section 3: Core Data Model |
| Section 3: Hybrid Model | dartwing-architecture.md | Section 3.1-3.6 |
| Section 4: Authentication | dartwing-auth-architecture.md | Full document |
| Section 4: Person Doctype | person_doctype_contract.md | Full document |
| Section 5: Offline Sync | offline_real_time_sync_spec.md | Full document |
| Section 5: Conflict Resolution | offline_real_time_sync_spec.md | Conflict Strategy |
| Section 6: UI Generation | dartwing-architecture.md | Section 4: Flutter Client |
| Section 9: Permissions | dartwing-architecture.md | Section 8.2.1 |
| Section 9: Compliance | dartwing-architecture.md | Section 8.3 |
| Section 12: AI Personas | dartwing-architecture.md | Section 6 |

### Doctype Reference

| Doctype | Module | Defined In |
|---------|--------|------------|
| Organization | dartwing_core | Architecture Doc 3.3 |
| Family | dartwing_family | Architecture Doc 3.4 |
| Company | dartwing_company | Architecture Doc 3.4 |
| Club | dartwing_associations | Architecture Doc 3.4 |
| Nonprofit | dartwing_nonprofit | Architecture Doc 3.4 |
| Person | dartwing_core | person_doctype_contract.md |
| Org Member | dartwing_core | Architecture Doc 3.8 |
| Role Template | dartwing_core | Architecture Doc 3.7 |
| Equipment | dartwing_core | Architecture Doc 3.11 |
| Family Relationship | dartwing_family | Architecture Doc 3.9 |
| Employment Record | dartwing_hr | Architecture Doc 3.10 |

### API Reference

| API Category | Endpoint Pattern | Documentation |
|--------------|------------------|---------------|
| CRUD Operations | `/api/resource/{doctype}` | Frappe REST API |
| Custom Methods | `/api/method/{path}` | Frappe Whitelist |
| Sync Feed | `/api/method/dartwing_core.sync.feed` | Section 5.5 |
| Sync Upsert | `/api/method/dartwing_core.sync.upsert_batch` | Section 5.5 |
| Module Discovery | `/api/method/dartwing_core.modules.*` | Section 10.5 |
| Feature Flags | `/api/method/dartwing_core.flags.*` | Section 10.6 |
| Storage | `/api/method/dartwing_core.storage.*` | Section 7.5 |
| Export | `/api/method/dartwing_core.export.*` | Section 13.8 |

## 15.3 Known Architectural Constraints

### Constraint 1: org_type Immutability

**Description:** Once an Organization is created with an `org_type`, it cannot be changed.

**Reason:** The hybrid model creates a 1:1 linked concrete type (Family, Company, etc.) on Organization creation. Changing org_type would require:
- Deleting the existing concrete type
- Creating a new concrete type
- Migrating all linked data
- Updating all User Permissions

**Workaround:** Users must create a new Organization with the correct type and migrate data manually.

**Impact:** Low - org_type changes are rare; most organizations know their type at creation.

### Constraint 2: 30-Day Sync Delta Retention

**Description:** Change logs are retained for 30 days. Clients offline longer than 30 days must perform full resync.

**Reason:** Unlimited delta retention would cause unbounded storage growth.

**Workaround:** Full resync automatically triggered when client watermark is older than 30 days.

**Impact:** Medium - Affects rarely-used devices that come back online after extended periods.

### Constraint 3: Single Keycloak Realm per Environment

**Description:** Each environment (dev, staging, prod) uses a single Keycloak realm.

**Reason:** Simplifies SSO and user management; organizations are isolated at the application layer.

**Workaround:** None needed - current architecture is intentional.

**Impact:** None - This is the designed behavior.

### Constraint 4: Socket.IO Connection Limits

**Description:** Each Socket.IO server instance has connection limits (~10,000 concurrent).

**Reason:** WebSocket connections consume server resources.

**Workaround:** Horizontal scaling with sticky sessions; Redis adapter for cross-instance communication.

**Impact:** Low - Standard scaling pattern handles growth.

### Constraint 5: Per-File Encryption Key Management

**Description:** Zero-trust file storage requires managing encryption keys per file.

**Reason:** Maximum security - compromised key affects only one file.

**Workaround:** Key management via AWS KMS / HashiCorp Vault with automatic rotation.

**Impact:** Medium - Adds operational complexity; requires KMS infrastructure.

## 15.4 Known Issues & Limitations

### Issue 1: Offline Conflict Resolution for Complex Documents

**Status:** Known limitation  
**Description:** AI merge may not handle complex nested documents (e.g., documents with multiple child tables) reliably.

**Current Behavior:** Falls back to human resolution for complex conflicts.

**Planned Resolution:** Improve AI merge prompts and add field-level conflict detection for child tables.

**Timeline:** Q2 2026

### Issue 2: Calendar View Performance with Large Datasets

**Status:** Known limitation  
**Description:** Calendar view may become slow with >10,000 events in view range.

**Current Behavior:** Performance degrades gradually.

**Planned Resolution:** Implement virtual scrolling and server-side pagination for calendar data.

**Timeline:** Q1 2026

### Issue 3: Knowledge Vault Embedding Latency

**Status:** Known limitation  
**Description:** Initial document ingestion into Knowledge Vault can take several minutes for large documents.

**Current Behavior:** Background job processes documents asynchronously.

**Planned Resolution:** Optimize chunking strategy and parallelize embedding generation.

**Timeline:** Q2 2026

### Issue 4: Zapier Rate Limits

**Status:** External dependency  
**Description:** Zapier has rate limits that may throttle high-volume integrations.

**Current Behavior:** Webhook delivery may be delayed during high traffic.

**Planned Resolution:** Implement webhook queuing and retry; document Zapier plan requirements.

**Timeline:** N/A - External limitation

### Issue 5: Local LLM Model Size

**Status:** Known limitation  
**Description:** Local LLM models (e.g., Llama 3 8B) require significant RAM (16GB+).

**Current Behavior:** Smaller models available but with reduced capability.

**Planned Resolution:** Document hardware requirements; support model selection based on available resources.

**Timeline:** Ongoing

## 15.5 Dependencies

### External Service Dependencies

| Service | Purpose | Fallback |
|---------|---------|----------|
| **Keycloak** | Authentication | None - Critical |
| **Redis** | Cache, Queue, Pub/Sub | None - Critical |
| **MariaDB/PostgreSQL** | Primary Database | Replica failover |
| **AWS S3** | File Storage | Multi-region replication |
| **Twilio** | SMS/Voice | Vonage backup |
| **Telnyx** | Fax | Bandwidth → SignalWire |
| **SendGrid** | Email | Mailgun backup |
| **OpenAI/Anthropic** | Cloud LLM | Ollama local fallback |
| **ClamAV** | Virus Scanning | Block uploads if unavailable |

### Internal Module Dependencies

```
dartwing_core (base)
├── dartwing_family (requires: dartwing_core)
├── dartwing_company (requires: dartwing_core)
├── dartwing_associations (requires: dartwing_core)
├── dartwing_nonprofit (requires: dartwing_core)
├── dartwing_hr (requires: dartwing_core, dartwing_company)
├── dartwing_fax (requires: dartwing_core)
├── dartwing_ai (requires: dartwing_core)
└── dartwing_comms (requires: dartwing_core)
```

## 15.6 Implementation Roadmap

### Phase 1: Foundation (Q1 2026)

| Feature | Priority | Dependencies |
|---------|----------|--------------|
| Core Doctypes (Organization, Person, Org Member) | P0 | None |
| Hybrid Organization Model | P0 | Core Doctypes |
| Flutter Project Scaffolding | P0 | None |
| Keycloak Integration | P0 | None |
| Basic Frappe API Client | P0 | None |
| iOS and Android Builds | P0 | Flutter Project |
| Offline Storage (SQLite) | P1 | Flutter Project |

### Phase 2: Core Features (Q2 2026)

| Feature | Priority | Dependencies |
|---------|----------|--------------|
| Role Template & Permissions | P0 | Phase 1 |
| Family & Company Concrete Types | P0 | Hybrid Model |
| Automatic UI Generation | P0 | Flutter Project |
| Real-time Sync (Socket.IO) | P1 | API Client |
| Web and Desktop Builds | P1 | Flutter Project |
| Notification Engine | P1 | Core Doctypes |

### Phase 3: AI & Communications (Q3 2026)

| Feature | Priority | Dependencies |
|---------|----------|--------------|
| AI Persona Engine | P1 | Phase 2 |
| Knowledge Vault | P1 | AI Engine |
| Document AI Pipeline | P1 | AI Engine |
| Fax-over-IP Engine | P1 | Core |
| Voice Interface | P2 | AI Engine |
| Integration Marketplace | P2 | Phase 2 |

### Phase 4: Scale & Polish (Q4 2026)

| Feature | Priority | Dependencies |
|---------|----------|--------------|
| Nonprofit & Club Types | P1 | Hybrid Model |
| Multi-jurisdiction Support | P1 | Data Residency |
| Compliance Mode (HIPAA/SOC2) | P0 | Audit Trail |
| Advanced Analytics | P2 | All Data |
| App Store Submissions | P0 | All Features |
| Enterprise Deployment | P1 | All Features |

## 15.7 Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Keycloak scalability | Low | High | Load testing, horizontal scaling |
| Sync conflict rate too high | Medium | Medium | Improve AI merge, user education |
| Mobile app rejection | Low | High | Follow guidelines, pre-submission review |
| HIPAA audit findings | Low | High | Regular security audits, BAA templates |
| Third-party API changes | Medium | Medium | Abstraction layers, version pinning |
| Performance degradation at scale | Medium | High | Load testing, profiling, caching |
| LLM cost overruns | Medium | Medium | Local LLM option, usage limits |

## 15.8 Open Questions

| Question | Owner | Due Date | Status |
|----------|-------|----------|--------|
| Final decision on vector database (pgvector vs Pinecone) | Architect | Q1 2026 | Open |
| Multi-region deployment strategy | DevOps | Q1 2026 | Open |
| Third-party module certification process | Product | Q2 2026 | Open |
| Enterprise pricing model | Business | Q2 2026 | Open |
| White-label mobile app distribution | Engineering | Q3 2026 | Open |

## 15.9 Glossary

| Term | Definition |
|------|------------|
| **Concrete Type** | Type-specific doctype (Family, Company, Club, Nonprofit) linked 1:1 to Organization |
| **DocType** | Frappe's equivalent of a database table with metadata and logic |
| **Hybrid Model** | Architecture pattern using thin reference (Organization) + concrete implementations |
| **Knowledge Vault** | Per-organization document repository for AI context via RAG |
| **org_type** | The classification of an Organization (Family/Company/Nonprofit/Club) |
| **PKCE** | Proof Key for Code Exchange - OAuth2 extension for mobile apps |
| **RAG** | Retrieval-Augmented Generation - AI technique combining search with LLM |
| **Role Template** | Reusable role definitions filtered by org_type |
| **Socket.IO** | Real-time bidirectional event-based communication library |
| **Watermark** | Sync cursor indicating last synchronized timestamp |
| **WORM** | Write Once Read Many - immutable storage pattern |
| **Zero Trust Files** | Per-file encryption with separate keys |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | November 2025 | Architecture Team | Initial PRD creation |
| 2.0 | November 2025 | Brett + Claude | Comprehensive rewrite with all 25 features |

---

*End of Section 15*

---

*End of Dartwing Core PRD*
