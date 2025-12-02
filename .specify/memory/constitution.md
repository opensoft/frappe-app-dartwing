# Dartwing Project Constitution

## Context Hierarchy (Read in this order)

1. **Always read**: `docs/README.md`, `docs/architecture.md`, `docs/overview.md`, `docs/dartwing_core_arch.md` (project-wide)
2. **Current context**: When working on specific modules, also read `docs/[module-name]/` and submodules
3. **Full scan**: `docs/**/*.md` (all docs when comprehensive understanding needed)

## Instructions for Agents

- Start with project root docs for architecture understanding
- When given module name (ex: "dartwing_core"), prioritize `docs/dartwing_core/` + root docs
- Reference specific docs paths in responses: `[docs/dartwing_core/organization.md]`
- For Flutter work, also read `lib/README.md` if present
- For Frappe doctypes, check `docs/doctypes/` for field definitions

---

## Client Architecture (Three Access Patterns)

All clients communicate with Frappe backend through the **same REST API layer**. This is non-negotiable.

| Client                  | Technology             | Communication                               | Use Case                                |
| ----------------------- | ---------------------- | ------------------------------------------- | --------------------------------------- |
| **DartwingFone**        | Flutter Mobile         | REST API (`/api/resource/`, `/api/method/`) | Primary end-user mobile app             |
| **Dartwing Desktop**    | Flutter Desktop        | REST API (same endpoints)                   | Desktop users (macOS, Windows, Linux)   |
| **Dartwing Web App**    | Flutter Web            | REST API (same endpoints)                   | Browser-based app experience            |
| **External Websites**   | Any (React, Vue, etc.) | REST API (same endpoints)                   | Third-party integrations, partner sites |
| **Frappe Builder Site** | Frappe Builder         | `frappe.call()` → REST API                  | Marketing site, public pages            |

**Critical Implication:** Every business logic function MUST be exposed via `@frappe.whitelist()` API methods. Never put logic only in Frappe Desk UI or only accessible via Jinja templates.

### API-First Development Rule

1. **All business logic** lives in Python controller methods with `@frappe.whitelist()`
2. **Flutter and external sites** call `/api/method/dartwing.{module}.{method}`
3. **Frappe Builder** uses same methods via `frappe.call('dartwing.{module}.{method}')`
4. **No client-specific endpoints** - one API serves all clients
5. **Real-time updates** via Socket.IO for all clients that support it

---

## Core Principles

These are non-negotiable principles that guide all development on this project.

### 1. Single Source of Truth

- ONE `Organization` doctype handles all organization types (Family, Company, Nonprofit, Club)
- Never create separate doctypes for different org types
- Use `org_type` Select field and `depends_on` for conditional behavior

### 2. Technology Stack (Non-Negotiable)

- **Frontend:** Flutter 3.24+ with Dart 3.5+
- **State Management:** Riverpod 2.x (not Provider, not Bloc)
- **Backend:** Frappe 15.x with Python 3.11+
- **Database:** MariaDB 10.6+ (not MySQL, not PostgreSQL for now)
- **Authentication:** Keycloak with OAuth2/OIDC + PKCE

### 3. Architecture Patterns

- Feature-first folder structure in Flutter
- Repository pattern for all data access
- AsyncNotifier for API state in Riverpod
- Frappe doctype system for all data models
- Socket.IO for real-time sync

### 4. Cross-Platform Requirements

- All features must work on iOS, Android, Web, and Desktop
- Platform-specific code only in services layer
- No web-only or mobile-only features in core

### 5. Security & Compliance

- All API calls over TLS 1.3
- HIPAA-compliant file storage in /private/files
- Audit logging for all sensitive operations
- Personal and business identity separation
- Role-based access control via Frappe permissions

### 6. Code Quality Standards

- Dart analyzer with zero warnings
- Python linting with flake8
- All doctypes must have complete field definitions
- No hardcoded strings (use constants/l10n)
- Tests required for business logic

### 7. Naming Conventions

- Doctypes: PascalCase (e.g., `Organization`, `OrgMember`)
- Frappe fieldnames: snake_case (e.g., `org_type`, `tax_id`)
- Dart classes: PascalCase
- Dart files: snake_case
- Flutter providers: camelCase with `Provider` suffix

### 8. API Design

- Use Frappe's `/api/resource/{doctype}` for CRUD
- Custom methods via `/api/method/dartwing.{module}.{method}`
- All responses include proper error codes
- Pagination via limit/offset

### 9. Offline-First

- Critical reads work offline via local cache
- Writes queue when offline and sync when online
- Conflict resolution: last-write-wins with user notification

### 10. AI Integration

- AI personas are org-scoped
- Knowledge Vault content never leaves org boundary
- Tool execution requires explicit permissions
- All AI interactions logged for audit
