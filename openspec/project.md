# Project Context

## Purpose

Dartwing is a comprehensive application framework combining Flutter for cross-platform mobile/web/desktop frontends with Frappe as the backend, enabling rapid low-code development of business applications.

**Vision:** One framework. Every platform. Any organization type.

Dartwing eliminates the need for separate CRM, HRIS, family-management, church-management, HOA, and club-membership systems by providing a single, unified architecture that adapts to any organizational structure.

### Key Differentiators

| Differentiator | Description |
|----------------|-------------|
| Universal Organization Model | Hybrid architecture with unified identity layer and type-specific concrete implementations (Family, Company, Club, Nonprofit) |
| Cross-Platform Native | Flutter provides true native performance on iOS, Android, Web, and Desktop from a single codebase |
| AI-First Design | Built-in AI personas, smart routing, and LLM integration with optional local/edge processing for privacy |
| Low-Code Development | Frappe's doctype system enables rapid app building; new verticals ship in ≤8 weeks |
| Offline-First Architecture | Full native apps work 100% offline with deterministic sync and conflict resolution |
| Multi-Tenant Isolation | Complete data isolation between Organizations with <400ms context switching |
| Compliance-Ready | One toggle enables HIPAA, SOC2, GDPR modes with signed BAA, Object Lock, encryption, and audit trails |

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend Framework | Flutter | 3.24+ |
| Frontend Language | Dart | 3.5+ |
| Backend Framework | Frappe | 16.x |
| Backend Language | Python | 3.11+ |
| Database | MariaDB | 10.6+ |
| Identity Provider | Keycloak | 24.x |
| Cache/Queue | Redis | 7.x |
| State Management | Riverpod | 2.5+ |
| Real-Time | Socket.IO | Latest |

### Three-Tier Architecture

| Layer | Technology | Responsibility |
|-------|------------|----------------|
| Presentation | Flutter (Dart) | UI/UX, State Management, Platform Adaptation |
| API Gateway | Frappe REST / Socket.IO | Authentication, Rate Limiting, Routing |
| Business Logic | Frappe (Python) | Workflows, Validations, Permissions |
| Data Layer | MariaDB / PostgreSQL | Persistence, Transactions, Indexing |
| Authentication | Keycloak | SSO, OAuth2, OIDC, Realm Management |

## Project Conventions

### Code Style

**Python (Frappe Backend):**
- Follow Frappe coding standards
- Use `@frappe.whitelist()` decorator for all API-exposed methods
- All business logic MUST be exposed via whitelisted Python methods
- Use hooks.py for doc_events and permission configurations

**Dart (Flutter Frontend):**
- Feature-first architecture with Riverpod 2.0 for state management
- Code generation with freezed and json_serializable
- Platform-adaptive widgets (Cupertino on iOS, Material on Android)

### Architecture Patterns

**Hybrid Organization Model:**
The core architectural pattern uses a thin reference shell (`Organization`) with 1:1 linked concrete types (`Family`, `Company`, `Club`, `Nonprofit`).

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
     └─────────┘      └──────────┘      └─────────┘      └───────────┘
```

**API-First Principle:**
- All business logic exposed via `@frappe.whitelist()` decorated Python methods
- Flutter mobile/desktop apps access all functionality via REST API
- Third-party websites integrate via standard REST calls
- Frappe Builder pages use the same backend logic via `frappe.call()`

**Permission Flow:**
```
User → Org Member → Organization → Concrete Type (Family/Company/Club/Nonprofit)
```

### Testing Strategy

- Unit tests for individual functions and validators
- Integration tests for API endpoints and hook interactions
- E2E tests for mobile app flows (PKCE auth, organization switching)
- Performance tests for <400ms context switching and <3s app cold start
- Security tests for multi-tenant data isolation

### Git Workflow

- Feature branches from `develop`
- Pull requests require code review
- Commit messages follow conventional commits pattern
- Main branch protected, merges only via PR

## Domain Context

### Core Modules

| Module | Description |
|--------|-------------|
| dartwing_core | Organization, Person, Org Member, Role Template, Equipment doctypes |
| dartwing_hr | Employment Record, Skills, Departments, Payroll integration |
| dartwing_family | Family Relationship, shared calendars, allowance tracking, Chore Gamification, Meal Planning, Family Vault |
| dartwing_comms | Virtual phone numbers, SMS/Voice, Fax management, Unified Inbox, Smart Routing, Broadcast System |
| dartwing_ai | AI Personas, Knowledge Vault, Tool Registry, LLM integration |
| dartwing_fax | HIPAA-compliant fax handling, patient mapping, audit logs |

### Organization Types

| Type | Module | Naming Series | Primary Use Cases |
|------|--------|---------------|-------------------|
| Family | dartwing_family | FAM-.##### | Households, personal life management, parental controls |
| Company | dartwing_company | CO-.##### | Businesses, LLCs, corporations, partnerships |
| Club/Association | dartwing_associations | CLB-.##### | HOAs, sports clubs, membership organizations |
| Nonprofit | dartwing_nonprofit | NPO-.##### | 501(c)(3), foundations, charities |

### Key Doctypes

| Doctype | Type | Description |
|---------|------|-------------|
| Organization | Parent | Thin reference shell for polymorphic identity |
| Person | Parent | Individual human identity |
| Org Member | Parent | Links Person to Organization with role |
| Role Template | Parent | Role definitions per org_type |
| Equipment | Parent | Assets owned by organizations |
| Family | Concrete | Family-specific data (parental controls, residence) |
| Company | Concrete | Business-specific data (tax_id, officers, entity_type) |
| Club | Concrete | Membership tiers, dues, amenities |
| Nonprofit | Concrete | Tax-exempt status, board, mission |

## Important Constraints

### Performance Requirements

| Metric | Target |
|--------|--------|
| API response time (simple queries) | <200ms |
| API response time (complex reports) | <1s |
| App cold start | <3s |
| App warm start | <1s |
| Real-time sync latency | <500ms |
| Organization context switch | <400ms |
| Concurrent connections per instance | 10,000+ |

### Security & Compliance

- **HIPAA:** PHI handling, BAAs, audit trails
- **GDPR:** Data portability, right to erasure, consent management
- **SOC 2:** Security controls and monitoring
- **Multi-Jurisdiction:** Data residency requirements (US, EU, Canada, Australia)

### Data Integrity Rules

| Rule | Enforcement |
|------|-------------|
| org_type immutability | `set_only_once` field attribute + validate hook |
| Bidirectional link integrity | Server hooks maintain both directions |
| Cascade delete | on_trash hook deletes concrete type |
| Permission propagation | after_insert creates User Permission |

### Authentication Requirements

- PKCE required for all public clients (S256 method)
- Access tokens expire in 5 minutes
- Refresh tokens valid for 30 days
- Tokens stored in platform secure storage (Keychain/Keystore)
- SSO session idle timeout: 30 minutes

## External Dependencies

### Core Infrastructure

| Service | Purpose |
|---------|---------|
| Keycloak | Identity Provider - SSO, OAuth2, OIDC |
| Redis | Cache, Queue, Socket.IO adapter |
| MariaDB | Primary database |
| S3-compatible storage | File storage with Object Lock for compliance |

### Integration Providers

| Provider | Integration |
|----------|-------------|
| Twilio | SMS/Voice, Fax-over-IP |
| Telnyx / Bandwidth / SignalWire | Multi-carrier fax abstraction |
| Stripe / Lemon Squeezy | Billing and payments |
| Google Workspace | Calendar, Drive, OAuth |
| Microsoft 365 | Office, OneDrive, OAuth |
| Salesforce, QuickBooks, DocuSign | Business integrations |

### Flutter Dependencies

Core packages:
- flutter_riverpod, riverpod_annotation, riverpod_generator
- dio, retrofit, json_serializable
- flutter_secure_storage, hive_flutter
- socket_io_client
- flutter_appauth (OAuth/OIDC)
- go_router
- freezed, freezed_annotation

## Repository Structure

```
dartwing/
├── docs/
│   ├── README.md              # Project overview
│   ├── dartwing_core/         # Core module docs
│   ├── dartwing_hr/           # HR module docs
│   ├── dartwing_family/       # Family module docs
│   ├── dartwing_comms/        # Communications module docs
│   ├── dartwing_ai/           # AI module docs
│   └── dartwing_fax/          # Fax module docs
├── dartwing/                   # Frappe app
│   ├── dartwing_core/         # Core doctypes
│   ├── dartwing_family/       # Family module
│   ├── dartwing_billing/      # Billing module
│   ├── dartwing_ops/          # Operations module
│   ├── api/                   # API endpoints
│   ├── permissions/           # Permission handlers
│   └── hooks.py               # Frappe hooks
├── dartwing_flutter/          # Flutter monorepo
│   ├── lib/
│   │   ├── core/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   └── services/
│   └── pubspec.yaml
├── openspec/                  # OpenSpec configuration
└── .specify/                  # spec-kit artifacts
```

## Documentation Hierarchy

When working on specific modules, read docs in this order:

1. **Always read**: `docs/README.md`, `docs/dartwing_core/dartwing_core_arch.md`, `docs/dartwing_core/dartwing_core_prd.md`
2. **Current context**: When working on specific modules, also read `docs/[module-name]/`
3. **Full scan**: `docs/**/*.md` when comprehensive understanding needed

### Key Reference Documents

| Document | Purpose |
|----------|---------|
| `docs/dartwing_core/dartwing_core_arch.md` | Full architecture specification |
| `docs/dartwing_core/dartwing_core_prd.md` | Product requirements with feature catalog |
| `docs/dartwing_core/person_doctype_contract.md` | Person identity and linkage requirements |
| `docs/dartwing_core/org_integrity_guardrails.md` | Immutability and reconciliation details |
| `docs/dartwing_core/integration_token_management_spec.md` | OAuth2 token lifecycle |
| `docs/dartwing_core/offline_real_time_sync_spec.md` | Sync behavior details |
| `docs/dartwing_core/observability_spec.md` | Metrics and logging |
