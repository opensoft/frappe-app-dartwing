# Architecture Document: Dartwing Fax Module

**Version:** 1.0
**Date:** November 23, 2025
**Author:** Dartwing Architecture Team
**Status:** Draft
**Related Documents:** [PRD: Dartwing Digital Fax System](prd_dartwing_fax.md)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Module Structure](#3-module-structure)
4. [DocType Architecture](#4-doctype-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Component Architecture](#6-component-architecture)
7. [Data Flow](#7-data-flow)
8. [Integration Architecture](#8-integration-architecture)
9. [Security Architecture](#9-security-architecture)
10. [Deployment Architecture](#10-deployment-architecture)
11. [Development Phases](#11-development-phases)

---

## 1. Executive Summary

This document defines the technical architecture for the Dartwing Fax Module (`dartwing_fax`), a comprehensive digital fax solution built on the Frappe Framework. The module implements AI-powered routing, document annotation, three-tier security validation, and robust audit capabilities.

### 1.1 Architecture Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Modularity** | Clear separation of concerns | Separate DocTypes for each domain (Fax, Routing, Security, Annotation) |
| **Scalability** | Horizontal scaling capability | Background workers for AI processing, queue-based architecture |
| **Security** | Defense in depth | Three-tier validation, encryption at rest/transit, audit logging |
| **Maintainability** | Clean code, clear interfaces | Frappe best practices, documented APIs, type hints |
| **Extensibility** | Plugin architecture | Webhook system, custom routing rules, provider abstraction |

### 1.2 Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    Frappe Framework v15                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │  Dartwing  │  │  Dartwing  │  │   Dartwing Fax       │  │
│  │    Core    │  │    Ops     │  │   (NEW MODULE)       │  │
│  └────────────┘  └────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
│
├─── Python 3.10+ (Application Logic)
├─── MariaDB 10.6+ (Primary Database)
├─── Redis (Cache, Queue, Pub/Sub)
├─── TensorFlow/PyTorch (AI/ML Models)
├─── Tesseract OCR (Document OCR)
├─── Celery/RQ (Background Jobs)
├─── S3-compatible Storage (Document Storage)
└─── Nginx (Reverse Proxy)
```

---

## 2. System Overview

### 2.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐     │
│  │ Web Browser │  │ Mobile App  │  │  External Systems    │     │
│  │   (Desk)    │  │  (Future)   │  │  (API/Webhooks)      │     │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘     │
└─────────┼─────────────────┼──────────────────────┼───────────────┘
          │                 │                      │
          └─────────────────┼──────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────┐
│                      APPLICATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              Frappe Framework (Python/Jinja)                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │              Dartwing Fax Module                         │ │ │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │ │ │
│  │  │  │   Fax    │ │ Routing  │ │ Security │ │Annotation │  │ │ │
│  │  │  │Management│ │  Engine  │ │  Engine  │ │  Engine   │  │ │ │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬───────────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────┐
│                      PROCESSING LAYER                              │
│  ┌───────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐ │
│  │    AI     │  │    OCR     │  │   Queue    │  │  Background │ │
│  │  Engine   │  │  Engine    │  │  Manager   │  │   Workers   │ │
│  │(TF/PyT)   │  │(Tesseract) │  │  (Redis)   │  │    (RQ)     │ │
│  └───────────┘  └────────────┘  └────────────┘  └─────────────┘ │
└───────────────────────────┬───────────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────┐
│                        DATA LAYER                                  │
│  ┌───────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐ │
│  │  MariaDB  │  │   Redis    │  │ S3 Storage │  │  External   │ │
│  │(Metadata) │  │  (Cache)   │  │(Documents) │  │  Services   │ │
│  └───────────┘  └────────────┘  └────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow Example: Incoming Fax

```
┌─────────────┐
│ Fax Provider│ (Webhook)
│   (SRFax)   │
└──────┬──────┘
       │ 1. POST /api/fax/receive
       ▼
┌─────────────────────────┐
│  Fax Receive Endpoint   │ (API Handler)
└──────┬──────────────────┘
       │ 2. Create Fax Document (pending)
       ▼
┌─────────────────────────┐
│  Validation Engine      │ (Tier 1: Whitelist/Blacklist)
└──────┬──────────────────┘
       │ 3. If not in lists → Queue for AI
       ▼
┌─────────────────────────┐
│  Background Worker      │ (RQ Job)
│  - OCR Processing       │
│  - AI Classification    │
│  - Spam Scoring         │
└──────┬──────────────────┘
       │ 4. Return score & category
       ▼
┌─────────────────────────┐
│  Routing Engine         │ (Apply rules)
└──────┬──────────────────┘
       │ 5. Assign to user/queue
       ▼
┌─────────────────────────┐
│  Notification Service   │ (Email/SMS)
└──────┬──────────────────┘
       │ 6. Notify recipient
       ▼
┌─────────────────────────┐
│  User Inbox             │ (Frappe Desk)
└─────────────────────────┘
```

---

## 3. Module Structure

### 3.1 Frappe Module: `dartwing_fax`

The Dartwing Fax functionality will be implemented as a new Frappe module within the Dartwing app.

**Location:** `apps/dartwing/dartwing/dartwing_fax/`

**Registration:**
```python
# apps/dartwing/dartwing/modules.txt
Dartwing Core
Dartwing Ops
Dartwing Billing
Dartwing Fax         # ← NEW MODULE
```

### 3.2 Module Components

| Component Type | Count | Purpose |
|----------------|-------|---------|
| **DocTypes** | 15 | Core data models (Fax Document, Routing Rule, etc.) |
| **API Endpoints** | 25+ | REST API for external integrations |
| **Background Jobs** | 8 | Async processing (OCR, AI, sending) |
| **Web Forms** | 5 | User-facing forms (Send Fax, Settings) |
| **Reports** | 6 | Analytics and audit reports |
| **Dashboards** | 2 | Inbox Dashboard, Admin Dashboard |
| **Hooks** | 10+ | Document lifecycle, scheduler, notifications |

---

## 4. DocType Architecture

### 4.1 Core DocTypes

#### 4.1.1 Fax Document
**DocType Name:** `Fax Document`
**Naming:** Auto-name with format `FAX-{YYYY}-{#####}`
**Submittable:** No
**Track Changes:** Yes
**Permissions:** Based on assigned user/group

**Fields:**

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `fax_id` | Data | Yes | Unique identifier (auto-generated) |
| `direction` | Select | Yes | Inbound / Outbound |
| `sender_number` | Data | Yes | E.164 format phone number |
| `sender_name` | Data | No | Extracted from CNID |
| `recipient_number` | Data | Yes | DID number |
| `received_at` / `sent_at` | Datetime | Yes | Transmission timestamp |
| `status` | Select | Yes | Pending / Held / Delivered / Rejected / Failed |
| `validation_status` | Select | No | Whitelisted / Blacklisted / Validated / Pending Challenge / Failed Challenge |
| `spam_score` | Float | No | 0-100 (from AI) |
| `ai_category` | Link | No | → Fax Category |
| `ai_confidence` | Float | No | 0-100 |
| `pages` | Int | Yes | Number of pages |
| `file_size` | Int | Yes | Bytes |
| `original_file` | Attach | Yes | Original TIFF/PDF |
| `ocr_text` | Long Text | No | Extracted text content |
| `entities_extracted` | JSON | No | Structured data (name, amounts, etc.) |
| `assigned_to` | Link | No | → User |
| `assigned_group` | Link | No | → User Group |
| `route_via_rule` | Link | No | → Routing Rule (which rule triggered) |
| `delivery_receipt` | Attach | No | Confirmation receipt |
| `created_by` | Link | Yes | → User (who initiated send) |
| `notes` | Text Editor | No | User notes |

**Child Tables:**

| Child Table | Purpose |
|-------------|---------|
| `Fax Annotation` | Signatures, stamps, highlights applied |
| `Fax Routing History` | Audit trail of routing decisions |
| `Fax Transmission Log` | Detailed transmission attempts |

**Methods (Python):**
```python
class FaxDocument(Document):
    def validate(self):
        """Validation before save"""
        self.validate_phone_numbers()
        self.calculate_spam_score()

    def after_insert(self):
        """After creating new fax"""
        self.enqueue_processing()

    def on_update(self):
        """After updates"""
        self.notify_assigned_user()

    def send_fax(self):
        """Trigger outbound transmission"""

    def apply_annotation(self, annotation_data):
        """Apply signature/stamp"""

    def return_via_fax(self):
        """Return annotated fax to sender"""

    def return_via_email(self, email_body):
        """Email annotated fax to sender"""
```

#### 4.1.2 Fax Category
**DocType Name:** `Fax Category`
**Naming:** field:category_name
**Purpose:** AI classification categories

**Fields:**
- `category_name` (Data): e.g., "Invoice", "Contract", "Complaint"
- `description` (Text)
- `default_assignment` (Link → User/Group)
- `priority` (Select): Low / Medium / High / Critical
- `color` (Color): For UI display
- `keywords` (Table): Training keywords for AI

#### 4.1.3 Routing Rule
**DocType Name:** `Routing Rule`
**Naming:** Auto-name `ROUTE-{#####}`
**Purpose:** Define routing logic

**Fields:**
- `rule_name` (Data)
- `priority` (Int): 1-1000 (lower = higher priority)
- `enabled` (Check): Enable/disable rule
- `condition_type` (Select): Area Code / DID / CSID / Time of Day / Page Count / AI Category
- `condition_config` (JSON): Rule-specific parameters
- `action_type` (Select): Route to User / Route to Group / Webhook / Create Task / Archive
- `action_config` (JSON): Action-specific parameters
- `test_mode` (Check): Simulate without executing

**Child Tables:**
- `Routing Rule Condition`: Multiple AND/OR conditions
- `Routing Rule Action`: Multiple sequential actions

#### 4.1.4 Whitelist Entry
**DocType Name:** `Whitelist Entry`
**Naming:** field:phone_pattern
**Purpose:** Approved senders bypass validation

**Fields:**
- `phone_pattern` (Data): +1212*, etc.
- `sender_name` (Data)
- `route_to` (Link → User/Group): Direct routing
- `bypass_ai` (Check): Skip AI classification
- `notes` (Text)
- `created_by` (Link → User)

#### 4.1.5 Blacklist Entry
**DocType Name:** `Blacklist Entry`
**Naming:** field:phone_pattern
**Purpose:** Block spam/malicious senders

**Fields:**
- `phone_pattern` (Data)
- `type` (Select): Global / Personal
- `user` (Link → User): If personal blacklist
- `reason` (Text)
- `source` (Select): Manual / External DB / AI Detected
- `created_by` (Link → User)

#### 4.1.6 Fax Challenge
**DocType Name:** `Fax Challenge`
**Naming:** Auto-name `CHAL-{YYYY}-{#####}`
**Purpose:** Track Tier 3 questionnaire challenges

**Fields:**
- `held_fax` (Link → Fax Document)
- `sender_number` (Data)
- `challenge_sent_at` (Datetime)
- `challenge_code` (Data): Unique validation code
- `expires_at` (Datetime): Default +24 hours
- `status` (Select): Pending / Validated / Failed / Expired
- `response_received_at` (Datetime)
- `questionnaire_response` (JSON): Filled answers
- `validation_method` (Select): Fax Back / Manual Override

#### 4.1.7 Signature
**DocType Name:** `Signature`
**Naming:** field:signature_name
**Purpose:** User's saved signatures

**Fields:**
- `signature_name` (Data)
- `user` (Link → User)
- `type` (Select): Typed / Drawn / Uploaded
- `signature_image` (Attach Image)
- `font` (Data): If typed
- `is_default` (Check)

#### 4.1.8 Stamp Template
**DocType Name:** `Stamp Template`
**Naming:** field:template_name
**Purpose:** Reusable stamp designs

**Fields:**
- `template_name` (Data)
- `text` (Data): e.g., "PAID", "APPROVED"
- `include_date` (Check)
- `include_user_name` (Check)
- `font` (Select)
- `font_size` (Int)
- `text_color` (Color)
- `border_style` (Select): Rectangle / Circle / None
- `border_color` (Color)
- `transparency` (Int): 0-100
- `is_public` (Check): Available to all users
- `allowed_roles` (Table): Role-based access

#### 4.1.9 Fax Settings
**DocType Name:** `Fax Settings`
**Single DocType:** Yes (only one record)
**Purpose:** Global fax system configuration

**Fields:**

| Section | Fields |
|---------|--------|
| **Provider** | `provider` (Select), `api_key` (Password), `api_url` (Data), `test_mode` (Check) |
| **AI/ML** | `ai_enabled` (Check), `confidence_threshold` (Float), `ocr_language` (Select) |
| **Validation** | `validation_enabled` (Check), `whitelist_bypass_ai` (Check), `challenge_timeout_hours` (Int) |
| **Routing** | `default_route` (Link → User/Group), `business_hours_start` (Time), `business_hours_end` (Time) |
| **Security** | `mfa_required` (Check), `email_to_fax_confirmation` (Check), `rate_limit_per_hour` (Int) |
| **Notifications** | `notify_on_receive` (Check), `notify_email_template` (Link → Email Template) |
| **Storage** | `storage_provider` (Select), `s3_bucket` (Data), `retention_days` (Int) |

#### 4.1.10 Fax Provider Configuration
**DocType Name:** `Fax Provider Configuration`
**Naming:** field:provider_name
**Purpose:** Multi-provider abstraction

**Fields:**
- `provider_name` (Select): SRFax / iFax / Custom
- `api_endpoint` (Data)
- `api_key` (Password)
- `webhook_secret` (Password)
- `enabled` (Check)
- `priority` (Int): Failover order
- `send_capability` (Check)
- `receive_capability` (Check)

#### 4.1.11 Fax Queue
**DocType Name:** `Fax Queue`
**Naming:** Auto-name `QUEUE-{#####}`
**Purpose:** Outbound sending queue

**Fields:**
- `fax_document` (Link → Fax Document)
- `priority` (Select): Low / Normal / High / Urgent
- `scheduled_at` (Datetime): When to send
- `retry_count` (Int)
- `max_retries` (Int)
- `last_attempt_at` (Datetime)
- `last_error` (Text)
- `status` (Select): Queued / Processing / Sent / Failed

### 4.2 Supporting DocTypes

#### 4.2.1 Fax Audit Log
**DocType Name:** `Fax Audit Log`
**Immutable:** Yes (no edit after creation)
**Purpose:** Comprehensive audit trail

**Fields:**
- `fax_document` (Link)
- `event_type` (Select): Created / Viewed / Annotated / Sent / Deleted / Routing Changed
- `user` (Link → User)
- `ip_address` (Data)
- `timestamp` (Datetime)
- `details` (JSON): Event-specific data
- `session_id` (Data)

#### 4.2.2 Fax Webhook Configuration
**DocType Name:** `Fax Webhook Configuration`
**Purpose:** External system integrations

**Fields:**
- `webhook_name` (Data)
- `event_trigger` (Select): Fax Received / Fax Sent / Routing Decided / Validation Failed
- `target_url` (Data)
- `method` (Select): POST / PUT
- `headers` (JSON): Custom HTTP headers
- `authentication` (Select): None / API Key / Bearer Token
- `secret_key` (Password)
- `enabled` (Check)
- `retry_on_failure` (Check)

#### 4.2.3 External Spam Database
**DocType Name:** `External Spam Database`
**Single DocType:** Yes
**Purpose:** Integration with spam/fraud databases

**Fields:**
- `provider_name` (Data)
- `api_url` (Data)
- `api_key` (Password)
- `update_frequency` (Select): Hourly / Daily / Manual
- `last_sync_at` (Datetime)
- `total_entries` (Int)
- `enabled` (Check)

#### 4.2.4 Fax API Key
**DocType Name:** `Fax API Key`
**Purpose:** API authentication for external access

**Fields:**
- `key_name` (Data)
- `user` (Link → User)
- `api_key` (Data): Auto-generated UUID
- `api_secret` (Password): Auto-generated
- `permissions` (Table): Scoped permissions (send, receive, read, etc.)
- `rate_limit` (Int)
- `expires_at` (Datetime)
- `last_used_at` (Datetime)
- `enabled` (Check)

#### 4.2.5 Fax Dashboard
**DocType Name:** `Fax Dashboard` (Custom Page)
**Purpose:** Real-time metrics display

**Widgets:**
- Total Faxes Today (by direction)
- Held Faxes Count
- Spam Blocked Count
- AI Routing Accuracy
- Average Processing Time
- Top Categories
- Recent Activity Feed

---

## 5. Folder Structure

### 5.1 Complete Module Structure

```
apps/dartwing/dartwing/dartwing_fax/
│
├── __init__.py                          # Module initialization
├── hooks.py                             # Module hooks (if needed, override)
│
├── doctype/                             # All DocTypes
│   ├── fax_document/
│   │   ├── __init__.py
│   │   ├── fax_document.py              # Controller
│   │   ├── fax_document.json            # Schema
│   │   ├── fax_document.js              # Client-side logic
│   │   ├── fax_document_list.js         # List view customization
│   │   ├── fax_document_dashboard.py    # Dashboard data
│   │   ├── test_fax_document.py         # Unit tests
│   │   └── templates/
│   │       └── fax_document.html        # Print format
│   │
│   ├── fax_category/
│   │   ├── __init__.py
│   │   ├── fax_category.py
│   │   ├── fax_category.json
│   │   └── fax_category.js
│   │
│   ├── routing_rule/
│   │   ├── __init__.py
│   │   ├── routing_rule.py
│   │   ├── routing_rule.json
│   │   ├── routing_rule.js
│   │   └── test_routing_rule.py
│   │
│   ├── whitelist_entry/
│   │   ├── __init__.py
│   │   ├── whitelist_entry.py
│   │   ├── whitelist_entry.json
│   │   └── whitelist_entry.js
│   │
│   ├── blacklist_entry/
│   │   ├── __init__.py
│   │   ├── blacklist_entry.py
│   │   ├── blacklist_entry.json
│   │   └── blacklist_entry.js
│   │
│   ├── fax_challenge/
│   │   ├── __init__.py
│   │   ├── fax_challenge.py
│   │   ├── fax_challenge.json
│   │   └── fax_challenge.js
│   │
│   ├── signature/
│   │   ├── __init__.py
│   │   ├── signature.py
│   │   ├── signature.json
│   │   ├── signature.js
│   │   └── templates/
│   │       └── signature_editor.html    # Custom signature creation UI
│   │
│   ├── stamp_template/
│   │   ├── __init__.py
│   │   ├── stamp_template.py
│   │   ├── stamp_template.json
│   │   ├── stamp_template.js
│   │   └── templates/
│   │       └── stamp_editor.html
│   │
│   ├── fax_settings/
│   │   ├── __init__.py
│   │   ├── fax_settings.py
│   │   ├── fax_settings.json
│   │   └── fax_settings.js
│   │
│   ├── fax_provider_configuration/
│   │   ├── __init__.py
│   │   ├── fax_provider_configuration.py
│   │   ├── fax_provider_configuration.json
│   │   └── fax_provider_configuration.js
│   │
│   ├── fax_queue/
│   │   ├── __init__.py
│   │   ├── fax_queue.py
│   │   ├── fax_queue.json
│   │   └── fax_queue.js
│   │
│   ├── fax_audit_log/
│   │   ├── __init__.py
│   │   ├── fax_audit_log.py
│   │   ├── fax_audit_log.json
│   │   └── fax_audit_log.js
│   │
│   ├── fax_webhook_configuration/
│   │   ├── __init__.py
│   │   ├── fax_webhook_configuration.py
│   │   ├── fax_webhook_configuration.json
│   │   └── fax_webhook_configuration.js
│   │
│   ├── external_spam_database/
│   │   ├── __init__.py
│   │   ├── external_spam_database.py
│   │   ├── external_spam_database.json
│   │   └── external_spam_database.js
│   │
│   └── fax_api_key/
│       ├── __init__.py
│       ├── fax_api_key.py
│       ├── fax_api_key.json
│       └── fax_api_key.js
│
├── page/                                # Custom pages (Frappe Desk)
│   ├── fax_inbox/
│   │   ├── fax_inbox.py
│   │   ├── fax_inbox.js
│   │   ├── fax_inbox.json
│   │   └── fax_inbox.html
│   │
│   ├── fax_viewer/
│   │   ├── fax_viewer.py
│   │   ├── fax_viewer.js
│   │   ├── fax_viewer.json
│   │   └── fax_viewer.html              # Annotation UI
│   │
│   ├── held_faxes_queue/
│   │   ├── held_faxes_queue.py
│   │   ├── held_faxes_queue.js
│   │   ├── held_faxes_queue.json
│   │   └── held_faxes_queue.html
│   │
│   └── fax_dashboard/
│       ├── fax_dashboard.py
│       ├── fax_dashboard.js
│       ├── fax_dashboard.json
│       └── fax_dashboard.html
│
├── report/                              # Reports
│   ├── fax_activity_log/
│   │   ├── __init__.py
│   │   ├── fax_activity_log.py
│   │   ├── fax_activity_log.json
│   │   └── fax_activity_log.js
│   │
│   ├── routing_accuracy/
│   │   ├── __init__.py
│   │   ├── routing_accuracy.py
│   │   └── routing_accuracy.json
│   │
│   ├── spam_blocked_report/
│   │   ├── __init__.py
│   │   ├── spam_blocked_report.py
│   │   └── spam_blocked_report.json
│   │
│   └── fax_audit_trail/
│       ├── __init__.py
│       ├── fax_audit_trail.py
│       └── fax_audit_trail.json
│
├── api/                                 # REST API endpoints
│   ├── __init__.py
│   ├── receive.py                       # Webhook: Receive fax
│   ├── send.py                          # API: Send fax
│   ├── routing.py                       # API: Manual routing
│   ├── annotation.py                    # API: Apply signatures/stamps
│   ├── validation.py                    # API: Whitelist/blacklist management
│   ├── challenge.py                     # API: Challenge management
│   └── webhooks.py                      # Outbound webhook dispatcher
│
├── services/                            # Business logic services
│   ├── __init__.py
│   ├── fax_provider/
│   │   ├── __init__.py
│   │   ├── base.py                      # Abstract provider interface
│   │   ├── srfax.py                     # SRFax implementation
│   │   ├── ifax.py                      # iFax implementation
│   │   └── factory.py                   # Provider factory
│   │
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── ocr_service.py               # OCR processing
│   │   └── text_preprocessor.py         # Image enhancement
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── classifier.py                # NLP classification
│   │   ├── entity_extractor.py          # Named entity extraction
│   │   ├── spam_detector.py             # Spam scoring
│   │   └── models/
│   │       ├── fax_classifier.h5        # Trained TensorFlow model
│   │       └── entity_model.pkl         # Trained entity model
│   │
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── routing_engine.py            # Main routing logic
│   │   ├── rule_evaluator.py            # Evaluate rules
│   │   └── workload_balancer.py         # Balance assignments
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── tier1_validator.py           # Whitelist/blacklist
│   │   ├── tier2_validator.py           # AI validation
│   │   ├── tier3_validator.py           # Challenge system
│   │   └── spam_db_sync.py              # External DB sync
│   │
│   ├── annotation/
│   │   ├── __init__.py
│   │   ├── signature_service.py         # Apply signatures
│   │   ├── stamp_service.py             # Apply stamps
│   │   ├── pdf_editor.py                # PDF manipulation
│   │   └── image_processor.py           # Image processing
│   │
│   ├── security/
│   │   ├── __init__.py
│   │   ├── mfa_service.py               # Multi-factor auth
│   │   ├── confirmation_loop.py         # Email-to-fax confirmation
│   │   ├── rate_limiter.py              # Rate limiting
│   │   └── anomaly_detector.py          # Anomaly detection
│   │
│   └── notification/
│       ├── __init__.py
│       ├── notification_service.py      # Notification dispatcher
│       ├── email_notifier.py            # Email notifications
│       └── sms_notifier.py              # SMS notifications
│
├── tasks/                               # Background jobs
│   ├── __init__.py
│   ├── process_incoming_fax.py          # Process new fax
│   ├── send_outgoing_fax.py             # Send queued fax
│   ├── retry_failed_fax.py              # Retry failed sends
│   ├── cleanup_expired_challenges.py    # Clean up old challenges
│   ├── sync_spam_database.py            # Hourly spam DB sync
│   ├── generate_daily_report.py         # Daily metrics
│   └── train_ai_model.py                # Retrain AI models
│
├── utils/                               # Utility functions
│   ├── __init__.py
│   ├── phone_validator.py               # E.164 phone validation
│   ├── file_converter.py                # TIFF ↔ PDF conversion
│   ├── encryption.py                    # AES encryption utilities
│   ├── audit_logger.py                  # Immutable audit logging
│   └── response_formatter.py            # API response formatting
│
├── public/                              # Frontend assets
│   ├── css/
│   │   ├── fax_inbox.css
│   │   ├── fax_viewer.css
│   │   └── signature_editor.css
│   │
│   ├── js/
│   │   ├── fax_inbox.bundle.js
│   │   ├── fax_viewer.bundle.js
│   │   ├── signature_editor.js
│   │   ├── stamp_editor.js
│   │   └── pdf_annotator.js             # Canvas-based PDF annotation
│   │
│   └── img/
│       ├── stamp_icons/
│       └── signature_fonts/
│
├── templates/                           # Email/Print templates
│   ├── emails/
│   │   ├── fax_received.html
│   │   ├── fax_sent_confirmation.html
│   │   ├── challenge_notification.html
│   │   └── confirmation_loop.html
│   │
│   └── prints/
│       ├── fax_cover_page.html
│       └── delivery_receipt.html
│
├── fixtures/                            # Default data
│   ├── fax_category.json                # Pre-defined categories
│   ├── routing_rule.json                # Example rules
│   └── stamp_template.json              # Default stamps
│
├── tests/                               # Integration tests
│   ├── __init__.py
│   ├── test_fax_receive.py
│   ├── test_fax_send.py
│   ├── test_routing.py
│   ├── test_validation.py
│   ├── test_annotation.py
│   └── test_ai_classifier.py
│
├── config/                              # Module configuration
│   └── desktop.py                       # Desk icons & shortcuts
│
├── patches/                             # Data migration scripts
│   └── v1_0/
│       └── setup_default_categories.py
│
└── docs/                                # Module-specific docs
    ├── api.md                           # API documentation
    ├── webhooks.md                      # Webhook specs
    └── provider_integration.md          # Provider integration guide
```

### 5.2 Key Directory Purposes

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `doctype/` | Frappe DocType definitions | `.py` (controller), `.json` (schema), `.js` (client-side) |
| `page/` | Custom Frappe Desk pages | Inbox, Viewer, Dashboard |
| `report/` | Frappe reports | Activity log, Routing accuracy, Audit trail |
| `api/` | REST API endpoints | Webhook handlers, public APIs |
| `services/` | Business logic layer | Provider abstraction, AI, OCR, Routing |
| `tasks/` | Background jobs | Queue processing, cleanup, sync |
| `utils/` | Shared utilities | Validation, conversion, logging |
| `public/` | Static assets | CSS, JS bundles, images |
| `templates/` | Jinja2 templates | Email templates, print formats |
| `fixtures/` | Seed data | Default categories, rules |
| `tests/` | Test suite | Unit and integration tests |

---

## 6. Component Architecture

### 6.1 AI/ML Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    AI/ML PROCESSING PIPELINE                 │
└─────────────────────────────────────────────────────────────┘

 Fax Document (TIFF/PDF)
         │
         ▼
┌────────────────────┐
│  1. Image Quality  │  → Enhance contrast, denoise, deskew
│    Enhancement     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  2. OCR Engine     │  → Tesseract OCR
│  (Text Extraction) │  → ICR for handwriting
└─────────┬──────────┘  → Output: Raw text
          │
          ▼
┌────────────────────┐
│  3. Text           │  → Tokenization
│     Preprocessing  │  → Normalization
└─────────┬──────────┘  → Stop word removal
          │
          ▼
┌────────────────────┐
│  4. NLP            │  → TensorFlow/PyTorch model
│     Classification │  → Input: Text features
└─────────┬──────────┘  → Output: Category + Confidence
          │
          ▼
┌────────────────────┐
│  5. Entity         │  → spaCy / Custom NER model
│     Extraction     │  → Extract: Names, Amounts, Dates
└─────────┬──────────┘  → Output: Structured JSON
          │
          ▼
┌────────────────────┐
│  6. Spam Scoring   │  → Content analysis
│                    │  → Metadata analysis
└─────────┬──────────┘  → Output: Score 0-100
          │
          ▼
     Store Results in Fax Document
```

**Key Technologies:**
- **OCR**: Tesseract 5.0+, pytesseract
- **NLP**: TensorFlow/Keras or PyTorch
- **Entity Extraction**: spaCy, transformers (BERT)
- **Preprocessing**: OpenCV, Pillow

**Model Storage:**
```
apps/dartwing/dartwing/dartwing_fax/services/ai/models/
├── fax_classifier_v1.h5          # TensorFlow model
├── fax_classifier_metadata.json  # Model config
├── entity_extractor.pkl          # spaCy pipeline
└── spam_detector.pkl             # Sklearn model
```

### 6.2 Routing Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ROUTING ENGINE                           │
└─────────────────────────────────────────────────────────────┘

Input: Fax Document + AI Results
    │
    ▼
┌─────────────────────┐
│ Load Routing Rules  │  → Query active rules ordered by priority
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Evaluate Rules      │  → For each rule:
│  (Rule Evaluator)   │     1. Check conditions (AND/OR logic)
└──────────┬──────────┘     2. If match, execute action
           │                3. Break if exclusive
           ▼
┌─────────────────────┐
│ Execute Actions     │  → Route to User/Group
│                     │  → Trigger Webhook
└──────────┬──────────┘  → Create Task
           │             → Archive
           ▼
┌─────────────────────┐
│ Workload Balancer  │  → If routing to group:
│                     │     - Get active users in group
└──────────┬──────────┘     - Check current workload
           │                - Assign to user with lowest load
           ▼
    Update Fax Document
```

**Routing Rule Example (JSON Config):**
```json
{
  "rule_name": "Invoice to Accounting",
  "priority": 10,
  "conditions": [
    {
      "type": "ai_category",
      "operator": "equals",
      "value": "Invoice"
    },
    {
      "type": "time_of_day",
      "operator": "within",
      "value": {"start": "08:00", "end": "17:00"}
    }
  ],
  "actions": [
    {
      "type": "route_to_group",
      "config": {"group": "Accounting Team"}
    },
    {
      "type": "webhook",
      "config": {
        "url": "https://erp.example.com/api/invoice",
        "method": "POST"
      }
    }
  ]
}
```

### 6.3 Validation Engine (Three-Tier)

```
┌─────────────────────────────────────────────────────────────┐
│                  THREE-TIER VALIDATION                       │
└─────────────────────────────────────────────────────────────┘

Incoming Fax
    │
    ▼
┌──────────────────────┐
│  TIER 1: Hard Rules  │
│  (Whitelist/Blacklist)│
└──────┬───────────────┘
       │
       ├─ Whitelist Match? → Bypass AI, Route Directly → DELIVER
       │
       ├─ Blacklist Match? → Reject → DELETE
       │
       └─ No Match → Continue to Tier 2
                │
                ▼
       ┌──────────────────────┐
       │  TIER 2: AI Scoring  │
       │  (Spam Detection)    │
       └──────┬───────────────┘
              │
              ├─ Score 0-30%   → Low Risk → DELIVER
              │
              ├─ Score 31-80%  → Suspicious → Tier 3 Challenge
              │                              │
              └─ Score 81-100% → High Risk → REJECT & DELETE
                                 │
                                 ▼
                        ┌──────────────────────┐
                        │  TIER 3: Challenge   │
                        │  (Questionnaire)     │
                        └──────┬───────────────┘
                               │
                               ├─ Send Fax-Back Challenge
                               │  (with validation code)
                               │
                               ├─ Hold Original Fax
                               │  (24-hour timeout)
                               │
                               └─ Wait for Response
                                   │
                                   ├─ Valid Response → Mark Validated → DELIVER
                                   │
                                   └─ No Response / Invalid → DELETE
```

**Implementation Classes:**
```python
# services/validation/tier1_validator.py
class Tier1Validator:
    def validate(self, sender_number):
        if self.is_whitelisted(sender_number):
            return ValidationResult(action="deliver", tier=1, bypass_ai=True)
        if self.is_blacklisted(sender_number):
            return ValidationResult(action="reject", tier=1)
        return ValidationResult(action="continue", tier=1)

# services/validation/tier2_validator.py
class Tier2Validator:
    def validate(self, fax_doc):
        score = self.calculate_spam_score(fax_doc)
        if score <= 30:
            return ValidationResult(action="deliver", tier=2, score=score)
        elif score <= 80:
            return ValidationResult(action="challenge", tier=2, score=score)
        else:
            return ValidationResult(action="reject", tier=2, score=score)

# services/validation/tier3_validator.py
class Tier3Validator:
    def initiate_challenge(self, fax_doc):
        challenge = create_fax_challenge(fax_doc)
        send_challenge_fax(challenge)
        return challenge

    def validate_response(self, challenge, response_fax):
        if self.verify_code(challenge, response_fax):
            return ValidationResult(action="deliver", tier=3)
        return ValidationResult(action="reject", tier=3)
```

### 6.4 Annotation Engine

```
┌─────────────────────────────────────────────────────────────┐
│                   ANNOTATION ENGINE                          │
└─────────────────────────────────────────────────────────────┘

User selects annotation tool (Signature/Stamp/Text)
    │
    ▼
┌──────────────────────┐
│  Frontend Canvas     │  → User draws/places annotation
│  (PDF.js + Canvas)   │  → Get coordinates, dimensions
└──────┬───────────────┘
       │ POST /api/fax/{id}/annotate
       ▼
┌──────────────────────┐
│  Annotation API      │  → Receive annotation data
└──────┬───────────────┘  → Validate permissions
       │
       ▼
┌──────────────────────┐
│  PDF Editor Service  │  → Load original PDF
│  (PyPDF2/ReportLab)  │  → Render annotation layer
└──────┬───────────────┘  → Embed metadata
       │
       ▼
┌──────────────────────┐
│  Audit Logger        │  → Log: User, Timestamp, IP, Action
└──────┬───────────────┘  → Create immutable record
       │
       ▼
┌──────────────────────┐
│  Save Annotated PDF  │  → Upload to S3/local storage
│  (Immutable)         │  → Link to Fax Document
└──────┬───────────────┘  → Preserve original
       │
       ▼
    Return URL to annotated PDF
```

**Key Libraries:**
- **PDF Rendering**: PDF.js (frontend), PyPDF2/pypdf (backend)
- **Image Processing**: Pillow, OpenCV
- **Canvas Drawing**: Fabric.js or Konva.js
- **PDF Generation**: ReportLab, WeasyPrint

**Annotation Data Structure:**
```json
{
  "type": "signature",
  "signature_id": "SIG-00001",
  "position": {"x": 450, "y": 700, "page": 1},
  "dimensions": {"width": 150, "height": 50},
  "rotation": 0,
  "metadata": {
    "user": "user@example.com",
    "timestamp": "2025-11-23T14:30:00Z",
    "ip_address": "192.168.1.100"
  }
}
```

### 6.5 Fax Provider Abstraction Layer

```
┌─────────────────────────────────────────────────────────────┐
│              FAX PROVIDER ABSTRACTION LAYER                  │
└─────────────────────────────────────────────────────────────┘

Application Code (Send Fax)
    │
    ▼
┌──────────────────────┐
│  Provider Factory    │  → Get configured provider
└──────┬───────────────┘  → Select by priority/capability
       │
       ▼
┌──────────────────────┐
│  Base Provider       │  → Abstract interface:
│  Interface           │     - send_fax()
└──────┬───────────────┘     - receive_fax()
       │                     - get_status()
       ├─────────┬──────────┬─────────┐
       ▼         ▼          ▼         ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ SRFax  │ │ iFax   │ │ Custom │ │ Mock   │
   │Provider│ │Provider│ │Provider│ │Provider│
   └────────┘ └────────┘ └────────┘ └────────┘
       │         │          │         │
       └─────────┴──────────┴─────────┘
                 │
                 ▼
         External Fax Service
```

**Interface Definition:**
```python
# services/fax_provider/base.py
from abc import ABC, abstractmethod

class FaxProvider(ABC):
    @abstractmethod
    def send_fax(self, recipient: str, file_path: str, options: dict) -> dict:
        """Send fax to recipient"""
        pass

    @abstractmethod
    def receive_fax(self, webhook_data: dict) -> dict:
        """Process incoming fax webhook"""
        pass

    @abstractmethod
    def get_status(self, fax_id: str) -> dict:
        """Get transmission status"""
        pass

    @abstractmethod
    def validate_webhook(self, request: dict) -> bool:
        """Validate webhook signature"""
        pass

# services/fax_provider/srfax.py
class SRFaxProvider(FaxProvider):
    def send_fax(self, recipient, file_path, options):
        # SRFax-specific implementation
        response = requests.post(
            self.api_url + "/Queue_Fax",
            data={
                "access_id": self.api_key,
                "access_pwd": self.api_secret,
                "sCallerID": options.get("sender_number"),
                "sFaxType": "SINGLE",
                "sToFaxNumber": recipient,
                "sFileName": file_path
            }
        )
        return self._parse_response(response)
```

---

## 7. Data Flow

### 7.1 Incoming Fax Flow

```
┌─────────────┐
│ Fax Provider│ (SRFax receives fax)
└──────┬──────┘
       │ Webhook POST /api/fax/receive
       ▼
┌──────────────────────┐
│ Webhook Handler      │ 1. Validate webhook signature
│ (api/receive.py)     │ 2. Download fax file from provider
└──────┬───────────────┘ 3. Create Fax Document (status=pending)
       │
       ▼
┌──────────────────────┐
│ Tier 1 Validation    │ Check whitelist/blacklist
└──────┬───────────────┘
       │ If not in lists
       ▼
┌──────────────────────┐
│ Background Job       │ Enqueue: process_incoming_fax
│ (RQ/Celery)          │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ OCR Processing       │ Extract text from TIFF/PDF
│ (tasks/process_...)  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ AI Classification    │ Category + Confidence
└──────┬───────────────┘ Entity extraction
       │                 Spam scoring
       ▼
┌──────────────────────┐
│ Tier 2 Validation    │ Evaluate spam score
└──────┬───────────────┘
       │
       ├─ Score 0-30%   → Continue
       ├─ Score 31-80%  → Tier 3 Challenge
       └─ Score 81-100% → Reject
       │
       ▼
┌──────────────────────┐
│ Routing Engine       │ Apply routing rules
└──────┬───────────────┘ Assign to user/group
       │
       ▼
┌──────────────────────┐
│ Notification         │ Email/SMS to assigned user
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Webhook Dispatch     │ Trigger configured webhooks
└──────────────────────┘
       │
       ▼
    USER INBOX
```

### 7.2 Outgoing Fax Flow

```
USER (Send Fax)
    │ Click "Send Fax" button
    ▼
┌──────────────────────┐
│ Send Fax Form        │ Fill recipient, upload file
│ (Web/API)            │
└──────┬───────────────┘
       │ POST /api/fax/send
       ▼
┌──────────────────────┐
│ Authentication       │ Validate user permissions
│ (MFA, Email verify)  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Create Fax Document  │ status=pending, direction=outbound
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Email-to-Fax?        │
└──────┬───────────────┘
       │
       ├─ YES → Confirmation Loop
       │         ├─ Generate preview + code
       │         ├─ Send confirmation email/SMS
       │         └─ Wait for confirmation
       │              │
       │              ├─ Confirmed → Continue
       │              └─ Expired/Invalid → Reject
       │
       └─ NO  → Continue
       │
       ▼
┌──────────────────────┐
│ Add to Fax Queue     │ Priority, scheduled_at
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Background Worker    │ Process queue
│ (tasks/send_...)     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Provider Send        │ Call provider API (SRFax, etc.)
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Update Status        │ status=sent/failed
│                      │ Save delivery receipt
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Audit Log            │ Immutable transmission record
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Notify User          │ Success/failure notification
└──────────────────────┘
```

### 7.3 Annotation & Return Flow

```
USER (View received fax)
    │
    ▼
┌──────────────────────┐
│ Fax Viewer Page      │ Display PDF in canvas
└──────┬───────────────┘
       │ User clicks "Sign" button
       ▼
┌──────────────────────┐
│ Signature Editor     │ Draw/upload signature
└──────┬───────────────┘
       │ User positions signature
       ▼
┌──────────────────────┐
│ POST /api/fax/       │ Send annotation data
│      {id}/annotate   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Annotation Service   │ Load original PDF
│                      │ Render signature layer
└──────┬───────────────┘ Save annotated PDF
       │
       ▼
┌──────────────────────┐
│ Audit Logger         │ Log annotation action
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Return Annotated?    │
└──────┬───────────────┘
       │
       ├─ Via FAX  → Create new outbound fax
       │             recipient = original sender
       │
       └─ Via EMAIL → Create email
                      attach annotated PDF
                      recipient = original sender email
```

---

## 8. Integration Architecture

### 8.1 External Integrations

| Integration | Direction | Protocol | Purpose |
|-------------|-----------|----------|---------|
| **Fax Provider (SRFax/iFax)** | Bidirectional | REST API + Webhook | Send/receive faxes |
| **External CRM/ERP** | Outbound | Webhook | Push fax data for processing |
| **Spam Database** | Inbound | REST API | Sync blacklist |
| **Cloud Storage (S3/Drive)** | Outbound | REST API | Archive documents |
| **Email Service (SMTP/SendGrid)** | Outbound | SMTP/API | Notifications, confirmations |
| **SMS Gateway (Twilio)** | Outbound | REST API | MFA, confirmations |
| **Project Management (Jira)** | Outbound | REST API | Create tasks from faxes |

### 8.2 Webhook System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WEBHOOK DISPATCHER                        │
└─────────────────────────────────────────────────────────────┘

Fax Event (e.g., Received, Routed, Sent)
    │
    ▼
┌──────────────────────┐
│ Load Active Webhooks │ Query Fax Webhook Configuration
└──────┬───────────────┘ Filter by event_trigger
       │
       ▼
┌──────────────────────┐
│ Build Payload        │ Format JSON payload
│                      │ Include fax metadata
└──────┬───────────────┘ Extract entities
       │
       ▼
┌──────────────────────┐
│ Sign Payload         │ HMAC-SHA256 signature
│                      │ Add timestamp
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ HTTP POST            │ Send to target_url
│                      │ Include signature header
└──────┬───────────────┘ Timeout: 30s
       │
       ├─ Success (200-299) → Log success
       │
       └─ Failure (4xx, 5xx) → Retry logic
                                │
                                ├─ Retry 1: After 5 minutes
                                ├─ Retry 2: After 30 minutes
                                └─ Retry 3: After 2 hours
                                    │
                                    └─ Final Failure → Alert admin
```

**Webhook Payload Example:**
```json
{
  "event": "fax.received",
  "timestamp": "2025-11-23T14:30:00Z",
  "fax": {
    "id": "FAX-2025-00123",
    "sender": "+12125551234",
    "recipient": "+13125555678",
    "pages": 3,
    "category": "Invoice",
    "confidence": 0.95,
    "entities": {
      "invoice_number": "INV-2025-001",
      "amount": 1250.00,
      "vendor": "Acme Corp"
    },
    "file_url": "https://storage.example.com/faxes/FAX-2025-00123.pdf"
  },
  "signature": "sha256=abc123..."
}
```

### 8.3 API Authentication

```
┌─────────────────────────────────────────────────────────────┐
│                   API AUTHENTICATION                         │
└─────────────────────────────────────────────────────────────┘

API Request
    │
    ▼
┌──────────────────────┐
│ Extract Credentials  │ Check headers:
└──────┬───────────────┘ - Authorization: Bearer {token}
       │                 - X-API-Key: {key}
       ▼                 - X-Signature: {hmac}
┌──────────────────────┐
│ Validate Credentials │ Query Fax API Key
└──────┬───────────────┘ Check expiration, enabled
       │
       ├─ Invalid → 401 Unauthorized
       │
       └─ Valid → Continue
       │
       ▼
┌──────────────────────┐
│ Verify Signature     │ HMAC-SHA256(request_body, secret)
└──────┬───────────────┘
       │
       ├─ Invalid → 403 Forbidden
       │
       └─ Valid → Continue
       │
       ▼
┌──────────────────────┐
│ Check Permissions    │ Scoped permissions (send, read, etc.)
└──────┬───────────────┘
       │
       ├─ Forbidden → 403 Forbidden
       │
       └─ Allowed → Continue
       │
       ▼
┌──────────────────────┐
│ Rate Limiting        │ Check request count
└──────┬───────────────┘ per API key per hour
       │
       ├─ Exceeded → 429 Too Many Requests
       │
       └─ OK → Process Request
```

---

## 9. Security Architecture

### 9.1 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                                    │
│ - TLS 1.3 for all connections                                │
│ - Firewall rules (only ports 80/443 exposed)                 │
│ - DDoS protection (CloudFlare/AWS Shield)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Application Security                                │
│ - MFA for user authentication                                │
│ - API key + signature verification                           │
│ - Session management (Redis)                                 │
│ - CSRF protection (Frappe built-in)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Data Security                                       │
│ - Encryption at rest (AES-256)                               │
│ - Encryption in transit (TLS 1.3)                            │
│ - Field-level encryption (sensitive data)                    │
│ - Secure deletion (overwrite + delete)                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Access Control                                      │
│ - Role-Based Access Control (RBAC)                           │
│ - Document-level permissions (assigned user only)            │
│ - Audit logging (all access recorded)                        │
│ - Principle of least privilege                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Validation Security (Fax-Specific)                  │
│ - Three-tier validation system                               │
│ - Whitelist/Blacklist                                        │
│ - AI spam detection                                          │
│ - Challenge-response verification                            │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Data Encryption

**At Rest:**
```python
# utils/encryption.py
from cryptography.fernet import Fernet
import frappe

class DataEncryption:
    def __init__(self):
        # Key stored in Frappe config (not in code!)
        self.key = frappe.get_conf().get("encryption_key")
        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_path):
        """Encrypt PDF/TIFF before storage"""
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = self.cipher.encrypt(data)
        # Save to S3/local storage

    def decrypt_file(self, encrypted_path):
        """Decrypt for viewing"""
        with open(encrypted_path, 'rb') as f:
            encrypted = f.read()
        return self.cipher.decrypt(encrypted)
```

**In Transit:**
- All API endpoints: HTTPS only (TLS 1.3)
- Fax provider communication: HTTPS
- Webhook delivery: HTTPS + signature

### 9.3 Audit Trail

**Immutable Logging:**
```python
# utils/audit_logger.py
def log_fax_access(fax_id, user, action, details=None):
    """Create immutable audit log entry"""
    frappe.get_doc({
        "doctype": "Fax Audit Log",
        "fax_document": fax_id,
        "event_type": action,  # Viewed, Annotated, Sent, etc.
        "user": user,
        "ip_address": frappe.local.request_ip,
        "timestamp": frappe.utils.now(),
        "details": json.dumps(details),
        "session_id": frappe.session.sid
    }).insert(ignore_permissions=True)
    frappe.db.commit()
```

**Logged Events:**
- Fax received
- Fax viewed
- Fax annotated (signature/stamp)
- Fax sent
- Fax deleted
- Routing rule changed
- Whitelist/blacklist modified
- API access
- Failed authentication attempts

---

## 10. Deployment Architecture

### 10.1 Production Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │   Internet  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ CloudFlare  │ (CDN, DDoS protection)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │Load Balancer│ (AWS ELB / Nginx)
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │  Web    │       │    Web    │     │    Web    │
   │ Server 1│       │  Server 2 │     │  Server 3 │
   └────┬────┘       └─────┬─────┘     └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │Background│       │Background │     │Background │
   │ Worker 1 │       │  Worker 2 │     │  Worker 3 │
   └────┬────┘       └─────┬─────┘     └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │ MariaDB │       │   Redis   │     │    S3     │
   │ Primary │       │  (Cache)  │     │ (Storage) │
   └────┬────┘       └───────────┘     └───────────┘
        │
   ┌────▼────┐
   │ MariaDB │
   │ Replica │
   └─────────┘
```

### 10.2 Scaling Strategy

| Component | Scaling Approach | Trigger |
|-----------|------------------|---------|
| **Web Servers** | Horizontal (auto-scale) | CPU > 70% |
| **Background Workers** | Horizontal (auto-scale) | Queue depth > 100 |
| **MariaDB** | Vertical + Read Replicas | Query latency > 200ms |
| **Redis** | Redis Cluster (sharding) | Memory > 80% |
| **S3 Storage** | Unlimited (cloud) | N/A |
| **AI Processing** | GPU instances (on-demand) | Batch size > 50 |

### 10.3 Monitoring & Observability

**Metrics to Monitor:**
```
Application Metrics:
- Fax throughput (faxes/hour)
- Processing latency (OCR, AI, routing)
- API response times
- Queue depth (send queue, AI queue)
- Error rate (failed sends, OCR failures)

AI/ML Metrics:
- Classification accuracy
- Confidence score distribution
- Spam detection rate (true positives, false positives)
- Model inference time

Security Metrics:
- Failed authentication attempts
- Blocked faxes (spam)
- Challenge success rate
- API rate limit violations

Infrastructure Metrics:
- CPU/Memory/Disk utilization
- Database query performance
- Redis hit rate
- S3 request rate
```

**Tools:**
- **Application**: Frappe built-in monitoring, custom dashboards
- **Infrastructure**: Prometheus + Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Alerts**: PagerDuty, Slack webhooks
- **APM**: New Relic or Datadog (optional)

---

## 11. Development Phases

### Phase 1: Foundation (MVP)
**Duration:** Months 1-3
**Goal:** Basic fax send/receive with manual routing

**DocTypes to Implement:**
- ✅ Fax Document (core fields only)
- ✅ Fax Settings
- ✅ Fax Provider Configuration
- ✅ Whitelist Entry
- ✅ Blacklist Entry
- ✅ Fax Queue

**Services to Implement:**
- ✅ Fax Provider (SRFax integration)
- ✅ Basic routing (manual assignment)
- ✅ Tier 1 validation (whitelist/blacklist only)
- ✅ Send/receive API endpoints

**UI to Implement:**
- ✅ Fax Inbox (basic list view)
- ✅ Send Fax form
- ✅ Settings page

### Phase 2: AI & Automation
**Duration:** Months 4-6
**Goal:** AI-powered routing and classification

**DocTypes to Add:**
- ✅ Fax Category
- ✅ Routing Rule

**Services to Add:**
- ✅ OCR Engine (Tesseract integration)
- ✅ AI Classifier (TensorFlow model)
- ✅ Entity Extractor
- ✅ Routing Engine (rule-based)
- ✅ Tier 2 Validation (AI spam detection)

**UI to Add:**
- ✅ Routing Rules Console
- ✅ Category Management

### Phase 3: Security & Validation
**Duration:** Months 7-9
**Goal:** Complete three-tier validation and outbound security

**DocTypes to Add:**
- ✅ Fax Challenge
- ✅ Fax Audit Log
- ✅ Fax API Key
- ✅ External Spam Database

**Services to Add:**
- ✅ Tier 3 Validator (challenge system)
- ✅ MFA Service
- ✅ Confirmation Loop (email-to-fax)
- ✅ Rate Limiter
- ✅ Anomaly Detector

**UI to Add:**
- ✅ Held Faxes Queue
- ✅ Security Console

### Phase 4: Annotation & Integrations
**Duration:** Months 10-12
**Goal:** Document annotation and external integrations

**DocTypes to Add:**
- ✅ Signature
- ✅ Stamp Template
- ✅ Fax Webhook Configuration

**Services to Add:**
- ✅ Annotation Engine (signature/stamp)
- ✅ PDF Editor
- ✅ Webhook Dispatcher
- ✅ Cloud Storage Integration

**UI to Add:**
- ✅ Fax Viewer & Editor (annotation UI)
- ✅ Signature/Stamp Console
- ✅ Webhook Configuration
- ✅ Analytics Dashboard

---

## 12. Appendices

### Appendix A: DocType Summary Table

| DocType Name | Type | Submittable | Track Changes | Phase |
|--------------|------|-------------|---------------|-------|
| Fax Document | Standard | No | Yes | 1 |
| Fax Category | Master | No | No | 2 |
| Routing Rule | Standard | No | Yes | 2 |
| Whitelist Entry | Master | No | Yes | 1 |
| Blacklist Entry | Master | No | Yes | 1 |
| Fax Challenge | Standard | No | Yes | 3 |
| Signature | Master | No | No | 4 |
| Stamp Template | Master | No | No | 4 |
| Fax Settings | Single | No | Yes | 1 |
| Fax Provider Configuration | Master | No | Yes | 1 |
| Fax Queue | Standard | No | No | 1 |
| Fax Audit Log | Immutable | No | No | 3 |
| Fax Webhook Configuration | Master | No | Yes | 4 |
| External Spam Database | Single | No | Yes | 3 |
| Fax API Key | Master | No | Yes | 3 |

### Appendix B: File Naming Conventions

**Python Files:**
- DocType controllers: `snake_case.py` (e.g., `fax_document.py`)
- Services: `snake_case.py` (e.g., `routing_engine.py`)
- API endpoints: `snake_case.py` (e.g., `receive.py`)
- Background tasks: `snake_case.py` (e.g., `process_incoming_fax.py`)

**JavaScript Files:**
- Client scripts: `snake_case.js` (e.g., `fax_document.js`)
- List views: `snake_case_list.js` (e.g., `fax_document_list.js`)
- Pages: `snake_case.js` (e.g., `fax_inbox.js`)

**Templates:**
- HTML templates: `snake_case.html` (e.g., `fax_cover_page.html`)
- Email templates: `snake_case.html` (e.g., `fax_received.html`)

### Appendix C: Technology Version Requirements

| Technology | Minimum Version | Recommended |
|------------|----------------|-------------|
| Python | 3.10 | 3.11+ |
| Frappe Framework | 15.0 | 15.89+ |
| MariaDB | 10.6 | 10.11+ |
| Redis | 6.0 | 7.0+ |
| Node.js | 16.x | 18.x+ |
| TensorFlow | 2.10 | 2.15+ |
| Tesseract OCR | 5.0 | 5.3+ |

---

**Document Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-23 | Dartwing Architecture Team | Initial architecture document |

---

**Review & Approval:**

- **Lead Architect:** _________________________ Date: _________
- **Engineering Lead:** ______________________ Date: _________
- **Product Owner:** _________________________ Date: _________
