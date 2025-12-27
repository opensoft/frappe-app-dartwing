# Dartwing Fax Module - Product Requirements Document

**Version 2.0 | November 2025**

**Product Owner:** Brett  
**Target Release:** Q1 2026 (Phase 1)  
**Status:** Ready for Implementation

---

## Table of Contents

1. Executive Summary
2. Vision & Strategic Goals
3. Target Markets & Use Cases
4. User Personas
5. System Architecture Overview
6. Module Structure
7. Feature Specifications
   - Module A: Fax Core Infrastructure
   - Module B: AI-Powered Document Processing
   - Module C: Intelligent Routing Engine
   - Module D: Three-Tier Inbound Security
   - Module E: Outbound Security & Anti-Spoofing
   - Module F: Document Annotation & Signature
   - Module G: Compliance & Audit Framework
   - Module H: Number Management & Provisioning
   - Module I: Search & Knowledge Layer
   - Module J: Notifications & Alerting
   - Module K: Team Collaboration
   - Module L: Integrations & Storage
   - Module M: Analytics & Reporting
   - Module N: Mobile Experience
   - Module O: Multi-Channel Communications
   - Module P: Form Recognition & Parsing
   - Module Q: Branding & Templates
   - Module R: HIPAA Compliance Framework
8. DocType Specifications
9. API Specifications
10. User Interface Specifications
11. Non-Functional Requirements
12. Security Requirements
13. Compliance Requirements
14. Integration Requirements
15. Implementation Roadmap
16. Success Metrics
17. Risks & Mitigations
18. Appendices

---

## 1. Executive Summary

### 1.1 Product Overview

**Dartwing Fax** (`dartwing_fax`) is an enterprise-grade, AI-powered digital fax platform built on the Frappe Framework. It transforms legacy fax infrastructure into a secure, intelligent document workflow system that automates routing, prevents fraud, ensures compliance, and integrates seamlessly with modern business systems.

### 1.2 Key Differentiators

| Capability                   | Description                                               |
| ---------------------------- | --------------------------------------------------------- |
| **AI-First Processing**      | OCR + NLP classification + entity extraction on every fax |
| **Three-Tier Security**      | Whitelist → AI Spam Detection → Challenge Verification    |
| **Zero-Friction Annotation** | Sign, stamp, and return faxes in under 30 seconds         |
| **Compliance-Ready**         | HIPAA, SOC 2, GDPR, FINRA, UETA/ESIGN built-in            |
| **Healthcare-Optimized**     | Foundation for MedxFax (clinical, lab, pharmacy fax)      |
| **Multi-Carrier Resilience** | 99.99% uptime with automatic failover                     |

### 1.3 Product Variants

| Product          | Target Market                          | Built On                       |
| ---------------- | -------------------------------------- | ------------------------------ |
| **Dartwing Fax** | General enterprise, legal, real estate | dartwing_fax module            |
| **MedxFax**      | Healthcare, clinical, lab, pharmacy    | dartwing_fax + HIPAA hardening |

### 1.4 Success Criteria

- ≥90% automated routing accuracy
- <30 second receive-to-return workflow
- ≥99.9% fax delivery success rate
- 99.99% platform uptime
- Zero PHI breaches (MedxFax)

---

## 2. Vision & Strategic Goals

### 2.1 Product Vision

Transform fax from a compliance burden into a competitive advantage by making every faxed document searchable, routable, and actionable within seconds of receipt.

### 2.2 Strategic Goals

| Goal                | Metric                  | Target | Timeframe |
| ------------------- | ----------------------- | ------ | --------- |
| Market Entry        | Paying customers        | 100    | Q2 2026   |
| Healthcare Vertical | MedxFax deployments     | 25     | Q3 2026   |
| Volume Scale        | Faxes processed/month   | 1M     | Q4 2026   |
| AI Accuracy         | Classification accuracy | 95%    | Q4 2026   |
| Revenue             | ARR                     | $500K  | Q4 2026   |

### 2.3 Design Principles

| Principle             | Implementation                                      |
| --------------------- | --------------------------------------------------- |
| **Security First**    | End-to-end encryption, audit everything, zero trust |
| **AI Augmented**      | Automate 90%+, humans handle exceptions             |
| **Compliance Native** | HIPAA/SOC 2 not bolted on, built in                 |
| **API First**         | Every feature accessible via REST API               |
| **Offline Capable**   | Mobile apps work without connectivity               |
| **Provider Agnostic** | Abstract fax carriers, avoid lock-in                |

---

## 3. Target Markets & Use Cases

### 3.1 Primary Markets

| Market                 | Pain Points                                           | Key Features                                           |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| **Healthcare**         | HIPAA compliance, high volume, manual sorting         | PHI detection, auto-routing to providers, audit trails |
| **Legal**              | Document authenticity, signature workflows, retention | E-signatures, legal hold, certified delivery           |
| **Financial Services** | Fraud prevention, FINRA compliance, audit             | Anti-spoofing, immutable logs, redaction               |
| **Real Estate**        | Contract turnaround, mobile signing                   | Quick annotation, mobile app, DocuSign integration     |
| **Government**         | Records retention, accessibility, security            | WORM storage, 508 compliance, FedRAMP path             |

### 3.2 Healthcare Sub-Verticals (MedxFax)

| Sub-Vertical          | Specific Needs                                            |
| --------------------- | --------------------------------------------------------- |
| **Clinical/Hospital** | Orders routing, lab results, referrals, consults          |
| **Pharmacy**          | Prescription verification, prior auth, refill requests    |
| **Laboratory**        | Result delivery, specimen tracking, critical value alerts |
| **Insurance/Payers**  | Claims processing, prior authorization, EOBs              |
| **Home Health**       | Care plans, orders, certifications                        |

### 3.3 Use Case Examples

**UC-001: Pharmacy Prescription Intake**

```
Prescriber faxes Rx → OCR extracts drug/patient/prescriber →
AI routes to pharmacist queue → Pharmacist reviews/signs →
Auto-files to patient record → Confirmation faxed back
```

**UC-002: Law Firm Contract Signing**

```
Client receives contract via fax → Opens on mobile →
Signs with finger → Stamps with date →
Returns via fax → Original + signed archived with audit trail
```

**UC-003: Hospital Lab Results**

```
Lab faxes critical result → AI detects STAT flag →
Routes to ordering physician + nurse station →
Push notification with 5-min escalation →
Acknowledgment logged for compliance
```

---

## 4. User Personas

### 4.1 Primary Persona: Healthcare Office Manager

**Name:** Maria Santos  
**Role:** Office Manager, Multi-Physician Practice  
**Daily Fax Volume:** 150-200 inbound, 50 outbound

**Pain Points:**

- Staff spends 3+ hours daily sorting/routing faxes
- Prescription faxes mixed with junk faxes
- No audit trail for HIPAA compliance
- Can't find faxes when patients call
- After-hours faxes pile up

**Goals:**

- Automated routing to correct provider
- Instant search across all faxes
- Mobile access for providers on call
- Compliance reports for auditors

**Quote:** _"I need faxes to go to the right person without me touching them, and I need proof they got there."_

---

### 4.2 Secondary Persona: Clinical Pharmacist

**Name:** Dr. James Chen, PharmD  
**Role:** Clinical Pharmacist, Retail Chain  
**Daily Fax Volume:** 100+ prescriptions

**Pain Points:**

- Handwritten Rx hard to read
- Can't verify prescriber DEA/NPI quickly
- Fax spam wastes time
- Signing and returning takes too long
- No mobile access when away from station

**Goals:**

- OCR that handles handwriting
- Auto-verify prescriber credentials
- Block junk faxes automatically
- One-tap sign and return
- Review urgent Rx on phone

**Quote:** _"Every minute I spend on fax admin is a minute I'm not counseling patients."_

---

### 4.3 Tertiary Persona: Compliance Officer

**Name:** Patricia Williams  
**Role:** HIPAA Privacy Officer, Hospital System  
**Responsibility:** 500-bed hospital + 20 clinics

**Pain Points:**

- No visibility into fax PHI exposure
- Manual audit log compilation
- Can't prove faxes weren't altered
- Retention policies hard to enforce
- Breach investigation is nightmare

**Goals:**

- Immutable audit trails
- Automated PHI detection and logging
- Retention policy enforcement
- One-click compliance reports
- Forensic investigation tools

**Quote:** _"When OCR asks for fax audit logs, I need them in minutes, not days."_

---

### 4.4 Edge Persona: Mobile Provider

**Name:** Dr. Sarah Kim  
**Role:** Hospitalist, Always On-Call  
**Device:** iPhone, rarely at desk

**Pain Points:**

- Gets paged about faxes, can't see them
- Has to call office to get fax contents
- Can't sign orders remotely
- Misses critical lab results

**Goals:**

- View faxes on phone instantly
- Sign and return from anywhere
- Critical alerts via push notification
- Offline access to recent faxes

**Quote:** _"If I can't handle it on my phone, it doesn't get handled until tomorrow."_

---

## 5. System Architecture Overview

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Frappe Desk  │  │ Flutter Web  │  │ Flutter      │  │ External     │    │
│  │ (Admin)      │  │ (Portal)     │  │ Mobile       │  │ Systems      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │                 │
          └─────────────────┴─────────────────┴─────────────────┘
                                    │
                         REST API + WebSocket
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                           APPLICATION LAYER                                  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │                    DARTWING FAX MODULE                                  ││
│  │                                                                         ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      ││
│  │  │ Fax Core    │ │ AI Engine   │ │ Routing     │ │ Security    │      ││
│  │  │ Service     │ │ (OCR/NLP)   │ │ Engine      │ │ Engine      │      ││
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      ││
│  │                                                                         ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      ││
│  │  │ Annotation  │ │ Compliance  │ │ Notification│ │ Integration │      ││
│  │  │ Engine      │ │ Engine      │ │ Service     │ │ Hub         │      ││
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │                    FRAPPE FRAMEWORK                                     ││
│  └────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                           PROCESSING LAYER                                   │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ OCR Workers │  │ AI/ML       │  │ Queue       │  │ Scheduler   │        │
│  │ (Tesseract) │  │ Workers     │  │ (Redis/RQ)  │  │ (Celery)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                              DATA LAYER                                      │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ MariaDB     │  │ Redis       │  │ S3/MinIO    │  │ OpenSearch  │        │
│  │ (Metadata)  │  │ (Cache/Q)   │  │ (Documents) │  │ (Search)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                  │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Fax Carriers│  │ Notification│  │ Identity    │  │ Cloud       │        │
│  │ (Telnyx,    │  │ (Twilio,    │  │ (Keycloak)  │  │ Storage     │        │
│  │ Bandwidth)  │  │ SendGrid)   │  │             │  │ (AWS/GCS)   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Data Flow: Inbound Fax

```
┌──────────────┐
│ Fax Carrier  │ (Telnyx/Bandwidth receives fax)
└──────┬───────┘
       │ 1. Webhook POST /api/method/dartwing_fax.api.receive
       ▼
┌──────────────────────────────────────────────────────────────┐
│ INBOUND PROCESSING PIPELINE                                   │
│                                                               │
│  ┌────────────────┐                                          │
│  │ 1. Webhook     │ Validate signature, download file        │
│  │    Handler     │ Create Fax Document (status=received)    │
│  └───────┬────────┘                                          │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 2. Tier 1      │ Check whitelist → bypass AI, deliver     │
│  │    Validation  │ Check blacklist → reject immediately     │
│  └───────┬────────┘ Neither → continue to AI                 │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 3. Background  │ Enqueue for async processing             │
│  │    Queue       │                                          │
│  └───────┬────────┘                                          │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 4. OCR Engine  │ Image enhancement → text extraction      │
│  │                │ ICR for handwriting, hOCR bounding boxes │
│  └───────┬────────┘                                          │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 5. AI Engine   │ NLP classification (category + conf)     │
│  │                │ Entity extraction (names, amounts, dates)│
│  │                │ PHI detection (MedxFax)                  │
│  └───────┬────────┘                                          │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 6. Tier 2      │ Score 0-30 → deliver                     │
│  │    Spam Score  │ Score 31-80 → challenge (Tier 3)         │
│  └───────┬────────┘ Score 81-100 → reject                    │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 7. Routing     │ Evaluate rules by priority               │
│  │    Engine      │ Workload balance across team             │
│  └───────┬────────┘ Assign to user/group/queue               │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 8. Actions     │ Send notifications (email/SMS/push)      │
│  │                │ Trigger webhooks                         │
│  │                │ Create tasks in external systems         │
│  └───────┬────────┘                                          │
│          │                                                    │
│  ┌───────▼────────┐                                          │
│  │ 9. Audit Log   │ Immutable record of all actions          │
│  └────────────────┘                                          │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ User Inbox   │
└──────────────┘
```

### 5.3 Technology Stack

| Layer                | Technology                  | Purpose                |
| -------------------- | --------------------------- | ---------------------- |
| **Framework**        | Frappe 16.x                 | Application platform   |
| **Language**         | Python 3.11+                | Backend logic          |
| **Database**         | MariaDB 10.11+              | Metadata storage       |
| **Cache/Queue**      | Redis 7.x                   | Caching, job queues    |
| **Search**           | OpenSearch 2.x              | Full-text search       |
| **Document Storage** | S3/MinIO                    | File storage           |
| **OCR**              | Tesseract 5.x + ABBYY       | Text extraction        |
| **AI/ML**            | TensorFlow, spaCy, LightGBM | Classification, NER    |
| **PDF Processing**   | PyMuPDF, ReportLab          | Annotation, generation |
| **Mobile**           | Flutter                     | iOS/Android apps       |
| **Auth**             | Keycloak                    | SSO, MFA               |
| **Fax Carriers**     | Telnyx, Bandwidth           | FoIP transport         |
| **Notifications**    | Twilio, SendGrid            | SMS, Email             |

---

## 6. Module Structure

### 6.1 Frappe Module Registration

```python
# apps/dartwing/dartwing/modules.txt
Dartwing Core
Dartwing User
Dartwing Fax          # ← This module
```

### 6.2 Module Dependencies

```
dartwing_fax
├── depends on: dartwing_core (Organization, Person)
├── depends on: dartwing_user (User Profile, preferences)
├── depends on: frappe (User, Role, Permission)
└── optional: dartwing_comms (unified notifications)
```

### 6.3 Sub-Module Organization

| Sub-Module       | Responsibility        | Key Components                  |
| ---------------- | --------------------- | ------------------------------- |
| `fax_core`       | Basic send/receive    | Fax Document, Queue, Provider   |
| `fax_ai`         | AI processing         | OCR, Classification, Extraction |
| `fax_routing`    | Routing logic         | Rules, Engine, Workload         |
| `fax_security`   | Validation            | Whitelist, Blacklist, Challenge |
| `fax_annotation` | Document editing      | Signature, Stamp, Editor        |
| `fax_compliance` | Audit/retention       | Audit Log, Retention, Redaction |
| `fax_numbers`    | DID management        | Provisioning, Porting           |
| `fax_search`     | Search/retrieval      | Index, Search, Filters          |
| `fax_notify`     | Notifications         | Alerts, Escalation              |
| `fax_integrate`  | External systems      | Webhooks, Connectors            |
| `fax_analytics`  | Reporting             | Dashboards, Reports             |
| `fax_mobile`     | Mobile support        | API, Offline sync               |
| `fax_hipaa`      | Healthcare compliance | PHI detection, BAA support      |

---

## 7. Feature Specifications

### Module A: Fax Core Infrastructure

#### A.1 Fax Document Management

**Feature ID:** FAX-A-001  
**Priority:** P0  
**Phase:** 1

**Description:**
Core fax document lifecycle management including creation, storage, retrieval, and status tracking.

**Requirements:**

| ID       | Requirement                                               | Priority |
| -------- | --------------------------------------------------------- | -------- |
| A-001-01 | Create fax document for inbound/outbound                  | Must     |
| A-001-02 | Store original file (TIFF/PDF) immutably                  | Must     |
| A-001-03 | Track status: Pending → Processing → Delivered/Failed     | Must     |
| A-001-04 | Support multi-page faxes (up to 200 pages)                | Must     |
| A-001-05 | Extract and store metadata (sender, recipient, timestamp) | Must     |
| A-001-06 | Generate unique fax ID (FAX-YYYY-NNNNN format)            | Must     |
| A-001-07 | Support file sizes up to 50MB                             | Must     |
| A-001-08 | Convert between TIFF ↔ PDF automatically                  | Must     |
| A-001-09 | Calculate and store file hash for integrity               | Should   |
| A-001-10 | Support fax priority levels (Low/Normal/High/Urgent)      | Should   |

**Fax Document Lifecycle:**

```
INBOUND:
  Received → Validating → Processing → [Delivered | Held | Rejected]

OUTBOUND:
  Draft → Queued → Sending → [Sent | Failed] → [Confirmed | Unconfirmed]
```

#### A.2 Multi-Provider Abstraction

**Feature ID:** FAX-A-002  
**Priority:** P0  
**Phase:** 1

**Description:**
Abstract fax carrier APIs to support multiple providers with automatic failover.

**Requirements:**

| ID       | Requirement                               | Priority |
| -------- | ----------------------------------------- | -------- |
| A-002-01 | Support Telnyx FoIP                       | Must     |
| A-002-02 | Support Bandwidth FoIP                    | Must     |
| A-002-03 | Support SignalWire FoIP                   | Should   |
| A-002-04 | Provider priority ordering for failover   | Must     |
| A-002-05 | Automatic failover on provider failure    | Must     |
| A-002-06 | Provider-specific configuration storage   | Must     |
| A-002-07 | Webhook signature validation per provider | Must     |
| A-002-08 | Rate limiting per provider                | Must     |
| A-002-09 | Cost tracking per provider                | Should   |
| A-002-10 | Health check monitoring                   | Should   |

**Provider Interface:**

```python
class FaxProvider(ABC):
    @abstractmethod
    def send_fax(self, recipient: str, file: bytes, options: dict) -> FaxResult

    @abstractmethod
    def get_status(self, provider_fax_id: str) -> FaxStatus

    @abstractmethod
    def validate_webhook(self, request: dict) -> bool

    @abstractmethod
    def download_fax(self, provider_fax_id: str) -> bytes

    @abstractmethod
    def provision_number(self, area_code: str) -> str

    @abstractmethod
    def release_number(self, number: str) -> bool
```

#### A.3 Outbound Queue Management

**Feature ID:** FAX-A-003  
**Priority:** P0  
**Phase:** 1

**Description:**
Queue-based outbound fax processing with retry logic and scheduling.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| A-003-01 | Queue outbound faxes for async processing       | Must     |
| A-003-02 | Support priority queue (urgent faxes first)     | Must     |
| A-003-03 | Scheduled sending (send at specific time)       | Must     |
| A-003-04 | Automatic retry on failure (configurable max)   | Must     |
| A-003-05 | Exponential backoff between retries             | Must     |
| A-003-06 | Parallel sending (configurable concurrency)     | Must     |
| A-003-07 | Queue depth monitoring and alerting             | Should   |
| A-003-08 | Manual queue management (pause, resume, cancel) | Should   |
| A-003-09 | Bulk queue operations                           | Should   |
| A-003-10 | Dead letter queue for permanent failures        | Should   |

**Retry Configuration:**

```json
{
  "max_retries": 3,
  "initial_delay_seconds": 60,
  "backoff_multiplier": 2,
  "max_delay_seconds": 3600,
  "retry_on_busy": true,
  "retry_on_no_answer": true,
  "retry_on_network_error": true
}
```

---

### Module B: AI-Powered Document Processing

#### B.1 OCR Engine

**Feature ID:** FAX-B-001  
**Priority:** P0  
**Phase:** 2

**Description:**
Optical Character Recognition to extract searchable text from fax images.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| B-001-01 | Extract text from TIFF/PDF fax images           | Must     |
| B-001-02 | Support multiple languages (EN, ES, FR, DE, ZH) | Must     |
| B-001-03 | ICR for handwritten text recognition            | Must     |
| B-001-04 | Image preprocessing (deskew, denoise, contrast) | Must     |
| B-001-05 | Generate hOCR with bounding boxes               | Must     |
| B-001-06 | Confidence scoring per word/line                | Must     |
| B-001-07 | Multi-engine fallback (Tesseract → ABBYY)       | Should   |
| B-001-08 | Process 10-page fax in <8 seconds (p99)         | Must     |
| B-001-09 | Support rotated/inverted pages                  | Should   |
| B-001-10 | Re-OCR capability (manual trigger)              | Should   |

**OCR Output Structure:**

```json
{
  "full_text": "Patient: John Smith\nDOB: 01/15/1980...",
  "pages": [
    {
      "page_number": 1,
      "text": "Patient: John Smith...",
      "confidence": 0.94,
      "words": [
        {
          "text": "Patient",
          "bbox": { "x": 100, "y": 50, "w": 80, "h": 20 },
          "confidence": 0.98
        }
      ]
    }
  ],
  "language_detected": "en",
  "processing_time_ms": 2340
}
```

#### B.2 NLP Classification

**Feature ID:** FAX-B-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Natural Language Processing to automatically classify fax content into categories.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| B-002-01 | Classify fax into predefined categories         | Must     |
| B-002-02 | Return confidence score (0-100%)                | Must     |
| B-002-03 | Support 20+ categories at launch                | Must     |
| B-002-04 | Configurable confidence threshold (default 70%) | Must     |
| B-002-05 | Route low-confidence to human review            | Must     |
| B-002-06 | Multi-label classification support              | Should   |
| B-002-07 | Custom category training per organization       | Should   |
| B-002-08 | Classification accuracy ≥90%                    | Must     |
| B-002-09 | Process in <2 seconds                           | Must     |
| B-002-10 | Feedback loop for model improvement             | Should   |

**Default Categories:**

| Category            | Description              | Keywords                     |
| ------------------- | ------------------------ | ---------------------------- |
| Prescription        | Medication orders        | Rx, DEA, NDC, sig, refill    |
| Lab Results         | Laboratory reports       | CBC, BMP, result, specimen   |
| Referral            | Patient referrals        | refer, consult, specialist   |
| Prior Authorization | Insurance PA requests    | prior auth, PA, approval     |
| Medical Records     | Patient records requests | records, release, HIPAA      |
| Invoice             | Bills and invoices       | invoice, amount due, payment |
| Contract            | Legal agreements         | agreement, terms, signature  |
| Purchase Order      | Procurement              | PO, purchase, order          |
| Resume              | Job applications         | resume, CV, experience       |
| Junk/Spam           | Unsolicited faxes        | free, offer, limited time    |

#### B.3 Entity Extraction

**Feature ID:** FAX-B-003  
**Priority:** P1  
**Phase:** 2

**Description:**
Extract structured data entities from fax content for indexing and automation.

**Requirements:**

| ID       | Requirement                                            | Priority |
| -------- | ------------------------------------------------------ | -------- |
| B-003-01 | Extract named entities (Person, Organization)          | Must     |
| B-003-02 | Extract dates and times                                | Must     |
| B-003-03 | Extract phone numbers                                  | Must     |
| B-003-04 | Extract monetary amounts                               | Must     |
| B-003-05 | Extract healthcare identifiers (MRN, NPI, DEA)         | Must     |
| B-003-06 | Extract medication information (drug, dose, frequency) | Should   |
| B-003-07 | Extract addresses                                      | Should   |
| B-003-08 | Custom entity types per organization                   | Should   |
| B-003-09 | Entity linking to existing records                     | Should   |
| B-003-10 | Store entities as searchable JSON                      | Must     |

**Entity Output Structure:**

```json
{
  "entities": {
    "PERSON": [
      { "text": "John Smith", "start": 10, "end": 20, "confidence": 0.95 }
    ],
    "DATE": [
      { "text": "01/15/1980", "normalized": "1980-01-15", "type": "DOB" }
    ],
    "PHONE": [{ "text": "(555) 123-4567", "normalized": "+15551234567" }],
    "MEDICATION": [
      {
        "drug": "Lisinopril",
        "dose": "10mg",
        "frequency": "daily",
        "quantity": 30
      }
    ],
    "NPI": ["1234567890"],
    "AMOUNT": [{ "value": 150.0, "currency": "USD" }]
  }
}
```

#### B.4 Spam Detection (AI Tier 2)

**Feature ID:** FAX-B-004  
**Priority:** P1  
**Phase:** 2

**Description:**
AI-powered spam scoring to filter unwanted faxes.

**Requirements:**

| ID       | Requirement                                         | Priority |
| -------- | --------------------------------------------------- | -------- |
| B-004-01 | Score fax spam likelihood 0-100                     | Must     |
| B-004-02 | Configurable thresholds per organization            | Must     |
| B-004-03 | Feature analysis: keywords, timing, sender patterns | Must     |
| B-004-04 | Learn from user feedback (mark as spam/not spam)    | Must     |
| B-004-05 | Block known spam senders automatically              | Must     |
| B-004-06 | Detect fax bombing attempts                         | Should   |
| B-004-07 | Geographic anomaly detection                        | Should   |
| B-004-08 | OCR entropy analysis (gibberish detection)          | Should   |
| B-004-09 | False positive rate <1%                             | Must     |
| B-004-10 | Process in <3 seconds                               | Must     |

**Spam Score Thresholds:**

```
0-30:   Low Risk    → Deliver normally
31-60:  Medium Risk → Flag for review, deliver
61-80:  High Risk   → Hold for verification (Tier 3)
81-100: Very High   → Auto-reject
```

---

### Module C: Intelligent Routing Engine

#### C.1 Rule-Based Routing

**Feature ID:** FAX-C-001  
**Priority:** P0  
**Phase:** 2

**Description:**
Configurable rules engine to automatically route faxes to appropriate recipients.

**Requirements:**

| ID       | Requirement                                        | Priority |
| -------- | -------------------------------------------------- | -------- |
| C-001-01 | Create routing rules with conditions and actions   | Must     |
| C-001-02 | Priority ordering (lower number = higher priority) | Must     |
| C-001-03 | Enable/disable rules without deletion              | Must     |
| C-001-04 | Support AND/OR condition logic                     | Must     |
| C-001-05 | Test mode (simulate without executing)             | Must     |
| C-001-06 | Rule audit trail (who created/modified)            | Must     |
| C-001-07 | Import/export rules as JSON                        | Should   |
| C-001-08 | Rule templates library                             | Should   |
| C-001-09 | Rule conflict detection                            | Should   |
| C-001-10 | Organization-scoped rules                          | Must     |

**Condition Types:**

| Condition       | Description               | Example             |
| --------------- | ------------------------- | ------------------- |
| `sender_number` | Match sender phone        | `+1212*` (NYC area) |
| `recipient_did` | Match DID received on     | `+18005551234`      |
| `ai_category`   | Match AI classification   | `Prescription`      |
| `ai_confidence` | Classification confidence | `>= 80`             |
| `page_count`    | Number of pages           | `> 10`              |
| `time_of_day`   | Received time             | `08:00-17:00`       |
| `day_of_week`   | Received day              | `Mon-Fri`           |
| `keyword`       | Text contains             | `STAT`, `URGENT`    |
| `entity_exists` | Extracted entity present  | `NPI`               |
| `spam_score`    | Spam score range          | `< 30`              |

**Action Types:**

| Action           | Description             | Parameters              |
| ---------------- | ----------------------- | ----------------------- |
| `route_to_user`  | Assign to specific user | `user_id`               |
| `route_to_group` | Assign to team/queue    | `group_id`              |
| `route_to_inbox` | Route to shared inbox   | `inbox_id`              |
| `webhook`        | POST to external URL    | `url`, `headers`        |
| `create_task`    | Create task in system   | `task_type`, `assignee` |
| `tag`            | Apply tag/label         | `tag_name`              |
| `priority`       | Set priority level      | `priority`              |
| `notify`         | Send notification       | `channel`, `recipients` |
| `archive`        | Move to archive         | `folder`                |
| `forward`        | Forward via fax/email   | `destination`           |

**Rule Example:**

```json
{
  "rule_name": "STAT Labs to On-Call",
  "priority": 10,
  "enabled": true,
  "conditions": {
    "operator": "AND",
    "rules": [
      { "field": "ai_category", "operator": "equals", "value": "Lab Results" },
      { "field": "keyword", "operator": "contains", "value": "STAT" },
      { "field": "time_of_day", "operator": "outside", "value": "08:00-17:00" }
    ]
  },
  "actions": [
    { "type": "route_to_user", "config": { "user": "oncall@hospital.com" } },
    { "type": "priority", "config": { "level": "urgent" } },
    { "type": "notify", "config": { "channel": "push", "escalate_minutes": 5 } }
  ]
}
```

#### C.2 Workload Balancing

**Feature ID:** FAX-C-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Distribute faxes evenly across team members based on current workload.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| C-002-01 | Round-robin distribution within group           | Must     |
| C-002-02 | Weighted distribution by user capacity          | Should   |
| C-002-03 | Consider current unprocessed fax count          | Must     |
| C-002-04 | Respect user availability (online/offline/busy) | Must     |
| C-002-05 | Skill-based routing (user capabilities)         | Should   |
| C-002-06 | Time-zone aware routing                         | Should   |
| C-002-07 | Overflow to secondary group                     | Should   |
| C-002-08 | Configurable max queue per user                 | Should   |

#### C.3 AI-Assisted Routing

**Feature ID:** FAX-C-003  
**Priority:** P2  
**Phase:** 3

**Description:**
Use AI to learn routing patterns and suggest/automate routing decisions.

**Requirements:**

| ID       | Requirement                            | Priority |
| -------- | -------------------------------------- | -------- |
| C-003-01 | Learn from manual routing decisions    | Should   |
| C-003-02 | Suggest routing for unmatched faxes    | Should   |
| C-003-03 | Auto-route with high confidence (>95%) | Should   |
| C-003-04 | Routing accuracy feedback loop         | Should   |
| C-003-05 | Per-organization model training        | Could    |

---

### Module D: Three-Tier Inbound Security

#### D.1 Tier 1: Whitelist/Blacklist

**Feature ID:** FAX-D-001  
**Priority:** P0  
**Phase:** 1

**Description:**
Hard rules for known good and bad senders.

**Requirements:**

| ID       | Requirement                                 | Priority |
| -------- | ------------------------------------------- | -------- |
| D-001-01 | Whitelist by exact phone number             | Must     |
| D-001-02 | Whitelist by pattern (area code, prefix)    | Must     |
| D-001-03 | Whitelist bypasses AI processing (optional) | Must     |
| D-001-04 | Whitelist direct routing to user/group      | Must     |
| D-001-05 | Blacklist by exact phone number             | Must     |
| D-001-06 | Blacklist by pattern                        | Must     |
| D-001-07 | Global vs personal lists                    | Must     |
| D-001-08 | Auto-add to blacklist on spam report        | Should   |
| D-001-09 | Import/export lists as CSV                  | Should   |
| D-001-10 | O(1) lookup performance (Bloom filter)      | Must     |
| D-001-11 | Sync with external spam databases           | Should   |
| D-001-12 | Whitelist expiration date                   | Should   |

**Lookup Performance:**

- 10M+ numbers in blacklist
- <5ms lookup time
- Hourly sync with external databases

#### D.2 Tier 2: AI Spam Scoring

**Feature ID:** FAX-D-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Machine learning-based spam detection (see B.4 for details).

#### D.3 Tier 3: Challenge Verification

**Feature ID:** FAX-D-003  
**Priority:** P1  
**Phase:** 3

**Description:**
Fax-back questionnaire challenge for suspicious senders.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| D-003-01 | Generate challenge fax with unique code  | Must     |
| D-003-02 | Send challenge to original sender        | Must     |
| D-003-03 | Hold original fax pending response       | Must     |
| D-003-04 | 24-hour response timeout (configurable)  | Must     |
| D-003-05 | Validate response via OCR + code match   | Must     |
| D-003-06 | Auto-whitelist on successful challenge   | Should   |
| D-003-07 | Auto-blacklist on repeated failures      | Should   |
| D-003-08 | Challenge customization per organization | Should   |
| D-003-09 | QR code alternative to numeric code      | Should   |
| D-003-10 | Admin override (manual release)          | Must     |

**Challenge Flow:**

```
1. Suspicious fax received (spam score 31-80)
2. Original fax held in "Held Faxes" queue
3. Challenge fax generated:
   - Unique 6-digit code
   - Instructions to fax back
   - 24-hour expiration
4. Challenge sent to sender's number
5. Wait for response:
   a. Valid response received → Release original, whitelist sender
   b. Invalid response → Keep held, notify admin
   c. No response in 24h → Delete original, optionally blacklist
6. Admin can manually release or reject at any time
```

#### D.4 Held Faxes Queue

**Feature ID:** FAX-D-004  
**Priority:** P0  
**Phase:** 1

**Description:**
Quarantine queue for faxes pending verification or review.

**Requirements:**

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------- |
| D-004-01 | Separate queue view for held faxes               | Must     |
| D-004-02 | Show hold reason (spam score, challenge pending) | Must     |
| D-004-03 | Manual release to inbox                          | Must     |
| D-004-04 | Manual reject and delete                         | Must     |
| D-004-05 | Bulk actions (release all, reject all)           | Should   |
| D-004-06 | Auto-delete after retention period               | Must     |
| D-004-07 | Add to whitelist on release                      | Should   |
| D-004-08 | Add to blacklist on reject                       | Should   |
| D-004-09 | Notification when faxes held                     | Should   |

---

### Module E: Outbound Security & Anti-Spoofing

#### E.1 Sender Authentication

**Feature ID:** FAX-E-001  
**Priority:** P0  
**Phase:** 1

**Description:**
Ensure only authorized users can send faxes and prevent spoofing.

**Requirements:**

| ID       | Requirement                                 | Priority |
| -------- | ------------------------------------------- | -------- |
| E-001-01 | Require user authentication for all sends   | Must     |
| E-001-02 | MFA option for high-volume/sensitive sends  | Must     |
| E-001-03 | Verify sender number ownership              | Must     |
| E-001-04 | Inject verifiable CSID (DFX-YYYYMMDD-XXXX)  | Must     |
| E-001-05 | Rate limiting per user (configurable)       | Must     |
| E-001-06 | Anomaly detection (unusual volume/patterns) | Should   |
| E-001-07 | Send approval workflow for new users        | Should   |
| E-001-08 | IP address restrictions                     | Should   |

#### E.2 Email-to-Fax Security

**Feature ID:** FAX-E-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Secure email-to-fax gateway with verification loop.

**Requirements:**

| ID       | Requirement                                   | Priority |
| -------- | --------------------------------------------- | -------- |
| E-002-01 | SPF/DKIM/DMARC validation on incoming email   | Must     |
| E-002-02 | Only accept from verified email addresses     | Must     |
| E-002-03 | Confirmation loop with preview and code       | Must     |
| E-002-04 | 10-minute code expiration                     | Must     |
| E-002-05 | Whitelist trusted senders (skip confirmation) | Should   |
| E-002-06 | Attachment validation (PDF, TIFF, DOC only)   | Must     |
| E-002-07 | Maximum attachment size (25MB)                | Must     |
| E-002-08 | Subject line parsing for recipient number     | Should   |

**Email-to-Fax Flow:**

```
1. User emails fax@company.dartwing.io
2. System validates SPF/DKIM/DMARC
3. System checks if sender email is verified
4. If not whitelisted:
   a. Generate preview PDF
   b. Send confirmation email with 6-char code
   c. User replies with code or clicks link
   d. Code valid → queue fax
   e. Code invalid/expired → reject
5. If whitelisted:
   a. Queue fax immediately
6. Send confirmation when fax delivered
```

#### E.3 API Security

**Feature ID:** FAX-E-003  
**Priority:** P0  
**Phase:** 1

**Description:**
Secure API access for programmatic fax sending.

**Requirements:**

| ID       | Requirement                      | Priority |
| -------- | -------------------------------- | -------- |
| E-003-01 | API key + secret authentication  | Must     |
| E-003-02 | JWT bearer token support         | Must     |
| E-003-03 | Optional Ed25519 request signing | Should   |
| E-003-04 | Per-key rate limiting            | Must     |
| E-003-05 | Per-key permission scopes        | Must     |
| E-003-06 | API key rotation support         | Must     |
| E-003-07 | IP allowlist per key             | Should   |
| E-003-08 | Usage tracking per key           | Must     |
| E-003-09 | Key expiration dates             | Should   |
| E-003-10 | Webhook signature for callbacks  | Must     |

---

### Module F: Document Annotation & Signature

#### F.1 Signature Management

**Feature ID:** FAX-F-001  
**Priority:** P0  
**Phase:** 4

**Description:**
Create, store, and apply electronic signatures to fax documents.

**Requirements:**

| ID       | Requirement                                    | Priority |
| -------- | ---------------------------------------------- | -------- |
| F-001-01 | Type-to-sign with font selection               | Must     |
| F-001-02 | Draw signature on canvas (mouse/touch)         | Must     |
| F-001-03 | Upload signature image                         | Must     |
| F-001-04 | Background removal for uploaded signatures     | Should   |
| F-001-05 | Save multiple signatures per user              | Must     |
| F-001-06 | Set default signature                          | Must     |
| F-001-07 | Drag/drop signature placement on PDF           | Must     |
| F-001-08 | Resize and rotate signatures                   | Must     |
| F-001-09 | Signature audit metadata (user, timestamp, IP) | Must     |
| F-001-10 | UETA/ESIGN compliant signatures                | Must     |

**Signature Types:**

```
TYPED:
  - Font: "Dancing Script", "Great Vibes", "Pacifico"
  - Random stroke variation for natural look
  - Text: User's name

DRAWN:
  - HTML5 Canvas capture
  - Export as SVG → PNG (2048x2048 transparent)
  - Pressure sensitivity support (stylus)

UPLOADED:
  - Accept PNG, JPG
  - Auto background removal (Remove.bg API)
  - Manual crop/adjust
```

#### F.2 Stamp Templates

**Feature ID:** FAX-F-002  
**Priority:** P1  
**Phase:** 4

**Description:**
Create and apply custom stamps to documents.

**Requirements:**

| ID       | Requirement                                   | Priority |
| -------- | --------------------------------------------- | -------- |
| F-002-01 | Pre-defined stamps (RECEIVED, APPROVED, PAID) | Must     |
| F-002-02 | Custom stamp designer                         | Must     |
| F-002-03 | Include dynamic fields (date, time, user)     | Must     |
| F-002-04 | Configurable colors, fonts, borders           | Must     |
| F-002-05 | Transparency/opacity control                  | Should   |
| F-002-06 | Signature-inside-stamp option                 | Should   |
| F-002-07 | Organization-wide stamp library               | Should   |
| F-002-08 | Role-based stamp access                       | Should   |
| F-002-09 | Drag/drop stamp placement                     | Must     |
| F-002-10 | Auto metadata stamp on receive                | Should   |

**Auto Metadata Stamp:**

```
┌────────────────────────────────────┐
│ RECEIVED VIA FAX                   │
│ 2025-11-26 14:33 EST              │
│ DartwingFax ID: FAX-2025-00123    │
│ From: +1 (555) 123-4567           │
└────────────────────────────────────┘
```

#### F.3 PDF Annotation Editor

**Feature ID:** FAX-F-003  
**Priority:** P0  
**Phase:** 4

**Description:**
Interactive PDF viewer and editor for annotations.

**Requirements:**

| ID       | Requirement                        | Priority |
| -------- | ---------------------------------- | -------- |
| F-003-01 | View PDF in browser (PDF.js)       | Must     |
| F-003-02 | Multi-page navigation              | Must     |
| F-003-03 | Zoom and pan controls              | Must     |
| F-003-04 | Add text annotations               | Must     |
| F-003-05 | Highlight/underline text           | Should   |
| F-003-06 | Draw freehand annotations          | Should   |
| F-003-07 | Add checkmarks and X marks         | Must     |
| F-003-08 | Fill form fields                   | Should   |
| F-003-09 | Undo/redo support                  | Must     |
| F-003-10 | Save annotations as separate layer | Must     |
| F-003-11 | Flatten annotations on finalize    | Must     |
| F-003-12 | Preserve original document         | Must     |

#### F.4 Return Actions

**Feature ID:** FAX-F-004  
**Priority:** P0  
**Phase:** 4

**Description:**
Quick actions to return annotated documents.

**Requirements:**

| ID       | Requirement                          | Priority |
| -------- | ------------------------------------ | -------- |
| F-004-01 | One-click "Return via Fax" to sender | Must     |
| F-004-02 | Return via fax to different number   | Must     |
| F-004-03 | Return via email                     | Must     |
| F-004-04 | Save to file/archive                 | Must     |
| F-004-05 | Flatten PDF before return            | Must     |
| F-004-06 | Add cover page option                | Should   |
| F-004-07 | Track return delivery status         | Must     |
| F-004-08 | Link returned doc to original        | Must     |

---

### Module G: Compliance & Audit Framework

#### G.1 Immutable Audit Logging

**Feature ID:** FAX-G-001  
**Priority:** P0  
**Phase:** 1

**Description:**
Comprehensive, tamper-proof audit trail for all fax activities.

**Requirements:**

| ID       | Requirement                                    | Priority |
| -------- | ---------------------------------------------- | -------- |
| G-001-01 | Log all fax lifecycle events                   | Must     |
| G-001-02 | Immutable logs (no edit/delete after creation) | Must     |
| G-001-03 | Include: user, timestamp, IP, action, details  | Must     |
| G-001-04 | Cryptographic hash chain for tamper detection  | Should   |
| G-001-05 | Log retention minimum 7 years                  | Must     |
| G-001-06 | Export logs for compliance audits              | Must     |
| G-001-07 | Real-time log streaming to SIEM                | Should   |
| G-001-08 | Log access logging (who viewed logs)           | Should   |

**Audit Event Types:**

```
FAX_RECEIVED, FAX_SENT, FAX_VIEWED, FAX_DOWNLOADED,
FAX_ANNOTATED, FAX_SIGNED, FAX_FORWARDED, FAX_DELETED,
FAX_ROUTING_CHANGED, FAX_VALIDATION_RESULT, FAX_CHALLENGE_SENT,
FAX_CHALLENGE_RESPONSE, USER_LOGIN, USER_LOGOUT,
SETTINGS_CHANGED, RULE_CREATED, RULE_MODIFIED
```

#### G.2 Retention Policies

**Feature ID:** FAX-G-002  
**Priority:** P1  
**Phase:** 3

**Description:**
Automated document retention and disposal.

**Requirements:**

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------- |
| G-002-01 | Configurable retention periods per category      | Must     |
| G-002-02 | Auto-archive after retention period              | Must     |
| G-002-03 | Auto-delete after extended retention             | Should   |
| G-002-04 | Legal hold to prevent deletion                   | Must     |
| G-002-05 | Retention policy inheritance (org → dept → user) | Should   |
| G-002-06 | Retention policy audit trail                     | Must     |
| G-002-07 | Notification before deletion                     | Should   |
| G-002-08 | WORM storage option for compliance               | Should   |

**Default Retention Periods:**

```
Healthcare/HIPAA:    6 years
Financial/SOX:       7 years
Legal/Contracts:     10 years
General Business:    3 years
Spam/Rejected:       30 days
```

#### G.3 Redaction Tools

**Feature ID:** FAX-G-003  
**Priority:** P1  
**Phase:** 3

**Description:**
Securely redact sensitive information from fax documents.

**Requirements:**

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------- |
| G-003-01 | Manual redaction (draw black boxes)              | Must     |
| G-003-02 | Remove underlying text, not just overlay         | Must     |
| G-003-03 | AI-assisted redaction (detect SSN, credit cards) | Should   |
| G-003-04 | Regex-based auto-redaction rules                 | Should   |
| G-003-05 | PHI auto-detection and redaction (MedxFax)       | Should   |
| G-003-06 | Redaction audit trail                            | Must     |
| G-003-07 | Irreversible redaction (no undo after save)      | Must     |
| G-003-08 | Redacted document as separate version            | Must     |

#### G.4 Certified Delivery Receipts

**Feature ID:** FAX-G-004  
**Priority:** P1  
**Phase:** 2

**Description:**
Tamper-evident proof of fax delivery.

**Requirements:**

| ID       | Requirement                                         | Priority |
| -------- | --------------------------------------------------- | -------- |
| G-004-01 | Generate delivery receipt on successful send        | Must     |
| G-004-02 | Include: timestamp, recipient, page count, duration | Must     |
| G-004-03 | Digital signature on receipt                        | Should   |
| G-004-04 | PDF receipt downloadable                            | Must     |
| G-004-05 | Receipt stored with fax document                    | Must     |
| G-004-06 | Verify receipt authenticity                         | Should   |

---

### Module H: Number Management & Provisioning

#### H.1 DID Provisioning

**Feature ID:** FAX-H-001  
**Priority:** P0  
**Phase:** 1

**Description:**
Self-service fax number acquisition and management.

**Requirements:**

| ID       | Requirement                           | Priority |
| -------- | ------------------------------------- | -------- |
| H-001-01 | Search available numbers by area code | Must     |
| H-001-02 | Search by city/state                  | Should   |
| H-001-03 | Toll-free number provisioning         | Must     |
| H-001-04 | International number provisioning     | Should   |
| H-001-05 | Instant activation (<60 seconds)      | Must     |
| H-001-06 | Monthly recurring billing             | Must     |
| H-001-07 | Number release/cancellation           | Must     |
| H-001-08 | Multiple numbers per organization     | Must     |
| H-001-09 | Personal dedicated numbers per user   | Should   |

#### H.2 Number Porting

**Feature ID:** FAX-H-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Port existing fax numbers from other providers.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| H-002-01 | Port-in request workflow                 | Must     |
| H-002-02 | LOA (Letter of Authorization) generation | Must     |
| H-002-03 | Port status tracking                     | Must     |
| H-002-04 | Estimated completion date                | Should   |
| H-002-05 | Port-out support                         | Should   |
| H-002-06 | Bulk porting (multiple numbers)          | Should   |

#### H.3 Number Assignment

**Feature ID:** FAX-H-003  
**Priority:** P0  
**Phase:** 1

**Description:**
Assign numbers to users, departments, or routing rules.

**Requirements:**

| ID       | Requirement                    | Priority |
| -------- | ------------------------------ | -------- |
| H-003-01 | Assign DID to user             | Must     |
| H-003-02 | Assign DID to group/department | Must     |
| H-003-03 | Assign DID to routing rule     | Must     |
| H-003-04 | Multiple DIDs per entity       | Must     |
| H-003-05 | DID display name/label         | Should   |
| H-003-06 | DID usage analytics            | Should   |

---

### Module I: Search & Knowledge Layer

#### I.1 Full-Text Search

**Feature ID:** FAX-I-001  
**Priority:** P0  
**Phase:** 2

**Description:**
Search across all fax content and metadata.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| I-001-01 | Full-text search of OCR content          | Must     |
| I-001-02 | Metadata search (sender, date, category) | Must     |
| I-001-03 | Combined content + metadata queries      | Must     |
| I-001-04 | Search results <1 second                 | Must     |
| I-001-05 | Relevance ranking                        | Must     |
| I-001-06 | Search highlighting                      | Should   |
| I-001-07 | Fuzzy matching                           | Should   |
| I-001-08 | Search suggestions/autocomplete          | Should   |
| I-001-09 | Boolean operators (AND, OR, NOT)         | Must     |
| I-001-10 | Date range filters                       | Must     |
| I-001-11 | Category filters                         | Must     |
| I-001-12 | Saved searches                           | Should   |
| I-001-13 | Shared searches (team)                   | Should   |

**Search Query Examples:**

```
# Simple text search
prescription lisinopril

# With filters
category:prescription AND date:>2025-01-01 AND sender:+1212*

# Entity search
entity.NPI:1234567890

# Complex boolean
(STAT OR urgent) AND category:lab_results AND NOT spam:true
```

#### I.2 Search Indexing

**Feature ID:** FAX-I-002  
**Priority:** P0  
**Phase:** 2

**Description:**
Real-time indexing of fax content for search.

**Requirements:**

| ID       | Requirement                                   | Priority |
| -------- | --------------------------------------------- | -------- |
| I-002-01 | Index fax within 10 seconds of OCR completion | Must     |
| I-002-02 | Index OCR text                                | Must     |
| I-002-03 | Index extracted entities                      | Must     |
| I-002-04 | Index metadata (sender, recipient, date)      | Must     |
| I-002-05 | Index annotations                             | Should   |
| I-002-06 | Re-index on OCR re-run                        | Must     |
| I-002-07 | Bulk re-index capability                      | Should   |
| I-002-08 | Index health monitoring                       | Should   |

---

### Module J: Notifications & Alerting

#### J.1 Rule-Based Alerts

**Feature ID:** FAX-J-001  
**Priority:** P1  
**Phase:** 2

**Description:**
Configurable notifications based on fax characteristics.

**Requirements:**

| ID       | Requirement                          | Priority |
| -------- | ------------------------------------ | -------- |
| J-001-01 | Alert on keyword detection           | Must     |
| J-001-02 | Alert on category match              | Must     |
| J-001-03 | Alert on sender match                | Must     |
| J-001-04 | Alert on priority level              | Must     |
| J-001-05 | Multiple notification channels       | Must     |
| J-001-06 | Alert schedule (business hours only) | Should   |
| J-001-07 | Alert cooldown (don't spam)          | Should   |
| J-001-08 | Alert acknowledgment                 | Should   |

#### J.2 Notification Channels

**Feature ID:** FAX-J-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Multi-channel notification delivery.

**Requirements:**

| ID       | Requirement                     | Priority |
| -------- | ------------------------------- | -------- |
| J-002-01 | Email notifications             | Must     |
| J-002-02 | SMS notifications (Twilio)      | Must     |
| J-002-03 | Push notifications (mobile app) | Must     |
| J-002-04 | Slack integration               | Should   |
| J-002-05 | Microsoft Teams integration     | Should   |
| J-002-06 | Webhook notifications           | Should   |
| J-002-07 | In-app notifications            | Must     |

#### J.3 Escalation Paths

**Feature ID:** FAX-J-003  
**Priority:** P2  
**Phase:** 3

**Description:**
Time-based escalation for unacknowledged faxes.

**Requirements:**

| ID       | Requirement                    | Priority |
| -------- | ------------------------------ | -------- |
| J-003-01 | Define escalation tiers        | Should   |
| J-003-02 | Time-based escalation triggers | Should   |
| J-003-03 | Escalate to manager/backup     | Should   |
| J-003-04 | Escalation audit trail         | Should   |
| J-003-05 | On-call schedule integration   | Could    |

---

### Module K: Team Collaboration

#### K.1 Shared Inboxes

**Feature ID:** FAX-K-001  
**Priority:** P1  
**Phase:** 2

**Description:**
Team-based fax queues with collaboration features.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| K-001-01 | Create shared inbox for team             | Must     |
| K-001-02 | Assign inbox members                     | Must     |
| K-001-03 | Role-based permissions (view/edit/admin) | Must     |
| K-001-04 | Claim/unclaim faxes                      | Must     |
| K-001-05 | See who is working on fax                | Must     |
| K-001-06 | Inbox-level routing rules                | Should   |
| K-001-07 | Inbox-level analytics                    | Should   |

#### K.2 Internal Comments

**Feature ID:** FAX-K-002  
**Priority:** P1  
**Phase:** 2

**Description:**
Add internal notes and discussions to faxes.

**Requirements:**

| ID       | Requirement                      | Priority |
| -------- | -------------------------------- | -------- |
| K-002-01 | Add text comments to fax         | Must     |
| K-002-02 | @mention team members            | Should   |
| K-002-03 | Comment timestamps and author    | Must     |
| K-002-04 | Edit/delete own comments         | Should   |
| K-002-05 | Comment notifications            | Should   |
| K-002-06 | Internal (not printed/forwarded) | Must     |

#### K.3 Folder Organization

**Feature ID:** FAX-K-003  
**Priority:** P1  
**Phase:** 2

**Description:**
Organize faxes into folders and subfolders.

**Requirements:**

| ID       | Requirement                            | Priority |
| -------- | -------------------------------------- | -------- |
| K-003-01 | Create folders and subfolders          | Must     |
| K-003-02 | Move faxes to folders                  | Must     |
| K-003-03 | Folder permissions                     | Should   |
| K-003-04 | Folder sharing                         | Should   |
| K-003-05 | Smart folders (auto-populate by rules) | Should   |
| K-003-06 | Folder templates                       | Should   |

---

### Module L: Integrations & Storage

#### L.1 Pre-Built Connectors

**Feature ID:** FAX-L-001  
**Priority:** P1  
**Phase:** 4

**Description:**
Zero-code integrations with popular business systems.

**Launch Connectors:**

| Connector        | Category           | Capabilities                  |
| ---------------- | ------------------ | ----------------------------- |
| Salesforce       | CRM                | Attach fax to contact/account |
| DocuSign         | E-Signature        | Send for signature            |
| Google Workspace | Productivity       | Save to Drive                 |
| Microsoft 365    | Productivity       | Save to OneDrive/SharePoint   |
| QuickBooks       | Accounting         | Attach to invoice             |
| Slack            | Communication      | Post fax notification         |
| Teams            | Communication      | Post fax notification         |
| Jira             | Project Management | Create issue                  |
| Asana            | Project Management | Create task                   |
| Zendesk          | Support            | Create ticket                 |

#### L.2 Webhook System

**Feature ID:** FAX-L-002  
**Priority:** P0  
**Phase:** 2

**Description:**
Push fax events to external systems via webhooks.

**Requirements:**

| ID       | Requirement                     | Priority |
| -------- | ------------------------------- | -------- |
| L-002-01 | Configure webhook endpoints     | Must     |
| L-002-02 | Select events to trigger        | Must     |
| L-002-03 | Include fax metadata in payload | Must     |
| L-002-04 | Include extracted entities      | Should   |
| L-002-05 | HMAC signature verification     | Must     |
| L-002-06 | Retry with exponential backoff  | Must     |
| L-002-07 | Delivery status tracking        | Must     |
| L-002-08 | Webhook testing UI              | Should   |

**Webhook Events:**

```
fax.received
fax.delivered
fax.sent
fax.failed
fax.routed
fax.annotated
fax.validation.held
fax.validation.released
fax.validation.rejected
```

**Webhook Payload:**

```json
{
  "event": "fax.received",
  "timestamp": "2025-11-26T14:33:00Z",
  "fax_id": "FAX-2025-00123",
  "data": {
    "direction": "inbound",
    "sender": "+15551234567",
    "recipient": "+18005559999",
    "pages": 3,
    "category": "Prescription",
    "confidence": 0.92,
    "entities": {
      "PATIENT": ["John Smith"],
      "MEDICATION": ["Lisinopril 10mg"]
    },
    "file_url": "https://..."
  },
  "signature": "sha256=..."
}
```

#### L.3 Cloud Storage Integration

**Feature ID:** FAX-L-003  
**Priority:** P1  
**Phase:** 3

**Description:**
Archive faxes to customer-controlled cloud storage.

**Requirements:**

| ID       | Requirement                             | Priority |
| -------- | --------------------------------------- | -------- |
| L-003-01 | Push to AWS S3                          | Must     |
| L-003-02 | Push to Azure Blob Storage              | Should   |
| L-003-03 | Push to Google Cloud Storage            | Should   |
| L-003-04 | Customer-managed encryption keys (BYOK) | Should   |
| L-003-05 | Configurable folder structure           | Should   |
| L-003-06 | Batch vs real-time push                 | Should   |
| L-003-07 | Storage connection health check         | Should   |

---

### Module M: Analytics & Reporting

#### M.1 Executive Dashboard

**Feature ID:** FAX-M-001  
**Priority:** P1  
**Phase:** 3

**Description:**
High-level metrics and KPIs visualization.

**Dashboard Widgets:**

| Widget                | Metrics                                          |
| --------------------- | ------------------------------------------------ |
| Volume Summary        | Inbound/outbound today, this week, this month    |
| Trend Chart           | Volume over time                                 |
| Status Breakdown      | Delivered, failed, held, pending                 |
| Category Distribution | Pie chart by AI category                         |
| Top Senders           | Most frequent inbound sources                    |
| Spam Metrics          | Blocked %, false positive rate                   |
| AI Performance        | Classification accuracy, confidence distribution |
| Response Time         | Average time to first action                     |

#### M.2 Operational Reports

**Feature ID:** FAX-M-002  
**Priority:** P1  
**Phase:** 3

**Description:**
Detailed reports for operations and compliance.

**Reports:**

| Report            | Purpose                       | Schedule  |
| ----------------- | ----------------------------- | --------- |
| Activity Log      | All fax actions               | On-demand |
| Routing Accuracy  | Rule performance              | Weekly    |
| User Productivity | Faxes processed per user      | Weekly    |
| Delivery Success  | Send success/failure rates    | Daily     |
| Spam Analysis     | Blocked vs delivered          | Weekly    |
| Compliance Audit  | Full audit trail              | On-demand |
| Cost Analysis     | Carrier costs, per-page costs | Monthly   |

#### M.3 Report Export

**Feature ID:** FAX-M-003  
**Priority:** P1  
**Phase:** 3

**Description:**
Export reports in various formats.

**Requirements:**

| ID       | Requirement               | Priority |
| -------- | ------------------------- | -------- |
| M-003-01 | Export to PDF             | Must     |
| M-003-02 | Export to Excel           | Must     |
| M-003-03 | Export to CSV             | Must     |
| M-003-04 | Scheduled report delivery | Should   |
| M-003-05 | Report customization      | Should   |

---

### Module N: Mobile Experience

#### N.1 Mobile App (Flutter)

**Feature ID:** FAX-N-001  
**Priority:** P1  
**Phase:** 4

**Description:**
Native mobile app for iOS and Android.

**Requirements:**

| ID       | Requirement                   | Priority |
| -------- | ----------------------------- | -------- |
| N-001-01 | View fax inbox                | Must     |
| N-001-02 | View fax document             | Must     |
| N-001-03 | Annotate and sign             | Must     |
| N-001-04 | Send fax                      | Must     |
| N-001-05 | Camera scan to fax            | Must     |
| N-001-06 | Auto deskew scanned documents | Should   |
| N-001-07 | Push notifications            | Must     |
| N-001-08 | Biometric login               | Must     |
| N-001-09 | Offline fax queue             | Should   |
| N-001-10 | Dark mode                     | Should   |
| N-001-11 | App Store rating goal: 4.8+   | Target   |

#### N.2 Offline Capability

**Feature ID:** FAX-N-002  
**Priority:** P2  
**Phase:** 4

**Description:**
Work with faxes without network connectivity.

**Requirements:**

| ID       | Requirement                     | Priority |
| -------- | ------------------------------- | -------- |
| N-002-01 | Cache recent faxes locally      | Should   |
| N-002-02 | Queue outbound faxes offline    | Should   |
| N-002-03 | Sync when connectivity restored | Should   |
| N-002-04 | Conflict resolution             | Should   |

---

### Module O: Multi-Channel Communications

#### O.1 Bulk/Broadcast Fax

**Feature ID:** FAX-O-001  
**Priority:** P2  
**Phase:** 3

**Description:**
Send fax to multiple recipients.

**Requirements:**

| ID       | Requirement                      | Priority |
| -------- | -------------------------------- | -------- |
| O-001-01 | Upload recipient list (CSV)      | Must     |
| O-001-02 | Merge fields for personalization | Should   |
| O-001-03 | Schedule broadcast               | Must     |
| O-001-04 | Track delivery per recipient     | Must     |
| O-001-05 | TCPA opt-out compliance          | Must     |
| O-001-06 | Rate limiting                    | Must     |
| O-001-07 | Pause/resume broadcast           | Should   |

#### O.2 Smart Reply

**Feature ID:** FAX-O-002  
**Priority:** P2  
**Phase:** 4

**Description:**
Automatically choose best response channel.

**Requirements:**

| ID       | Requirement                     | Priority |
| -------- | ------------------------------- | -------- |
| O-002-01 | Detect recipient preference     | Should   |
| O-002-02 | Auto-select: fax, email, or SMS | Should   |
| O-002-03 | Fallback chain if primary fails | Should   |
| O-002-04 | User override                   | Should   |

#### O.3 Large File Fallback

**Feature ID:** FAX-O-003  
**Priority:** P2  
**Phase:** 4

**Description:**
Handle files too large for fax.

**Requirements:**

| ID       | Requirement                      | Priority |
| -------- | -------------------------------- | -------- |
| O-003-01 | Detect files >50MB               | Should   |
| O-003-02 | Generate encrypted download link | Should   |
| O-003-03 | Link expiration (configurable)   | Should   |
| O-003-04 | Send link via fax cover page     | Should   |
| O-003-05 | Download tracking                | Should   |

---

### Module P: Form Recognition & Parsing

#### P.1 Template-Based Form Parsing

**Feature ID:** FAX-P-001  
**Priority:** P2  
**Phase:** 3

**Description:**
Extract structured data from known form types.

**Supported Forms (Launch):**

| Form         | Category   | Key Fields                              |
| ------------ | ---------- | --------------------------------------- |
| CMS-1500     | Healthcare | Patient, provider, diagnosis, procedure |
| UB-04        | Healthcare | Patient, facility, charges              |
| W-9          | Tax        | Name, TIN, address                      |
| 1099         | Tax        | Payer, recipient, amounts               |
| Prior Auth   | Healthcare | Patient, medication, diagnosis          |
| Prescription | Healthcare | Patient, drug, dosage, prescriber       |

**Requirements:**

| ID       | Requirement                       | Priority |
| -------- | --------------------------------- | -------- |
| P-001-01 | Recognize form type automatically | Must     |
| P-001-02 | Extract fields to structured JSON | Must     |
| P-001-03 | Confidence score per field        | Should   |
| P-001-04 | Custom form template creation     | Should   |
| P-001-05 | Form template marketplace         | Could    |
| P-001-06 | Export to EHR/Practice Management | Should   |

---

### Module Q: Branding & Templates

#### Q.1 Cover Page Designer

**Feature ID:** FAX-Q-001  
**Priority:** P1  
**Phase:** 2

**Description:**
WYSIWYG cover page template designer.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| Q-001-01 | Drag-drop cover page designer            | Must     |
| Q-001-02 | Add logo, text, fields                   | Must     |
| Q-001-03 | Dynamic fields (recipient, sender, date) | Must     |
| Q-001-04 | Per-department templates                 | Should   |
| Q-001-05 | Default template per user                | Should   |
| Q-001-06 | HIPAA confidentiality notice             | Must     |
| Q-001-07 | Handlebars template support              | Should   |

**Dynamic Fields:**

```
{{sender_name}}
{{sender_company}}
{{sender_phone}}
{{sender_fax}}
{{recipient_name}}
{{recipient_company}}
{{recipient_fax}}
{{date}}
{{time}}
{{page_count}}
{{subject}}
{{message}}
{{confidentiality_notice}}
```

---

### Module R: HIPAA Compliance Framework

_This module provides the foundation for MedxFax and other healthcare applications._

#### R.1 PHI Detection

**Feature ID:** FAX-R-001  
**Priority:** P0 (MedxFax)  
**Phase:** 2

**Description:**
Automatically detect Protected Health Information in fax content.

**PHI Elements Detected:**

| Element                  | Detection Method | Action           |
| ------------------------ | ---------------- | ---------------- |
| Patient Name             | NER              | Flag, log        |
| Date of Birth            | Regex + NER      | Flag, log        |
| SSN                      | Regex            | Flag, log, alert |
| Medical Record Number    | Regex            | Flag, log        |
| Account Number           | Regex            | Flag, log        |
| Health Plan ID           | Regex            | Flag, log        |
| Diagnosis Codes (ICD-10) | Regex            | Flag, log        |
| Procedure Codes (CPT)    | Regex            | Flag, log        |
| Lab Results              | Category + NER   | Flag, log        |
| Medication Names         | NER + drug DB    | Flag, log        |

**Requirements:**

| ID       | Requirement                             | Priority |
| -------- | --------------------------------------- | -------- |
| R-001-01 | Scan all inbound faxes for PHI          | Must     |
| R-001-02 | Flag faxes containing PHI               | Must     |
| R-001-03 | Log PHI elements detected (not content) | Must     |
| R-001-04 | PHI detection accuracy >95%             | Must     |
| R-001-05 | PHI-aware routing rules                 | Must     |
| R-001-06 | PHI access audit trail                  | Must     |
| R-001-07 | PHI masking in logs                     | Must     |

#### R.2 Access Controls

**Feature ID:** FAX-R-002  
**Priority:** P0 (MedxFax)  
**Phase:** 1

**Description:**
Role-based access controls for PHI-containing faxes.

**Requirements:**

| ID       | Requirement                        | Priority |
| -------- | ---------------------------------- | -------- |
| R-002-01 | Role-based fax access              | Must     |
| R-002-02 | Minimum necessary access principle | Must     |
| R-002-03 | Break-glass emergency access       | Should   |
| R-002-04 | Access request workflow            | Should   |
| R-002-05 | Access expiration                  | Should   |
| R-002-06 | Department-based access            | Must     |

#### R.3 Encryption Requirements

**Feature ID:** FAX-R-003  
**Priority:** P0 (MedxFax)  
**Phase:** 1

**Description:**
Encryption for PHI at rest and in transit.

**Requirements:**

| ID       | Requirement                     | Priority |
| -------- | ------------------------------- | -------- |
| R-003-01 | TLS 1.3 for all data in transit | Must     |
| R-003-02 | AES-256 encryption at rest      | Must     |
| R-003-03 | Encryption key management       | Must     |
| R-003-04 | Customer-managed keys option    | Should   |
| R-003-05 | Encrypted backups               | Must     |
| R-003-06 | Secure key rotation             | Must     |

#### R.4 BAA Support

**Feature ID:** FAX-R-004  
**Priority:** P0 (MedxFax)  
**Phase:** 1

**Description:**
Business Associate Agreement workflow.

**Requirements:**

| ID       | Requirement                | Priority |
| -------- | -------------------------- | -------- |
| R-004-01 | BAA template generation    | Must     |
| R-004-02 | Electronic BAA signing     | Should   |
| R-004-03 | BAA tracking per customer  | Must     |
| R-004-04 | BAA expiration alerts      | Should   |
| R-004-05 | Subcontractor BAA tracking | Should   |

#### R.5 Healthcare-Specific Routing

**Feature ID:** FAX-R-005  
**Priority:** P1 (MedxFax)  
**Phase:** 2

**Description:**
Route faxes based on healthcare-specific criteria.

**Requirements:**

| ID       | Requirement                                  | Priority |
| -------- | -------------------------------------------- | -------- |
| R-005-01 | Route by NPI (provider lookup)               | Should   |
| R-005-02 | Route by department (lab, pharmacy, nursing) | Must     |
| R-005-03 | STAT/urgent priority detection               | Must     |
| R-005-04 | Critical value alerts                        | Must     |
| R-005-05 | Prescription routing to pharmacy             | Must     |
| R-005-06 | Lab result routing to ordering provider      | Must     |

#### R.6 Compliance Reporting

**Feature ID:** FAX-R-006  
**Priority:** P1 (MedxFax)  
**Phase:** 3

**Description:**
HIPAA compliance audit reports.

**Reports:**

| Report                | Purpose                        |
| --------------------- | ------------------------------ |
| PHI Access Log        | Who accessed what PHI and when |
| PHI Disclosure Log    | External PHI transmissions     |
| Security Incident Log | Potential breach events        |
| User Access Review    | Periodic access certification  |
| Training Compliance   | User HIPAA training status     |

---

## 8. DocType Specifications

### 8.1 Core DocTypes

| DocType          | Module         | Type      | Phase | Description               |
| ---------------- | -------------- | --------- | ----- | ------------------------- |
| Fax Document     | fax_core       | Standard  | 1     | Main fax record           |
| Fax Queue        | fax_core       | Standard  | 1     | Outbound queue            |
| Fax Provider     | fax_core       | Master    | 1     | Carrier configuration     |
| Fax Settings     | fax_core       | Single    | 1     | Global settings           |
| Fax Number       | fax_numbers    | Master    | 1     | DID management            |
| Fax Category     | fax_ai         | Master    | 2     | Classification categories |
| Routing Rule     | fax_routing    | Standard  | 2     | Routing configuration     |
| Whitelist Entry  | fax_security   | Master    | 1     | Approved senders          |
| Blacklist Entry  | fax_security   | Master    | 1     | Blocked senders           |
| Fax Challenge    | fax_security   | Standard  | 3     | Tier 3 verification       |
| Signature        | fax_annotation | Master    | 4     | User signatures           |
| Stamp Template   | fax_annotation | Master    | 4     | Stamp designs             |
| Fax Audit Log    | fax_compliance | Immutable | 1     | Audit trail               |
| Retention Policy | fax_compliance | Master    | 3     | Retention rules           |
| Fax Webhook      | fax_integrate  | Master    | 2     | Webhook configs           |
| Fax API Key      | fax_security   | Master    | 1     | API credentials           |
| Shared Inbox     | fax_collab     | Master    | 2     | Team inboxes              |
| Fax Folder       | fax_collab     | Master    | 2     | Organization              |
| Fax Comment      | fax_collab     | Standard  | 2     | Internal comments         |
| Alert Rule       | fax_notify     | Master    | 2     | Notification rules        |

### 8.2 Fax Document DocType (Detailed)

```json
{
  "doctype": "Fax Document",
  "module": "Dartwing Fax",
  "naming_rule": "Expression",
  "autoname": "FAX-{YYYY}-{#####}",
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "direction",
      "label": "Direction",
      "fieldtype": "Select",
      "options": "Inbound\nOutbound",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Received\nProcessing\nDelivered\nHeld\nRejected\nDraft\nQueued\nSending\nSent\nFailed",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "section_contact",
      "label": "Contact Information",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "sender_number",
      "label": "Sender Number",
      "fieldtype": "Data",
      "options": "Phone",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "sender_name",
      "label": "Sender Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "recipient_number",
      "label": "Recipient Number",
      "fieldtype": "Data",
      "options": "Phone",
      "reqd": 1
    },
    {
      "fieldname": "recipient_name",
      "label": "Recipient Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_timing",
      "label": "Timing",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "received_at",
      "label": "Received At",
      "fieldtype": "Datetime",
      "depends_on": "eval:doc.direction=='Inbound'"
    },
    {
      "fieldname": "sent_at",
      "label": "Sent At",
      "fieldtype": "Datetime",
      "depends_on": "eval:doc.direction=='Outbound'"
    },
    {
      "fieldname": "column_break_2",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "section_document",
      "label": "Document",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "original_file",
      "label": "Original File",
      "fieldtype": "Attach",
      "reqd": 1
    },
    {
      "fieldname": "annotated_file",
      "label": "Annotated File",
      "fieldtype": "Attach"
    },
    {
      "fieldname": "column_break_3",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "pages",
      "label": "Pages",
      "fieldtype": "Int",
      "reqd": 1
    },
    {
      "fieldname": "file_size",
      "label": "File Size (bytes)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "file_hash",
      "label": "File Hash",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "section_ai",
      "label": "AI Processing",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "ocr_text",
      "label": "OCR Text",
      "fieldtype": "Long Text"
    },
    {
      "fieldname": "ocr_confidence",
      "label": "OCR Confidence",
      "fieldtype": "Percent"
    },
    {
      "fieldname": "column_break_4",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "ai_category",
      "label": "Category",
      "fieldtype": "Link",
      "options": "Fax Category"
    },
    {
      "fieldname": "ai_confidence",
      "label": "Classification Confidence",
      "fieldtype": "Percent"
    },
    {
      "fieldname": "entities_json",
      "label": "Extracted Entities",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "section_validation",
      "label": "Validation",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "validation_status",
      "label": "Validation Status",
      "fieldtype": "Select",
      "options": "\nWhitelisted\nPassed\nHeld\nChallenged\nRejected"
    },
    {
      "fieldname": "spam_score",
      "label": "Spam Score",
      "fieldtype": "Percent"
    },
    {
      "fieldname": "column_break_5",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "validation_tier",
      "label": "Validation Tier",
      "fieldtype": "Int"
    },
    {
      "fieldname": "challenge_id",
      "label": "Challenge",
      "fieldtype": "Link",
      "options": "Fax Challenge"
    },
    {
      "fieldname": "section_assignment",
      "label": "Assignment",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "User"
    },
    {
      "fieldname": "assigned_group",
      "label": "Assigned Group",
      "fieldtype": "Link",
      "options": "User Group"
    },
    {
      "fieldname": "shared_inbox",
      "label": "Shared Inbox",
      "fieldtype": "Link",
      "options": "Shared Inbox"
    },
    {
      "fieldname": "column_break_6",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "routed_by_rule",
      "label": "Routed By Rule",
      "fieldtype": "Link",
      "options": "Routing Rule"
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Select",
      "options": "Low\nNormal\nHigh\nUrgent",
      "default": "Normal"
    },
    {
      "fieldname": "section_compliance",
      "label": "Compliance",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "contains_phi",
      "label": "Contains PHI",
      "fieldtype": "Check"
    },
    {
      "fieldname": "phi_elements",
      "label": "PHI Elements Detected",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "column_break_7",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "retention_policy",
      "label": "Retention Policy",
      "fieldtype": "Link",
      "options": "Retention Policy"
    },
    {
      "fieldname": "legal_hold",
      "label": "Legal Hold",
      "fieldtype": "Check"
    },
    {
      "fieldname": "retain_until",
      "label": "Retain Until",
      "fieldtype": "Date"
    },
    {
      "fieldname": "section_provider",
      "label": "Provider Details",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "fax_provider",
      "label": "Fax Provider",
      "fieldtype": "Link",
      "options": "Fax Provider"
    },
    {
      "fieldname": "provider_fax_id",
      "label": "Provider Fax ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "column_break_8",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "delivery_receipt",
      "label": "Delivery Receipt",
      "fieldtype": "Attach"
    },
    {
      "fieldname": "transmission_log",
      "label": "Transmission Log",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "section_folder",
      "label": "Organization",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "folder",
      "label": "Folder",
      "fieldtype": "Link",
      "options": "Fax Folder"
    },
    {
      "fieldname": "tags",
      "label": "Tags",
      "fieldtype": "Table MultiSelect",
      "options": "Fax Tag"
    },
    {
      "fieldname": "section_notes",
      "label": "Notes",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "notes",
      "label": "Notes",
      "fieldtype": "Text Editor"
    },
    {
      "fieldname": "section_child_tables",
      "label": "",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "annotations",
      "label": "Annotations",
      "fieldtype": "Table",
      "options": "Fax Annotation"
    },
    {
      "fieldname": "routing_history",
      "label": "Routing History",
      "fieldtype": "Table",
      "options": "Fax Routing History"
    },
    {
      "fieldname": "comments",
      "label": "Comments",
      "fieldtype": "Table",
      "options": "Fax Comment"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    { "role": "Fax Admin", "read": 1, "write": 1, "create": 1, "delete": 1 },
    { "role": "Fax User", "read": 1, "write": 1, "create": 1 }
  ]
}
```

---

## 9. API Specifications

### 9.1 API Endpoints Summary

| Endpoint                                         | Method | Purpose             | Auth      |
| ------------------------------------------------ | ------ | ------------------- | --------- |
| `/api/method/dartwing_fax.api.receive`           | POST   | Inbound webhook     | Signature |
| `/api/method/dartwing_fax.api.send`              | POST   | Send fax            | Bearer    |
| `/api/method/dartwing_fax.api.status`            | GET    | Get fax status      | Bearer    |
| `/api/method/dartwing_fax.api.list`              | GET    | List faxes          | Bearer    |
| `/api/method/dartwing_fax.api.download`          | GET    | Download fax file   | Bearer    |
| `/api/method/dartwing_fax.api.annotate`          | POST   | Apply annotation    | Bearer    |
| `/api/method/dartwing_fax.api.route`             | POST   | Manual routing      | Bearer    |
| `/api/method/dartwing_fax.api.validate`          | POST   | Manual validation   | Bearer    |
| `/api/method/dartwing_fax.api.search`            | POST   | Search faxes        | Bearer    |
| `/api/method/dartwing_fax.api.numbers.list`      | GET    | List DIDs           | Bearer    |
| `/api/method/dartwing_fax.api.numbers.provision` | POST   | Provision DID       | Bearer    |
| `/api/resource/Fax Document`                     | CRUD   | Standard Frappe API | Bearer    |

### 9.2 Send Fax API

**Endpoint:** `POST /api/method/dartwing_fax.api.send`

**Request:**

```json
{
  "recipient": "+15551234567",
  "file": "base64_encoded_pdf_or_url",
  "file_type": "pdf",
  "sender_number": "+18005559999",
  "cover_page": true,
  "cover_page_template": "default",
  "subject": "Invoice #12345",
  "message": "Please review the attached invoice.",
  "priority": "normal",
  "scheduled_at": "2025-11-27T09:00:00Z",
  "callback_url": "https://example.com/webhook",
  "metadata": {
    "invoice_id": "12345",
    "customer_id": "CUST-001"
  }
}
```

**Response:**

```json
{
  "success": true,
  "fax_id": "FAX-2025-00123",
  "status": "queued",
  "estimated_delivery": "2025-11-27T09:05:00Z"
}
```

### 9.3 Receive Webhook

**Endpoint:** `POST /api/method/dartwing_fax.api.receive`

**Headers:**

```
X-Signature: sha256=abc123...
X-Provider: telnyx
Content-Type: application/json
```

**Payload (varies by provider, normalized):**

```json
{
  "event_type": "fax.received",
  "fax_id": "provider_fax_id_123",
  "from": "+15551234567",
  "to": "+18005559999",
  "pages": 3,
  "file_url": "https://provider.com/download/..."
}
```

---

## 10. User Interface Specifications

### 10.1 UI Screens

| Screen           | Purpose              | Phase |
| ---------------- | -------------------- | ----- |
| Fax Inbox        | Main fax list view   | 1     |
| Fax Viewer       | View/annotate fax    | 1     |
| Send Fax         | Compose outbound fax | 1     |
| Held Faxes       | Quarantine queue     | 1     |
| Routing Rules    | Rule configuration   | 2     |
| Signature Studio | Signature management | 4     |
| Stamp Designer   | Stamp creation       | 4     |
| Settings         | Module configuration | 1     |
| Dashboard        | Analytics overview   | 3     |
| Number Manager   | DID management       | 1     |

### 10.2 Fax Inbox Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ← Fax Inbox                                    [🔍 Search] [📤 Send Fax]   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filters: [All ▼] [Inbound ▼] [Today ▼] [Category ▼] [Status ▼]            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ☐ │ 📥 │ +1 (555) 123-4567    │ Prescription    │ Nov 26, 2:33 PM │ 3p │ │
│ │   │    │ Dr. Smith Office     │ 🟢 92%          │ @JohnDoe        │    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ☐ │ 📥 │ +1 (555) 987-6543    │ Lab Results     │ Nov 26, 1:15 PM │ 5p │ │
│ │   │    │ Quest Diagnostics    │ 🟢 88%          │ @DrKim          │    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ☐ │ 📤 │ +1 (555) 111-2222    │ Referral        │ Nov 26, 11:00 AM│ 2p │ │
│ │   │    │ Cardiology Assoc.    │ ✅ Sent         │ Me              │    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ☐ │ 📥 │ +1 (800) 555-0000    │ 🚫 Spam         │ Nov 26, 10:30 AM│ 1p │ │
│ │   │    │ Unknown              │ 🔴 Rejected     │ Auto            │    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Showing 1-50 of 234 faxes                              [← Prev] [Next →]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Fax Viewer Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ← Back to Inbox         FAX-2025-00123         [🖨️] [📧] [📠 Return]      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ ┌─────────────────────────────────────┬─────────────────────────────────┐   │
│ │                                     │ Details                         │   │
│ │                                     │ ─────────────────────────────── │   │
│ │                                     │ From: +1 (555) 123-4567        │   │
│ │                                     │ To: +1 (800) 555-9999          │   │
│ │         [PDF VIEWER]                │ Received: Nov 26, 2:33 PM      │   │
│ │                                     │ Pages: 3                        │   │
│ │         Page 1 of 3                 │ Category: Prescription          │   │
│ │                                     │ Confidence: 92%                 │   │
│ │         [◀] [▶]                     │ ─────────────────────────────── │   │
│ │                                     │ Entities                        │   │
│ │         [🔍-] [🔍+]                 │ Patient: John Smith            │   │
│ │                                     │ DOB: 01/15/1980                │   │
│ │                                     │ Drug: Lisinopril 10mg          │   │
│ │                                     │ ─────────────────────────────── │   │
│ │                                     │ Actions                         │   │
│ │                                     │ [✍️ Sign] [📋 Stamp]            │   │
│ │                                     │ [📁 Move] [🗑️ Delete]          │   │
│ └─────────────────────────────────────┴─────────────────────────────────┘   │
│                                                                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Tools: [✍️ Signature] [📋 Stamp] [T Text] [✓ Check] [✏️ Draw]         │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Non-Functional Requirements

### 11.1 Performance

| Metric                          | Target      | Measurement |
| ------------------------------- | ----------- | ----------- |
| Inbound webhook response        | <500ms      | p99         |
| OCR processing (10 pages)       | <8 seconds  | p99         |
| AI classification               | <2 seconds  | p99         |
| Full pipeline (receive → inbox) | <15 seconds | p99         |
| Search query response           | <1 second   | p99         |
| Fax viewer load time            | <2 seconds  | p99         |
| Outbound queue processing       | <5 seconds  | p99         |
| API response time               | <200ms      | p99         |

### 11.2 Scalability

| Dimension                   | Target | Notes         |
| --------------------------- | ------ | ------------- |
| Concurrent faxes processing | 1,000  | Per cluster   |
| Faxes stored                | 100M+  | With archival |
| Users per tenant            | 10,000 |               |
| Organizations               | 1,000  | Multi-tenant  |
| Search index size           | 10TB   | Full-text     |
| API requests/second         | 10,000 |               |

### 11.3 Availability

| Metric                         | Target        |
| ------------------------------ | ------------- |
| Uptime                         | 99.99%        |
| RTO (Recovery Time Objective)  | 15 minutes    |
| RPO (Recovery Point Objective) | 5 minutes     |
| Planned maintenance window     | 4 hours/month |

### 11.4 Reliability

| Metric                     | Target |
| -------------------------- | ------ |
| Fax delivery success rate  | ≥99.9% |
| OCR accuracy               | ≥95%   |
| AI classification accuracy | ≥90%   |
| Spam detection accuracy    | ≥98%   |
| False positive rate (spam) | <1%    |

---

## 12. Security Requirements

### 12.1 Authentication & Authorization

| Requirement         | Implementation        |
| ------------------- | --------------------- |
| User authentication | Keycloak SSO          |
| API authentication  | JWT + API keys        |
| MFA support         | TOTP, WebAuthn        |
| Role-based access   | Frappe permissions    |
| Session management  | Redis with encryption |

### 12.2 Data Protection

| Requirement           | Implementation             |
| --------------------- | -------------------------- |
| Encryption in transit | TLS 1.3                    |
| Encryption at rest    | AES-256-GCM                |
| Key management        | AWS KMS or HashiCorp Vault |
| Data masking          | PHI/PII in logs            |
| Secure deletion       | Cryptographic erasure      |

### 12.3 Network Security

| Requirement     | Implementation            |
| --------------- | ------------------------- |
| WAF             | AWS WAF or Cloudflare     |
| DDoS protection | Cloud provider            |
| Rate limiting   | Per-user, per-API key     |
| IP allowlisting | Optional per organization |

---

## 13. Compliance Requirements

### 13.1 HIPAA (Healthcare)

| Control               | Implementation                     |
| --------------------- | ---------------------------------- |
| Access controls       | RBAC, minimum necessary            |
| Audit controls        | Immutable audit logs               |
| Transmission security | TLS 1.3                            |
| Encryption            | AES-256 at rest                    |
| BAA                   | Template + tracking                |
| PHI handling          | Detection, logging, access control |

### 13.2 SOC 2 Type II

| Trust Principle      | Controls                               |
| -------------------- | -------------------------------------- |
| Security             | Access control, encryption, monitoring |
| Availability         | HA architecture, monitoring, DR        |
| Processing Integrity | Input validation, audit trails         |
| Confidentiality      | Encryption, access control             |
| Privacy              | Data retention, deletion, consent      |

### 13.3 GDPR

| Requirement         | Implementation     |
| ------------------- | ------------------ |
| Data portability    | Export API         |
| Right to erasure    | Deletion workflow  |
| Consent management  | Opt-in tracking    |
| Data minimization   | Retention policies |
| Breach notification | Incident response  |

### 13.4 UETA/ESIGN (Electronic Signatures)

| Requirement      | Implementation               |
| ---------------- | ---------------------------- |
| Intent to sign   | User action required         |
| Consent          | Signature creation = consent |
| Attribution      | User ID, timestamp, IP       |
| Record retention | Immutable storage            |
| Integrity        | Hash + audit trail           |

---

## 14. Integration Requirements

### 14.1 Fax Carriers

| Carrier    | Priority  | Capabilities             |
| ---------- | --------- | ------------------------ |
| Telnyx     | Primary   | Send, receive, provision |
| Bandwidth  | Secondary | Send, receive, provision |
| SignalWire | Tertiary  | Send, receive            |

### 14.2 Notification Services

| Service  | Purpose             |
| -------- | ------------------- |
| Twilio   | SMS notifications   |
| SendGrid | Email notifications |
| FCM/APNs | Push notifications  |

### 14.3 AI/ML Services

| Service           | Purpose                    |
| ----------------- | -------------------------- |
| Tesseract         | Primary OCR                |
| ABBYY             | Fallback OCR (handwriting) |
| AWS SageMaker     | Model hosting              |
| OpenAI (optional) | Advanced NLP               |

### 14.4 Storage Services

| Service    | Purpose                  |
| ---------- | ------------------------ |
| S3/MinIO   | Primary document storage |
| OpenSearch | Search index             |
| Redis      | Cache, queues            |

---

## 15. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)

**Goal:** Basic fax send/receive with manual routing

**Features:**

- Fax Document DocType
- Multi-provider abstraction (Telnyx, Bandwidth)
- Inbound webhook processing
- Outbound queue with retry
- Tier 1 validation (whitelist/blacklist)
- Basic inbox UI
- Send fax form
- DID provisioning
- API authentication
- Audit logging

**Success Criteria:**

- Send and receive faxes
- 99% delivery success
- <30 second inbound processing

### Phase 2: AI & Automation (Months 4-6)

**Goal:** Automated classification and routing

**Features:**

- OCR engine integration
- NLP classification
- Entity extraction
- Spam detection (Tier 2)
- Rule-based routing engine
- Workload balancing
- Full-text search
- Webhook system
- Notifications (email, SMS)
- Shared inboxes
- Cover page designer

**Success Criteria:**

- 90% classification accuracy
- <15 second full pipeline
- Search <1 second

### Phase 3: Security & Compliance (Months 7-9)

**Goal:** Enterprise security and compliance

**Features:**

- Tier 3 challenge verification
- Email-to-fax security
- PHI detection (MedxFax)
- Retention policies
- Legal hold
- Redaction tools
- Certified delivery receipts
- Compliance reports
- HIPAA controls
- Bulk/broadcast fax

**Success Criteria:**

- HIPAA ready
- SOC 2 audit prep
- <1% spam false positive

### Phase 4: Annotation & Mobile (Months 10-12)

**Goal:** Complete annotation and mobile experience

**Features:**

- Signature management
- Stamp designer
- PDF annotation editor
- Return actions (fax, email)
- Mobile app (Flutter)
- Offline capability
- Pre-built integrations
- Form parsing
- Analytics dashboard
- Smart reply

**Success Criteria:**

- <30 second sign and return
- 4.8+ app store rating
- 50+ form templates

---

## 16. Success Metrics

### 16.1 Business Metrics

| Metric             | Target | Timeframe |
| ------------------ | ------ | --------- |
| Paying customers   | 100    | Month 6   |
| Monthly fax volume | 1M     | Month 12  |
| ARR                | $500K  | Month 12  |
| Customer churn     | <5%    | Monthly   |
| NPS                | >50    | Quarterly |

### 16.2 Product Metrics

| Metric                 | Target      |
| ---------------------- | ----------- |
| Automated routing rate | ≥90%        |
| Time to first action   | <60 seconds |
| Sign and return time   | <30 seconds |
| User satisfaction      | 4.5/5       |
| Mobile app rating      | 4.8+        |

### 16.3 Technical Metrics

| Metric                  | Target    |
| ----------------------- | --------- |
| Uptime                  | 99.99%    |
| Delivery success        | 99.9%     |
| OCR accuracy            | 95%       |
| Classification accuracy | 90%       |
| Search latency          | <1 second |
| API latency             | <200ms    |

---

## 17. Risks & Mitigations

| Risk                   | Probability | Impact   | Mitigation                        |
| ---------------------- | ----------- | -------- | --------------------------------- |
| Carrier API changes    | Medium      | High     | Multi-provider abstraction        |
| OCR accuracy issues    | Medium      | Medium   | Multi-engine fallback             |
| Spam evolution         | High        | Medium   | Continuous model training         |
| HIPAA breach           | Low         | Critical | Encryption, access control, audit |
| Scalability bottleneck | Medium      | High     | Horizontal scaling, caching       |
| Mobile app rejection   | Low         | Medium   | Follow platform guidelines        |
| Integration complexity | Medium      | Medium   | Clear API documentation           |

---

## 18. Appendices

### Appendix A: Glossary

| Term  | Definition                                          |
| ----- | --------------------------------------------------- |
| DID   | Direct Inward Dialing - a dedicated fax number      |
| FoIP  | Fax over IP - fax transmission via internet         |
| CSID  | Called Subscriber Identification - sender ID in fax |
| T.38  | ITU standard for fax over IP                        |
| OCR   | Optical Character Recognition                       |
| ICR   | Intelligent Character Recognition (handwriting)     |
| NER   | Named Entity Recognition                            |
| PHI   | Protected Health Information                        |
| BAA   | Business Associate Agreement                        |
| HIPAA | Health Insurance Portability and Accountability Act |
| WORM  | Write Once Read Many storage                        |

### Appendix B: Category Definitions

| Category            | Description             | Typical Routing   |
| ------------------- | ----------------------- | ----------------- |
| Prescription        | Medication orders, Rx   | Pharmacy          |
| Lab Results         | Laboratory test results | Ordering provider |
| Referral            | Patient referrals       | Scheduling        |
| Prior Authorization | Insurance PA requests   | Billing           |
| Medical Records     | Records requests        | HIM department    |
| Invoice             | Bills, invoices         | Accounting        |
| Contract            | Legal agreements        | Legal             |
| Purchase Order      | Procurement             | Purchasing        |
| Resume              | Job applications        | HR                |
| Junk/Spam           | Unsolicited faxes       | Auto-reject       |

### Appendix C: API Error Codes

| Code    | Message           | Description                 |
| ------- | ----------------- | --------------------------- |
| FAX-001 | Invalid recipient | Phone number format invalid |
| FAX-002 | File too large    | Exceeds 50MB limit          |
| FAX-003 | Invalid file type | Not PDF/TIFF/DOC            |
| FAX-004 | Rate limited      | Too many requests           |
| FAX-005 | Unauthorized      | Invalid API key             |
| FAX-006 | Fax not found     | Invalid fax ID              |
| FAX-007 | Carrier error     | Provider API failure        |
| FAX-008 | Validation failed | Sender blocked              |

### Appendix D: Webhook Event Reference

| Event                   | Trigger                | Payload                  |
| ----------------------- | ---------------------- | ------------------------ |
| fax.received            | Inbound fax arrives    | Full fax metadata        |
| fax.processed           | AI processing complete | Classification, entities |
| fax.routed              | Routing decision made  | Assignee, rule           |
| fax.delivered           | Outbound delivered     | Delivery receipt         |
| fax.failed              | Outbound failed        | Error details            |
| fax.annotated           | Annotation saved       | Annotation details       |
| fax.validation.held     | Fax held for review    | Hold reason              |
| fax.validation.released | Held fax released      | Release details          |

---

## Document History

| Version | Date          | Author         | Changes                               |
| ------- | ------------- | -------------- | ------------------------------------- |
| 1.0     | November 2025 | Original       | Initial PRD                           |
| 2.0     | November 2025 | Claude + Brett | Complete rewrite with HIPAA framework |

---

_End of Document_
