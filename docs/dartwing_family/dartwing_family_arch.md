# Dartwing Family Module - Technical Architecture Document

**Version:** 1.0
**Last Updated:** November 2025
**Module:** dartwing_family
**Framework:** Frappe v15 + Flutter

---

> **Document Type:** TARGET ARCHITECTURE
>
> This document describes the **complete technical architecture** for Dartwing Family. Most components are not yet implemented.
>
> **Implementation Status:**
>
> | Component | Status | Notes |
> |-----------|--------|-------|
> | Organization Model | ✅ Done | Thin shell + Family linking |
> | Family DocType | ✅ Done | Basic fields + org link |
> | Family Member | ✅ Done | Age fields, COPPA flags |
> | Permission System | ✅ Done | Org-scoped query conditions |
> | Role Fixtures | ✅ Done | 6 family roles defined |
> | Family Relationship | ❌ Pending | Phase 2 |
> | Custody Schedules | ❌ Pending | Phase 2 |
> | Chore System | ❌ Pending | Phase 3 |
> | Real-Time Sync | ❌ Pending | Phase 3 |
> | Offline Sync | ❌ Pending | Phase 3 |
> | Integrations | ❌ Pending | Phase 4 |
> | Voice Assistant | ❌ Deferred | Post-MVP |
> | Flutter App | ❌ Pending | Not started |
>
> **See Also:**
> - [Implementation Status](./implementation_status.md) - Full tracking
> - [Implementation Plan](./critique/dartwing_family_arch_plan.md) - Phased roadmap

---

## Executive Summary

The Dartwing Family module is a comprehensive family management platform built on the Frappe framework with a Flutter mobile application. It provides features for chore management, allowance tracking, location sharing, calendar coordination, custody scheduling, and smart home integration—all with robust age-appropriate permissions and child safety controls.

### Key Capabilities

- **Multi-tenant family organization** with complete data isolation
- **Age-based permission system** with COPPA compliance for children under 13
- **Real-time communication** via Socket.IO for instant family updates
- **Offline-first mobile app** with automatic sync and conflict resolution
- **Voice assistant** with family-cloned voices and child-safe responses
- **20+ third-party integrations** including home automation, retail, education, and vehicle telematics
- **Comprehensive background job system** for scheduled tasks and notifications

---

## Table of Contents

1. [System Architecture Overview](#section-1-system-architecture-overview)

   - 1.1 High-Level Architecture
   - 1.2 Technology Stack
   - 1.3 Multi-Tenant Isolation
   - 1.4 Real-Time Communication
   - 1.5 Offline-First Architecture
   - 1.6 Security Architecture

2. [Data Model Architecture](#section-2-data-model-architecture)

   - 2.1 Core DocTypes Overview
   - 2.2 Family Member DocType
   - 2.3 Family Relationships
   - 2.4 Chore Management
   - 2.5 Allowance & Rewards
   - 2.6 Calendar & Events
   - 2.7 Location Tracking
   - 2.8 Custody & Co-Parenting

3. [Permission & Access Control Architecture](#section-3-permission--access-control-architecture)

   - 3.1 Permission Architecture Overview
   - 3.2 Organization-Level Isolation
   - 3.3 Role-Based Permissions
   - 3.4 Age-Based Access Control
   - 3.5 Relationship-Based Permissions
   - 3.6 Feature-Specific Permissions
   - 3.7 COPPA Compliance

4. [Integration Architecture](#section-4-integration-architecture)

   - 4.1 Integration Framework Overview
   - 4.2 Base Adapter Pattern
   - 4.3 Home Automation Adapters
   - 4.4 Retail Integration Adapters
   - 4.5 Education Platform Adapters
   - 4.6 Location & Tracker Adapters
   - 4.7 Vehicle Telematics Adapters
   - 4.8 Webhook Router

5. [Mobile Application Architecture](#section-5-mobile-application-architecture)

   - 5.1 Flutter Application Structure
   - 5.2 State Management (Riverpod)
   - 5.3 API Client & Interceptors
   - 5.4 WebSocket Client
   - 5.5 Offline Storage (Hive)
   - 5.6 Sync Engine
   - 5.7 Native Integrations
   - 5.8 Age-Appropriate UI Themes

6. [Voice Assistant & AI Integration Architecture](#section-6-voice-assistant--ai-integration-architecture)

   - 6.1 Voice Assistant Overview
   - 6.2 Voice Cloning System
   - 6.3 Natural Language Understanding
   - 6.4 Child Safety Filter
   - 6.5 Family Knowledge Base
   - 6.6 Response Generation
   - 6.7 Speech Services Integration
   - 6.8 Voice Assistant API

7. [Background Services & Scheduled Tasks](#section-7-background-services--scheduled-tasks)

   - 7.1 Scheduler Architecture Overview
   - 7.2 Scheduler Configuration
   - 7.3 Daily Tasks
   - 7.4 Hourly Tasks
   - 7.5 Cron Tasks
   - 7.6 Background Job Utilities

8. [Testing & Quality Assurance Architecture](#section-8-testing--quality-assurance-architecture)

   - 8.1 Testing Strategy Overview
   - 8.2 Backend Testing (Python/Frappe)
   - 8.3 Frontend Testing (Flutter)
   - 8.4 Security Testing
   - 8.5 Performance Testing
   - 8.6 CI/CD Test Configuration

9. [Deployment & DevOps Architecture](#section-9-deployment--devops-architecture)
   - 9.1 Infrastructure Overview
   - 9.2 Kubernetes Deployment
   - 9.3 Database Configuration
   - 9.4 CI/CD Pipeline
   - 9.5 Monitoring & Observability
   - 9.6 Backup & Disaster Recovery
   - 9.7 Environment Configuration

---

# Dartwing Family Module - Technical Architecture Document

**Version:** 1.0  
**Date:** November 28, 2025  
**Status:** Draft  
**Module Activation:** `Organization.org_type = "Family"`

---

# Section 1: System Architecture Overview

## 1.1 Architecture Principles

### Core Design Tenets

| Principle                  | Implementation                                                                                                          |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Privacy-First**          | All data encrypted at rest (AES-256) and in transit (TLS 1.3). Age-based data minimization enforced at the model layer. |
| **Offline-Capable**        | Critical features (emergency contacts, medical info, schedules) cached locally with sync-on-connect.                    |
| **Real-Time Sync**         | Frappe's Socket.IO for instant family updates across all devices.                                                       |
| **Multi-Tenant Isolation** | Each family is a Frappe Organization with complete data isolation.                                                      |
| **Age-Aware Permissions**  | Permission checks embedded in every API endpoint and UI component.                                                      |
| **Modular Integration**    | All third-party integrations via abstracted adapter pattern.                                                            |

### Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Flutter Mobile App          │  Flutter Web App       │  Voice Interface    │
│  (iOS/Android)               │  (PWA)                 │  (Dartwing VA)      │
│  ├─ Riverpod State           │  ├─ Riverpod State     │  ├─ Wake Word       │
│  ├─ Hive Local DB            │  ├─ IndexedDB          │  ├─ STT/TTS         │
│  ├─ Background Services      │  └─ Service Worker     │  └─ NLU Pipeline    │
│  └─ Native Integrations      │                        │                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  Frappe REST API             │  GraphQL (optional)    │  WebSocket (Real-time)│
│  ├─ JWT Authentication       │  ├─ Subscriptions      │  ├─ Socket.IO        │
│  ├─ Rate Limiting            │  └─ Batched Queries    │  └─ Room-based       │
│  ├─ Age-Based Filtering      │                        │      (per-family)    │
│  └─ Request Validation       │                        │                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Frappe Framework v15+                                                      │
│  ├─ DocTypes (Data Models)                                                  │
│  ├─ Controllers (Business Logic)                                            │
│  ├─ Hooks (Event System)                                                    │
│  ├─ Scheduler (Background Jobs)                                             │
│  └─ Workflow Engine                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Dartwing Core Modules                                                      │
│  ├─ dartwing_core (Base Platform)                                           │
│  ├─ dartwing_family (This Module)                                           │
│  ├─ dartwing_va (Voice Assistant)                                           │
│  └─ dartwing_integrations (Third-Party Connectors)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  MariaDB 10.6+               │  Redis 7+              │  Frappe Drive        │
│  ├─ Primary Data Store       │  ├─ Session Cache      │  ├─ File Storage     │
│  ├─ Full-Text Search         │  ├─ Real-time Pub/Sub  │  ├─ Media Files      │
│  └─ Encrypted Columns        │  └─ Rate Limit State   │  └─ Documents        │
├─────────────────────────────────────────────────────────────────────────────┤
│  TimescaleDB (optional)      │  Vector DB (Qdrant)    │  Object Storage      │
│  └─ Time-series (location,   │  └─ Semantic Search    │  └─ S3-Compatible    │
│      telemetry)              │      (manuals, docs)   │      (backups)       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Home Automation             │  Retail/Shopping       │  Education           │
│  ├─ Home Assistant           │  ├─ Amazon Orders      │  ├─ Google Classroom │
│  ├─ Apple HomeKit            │  ├─ Walmart            │  ├─ Canvas           │
│  ├─ Google Home              │  ├─ Instacart          │  ├─ PowerSchool      │
│  ├─ Amazon Alexa             │  └─ Costco             │  └─ Khan Academy     │
│  └─ Samsung SmartThings      │                        │                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Location Services           │  Vehicle Telematics    │  Health              │
│  ├─ Apple FindMy             │  ├─ OBD-II Dongles     │  ├─ MedxHealthLinc   │
│  ├─ Google Location          │  ├─ Tesla API          │  ├─ Apple Health     │
│  ├─ Tile                     │  ├─ Ford Pass          │  └─ Google Fit       │
│  └─ Samsung SmartTag         │  └─ GM OnStar          │                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 Module Activation Architecture

When `Organization.org_type = "Family"` is set, the system activates family-specific features through a module activation pattern:

```python
# dartwing_family/hooks.py

app_name = "dartwing_family"
app_title = "Dartwing Family"
app_publisher = "Opensoft Inc"
app_description = "Family Management Module for Dartwing"

# Conditional activation based on org_type
def get_org_type_modules():
    return {
        "Family": {
            "module": "dartwing_family",
            "features": [
                "family_relationships",
                "parental_controls",
                "chores_allowance",
                "family_calendar",
                "location_sharing",
                "home_automation",
                "meal_planning",
                "teen_driving",
                "emergency_broadcast"
            ],
            "ui_theme": "family",
            "permission_model": "family_hierarchical"
        }
    }

# DocType overrides for Family org_type
doctype_js = {
    "Organization": "public/js/organization_family.js"
}

# Fixtures loaded when org_type = Family
fixtures = [
    {
        "doctype": "Role",
        "filters": [["name", "in", [
            "Family Admin",
            "Family Parent",
            "Family Teen",
            "Family Child",
            "Family Extended"
        ]]]
    },
    {
        "doctype": "Chore Template",
        "filters": [["is_standard", "=", 1]]
    }
]

# Scheduler jobs
scheduler_events = {
    "daily": [
        "dartwing_family.tasks.daily_age_check",
        "dartwing_family.tasks.sync_external_calendars",
        "dartwing_family.tasks.process_allowance_payments"
    ],
    "hourly": [
        "dartwing_family.tasks.sync_location_data",
        "dartwing_family.tasks.check_geofence_alerts"
    ],
    "cron": {
        "0 6 * * *": [
            "dartwing_family.tasks.morning_briefing"
        ],
        "*/5 * * * *": [
            "dartwing_family.tasks.sync_grade_data"
        ]
    }
}
```

## 1.3 Multi-Tenant Family Isolation

Each family operates as a completely isolated tenant:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MULTI-TENANT ARCHITECTURE                            │
│                                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │   Smith Family      │  │   Johnson Family    │  │   Garcia Family     │  │
│  │   (org_001)         │  │   (org_002)         │  │   (org_003)         │  │
│  │                     │  │                     │  │                     │  │
│  │  ├─ 4 members       │  │  ├─ 6 members       │  │  ├─ 5 members       │  │
│  │  ├─ 12 chores       │  │  ├─ 8 chores        │  │  ├─ 15 chores       │  │
│  │  ├─ 3 vehicles      │  │  ├─ 2 vehicles      │  │  ├─ 4 vehicles      │  │
│  │  └─ 2 homes         │  │  └─ 1 home          │  │  └─ 1 home          │  │
│  │                     │  │                     │  │                     │  │
│  │  [Encrypted Data]   │  │  [Encrypted Data]   │  │  [Encrypted Data]   │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        SHARED INFRASTRUCTURE                          │  │
│  │  • Standard Chore Templates    • Age-Based Permission Rules          │  │
│  │  • Integration Adapters        • AI Models (no family data)          │  │
│  │  • Platform Configuration      • Audit Logging                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Isolation Implementation

```python
# dartwing_family/permissions.py

class FamilyPermissionManager:
    """Ensures complete data isolation between families."""

    @staticmethod
    def get_family_filter(user: str) -> dict:
        """Returns filter to limit queries to user's family."""
        family_member = frappe.get_value(
            "Family Member",
            {"user_account": user},
            ["parent_organization"]
        )

        if not family_member:
            frappe.throw("User is not a member of any family")

        return {"organization": family_member.parent_organization}

    @staticmethod
    def validate_family_access(doc, user: str) -> bool:
        """Validates user can access this document."""
        user_org = FamilyPermissionManager.get_user_organization(user)
        doc_org = doc.get("organization")

        if user_org != doc_org:
            frappe.throw(
                "Access Denied: You cannot access another family's data",
                frappe.PermissionError
            )

        return True

# Applied via hooks to all Family DocTypes
def has_permission(doc, ptype, user):
    if doc.doctype in FAMILY_DOCTYPES:
        return FamilyPermissionManager.validate_family_access(doc, user)
    return True
```

## 1.4 Real-Time Communication Architecture

Family updates propagate instantly using Socket.IO rooms:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        REAL-TIME EVENT FLOW                                  │
│                                                                              │
│  Event: "Johnny completed his chore"                                        │
│                                                                              │
│  1. Johnny's App → POST /api/chore/complete                                 │
│                          │                                                   │
│                          ▼                                                   │
│  2. Frappe Controller validates + saves                                      │
│                          │                                                   │
│                          ▼                                                   │
│  3. After-save hook triggers:                                               │
│     frappe.publish_realtime(                                                │
│         "family_event",                                                     │
│         {                                                                   │
│             "type": "chore_completed",                                      │
│             "member": "Johnny",                                             │
│             "chore": "Clean Room",                                          │
│             "points": 15,                                                   │
│             "money": 2.00                                                   │
│         },                                                                  │
│         room=f"family_{org_id}"                                             │
│     )                                                                       │
│                          │                                                   │
│                          ▼                                                   │
│  4. Socket.IO broadcasts to room "family_org_001"                           │
│                          │                                                   │
│     ┌────────────────────┼────────────────────┐                             │
│     ▼                    ▼                    ▼                             │
│  Mom's Phone         Dad's Phone         Emma's Tablet                      │
│  [Push Notification] [Push Notification] [UI Update]                        │
│  "Johnny earned $2!" "Johnny earned $2!" [Leaderboard refresh]              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Socket Room Management

```python
# dartwing_family/realtime.py

class FamilyRealtimeManager:
    """Manages real-time communication within families."""

    @staticmethod
    def join_family_room(user: str):
        """Called when user connects - joins their family room."""
        family_org = get_user_family_org(user)
        if family_org:
            frappe.realtime.join_room(f"family_{family_org}")

    @staticmethod
    def broadcast_family_event(
        org_id: str,
        event_type: str,
        payload: dict,
        exclude_user: str = None
    ):
        """Broadcasts event to all family members."""
        frappe.publish_realtime(
            "family_event",
            {
                "type": event_type,
                "payload": payload,
                "timestamp": now_datetime()
            },
            room=f"family_{org_id}",
            after_commit=True
        )

    @staticmethod
    def send_to_member(member_id: str, event_type: str, payload: dict):
        """Sends event to specific family member."""
        user = frappe.get_value("Family Member", member_id, "user_account")
        if user:
            frappe.publish_realtime(
                "family_event",
                {"type": event_type, "payload": payload},
                user=user
            )
```

## 1.5 Offline-First Architecture

Critical family features work without internet:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OFFLINE CAPABILITY MATRIX                            │
│                                                                              │
│  Feature                        │ Offline │ Sync Strategy                   │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Emergency contacts/medical     │   ✓     │ Cached on login, refresh daily  │
│  Today's chores                 │   ✓     │ Pre-fetched, queue completions  │
│  Family calendar (7 days)       │   ✓     │ Background sync every hour      │
│  Shopping list                  │   ✓     │ Optimistic updates, merge sync  │
│  Last known locations           │   ✓     │ Cached with timestamp           │
│  Allowance balance              │   ✓     │ Read-only cache                 │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Real-time location             │   ✗     │ Requires connection             │
│  Voice assistant                │   ✗     │ Requires connection             │
│  External integrations          │   ✗     │ Requires connection             │
│  Payments/transfers             │   ✗     │ Requires connection + verify    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sync Queue Implementation

```dart
// lib/core/sync/sync_queue.dart

class FamilySyncQueue {
  final HiveBox _pendingActionsBox;
  final ApiClient _apiClient;

  /// Queues an action for sync when online
  Future<void> queueAction(SyncAction action) async {
    await _pendingActionsBox.add(action.toJson());
  }

  /// Processes pending actions when connection restored
  Future<void> processPendingActions() async {
    final pending = _pendingActionsBox.values.toList();

    for (final actionJson in pending) {
      final action = SyncAction.fromJson(actionJson);

      try {
        await _executeAction(action);
        await _pendingActionsBox.delete(action.id);
      } on ConflictException catch (e) {
        await _handleConflict(action, e);
      }
    }
  }

  /// Handles sync conflicts with server state
  Future<void> _handleConflict(SyncAction action, ConflictException e) async {
    switch (action.conflictResolution) {
      case ConflictResolution.serverWins:
        // Discard local change, refresh from server
        await _refreshFromServer(action.doctype, action.docname);
        break;
      case ConflictResolution.clientWins:
        // Force push local change
        await _forcePush(action);
        break;
      case ConflictResolution.manual:
        // Queue for user resolution
        await _queueForManualResolution(action, e);
        break;
    }
  }
}
```

## 1.6 Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY LAYERS                                    │
│                                                                              │
│  Layer 1: Network                                                            │
│  ├─ TLS 1.3 for all connections                                             │
│  ├─ Certificate pinning in mobile apps                                       │
│  └─ WAF (Web Application Firewall)                                          │
│                                                                              │
│  Layer 2: Authentication                                                     │
│  ├─ JWT with short expiry (15 min) + refresh tokens                         │
│  ├─ Biometric authentication for sensitive actions                          │
│  ├─ Device binding for family devices                                       │
│  └─ Parental PIN for child device management                                │
│                                                                              │
│  Layer 3: Authorization                                                      │
│  ├─ Role-based access (Parent, Teen, Child, Extended)                       │
│  ├─ Age-based permission matrix                                             │
│  ├─ Family relationship-based access                                        │
│  └─ Document-level permissions                                              │
│                                                                              │
│  Layer 4: Data Protection                                                    │
│  ├─ AES-256 encryption at rest                                              │
│  ├─ Field-level encryption for PII/PHI                                      │
│  ├─ Automatic data masking for age groups                                   │
│  └─ Audit logging for all access                                            │
│                                                                              │
│  Layer 5: Privacy Compliance                                                 │
│  ├─ COPPA: Under-13 protections baked in                                    │
│  ├─ GDPR-K: EU minor protections                                            │
│  ├─ Data minimization by default                                            │
│  └─ Right to deletion implemented                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Age-Based Data Filtering

```python
# dartwing_family/security/age_filter.py

class AgeBasedDataFilter:
    """Automatically filters data based on requester's age."""

    AGE_RESTRICTED_FIELDS = {
        "Family Member": {
            "financial_details": 18,
            "full_medical_history": 16,
            "location_history_days": {6: 0, 13: 7, 16: 30, 18: 365}
        },
        "Family Asset": {
            "purchase_price": 16,
            "insurance_value": 18
        }
    }

    @staticmethod
    def filter_response(doctype: str, data: dict, requester_age: int) -> dict:
        """Removes age-restricted fields from response."""
        restrictions = AgeBasedDataFilter.AGE_RESTRICTED_FIELDS.get(doctype, {})

        filtered = data.copy()
        for field, min_age in restrictions.items():
            if isinstance(min_age, dict):
                # Graduated access (e.g., location history days)
                allowed_value = AgeBasedDataFilter._get_graduated_value(
                    min_age, requester_age
                )
                filtered[field] = allowed_value
            elif requester_age < min_age:
                filtered.pop(field, None)

        return filtered
```

## 1.7 Deployment Architecture

### Production Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION DEPLOYMENT                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        LOAD BALANCER (Azure/AWS)                    │    │
│  │                        ├─ SSL Termination                           │    │
│  │                        ├─ Geographic Routing                        │    │
│  │                        └─ Health Checks                             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│              ┌─────────────────────┼─────────────────────┐                  │
│              ▼                     ▼                     ▼                  │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │   Web Server 1  │   │   Web Server 2  │   │   Web Server 3  │           │
│  │   (Frappe)      │   │   (Frappe)      │   │   (Frappe)      │           │
│  │   + Gunicorn    │   │   + Gunicorn    │   │   + Gunicorn    │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
│              │                     │                     │                  │
│              └─────────────────────┼─────────────────────┘                  │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        SOCKET.IO CLUSTER                            │    │
│  │                        (Redis Adapter for cross-node)               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│              ┌─────────────────────┼─────────────────────┐                  │
│              ▼                     ▼                     ▼                  │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │   MariaDB       │   │   Redis Cluster │   │   Frappe Drive  │           │
│  │   Primary       │   │   (Cache+Pub/   │   │   (S3-backed)   │           │
│  │   + Replica     │   │    Sub+Queue)   │   │                 │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        BACKGROUND WORKERS                           │    │
│  │   ├─ Scheduler (cron jobs)                                          │    │
│  │   ├─ Long Queue (integrations, sync)                                │    │
│  │   ├─ Short Queue (notifications, calculations)                      │    │
│  │   └─ Default Queue (general tasks)                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Kubernetes Configuration (Optional)

```yaml
# k8s/dartwing-family/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-family-web
  namespace: dartwing
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dartwing-family
      component: web
  template:
    spec:
      containers:
        - name: frappe
          image: dartwing/family:latest
          ports:
            - containerPort: 8000
          env:
            - name: FRAPPE_SITE
              value: "family.dartwing.app"
            - name: REDIS_CACHE
              valueFrom:
                secretKeyRef:
                  name: dartwing-secrets
                  key: redis-cache-url
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /api/method/ping
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
```

---

_End of Section 1: System Architecture Overview_

**Next Section:** Section 2 - Data Model Architecture (DocTypes, relationships, field definitions)

# Section 2: Data Model Architecture

## 2.1 DocType Hierarchy Overview

The Dartwing Family module consists of 45+ DocTypes organized into logical domains:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DOCTYPE DOMAIN MAP                                   │
│                                                                              │
│  CORE FAMILY                    │  PARENTAL CONTROLS                        │
│  ├─ Family Member               │  ├─ Screen Time Profile                   │
│  ├─ Family Relationship         │  ├─ App Approval                          │
│  ├─ Custody Schedule            │  ├─ Approved Contact                      │
│  ├─ Custody Schedule Rule       │  ├─ Content Filter Profile                │
│  └─ Family Permission Profile   │  └─ Device Management                     │
│                                 │                                            │
│  CALENDAR & EVENTS              │  CHORES & REWARDS                         │
│  ├─ Family Calendar Event       │  ├─ Chore Template                        │
│  ├─ Event Reminder              │  ├─ Chore Assignment                      │
│  ├─ External Calendar Sync      │  ├─ Chore Completion                      │
│  └─ Transportation Request      │  ├─ Reward Rule                           │
│                                 │  └─ Point Transaction                     │
│  FINANCE & ALLOWANCE            │                                            │
│  ├─ Allowance Configuration     │  ACADEMICS                                │
│  ├─ Allowance Payment           │  ├─ Academic Record                       │
│  ├─ Savings Goal                │  ├─ Academic Class                        │
│  ├─ Savings Transaction         │  ├─ Grade Reward Rule                     │
│  └─ Parent Match Program        │  └─ Learning Platform Progress            │
│                                 │                                            │
│  MEDICAL & EMERGENCY            │  LOCATION & SAFETY                        │
│  ├─ Family Medical Profile      │  ├─ Family Geofence                       │
│  ├─ Medical Allergy             │  ├─ Location History                      │
│  ├─ Current Medication          │  ├─ Check-In Request                      │
│  ├─ Immunization Record         │  └─ Emergency SOS Event                   │
│  └─ Emergency Contact           │                                            │
│                                 │  HOME AUTOMATION                           │
│  INVENTORY & ASSETS             │  ├─ Home Platform Integration             │
│  ├─ Storage Location            │  ├─ Family Home Automation                │
│  ├─ Household Item              │  ├─ Weather Automation                    │
│  ├─ Family Asset                │  └─ Voice Command Restriction             │
│  ├─ Asset Checkout Log          │                                            │
│  └─ Maintenance Schedule        │  MEAL PLANNING                            │
│                                 │  ├─ Meal Plan                              │
│  VOICE & COMMUNICATION          │  ├─ Family Recipe                         │
│  ├─ Family Voice Profile        │  ├─ Shopping List                         │
│  ├─ Voice Training Sample       │  └─ Shopping List Item                    │
│  ├─ Family Broadcast            │                                            │
│  └─ Broadcast Response          │  TEEN DRIVING                             │
│                                 │  ├─ Driving Profile                       │
│  INTEGRATIONS                   │  ├─ Driving Trip                          │
│  ├─ Retail Account Integration  │  ├─ Driving Event                         │
│  ├─ Education Platform Sync     │  └─ Driving Privilege                     │
│  └─ Vehicle Integration         │                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Core Family DocTypes

### Family Member

The central identity DocType for all family members.

```python
# dartwing_family/doctype/family_member/family_member.json
{
    "doctype": "DocType",
    "name": "Family Member",
    "module": "Dartwing Family",
    "naming_rule": "Expression",
    "autoname": "format:FM-{organization}-{####}",
    "track_changes": 1,
    "track_views": 1,

    "fields": [
        # ─── IDENTITY ───────────────────────────────────────────────────
        {
            "fieldname": "first_name",
            "fieldtype": "Data",
            "label": "First Name",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "last_name",
            "fieldtype": "Data",
            "label": "Last Name",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "nickname",
            "fieldtype": "Data",
            "label": "Nickname",
            "description": "What the family calls this person"
        },
        {
            "fieldname": "date_of_birth",
            "fieldtype": "Date",
            "label": "Date of Birth",
            "reqd": 1
        },
        {
            "fieldname": "gender",
            "fieldtype": "Select",
            "label": "Gender",
            "options": "\nMale\nFemale\nNon-Binary\nPrefer not to say"
        },
        {
            "fieldname": "photo",
            "fieldtype": "Attach Image",
            "label": "Photo"
        },

        # ─── COMPUTED FIELDS ────────────────────────────────────────────
        {
            "fieldname": "age",
            "fieldtype": "Int",
            "label": "Age",
            "read_only": 1,
            "description": "Calculated from date_of_birth"
        },
        {
            "fieldname": "age_category",
            "fieldtype": "Select",
            "label": "Age Category",
            "options": "Infant\nToddler\nChild\nTween\nTeen\nAdult\nSenior",
            "read_only": 1
        },
        {
            "fieldname": "is_minor",
            "fieldtype": "Check",
            "label": "Is Minor",
            "read_only": 1,
            "description": "Under 18"
        },
        {
            "fieldname": "is_coppa_protected",
            "fieldtype": "Check",
            "label": "COPPA Protected",
            "read_only": 1,
            "description": "Under 13 - special privacy rules apply"
        },

        # ─── LINKED ACCOUNTS ────────────────────────────────────────────
        {
            "fieldname": "section_accounts",
            "fieldtype": "Section Break",
            "label": "Linked Accounts"
        },
        {
            "fieldname": "user_account",
            "fieldtype": "Link",
            "label": "System User",
            "options": "User",
            "description": "Frappe user account for login"
        },
        {
            "fieldname": "dartwing_user",
            "fieldtype": "Link",
            "label": "Dartwing User",
            "options": "Dartwing User"
        },
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Family Organization",
            "options": "Organization",
            "reqd": 1,
            "in_standard_filter": 1
        },

        # ─── PERMISSIONS ────────────────────────────────────────────────
        {
            "fieldname": "section_permissions",
            "fieldtype": "Section Break",
            "label": "Permissions & Roles"
        },
        {
            "fieldname": "family_role",
            "fieldtype": "Select",
            "label": "Family Role",
            "options": "Parent\nStep-Parent\nGrandparent\nTeen\nChild\nExtended Family\nCaregiver",
            "reqd": 1
        },
        {
            "fieldname": "is_admin",
            "fieldtype": "Check",
            "label": "Family Admin",
            "description": "Can manage all family settings"
        },
        {
            "fieldname": "is_guardian",
            "fieldtype": "Check",
            "label": "Legal Guardian",
            "description": "Has legal authority over minors"
        },
        {
            "fieldname": "permission_profile",
            "fieldtype": "Link",
            "label": "Permission Profile",
            "options": "Family Permission Profile"
        },

        # ─── CONTACT INFO ───────────────────────────────────────────────
        {
            "fieldname": "section_contact",
            "fieldtype": "Section Break",
            "label": "Contact Information"
        },
        {
            "fieldname": "email",
            "fieldtype": "Data",
            "label": "Email",
            "options": "Email"
        },
        {
            "fieldname": "phone",
            "fieldtype": "Data",
            "label": "Phone",
            "options": "Phone"
        },

        # ─── RELATIONSHIPS (Child Table) ────────────────────────────────
        {
            "fieldname": "section_relationships",
            "fieldtype": "Section Break",
            "label": "Family Relationships"
        },
        {
            "fieldname": "relationships",
            "fieldtype": "Table",
            "label": "Relationships",
            "options": "Family Relationship Link"
        },

        # ─── MEDICAL REFERENCE ──────────────────────────────────────────
        {
            "fieldname": "section_medical",
            "fieldtype": "Section Break",
            "label": "Medical Information"
        },
        {
            "fieldname": "medical_profile",
            "fieldtype": "Link",
            "label": "Medical Profile",
            "options": "Family Medical Profile"
        },
        {
            "fieldname": "has_critical_allergies",
            "fieldtype": "Check",
            "label": "Has Critical Allergies",
            "read_only": 1
        },

        # ─── STATUS ─────────────────────────────────────────────────────
        {
            "fieldname": "section_status",
            "fieldtype": "Section Break",
            "label": "Status"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Active\nInactive\nDeceased",
            "default": "Active"
        },
        {
            "fieldname": "last_activity",
            "fieldtype": "Datetime",
            "label": "Last Activity",
            "read_only": 1
        }
    ],

    "permissions": [
        {"role": "Family Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Family Parent", "read": 1, "write": 1, "create": 1},
        {"role": "Family Teen", "read": 1, "if_owner": 1},
        {"role": "Family Child", "read": 1, "if_owner": 1}
    ]
}
```

### Family Member Controller

```python
# dartwing_family/doctype/family_member/family_member.py

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, date_diff
from dartwing_family.utils.age import calculate_age, get_age_category

class FamilyMember(Document):
    def validate(self):
        self.calculate_age_fields()
        self.validate_guardian_age()
        self.set_permission_profile()

    def before_save(self):
        if self.has_value_changed("date_of_birth"):
            self.update_age_based_permissions()

    def after_insert(self):
        self.create_default_profiles()
        self.setup_user_permissions()

    def calculate_age_fields(self):
        """Calculate age and related fields from DOB."""
        if self.date_of_birth:
            self.age = calculate_age(self.date_of_birth)
            self.age_category = get_age_category(self.age)
            self.is_minor = self.age < 18
            self.is_coppa_protected = self.age < 13

    def validate_guardian_age(self):
        """Ensure guardians are adults."""
        if self.is_guardian and self.age < 18:
            frappe.throw("Guardians must be 18 or older")

    def set_permission_profile(self):
        """Assign appropriate permission profile based on age."""
        if not self.permission_profile:
            profile_name = self._get_default_permission_profile()
            self.permission_profile = profile_name

    def _get_default_permission_profile(self) -> str:
        """Get default permission profile based on age category."""
        profile_map = {
            "Infant": "Child Under 6",
            "Toddler": "Child Under 6",
            "Child": "Child 6-12",
            "Tween": "Tween 13-15",
            "Teen": "Teen 16-17",
            "Adult": "Adult",
            "Senior": "Adult"
        }
        return profile_map.get(self.age_category, "Adult")

    def create_default_profiles(self):
        """Create linked profiles for new family members."""
        # Create medical profile
        if not self.medical_profile:
            med_profile = frappe.new_doc("Family Medical Profile")
            med_profile.family_member = self.name
            med_profile.organization = self.organization
            med_profile.insert(ignore_permissions=True)
            self.db_set("medical_profile", med_profile.name)

        # Create screen time profile for minors
        if self.is_minor:
            screen_profile = frappe.new_doc("Screen Time Profile")
            screen_profile.family_member = self.name
            screen_profile.organization = self.organization
            screen_profile.apply_age_defaults(self.age)
            screen_profile.insert(ignore_permissions=True)

    def setup_user_permissions(self):
        """Setup Frappe user permissions for family member."""
        if self.user_account:
            # Add to family organization
            frappe.get_doc({
                "doctype": "User Permission",
                "user": self.user_account,
                "allow": "Organization",
                "for_value": self.organization,
                "apply_to_all_doctypes": 1
            }).insert(ignore_permissions=True)

            # Assign family role
            role = self._get_frappe_role()
            if role:
                frappe.get_doc({
                    "doctype": "Has Role",
                    "parent": self.user_account,
                    "parenttype": "User",
                    "parentfield": "roles",
                    "role": role
                }).insert(ignore_permissions=True)

    def _get_frappe_role(self) -> str:
        """Map family role to Frappe role."""
        role_map = {
            "Parent": "Family Parent",
            "Step-Parent": "Family Parent",
            "Grandparent": "Family Extended",
            "Teen": "Family Teen",
            "Child": "Family Child",
            "Extended Family": "Family Extended",
            "Caregiver": "Family Extended"
        }
        role = role_map.get(self.family_role, "Family Extended")
        if self.is_admin:
            role = "Family Admin"
        return role

    def update_age_based_permissions(self):
        """Called when age changes to update permissions."""
        old_age = frappe.db.get_value("Family Member", self.name, "age")

        # Check for milestone transitions
        if old_age and self.age:
            if old_age < 13 and self.age >= 13:
                self.trigger_13th_birthday_transition()
            elif old_age < 18 and self.age >= 18:
                self.trigger_18th_birthday_transition()

    def trigger_13th_birthday_transition(self):
        """Handle transition out of COPPA protection."""
        # Update permission profile
        self.permission_profile = "Tween 13-15"

        # Notify parents
        self.notify_guardians(
            subject=f"{self.first_name} is now 13!",
            message=f"{self.first_name} has turned 13 and their permissions have been updated. "
                    f"Some COPPA restrictions have been lifted. Please review their settings."
        )

        # Log transition
        frappe.log_error(
            title="COPPA Transition",
            message=f"Family Member {self.name} transitioned out of COPPA protection"
        )

    def trigger_18th_birthday_transition(self):
        """Handle transition to adulthood."""
        self.permission_profile = "Adult"
        self.is_minor = 0

        # Notify the new adult
        if self.user_account:
            frappe.sendmail(
                recipients=[self.email],
                subject="Happy 18th Birthday! Your Dartwing account has been upgraded",
                message=f"Congratulations {self.first_name}! You now have full adult access. "
                        f"Parental oversight has been removed. You can now manage your own privacy settings."
            )

        # Offer to convert to independent account
        frappe.publish_realtime(
            "independence_offer",
            {"member": self.name},
            user=self.user_account
        )

    def notify_guardians(self, subject: str, message: str):
        """Send notification to all guardians."""
        guardians = frappe.get_all(
            "Family Relationship",
            filters={
                "person_b": self.name,
                "is_legal_guardian": 1,
                "status": "Active"
            },
            fields=["person_a"]
        )

        for guardian in guardians:
            guardian_doc = frappe.get_doc("Family Member", guardian.person_a)
            if guardian_doc.email:
                frappe.sendmail(
                    recipients=[guardian_doc.email],
                    subject=subject,
                    message=message
                )


# Daily scheduled job to check ages
def daily_age_check():
    """Run daily to update age-based fields for all family members."""
    members = frappe.get_all(
        "Family Member",
        filters={"status": "Active"},
        fields=["name"]
    )

    for member in members:
        doc = frappe.get_doc("Family Member", member.name)
        old_age = doc.age
        doc.calculate_age_fields()

        if doc.age != old_age:
            doc.save(ignore_permissions=True)
            frappe.db.commit()
```

### Family Relationship

```python
# dartwing_family/doctype/family_relationship/family_relationship.json
{
    "doctype": "DocType",
    "name": "Family Relationship",
    "module": "Dartwing Family",
    "naming_rule": "Expression",
    "autoname": "format:REL-{person_a}-{person_b}",
    "track_changes": 1,

    "fields": [
        # ─── PEOPLE ─────────────────────────────────────────────────────
        {
            "fieldname": "person_a",
            "fieldtype": "Link",
            "label": "Person A",
            "options": "Family Member",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "person_b",
            "fieldtype": "Link",
            "label": "Person B",
            "options": "Family Member",
            "reqd": 1,
            "in_list_view": 1
        },

        # ─── RELATIONSHIP TYPE ──────────────────────────────────────────
        {
            "fieldname": "relationship_type",
            "fieldtype": "Select",
            "label": "Relationship Type",
            "options": "Parent-Child\nSpouse\nSibling\nGrandparent-Grandchild\nGuardian-Ward\nAunt/Uncle-Niece/Nephew\nCousin\nGodparent\nStep-Parent-Step-Child\nFoster",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "a_role",
            "fieldtype": "Data",
            "label": "Person A's Role",
            "read_only": 1,
            "description": "e.g., Parent, Grandparent"
        },
        {
            "fieldname": "b_role",
            "fieldtype": "Data",
            "label": "Person B's Role",
            "read_only": 1,
            "description": "e.g., Child, Grandchild"
        },

        # ─── LEGAL / CUSTODY ────────────────────────────────────────────
        {
            "fieldname": "section_legal",
            "fieldtype": "Section Break",
            "label": "Legal & Custody"
        },
        {
            "fieldname": "is_legal_guardian",
            "fieldtype": "Check",
            "label": "Is Legal Guardian",
            "description": "Person A is legal guardian of Person B"
        },
        {
            "fieldname": "custody_schedule",
            "fieldtype": "Link",
            "label": "Custody Schedule",
            "options": "Custody Schedule",
            "depends_on": "eval:doc.relationship_type=='Parent-Child'"
        },
        {
            "fieldname": "legal_documents",
            "fieldtype": "Table",
            "label": "Legal Documents",
            "options": "Family Legal Document"
        },

        # ─── STATUS ─────────────────────────────────────────────────────
        {
            "fieldname": "section_status",
            "fieldtype": "Section Break",
            "label": "Status"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Active\nSeparated\nDivorced\nDeceased\nInactive",
            "default": "Active"
        },
        {
            "fieldname": "start_date",
            "fieldtype": "Date",
            "label": "Start Date"
        },
        {
            "fieldname": "end_date",
            "fieldtype": "Date",
            "label": "End Date"
        },

        # ─── REVERSE LINK ───────────────────────────────────────────────
        {
            "fieldname": "reverse_relationship",
            "fieldtype": "Link",
            "label": "Reverse Relationship",
            "options": "Family Relationship",
            "read_only": 1
        },

        # ─── ORGANIZATION ───────────────────────────────────────────────
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Organization",
            "options": "Organization",
            "reqd": 1,
            "hidden": 1
        }
    ]
}
```

### Family Relationship Controller

```python
# dartwing_family/doctype/family_relationship/family_relationship.py

import frappe
from frappe.model.document import Document

RELATIONSHIP_ROLES = {
    "Parent-Child": ("Parent", "Child"),
    "Spouse": ("Spouse", "Spouse"),
    "Sibling": ("Sibling", "Sibling"),
    "Grandparent-Grandchild": ("Grandparent", "Grandchild"),
    "Guardian-Ward": ("Guardian", "Ward"),
    "Aunt/Uncle-Niece/Nephew": ("Aunt/Uncle", "Niece/Nephew"),
    "Cousin": ("Cousin", "Cousin"),
    "Godparent": ("Godparent", "Godchild"),
    "Step-Parent-Step-Child": ("Step-Parent", "Step-Child"),
    "Foster": ("Foster Parent", "Foster Child")
}

class FamilyRelationship(Document):
    def validate(self):
        self.set_roles()
        self.validate_relationship_rules()
        self.set_organization()

    def after_insert(self):
        self.create_reverse_relationship()
        self.create_derived_relationships()
        self.update_guardian_status()

    def on_trash(self):
        # Delete reverse relationship
        if self.reverse_relationship:
            frappe.delete_doc(
                "Family Relationship",
                self.reverse_relationship,
                ignore_permissions=True
            )

    def set_roles(self):
        """Set the role labels based on relationship type."""
        if self.relationship_type in RELATIONSHIP_ROLES:
            self.a_role, self.b_role = RELATIONSHIP_ROLES[self.relationship_type]

    def validate_relationship_rules(self):
        """Validate relationship-specific rules."""
        person_a = frappe.get_doc("Family Member", self.person_a)
        person_b = frappe.get_doc("Family Member", self.person_b)

        if self.relationship_type == "Parent-Child":
            # Parent must be at least 16 years older OR legal guardian
            if person_a.age - person_b.age < 16 and not self.is_legal_guardian:
                frappe.throw(
                    "Parent must be at least 16 years older than child, "
                    "unless marked as legal guardian"
                )

        elif self.relationship_type == "Spouse":
            # Both must be 18+
            if person_a.age < 18 or person_b.age < 18:
                frappe.throw("Both spouses must be 18 or older")

        elif self.relationship_type in ["Guardian-Ward", "Foster"]:
            # Require legal document
            if not self.legal_documents:
                frappe.msgprint(
                    "Legal documentation recommended for Guardian/Foster relationships",
                    indicator="orange"
                )

    def set_organization(self):
        """Set organization from person_a."""
        if not self.organization:
            self.organization = frappe.get_value(
                "Family Member", self.person_a, "organization"
            )

    def create_reverse_relationship(self):
        """Create the bidirectional reverse relationship."""
        if self.reverse_relationship:
            return

        # Create reverse
        reverse = frappe.new_doc("Family Relationship")
        reverse.person_a = self.person_b
        reverse.person_b = self.person_a
        reverse.relationship_type = self.relationship_type
        reverse.a_role = self.b_role
        reverse.b_role = self.a_role
        reverse.is_legal_guardian = 0  # Only one direction for guardian
        reverse.status = self.status
        reverse.start_date = self.start_date
        reverse.organization = self.organization
        reverse.reverse_relationship = self.name
        reverse.flags.ignore_reverse_creation = True
        reverse.insert(ignore_permissions=True)

        # Link back
        self.db_set("reverse_relationship", reverse.name)

    def create_derived_relationships(self):
        """Auto-create extended family relationships."""
        if self.relationship_type == "Parent-Child":
            self._create_grandparent_relationships()
            self._create_sibling_relationships()
            self._create_aunt_uncle_relationships()

    def _create_grandparent_relationships(self):
        """Create grandparent relationships when parent has parent."""
        # Find parent's parents
        parent_parents = frappe.get_all(
            "Family Relationship",
            filters={
                "person_b": self.person_a,  # person_a is the parent
                "relationship_type": "Parent-Child",
                "status": "Active"
            },
            fields=["person_a"]  # grandparents
        )

        for gp in parent_parents:
            # Create grandparent-grandchild relationship
            if not frappe.db.exists("Family Relationship", {
                "person_a": gp.person_a,
                "person_b": self.person_b,
                "relationship_type": "Grandparent-Grandchild"
            }):
                frappe.get_doc({
                    "doctype": "Family Relationship",
                    "person_a": gp.person_a,
                    "person_b": self.person_b,
                    "relationship_type": "Grandparent-Grandchild",
                    "organization": self.organization
                }).insert(ignore_permissions=True)

    def _create_sibling_relationships(self):
        """Create sibling relationships for children of same parent."""
        # Find other children of this parent
        other_children = frappe.get_all(
            "Family Relationship",
            filters={
                "person_a": self.person_a,  # same parent
                "person_b": ["!=", self.person_b],  # different child
                "relationship_type": "Parent-Child",
                "status": "Active"
            },
            fields=["person_b"]
        )

        for sibling in other_children:
            # Create sibling relationship if doesn't exist
            if not frappe.db.exists("Family Relationship", {
                "person_a": self.person_b,
                "person_b": sibling.person_b,
                "relationship_type": "Sibling"
            }):
                frappe.get_doc({
                    "doctype": "Family Relationship",
                    "person_a": self.person_b,
                    "person_b": sibling.person_b,
                    "relationship_type": "Sibling",
                    "organization": self.organization
                }).insert(ignore_permissions=True)

    def _create_aunt_uncle_relationships(self):
        """Create aunt/uncle relationships from parent's siblings."""
        # Find parent's siblings
        parent_siblings = frappe.get_all(
            "Family Relationship",
            filters={
                "person_a": self.person_a,
                "relationship_type": "Sibling",
                "status": "Active"
            },
            fields=["person_b"]  # aunts/uncles
        )

        for aunt_uncle in parent_siblings:
            if not frappe.db.exists("Family Relationship", {
                "person_a": aunt_uncle.person_b,
                "person_b": self.person_b,
                "relationship_type": "Aunt/Uncle-Niece/Nephew"
            }):
                frappe.get_doc({
                    "doctype": "Family Relationship",
                    "person_a": aunt_uncle.person_b,
                    "person_b": self.person_b,
                    "relationship_type": "Aunt/Uncle-Niece/Nephew",
                    "organization": self.organization
                }).insert(ignore_permissions=True)

    def update_guardian_status(self):
        """Update is_guardian flag on Family Member."""
        if self.is_legal_guardian:
            frappe.db.set_value(
                "Family Member",
                self.person_a,
                "is_guardian",
                1
            )
```

## 2.3 Custody Schedule DocTypes

### Custody Schedule

```python
# dartwing_family/doctype/custody_schedule/custody_schedule.json
{
    "doctype": "DocType",
    "name": "Custody Schedule",
    "module": "Dartwing Family",

    "fields": [
        {
            "fieldname": "child",
            "fieldtype": "Link",
            "label": "Child",
            "options": "Family Member",
            "reqd": 1
        },
        {
            "fieldname": "parent_a",
            "fieldtype": "Link",
            "label": "Parent A",
            "options": "Family Member",
            "reqd": 1
        },
        {
            "fieldname": "parent_b",
            "fieldtype": "Link",
            "label": "Parent B",
            "options": "Family Member",
            "reqd": 1
        },
        {
            "fieldname": "schedule_type",
            "fieldtype": "Select",
            "label": "Schedule Type",
            "options": "50/50 Weekly\n50/50 Bi-Weekly\nPrimary/Visitation\n2-2-3\n3-4-4-3\nCustom",
            "reqd": 1
        },
        {
            "fieldname": "schedule_rules",
            "fieldtype": "Table",
            "label": "Schedule Rules",
            "options": "Custody Schedule Rule"
        },
        {
            "fieldname": "holiday_schedule",
            "fieldtype": "Link",
            "label": "Holiday Schedule",
            "options": "Holiday Custody Schedule"
        },
        {
            "fieldname": "section_visibility",
            "fieldtype": "Section Break",
            "label": "Visibility Rules"
        },
        {
            "fieldname": "parent_a_sees_location_during_b",
            "fieldtype": "Check",
            "label": "Parent A sees location during Parent B's time",
            "default": 1
        },
        {
            "fieldname": "parent_b_sees_location_during_a",
            "fieldtype": "Check",
            "label": "Parent B sees location during Parent A's time",
            "default": 1
        },
        {
            "fieldname": "section_notifications",
            "fieldtype": "Section Break",
            "label": "Notifications"
        },
        {
            "fieldname": "notify_handoff",
            "fieldtype": "Check",
            "label": "Notify on custody handoff",
            "default": 1
        },
        {
            "fieldname": "notify_arrival",
            "fieldtype": "Check",
            "label": "Notify on arrival at other parent",
            "default": 1
        },
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Organization",
            "options": "Organization",
            "reqd": 1,
            "hidden": 1
        }
    ]
}
```

### Custody Schedule Controller

```python
# dartwing_family/doctype/custody_schedule/custody_schedule.py

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, get_first_day_of_week, add_days

class CustodySchedule(Document):
    def validate(self):
        self.validate_parents()
        self.generate_schedule_rules()

    def validate_parents(self):
        """Ensure both parents are guardians of the child."""
        for parent_field in ["parent_a", "parent_b"]:
            parent = getattr(self, parent_field)
            if not frappe.db.exists("Family Relationship", {
                "person_a": parent,
                "person_b": self.child,
                "relationship_type": ["in", ["Parent-Child", "Guardian-Ward"]],
                "status": "Active"
            }):
                frappe.throw(
                    f"{frappe.get_value('Family Member', parent, 'first_name')} "
                    f"is not a guardian of this child"
                )

    def generate_schedule_rules(self):
        """Generate schedule rules based on type if not custom."""
        if self.schedule_type == "Custom":
            return

        if self.schedule_rules:
            return  # Don't overwrite existing rules

        rules = []
        if self.schedule_type == "50/50 Weekly":
            # Week 1: Parent A, Week 2: Parent B
            rules = [
                {"week_number": "odd", "parent": "parent_a"},
                {"week_number": "even", "parent": "parent_b"}
            ]
        elif self.schedule_type == "50/50 Bi-Weekly":
            # 2 weeks each
            rules = [
                {"week_number": "1,2", "parent": "parent_a"},
                {"week_number": "3,4", "parent": "parent_b"}
            ]
        elif self.schedule_type == "2-2-3":
            # Mon-Tue: A, Wed-Thu: B, Fri-Sun: alternates
            rules = [
                {"day_of_week": "Monday,Tuesday", "parent": "parent_a"},
                {"day_of_week": "Wednesday,Thursday", "parent": "parent_b"},
                {"day_of_week": "Friday,Saturday,Sunday", "week_number": "odd", "parent": "parent_a"},
                {"day_of_week": "Friday,Saturday,Sunday", "week_number": "even", "parent": "parent_b"}
            ]

        for rule in rules:
            self.append("schedule_rules", {
                "day_of_week": rule.get("day_of_week", ""),
                "week_number": rule.get("week_number", ""),
                "assigned_parent": rule["parent"]
            })

    def get_current_parent(self, date=None) -> str:
        """Determine which parent has custody on given date."""
        if not date:
            date = getdate()

        # Check holiday schedule first
        if self.holiday_schedule:
            holiday_parent = self.check_holiday_schedule(date)
            if holiday_parent:
                return holiday_parent

        # Check regular schedule
        for rule in self.schedule_rules:
            if self._rule_matches(rule, date):
                return getattr(self, rule.assigned_parent)

        return self.parent_a  # Default

    def _rule_matches(self, rule, date) -> bool:
        """Check if a schedule rule matches the given date."""
        day_name = date.strftime("%A")
        week_num = date.isocalendar()[1]

        # Check day of week
        if rule.day_of_week:
            if day_name not in rule.day_of_week:
                return False

        # Check week number
        if rule.week_number:
            if rule.week_number == "odd" and week_num % 2 == 0:
                return False
            if rule.week_number == "even" and week_num % 2 == 1:
                return False
            if rule.week_number not in ["odd", "even"]:
                weeks = [int(w) for w in rule.week_number.split(",")]
                if (week_num % 4) not in weeks:
                    return False

        return True

    def check_holiday_schedule(self, date) -> str:
        """Check if date falls under holiday custody rules."""
        # Implementation for holiday schedule checking
        pass
```

## 2.4 Chore System DocTypes

### Chore Template

```python
# dartwing_family/doctype/chore_template/chore_template.json
{
    "doctype": "DocType",
    "name": "Chore Template",
    "module": "Dartwing Family",

    "fields": [
        {
            "fieldname": "chore_name",
            "fieldtype": "Data",
            "label": "Chore Name",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "description",
            "fieldtype": "Text",
            "label": "Description"
        },
        {
            "fieldname": "instructions",
            "fieldtype": "Text Editor",
            "label": "Instructions"
        },
        {
            "fieldname": "estimated_minutes",
            "fieldtype": "Int",
            "label": "Estimated Duration (minutes)",
            "default": 15
        },
        {
            "fieldname": "category",
            "fieldtype": "Select",
            "label": "Category",
            "options": "Bedroom\nBathroom\nKitchen\nLiving Areas\nOutdoor\nPet Care\nLaundry\nDishes\nOther",
            "in_list_view": 1
        },
        {
            "fieldname": "difficulty",
            "fieldtype": "Select",
            "label": "Difficulty",
            "options": "Easy\nMedium\nHard",
            "default": "Easy"
        },
        {
            "fieldname": "section_age",
            "fieldtype": "Section Break",
            "label": "Age Requirements"
        },
        {
            "fieldname": "minimum_age",
            "fieldtype": "Int",
            "label": "Minimum Age",
            "default": 6
        },
        {
            "fieldname": "maximum_age",
            "fieldtype": "Int",
            "label": "Maximum Age",
            "default": 99
        },
        {
            "fieldname": "section_verification",
            "fieldtype": "Section Break",
            "label": "Verification"
        },
        {
            "fieldname": "requires_photo",
            "fieldtype": "Check",
            "label": "Requires Photo Proof"
        },
        {
            "fieldname": "requires_parent_verification",
            "fieldtype": "Check",
            "label": "Requires Parent Verification"
        },
        {
            "fieldname": "verification_checklist",
            "fieldtype": "Table",
            "label": "Verification Checklist",
            "options": "Chore Checklist Item"
        },
        {
            "fieldname": "section_rewards",
            "fieldtype": "Section Break",
            "label": "Rewards"
        },
        {
            "fieldname": "base_points",
            "fieldtype": "Int",
            "label": "Base Points",
            "default": 10
        },
        {
            "fieldname": "base_money",
            "fieldtype": "Currency",
            "label": "Base Money Reward",
            "default": 1.00
        },
        {
            "fieldname": "early_bonus",
            "fieldtype": "Currency",
            "label": "Early Completion Bonus"
        },
        {
            "fieldname": "screen_time_bonus",
            "fieldtype": "Int",
            "label": "Screen Time Bonus (minutes)"
        },
        {
            "fieldname": "section_schedule",
            "fieldtype": "Section Break",
            "label": "Scheduling"
        },
        {
            "fieldname": "default_frequency",
            "fieldtype": "Select",
            "label": "Default Frequency",
            "options": "Daily\nWeekly\nBi-Weekly\nMonthly\nAs Needed"
        },
        {
            "fieldname": "default_day",
            "fieldtype": "Select",
            "label": "Default Day",
            "options": "\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday"
        },
        {
            "fieldname": "default_time",
            "fieldtype": "Time",
            "label": "Default Due Time"
        },
        {
            "fieldname": "is_standard",
            "fieldtype": "Check",
            "label": "Is Standard Template",
            "description": "Provided by system"
        },
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Organization",
            "options": "Organization",
            "description": "Null for standard templates"
        }
    ]
}
```

### Chore Assignment

```python
# dartwing_family/doctype/chore_assignment/chore_assignment.json
{
    "doctype": "DocType",
    "name": "Chore Assignment",
    "module": "Dartwing Family",
    "naming_rule": "Expression",
    "autoname": "format:CHR-{assigned_to}-{due_date}-{####}",

    "fields": [
        {
            "fieldname": "chore_template",
            "fieldtype": "Link",
            "label": "Chore",
            "options": "Chore Template",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "assigned_to",
            "fieldtype": "Link",
            "label": "Assigned To",
            "options": "Family Member",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "assigned_by",
            "fieldtype": "Link",
            "label": "Assigned By",
            "options": "Family Member"
        },
        {
            "fieldname": "section_schedule",
            "fieldtype": "Section Break",
            "label": "Schedule"
        },
        {
            "fieldname": "due_date",
            "fieldtype": "Date",
            "label": "Due Date",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "due_time",
            "fieldtype": "Time",
            "label": "Due Time"
        },
        {
            "fieldname": "recurrence",
            "fieldtype": "Link",
            "label": "Recurrence",
            "options": "Chore Recurrence"
        },
        {
            "fieldname": "section_status",
            "fieldtype": "Section Break",
            "label": "Status"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Pending\nIn Progress\nCompleted\nVerified\nOverdue\nSkipped",
            "default": "Pending",
            "in_list_view": 1
        },
        {
            "fieldname": "section_completion",
            "fieldtype": "Section Break",
            "label": "Completion"
        },
        {
            "fieldname": "completed_at",
            "fieldtype": "Datetime",
            "label": "Completed At"
        },
        {
            "fieldname": "completion_photo",
            "fieldtype": "Attach Image",
            "label": "Completion Photo"
        },
        {
            "fieldname": "completion_notes",
            "fieldtype": "Small Text",
            "label": "Completion Notes"
        },
        {
            "fieldname": "section_verification",
            "fieldtype": "Section Break",
            "label": "Verification"
        },
        {
            "fieldname": "verified_by",
            "fieldtype": "Link",
            "label": "Verified By",
            "options": "Family Member"
        },
        {
            "fieldname": "verified_at",
            "fieldtype": "Datetime",
            "label": "Verified At"
        },
        {
            "fieldname": "verification_status",
            "fieldtype": "Select",
            "label": "Verification Status",
            "options": "\nApproved\nNeeds Redo\nPartial Credit"
        },
        {
            "fieldname": "verification_notes",
            "fieldtype": "Small Text",
            "label": "Verification Notes"
        },
        {
            "fieldname": "section_rewards",
            "fieldtype": "Section Break",
            "label": "Rewards Earned"
        },
        {
            "fieldname": "points_earned",
            "fieldtype": "Int",
            "label": "Points Earned",
            "read_only": 1
        },
        {
            "fieldname": "money_earned",
            "fieldtype": "Currency",
            "label": "Money Earned",
            "read_only": 1
        },
        {
            "fieldname": "screen_time_earned",
            "fieldtype": "Int",
            "label": "Screen Time Earned (minutes)",
            "read_only": 1
        },
        {
            "fieldname": "bonuses",
            "fieldtype": "Table",
            "label": "Bonuses Applied",
            "options": "Chore Bonus"
        },
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Organization",
            "options": "Organization",
            "reqd": 1,
            "hidden": 1
        }
    ]
}
```

### Chore Assignment Controller

```python
# dartwing_family/doctype/chore_assignment/chore_assignment.py

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, getdate, get_datetime

class ChoreAssignment(Document):
    def validate(self):
        self.validate_age_requirement()
        self.check_overdue()

    def validate_age_requirement(self):
        """Ensure assignee meets age requirements."""
        template = frappe.get_doc("Chore Template", self.chore_template)
        member = frappe.get_doc("Family Member", self.assigned_to)

        if member.age < template.minimum_age:
            frappe.throw(
                f"{member.first_name} is too young for this chore "
                f"(minimum age: {template.minimum_age})"
            )
        if member.age > template.maximum_age:
            frappe.throw(
                f"{member.first_name} is too old for this chore "
                f"(maximum age: {template.maximum_age})"
            )

    def check_overdue(self):
        """Mark as overdue if past due date."""
        if self.status == "Pending" and self.due_date:
            if getdate(self.due_date) < getdate():
                self.status = "Overdue"

    @frappe.whitelist()
    def mark_complete(self, photo=None, notes=None):
        """Mark chore as completed by assignee."""
        template = frappe.get_doc("Chore Template", self.chore_template)

        # Validate photo requirement
        if template.requires_photo and not photo:
            frappe.throw("Photo proof is required for this chore")

        self.status = "Completed"
        self.completed_at = now_datetime()
        self.completion_photo = photo
        self.completion_notes = notes

        # If no parent verification needed, auto-verify
        if not template.requires_parent_verification:
            self.auto_verify()

        self.save()
        self.notify_family()

        return {"status": "success", "rewards": self.get_rewards_summary()}

    def auto_verify(self):
        """Auto-verify and calculate rewards."""
        self.status = "Verified"
        self.verified_at = now_datetime()
        self.verification_status = "Approved"
        self.calculate_rewards()

    @frappe.whitelist()
    def verify(self, status, notes=None, verifier=None):
        """Parent verification of completed chore."""
        self.verified_by = verifier or frappe.session.user
        self.verified_at = now_datetime()
        self.verification_status = status
        self.verification_notes = notes

        if status == "Approved":
            self.status = "Verified"
            self.calculate_rewards()
        elif status == "Needs Redo":
            self.status = "Pending"
            self.completed_at = None
        elif status == "Partial Credit":
            self.status = "Verified"
            self.calculate_rewards(partial=True)

        self.save()
        self.notify_assignee()

    def calculate_rewards(self, partial=False):
        """Calculate and apply rewards."""
        template = frappe.get_doc("Chore Template", self.chore_template)
        multiplier = 0.5 if partial else 1.0

        # Base rewards
        self.points_earned = int(template.base_points * multiplier)
        self.money_earned = template.base_money * multiplier
        self.screen_time_earned = int((template.screen_time_bonus or 0) * multiplier)

        # Check for bonuses
        self.apply_bonuses(template)

        # Credit to member's balance
        self.credit_rewards()

    def apply_bonuses(self, template):
        """Apply any applicable bonuses."""
        # Early completion bonus
        if template.early_bonus and self.completed_at:
            due_datetime = get_datetime(f"{self.due_date} {self.due_time or '23:59:59'}")
            if get_datetime(self.completed_at) < due_datetime:
                self.append("bonuses", {
                    "bonus_type": "Early Completion",
                    "bonus_amount": template.early_bonus
                })
                self.money_earned += template.early_bonus

        # Streak bonus
        streak = self.get_streak()
        if streak >= 7:
            streak_bonus = self.money_earned * 0.5  # 50% bonus for 7+ day streak
            self.append("bonuses", {
                "bonus_type": f"{streak}-Day Streak",
                "bonus_amount": streak_bonus
            })
            self.money_earned += streak_bonus

    def get_streak(self) -> int:
        """Get current streak for this chore type."""
        # Count consecutive days of completion
        streak = frappe.db.sql("""
            SELECT COUNT(*) as streak
            FROM `tabChore Assignment`
            WHERE assigned_to = %s
            AND chore_template = %s
            AND status = 'Verified'
            AND due_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY due_date DESC
        """, (self.assigned_to, self.chore_template), as_dict=True)

        return streak[0].streak if streak else 0

    def credit_rewards(self):
        """Credit rewards to family member's balance."""
        # Create point transaction
        if self.points_earned:
            frappe.get_doc({
                "doctype": "Point Transaction",
                "family_member": self.assigned_to,
                "points": self.points_earned,
                "transaction_type": "Earned",
                "source": "Chore",
                "reference_doctype": "Chore Assignment",
                "reference_name": self.name,
                "organization": self.organization
            }).insert(ignore_permissions=True)

        # Create allowance payment
        if self.money_earned:
            frappe.get_doc({
                "doctype": "Allowance Payment",
                "recipient": self.assigned_to,
                "amount": self.money_earned,
                "source_type": "Chore Completion",
                "source_reference": self.name,
                "status": "Approved",  # Auto-approved for verified chores
                "organization": self.organization
            }).insert(ignore_permissions=True)

    def notify_family(self):
        """Broadcast chore completion to family."""
        from dartwing_family.realtime import FamilyRealtimeManager

        member = frappe.get_doc("Family Member", self.assigned_to)
        template = frappe.get_doc("Chore Template", self.chore_template)

        FamilyRealtimeManager.broadcast_family_event(
            org_id=self.organization,
            event_type="chore_completed",
            payload={
                "member_name": member.first_name,
                "chore_name": template.chore_name,
                "points": self.points_earned,
                "money": float(self.money_earned or 0)
            }
        )

    def notify_assignee(self):
        """Notify assignee of verification result."""
        member = frappe.get_doc("Family Member", self.assigned_to)

        if member.user_account:
            frappe.publish_realtime(
                "chore_verified",
                {
                    "chore": self.name,
                    "status": self.verification_status,
                    "notes": self.verification_notes,
                    "rewards": self.get_rewards_summary()
                },
                user=member.user_account
            )

    def get_rewards_summary(self) -> dict:
        """Get summary of rewards earned."""
        return {
            "points": self.points_earned,
            "money": float(self.money_earned or 0),
            "screen_time": self.screen_time_earned,
            "bonuses": [b.as_dict() for b in self.bonuses]
        }
```

## 2.5 Field-Level Encryption

Sensitive fields are encrypted at the database level:

```python
# dartwing_family/encryption.py

from cryptography.fernet import Fernet
import frappe

ENCRYPTED_FIELDS = {
    "Family Medical Profile": [
        "medical_conditions",
        "current_medications",
        "insurance_policy_number"
    ],
    "Family Member": [
        "date_of_birth"  # PII
    ],
    "Allowance Payment": [
        "amount"  # Financial
    ]
}

class FieldEncryption:
    """Handles field-level encryption for sensitive data."""

    @staticmethod
    def get_encryption_key() -> bytes:
        """Get or generate encryption key from site config."""
        key = frappe.conf.get("family_encryption_key")
        if not key:
            key = Fernet.generate_key().decode()
            # Store in site_config.json
            frappe.throw("Encryption key not configured. Add 'family_encryption_key' to site_config.json")
        return key.encode()

    @staticmethod
    def encrypt_value(value: str) -> str:
        """Encrypt a string value."""
        if not value:
            return value
        f = Fernet(FieldEncryption.get_encryption_key())
        return f.encrypt(value.encode()).decode()

    @staticmethod
    def decrypt_value(encrypted: str) -> str:
        """Decrypt an encrypted value."""
        if not encrypted:
            return encrypted
        f = Fernet(FieldEncryption.get_encryption_key())
        return f.decrypt(encrypted.encode()).decode()


# Hook to encrypt before saving
def encrypt_sensitive_fields(doc, method):
    """Called before_save to encrypt sensitive fields."""
    if doc.doctype in ENCRYPTED_FIELDS:
        for field in ENCRYPTED_FIELDS[doc.doctype]:
            if doc.get(field):
                # Check if already encrypted
                if not doc.get(field).startswith("gAAAAA"):
                    doc.set(field, FieldEncryption.encrypt_value(doc.get(field)))


# Hook to decrypt after loading
def decrypt_sensitive_fields(doc, method):
    """Called after_load to decrypt sensitive fields."""
    if doc.doctype in ENCRYPTED_FIELDS:
        for field in ENCRYPTED_FIELDS[doc.doctype]:
            if doc.get(field) and doc.get(field).startswith("gAAAAA"):
                doc.set(field, FieldEncryption.decrypt_value(doc.get(field)))
```

---

_End of Section 2: Data Model Architecture_

**Next Section:** Section 3 - Permission & Access Control Architecture

# Section 3: Permission & Access Control Architecture

## 3.1 Permission Model Overview

The Dartwing Family module implements a multi-layered permission system:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PERMISSION HIERARCHY                                    │
│                                                                              │
│  Layer 1: Organization Isolation                                            │
│  └─ All data scoped to family organization                                  │
│                                                                              │
│  Layer 2: Role-Based Access (Frappe Roles)                                  │
│  ├─ Family Admin     → Full access to family data                           │
│  ├─ Family Parent    → Manage children, view all, modify most               │
│  ├─ Family Teen      → Self-management, limited family view                 │
│  ├─ Family Child     → Highly restricted, own data only                     │
│  └─ Family Extended  → View-only, emergency access                          │
│                                                                              │
│  Layer 3: Age-Based Permissions                                             │
│  ├─ Under 6          → No app access, parent-managed profile                │
│  ├─ 6-12 (COPPA)     → Kid mode, no external sharing, full parental view   │
│  ├─ 13-15            → More features, some privacy, parental oversight     │
│  ├─ 16-17            → Most features, limited location privacy             │
│  └─ 18+              → Full autonomy, optional family sharing              │
│                                                                              │
│  Layer 4: Relationship-Based Access                                         │
│  ├─ Guardian can see ward's data                                            │
│  ├─ Custody schedule affects visibility                                     │
│  └─ Extended family has emergency-only access                               │
│                                                                              │
│  Layer 5: Feature-Specific Rules                                            │
│  ├─ Screen time: Enforced by device agent                                   │
│  ├─ Location: Age-based sharing controls                                    │
│  ├─ Financial: Parent approval required for minors                          │
│  └─ Content: Age-appropriate filtering                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3.2 Frappe Role Definitions

### Role Configuration

```python
# dartwing_family/fixtures/roles.json
[
    {
        "doctype": "Role",
        "role_name": "Family Admin",
        "desk_access": 1,
        "is_custom": 1,
        "description": "Full administrative access to family organization"
    },
    {
        "doctype": "Role",
        "role_name": "Family Parent",
        "desk_access": 1,
        "is_custom": 1,
        "description": "Parent/Guardian with oversight of children"
    },
    {
        "doctype": "Role",
        "role_name": "Family Teen",
        "desk_access": 0,
        "is_custom": 1,
        "description": "Teenager (13-17) with limited self-management"
    },
    {
        "doctype": "Role",
        "role_name": "Family Child",
        "desk_access": 0,
        "is_custom": 1,
        "description": "Child (6-12) with highly restricted access"
    },
    {
        "doctype": "Role",
        "role_name": "Family Extended",
        "desk_access": 0,
        "is_custom": 1,
        "description": "Extended family with view-only access"
    }
]
```

### DocType Permission Matrix

```python
# dartwing_family/permissions/permission_matrix.py

DOCTYPE_PERMISSIONS = {
    "Family Member": {
        "Family Admin":   {"read": 1, "write": 1, "create": 1, "delete": 1},
        "Family Parent":  {"read": 1, "write": 1, "create": 1, "delete": 0},
        "Family Teen":    {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Extended": {"read": 1, "write": 0, "create": 0, "delete": 0}
    },
    "Chore Assignment": {
        "Family Admin":   {"read": 1, "write": 1, "create": 1, "delete": 1},
        "Family Parent":  {"read": 1, "write": 1, "create": 1, "delete": 1},
        "Family Teen":    {"read": 1, "write": 1, "create": 0, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 1, "write": 1, "create": 0, "delete": 0, "if_owner": 1},
        "Family Extended": {"read": 1, "write": 0, "create": 0, "delete": 0}
    },
    "Allowance Payment": {
        "Family Admin":   {"read": 1, "write": 1, "create": 1, "delete": 1},
        "Family Parent":  {"read": 1, "write": 1, "create": 1, "delete": 0},
        "Family Teen":    {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Extended": {"read": 0, "write": 0, "create": 0, "delete": 0}
    },
    "Family Medical Profile": {
        "Family Admin":   {"read": 1, "write": 1, "create": 1, "delete": 0},
        "Family Parent":  {"read": 1, "write": 1, "create": 1, "delete": 0},
        "Family Teen":    {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 0, "write": 0, "create": 0, "delete": 0},
        "Family Extended": {"read": 1, "write": 0, "create": 0, "delete": 0}  # Emergency access
    },
    "Location History": {
        "Family Admin":   {"read": 1, "write": 0, "create": 1, "delete": 1},
        "Family Parent":  {"read": 1, "write": 0, "create": 1, "delete": 0},
        "Family Teen":    {"read": 1, "write": 0, "create": 1, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 0, "write": 0, "create": 1, "delete": 0},
        "Family Extended": {"read": 0, "write": 0, "create": 0, "delete": 0}
    },
    "Screen Time Profile": {
        "Family Admin":   {"read": 1, "write": 1, "create": 1, "delete": 1},
        "Family Parent":  {"read": 1, "write": 1, "create": 1, "delete": 0},
        "Family Teen":    {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Child":   {"read": 1, "write": 0, "create": 0, "delete": 0, "if_owner": 1},
        "Family Extended": {"read": 0, "write": 0, "create": 0, "delete": 0}
    }
}
```

## 3.3 Age-Based Permission Profiles

### Permission Profile DocType

```python
# dartwing_family/doctype/family_permission_profile/family_permission_profile.json
{
    "doctype": "DocType",
    "name": "Family Permission Profile",
    "module": "Dartwing Family",

    "fields": [
        {
            "fieldname": "profile_name",
            "fieldtype": "Data",
            "label": "Profile Name",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "age_range_start",
            "fieldtype": "Int",
            "label": "Age Range Start"
        },
        {
            "fieldname": "age_range_end",
            "fieldtype": "Int",
            "label": "Age Range End"
        },
        {
            "fieldname": "section_features",
            "fieldtype": "Section Break",
            "label": "Feature Access"
        },
        {
            "fieldname": "can_access_app",
            "fieldtype": "Check",
            "label": "Can Access App"
        },
        {
            "fieldname": "can_view_calendar",
            "fieldtype": "Check",
            "label": "Can View Family Calendar"
        },
        {
            "fieldname": "can_create_events",
            "fieldtype": "Check",
            "label": "Can Create Events"
        },
        {
            "fieldname": "can_view_location_others",
            "fieldtype": "Check",
            "label": "Can View Others' Location"
        },
        {
            "fieldname": "can_control_own_location",
            "fieldtype": "Check",
            "label": "Can Control Own Location Sharing"
        },
        {
            "fieldname": "can_spend_allowance",
            "fieldtype": "Check",
            "label": "Can Spend Allowance"
        },
        {
            "fieldname": "spending_limit",
            "fieldtype": "Currency",
            "label": "Spending Limit per Transaction"
        },
        {
            "fieldname": "can_request_contact",
            "fieldtype": "Check",
            "label": "Can Request New Contacts"
        },
        {
            "fieldname": "can_approve_contact",
            "fieldtype": "Check",
            "label": "Can Approve Contacts"
        },
        {
            "fieldname": "section_screen_time",
            "fieldtype": "Section Break",
            "label": "Screen Time"
        },
        {
            "fieldname": "screen_time_enforced",
            "fieldtype": "Check",
            "label": "Screen Time Limits Enforced"
        },
        {
            "fieldname": "default_weekday_minutes",
            "fieldtype": "Int",
            "label": "Default Weekday Limit (minutes)"
        },
        {
            "fieldname": "default_weekend_minutes",
            "fieldtype": "Int",
            "label": "Default Weekend Limit (minutes)"
        },
        {
            "fieldname": "section_location",
            "fieldtype": "Section Break",
            "label": "Location Sharing"
        },
        {
            "fieldname": "location_always_shared",
            "fieldtype": "Check",
            "label": "Location Always Shared with Guardians"
        },
        {
            "fieldname": "can_use_ghost_mode",
            "fieldtype": "Check",
            "label": "Can Use Ghost Mode"
        },
        {
            "fieldname": "ghost_mode_max_hours",
            "fieldtype": "Int",
            "label": "Ghost Mode Maximum Hours"
        },
        {
            "fieldname": "location_history_days",
            "fieldtype": "Int",
            "label": "Location History Retention (days)"
        },
        {
            "fieldname": "section_privacy",
            "fieldtype": "Section Break",
            "label": "Privacy & Safety"
        },
        {
            "fieldname": "coppa_protected",
            "fieldtype": "Check",
            "label": "COPPA Protected",
            "description": "No external data sharing allowed"
        },
        {
            "fieldname": "content_filter_level",
            "fieldtype": "Select",
            "label": "Content Filter Level",
            "options": "Strict\nModerate\nLight\nNone"
        },
        {
            "fieldname": "requires_parent_approval_apps",
            "fieldtype": "Check",
            "label": "Requires Parent Approval for Apps"
        }
    ]
}
```

### Default Permission Profiles

```python
# dartwing_family/fixtures/permission_profiles.py

DEFAULT_PROFILES = [
    {
        "profile_name": "Child Under 6",
        "age_range_start": 0,
        "age_range_end": 5,
        "can_access_app": 0,
        "can_view_calendar": 0,
        "can_create_events": 0,
        "can_view_location_others": 0,
        "can_control_own_location": 0,
        "can_spend_allowance": 0,
        "spending_limit": 0,
        "can_request_contact": 0,
        "can_approve_contact": 0,
        "screen_time_enforced": 0,  # N/A - no app access
        "location_always_shared": 1,
        "can_use_ghost_mode": 0,
        "ghost_mode_max_hours": 0,
        "location_history_days": 365,
        "coppa_protected": 1,
        "content_filter_level": "Strict",
        "requires_parent_approval_apps": 1
    },
    {
        "profile_name": "Child 6-12",
        "age_range_start": 6,
        "age_range_end": 12,
        "can_access_app": 1,
        "can_view_calendar": 1,
        "can_create_events": 0,
        "can_view_location_others": 0,
        "can_control_own_location": 0,
        "can_spend_allowance": 0,
        "spending_limit": 0,
        "can_request_contact": 1,
        "can_approve_contact": 0,
        "screen_time_enforced": 1,
        "default_weekday_minutes": 120,
        "default_weekend_minutes": 240,
        "location_always_shared": 1,
        "can_use_ghost_mode": 0,
        "ghost_mode_max_hours": 0,
        "location_history_days": 365,
        "coppa_protected": 1,
        "content_filter_level": "Strict",
        "requires_parent_approval_apps": 1
    },
    {
        "profile_name": "Tween 13-15",
        "age_range_start": 13,
        "age_range_end": 15,
        "can_access_app": 1,
        "can_view_calendar": 1,
        "can_create_events": 1,
        "can_view_location_others": 1,
        "can_control_own_location": 0,
        "can_spend_allowance": 1,
        "spending_limit": 25.00,
        "can_request_contact": 1,
        "can_approve_contact": 0,
        "screen_time_enforced": 1,
        "default_weekday_minutes": 180,
        "default_weekend_minutes": 300,
        "location_always_shared": 1,
        "can_use_ghost_mode": 0,
        "ghost_mode_max_hours": 0,
        "location_history_days": 30,
        "coppa_protected": 0,
        "content_filter_level": "Moderate",
        "requires_parent_approval_apps": 1
    },
    {
        "profile_name": "Teen 16-17",
        "age_range_start": 16,
        "age_range_end": 17,
        "can_access_app": 1,
        "can_view_calendar": 1,
        "can_create_events": 1,
        "can_view_location_others": 1,
        "can_control_own_location": 1,
        "can_spend_allowance": 1,
        "spending_limit": 100.00,
        "can_request_contact": 1,
        "can_approve_contact": 0,
        "screen_time_enforced": 0,  # Advisory only
        "default_weekday_minutes": 0,  # Unlimited
        "default_weekend_minutes": 0,
        "location_always_shared": 0,
        "can_use_ghost_mode": 1,
        "ghost_mode_max_hours": 2,
        "location_history_days": 7,
        "coppa_protected": 0,
        "content_filter_level": "Light",
        "requires_parent_approval_apps": 0
    },
    {
        "profile_name": "Adult",
        "age_range_start": 18,
        "age_range_end": 999,
        "can_access_app": 1,
        "can_view_calendar": 1,
        "can_create_events": 1,
        "can_view_location_others": 1,
        "can_control_own_location": 1,
        "can_spend_allowance": 1,
        "spending_limit": 0,  # No limit
        "can_request_contact": 1,
        "can_approve_contact": 1,
        "screen_time_enforced": 0,
        "location_always_shared": 0,
        "can_use_ghost_mode": 1,
        "ghost_mode_max_hours": 0,  # Unlimited
        "location_history_days": 0,  # No auto-retention
        "coppa_protected": 0,
        "content_filter_level": "None",
        "requires_parent_approval_apps": 0
    }
]
```

## 3.4 Permission Enforcement Engine

### Core Permission Checker

```python
# dartwing_family/permissions/permission_engine.py

import frappe
from functools import wraps
from typing import Optional, List
from dartwing_family.utils.family import get_family_member_for_user

class FamilyPermissionEngine:
    """Central permission enforcement for all family operations."""

    def __init__(self, user: str = None):
        self.user = user or frappe.session.user
        self.member = get_family_member_for_user(self.user)
        self.profile = self._load_permission_profile()
        self.relationships = self._load_relationships()

    def _load_permission_profile(self) -> dict:
        """Load the member's permission profile."""
        if not self.member:
            return {}

        profile_name = frappe.get_value(
            "Family Member", self.member, "permission_profile"
        )
        if profile_name:
            return frappe.get_doc("Family Permission Profile", profile_name).as_dict()
        return {}

    def _load_relationships(self) -> List[dict]:
        """Load all relationships for this member."""
        if not self.member:
            return []

        return frappe.get_all(
            "Family Relationship",
            filters={"person_a": self.member, "status": "Active"},
            fields=["person_b", "relationship_type", "is_legal_guardian"]
        )

    # ─── FEATURE ACCESS CHECKS ──────────────────────────────────────────

    def can_access_app(self) -> bool:
        """Check if user can access the family app."""
        return self.profile.get("can_access_app", True)

    def can_view_member_location(self, target_member: str) -> bool:
        """Check if user can view another member's location."""
        # Adults can always opt-out of sharing
        target_doc = frappe.get_doc("Family Member", target_member)
        if not target_doc.is_minor:
            # Check if target has enabled sharing with this user
            return self._check_location_sharing_consent(target_member)

        # For minors, check if user is guardian
        if self._is_guardian_of(target_member):
            # Check custody schedule
            if self._is_custody_restricted(target_member):
                return False
            return True

        # Check permission profile for viewing others
        return self.profile.get("can_view_location_others", False)

    def can_control_own_location(self) -> bool:
        """Check if user can control their own location sharing."""
        return self.profile.get("can_control_own_location", False)

    def can_use_ghost_mode(self) -> tuple:
        """Check if user can use ghost mode, return (allowed, max_hours)."""
        allowed = self.profile.get("can_use_ghost_mode", False)
        max_hours = self.profile.get("ghost_mode_max_hours", 0)
        return (allowed, max_hours)

    def can_spend_allowance(self, amount: float) -> tuple:
        """Check if user can spend given amount, return (allowed, reason)."""
        if not self.profile.get("can_spend_allowance", False):
            return (False, "Spending not allowed for your age group")

        limit = self.profile.get("spending_limit", 0)
        if limit > 0 and amount > limit:
            return (False, f"Amount exceeds your spending limit of ${limit}")

        return (True, None)

    def can_approve_for_minor(self, minor_member: str) -> bool:
        """Check if user can approve actions for a minor."""
        if not self._is_guardian_of(minor_member):
            return False

        # Check custody schedule
        if self._is_custody_restricted(minor_member):
            return False

        return True

    def can_view_medical_info(self, target_member: str) -> bool:
        """Check if user can view medical information."""
        # Own medical info
        if target_member == self.member:
            member_age = frappe.get_value("Family Member", self.member, "age")
            return member_age >= 13  # Kids can't see own detailed medical

        # Guardian can see ward's medical
        if self._is_guardian_of(target_member):
            return True

        # Extended family has emergency access only
        role = frappe.get_roles(self.user)
        if "Family Extended" in role:
            return frappe.flags.emergency_access  # Set during emergency

        return False

    def can_modify_parental_controls(self, target_member: str) -> bool:
        """Check if user can modify parental controls for target."""
        if not self._is_guardian_of(target_member):
            return False

        # Must be admin or parent role
        roles = frappe.get_roles(self.user)
        return "Family Admin" in roles or "Family Parent" in roles

    # ─── RELATIONSHIP CHECKS ────────────────────────────────────────────

    def _is_guardian_of(self, member: str) -> bool:
        """Check if current user is legal guardian of member."""
        for rel in self.relationships:
            if rel.person_b == member and rel.is_legal_guardian:
                return True
        return False

    def _is_custody_restricted(self, child_member: str) -> bool:
        """Check if custody schedule restricts access right now."""
        custody_schedule = frappe.get_value(
            "Custody Schedule",
            {"child": child_member},
            "name"
        )

        if not custody_schedule:
            return False  # No custody schedule = no restrictions

        schedule = frappe.get_doc("Custody Schedule", custody_schedule)
        current_parent = schedule.get_current_parent()

        # If this user is not the current parent, check visibility rules
        if current_parent != self.member:
            # Check if non-current parent can see location
            if self.member == schedule.parent_a:
                return not schedule.parent_a_sees_location_during_b
            elif self.member == schedule.parent_b:
                return not schedule.parent_b_sees_location_during_a

        return False

    def _check_location_sharing_consent(self, target_member: str) -> bool:
        """Check if target has consented to share location with user."""
        # Implementation for adult location sharing consent
        consent = frappe.get_value(
            "Location Sharing Consent",
            {"from_member": target_member, "to_member": self.member},
            "enabled"
        )
        return consent == 1

    # ─── DATA FILTERING ─────────────────────────────────────────────────

    def get_viewable_members(self) -> List[str]:
        """Get list of family members this user can view."""
        org = frappe.get_value("Family Member", self.member, "organization")

        all_members = frappe.get_all(
            "Family Member",
            filters={"organization": org, "status": "Active"},
            fields=["name"]
        )

        viewable = []
        for m in all_members:
            if self._can_view_member(m.name):
                viewable.append(m.name)

        return viewable

    def _can_view_member(self, member: str) -> bool:
        """Check if user can view this member's basic info."""
        # Can always view self
        if member == self.member:
            return True

        # Check if in same organization
        user_org = frappe.get_value("Family Member", self.member, "organization")
        member_org = frappe.get_value("Family Member", member, "organization")

        return user_org == member_org

    def filter_response_by_age(self, doctype: str, data: dict) -> dict:
        """Filter response data based on requester's age."""
        member_age = frappe.get_value("Family Member", self.member, "age") or 18

        from dartwing_family.security.age_filter import AgeBasedDataFilter
        return AgeBasedDataFilter.filter_response(doctype, data, member_age)


# Decorator for permission-protected endpoints
def requires_permission(permission_check: str):
    """Decorator to enforce permission checks on API methods."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            engine = FamilyPermissionEngine()
            check_method = getattr(engine, permission_check, None)

            if not check_method:
                frappe.throw(f"Unknown permission check: {permission_check}")

            # For checks that need a target member
            target = kwargs.get("target_member") or kwargs.get("member")
            if target:
                allowed = check_method(target)
            else:
                allowed = check_method()

            if not allowed:
                frappe.throw(
                    "Permission Denied",
                    frappe.PermissionError
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 3.5 API-Level Permission Enforcement

### Whitelisted API Methods

```python
# dartwing_family/api/family_api.py

import frappe
from frappe import _
from dartwing_family.permissions.permission_engine import (
    FamilyPermissionEngine,
    requires_permission
)

@frappe.whitelist()
def get_family_dashboard():
    """Get dashboard data for current user's family."""
    engine = FamilyPermissionEngine()

    if not engine.can_access_app():
        frappe.throw(_("App access not available for your account"))

    member = engine.member
    org = frappe.get_value("Family Member", member, "organization")

    # Get viewable members
    viewable = engine.get_viewable_members()

    # Build dashboard
    dashboard = {
        "member": member,
        "organization": org,
        "family_members": get_members_summary(viewable, engine),
        "today_chores": get_today_chores(member),
        "upcoming_events": get_upcoming_events(org, viewable),
        "notifications": get_notifications(member)
    }

    return dashboard


@frappe.whitelist()
@requires_permission("can_view_member_location")
def get_member_location(target_member: str):
    """Get real-time location of a family member."""
    location = frappe.get_last_doc(
        "Location History",
        filters={"family_member": target_member}
    )

    if location:
        return {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": location.timestamp,
            "accuracy": location.accuracy
        }

    return None


@frappe.whitelist()
def request_ghost_mode(duration_hours: int):
    """Request ghost mode for current user."""
    engine = FamilyPermissionEngine()

    allowed, max_hours = engine.can_use_ghost_mode()

    if not allowed:
        frappe.throw(_("Ghost mode is not available for your account"))

    if max_hours > 0 and duration_hours > max_hours:
        frappe.throw(_(f"Maximum ghost mode duration is {max_hours} hours"))

    # Activate ghost mode
    member = engine.member
    frappe.db.set_value(
        "Family Member",
        member,
        {
            "ghost_mode_active": 1,
            "ghost_mode_expires": frappe.utils.add_to_date(
                frappe.utils.now_datetime(),
                hours=duration_hours
            )
        }
    )

    # Notify guardians
    notify_guardians_ghost_mode(member, duration_hours)

    return {"status": "success", "expires_in_hours": duration_hours}


@frappe.whitelist()
def approve_child_action(
    action_type: str,
    action_id: str,
    child_member: str,
    approved: bool,
    notes: str = None
):
    """Parent approval for child's action."""
    engine = FamilyPermissionEngine()

    if not engine.can_approve_for_minor(child_member):
        frappe.throw(_("You cannot approve actions for this family member"))

    # Route to appropriate handler
    if action_type == "app_install":
        return handle_app_approval(action_id, approved, notes)
    elif action_type == "contact_request":
        return handle_contact_approval(action_id, approved, notes)
    elif action_type == "spending_request":
        return handle_spending_approval(action_id, approved, notes)
    else:
        frappe.throw(_("Unknown action type"))


@frappe.whitelist()
def get_parental_controls(target_member: str):
    """Get parental control settings for a minor."""
    engine = FamilyPermissionEngine()

    if not engine.can_modify_parental_controls(target_member):
        frappe.throw(_("Access denied"))

    # Get screen time profile
    screen_time = frappe.get_doc(
        "Screen Time Profile",
        {"family_member": target_member}
    )

    # Get content filter
    content_filter = frappe.get_value(
        "Content Filter Profile",
        {"family_member": target_member}
    )

    # Get approved contacts
    contacts = frappe.get_all(
        "Approved Contact",
        filters={"child": target_member},
        fields=["contact_name", "relationship", "can_call", "can_text"]
    )

    return {
        "screen_time": screen_time.as_dict() if screen_time else None,
        "content_filter": content_filter,
        "approved_contacts": contacts
    }


@frappe.whitelist()
def update_screen_time_profile(target_member: str, settings: dict):
    """Update screen time settings for a minor."""
    engine = FamilyPermissionEngine()

    if not engine.can_modify_parental_controls(target_member):
        frappe.throw(_("Access denied"))

    profile = frappe.get_doc(
        "Screen Time Profile",
        {"family_member": target_member}
    )

    # Update allowed fields
    allowed_fields = [
        "weekday_limit_minutes",
        "weekend_limit_minutes",
        "allowed_start_time",
        "allowed_end_time"
    ]

    for field in allowed_fields:
        if field in settings:
            profile.set(field, settings[field])

    profile.save()

    # Broadcast update to child's devices
    broadcast_screen_time_update(target_member, profile)

    return {"status": "success"}
```

## 3.6 COPPA Compliance Implementation

### COPPA Enforcement

```python
# dartwing_family/compliance/coppa.py

import frappe
from frappe import _

class COPPACompliance:
    """Enforces COPPA requirements for users under 13."""

    COPPA_AGE_LIMIT = 13

    # Data that cannot be collected from COPPA-protected users
    RESTRICTED_DATA = [
        "precise_location",  # Can only be shared with guardians
        "behavioral_data",   # No tracking for ads
        "external_sharing",  # No third-party data sharing
        "public_profiles",   # No public-facing profiles
        "social_features"    # No contact with non-approved users
    ]

    @staticmethod
    def is_coppa_protected(member: str) -> bool:
        """Check if member is COPPA-protected."""
        age = frappe.get_value("Family Member", member, "age")
        return age < COPPACompliance.COPPA_AGE_LIMIT

    @staticmethod
    def validate_action(member: str, action: str, data: dict = None):
        """Validate that action is COPPA-compliant."""
        if not COPPACompliance.is_coppa_protected(member):
            return True

        if action in COPPACompliance.RESTRICTED_DATA:
            frappe.throw(_(
                "This action is not available for users under 13 "
                "in compliance with COPPA regulations."
            ))

        return True

    @staticmethod
    def filter_response_for_coppa(member: str, data: dict) -> dict:
        """Remove COPPA-restricted data from responses."""
        if not COPPACompliance.is_coppa_protected(member):
            return data

        # Remove restricted fields
        restricted_fields = [
            "behavioral_analytics",
            "advertising_id",
            "third_party_sync"
        ]

        filtered = data.copy()
        for field in restricted_fields:
            filtered.pop(field, None)

        return filtered

    @staticmethod
    def verify_parental_consent(parent_member: str, child_member: str) -> bool:
        """Verify parental consent for COPPA-protected child."""
        # Check for verified consent record
        consent = frappe.db.exists(
            "Parental Consent",
            {
                "parent": parent_member,
                "child": child_member,
                "verified": 1,
                "consent_type": "COPPA"
            }
        )
        return bool(consent)

    @staticmethod
    def request_parental_consent(parent_member: str, child_member: str):
        """Create parental consent request."""
        parent = frappe.get_doc("Family Member", parent_member)
        child = frappe.get_doc("Family Member", child_member)

        # Create consent request
        consent = frappe.get_doc({
            "doctype": "Parental Consent",
            "parent": parent_member,
            "child": child_member,
            "consent_type": "COPPA",
            "requested_at": frappe.utils.now_datetime(),
            "verification_method": "email_and_payment",
            "organization": parent.organization
        })
        consent.insert(ignore_permissions=True)

        # Send verification email with micro-payment option
        send_coppa_verification_email(parent, child, consent)

        return consent.name


# Hook to enforce COPPA on API calls
def coppa_api_guard(doc, method):
    """API hook to enforce COPPA compliance."""
    if frappe.session.user == "Guest":
        return

    member = get_family_member_for_user(frappe.session.user)
    if member and COPPACompliance.is_coppa_protected(member):
        # Check if action requires verification
        if doc.doctype in COPPA_REQUIRES_CONSENT:
            if not COPPACompliance.verify_parental_consent_for_action(member, doc.doctype):
                frappe.throw(_(
                    "Parental consent required for this action. "
                    "Please ask a parent to approve."
                ))


COPPA_REQUIRES_CONSENT = [
    "Approved Contact",
    "External Account Integration",
    "Location Sharing Consent"
]
```

## 3.7 Audit Logging

### Audit Log Implementation

```python
# dartwing_family/audit/audit_log.py

import frappe
from frappe.utils import now_datetime

class FamilyAuditLog:
    """Comprehensive audit logging for family actions."""

    SENSITIVE_ACTIONS = [
        "view_location",
        "view_medical",
        "modify_parental_controls",
        "approve_spending",
        "access_financial",
        "emergency_override"
    ]

    @staticmethod
    def log(
        action: str,
        actor_member: str,
        target_member: str = None,
        details: dict = None,
        outcome: str = "success"
    ):
        """Create audit log entry."""
        frappe.get_doc({
            "doctype": "Family Audit Log",
            "action": action,
            "actor_member": actor_member,
            "actor_user": frappe.session.user,
            "target_member": target_member,
            "details": frappe.as_json(details or {}),
            "outcome": outcome,
            "timestamp": now_datetime(),
            "ip_address": frappe.local.request_ip,
            "user_agent": frappe.request.headers.get("User-Agent"),
            "organization": frappe.get_value(
                "Family Member", actor_member, "organization"
            )
        }).insert(ignore_permissions=True)

    @staticmethod
    def log_sensitive_access(
        action: str,
        actor_member: str,
        target_member: str,
        reason: str = None
    ):
        """Log access to sensitive data with additional scrutiny."""
        if action not in FamilyAuditLog.SENSITIVE_ACTIONS:
            return FamilyAuditLog.log(action, actor_member, target_member)

        # Enhanced logging for sensitive access
        entry = frappe.get_doc({
            "doctype": "Family Audit Log",
            "action": action,
            "actor_member": actor_member,
            "actor_user": frappe.session.user,
            "target_member": target_member,
            "details": frappe.as_json({
                "reason": reason,
                "sensitive": True,
                "session_id": frappe.session.sid
            }),
            "outcome": "success",
            "timestamp": now_datetime(),
            "ip_address": frappe.local.request_ip,
            "user_agent": frappe.request.headers.get("User-Agent"),
            "is_sensitive": 1,
            "organization": frappe.get_value(
                "Family Member", actor_member, "organization"
            )
        })
        entry.insert(ignore_permissions=True)

        # Alert for certain sensitive actions
        if action in ["emergency_override", "modify_parental_controls"]:
            notify_family_admins(entry)

    @staticmethod
    def get_member_access_log(
        member: str,
        days: int = 30,
        action_filter: str = None
    ) -> list:
        """Get audit log of who accessed this member's data."""
        filters = {
            "target_member": member,
            "timestamp": [">=", frappe.utils.add_days(now_datetime(), -days)]
        }

        if action_filter:
            filters["action"] = action_filter

        return frappe.get_all(
            "Family Audit Log",
            filters=filters,
            fields=["action", "actor_member", "timestamp", "outcome", "is_sensitive"],
            order_by="timestamp desc"
        )


# Family Audit Log DocType
"""
{
    "doctype": "DocType",
    "name": "Family Audit Log",
    "module": "Dartwing Family",
    "fields": [
        {"fieldname": "action", "fieldtype": "Data", "label": "Action"},
        {"fieldname": "actor_member", "fieldtype": "Link", "options": "Family Member"},
        {"fieldname": "actor_user", "fieldtype": "Link", "options": "User"},
        {"fieldname": "target_member", "fieldtype": "Link", "options": "Family Member"},
        {"fieldname": "details", "fieldtype": "JSON", "label": "Details"},
        {"fieldname": "outcome", "fieldtype": "Select", "options": "success\nfailed\ndenied"},
        {"fieldname": "timestamp", "fieldtype": "Datetime"},
        {"fieldname": "ip_address", "fieldtype": "Data"},
        {"fieldname": "user_agent", "fieldtype": "Small Text"},
        {"fieldname": "is_sensitive", "fieldtype": "Check"},
        {"fieldname": "organization", "fieldtype": "Link", "options": "Organization"}
    ]
}
"""
```

---

_End of Section 3: Permission & Access Control Architecture_

**Next Section:** Section 4 - Integration Architecture (Third-party services, APIs, adapters)

# Section 4: Integration Architecture

## 4.1 Integration Framework Overview

Dartwing Family integrates with 20+ external services through a standardized adapter pattern:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       INTEGRATION ARCHITECTURE                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    DARTWING INTEGRATION HUB                          │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │   Adapter    │  │   Adapter    │  │   Adapter    │               │    │
│  │  │   Registry   │  │   Factory    │  │   Manager    │               │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                    ADAPTER BASE CLASS                         │   │    │
│  │  │  • OAuth2 Flow      • Rate Limiting     • Error Handling     │   │    │
│  │  │  • Token Refresh    • Retry Logic       • Audit Logging      │   │    │
│  │  │  • Webhook Handler  • Data Transform    • Health Check       │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │ HOME AUTOMATION │    │     RETAIL      │    │   EDUCATION     │         │
│  │                 │    │                 │    │                 │         │
│  │ • Home Assist.  │    │ • Amazon        │    │ • Google Class. │         │
│  │ • Apple HomeKit │    │ • Walmart       │    │ • Canvas        │         │
│  │ • Google Home   │    │ • Instacart     │    │ • PowerSchool   │         │
│  │ • Amazon Alexa  │    │ • Costco        │    │ • Khan Academy  │         │
│  │ • SmartThings   │    │ • Target        │    │ • Seesaw        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │    LOCATION     │    │    VEHICLES     │    │     HEALTH      │         │
│  │                 │    │                 │    │                 │         │
│  │ • Apple FindMy  │    │ • OBD-II        │    │ • MedxHealthL.  │         │
│  │ • Tile          │    │ • Tesla API     │    │ • Apple Health  │         │
│  │ • SmartTag      │    │ • Ford Pass     │    │ • Google Fit    │         │
│  │ • Phone GPS     │    │ • GM OnStar     │    │                 │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Base Adapter Architecture

### Abstract Base Adapter

```python
# dartwing_family/integrations/base_adapter.py

import frappe
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class BaseIntegrationAdapter(ABC):
    """Abstract base class for all third-party integrations."""

    # Override in subclasses
    ADAPTER_NAME: str = "base"
    ADAPTER_TYPE: str = "generic"  # home, retail, education, location, vehicle, health
    REQUIRES_OAUTH: bool = True
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds

    def __init__(self, organization: str, config: dict = None):
        self.organization = organization
        self.config = config or self._load_config()
        self.session = self._create_session()
        self._access_token = None
        self._token_expires = None

    def _load_config(self) -> dict:
        """Load adapter configuration from database."""
        config = frappe.get_doc(
            "Integration Configuration",
            {"organization": self.organization, "adapter": self.ADAPTER_NAME}
        )
        return config.as_dict() if config else {}

    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    # ─── OAUTH FLOW ─────────────────────────────────────────────────────

    @abstractmethod
    def get_oauth_url(self, redirect_uri: str) -> str:
        """Generate OAuth authorization URL."""
        pass

    @abstractmethod
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for access token."""
        pass

    def get_access_token(self) -> str:
        """Get valid access token, refreshing if needed."""
        if self._access_token and self._token_expires:
            if datetime.now() < self._token_expires - timedelta(minutes=5):
                return self._access_token

        # Try refresh
        if self.config.get("refresh_token"):
            self._refresh_token()
        else:
            frappe.throw(f"No valid authentication for {self.ADAPTER_NAME}")

        return self._access_token

    def _refresh_token(self):
        """Refresh the access token using refresh token."""
        # Override in subclasses with specific OAuth implementation
        pass

    def _save_tokens(self, access_token: str, refresh_token: str, expires_in: int):
        """Save tokens to database."""
        frappe.db.set_value(
            "Integration Configuration",
            {"organization": self.organization, "adapter": self.ADAPTER_NAME},
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expires": datetime.now() + timedelta(seconds=expires_in)
            }
        )

        self._access_token = access_token
        self._token_expires = datetime.now() + timedelta(seconds=expires_in)

    # ─── API REQUEST HANDLING ───────────────────────────────────────────

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None
    ) -> dict:
        """Make authenticated API request with rate limiting."""
        # Check rate limit
        self._check_rate_limit()

        # Build headers
        request_headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }
        if headers:
            request_headers.update(headers)

        # Make request
        url = self._build_url(endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=30
            )

            # Log request
            self._log_request(method, endpoint, response.status_code)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e, endpoint)
        except requests.exceptions.RequestException as e:
            self._handle_request_error(e, endpoint)

    @abstractmethod
    def _build_url(self, endpoint: str) -> str:
        """Build full URL for API endpoint."""
        pass

    def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        cache_key = f"rate_limit:{self.ADAPTER_NAME}:{self.organization}"

        current = frappe.cache().get(cache_key) or 0

        if current >= self.RATE_LIMIT_CALLS:
            frappe.throw(
                f"Rate limit exceeded for {self.ADAPTER_NAME}. "
                f"Please wait before making more requests."
            )

        frappe.cache().set(cache_key, current + 1, expires_in_sec=self.RATE_LIMIT_PERIOD)

    def _log_request(self, method: str, endpoint: str, status: int):
        """Log API request for debugging and auditing."""
        frappe.get_doc({
            "doctype": "Integration Request Log",
            "adapter": self.ADAPTER_NAME,
            "organization": self.organization,
            "method": method,
            "endpoint": endpoint,
            "status_code": status,
            "timestamp": datetime.now()
        }).insert(ignore_permissions=True)

    def _handle_http_error(self, error, endpoint: str):
        """Handle HTTP errors with appropriate logging."""
        status_code = error.response.status_code

        if status_code == 401:
            # Try to refresh token
            self._refresh_token()
            # Caller should retry
            frappe.throw("Authentication refreshed, please retry")
        elif status_code == 403:
            frappe.throw(f"Access denied to {endpoint}")
        elif status_code == 404:
            frappe.throw(f"Resource not found: {endpoint}")
        elif status_code == 429:
            frappe.throw("Rate limited by external service")
        else:
            frappe.throw(f"API error ({status_code}): {error}")

    def _handle_request_error(self, error, endpoint: str):
        """Handle request errors (network, timeout, etc.)."""
        frappe.log_error(
            title=f"{self.ADAPTER_NAME} Request Error",
            message=f"Endpoint: {endpoint}\nError: {str(error)}"
        )
        frappe.throw(f"Connection error with {self.ADAPTER_NAME}")

    # ─── WEBHOOK HANDLING ───────────────────────────────────────────────

    def handle_webhook(self, payload: dict, headers: dict) -> dict:
        """Process incoming webhook from external service."""
        # Verify webhook signature
        if not self._verify_webhook(payload, headers):
            frappe.throw("Invalid webhook signature")

        # Route to appropriate handler
        event_type = self._extract_event_type(payload)
        handler = getattr(self, f"_handle_{event_type}", None)

        if handler:
            return handler(payload)
        else:
            frappe.log_error(
                title=f"Unhandled webhook: {event_type}",
                message=str(payload)
            )
            return {"status": "unhandled"}

    @abstractmethod
    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        """Verify webhook signature."""
        pass

    @abstractmethod
    def _extract_event_type(self, payload: dict) -> str:
        """Extract event type from webhook payload."""
        pass

    # ─── DATA TRANSFORMATION ────────────────────────────────────────────

    @abstractmethod
    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        """Transform external data to internal Dartwing format."""
        pass

    @abstractmethod
    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        """Transform internal Dartwing data to external format."""
        pass

    # ─── HEALTH CHECK ───────────────────────────────────────────────────

    @abstractmethod
    def health_check(self) -> dict:
        """Check if integration is healthy and connected."""
        pass

    def is_connected(self) -> bool:
        """Quick check if integration is connected."""
        return bool(self.config.get("access_token"))
```

### Adapter Registry

```python
# dartwing_family/integrations/registry.py

import frappe
from typing import Dict, Type
from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter

class AdapterRegistry:
    """Registry for all available integration adapters."""

    _adapters: Dict[str, Type[BaseIntegrationAdapter]] = {}

    @classmethod
    def register(cls, adapter_class: Type[BaseIntegrationAdapter]):
        """Register an adapter class."""
        cls._adapters[adapter_class.ADAPTER_NAME] = adapter_class

    @classmethod
    def get_adapter(cls, adapter_name: str, organization: str) -> BaseIntegrationAdapter:
        """Get an instance of the specified adapter."""
        if adapter_name not in cls._adapters:
            frappe.throw(f"Unknown adapter: {adapter_name}")

        adapter_class = cls._adapters[adapter_name]
        return adapter_class(organization)

    @classmethod
    def get_available_adapters(cls) -> list:
        """Get list of all available adapters."""
        return [
            {
                "name": name,
                "type": adapter.ADAPTER_TYPE,
                "requires_oauth": adapter.REQUIRES_OAUTH
            }
            for name, adapter in cls._adapters.items()
        ]

    @classmethod
    def get_adapters_by_type(cls, adapter_type: str) -> list:
        """Get adapters of a specific type."""
        return [
            name for name, adapter in cls._adapters.items()
            if adapter.ADAPTER_TYPE == adapter_type
        ]


# Decorator to auto-register adapters
def register_adapter(cls):
    """Decorator to register an adapter class."""
    AdapterRegistry.register(cls)
    return cls
```

## 4.3 Home Automation Adapters

### Home Assistant Adapter

```python
# dartwing_family/integrations/home/home_assistant.py

import frappe
import hashlib
import hmac
from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class HomeAssistantAdapter(BaseIntegrationAdapter):
    """Integration with Home Assistant for smart home control."""

    ADAPTER_NAME = "home_assistant"
    ADAPTER_TYPE = "home"
    REQUIRES_OAUTH = False  # Uses long-lived access token
    RATE_LIMIT_CALLS = 1000
    RATE_LIMIT_PERIOD = 60

    def __init__(self, organization: str, config: dict = None):
        super().__init__(organization, config)
        self.base_url = self.config.get("home_assistant_url")
        self.access_token = self.config.get("access_token")

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/api/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        # Home Assistant uses long-lived tokens, not OAuth
        return None

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        # Not applicable for Home Assistant
        return {}

    def get_access_token(self) -> str:
        return self.access_token

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        # Verify using webhook secret
        webhook_secret = self.config.get("webhook_secret")
        if not webhook_secret:
            return True  # No secret configured

        signature = headers.get("X-HA-Signature")
        expected = hmac.new(
            webhook_secret.encode(),
            frappe.as_json(payload).encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("event_type", "unknown")

    # ─── DEVICE CONTROL ─────────────────────────────────────────────────

    def get_states(self) -> list:
        """Get all entity states."""
        return self._make_request("GET", "states")

    def get_entity_state(self, entity_id: str) -> dict:
        """Get state of specific entity."""
        return self._make_request("GET", f"states/{entity_id}")

    def call_service(
        self,
        domain: str,
        service: str,
        entity_id: str = None,
        data: dict = None
    ) -> dict:
        """Call a Home Assistant service."""
        payload = data or {}
        if entity_id:
            payload["entity_id"] = entity_id

        return self._make_request(
            "POST",
            f"services/{domain}/{service}",
            data=payload
        )

    def turn_on(self, entity_id: str, **kwargs) -> dict:
        """Turn on an entity."""
        domain = entity_id.split(".")[0]
        return self.call_service(domain, "turn_on", entity_id, kwargs)

    def turn_off(self, entity_id: str) -> dict:
        """Turn off an entity."""
        domain = entity_id.split(".")[0]
        return self.call_service(domain, "turn_off", entity_id)

    def set_thermostat(self, entity_id: str, temperature: float, hvac_mode: str = None) -> dict:
        """Set thermostat temperature."""
        data = {"temperature": temperature}
        if hvac_mode:
            data["hvac_mode"] = hvac_mode
        return self.call_service("climate", "set_temperature", entity_id, data)

    def lock_door(self, entity_id: str) -> dict:
        """Lock a door."""
        return self.call_service("lock", "lock", entity_id)

    def unlock_door(self, entity_id: str) -> dict:
        """Unlock a door."""
        return self.call_service("lock", "unlock", entity_id)

    def trigger_scene(self, scene_id: str) -> dict:
        """Trigger a scene."""
        return self.call_service("scene", "turn_on", scene_id)

    # ─── AUTOMATION ─────────────────────────────────────────────────────

    def get_automations(self) -> list:
        """Get all automations."""
        states = self.get_states()
        return [s for s in states if s["entity_id"].startswith("automation.")]

    def trigger_automation(self, automation_id: str) -> dict:
        """Manually trigger an automation."""
        return self.call_service("automation", "trigger", automation_id)

    def enable_automation(self, automation_id: str) -> dict:
        """Enable an automation."""
        return self.call_service("automation", "turn_on", automation_id)

    def disable_automation(self, automation_id: str) -> dict:
        """Disable an automation."""
        return self.call_service("automation", "turn_off", automation_id)

    # ─── PRESENCE DETECTION ─────────────────────────────────────────────

    def get_presence_entities(self) -> list:
        """Get all presence tracking entities."""
        states = self.get_states()
        return [
            s for s in states
            if s["entity_id"].startswith(("person.", "device_tracker."))
        ]

    def is_anyone_home(self) -> bool:
        """Check if anyone is home."""
        presence = self.get_presence_entities()
        return any(p["state"] == "home" for p in presence)

    def get_home_members(self) -> list:
        """Get list of people currently home."""
        presence = self.get_presence_entities()
        return [
            p["attributes"].get("friendly_name", p["entity_id"])
            for p in presence
            if p["state"] == "home"
        ]

    # ─── DATA TRANSFORMATION ────────────────────────────────────────────

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "device":
            return {
                "device_id": external_data["entity_id"],
                "name": external_data["attributes"].get("friendly_name"),
                "state": external_data["state"],
                "device_type": external_data["entity_id"].split(".")[0],
                "attributes": external_data["attributes"],
                "last_updated": external_data["last_updated"]
            }
        elif data_type == "presence":
            return {
                "entity_id": external_data["entity_id"],
                "name": external_data["attributes"].get("friendly_name"),
                "is_home": external_data["state"] == "home",
                "latitude": external_data["attributes"].get("latitude"),
                "longitude": external_data["attributes"].get("longitude")
            }
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        # Transform Dartwing data to Home Assistant format
        return internal_data

    # ─── HEALTH CHECK ───────────────────────────────────────────────────

    def health_check(self) -> dict:
        try:
            response = self._make_request("GET", "")
            return {
                "status": "healthy",
                "version": response.get("version"),
                "message": response.get("message")
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    # ─── WEBHOOK HANDLERS ───────────────────────────────────────────────

    def _handle_state_changed(self, payload: dict) -> dict:
        """Handle state change event from Home Assistant."""
        entity_id = payload.get("data", {}).get("entity_id")
        new_state = payload.get("data", {}).get("new_state")

        # Broadcast to family
        from dartwing_family.realtime import FamilyRealtimeManager
        FamilyRealtimeManager.broadcast_family_event(
            org_id=self.organization,
            event_type="home_state_changed",
            payload={
                "entity_id": entity_id,
                "new_state": new_state.get("state") if new_state else None,
                "friendly_name": new_state.get("attributes", {}).get("friendly_name")
            }
        )

        return {"status": "processed"}

    def _handle_automation_triggered(self, payload: dict) -> dict:
        """Handle automation triggered event."""
        # Log automation trigger
        automation_id = payload.get("data", {}).get("entity_id")

        frappe.get_doc({
            "doctype": "Home Automation Log",
            "organization": self.organization,
            "automation_id": automation_id,
            "trigger_source": "home_assistant",
            "timestamp": frappe.utils.now_datetime()
        }).insert(ignore_permissions=True)

        return {"status": "logged"}
```

### Apple HomeKit Adapter

```python
# dartwing_family/integrations/home/homekit.py

from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class HomeKitAdapter(BaseIntegrationAdapter):
    """Integration with Apple HomeKit via HomeKit Controller."""

    ADAPTER_NAME = "homekit"
    ADAPTER_TYPE = "home"
    REQUIRES_OAUTH = False  # Uses pairing codes

    def __init__(self, organization: str, config: dict = None):
        super().__init__(organization, config)
        self.pairing_data = self.config.get("pairing_data", {})

    # HomeKit integration via homekit_controller library
    # This provides a bridge to HomeKit accessories

    def discover_accessories(self) -> list:
        """Discover HomeKit accessories on the network."""
        # Uses mDNS/Bonjour to find accessories
        pass

    def pair_accessory(self, accessory_id: str, pairing_code: str) -> dict:
        """Pair with a HomeKit accessory."""
        pass

    def get_paired_accessories(self) -> list:
        """Get all paired accessories."""
        pass

    def get_accessory_characteristics(self, accessory_id: str) -> list:
        """Get characteristics of an accessory."""
        pass

    def set_characteristic(
        self,
        accessory_id: str,
        characteristic: str,
        value: any
    ) -> dict:
        """Set a characteristic value."""
        pass

    # Standard home control methods
    def turn_on(self, accessory_id: str) -> dict:
        return self.set_characteristic(accessory_id, "On", True)

    def turn_off(self, accessory_id: str) -> dict:
        return self.set_characteristic(accessory_id, "On", False)

    def set_brightness(self, accessory_id: str, brightness: int) -> dict:
        return self.set_characteristic(accessory_id, "Brightness", brightness)

    def set_thermostat(self, accessory_id: str, temperature: float) -> dict:
        return self.set_characteristic(
            accessory_id,
            "TargetTemperature",
            temperature
        )

    def _build_url(self, endpoint: str) -> str:
        # HomeKit uses local network, not HTTP API
        return None

    def get_oauth_url(self, redirect_uri: str) -> str:
        return None

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        return {}

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        return True  # HomeKit uses encrypted local communication

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("type", "unknown")

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def health_check(self) -> dict:
        return {"status": "healthy" if self.pairing_data else "not_configured"}
```

## 4.4 Retail Integration Adapters

### Amazon Orders Adapter

```python
# dartwing_family/integrations/retail/amazon.py

import frappe
from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class AmazonAdapter(BaseIntegrationAdapter):
    """Integration with Amazon for order tracking and inventory."""

    ADAPTER_NAME = "amazon"
    ADAPTER_TYPE = "retail"
    REQUIRES_OAUTH = True
    RATE_LIMIT_CALLS = 30
    RATE_LIMIT_PERIOD = 60

    # Amazon API endpoints
    BASE_URL = "https://api.amazon.com"
    AUTH_URL = "https://www.amazon.com/ap/oa"
    TOKEN_URL = "https://api.amazon.com/auth/o2/token"

    SCOPES = [
        "profile",
        "postal_code",
        "dash:replenish"  # For order history
    ]

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        client_id = frappe.conf.get("amazon_client_id")
        scope = " ".join(self.SCOPES)

        return (
            f"{self.AUTH_URL}?"
            f"client_id={client_id}&"
            f"scope={scope}&"
            f"response_type=code&"
            f"redirect_uri={redirect_uri}"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        response = self.session.post(
            self.TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": frappe.conf.get("amazon_client_id"),
                "client_secret": frappe.conf.get("amazon_client_secret")
            }
        )

        tokens = response.json()
        self._save_tokens(
            tokens["access_token"],
            tokens["refresh_token"],
            tokens["expires_in"]
        )

        return tokens

    def _refresh_token(self):
        response = self.session.post(
            self.TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.config.get("refresh_token"),
                "client_id": frappe.conf.get("amazon_client_id"),
                "client_secret": frappe.conf.get("amazon_client_secret")
            }
        )

        tokens = response.json()
        self._save_tokens(
            tokens["access_token"],
            tokens.get("refresh_token", self.config.get("refresh_token")),
            tokens["expires_in"]
        )

    # ─── ORDER TRACKING ─────────────────────────────────────────────────

    def get_orders(self, days: int = 30) -> list:
        """Get recent orders."""
        # Note: Amazon's actual order API requires seller/vendor partnership
        # This is a conceptual implementation
        orders = self._make_request(
            "GET",
            "user/orders",
            params={"days": days}
        )

        return [self.transform_to_internal(o, "order") for o in orders]

    def get_order_details(self, order_id: str) -> dict:
        """Get details of a specific order."""
        order = self._make_request("GET", f"user/orders/{order_id}")
        return self.transform_to_internal(order, "order")

    def get_order_tracking(self, order_id: str) -> dict:
        """Get tracking information for an order."""
        return self._make_request("GET", f"user/orders/{order_id}/tracking")

    # ─── PRODUCT INFORMATION ────────────────────────────────────────────

    def get_product_details(self, asin: str) -> dict:
        """Get product details by ASIN."""
        return self._make_request("GET", f"products/{asin}")

    def search_products(self, query: str, category: str = None) -> list:
        """Search for products."""
        params = {"query": query}
        if category:
            params["category"] = category

        return self._make_request("GET", "products/search", params=params)

    # ─── DATA TRANSFORMATION ────────────────────────────────────────────

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "order":
            return {
                "external_order_id": external_data.get("orderId"),
                "platform": "amazon",
                "order_date": external_data.get("orderDate"),
                "status": self._map_order_status(external_data.get("orderStatus")),
                "items": [
                    {
                        "name": item.get("title"),
                        "asin": item.get("asin"),
                        "quantity": item.get("quantity"),
                        "price": item.get("price", {}).get("amount")
                    }
                    for item in external_data.get("items", [])
                ],
                "shipping_address": external_data.get("shippingAddress"),
                "estimated_delivery": external_data.get("estimatedDelivery")
            }
        return external_data

    def _map_order_status(self, amazon_status: str) -> str:
        status_map = {
            "Pending": "pending",
            "Shipped": "shipped",
            "Delivered": "delivered",
            "Cancelled": "cancelled",
            "Returned": "returned"
        }
        return status_map.get(amazon_status, "unknown")

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        # Amazon SNS webhook verification
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("Type", "unknown")

    def health_check(self) -> dict:
        try:
            self._make_request("GET", "user/profile")
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

### Walmart Adapter

```python
# dartwing_family/integrations/retail/walmart.py

from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class WalmartAdapter(BaseIntegrationAdapter):
    """Integration with Walmart for grocery and order tracking."""

    ADAPTER_NAME = "walmart"
    ADAPTER_TYPE = "retail"
    REQUIRES_OAUTH = True

    BASE_URL = "https://developer.api.walmart.com"

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/api/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        # Walmart OAuth implementation
        pass

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        pass

    # ─── GROCERY FEATURES ───────────────────────────────────────────────

    def get_grocery_orders(self, days: int = 30) -> list:
        """Get recent grocery orders."""
        pass

    def get_pickup_slots(self, store_id: str, date: str) -> list:
        """Get available pickup time slots."""
        pass

    def add_to_cart(self, items: list) -> dict:
        """Add items to Walmart cart."""
        pass

    def get_cart(self) -> dict:
        """Get current cart contents."""
        pass

    def search_products(self, query: str) -> list:
        """Search Walmart products."""
        pass

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("event", "unknown")

    def health_check(self) -> dict:
        return {"status": "healthy"}
```

## 4.5 Education Platform Adapters

### Google Classroom Adapter

```python
# dartwing_family/integrations/education/google_classroom.py

import frappe
from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class GoogleClassroomAdapter(BaseIntegrationAdapter):
    """Integration with Google Classroom for academic tracking."""

    ADAPTER_NAME = "google_classroom"
    ADAPTER_TYPE = "education"
    REQUIRES_OAUTH = True

    BASE_URL = "https://classroom.googleapis.com/v1"
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    SCOPES = [
        "https://www.googleapis.com/auth/classroom.courses.readonly",
        "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
        "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
        "https://www.googleapis.com/auth/classroom.profile.emails"
    ]

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        client_id = frappe.conf.get("google_client_id")
        scope = " ".join(self.SCOPES)

        return (
            f"{self.AUTH_URL}?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"access_type=offline&"
            f"prompt=consent"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        response = self.session.post(
            self.TOKEN_URL,
            data={
                "code": code,
                "client_id": frappe.conf.get("google_client_id"),
                "client_secret": frappe.conf.get("google_client_secret"),
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
        )

        tokens = response.json()
        self._save_tokens(
            tokens["access_token"],
            tokens["refresh_token"],
            tokens["expires_in"]
        )

        return tokens

    def _refresh_token(self):
        response = self.session.post(
            self.TOKEN_URL,
            data={
                "refresh_token": self.config.get("refresh_token"),
                "client_id": frappe.conf.get("google_client_id"),
                "client_secret": frappe.conf.get("google_client_secret"),
                "grant_type": "refresh_token"
            }
        )

        tokens = response.json()
        self._save_tokens(
            tokens["access_token"],
            self.config.get("refresh_token"),  # Google doesn't always return new refresh token
            tokens["expires_in"]
        )

    # ─── COURSES ────────────────────────────────────────────────────────

    def get_courses(self, student_id: str = "me") -> list:
        """Get all courses for a student."""
        courses = self._make_request(
            "GET",
            "courses",
            params={"studentId": student_id}
        )

        return [
            self.transform_to_internal(c, "course")
            for c in courses.get("courses", [])
        ]

    def get_course(self, course_id: str) -> dict:
        """Get details of a specific course."""
        course = self._make_request("GET", f"courses/{course_id}")
        return self.transform_to_internal(course, "course")

    # ─── ASSIGNMENTS ────────────────────────────────────────────────────

    def get_coursework(self, course_id: str) -> list:
        """Get all assignments for a course."""
        coursework = self._make_request(
            "GET",
            f"courses/{course_id}/courseWork"
        )

        return [
            self.transform_to_internal(cw, "assignment")
            for cw in coursework.get("courseWork", [])
        ]

    def get_student_submissions(
        self,
        course_id: str,
        coursework_id: str,
        student_id: str = "me"
    ) -> list:
        """Get student's submissions for an assignment."""
        submissions = self._make_request(
            "GET",
            f"courses/{course_id}/courseWork/{coursework_id}/studentSubmissions",
            params={"userId": student_id}
        )

        return [
            self.transform_to_internal(s, "submission")
            for s in submissions.get("studentSubmissions", [])
        ]

    def get_all_grades(self, student_id: str = "me") -> list:
        """Get all grades across all courses."""
        courses = self.get_courses(student_id)
        all_grades = []

        for course in courses:
            coursework = self.get_coursework(course["course_id"])
            for assignment in coursework:
                submissions = self.get_student_submissions(
                    course["course_id"],
                    assignment["assignment_id"],
                    student_id
                )
                for submission in submissions:
                    if submission.get("grade"):
                        all_grades.append({
                            "course": course["name"],
                            "assignment": assignment["title"],
                            "grade": submission["grade"],
                            "max_points": assignment["max_points"],
                            "due_date": assignment["due_date"],
                            "submitted_at": submission.get("submitted_at")
                        })

        return all_grades

    def get_missing_assignments(self, student_id: str = "me") -> list:
        """Get all missing/late assignments."""
        courses = self.get_courses(student_id)
        missing = []

        for course in courses:
            coursework = self.get_coursework(course["course_id"])
            for assignment in coursework:
                submissions = self.get_student_submissions(
                    course["course_id"],
                    assignment["assignment_id"],
                    student_id
                )

                for submission in submissions:
                    if submission.get("status") in ["NEW", "CREATED"]:
                        # Check if past due
                        if assignment.get("due_date"):
                            due = frappe.utils.get_datetime(assignment["due_date"])
                            if due < frappe.utils.now_datetime():
                                missing.append({
                                    "course": course["name"],
                                    "assignment": assignment["title"],
                                    "due_date": assignment["due_date"],
                                    "days_overdue": (
                                        frappe.utils.now_datetime() - due
                                    ).days
                                })

        return missing

    # ─── DATA TRANSFORMATION ────────────────────────────────────────────

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "course":
            return {
                "course_id": external_data.get("id"),
                "name": external_data.get("name"),
                "section": external_data.get("section"),
                "teacher_name": external_data.get("ownerId"),
                "room": external_data.get("room"),
                "course_state": external_data.get("courseState")
            }
        elif data_type == "assignment":
            due_date = None
            if external_data.get("dueDate"):
                due = external_data["dueDate"]
                due_date = f"{due.get('year')}-{due.get('month'):02d}-{due.get('day'):02d}"

            return {
                "assignment_id": external_data.get("id"),
                "course_id": external_data.get("courseId"),
                "title": external_data.get("title"),
                "description": external_data.get("description"),
                "max_points": external_data.get("maxPoints"),
                "due_date": due_date,
                "state": external_data.get("state"),
                "work_type": external_data.get("workType")
            }
        elif data_type == "submission":
            return {
                "submission_id": external_data.get("id"),
                "student_id": external_data.get("userId"),
                "status": external_data.get("state"),
                "grade": external_data.get("assignedGrade"),
                "draft_grade": external_data.get("draftGrade"),
                "submitted_at": external_data.get("updateTime"),
                "late": external_data.get("late", False)
            }

        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        # Google Classroom doesn't have webhooks, uses polling
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return "poll_update"

    def health_check(self) -> dict:
        try:
            self.get_courses()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

## 4.6 Location & Tracker Adapters

### Apple FindMy Adapter

```python
# dartwing_family/integrations/location/findmy.py

from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class AppleFindMyAdapter(BaseIntegrationAdapter):
    """Integration with Apple Find My network for AirTags and devices."""

    ADAPTER_NAME = "apple_findmy"
    ADAPTER_TYPE = "location"
    REQUIRES_OAUTH = True

    # Apple iCloud API
    BASE_URL = "https://fmipmobile.icloud.com"

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        # Apple Sign In with iCloud scope
        pass

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        pass

    # ─── DEVICE LOCATION ────────────────────────────────────────────────

    def get_all_devices(self) -> list:
        """Get all devices and items in Find My."""
        # Returns iPhones, iPads, AirTags, etc.
        pass

    def get_device_location(self, device_id: str) -> dict:
        """Get current location of a device."""
        pass

    def play_sound(self, device_id: str) -> dict:
        """Play sound on a device to help locate it."""
        pass

    def enable_lost_mode(
        self,
        device_id: str,
        phone_number: str,
        message: str
    ) -> dict:
        """Enable lost mode on a device."""
        pass

    def get_airtag_location(self, airtag_id: str) -> dict:
        """Get location of an AirTag."""
        pass

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "device":
            return {
                "device_id": external_data.get("id"),
                "name": external_data.get("name"),
                "device_type": external_data.get("deviceClass"),
                "latitude": external_data.get("location", {}).get("latitude"),
                "longitude": external_data.get("location", {}).get("longitude"),
                "accuracy": external_data.get("location", {}).get("horizontalAccuracy"),
                "battery_level": external_data.get("batteryLevel"),
                "last_updated": external_data.get("location", {}).get("timeStamp")
            }
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return "location_update"

    def health_check(self) -> dict:
        return {"status": "healthy"}
```

### Tile Adapter

```python
# dartwing_family/integrations/location/tile.py

from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class TileAdapter(BaseIntegrationAdapter):
    """Integration with Tile trackers."""

    ADAPTER_NAME = "tile"
    ADAPTER_TYPE = "location"
    REQUIRES_OAUTH = True

    BASE_URL = "https://production.tile-api.com/api/v1"
    AUTH_URL = "https://production.tile-api.com/api/v1/clients/sessions"

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        # Tile uses username/password auth, not OAuth
        return None

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        return {}

    def authenticate(self, email: str, password: str) -> dict:
        """Authenticate with Tile using email/password."""
        response = self.session.post(
            self.AUTH_URL,
            json={
                "email": email,
                "password": password
            }
        )

        data = response.json()
        self._save_tokens(
            data.get("session_token"),
            None,  # No refresh token
            86400  # 24 hours
        )

        return data

    # ─── TILE OPERATIONS ────────────────────────────────────────────────

    def get_tiles(self) -> list:
        """Get all Tile devices."""
        tiles = self._make_request("GET", "tiles")
        return [self.transform_to_internal(t, "tile") for t in tiles]

    def get_tile_state(self, tile_uuid: str) -> dict:
        """Get current state of a Tile."""
        return self._make_request("GET", f"tiles/{tile_uuid}/state")

    def ring_tile(self, tile_uuid: str) -> dict:
        """Ring a Tile to help locate it."""
        return self._make_request("POST", f"tiles/{tile_uuid}/ring")

    def notify_when_found(self, tile_uuid: str) -> dict:
        """Enable notify when found for a lost Tile."""
        return self._make_request(
            "POST",
            f"tiles/{tile_uuid}/notify_when_found"
        )

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "tile":
            return {
                "device_id": external_data.get("tile_uuid"),
                "name": external_data.get("name"),
                "device_type": "tile",
                "latitude": external_data.get("last_tile_state", {}).get("latitude"),
                "longitude": external_data.get("last_tile_state", {}).get("longitude"),
                "last_updated": external_data.get("last_tile_state", {}).get("timestamp"),
                "is_lost": external_data.get("is_lost", False)
            }
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("event_type", "unknown")

    def health_check(self) -> dict:
        try:
            self.get_tiles()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

## 4.7 Vehicle Telematics Adapters

### OBD-II Adapter

```python
# dartwing_family/integrations/vehicle/obd2.py

from dartwing_family.integrations.base_adapter import BaseIntegrationAdapter
from dartwing_family.integrations.registry import register_adapter

@register_adapter
class OBD2Adapter(BaseIntegrationAdapter):
    """Integration with OBD-II dongles for vehicle telematics."""

    ADAPTER_NAME = "obd2"
    ADAPTER_TYPE = "vehicle"
    REQUIRES_OAUTH = False

    # Supports various OBD-II dongle providers
    SUPPORTED_PROVIDERS = [
        "automatic",
        "bouncie",
        "carlock",
        "zubie",
        "hum"
    ]

    def __init__(self, organization: str, config: dict = None):
        super().__init__(organization, config)
        self.provider = self.config.get("provider", "bouncie")
        self.base_url = self._get_provider_url()

    def _get_provider_url(self) -> str:
        urls = {
            "bouncie": "https://api.bouncie.com/v1",
            "automatic": "https://api.automatic.com/v1",
            "carlock": "https://api.carlock.co/v1"
        }
        return urls.get(self.provider, "")

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"

    def get_oauth_url(self, redirect_uri: str) -> str:
        # Provider-specific OAuth
        pass

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        pass

    # ─── VEHICLE DATA ───────────────────────────────────────────────────

    def get_vehicles(self) -> list:
        """Get all connected vehicles."""
        vehicles = self._make_request("GET", "vehicles")
        return [self.transform_to_internal(v, "vehicle") for v in vehicles]

    def get_vehicle_location(self, vehicle_id: str) -> dict:
        """Get current vehicle location."""
        return self._make_request("GET", f"vehicles/{vehicle_id}/location")

    def get_trips(self, vehicle_id: str, start_date: str, end_date: str) -> list:
        """Get trips for a vehicle in date range."""
        trips = self._make_request(
            "GET",
            f"vehicles/{vehicle_id}/trips",
            params={"start": start_date, "end": end_date}
        )
        return [self.transform_to_internal(t, "trip") for t in trips]

    def get_driving_events(self, vehicle_id: str, trip_id: str = None) -> list:
        """Get driving events (hard braking, speeding, etc.)."""
        endpoint = f"vehicles/{vehicle_id}/events"
        if trip_id:
            endpoint = f"vehicles/{vehicle_id}/trips/{trip_id}/events"

        events = self._make_request("GET", endpoint)
        return [self.transform_to_internal(e, "event") for e in events]

    def get_diagnostics(self, vehicle_id: str) -> dict:
        """Get vehicle diagnostics (check engine codes, etc.)."""
        return self._make_request("GET", f"vehicles/{vehicle_id}/diagnostics")

    def get_fuel_level(self, vehicle_id: str) -> dict:
        """Get current fuel level."""
        return self._make_request("GET", f"vehicles/{vehicle_id}/fuel")

    # ─── TEEN DRIVING SPECIFIC ──────────────────────────────────────────

    def calculate_driving_score(self, vehicle_id: str, driver_id: str, days: int = 7) -> dict:
        """Calculate driving score for a driver."""
        from datetime import datetime, timedelta

        end_date = datetime.now().isoformat()
        start_date = (datetime.now() - timedelta(days=days)).isoformat()

        trips = self.get_trips(vehicle_id, start_date, end_date)

        # Filter trips by driver if multiple drivers
        driver_trips = [t for t in trips if t.get("driver_id") == driver_id]

        # Calculate score
        total_miles = sum(t.get("distance_miles", 0) for t in driver_trips)
        hard_brakes = sum(t.get("hard_brakes", 0) for t in driver_trips)
        speed_events = sum(t.get("speeding_events", 0) for t in driver_trips)

        # Base score of 100, deduct for events
        score = 100
        score -= hard_brakes * 3  # -3 per hard brake
        score -= speed_events * 5  # -5 per speeding event

        # Bonus for miles without incident
        incident_free_miles = total_miles - (hard_brakes + speed_events) * 2
        if incident_free_miles > 50:
            score += min(10, incident_free_miles / 10)

        return {
            "score": max(0, min(100, score)),
            "total_miles": total_miles,
            "total_trips": len(driver_trips),
            "hard_brakes": hard_brakes,
            "speeding_events": speed_events,
            "period_days": days
        }

    def transform_to_internal(self, external_data: dict, data_type: str) -> dict:
        if data_type == "vehicle":
            return {
                "vehicle_id": external_data.get("id"),
                "vin": external_data.get("vin"),
                "make": external_data.get("make"),
                "model": external_data.get("model"),
                "year": external_data.get("year"),
                "nickname": external_data.get("nickname"),
                "odometer": external_data.get("odometer")
            }
        elif data_type == "trip":
            return {
                "trip_id": external_data.get("id"),
                "vehicle_id": external_data.get("vehicle_id"),
                "driver_id": external_data.get("driver_id"),
                "start_time": external_data.get("started_at"),
                "end_time": external_data.get("ended_at"),
                "start_location": external_data.get("start_location"),
                "end_location": external_data.get("end_location"),
                "distance_miles": external_data.get("distance_miles"),
                "duration_minutes": external_data.get("duration_minutes"),
                "average_speed": external_data.get("average_speed_mph"),
                "max_speed": external_data.get("max_speed_mph"),
                "hard_brakes": external_data.get("hard_brakes"),
                "rapid_accelerations": external_data.get("rapid_accelerations"),
                "speeding_events": external_data.get("speeding_events")
            }
        elif data_type == "event":
            return {
                "event_id": external_data.get("id"),
                "event_type": external_data.get("type"),
                "timestamp": external_data.get("timestamp"),
                "latitude": external_data.get("latitude"),
                "longitude": external_data.get("longitude"),
                "speed": external_data.get("speed_mph"),
                "speed_limit": external_data.get("speed_limit_mph")
            }
        return external_data

    def transform_to_external(self, internal_data: dict, data_type: str) -> dict:
        return internal_data

    def _verify_webhook(self, payload: dict, headers: dict) -> bool:
        return True

    def _extract_event_type(self, payload: dict) -> str:
        return payload.get("event", "unknown")

    def health_check(self) -> dict:
        try:
            self.get_vehicles()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

## 4.8 Integration Configuration DocType

```python
# dartwing_family/doctype/integration_configuration/integration_configuration.json
{
    "doctype": "DocType",
    "name": "Integration Configuration",
    "module": "Dartwing Family",

    "fields": [
        {
            "fieldname": "adapter",
            "fieldtype": "Select",
            "label": "Integration",
            "options": "home_assistant\nhomekit\ngoogle_home\namazon_alexa\nsmartthings\namazon\nwalmart\ngoogle_classroom\ncanvas\npowerschool\napple_findmy\ntile\nobd2\ntesla",
            "reqd": 1
        },
        {
            "fieldname": "adapter_type",
            "fieldtype": "Select",
            "label": "Type",
            "options": "home\nretail\neducation\nlocation\nvehicle\nhealth",
            "read_only": 1
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Connected\nDisconnected\nError\nPending",
            "default": "Disconnected"
        },
        {
            "fieldname": "section_auth",
            "fieldtype": "Section Break",
            "label": "Authentication"
        },
        {
            "fieldname": "access_token",
            "fieldtype": "Password",
            "label": "Access Token"
        },
        {
            "fieldname": "refresh_token",
            "fieldtype": "Password",
            "label": "Refresh Token"
        },
        {
            "fieldname": "token_expires",
            "fieldtype": "Datetime",
            "label": "Token Expires"
        },
        {
            "fieldname": "section_config",
            "fieldtype": "Section Break",
            "label": "Configuration"
        },
        {
            "fieldname": "config_json",
            "fieldtype": "JSON",
            "label": "Additional Configuration"
        },
        {
            "fieldname": "webhook_secret",
            "fieldtype": "Password",
            "label": "Webhook Secret"
        },
        {
            "fieldname": "section_status",
            "fieldtype": "Section Break",
            "label": "Status"
        },
        {
            "fieldname": "last_sync",
            "fieldtype": "Datetime",
            "label": "Last Sync"
        },
        {
            "fieldname": "last_error",
            "fieldtype": "Small Text",
            "label": "Last Error"
        },
        {
            "fieldname": "organization",
            "fieldtype": "Link",
            "label": "Organization",
            "options": "Organization",
            "reqd": 1
        }
    ]
}
```

## 4.9 Webhook Router

```python
# dartwing_family/integrations/webhook_router.py

import frappe
from dartwing_family.integrations.registry import AdapterRegistry

@frappe.whitelist(allow_guest=True)
def handle_webhook(adapter: str, organization: str):
    """Universal webhook endpoint for all integrations."""

    # Validate organization exists
    if not frappe.db.exists("Organization", organization):
        frappe.throw("Invalid organization")

    # Get adapter instance
    adapter_instance = AdapterRegistry.get_adapter(adapter, organization)

    # Get payload and headers
    payload = frappe.request.get_json()
    headers = dict(frappe.request.headers)

    # Process webhook
    try:
        result = adapter_instance.handle_webhook(payload, headers)
        return {"status": "success", "result": result}
    except Exception as e:
        frappe.log_error(
            title=f"Webhook Error: {adapter}",
            message=f"Organization: {organization}\nPayload: {payload}\nError: {str(e)}"
        )
        return {"status": "error", "message": str(e)}


# Webhook URL format: /api/method/dartwing_family.integrations.webhook_router.handle_webhook?adapter={adapter}&organization={org_id}
```

---

_End of Section 4: Integration Architecture_

**Next Section:** Section 5 - Mobile Application Architecture (Flutter, state management, native integrations)

# Section 5: Mobile Application Architecture

## 5.1 Flutter Application Overview

The Dartwing Family mobile app is built with Flutter for cross-platform iOS and Android deployment:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUTTER APPLICATION ARCHITECTURE                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         PRESENTATION LAYER                           │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Screens   │  │   Widgets    │  │   Themes     │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • Dashboard  │  │ • FamilyCard │  │ • Light Mode │              │    │
│  │  │ • Calendar   │  │ • ChoreItem  │  │ • Dark Mode  │              │    │
│  │  │ • Chores     │  │ • MapView    │  │ • Kid Mode   │              │    │
│  │  │ • Location   │  │ • Charts     │  │ • Senior UI  │              │    │
│  │  │ • Settings   │  │ • Forms      │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          STATE MANAGEMENT                            │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                      RIVERPOD PROVIDERS                       │   │    │
│  │  │                                                               │   │    │
│  │  │  • authProvider          • choreProvider                     │   │    │
│  │  │  • familyProvider        • calendarProvider                  │   │    │
│  │  │  • locationProvider      • notificationProvider              │   │    │
│  │  │  • settingsProvider      • realtimeProvider                  │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          DOMAIN LAYER                                │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Entities   │  │  Use Cases   │  │ Repositories │              │    │
│  │  │              │  │              │  │  (Abstract)  │              │    │
│  │  │ • Member     │  │ • GetFamily  │  │              │              │    │
│  │  │ • Chore      │  │ • CompleteC. │  │ • IFamily    │              │    │
│  │  │ • Event      │  │ • AddEvent   │  │ • IChore     │              │    │
│  │  │ • Location   │  │ • ShareLoc   │  │ • ILocation  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           DATA LAYER                                 │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  API Client  │  │  Local DB    │  │    Sync      │              │    │
│  │  │   (Dio)      │  │   (Hive)     │  │   Engine     │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • REST       │  │ • Offline    │  │ • Queue      │              │    │
│  │  │ • WebSocket  │  │ • Cache      │  │ • Conflict   │              │    │
│  │  │ • Auth       │  │ • Encrypted  │  │ • Delta      │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      NATIVE INTEGRATIONS                             │    │
│  │                                                                      │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │    │
│  │  │ Location │ │ Biometric│ │  Camera  │ │  Push    │ │ Background│  │    │
│  │  │ Services │ │   Auth   │ │          │ │  Notif.  │ │  Tasks   │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 5.2 Project Structure

```
dartwing_family_app/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   │
│   ├── core/
│   │   ├── config/
│   │   │   ├── app_config.dart
│   │   │   ├── environment.dart
│   │   │   └── routes.dart
│   │   ├── constants/
│   │   │   ├── api_constants.dart
│   │   │   ├── app_constants.dart
│   │   │   └── storage_keys.dart
│   │   ├── errors/
│   │   │   ├── exceptions.dart
│   │   │   └── failures.dart
│   │   ├── network/
│   │   │   ├── api_client.dart
│   │   │   ├── api_interceptors.dart
│   │   │   └── websocket_client.dart
│   │   ├── storage/
│   │   │   ├── secure_storage.dart
│   │   │   ├── hive_storage.dart
│   │   │   └── cache_manager.dart
│   │   ├── sync/
│   │   │   ├── sync_engine.dart
│   │   │   ├── sync_queue.dart
│   │   │   └── conflict_resolver.dart
│   │   └── utils/
│   │       ├── date_utils.dart
│   │       ├── permission_utils.dart
│   │       └── validators.dart
│   │
│   ├── data/
│   │   ├── datasources/
│   │   │   ├── remote/
│   │   │   │   ├── family_remote_datasource.dart
│   │   │   │   ├── chore_remote_datasource.dart
│   │   │   │   └── location_remote_datasource.dart
│   │   │   └── local/
│   │   │       ├── family_local_datasource.dart
│   │   │       ├── chore_local_datasource.dart
│   │   │       └── location_local_datasource.dart
│   │   ├── models/
│   │   │   ├── family_member_model.dart
│   │   │   ├── chore_model.dart
│   │   │   ├── calendar_event_model.dart
│   │   │   └── location_model.dart
│   │   └── repositories/
│   │       ├── family_repository_impl.dart
│   │       ├── chore_repository_impl.dart
│   │       └── location_repository_impl.dart
│   │
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── family_member.dart
│   │   │   ├── chore.dart
│   │   │   ├── calendar_event.dart
│   │   │   └── location.dart
│   │   ├── repositories/
│   │   │   ├── i_family_repository.dart
│   │   │   ├── i_chore_repository.dart
│   │   │   └── i_location_repository.dart
│   │   └── usecases/
│   │       ├── family/
│   │       │   ├── get_family_members.dart
│   │       │   └── update_member.dart
│   │       ├── chores/
│   │       │   ├── get_chores.dart
│   │       │   ├── complete_chore.dart
│   │       │   └── verify_chore.dart
│   │       └── location/
│   │           ├── get_family_locations.dart
│   │           └── share_location.dart
│   │
│   ├── presentation/
│   │   ├── providers/
│   │   │   ├── auth_provider.dart
│   │   │   ├── family_provider.dart
│   │   │   ├── chore_provider.dart
│   │   │   ├── calendar_provider.dart
│   │   │   ├── location_provider.dart
│   │   │   └── settings_provider.dart
│   │   ├── screens/
│   │   │   ├── auth/
│   │   │   │   ├── login_screen.dart
│   │   │   │   └── pin_setup_screen.dart
│   │   │   ├── dashboard/
│   │   │   │   ├── dashboard_screen.dart
│   │   │   │   └── widgets/
│   │   │   ├── family/
│   │   │   │   ├── family_screen.dart
│   │   │   │   └── member_detail_screen.dart
│   │   │   ├── chores/
│   │   │   │   ├── chores_screen.dart
│   │   │   │   ├── chore_detail_screen.dart
│   │   │   │   └── chore_completion_screen.dart
│   │   │   ├── calendar/
│   │   │   │   ├── calendar_screen.dart
│   │   │   │   └── event_detail_screen.dart
│   │   │   ├── location/
│   │   │   │   ├── family_map_screen.dart
│   │   │   │   └── location_history_screen.dart
│   │   │   ├── allowance/
│   │   │   │   ├── allowance_screen.dart
│   │   │   │   └── savings_goal_screen.dart
│   │   │   └── settings/
│   │   │       ├── settings_screen.dart
│   │   │       └── parental_controls_screen.dart
│   │   ├── widgets/
│   │   │   ├── common/
│   │   │   │   ├── loading_widget.dart
│   │   │   │   ├── error_widget.dart
│   │   │   │   └── empty_state_widget.dart
│   │   │   ├── family/
│   │   │   │   ├── family_member_card.dart
│   │   │   │   └── family_member_avatar.dart
│   │   │   ├── chores/
│   │   │   │   ├── chore_card.dart
│   │   │   │   └── chore_progress_indicator.dart
│   │   │   ├── calendar/
│   │   │   │   ├── event_card.dart
│   │   │   │   └── calendar_day_view.dart
│   │   │   └── location/
│   │   │       ├── family_map.dart
│   │   │       └── member_marker.dart
│   │   └── themes/
│   │       ├── app_theme.dart
│   │       ├── kid_theme.dart
│   │       └── senior_theme.dart
│   │
│   └── services/
│       ├── auth_service.dart
│       ├── notification_service.dart
│       ├── location_service.dart
│       ├── biometric_service.dart
│       └── background_service.dart
│
├── android/
│   └── app/
│       └── src/
│           └── main/
│               └── kotlin/
│                   └── BackgroundLocationService.kt
│
├── ios/
│   └── Runner/
│       └── BackgroundLocationManager.swift
│
├── test/
│   ├── unit/
│   ├── widget/
│   └── integration/
│
└── pubspec.yaml
```

## 5.3 State Management with Riverpod

### Provider Architecture

```dart
// lib/presentation/providers/family_provider.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dartwing_family/domain/entities/family_member.dart';
import 'package:dartwing_family/domain/usecases/family/get_family_members.dart';

// ─── STATE CLASSES ─────────────────────────────────────────────────────────

class FamilyState {
  final List<FamilyMember> members;
  final FamilyMember? currentMember;
  final bool isLoading;
  final String? error;

  const FamilyState({
    this.members = const [],
    this.currentMember,
    this.isLoading = false,
    this.error,
  });

  FamilyState copyWith({
    List<FamilyMember>? members,
    FamilyMember? currentMember,
    bool? isLoading,
    String? error,
  }) {
    return FamilyState(
      members: members ?? this.members,
      currentMember: currentMember ?? this.currentMember,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

// ─── NOTIFIER ──────────────────────────────────────────────────────────────

class FamilyNotifier extends StateNotifier<FamilyState> {
  final GetFamilyMembers _getFamilyMembers;
  final Ref _ref;

  FamilyNotifier(this._getFamilyMembers, this._ref) : super(const FamilyState());

  Future<void> loadFamily() async {
    state = state.copyWith(isLoading: true, error: null);

    final result = await _getFamilyMembers.execute();

    result.fold(
      (failure) => state = state.copyWith(
        isLoading: false,
        error: failure.message,
      ),
      (members) => state = state.copyWith(
        isLoading: false,
        members: members,
      ),
    );
  }

  void setCurrentMember(FamilyMember member) {
    state = state.copyWith(currentMember: member);
  }

  FamilyMember? getMemberById(String id) {
    return state.members.firstWhere(
      (m) => m.id == id,
      orElse: () => null,
    );
  }

  List<FamilyMember> getChildren() {
    return state.members.where((m) => m.isMinor).toList();
  }

  List<FamilyMember> getAdults() {
    return state.members.where((m) => !m.isMinor).toList();
  }
}

// ─── PROVIDERS ─────────────────────────────────────────────────────────────

final familyProvider = StateNotifierProvider<FamilyNotifier, FamilyState>((ref) {
  final getFamilyMembers = ref.watch(getFamilyMembersProvider);
  return FamilyNotifier(getFamilyMembers, ref);
});

// Derived providers for specific data
final childrenProvider = Provider<List<FamilyMember>>((ref) {
  return ref.watch(familyProvider).members.where((m) => m.isMinor).toList();
});

final currentMemberProvider = Provider<FamilyMember?>((ref) {
  return ref.watch(familyProvider).currentMember;
});

final memberByIdProvider = Provider.family<FamilyMember?, String>((ref, id) {
  return ref.watch(familyProvider).members.firstWhere(
    (m) => m.id == id,
    orElse: () => null,
  );
});
```

### Chore Provider

```dart
// lib/presentation/providers/chore_provider.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dartwing_family/domain/entities/chore.dart';

class ChoreState {
  final List<ChoreAssignment> todayChores;
  final List<ChoreAssignment> weekChores;
  final Map<String, int> streaks;
  final int totalPoints;
  final double totalEarnings;
  final bool isLoading;
  final String? error;

  const ChoreState({
    this.todayChores = const [],
    this.weekChores = const [],
    this.streaks = const {},
    this.totalPoints = 0,
    this.totalEarnings = 0.0,
    this.isLoading = false,
    this.error,
  });

  ChoreState copyWith({
    List<ChoreAssignment>? todayChores,
    List<ChoreAssignment>? weekChores,
    Map<String, int>? streaks,
    int? totalPoints,
    double? totalEarnings,
    bool? isLoading,
    String? error,
  }) {
    return ChoreState(
      todayChores: todayChores ?? this.todayChores,
      weekChores: weekChores ?? this.weekChores,
      streaks: streaks ?? this.streaks,
      totalPoints: totalPoints ?? this.totalPoints,
      totalEarnings: totalEarnings ?? this.totalEarnings,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class ChoreNotifier extends StateNotifier<ChoreState> {
  final Ref _ref;
  final IChoreRepository _choreRepository;

  ChoreNotifier(this._ref, this._choreRepository) : super(const ChoreState());

  Future<void> loadChores(String memberId) async {
    state = state.copyWith(isLoading: true);

    final todayResult = await _choreRepository.getTodayChores(memberId);
    final weekResult = await _choreRepository.getWeekChores(memberId);
    final streaksResult = await _choreRepository.getStreaks(memberId);

    todayResult.fold(
      (failure) => state = state.copyWith(error: failure.message),
      (chores) => state = state.copyWith(todayChores: chores),
    );

    weekResult.fold(
      (failure) => null,
      (chores) => state = state.copyWith(weekChores: chores),
    );

    streaksResult.fold(
      (failure) => null,
      (streaks) => state = state.copyWith(streaks: streaks),
    );

    state = state.copyWith(isLoading: false);
  }

  Future<ChoreCompletionResult> completeChore(
    String choreId, {
    String? photoPath,
    String? notes,
  }) async {
    // Optimistic update
    _updateChoreStatus(choreId, ChoreStatus.completed);

    final result = await _choreRepository.completeChore(
      choreId,
      photoPath: photoPath,
      notes: notes,
    );

    return result.fold(
      (failure) {
        // Revert optimistic update
        _updateChoreStatus(choreId, ChoreStatus.pending);
        return ChoreCompletionResult.failure(failure.message);
      },
      (completion) {
        // Update earnings and points
        state = state.copyWith(
          totalPoints: state.totalPoints + completion.pointsEarned,
          totalEarnings: state.totalEarnings + completion.moneyEarned,
        );
        return ChoreCompletionResult.success(completion);
      },
    );
  }

  void _updateChoreStatus(String choreId, ChoreStatus status) {
    final updatedChores = state.todayChores.map((c) {
      if (c.id == choreId) {
        return c.copyWith(status: status);
      }
      return c;
    }).toList();

    state = state.copyWith(todayChores: updatedChores);
  }
}

final choreProvider = StateNotifierProvider<ChoreNotifier, ChoreState>((ref) {
  final repository = ref.watch(choreRepositoryProvider);
  return ChoreNotifier(ref, repository);
});

// Convenience providers
final pendingChoresProvider = Provider<List<ChoreAssignment>>((ref) {
  return ref.watch(choreProvider).todayChores
      .where((c) => c.status == ChoreStatus.pending)
      .toList();
});

final completedChoresProvider = Provider<List<ChoreAssignment>>((ref) {
  return ref.watch(choreProvider).todayChores
      .where((c) => c.status == ChoreStatus.completed ||
                    c.status == ChoreStatus.verified)
      .toList();
});
```

### Real-Time Provider

```dart
// lib/presentation/providers/realtime_provider.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dartwing_family/core/network/websocket_client.dart';

class RealtimeState {
  final bool isConnected;
  final List<FamilyEvent> recentEvents;
  final DateTime? lastEventTime;

  const RealtimeState({
    this.isConnected = false,
    this.recentEvents = const [],
    this.lastEventTime,
  });
}

class RealtimeNotifier extends StateNotifier<RealtimeState> {
  final WebSocketClient _wsClient;
  final Ref _ref;

  RealtimeNotifier(this._wsClient, this._ref) : super(const RealtimeState()) {
    _initializeConnection();
  }

  void _initializeConnection() {
    _wsClient.connect();

    _wsClient.onConnectionChanged = (isConnected) {
      state = RealtimeState(
        isConnected: isConnected,
        recentEvents: state.recentEvents,
      );
    };

    _wsClient.onFamilyEvent = _handleFamilyEvent;
  }

  void _handleFamilyEvent(FamilyEvent event) {
    // Add to recent events
    final updatedEvents = [event, ...state.recentEvents].take(50).toList();

    state = RealtimeState(
      isConnected: state.isConnected,
      recentEvents: updatedEvents,
      lastEventTime: DateTime.now(),
    );

    // Dispatch to appropriate provider based on event type
    switch (event.type) {
      case 'chore_completed':
        _ref.read(choreProvider.notifier).handleChoreCompleted(event.payload);
        break;
      case 'location_updated':
        _ref.read(locationProvider.notifier).handleLocationUpdate(event.payload);
        break;
      case 'calendar_event_added':
        _ref.read(calendarProvider.notifier).handleEventAdded(event.payload);
        break;
      case 'home_state_changed':
        _ref.read(homeProvider.notifier).handleStateChange(event.payload);
        break;
      case 'emergency_broadcast':
        _ref.read(emergencyProvider.notifier).handleEmergency(event.payload);
        break;
    }
  }

  void disconnect() {
    _wsClient.disconnect();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}

final realtimeProvider = StateNotifierProvider<RealtimeNotifier, RealtimeState>((ref) {
  final wsClient = ref.watch(webSocketClientProvider);
  return RealtimeNotifier(wsClient, ref);
});
```

## 5.4 API Client

### Dio-Based API Client

```dart
// lib/core/network/api_client.dart

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  late final Dio _dio;
  final FlutterSecureStorage _secureStorage;

  static const String _baseUrl = 'https://api.dartwing.app';

  ApiClient(this._secureStorage) {
    _dio = Dio(BaseOptions(
      baseUrl: _baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    _dio.interceptors.addAll([
      AuthInterceptor(_secureStorage),
      LoggingInterceptor(),
      ErrorInterceptor(),
      RetryInterceptor(_dio),
    ]);
  }

  // ─── HTTP METHODS ────────────────────────────────────────────────────────

  Future<T> get<T>(
    String endpoint, {
    Map<String, dynamic>? queryParams,
    Options? options,
  }) async {
    final response = await _dio.get<T>(
      endpoint,
      queryParameters: queryParams,
      options: options,
    );
    return response.data as T;
  }

  Future<T> post<T>(
    String endpoint, {
    dynamic data,
    Map<String, dynamic>? queryParams,
    Options? options,
  }) async {
    final response = await _dio.post<T>(
      endpoint,
      data: data,
      queryParameters: queryParams,
      options: options,
    );
    return response.data as T;
  }

  Future<T> put<T>(
    String endpoint, {
    dynamic data,
    Options? options,
  }) async {
    final response = await _dio.put<T>(
      endpoint,
      data: data,
      options: options,
    );
    return response.data as T;
  }

  Future<T> delete<T>(
    String endpoint, {
    Options? options,
  }) async {
    final response = await _dio.delete<T>(
      endpoint,
      options: options,
    );
    return response.data as T;
  }

  // ─── FILE UPLOAD ─────────────────────────────────────────────────────────

  Future<T> uploadFile<T>(
    String endpoint,
    String filePath,
    String fieldName, {
    Map<String, dynamic>? additionalFields,
    void Function(int, int)? onProgress,
  }) async {
    final formData = FormData.fromMap({
      fieldName: await MultipartFile.fromFile(filePath),
      ...?additionalFields,
    });

    final response = await _dio.post<T>(
      endpoint,
      data: formData,
      onSendProgress: onProgress,
    );

    return response.data as T;
  }

  // ─── FRAPPE-SPECIFIC METHODS ─────────────────────────────────────────────

  Future<Map<String, dynamic>> callFrappeMethod(
    String method, {
    Map<String, dynamic>? args,
  }) async {
    final response = await post<Map<String, dynamic>>(
      '/api/method/$method',
      data: args,
    );
    return response['message'] ?? response;
  }

  Future<Map<String, dynamic>> getDoc(
    String doctype,
    String name, {
    List<String>? fields,
  }) async {
    final params = <String, dynamic>{};
    if (fields != null) {
      params['fields'] = fields;
    }

    return await get<Map<String, dynamic>>(
      '/api/resource/$doctype/$name',
      queryParams: params,
    );
  }

  Future<List<Map<String, dynamic>>> getList(
    String doctype, {
    List<String>? fields,
    Map<String, dynamic>? filters,
    String? orderBy,
    int? limitStart,
    int? limitPageLength,
  }) async {
    final params = <String, dynamic>{
      if (fields != null) 'fields': jsonEncode(fields),
      if (filters != null) 'filters': jsonEncode(filters),
      if (orderBy != null) 'order_by': orderBy,
      if (limitStart != null) 'limit_start': limitStart,
      if (limitPageLength != null) 'limit_page_length': limitPageLength,
    };

    final response = await get<Map<String, dynamic>>(
      '/api/resource/$doctype',
      queryParams: params,
    );

    return List<Map<String, dynamic>>.from(response['data'] ?? []);
  }

  Future<Map<String, dynamic>> createDoc(
    String doctype,
    Map<String, dynamic> data,
  ) async {
    return await post<Map<String, dynamic>>(
      '/api/resource/$doctype',
      data: data,
    );
  }

  Future<Map<String, dynamic>> updateDoc(
    String doctype,
    String name,
    Map<String, dynamic> data,
  ) async {
    return await put<Map<String, dynamic>>(
      '/api/resource/$doctype/$name',
      data: data,
    );
  }
}

// ─── INTERCEPTORS ──────────────────────────────────────────────────────────

class AuthInterceptor extends Interceptor {
  final FlutterSecureStorage _storage;

  AuthInterceptor(this._storage);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await _storage.read(key: 'access_token');

    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      // Try to refresh token
      final refreshed = await _refreshToken();

      if (refreshed) {
        // Retry the request
        final retryResponse = await _retry(err.requestOptions);
        handler.resolve(retryResponse);
        return;
      }
    }

    handler.next(err);
  }

  Future<bool> _refreshToken() async {
    final refreshToken = await _storage.read(key: 'refresh_token');
    if (refreshToken == null) return false;

    try {
      final dio = Dio();
      final response = await dio.post(
        '${ApiClient._baseUrl}/api/method/frappe.core.doctype.user.user.refresh_token',
        data: {'refresh_token': refreshToken},
      );

      if (response.statusCode == 200) {
        await _storage.write(
          key: 'access_token',
          value: response.data['access_token'],
        );
        return true;
      }
    } catch (e) {
      // Refresh failed
    }

    return false;
  }

  Future<Response> _retry(RequestOptions requestOptions) async {
    final token = await _storage.read(key: 'access_token');
    requestOptions.headers['Authorization'] = 'Bearer $token';

    return Dio().fetch(requestOptions);
  }
}

class ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final ApiException apiException;

    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        apiException = ApiException.timeout();
        break;
      case DioExceptionType.connectionError:
        apiException = ApiException.noConnection();
        break;
      case DioExceptionType.badResponse:
        apiException = ApiException.fromResponse(err.response!);
        break;
      default:
        apiException = ApiException.unknown(err.message);
    }

    handler.reject(DioException(
      requestOptions: err.requestOptions,
      error: apiException,
    ));
  }
}

class RetryInterceptor extends Interceptor {
  final Dio _dio;
  static const int _maxRetries = 3;

  RetryInterceptor(this._dio);

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final retryCount = err.requestOptions.extra['retryCount'] ?? 0;

    if (_shouldRetry(err) && retryCount < _maxRetries) {
      err.requestOptions.extra['retryCount'] = retryCount + 1;

      await Future.delayed(Duration(seconds: retryCount + 1));

      try {
        final response = await _dio.fetch(err.requestOptions);
        handler.resolve(response);
        return;
      } catch (e) {
        // Retry failed, continue with error
      }
    }

    handler.next(err);
  }

  bool _shouldRetry(DioException err) {
    return err.type == DioExceptionType.connectionError ||
           err.response?.statusCode == 503 ||
           err.response?.statusCode == 504;
  }
}
```

## 5.5 WebSocket Client for Real-Time

```dart
// lib/core/network/websocket_client.dart

import 'dart:async';
import 'dart:convert';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class WebSocketClient {
  IO.Socket? _socket;
  final String _baseUrl;
  final FlutterSecureStorage _storage;

  bool _isConnected = false;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  static const int _maxReconnectAttempts = 5;

  // Callbacks
  void Function(bool)? onConnectionChanged;
  void Function(FamilyEvent)? onFamilyEvent;
  void Function(String)? onError;

  WebSocketClient(this._baseUrl, this._storage);

  Future<void> connect() async {
    if (_socket != null) return;

    final token = await _storage.read(key: 'access_token');
    if (token == null) {
      onError?.call('No authentication token');
      return;
    }

    _socket = IO.io(
      _baseUrl,
      IO.OptionBuilder()
          .setTransports(['websocket'])
          .setAuth({'token': token})
          .enableAutoConnect()
          .enableReconnection()
          .setReconnectionAttempts(_maxReconnectAttempts)
          .setReconnectionDelay(1000)
          .build(),
    );

    _setupListeners();
  }

  void _setupListeners() {
    _socket!.onConnect((_) {
      _isConnected = true;
      _reconnectAttempts = 0;
      onConnectionChanged?.call(true);

      // Join family room
      _joinFamilyRoom();
    });

    _socket!.onDisconnect((_) {
      _isConnected = false;
      onConnectionChanged?.call(false);
    });

    _socket!.onConnectError((error) {
      onError?.call('Connection error: $error');
      _handleReconnect();
    });

    // Family events
    _socket!.on('family_event', (data) {
      try {
        final event = FamilyEvent.fromJson(data);
        onFamilyEvent?.call(event);
      } catch (e) {
        onError?.call('Failed to parse family event: $e');
      }
    });

    // Emergency events (high priority)
    _socket!.on('emergency', (data) {
      final event = FamilyEvent(
        type: 'emergency_broadcast',
        payload: data,
        timestamp: DateTime.now(),
      );
      onFamilyEvent?.call(event);
    });
  }

  Future<void> _joinFamilyRoom() async {
    final orgId = await _storage.read(key: 'organization_id');
    if (orgId != null) {
      _socket!.emit('join_room', {'room': 'family_$orgId'});
    }
  }

  void _handleReconnect() {
    if (_reconnectAttempts >= _maxReconnectAttempts) {
      onError?.call('Max reconnection attempts reached');
      return;
    }

    _reconnectAttempts++;
    final delay = Duration(seconds: _reconnectAttempts * 2);

    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(delay, () {
      connect();
    });
  }

  void emit(String event, Map<String, dynamic> data) {
    if (_isConnected) {
      _socket!.emit(event, data);
    }
  }

  void disconnect() {
    _reconnectTimer?.cancel();
    _socket?.disconnect();
    _socket?.dispose();
    _socket = null;
    _isConnected = false;
  }

  bool get isConnected => _isConnected;
}

class FamilyEvent {
  final String type;
  final Map<String, dynamic> payload;
  final DateTime timestamp;

  FamilyEvent({
    required this.type,
    required this.payload,
    required this.timestamp,
  });

  factory FamilyEvent.fromJson(Map<String, dynamic> json) {
    return FamilyEvent(
      type: json['type'] as String,
      payload: Map<String, dynamic>.from(json['payload'] ?? {}),
      timestamp: DateTime.tryParse(json['timestamp'] ?? '') ?? DateTime.now(),
    );
  }
}
```

## 5.6 Offline Storage & Sync

### Hive Local Storage

```dart
// lib/core/storage/hive_storage.dart

import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';

class HiveStorage {
  static const String _familyBox = 'family';
  static const String _choresBox = 'chores';
  static const String _calendarBox = 'calendar';
  static const String _locationBox = 'location';
  static const String _syncQueueBox = 'sync_queue';

  static Future<void> initialize() async {
    final appDir = await getApplicationDocumentsDirectory();
    await Hive.initFlutter(appDir.path);

    // Register adapters
    Hive.registerAdapter(FamilyMemberModelAdapter());
    Hive.registerAdapter(ChoreAssignmentModelAdapter());
    Hive.registerAdapter(CalendarEventModelAdapter());
    Hive.registerAdapter(LocationModelAdapter());
    Hive.registerAdapter(SyncActionAdapter());

    // Open boxes with encryption
    final encryptionKey = await _getEncryptionKey();

    await Future.wait([
      Hive.openBox<FamilyMemberModel>(_familyBox, encryptionCipher: HiveAesCipher(encryptionKey)),
      Hive.openBox<ChoreAssignmentModel>(_choresBox, encryptionCipher: HiveAesCipher(encryptionKey)),
      Hive.openBox<CalendarEventModel>(_calendarBox, encryptionCipher: HiveAesCipher(encryptionKey)),
      Hive.openBox<LocationModel>(_locationBox, encryptionCipher: HiveAesCipher(encryptionKey)),
      Hive.openBox<SyncAction>(_syncQueueBox),
    ]);
  }

  static Future<Uint8List> _getEncryptionKey() async {
    const storage = FlutterSecureStorage();
    var key = await storage.read(key: 'hive_key');

    if (key == null) {
      final newKey = Hive.generateSecureKey();
      await storage.write(key: 'hive_key', value: base64Encode(newKey));
      return Uint8List.fromList(newKey);
    }

    return base64Decode(key);
  }

  // ─── FAMILY OPERATIONS ───────────────────────────────────────────────────

  static Box<FamilyMemberModel> get familyBox => Hive.box<FamilyMemberModel>(_familyBox);

  static Future<void> saveFamilyMembers(List<FamilyMemberModel> members) async {
    final box = familyBox;
    await box.clear();
    for (final member in members) {
      await box.put(member.id, member);
    }
  }

  static List<FamilyMemberModel> getFamilyMembers() {
    return familyBox.values.toList();
  }

  static FamilyMemberModel? getFamilyMember(String id) {
    return familyBox.get(id);
  }

  // ─── CHORE OPERATIONS ────────────────────────────────────────────────────

  static Box<ChoreAssignmentModel> get choresBox => Hive.box<ChoreAssignmentModel>(_choresBox);

  static Future<void> saveChores(List<ChoreAssignmentModel> chores) async {
    final box = choresBox;
    await box.clear();
    for (final chore in chores) {
      await box.put(chore.id, chore);
    }
  }

  static List<ChoreAssignmentModel> getChores({String? memberId, DateTime? date}) {
    var chores = choresBox.values.toList();

    if (memberId != null) {
      chores = chores.where((c) => c.assignedTo == memberId).toList();
    }

    if (date != null) {
      chores = chores.where((c) => _isSameDay(c.dueDate, date)).toList();
    }

    return chores;
  }

  static bool _isSameDay(DateTime a, DateTime b) {
    return a.year == b.year && a.month == b.month && a.day == b.day;
  }

  // ─── SYNC QUEUE ──────────────────────────────────────────────────────────

  static Box<SyncAction> get syncQueueBox => Hive.box<SyncAction>(_syncQueueBox);

  static Future<void> queueAction(SyncAction action) async {
    await syncQueueBox.add(action);
  }

  static List<SyncAction> getPendingActions() {
    return syncQueueBox.values.where((a) => !a.isSynced).toList();
  }

  static Future<void> markActionSynced(int key) async {
    final action = syncQueueBox.get(key);
    if (action != null) {
      action.isSynced = true;
      await action.save();
    }
  }

  static Future<void> clearSyncedActions() async {
    final syncedKeys = syncQueueBox.keys.where((key) {
      final action = syncQueueBox.get(key);
      return action?.isSynced ?? false;
    }).toList();

    await syncQueueBox.deleteAll(syncedKeys);
  }
}
```

### Sync Engine

```dart
// lib/core/sync/sync_engine.dart

import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

class SyncEngine {
  final ApiClient _apiClient;
  final HiveStorage _localStorage;

  StreamSubscription<ConnectivityResult>? _connectivitySubscription;
  Timer? _syncTimer;
  bool _isSyncing = false;

  SyncEngine(this._apiClient, this._localStorage);

  void initialize() {
    // Listen for connectivity changes
    _connectivitySubscription = Connectivity().onConnectivityChanged.listen((result) {
      if (result != ConnectivityResult.none) {
        syncPendingActions();
      }
    });

    // Periodic sync every 5 minutes
    _syncTimer = Timer.periodic(const Duration(minutes: 5), (_) {
      syncPendingActions();
    });
  }

  Future<void> syncPendingActions() async {
    if (_isSyncing) return;

    final connectivityResult = await Connectivity().checkConnectivity();
    if (connectivityResult == ConnectivityResult.none) return;

    _isSyncing = true;

    try {
      final pendingActions = HiveStorage.getPendingActions();

      for (final action in pendingActions) {
        try {
          await _executeAction(action);
          await HiveStorage.markActionSynced(action.key);
        } on ConflictException catch (e) {
          await _handleConflict(action, e);
        } catch (e) {
          // Log error but continue with other actions
          print('Sync error for action ${action.id}: $e');
        }
      }

      // Clean up synced actions
      await HiveStorage.clearSyncedActions();

      // Pull latest data from server
      await _pullLatestData();
    } finally {
      _isSyncing = false;
    }
  }

  Future<void> _executeAction(SyncAction action) async {
    switch (action.type) {
      case SyncActionType.create:
        await _apiClient.createDoc(action.doctype, action.data);
        break;
      case SyncActionType.update:
        await _apiClient.updateDoc(action.doctype, action.docname!, action.data);
        break;
      case SyncActionType.delete:
        await _apiClient.delete('/api/resource/${action.doctype}/${action.docname}');
        break;
      case SyncActionType.method:
        await _apiClient.callFrappeMethod(action.method!, args: action.data);
        break;
    }
  }

  Future<void> _handleConflict(SyncAction action, ConflictException e) async {
    switch (action.conflictResolution) {
      case ConflictResolution.serverWins:
        // Discard local changes, pull server version
        await _pullDoc(action.doctype, action.docname!);
        await HiveStorage.markActionSynced(action.key);
        break;
      case ConflictResolution.clientWins:
        // Force push with latest timestamp
        action.data['modified'] = DateTime.now().toIso8601String();
        await _executeAction(action);
        await HiveStorage.markActionSynced(action.key);
        break;
      case ConflictResolution.merge:
        // Attempt to merge changes
        await _mergeChanges(action, e.serverVersion);
        break;
      case ConflictResolution.manual:
        // Flag for user resolution
        action.requiresManualResolution = true;
        await action.save();
        break;
    }
  }

  Future<void> _pullLatestData() async {
    // Pull family members
    final members = await _apiClient.getList('Family Member');
    await HiveStorage.saveFamilyMembers(
      members.map((m) => FamilyMemberModel.fromJson(m)).toList(),
    );

    // Pull today's chores
    final chores = await _apiClient.callFrappeMethod(
      'dartwing_family.api.family_api.get_today_chores',
    );
    await HiveStorage.saveChores(
      (chores['chores'] as List).map((c) => ChoreAssignmentModel.fromJson(c)).toList(),
    );

    // Pull upcoming calendar events
    final events = await _apiClient.callFrappeMethod(
      'dartwing_family.api.family_api.get_upcoming_events',
      args: {'days': 7},
    );
    // Save to local storage...
  }

  Future<void> _pullDoc(String doctype, String name) async {
    final doc = await _apiClient.getDoc(doctype, name);
    // Save to appropriate local storage based on doctype
  }

  Future<void> _mergeChanges(SyncAction action, Map<String, dynamic> serverVersion) async {
    // Field-level merge logic
    final localData = action.data;
    final merged = Map<String, dynamic>.from(serverVersion);

    for (final key in localData.keys) {
      if (action.mergeableFields?.contains(key) ?? false) {
        // Use local value for mergeable fields
        merged[key] = localData[key];
      }
    }

    action.data = merged;
    await _executeAction(action);
    await HiveStorage.markActionSynced(action.key);
  }

  void dispose() {
    _connectivitySubscription?.cancel();
    _syncTimer?.cancel();
  }
}

enum SyncActionType { create, update, delete, method }
enum ConflictResolution { serverWins, clientWins, merge, manual }

@HiveType(typeId: 100)
class SyncAction extends HiveObject {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final SyncActionType type;

  @HiveField(2)
  final String doctype;

  @HiveField(3)
  String? docname;

  @HiveField(4)
  Map<String, dynamic> data;

  @HiveField(5)
  String? method;

  @HiveField(6)
  ConflictResolution conflictResolution;

  @HiveField(7)
  List<String>? mergeableFields;

  @HiveField(8)
  bool isSynced;

  @HiveField(9)
  bool requiresManualResolution;

  @HiveField(10)
  DateTime createdAt;

  SyncAction({
    required this.id,
    required this.type,
    required this.doctype,
    this.docname,
    required this.data,
    this.method,
    this.conflictResolution = ConflictResolution.serverWins,
    this.mergeableFields,
    this.isSynced = false,
    this.requiresManualResolution = false,
    DateTime? createdAt,
  }) : createdAt = createdAt ?? DateTime.now();
}
```

## 5.7 Native Services

### Location Service

```dart
// lib/services/location_service.dart

import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

class LocationService {
  StreamSubscription<Position>? _positionSubscription;
  final ApiClient _apiClient;
  final String _memberId;

  Timer? _uploadTimer;
  Position? _lastPosition;
  static const Duration _uploadInterval = Duration(minutes: 5);

  LocationService(this._apiClient, this._memberId);

  Future<bool> initialize() async {
    // Check permissions
    final status = await Permission.locationAlways.request();
    if (!status.isGranted) {
      return false;
    }

    // Check if location services are enabled
    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return false;
    }

    return true;
  }

  Future<void> startTracking() async {
    if (!await initialize()) return;

    // Start position stream
    _positionSubscription = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 50, // meters
      ),
    ).listen(_onPositionUpdate);

    // Start periodic upload timer
    _uploadTimer = Timer.periodic(_uploadInterval, (_) => _uploadPosition());
  }

  void _onPositionUpdate(Position position) {
    _lastPosition = position;

    // Upload immediately if significant movement
    if (_shouldUploadImmediately(position)) {
      _uploadPosition();
    }
  }

  bool _shouldUploadImmediately(Position position) {
    // Upload immediately if speed > 20 m/s (72 km/h) - likely driving
    if (position.speed > 20) return true;

    // Upload immediately if moved > 500m from last uploaded position
    // Implementation depends on tracking last uploaded position

    return false;
  }

  Future<void> _uploadPosition() async {
    if (_lastPosition == null) return;

    try {
      await _apiClient.callFrappeMethod(
        'dartwing_family.api.location_api.update_location',
        args: {
          'member_id': _memberId,
          'latitude': _lastPosition!.latitude,
          'longitude': _lastPosition!.longitude,
          'accuracy': _lastPosition!.accuracy,
          'speed': _lastPosition!.speed,
          'heading': _lastPosition!.heading,
          'timestamp': _lastPosition!.timestamp?.toIso8601String(),
        },
      );
    } catch (e) {
      // Queue for later sync if offline
      await HiveStorage.queueAction(SyncAction(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        type: SyncActionType.method,
        doctype: 'Location History',
        method: 'dartwing_family.api.location_api.update_location',
        data: {
          'member_id': _memberId,
          'latitude': _lastPosition!.latitude,
          'longitude': _lastPosition!.longitude,
          'accuracy': _lastPosition!.accuracy,
          'timestamp': _lastPosition!.timestamp?.toIso8601String(),
        },
      ));
    }
  }

  Future<Position?> getCurrentPosition() async {
    try {
      return await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
    } catch (e) {
      return _lastPosition;
    }
  }

  void stopTracking() {
    _positionSubscription?.cancel();
    _uploadTimer?.cancel();
    _positionSubscription = null;
    _uploadTimer = null;
  }

  void dispose() {
    stopTracking();
  }
}
```

### Background Service (Android)

```kotlin
// android/app/src/main/kotlin/com/dartwing/family/BackgroundLocationService.kt

package com.dartwing.family

import android.app.*
import android.content.Intent
import android.os.IBinder
import android.os.Looper
import androidx.core.app.NotificationCompat
import com.google.android.gms.location.*

class BackgroundLocationService : Service() {

    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var locationCallback: LocationCallback

    companion object {
        const val CHANNEL_ID = "location_service_channel"
        const val NOTIFICATION_ID = 1
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        setupLocationCallback()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        startForeground(NOTIFICATION_ID, createNotification())
        startLocationUpdates()
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID,
            "Location Service",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Keeps family location updated"
        }

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.createNotificationChannel(channel)
    }

    private fun createNotification(): Notification {
        val intent = packageManager.getLaunchIntentForPackage(packageName)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent, PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Dartwing Family")
            .setContentText("Sharing location with family")
            .setSmallIcon(R.drawable.ic_location)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .build()
    }

    private fun setupLocationCallback() {
        locationCallback = object : LocationCallback() {
            override fun onLocationResult(locationResult: LocationResult) {
                locationResult.lastLocation?.let { location ->
                    // Send to Flutter via method channel
                    LocationMethodChannel.sendLocation(
                        location.latitude,
                        location.longitude,
                        location.accuracy,
                        location.speed,
                        location.time
                    )
                }
            }
        }
    }

    private fun startLocationUpdates() {
        val locationRequest = LocationRequest.Builder(
            Priority.PRIORITY_HIGH_ACCURACY,
            300000 // 5 minutes
        ).apply {
            setMinUpdateDistanceMeters(50f)
            setMinUpdateIntervalMillis(60000) // 1 minute minimum
        }.build()

        try {
            fusedLocationClient.requestLocationUpdates(
                locationRequest,
                locationCallback,
                Looper.getMainLooper()
            )
        } catch (e: SecurityException) {
            // Handle permission not granted
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        fusedLocationClient.removeLocationUpdates(locationCallback)
    }
}
```

### Biometric Authentication

```dart
// lib/services/biometric_service.dart

import 'package:local_auth/local_auth.dart';
import 'package:flutter/services.dart';

class BiometricService {
  final LocalAuthentication _localAuth = LocalAuthentication();

  Future<bool> isAvailable() async {
    try {
      final canCheck = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      return canCheck && isDeviceSupported;
    } on PlatformException {
      return false;
    }
  }

  Future<List<BiometricType>> getAvailableBiometrics() async {
    try {
      return await _localAuth.getAvailableBiometrics();
    } on PlatformException {
      return [];
    }
  }

  Future<bool> authenticate({
    required String reason,
    bool useErrorDialogs = true,
    bool stickyAuth = true,
    bool biometricOnly = false,
  }) async {
    try {
      return await _localAuth.authenticate(
        localizedReason: reason,
        options: AuthenticationOptions(
          useErrorDialogs: useErrorDialogs,
          stickyAuth: stickyAuth,
          biometricOnly: biometricOnly,
        ),
      );
    } on PlatformException catch (e) {
      if (e.code == 'NotAvailable') {
        return false;
      }
      rethrow;
    }
  }

  Future<bool> authenticateForSensitiveAction(String action) async {
    return authenticate(
      reason: 'Please authenticate to $action',
      biometricOnly: false, // Allow PIN/pattern fallback
    );
  }

  Future<bool> authenticateForPayment(double amount) async {
    return authenticate(
      reason: 'Authenticate to approve \$${amount.toStringAsFixed(2)} payment',
      biometricOnly: true, // Require biometric for payments
    );
  }
}
```

## 5.8 Age-Appropriate UI Themes

```dart
// lib/presentation/themes/app_theme.dart

import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData standard({bool isDark = false}) {
    return ThemeData(
      useMaterial3: true,
      colorScheme: isDark ? _darkColorScheme : _lightColorScheme,
      fontFamily: 'Inter',
      // Standard theme configuration
    );
  }

  static ThemeData kidMode() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF7C4DFF), // Playful purple
        brightness: Brightness.light,
      ),
      fontFamily: 'ComicNeue', // Friendly, readable font
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
        bodyLarge: TextStyle(fontSize: 18), // Larger text for kids
        bodyMedium: TextStyle(fontSize: 16),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
        ),
      ),
      cardTheme: CardTheme(
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      // Kid-friendly colors and larger touch targets
    );
  }

  static ThemeData seniorMode() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF1976D2), // Clear blue
        brightness: Brightness.light,
      ),
      fontFamily: 'Roboto',
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontSize: 36, fontWeight: FontWeight.bold),
        displayMedium: TextStyle(fontSize: 32),
        bodyLarge: TextStyle(fontSize: 20), // Larger text
        bodyMedium: TextStyle(fontSize: 18),
        labelLarge: TextStyle(fontSize: 18),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 20),
          minimumSize: const Size(200, 60), // Larger buttons
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
      inputDecorationTheme: const InputDecorationTheme(
        contentPadding: EdgeInsets.all(20),
        border: OutlineInputBorder(),
      ),
      // High contrast, large touch targets
    );
  }

  static final _lightColorScheme = ColorScheme.fromSeed(
    seedColor: const Color(0xFF6366F1), // Indigo
    brightness: Brightness.light,
  );

  static final _darkColorScheme = ColorScheme.fromSeed(
    seedColor: const Color(0xFF6366F1),
    brightness: Brightness.dark,
  );
}

// Theme provider
final themeProvider = StateNotifierProvider<ThemeNotifier, ThemeMode>((ref) {
  return ThemeNotifier();
});

class ThemeNotifier extends StateNotifier<ThemeMode> {
  ThemeNotifier() : super(ThemeMode.system);

  void setTheme(ThemeMode mode) {
    state = mode;
  }

  ThemeData getTheme(BuildContext context, {String? ageCategory}) {
    final isDark = state == ThemeMode.dark ||
        (state == ThemeMode.system &&
            MediaQuery.of(context).platformBrightness == Brightness.dark);

    switch (ageCategory) {
      case 'Child':
      case 'Tween':
        return AppTheme.kidMode();
      case 'Senior':
        return AppTheme.seniorMode();
      default:
        return AppTheme.standard(isDark: isDark);
    }
  }
}
```

---

_End of Section 5: Mobile Application Architecture_

**Next Section:** Section 6 - Voice Assistant & AI Integration Architecture

# Section 6: Voice Assistant & AI Integration Architecture

## 6.1 Voice Assistant Overview

The Dartwing Family Voice Assistant (VA) provides a shared family assistant with personalized voice personas, child-safe responses, and family-scoped knowledge.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VOICE ASSISTANT ARCHITECTURE                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         AUDIO INPUT                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Wake Word   │  │   Mobile     │  │  Smart       │              │    │
│  │  │  Detection   │  │   Mic Input  │  │  Speaker     │              │    │
│  │  │  "Hey Buddy" │  │              │  │  Integration │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     SPEECH-TO-TEXT (STT)                             │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Whisper    │  │   Google     │  │   On-Device  │              │    │
│  │  │   (Primary)  │  │   STT        │  │   (Offline)  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  NATURAL LANGUAGE UNDERSTANDING                      │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Intent     │  │   Entity     │  │   Context    │              │    │
│  │  │   Detection  │  │   Extraction │  │   Manager    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      DIALOG MANAGEMENT                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Family     │  │   Child      │  │   Response   │              │    │
│  │  │   Knowledge  │  │   Safety     │  │   Generator  │              │    │
│  │  │   Base       │  │   Filter     │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      TEXT-TO-SPEECH (TTS)                            │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Voice      │  │   ElevenLabs │  │   On-Device  │              │    │
│  │  │   Cloning    │  │   TTS        │  │   TTS        │              │    │
│  │  │   Engine     │  │              │  │   (Offline)  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        AUDIO OUTPUT                                  │    │
│  │                                                                      │    │
│  │  • Mom's Voice    • Buddy (AI Character)    • Standard VA           │    │
│  │  • Dad's Voice    • Sparkle (Fairy)         • Grandma's Voice       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Voice Cloning System

### Voice Profile Management

```python
# dartwing_family/voice/voice_profile.py

import frappe
from typing import List, Optional
from dartwing_family.voice.providers import VoiceCloningProvider

class VoiceProfileManager:
    """Manages voice profiles for family members."""

    REQUIRED_SAMPLES = 5
    MIN_SAMPLE_DURATION = 5  # seconds
    MAX_SAMPLE_DURATION = 30  # seconds

    def __init__(self, organization: str):
        self.organization = organization
        self.provider = VoiceCloningProvider()

    def create_voice_profile(
        self,
        family_member: str,
        voice_name: str
    ) -> str:
        """Create a new voice profile for a family member."""
        profile = frappe.get_doc({
            "doctype": "Family Voice Profile",
            "family_member": family_member,
            "voice_name": voice_name,
            "training_status": "Not Started",
            "organization": self.organization
        })
        profile.insert()
        return profile.name

    def add_training_sample(
        self,
        profile_id: str,
        audio_file: str,
        transcript: str
    ) -> dict:
        """Add a training sample to a voice profile."""
        profile = frappe.get_doc("Family Voice Profile", profile_id)

        # Validate audio
        validation = self._validate_audio(audio_file)
        if not validation["valid"]:
            return {"success": False, "error": validation["error"]}

        # Add sample
        profile.append("training_samples", {
            "audio_file": audio_file,
            "transcript": transcript,
            "duration_seconds": validation["duration"],
            "quality_score": validation["quality"]
        })

        # Update status
        if len(profile.training_samples) >= self.REQUIRED_SAMPLES:
            profile.training_status = "Ready for Training"
        else:
            profile.training_status = "Partial"

        profile.save()

        return {
            "success": True,
            "samples_collected": len(profile.training_samples),
            "samples_required": self.REQUIRED_SAMPLES,
            "ready_for_training": profile.training_status == "Ready for Training"
        }

    def train_voice_model(self, profile_id: str) -> dict:
        """Train the voice clone model with collected samples."""
        profile = frappe.get_doc("Family Voice Profile", profile_id)

        if len(profile.training_samples) < self.REQUIRED_SAMPLES:
            return {
                "success": False,
                "error": f"Need at least {self.REQUIRED_SAMPLES} samples"
            }

        # Collect audio files
        audio_files = [s.audio_file for s in profile.training_samples]

        # Send to voice cloning provider
        profile.training_status = "Processing"
        profile.save()
        frappe.db.commit()

        try:
            result = self.provider.create_voice_clone(
                name=profile.voice_name,
                audio_files=audio_files,
                description=f"Family voice clone for {profile.voice_name}"
            )

            profile.voice_model_id = result["voice_id"]
            profile.training_status = "Complete"
            profile.quality_score = result.get("quality_score", 0.0)
            profile.save()

            return {"success": True, "voice_id": result["voice_id"]}

        except Exception as e:
            profile.training_status = "Failed"
            profile.save()
            frappe.log_error(
                title="Voice Training Failed",
                message=str(e)
            )
            return {"success": False, "error": str(e)}

    def _validate_audio(self, audio_file: str) -> dict:
        """Validate audio file for voice training."""
        import librosa

        try:
            # Load audio
            y, sr = librosa.load(audio_file)
            duration = librosa.get_duration(y=y, sr=sr)

            # Check duration
            if duration < self.MIN_SAMPLE_DURATION:
                return {
                    "valid": False,
                    "error": f"Audio too short. Minimum {self.MIN_SAMPLE_DURATION} seconds."
                }

            if duration > self.MAX_SAMPLE_DURATION:
                return {
                    "valid": False,
                    "error": f"Audio too long. Maximum {self.MAX_SAMPLE_DURATION} seconds."
                }

            # Calculate quality score (based on SNR, clipping, etc.)
            quality = self._calculate_audio_quality(y, sr)

            if quality < 0.5:
                return {
                    "valid": False,
                    "error": "Audio quality too low. Please record in a quieter environment."
                }

            return {
                "valid": True,
                "duration": duration,
                "quality": quality
            }

        except Exception as e:
            return {"valid": False, "error": f"Could not process audio: {str(e)}"}

    def _calculate_audio_quality(self, y, sr) -> float:
        """Calculate audio quality score (0-1)."""
        import numpy as np

        # Check for clipping
        clipping_ratio = np.sum(np.abs(y) > 0.99) / len(y)
        clipping_score = max(0, 1 - clipping_ratio * 10)

        # Check for silence ratio
        silence_threshold = 0.02
        silence_ratio = np.sum(np.abs(y) < silence_threshold) / len(y)
        silence_score = max(0, 1 - silence_ratio)

        # Estimate SNR (simplified)
        signal_power = np.mean(y ** 2)
        snr_score = min(1, signal_power * 100)

        # Combined score
        return (clipping_score * 0.3 + silence_score * 0.3 + snr_score * 0.4)

    def get_available_voices(self, family_member: str = None) -> List[dict]:
        """Get all available voices for the family."""
        filters = {"organization": self.organization, "training_status": "Complete"}

        profiles = frappe.get_all(
            "Family Voice Profile",
            filters=filters,
            fields=["name", "voice_name", "family_member", "voice_model_id", "quality_score"]
        )

        # Add AI character voices
        ai_voices = self._get_ai_character_voices()

        # Filter by availability if family_member specified
        if family_member:
            profiles = [
                p for p in profiles
                if self._is_voice_available_to(p["name"], family_member)
            ]

        return profiles + ai_voices

    def _get_ai_character_voices(self) -> List[dict]:
        """Get predefined AI character voices."""
        return [
            {
                "name": "buddy",
                "voice_name": "Buddy",
                "description": "Friendly robot helper",
                "voice_model_id": "ai_buddy_v1",
                "is_ai_character": True
            },
            {
                "name": "sparkle",
                "voice_name": "Sparkle",
                "description": "Magical fairy guide",
                "voice_model_id": "ai_sparkle_v1",
                "is_ai_character": True
            },
            {
                "name": "max",
                "voice_name": "Max",
                "description": "Wise dog companion",
                "voice_model_id": "ai_max_v1",
                "is_ai_character": True
            },
            {
                "name": "captain",
                "voice_name": "Captain",
                "description": "Superhero mentor",
                "voice_model_id": "ai_captain_v1",
                "is_ai_character": True
            },
            {
                "name": "nova",
                "voice_name": "Nova",
                "description": "Space explorer",
                "voice_model_id": "ai_nova_v1",
                "is_ai_character": True
            }
        ]

    def _is_voice_available_to(self, profile_id: str, family_member: str) -> bool:
        """Check if a voice profile is available to a family member."""
        profile = frappe.get_doc("Family Voice Profile", profile_id)

        # Check available_to list
        if profile.available_to:
            return family_member in [a.family_member for a in profile.available_to]

        # Default: available to all family members
        return True
```

### Voice Cloning Provider Integration

```python
# dartwing_family/voice/providers.py

import frappe
import requests
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseVoiceProvider(ABC):
    """Abstract base class for voice synthesis providers."""

    @abstractmethod
    def create_voice_clone(
        self,
        name: str,
        audio_files: List[str],
        description: str = ""
    ) -> dict:
        """Create a voice clone from audio samples."""
        pass

    @abstractmethod
    def synthesize_speech(
        self,
        text: str,
        voice_id: str,
        **kwargs
    ) -> bytes:
        """Synthesize speech from text using specified voice."""
        pass

    @abstractmethod
    def get_voices(self) -> List[dict]:
        """Get all available voices."""
        pass


class ElevenLabsProvider(BaseVoiceProvider):
    """ElevenLabs voice synthesis provider."""

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self):
        self.api_key = frappe.conf.get("elevenlabs_api_key")
        if not self.api_key:
            frappe.throw("ElevenLabs API key not configured")

    def _headers(self) -> dict:
        return {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def create_voice_clone(
        self,
        name: str,
        audio_files: List[str],
        description: str = ""
    ) -> dict:
        """Create a voice clone using ElevenLabs Instant Voice Cloning."""

        # Prepare files
        files = []
        for i, audio_path in enumerate(audio_files):
            with open(frappe.get_site_path(audio_path), 'rb') as f:
                files.append(
                    ('files', (f'sample_{i}.mp3', f.read(), 'audio/mpeg'))
                )

        response = requests.post(
            f"{self.BASE_URL}/voices/add",
            headers={"xi-api-key": self.api_key},
            data={
                "name": name,
                "description": description,
                "labels": '{"family": "dartwing"}'
            },
            files=files
        )

        response.raise_for_status()
        result = response.json()

        return {
            "voice_id": result["voice_id"],
            "quality_score": 0.8  # ElevenLabs doesn't return quality score
        }

    def synthesize_speech(
        self,
        text: str,
        voice_id: str,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        use_speaker_boost: bool = True
    ) -> bytes:
        """Synthesize speech using ElevenLabs."""

        response = requests.post(
            f"{self.BASE_URL}/text-to-speech/{voice_id}",
            headers=self._headers(),
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": use_speaker_boost
                }
            }
        )

        response.raise_for_status()
        return response.content

    def get_voices(self) -> List[dict]:
        """Get all ElevenLabs voices."""
        response = requests.get(
            f"{self.BASE_URL}/voices",
            headers=self._headers()
        )

        response.raise_for_status()
        return response.json()["voices"]


class VoiceCloningProvider:
    """Factory for voice providers with fallback support."""

    def __init__(self):
        self.primary_provider = ElevenLabsProvider()
        # Could add fallback providers here

    def create_voice_clone(self, **kwargs) -> dict:
        return self.primary_provider.create_voice_clone(**kwargs)

    def synthesize_speech(self, **kwargs) -> bytes:
        return self.primary_provider.synthesize_speech(**kwargs)

    def get_voices(self) -> List[dict]:
        return self.primary_provider.get_voices()
```

## 6.3 Natural Language Understanding

### Intent Detection System

```python
# dartwing_family/voice/nlu/intent_detection.py

import frappe
from typing import Dict, List, Optional, Tuple
from enum import Enum

class IntentCategory(Enum):
    FAMILY = "family"
    CHORES = "chores"
    CALENDAR = "calendar"
    LOCATION = "location"
    HOME = "home"
    ALLOWANCE = "allowance"
    HEALTH = "health"
    GENERAL = "general"

class Intent(Enum):
    # Family intents
    GET_FAMILY_STATUS = "get_family_status"
    GET_MEMBER_LOCATION = "get_member_location"
    WHO_IS_HOME = "who_is_home"

    # Chore intents
    GET_MY_CHORES = "get_my_chores"
    COMPLETE_CHORE = "complete_chore"
    GET_CHORE_STATUS = "get_chore_status"
    HOW_MUCH_EARNED = "how_much_earned"

    # Calendar intents
    GET_TODAY_SCHEDULE = "get_today_schedule"
    ADD_EVENT = "add_event"
    WHEN_IS_EVENT = "when_is_event"
    WHO_IS_DRIVING = "who_is_driving"

    # Location intents
    WHERE_IS_PERSON = "where_is_person"
    SHARE_MY_LOCATION = "share_my_location"
    CHECK_IN = "check_in"

    # Home intents
    CONTROL_DEVICE = "control_device"
    GET_DEVICE_STATUS = "get_device_status"
    TRIGGER_SCENE = "trigger_scene"
    SET_THERMOSTAT = "set_thermostat"

    # Allowance intents
    CHECK_BALANCE = "check_balance"
    CHECK_SAVINGS_GOAL = "check_savings_goal"

    # Health intents
    GET_EMERGENCY_INFO = "get_emergency_info"

    # General
    HELP = "help"
    UNKNOWN = "unknown"


class IntentDetector:
    """Detects user intent from natural language input."""

    # Pattern-based intent matching for common queries
    INTENT_PATTERNS = {
        Intent.GET_MY_CHORES: [
            r"what (are )?my chores",
            r"what do i (have to|need to) do",
            r"chores (for )?(today|this week)",
            r"any chores"
        ],
        Intent.COMPLETE_CHORE: [
            r"(i )?(finished|completed|done with|did) (my |the )?(.+)",
            r"mark (.+) (as )?(done|complete)",
            r"(.+) is (done|finished|complete)"
        ],
        Intent.WHERE_IS_PERSON: [
            r"where is (my )?(mom|dad|brother|sister|\w+)",
            r"where('s| is) (\w+)",
            r"find (my )?(mom|dad|\w+)",
            r"locate (\w+)"
        ],
        Intent.WHO_IS_HOME: [
            r"who('s| is) home",
            r"is (anyone|everybody|everyone) home",
            r"who('s| is) at home"
        ],
        Intent.GET_TODAY_SCHEDULE: [
            r"what('s| is) (on )?(today|my schedule|the schedule)",
            r"(what|any)(thing)? happening today",
            r"today's (schedule|events|calendar)"
        ],
        Intent.CONTROL_DEVICE: [
            r"turn (on|off) (the )?(.+)",
            r"(switch|toggle) (the )?(.+)",
            r"(dim|brighten) (the )?(.+)"
        ],
        Intent.SET_THERMOSTAT: [
            r"set (the )?(temperature|thermostat|heat|ac|air) to (\d+)",
            r"(make it|turn it) (warmer|cooler|hotter|colder)",
            r"(\d+) degrees"
        ],
        Intent.CHECK_BALANCE: [
            r"(what('s| is)|check) my (balance|money|allowance)",
            r"how much (money |allowance )?(do i have|have i (got|earned))"
        ],
        Intent.CHECK_SAVINGS_GOAL: [
            r"how (much |far )?(am i|close) (to|from) (my )?goal",
            r"(check |what's )?my savings",
            r"(nintendo|switch|bike|goal) progress"
        ]
    }

    def __init__(self, organization: str, speaker_member: str):
        self.organization = organization
        self.speaker_member = speaker_member
        self.context = ConversationContext()

    def detect_intent(self, text: str) -> Tuple[Intent, Dict[str, any], float]:
        """
        Detect intent from text.
        Returns: (intent, entities, confidence)
        """
        text = text.lower().strip()

        # First try pattern matching for high-confidence matches
        intent, entities, confidence = self._pattern_match(text)

        if confidence >= 0.8:
            return intent, entities, confidence

        # Fall back to LLM-based intent detection
        return self._llm_detect(text)

    def _pattern_match(self, text: str) -> Tuple[Intent, Dict, float]:
        """Pattern-based intent matching."""
        import re

        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities = self._extract_entities_from_match(intent, match, text)
                    return intent, entities, 0.9

        return Intent.UNKNOWN, {}, 0.0

    def _extract_entities_from_match(
        self,
        intent: Intent,
        match,
        text: str
    ) -> Dict[str, any]:
        """Extract entities from regex match."""
        entities = {}

        if intent == Intent.WHERE_IS_PERSON:
            # Extract person name
            groups = match.groups()
            person_name = groups[-1] if groups else None
            if person_name:
                entities["person"] = self._resolve_person(person_name)

        elif intent == Intent.COMPLETE_CHORE:
            # Extract chore name
            groups = match.groups()
            chore_name = groups[-2] if len(groups) >= 2 else None
            if chore_name:
                entities["chore"] = self._resolve_chore(chore_name)

        elif intent == Intent.CONTROL_DEVICE:
            # Extract device and action
            groups = match.groups()
            entities["action"] = groups[0] if groups else "toggle"
            entities["device"] = groups[-1] if groups else None

        elif intent == Intent.SET_THERMOSTAT:
            # Extract temperature
            import re
            temp_match = re.search(r'(\d+)', text)
            if temp_match:
                entities["temperature"] = int(temp_match.group(1))

        return entities

    def _resolve_person(self, name: str) -> Optional[str]:
        """Resolve person name to family member ID."""
        name = name.lower()

        # Check for relationship terms
        relationship_map = {
            "mom": self._get_member_by_role("Parent", "Female"),
            "mother": self._get_member_by_role("Parent", "Female"),
            "dad": self._get_member_by_role("Parent", "Male"),
            "father": self._get_member_by_role("Parent", "Male"),
            "grandma": self._get_member_by_role("Grandparent", "Female"),
            "grandpa": self._get_member_by_role("Grandparent", "Male"),
        }

        if name in relationship_map:
            return relationship_map[name]

        # Search by first name or nickname
        member = frappe.db.get_value(
            "Family Member",
            {
                "organization": self.organization,
                "status": "Active"
            },
            "name",
            filters=[
                ["first_name", "like", f"%{name}%"],
                ["nickname", "like", f"%{name}%"]
            ],
            or_filters=True
        )

        return member

    def _get_member_by_role(self, role: str, gender: str = None) -> Optional[str]:
        """Get family member by role and optionally gender."""
        filters = {
            "organization": self.organization,
            "family_role": role,
            "status": "Active"
        }
        if gender:
            filters["gender"] = gender

        return frappe.db.get_value("Family Member", filters, "name")

    def _resolve_chore(self, chore_text: str) -> Optional[str]:
        """Resolve chore description to chore assignment ID."""
        # Find matching chore for this speaker
        chores = frappe.get_all(
            "Chore Assignment",
            filters={
                "assigned_to": self.speaker_member,
                "status": ["in", ["Pending", "In Progress"]],
                "due_date": frappe.utils.today()
            },
            fields=["name", "chore_template"]
        )

        for chore in chores:
            template = frappe.get_doc("Chore Template", chore.chore_template)
            if chore_text.lower() in template.chore_name.lower():
                return chore.name

        return None

    def _llm_detect(self, text: str) -> Tuple[Intent, Dict, float]:
        """Use LLM for intent detection when pattern matching fails."""
        from dartwing_family.voice.ai import FamilyAI

        ai = FamilyAI(self.organization)
        result = ai.detect_intent(text, self.context.get_recent_context())

        try:
            intent = Intent[result["intent"].upper()]
        except KeyError:
            intent = Intent.UNKNOWN

        return intent, result.get("entities", {}), result.get("confidence", 0.5)


class ConversationContext:
    """Manages conversation context for multi-turn dialogs."""

    def __init__(self):
        self.history: List[dict] = []
        self.current_topic: Optional[str] = None
        self.pending_entities: Dict[str, any] = {}
        self.max_history = 10

    def add_turn(self, user_input: str, intent: Intent, response: str):
        """Add a conversation turn to history."""
        self.history.append({
            "user": user_input,
            "intent": intent.value,
            "response": response,
            "timestamp": frappe.utils.now_datetime()
        })

        # Trim old history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_recent_context(self, turns: int = 3) -> List[dict]:
        """Get recent conversation turns for context."""
        return self.history[-turns:] if self.history else []

    def set_pending_entity(self, key: str, value: any):
        """Store an entity for follow-up questions."""
        self.pending_entities[key] = value

    def get_pending_entity(self, key: str) -> Optional[any]:
        """Retrieve a pending entity."""
        return self.pending_entities.get(key)

    def clear_pending(self):
        """Clear pending entities after resolution."""
        self.pending_entities.clear()
```

## 6.4 Child Safety Filter

```python
# dartwing_family/voice/safety/child_filter.py

import frappe
from typing import Dict, List, Optional, Tuple
from enum import Enum

class ContentCategory(Enum):
    SAFE = "safe"
    REDIRECT_TO_PARENT = "redirect_to_parent"
    AGE_INAPPROPRIATE = "age_inappropriate"
    EDUCATIONAL = "educational"
    SENSITIVE = "sensitive"

class ChildSafetyFilter:
    """Filters and adapts responses for child-appropriate content."""

    # Topics that should be redirected to parents
    PARENT_REDIRECT_TOPICS = [
        "adult content",
        "violence",
        "drugs",
        "alcohol",
        "dating",
        "relationships",
        "money management",  # For young children
        "medical decisions",
        "family conflicts"
    ]

    # Topics requiring gentle, age-appropriate handling
    SENSITIVE_TOPICS = [
        "death",
        "illness",
        "divorce",
        "moving",
        "pets dying",
        "scary things",
        "nightmares"
    ]

    # Educational topics that should be explained at age level
    EDUCATIONAL_TOPICS = [
        "science",
        "math",
        "history",
        "geography",
        "animals",
        "space",
        "nature"
    ]

    def __init__(self, speaker_age: int, speaker_member: str):
        self.speaker_age = speaker_age
        self.speaker_member = speaker_member
        self.age_category = self._get_age_category()

    def _get_age_category(self) -> str:
        if self.speaker_age < 6:
            return "toddler"
        elif self.speaker_age < 10:
            return "young_child"
        elif self.speaker_age < 13:
            return "tween"
        elif self.speaker_age < 16:
            return "young_teen"
        elif self.speaker_age < 18:
            return "older_teen"
        else:
            return "adult"

    def filter_query(self, query: str) -> Tuple[ContentCategory, Optional[str]]:
        """
        Analyze query and determine how to handle it.
        Returns: (category, redirect_message)
        """
        query_lower = query.lower()

        # Check for parent redirect topics
        for topic in self.PARENT_REDIRECT_TOPICS:
            if topic in query_lower:
                if self.age_category in ["toddler", "young_child", "tween"]:
                    return (
                        ContentCategory.REDIRECT_TO_PARENT,
                        f"That's a great question! Let's ask Mom or Dad about that together."
                    )

        # Check for sensitive topics
        for topic in self.SENSITIVE_TOPICS:
            if topic in query_lower:
                return (ContentCategory.SENSITIVE, None)

        # Check for educational topics
        for topic in self.EDUCATIONAL_TOPICS:
            if topic in query_lower:
                return (ContentCategory.EDUCATIONAL, None)

        return (ContentCategory.SAFE, None)

    def adapt_response(
        self,
        response: str,
        category: ContentCategory
    ) -> str:
        """Adapt response text for the child's age level."""
        if self.age_category == "adult":
            return response

        if category == ContentCategory.SENSITIVE:
            return self._adapt_sensitive_response(response)
        elif category == ContentCategory.EDUCATIONAL:
            return self._adapt_educational_response(response)
        else:
            return self._simplify_language(response)

    def _adapt_sensitive_response(self, response: str) -> str:
        """Adapt sensitive topic responses to be gentle and supportive."""
        # Add reassuring language
        prefix = ""
        suffix = ""

        if self.age_category in ["toddler", "young_child"]:
            prefix = "I understand that can feel confusing. "
            suffix = " Would you like to talk to Mom or Dad about how you're feeling?"
        elif self.age_category in ["tween", "young_teen"]:
            prefix = "That's a thoughtful question. "
            suffix = " If you want to talk more about this, your parents are always there for you."

        return prefix + self._simplify_language(response) + suffix

    def _adapt_educational_response(self, response: str) -> str:
        """Adapt educational content to age level."""
        # Simplify based on age
        simplified = self._simplify_language(response)

        # Add engagement for younger kids
        if self.age_category in ["toddler", "young_child"]:
            simplified += " Isn't that cool? Would you like to learn more?"

        return simplified

    def _simplify_language(self, text: str) -> str:
        """Simplify language complexity based on age."""
        if self.age_category == "adult":
            return text

        # For younger children, use simpler vocabulary
        if self.age_category in ["toddler", "young_child"]:
            # Replace complex words with simpler alternatives
            replacements = {
                "approximately": "about",
                "consequently": "so",
                "furthermore": "also",
                "nevertheless": "but",
                "subsequently": "then",
                "utilize": "use",
                "terminate": "end",
                "commence": "start",
                "obtain": "get",
                "sufficient": "enough"
            }

            for complex_word, simple_word in replacements.items():
                text = text.replace(complex_word, simple_word)
                text = text.replace(complex_word.capitalize(), simple_word.capitalize())

            # Shorten long sentences
            sentences = text.split(". ")
            shortened = []
            for sentence in sentences:
                if len(sentence.split()) > 15:
                    # Break into smaller chunks
                    words = sentence.split()
                    mid = len(words) // 2
                    shortened.append(" ".join(words[:mid]) + ".")
                    shortened.append(" ".join(words[mid:]))
                else:
                    shortened.append(sentence)

            text = ". ".join(shortened)

        return text

    def get_character_response_style(self, character: str) -> Dict[str, any]:
        """Get response style parameters for AI characters."""
        styles = {
            "buddy": {
                "personality": "friendly robot",
                "speech_patterns": ["beep boop", "processing", "computing"],
                "enthusiasm_level": "high",
                "use_simple_language": True,
                "add_encouragement": True
            },
            "sparkle": {
                "personality": "magical fairy",
                "speech_patterns": ["sprinkle of magic", "fairy dust", "enchanting"],
                "enthusiasm_level": "high",
                "use_simple_language": True,
                "add_encouragement": True
            },
            "max": {
                "personality": "wise dog",
                "speech_patterns": ["good boy energy", "loyal", "brave"],
                "enthusiasm_level": "medium",
                "use_simple_language": True,
                "add_encouragement": True
            },
            "captain": {
                "personality": "superhero mentor",
                "speech_patterns": ["hero", "brave", "mission"],
                "enthusiasm_level": "high",
                "use_simple_language": True,
                "add_encouragement": True
            },
            "nova": {
                "personality": "space explorer",
                "speech_patterns": ["galaxy", "stars", "adventure"],
                "enthusiasm_level": "high",
                "use_simple_language": True,
                "add_encouragement": True
            }
        }

        return styles.get(character.lower(), {
            "personality": "friendly assistant",
            "enthusiasm_level": "medium",
            "use_simple_language": self.age_category in ["toddler", "young_child"],
            "add_encouragement": True
        })
```

## 6.5 Family Knowledge Base

```python
# dartwing_family/voice/knowledge/family_kb.py

import frappe
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class FamilyKnowledgeBase:
    """Provides family-specific knowledge for the voice assistant."""

    def __init__(self, organization: str):
        self.organization = organization
        self._cache = {}
        self._cache_ttl = timedelta(minutes=5)
        self._cache_time = {}

    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached value if still valid."""
        if key in self._cache:
            if datetime.now() - self._cache_time[key] < self._cache_ttl:
                return self._cache[key]
        return None

    def _set_cached(self, key: str, value: Any):
        """Set cached value."""
        self._cache[key] = value
        self._cache_time[key] = datetime.now()

    # ─── FAMILY INFORMATION ─────────────────────────────────────────────

    def get_family_members(self) -> List[dict]:
        """Get all family members."""
        cached = self._get_cached("family_members")
        if cached:
            return cached

        members = frappe.get_all(
            "Family Member",
            filters={"organization": self.organization, "status": "Active"},
            fields=[
                "name", "first_name", "nickname", "family_role",
                "age", "age_category", "is_minor"
            ]
        )

        self._set_cached("family_members", members)
        return members

    def get_member_by_name(self, name: str) -> Optional[dict]:
        """Find family member by name or nickname."""
        members = self.get_family_members()
        name_lower = name.lower()

        for member in members:
            if (member["first_name"].lower() == name_lower or
                (member["nickname"] and member["nickname"].lower() == name_lower)):
                return member

        return None

    def who_is_home(self) -> List[dict]:
        """Get family members currently at home."""
        home_geofence = frappe.get_value(
            "Family Geofence",
            {"organization": self.organization, "location_type": "Home"},
            "name"
        )

        if not home_geofence:
            return []

        # Get recent locations within home geofence
        # This would check against geofence coordinates
        return []  # Implementation depends on location tracking

    # ─── CALENDAR INFORMATION ───────────────────────────────────────────

    def get_today_events(self, member_id: str = None) -> List[dict]:
        """Get today's calendar events."""
        filters = {
            "organization": self.organization,
            "start_datetime": [">=", frappe.utils.today()],
            "start_datetime": ["<", frappe.utils.add_days(frappe.utils.today(), 1)]
        }

        events = frappe.get_all(
            "Family Calendar Event",
            filters=filters,
            fields=[
                "name", "title", "start_datetime", "end_datetime",
                "location", "primary_person", "event_type"
            ],
            order_by="start_datetime asc"
        )

        if member_id:
            # Filter to events involving this member
            events = [
                e for e in events
                if e["primary_person"] == member_id or
                self._is_attendee(e["name"], member_id)
            ]

        return events

    def get_upcoming_event(self, event_name: str) -> Optional[dict]:
        """Find upcoming event by name."""
        events = frappe.get_all(
            "Family Calendar Event",
            filters={
                "organization": self.organization,
                "title": ["like", f"%{event_name}%"],
                "start_datetime": [">=", frappe.utils.now_datetime()]
            },
            fields=["name", "title", "start_datetime", "location"],
            order_by="start_datetime asc",
            limit=1
        )

        return events[0] if events else None

    def _is_attendee(self, event_id: str, member_id: str) -> bool:
        """Check if member is an attendee of event."""
        return frappe.db.exists(
            "Family Calendar Event Attendee",
            {"parent": event_id, "family_member": member_id}
        )

    # ─── CHORE INFORMATION ──────────────────────────────────────────────

    def get_member_chores(self, member_id: str, date: str = None) -> List[dict]:
        """Get chores for a family member."""
        if not date:
            date = frappe.utils.today()

        chores = frappe.get_all(
            "Chore Assignment",
            filters={
                "assigned_to": member_id,
                "due_date": date
            },
            fields=["name", "chore_template", "status", "due_time"]
        )

        # Add chore template details
        for chore in chores:
            template = frappe.get_doc("Chore Template", chore["chore_template"])
            chore["chore_name"] = template.chore_name
            chore["points"] = template.base_points
            chore["money"] = template.base_money

        return chores

    def get_chore_earnings(self, member_id: str, period: str = "week") -> dict:
        """Get chore earnings for a period."""
        if period == "week":
            start_date = frappe.utils.add_days(frappe.utils.today(), -7)
        elif period == "month":
            start_date = frappe.utils.add_days(frappe.utils.today(), -30)
        else:
            start_date = frappe.utils.today()

        earnings = frappe.db.sql("""
            SELECT
                SUM(points_earned) as total_points,
                SUM(money_earned) as total_money,
                COUNT(*) as chores_completed
            FROM `tabChore Assignment`
            WHERE assigned_to = %s
            AND status = 'Verified'
            AND due_date >= %s
        """, (member_id, start_date), as_dict=True)

        return earnings[0] if earnings else {
            "total_points": 0,
            "total_money": 0,
            "chores_completed": 0
        }

    # ─── HOUSE RULES ────────────────────────────────────────────────────

    def get_house_rules(self) -> List[dict]:
        """Get family house rules."""
        return frappe.get_all(
            "Family House Rule",
            filters={"organization": self.organization},
            fields=["rule_name", "description", "applies_to"]
        )

    def get_bedtime(self, member_id: str) -> Optional[str]:
        """Get bedtime rule for a member."""
        member = frappe.get_doc("Family Member", member_id)

        # Check screen time profile for bedtime
        profile = frappe.get_value(
            "Screen Time Profile",
            {"family_member": member_id},
            ["allowed_end_time"]
        )

        return profile

    # ─── RECIPES ────────────────────────────────────────────────────────

    def get_family_recipe(self, recipe_name: str) -> Optional[dict]:
        """Get a family recipe by name."""
        recipe = frappe.get_value(
            "Family Recipe",
            {
                "organization": self.organization,
                "recipe_name": ["like", f"%{recipe_name}%"]
            },
            ["name", "recipe_name", "instructions", "ingredients", "source"],
            as_dict=True
        )

        return recipe

    def get_grandma_recipes(self) -> List[dict]:
        """Get recipes from grandparents."""
        return frappe.get_all(
            "Family Recipe",
            filters={
                "organization": self.organization,
                "source": ["like", "%grandma%"]
            },
            fields=["recipe_name", "description"]
        )

    # ─── EMERGENCY INFORMATION ──────────────────────────────────────────

    def get_emergency_contacts(self) -> List[dict]:
        """Get emergency contacts."""
        return frappe.get_all(
            "Emergency Contact",
            filters={"organization": self.organization},
            fields=["contact_name", "phone_number", "relationship", "priority"],
            order_by="priority asc"
        )

    def get_doctor_info(self, member_id: str = None) -> dict:
        """Get doctor/healthcare information."""
        if member_id:
            profile = frappe.get_doc(
                "Family Medical Profile",
                {"family_member": member_id}
            )
            return {
                "primary_doctor": profile.primary_care_physician,
                "preferred_hospital": profile.preferred_hospital,
                "preferred_pharmacy": profile.preferred_pharmacy
            }

        # Return family's default healthcare info
        return {}
```

## 6.6 Response Generation

```python
# dartwing_family/voice/response/generator.py

import frappe
from typing import Dict, Optional
from dartwing_family.voice.nlu.intent_detection import Intent, IntentCategory
from dartwing_family.voice.knowledge.family_kb import FamilyKnowledgeBase
from dartwing_family.voice.safety.child_filter import ChildSafetyFilter, ContentCategory

class ResponseGenerator:
    """Generates natural language responses for voice assistant."""

    def __init__(
        self,
        organization: str,
        speaker_member: str,
        voice_character: str = None
    ):
        self.organization = organization
        self.speaker_member = speaker_member
        self.voice_character = voice_character

        self.kb = FamilyKnowledgeBase(organization)

        # Get speaker info
        member = frappe.get_doc("Family Member", speaker_member)
        self.speaker_age = member.age
        self.speaker_name = member.first_name

        self.safety_filter = ChildSafetyFilter(self.speaker_age, speaker_member)

    def generate_response(
        self,
        intent: Intent,
        entities: Dict,
        original_query: str
    ) -> str:
        """Generate response based on intent and entities."""

        # Check safety filter first
        category, redirect_msg = self.safety_filter.filter_query(original_query)

        if category == ContentCategory.REDIRECT_TO_PARENT:
            return redirect_msg

        # Route to appropriate handler
        handler = self._get_handler(intent)
        if handler:
            response = handler(entities)
        else:
            response = self._handle_unknown(original_query)

        # Adapt response for child if needed
        response = self.safety_filter.adapt_response(response, category)

        # Apply character personality if set
        if self.voice_character:
            response = self._apply_character_style(response)

        return response

    def _get_handler(self, intent: Intent):
        """Get handler function for intent."""
        handlers = {
            Intent.GET_MY_CHORES: self._handle_get_chores,
            Intent.COMPLETE_CHORE: self._handle_complete_chore,
            Intent.WHERE_IS_PERSON: self._handle_where_is,
            Intent.WHO_IS_HOME: self._handle_who_is_home,
            Intent.GET_TODAY_SCHEDULE: self._handle_today_schedule,
            Intent.CONTROL_DEVICE: self._handle_control_device,
            Intent.SET_THERMOSTAT: self._handle_set_thermostat,
            Intent.CHECK_BALANCE: self._handle_check_balance,
            Intent.CHECK_SAVINGS_GOAL: self._handle_savings_goal,
            Intent.HELP: self._handle_help,
        }
        return handlers.get(intent)

    # ─── INTENT HANDLERS ────────────────────────────────────────────────

    def _handle_get_chores(self, entities: Dict) -> str:
        """Handle request for chores."""
        chores = self.kb.get_member_chores(self.speaker_member)

        if not chores:
            return f"Great news {self.speaker_name}! You don't have any chores right now."

        pending = [c for c in chores if c["status"] == "Pending"]
        completed = [c for c in chores if c["status"] in ["Completed", "Verified"]]

        if not pending:
            return (
                f"Awesome job {self.speaker_name}! You've finished all your chores today. "
                f"You completed {len(completed)} chores!"
            )

        chore_list = ", ".join([c["chore_name"] for c in pending])
        points = sum(c["points"] for c in pending)
        money = sum(c["money"] for c in pending)

        response = f"You have {len(pending)} chores to do: {chore_list}. "
        response += f"You can earn {points} points and ${money:.2f}!"

        return response

    def _handle_complete_chore(self, entities: Dict) -> str:
        """Handle chore completion request."""
        chore_id = entities.get("chore")

        if not chore_id:
            return "Which chore did you finish? Try saying 'I finished cleaning my room.'"

        try:
            chore = frappe.get_doc("Chore Assignment", chore_id)
            result = chore.mark_complete()

            if result.get("status") == "success":
                rewards = result.get("rewards", {})
                return (
                    f"Great job {self.speaker_name}! I've marked that as done. "
                    f"You earned {rewards.get('points', 0)} points and "
                    f"${rewards.get('money', 0):.2f}!"
                )
            else:
                return "I couldn't mark that chore as complete. Can you try again?"

        except Exception as e:
            return "I had trouble with that. Please try completing it in the app."

    def _handle_where_is(self, entities: Dict) -> str:
        """Handle location query."""
        person = entities.get("person")

        if not person:
            return "Who are you looking for?"

        # Check permission to view location
        from dartwing_family.permissions.permission_engine import FamilyPermissionEngine
        engine = FamilyPermissionEngine(
            frappe.get_value("Family Member", self.speaker_member, "user_account")
        )

        if not engine.can_view_member_location(person):
            return "I'm not able to share that location right now."

        # Get location
        location = frappe.get_last_doc(
            "Location History",
            filters={"family_member": person}
        )

        if not location:
            member = frappe.get_doc("Family Member", person)
            return f"I don't have a recent location for {member.first_name}."

        # Check if at known location
        known_location = self._get_known_location_name(
            location.latitude,
            location.longitude
        )

        member = frappe.get_doc("Family Member", person)
        if known_location:
            return f"{member.first_name} is at {known_location}."
        else:
            return f"{member.first_name}'s location was last updated {self._time_ago(location.timestamp)}."

    def _handle_who_is_home(self, entities: Dict) -> str:
        """Handle query about who is home."""
        home_members = self.kb.who_is_home()

        if not home_members:
            return "I'm not sure who's home right now. Let me check the app for you."

        names = [m["first_name"] for m in home_members]

        if len(names) == 1:
            return f"Just {names[0]} is home right now."
        elif len(names) == 2:
            return f"{names[0]} and {names[1]} are home."
        else:
            return f"{', '.join(names[:-1])}, and {names[-1]} are all home."

    def _handle_today_schedule(self, entities: Dict) -> str:
        """Handle schedule query."""
        events = self.kb.get_today_events(self.speaker_member)

        if not events:
            return "You don't have any events scheduled for today!"

        response = "Here's what's happening today: "

        for i, event in enumerate(events[:5]):  # Limit to 5 events
            time = frappe.utils.format_datetime(
                event["start_datetime"],
                "h:mm a"
            )
            response += f"{event['title']} at {time}"
            if event.get("location"):
                response += f" at {event['location']}"
            response += ". "

        if len(events) > 5:
            response += f"Plus {len(events) - 5} more events."

        return response

    def _handle_control_device(self, entities: Dict) -> str:
        """Handle home device control."""
        device = entities.get("device")
        action = entities.get("action", "toggle")

        if not device:
            return "Which device should I control?"

        # Check if child can control this device
        if self.speaker_age < 18:
            restricted = self._is_restricted_device(device)
            if restricted:
                return f"You'll need to ask a parent to control the {device}."

        try:
            from dartwing_family.integrations.registry import AdapterRegistry

            adapter = AdapterRegistry.get_adapter("home_assistant", self.organization)

            if action in ["on", "turn on"]:
                adapter.turn_on(device)
                return f"I've turned on the {device}."
            elif action in ["off", "turn off"]:
                adapter.turn_off(device)
                return f"I've turned off the {device}."
            else:
                return f"I've toggled the {device}."

        except Exception as e:
            return f"I couldn't control the {device}. Please try the app."

    def _handle_set_thermostat(self, entities: Dict) -> str:
        """Handle thermostat control."""
        temperature = entities.get("temperature")

        if not temperature:
            return "What temperature would you like?"

        # Check if child can adjust thermostat
        if self.speaker_age < 18:
            # Children can only adjust ±3 degrees
            current_temp = self._get_current_thermostat()
            if abs(temperature - current_temp) > 3:
                return (
                    f"You can only change the temperature by up to 3 degrees. "
                    f"Ask a parent if you need a bigger change."
                )

        try:
            from dartwing_family.integrations.registry import AdapterRegistry
            adapter = AdapterRegistry.get_adapter("home_assistant", self.organization)
            adapter.set_thermostat("climate.main", temperature)
            return f"I've set the temperature to {temperature} degrees."
        except Exception:
            return "I couldn't change the thermostat. Please try the app."

    def _handle_check_balance(self, entities: Dict) -> str:
        """Handle balance check request."""
        # Get current balance
        balance = frappe.db.get_value(
            "Allowance Balance",
            {"family_member": self.speaker_member},
            "current_balance"
        ) or 0

        # Get this week's earnings
        earnings = self.kb.get_chore_earnings(self.speaker_member, "week")

        response = f"You have ${balance:.2f} in your piggy bank. "

        if earnings["total_money"] > 0:
            response += f"This week you've earned ${earnings['total_money']:.2f} from chores!"

        return response

    def _handle_savings_goal(self, entities: Dict) -> str:
        """Handle savings goal query."""
        goal = frappe.get_value(
            "Savings Goal",
            {
                "owner": self.speaker_member,
                "status": "Active"
            },
            ["goal_name", "target_amount", "current_amount", "target_date"],
            as_dict=True
        )

        if not goal:
            return "You don't have a savings goal set up yet. Want to create one?"

        percent = (goal["current_amount"] / goal["target_amount"]) * 100
        remaining = goal["target_amount"] - goal["current_amount"]

        return (
            f"You're {percent:.0f}% of the way to your {goal['goal_name']}! "
            f"You have ${goal['current_amount']:.2f} saved, "
            f"and need ${remaining:.2f} more to reach your goal."
        )

    def _handle_help(self, entities: Dict) -> str:
        """Handle help request."""
        return (
            f"Hi {self.speaker_name}! I can help you with lots of things. "
            "Try asking me: What are my chores? Where is Mom? "
            "What's happening today? How much money do I have? "
            "Or you can tell me when you finish a chore!"
        )

    def _handle_unknown(self, query: str) -> str:
        """Handle unknown intent."""
        return (
            f"I'm not sure how to help with that, {self.speaker_name}. "
            "Try asking about your chores, schedule, or family location!"
        )

    # ─── HELPER METHODS ─────────────────────────────────────────────────

    def _apply_character_style(self, response: str) -> str:
        """Apply voice character personality to response."""
        style = self.safety_filter.get_character_response_style(self.voice_character)

        # Add character-specific phrases
        if self.voice_character == "buddy":
            response = "Beep boop! " + response
        elif self.voice_character == "sparkle":
            response = "✨ " + response + " Magical!"
        elif self.voice_character == "captain":
            response = "Great work, hero! " + response

        return response

    def _get_known_location_name(self, lat: float, lon: float) -> Optional[str]:
        """Get name of known location from coordinates."""
        geofences = frappe.get_all(
            "Family Geofence",
            filters={"organization": self.organization},
            fields=["name", "latitude", "longitude", "radius_meters"]
        )

        for gf in geofences:
            distance = self._haversine_distance(lat, lon, gf["latitude"], gf["longitude"])
            if distance <= gf["radius_meters"]:
                return gf["name"]

        return None

    def _haversine_distance(self, lat1, lon1, lat2, lon2) -> float:
        """Calculate distance between two coordinates in meters."""
        from math import radians, cos, sin, sqrt, atan2

        R = 6371000  # Earth's radius in meters

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def _time_ago(self, timestamp) -> str:
        """Convert timestamp to human-readable time ago."""
        now = frappe.utils.now_datetime()
        diff = now - timestamp

        if diff.seconds < 60:
            return "just now"
        elif diff.seconds < 3600:
            mins = diff.seconds // 60
            return f"{mins} minute{'s' if mins > 1 else ''} ago"
        elif diff.seconds < 86400:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"

    def _is_restricted_device(self, device: str) -> bool:
        """Check if device is restricted for children."""
        restricted_keywords = ["lock", "alarm", "security", "garage"]
        return any(kw in device.lower() for kw in restricted_keywords)

    def _get_current_thermostat(self) -> int:
        """Get current thermostat temperature."""
        # Implementation depends on home automation integration
        return 72  # Default
```

## 6.7 Speech Services Integration

```python
# dartwing_family/voice/speech/speech_service.py

import frappe
from typing import Optional
import io

class SpeechService:
    """Unified speech service for STT and TTS."""

    def __init__(self, organization: str):
        self.organization = organization
        self.stt_provider = self._get_stt_provider()
        self.tts_provider = self._get_tts_provider()

    def _get_stt_provider(self):
        """Get configured STT provider."""
        provider = frappe.conf.get("stt_provider", "whisper")

        if provider == "whisper":
            return WhisperSTT()
        elif provider == "google":
            return GoogleSTT()
        else:
            return WhisperSTT()

    def _get_tts_provider(self):
        """Get configured TTS provider."""
        from dartwing_family.voice.providers import VoiceCloningProvider
        return VoiceCloningProvider()

    def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Convert speech to text."""
        return self.stt_provider.transcribe(audio_data, language)

    def synthesize(
        self,
        text: str,
        voice_id: str,
        **kwargs
    ) -> bytes:
        """Convert text to speech with specified voice."""
        return self.tts_provider.synthesize_speech(text, voice_id, **kwargs)

    def get_preferred_voice(self, family_member: str) -> str:
        """Get preferred voice for a family member."""
        preference = frappe.get_value(
            "Family Voice Preference",
            {"family_member": family_member},
            "voice_profile"
        )

        if preference:
            profile = frappe.get_doc("Family Voice Profile", preference)
            return profile.voice_model_id

        # Default to standard voice
        return "standard_voice_v1"


class WhisperSTT:
    """OpenAI Whisper speech-to-text."""

    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=frappe.conf.get("openai_api_key"))

    def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Transcribe audio using Whisper."""
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.wav"

        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language
        )

        return response.text


class GoogleSTT:
    """Google Cloud speech-to-text."""

    def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Transcribe audio using Google Cloud."""
        from google.cloud import speech

        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=f"{language}-US",
            enable_automatic_punctuation=True
        )

        response = client.recognize(config=config, audio=audio)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript
```

## 6.8 Voice Assistant API

```python
# dartwing_family/api/voice_api.py

import frappe
from frappe import _

@frappe.whitelist()
def process_voice_command(
    audio_base64: str = None,
    text: str = None,
    voice_id: str = None
) -> dict:
    """
    Process a voice command and return audio response.

    Args:
        audio_base64: Base64 encoded audio input (if voice)
        text: Text input (if typed)
        voice_id: Preferred voice for response

    Returns:
        {
            "text": "Response text",
            "audio_base64": "Base64 encoded audio response",
            "intent": "detected_intent",
            "entities": {}
        }
    """
    from dartwing_family.voice.speech.speech_service import SpeechService
    from dartwing_family.voice.nlu.intent_detection import IntentDetector
    from dartwing_family.voice.response.generator import ResponseGenerator

    # Get current user's family member
    member = frappe.get_value(
        "Family Member",
        {"user_account": frappe.session.user},
        ["name", "organization", "first_name", "age"],
        as_dict=True
    )

    if not member:
        frappe.throw(_("User is not a family member"))

    speech_service = SpeechService(member.organization)

    # Convert audio to text if needed
    if audio_base64 and not text:
        import base64
        audio_data = base64.b64decode(audio_base64)
        text = speech_service.transcribe(audio_data)

    if not text:
        frappe.throw(_("No input provided"))

    # Detect intent
    intent_detector = IntentDetector(member.organization, member.name)
    intent, entities, confidence = intent_detector.detect_intent(text)

    # Generate response
    response_gen = ResponseGenerator(
        member.organization,
        member.name,
        voice_character=_get_voice_character(member.name, voice_id)
    )

    response_text = response_gen.generate_response(intent, entities, text)

    # Synthesize audio response
    voice = voice_id or speech_service.get_preferred_voice(member.name)
    audio_response = speech_service.synthesize(response_text, voice)

    import base64
    audio_base64_response = base64.b64encode(audio_response).decode()

    return {
        "text": response_text,
        "audio_base64": audio_base64_response,
        "intent": intent.value,
        "entities": entities,
        "confidence": confidence
    }


@frappe.whitelist()
def get_available_voices() -> list:
    """Get all available voices for the current user's family."""
    member = frappe.get_value(
        "Family Member",
        {"user_account": frappe.session.user},
        ["name", "organization"],
        as_dict=True
    )

    if not member:
        frappe.throw(_("User is not a family member"))

    from dartwing_family.voice.voice_profile import VoiceProfileManager
    manager = VoiceProfileManager(member.organization)

    return manager.get_available_voices(member.name)


@frappe.whitelist()
def set_voice_preference(voice_profile: str):
    """Set user's preferred voice."""
    member = frappe.get_value(
        "Family Member",
        {"user_account": frappe.session.user},
        "name"
    )

    if not member:
        frappe.throw(_("User is not a family member"))

    # Update or create preference
    existing = frappe.get_value(
        "Family Voice Preference",
        {"family_member": member}
    )

    if existing:
        frappe.db.set_value(
            "Family Voice Preference",
            existing,
            "voice_profile",
            voice_profile
        )
    else:
        frappe.get_doc({
            "doctype": "Family Voice Preference",
            "family_member": member,
            "voice_profile": voice_profile
        }).insert()

    return {"status": "success"}


def _get_voice_character(member_id: str, voice_id: str = None) -> Optional[str]:
    """Determine if using an AI character voice."""
    if voice_id and voice_id.startswith("ai_"):
        return voice_id.replace("ai_", "").replace("_v1", "")
    return None
```

---

_End of Section 6: Voice Assistant & AI Integration Architecture_

**Next Section:** Section 7 - Background Services & Scheduled Tasks

# Section 7: Background Services & Scheduled Tasks

## 7.1 Scheduler Architecture Overview

Dartwing Family uses Frappe's built-in scheduler with RQ (Redis Queue) for background job processing:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BACKGROUND SERVICES ARCHITECTURE                        │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         FRAPPE SCHEDULER                             │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Cron      │  │   Interval   │  │   One-Time   │              │    │
│  │  │    Jobs      │  │    Jobs      │  │    Jobs      │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • Daily 6AM  │  │ • Every 5min │  │ • Triggered  │              │    │
│  │  │ • Hourly     │  │ • Every hour │  │   by events  │              │    │
│  │  │ • Weekly     │  │              │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          REDIS QUEUE (RQ)                            │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Default    │  │    Short     │  │    Long      │              │    │
│  │  │   Queue      │  │    Queue     │  │    Queue     │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • General    │  │ • Notifs     │  │ • Sync jobs  │              │    │
│  │  │   tasks      │  │ • Quick ops  │  │ • Imports    │              │    │
│  │  │              │  │              │  │ • Reports    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         RQ WORKERS                                   │    │
│  │                                                                      │    │
│  │  Worker 1        Worker 2        Worker 3        Worker 4           │    │
│  │  (default)       (short)         (long)          (long)             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     FAMILY-SPECIFIC JOBS                             │    │
│  │                                                                      │    │
│  │  • Age Check & Transitions      • External Calendar Sync            │    │
│  │  • Chore Reminders              • Grade Data Sync                   │    │
│  │  • Allowance Processing         • Location History Cleanup          │    │
│  │  • Screen Time Enforcement      • Maintenance Reminders             │    │
│  │  • Geofence Monitoring          • Weather Automation                │    │
│  │  • Morning/Evening Briefings    • Backup & Archive                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 7.2 Scheduler Configuration

```python
# dartwing_family/hooks.py

scheduler_events = {
    # ─── DAILY JOBS (run once per day) ──────────────────────────────────
    "daily": [
        "dartwing_family.tasks.daily.daily_age_check",
        "dartwing_family.tasks.daily.process_recurring_chores",
        "dartwing_family.tasks.daily.calculate_daily_allowances",
        "dartwing_family.tasks.daily.cleanup_old_location_history",
        "dartwing_family.tasks.daily.generate_daily_reports",
        "dartwing_family.tasks.daily.check_maintenance_reminders",
        "dartwing_family.tasks.daily.sync_external_calendars",
    ],

    # ─── DAILY LONG (run once per day, can take longer) ─────────────────
    "daily_long": [
        "dartwing_family.tasks.daily.full_integration_sync",
        "dartwing_family.tasks.daily.backup_family_data",
    ],

    # ─── HOURLY JOBS ────────────────────────────────────────────────────
    "hourly": [
        "dartwing_family.tasks.hourly.sync_location_data",
        "dartwing_family.tasks.hourly.check_geofence_alerts",
        "dartwing_family.tasks.hourly.process_pending_approvals",
        "dartwing_family.tasks.hourly.check_overdue_chores",
        "dartwing_family.tasks.hourly.sync_grade_data",
    ],

    # ─── HOURLY LONG ────────────────────────────────────────────────────
    "hourly_long": [
        "dartwing_family.tasks.hourly.sync_retail_orders",
    ],

    # ─── WEEKLY JOBS ────────────────────────────────────────────────────
    "weekly": [
        "dartwing_family.tasks.weekly.generate_weekly_summary",
        "dartwing_family.tasks.weekly.process_weekly_allowances",
        "dartwing_family.tasks.weekly.calculate_driving_scores",
        "dartwing_family.tasks.weekly.archive_old_data",
    ],

    # ─── MONTHLY JOBS ───────────────────────────────────────────────────
    "monthly": [
        "dartwing_family.tasks.monthly.generate_monthly_report",
        "dartwing_family.tasks.monthly.process_savings_matching",
        "dartwing_family.tasks.monthly.review_permission_profiles",
    ],

    # ─── CRON JOBS (specific times) ─────────────────────────────────────
    "cron": {
        # Morning briefing at 6 AM
        "0 6 * * *": [
            "dartwing_family.tasks.cron.morning_briefing"
        ],
        # Evening summary at 8 PM
        "0 20 * * *": [
            "dartwing_family.tasks.cron.evening_summary"
        ],
        # Check screen time every 5 minutes
        "*/5 * * * *": [
            "dartwing_family.tasks.cron.check_screen_time_limits"
        ],
        # Sync weather data every 30 minutes
        "*/30 * * * *": [
            "dartwing_family.tasks.cron.sync_weather_data"
        ],
        # Process custody handoffs at midnight
        "0 0 * * *": [
            "dartwing_family.tasks.cron.process_custody_handoffs"
        ],
        # Birthday check at 12:01 AM
        "1 0 * * *": [
            "dartwing_family.tasks.cron.check_birthdays"
        ]
    }
}
```

## 7.3 Daily Tasks

### Age Check & Transitions

```python
# dartwing_family/tasks/daily/age_check.py

import frappe
from frappe.utils import getdate, today, date_diff
from datetime import date

def daily_age_check():
    """
    Daily job to:
    1. Recalculate ages for all family members
    2. Trigger age milestone transitions
    3. Update permission profiles
    """
    frappe.logger().info("Starting daily age check")

    # Get all active family members
    members = frappe.get_all(
        "Family Member",
        filters={"status": "Active"},
        fields=["name", "date_of_birth", "age", "age_category", "organization"]
    )

    transitions = []

    for member in members:
        old_age = member.age
        new_age = calculate_age(member.date_of_birth)

        if new_age != old_age:
            # Update member
            frappe.db.set_value(
                "Family Member",
                member.name,
                {
                    "age": new_age,
                    "age_category": get_age_category(new_age),
                    "is_minor": new_age < 18,
                    "is_coppa_protected": new_age < 13
                }
            )

            # Check for milestone transitions
            transition = check_milestone_transition(member.name, old_age, new_age)
            if transition:
                transitions.append(transition)

    # Process transitions
    for transition in transitions:
        process_age_transition(transition)

    frappe.db.commit()
    frappe.logger().info(f"Age check complete. {len(transitions)} transitions processed.")


def calculate_age(dob) -> int:
    """Calculate age from date of birth."""
    if not dob:
        return 0

    dob = getdate(dob)
    today_date = getdate(today())

    age = today_date.year - dob.year

    # Adjust if birthday hasn't occurred this year
    if (today_date.month, today_date.day) < (dob.month, dob.day):
        age -= 1

    return age


def get_age_category(age: int) -> str:
    """Determine age category."""
    if age < 1:
        return "Infant"
    elif age < 3:
        return "Toddler"
    elif age < 13:
        return "Child"
    elif age < 16:
        return "Tween"
    elif age < 18:
        return "Teen"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"


def check_milestone_transition(member_id: str, old_age: int, new_age: int) -> dict:
    """Check for significant age milestones."""
    milestones = [
        (6, "app_access"),      # Can now use kid mode
        (13, "coppa_exit"),     # No longer COPPA protected
        (16, "teen_privileges"), # More independence
        (18, "adult"),          # Full adult access
    ]

    for milestone_age, milestone_type in milestones:
        if old_age < milestone_age <= new_age:
            return {
                "member_id": member_id,
                "milestone_type": milestone_type,
                "new_age": new_age
            }

    return None


def process_age_transition(transition: dict):
    """Process an age milestone transition."""
    member = frappe.get_doc("Family Member", transition["member_id"])
    milestone = transition["milestone_type"]

    if milestone == "coppa_exit":
        # Turning 13 - exit COPPA protection
        member.permission_profile = "Tween 13-15"
        member.save()

        # Notify parents
        notify_parents(
            member,
            subject=f"🎂 {member.first_name} is now 13!",
            message=f"""
            {member.first_name} has turned 13 today!

            Their account permissions have been updated:
            - COPPA restrictions have been lifted
            - They now have access to more features
            - Some parental controls can now be adjusted

            Please review their settings in the app.
            """
        )

        # Log transition
        log_transition(member.name, "coppa_exit")

    elif milestone == "adult":
        # Turning 18 - full adult access
        member.permission_profile = "Adult"
        member.is_minor = 0
        member.save()

        # Notify the new adult
        if member.email:
            frappe.sendmail(
                recipients=[member.email],
                subject="🎉 Happy 18th Birthday! Your Dartwing Account is Now Independent",
                message=f"""
                Happy 18th Birthday, {member.first_name}!

                Your Dartwing Family account has been upgraded to full adult access.

                What's changed:
                - You now have full control over your privacy settings
                - Parental oversight has been removed
                - You can manage your own financial settings
                - Location sharing is now opt-in

                You can choose to stay connected with your family or
                convert to an independent account.

                Welcome to adulthood!
                """
            )

        log_transition(member.name, "adult")

    elif milestone == "teen_privileges":
        member.permission_profile = "Teen 16-17"
        member.save()

        notify_parents(
            member,
            subject=f"🚗 {member.first_name} has turned 16!",
            message=f"""
            {member.first_name} has turned 16!

            New privileges available:
            - Ghost mode (up to 2 hours)
            - Higher spending limits
            - Driver monitoring (if applicable)

            Review their settings in the app.
            """
        )

        log_transition(member.name, "teen_privileges")


def notify_parents(member, subject: str, message: str):
    """Notify all parents/guardians of a family member."""
    guardians = frappe.get_all(
        "Family Relationship",
        filters={
            "person_b": member.name,
            "is_legal_guardian": 1,
            "status": "Active"
        },
        fields=["person_a"]
    )

    for guardian in guardians:
        guardian_doc = frappe.get_doc("Family Member", guardian.person_a)
        if guardian_doc.email:
            frappe.sendmail(
                recipients=[guardian_doc.email],
                subject=subject,
                message=message
            )

        # Also send push notification
        frappe.publish_realtime(
            "family_notification",
            {
                "type": "age_transition",
                "title": subject,
                "message": message[:100] + "..."
            },
            user=guardian_doc.user_account
        )


def log_transition(member_id: str, transition_type: str):
    """Log age transition for audit."""
    frappe.get_doc({
        "doctype": "Family Audit Log",
        "action": f"age_transition_{transition_type}",
        "actor_member": member_id,
        "target_member": member_id,
        "timestamp": frappe.utils.now_datetime(),
        "details": frappe.as_json({
            "transition_type": transition_type,
            "automated": True
        })
    }).insert(ignore_permissions=True)
```

### Process Recurring Chores

```python
# dartwing_family/tasks/daily/recurring_chores.py

import frappe
from frappe.utils import today, add_days, getdate, get_weekday

def process_recurring_chores():
    """
    Daily job to create chore assignments from recurring schedules.
    """
    frappe.logger().info("Processing recurring chores")

    today_date = getdate(today())
    today_weekday = get_weekday(today_date)  # 0 = Monday

    # Get all active chore recurrences
    recurrences = frappe.get_all(
        "Chore Recurrence",
        filters={"status": "Active"},
        fields=[
            "name", "chore_template", "assigned_to", "organization",
            "frequency", "day_of_week", "day_of_month", "due_time",
            "last_created_date"
        ]
    )

    created_count = 0

    for recurrence in recurrences:
        should_create = False

        if recurrence.frequency == "Daily":
            should_create = True

        elif recurrence.frequency == "Weekly":
            # Check if today is the scheduled day
            scheduled_day = get_weekday_number(recurrence.day_of_week)
            should_create = (today_weekday == scheduled_day)

        elif recurrence.frequency == "Bi-Weekly":
            # Check if today is scheduled day and it's been 2 weeks
            scheduled_day = get_weekday_number(recurrence.day_of_week)
            if today_weekday == scheduled_day:
                if recurrence.last_created_date:
                    days_since = (today_date - getdate(recurrence.last_created_date)).days
                    should_create = (days_since >= 14)
                else:
                    should_create = True

        elif recurrence.frequency == "Monthly":
            should_create = (today_date.day == recurrence.day_of_month)

        # Create the assignment if scheduled
        if should_create:
            # Check if already exists for today
            existing = frappe.db.exists(
                "Chore Assignment",
                {
                    "chore_template": recurrence.chore_template,
                    "assigned_to": recurrence.assigned_to,
                    "due_date": today_date
                }
            )

            if not existing:
                create_chore_assignment(recurrence, today_date)
                created_count += 1

                # Update last created date
                frappe.db.set_value(
                    "Chore Recurrence",
                    recurrence.name,
                    "last_created_date",
                    today_date
                )

    frappe.db.commit()
    frappe.logger().info(f"Created {created_count} recurring chore assignments")


def create_chore_assignment(recurrence: dict, date) -> str:
    """Create a chore assignment from recurrence."""
    assignment = frappe.get_doc({
        "doctype": "Chore Assignment",
        "chore_template": recurrence.chore_template,
        "assigned_to": recurrence.assigned_to,
        "assigned_by": None,  # System-assigned
        "due_date": date,
        "due_time": recurrence.due_time,
        "recurrence": recurrence.name,
        "status": "Pending",
        "organization": recurrence.organization
    })
    assignment.insert(ignore_permissions=True)

    # Send reminder notification
    send_chore_reminder(assignment)

    return assignment.name


def send_chore_reminder(assignment):
    """Send notification about new chore."""
    member = frappe.get_doc("Family Member", assignment.assigned_to)
    template = frappe.get_doc("Chore Template", assignment.chore_template)

    if member.user_account:
        frappe.publish_realtime(
            "chore_assigned",
            {
                "chore_name": template.chore_name,
                "due_time": str(assignment.due_time) if assignment.due_time else None,
                "points": template.base_points,
                "money": float(template.base_money or 0)
            },
            user=member.user_account
        )


def get_weekday_number(day_name: str) -> int:
    """Convert day name to number (0 = Monday)."""
    days = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    return days.get(day_name, 0)
```

### Allowance Processing

```python
# dartwing_family/tasks/daily/allowance.py

import frappe
from frappe.utils import today, getdate, get_first_day, get_last_day
from decimal import Decimal

def calculate_daily_allowances():
    """
    Daily job to:
    1. Process pending allowance payments
    2. Apply parent matching to savings
    3. Update balances
    """
    frappe.logger().info("Processing daily allowances")

    # Get all pending payments
    pending_payments = frappe.get_all(
        "Allowance Payment",
        filters={"status": "Pending"},
        fields=["name", "recipient", "amount", "source_type", "organization"]
    )

    for payment in pending_payments:
        process_pending_payment(payment)

    # Check for base allowance distributions (weekly/monthly)
    process_base_allowances()

    frappe.db.commit()


def process_pending_payment(payment: dict):
    """Process a pending allowance payment."""
    # Check if auto-approval is enabled for this source type
    auto_approve = frappe.get_value(
        "Family Settings",
        {"organization": payment.organization},
        "auto_approve_chore_earnings"
    )

    if auto_approve and payment.source_type == "Chore Completion":
        approve_payment(payment.name)
    elif payment.source_type == "Grade Reward":
        # Grade rewards may need parent review
        if should_auto_approve_grade_reward(payment):
            approve_payment(payment.name)


def approve_payment(payment_id: str):
    """Approve and credit a payment."""
    payment = frappe.get_doc("Allowance Payment", payment_id)

    payment.status = "Approved"
    payment.approved_at = frappe.utils.now_datetime()
    payment.save()

    # Credit to recipient's balance
    update_balance(payment.recipient, payment.amount, "credit")

    # Check for savings auto-transfer
    auto_save_percent = frappe.get_value(
        "Allowance Configuration",
        {"family_member": payment.recipient},
        "auto_save_percent"
    )

    if auto_save_percent:
        savings_amount = payment.amount * (auto_save_percent / 100)
        transfer_to_savings(payment.recipient, savings_amount)

    # Check for parent matching
    apply_parent_matching(payment.recipient, payment.amount)


def update_balance(member_id: str, amount: Decimal, operation: str):
    """Update member's allowance balance."""
    balance_doc = frappe.get_value(
        "Allowance Balance",
        {"family_member": member_id},
        "name"
    )

    if balance_doc:
        current = frappe.get_value("Allowance Balance", balance_doc, "current_balance")
        new_balance = current + amount if operation == "credit" else current - amount
        frappe.db.set_value("Allowance Balance", balance_doc, "current_balance", new_balance)
    else:
        frappe.get_doc({
            "doctype": "Allowance Balance",
            "family_member": member_id,
            "current_balance": amount if operation == "credit" else 0,
            "organization": frappe.get_value("Family Member", member_id, "organization")
        }).insert(ignore_permissions=True)


def transfer_to_savings(member_id: str, amount: Decimal):
    """Transfer amount to active savings goal."""
    goal = frappe.get_value(
        "Savings Goal",
        {"owner": member_id, "status": "Active"},
        ["name", "current_amount", "target_amount"],
        as_dict=True
    )

    if goal:
        new_amount = goal.current_amount + amount
        frappe.db.set_value("Savings Goal", goal.name, "current_amount", new_amount)

        # Update percent complete
        percent = (new_amount / goal.target_amount) * 100
        frappe.db.set_value("Savings Goal", goal.name, "percent_complete", percent)

        # Check for milestone achievements
        check_savings_milestones(goal.name, new_amount, goal.target_amount)

        # Deduct from spending balance
        update_balance(member_id, amount, "debit")


def apply_parent_matching(member_id: str, earned_amount: Decimal):
    """Apply parent matching program to savings."""
    match_program = frappe.get_value(
        "Parent Match Program",
        {"child": member_id, "status": "Active"},
        ["name", "match_percent", "match_cap_per_deposit", "remaining_cap"],
        as_dict=True
    )

    if not match_program:
        return

    # Calculate match amount
    match_amount = earned_amount * (match_program.match_percent / 100)

    # Apply caps
    if match_program.match_cap_per_deposit:
        match_amount = min(match_amount, match_program.match_cap_per_deposit)

    if match_program.remaining_cap:
        match_amount = min(match_amount, match_program.remaining_cap)

    if match_amount > 0:
        # Credit match to savings
        transfer_to_savings(member_id, match_amount)

        # Update remaining cap
        new_remaining = match_program.remaining_cap - match_amount
        frappe.db.set_value(
            "Parent Match Program",
            match_program.name,
            "remaining_cap",
            new_remaining
        )

        # Notify child
        notify_match_applied(member_id, match_amount)


def process_base_allowances():
    """Process base allowance distributions."""
    today_date = getdate(today())

    configs = frappe.get_all(
        "Allowance Configuration",
        filters={"base_allowance": [">", 0]},
        fields=[
            "name", "family_member", "base_allowance", "frequency",
            "distribution_day", "last_distribution"
        ]
    )

    for config in configs:
        should_distribute = False

        if config.frequency == "Weekly":
            # Distribute on specified day of week
            if today_date.strftime("%A") == config.distribution_day:
                if not config.last_distribution or \
                   (today_date - getdate(config.last_distribution)).days >= 7:
                    should_distribute = True

        elif config.frequency == "Bi-Weekly":
            if today_date.strftime("%A") == config.distribution_day:
                if not config.last_distribution or \
                   (today_date - getdate(config.last_distribution)).days >= 14:
                    should_distribute = True

        elif config.frequency == "Monthly":
            if today_date.day == int(config.distribution_day):
                if not config.last_distribution or \
                   getdate(config.last_distribution).month != today_date.month:
                    should_distribute = True

        if should_distribute:
            create_base_allowance_payment(config)


def create_base_allowance_payment(config: dict):
    """Create base allowance payment."""
    payment = frappe.get_doc({
        "doctype": "Allowance Payment",
        "recipient": config.family_member,
        "amount": config.base_allowance,
        "source_type": "Base Allowance",
        "status": "Approved",
        "approved_at": frappe.utils.now_datetime(),
        "organization": frappe.get_value("Family Member", config.family_member, "organization")
    })
    payment.insert(ignore_permissions=True)

    # Credit balance
    update_balance(config.family_member, config.base_allowance, "credit")

    # Update last distribution
    frappe.db.set_value(
        "Allowance Configuration",
        config.name,
        "last_distribution",
        today()
    )

    # Notify
    member = frappe.get_doc("Family Member", config.family_member)
    if member.user_account:
        frappe.publish_realtime(
            "allowance_received",
            {
                "amount": float(config.base_allowance),
                "source": "Base Allowance"
            },
            user=member.user_account
        )
```

## 7.4 Hourly Tasks

### Location Sync & Geofence Monitoring

```python
# dartwing_family/tasks/hourly/location.py

import frappe
from frappe.utils import now_datetime
from datetime import timedelta
from math import radians, cos, sin, sqrt, atan2

def sync_location_data():
    """
    Hourly job to:
    1. Aggregate location updates
    2. Update family location cache
    3. Clean up stale locations
    """
    frappe.logger().info("Syncing location data")

    # Get all family organizations
    orgs = frappe.get_all(
        "Organization",
        filters={"org_type": "Family"},
        fields=["name"]
    )

    for org in orgs:
        sync_family_locations(org.name)

    frappe.db.commit()


def sync_family_locations(organization: str):
    """Sync and cache family member locations."""
    members = frappe.get_all(
        "Family Member",
        filters={"organization": organization, "status": "Active"},
        fields=["name"]
    )

    location_cache = {}

    for member in members:
        # Get latest location
        latest = frappe.get_all(
            "Location History",
            filters={"family_member": member.name},
            fields=["latitude", "longitude", "accuracy", "timestamp"],
            order_by="timestamp desc",
            limit=1
        )

        if latest:
            loc = latest[0]
            location_cache[member.name] = {
                "lat": loc.latitude,
                "lon": loc.longitude,
                "accuracy": loc.accuracy,
                "timestamp": loc.timestamp.isoformat(),
                "is_stale": is_location_stale(loc.timestamp)
            }

    # Update cache
    frappe.cache().hset(
        f"family_locations_{organization}",
        "locations",
        frappe.as_json(location_cache)
    )


def is_location_stale(timestamp, threshold_minutes: int = 30) -> bool:
    """Check if location is stale."""
    return (now_datetime() - timestamp) > timedelta(minutes=threshold_minutes)


def check_geofence_alerts():
    """
    Hourly job to check geofence violations and alerts.
    """
    frappe.logger().info("Checking geofence alerts")

    # Get all active geofences
    geofences = frappe.get_all(
        "Family Geofence",
        filters={"status": "Active"},
        fields=[
            "name", "organization", "location_type", "latitude", "longitude",
            "radius_meters", "alert_on_arrival", "alert_on_departure",
            "expected_arrival_time", "alert_if_not_arrived_by", "applies_to"
        ]
    )

    for geofence in geofences:
        check_geofence(geofence)

    frappe.db.commit()


def check_geofence(geofence: dict):
    """Check a single geofence for all applicable members."""
    # Get applicable members
    if geofence.applies_to:
        members = [m.family_member for m in
                   frappe.get_all("Family Geofence Member",
                                  filters={"parent": geofence.name},
                                  fields=["family_member"])]
    else:
        # All family members
        members = [m.name for m in
                   frappe.get_all("Family Member",
                                  filters={"organization": geofence.organization,
                                          "status": "Active"},
                                  fields=["name"])]

    for member_id in members:
        check_member_geofence(member_id, geofence)


def check_member_geofence(member_id: str, geofence: dict):
    """Check if member is in/out of geofence and generate alerts."""
    # Get member's current location
    location = frappe.get_all(
        "Location History",
        filters={"family_member": member_id},
        fields=["latitude", "longitude", "timestamp"],
        order_by="timestamp desc",
        limit=1
    )

    if not location:
        return

    loc = location[0]

    # Skip stale locations
    if is_location_stale(loc.timestamp, 60):  # 1 hour threshold
        return

    # Calculate distance from geofence center
    distance = haversine_distance(
        loc.latitude, loc.longitude,
        geofence.latitude, geofence.longitude
    )

    is_inside = distance <= geofence.radius_meters

    # Get previous state
    cache_key = f"geofence_state_{member_id}_{geofence.name}"
    previous_state = frappe.cache().get(cache_key)

    # Update state
    frappe.cache().set(cache_key, "inside" if is_inside else "outside", expires_in_sec=7200)

    # Generate alerts for state changes
    if previous_state:
        if previous_state == "outside" and is_inside:
            if geofence.alert_on_arrival:
                send_geofence_alert(member_id, geofence, "arrived")
        elif previous_state == "inside" and not is_inside:
            if geofence.alert_on_departure:
                send_geofence_alert(member_id, geofence, "departed")

    # Check for expected arrival alerts
    if not is_inside and geofence.alert_if_not_arrived_by:
        check_late_arrival(member_id, geofence)


def send_geofence_alert(member_id: str, geofence: dict, event: str):
    """Send geofence alert to family."""
    member = frappe.get_doc("Family Member", member_id)

    # Get alert recipients
    recipients = frappe.get_all(
        "Family Geofence Alert Recipient",
        filters={"parent": geofence.name},
        fields=["family_member"]
    )

    for recipient in recipients:
        recipient_doc = frappe.get_doc("Family Member", recipient.family_member)

        if recipient_doc.user_account:
            message = f"{member.first_name} {event} {geofence.name}"

            frappe.publish_realtime(
                "geofence_alert",
                {
                    "member": member.first_name,
                    "location": geofence.name,
                    "event": event,
                    "timestamp": now_datetime().isoformat()
                },
                user=recipient_doc.user_account
            )

    # Log the event
    frappe.get_doc({
        "doctype": "Geofence Event Log",
        "family_member": member_id,
        "geofence": geofence.name,
        "event_type": event,
        "timestamp": now_datetime(),
        "organization": geofence.organization
    }).insert(ignore_permissions=True)


def check_late_arrival(member_id: str, geofence: dict):
    """Check if member should have arrived but hasn't."""
    from frappe.utils import get_time, now_datetime

    current_time = now_datetime().time()
    alert_time = get_time(geofence.alert_if_not_arrived_by)

    if current_time >= alert_time:
        # Check if we already sent alert today
        cache_key = f"late_alert_{member_id}_{geofence.name}_{frappe.utils.today()}"
        already_alerted = frappe.cache().get(cache_key)

        if not already_alerted:
            send_late_arrival_alert(member_id, geofence)
            frappe.cache().set(cache_key, True, expires_in_sec=86400)


def send_late_arrival_alert(member_id: str, geofence: dict):
    """Send alert that member hasn't arrived as expected."""
    member = frappe.get_doc("Family Member", member_id)

    # Alert all parents/guardians
    guardians = frappe.get_all(
        "Family Relationship",
        filters={
            "person_b": member_id,
            "is_legal_guardian": 1,
            "status": "Active"
        },
        fields=["person_a"]
    )

    for guardian in guardians:
        guardian_doc = frappe.get_doc("Family Member", guardian.person_a)

        if guardian_doc.user_account:
            frappe.publish_realtime(
                "late_arrival_alert",
                {
                    "member": member.first_name,
                    "expected_location": geofence.name,
                    "expected_time": str(geofence.alert_if_not_arrived_by)
                },
                user=guardian_doc.user_account
            )


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Calculate distance between two points in meters."""
    R = 6371000  # Earth's radius in meters

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
```

### Grade Data Sync

```python
# dartwing_family/tasks/hourly/grades.py

import frappe
from dartwing_family.integrations.registry import AdapterRegistry

def sync_grade_data():
    """
    Hourly job to sync grade data from educational platforms.
    """
    frappe.logger().info("Syncing grade data")

    # Get all education integrations
    integrations = frappe.get_all(
        "Integration Configuration",
        filters={
            "adapter_type": "education",
            "status": "Connected"
        },
        fields=["name", "adapter", "organization"]
    )

    for integration in integrations:
        try:
            sync_education_integration(integration)
        except Exception as e:
            frappe.log_error(
                title=f"Grade Sync Error: {integration.adapter}",
                message=str(e)
            )

            # Update integration status
            frappe.db.set_value(
                "Integration Configuration",
                integration.name,
                {
                    "status": "Error",
                    "last_error": str(e)
                }
            )

    frappe.db.commit()


def sync_education_integration(integration: dict):
    """Sync data from a single education integration."""
    adapter = AdapterRegistry.get_adapter(integration.adapter, integration.organization)

    # Get students linked to this integration
    students = frappe.get_all(
        "Education Platform Link",
        filters={
            "integration": integration.name,
            "status": "Active"
        },
        fields=["family_member", "external_student_id"]
    )

    for student in students:
        sync_student_grades(adapter, student, integration.organization)


def sync_student_grades(adapter, student: dict, organization: str):
    """Sync grades for a single student."""
    # Get courses
    courses = adapter.get_courses(student.external_student_id)

    for course in courses:
        # Update or create academic class record
        update_academic_class(student.family_member, course, organization)

        # Get assignments and grades
        coursework = adapter.get_coursework(course["course_id"])

        for assignment in coursework:
            submissions = adapter.get_student_submissions(
                course["course_id"],
                assignment["assignment_id"],
                student.external_student_id
            )

            for submission in submissions:
                update_assignment_record(
                    student.family_member,
                    course,
                    assignment,
                    submission,
                    organization
                )

    # Check for missing assignments
    check_missing_assignments(adapter, student, organization)

    # Calculate and update GPA
    update_gpa(student.family_member)

    # Check grade reward triggers
    check_grade_rewards(student.family_member, organization)


def update_academic_class(member_id: str, course: dict, organization: str):
    """Update or create academic class record."""
    existing = frappe.db.exists(
        "Academic Class",
        {
            "family_member": member_id,
            "external_course_id": course["course_id"]
        }
    )

    if existing:
        frappe.db.set_value(
            "Academic Class",
            existing,
            {
                "class_name": course["name"],
                "teacher_name": course.get("teacher_name")
            }
        )
    else:
        frappe.get_doc({
            "doctype": "Academic Class",
            "family_member": member_id,
            "external_course_id": course["course_id"],
            "class_name": course["name"],
            "teacher_name": course.get("teacher_name"),
            "organization": organization
        }).insert(ignore_permissions=True)


def update_assignment_record(member_id, course, assignment, submission, organization):
    """Update assignment and grade records."""
    if submission.get("grade") is not None:
        # Calculate grade percent
        if assignment.get("max_points"):
            grade_percent = (submission["grade"] / assignment["max_points"]) * 100
        else:
            grade_percent = submission["grade"]

        # Check if this is a new grade
        existing = frappe.db.exists(
            "Academic Assignment",
            {
                "family_member": member_id,
                "external_assignment_id": assignment["assignment_id"]
            }
        )

        if existing:
            old_grade = frappe.get_value("Academic Assignment", existing, "grade_percent")

            frappe.db.set_value(
                "Academic Assignment",
                existing,
                {
                    "grade_percent": grade_percent,
                    "submission_status": submission["status"],
                    "is_late": submission.get("late", False)
                }
            )

            # Notify if grade changed significantly
            if old_grade and abs(grade_percent - old_grade) > 5:
                notify_grade_change(member_id, assignment["title"], old_grade, grade_percent)
        else:
            frappe.get_doc({
                "doctype": "Academic Assignment",
                "family_member": member_id,
                "external_assignment_id": assignment["assignment_id"],
                "assignment_name": assignment["title"],
                "class_name": course["name"],
                "grade_percent": grade_percent,
                "max_points": assignment.get("max_points"),
                "due_date": assignment.get("due_date"),
                "submission_status": submission["status"],
                "is_late": submission.get("late", False),
                "organization": organization
            }).insert(ignore_permissions=True)


def check_missing_assignments(adapter, student: dict, organization: str):
    """Check for and alert on missing assignments."""
    missing = adapter.get_missing_assignments(student.external_student_id)

    if missing:
        # Update missing assignment count in member profile
        frappe.db.set_value(
            "Academic Record",
            {"family_member": student.family_member},
            "missing_assignments",
            len(missing)
        )

        # Alert parents if there are new missing assignments
        notify_missing_assignments(student.family_member, missing)


def check_grade_rewards(member_id: str, organization: str):
    """Check and apply grade-based rewards."""
    # Get recent graded assignments
    recent_grades = frappe.get_all(
        "Academic Assignment",
        filters={
            "family_member": member_id,
            "modified": [">=", frappe.utils.add_days(frappe.utils.today(), -1)]
        },
        fields=["assignment_name", "grade_percent", "class_name"]
    )

    # Get reward rules
    rules = frappe.get_all(
        "Grade Reward Rule",
        filters={"family_member": member_id, "status": "Active"},
        fields=["rule_type", "grade_threshold", "money_reward", "points_reward"]
    )

    for grade in recent_grades:
        for rule in rules:
            if rule.rule_type == "Grade Threshold":
                threshold = parse_grade_threshold(rule.grade_threshold)
                if grade.grade_percent >= threshold:
                    apply_grade_reward(member_id, grade, rule, organization)

            elif rule.rule_type == "Perfect Score":
                if grade.grade_percent >= 100:
                    apply_grade_reward(member_id, grade, rule, organization)


def apply_grade_reward(member_id: str, grade: dict, rule: dict, organization: str):
    """Apply a grade-based reward."""
    # Check if already rewarded for this grade
    existing = frappe.db.exists(
        "Allowance Payment",
        {
            "recipient": member_id,
            "source_type": "Grade Reward",
            "source_reference": grade.assignment_name
        }
    )

    if not existing:
        frappe.get_doc({
            "doctype": "Allowance Payment",
            "recipient": member_id,
            "amount": rule.money_reward,
            "source_type": "Grade Reward",
            "source_reference": grade.assignment_name,
            "status": "Pending",
            "organization": organization
        }).insert(ignore_permissions=True)

        # Notify
        member = frappe.get_doc("Family Member", member_id)
        if member.user_account:
            frappe.publish_realtime(
                "grade_reward",
                {
                    "assignment": grade.assignment_name,
                    "grade": grade.grade_percent,
                    "reward": float(rule.money_reward)
                },
                user=member.user_account
            )


def parse_grade_threshold(threshold: str) -> float:
    """Parse grade threshold string to percent."""
    thresholds = {"A": 90, "A-": 90, "B+": 87, "B": 83, "B-": 80, "C+": 77, "C": 73}
    return thresholds.get(threshold, float(threshold.replace("%", "")))
```

## 7.5 Cron Tasks

### Morning Briefing

```python
# dartwing_family/tasks/cron/morning_briefing.py

import frappe
from frappe.utils import today, getdate, format_datetime

def morning_briefing():
    """
    Daily 6 AM job to send morning briefings to family members.
    """
    frappe.logger().info("Generating morning briefings")

    # Get all family organizations
    orgs = frappe.get_all(
        "Organization",
        filters={"org_type": "Family"},
        fields=["name"]
    )

    for org in orgs:
        generate_family_briefing(org.name)

    frappe.db.commit()


def generate_family_briefing(organization: str):
    """Generate and send morning briefing for a family."""
    # Get family settings
    settings = frappe.get_value(
        "Family Settings",
        {"organization": organization},
        ["enable_morning_briefing", "briefing_time", "briefing_recipients"],
        as_dict=True
    )

    if not settings or not settings.enable_morning_briefing:
        return

    # Generate briefing content
    briefing = compile_briefing(organization)

    # Get recipients
    recipients = get_briefing_recipients(organization, settings.briefing_recipients)

    for recipient in recipients:
        send_briefing(recipient, briefing)


def compile_briefing(organization: str) -> dict:
    """Compile all briefing information."""
    today_date = getdate(today())

    briefing = {
        "date": format_datetime(today_date, "EEEE, MMMM d"),
        "weather": get_weather_summary(organization),
        "calendar": get_today_events(organization),
        "chores": get_chore_summary(organization),
        "birthdays": get_todays_birthdays(organization),
        "reminders": get_reminders(organization)
    }

    return briefing


def get_weather_summary(organization: str) -> dict:
    """Get weather summary for family's location."""
    # Get family's primary location
    home = frappe.get_value(
        "Family Geofence",
        {"organization": organization, "location_type": "Home"},
        ["latitude", "longitude"],
        as_dict=True
    )

    if not home:
        return None

    # Fetch weather (cached from sync_weather_data)
    weather = frappe.cache().hget(f"weather_{organization}", "current")

    if weather:
        return frappe.parse_json(weather)

    return None


def get_today_events(organization: str) -> list:
    """Get today's calendar events."""
    events = frappe.get_all(
        "Family Calendar Event",
        filters={
            "organization": organization,
            "start_datetime": [">=", frappe.utils.today()],
            "start_datetime": ["<", frappe.utils.add_days(frappe.utils.today(), 1)]
        },
        fields=[
            "title", "start_datetime", "end_datetime",
            "location", "primary_person", "event_type"
        ],
        order_by="start_datetime asc"
    )

    # Format events
    formatted = []
    for event in events:
        member = frappe.get_value("Family Member", event.primary_person, "first_name")
        formatted.append({
            "title": event.title,
            "time": format_datetime(event.start_datetime, "h:mm a"),
            "location": event.location,
            "person": member,
            "type": event.event_type
        })

    return formatted


def get_chore_summary(organization: str) -> dict:
    """Get summary of today's chores."""
    chores = frappe.get_all(
        "Chore Assignment",
        filters={
            "organization": organization,
            "due_date": frappe.utils.today()
        },
        fields=["assigned_to", "status", "chore_template"]
    )

    # Group by member
    by_member = {}
    for chore in chores:
        member = frappe.get_value("Family Member", chore.assigned_to, "first_name")
        if member not in by_member:
            by_member[member] = {"pending": 0, "completed": 0}

        if chore.status in ["Pending", "In Progress"]:
            by_member[member]["pending"] += 1
        else:
            by_member[member]["completed"] += 1

    return by_member


def get_todays_birthdays(organization: str) -> list:
    """Check for family birthdays today."""
    today_date = getdate(today())

    members = frappe.get_all(
        "Family Member",
        filters={"organization": organization, "status": "Active"},
        fields=["first_name", "date_of_birth", "age"]
    )

    birthdays = []
    for member in members:
        if member.date_of_birth:
            dob = getdate(member.date_of_birth)
            if dob.month == today_date.month and dob.day == today_date.day:
                birthdays.append({
                    "name": member.first_name,
                    "age": member.age
                })

    return birthdays


def get_reminders(organization: str) -> list:
    """Get reminders for today."""
    reminders = []

    # Check for maintenance reminders
    maintenance = frappe.get_all(
        "Maintenance Schedule Item",
        filters={
            "organization": organization,
            "next_due_date": frappe.utils.today()
        },
        fields=["maintenance_item", "asset"]
    )

    for m in maintenance:
        asset_name = frappe.get_value("Family Asset", m.asset, "asset_name")
        reminders.append({
            "type": "maintenance",
            "message": f"{m.maintenance_item} for {asset_name}"
        })

    # Check for expiring items
    expiring = frappe.get_all(
        "Household Item",
        filters={
            "organization": organization,
            "expiration_date": ["between", [
                frappe.utils.today(),
                frappe.utils.add_days(frappe.utils.today(), 3)
            ]]
        },
        fields=["item_name", "expiration_date"]
    )

    for item in expiring:
        days = (getdate(item.expiration_date) - getdate(today())).days
        if days == 0:
            reminders.append({
                "type": "expiration",
                "message": f"{item.item_name} expires today!"
            })
        else:
            reminders.append({
                "type": "expiration",
                "message": f"{item.item_name} expires in {days} days"
            })

    return reminders


def send_briefing(recipient: dict, briefing: dict):
    """Send briefing to a family member."""
    member = frappe.get_doc("Family Member", recipient["member_id"])

    # Customize briefing for this member
    personalized = personalize_briefing(briefing, member)

    # Send via preferred channel
    if recipient.get("channel") == "voice" and member.user_account:
        # Queue voice briefing
        frappe.enqueue(
            "dartwing_family.voice.briefing.deliver_voice_briefing",
            member_id=member.name,
            briefing=personalized
        )

    # Send push notification
    if member.user_account:
        frappe.publish_realtime(
            "morning_briefing",
            personalized,
            user=member.user_account
        )

    # Send email if configured
    if recipient.get("email") and member.email:
        send_briefing_email(member.email, personalized)


def personalize_briefing(briefing: dict, member) -> dict:
    """Personalize briefing for specific member."""
    personalized = briefing.copy()

    # Filter calendar to relevant events
    personalized["my_events"] = [
        e for e in briefing["calendar"]
        if e["person"] == member.first_name
    ]

    # Get member's chores
    personalized["my_chores"] = briefing["chores"].get(member.first_name, {})

    # Add personalized greeting
    hour = frappe.utils.now_datetime().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    personalized["greeting"] = f"{greeting}, {member.first_name}!"

    return personalized
```

### Screen Time Enforcement

```python
# dartwing_family/tasks/cron/screen_time.py

import frappe
from frappe.utils import now_datetime, get_time, time_diff_in_seconds

def check_screen_time_limits():
    """
    Every 5 minutes: Check and enforce screen time limits.
    """
    # Get all active screen time profiles for minors
    profiles = frappe.get_all(
        "Screen Time Profile",
        filters={"status": "Active"},
        fields=[
            "name", "family_member", "weekday_limit_minutes",
            "weekend_limit_minutes", "allowed_start_time",
            "allowed_end_time", "organization"
        ]
    )

    current_time = now_datetime().time()
    is_weekend = now_datetime().weekday() >= 5

    for profile in profiles:
        check_member_screen_time(profile, current_time, is_weekend)


def check_member_screen_time(profile: dict, current_time, is_weekend: bool):
    """Check screen time for a single member."""
    member = frappe.get_doc("Family Member", profile.family_member)

    # Skip if member is adult
    if not member.is_minor:
        return

    # Check time window
    if profile.allowed_start_time and profile.allowed_end_time:
        start = get_time(profile.allowed_start_time)
        end = get_time(profile.allowed_end_time)

        if current_time < start or current_time > end:
            # Outside allowed time - send lock signal
            send_screen_lock_signal(member, "outside_hours")
            return

    # Check daily limit
    limit = profile.weekend_limit_minutes if is_weekend else profile.weekday_limit_minutes

    if limit and limit > 0:
        used = get_screen_time_used(profile.family_member)

        if used >= limit:
            send_screen_lock_signal(member, "limit_reached")
        elif used >= limit - 15:  # 15 minute warning
            send_screen_time_warning(member, limit - used)


def get_screen_time_used(member_id: str) -> int:
    """Get minutes of screen time used today."""
    today_start = frappe.utils.get_datetime(frappe.utils.today())

    usage = frappe.db.sql("""
        SELECT SUM(duration_minutes) as total
        FROM `tabScreen Time Log`
        WHERE family_member = %s
        AND start_time >= %s
    """, (member_id, today_start), as_dict=True)

    return usage[0].total or 0 if usage else 0


def send_screen_lock_signal(member, reason: str):
    """Send signal to lock devices."""
    if member.user_account:
        frappe.publish_realtime(
            "screen_time_lock",
            {
                "action": "lock",
                "reason": reason,
                "member_id": member.name
            },
            user=member.user_account
        )

    # Also notify parents
    notify_parents_screen_time(member, reason)


def send_screen_time_warning(member, minutes_left: int):
    """Send warning about remaining screen time."""
    if member.user_account:
        frappe.publish_realtime(
            "screen_time_warning",
            {
                "minutes_left": minutes_left,
                "member_id": member.name
            },
            user=member.user_account
        )


def notify_parents_screen_time(member, reason: str):
    """Notify parents about screen time limit reached."""
    guardians = frappe.get_all(
        "Family Relationship",
        filters={
            "person_b": member.name,
            "is_legal_guardian": 1,
            "status": "Active"
        },
        fields=["person_a"]
    )

    for guardian in guardians:
        guardian_doc = frappe.get_doc("Family Member", guardian.person_a)
        if guardian_doc.user_account:
            frappe.publish_realtime(
                "child_screen_time_limit",
                {
                    "child": member.first_name,
                    "reason": reason
                },
                user=guardian_doc.user_account
            )
```

## 7.6 Background Job Utilities

```python
# dartwing_family/tasks/utils.py

import frappe
from functools import wraps
from typing import Callable
import traceback

def family_job(queue: str = "default"):
    """
    Decorator for family background jobs with error handling and logging.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            job_name = func.__name__
            start_time = frappe.utils.now_datetime()

            frappe.logger().info(f"Starting job: {job_name}")

            try:
                result = func(*args, **kwargs)

                # Log success
                log_job_execution(job_name, "Success", start_time)

                return result

            except Exception as e:
                # Log error
                error_msg = traceback.format_exc()
                frappe.log_error(
                    title=f"Job Failed: {job_name}",
                    message=error_msg
                )

                log_job_execution(job_name, "Failed", start_time, str(e))

                # Re-raise for RQ to handle retry
                raise

        return wrapper
    return decorator


def log_job_execution(job_name: str, status: str, start_time, error: str = None):
    """Log job execution for monitoring."""
    end_time = frappe.utils.now_datetime()
    duration = (end_time - start_time).total_seconds()

    frappe.get_doc({
        "doctype": "Background Job Log",
        "job_name": job_name,
        "status": status,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration,
        "error_message": error
    }).insert(ignore_permissions=True)


def enqueue_for_all_families(method: str, **kwargs):
    """Enqueue a job for each family organization."""
    orgs = frappe.get_all(
        "Organization",
        filters={"org_type": "Family"},
        fields=["name"]
    )

    for org in orgs:
        frappe.enqueue(
            method,
            organization=org.name,
            **kwargs
        )


def with_organization_context(func: Callable):
    """
    Decorator to set organization context for a job.
    """
    @wraps(func)
    def wrapper(organization: str, *args, **kwargs):
        # Set organization in flags for permission checks
        frappe.flags.current_organization = organization

        try:
            return func(organization, *args, **kwargs)
        finally:
            frappe.flags.current_organization = None

    return wrapper
```

---

_End of Section 7: Background Services & Scheduled Tasks_

**Next Section:** Section 8 - Testing & Quality Assurance Architecture

# Section 8: Testing & Quality Assurance Architecture

## 8.1 Testing Strategy Overview

Dartwing Family implements a comprehensive multi-layer testing strategy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TESTING PYRAMID                                       │
│                                                                              │
│                            ┌─────────┐                                       │
│                            │   E2E   │  ◄── Cypress, Appium                 │
│                            │  Tests  │      (10% of tests)                  │
│                           ─┴─────────┴─                                      │
│                          ┌─────────────┐                                     │
│                          │ Integration │  ◄── API tests, DB tests           │
│                          │   Tests     │      (20% of tests)                │
│                         ─┴─────────────┴─                                    │
│                        ┌─────────────────┐                                   │
│                        │   Component     │  ◄── Widget tests, Controller    │
│                        │    Tests        │      tests (30% of tests)        │
│                       ─┴─────────────────┴─                                  │
│                      ┌─────────────────────┐                                 │
│                      │     Unit Tests      │  ◄── Functions, Classes        │
│                      │                     │      (40% of tests)            │
│                     ─┴─────────────────────┴─                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    SPECIALIZED TESTING                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Security   │  │  Performance │  │  Compliance  │              │    │
│  │  │   Testing    │  │   Testing    │  │   Testing    │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • OWASP      │  │ • Load tests │  │ • COPPA      │              │    │
│  │  │ • Pen tests  │  │ • Stress     │  │ • HIPAA      │              │    │
│  │  │ • Auth tests │  │ • Benchmark  │  │ • GDPR       │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8.2 Backend Testing (Python/Frappe)

### Test Configuration

```python
# dartwing_family/tests/conftest.py

import pytest
import frappe
from frappe.tests.utils import FrappeTestCase
from typing import Generator
from datetime import date, timedelta

@pytest.fixture(scope="session")
def test_site():
    """Initialize test site."""
    frappe.init(site="test_site")
    frappe.connect()
    yield
    frappe.destroy()


@pytest.fixture(scope="function")
def test_family(test_site) -> Generator[dict, None, None]:
    """Create a test family organization with members."""
    # Create organization
    org = frappe.get_doc({
        "doctype": "Organization",
        "organization_name": "Test Family",
        "org_type": "Family"
    })
    org.insert(ignore_permissions=True)

    # Create family members
    parent1 = create_test_member(org.name, "Parent", "John", age=40, is_admin=True)
    parent2 = create_test_member(org.name, "Parent", "Jane", age=38, gender="Female")
    teen = create_test_member(org.name, "Teen", "Alex", age=15)
    child = create_test_member(org.name, "Child", "Emma", age=8)

    # Create relationships
    create_relationship(parent1.name, teen.name, "Parent-Child")
    create_relationship(parent1.name, child.name, "Parent-Child")
    create_relationship(parent2.name, teen.name, "Parent-Child")
    create_relationship(parent2.name, child.name, "Parent-Child")
    create_relationship(parent1.name, parent2.name, "Spouse")

    family_data = {
        "organization": org.name,
        "parent1": parent1,
        "parent2": parent2,
        "teen": teen,
        "child": child
    }

    yield family_data

    # Cleanup
    cleanup_test_family(org.name)


@pytest.fixture
def test_user(test_site) -> Generator[str, None, None]:
    """Create a test user."""
    user = frappe.get_doc({
        "doctype": "User",
        "email": "test@example.com",
        "first_name": "Test",
        "user_type": "Website User"
    })
    user.insert(ignore_permissions=True)

    yield user.name

    frappe.delete_doc("User", user.name, force=True)


def create_test_member(
    organization: str,
    role: str,
    first_name: str,
    age: int = 30,
    gender: str = "Male",
    is_admin: bool = False
) -> "FamilyMember":
    """Helper to create test family member."""
    dob = date.today() - timedelta(days=age * 365)

    member = frappe.get_doc({
        "doctype": "Family Member",
        "first_name": first_name,
        "last_name": "Test",
        "date_of_birth": dob,
        "gender": gender,
        "family_role": role,
        "is_admin": is_admin,
        "organization": organization,
        "status": "Active"
    })
    member.insert(ignore_permissions=True)
    return member


def create_relationship(person_a: str, person_b: str, rel_type: str):
    """Helper to create family relationship."""
    frappe.get_doc({
        "doctype": "Family Relationship",
        "person_a": person_a,
        "person_b": person_b,
        "relationship_type": rel_type,
        "is_legal_guardian": rel_type == "Parent-Child",
        "status": "Active"
    }).insert(ignore_permissions=True)


def cleanup_test_family(organization: str):
    """Clean up all test family data."""
    # Delete in correct order for foreign key constraints
    doctypes = [
        "Chore Assignment",
        "Family Relationship",
        "Family Member",
        "Organization"
    ]

    for doctype in doctypes:
        docs = frappe.get_all(doctype, filters={"organization": organization})
        for doc in docs:
            frappe.delete_doc(doctype, doc.name, force=True)
```

### Unit Tests

```python
# dartwing_family/tests/unit/test_age_calculations.py

import pytest
from datetime import date, timedelta
from dartwing_family.tasks.daily.age_check import (
    calculate_age,
    get_age_category,
    check_milestone_transition
)


class TestAgeCalculations:
    """Test age calculation functions."""

    def test_calculate_age_exact_birthday(self):
        """Test age on exact birthday."""
        today = date.today()
        dob = date(today.year - 10, today.month, today.day)
        assert calculate_age(dob) == 10

    def test_calculate_age_before_birthday(self):
        """Test age before birthday this year."""
        today = date.today()
        # Birthday is tomorrow
        dob = date(today.year - 10, today.month, today.day) + timedelta(days=1)
        if dob > today:
            dob = date(today.year - 10 - 1, dob.month, dob.day)
        assert calculate_age(dob) == 9

    def test_calculate_age_after_birthday(self):
        """Test age after birthday this year."""
        today = date.today()
        # Birthday was yesterday
        dob = date(today.year - 10, today.month, today.day) - timedelta(days=1)
        assert calculate_age(dob) == 10

    def test_calculate_age_none_dob(self):
        """Test age calculation with no DOB."""
        assert calculate_age(None) == 0

    @pytest.mark.parametrize("age,expected_category", [
        (0, "Infant"),
        (1, "Toddler"),
        (2, "Toddler"),
        (3, "Child"),
        (12, "Child"),
        (13, "Tween"),
        (15, "Tween"),
        (16, "Teen"),
        (17, "Teen"),
        (18, "Adult"),
        (64, "Adult"),
        (65, "Senior"),
        (80, "Senior"),
    ])
    def test_get_age_category(self, age, expected_category):
        """Test age category mapping."""
        assert get_age_category(age) == expected_category

    def test_milestone_transition_coppa_exit(self):
        """Test COPPA exit transition at 13."""
        transition = check_milestone_transition("member_1", 12, 13)
        assert transition is not None
        assert transition["milestone_type"] == "coppa_exit"

    def test_milestone_transition_adult(self):
        """Test adult transition at 18."""
        transition = check_milestone_transition("member_1", 17, 18)
        assert transition is not None
        assert transition["milestone_type"] == "adult"

    def test_milestone_transition_no_milestone(self):
        """Test no transition for regular birthday."""
        transition = check_milestone_transition("member_1", 10, 11)
        assert transition is None


# dartwing_family/tests/unit/test_permission_engine.py

import pytest
from unittest.mock import Mock, patch
from dartwing_family.permissions.permission_engine import FamilyPermissionEngine


class TestPermissionEngine:
    """Test permission engine logic."""

    @pytest.fixture
    def mock_parent_engine(self):
        """Create permission engine for parent user."""
        with patch('frappe.get_doc') as mock_get_doc:
            mock_member = Mock()
            mock_member.family_role = "Parent"
            mock_member.is_admin = True
            mock_member.age = 40
            mock_member.organization = "test_org"
            mock_get_doc.return_value = mock_member

            engine = FamilyPermissionEngine("parent_user")
            engine.member = mock_member
            return engine

    @pytest.fixture
    def mock_child_engine(self):
        """Create permission engine for child user."""
        with patch('frappe.get_doc') as mock_get_doc:
            mock_member = Mock()
            mock_member.family_role = "Child"
            mock_member.is_admin = False
            mock_member.age = 8
            mock_member.organization = "test_org"
            mock_member.permission_profile = Mock()
            mock_member.permission_profile.can_use_ghost_mode = False
            mock_get_doc.return_value = mock_member

            engine = FamilyPermissionEngine("child_user")
            engine.member = mock_member
            return engine

    def test_parent_can_view_child_location(self, mock_parent_engine):
        """Parent should be able to view child's location."""
        with patch.object(mock_parent_engine, '_is_guardian_of', return_value=True):
            assert mock_parent_engine.can_view_member_location("child_member") is True

    def test_child_cannot_use_ghost_mode(self, mock_child_engine):
        """Child should not be able to use ghost mode."""
        assert mock_child_engine.can_use_ghost_mode() is False

    def test_parent_can_modify_child_controls(self, mock_parent_engine):
        """Parent should be able to modify child's parental controls."""
        with patch.object(mock_parent_engine, '_is_guardian_of', return_value=True):
            with patch('frappe.get_doc') as mock_get_doc:
                mock_child = Mock()
                mock_child.is_minor = True
                mock_get_doc.return_value = mock_child

                assert mock_parent_engine.can_modify_parental_controls("child_member") is True

    def test_child_cannot_approve_spending(self, mock_child_engine):
        """Child should not be able to approve their own spending over limit."""
        mock_child_engine.member.permission_profile.max_spend_per_transaction = 10
        assert mock_child_engine.can_spend_allowance(50) is False

    def test_child_can_spend_within_limit(self, mock_child_engine):
        """Child should be able to spend within their limit."""
        mock_child_engine.member.permission_profile.max_spend_per_transaction = 25
        assert mock_child_engine.can_spend_allowance(10) is True
```

### Integration Tests

```python
# dartwing_family/tests/integration/test_chore_workflow.py

import pytest
import frappe
from dartwing_family.tests.conftest import test_family


class TestChoreWorkflow:
    """Integration tests for complete chore workflow."""

    def test_chore_assignment_to_completion(self, test_family):
        """Test full chore lifecycle: assign -> complete -> verify -> reward."""
        # Create chore template
        template = frappe.get_doc({
            "doctype": "Chore Template",
            "chore_name": "Clean Room",
            "description": "Clean and organize bedroom",
            "base_points": 10,
            "base_money": 2.00,
            "minimum_age": 6,
            "organization": test_family["organization"]
        })
        template.insert(ignore_permissions=True)

        # Assign chore to child
        assignment = frappe.get_doc({
            "doctype": "Chore Assignment",
            "chore_template": template.name,
            "assigned_to": test_family["child"].name,
            "assigned_by": test_family["parent1"].name,
            "due_date": frappe.utils.today(),
            "status": "Pending",
            "organization": test_family["organization"]
        })
        assignment.insert(ignore_permissions=True)

        assert assignment.status == "Pending"

        # Child completes chore
        assignment.reload()
        assignment.status = "Completed"
        assignment.completed_at = frappe.utils.now_datetime()
        assignment.save()

        assert assignment.status == "Completed"

        # Parent verifies
        assignment.reload()
        assignment.status = "Verified"
        assignment.verified_by = test_family["parent1"].name
        assignment.verified_at = frappe.utils.now_datetime()
        assignment.points_earned = template.base_points
        assignment.money_earned = template.base_money
        assignment.save()

        assert assignment.status == "Verified"
        assert assignment.points_earned == 10
        assert assignment.money_earned == 2.00

        # Cleanup
        frappe.delete_doc("Chore Assignment", assignment.name, force=True)
        frappe.delete_doc("Chore Template", template.name, force=True)

    def test_chore_streak_calculation(self, test_family):
        """Test streak bonus calculation."""
        from dartwing_family.chores.streak import calculate_streak_bonus

        # Create 7 consecutive completed chores
        for i in range(7):
            # Simulate 7 days of completed chores
            pass  # Implementation

        bonus = calculate_streak_bonus(
            test_family["child"].name,
            "daily_chore_template"
        )

        # 7-day streak should give 50% bonus
        assert bonus == 0.5

    def test_chore_age_restriction(self, test_family):
        """Test that age-restricted chores cannot be assigned to young children."""
        template = frappe.get_doc({
            "doctype": "Chore Template",
            "chore_name": "Mow Lawn",
            "minimum_age": 14,
            "organization": test_family["organization"]
        })
        template.insert(ignore_permissions=True)

        # Try to assign to 8-year-old - should fail
        with pytest.raises(frappe.ValidationError):
            assignment = frappe.get_doc({
                "doctype": "Chore Assignment",
                "chore_template": template.name,
                "assigned_to": test_family["child"].name,  # Age 8
                "organization": test_family["organization"]
            })
            assignment.insert()

        # Cleanup
        frappe.delete_doc("Chore Template", template.name, force=True)


# dartwing_family/tests/integration/test_allowance_system.py

class TestAllowanceSystem:
    """Integration tests for allowance and rewards system."""

    def test_allowance_credit_flow(self, test_family):
        """Test allowance credit from chore completion."""
        # Setup initial balance
        balance = frappe.get_doc({
            "doctype": "Allowance Balance",
            "family_member": test_family["teen"].name,
            "current_balance": 10.00,
            "organization": test_family["organization"]
        })
        balance.insert(ignore_permissions=True)

        # Create and approve payment
        payment = frappe.get_doc({
            "doctype": "Allowance Payment",
            "recipient": test_family["teen"].name,
            "amount": 5.00,
            "source_type": "Chore Completion",
            "status": "Approved",
            "organization": test_family["organization"]
        })
        payment.insert(ignore_permissions=True)

        # Trigger balance update
        from dartwing_family.tasks.daily.allowance import update_balance
        update_balance(test_family["teen"].name, 5.00, "credit")

        # Verify balance updated
        balance.reload()
        assert balance.current_balance == 15.00

        # Cleanup
        frappe.delete_doc("Allowance Payment", payment.name, force=True)
        frappe.delete_doc("Allowance Balance", balance.name, force=True)

    def test_parent_matching_program(self, test_family):
        """Test parent matching for savings."""
        # Create savings goal
        goal = frappe.get_doc({
            "doctype": "Savings Goal",
            "owner": test_family["teen"].name,
            "goal_name": "Nintendo Switch",
            "target_amount": 300.00,
            "current_amount": 0.00,
            "status": "Active",
            "organization": test_family["organization"]
        })
        goal.insert(ignore_permissions=True)

        # Create matching program (50% match up to $50)
        match_program = frappe.get_doc({
            "doctype": "Parent Match Program",
            "child": test_family["teen"].name,
            "match_percent": 50,
            "match_cap_per_deposit": 10.00,
            "remaining_cap": 50.00,
            "status": "Active",
            "organization": test_family["organization"]
        })
        match_program.insert(ignore_permissions=True)

        # Simulate deposit of $20 to savings
        from dartwing_family.tasks.daily.allowance import apply_parent_matching
        apply_parent_matching(test_family["teen"].name, 20.00)

        # Verify match applied (50% of $20 = $10, but capped at $10 per deposit)
        match_program.reload()
        assert match_program.remaining_cap == 40.00  # $50 - $10 = $40

        # Cleanup
        frappe.delete_doc("Parent Match Program", match_program.name, force=True)
        frappe.delete_doc("Savings Goal", goal.name, force=True)
```

### API Tests

```python
# dartwing_family/tests/api/test_family_api.py

import pytest
import frappe
from frappe.tests.utils import make_test_records


class TestFamilyAPI:
    """Test API endpoints."""

    @pytest.fixture
    def authenticated_parent(self, test_family):
        """Setup authenticated parent user."""
        # Create user for parent
        user = frappe.get_doc({
            "doctype": "User",
            "email": "parent@test.com",
            "first_name": "Parent",
            "user_type": "Website User"
        })
        user.insert(ignore_permissions=True)

        # Link to family member
        frappe.db.set_value(
            "Family Member",
            test_family["parent1"].name,
            "user_account",
            user.name
        )

        frappe.set_user(user.name)

        yield user

        frappe.set_user("Administrator")
        frappe.delete_doc("User", user.name, force=True)

    def test_get_family_dashboard(self, test_family, authenticated_parent):
        """Test dashboard API returns correct data."""
        from dartwing_family.api.family_api import get_family_dashboard

        result = get_family_dashboard()

        assert "members" in result
        assert "today_events" in result
        assert "pending_chores" in result
        assert len(result["members"]) == 4  # 2 parents + teen + child

    def test_get_member_location_permission(self, test_family, authenticated_parent):
        """Test location API respects permissions."""
        from dartwing_family.api.location_api import get_member_location

        # Parent should be able to get child's location
        result = get_member_location(test_family["child"].name)
        assert "error" not in result

        # But not non-family member
        with pytest.raises(frappe.PermissionError):
            get_member_location("non_family_member")

    def test_complete_chore_api(self, test_family, authenticated_parent):
        """Test chore completion API."""
        from dartwing_family.api.chore_api import complete_chore

        # Create test chore
        template = frappe.get_doc({
            "doctype": "Chore Template",
            "chore_name": "Test Chore",
            "base_points": 5,
            "organization": test_family["organization"]
        })
        template.insert(ignore_permissions=True)

        assignment = frappe.get_doc({
            "doctype": "Chore Assignment",
            "chore_template": template.name,
            "assigned_to": test_family["child"].name,
            "due_date": frappe.utils.today(),
            "status": "Pending",
            "organization": test_family["organization"]
        })
        assignment.insert(ignore_permissions=True)

        # Complete via API
        result = complete_chore(assignment.name)

        assert result["status"] == "success"

        assignment.reload()
        assert assignment.status == "Completed"

        # Cleanup
        frappe.delete_doc("Chore Assignment", assignment.name, force=True)
        frappe.delete_doc("Chore Template", template.name, force=True)
```

## 8.3 Frontend Testing (Flutter)

### Unit Tests

```dart
// test/unit/age_utils_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:dartwing_family/core/utils/age_utils.dart';

void main() {
  group('AgeUtils', () {
    test('calculateAge returns correct age', () {
      final today = DateTime.now();
      final dob = DateTime(today.year - 10, today.month, today.day);

      expect(AgeUtils.calculateAge(dob), equals(10));
    });

    test('calculateAge returns correct age before birthday', () {
      final today = DateTime.now();
      final dob = DateTime(today.year - 10, today.month, today.day + 1);

      expect(AgeUtils.calculateAge(dob), equals(9));
    });

    test('getAgeCategory returns correct category', () {
      expect(AgeUtils.getAgeCategory(5), equals('Child'));
      expect(AgeUtils.getAgeCategory(14), equals('Tween'));
      expect(AgeUtils.getAgeCategory(17), equals('Teen'));
      expect(AgeUtils.getAgeCategory(25), equals('Adult'));
    });

    test('isMinor returns true for under 18', () {
      expect(AgeUtils.isMinor(17), isTrue);
      expect(AgeUtils.isMinor(18), isFalse);
    });

    test('isCoppaProtected returns true for under 13', () {
      expect(AgeUtils.isCoppaProtected(12), isTrue);
      expect(AgeUtils.isCoppaProtected(13), isFalse);
    });
  });
}


// test/unit/chore_streak_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:dartwing_family/domain/usecases/chores/calculate_streak.dart';

void main() {
  group('ChoreStreak', () {
    test('calculateStreakBonus returns 0 for less than 7 days', () {
      final calculator = ChoreStreakCalculator();
      expect(calculator.calculateBonus(5), equals(0.0));
    });

    test('calculateStreakBonus returns 0.5 for 7+ days', () {
      final calculator = ChoreStreakCalculator();
      expect(calculator.calculateBonus(7), equals(0.5));
    });

    test('calculateStreakBonus returns 1.0 for 30+ days', () {
      final calculator = ChoreStreakCalculator();
      expect(calculator.calculateBonus(30), equals(1.0));
    });

    test('isStreakBroken detects broken streak', () {
      final calculator = ChoreStreakCalculator();
      final completions = [
        DateTime.now().subtract(Duration(days: 3)),
        DateTime.now().subtract(Duration(days: 2)),
        // Missing day 1
        DateTime.now(),
      ];

      expect(calculator.isStreakBroken(completions), isTrue);
    });
  });
}
```

### Widget Tests

```dart
// test/widget/chore_card_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dartwing_family/presentation/widgets/chores/chore_card.dart';
import 'package:dartwing_family/domain/entities/chore.dart';

void main() {
  group('ChoreCard', () {
    testWidgets('displays chore name and points', (tester) async {
      final chore = ChoreAssignment(
        id: '1',
        choreName: 'Clean Room',
        status: ChoreStatus.pending,
        points: 10,
        money: 2.00,
        dueDate: DateTime.now(),
      );

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: ChoreCard(chore: chore),
            ),
          ),
        ),
      );

      expect(find.text('Clean Room'), findsOneWidget);
      expect(find.text('10 pts'), findsOneWidget);
      expect(find.text('\$2.00'), findsOneWidget);
    });

    testWidgets('shows completed state correctly', (tester) async {
      final chore = ChoreAssignment(
        id: '1',
        choreName: 'Clean Room',
        status: ChoreStatus.completed,
        points: 10,
        money: 2.00,
        dueDate: DateTime.now(),
      );

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: ChoreCard(chore: chore),
            ),
          ),
        ),
      );

      // Should show checkmark icon
      expect(find.byIcon(Icons.check_circle), findsOneWidget);
    });

    testWidgets('tap triggers completion callback', (tester) async {
      bool tapped = false;

      final chore = ChoreAssignment(
        id: '1',
        choreName: 'Clean Room',
        status: ChoreStatus.pending,
        points: 10,
        money: 2.00,
        dueDate: DateTime.now(),
      );

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: ChoreCard(
                chore: chore,
                onComplete: () => tapped = true,
              ),
            ),
          ),
        ),
      );

      await tester.tap(find.text('Mark Complete'));
      await tester.pump();

      expect(tapped, isTrue);
    });
  });
}


// test/widget/family_map_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:dartwing_family/presentation/widgets/location/family_map.dart';
import 'package:dartwing_family/domain/entities/location.dart';

void main() {
  group('FamilyMap', () {
    testWidgets('displays markers for family members', (tester) async {
      final locations = [
        FamilyLocation(
          memberId: '1',
          memberName: 'John',
          latitude: 37.7749,
          longitude: -122.4194,
          timestamp: DateTime.now(),
        ),
        FamilyLocation(
          memberId: '2',
          memberName: 'Jane',
          latitude: 37.7849,
          longitude: -122.4094,
          timestamp: DateTime.now(),
        ),
      ];

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: FamilyMap(locations: locations),
            ),
          ),
        ),
      );

      // Verify map widget exists
      expect(find.byType(GoogleMap), findsOneWidget);
    });

    testWidgets('shows stale location indicator', (tester) async {
      final locations = [
        FamilyLocation(
          memberId: '1',
          memberName: 'John',
          latitude: 37.7749,
          longitude: -122.4194,
          timestamp: DateTime.now().subtract(Duration(hours: 2)),
          isStale: true,
        ),
      ];

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: FamilyMap(locations: locations),
            ),
          ),
        ),
      );

      // Should show stale indicator
      expect(find.text('Location may be outdated'), findsOneWidget);
    });
  });
}
```

### Integration Tests

```dart
// integration_test/chore_flow_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:dartwing_family/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Chore Flow E2E', () {
    testWidgets('complete chore flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Login (assumes test account)
      await tester.enterText(
        find.byKey(Key('email_field')),
        'test_child@example.com',
      );
      await tester.enterText(
        find.byKey(Key('password_field')),
        'testpassword',
      );
      await tester.tap(find.byKey(Key('login_button')));
      await tester.pumpAndSettle();

      // Navigate to chores
      await tester.tap(find.byIcon(Icons.assignment));
      await tester.pumpAndSettle();

      // Find a pending chore
      expect(find.text('Clean Room'), findsOneWidget);

      // Tap to view details
      await tester.tap(find.text('Clean Room'));
      await tester.pumpAndSettle();

      // Take verification photo (mock)
      await tester.tap(find.byKey(Key('take_photo_button')));
      await tester.pumpAndSettle();

      // Submit completion
      await tester.tap(find.text('Mark as Done'));
      await tester.pumpAndSettle();

      // Verify success message
      expect(find.text('Great job!'), findsOneWidget);

      // Verify status changed
      await tester.pageBack();
      await tester.pumpAndSettle();

      expect(find.byIcon(Icons.check_circle), findsOneWidget);
    });
  });
}
```

## 8.4 Security Testing

### Authentication Tests

```python
# dartwing_family/tests/security/test_authentication.py

import pytest
import frappe
from dartwing_family.tests.conftest import test_family


class TestAuthentication:
    """Security tests for authentication system."""

    def test_jwt_token_expiry(self):
        """Test JWT tokens expire correctly."""
        from dartwing_family.auth.jwt_handler import create_jwt_token, verify_jwt_token
        import time

        # Create short-lived token for testing
        token = create_jwt_token("test_user", expiry_minutes=0.1)  # 6 seconds

        # Should be valid immediately
        assert verify_jwt_token(token) is not None

        # Wait for expiry
        time.sleep(7)

        # Should be invalid now
        with pytest.raises(Exception):
            verify_jwt_token(token)

    def test_refresh_token_rotation(self):
        """Test refresh tokens are rotated on use."""
        from dartwing_family.auth.jwt_handler import (
            create_refresh_token,
            use_refresh_token
        )

        refresh_token = create_refresh_token("test_user")

        # Use refresh token
        new_access, new_refresh = use_refresh_token(refresh_token)

        # Old refresh token should be invalid
        with pytest.raises(Exception):
            use_refresh_token(refresh_token)

        # New refresh token should work
        assert use_refresh_token(new_refresh) is not None

    def test_brute_force_protection(self):
        """Test rate limiting on login attempts."""
        from dartwing_family.auth.rate_limiter import check_login_rate_limit

        # Simulate multiple failed attempts
        for i in range(5):
            check_login_rate_limit("test@example.com", success=False)

        # 6th attempt should be blocked
        with pytest.raises(frappe.RateLimitExceededError):
            check_login_rate_limit("test@example.com", success=False)

    def test_password_requirements(self):
        """Test password strength requirements."""
        from dartwing_family.auth.password_validator import validate_password

        # Too short
        assert validate_password("short") is False

        # No numbers
        assert validate_password("NoNumbersHere!") is False

        # No special characters
        assert validate_password("NoSpecial123") is False

        # Valid password
        assert validate_password("SecurePass123!") is True

    def test_session_invalidation(self):
        """Test session invalidation on password change."""
        # Implementation
        pass


class TestAuthorization:
    """Security tests for authorization system."""

    def test_cross_family_access_blocked(self, test_family):
        """Test users cannot access other families' data."""
        # Create another family
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "organization_name": "Other Family",
            "org_type": "Family"
        })
        other_org.insert(ignore_permissions=True)

        other_member = frappe.get_doc({
            "doctype": "Family Member",
            "first_name": "Other",
            "organization": other_org.name
        })
        other_member.insert(ignore_permissions=True)

        # Try to access from test family context
        frappe.flags.current_organization = test_family["organization"]

        # Should raise permission error
        with pytest.raises(frappe.PermissionError):
            frappe.get_doc("Family Member", other_member.name)

        # Cleanup
        frappe.delete_doc("Family Member", other_member.name, force=True)
        frappe.delete_doc("Organization", other_org.name, force=True)

    def test_child_cannot_view_parent_location_history(self, test_family):
        """Test children cannot view parents' location history."""
        # Set child as current user
        frappe.set_user(test_family["child"].user_account or "Guest")

        from dartwing_family.api.location_api import get_location_history

        # Should raise permission error
        with pytest.raises(frappe.PermissionError):
            get_location_history(test_family["parent1"].name)

        frappe.set_user("Administrator")

    def test_coppa_data_access_restrictions(self, test_family):
        """Test COPPA-protected data access restrictions."""
        from dartwing_family.permissions.coppa import COPPACompliance

        compliance = COPPACompliance()

        # Child under 13 should have restricted data access
        assert compliance.is_coppa_protected(test_family["child"]) is True

        # Behavioral data should be blocked
        assert compliance.can_access_data(
            test_family["child"].name,
            "behavioral_data"
        ) is False

        # External sharing should be blocked
        assert compliance.can_access_data(
            test_family["child"].name,
            "external_sharing"
        ) is False
```

### OWASP Security Tests

```python
# dartwing_family/tests/security/test_owasp.py

import pytest
import frappe


class TestInjectionPrevention:
    """Test protection against injection attacks."""

    def test_sql_injection_in_filters(self):
        """Test SQL injection prevention in API filters."""
        malicious_input = "'; DROP TABLE `tabFamily Member`; --"

        # Should safely escape the input
        members = frappe.get_all(
            "Family Member",
            filters={"first_name": malicious_input}
        )

        # Table should still exist
        assert frappe.db.table_exists("tabFamily Member")

    def test_xss_in_user_content(self):
        """Test XSS prevention in user-generated content."""
        from dartwing_family.utils.sanitizer import sanitize_html

        malicious_input = '<script>alert("xss")</script>Hello'
        sanitized = sanitize_html(malicious_input)

        assert '<script>' not in sanitized
        assert 'Hello' in sanitized

    def test_path_traversal_in_file_access(self):
        """Test path traversal prevention."""
        from dartwing_family.utils.file_handler import safe_file_path

        malicious_path = "../../../etc/passwd"

        with pytest.raises(ValueError):
            safe_file_path(malicious_path)


class TestDataProtection:
    """Test data protection measures."""

    def test_sensitive_fields_encrypted(self):
        """Test sensitive fields are encrypted at rest."""
        member = frappe.get_doc({
            "doctype": "Family Member",
            "first_name": "Test",
            "date_of_birth": "2015-01-01",
            "organization": "test_org"
        })
        member.insert(ignore_permissions=True)

        # Check raw database value
        raw_dob = frappe.db.sql(
            "SELECT date_of_birth FROM `tabFamily Member` WHERE name = %s",
            member.name
        )

        # Should be encrypted (not plain text date)
        # Implementation depends on encryption method

        frappe.delete_doc("Family Member", member.name, force=True)

    def test_audit_log_created(self, test_family):
        """Test audit logs are created for sensitive actions."""
        from dartwing_family.api.location_api import get_member_location

        # View location (sensitive action)
        frappe.set_user(test_family["parent1"].user_account)
        get_member_location(test_family["child"].name)

        # Check audit log exists
        log = frappe.get_last_doc(
            "Family Audit Log",
            filters={
                "action": "view_location",
                "target_member": test_family["child"].name
            }
        )

        assert log is not None
        assert log.actor_member == test_family["parent1"].name

        frappe.set_user("Administrator")
```

## 8.5 Performance Testing

```python
# dartwing_family/tests/performance/test_api_performance.py

import pytest
import time
import frappe
from concurrent.futures import ThreadPoolExecutor


class TestAPIPerformance:
    """Performance tests for API endpoints."""

    @pytest.mark.performance
    def test_dashboard_load_time(self, test_family, authenticated_parent):
        """Dashboard should load in under 500ms."""
        from dartwing_family.api.family_api import get_family_dashboard

        start = time.time()
        get_family_dashboard()
        elapsed = time.time() - start

        assert elapsed < 0.5, f"Dashboard took {elapsed:.2f}s"

    @pytest.mark.performance
    def test_location_query_performance(self, test_family):
        """Location queries should handle many records efficiently."""
        # Create 1000 location records
        for i in range(1000):
            frappe.get_doc({
                "doctype": "Location History",
                "family_member": test_family["child"].name,
                "latitude": 37.7749 + (i * 0.0001),
                "longitude": -122.4194,
                "timestamp": frappe.utils.add_days(frappe.utils.now(), -i/24)
            }).insert(ignore_permissions=True)

        frappe.db.commit()

        # Query should be fast
        start = time.time()
        locations = frappe.get_all(
            "Location History",
            filters={
                "family_member": test_family["child"].name,
                "timestamp": [">=", frappe.utils.add_days(frappe.utils.now(), -7)]
            },
            order_by="timestamp desc",
            limit=100
        )
        elapsed = time.time() - start

        assert elapsed < 0.1, f"Query took {elapsed:.2f}s"

        # Cleanup
        frappe.db.sql(
            "DELETE FROM `tabLocation History` WHERE family_member = %s",
            test_family["child"].name
        )

    @pytest.mark.performance
    def test_concurrent_requests(self, test_family):
        """API should handle concurrent requests."""
        from dartwing_family.api.family_api import get_family_dashboard

        def make_request():
            return get_family_dashboard()

        start = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [f.result() for f in futures]

        elapsed = time.time() - start

        # 50 concurrent requests should complete in under 5 seconds
        assert elapsed < 5, f"Concurrent requests took {elapsed:.2f}s"
        assert all(r is not None for r in results)


# Load testing script (run separately)
# dartwing_family/tests/performance/locustfile.py

from locust import HttpUser, task, between


class FamilyUser(HttpUser):
    """Simulated family app user for load testing."""

    wait_time = between(1, 3)

    def on_start(self):
        """Login on start."""
        self.client.post("/api/method/login", {
            "usr": "test@example.com",
            "pwd": "testpassword"
        })

    @task(3)
    def view_dashboard(self):
        """Most common action: view dashboard."""
        self.client.get("/api/method/dartwing_family.api.family_api.get_family_dashboard")

    @task(2)
    def view_chores(self):
        """View chores list."""
        self.client.get("/api/method/dartwing_family.api.chore_api.get_my_chores")

    @task(1)
    def view_calendar(self):
        """View calendar."""
        self.client.get("/api/method/dartwing_family.api.calendar_api.get_today_events")

    @task(1)
    def update_location(self):
        """Update location."""
        self.client.post(
            "/api/method/dartwing_family.api.location_api.update_location",
            json={
                "latitude": 37.7749,
                "longitude": -122.4194,
                "accuracy": 10
            }
        )
```

## 8.6 CI/CD Test Configuration

```yaml
# .github/workflows/test.yml

name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    services:
      mariadb:
        image: mariadb:10.6
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_dartwing
        ports:
          - 3306:3306

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install frappe-bench
          bench init --frappe-branch version-15 frappe-bench
          cd frappe-bench
          bench get-app dartwing_family $GITHUB_WORKSPACE
          bench setup requirements

      - name: Setup test site
        run: |
          cd frappe-bench
          bench new-site test_site --db-root-password root --admin-password admin
          bench --site test_site install-app dartwing_family

      - name: Run unit tests
        run: |
          cd frappe-bench
          bench --site test_site run-tests --app dartwing_family --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frappe-bench/sites/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: "3.16.0"

      - name: Install dependencies
        working-directory: ./mobile
        run: flutter pub get

      - name: Run unit tests
        working-directory: ./mobile
        run: flutter test --coverage

      - name: Run widget tests
        working-directory: ./mobile
        run: flutter test test/widget/

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./mobile/coverage/lcov.info

  integration-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]

    steps:
      - uses: actions/checkout@v3

      - name: Setup test environment
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 30  # Wait for services

      - name: Run API integration tests
        run: |
          cd frappe-bench
          bench --site test_site run-tests \
            --app dartwing_family \
            --module dartwing_family.tests.integration

      - name: Run E2E tests
        working-directory: ./mobile
        run: |
          flutter drive \
            --driver=test_driver/integration_test.dart \
            --target=integration_test/app_test.dart

      - name: Cleanup
        if: always()
        run: docker-compose -f docker-compose.test.yml down

  security-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run Bandit security scan
        run: |
          pip install bandit
          bandit -r dartwing_family/ -f json -o bandit-report.json

      - name: Run dependency check
        run: |
          pip install safety
          safety check --full-report

      - name: Upload security report
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: bandit-report.json
```

---

_End of Section 8: Testing & Quality Assurance Architecture_

**Next Section:** Section 9 - Deployment & DevOps Architecture

# Section 9: Deployment & DevOps Architecture

## 9.1 Infrastructure Overview

Dartwing Family uses a cloud-native architecture designed for scalability, reliability, and security:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PRODUCTION INFRASTRUCTURE                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         CDN / EDGE LAYER                             │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  CloudFlare  │  │   WAF        │  │   DDoS       │              │    │
│  │  │  CDN         │  │   Rules      │  │   Protection │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      LOAD BALANCER LAYER                             │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │              Azure Application Gateway / AWS ALB              │   │    │
│  │  │         SSL Termination │ Path Routing │ Health Checks        │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   WEB SERVERS   │    │  SOCKET.IO      │    │   BACKGROUND    │         │
│  │   (Gunicorn)    │    │  CLUSTER        │    │   WORKERS       │         │
│  │                 │    │                 │    │                 │         │
│  │ • REST API      │    │ • Real-time     │    │ • RQ Workers    │         │
│  │ • Web UI        │    │ • WebSocket     │    │ • Scheduler     │         │
│  │ • 3 replicas    │    │ • 2 replicas    │    │ • 4 workers     │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│         │                          │                          │             │
│         └──────────────────────────┼──────────────────────────┘             │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         DATA LAYER                                   │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  MariaDB     │  │    Redis     │  │   Object     │              │    │
│  │  │  Primary +   │  │   Cluster    │  │   Storage    │              │    │
│  │  │  Replica     │  │   (3 nodes)  │  │   (Azure/S3) │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │  TimescaleDB │  │   Qdrant     │                                │    │
│  │  │  (Time-series)│  │  (Vector DB) │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     MONITORING & OBSERVABILITY                       │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Prometheus  │  │   Grafana    │  │    Loki      │              │    │
│  │  │  Metrics     │  │  Dashboards  │  │    Logs      │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │   Jaeger     │  │   PagerDuty  │                                │    │
│  │  │   Tracing    │  │   Alerts     │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 9.2 Kubernetes Deployment

### Namespace and Resource Configuration

```yaml
# kubernetes/base/namespace.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: dartwing-family
  labels:
    app.kubernetes.io/name: dartwing-family
    app.kubernetes.io/part-of: dartwing

---
# kubernetes/base/resource-quotas.yaml

apiVersion: v1
kind: ResourceQuota
metadata:
  name: dartwing-family-quota
  namespace: dartwing-family
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 16Gi
    limits.cpu: "16"
    limits.memory: 32Gi
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"

---
# kubernetes/base/limit-range.yaml

apiVersion: v1
kind: LimitRange
metadata:
  name: dartwing-family-limits
  namespace: dartwing-family
spec:
  limits:
    - default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      type: Container
```

### Web Server Deployment

```yaml
# kubernetes/deployments/web.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-web
  namespace: dartwing-family
  labels:
    app: dartwing-web
    component: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dartwing-web
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: dartwing-web
        component: web
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      serviceAccountName: dartwing-web

      initContainers:
        - name: wait-for-db
          image: busybox:1.35
          command:
            ["sh", "-c", "until nc -z mariadb-primary 3306; do sleep 2; done"]

        - name: wait-for-redis
          image: busybox:1.35
          command:
            ["sh", "-c", "until nc -z redis-master 6379; do sleep 2; done"]

      containers:
        - name: web
          image: dartwing/family:${IMAGE_TAG}
          imagePullPolicy: Always

          ports:
            - name: http
              containerPort: 8000
              protocol: TCP

          env:
            - name: FRAPPE_SITE
              value: "dartwing.app"
            - name: WORKERS
              value: "4"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: dartwing-config
                  key: redis_url
            - name: ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: dartwing-secrets
                  key: encryption_key

          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "2Gi"

          livenessProbe:
            httpGet:
              path: /api/method/ping
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /api/method/ping
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites
            - name: logs
              mountPath: /home/frappe/frappe-bench/logs

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc
        - name: logs
          emptyDir: {}

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: dartwing-web
                topologyKey: kubernetes.io/hostname

      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: dartwing-web

---
# kubernetes/deployments/web-service.yaml

apiVersion: v1
kind: Service
metadata:
  name: dartwing-web
  namespace: dartwing-family
  labels:
    app: dartwing-web
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
      name: http
  selector:
    app: dartwing-web
```

### Socket.IO Deployment

```yaml
# kubernetes/deployments/socketio.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-socketio
  namespace: dartwing-family
  labels:
    app: dartwing-socketio
    component: realtime
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dartwing-socketio
  template:
    metadata:
      labels:
        app: dartwing-socketio
        component: realtime
    spec:
      containers:
        - name: socketio
          image: dartwing/family-socketio:${IMAGE_TAG}
          imagePullPolicy: Always

          ports:
            - name: socketio
              containerPort: 9000
              protocol: TCP

          env:
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: dartwing-config
                  key: redis_url
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: dartwing-secrets
                  key: jwt_secret

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "1Gi"

          livenessProbe:
            httpGet:
              path: /health
              port: 9000
            initialDelaySeconds: 10
            periodSeconds: 10

          readinessProbe:
            httpGet:
              path: /health
              port: 9000
            initialDelaySeconds: 5
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: dartwing-socketio
  namespace: dartwing-family
spec:
  type: ClusterIP
  ports:
    - port: 9000
      targetPort: 9000
      protocol: TCP
      name: socketio
  selector:
    app: dartwing-socketio
```

### Background Workers Deployment

```yaml
# kubernetes/deployments/workers.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-worker-default
  namespace: dartwing-family
  labels:
    app: dartwing-worker
    queue: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dartwing-worker
      queue: default
  template:
    metadata:
      labels:
        app: dartwing-worker
        queue: default
    spec:
      containers:
        - name: worker
          image: dartwing/family:${IMAGE_TAG}
          command: ["bench", "worker", "--queue", "default"]

          env:
            - name: FRAPPE_SITE
              value: "dartwing.app"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: dartwing-config
                  key: redis_url

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "1Gi"

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-worker-long
  namespace: dartwing-family
  labels:
    app: dartwing-worker
    queue: long
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dartwing-worker
      queue: long
  template:
    metadata:
      labels:
        app: dartwing-worker
        queue: long
    spec:
      containers:
        - name: worker
          image: dartwing/family:${IMAGE_TAG}
          command: ["bench", "worker", "--queue", "long"]

          env:
            - name: FRAPPE_SITE
              value: "dartwing.app"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: dartwing-config
                  key: redis_url

          resources:
            requests:
              cpu: "200m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "2Gi"

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc

---
# Scheduler deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-scheduler
  namespace: dartwing-family
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dartwing-scheduler
  template:
    metadata:
      labels:
        app: dartwing-scheduler
    spec:
      containers:
        - name: scheduler
          image: dartwing/family:${IMAGE_TAG}
          command: ["bench", "schedule"]

          env:
            - name: FRAPPE_SITE
              value: "dartwing.app"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: dartwing-config
                  key: redis_url

          resources:
            requests:
              cpu: "50m"
              memory: "128Mi"
            limits:
              cpu: "200m"
              memory: "512Mi"

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc
```

### Ingress Configuration

```yaml
# kubernetes/ingress/ingress.yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dartwing-ingress
  namespace: dartwing-family
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/websocket-services: "dartwing-socketio"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts:
        - api.dartwing.app
        - app.dartwing.app
      secretName: dartwing-tls
  rules:
    - host: api.dartwing.app
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: dartwing-web
                port:
                  number: 80

          - path: /socket.io
            pathType: Prefix
            backend:
              service:
                name: dartwing-socketio
                port:
                  number: 9000

    - host: app.dartwing.app
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: dartwing-web
                port:
                  number: 80
```

## 9.3 Database Configuration

### MariaDB StatefulSet

```yaml
# kubernetes/database/mariadb.yaml

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mariadb
  namespace: dartwing-family
spec:
  serviceName: mariadb
  replicas: 2 # Primary + Replica
  selector:
    matchLabels:
      app: mariadb
  template:
    metadata:
      labels:
        app: mariadb
    spec:
      containers:
        - name: mariadb
          image: mariadb:10.6

          ports:
            - name: mysql
              containerPort: 3306

          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: root_password
            - name: MYSQL_DATABASE
              value: "dartwing"
            - name: MYSQL_USER
              value: "dartwing"
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password

          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2000m"
              memory: "4Gi"

          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
            - name: config
              mountPath: /etc/mysql/conf.d

          livenessProbe:
            exec:
              command:
                - mysqladmin
                - ping
                - -h
                - localhost
            initialDelaySeconds: 30
            periodSeconds: 10

          readinessProbe:
            exec:
              command:
                - mysql
                - -h
                - localhost
                - -e
                - "SELECT 1"
            initialDelaySeconds: 5
            periodSeconds: 5

      volumes:
        - name: config
          configMap:
            name: mariadb-config

  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 100Gi

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mariadb-config
  namespace: dartwing-family
data:
  custom.cnf: |
    [mysqld]
    # Performance
    innodb_buffer_pool_size = 2G
    innodb_log_file_size = 512M
    innodb_flush_log_at_trx_commit = 2
    innodb_flush_method = O_DIRECT

    # Character set
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci

    # Connections
    max_connections = 500
    wait_timeout = 600

    # Query cache (disabled in MariaDB 10.4+)
    query_cache_type = 0

    # Logging
    slow_query_log = 1
    slow_query_log_file = /var/lib/mysql/slow.log
    long_query_time = 2

---
apiVersion: v1
kind: Service
metadata:
  name: mariadb-primary
  namespace: dartwing-family
spec:
  type: ClusterIP
  ports:
    - port: 3306
      targetPort: 3306
  selector:
    app: mariadb
    statefulset.kubernetes.io/pod-name: mariadb-0
```

### Redis Cluster

```yaml
# kubernetes/database/redis.yaml

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: dartwing-family
spec:
  serviceName: redis
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine

          ports:
            - name: redis
              containerPort: 6379
            - name: cluster
              containerPort: 16379

          command:
            - redis-server
            - /etc/redis/redis.conf

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "1Gi"

          volumeMounts:
            - name: data
              mountPath: /data
            - name: config
              mountPath: /etc/redis

          livenessProbe:
            exec:
              command: ["redis-cli", "ping"]
            initialDelaySeconds: 15
            periodSeconds: 5

          readinessProbe:
            exec:
              command: ["redis-cli", "ping"]
            initialDelaySeconds: 5
            periodSeconds: 3

      volumes:
        - name: config
          configMap:
            name: redis-config

  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 10Gi

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: dartwing-family
data:
  redis.conf: |
    # Memory
    maxmemory 512mb
    maxmemory-policy allkeys-lru

    # Persistence
    appendonly yes
    appendfsync everysec

    # Security
    protected-mode yes

    # Cluster
    cluster-enabled no

    # Performance
    tcp-keepalive 300
    timeout 0

---
apiVersion: v1
kind: Service
metadata:
  name: redis-master
  namespace: dartwing-family
spec:
  type: ClusterIP
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    app: redis
    statefulset.kubernetes.io/pod-name: redis-0
```

## 9.4 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml

name: Build and Deploy

on:
  push:
    branches:
      - main
      - develop
    tags:
      - "v*"
  pull_request:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: dartwing/family

jobs:
  # ─── BUILD ────────────────────────────────────────────────────────────
  build:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VCS_REF=${{ github.sha }}

  # ─── TEST ─────────────────────────────────────────────────────────────
  test:
    needs: build
    runs-on: ubuntu-latest

    services:
      mariadb:
        image: mariadb:10.6
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_dartwing
        ports:
          - 3306:3306

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Run tests
        run: |
          pip install -r requirements-dev.txt
          pytest tests/ --cov=dartwing_family --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  # ─── SECURITY SCAN ────────────────────────────────────────────────────
  security:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: "sarif"
          output: "trivy-results.sarif"

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: "trivy-results.sarif"

  # ─── DEPLOY STAGING ───────────────────────────────────────────────────
  deploy-staging:
    needs: [build, test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.STAGING_KUBECONFIG }}" | base64 -d > ~/.kube/config

      - name: Deploy to staging
        run: |
          export IMAGE_TAG=${{ github.sha }}
          envsubst < kubernetes/deployments/web.yaml | kubectl apply -f -
          envsubst < kubernetes/deployments/workers.yaml | kubectl apply -f -
          envsubst < kubernetes/deployments/socketio.yaml | kubectl apply -f -

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/dartwing-web -n dartwing-family-staging
          kubectl rollout status deployment/dartwing-socketio -n dartwing-family-staging

      - name: Run smoke tests
        run: |
          ./scripts/smoke-test.sh https://staging.dartwing.app

  # ─── DEPLOY PRODUCTION ────────────────────────────────────────────────
  deploy-production:
    needs: [build, test, security]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.PROD_KUBECONFIG }}" | base64 -d > ~/.kube/config

      - name: Create backup
        run: |
          kubectl exec -n dartwing-family mariadb-0 -- \
            mysqldump -u root -p${{ secrets.DB_PASSWORD }} dartwing > backup.sql

          aws s3 cp backup.sql s3://dartwing-backups/pre-deploy/$(date +%Y%m%d_%H%M%S).sql

      - name: Deploy to production
        run: |
          export IMAGE_TAG=${GITHUB_REF#refs/tags/}
          envsubst < kubernetes/deployments/web.yaml | kubectl apply -f -
          envsubst < kubernetes/deployments/workers.yaml | kubectl apply -f -
          envsubst < kubernetes/deployments/socketio.yaml | kubectl apply -f -

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/dartwing-web -n dartwing-family
          kubectl rollout status deployment/dartwing-socketio -n dartwing-family

      - name: Run smoke tests
        run: |
          ./scripts/smoke-test.sh https://api.dartwing.app

      - name: Notify on success
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Dartwing Family ${GITHUB_REF#refs/tags/} deployed to production"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

      - name: Rollback on failure
        if: failure()
        run: |
          kubectl rollout undo deployment/dartwing-web -n dartwing-family
          kubectl rollout undo deployment/dartwing-socketio -n dartwing-family
```

### Database Migration Job

```yaml
# kubernetes/jobs/migrate.yaml

apiVersion: batch/v1
kind: Job
metadata:
  name: dartwing-migrate-${TIMESTAMP}
  namespace: dartwing-family
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: OnFailure

      containers:
        - name: migrate
          image: dartwing/family:${IMAGE_TAG}
          command:
            - /bin/bash
            - -c
            - |
              bench --site dartwing.app migrate
              bench --site dartwing.app clear-cache

          env:
            - name: FRAPPE_SITE
              value: "dartwing.app"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc
```

## 9.5 Monitoring & Observability

### Prometheus ServiceMonitor

```yaml
# kubernetes/monitoring/servicemonitor.yaml

apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: dartwing-monitor
  namespace: dartwing-family
  labels:
    app: dartwing
spec:
  selector:
    matchLabels:
      app: dartwing-web
  endpoints:
    - port: http
      path: /api/method/frappe.monitor.get_metrics
      interval: 30s
      scrapeTimeout: 10s

---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: dartwing-alerts
  namespace: dartwing-family
spec:
  groups:
    - name: dartwing.rules
      rules:
        - alert: HighErrorRate
          expr: |
            sum(rate(http_requests_total{app="dartwing-web",status=~"5.."}[5m]))
            / sum(rate(http_requests_total{app="dartwing-web"}[5m])) > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: High error rate detected
            description: Error rate is {{ $value | humanizePercentage }}

        - alert: HighLatency
          expr: |
            histogram_quantile(0.95,
              sum(rate(http_request_duration_seconds_bucket{app="dartwing-web"}[5m]))
              by (le)) > 2
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: High API latency
            description: P95 latency is {{ $value | humanizeDuration }}

        - alert: WorkerQueueBacklog
          expr: rq_queue_length{queue="default"} > 1000
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: Worker queue backlog
            description: Queue has {{ $value }} pending jobs

        - alert: DatabaseConnectionsHigh
          expr: mysql_global_status_threads_connected > 400
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: High database connections
            description: {{ $value }} active connections
```

### Grafana Dashboard

```yaml
# kubernetes/monitoring/grafana-dashboard.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: dartwing-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  dartwing-dashboard.json: |
    {
      "dashboard": {
        "title": "Dartwing Family",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{app=\"dartwing-web\"}[5m]))",
                "legendFormat": "Requests/s"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{app=\"dartwing-web\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{app=\"dartwing-web\"}[5m]))",
                "legendFormat": "Error Rate"
              }
            ]
          },
          {
            "title": "Response Time (P95)",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app=\"dartwing-web\"}[5m])) by (le))",
                "legendFormat": "P95 Latency"
              }
            ]
          },
          {
            "title": "Active Users",
            "type": "stat",
            "targets": [
              {
                "expr": "dartwing_active_sessions",
                "legendFormat": "Active Sessions"
              }
            ]
          },
          {
            "title": "Worker Queue Length",
            "type": "graph",
            "targets": [
              {
                "expr": "rq_queue_length{app=\"dartwing-worker\"}",
                "legendFormat": "{{queue}}"
              }
            ]
          },
          {
            "title": "Database Connections",
            "type": "graph",
            "targets": [
              {
                "expr": "mysql_global_status_threads_connected{app=\"mariadb\"}",
                "legendFormat": "Connections"
              }
            ]
          }
        ]
      }
    }
```

## 9.6 Backup & Disaster Recovery

### Backup CronJob

```yaml
# kubernetes/backup/backup-cronjob.yaml

apiVersion: batch/v1
kind: CronJob
metadata:
  name: dartwing-backup
  namespace: dartwing-family
spec:
  schedule: "0 2 * * *" # Daily at 2 AM
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1

  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure

          containers:
            - name: backup
              image: dartwing/backup:latest

              env:
                - name: DB_HOST
                  valueFrom:
                    secretKeyRef:
                      name: dartwing-db-credentials
                      key: host
                - name: DB_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: dartwing-db-credentials
                      key: password
                - name: S3_BUCKET
                  value: "dartwing-backups"
                - name: AWS_ACCESS_KEY_ID
                  valueFrom:
                    secretKeyRef:
                      name: aws-credentials
                      key: access_key
                - name: AWS_SECRET_ACCESS_KEY
                  valueFrom:
                    secretKeyRef:
                      name: aws-credentials
                      key: secret_key
                - name: ENCRYPTION_KEY
                  valueFrom:
                    secretKeyRef:
                      name: dartwing-secrets
                      key: backup_encryption_key

              command:
                - /bin/bash
                - -c
                - |
                  set -e

                  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                  BACKUP_DIR="/tmp/backup_${TIMESTAMP}"
                  mkdir -p ${BACKUP_DIR}

                  echo "Starting database backup..."
                  mysqldump -h ${DB_HOST} -u dartwing -p${DB_PASSWORD} \
                    --single-transaction --routines --triggers \
                    dartwing > ${BACKUP_DIR}/database.sql

                  echo "Starting files backup..."
                  tar -czf ${BACKUP_DIR}/files.tar.gz \
                    /home/frappe/frappe-bench/sites/dartwing.app/private \
                    /home/frappe/frappe-bench/sites/dartwing.app/public

                  echo "Encrypting backup..."
                  tar -czf - -C ${BACKUP_DIR} . | \
                    openssl enc -aes-256-cbc -salt -pbkdf2 \
                    -pass env:ENCRYPTION_KEY \
                    -out /tmp/dartwing_backup_${TIMESTAMP}.tar.gz.enc

                  echo "Uploading to S3..."
                  aws s3 cp /tmp/dartwing_backup_${TIMESTAMP}.tar.gz.enc \
                    s3://${S3_BUCKET}/daily/

                  echo "Cleaning up old backups..."
                  aws s3 ls s3://${S3_BUCKET}/daily/ | \
                    sort -r | tail -n +31 | \
                    awk '{print $4}' | \
                    xargs -I {} aws s3 rm s3://${S3_BUCKET}/daily/{}

                  echo "Backup complete!"

              volumeMounts:
                - name: sites
                  mountPath: /home/frappe/frappe-bench/sites
                  readOnly: true

          volumes:
            - name: sites
              persistentVolumeClaim:
                claimName: dartwing-sites-pvc
```

### Disaster Recovery Procedure

```yaml
# kubernetes/backup/restore-job.yaml

apiVersion: batch/v1
kind: Job
metadata:
  name: dartwing-restore
  namespace: dartwing-family
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never

      containers:
        - name: restore
          image: dartwing/backup:latest

          env:
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: dartwing-db-credentials
                  key: password
            - name: S3_BUCKET
              value: "dartwing-backups"
            - name: BACKUP_FILE
              value: "${BACKUP_FILE}" # Set when creating job
            - name: ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: dartwing-secrets
                  key: backup_encryption_key

          command:
            - /bin/bash
            - -c
            - |
              set -e

              echo "Downloading backup from S3..."
              aws s3 cp s3://${S3_BUCKET}/${BACKUP_FILE} /tmp/backup.tar.gz.enc

              echo "Decrypting backup..."
              openssl enc -aes-256-cbc -d -pbkdf2 \
                -pass env:ENCRYPTION_KEY \
                -in /tmp/backup.tar.gz.enc | \
                tar -xzf - -C /tmp/restore

              echo "Restoring database..."
              mysql -h ${DB_HOST} -u dartwing -p${DB_PASSWORD} \
                dartwing < /tmp/restore/database.sql

              echo "Restoring files..."
              tar -xzf /tmp/restore/files.tar.gz -C /

              echo "Running migrations..."
              cd /home/frappe/frappe-bench
              bench --site dartwing.app migrate
              bench --site dartwing.app clear-cache

              echo "Restore complete!"

          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites

      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: dartwing-sites-pvc
```

## 9.7 Environment Configuration

### ConfigMaps and Secrets

```yaml
# kubernetes/config/configmap.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: dartwing-config
  namespace: dartwing-family
data:
  redis_url: "redis://redis-master:6379"
  socketio_url: "http://dartwing-socketio:9000"
  site_name: "dartwing.app"

  # Feature flags
  enable_voice_assistant: "true"
  enable_home_automation: "true"
  enable_driving_monitor: "true"

  # Limits
  max_family_members: "20"
  max_chores_per_day: "50"
  location_history_days: "30"

---
apiVersion: v1
kind: Secret
metadata:
  name: dartwing-secrets
  namespace: dartwing-family
type: Opaque
stringData:
  encryption_key: "${ENCRYPTION_KEY}"
  jwt_secret: "${JWT_SECRET}"
  backup_encryption_key: "${BACKUP_ENCRYPTION_KEY}"

  # External API keys
  elevenlabs_api_key: "${ELEVENLABS_API_KEY}"
  openai_api_key: "${OPENAI_API_KEY}"
  google_client_id: "${GOOGLE_CLIENT_ID}"
  google_client_secret: "${GOOGLE_CLIENT_SECRET}"

---
apiVersion: v1
kind: Secret
metadata:
  name: dartwing-db-credentials
  namespace: dartwing-family
type: Opaque
stringData:
  host: "mariadb-primary"
  port: "3306"
  database: "dartwing"
  username: "dartwing"
  password: "${DB_PASSWORD}"
  root_password: "${DB_ROOT_PASSWORD}"
```

---

_End of Section 9: Deployment & DevOps Architecture_

**All Sections Complete!**

The Dartwing Family Architecture Documentation now consists of:

1. System Architecture Overview
2. Data Model Architecture
3. Permission & Access Control Architecture
4. Integration Architecture
5. Mobile Application Architecture
6. Voice Assistant & AI Integration Architecture
7. Background Services & Scheduled Tasks
8. Testing & Quality Assurance Architecture
9. Deployment & DevOps Architecture

**Next Step:** Combine all sections into a single comprehensive document.
