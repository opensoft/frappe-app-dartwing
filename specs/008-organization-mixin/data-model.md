# Data Model: OrganizationMixin Base Class

**Feature**: 008-organization-mixin
**Date**: 2025-12-14

## Overview

This feature does not introduce new doctypes or database schema changes. It enhances an existing Python mixin class that provides access to Organization data from concrete type documents.

## Entities

### OrganizationMixin (Python Class)

A mixin class providing shared functionality for concrete organization types.

**Module**: `dartwing.dartwing_core.mixins.organization_mixin`

**Properties** (read-only):

| Property | Type | Description | Returns if missing |
|----------|------|-------------|-------------------|
| `org_name` | str \| None | Organization's display name | None |
| `logo` | str \| None | Organization's logo URL | None |
| `org_status` | str \| None | Organization's status | None |

**Methods**:

| Method | Signature | Description | Error Cases |
|--------|-----------|-------------|-------------|
| `get_organization_doc()` | `() -> Document \| None` | Returns full Organization document | Returns None if no org linked |
| `update_org_name()` | `(new_name: str) -> None` | Updates Organization's org_name | Throws if empty name or no org linked |

**Internal Methods**:

| Method | Description |
|--------|-------------|
| `_get_organization_cache()` | Lazy-loads and caches Organization data |
| `_clear_organization_cache()` | Invalidates cached Organization data |

### Related Existing Entities

**Organization** (existing doctype):
- `org_name`: Data, required - The display name
- `logo`: Attach Image - Organization logo
- `status`: Select - Active/Inactive/Dissolved
- `linked_doctype`: Data - Name of concrete type doctype
- `linked_name`: Data - Name of concrete type record

**Concrete Types** (existing doctypes):
- `Family` - family.py will inherit from OrganizationMixin
- `Company` - company.py already inherits from OrganizationMixin
- `Association` - future: will inherit from OrganizationMixin
- `Nonprofit` - future: will inherit from OrganizationMixin

All concrete types have:
- `organization`: Link → Organization - Back-reference to parent

## Relationships

```
┌─────────────────────────────────────────────────────────┐
│                   OrganizationMixin                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Properties: org_name, logo, org_status          │    │
│  │ Methods: get_organization_doc(), update_org_name│    │
│  └─────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────┘
                         │ inherits
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌───────────┐
    │ Family  │    │ Company  │    │ Future:   │
    │(Document│    │(Document,│    │Association│
    │ Mixin)  │    │ Mixin)   │    │ Nonprofit │
    └────┬────┘    └────┬─────┘    └───────────┘
         │              │
         │ organization │ organization
         │ (Link)       │ (Link)
         ▼              ▼
    ┌─────────────────────────────────────────┐
    │              Organization               │
    │  org_name, logo, status                 │
    │  linked_doctype, linked_name            │
    └─────────────────────────────────────────┘
```

## State Transitions

Not applicable - the mixin does not manage state. Organization status is managed by the Organization doctype itself.

## Validation Rules

| Rule | Enforcement Location | Description |
|------|---------------------|-------------|
| Non-empty org_name on update | `OrganizationMixin.update_org_name()` | Empty or whitespace-only names rejected |
| Organization link required for update | `OrganizationMixin.update_org_name()` | Cannot update if `self.organization` is None |

## Data Volume Assumptions

- Mixin is instantiated per-request, not cached globally
- Cache (`_org_cache`) lives for single request lifetime
- Single query fetches all needed Organization fields
- No impact on database size or indexes
