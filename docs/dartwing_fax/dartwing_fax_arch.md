# Dartwing Fax Architecture - Section 1: Executive Summary

**Version:** 2.0 | **Date:** November 28, 2025

---

## 1.1 Purpose

This document defines the technical architecture for `dartwing_fax`, an enterprise fax platform built on Frappe Framework supporting:

- **Dartwing Fax**: General enterprise fax
- **MedxFax**: HIPAA-compliant healthcare variant

---

## 1.2 Architecture Principles

| Principle               | Implementation                               |
| ----------------------- | -------------------------------------------- |
| **Layered Abstraction** | Carrier Layer, Integration Layer, Core Layer |
| **Provider Agnostic**   | Pluggable carrier connectors                 |
| **Healthcare Ready**    | PHI detection, encryption, audit built-in    |
| **API First**           | Every feature via REST API                   |
| **Event Driven**        | Frappe hooks + Redis pub/sub                 |
| **Horizontal Scale**    | Worker pools, queue-based                    |

---

## 1.3 Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│ LAYER 1: INTEGRATION LAYER                  │
│ HIS, EHR, Pharmacy, Business connectors     │
│ Protocols: HL7, FHIR, NCPDP, REST          │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│ LAYER 2: CARRIER LAYER                      │
│ Telnyx, Bandwidth, SignalWire connectors    │
│ Failover, load balancing, health monitoring │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│ LAYER 3: CORE LAYER                         │
│ Fax, Routing, Security, Annotation engines  │
│ AI/OCR, Search, Audit, Notifications        │
└─────────────────────────────────────────────┘
```

---

## 1.4 Technology Stack

| Component   | Technology        |
| ----------- | ----------------- |
| Framework   | Frappe 16.x       |
| Language    | Python 3.11+      |
| Database    | MariaDB 10.11+    |
| Cache/Queue | Redis 7.x         |
| Search      | OpenSearch 2.x    |
| Storage     | S3/MinIO          |
| OCR         | Tesseract 5.x     |
| AI/ML       | TensorFlow, spaCy |
| Mobile      | Flutter           |
| Auth        | Keycloak          |
| Carriers    | Telnyx, Bandwidth |

---

## 1.5 Key Decisions

| Decision                  | Rationale                             |
| ------------------------- | ------------------------------------- |
| Multi-carrier abstraction | Avoid vendor lock-in, enable failover |
| Separate AI workers       | Scale OCR/ML independently            |
| OpenSearch                | Better full-text than MariaDB         |
| Redis queues              | Already in Frappe stack               |

---

**Next: Section 2 - System Overview**

# Dartwing Fax Architecture - Section 2: System Overview

---

## 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │Frappe Desk │ │Flutter Web │ │Flutter App │ │External API│   │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘   │
└────────┼──────────────┼──────────────┼──────────────┼───────────┘
         └──────────────┴──────────────┴──────────────┘
                              │
                    REST API + WebSocket
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                     APPLICATION LAYER                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   DARTWING FAX MODULE                       │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ INTEGRATION LAYER: HIS, Pharmacy, EHR connectors     │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ CARRIER LAYER: Telnyx, Bandwidth, SignalWire         │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ CORE LAYER: Fax, Routing, Security, AI, Audit        │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              FRAPPE FRAMEWORK + DARTWING CORE              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                      PROCESSING LAYER                            │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │OCR Workers│ │AI Workers │ │Queue Mgr  │ │Scheduler  │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                        DATA LAYER                                │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │ MariaDB   │ │  Redis    │ │ S3/MinIO  │ │OpenSearch │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                     EXTERNAL SERVICES                            │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │Fax Carriers│ │HIS/EHR   │ │Pharmacy   │ │Twilio/SG  │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2.2 Inbound Fax Flow

```
Carrier Webhook
      │
      ▼
┌─────────────┐
│1. Validate  │ Verify webhook signature
│   Webhook   │ Download fax file
└──────┬──────┘
       │
┌──────▼──────┐
│2. Tier 1    │ Whitelist → deliver
│   Security  │ Blacklist → reject
└──────┬──────┘
       │
┌──────▼──────┐
│3. Queue for │ Background processing
│   AI/OCR    │
└──────┬──────┘
       │
┌──────▼──────┐
│4. OCR       │ Text extraction
│   Engine    │ Entity extraction
└──────┬──────┘
       │
┌──────▼──────┐
│5. AI        │ Classification
│   Engine    │ PHI detection
└──────┬──────┘
       │
┌──────▼──────┐
│6. Tier 2    │ Spam scoring
│   Security  │ Hold if suspicious
└──────┬──────┘
       │
┌──────▼──────┐
│7. Routing   │ Apply rules
│   Engine    │ Assign user/inbox
└──────┬──────┘
       │
┌──────▼──────┐
│8. Notify    │ Email/SMS/Push
│             │ Webhooks
└──────┬──────┘
       │
       ▼
   User Inbox
```

---

## 2.3 Outbound Fax Flow

```
User/API Request
      │
      ▼
┌─────────────┐
│1. Auth      │ User permissions
│   Check     │ MFA if required
└──────┬──────┘
       │
┌──────▼──────┐
│2. Create    │ Fax Document
│   Document  │ status=Draft
└──────┬──────┘
       │
┌──────▼──────┐
│3. Queue     │ Add to send queue
│             │ Set priority
└──────┬──────┘
       │
┌──────▼──────┐
│4. Carrier   │ Select carrier
│   Manager   │ Failover if needed
└──────┬──────┘
       │
┌──────▼──────┐
│5. Send      │ Call carrier API
│             │ Track status
└──────┬──────┘
       │
┌──────▼──────┐
│6. Audit     │ Log result
│   + Notify  │ Update user
└─────────────┘
```

---

## 2.4 Multi-Tenancy

```
Organization (dartwing_core)
    │
    ├── Fax Settings (per-org config)
    │
    ├── Fax Numbers (DIDs)
    │
    ├── Fax Documents (org-scoped)
    │
    └── Users (via Org Member)
        ├── Fax User
        ├── Fax Admin
        └── Fax Auditor
```

All queries filtered by organization automatically.

---

**Next: Section 3 - Module Structure**

# Dartwing Fax Architecture - Section 3: Module Structure

---

## 3.1 Frappe Module Registration

```python
# apps/dartwing/dartwing/modules.txt
Dartwing Core
Dartwing User
Dartwing Fax          # ← This module
```

---

## 3.2 Directory Structure

```
apps/dartwing/dartwing/dartwing_fax/
│
├── __init__.py
├── hooks.py
├── patches/
│
├── doctype/                    # Frappe DocTypes
│   ├── fax_document/
│   ├── fax_settings/
│   ├── fax_provider/
│   ├── fax_number/
│   ├── fax_queue/
│   ├── fax_category/
│   ├── routing_rule/
│   ├── whitelist_entry/
│   ├── blacklist_entry/
│   ├── fax_challenge/
│   ├── signature/
│   ├── stamp_template/
│   ├── fax_audit_log/
│   ├── retention_policy/
│   ├── fax_webhook/
│   ├── fax_api_key/
│   ├── shared_inbox/
│   ├── fax_folder/
│   ├── alert_rule/
│   ├── his_connector/
│   └── pharmacy_connector/
│
├── carriers/                   # LAYER 2: Carrier Abstraction
│   ├── __init__.py
│   ├── base.py                 # Abstract interface
│   ├── manager.py              # Selection/failover
│   ├── telnyx/
│   │   ├── connector.py
│   │   └── webhook.py
│   ├── bandwidth/
│   │   ├── connector.py
│   │   └── webhook.py
│   ├── signalwire/
│   └── mock/                   # Testing
│
├── integrations/               # LAYER 1: External Systems
│   ├── __init__.py
│   ├── base.py
│   ├── manager.py
│   ├── healthcare/
│   │   ├── hl7/                # HL7 v2
│   │   ├── fhir/               # FHIR R4
│   │   ├── his/                # Epic, Cerner, etc.
│   │   └── pharmacy/           # Surescripts, NCPDP
│   └── business/
│       ├── salesforce.py
│       ├── docusign.py
│       └── google_drive.py
│
├── core/                       # LAYER 3: Business Logic
│   ├── __init__.py
│   ├── fax_engine.py
│   ├── routing_engine.py
│   ├── security_engine.py
│   ├── annotation_engine.py
│   ├── audit_engine.py
│   ├── search_engine.py
│   └── notification_engine.py
│
├── ai/                         # AI/ML Components
│   ├── ocr/
│   │   ├── engine.py
│   │   ├── tesseract.py
│   │   └── preprocessor.py
│   ├── classification/
│   │   ├── classifier.py
│   │   └── models.py
│   ├── extraction/
│   │   ├── entity_extractor.py
│   │   ├── form_parser.py
│   │   └── phi_detector.py
│   └── spam/
│       └── detector.py
│
├── api/                        # REST Endpoints
│   ├── v1/
│   │   ├── fax.py
│   │   ├── numbers.py
│   │   ├── routing.py
│   │   ├── search.py
│   │   └── webhooks.py
│   └── internal/
│
├── tasks/                      # Background Jobs
│   ├── process_inbound.py
│   ├── send_outbound.py
│   ├── ocr_processing.py
│   ├── ai_processing.py
│   ├── cleanup.py
│   └── health_check.py
│
├── utils/
│   ├── phone.py
│   ├── file_converter.py
│   ├── encryption.py
│   └── validators.py
│
├── flutter/                    # Flutter-specific
│   ├── api_schema.py
│   ├── push_notifications.py
│   └── offline_sync.py
│
├── templates/
├── public/
├── fixtures/
└── tests/
```

---

## 3.3 Module Dependencies

```
frappe
   │
   ▼
dartwing_core (Organization, Person)
   │
   ├──► dartwing_user (User Profile)
   │
   └──► dartwing_fax (This Module)
```

---

## 3.4 hooks.py

```python
app_name = "dartwing_fax"
app_title = "Dartwing Fax"
app_version = "2.0.0"

# DocType events
doc_events = {
    "Fax Document": {
        "after_insert": "dartwing_fax.events.fax.after_insert",
        "on_update": "dartwing_fax.events.fax.on_update",
        "validate": "dartwing_fax.events.fax.validate"
    }
}

# Scheduled tasks
scheduler_events = {
    "cron": {
        "* * * * *": [
            "dartwing_fax.tasks.send_outbound.process_queue",
            "dartwing_fax.tasks.health_check.check_carriers"
        ],
        "*/5 * * * *": [
            "dartwing_fax.tasks.send_outbound.retry_failed"
        ],
        "0 * * * *": [
            "dartwing_fax.tasks.cleanup.expire_challenges"
        ],
        "0 */6 * * *": [
            "dartwing_fax.tasks.sync_spam_db.sync"
        ],
        "0 2 * * *": [
            "dartwing_fax.tasks.cleanup.apply_retention"
        ]
    }
}

# Permission queries
permission_query_conditions = {
    "Fax Document": "dartwing_fax.permissions.fax_query"
}
```

---

**Next: Section 4 - DocType Architecture**

# Dartwing Fax Architecture - Section 4: DocType Architecture

---

## 4.1 DocType Overview

| DocType            | Purpose          | Type       | Phase |
| ------------------ | ---------------- | ---------- | ----- |
| **Core**           |                  |            |       |
| Fax Document       | Main fax record  | Standard   | 1     |
| Fax Settings       | Per-org config   | Single/Org | 1     |
| Fax Queue          | Outbound queue   | Standard   | 1     |
| Fax Number         | DID management   | Master     | 1     |
| Fax Provider       | Carrier config   | Master     | 1     |
| **AI/Routing**     |                  |            |       |
| Fax Category       | Classification   | Master     | 2     |
| Routing Rule       | Routing config   | Standard   | 2     |
| **Security**       |                  |            |       |
| Whitelist Entry    | Approved senders | Master     | 1     |
| Blacklist Entry    | Blocked senders  | Master     | 1     |
| Fax Challenge      | Tier 3 verify    | Standard   | 3     |
| Fax API Key        | API credentials  | Master     | 1     |
| **Annotation**     |                  |            |       |
| Signature          | User signatures  | Master     | 4     |
| Stamp Template     | Stamp designs    | Master     | 4     |
| **Compliance**     |                  |            |       |
| Fax Audit Log      | Immutable trail  | Immutable  | 1     |
| Retention Policy   | Retention rules  | Master     | 3     |
| **Collaboration**  |                  |            |       |
| Shared Inbox       | Team inboxes     | Master     | 2     |
| Fax Folder         | Organization     | Master     | 2     |
| Alert Rule         | Notifications    | Master     | 2     |
| Fax Webhook        | Outbound hooks   | Master     | 2     |
| **Healthcare**     |                  |            |       |
| HIS Connector      | HIS config       | Master     | 3     |
| Pharmacy Connector | Pharmacy config  | Master     | 3     |

---

## 4.2 Fax Document (Core DocType)

```
Fax Document
├── Basic Information
│   ├── organization (Link → Organization)
│   ├── direction (Select: Inbound/Outbound)
│   ├── status (Select: Received/Processing/Delivered/Held/Rejected/Draft/Queued/Sending/Sent/Failed)
│   ├── priority (Select: Low/Normal/High/Urgent)
│   ├── sender_number (Phone)
│   ├── sender_name (Data)
│   ├── recipient_number (Phone)
│   └── recipient_name (Data)
│
├── Timing
│   ├── received_at (Datetime)
│   ├── sent_at (Datetime)
│   ├── scheduled_at (Datetime)
│   └── duration_seconds (Int)
│
├── Document
│   ├── original_file (Attach) [Required]
│   ├── annotated_file (Attach)
│   ├── thumbnail (Attach Image)
│   ├── pages (Int)
│   ├── file_size (Int)
│   ├── file_hash (Data)
│   └── file_format (Select: PDF/TIFF)
│
├── AI Processing
│   ├── ocr_status (Select)
│   ├── ocr_text (Long Text)
│   ├── ocr_confidence (Percent)
│   ├── ai_category (Link → Fax Category)
│   ├── ai_confidence (Percent)
│   └── entities_json (JSON)
│
├── Security
│   ├── validation_status (Select)
│   ├── validation_tier (Int)
│   ├── spam_score (Percent)
│   ├── challenge (Link → Fax Challenge)
│   └── hold_reason (Data)
│
├── HIPAA/PHI (MedxFax)
│   ├── contains_phi (Check)
│   ├── phi_elements (JSON)
│   ├── patient_mrn (Data)
│   ├── patient_name (Data)
│   └── provider_npi (Data)
│
├── Assignment
│   ├── assigned_to (Link → User)
│   ├── assigned_group (Link → User Group)
│   ├── shared_inbox (Link → Shared Inbox)
│   ├── routed_by_rule (Link → Routing Rule)
│   └── routed_at (Datetime)
│
├── Carrier
│   ├── fax_provider (Link → Fax Provider)
│   ├── provider_fax_id (Data)
│   ├── delivery_receipt (Attach)
│   ├── error_message (Text)
│   └── retry_count (Int)
│
├── Organization
│   ├── folder (Link → Fax Folder)
│   ├── tags (Table MultiSelect)
│   ├── retention_policy (Link)
│   ├── legal_hold (Check)
│   └── archived (Check)
│
└── Child Tables
    ├── annotations (Table → Fax Annotation)
    └── routing_history (Table → Fax Routing History)
```

---

## 4.3 Fax Provider DocType

```
Fax Provider
├── provider_name (Data) [Unique]
├── provider_type (Select: Telnyx/Bandwidth/SignalWire/Custom)
├── enabled (Check)
├── priority (Int) [Lower = higher priority]
│
├── API Configuration
│   ├── api_endpoint (Data)
│   ├── api_key (Password)
│   ├── api_secret (Password)
│   ├── webhook_secret (Password)
│   └── webhook_url (Data) [Auto-generated]
│
├── Capabilities
│   ├── can_send (Check)
│   ├── can_receive (Check)
│   ├── can_provision_numbers (Check)
│   ├── supports_t38 (Check)
│   └── max_pages (Int)
│
├── Rate Limits
│   ├── rate_limit_per_minute (Int)
│   ├── rate_limit_per_hour (Int)
│   └── concurrent_limit (Int)
│
└── Health Status
    ├── health_status (Select: Healthy/Degraded/Down)
    ├── last_health_check (Datetime)
    ├── consecutive_failures (Int)
    └── last_failure_reason (Text)
```

---

## 4.4 Routing Rule DocType

```
Routing Rule
├── rule_name (Data)
├── organization (Link → Organization)
├── enabled (Check)
├── priority (Int) [Lower = higher priority]
├── description (Text)
│
├── conditions (Table → Routing Rule Condition)
│   ├── condition_type (Select: sender_number/recipient_did/ai_category/keyword/spam_score/phi_detected/etc.)
│   ├── operator (Select: equals/contains/greater_than/etc.)
│   ├── value (Data)
│   └── logic_operator (Select: AND/OR)
│
└── actions (Table → Routing Rule Action)
    ├── action_type (Select: route_to_user/route_to_inbox/set_priority/notify/webhook/push_to_his/etc.)
    ├── target_user (Link → User)
    ├── target_inbox (Link → Shared Inbox)
    ├── webhook (Link → Fax Webhook)
    ├── his_connector (Link → HIS Connector)
    └── stop_processing (Check)
```

---

## 4.5 Entity Relationship Diagram

```
Organization
    │
    ├──1:1── Fax Settings
    │            ├── primary_carrier ──► Fax Provider
    │            ├── his_connector ────► HIS Connector
    │            └── pharmacy_connector ► Pharmacy Connector
    │
    ├──1:N── Fax Number
    │
    ├──1:N── Fax Document
    │            ├── ai_category ───► Fax Category
    │            ├── assigned_to ───► User
    │            ├── shared_inbox ──► Shared Inbox
    │            ├── fax_provider ──► Fax Provider
    │            └── annotations ───► Fax Annotation (child)
    │
    ├──1:N── Routing Rule
    │            ├── conditions ───► Routing Rule Condition (child)
    │            └── actions ──────► Routing Rule Action (child)
    │
    ├──1:N── Whitelist Entry
    ├──1:N── Blacklist Entry
    └──1:N── Shared Inbox
```

---

**Next: Section 5 - Carrier Abstraction Layer**

# Dartwing Fax Architecture - Section 5: Carrier Abstraction Layer

---

## 5.1 Overview

The Carrier Layer abstracts fax transport providers, enabling:

- **Provider Independence**: Switch carriers without code changes
- **Automatic Failover**: Switch to backup on failures
- **Load Balancing**: Distribute across carriers
- **Health Monitoring**: Track availability

```
┌─────────────────────────────────────────────┐
│              CarrierManager                  │
│  • select_carrier()                         │
│  • failover()                               │
│  • health_check()                           │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌────▼────┐   ┌────▼────┐
│Telnyx │   │Bandwidth│   │SignalWire│
│Connector   │Connector│   │Connector│
└───────┘   └─────────┘   └─────────┘
```

---

## 5.2 Base Connector Interface

```python
# carriers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class FaxStatus(Enum):
    QUEUED = "queued"
    SENDING = "sending"
    DELIVERED = "delivered"
    FAILED = "failed"
    BUSY = "busy"
    NO_ANSWER = "no_answer"

@dataclass
class SendFaxRequest:
    recipient_number: str
    file_content: bytes
    file_type: str  # 'pdf' or 'tiff'
    sender_number: str
    sender_name: str = None
    quality: str = "standard"
    callback_url: str = None

@dataclass
class SendFaxResponse:
    success: bool
    provider_fax_id: str
    status: FaxStatus
    message: str = None

@dataclass
class InboundFaxEvent:
    provider_fax_id: str
    sender_number: str
    recipient_number: str
    pages: int
    file_url: str
    received_at: str

class CarrierConnector(ABC):
    """Abstract base for all carriers"""

    def __init__(self, config: "FaxProvider"):
        self.config = config
        self.name = config.provider_name
        self.api_key = config.api_key

    @abstractmethod
    async def send_fax(self, request: SendFaxRequest) -> SendFaxResponse:
        """Send a fax"""
        pass

    @abstractmethod
    async def get_status(self, provider_fax_id: str) -> FaxStatus:
        """Get fax status"""
        pass

    @abstractmethod
    async def download_fax(self, provider_fax_id: str) -> bytes:
        """Download fax content"""
        pass

    @abstractmethod
    async def cancel_fax(self, provider_fax_id: str) -> bool:
        """Cancel queued fax"""
        pass

    @abstractmethod
    def validate_webhook(self, request: dict, signature: str) -> bool:
        """Validate webhook signature"""
        pass

    @abstractmethod
    def parse_webhook(self, request: dict) -> InboundFaxEvent:
        """Parse webhook to normalized event"""
        pass

    @abstractmethod
    async def search_numbers(self, area_code: str) -> list[str]:
        """Search available DIDs"""
        pass

    @abstractmethod
    async def provision_number(self, phone: str) -> dict:
        """Provision a DID"""
        pass

    @abstractmethod
    async def release_number(self, phone: str) -> bool:
        """Release a DID"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check carrier health"""
        pass
```

---

## 5.3 Carrier Manager

```python
# carriers/manager.py
class CarrierManager:
    """Manages carriers with failover"""

    def __init__(self, organization: str):
        self.organization = organization
        self.connectors: dict[str, CarrierConnector] = {}
        self._load_carriers()

    def _load_carriers(self):
        """Load carrier configs"""
        settings = frappe.get_doc("Fax Settings",
            {"organization": self.organization})

        if settings.primary_carrier:
            self._add_carrier(settings.primary_carrier)
        if settings.secondary_carrier:
            self._add_carrier(settings.secondary_carrier)

    def _add_carrier(self, name: str):
        """Instantiate carrier connector"""
        provider = frappe.get_doc("Fax Provider", name)

        if provider.provider_type == "Telnyx":
            from .telnyx import TelnyxConnector
            self.connectors[name] = TelnyxConnector(provider)
        elif provider.provider_type == "Bandwidth":
            from .bandwidth import BandwidthConnector
            self.connectors[name] = BandwidthConnector(provider)
        # etc.

    def select_carrier(self, for_send=True) -> CarrierConnector:
        """Select best available carrier"""
        healthy = [c for c in self.connectors.values()
                   if self._is_healthy(c)]

        if not healthy:
            raise NoHealthyCarrierError()

        # Sort by priority
        healthy.sort(key=lambda c: c.config.priority)
        return healthy[0]

    async def send_with_failover(self, request: SendFaxRequest) -> SendFaxResponse:
        """Send with automatic failover"""
        carriers = self._get_sorted_carriers()
        last_error = None

        for carrier in carriers:
            try:
                response = await carrier.send_fax(request)
                if response.success:
                    self._record_success(carrier)
                    return response
            except Exception as e:
                last_error = e
                self._record_failure(carrier, str(e))
                continue

        raise AllCarriersFailedError(last_error)

    def _record_failure(self, carrier: CarrierConnector, reason: str):
        """Track carrier failure"""
        provider = carrier.config
        provider.consecutive_failures += 1
        provider.last_failure_reason = reason

        if provider.consecutive_failures >= 3:
            provider.health_status = "Down"

        provider.save()

    def _record_success(self, carrier: CarrierConnector):
        """Reset failure count on success"""
        provider = carrier.config
        provider.consecutive_failures = 0
        provider.health_status = "Healthy"
        provider.save()
```

---

## 5.4 Telnyx Connector Example

```python
# carriers/telnyx/connector.py
import telnyx
from ..base import CarrierConnector, SendFaxRequest, SendFaxResponse

class TelnyxConnector(CarrierConnector):

    def __init__(self, config):
        super().__init__(config)
        telnyx.api_key = config.api_key

    async def send_fax(self, request: SendFaxRequest) -> SendFaxResponse:
        try:
            fax = telnyx.Fax.create(
                connection_id=self.config.connection_id,
                to=request.recipient_number,
                from_=request.sender_number,
                media_url=self._upload_file(request.file_content),
                quality=request.quality,
                webhook_url=self.get_webhook_url()
            )
            return SendFaxResponse(
                success=True,
                provider_fax_id=fax.id,
                status=FaxStatus.QUEUED
            )
        except telnyx.error.TelnyxError as e:
            return SendFaxResponse(
                success=False,
                provider_fax_id=None,
                status=FaxStatus.FAILED,
                message=str(e)
            )

    def validate_webhook(self, request: dict, signature: str) -> bool:
        return telnyx.Webhook.verify(
            request, signature, self.config.webhook_secret
        )

    def parse_webhook(self, request: dict) -> InboundFaxEvent:
        data = request["data"]["payload"]
        return InboundFaxEvent(
            provider_fax_id=data["fax_id"],
            sender_number=data["from"],
            recipient_number=data["to"],
            pages=data["page_count"],
            file_url=data["media_url"],
            received_at=data["received_at"]
        )

    async def health_check(self) -> bool:
        try:
            telnyx.Balance.retrieve()
            return True
        except:
            return False
```

---

## 5.5 Webhook Handler

```python
# api/v1/webhooks.py
import frappe
from dartwing_fax.carriers.manager import CarrierManager

@frappe.whitelist(allow_guest=True)
def telnyx():
    """Handle Telnyx webhooks"""
    request = frappe.request.get_json()
    signature = frappe.request.headers.get("Telnyx-Signature")

    # Get connector and validate
    manager = CarrierManager.get_for_webhook("telnyx")
    connector = manager.get_connector("telnyx")

    if not connector.validate_webhook(request, signature):
        frappe.throw("Invalid signature", frappe.AuthenticationError)

    # Parse and process
    event_type = request.get("data", {}).get("event_type")

    if event_type == "fax.received":
        event = connector.parse_webhook(request)
        frappe.enqueue(
            "dartwing_fax.tasks.process_inbound.process",
            event=event,
            carrier="telnyx"
        )

    elif event_type == "fax.sent":
        _update_outbound_status(request)

    return {"status": "ok"}
```

---

**Next: Section 6 - Healthcare Integration Layer**

# Dartwing Fax Architecture - Section 6: Healthcare Integration Layer

---

## 6.1 Overview

The Healthcare Integration Layer connects MedxFax to clinical systems:

```
┌─────────────────────────────────────────────────────────────┐
│                 HEALTHCARE INTEGRATION LAYER                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  IntegrationManager                          │
│  • route_to_his()                                           │
│  • lookup_patient()                                         │
│  • verify_provider()                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
     ┌──────────────────────┼──────────────────────┐
     │                      │                      │
┌────▼─────┐          ┌─────▼─────┐          ┌────▼─────┐
│ HIS/EHR  │          │ Pharmacy  │          │ Business │
│ Connectors│          │ Connectors│          │Connectors│
├──────────┤          ├───────────┤          ├──────────┤
│ • Epic   │          │• Surescripts          │• Salesforce
│ • Cerner │          │• NCPDP    │          │• DocuSign│
│ • Meditech          │• PioneerRx│          │• Google  │
│ • FHIR   │          │• McKesson │          │• M365    │
└──────────┘          └───────────┘          └──────────┘
```

---

## 6.2 Protocol Support

| Protocol     | Use Case               | Standard         |
| ------------ | ---------------------- | ---------------- |
| HL7 v2.x     | ADT, ORM, ORU messages | Most HIS systems |
| FHIR R4      | Modern EHR integration | Epic, Cerner     |
| NCPDP SCRIPT | Prescriptions          | Surescripts      |
| X12          | Claims, eligibility    | Payers           |
| REST         | Custom integrations    | Various          |
| SOAP         | Legacy systems         | Some HIS         |

---

## 6.3 Base Integration Interface

```python
# integrations/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PatientMatch:
    mrn: str
    name: str
    dob: str
    confidence: float
    source_system: str

@dataclass
class ProviderInfo:
    npi: str
    name: str
    specialty: str
    dea: str = None
    verified: bool = False

class HealthcareConnector(ABC):
    """Base class for healthcare integrations"""

    @abstractmethod
    async def lookup_patient(self, identifiers: dict) -> list[PatientMatch]:
        """Find patient by MRN, name, DOB, etc."""
        pass

    @abstractmethod
    async def verify_provider(self, npi: str) -> ProviderInfo:
        """Verify provider credentials"""
        pass

    @abstractmethod
    async def push_document(self, fax: "FaxDocument", doc_type: str) -> bool:
        """Push fax to patient chart"""
        pass

    @abstractmethod
    async def create_task(self, fax: "FaxDocument", task_type: str) -> str:
        """Create follow-up task in HIS"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check connectivity"""
        pass
```

---

## 6.4 HIS Connector (Epic Example)

```python
# integrations/healthcare/his/epic.py
from ..base import HealthcareConnector, PatientMatch

class EpicConnector(HealthcareConnector):
    """Epic EHR integration via FHIR R4"""

    def __init__(self, config: "HISConnector"):
        self.base_url = config.api_endpoint
        self.client_id = config.client_id
        self.private_key = config.private_key
        self._token = None

    async def _get_token(self):
        """Get OAuth2 token using JWT assertion"""
        if self._token and not self._token_expired():
            return self._token

        # Epic uses SMART Backend Services
        assertion = self._create_jwt_assertion()
        response = await self._post_token(assertion)
        self._token = response["access_token"]
        return self._token

    async def lookup_patient(self, identifiers: dict) -> list[PatientMatch]:
        """Search patient via FHIR Patient resource"""
        token = await self._get_token()

        params = {}
        if identifiers.get("mrn"):
            params["identifier"] = f"MRN|{identifiers['mrn']}"
        if identifiers.get("name"):
            params["name"] = identifiers["name"]
        if identifiers.get("dob"):
            params["birthdate"] = identifiers["dob"]

        response = await self._fhir_search("Patient", params, token)

        matches = []
        for entry in response.get("entry", []):
            patient = entry["resource"]
            matches.append(PatientMatch(
                mrn=self._extract_mrn(patient),
                name=self._format_name(patient),
                dob=patient.get("birthDate"),
                confidence=0.9,
                source_system="Epic"
            ))
        return matches

    async def push_document(self, fax: "FaxDocument", doc_type: str) -> bool:
        """Create DocumentReference in Epic"""
        token = await self._get_token()

        # Upload binary
        binary_id = await self._upload_binary(fax.original_file, token)

        # Create DocumentReference
        doc_ref = {
            "resourceType": "DocumentReference",
            "status": "current",
            "type": {"coding": [{"code": doc_type}]},
            "subject": {"reference": f"Patient/{fax.patient_mrn}"},
            "content": [{
                "attachment": {
                    "contentType": "application/pdf",
                    "url": f"Binary/{binary_id}"
                }
            }],
            "context": {
                "related": [{
                    "display": f"Fax from {fax.sender_number}"
                }]
            }
        }

        await self._fhir_create("DocumentReference", doc_ref, token)
        return True
```

---

## 6.5 Pharmacy Connector (Surescripts Example)

```python
# integrations/healthcare/pharmacy/surescripts.py
from ..base import HealthcareConnector

class SurescriptsConnector(HealthcareConnector):
    """Surescripts e-prescribing network"""

    def __init__(self, config: "PharmacyConnector"):
        self.base_url = config.api_endpoint
        self.sender_id = config.sender_id
        self.password = config.password

    async def verify_provider(self, npi: str) -> ProviderInfo:
        """Verify prescriber via Surescripts directory"""
        response = await self._directory_search(npi)

        if not response.get("prescribers"):
            return ProviderInfo(npi=npi, verified=False)

        prescriber = response["prescribers"][0]
        return ProviderInfo(
            npi=npi,
            name=prescriber["name"],
            specialty=prescriber["specialty"],
            dea=prescriber.get("dea"),
            verified=True
        )

    async def send_refill_response(self, fax: "FaxDocument",
                                    status: str) -> bool:
        """Send NCPDP SCRIPT RefillResponse"""
        # Build NCPDP message
        message = self._build_refill_response(fax, status)

        # Send via Surescripts
        response = await self._send_ncpdp(message)
        return response.get("status") == "success"
```

---

## 6.6 HL7 v2 Support

```python
# integrations/healthcare/hl7/parser.py
from hl7apy.parser import parse_message
from hl7apy.core import Message

class HL7Parser:
    """Parse and build HL7 v2 messages"""

    @staticmethod
    def parse(raw_message: str) -> dict:
        """Parse HL7 message to dict"""
        msg = parse_message(raw_message)
        return {
            "type": str(msg.msh.msh_9),
            "control_id": str(msg.msh.msh_10),
            "patient": HL7Parser._extract_patient(msg),
            "order": HL7Parser._extract_order(msg) if hasattr(msg, 'orc') else None
        }

    @staticmethod
    def build_oru(fax: "FaxDocument", result_type: str) -> str:
        """Build ORU (Observation Result) message"""
        msg = Message("ORU_R01")

        # MSH segment
        msg.msh.msh_3 = "DARTWING_FAX"
        msg.msh.msh_9 = "ORU^R01"

        # PID segment (patient)
        msg.pid.pid_3 = fax.patient_mrn
        msg.pid.pid_5 = fax.patient_name

        # OBR segment (observation request)
        msg.obr.obr_4 = result_type

        # OBX segment (observation)
        msg.obx.obx_2 = "ED"  # Encapsulated Data
        msg.obx.obx_5 = self._encode_pdf(fax.original_file)

        return msg.to_er7()
```

---

## 6.7 Integration Manager

```python
# integrations/manager.py
class IntegrationManager:
    """Orchestrates healthcare integrations"""

    def __init__(self, organization: str):
        self.organization = organization
        self.his_connector = None
        self.pharmacy_connector = None
        self._load_connectors()

    def _load_connectors(self):
        settings = frappe.get_doc("Fax Settings",
            {"organization": self.organization})

        if settings.his_connector:
            self.his_connector = self._create_his_connector(
                settings.his_connector)

        if settings.pharmacy_connector:
            self.pharmacy_connector = self._create_pharmacy_connector(
                settings.pharmacy_connector)

    async def auto_route_to_patient(self, fax: "FaxDocument") -> bool:
        """Match fax to patient and push to chart"""
        if not self.his_connector:
            return False

        # Extract patient identifiers from fax
        identifiers = self._extract_identifiers(fax)

        # Lookup patient
        matches = await self.his_connector.lookup_patient(identifiers)

        if not matches:
            return False

        # Use highest confidence match
        best_match = max(matches, key=lambda m: m.confidence)

        if best_match.confidence < 0.8:
            # Low confidence - queue for review
            fax.status = "Held"
            fax.hold_reason = "Patient match needs verification"
            fax.save()
            return False

        # Push to chart
        fax.patient_mrn = best_match.mrn
        fax.patient_name = best_match.name
        await self.his_connector.push_document(fax, "FAX")
        fax.save()
        return True
```

---

## 6.8 HIS Connector DocType

```
HIS Connector
├── connector_name (Data)
├── connector_type (Select: Epic/Cerner/Meditech/FHIR_Generic/HL7_Generic)
├── enabled (Check)
│
├── Connection
│   ├── api_endpoint (Data)
│   ├── client_id (Data)
│   ├── client_secret (Password)
│   ├── private_key (Text) [For JWT auth]
│   └── hl7_port (Int) [For MLLP]
│
├── Capabilities
│   ├── can_lookup_patient (Check)
│   ├── can_verify_provider (Check)
│   ├── can_push_documents (Check)
│   └── can_create_tasks (Check)
│
└── Mapping
    ├── patient_id_system (Data)
    ├── document_type_mapping (JSON)
    └── department_mapping (JSON)
```

---

**Next: Section 7 - AI/ML Pipeline**

# Dartwing Fax Architecture - Section 7: AI/ML Pipeline

---

## 7.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML PIPELINE                              │
└─────────────────────────────────────────────────────────────────┘

Fax Document
      │
      ▼
┌─────────────┐
│1. Preprocess│ Deskew, denoise, enhance contrast
└──────┬──────┘
       │
┌──────▼──────┐
│2. OCR       │ Tesseract → text + hOCR
│             │ ABBYY fallback for handwriting
└──────┬──────┘
       │
┌──────▼──────┐
│3. Classify  │ NLP model → category + confidence
└──────┬──────┘
       │
┌──────▼──────┐
│4. Extract   │ Named entities (patient, provider, dates)
│   Entities  │ Form fields (CMS-1500, W-9, Rx)
└──────┬──────┘
       │
┌──────▼──────┐
│5. PHI Detect│ SSN, DOB, MRN, diagnoses (MedxFax)
└──────┬──────┘
       │
┌──────▼──────┐
│6. Spam Score│ LightGBM → 0-100 score
└──────┬──────┘
       │
       ▼
   Processed Fax
```

---

## 7.2 OCR Engine

```python
# ai/ocr/engine.py
from dataclasses import dataclass

@dataclass
class OCRResult:
    full_text: str
    confidence: float
    pages: list[dict]  # Per-page text + bounding boxes
    hocr: str          # hOCR XML for positioning
    language: str

class OCREngine:
    """Orchestrates OCR processing"""

    def __init__(self, config: dict):
        self.primary = TesseractOCR(config)
        self.fallback = ABBYYFallback(config) if config.get("abbyy_key") else None
        self.preprocessor = ImagePreprocessor()

    async def process(self, file_path: str) -> OCRResult:
        """Run OCR pipeline"""
        # Preprocess images
        images = self.preprocessor.prepare(file_path)

        # Primary OCR
        result = await self.primary.extract(images)

        # Fallback for low confidence (likely handwriting)
        if result.confidence < 0.6 and self.fallback:
            fallback_result = await self.fallback.extract(images)
            if fallback_result.confidence > result.confidence:
                result = fallback_result

        return result

# ai/ocr/tesseract.py
import pytesseract
from PIL import Image

class TesseractOCR:
    """Tesseract 5.x wrapper"""

    def __init__(self, config: dict):
        self.language = config.get("language", "eng")
        self.config = "--oem 3 --psm 3"  # LSTM + auto page seg

    async def extract(self, images: list[Image]) -> OCRResult:
        pages = []
        full_text = []
        total_conf = 0

        for i, img in enumerate(images):
            # Get text with confidence
            data = pytesseract.image_to_data(
                img, lang=self.language,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )

            page_text = " ".join(data["text"])
            page_conf = sum(data["conf"]) / len(data["conf"])

            pages.append({
                "page": i + 1,
                "text": page_text,
                "confidence": page_conf,
                "words": self._build_word_boxes(data)
            })

            full_text.append(page_text)
            total_conf += page_conf

        # Get hOCR
        hocr = pytesseract.image_to_pdf_or_hocr(
            images[0], extension="hocr", lang=self.language
        )

        return OCRResult(
            full_text="\n\n".join(full_text),
            confidence=total_conf / len(images),
            pages=pages,
            hocr=hocr.decode(),
            language=self.language
        )
```

---

## 7.3 Image Preprocessor

```python
# ai/ocr/preprocessor.py
import cv2
import numpy as np
from PIL import Image

class ImagePreprocessor:
    """Enhance images for better OCR"""

    def prepare(self, file_path: str) -> list[Image]:
        """Convert PDF/TIFF to preprocessed images"""
        images = self._load_pages(file_path)
        return [self._enhance(img) for img in images]

    def _enhance(self, img: np.ndarray) -> Image:
        """Apply enhancement pipeline"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Deskew
        gray = self._deskew(gray)

        # Denoise
        gray = cv2.fastNlMeansDenoising(gray, h=10)

        # Enhance contrast (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        # Binarize (Otsu's method)
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return Image.fromarray(binary)

    def _deskew(self, img: np.ndarray) -> np.ndarray:
        """Correct skew angle"""
        coords = np.column_stack(np.where(img > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = 90 + angle

        if abs(angle) > 0.5:
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE)

        return img
```

---

## 7.4 NLP Classifier

```python
# ai/classification/classifier.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

CATEGORIES = [
    "prescription", "lab_results", "referral", "prior_auth",
    "medical_records", "invoice", "contract", "purchase_order",
    "resume", "marketing", "legal", "insurance", "other"
]

class FaxClassifier:
    """Document classification using fine-tuned transformer"""

    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

    def classify(self, text: str) -> tuple[str, float, list]:
        """Classify text, return (category, confidence, all_scores)"""
        # Tokenize
        inputs = self.tokenizer(
            text[:512],  # Truncate to max length
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0]

        # Get top prediction
        top_idx = probs.argmax().item()
        top_category = CATEGORIES[top_idx]
        top_confidence = probs[top_idx].item()

        # Get all scores for secondary categories
        all_scores = [
            {"category": CATEGORIES[i], "score": probs[i].item()}
            for i in range(len(CATEGORIES))
        ]
        all_scores.sort(key=lambda x: x["score"], reverse=True)

        return top_category, top_confidence, all_scores
```

---

## 7.5 Entity Extractor

```python
# ai/extraction/entity_extractor.py
import spacy
import re
from dataclasses import dataclass

@dataclass
class ExtractedEntity:
    entity_type: str
    value: str
    normalized: str = None
    confidence: float = 1.0
    start: int = 0
    end: int = 0

class EntityExtractor:
    """Extract named entities from fax text"""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> dict:
        return {
            "SSN": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "PHONE": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "NPI": re.compile(r'\bNPI[:\s]*(\d{10})\b', re.I),
            "DEA": re.compile(r'\bDEA[:\s]*([A-Z]{2}\d{7})\b', re.I),
            "MRN": re.compile(r'\bMRN[:\s#]*(\w+)\b', re.I),
            "DOB": re.compile(r'\b(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](\d{2}|\d{4})\b'),
            "ICD10": re.compile(r'\b[A-Z]\d{2}\.?\d{0,2}\b'),
            "NDC": re.compile(r'\b\d{5}-\d{4}-\d{2}\b'),
        }

    def extract(self, text: str) -> list[ExtractedEntity]:
        entities = []

        # SpaCy NER
        doc = self.nlp(text)
        for ent in doc.ents:
            entities.append(ExtractedEntity(
                entity_type=ent.label_,
                value=ent.text,
                start=ent.start_char,
                end=ent.end_char
            ))

        # Regex patterns for domain-specific entities
        for entity_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                value = match.group(1) if match.groups() else match.group()
                entities.append(ExtractedEntity(
                    entity_type=entity_type,
                    value=value,
                    normalized=self._normalize(entity_type, value),
                    start=match.start(),
                    end=match.end()
                ))

        return entities

    def _normalize(self, entity_type: str, value: str) -> str:
        if entity_type == "PHONE":
            digits = re.sub(r'\D', '', value)
            return f"+1{digits}" if len(digits) == 10 else digits
        if entity_type == "DOB":
            # Convert to ISO format
            return self._parse_date(value)
        return value
```

---

## 7.6 PHI Detector (MedxFax)

```python
# ai/extraction/phi_detector.py
PHI_TYPES = [
    "patient_name", "dob", "ssn", "mrn", "account_number",
    "health_plan_id", "diagnosis", "medication", "lab_result",
    "address", "phone", "email", "provider_name"
]

class PHIDetector:
    """Detect Protected Health Information"""

    def __init__(self, entity_extractor: EntityExtractor):
        self.extractor = entity_extractor
        self.phi_mapping = {
            "PERSON": "patient_name",
            "SSN": "ssn",
            "DOB": "dob",
            "MRN": "mrn",
            "ICD10": "diagnosis",
            "NDC": "medication"
        }

    def detect(self, text: str) -> dict:
        """Detect PHI elements, return summary"""
        entities = self.extractor.extract(text)

        phi_found = {}
        for entity in entities:
            if entity.entity_type in self.phi_mapping:
                phi_type = self.phi_mapping[entity.entity_type]
                if phi_type not in phi_found:
                    phi_found[phi_type] = []
                phi_found[phi_type].append({
                    "value_hash": self._hash_value(entity.value),
                    "position": [entity.start, entity.end]
                })

        return {
            "contains_phi": len(phi_found) > 0,
            "phi_types": list(phi_found.keys()),
            "phi_count": sum(len(v) for v in phi_found.values()),
            "elements": phi_found  # Hashed, not raw values
        }

    def _hash_value(self, value: str) -> str:
        """Hash PHI for logging without exposing data"""
        import hashlib
        return hashlib.sha256(value.encode()).hexdigest()[:16]
```

---

## 7.7 Spam Detector

```python
# ai/spam/detector.py
import lightgbm as lgb
import numpy as np

class SpamDetector:
    """Score spam likelihood 0-100"""

    def __init__(self, model_path: str):
        self.model = lgb.Booster(model_file=model_path)
        self.feature_names = self._get_feature_names()

    def score(self, fax: "FaxDocument", text: str) -> int:
        """Calculate spam score"""
        features = self._extract_features(fax, text)
        feature_vector = np.array([[features[f] for f in self.feature_names]])

        prob = self.model.predict(feature_vector)[0]
        return int(prob * 100)

    def _extract_features(self, fax, text: str) -> dict:
        return {
            # Content features
            "text_length": len(text),
            "word_count": len(text.split()),
            "uppercase_ratio": sum(1 for c in text if c.isupper()) / max(len(text), 1),
            "digit_ratio": sum(1 for c in text if c.isdigit()) / max(len(text), 1),
            "special_char_ratio": sum(1 for c in text if not c.isalnum()) / max(len(text), 1),

            # Spam keyword density
            "free_count": text.lower().count("free"),
            "offer_count": text.lower().count("offer"),
            "limited_count": text.lower().count("limited"),
            "act_now_count": text.lower().count("act now"),

            # Sender features
            "is_toll_free": fax.sender_number.startswith("+1800") or fax.sender_number.startswith("+1888"),
            "sender_in_whitelist": self._check_whitelist(fax.sender_number),

            # Timing features
            "is_overnight": self._is_overnight(fax.received_at),
            "is_weekend": self._is_weekend(fax.received_at),

            # Page features
            "page_count": fax.pages,
            "is_single_page": fax.pages == 1,
        }
```

---

## 7.8 AI Pipeline Orchestration

```python
# ai/pipeline.py
class AIPipeline:
    """Orchestrates full AI processing"""

    def __init__(self, config: dict):
        self.ocr = OCREngine(config)
        self.classifier = FaxClassifier(config["model_path"])
        self.extractor = EntityExtractor()
        self.phi_detector = PHIDetector(self.extractor)
        self.spam_detector = SpamDetector(config["spam_model"])

    async def process(self, fax: "FaxDocument") -> dict:
        """Run full pipeline"""
        # OCR
        ocr_result = await self.ocr.process(fax.original_file)

        # Classification
        category, confidence, all_scores = self.classifier.classify(
            ocr_result.full_text)

        # Entity extraction
        entities = self.extractor.extract(ocr_result.full_text)

        # PHI detection (MedxFax)
        phi_result = self.phi_detector.detect(ocr_result.full_text)

        # Spam scoring
        spam_score = self.spam_detector.score(fax, ocr_result.full_text)

        return {
            "ocr_text": ocr_result.full_text,
            "ocr_confidence": ocr_result.confidence,
            "ai_category": category,
            "ai_confidence": confidence,
            "ai_secondary": all_scores[:3],
            "entities": [e.__dict__ for e in entities],
            "phi": phi_result,
            "spam_score": spam_score
        }
```

---

**Next: Section 8 - Security Architecture**

# Dartwing Fax Architecture - Section 8: Security Architecture

---

## 8.1 Three-Tier Validation

```
┌─────────────────────────────────────────────────────────────────┐
│                    INBOUND SECURITY PIPELINE                     │
└─────────────────────────────────────────────────────────────────┘

Inbound Fax
      │
      ▼
┌─────────────────────────────────────────┐
│ TIER 1: Whitelist/Blacklist             │
│ ─────────────────────────────────────── │
│ • O(1) lookup via Redis Bloom filter    │
│ • Whitelist → bypass AI, deliver        │
│ • Blacklist → reject immediately        │
│ • Neither → continue to Tier 2          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ TIER 2: AI Spam Scoring                 │
│ ─────────────────────────────────────── │
│ • LightGBM model → score 0-100          │
│ • 0-30: Low risk → deliver              │
│ • 31-80: Medium → challenge (Tier 3)    │
│ • 81-100: High → reject                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ TIER 3: Challenge Verification          │
│ ─────────────────────────────────────── │
│ • Send challenge fax to sender          │
│ • 6-digit code + QR code                │
│ • 24-hour timeout                       │
│ • Valid response → whitelist + deliver  │
│ • No response → delete                  │
└─────────────────────────────────────────┘
```

---

## 8.2 Security Engine

```python
# core/security_engine.py
class SecurityEngine:
    """Three-tier inbound validation"""

    def __init__(self, organization: str):
        self.org = organization
        self.settings = get_fax_settings(organization)
        self.bloom_filter = self._load_bloom_filter()

    async def validate(self, fax: "FaxDocument") -> ValidationResult:
        """Run validation pipeline"""

        # Tier 1: Whitelist/Blacklist
        if self.settings.enable_tier1_validation:
            tier1 = await self._check_tier1(fax.sender_number)
            if tier1.decision != "continue":
                return tier1

        # Tier 2: AI Spam Score
        if self.settings.enable_tier2_validation:
            tier2 = await self._check_tier2(fax)
            if tier2.decision != "continue":
                return tier2

        # Default: deliver
        return ValidationResult(
            status="passed",
            tier=2,
            decision="deliver"
        )

    async def _check_tier1(self, sender: str) -> ValidationResult:
        """Check whitelist/blacklist"""
        # Normalize number
        sender = normalize_phone(sender)

        # Check whitelist first
        if self._in_whitelist(sender):
            return ValidationResult(
                status="whitelisted",
                tier=1,
                decision="deliver",
                bypass_ai=self.settings.whitelist_bypass_ai
            )

        # Check blacklist
        if self._in_blacklist(sender):
            return ValidationResult(
                status="blacklisted",
                tier=1,
                decision="reject",
                reason="Sender is blacklisted"
            )

        return ValidationResult(status="unknown", tier=1, decision="continue")

    async def _check_tier2(self, fax: "FaxDocument") -> ValidationResult:
        """AI spam scoring"""
        score = fax.spam_score or 0

        if score <= self.settings.spam_threshold_deliver:
            return ValidationResult(
                status="passed",
                tier=2,
                decision="deliver",
                spam_score=score
            )

        if score <= self.settings.spam_threshold_hold:
            # Trigger Tier 3 challenge
            if self.settings.enable_tier3_validation:
                return ValidationResult(
                    status="challenged",
                    tier=2,
                    decision="challenge",
                    spam_score=score
                )
            else:
                return ValidationResult(
                    status="held",
                    tier=2,
                    decision="hold",
                    spam_score=score
                )

        # High spam score - reject
        return ValidationResult(
            status="rejected",
            tier=2,
            decision="reject",
            spam_score=score,
            reason=f"Spam score {score} exceeds threshold"
        )

    def _in_whitelist(self, number: str) -> bool:
        """O(1) whitelist lookup"""
        # Check Bloom filter first (fast negative)
        if not self.bloom_filter.check(f"wl:{number}"):
            return False
        # Confirm with DB (handles false positives)
        return frappe.db.exists("Whitelist Entry", {
            "phone_number": number,
            "organization": self.org
        })
```

---

## 8.3 Challenge System

```python
# core/challenge.py
import secrets
from datetime import timedelta

class ChallengeManager:
    """Tier 3 fax-back challenge"""

    def create_challenge(self, fax: "FaxDocument") -> "FaxChallenge":
        """Create and send challenge"""
        # Generate code
        code = secrets.token_hex(3).upper()  # 6-char hex

        # Create challenge record
        challenge = frappe.get_doc({
            "doctype": "Fax Challenge",
            "fax_document": fax.name,
            "sender_number": fax.sender_number,
            "challenge_code": code,
            "expires_at": now() + timedelta(hours=24),
            "status": "pending"
        })
        challenge.insert()

        # Generate challenge PDF
        pdf = self._generate_challenge_pdf(code, challenge.name)

        # Send challenge fax
        send_fax(
            recipient=fax.sender_number,
            file=pdf,
            sender=fax.recipient_number,
            priority="high"
        )

        # Hold original fax
        fax.status = "Held"
        fax.hold_reason = "Awaiting challenge response"
        fax.challenge = challenge.name
        fax.save()

        return challenge

    def verify_response(self, sender: str, text: str) -> bool:
        """Verify challenge response from OCR text"""
        # Find pending challenge for this sender
        challenge = frappe.get_doc("Fax Challenge", {
            "sender_number": sender,
            "status": "pending"
        })

        if not challenge or challenge.expires_at < now():
            return False

        # Extract code from response
        code = self._extract_code(text)

        if code == challenge.challenge_code:
            # Success - release fax and whitelist
            self._release_fax(challenge.fax_document)
            self._add_to_whitelist(sender)
            challenge.status = "verified"
            challenge.save()
            return True

        return False
```

---

## 8.4 Encryption

```python
# utils/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class FaxEncryption:
    """AES-256 encryption for fax documents"""

    def __init__(self):
        self.key = self._derive_key()
        self.fernet = Fernet(self.key)

    def _derive_key(self) -> bytes:
        """Derive key from site secret"""
        secret = frappe.conf.get("encryption_key") or frappe.conf.secret
        salt = b"dartwing_fax_v2"

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
        return key

    def encrypt_file(self, content: bytes) -> bytes:
        """Encrypt file content"""
        return self.fernet.encrypt(content)

    def decrypt_file(self, encrypted: bytes) -> bytes:
        """Decrypt file content"""
        return self.fernet.decrypt(encrypted)

    def encrypt_phi(self, data: dict) -> str:
        """Encrypt PHI JSON"""
        import json
        return self.fernet.encrypt(json.dumps(data).encode()).decode()

    def decrypt_phi(self, encrypted: str) -> dict:
        """Decrypt PHI JSON"""
        import json
        return json.loads(self.fernet.decrypt(encrypted.encode()))
```

---

## 8.5 API Authentication

```python
# api/auth.py
import jwt
import hmac
import hashlib

class APIAuthenticator:
    """API key + JWT authentication"""

    def authenticate(self, request) -> tuple[bool, str]:
        """Authenticate API request"""
        auth_header = request.headers.get("Authorization", "")

        # Bearer token (JWT)
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            return self._verify_jwt(token)

        # API Key
        api_key = request.headers.get("X-API-Key")
        api_secret = request.headers.get("X-API-Secret")
        if api_key:
            return self._verify_api_key(api_key, api_secret, request)

        return False, "No authentication provided"

    def _verify_jwt(self, token: str) -> tuple[bool, str]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                frappe.conf.jwt_secret,
                algorithms=["HS256"]
            )
            return True, payload.get("sub")
        except jwt.ExpiredSignatureError:
            return False, "Token expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"

    def _verify_api_key(self, key: str, secret: str, request) -> tuple[bool, str]:
        """Verify API key and optional signature"""
        api_key_doc = frappe.get_doc("Fax API Key", {"api_key": key})

        if not api_key_doc or not api_key_doc.enabled:
            return False, "Invalid API key"

        if api_key_doc.api_secret != secret:
            return False, "Invalid API secret"

        # Check rate limit
        if not self._check_rate_limit(key, api_key_doc.rate_limit):
            return False, "Rate limit exceeded"

        return True, api_key_doc.organization
```

---

## 8.6 Audit Logging

```python
# core/audit_engine.py
class AuditEngine:
    """Immutable audit trail"""

    EVENTS = [
        "fax.received", "fax.sent", "fax.viewed", "fax.downloaded",
        "fax.annotated", "fax.signed", "fax.forwarded", "fax.deleted",
        "fax.held", "fax.released", "fax.rejected",
        "phi.accessed", "phi.exported", "settings.changed"
    ]

    def log(self, event: str, fax: str = None, details: dict = None):
        """Create immutable audit log entry"""
        log = frappe.get_doc({
            "doctype": "Fax Audit Log",
            "event_type": event,
            "fax_document": fax,
            "user": frappe.session.user,
            "timestamp": now(),
            "ip_address": frappe.request.remote_addr if frappe.request else None,
            "user_agent": frappe.request.user_agent if frappe.request else None,
            "details": json.dumps(details) if details else None,
            "hash": self._compute_hash(event, fax, details)
        })
        log.flags.ignore_permissions = True
        log.insert()

        # Also send to SIEM if configured
        self._send_to_siem(log)

    def _compute_hash(self, event: str, fax: str, details: dict) -> str:
        """Compute hash for tamper detection"""
        import hashlib
        content = f"{event}|{fax}|{json.dumps(details)}|{now()}"
        return hashlib.sha256(content.encode()).hexdigest()

    def log_phi_access(self, fax: str, phi_types: list):
        """Log PHI access for HIPAA"""
        self.log("phi.accessed", fax, {
            "phi_types": phi_types,
            "access_reason": "user_request"
        })
```

---

## 8.7 HIPAA Security Controls

| Control                   | Implementation                                 |
| ------------------------- | ---------------------------------------------- |
| **Access Control**        | RBAC via Frappe permissions, minimum necessary |
| **Audit Controls**        | Immutable Fax Audit Log, PHI access logging    |
| **Transmission Security** | TLS 1.3 required, no fallback                  |
| **Encryption at Rest**    | AES-256 for files, encrypted PHI fields        |
| **Integrity Controls**    | File hashing, audit log hashing                |
| **Authentication**        | Keycloak SSO, MFA required for PHI access      |
| **Automatic Logoff**      | Session timeout 15 min idle                    |
| **Unique User ID**        | User linked to all actions                     |

---

## 8.8 Outbound Security

```python
# core/outbound_security.py
class OutboundSecurity:
    """Outbound fax security controls"""

    def validate_send(self, user: str, request: dict) -> bool:
        """Validate outbound fax request"""
        # Check user has send permission
        if not self._has_send_permission(user):
            raise PermissionError("User cannot send faxes")

        # Check rate limit
        if not self._check_rate_limit(user):
            raise RateLimitError("Rate limit exceeded")

        # Verify sender number is owned
        if not self._verify_sender_number(request["sender_number"]):
            raise ValidationError("Sender number not authorized")

        # MFA for sensitive sends (optional)
        if self._requires_mfa(request):
            if not self._verify_mfa(user):
                raise MFARequiredError("MFA required for this send")

        return True

    def inject_csid(self, fax: "FaxDocument") -> str:
        """Generate verifiable CSID"""
        date = now().strftime("%Y%m%d")
        code = secrets.token_hex(2).upper()
        return f"DFX-{date}-{code}"
```

---

**Next: Section 9 - Flutter Mobile Architecture**

# Dartwing Fax Architecture - Section 9: Flutter Mobile Architecture

---

## 9.1 Overview

The Dartwing Flutter app integrates fax functionality into the existing mobile experience:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DARTWING FLUTTER APP                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │Fax Inbox  │ │Fax Viewer │ │Send Fax   │ │Signature  │       │
│  │Screen     │ │Screen     │ │Screen     │ │Screen     │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                       STATE MANAGEMENT                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │FaxCubit   │ │InboxCubit │ │SendCubit  │ │SignCubit  │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                      REPOSITORY LAYER                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   FaxRepository                            │  │
│  │  • getFaxes()  • sendFax()  • downloadFax()  • sign()     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                       DATA SOURCES                               │
│  ┌───────────────────┐           ┌───────────────────┐         │
│  │  Remote (API)     │           │  Local (SQLite)   │         │
│  │  • Frappe REST    │           │  • Offline cache  │         │
│  │  • WebSocket      │           │  • Signatures     │         │
│  └───────────────────┘           └───────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9.2 Directory Structure (Flutter)

```
lib/
├── features/
│   └── fax/
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── fax_remote_datasource.dart
│       │   │   └── fax_local_datasource.dart
│       │   ├── models/
│       │   │   ├── fax_document_model.dart
│       │   │   ├── fax_number_model.dart
│       │   │   └── signature_model.dart
│       │   └── repositories/
│       │       └── fax_repository_impl.dart
│       │
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── fax_document.dart
│       │   │   └── signature.dart
│       │   ├── repositories/
│       │   │   └── fax_repository.dart
│       │   └── usecases/
│       │       ├── get_faxes.dart
│       │       ├── send_fax.dart
│       │       ├── sign_fax.dart
│       │       └── download_fax.dart
│       │
│       └── presentation/
│           ├── cubits/
│           │   ├── inbox_cubit.dart
│           │   ├── fax_viewer_cubit.dart
│           │   └── send_fax_cubit.dart
│           ├── screens/
│           │   ├── fax_inbox_screen.dart
│           │   ├── fax_viewer_screen.dart
│           │   ├── send_fax_screen.dart
│           │   └── signature_screen.dart
│           └── widgets/
│               ├── fax_list_tile.dart
│               ├── pdf_viewer.dart
│               ├── signature_pad.dart
│               └── annotation_toolbar.dart
```

---

## 9.3 API Client

```dart
// data/datasources/fax_remote_datasource.dart
class FaxRemoteDatasource {
  final DartwingApiClient _client;

  FaxRemoteDatasource(this._client);

  Future<List<FaxDocumentModel>> getFaxes({
    String? direction,
    String? status,
    int page = 1,
    int pageSize = 20,
  }) async {
    final response = await _client.call(
      'dartwing_fax.api.v1.fax.list',
      params: {
        'direction': direction,
        'status': status,
        'page': page,
        'page_size': pageSize,
      },
    );
    return (response['data'] as List)
        .map((e) => FaxDocumentModel.fromJson(e))
        .toList();
  }

  Future<FaxDocumentModel> getFax(String faxId) async {
    final response = await _client.getDoc('Fax Document', faxId);
    return FaxDocumentModel.fromJson(response);
  }

  Future<String> sendFax({
    required String recipient,
    required Uint8List file,
    required String senderNumber,
    String? subject,
    String? message,
  }) async {
    final response = await _client.call(
      'dartwing_fax.api.v1.fax.send',
      params: {
        'recipient': recipient,
        'file': base64Encode(file),
        'sender_number': senderNumber,
        'subject': subject,
        'message': message,
      },
    );
    return response['fax_id'];
  }

  Future<Uint8List> downloadFax(String faxId) async {
    final response = await _client.call(
      'dartwing_fax.api.v1.fax.download',
      params: {'fax_id': faxId},
    );
    return base64Decode(response['file']);
  }

  Future<void> annotateFax({
    required String faxId,
    required List<AnnotationModel> annotations,
  }) async {
    await _client.call(
      'dartwing_fax.api.v1.fax.annotate',
      params: {
        'fax_id': faxId,
        'annotations': annotations.map((a) => a.toJson()).toList(),
      },
    );
  }
}
```

---

## 9.4 State Management (Cubit)

```dart
// presentation/cubits/inbox_cubit.dart
class InboxCubit extends Cubit<InboxState> {
  final GetFaxes _getFaxes;

  InboxCubit(this._getFaxes) : super(InboxInitial());

  Future<void> loadInbox({String? filter}) async {
    emit(InboxLoading());

    final result = await _getFaxes(
      direction: 'Inbound',
      status: filter,
    );

    result.fold(
      (failure) => emit(InboxError(failure.message)),
      (faxes) => emit(InboxLoaded(faxes)),
    );
  }

  Future<void> refresh() async {
    final currentState = state;
    if (currentState is InboxLoaded) {
      final result = await _getFaxes(direction: 'Inbound');
      result.fold(
        (failure) => emit(InboxError(failure.message)),
        (faxes) => emit(InboxLoaded(faxes)),
      );
    }
  }
}

// presentation/cubits/fax_viewer_cubit.dart
class FaxViewerCubit extends Cubit<FaxViewerState> {
  final DownloadFax _downloadFax;
  final SignFax _signFax;

  FaxViewerCubit(this._downloadFax, this._signFax)
      : super(FaxViewerInitial());

  Future<void> loadFax(String faxId) async {
    emit(FaxViewerLoading());

    final result = await _downloadFax(faxId);

    result.fold(
      (failure) => emit(FaxViewerError(failure.message)),
      (pdfBytes) => emit(FaxViewerLoaded(pdfBytes, [])),
    );
  }

  void addAnnotation(Annotation annotation) {
    final currentState = state;
    if (currentState is FaxViewerLoaded) {
      final annotations = [...currentState.annotations, annotation];
      emit(currentState.copyWith(annotations: annotations));
    }
  }

  Future<void> saveAndReturn(String faxId) async {
    final currentState = state;
    if (currentState is FaxViewerLoaded) {
      emit(FaxViewerSaving());

      final result = await _signFax(
        faxId: faxId,
        annotations: currentState.annotations,
        returnToSender: true,
      );

      result.fold(
        (failure) => emit(FaxViewerError(failure.message)),
        (_) => emit(FaxViewerSaved()),
      );
    }
  }
}
```

---

## 9.5 PDF Viewer with Annotations

```dart
// presentation/widgets/pdf_viewer.dart
class AnnotatablePdfViewer extends StatefulWidget {
  final Uint8List pdfBytes;
  final List<Annotation> annotations;
  final Function(Annotation) onAnnotationAdded;

  @override
  _AnnotatablePdfViewerState createState() => _AnnotatablePdfViewerState();
}

class _AnnotatablePdfViewerState extends State<AnnotatablePdfViewer> {
  PdfController? _pdfController;
  int _currentPage = 1;
  AnnotationTool _currentTool = AnnotationTool.none;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // PDF Document
        PdfView(
          controller: _pdfController!,
          onPageChanged: (page) => setState(() => _currentPage = page),
        ),

        // Annotation overlay
        GestureDetector(
          onTapUp: _handleTap,
          onPanStart: _handlePanStart,
          onPanUpdate: _handlePanUpdate,
          onPanEnd: _handlePanEnd,
          child: CustomPaint(
            painter: AnnotationPainter(
              annotations: widget.annotations
                  .where((a) => a.pageNumber == _currentPage)
                  .toList(),
            ),
          ),
        ),

        // Toolbar
        Positioned(
          bottom: 16,
          left: 0,
          right: 0,
          child: AnnotationToolbar(
            currentTool: _currentTool,
            onToolSelected: (tool) => setState(() => _currentTool = tool),
          ),
        ),
      ],
    );
  }

  void _handleTap(TapUpDetails details) {
    if (_currentTool == AnnotationTool.signature) {
      _showSignaturePicker(details.localPosition);
    } else if (_currentTool == AnnotationTool.stamp) {
      _showStampPicker(details.localPosition);
    } else if (_currentTool == AnnotationTool.checkmark) {
      _addCheckmark(details.localPosition);
    }
  }
}
```

---

## 9.6 Signature Capture

```dart
// presentation/widgets/signature_pad.dart
class SignaturePad extends StatefulWidget {
  final Function(Uint8List) onSignatureComplete;

  @override
  _SignaturePadState createState() => _SignaturePadState();
}

class _SignaturePadState extends State<SignaturePad> {
  final _signatureController = SignatureController(
    penStrokeWidth: 3,
    penColor: Colors.black,
    exportBackgroundColor: Colors.transparent,
  );

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          height: 200,
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Signature(
            controller: _signatureController,
            backgroundColor: Colors.white,
          ),
        ),
        SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            TextButton(
              onPressed: () => _signatureController.clear(),
              child: Text('Clear'),
            ),
            ElevatedButton(
              onPressed: _saveSignature,
              child: Text('Use Signature'),
            ),
          ],
        ),
      ],
    );
  }

  Future<void> _saveSignature() async {
    if (_signatureController.isNotEmpty) {
      final signature = await _signatureController.toPngBytes();
      if (signature != null) {
        widget.onSignatureComplete(signature);
      }
    }
  }
}
```

---

## 9.7 Offline Support

```dart
// data/datasources/fax_local_datasource.dart
class FaxLocalDatasource {
  final Database _db;

  Future<void> cacheFaxes(List<FaxDocumentModel> faxes) async {
    final batch = _db.batch();
    for (final fax in faxes) {
      batch.insert(
        'faxes',
        fax.toJson(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit();
  }

  Future<List<FaxDocumentModel>> getCachedFaxes() async {
    final results = await _db.query('faxes', orderBy: 'received_at DESC');
    return results.map((e) => FaxDocumentModel.fromJson(e)).toList();
  }

  Future<void> queueOutboundFax(SendFaxRequest request) async {
    await _db.insert('outbound_queue', {
      'id': uuid.v4(),
      'recipient': request.recipient,
      'file': base64Encode(request.file),
      'sender_number': request.senderNumber,
      'created_at': DateTime.now().toIso8601String(),
      'status': 'pending',
    });
  }

  Future<List<SendFaxRequest>> getPendingOutbound() async {
    final results = await _db.query(
      'outbound_queue',
      where: 'status = ?',
      whereArgs: ['pending'],
    );
    return results.map((e) => SendFaxRequest.fromJson(e)).toList();
  }
}

// Sync manager
class FaxSyncManager {
  final FaxRemoteDatasource _remote;
  final FaxLocalDatasource _local;

  Future<void> syncPendingFaxes() async {
    final pending = await _local.getPendingOutbound();

    for (final request in pending) {
      try {
        await _remote.sendFax(
          recipient: request.recipient,
          file: request.file,
          senderNumber: request.senderNumber,
        );
        await _local.markAsSent(request.id);
      } catch (e) {
        // Will retry on next sync
        continue;
      }
    }
  }
}
```

---

## 9.8 Push Notifications

```dart
// services/fax_notification_service.dart
class FaxNotificationService {
  final FirebaseMessaging _fcm;

  Future<void> initialize() async {
    // Request permission
    await _fcm.requestPermission();

    // Get token and register with backend
    final token = await _fcm.getToken();
    await _registerToken(token);

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleMessage);

    // Handle background/terminated messages
    FirebaseMessaging.onBackgroundMessage(_handleBackgroundMessage);
  }

  void _handleMessage(RemoteMessage message) {
    if (message.data['type'] == 'fax_received') {
      // Show local notification
      _showNotification(
        title: 'New Fax Received',
        body: 'From: ${message.data['sender']}',
        payload: message.data['fax_id'],
      );
    }
  }
}
```

---

## 9.9 Camera Scan to Fax

```dart
// presentation/screens/scan_to_fax_screen.dart
class ScanToFaxScreen extends StatefulWidget {
  @override
  _ScanToFaxScreenState createState() => _ScanToFaxScreenState();
}

class _ScanToFaxScreenState extends State<ScanToFaxScreen> {
  List<Uint8List> _scannedPages = [];

  Future<void> _scanPage() async {
    final image = await ImagePicker().pickImage(source: ImageSource.camera);
    if (image != null) {
      // Process image
      final processed = await _processImage(File(image.path));
      setState(() => _scannedPages.add(processed));
    }
  }

  Future<Uint8List> _processImage(File image) async {
    // Load image
    final bytes = await image.readAsBytes();
    final decoded = img.decodeImage(bytes)!;

    // Auto-detect document edges
    final edges = await _detectEdges(decoded);

    // Perspective correction
    final corrected = _perspectiveCorrect(decoded, edges);

    // Convert to grayscale and enhance
    final enhanced = _enhance(corrected);

    return img.encodePng(enhanced);
  }

  Future<void> _sendAsFax() async {
    // Combine pages into PDF
    final pdf = await _createPdf(_scannedPages);

    // Navigate to send screen
    Navigator.push(context, MaterialPageRoute(
      builder: (_) => SendFaxScreen(file: pdf),
    ));
  }
}
```

---

**Next: Section 10 - API Architecture**

# Dartwing Fax Architecture - Section 10: API Architecture

---

## 10.1 API Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      API ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       PUBLIC APIs                                │
│  /api/method/dartwing_fax.api.v1.*                              │
│  ─────────────────────────────────────────────────────────────  │
│  • fax.list, fax.get, fax.send, fax.download                   │
│  • numbers.list, numbers.provision, numbers.release             │
│  • routing.rules, routing.test                                  │
│  • search.query                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     WEBHOOK ENDPOINTS                            │
│  /api/method/dartwing_fax.api.v1.webhooks.*                     │
│  ─────────────────────────────────────────────────────────────  │
│  • telnyx (carrier inbound)                                     │
│  • bandwidth (carrier inbound)                                  │
│  • signalwire (carrier inbound)                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FRAPPE REST API                               │
│  /api/resource/Fax Document                                     │
│  /api/resource/Routing Rule                                     │
│  /api/resource/Fax Settings                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10.2 API Endpoints

| Endpoint              | Method | Purpose                 | Auth           |
| --------------------- | ------ | ----------------------- | -------------- |
| **Fax Operations**    |        |                         |                |
| `fax.list`            | GET    | List faxes with filters | Bearer/API Key |
| `fax.get`             | GET    | Get single fax details  | Bearer/API Key |
| `fax.send`            | POST   | Send outbound fax       | Bearer/API Key |
| `fax.download`        | GET    | Download fax file       | Bearer/API Key |
| `fax.annotate`        | POST   | Apply annotations       | Bearer/API Key |
| `fax.return`          | POST   | Return fax to sender    | Bearer/API Key |
| `fax.forward`         | POST   | Forward fax             | Bearer/API Key |
| `fax.delete`          | DELETE | Delete fax              | Bearer/API Key |
| **Number Management** |        |                         |                |
| `numbers.list`        | GET    | List org's DIDs         | Bearer/API Key |
| `numbers.search`      | GET    | Search available DIDs   | Bearer/API Key |
| `numbers.provision`   | POST   | Provision new DID       | Bearer/API Key |
| `numbers.release`     | DELETE | Release DID             | Bearer/API Key |
| **Routing**           |        |                         |                |
| `routing.rules`       | GET    | List routing rules      | Bearer/API Key |
| `routing.test`        | POST   | Test routing logic      | Bearer/API Key |
| **Search**            |        |                         |                |
| `search.query`        | POST   | Full-text search        | Bearer/API Key |
| **Webhooks**          |        |                         |                |
| `webhooks.telnyx`     | POST   | Telnyx events           | Signature      |
| `webhooks.bandwidth`  | POST   | Bandwidth events        | Signature      |

---

## 10.3 Send Fax API

```python
# api/v1/fax.py
@frappe.whitelist()
def send(
    recipient: str,
    file: str = None,
    file_url: str = None,
    sender_number: str = None,
    subject: str = None,
    message: str = None,
    include_cover_page: bool = True,
    priority: str = "normal",
    scheduled_at: str = None,
    callback_url: str = None,
    metadata: dict = None
) -> dict:
    """
    Send an outbound fax.

    Args:
        recipient: Destination fax number (E.164 format)
        file: Base64-encoded PDF or TIFF
        file_url: URL to download file from
        sender_number: Caller ID (must be owned by org)
        subject: Cover page subject
        message: Cover page message
        include_cover_page: Whether to add cover page
        priority: low/normal/high/urgent
        scheduled_at: ISO datetime for scheduled send
        callback_url: Webhook for status updates
        metadata: Custom metadata dict

    Returns:
        {
            "success": true,
            "fax_id": "FAX-2025-00123",
            "status": "queued",
            "estimated_pages": 3,
            "estimated_delivery": "2025-11-28T15:30:00Z"
        }
    """
    # Authenticate
    org = authenticate_request()

    # Validate recipient
    recipient = validate_phone(recipient)

    # Get or validate sender number
    if not sender_number:
        sender_number = get_default_sender(org)
    else:
        validate_sender_ownership(org, sender_number)

    # Get file content
    if file:
        file_content = base64.b64decode(file)
    elif file_url:
        file_content = download_file(file_url)
    else:
        frappe.throw("Either file or file_url required")

    # Validate file
    file_type = detect_file_type(file_content)
    if file_type not in ["pdf", "tiff"]:
        frappe.throw("File must be PDF or TIFF")

    # Create fax document
    fax = frappe.get_doc({
        "doctype": "Fax Document",
        "organization": org,
        "direction": "Outbound",
        "status": "Draft",
        "sender_number": sender_number,
        "recipient_number": recipient,
        "priority": priority,
        "original_file": save_file(file_content),
        "include_cover_page": include_cover_page,
        "cover_subject": subject,
        "cover_message": message,
        "scheduled_at": scheduled_at,
        "callback_url": callback_url,
        "metadata": json.dumps(metadata) if metadata else None
    })
    fax.insert()

    # Queue for sending (or schedule)
    if scheduled_at:
        schedule_fax(fax.name, scheduled_at)
    else:
        queue_fax(fax.name, priority)

    # Update status
    fax.status = "Queued"
    fax.save()

    return {
        "success": True,
        "fax_id": fax.name,
        "status": "queued",
        "estimated_pages": count_pages(file_content),
        "estimated_delivery": estimate_delivery(priority)
    }
```

---

## 10.4 List Faxes API

```python
@frappe.whitelist()
def list(
    direction: str = None,
    status: str = None,
    category: str = None,
    date_from: str = None,
    date_to: str = None,
    assigned_to: str = None,
    shared_inbox: str = None,
    search: str = None,
    page: int = 1,
    page_size: int = 20,
    order_by: str = "received_at desc"
) -> dict:
    """
    List faxes with filters.

    Returns:
        {
            "data": [...],
            "total": 150,
            "page": 1,
            "page_size": 20,
            "pages": 8
        }
    """
    org = authenticate_request()

    filters = {"organization": org}

    if direction:
        filters["direction"] = direction
    if status:
        filters["status"] = status
    if category:
        filters["ai_category"] = category
    if assigned_to:
        filters["assigned_to"] = assigned_to
    if shared_inbox:
        filters["shared_inbox"] = shared_inbox
    if date_from:
        filters["received_at"] = [">=", date_from]
    if date_to:
        filters["received_at"] = ["<=", date_to]

    # Full-text search
    if search:
        fax_ids = search_faxes(org, search)
        filters["name"] = ["in", fax_ids]

    # Get total count
    total = frappe.db.count("Fax Document", filters)

    # Get page
    faxes = frappe.get_all(
        "Fax Document",
        filters=filters,
        fields=[
            "name", "direction", "status", "priority",
            "sender_number", "sender_name",
            "recipient_number", "recipient_name",
            "received_at", "sent_at", "pages",
            "ai_category", "ai_confidence",
            "assigned_to", "shared_inbox"
        ],
        order_by=order_by,
        start=(page - 1) * page_size,
        limit=page_size
    )

    return {
        "data": faxes,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": ceil(total / page_size)
    }
```

---

## 10.5 Search API

```python
@frappe.whitelist()
def query(
    q: str,
    filters: dict = None,
    page: int = 1,
    page_size: int = 20
) -> dict:
    """
    Full-text search across fax content.

    Args:
        q: Search query string
        filters: Additional filters (date_from, date_to, category, etc.)
        page: Page number
        page_size: Results per page

    Returns:
        {
            "data": [
                {
                    "fax_id": "FAX-2025-00123",
                    "snippet": "...matching text...",
                    "score": 0.95,
                    ...
                }
            ],
            "total": 50
        }
    """
    org = authenticate_request()

    # Build OpenSearch query
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"ocr_text": q}},
                    {"term": {"organization": org}}
                ],
                "filter": []
            }
        },
        "highlight": {
            "fields": {"ocr_text": {}},
            "pre_tags": ["<mark>"],
            "post_tags": ["</mark>"]
        },
        "from": (page - 1) * page_size,
        "size": page_size
    }

    # Add filters
    if filters:
        if filters.get("date_from"):
            search_body["query"]["bool"]["filter"].append(
                {"range": {"received_at": {"gte": filters["date_from"]}}}
            )
        if filters.get("category"):
            search_body["query"]["bool"]["filter"].append(
                {"term": {"ai_category": filters["category"]}}
            )

    # Execute search
    results = opensearch.search(index="faxes", body=search_body)

    # Format response
    data = []
    for hit in results["hits"]["hits"]:
        data.append({
            "fax_id": hit["_source"]["name"],
            "snippet": hit.get("highlight", {}).get("ocr_text", [""])[0],
            "score": hit["_score"],
            "direction": hit["_source"]["direction"],
            "sender_number": hit["_source"]["sender_number"],
            "received_at": hit["_source"]["received_at"],
            "ai_category": hit["_source"]["ai_category"]
        })

    return {
        "data": data,
        "total": results["hits"]["total"]["value"]
    }
```

---

## 10.6 Webhook Handler

```python
# api/v1/webhooks.py
@frappe.whitelist(allow_guest=True)
def telnyx():
    """Handle Telnyx webhook events"""
    # Get raw request
    payload = frappe.request.get_json()
    signature = frappe.request.headers.get("Telnyx-Signature-Ed25519")
    timestamp = frappe.request.headers.get("Telnyx-Timestamp")

    # Validate signature
    if not validate_telnyx_signature(payload, signature, timestamp):
        frappe.throw("Invalid webhook signature", frappe.AuthenticationError)

    # Route by event type
    event_type = payload.get("data", {}).get("event_type")

    if event_type == "fax.received":
        handle_fax_received(payload)
    elif event_type == "fax.sent":
        handle_fax_sent(payload)
    elif event_type == "fax.failed":
        handle_fax_failed(payload)
    elif event_type == "fax.queued":
        handle_fax_queued(payload)

    return {"status": "ok"}

def handle_fax_received(payload: dict):
    """Process inbound fax webhook"""
    data = payload["data"]["payload"]

    # Find organization by recipient DID
    fax_number = frappe.get_doc("Fax Number", {
        "phone_number": data["to"]
    })

    if not fax_number:
        frappe.log_error(f"Unknown DID: {data['to']}")
        return

    # Download fax file
    file_content = download_from_carrier(data["media_url"])

    # Create fax document
    fax = frappe.get_doc({
        "doctype": "Fax Document",
        "organization": fax_number.organization,
        "direction": "Inbound",
        "status": "Received",
        "sender_number": data["from"],
        "recipient_number": data["to"],
        "received_at": data["received_at"],
        "pages": data["page_count"],
        "fax_provider": "Telnyx",
        "provider_fax_id": data["fax_id"],
        "original_file": save_file(file_content)
    })
    fax.insert()

    # Queue for processing
    frappe.enqueue(
        "dartwing_fax.tasks.process_inbound.process",
        fax_id=fax.name,
        queue="default"
    )
```

---

## 10.7 Response Formats

**Success Response:**

```json
{
    "success": true,
    "data": {...},
    "message": "Operation completed"
}
```

**Error Response:**

```json
{
  "success": false,
  "error": {
    "code": "FAX-001",
    "message": "Invalid recipient number",
    "details": "Phone number must be in E.164 format"
  }
}
```

**Error Codes:**
| Code | Message |
|------|---------|
| FAX-001 | Invalid recipient number |
| FAX-002 | File too large |
| FAX-003 | Invalid file type |
| FAX-004 | Rate limit exceeded |
| FAX-005 | Unauthorized |
| FAX-006 | Fax not found |
| FAX-007 | Carrier error |
| FAX-008 | Sender blocked |
| FAX-009 | Number not owned |

---

## 10.8 Rate Limiting

```python
# api/rate_limit.py
class RateLimiter:
    """API rate limiting via Redis"""

    def check(self, key: str, limit: int, window: int = 3600) -> bool:
        """
        Check if request is within rate limit.

        Args:
            key: Rate limit key (api_key or user)
            limit: Max requests per window
            window: Window in seconds (default 1 hour)

        Returns:
            True if allowed, False if exceeded
        """
        redis = frappe.cache()
        count_key = f"rate_limit:{key}"

        current = redis.get(count_key) or 0

        if int(current) >= limit:
            return False

        pipe = redis.pipeline()
        pipe.incr(count_key)
        pipe.expire(count_key, window)
        pipe.execute()

        return True

    def get_remaining(self, key: str, limit: int) -> int:
        """Get remaining requests in current window"""
        current = frappe.cache().get(f"rate_limit:{key}") or 0
        return max(0, limit - int(current))
```

---

**Next: Section 11 - Background Jobs**

# Dartwing Fax Architecture - Section 11: Background Jobs

---

## 11.1 Job Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BACKGROUND JOB ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         QUEUES                                   │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │  default  │ │   long    │ │   short   │ │    ai     │       │
│  │ (general) │ │(AI/OCR)   │ │(webhooks) │ │(ML jobs)  │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        WORKERS                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Worker Pool (configurable)                                 │  │
│  │  • default: 4 workers                                     │  │
│  │  • long: 2 workers (high memory for AI)                   │  │
│  │  • short: 2 workers (fast response)                       │  │
│  │  • ai: 2 workers (GPU if available)                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SCHEDULED JOBS                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Every minute:                                              │  │
│  │   • process_outbound_queue                                │  │
│  │   • carrier_health_check                                  │  │
│  │ Every 5 minutes:                                          │  │
│  │   • retry_failed_faxes                                    │  │
│  │ Every hour:                                               │  │
│  │   • expire_challenges                                     │  │
│  │ Every 6 hours:                                            │  │
│  │   • sync_spam_database                                    │  │
│  │ Daily at 2 AM:                                            │  │
│  │   • apply_retention_policies                              │  │
│  │   • reindex_search                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11.2 Inbound Processing Job

```python
# tasks/process_inbound.py
import frappe
from dartwing_fax.core.security_engine import SecurityEngine
from dartwing_fax.core.routing_engine import RoutingEngine
from dartwing_fax.ai.pipeline import AIPipeline

def process(fax_id: str):
    """
    Process inbound fax through full pipeline.

    Pipeline:
    1. Tier 1 validation (whitelist/blacklist)
    2. AI/OCR processing
    3. Tier 2 validation (spam scoring)
    4. Routing
    5. Notifications
    """
    fax = frappe.get_doc("Fax Document", fax_id)
    fax.status = "Processing"
    fax.save()

    try:
        org = fax.organization
        settings = get_fax_settings(org)

        # Initialize engines
        security = SecurityEngine(org)
        routing = RoutingEngine(org)
        ai = AIPipeline(settings)

        # Step 1: Tier 1 validation
        tier1_result = security.check_tier1(fax.sender_number)

        if tier1_result.decision == "reject":
            _reject_fax(fax, tier1_result.reason)
            return

        if tier1_result.decision == "deliver" and tier1_result.bypass_ai:
            # Whitelisted - skip AI, route directly
            fax.validation_status = "Whitelisted"
            fax.validation_tier = 1
        else:
            # Step 2: AI/OCR processing
            ai_result = ai.process(fax)

            # Update fax with AI results
            fax.ocr_text = ai_result["ocr_text"]
            fax.ocr_confidence = ai_result["ocr_confidence"]
            fax.ai_category = ai_result["ai_category"]
            fax.ai_confidence = ai_result["ai_confidence"]
            fax.entities_json = json.dumps(ai_result["entities"])
            fax.spam_score = ai_result["spam_score"]

            # PHI detection (MedxFax)
            if ai_result["phi"]["contains_phi"]:
                fax.contains_phi = True
                fax.phi_elements = json.dumps(ai_result["phi"]["elements"])

            # Index for search
            index_fax(fax)

            # Step 3: Tier 2 validation
            tier2_result = security.check_tier2(fax)

            if tier2_result.decision == "reject":
                _reject_fax(fax, tier2_result.reason)
                return

            if tier2_result.decision == "challenge":
                _challenge_fax(fax)
                return

            if tier2_result.decision == "hold":
                _hold_fax(fax, tier2_result.reason)
                return

            fax.validation_status = "Passed"
            fax.validation_tier = 2

        # Step 4: Routing
        route_result = routing.route(fax)

        fax.assigned_to = route_result.assigned_user
        fax.assigned_group = route_result.assigned_group
        fax.shared_inbox = route_result.shared_inbox
        fax.routed_by_rule = route_result.rule_name
        fax.routed_at = now()

        # Execute routing actions
        for action in route_result.actions:
            execute_action(action, fax)

        # Step 5: Update status
        fax.status = "Delivered"
        fax.save()

        # Step 6: Notifications
        send_notifications(fax, route_result)

        # Audit log
        audit_log("fax.received", fax.name, {
            "category": fax.ai_category,
            "routed_to": fax.assigned_to or fax.shared_inbox
        })

    except Exception as e:
        fax.status = "Failed"
        fax.error_message = str(e)
        fax.save()
        frappe.log_error(f"Fax processing failed: {fax_id}")
        raise

def _reject_fax(fax, reason: str):
    """Mark fax as rejected"""
    fax.status = "Rejected"
    fax.validation_status = "Rejected"
    fax.hold_reason = reason
    fax.save()
    audit_log("fax.rejected", fax.name, {"reason": reason})

def _hold_fax(fax, reason: str):
    """Hold fax for manual review"""
    fax.status = "Held"
    fax.validation_status = "Held"
    fax.hold_reason = reason
    fax.save()
    audit_log("fax.held", fax.name, {"reason": reason})
    notify_held_fax(fax)

def _challenge_fax(fax):
    """Initiate Tier 3 challenge"""
    from dartwing_fax.core.challenge import ChallengeManager
    ChallengeManager().create_challenge(fax)
```

---

## 11.3 Outbound Processing Job

```python
# tasks/send_outbound.py
import frappe
from dartwing_fax.carriers.manager import CarrierManager

def process_queue():
    """Process outbound fax queue"""
    # Get pending faxes ordered by priority
    pending = frappe.get_all(
        "Fax Document",
        filters={
            "direction": "Outbound",
            "status": "Queued"
        },
        fields=["name", "priority", "organization"],
        order_by="FIELD(priority, 'Urgent', 'High', 'Normal', 'Low'), creation"
    )

    for fax_data in pending:
        # Check if scheduled
        fax = frappe.get_doc("Fax Document", fax_data.name)

        if fax.scheduled_at and fax.scheduled_at > now():
            continue  # Not time yet

        # Process
        frappe.enqueue(
            "dartwing_fax.tasks.send_outbound.send_fax",
            fax_id=fax.name,
            queue="default"
        )

def send_fax(fax_id: str):
    """Send a single fax"""
    fax = frappe.get_doc("Fax Document", fax_id)
    fax.status = "Sending"
    fax.save()

    try:
        # Get carrier manager
        carrier_mgr = CarrierManager(fax.organization)

        # Build request
        file_content = get_file_content(fax.original_file)

        # Add cover page if configured
        if fax.include_cover_page:
            file_content = prepend_cover_page(fax, file_content)

        request = SendFaxRequest(
            recipient_number=fax.recipient_number,
            file_content=file_content,
            file_type="pdf",
            sender_number=fax.sender_number,
            sender_name=get_org_name(fax.organization),
            callback_url=get_callback_url(fax.name)
        )

        # Send with failover
        response = carrier_mgr.send_with_failover(request)

        if response.success:
            fax.status = "Sent"
            fax.fax_provider = response.carrier_name
            fax.provider_fax_id = response.provider_fax_id
            fax.sent_at = now()
            fax.save()

            audit_log("fax.sent", fax.name, {
                "carrier": response.carrier_name,
                "provider_id": response.provider_fax_id
            })

            # Notify success
            if fax.callback_url:
                send_callback(fax.callback_url, fax, "sent")
        else:
            _handle_send_failure(fax, response.message)

    except Exception as e:
        _handle_send_failure(fax, str(e))

def _handle_send_failure(fax, error: str):
    """Handle send failure with retry logic"""
    fax.retry_count += 1
    fax.error_message = error

    settings = get_fax_settings(fax.organization)
    max_retries = settings.get("max_retries", 3)

    if fax.retry_count >= max_retries:
        fax.status = "Failed"
        audit_log("fax.failed", fax.name, {"error": error})
        notify_send_failure(fax)
    else:
        # Requeue for retry
        fax.status = "Queued"
        delay = calculate_retry_delay(fax.retry_count)
        frappe.enqueue(
            "dartwing_fax.tasks.send_outbound.send_fax",
            fax_id=fax.name,
            queue="default",
            enqueue_after_commit=True,
            at_front=False,
            job_name=f"retry-{fax.name}",
            now=False,
            scheduled_time=now() + timedelta(seconds=delay)
        )

    fax.save()

def retry_failed():
    """Retry failed faxes that haven't exceeded max retries"""
    failed = frappe.get_all(
        "Fax Document",
        filters={
            "direction": "Outbound",
            "status": "Failed",
            "retry_count": ["<", 3]
        },
        fields=["name"]
    )

    for fax_data in failed:
        frappe.enqueue(
            "dartwing_fax.tasks.send_outbound.send_fax",
            fax_id=fax_data.name,
            queue="default"
        )
```

---

## 11.4 OCR Processing Job

```python
# tasks/ocr_processing.py
def process_ocr(fax_id: str):
    """
    Run OCR on fax document.
    Separated for scaling OCR workers independently.
    """
    fax = frappe.get_doc("Fax Document", fax_id)
    settings = get_fax_settings(fax.organization)

    fax.ocr_status = "Processing"
    fax.save()

    try:
        ocr_engine = OCREngine(settings)
        result = ocr_engine.process(fax.original_file)

        fax.ocr_text = result.full_text
        fax.ocr_confidence = result.confidence
        fax.ocr_hocr = result.hocr
        fax.ocr_status = "Completed"
        fax.save()

        # Trigger AI processing
        frappe.enqueue(
            "dartwing_fax.tasks.ai_processing.classify",
            fax_id=fax.name,
            queue="ai"
        )

    except Exception as e:
        fax.ocr_status = "Failed"
        fax.error_message = str(e)
        fax.save()
        frappe.log_error(f"OCR failed: {fax_id}")
```

---

## 11.5 Cleanup Jobs

```python
# tasks/cleanup.py
def expire_challenges():
    """Delete expired challenge records and held faxes"""
    expired = frappe.get_all(
        "Fax Challenge",
        filters={
            "status": "pending",
            "expires_at": ["<", now()]
        }
    )

    for challenge in expired:
        challenge_doc = frappe.get_doc("Fax Challenge", challenge.name)

        # Delete the held fax
        if challenge_doc.fax_document:
            fax = frappe.get_doc("Fax Document", challenge_doc.fax_document)
            fax.status = "Rejected"
            fax.hold_reason = "Challenge expired"
            fax.save()

            # Optionally auto-blacklist
            settings = get_fax_settings(fax.organization)
            if settings.auto_blacklist_on_challenge_fail:
                add_to_blacklist(fax.sender_number, fax.organization)

        challenge_doc.status = "expired"
        challenge_doc.save()

def apply_retention():
    """Apply retention policies and archive/delete old faxes"""
    # Get all organizations with retention policies
    policies = frappe.get_all(
        "Retention Policy",
        filters={"enabled": 1},
        fields=["name", "organization", "retention_days", "action"]
    )

    for policy in policies:
        cutoff = now() - timedelta(days=policy.retention_days)

        faxes = frappe.get_all(
            "Fax Document",
            filters={
                "organization": policy.organization,
                "received_at": ["<", cutoff],
                "legal_hold": 0,
                "archived": 0
            }
        )

        for fax_data in faxes:
            fax = frappe.get_doc("Fax Document", fax_data.name)

            if policy.action == "archive":
                fax.archived = True
                fax.archived_at = now()
                move_to_archive_storage(fax)
                fax.save()
            elif policy.action == "delete":
                audit_log("fax.deleted", fax.name, {"reason": "retention"})
                fax.delete()
```

---

## 11.6 Health Check Job

```python
# tasks/health_check.py
def check_carriers():
    """Check health of all enabled carriers"""
    carriers = frappe.get_all(
        "Fax Provider",
        filters={"enabled": 1},
        fields=["name", "provider_type"]
    )

    for carrier_data in carriers:
        carrier = frappe.get_doc("Fax Provider", carrier_data.name)

        try:
            # Get connector
            connector = get_connector(carrier)

            # Check health
            is_healthy = connector.health_check()

            if is_healthy:
                carrier.health_status = "Healthy"
                carrier.consecutive_failures = 0
            else:
                carrier.health_status = "Degraded"
                carrier.consecutive_failures += 1

        except Exception as e:
            carrier.health_status = "Down"
            carrier.consecutive_failures += 1
            carrier.last_failure_reason = str(e)

            # Alert if carrier down
            if carrier.consecutive_failures >= 3:
                alert_carrier_down(carrier)

        carrier.last_health_check = now()
        carrier.save()
```

---

## 11.7 Worker Configuration

```python
# In site_config.json
{
    "workers": {
        "default": 4,
        "long": 2,
        "short": 2
    },
    "redis_queue": "redis://localhost:6379/1",
    "scheduler_tick_interval": 60
}
```

```bash
# Start workers
bench worker --queue default &
bench worker --queue long &
bench worker --queue short &
bench schedule
```

---

**Next: Section 12 - Deployment Architecture**

# Dartwing Fax Architecture - Section 12: Deployment & Phases

---

## 12.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION DEPLOYMENT                                │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────┐
                    │     Load Balancer       │
                    │    (AWS ALB / nginx)    │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
      ┌───────▼───────┐ ┌──────▼──────┐ ┌───────▼───────┐
      │   Web Server  │ │  Web Server │ │   Web Server  │
      │   (Gunicorn)  │ │  (Gunicorn) │ │   (Gunicorn)  │
      │   + Frappe    │ │  + Frappe   │ │   + Frappe    │
      └───────┬───────┘ └──────┬──────┘ └───────┬───────┘
              │                │                 │
              └────────────────┼─────────────────┘
                               │
      ┌────────────────────────┼────────────────────────┐
      │                        │                        │
┌─────▼─────┐          ┌──────▼──────┐          ┌──────▼──────┐
│  MariaDB  │          │    Redis    │          │  OpenSearch │
│  Primary  │          │   Cluster   │          │   Cluster   │
│    +      │          │  (3 nodes)  │          │  (3 nodes)  │
│  Replica  │          └─────────────┘          └─────────────┘
└───────────┘
      │
      │                 ┌─────────────────────────────────────┐
      │                 │           WORKER NODES              │
      │                 │  ┌─────────┐ ┌─────────┐           │
      │                 │  │ Default │ │   Long  │           │
      │                 │  │ Workers │ │ Workers │           │
      │                 │  │  (x4)   │ │  (x2)   │           │
      │                 │  └─────────┘ └─────────┘           │
      │                 │  ┌─────────┐ ┌─────────┐           │
      │                 │  │  Short  │ │   AI    │           │
      │                 │  │ Workers │ │ Workers │           │
      │                 │  │  (x2)   │ │  (x2)   │           │
      │                 │  └─────────┘ └─────────┘           │
      │                 └─────────────────────────────────────┘
      │
      │                 ┌─────────────────────────────────────┐
      │                 │          STORAGE                    │
      └─────────────────│  ┌───────────────────────────────┐ │
                        │  │    S3 / MinIO                  │ │
                        │  │    - Fax documents             │ │
                        │  │    - Annotations               │ │
                        │  │    - Thumbnails                │ │
                        │  └───────────────────────────────┘ │
                        └─────────────────────────────────────┘
```

---

## 12.2 Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dartwing-web
  template:
    metadata:
      labels:
        app: dartwing-web
    spec:
      containers:
        - name: frappe
          image: dartwing/frappe:latest
          ports:
            - containerPort: 8000
          env:
            - name: REDIS_CACHE
              value: "redis://redis-cache:6379"
            - name: REDIS_QUEUE
              value: "redis://redis-queue:6379"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: host
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-worker-default
spec:
  replicas: 4
  template:
    spec:
      containers:
        - name: worker
          image: dartwing/frappe:latest
          command: ["bench", "worker", "--queue", "default"]
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-worker-ai
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: worker
          image: dartwing/frappe:latest
          command: ["bench", "worker", "--queue", "ai"]
          resources:
            requests:
              memory: "4Gi"
              cpu: "2000m"
            limits:
              memory: "8Gi"
              cpu: "4000m"
```

---

## 12.3 Environment Configuration

```python
# site_config.json (production)
{
    "db_host": "mariadb.cluster.local",
    "db_port": 3306,
    "db_name": "dartwing",

    "redis_cache": "redis://redis-cache:6379",
    "redis_queue": "redis://redis-queue:6379",
    "redis_socketio": "redis://redis-socketio:6379",

    "encryption_key": "${ENCRYPTION_KEY}",
    "jwt_secret": "${JWT_SECRET}",

    "s3_bucket": "dartwing-fax-documents",
    "s3_region": "us-east-1",
    "s3_access_key": "${S3_ACCESS_KEY}",
    "s3_secret_key": "${S3_SECRET_KEY}",

    "opensearch_host": "opensearch.cluster.local",
    "opensearch_index": "faxes",

    "sentry_dsn": "${SENTRY_DSN}",

    "fax_settings": {
        "ocr_engine": "tesseract",
        "ocr_language": "eng",
        "ai_model_path": "/models/fax-classifier",
        "spam_model_path": "/models/spam-detector",
        "max_retries": 3,
        "retry_delay_base": 60
    }
}
```

---

## 12.4 High Availability

| Component        | HA Strategy                       |
| ---------------- | --------------------------------- |
| **Web Servers**  | 3+ replicas behind load balancer  |
| **MariaDB**      | Primary + replica, auto-failover  |
| **Redis**        | 3-node cluster with sentinel      |
| **OpenSearch**   | 3-node cluster                    |
| **S3**           | Multi-AZ storage                  |
| **Workers**      | Auto-scaling based on queue depth |
| **Fax Carriers** | Multi-carrier with failover       |

---

## 12.5 Monitoring & Observability

```yaml
# Prometheus metrics
- dartwing_fax_received_total
- dartwing_fax_sent_total
- dartwing_fax_failed_total
- dartwing_fax_processing_duration_seconds
- dartwing_ocr_duration_seconds
- dartwing_ai_classification_duration_seconds
- dartwing_carrier_health_status
- dartwing_queue_depth
```

**Alerting Rules:**

```yaml
- alert: FaxCarrierDown
  expr: dartwing_carrier_health_status == 0
  for: 5m
  labels:
    severity: critical

- alert: HighQueueDepth
  expr: dartwing_queue_depth > 100
  for: 10m
  labels:
    severity: warning

- alert: FaxFailureRate
  expr: rate(dartwing_fax_failed_total[5m]) > 0.1
  for: 5m
  labels:
    severity: warning
```

---

## 12.6 Development Phases

### Phase 1: Foundation (Months 1-3)

**Goal:** Basic send/receive with manual routing

**Deliverables:**

- Fax Document DocType
- Multi-carrier abstraction (Telnyx, Bandwidth)
- Inbound webhook processing
- Outbound queue with retry
- Tier 1 validation (whitelist/blacklist)
- Basic inbox UI (Frappe Desk)
- Send fax form
- DID provisioning
- API authentication
- Audit logging

**Success Criteria:**

- Send and receive faxes
- 99% delivery success
- <30 second inbound processing

---

### Phase 2: AI & Automation (Months 4-6)

**Goal:** Automated classification and routing

**Deliverables:**

- OCR engine (Tesseract)
- NLP classification
- Entity extraction
- Spam detection (Tier 2)
- Rule-based routing engine
- Workload balancing
- Full-text search (OpenSearch)
- Webhook system
- Notifications (email, SMS)
- Shared inboxes
- Cover page designer

**Success Criteria:**

- 90% classification accuracy
- <15 second full pipeline
- Search <1 second

---

### Phase 3: Security & Compliance (Months 7-9)

**Goal:** Enterprise security and HIPAA compliance

**Deliverables:**

- Tier 3 challenge verification
- Email-to-fax security
- PHI detection (MedxFax)
- Retention policies
- Legal hold
- Redaction tools
- Certified delivery receipts
- Compliance reports
- HIPAA controls
- HIS/Pharmacy connectors (basic)

**Success Criteria:**

- HIPAA ready
- SOC 2 audit prep
- <1% spam false positive

---

### Phase 4: Annotation & Mobile (Months 10-12)

**Goal:** Complete annotation and mobile experience

**Deliverables:**

- Signature management
- Stamp designer
- PDF annotation editor
- Return actions (fax, email)
- Flutter mobile app
- Offline capability
- Push notifications
- Pre-built integrations (Salesforce, DocuSign)
- Form parsing
- Analytics dashboard

**Success Criteria:**

- <30 second sign and return
- 4.8+ app store rating
- 50+ form templates

---

## 12.7 Resource Estimates

| Environment | Web   | Workers | DB    | Redis   | Search | Storage |
| ----------- | ----- | ------- | ----- | ------- | ------ | ------- |
| **Dev**     | 1x1GB | 2x1GB   | 1x2GB | 1x512MB | 1x2GB  | 50GB    |
| **Staging** | 2x2GB | 4x2GB   | 1x4GB | 3x1GB   | 3x4GB  | 200GB   |
| **Prod**    | 3x4GB | 10x4GB  | 2x8GB | 3x2GB   | 3x8GB  | 2TB     |

---

## 12.8 Document Summary

| Section | File                                | Description                       |
| ------- | ----------------------------------- | --------------------------------- |
| 1       | `arch-01-executive-summary.md`      | Overview, principles, stack       |
| 2       | `arch-02-system-overview.md`        | Architecture diagrams, flows      |
| 3       | `arch-03-module-structure.md`       | Directory structure, hooks        |
| 4       | `arch-04-doctype-architecture.md`   | DocType definitions               |
| 5       | `arch-05-carrier-layer.md`          | Carrier abstraction               |
| 6       | `arch-06-healthcare-integration.md` | HIS/Pharmacy connectors           |
| 7       | `arch-07-ai-pipeline.md`            | OCR, classification, extraction   |
| 8       | `arch-08-security.md`               | Three-tier validation, encryption |
| 9       | `arch-09-flutter-mobile.md`         | Mobile architecture               |
| 10      | `arch-10-api.md`                    | API endpoints, webhooks           |
| 11      | `arch-11-background-jobs.md`        | Workers, scheduled tasks          |
| 12      | `arch-12-deployment.md`             | Deployment, phases                |

---

**End of Architecture Document**
