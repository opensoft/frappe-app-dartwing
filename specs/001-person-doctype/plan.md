# Implementation Plan: Person DocType

**Branch**: `001-person-doctype` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-person-doctype/spec.md`

## Summary

Implement the Person DocType as the foundational identity layer for Dartwing. Person serves as the central identity entity linking individuals to Frappe Users (for system access), Keycloak (for external authentication), and Organizations (via personal_org). This is a P1-CRITICAL feature that blocks Org Member, Employment Record, Family Relationship, and all user flows.

Key capabilities:
- Unique identity enforcement (primary_email, keycloak_user_id, frappe_user)
- Consent tracking for minors with write-blocking until consent captured
- Resilient Frappe User auto-creation with background retry on failure
- Person merge functionality with full audit trail via child table

## Technical Context

**Language/Version**: Python 3.11+ (Frappe 16.x backend)
**Primary Dependencies**: Frappe Framework 16.x, frappe.model.document, frappe.background_jobs
**Storage**: MariaDB 10.6+ (via Frappe ORM)
**Testing**: pytest with frappe.tests.utils
**Target Platform**: Frappe Server (Linux), accessible via REST API from Flutter clients
**Project Type**: Frappe App (dartwing_core module)
**Performance Goals**: Duplicate rejection <1s, User auto-creation <2s (per SC-002, SC-004)
**Constraints**: API-first (all logic via @frappe.whitelist()), HIPAA-compliant audit logging
**Scale/Scope**: Foundation doctype - all users will have Person records

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Single Source of Truth | PASS | Person is single identity doctype, no parallel identity types |
| Technology Stack | PASS | Python/Frappe backend, MariaDB storage per constitution |
| Architecture Patterns | PASS | Using Frappe doctype system for data model |
| API-First Development | PASS | All methods will use @frappe.whitelist() |
| Security & Compliance | PASS | Audit logging for merge ops, consent tracking, HIPAA file storage |
| Code Quality Standards | PASS | Will include complete field definitions and tests |
| Naming Conventions | PASS | DocType: Person (PascalCase), fields: snake_case |
| Offline-First | N/A | Backend doctype - offline handled by Flutter clients |

**Gate Result**: PASS - No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-person-doctype/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── person-api.yaml  # OpenAPI spec for Person endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dartwing/
└── dartwing_core/
    └── doctype/
        ├── person/
        │   ├── __init__.py
        │   ├── person.json          # DocType definition
        │   ├── person.py            # Controller with validation hooks
        │   └── test_person.py       # Unit tests
        └── person_merge_log/
            ├── __init__.py
            ├── person_merge_log.json # Child table definition
            └── person_merge_log.py   # Child table controller

dartwing/
├── api/
│   └── person.py                    # @frappe.whitelist() API methods
├── utils/
│   └── person_sync.py               # Background job for user sync retry
└── tests/
    └── test_person_api.py           # API integration tests
```

**Structure Decision**: Following existing dartwing_core module pattern. Person DocType goes in `dartwing/dartwing_core/doctype/person/` alongside existing doctypes (Organization, Family, Customer). Person Merge Log is a child table in separate folder per Frappe conventions.

## Complexity Tracking

> No constitution violations - table not required.
