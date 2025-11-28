# Dartwing Company Module - Architecture Document

**Version:** 1.0  
**Date:** November 28, 2025  
**Status:** Draft

---

## Section 1: Executive Summary

### 1.1 Architecture Vision

Dartwing Company is an **AI-First Operations Platform** built as an intelligent overlay on the Frappe ecosystem. Rather than reinventing functionality, it leverages and enhances existing Frappe applications:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DARTWING COMPANY                                     │
│                    (AI-First Operations Layer)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  OPS Engine  │  CRM Overlay  │  HR Overlay  │  Healthcare Overlay  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│   DARTWING    │           │   DARTWING    │           │   DARTWING    │
│    FLUTTER    │           │    LEADGEN    │           │     FONE      │
│  (Mobile App) │           │ (Lead Engine) │           │ (Voice/SMS)   │
└───────────────┘           └───────────────┘           └───────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                           FRAPPE ECOSYSTEM                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ ERPNext  │ │  HRMS    │ │   CRM    │ │  Health  │ │  Drive   │       │
│  │          │ │          │ │          │ │          │ │          │       │
│  │•Accounting│ │•Employee │ │•Lead     │ │•Patient  │ │•Files    │       │
│  │•Inventory│ │•Attendance│ │•Deal     │ │•Encounter│ │•Folders  │       │
│  │•Projects │ │•Payroll  │ │•Pipeline │ │•Clinical │ │•Sharing  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      FRAPPE FRAMEWORK                             │   │
│  │  DocTypes │ REST API │ WebSocket │ Background Jobs │ Permissions  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Principles

| Principle                 | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| **Overlay, Don't Extend** | Add functionality on top of Frappe apps; never modify their core |
| **Leverage Existing**     | Use ERPNext/HRMS/CRM DocTypes as data sources, not duplicates    |
| **Link, Don't Copy**      | Reference existing records; avoid data duplication               |
| **Event-Driven**          | React to Frappe doc_events to trigger our logic                  |
| **API-First**             | Every feature accessible via REST for Flutter/external           |
| **AI-Enhanced**           | AI augments every workflow, not a bolt-on                        |

### 1.3 Integration Strategy

| Frappe App    | What We Leverage                       | What We Add                                             |
| ------------- | -------------------------------------- | ------------------------------------------------------- |
| **ERPNext**   | Customer, Sales Invoice, Project, Item | AI dispatch, workflow automation                        |
| **HRMS**      | Employee, Attendance, Shift Assignment | Geo clock-in, shift marketplace, qualification blocking |
| **CRM**       | Lead, Deal, Contact, Communication     | Growth Orchestrator, sentiment analysis, SLA engine     |
| **Health**    | Patient, Encounter, Clinical Procedure | Healthcare workflow integration, PHI handling           |
| **Drive**     | File, Folder                           | Client portal vault, secure sharing, audit              |
| **Framework** | DocType, API, Permissions, Jobs        | All custom logic                                        |

### 1.4 Technology Stack

| Layer        | Technology          | Purpose                   |
| ------------ | ------------------- | ------------------------- |
| **Mobile**   | Dartwing Flutter    | Cross-platform mobile app |
| **Frontend** | Frappe UI + Vue.js  | Web interface             |
| **Backend**  | Frappe Framework    | Application logic         |
| **Database** | MariaDB 10.11+      | Primary data store        |
| **Cache**    | Redis 7.x           | Caching, queues, pub/sub  |
| **Search**   | OpenSearch 2.x      | Full-text + vector search |
| **AI/LLM**   | OpenAI / Claude API | Intent, RAG, summaries    |
| **Voice**    | dartwing_fone       | SIP, SMS, voice AI        |
| **Maps**     | Google Maps API     | Geocoding, routing        |
| **Payments** | Stripe              | Appointment deposits      |

### 1.5 Module Dependencies

```python
# pyproject.toml / setup.py
install_requires = [
    "frappe>=15.0.0",
    "erpnext>=15.0.0",        # Optional but recommended
    "hrms>=15.0.0",           # Optional - for HR features
    "crm>=15.0.0",            # Optional - for CRM overlay
    "health>=15.0.0",         # Optional - for healthcare
    "drive>=1.0.0",           # Optional - for document vault
    "dartwing_core>=1.0.0",   # Required - base module
    "dartwing_leadgen>=1.0.0" # Required - lead generation
]

optional_requires = {
    "voice": ["dartwing_fone>=1.0.0"],
    "ai": ["openai>=1.0.0", "langchain>=0.1.0"]
}
```

---

**Next: Section 2 - System Architecture**

# Dartwing Company Architecture - Section 2: System Architecture

---

## 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Frappe Desk    │  │ Client Portal  │  │ Dartwing       │                │
│  │ (Admin/Staff)  │  │ (Customers)    │  │ Flutter App    │                │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                │
└──────────┼───────────────────┼───────────────────┼──────────────────────────┘
           │                   │                   │
           └───────────────────┴───────────────────┘
                               │
                     REST API + WebSocket
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                         APPLICATION LAYER                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      DARTWING COMPANY MODULE                            │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │ OPERATIONS CORE                                                   │  │ │
│  │  │ • Receptionist • Inbox • Workflow • Dispatch • Forms • Knowledge │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │ CRM OVERLAY (on Frappe CRM)                                       │  │ │
│  │  │ • Portal • Appointments • Tickets • SLA • Growth Orchestrator    │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │ HR OVERLAY (on HRMS)                                              │  │ │
│  │  │ • Shift Scheduler • Geo Clock-In • Swap Marketplace              │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │ HEALTHCARE OVERLAY (on Frappe Health)                             │  │ │
│  │  │ • Patient Workflows • Clinical Forms • Encounter Integration     │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │dartwing_core │ │dartwing_fone │ │dartwing_     │ │ frappe_drive │       │
│  │              │ │              │ │ leadgen      │ │              │       │
│  │• Organization│ │• Voice/SIP   │ │• Search      │ │• File Mgmt   │       │
│  │• Person      │ │• SMS         │ │• Enrich      │ │• Sharing     │       │
│  │• Settings    │ │• AI Voice    │ │• Match       │ │• Audit       │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   ERPNext    │ │    HRMS      │ │  Frappe CRM  │ │Frappe Health │       │
│  │              │ │              │ │              │ │              │       │
│  │• Customer    │ │• Employee    │ │• Lead        │ │• Patient     │       │
│  │• Invoice     │ │• Attendance  │ │• Deal        │ │• Encounter   │       │
│  │• Project     │ │• Shift       │ │• Contact     │ │• Procedure   │       │
│  │• Item        │ │• Payroll     │ │• Communication│ │• Medication │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        FRAPPE FRAMEWORK                                 │ │
│  │  DocTypes │ REST API │ Permissions │ Scheduler │ WebSocket │ Hooks     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                           DATA LAYER                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   MariaDB    │ │    Redis     │ │  OpenSearch  │ │   S3/MinIO   │       │
│  │              │ │              │ │              │ │              │       │
│  │• DocTypes    │ │• Cache       │ │• Full-text   │ │• Files       │       │
│  │• Relations   │ │• Queues      │ │• Vectors     │ │• Attachments │       │
│  │• Transactions│ │• Pub/Sub     │ │• Analytics   │ │• Backups     │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└──────────────────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  AI/LLM API  │ │  Maps API    │ │   Stripe     │ │  Calendar    │       │
│  │ OpenAI/Claude│ │Google/Mapbox │ │  Payments    │ │Google/Outlook│       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.2 Integration Architecture

### 2.2.1 ERPNext Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERPNEXT INTEGRATION                           │
└─────────────────────────────────────────────────────────────────┘

dartwing_company                          ERPNext
================                          =======

┌──────────────────┐                  ┌──────────────────┐
│ Dispatch Job     │───references────▶│ Customer         │
│                  │                  │ • customer_name  │
│ • customer (Link)│                  │ • territory      │
│ • address (Link) │───references────▶│ • customer_group │
│ • items (Table)  │───references────▶│ Address          │
└──────────────────┘                  │ Item             │
                                      └──────────────────┘
        │
        │ on_complete
        ▼
┌──────────────────┐                  ┌──────────────────┐
│ Create           │────creates──────▶│ Sales Invoice    │
│ Invoice Action   │                  │ Delivery Note    │
└──────────────────┘                  │ Timesheet        │
                                      └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Client Portal    │────reads────────▶│ Sales Invoice    │
│ Invoice Widget   │                  │ Payment Entry    │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Workflow Engine  │────references───▶│ Project          │
│ Project Actions  │                  │ Task             │
└──────────────────┘                  └──────────────────┘
```

### 2.2.2 HRMS Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                      HRMS INTEGRATION                            │
└─────────────────────────────────────────────────────────────────┘

dartwing_company                          HRMS
================                          ====

┌──────────────────┐                  ┌──────────────────┐
│ Schedule Entry   │───syncs to──────▶│ Shift Assignment │
│                  │                  │                  │
│ • employee       │───references────▶│ Employee         │
│ • shift_template │                  │ Shift Type       │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Geo Clock-In     │───creates───────▶│ Attendance       │
│                  │                  │                  │
│ • employee       │                  │ • employee       │
│ • in_time        │                  │ • attendance_date│
│ • location       │                  │ • in_time        │
│ • validation     │                  │ • out_time       │
└──────────────────┘                  └──────────────────┘
        │
        │ extends
        ▼
┌──────────────────┐
│ Attendance       │ (Child Table or Custom Fields)
│ Extension        │
│                  │
│ • clock_in_gps   │
│ • clock_out_gps  │
│ • validation_type│
│ • photos         │
└──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Employee         │───references────▶│ Employee         │
│ Certification    │                  │                  │
│                  │                  │ (via Custom Field│
│ • certification  │                  │  or Link)        │
│ • expiry_date    │                  │                  │
└──────────────────┘                  └──────────────────┘
```

### 2.2.3 Frappe CRM Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAPPE CRM INTEGRATION                        │
└─────────────────────────────────────────────────────────────────┘

dartwing_company                          Frappe CRM
================                          ==========

┌──────────────────┐                  ┌──────────────────┐
│ Growth           │───creates───────▶│ Lead             │
│ Orchestrator     │                  │                  │
│                  │                  │ • source         │
│ • campaign       │                  │ • campaign_name  │
│ • icp_score      │                  │ • custom_data    │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Service Ticket   │───extends───────▶│ Issue            │
│ (Overlay)        │                  │ (if ERPNext)     │
│                  │                  │                  │
│ • sla_policy     │                  │ OR               │
│ • sentiment      │                  │                  │
│ • escalation     │                  │ CRM Ticket       │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Universal Inbox  │───reads/writes──▶│ Communication    │
│                  │                  │                  │
│ • conversation   │◀──linked to──────│ • reference_doctype
│ • messages       │                  │ • reference_name │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Appointment      │───references────▶│ Contact          │
│                  │                  │ Lead             │
│ • contact        │                  │ Deal             │
│ • deal           │                  │                  │
└──────────────────┘                  └──────────────────┘

EVENT HOOKS:
┌──────────────────┐
│ Lead.after_insert│──────────────────▶ Track in Campaign
│ Deal.on_update   │──────────────────▶ Update Campaign ROI
│ Communication    │──────────────────▶ Add to Conversation
│   .after_insert  │
└──────────────────┘
```

### 2.2.4 Frappe Health Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                  FRAPPE HEALTH INTEGRATION                       │
└─────────────────────────────────────────────────────────────────┘

dartwing_company                          Frappe Health
================                          =============

┌──────────────────┐                  ┌──────────────────┐
│ Appointment      │───references────▶│ Patient          │
│ (Healthcare Mode)│                  │ Healthcare       │
│                  │                  │ Practitioner     │
│ • patient        │                  │                  │
│ • practitioner   │                  │ Patient          │
│ • encounter_type │                  │ Appointment      │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Clinical Form    │───creates───────▶│ Patient Encounter│
│ Submission       │                  │                  │
│                  │                  │ Clinical         │
│ • patient        │                  │ Procedure        │
│ • vitals         │                  │                  │
│ • observations   │                  │ Vital Signs      │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Client Portal    │───reads (PHI)───▶│ Patient          │
│ Patient View     │                  │ Lab Test         │
│                  │                  │ Prescription     │
│ (HIPAA controls) │                  │                  │
└──────────────────┘                  └──────────────────┘
```

### 2.2.5 Frappe Drive Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                   FRAPPE DRIVE INTEGRATION                       │
└─────────────────────────────────────────────────────────────────┘

dartwing_company                          Frappe Drive
================                          ============

┌──────────────────┐                  ┌──────────────────┐
│ Document Vault   │───uses──────────▶│ Drive Folder     │
│                  │                  │ Drive File       │
│ • Per-customer   │                  │                  │
│   folders        │                  │ • File storage   │
│ • Access control │                  │ • Versioning     │
│ • Audit logging  │                  │ • Thumbnails     │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐                  ┌──────────────────┐
│ Portal File      │───wraps─────────▶│ Drive Entity     │
│ Share            │                  │ Share            │
│                  │                  │                  │
│ • expiry_date    │                  │ • share_link     │
│ • password       │                  │ • permissions    │
│ • download_count │                  │                  │
└──────────────────┘                  └──────────────────┘

┌──────────────────┐
│ File Audit Log   │ (Our addition)
│                  │
│ • file           │
│ • action         │
│ • user           │
│ • timestamp      │
│ • ip_address     │
└──────────────────┘
```

---

## 2.3 Data Flow Diagrams

### 2.3.1 Inbound Communication Flow

```
External Channel (Email/SMS/Voice/WhatsApp)
        │
        ▼
┌───────────────────┐
│ dartwing_fone     │ (Voice/SMS)
│ Channel Webhook   │ (Email IMAP, WhatsApp API)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Channel Router    │ Normalize message format
│ (dartwing_company)│
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Contact Matcher   │ Match to Contact/Lead/Customer
│                   │ (Query Frappe CRM + ERPNext)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Conversation      │ Create or update Conversation
│ Manager           │ Add message to thread
└─────────┬─────────┘
          │
          ├──────────────────────┐
          │                      │
          ▼                      ▼
┌───────────────────┐  ┌───────────────────┐
│ Frappe CRM        │  │ AI Analysis       │
│ Communication     │  │ • Sentiment       │
│ (linked)          │  │ • Intent          │
└───────────────────┘  │ • Suggested reply │
                       └─────────┬─────────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │ Route/Assign      │
                       │ Notify user       │
                       └───────────────────┘
```

### 2.3.2 Dispatch Job Flow

```
Job Request (Portal/API/Manual)
        │
        ▼
┌───────────────────┐
│ Create Dispatch   │ Link to Customer (ERPNext)
│ Job               │ Link to Address (ERPNext)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ GIS Service       │ Geocode address
│ (Google Maps)     │ Calculate geohash
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Smart Assignment  │ Query Employee (HRMS)
│ Engine            │ Check skills/certs
│                   │ Check availability (HRMS Attendance)
│                   │ Calculate drive time
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Assign to         │ Update Job status
│ Technician        │ Notify via dartwing_fone
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Mobile App        │ Tech receives job
│ (Flutter)         │ Navigation, forms
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Job Completion    │ Form submission
│                   │ Customer signature
└─────────┬─────────┘
          │
          ├─────────────────┬─────────────────┐
          ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ ERPNext       │  │ HRMS          │  │ Frappe CRM    │
│ Sales Invoice │  │ Timesheet     │  │ Activity Log  │
│ Delivery Note │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## 2.4 Multi-Tenancy Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-TENANCY MODEL                           │
└─────────────────────────────────────────────────────────────────┘

Organization (dartwing_core)
│
├── Company Settings (dartwing_company)
│   ├── Features enabled/disabled
│   ├── Branding (portal)
│   └── Integration configs
│
├── ERPNext Company ←─────────────── Linked 1:1
│   ├── Customers
│   ├── Invoices
│   └── Projects
│
├── HRMS Company ←──────────────────── Linked 1:1
│   ├── Employees
│   ├── Attendance
│   └── Shifts
│
├── dartwing_company DocTypes (org-scoped)
│   ├── Conversations
│   ├── Dispatch Jobs
│   ├── Workflows
│   ├── Appointments
│   ├── Campaigns
│   └── ...
│
└── Users (via Organization Member)
    ├── Roles determine feature access
    └── Portal users (client access)
```

All queries automatically filtered by organization:

```python
# Permission query for org-scoped DocTypes
def get_permission_query_conditions(user):
    org = get_user_organization(user)
    if not org:
        return "1=0"  # No access
    return f"`tabDispatch Job`.organization = '{org}'"
```

---

**Next: Section 3 - Module Structure**

# Dartwing Company Architecture - Section 3: Module Structure

---

## 3.1 Directory Structure

```
apps/dartwing/dartwing/dartwing_company/
│
├── __init__.py
├── hooks.py
├── patches/
│
├── doctype/                              # Frappe DocTypes
│   │
│   ├── # ─────────────── CONFIGURATION ───────────────
│   ├── company_settings/                 # Per-org settings
│   ├── feature_flag/                     # Feature toggles
│   │
│   ├── # ─────────────── OPERATIONS CORE ─────────────
│   ├── conversation/                     # OPS-02 Universal Inbox
│   ├── conversation_message/             # Child: messages
│   ├── conversation_note/                # Child: internal notes
│   ├── workflow_template/                # OPS-03 Workflow Builder
│   ├── workflow_step/                    # Child: workflow steps
│   ├── workflow_instance/                # Running workflow
│   ├── dispatch_job/                     # OPS-04 Dispatch
│   ├── dispatch_assignment/              # Assignment history
│   ├── mobile_form/                      # OPS-05 Form Builder
│   ├── form_field/                       # Child: form fields
│   ├── form_submission/                  # Submitted form data
│   ├── knowledge_article/                # OPS-07 Knowledge Base
│   ├── knowledge_category/               # Article categories
│   ├── broadcast_alert/                  # OPS-08 Alerts
│   ├── broadcast_recipient/              # Child: recipients
│   ├── visitor_log/                      # OPS-10 Visitor Mgmt
│   ├── resource/                         # OPS-11 Bookable assets
│   ├── resource_booking/                 # Reservations
│   │
│   ├── # ─────────────── CRM OVERLAY ─────────────────
│   ├── portal_settings/                  # CRM-01 Portal config
│   ├── view_set/                         # Widget configuration
│   ├── view_set_widget/                  # Child: widgets
│   ├── document_vault/                   # CRM-02 File container
│   ├── vault_folder/                     # Folder structure
│   ├── vault_share/                      # Share links
│   ├── vault_audit_log/                  # Access audit
│   ├── appointment_type/                 # CRM-03 Appointment config
│   ├── appointment/                      # Booked appointments
│   ├── service_ticket/                   # CRM-04 Support tickets
│   ├── ticket_escalation/                # Escalation history
│   ├── sla_policy/                       # CRM-06 SLA rules
│   ├── sla_policy_rule/                  # Child: SLA rules
│   ├── custom_field_schema/              # CRM-05 Dynamic fields
│   ├── campaign/                         # CRM-07 Lead gen campaigns
│   ├── campaign_persona/                 # Child: target personas
│   │
│   ├── # ─────────────── HR OVERLAY ──────────────────
│   ├── shift_template/                   # HR-01 Shift definitions
│   ├── schedule_entry/                   # Schedule assignments
│   ├── shift_swap_request/               # Swap marketplace
│   ├── work_location/                    # Geofenced locations
│   ├── employee_certification/           # Certifications
│   ├── certification_type/               # Cert types
│   └── attendance_extension/             # HR-02 Extra attendance data
│
├── overrides/                            # DocType method overrides
│   ├── __init__.py
│   ├── customer.py                       # ERPNext Customer extensions
│   ├── employee.py                       # HRMS Employee extensions
│   ├── lead.py                           # CRM Lead extensions
│   ├── attendance.py                     # HRMS Attendance extensions
│   └── communication.py                  # CRM Communication extensions
│
├── operations/                           # OPS Feature Engines
│   ├── __init__.py
│   ├── receptionist/
│   │   ├── __init__.py
│   │   ├── call_handler.py               # SIP call handling
│   │   ├── intent_classifier.py          # AI intent detection
│   │   ├── router.py                     # Call routing logic
│   │   └── whisper.py                    # Agent whisper
│   ├── inbox/
│   │   ├── __init__.py
│   │   ├── aggregator.py                 # Channel aggregation
│   │   ├── session_manager.py            # Conversation sessions
│   │   └── channels/
│   │       ├── __init__.py
│   │       ├── base.py                   # Base channel class
│   │       ├── email.py                  # IMAP/SMTP
│   │       ├── sms.py                    # via dartwing_fone
│   │       ├── voice.py                  # via dartwing_fone
│   │       ├── whatsapp.py               # WhatsApp Business API
│   │       ├── messenger.py              # Facebook Messenger
│   │       └── telegram.py               # Telegram Bot API
│   ├── workflow/
│   │   ├── __init__.py
│   │   ├── engine.py                     # Workflow executor
│   │   ├── builder.py                    # Visual builder backend
│   │   ├── actions.py                    # Built-in actions
│   │   └── external_sync/
│   │       ├── __init__.py
│   │       ├── planner.py                # Microsoft Planner
│   │       └── trello.py                 # Trello
│   ├── dispatch/
│   │   ├── __init__.py
│   │   ├── engine.py                     # Dispatch orchestration
│   │   ├── geo_service.py                # Geocoding, routing
│   │   ├── optimizer.py                  # Route optimization
│   │   └── assignment.py                 # Smart assignment
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── builder.py                    # Form schema builder
│   │   ├── renderer.py                   # Form rendering
│   │   └── validator.py                  # Submission validation
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── rag_engine.py                 # RAG Q&A
│   │   ├── indexer.py                    # Content indexing
│   │   └── embeddings.py                 # Vector embeddings
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── broadcaster.py                # Mass notifications
│   └── search/
│       ├── __init__.py
│       └── global_search.py              # Ask Anything engine
│
├── crm/                                  # CRM Overlay Engines
│   ├── __init__.py
│   ├── portal/
│   │   ├── __init__.py
│   │   ├── auth.py                       # Portal authentication
│   │   ├── views.py                      # Portal page controllers
│   │   └── widgets.py                    # Dashboard widgets
│   ├── appointments/
│   │   ├── __init__.py
│   │   ├── scheduler.py                  # Availability/booking
│   │   ├── availability.py               # Slot calculation
│   │   └── payments.py                   # Stripe integration
│   ├── tickets/
│   │   ├── __init__.py
│   │   ├── router.py                     # Ticket routing
│   │   ├── sentiment.py                  # Sentiment analysis
│   │   └── sla_engine.py                 # SLA tracking
│   ├── vault/
│   │   ├── __init__.py
│   │   ├── manager.py                    # Vault operations
│   │   └── drive_bridge.py               # Frappe Drive integration
│   └── growth/
│       ├── __init__.py
│       ├── orchestrator.py               # Growth Orchestrator AI
│       ├── interview_agent.py            # ICP interview
│       └── lead_creator.py               # Lead creation
│
├── hr/                                   # HR Overlay Engines
│   ├── __init__.py
│   ├── scheduling/
│   │   ├── __init__.py
│   │   ├── builder.py                    # Schedule builder
│   │   ├── swap_marketplace.py           # Shift swaps
│   │   ├── qualifications.py             # Cert checking
│   │   └── hrms_sync.py                  # Sync to HRMS
│   └── attendance/
│       ├── __init__.py
│       ├── clock_manager.py              # Clock in/out
│       ├── geofence.py                   # Location validation
│       ├── anomaly_detector.py           # Anomaly detection
│       └── hrms_sync.py                  # Sync to HRMS Attendance
│
├── healthcare/                           # Healthcare Overlay
│   ├── __init__.py
│   ├── patient_portal.py                 # Patient-specific portal
│   ├── clinical_forms.py                 # Healthcare forms
│   └── health_bridge.py                  # Frappe Health integration
│
├── integrations/                         # External Service Clients
│   ├── __init__.py
│   ├── leadgen_client.py                 # dartwing_leadgen API
│   ├── fone_client.py                    # dartwing_fone API
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py                 # OpenAI/Claude wrapper
│   │   ├── embeddings.py                 # Embedding service
│   │   └── prompts.py                    # Prompt templates
│   ├── calendar/
│   │   ├── __init__.py
│   │   ├── google.py                     # Google Calendar
│   │   └── outlook.py                    # Microsoft Graph
│   ├── maps/
│   │   ├── __init__.py
│   │   └── google_maps.py                # Geocoding, directions
│   └── payments/
│       ├── __init__.py
│       └── stripe.py                     # Stripe payments
│
├── api/                                  # REST API Endpoints
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── conversations.py              # Inbox API
│   │   ├── dispatch.py                   # Dispatch API
│   │   ├── forms.py                      # Forms API
│   │   ├── appointments.py               # Appointments API
│   │   ├── tickets.py                    # Tickets API
│   │   ├── campaigns.py                  # Campaigns API
│   │   ├── knowledge.py                  # Knowledge API
│   │   ├── schedule.py                   # Scheduling API
│   │   ├── attendance.py                 # Attendance API
│   │   └── search.py                     # Global search API
│   └── webhooks/
│       ├── __init__.py
│       ├── fone.py                       # dartwing_fone webhooks
│       ├── leadgen.py                    # dartwing_leadgen webhooks
│       ├── stripe.py                     # Stripe webhooks
│       └── channels.py                   # Channel webhooks
│
├── portal/                               # Client Portal
│   ├── www/
│   │   └── portal/
│   │       ├── index.html
│   │       ├── index.py
│   │       ├── dashboard.html
│   │       ├── invoices.html
│   │       ├── projects.html
│   │       ├── documents.html
│   │       ├── tickets.html
│   │       ├── appointments.html
│   │       └── messages.html
│   └── templates/
│       ├── portal_base.html
│       └── widgets/
│
├── flutter/                              # Flutter Integration
│   ├── __init__.py
│   ├── api_schema.py                     # API response schemas
│   ├── push_notifications.py             # FCM integration
│   └── offline_sync.py                   # Sync protocol
│
├── tasks/                                # Background Jobs
│   ├── __init__.py
│   ├── inbox_sync.py                     # Channel sync
│   ├── sla_monitor.py                    # SLA checking
│   ├── standup_generator.py              # Daily standup
│   ├── schedule_publisher.py             # Publish schedules
│   ├── attendance_anomalies.py           # Anomaly detection
│   ├── campaign_sync.py                  # LeadGen sync
│   ├── calendar_sync.py                  # External calendar sync
│   └── cleanup.py                        # Data cleanup
│
├── events/                               # Doc Event Handlers
│   ├── __init__.py
│   ├── conversation.py
│   ├── dispatch_job.py
│   ├── appointment.py
│   ├── service_ticket.py
│   ├── schedule_entry.py
│   ├── crm_events.py                     # CRM Lead/Deal events
│   └── erpnext_events.py                 # ERPNext events
│
├── utils/
│   ├── __init__.py
│   ├── phone.py                          # Phone number handling
│   ├── geo.py                            # Geo utilities
│   ├── encryption.py                     # Data encryption
│   └── validators.py                     # Common validators
│
├── templates/
│   ├── emails/
│   └── notifications/
│
├── public/
│   ├── js/
│   ├── css/
│   └── images/
│
├── fixtures/
│   └── custom_field.json                 # Custom fields on Frappe apps
│
└── tests/
    ├── test_operations.py
    ├── test_crm.py
    ├── test_hr.py
    └── test_integrations.py
```

---

## 3.2 hooks.py Configuration

```python
# dartwing_company/hooks.py

app_name = "dartwing_company"
app_title = "Dartwing Company"
app_version = "1.0.0"
app_publisher = "Dartwing"
app_description = "AI-First Operations Platform"
app_license = "MIT"

required_apps = ["frappe", "dartwing_core", "dartwing_leadgen"]

# ─────────────────────────────────────────────────────────────────
# DocType Events - React to changes in our and Frappe app DocTypes
# ─────────────────────────────────────────────────────────────────

doc_events = {
    # Our DocTypes
    "Conversation": {
        "after_insert": "dartwing_company.events.conversation.after_insert",
        "on_update": "dartwing_company.events.conversation.on_update"
    },
    "Dispatch Job": {
        "validate": "dartwing_company.events.dispatch_job.validate",
        "after_insert": "dartwing_company.events.dispatch_job.after_insert",
        "on_update": "dartwing_company.events.dispatch_job.on_update"
    },
    "Appointment": {
        "validate": "dartwing_company.events.appointment.validate",
        "after_insert": "dartwing_company.events.appointment.after_insert"
    },
    "Service Ticket": {
        "after_insert": "dartwing_company.events.service_ticket.after_insert",
        "on_update": "dartwing_company.events.service_ticket.on_update"
    },
    "Schedule Entry": {
        "after_insert": "dartwing_company.events.schedule_entry.sync_to_hrms",
        "on_update": "dartwing_company.events.schedule_entry.sync_to_hrms",
        "on_trash": "dartwing_company.events.schedule_entry.remove_from_hrms"
    },
    "Campaign": {
        "on_update": "dartwing_company.events.campaign.on_update"
    },

    # Frappe CRM DocTypes
    "Lead": {
        "after_insert": "dartwing_company.events.crm_events.on_lead_create",
        "on_update": "dartwing_company.events.crm_events.on_lead_update"
    },
    "Deal": {
        "on_update": "dartwing_company.events.crm_events.on_deal_update"
    },
    "Communication": {
        "after_insert": "dartwing_company.events.crm_events.on_communication"
    },

    # ERPNext DocTypes
    "Customer": {
        "after_insert": "dartwing_company.events.erpnext_events.on_customer_create"
    },
    "Sales Invoice": {
        "on_submit": "dartwing_company.events.erpnext_events.on_invoice_submit"
    },

    # HRMS DocTypes
    "Attendance": {
        "validate": "dartwing_company.events.hrms_events.validate_attendance"
    },
    "Employee": {
        "on_update": "dartwing_company.events.hrms_events.on_employee_update"
    }
}

# ─────────────────────────────────────────────────────────────────
# Scheduled Tasks
# ─────────────────────────────────────────────────────────────────

scheduler_events = {
    "cron": {
        # Every minute
        "* * * * *": [
            "dartwing_company.tasks.inbox_sync.sync_all_channels",
            "dartwing_company.tasks.sla_monitor.check_sla_breaches"
        ],
        # Every 5 minutes
        "*/5 * * * *": [
            "dartwing_company.tasks.attendance_anomalies.detect"
        ],
        # Every 15 minutes
        "*/15 * * * *": [
            "dartwing_company.tasks.campaign_sync.sync_pending_jobs"
        ],
        # Every hour
        "0 * * * *": [
            "dartwing_company.tasks.calendar_sync.sync_all",
            "dartwing_company.tasks.certification_alerts.check_expiring"
        ],
        # Daily at 6 AM
        "0 6 * * *": [
            "dartwing_company.tasks.standup_generator.generate_all"
        ],
        # Daily at midnight
        "0 0 * * *": [
            "dartwing_company.tasks.schedule_publisher.publish_upcoming",
            "dartwing_company.tasks.cleanup.archive_old_conversations"
        ],
        # Weekly on Sunday
        "0 2 * * 0": [
            "dartwing_company.tasks.cleanup.purge_expired_shares"
        ]
    }
}

# ─────────────────────────────────────────────────────────────────
# Permission Queries (Multi-tenancy)
# ─────────────────────────────────────────────────────────────────

permission_query_conditions = {
    "Conversation": "dartwing_company.permissions.get_org_condition",
    "Dispatch Job": "dartwing_company.permissions.get_org_condition",
    "Appointment": "dartwing_company.permissions.get_org_condition",
    "Service Ticket": "dartwing_company.permissions.get_org_condition",
    "Campaign": "dartwing_company.permissions.get_org_condition",
    "Schedule Entry": "dartwing_company.permissions.get_org_condition",
    "Knowledge Article": "dartwing_company.permissions.get_org_condition",
    "Mobile Form": "dartwing_company.permissions.get_org_condition"
}

has_permission = {
    "Conversation": "dartwing_company.permissions.has_org_permission",
    "Dispatch Job": "dartwing_company.permissions.has_org_permission",
    "Document Vault": "dartwing_company.permissions.has_vault_permission"
}

# ─────────────────────────────────────────────────────────────────
# Website / Portal
# ─────────────────────────────────────────────────────────────────

website_route_rules = [
    {"from_route": "/portal/<path:page>", "to_route": "portal"}
]

# Portal pages
web_include_css = ["/assets/dartwing_company/css/portal.css"]
web_include_js = ["/assets/dartwing_company/js/portal.js"]

# ─────────────────────────────────────────────────────────────────
# Jinja Methods
# ─────────────────────────────────────────────────────────────────

jinja = {
    "methods": [
        "dartwing_company.utils.jinja.get_portal_settings",
        "dartwing_company.utils.jinja.get_view_set_widgets"
    ]
}

# ─────────────────────────────────────────────────────────────────
# DocType Class Overrides
# ─────────────────────────────────────────────────────────────────

override_doctype_class = {
    "Customer": "dartwing_company.overrides.customer.CustomCustomer",
    "Employee": "dartwing_company.overrides.employee.CustomEmployee",
    "Lead": "dartwing_company.overrides.lead.CustomLead",
    "Attendance": "dartwing_company.overrides.attendance.CustomAttendance"
}

# ─────────────────────────────────────────────────────────────────
# Fixtures (Custom Fields on Frappe Apps)
# ─────────────────────────────────────────────────────────────────

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["module", "=", "Dartwing Company"]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            ["module", "=", "Dartwing Company"]
        ]
    }
]

# ─────────────────────────────────────────────────────────────────
# After Migrate Hook
# ─────────────────────────────────────────────────────────────────

after_migrate = [
    "dartwing_company.setup.after_migrate"
]
```

---

## 3.3 Custom Fields on Frappe Apps

```python
# fixtures/custom_field.json (excerpt)

[
    # ─────── ERPNext Customer ───────
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "dartwing_section",
        "fieldtype": "Section Break",
        "label": "Dartwing Company",
        "insert_after": "default_currency"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "portal_enabled",
        "fieldtype": "Check",
        "label": "Portal Access Enabled",
        "insert_after": "dartwing_section"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "view_set",
        "fieldtype": "Link",
        "options": "View Set",
        "label": "Portal View Set",
        "insert_after": "portal_enabled"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "document_vault",
        "fieldtype": "Link",
        "options": "Document Vault",
        "label": "Document Vault",
        "insert_after": "view_set"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_data",
        "fieldtype": "JSON",
        "label": "Custom Fields Data",
        "insert_after": "document_vault"
    },

    # ─────── HRMS Employee ───────
    {
        "doctype": "Custom Field",
        "dt": "Employee",
        "fieldname": "dartwing_section",
        "fieldtype": "Section Break",
        "label": "Dartwing Company",
        "insert_after": "attendance_device_id"
    },
    {
        "doctype": "Custom Field",
        "dt": "Employee",
        "fieldname": "skills",
        "fieldtype": "Table MultiSelect",
        "options": "Employee Skill",
        "label": "Skills",
        "insert_after": "dartwing_section"
    },
    {
        "doctype": "Custom Field",
        "dt": "Employee",
        "fieldname": "home_location",
        "fieldtype": "Link",
        "options": "Work Location",
        "label": "Home Work Location",
        "insert_after": "skills"
    },
    {
        "doctype": "Custom Field",
        "dt": "Employee",
        "fieldname": "dispatch_enabled",
        "fieldtype": "Check",
        "label": "Available for Dispatch",
        "insert_after": "home_location"
    },

    # ─────── HRMS Attendance ───────
    {
        "doctype": "Custom Field",
        "dt": "Attendance",
        "fieldname": "dartwing_section",
        "fieldtype": "Section Break",
        "label": "Dartwing Attendance",
        "insert_after": "shift"
    },
    {
        "doctype": "Custom Field",
        "dt": "Attendance",
        "fieldname": "clock_in_location",
        "fieldtype": "Geolocation",
        "label": "Clock In Location",
        "insert_after": "dartwing_section"
    },
    {
        "doctype": "Custom Field",
        "dt": "Attendance",
        "fieldname": "clock_out_location",
        "fieldtype": "Geolocation",
        "label": "Clock Out Location",
        "insert_after": "clock_in_location"
    },
    {
        "doctype": "Custom Field",
        "dt": "Attendance",
        "fieldname": "validation_method",
        "fieldtype": "Select",
        "options": "GPS\nWiFi\nQR Code\nManual",
        "label": "Validation Method",
        "insert_after": "clock_out_location"
    },
    {
        "doctype": "Custom Field",
        "dt": "Attendance",
        "fieldname": "validation_status",
        "fieldtype": "Select",
        "options": "Verified\nFlagged\nOverridden",
        "label": "Validation Status",
        "insert_after": "validation_method"
    },

    # ─────── Frappe CRM Lead ───────
    {
        "doctype": "Custom Field",
        "dt": "Lead",
        "fieldname": "dartwing_section",
        "fieldtype": "Section Break",
        "label": "Dartwing Growth",
        "insert_after": "notes"
    },
    {
        "doctype": "Custom Field",
        "dt": "Lead",
        "fieldname": "leadgen_source",
        "fieldtype": "Data",
        "label": "LeadGen Source",
        "insert_after": "dartwing_section",
        "read_only": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Lead",
        "fieldname": "icp_score",
        "fieldtype": "Int",
        "label": "ICP Score",
        "insert_after": "leadgen_source"
    },
    {
        "doctype": "Custom Field",
        "dt": "Lead",
        "fieldname": "campaign",
        "fieldtype": "Link",
        "options": "Campaign",
        "label": "Dartwing Campaign",
        "insert_after": "icp_score"
    }
]
```

---

**Next: Section 4 - DocType Architecture**

# Dartwing Company Architecture - Section 4: DocType Architecture

---

## 4.1 DocType Categorization

### Our DocTypes (New)

| Category        | DocType                | Purpose              |
| --------------- | ---------------------- | -------------------- |
| **Operations**  | Conversation           | Unified inbox thread |
|                 | Dispatch Job           | Field job assignment |
|                 | Mobile Form            | Custom form schema   |
|                 | Form Submission        | Completed forms      |
|                 | Knowledge Article      | Wiki/SOP content     |
|                 | Workflow Template      | Automation rules     |
|                 | Broadcast Alert        | Mass notifications   |
|                 | Resource               | Bookable assets      |
|                 | Resource Booking       | Reservations         |
|                 | Visitor Log            | Guest check-in       |
| **CRM Overlay** | Portal Settings        | Portal configuration |
|                 | View Set               | Widget configuration |
|                 | Document Vault         | File container       |
|                 | Appointment            | Scheduled meetings   |
|                 | Appointment Type       | Appointment config   |
|                 | Service Ticket         | Support tickets      |
|                 | SLA Policy             | Response rules       |
|                 | Campaign               | Lead gen campaigns   |
| **HR Overlay**  | Shift Template         | Shift definitions    |
|                 | Schedule Entry         | Schedule assignments |
|                 | Shift Swap Request     | Swap marketplace     |
|                 | Work Location          | Geofenced locations  |
|                 | Employee Certification | Certifications       |

### Frappe App DocTypes (We Link To)

| App               | DocType           | How We Use It             |
| ----------------- | ----------------- | ------------------------- |
| **ERPNext**       | Customer          | Link from jobs, portal    |
|                   | Contact           | Link from conversations   |
|                   | Address           | Link from dispatch jobs   |
|                   | Sales Invoice     | Display in portal         |
|                   | Project           | Link from workflows       |
|                   | Item              | Service items             |
| **HRMS**          | Employee          | Link from schedules, jobs |
|                   | Attendance        | Sync clock-in data        |
|                   | Shift Assignment  | Sync schedule             |
|                   | Shift Type        | Reference for templates   |
| **Frappe CRM**    | Lead              | Create from campaigns     |
|                   | Deal              | Track conversions         |
|                   | Communication     | Link to conversations     |
| **Frappe Health** | Patient           | Healthcare portal         |
|                   | Patient Encounter | Clinical forms            |
| **Frappe Drive**  | Drive Folder      | Vault storage             |
|                   | Drive File        | Document storage          |

---

## 4.2 Core DocType Schemas

### Conversation (Universal Inbox)

```
Conversation
├── name (autoname: CONV-.YYYY.-.#####)
├── organization (Link → Organization) [dartwing_core]
│
├── # Contact Identification (links to Frappe Apps)
├── contact (Link → Contact) [ERPNext/CRM]
├── lead (Link → Lead) [Frappe CRM]
├── customer (Link → Customer) [ERPNext]
├── patient (Link → Patient) [Frappe Health] (if healthcare mode)
│
├── # Conversation Meta
├── channel (Select: email/sms/voice/whatsapp/messenger/telegram)
├── subject (Data)
├── status (Select: open/pending/resolved/closed)
├── priority (Select: low/normal/high/urgent)
├── last_message_at (Datetime)
├── last_message_preview (Small Text)
├── unread_count (Int)
│
├── # Assignment
├── assigned_to (Link → User)
├── assigned_team (Link → User Group)
│
├── # AI Analysis
├── sentiment_score (Float) [-1 to 1]
├── intent (Data)
├── suggested_reply (Long Text)
│
├── # Child Tables
├── messages (Table → Conversation Message)
└── internal_notes (Table → Conversation Note)

Conversation Message (Child Table)
├── direction (Select: inbound/outbound)
├── channel (Select: email/sms/voice/whatsapp/messenger/telegram)
├── content (Long Text)
├── content_html (Long Text)
├── timestamp (Datetime)
├── sender_name (Data)
├── sender_id (Data) [email address, phone, etc.]
├── channel_message_id (Data) [external reference]
├── read (Check)
├── attachments (Table → Message Attachment)
│
├── # Voice-specific
├── duration_seconds (Int)
├── recording_url (Data)
├── transcription (Long Text)
│
├── # AI
└── ai_summary (Text)

Conversation Note (Child Table - Internal)
├── user (Link → User)
├── note (Long Text)
├── timestamp (Datetime)
└── mentioned_users (Table MultiSelect → User)
```

### Dispatch Job

```
Dispatch Job
├── name (autoname: JOB-.YYYY.-.#####)
├── organization (Link → Organization)
│
├── # Source Links (Frappe Apps)
├── customer (Link → Customer) [ERPNext]
├── contact (Link → Contact) [ERPNext]
├── address (Link → Address) [ERPNext]
├── project (Link → Project) [ERPNext]
├── sales_order (Link → Sales Order) [ERPNext]
│
├── # Location (Geocoded from Address)
├── latitude (Float)
├── longitude (Float)
├── geohash (Data) [for spatial queries]
├── formatted_address (Data) [cached]
│
├── # Job Details
├── job_type (Link → Dispatch Job Type)
├── title (Data)
├── description (Long Text)
├── priority (Select: low/normal/high/urgent)
├── estimated_duration (Duration)
│
├── # Scheduling
├── scheduled_date (Date)
├── scheduled_start (Time)
├── scheduled_end (Time)
├── preferred_window (Select: morning/afternoon/evening/any)
├── customer_notes (Text)
│
├── # Assignment (Links to HRMS)
├── assigned_to (Link → Employee) [HRMS]
├── assigned_team (Link → Employee Group)
├── assignment_method (Select: manual/auto_nearest/auto_workload/auto_skill)
├── assigned_at (Datetime)
├── assigned_by (Link → User)
│
├── # Status
├── status (Select: draft/unassigned/assigned/en_route/arrived/in_progress/completed/cancelled)
├── status_updated_at (Datetime)
│
├── # Execution
├── actual_arrival (Datetime)
├── actual_departure (Datetime)
├── actual_duration (Duration) [calculated]
├── technician_notes (Long Text)
│
├── # Requirements
├── required_skills (Table MultiSelect → Skill)
├── required_certifications (Table MultiSelect → Certification Type)
├── required_equipment (Table → Job Equipment)
│
├── # Completion
├── customer_signature (Signature)
├── signed_by_name (Data)
├── signed_at (Datetime)
├── completion_photos (Attach)
├── form_submissions (Table → Linked Form Submission)
│
├── # Billing Integration (ERPNext)
├── billable (Check)
├── billing_status (Select: not_billed/partially_billed/billed)
├── sales_invoice (Link → Sales Invoice) [ERPNext]
├── timesheet (Link → Timesheet) [ERPNext]
│
└── # Assignment History
└── assignments (Table → Dispatch Assignment)

Dispatch Assignment (Child Table - History)
├── employee (Link → Employee)
├── assigned_at (Datetime)
├── assigned_by (Link → User)
├── reason (Data)
├── status (Select: assigned/declined/reassigned/completed)
└── notes (Text)
```

### Campaign (Growth Orchestrator)

```
Campaign
├── name (autoname: CAMP-.YYYY.-.#####)
├── campaign_name (Data)
├── organization (Link → Organization)
├── owner (Link → User)
├── status (Select: draft/configuring/active/paused/completed)
│
├── # ICP Definition (Output of AI Interview)
├── description (Long Text) [AI-generated summary]
├── target_industries (Table MultiSelect → Industry)
├── company_size_min (Int)
├── company_size_max (Int)
├── revenue_min (Currency)
├── revenue_max (Currency)
├── target_technologies (Table MultiSelect)
│
├── # Geographic Targeting
├── target_countries (Table MultiSelect → Country)
├── target_states (Table MultiSelect)
├── target_cities (Table MultiSelect)
├── radius_miles (Int)
│
├── # Persona Targeting
├── personas (Table → Campaign Persona)
│   ├── title (Data)
│   ├── department (Data)
│   └── seniority (Select: entry/mid/senior/executive)
│
├── # ICP Scoring Criteria
├── icp_criteria (JSON)
├── minimum_score (Int)
│
├── # LeadGen Integration (dartwing_leadgen)
├── search_job_id (Data) [from dartwing_leadgen]
├── job_status (Select: pending/running/completed/failed)
├── job_submitted_at (Datetime)
├── job_completed_at (Datetime)
│
├── # Budget
├── budget (Currency)
├── spent (Currency)
├── cost_per_lead_target (Currency)
│
├── # Results Summary
├── entities_found (Int)
├── entities_enriched (Int)
├── entities_qualified (Int)
├── leads_created (Int)
├── leads_contacted (Int)
├── leads_qualified (Int) [MQL]
├── deals_created (Int)
├── deals_won (Int)
├── revenue_generated (Currency)
│
├── # Calculated Metrics
├── cost_per_lead (Currency) [spent / leads_created]
├── lead_to_deal_rate (Percent) [deals_created / leads_created]
├── win_rate (Percent) [deals_won / deals_created]
└── roi (Percent) [(revenue - spent) / spent * 100]
```

### Schedule Entry (HR)

```
Schedule Entry
├── name (autoname: SCH-.YYYY.-.#####)
├── organization (Link → Organization)
│
├── # Core Assignment
├── employee (Link → Employee) [HRMS]
├── shift_template (Link → Shift Template) [ours]
├── date (Date)
│
├── # Override Times (optional)
├── start_time (Time) [defaults from template]
├── end_time (Time) [defaults from template]
│
├── # Location
├── work_location (Link → Work Location)
│
├── # Status
├── status (Select: draft/published/confirmed/completed/cancelled)
├── published_at (Datetime)
├── confirmed_at (Datetime)
│
├── # Swap Status
├── swap_status (Select: none/requested/offered/approved)
├── swap_request (Link → Shift Swap Request)
│
├── # HRMS Sync
├── hrms_shift_assignment (Link → Shift Assignment) [HRMS]
├── synced_to_hrms (Check)
├── last_sync (Datetime)
│
└── # Notes
└── notes (Text)

Shift Template
├── name (autoname: format:SHIFT-{shift_name})
├── organization (Link → Organization)
├── shift_name (Data)
├── start_time (Time)
├── end_time (Time)
├── break_duration_minutes (Int)
├── color (Color) [for UI]
├── roles (Table MultiSelect → Role)
├── default_location (Link → Work Location)
│
├── # HRMS Mapping
└── hrms_shift_type (Link → Shift Type) [HRMS]

Work Location
├── name (autoname: LOC-.#####)
├── organization (Link → Organization)
├── location_name (Data)
├── address (Link → Address) [ERPNext]
│
├── # Geofence
├── latitude (Float)
├── longitude (Float)
├── geofence_radius_meters (Int)
│
├── # Alternative Validation
├── allowed_wifi_networks (Table → WiFi Network)
├── qr_code (Data) [auto-generated]
│
├── # Validation Mode
├── validation_mode (Select: gps_only/wifi_only/qr_only/any)
│
└── # Linked Customer (for client sites)
└── customer (Link → Customer) [ERPNext]
```

---

## 4.3 Service Ticket (CRM Overlay)

```
Service Ticket
├── name (autoname: TKT-.YYYY.-.#####)
├── organization (Link → Organization)
│
├── # Links to Frappe Apps
├── customer (Link → Customer) [ERPNext]
├── contact (Link → Contact) [ERPNext]
├── lead (Link → Lead) [Frappe CRM]
├── conversation (Link → Conversation) [ours]
│
├── # Ticket Details
├── subject (Data)
├── description (Long Text)
├── category (Link → Ticket Category)
├── priority (Select: low/normal/high/urgent)
├── source (Select: portal/email/phone/chat/manual)
│
├── # Status
├── status (Select: new/open/pending/on_hold/resolved/closed)
├── resolution (Long Text)
├── resolved_at (Datetime)
├── closed_at (Datetime)
│
├── # Assignment
├── assigned_to (Link → User)
├── assigned_team (Link → User Group)
├── escalation_level (Int)
│
├── # SLA Tracking
├── sla_policy (Link → SLA Policy)
├── response_due (Datetime)
├── resolution_due (Datetime)
├── first_response_at (Datetime)
├── sla_status (Select: within_sla/at_risk/breached)
├── paused_at (Datetime) [for waiting on customer]
├── total_pause_duration (Duration)
│
├── # AI Analysis
├── sentiment_score (Float) [-1 to 1]
├── auto_category (Data) [AI-suggested]
├── auto_priority (Select) [AI-suggested]
│
├── # Escalation History
├── escalations (Table → Ticket Escalation)
│
└── # Internal Notes
└── notes (Table → Ticket Note)
```

---

## 4.4 Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTITY RELATIONSHIP DIAGRAM                          │
└─────────────────────────────────────────────────────────────────────────────┘

Organization (dartwing_core)
│
├────────────────────────────────────────────────────────────────────────────┐
│                           OUR DOCTYPES                                      │
├─────────────────────────────────────────────────────────────────────────────
│
├──1:N── Conversation
│         ├── contact ────────────────────────┐
│         ├── customer ───────────────────────┤
│         ├── lead ───────────────────────────┤
│         └── messages (child) ───────────────│
│                                             │
├──1:N── Dispatch Job                         │
│         ├── customer ───────────────────────┤─── ERPNext
│         ├── address ────────────────────────┤
│         ├── project ────────────────────────┤
│         ├── assigned_to (Employee) ─────────┤─── HRMS
│         └── sales_invoice ──────────────────┤─── ERPNext
│                                             │
├──1:N── Campaign                             │
│         └── creates ─► Lead ────────────────┤─── Frappe CRM
│                                             │
├──1:N── Service Ticket                       │
│         ├── customer ───────────────────────┤─── ERPNext
│         ├── contact ────────────────────────┤
│         └── conversation ───────────────────┘
│
├──1:N── Schedule Entry
│         ├── employee ───────────────────────┐
│         ├── shift_template ─────────────────┤
│         └── hrms_shift_assignment ──────────┤─── HRMS
│                                             │
├──1:N── Work Location                        │
│         └── linked for geo clock-in ────────┤
│                                             │
├──1:N── Employee Certification               │
│         └── employee ───────────────────────┘─── HRMS
│
├──1:N── Appointment
│         ├── contact ────────────────────────┐
│         ├── customer ───────────────────────┤─── ERPNext
│         ├── lead ───────────────────────────┤─── Frappe CRM
│         └── patient ────────────────────────┤─── Frappe Health
│                                             │
├──1:N── Document Vault                       │
│         ├── customer ───────────────────────┤─── ERPNext
│         └── drive_folder ───────────────────┘─── Frappe Drive
│
└──1:N── Mobile Form
          └── form_submissions (child)
```

---

## 4.5 Frappe App Linking Strategy

### Link vs Embed Decision

| Scenario      | Strategy                     | Reason                         |
| ------------- | ---------------------------- | ------------------------------ |
| Customer data | **Link** to ERPNext Customer | Single source of truth         |
| Employee data | **Link** to HRMS Employee    | Leverage HRMS features         |
| Lead data     | **Link** to CRM Lead         | Use CRM pipeline               |
| Attendance    | **Extend** HRMS Attendance   | Add GPS fields, sync our data  |
| Files         | **Use** Frappe Drive         | Leverage Drive storage/sharing |
| Invoices      | **Link** to ERPNext          | Display in portal, don't copy  |

### Custom Fields vs Child Tables

```python
# When to use Custom Fields on Frappe Apps:
# - Small amount of extra data
# - Data that "belongs" to the parent
# - Example: GPS location on Attendance

# When to use separate DocType with Link:
# - Complex data structures
# - Data with its own lifecycle
# - Example: Employee Certification (has expiry, renewal workflow)
```

---

**Next: Section 5 - Operations Core Architecture**

# Dartwing Company Architecture - Section 5: Operations Core

---

## 5.1 Universal Inbox Architecture

### Channel Aggregation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       UNIVERSAL INBOX ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHANNEL PLUGINS                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │    Email    │ │     SMS     │ │    Voice    │ │  WhatsApp   │           │
│  │   (IMAP)    │ │(dartwing_   │ │(dartwing_   │ │  Business   │           │
│  │             │ │   fone)     │ │   fone)     │ │    API      │           │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
│         │               │               │               │                   │
│  ┌──────┴───────────────┴───────────────┴───────────────┴──────┐           │
│  │                     CHANNEL ROUTER                           │           │
│  │  • Normalize message format                                 │           │
│  │  • Extract sender/recipient                                 │           │
│  │  • Parse attachments                                        │           │
│  └──────────────────────────┬──────────────────────────────────┘           │
└─────────────────────────────┼───────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                        CONTACT MATCHER                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  1. Search ERPNext Contact by phone/email                           │    │
│  │  2. Search Frappe CRM Lead by phone/email                           │    │
│  │  3. Search ERPNext Customer by phone/email                          │    │
│  │  4. Search Frappe Health Patient (if healthcare mode)               │    │
│  │  5. If no match → Create new Contact or flag for review            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                      SESSION MANAGER                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  • Find or create Conversation for this contact/channel             │    │
│  │  • Add message to Conversation                                      │    │
│  │  • Update last_message_at, unread_count                            │    │
│  │  • Create linked Communication in Frappe CRM                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                         AI PROCESSOR                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  • Sentiment analysis → sentiment_score                             │    │
│  │  • Intent detection → intent                                        │    │
│  │  • Auto-reply suggestion → suggested_reply                          │    │
│  │  • Ticket auto-creation (if support request detected)               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Notify Assignee │
                    │ (Push/Email)    │
                    └─────────────────┘
```

### Channel Plugin Interface

```python
# operations/inbox/channels/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class InboundMessage:
    """Normalized inbound message"""
    channel: str
    sender_id: str           # Email, phone, user ID
    sender_name: str
    recipient_id: str        # Our address/number
    content: str
    content_html: str = None
    timestamp: datetime = None
    external_id: str = None  # Provider's message ID
    attachments: list = None
    metadata: dict = None

    # Voice-specific
    duration_seconds: int = None
    recording_url: str = None
    transcription: str = None

class ChannelPlugin(ABC):
    """Base class for all channel integrations"""

    channel_name: str  # 'email', 'sms', 'voice', etc.

    @abstractmethod
    async def sync_inbound(self) -> list[InboundMessage]:
        """Poll for new inbound messages"""
        pass

    @abstractmethod
    async def send_message(self, recipient: str, content: str,
                           attachments: list = None) -> str:
        """Send outbound message, return external ID"""
        pass

    @abstractmethod
    def validate_webhook(self, request: dict, signature: str) -> bool:
        """Validate webhook authenticity"""
        pass

    @abstractmethod
    def parse_webhook(self, request: dict) -> InboundMessage:
        """Parse webhook payload to normalized message"""
        pass
```

### Email Channel Implementation

```python
# operations/inbox/channels/email.py
import imaplib
import email
from email.mime.multipart import MIMEMultipart

class EmailChannel(ChannelPlugin):
    channel_name = "email"

    def __init__(self, config: dict):
        self.imap_host = config["imap_host"]
        self.imap_user = config["imap_user"]
        self.imap_password = config["imap_password"]
        self.smtp_host = config["smtp_host"]

    async def sync_inbound(self) -> list[InboundMessage]:
        """Fetch new emails via IMAP"""
        messages = []

        with imaplib.IMAP4_SSL(self.imap_host) as imap:
            imap.login(self.imap_user, self.imap_password)
            imap.select("INBOX")

            # Search for unseen messages
            _, msg_nums = imap.search(None, "UNSEEN")

            for num in msg_nums[0].split():
                _, data = imap.fetch(num, "(RFC822)")
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                messages.append(InboundMessage(
                    channel="email",
                    sender_id=self._extract_email(msg["From"]),
                    sender_name=self._extract_name(msg["From"]),
                    recipient_id=self._extract_email(msg["To"]),
                    content=self._get_body_text(msg),
                    content_html=self._get_body_html(msg),
                    timestamp=self._parse_date(msg["Date"]),
                    external_id=msg["Message-ID"],
                    attachments=self._extract_attachments(msg)
                ))

        return messages

    async def send_message(self, recipient: str, content: str,
                           attachments: list = None) -> str:
        """Send email via SMTP"""
        msg = MIMEMultipart()
        msg["To"] = recipient
        msg["From"] = self.imap_user
        msg["Subject"] = content[:50]  # Or from context

        # Add body
        msg.attach(MIMEText(content, "plain"))

        # Send via SMTP
        with smtplib.SMTP_SSL(self.smtp_host) as smtp:
            smtp.login(self.imap_user, self.imap_password)
            smtp.send_message(msg)

        return msg["Message-ID"]
```

### Voice/SMS via dartwing_fone

```python
# operations/inbox/channels/sms.py
from dartwing_fone.api import FoneClient

class SMSChannel(ChannelPlugin):
    channel_name = "sms"

    def __init__(self, config: dict):
        self.fone = FoneClient(config["organization"])

    async def sync_inbound(self) -> list[InboundMessage]:
        """Fetch new SMS via dartwing_fone API"""
        sms_list = await self.fone.get_sms(
            status="unprocessed",
            direction="inbound"
        )

        messages = []
        for sms in sms_list:
            messages.append(InboundMessage(
                channel="sms",
                sender_id=sms["from_number"],
                sender_name=sms.get("caller_id_name"),
                recipient_id=sms["to_number"],
                content=sms["body"],
                timestamp=sms["received_at"],
                external_id=sms["sms_id"],
                attachments=sms.get("media_urls", [])
            ))

            # Mark as processed
            await self.fone.mark_sms_processed(sms["sms_id"])

        return messages

    async def send_message(self, recipient: str, content: str,
                           attachments: list = None) -> str:
        """Send SMS via dartwing_fone"""
        result = await self.fone.send_sms(
            to_number=recipient,
            body=content,
            media_urls=attachments
        )
        return result["sms_id"]

    def parse_webhook(self, request: dict) -> InboundMessage:
        """Parse dartwing_fone SMS webhook"""
        return InboundMessage(
            channel="sms",
            sender_id=request["from"],
            sender_name=request.get("caller_id"),
            recipient_id=request["to"],
            content=request["body"],
            timestamp=request["timestamp"],
            external_id=request["sms_id"]
        )
```

---

## 5.2 Smart Dispatch Architecture

### Dispatch Engine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DISPATCH ENGINE ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

Job Request (Portal/API/Manual)
        │
        ▼
┌───────────────────┐
│ Create Dispatch   │
│ Job               │
│ • Link Customer   │───────────────▶ ERPNext Customer
│ • Link Address    │───────────────▶ ERPNext Address
└─────────┬─────────┘
          │
┌─────────▼─────────┐
│ GEO SERVICE       │
│ (Google Maps API) │
│ • Geocode address │
│ • Generate geohash│
└─────────┬─────────┘
          │
┌─────────▼─────────────────────────────────────────────────────┐
│                    ASSIGNMENT ENGINE                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 1. Query Available Employees (HRMS)                      │  │
│  │    • Not on leave (HRMS Leave Application)              │  │
│  │    • Within shift hours (Schedule Entry)                │  │
│  │    • dispatch_enabled = True (Custom Field)             │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 2. Filter by Skills/Certifications                       │  │
│  │    • Check Employee Certification (ours)                │  │
│  │    • Verify not expired                                 │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 3. Calculate Drive Times                                 │  │
│  │    • From employee current location OR home location    │  │
│  │    • Google Maps Directions API                         │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 4. Score and Rank                                        │  │
│  │    • Proximity score                                    │  │
│  │    • Workload balance score                             │  │
│  │    • Skill match score                                  │  │
│  │    • Customer preference score                          │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬─────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                    ASSIGNMENT RESULT                           │
│  Best Match: Carlos Rodriguez                                  │
│  • 12 min drive time                                          │
│  • HVAC Certified ✓                                           │
│  • 2 jobs today (vs team avg 3.5)                            │
│  • Customer preference: None                                   │
│                                                                │
│  [Auto-Assign] [Show Alternatives] [Manual Override]          │
└───────────────────────────────────────────────────────────────┘
```

### Assignment Algorithm

```python
# operations/dispatch/assignment.py
@dataclass
class AssignmentScore:
    employee: str
    total_score: float
    proximity_score: float
    workload_score: float
    skill_score: float
    preference_score: float
    drive_time_minutes: int
    distance_km: float

class SmartAssignment:
    """AI-powered job assignment"""

    def __init__(self, organization: str):
        self.org = organization
        self.geo = GeoService()

    async def find_best_match(self, job: "DispatchJob") -> list[AssignmentScore]:
        """Find and rank best employees for job"""

        # 1. Get available employees from HRMS
        employees = self._get_available_employees(job.scheduled_date)

        # 2. Filter by required skills
        if job.required_skills:
            employees = self._filter_by_skills(employees, job.required_skills)

        # 3. Filter by certifications
        if job.required_certifications:
            employees = self._filter_by_certifications(
                employees, job.required_certifications)

        if not employees:
            return []

        # 4. Calculate scores for each
        scores = []
        for emp in employees:
            score = await self._calculate_score(emp, job)
            scores.append(score)

        # 5. Sort by total score (descending)
        scores.sort(key=lambda s: s.total_score, reverse=True)

        return scores

    def _get_available_employees(self, date: date) -> list:
        """Query HRMS for available employees"""
        # Get employees with dispatch_enabled
        employees = frappe.get_all("Employee",
            filters={
                "status": "Active",
                "dispatch_enabled": 1,
                "company": self.org
            },
            fields=["name", "employee_name", "home_location"]
        )

        # Exclude those on leave
        on_leave = frappe.get_all("Leave Application",
            filters={
                "from_date": ["<=", date],
                "to_date": [">=", date],
                "status": "Approved"
            },
            pluck="employee"
        )

        return [e for e in employees if e.name not in on_leave]

    def _filter_by_certifications(self, employees: list,
                                   required: list) -> list:
        """Filter employees by valid certifications"""
        qualified = []
        today = frappe.utils.today()

        for emp in employees:
            certs = frappe.get_all("Employee Certification",
                filters={
                    "employee": emp.name,
                    "certification_type": ["in", required],
                    "expiry_date": [">=", today]
                },
                pluck="certification_type"
            )

            if set(required).issubset(set(certs)):
                qualified.append(emp)

        return qualified

    async def _calculate_score(self, employee: dict,
                                job: "DispatchJob") -> AssignmentScore:
        """Calculate assignment score"""

        # Get employee location
        emp_location = self._get_employee_location(employee)
        job_location = (job.latitude, job.longitude)

        # Calculate drive time
        drive_result = await self.geo.get_drive_time(
            emp_location, job_location)

        # Proximity score (0-100, inverse of drive time)
        max_acceptable_minutes = 60
        proximity_score = max(0, 100 - (drive_result.duration_minutes / max_acceptable_minutes * 100))

        # Workload score (prefer employees with fewer jobs)
        jobs_today = self._count_jobs_today(employee.name, job.scheduled_date)
        team_avg = self._get_team_average_jobs(job.scheduled_date)
        workload_score = max(0, 100 - (jobs_today / max(team_avg, 1) * 50))

        # Skill score (how well skills match)
        skill_score = self._calculate_skill_match(employee, job)

        # Customer preference (previous positive interactions)
        preference_score = self._get_customer_preference(
            employee.name, job.customer)

        # Weighted total
        total = (
            proximity_score * 0.4 +
            workload_score * 0.25 +
            skill_score * 0.25 +
            preference_score * 0.1
        )

        return AssignmentScore(
            employee=employee.name,
            total_score=total,
            proximity_score=proximity_score,
            workload_score=workload_score,
            skill_score=skill_score,
            preference_score=preference_score,
            drive_time_minutes=drive_result.duration_minutes,
            distance_km=drive_result.distance_km
        )
```

---

## 5.3 Workflow Engine Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       WORKFLOW ENGINE ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          WORKFLOW TEMPLATE                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Trigger: Service Ticket.after_insert                                │    │
│  │ Condition: priority == 'urgent' AND customer_group == 'VIP'         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Step 1   │───▶│ Step 2   │───▶│ Step 3   │───▶│ Step 4   │             │
│  │ Assign   │    │ Notify   │    │ Create   │    │ Schedule │             │
│  │ to VIP   │    │ Manager  │    │ Calendar │    │ Follow-up│             │
│  │ Team     │    │          │    │ Event    │    │ Task     │             │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘

Trigger Types:
• doc_event: DocType created/updated/field changed
• schedule: Cron expression
• webhook: External event
• manual: User-initiated

Action Types:
• assign_user: Assign to user/team
• update_field: Update document field
• create_document: Create new document
• send_email: Send email notification
• send_sms: Send SMS (via dartwing_fone)
• call_webhook: HTTP POST to external URL
• create_task: Create ERPNext Task
• create_calendar_event: Create Event
• wait: Delay execution
• branch: Conditional branching
• approve: Require approval
```

### Workflow Engine Implementation

```python
# operations/workflow/engine.py
class WorkflowEngine:
    """Execute workflow instances"""

    def trigger_workflows(self, doctype: str, doc: Document,
                          event: str, changed_fields: list = None):
        """Find and execute matching workflows"""

        # Find active workflows for this trigger
        workflows = frappe.get_all("Workflow Template",
            filters={
                "enabled": 1,
                "trigger_doctype": doctype,
                "trigger_event": event
            }
        )

        for wf in workflows:
            template = frappe.get_doc("Workflow Template", wf.name)

            # Check conditions
            if not self._evaluate_condition(template.condition, doc):
                continue

            # Check field change condition
            if template.trigger_field and changed_fields:
                if template.trigger_field not in changed_fields:
                    continue

            # Create workflow instance
            instance = self._create_instance(template, doc)

            # Execute first step
            frappe.enqueue(
                "dartwing_company.operations.workflow.engine.execute_step",
                instance_id=instance.name,
                step_index=0
            )

    def execute_step(self, instance_id: str, step_index: int):
        """Execute a single workflow step"""
        instance = frappe.get_doc("Workflow Instance", instance_id)
        template = frappe.get_doc("Workflow Template", instance.workflow_template)

        if step_index >= len(template.steps):
            instance.status = "Completed"
            instance.save()
            return

        step = template.steps[step_index]

        try:
            # Execute action
            result = self._execute_action(step, instance)

            # Log step completion
            instance.append("execution_log", {
                "step_index": step_index,
                "action_type": step.action_type,
                "status": "completed",
                "result": str(result)
            })

            # Handle branching
            next_step = step_index + 1
            if step.action_type == "branch":
                next_step = self._evaluate_branch(step, instance, result)

            # Handle wait
            if step.action_type == "wait":
                instance.status = "Waiting"
                instance.resume_at = now() + timedelta(seconds=step.wait_seconds)
                instance.next_step = next_step
                instance.save()
                return

            # Execute next step
            instance.save()
            self.execute_step(instance_id, next_step)

        except Exception as e:
            instance.status = "Failed"
            instance.error_message = str(e)
            instance.save()
            raise

    def _execute_action(self, step: dict, instance: "WorkflowInstance"):
        """Execute a workflow action"""
        action_type = step.action_type
        doc = frappe.get_doc(instance.reference_doctype, instance.reference_name)

        if action_type == "assign_user":
            doc.assigned_to = step.target_user
            doc.save()

        elif action_type == "update_field":
            doc.set(step.target_field, step.field_value)
            doc.save()

        elif action_type == "create_document":
            new_doc = frappe.get_doc({
                "doctype": step.create_doctype,
                **self._interpolate_values(step.create_values, doc)
            })
            new_doc.insert()
            return new_doc.name

        elif action_type == "send_email":
            frappe.sendmail(
                recipients=self._resolve_recipients(step.email_to, doc),
                subject=self._interpolate(step.email_subject, doc),
                message=self._interpolate(step.email_body, doc)
            )

        elif action_type == "send_sms":
            from dartwing_fone.api import send_sms
            send_sms(
                to=self._resolve_phone(step.sms_to, doc),
                message=self._interpolate(step.sms_body, doc)
            )

        elif action_type == "call_webhook":
            import requests
            response = requests.post(
                step.webhook_url,
                json=self._build_webhook_payload(step, doc),
                headers={"Content-Type": "application/json"}
            )
            return response.status_code
```

---

## 5.4 Knowledge Base RAG Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAG ARCHITECTURE                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │         CONTENT SOURCES             │
                    │  ┌───────────┐ ┌───────────┐       │
                    │  │ Knowledge │ │   PDFs    │       │
                    │  │ Articles  │ │(via Drive)│       │
                    │  └─────┬─────┘ └─────┬─────┘       │
                    └────────┼─────────────┼─────────────┘
                             │             │
                    ┌────────▼─────────────▼─────────────┐
                    │           INDEXER                   │
                    │  • Chunk documents (500 tokens)    │
                    │  • Generate embeddings (OpenAI)    │
                    │  • Store in OpenSearch             │
                    └────────────────┬────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OPENSEARCH INDEX                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Index: knowledge_chunks                                              │    │
│  │ • chunk_id                                                          │    │
│  │ • content (text)                                                    │    │
│  │ • embedding (vector, 1536 dim)                                      │    │
│  │ • source_doctype                                                    │    │
│  │ • source_name                                                       │    │
│  │ • organization                                                      │    │
│  │ • access_roles (array)                                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

User Question: "How do I reset the XYZ controller?"
        │
        ▼
┌───────────────────┐
│ QUERY PROCESSOR   │
│ • Embed question  │
│ • Filter by org   │
│ • Filter by roles │
└─────────┬─────────┘
          │
┌─────────▼─────────┐
│ VECTOR SEARCH     │
│ • k-NN search     │
│ • Top 5 chunks    │
└─────────┬─────────┘
          │
┌─────────▼─────────┐
│ CONTEXT BUILDER   │
│ • Assemble chunks │
│ • Add source refs │
└─────────┬─────────┘
          │
┌─────────▼─────────────────────────────────────────────────────┐
│ LLM GENERATION (OpenAI/Claude)                                 │
│                                                                │
│ System: You are a helpful assistant. Answer based on the      │
│ provided context. Cite sources.                               │
│                                                                │
│ Context:                                                       │
│ [1] From "SOP-XYZ-Reset": To reset the XYZ controller...      │
│ [2] From "Troubleshooting Guide": Common reset issues...       │
│                                                                │
│ Question: How do I reset the XYZ controller?                   │
│                                                                │
│ Answer: According to [1] SOP-XYZ-Reset, you can reset the     │
│ XYZ controller by holding the power button for 10 seconds...   │
└───────────────────────────────────────────────────────────────┘
```

### RAG Implementation

```python
# operations/knowledge/rag_engine.py
from openai import OpenAI
from opensearchpy import OpenSearch

class RAGEngine:
    """Retrieval-Augmented Generation for Knowledge Base"""

    def __init__(self, organization: str):
        self.org = organization
        self.openai = OpenAI()
        self.opensearch = OpenSearch(hosts=[frappe.conf.opensearch_host])
        self.index = "knowledge_chunks"
        self.embedding_model = "text-embedding-3-small"
        self.llm_model = "gpt-4o"

    async def answer_question(self, question: str,
                               user_roles: list) -> dict:
        """Answer question using RAG"""

        # 1. Embed question
        question_embedding = await self._embed(question)

        # 2. Search for relevant chunks
        chunks = await self._search_chunks(
            question_embedding,
            user_roles,
            k=5
        )

        if not chunks:
            return {
                "answer": "I couldn't find relevant information in the knowledge base.",
                "sources": [],
                "confidence": 0
            }

        # 3. Build context
        context = self._build_context(chunks)

        # 4. Generate answer
        answer = await self._generate_answer(question, context)

        return {
            "answer": answer,
            "sources": [
                {
                    "title": c["source_title"],
                    "doctype": c["source_doctype"],
                    "name": c["source_name"],
                    "relevance": c["score"]
                }
                for c in chunks
            ],
            "confidence": chunks[0]["score"] if chunks else 0
        }

    async def _embed(self, text: str) -> list[float]:
        """Generate embedding for text"""
        response = self.openai.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    async def _search_chunks(self, embedding: list,
                              roles: list, k: int) -> list:
        """Search OpenSearch for relevant chunks"""
        query = {
            "size": k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "knn": {
                                "embedding": {
                                    "vector": embedding,
                                    "k": k
                                }
                            }
                        }
                    ],
                    "filter": [
                        {"term": {"organization": self.org}},
                        {"terms": {"access_roles": roles + ["All"]}}
                    ]
                }
            }
        }

        response = self.opensearch.search(index=self.index, body=query)

        return [
            {
                "content": hit["_source"]["content"],
                "source_doctype": hit["_source"]["source_doctype"],
                "source_name": hit["_source"]["source_name"],
                "source_title": hit["_source"]["source_title"],
                "score": hit["_score"]
            }
            for hit in response["hits"]["hits"]
        ]

    async def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM"""
        response = self.openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant answering questions
                    based on company knowledge base. Always cite your sources using
                    [n] notation. If the context doesn't contain relevant information,
                    say so."""
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content
```

---

**Next: Section 6 - CRM Overlay Architecture**

# Dartwing Company Architecture - Section 6: CRM Overlay

_Overlay architecture that enhances Frappe CRM without modifying it._

---

## 6.1 Client Portal Architecture

### Portal Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLIENT PORTAL AUTHENTICATION                             │
└─────────────────────────────────────────────────────────────────────────────┘

Customer requests portal access
        │
        ▼
┌───────────────────┐
│ Check Customer    │ ERPNext Customer.portal_enabled (custom field)
│ portal_enabled    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Get Contact       │ ERPNext Contact linked to Customer
│                   │ Contact.email_id → Portal User email
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Create/Get        │ Frappe User with role "Portal User"
│ Portal User       │ User.user_type = "Website User"
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Get View Set      │ Customer.view_set (custom field)
│                   │ OR Customer Group default View Set
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Render Portal     │ Based on View Set widgets
│ Dashboard         │
└───────────────────┘
```

### View Set Widget System

```python
# crm/portal/widgets.py

# Available widget types
WIDGET_TYPES = {
    "dashboard_summary": DashboardSummaryWidget,
    "open_invoices": InvoiceListWidget,
    "invoice_detail": InvoiceDetailWidget,
    "project_list": ProjectListWidget,
    "project_status": ProjectStatusWidget,
    "document_vault": DocumentVaultWidget,
    "support_tickets": TicketListWidget,
    "ticket_submit": TicketSubmitWidget,
    "appointment_scheduler": AppointmentWidget,
    "message_center": MessageWidget,
    "team_contacts": TeamContactsWidget,
    "custom_html": CustomHTMLWidget,
}

class BaseWidget:
    """Base class for portal widgets"""

    widget_type: str
    requires_permission: str = None

    def __init__(self, config: dict, customer: str, user: str):
        self.config = config
        self.customer = customer
        self.user = user

    def can_view(self) -> bool:
        """Check if user can view this widget"""
        if not self.requires_permission:
            return True
        return frappe.has_permission(self.requires_permission, user=self.user)

    def get_data(self) -> dict:
        """Fetch widget data"""
        raise NotImplementedError

    def render(self) -> str:
        """Render widget HTML"""
        raise NotImplementedError


class InvoiceListWidget(BaseWidget):
    """Shows customer's invoices from ERPNext"""

    widget_type = "open_invoices"
    requires_permission = "Sales Invoice"

    def get_data(self) -> dict:
        invoices = frappe.get_all("Sales Invoice",
            filters={
                "customer": self.customer,
                "docstatus": 1
            },
            fields=[
                "name", "posting_date", "grand_total",
                "outstanding_amount", "status"
            ],
            order_by="posting_date desc",
            limit=10
        )

        return {
            "invoices": invoices,
            "total_outstanding": sum(i.outstanding_amount for i in invoices)
        }


class ProjectStatusWidget(BaseWidget):
    """Shows project status from ERPNext"""

    widget_type = "project_status"
    requires_permission = "Project"

    def get_data(self) -> dict:
        # Get projects linked to customer
        projects = frappe.get_all("Project",
            filters={
                "customer": self.customer,
                "status": ["not in", ["Completed", "Cancelled"]]
            },
            fields=[
                "name", "project_name", "status",
                "percent_complete", "expected_end_date"
            ]
        )

        return {"projects": projects}


class DocumentVaultWidget(BaseWidget):
    """Shows files from Document Vault (backed by Frappe Drive)"""

    widget_type = "document_vault"

    def get_data(self) -> dict:
        # Get customer's vault
        vault = frappe.get_value("Document Vault",
            {"customer": self.customer}, "name")

        if not vault:
            return {"folders": [], "files": []}

        vault_doc = frappe.get_doc("Document Vault", vault)

        # Get files from Frappe Drive
        from frappe_drive.api import get_folder_contents
        contents = get_folder_contents(vault_doc.drive_folder)

        return {
            "folders": contents.get("folders", []),
            "files": contents.get("files", []),
            "vault_id": vault
        }
```

### Portal Page Controller

```python
# portal/www/portal/index.py
import frappe
from dartwing_company.crm.portal.auth import get_portal_context
from dartwing_company.crm.portal.widgets import get_widgets_for_view_set

def get_context(context):
    """Main portal page context"""

    # Check authentication
    if frappe.session.user == "Guest":
        frappe.throw("Please login", frappe.PermissionError)

    # Get portal context (customer, view set, etc.)
    portal_ctx = get_portal_context(frappe.session.user)

    if not portal_ctx.get("customer"):
        frappe.throw("No customer linked to your account")

    context.customer = portal_ctx["customer"]
    context.customer_name = portal_ctx["customer_name"]
    context.view_set = portal_ctx["view_set"]
    context.branding = portal_ctx["branding"]

    # Get widgets for this view set
    context.widgets = get_widgets_for_view_set(
        view_set=context.view_set,
        customer=context.customer,
        user=frappe.session.user
    )

    return context
```

---

## 6.2 SLA Engine Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SLA ENGINE ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────────────┘

Service Ticket Created
        │
        ▼
┌───────────────────┐
│ Match SLA Policy  │
│ • By Customer Group (ERPNext)                                               │
│ • By Priority                                                               │
│ • By Category                                                               │
└─────────┬─────────┘
          │
          ▼
┌───────────────────────────────────────────────────────────────┐
│ CALCULATE DEADLINES                                            │
│                                                                │
│ Priority: Urgent                                               │
│ Response SLA: 1 hour                                          │
│ Resolution SLA: 4 hours                                       │
│ Business Hours: Mon-Fri 8AM-6PM EST                           │
│                                                                │
│ Created: Friday 5:00 PM                                       │
│ Response Due: Monday 9:00 AM (next business hour + 1hr)       │
│ Resolution Due: Monday 12:00 PM (next business + 4hr)         │
└─────────┬─────────────────────────────────────────────────────┘
          │
          ▼
┌───────────────────┐
│ Set Deadlines     │
│ • response_due    │
│ • resolution_due  │
└─────────┬─────────┘
          │
          ▼
    ┌─────────────────────────────────────────────┐
    │           SLA MONITOR (Background Job)      │
    │                                             │
    │ Every minute:                               │
    │ • Check tickets approaching deadline        │
    │ • 75% elapsed → Warning notification        │
    │ • 90% elapsed → Escalation alert            │
    │ • 100% → Breach, escalate to manager        │
    │                                             │
    │ Pause handling:                             │
    │ • Status = "Waiting on Customer"            │
    │ • Pause SLA timer                           │
    │ • Resume when customer responds             │
    └─────────────────────────────────────────────┘
```

### SLA Engine Implementation

```python
# crm/tickets/sla_engine.py
from datetime import datetime, timedelta

class SLAEngine:
    """SLA calculation and monitoring"""

    def __init__(self, organization: str):
        self.org = organization

    def get_policy_for_ticket(self, ticket: "ServiceTicket") -> "SLAPolicy":
        """Find matching SLA policy"""

        # Get customer group from ERPNext
        customer = frappe.get_doc("Customer", ticket.customer)
        customer_group = customer.customer_group

        # Find policy by priority order:
        # 1. Specific customer
        # 2. Customer group
        # 3. Category
        # 4. Default

        policy = frappe.get_value("SLA Policy", {
            "organization": self.org,
            "applies_to_customer": ticket.customer
        }, "name")

        if not policy:
            policy = frappe.get_value("SLA Policy", {
                "organization": self.org,
                "applies_to_customer_group": customer_group
            }, "name")

        if not policy:
            policy = frappe.get_value("SLA Policy", {
                "organization": self.org,
                "applies_to_category": ticket.category
            }, "name")

        if not policy:
            policy = frappe.get_value("SLA Policy", {
                "organization": self.org,
                "is_default": 1
            }, "name")

        if policy:
            return frappe.get_doc("SLA Policy", policy)
        return None

    def calculate_deadlines(self, ticket: "ServiceTicket",
                            policy: "SLAPolicy") -> dict:
        """Calculate SLA deadlines considering business hours"""

        created_at = ticket.creation
        priority = ticket.priority

        # Get SLA times from policy rules
        rule = self._get_rule_for_priority(policy, priority)

        if not rule:
            return {}

        # Get business hours
        business_hours = self._parse_business_hours(policy.business_hours)
        holidays = self._get_holidays(policy.holiday_list)

        # Calculate response deadline
        response_due = self._add_business_time(
            created_at,
            rule.response_time_hours,
            business_hours,
            holidays
        )

        # Calculate resolution deadline
        resolution_due = self._add_business_time(
            created_at,
            rule.resolution_time_hours,
            business_hours,
            holidays
        )

        return {
            "response_due": response_due,
            "resolution_due": resolution_due
        }

    def _add_business_time(self, start: datetime, hours: float,
                           business_hours: dict, holidays: list) -> datetime:
        """Add business hours to datetime"""
        remaining_minutes = hours * 60
        current = start

        while remaining_minutes > 0:
            # Skip weekends
            if current.weekday() >= 5:
                current += timedelta(days=1)
                current = current.replace(
                    hour=business_hours["start_hour"],
                    minute=0
                )
                continue

            # Skip holidays
            if current.date() in holidays:
                current += timedelta(days=1)
                current = current.replace(
                    hour=business_hours["start_hour"],
                    minute=0
                )
                continue

            # Check if within business hours
            start_time = current.replace(
                hour=business_hours["start_hour"],
                minute=business_hours["start_minute"]
            )
            end_time = current.replace(
                hour=business_hours["end_hour"],
                minute=business_hours["end_minute"]
            )

            if current < start_time:
                current = start_time

            if current >= end_time:
                # Move to next business day
                current += timedelta(days=1)
                current = current.replace(
                    hour=business_hours["start_hour"],
                    minute=0
                )
                continue

            # Calculate time until end of business day
            minutes_until_end = (end_time - current).seconds // 60

            if remaining_minutes <= minutes_until_end:
                current += timedelta(minutes=remaining_minutes)
                remaining_minutes = 0
            else:
                remaining_minutes -= minutes_until_end
                current = end_time

        return current

    def check_sla_status(self, ticket: "ServiceTicket") -> str:
        """Check current SLA status"""
        now = datetime.now()

        # If paused, don't check
        if ticket.paused_at:
            return "paused"

        # Check response SLA
        if not ticket.first_response_at:
            if now >= ticket.response_due:
                return "response_breached"
            elif now >= ticket.response_due - timedelta(
                    minutes=ticket.response_due.minute * 0.25):
                return "response_at_risk"

        # Check resolution SLA
        if ticket.status not in ["Resolved", "Closed"]:
            if now >= ticket.resolution_due:
                return "resolution_breached"
            elif now >= ticket.resolution_due - timedelta(
                    minutes=ticket.resolution_due.minute * 0.25):
                return "resolution_at_risk"

        return "within_sla"
```

---

## 6.3 Growth Orchestrator Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GROWTH ORCHESTRATOR ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI INTERVIEW AGENT                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Conversational AI that builds ICP through questions:                │    │
│  │                                                                      │    │
│  │ 1. "What does your company do?" → Read from Organization            │    │
│  │ 2. "What products/services?" → Read from ERPNext Item catalog       │    │
│  │ 3. "What industries are your best customers?" → Suggest from data   │    │
│  │ 4. "What company size?" → Build criteria                            │    │
│  │ 5. "What job titles do you sell to?" → Build personas               │    │
│  │ 6. "Geographic focus?" → Build targeting                            │    │
│  │ 7. "What's your lead offer?" → Campaign hook                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼ Creates Campaign DocType
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAMPAIGN                                           │
│  • ICP Definition                                                            │
│  • Geographic Targeting                                                      │
│  • Persona Definitions                                                       │
│  • Scoring Criteria                                                          │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼ Generate Search_Job JSON
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LEADGEN CLIENT                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ POST to dartwing_leadgen.api.search.create_job                      │    │
│  │                                                                      │    │
│  │ {                                                                    │    │
│  │   "requestor": {"module": "dartwing_company", "campaign": "..."},   │    │
│  │   "search_parameters": {...},                                       │    │
│  │   "geographic": {...},                                              │    │
│  │   "personas": {...},                                                │    │
│  │   "scoring": {"icp_criteria": {...}}                                │    │
│  │ }                                                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              │ Async processing in dartwing_leadgen
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                      WEBHOOK: job.completed                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Receive qualified entities from dartwing_leadgen                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LEAD CREATOR                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ For each entity:                                                     │    │
│  │ 1. Check for duplicates in Frappe CRM Lead                          │    │
│  │ 2. Map entity fields → Lead fields                                  │    │
│  │ 3. Set source = "Growth Orchestrator"                               │    │
│  │ 4. Set campaign link                                                │    │
│  │ 5. Set icp_score (custom field)                                     │    │
│  │ 6. Create Lead in Frappe CRM                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FRAPPE CRM                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Lead                                                                 │    │
│  │ • first_name, last_name, email, phone                               │    │
│  │ • company_name, industry                                            │    │
│  │ • source: "Growth Orchestrator"                                     │    │
│  │ • campaign: "CAMP-2025-001" (custom field link)                     │    │
│  │ • icp_score: 85 (custom field)                                      │    │
│  │ • leadgen_source: "linkedin" (custom field)                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Deal Pipeline                                                               │
│  • Track conversions → Update Campaign.deals_created                        │
│  • Track wins → Update Campaign.deals_won, revenue_generated                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Interview Agent Implementation

```python
# crm/growth/interview_agent.py
from openai import OpenAI

class InterviewAgent:
    """AI agent that conducts ICP interview"""

    INTERVIEW_STAGES = [
        "business_context",
        "products_services",
        "ideal_customer",
        "company_size",
        "geographic",
        "personas",
        "campaign_offer"
    ]

    def __init__(self, organization: str):
        self.org = organization
        self.openai = OpenAI()
        self.context = self._load_org_context()

    def _load_org_context(self) -> dict:
        """Load existing organization data"""
        org = frappe.get_doc("Organization", self.org)

        # Get ERPNext data
        customers = frappe.get_all("Customer",
            filters={"company": self.org},
            fields=["customer_group", "territory"],
            limit=100
        )

        items = frappe.get_all("Item",
            filters={"item_group": ["like", "%Service%"]},
            fields=["item_name", "item_group"],
            limit=50
        )

        return {
            "organization_name": org.organization_name,
            "industry": org.industry,
            "description": org.description,
            "top_customer_groups": self._get_top_groups(customers),
            "top_territories": self._get_top_territories(customers),
            "services": [i.item_name for i in items]
        }

    def conduct_interview(self, conversation_history: list) -> dict:
        """Process interview step and generate next question"""

        current_stage = self._determine_stage(conversation_history)

        # Build system prompt
        system_prompt = self._build_system_prompt(current_stage)

        # Generate response
        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                *conversation_history
            ],
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Check if interview is complete
        is_complete = current_stage == "campaign_offer" and \
                      self._has_all_required_info(conversation_history)

        return {
            "message": assistant_message,
            "stage": current_stage,
            "is_complete": is_complete,
            "extracted_data": self._extract_icp_data(conversation_history) if is_complete else None
        }

    def _build_system_prompt(self, stage: str) -> str:
        """Build stage-specific system prompt"""
        base = f"""You are a growth strategy consultant helping build an Ideal Customer Profile.

Current organization context:
- Name: {self.context['organization_name']}
- Industry: {self.context['industry']}
- Services: {', '.join(self.context['services'][:10])}
- Top customer segments: {', '.join(self.context['top_customer_groups'])}
"""

        stage_prompts = {
            "business_context": """Focus on understanding what the business does and their value proposition.
Ask clarifying questions about their core offering.""",

            "ideal_customer": """Now focus on defining their ideal customer:
- What industries are their best customers in?
- What problems do they solve for customers?
- What makes a customer a "good fit"?""",

            "company_size": """Understand target company size:
- Employee count range
- Revenue range
- Company stage (startup, growth, enterprise)""",

            "personas": """Define the buyer personas:
- Job titles they typically sell to
- Decision maker vs user vs influencer
- Departments involved in purchase"""
        }

        return base + stage_prompts.get(stage, "")

    def _extract_icp_data(self, conversation: list) -> dict:
        """Extract structured ICP data from conversation"""

        extraction_prompt = """Based on this conversation, extract the Ideal Customer Profile in JSON:

{
    "industries": ["industry1", "industry2"],
    "company_size": {"employees_min": X, "employees_max": Y},
    "revenue_range": {"min": X, "max": Y},
    "geographic": {"countries": [], "states": [], "cities": []},
    "personas": [{"title": "", "department": "", "seniority": ""}],
    "icp_criteria": {"must_have": [], "nice_to_have": []},
    "campaign_offer": ""
}"""

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": extraction_prompt},
                {"role": "user", "content": str(conversation)}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### Campaign Tracking via CRM Events

```python
# events/crm_events.py

def on_lead_create(doc, method):
    """Track lead creation in campaign"""
    if doc.campaign:
        campaign = frappe.get_doc("Campaign", doc.campaign)
        campaign.leads_created = (campaign.leads_created or 0) + 1
        campaign.save(ignore_permissions=True)

def on_lead_update(doc, method):
    """Track lead qualification"""
    if not doc.campaign:
        return

    # Check if lead was qualified (status changed)
    if doc.has_value_changed("status"):
        if doc.status == "Qualified":
            campaign = frappe.get_doc("Campaign", doc.campaign)
            campaign.leads_qualified = (campaign.leads_qualified or 0) + 1
            campaign.save(ignore_permissions=True)

def on_deal_update(doc, method):
    """Track deal conversions and wins"""
    # Find associated lead
    lead = frappe.get_value("Lead", {"email_id": doc.email_id}, "campaign")
    if not lead:
        return

    campaign = frappe.get_doc("Campaign", lead)

    # Track new deals
    if doc.is_new():
        campaign.deals_created = (campaign.deals_created or 0) + 1

    # Track won deals
    if doc.has_value_changed("status") and doc.status == "Won":
        campaign.deals_won = (campaign.deals_won or 0) + 1
        campaign.revenue_generated = (campaign.revenue_generated or 0) + doc.deal_value

        # Recalculate metrics
        campaign.cost_per_lead = campaign.spent / max(campaign.leads_created, 1)
        campaign.roi = ((campaign.revenue_generated - campaign.spent) /
                        max(campaign.spent, 1)) * 100

    campaign.save(ignore_permissions=True)
```

---

**Next: Section 7 - HR Overlay Architecture**

# Dartwing Company Architecture - Section 7: HR Overlay

_Overlay architecture that enhances Frappe HRMS without modifying it._

---

## 7.1 HRMS Integration Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HRMS INTEGRATION MODEL                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       OUR DOCTYPES (dartwing_company)                        │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Shift Template │  │ Schedule Entry │  │ Work Location  │                │
│  │                │  │                │  │                │                │
│  │ • Our config   │  │ • Our assignment│ │ • Geofences   │                │
│  │ • Maps to HRMS │  │ • Syncs to HRMS│  │ • Validation  │                │
│  └───────┬────────┘  └───────┬────────┘  └────────────────┘                │
│          │                   │                                              │
│  ┌───────┴────────┐  ┌───────┴────────┐                                    │
│  │ Shift Swap     │  │ Employee       │                                    │
│  │ Request        │  │ Certification  │                                    │
│  └────────────────┘  └────────────────┘                                    │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              │ SYNC / LINK
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                          FRAPPE HRMS DOCTYPES                                │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Employee       │  │ Shift Type     │  │ Shift          │                │
│  │                │  │                │  │ Assignment     │                │
│  │ • Master data  │  │ • Base config  │  │ • Official     │                │
│  │ • Custom fields│  │ • Start/end    │  │   schedule     │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ Attendance     │  │ Leave          │  │ Holiday List   │                │
│  │                │  │ Application    │  │                │                │
│  │ • Clock data   │  │ • Time off     │  │ • Company      │                │
│  │ • Custom fields│  │                │  │   holidays     │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7.2 Shift Scheduling Architecture

### Schedule Builder Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SCHEDULE BUILDER ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           UI: SCHEDULE BUILDER                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │               WEEK VIEW: Dec 2-8, 2025                               │    │
│  │  ┌─────────────────────────────────────────────────────────────────┐│    │
│  │  │Employee   │ Mon    │ Tue    │ Wed    │ Thu    │ Fri    │ Sat   ││    │
│  │  ├───────────┼────────┼────────┼────────┼────────┼────────┼───────┤│    │
│  │  │Carlos R.  │[Morning]│[Morning]│  OFF  │[Morning]│[Morning]│ OFF  ││    │
│  │  │Maria S.   │[Evening]│[Evening]│[Evening]│  OFF  │[Evening]│ OFF  ││    │
│  │  │John D.    │[Morning]│  OFF  │[Morning]│[Morning]│[Morning]│[Sat] ││    │
│  │  └─────────────────────────────────────────────────────────────────┘│    │
│  │                                                                      │    │
│  │  [Copy from Last Week] [Auto-Fill] [Publish]                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

User drags shift onto cell
        │
        ▼
┌───────────────────┐
│ CREATE SCHEDULE   │
│ ENTRY             │
│ • employee        │────────────────────▶ HRMS Employee
│ • shift_template  │────────────────────▶ Our Shift Template
│ • date            │                       │
│ • work_location   │────────────────────▶ Our Work Location
└─────────┬─────────┘                       │
          │                                  │
          ▼                                  ▼
┌───────────────────┐              ┌───────────────────┐
│ VALIDATION        │              │ Shift Template    │
│                   │              │ • hrms_shift_type │──▶ HRMS Shift Type
│ • Check employee  │              └───────────────────┘
│   availability    │
│ • Check certs     │
│ • Check conflicts │
└─────────┬─────────┘
          │
          │ On Publish
          ▼
┌───────────────────┐
│ SYNC TO HRMS      │
│                   │
│ Create/Update     │────────────────────▶ HRMS Shift Assignment
│ Shift Assignment  │                      • employee
│                   │                      • shift_type
│                   │                      • start_date
│                   │                      • end_date
└───────────────────┘
```

### Schedule Builder Implementation

```python
# hr/scheduling/builder.py
class ScheduleBuilder:
    """Build and manage employee schedules"""

    def __init__(self, organization: str):
        self.org = organization

    def create_entry(self, employee: str, shift_template: str,
                     date: date, work_location: str = None) -> "ScheduleEntry":
        """Create a schedule entry with validation"""

        # Get employee from HRMS
        emp = frappe.get_doc("Employee", employee)
        template = frappe.get_doc("Shift Template", shift_template)

        # Validate availability
        self._validate_availability(emp, date)

        # Validate certifications for role
        if template.roles:
            self._validate_certifications(emp, template.roles, date)

        # Check for conflicts
        self._check_conflicts(emp, date, template)

        # Create entry
        entry = frappe.get_doc({
            "doctype": "Schedule Entry",
            "organization": self.org,
            "employee": employee,
            "shift_template": shift_template,
            "date": date,
            "start_time": template.start_time,
            "end_time": template.end_time,
            "work_location": work_location or template.default_location,
            "status": "Draft"
        })
        entry.insert()

        return entry

    def _validate_availability(self, employee: "Employee", date: date):
        """Check HRMS leave applications"""
        on_leave = frappe.db.exists("Leave Application", {
            "employee": employee.name,
            "from_date": ["<=", date],
            "to_date": [">=", date],
            "status": "Approved"
        })

        if on_leave:
            frappe.throw(f"{employee.employee_name} is on approved leave on {date}")

    def _validate_certifications(self, employee: "Employee",
                                  roles: list, date: date):
        """Check our Employee Certification DocType"""
        for role in roles:
            required_certs = frappe.get_all("Certification Requirement",
                filters={"role": role.role},
                pluck="certification_type"
            )

            for cert_type in required_certs:
                cert = frappe.get_value("Employee Certification", {
                    "employee": employee.name,
                    "certification_type": cert_type,
                    "expiry_date": [">=", date]
                }, "name")

                if not cert:
                    frappe.throw(
                        f"{employee.employee_name} lacks valid {cert_type} "
                        f"certification for {role.role}"
                    )

    def publish_schedule(self, start_date: date, end_date: date):
        """Publish schedule and sync to HRMS"""
        entries = frappe.get_all("Schedule Entry",
            filters={
                "organization": self.org,
                "date": ["between", [start_date, end_date]],
                "status": "Draft"
            }
        )

        for entry_name in entries:
            entry = frappe.get_doc("Schedule Entry", entry_name)

            # Sync to HRMS
            self._sync_to_hrms(entry)

            # Update status
            entry.status = "Published"
            entry.published_at = now()
            entry.save()

        # Notify employees
        self._notify_employees(start_date, end_date)

    def _sync_to_hrms(self, entry: "ScheduleEntry"):
        """Create/update HRMS Shift Assignment"""
        template = frappe.get_doc("Shift Template", entry.shift_template)

        # Check if assignment exists
        existing = frappe.get_value("Shift Assignment", {
            "employee": entry.employee,
            "start_date": entry.date,
            "shift_type": template.hrms_shift_type
        }, "name")

        if existing:
            # Update
            assignment = frappe.get_doc("Shift Assignment", existing)
            assignment.end_date = entry.date
            assignment.save()
        else:
            # Create
            assignment = frappe.get_doc({
                "doctype": "Shift Assignment",
                "employee": entry.employee,
                "shift_type": template.hrms_shift_type,
                "start_date": entry.date,
                "end_date": entry.date,
                "company": self.org
            })
            assignment.insert()

        # Link back
        entry.hrms_shift_assignment = assignment.name
        entry.synced_to_hrms = True
        entry.save()
```

### Shift Swap Marketplace

```python
# hr/scheduling/swap_marketplace.py
class SwapMarketplace:
    """Manage shift swap requests"""

    def create_swap_request(self, schedule_entry: str) -> "ShiftSwapRequest":
        """Employee requests to swap their shift"""
        entry = frappe.get_doc("Schedule Entry", schedule_entry)

        # Validate can be swapped
        if entry.status not in ["Published", "Confirmed"]:
            frappe.throw("Only published/confirmed shifts can be swapped")

        if entry.date <= today():
            frappe.throw("Cannot swap past or current day shifts")

        # Create request
        request = frappe.get_doc({
            "doctype": "Shift Swap Request",
            "organization": entry.organization,
            "requesting_employee": entry.employee,
            "original_schedule": entry.name,
            "shift_date": entry.date,
            "shift_template": entry.shift_template,
            "work_location": entry.work_location,
            "status": "Open"
        })
        request.insert()

        # Update schedule entry
        entry.swap_status = "Requested"
        entry.swap_request = request.name
        entry.save()

        # Notify potential swappers
        self._notify_potential_swappers(request)

        return request

    def offer_to_cover(self, swap_request: str,
                       offering_employee: str) -> "ShiftSwapRequest":
        """Another employee offers to cover the shift"""
        request = frappe.get_doc("Shift Swap Request", swap_request)
        entry = frappe.get_doc("Schedule Entry", request.original_schedule)
        template = frappe.get_doc("Shift Template", entry.shift_template)

        # Validate offerer qualifications
        offerer = frappe.get_doc("Employee", offering_employee)

        # Check certifications
        if template.roles:
            self._validate_certifications(offerer, template.roles, entry.date)

        # Check not already scheduled
        existing = frappe.db.exists("Schedule Entry", {
            "employee": offering_employee,
            "date": entry.date,
            "status": ["not in", ["Cancelled"]]
        })
        if existing:
            frappe.throw("You are already scheduled on this date")

        # Record offer
        request.offered_by = offering_employee
        request.offered_at = now()
        request.status = "Offered"
        request.save()

        # Notify requesting employee
        self._notify_offer_made(request)

        return request

    def approve_swap(self, swap_request: str, approver: str) -> "ShiftSwapRequest":
        """Manager approves the swap"""
        request = frappe.get_doc("Shift Swap Request", swap_request)

        if request.status != "Offered":
            frappe.throw("No offer to approve")

        original_entry = frappe.get_doc("Schedule Entry", request.original_schedule)

        # Update original entry to cancelled
        original_entry.status = "Cancelled"
        original_entry.swap_status = "Approved"
        original_entry.save()

        # Create new entry for covering employee
        new_entry = frappe.get_doc({
            "doctype": "Schedule Entry",
            "organization": original_entry.organization,
            "employee": request.offered_by,
            "shift_template": original_entry.shift_template,
            "date": original_entry.date,
            "start_time": original_entry.start_time,
            "end_time": original_entry.end_time,
            "work_location": original_entry.work_location,
            "status": "Published"
        })
        new_entry.insert()

        # Sync to HRMS
        builder = ScheduleBuilder(original_entry.organization)
        builder._sync_to_hrms(new_entry)

        # Remove old HRMS assignment
        if original_entry.hrms_shift_assignment:
            frappe.delete_doc("Shift Assignment",
                              original_entry.hrms_shift_assignment)

        # Update request
        request.status = "Approved"
        request.approved_by = approver
        request.approved_at = now()
        request.new_schedule_entry = new_entry.name
        request.save()

        # Notify both parties
        self._notify_swap_approved(request)

        return request
```

---

## 7.3 Geo Clock-In Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GEO CLOCK-IN ARCHITECTURE                               │
└─────────────────────────────────────────────────────────────────────────────┘

Mobile App: Employee taps "Clock In"
        │
        ▼
┌───────────────────┐
│ GET LOCATION      │
│ • GPS coordinates │
│ • Accuracy        │
│ • WiFi SSID       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────────────────────────────────────────────────┐
│                    VALIDATION ENGINE                           │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 1. Find scheduled Work Location for today               │  │
│  │    - Query Schedule Entry for employee + today          │  │
│  │    - Get Work Location from entry                       │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 2. Validate based on location's validation_mode         │  │
│  │                                                          │  │
│  │    GPS Mode:                                            │  │
│  │    • Calculate distance from location center            │  │
│  │    • distance <= geofence_radius_meters → VALID         │  │
│  │                                                          │  │
│  │    WiFi Mode:                                           │  │
│  │    • Check current SSID in allowed_wifi_networks        │  │
│  │    • Match found → VALID                                │  │
│  │                                                          │  │
│  │    QR Mode:                                             │  │
│  │    • Scan QR code at location                           │  │
│  │    • QR matches location.qr_code → VALID                │  │
│  │                                                          │  │
│  │    Any Mode:                                            │  │
│  │    • Any of above passes → VALID                        │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬─────────────────────────────────┘
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
          ▼ VALID                                 ▼ INVALID
┌───────────────────┐                   ┌───────────────────┐
│ CREATE ATTENDANCE │                   │ SHOW ERROR        │
│ (HRMS)            │                   │                   │
│                   │                   │ "You appear to be │
│ • employee        │                   │  outside the work │
│ • attendance_date │                   │  area"            │
│ • status: Present │                   │                   │
│ • in_time         │                   │ [Try Again]       │
│                   │                   │ [Request Override]│
│ + Custom Fields:  │                   └───────────────────┘
│ • clock_in_location│
│ • validation_method│
│ • validation_status│
└───────────────────┘
```

### Clock Manager Implementation

```python
# hr/attendance/clock_manager.py
from math import radians, cos, sin, asin, sqrt

class ClockManager:
    """Manage clock in/out with geo validation"""

    def __init__(self, organization: str):
        self.org = organization

    def clock_in(self, employee: str, latitude: float, longitude: float,
                 wifi_ssid: str = None, qr_code: str = None,
                 photo: str = None) -> dict:
        """Process clock in request"""

        emp = frappe.get_doc("Employee", employee)
        today = frappe.utils.today()

        # Check not already clocked in
        existing = frappe.get_value("Attendance", {
            "employee": employee,
            "attendance_date": today,
            "docstatus": ["<", 2]
        }, "name")

        if existing:
            att = frappe.get_doc("Attendance", existing)
            if att.in_time and not att.out_time:
                frappe.throw("Already clocked in")

        # Get scheduled work location
        schedule = self._get_todays_schedule(employee)
        work_location = None

        if schedule:
            work_location = frappe.get_doc("Work Location", schedule.work_location)
        else:
            # Use employee's home location
            if emp.home_location:
                work_location = frappe.get_doc("Work Location", emp.home_location)

        # Validate location
        validation_result = self._validate_location(
            work_location=work_location,
            latitude=latitude,
            longitude=longitude,
            wifi_ssid=wifi_ssid,
            qr_code=qr_code
        )

        if not validation_result["valid"]:
            return {
                "success": False,
                "error": validation_result["reason"],
                "can_request_override": True
            }

        # Create or update HRMS Attendance
        attendance = self._create_attendance(
            employee=employee,
            in_time=now(),
            latitude=latitude,
            longitude=longitude,
            validation_method=validation_result["method"],
            photo=photo
        )

        return {
            "success": True,
            "attendance_id": attendance.name,
            "message": f"Clocked in at {now().strftime('%I:%M %p')}",
            "location": work_location.location_name if work_location else "Unknown"
        }

    def clock_out(self, employee: str, latitude: float, longitude: float,
                  wifi_ssid: str = None) -> dict:
        """Process clock out request"""

        today = frappe.utils.today()

        # Get today's attendance
        attendance = frappe.get_value("Attendance", {
            "employee": employee,
            "attendance_date": today,
            "docstatus": 0
        }, "name")

        if not attendance:
            frappe.throw("No clock-in found for today")

        att = frappe.get_doc("Attendance", attendance)

        if att.out_time:
            frappe.throw("Already clocked out")

        # Validate location (optional for clock out)
        # Update attendance
        att.out_time = now()
        att.clock_out_location = f"{latitude},{longitude}"
        att.working_hours = self._calculate_hours(att.in_time, att.out_time)
        att.save()

        return {
            "success": True,
            "attendance_id": att.name,
            "message": f"Clocked out at {now().strftime('%I:%M %p')}",
            "working_hours": att.working_hours
        }

    def _validate_location(self, work_location: "WorkLocation",
                           latitude: float, longitude: float,
                           wifi_ssid: str = None,
                           qr_code: str = None) -> dict:
        """Validate clock-in location"""

        if not work_location:
            # No location requirement
            return {"valid": True, "method": "none"}

        mode = work_location.validation_mode

        # GPS validation
        if mode in ["gps_only", "any"]:
            distance = self._haversine(
                latitude, longitude,
                work_location.latitude, work_location.longitude
            )

            if distance <= work_location.geofence_radius_meters:
                return {"valid": True, "method": "GPS"}

            if mode == "gps_only":
                return {
                    "valid": False,
                    "reason": f"You are {int(distance)}m from {work_location.location_name}. "
                              f"Must be within {work_location.geofence_radius_meters}m."
                }

        # WiFi validation
        if mode in ["wifi_only", "any"] and wifi_ssid:
            allowed_networks = [n.ssid for n in work_location.allowed_wifi_networks]

            if wifi_ssid in allowed_networks:
                return {"valid": True, "method": "WiFi"}

            if mode == "wifi_only":
                return {
                    "valid": False,
                    "reason": "Not connected to authorized WiFi network"
                }

        # QR validation
        if mode in ["qr_only", "any"] and qr_code:
            if qr_code == work_location.qr_code:
                return {"valid": True, "method": "QR"}

            if mode == "qr_only":
                return {
                    "valid": False,
                    "reason": "Invalid QR code"
                }

        return {
            "valid": False,
            "reason": "Location validation failed"
        }

    def _haversine(self, lat1: float, lon1: float,
                   lat2: float, lon2: float) -> float:
        """Calculate distance between two points in meters"""
        R = 6371000  # Earth's radius in meters

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        return R * c

    def _create_attendance(self, employee: str, in_time: datetime,
                           latitude: float, longitude: float,
                           validation_method: str,
                           photo: str = None) -> "Attendance":
        """Create HRMS Attendance with custom fields"""

        attendance = frappe.get_doc({
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": in_time.date(),
            "status": "Present",
            "in_time": in_time,

            # Custom fields (via fixtures)
            "clock_in_location": f"{latitude},{longitude}",
            "validation_method": validation_method,
            "validation_status": "Verified"
        })

        if photo:
            attendance.clock_in_photo = photo

        attendance.insert()

        return attendance
```

### Anomaly Detection

```python
# hr/attendance/anomaly_detector.py
class AnomalyDetector:
    """Detect attendance anomalies"""

    RULES = [
        {
            "name": "long_shift",
            "condition": lambda att: att.working_hours and att.working_hours > 12,
            "severity": "warning",
            "message": "Shift exceeds 12 hours"
        },
        {
            "name": "early_clock_in",
            "condition": lambda att, sched: (
                sched and att.in_time.time() <
                (datetime.combine(date.today(), sched.start_time) -
                 timedelta(minutes=30)).time()
            ),
            "severity": "info",
            "message": "Clocked in more than 30 minutes early"
        },
        {
            "name": "location_mismatch",
            "condition": lambda att, sched: (
                sched and att.work_location and
                sched.work_location != att.work_location
            ),
            "severity": "warning",
            "message": "Location differs from scheduled location"
        },
        {
            "name": "missed_clock_out",
            "condition": lambda att: (
                att.in_time and not att.out_time and
                now() > datetime.combine(att.attendance_date,
                                         time(23, 59))
            ),
            "severity": "error",
            "message": "Missed clock out"
        }
    ]

    def detect_anomalies(self):
        """Run anomaly detection on recent attendance"""

        # Get yesterday's attendance
        yesterday = add_days(today(), -1)

        attendances = frappe.get_all("Attendance",
            filters={
                "attendance_date": yesterday,
                "docstatus": 0
            },
            fields=["name", "employee", "in_time", "out_time",
                    "working_hours", "clock_in_location", "validation_status"]
        )

        for att_data in attendances:
            att = frappe.get_doc("Attendance", att_data.name)

            # Get schedule for comparison
            schedule = frappe.get_value("Schedule Entry", {
                "employee": att.employee,
                "date": att.attendance_date
            }, ["start_time", "end_time", "work_location"], as_dict=True)

            for rule in self.RULES:
                try:
                    if rule["condition"](att, schedule):
                        self._flag_anomaly(att, rule)
                except:
                    continue

    def _flag_anomaly(self, attendance: "Attendance", rule: dict):
        """Flag attendance with anomaly"""

        # Update attendance status
        attendance.validation_status = "Flagged"
        attendance.add_comment("Comment", rule["message"])
        attendance.save()

        # Notify manager
        employee = frappe.get_doc("Employee", attendance.employee)
        if employee.reports_to:
            manager = frappe.get_value("Employee", employee.reports_to, "user_id")

            frappe.sendmail(
                recipients=[manager],
                subject=f"Attendance Anomaly: {employee.employee_name}",
                message=f"""
                Anomaly detected for {employee.employee_name} on {attendance.attendance_date}:

                {rule['message']}

                Please review the attendance record.
                """
            )
```

---

## 7.4 HRMS Sync Summary

| Our DocType            | HRMS DocType                | Sync Direction | Trigger    |
| ---------------------- | --------------------------- | -------------- | ---------- |
| Schedule Entry         | Shift Assignment            | Our → HRMS     | On publish |
| Shift Template         | Shift Type                  | Manual link    | Setup      |
| Geo Clock-In           | Attendance                  | Our → HRMS     | On clock   |
| Employee Certification | (Custom fields on Employee) | Read HRMS      | Reference  |
| Work Location          | (New concept)               | N/A            | N/A        |
| Shift Swap Request     | (Updates Shift Assignment)  | Our → HRMS     | On approve |

---

**Next: Section 8 - Flutter Mobile Architecture**

# Dartwing Company Architecture - Section 8: Flutter Mobile Architecture

_Integration with Dartwing Flutter app for mobile-first operations._

---

## 8.1 Flutter App Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DARTWING FLUTTER APP STRUCTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ COMPANY MODULE SCREENS                                               │    │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │    │
│  │  │  Inbox    │ │  Dispatch │ │   Forms   │ │  Schedule │           │    │
│  │  │  Screen   │ │   Map     │ │  Builder  │ │   View    │           │    │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │    │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │    │
│  │  │  Clock    │ │ Knowledge │ │   Swap    │ │   Job     │           │    │
│  │  │  In/Out   │ │   Base    │ │Marketplace│ │  Details  │           │    │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                         STATE MANAGEMENT (Bloc/Cubit)                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  InboxCubit │ DispatchCubit │ FormsCubit │ ScheduleCubit │ ClockCubit│   │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                         REPOSITORY LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ ConversationRepo │ DispatchRepo │ FormsRepo │ AttendanceRepo │ etc. │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                          DATA SOURCES                                        │
│  ┌───────────────────────────────┐  ┌───────────────────────────────────┐  │
│  │      REMOTE (Frappe API)      │  │        LOCAL (SQLite/Hive)        │  │
│  │  • REST API calls             │  │  • Offline cache                  │  │
│  │  • WebSocket realtime         │  │  • Pending sync queue             │  │
│  │  • File uploads               │  │  • Form drafts                    │  │
│  └───────────────────────────────┘  └───────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                      DARTWING FLUTTER CORE                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ DartwingApiClient │ AuthService │ SyncService │ LocationService     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8.2 Flutter Directory Structure

```
lib/
├── features/
│   └── company/                          # dartwing_company module
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── conversation_remote_datasource.dart
│       │   │   ├── conversation_local_datasource.dart
│       │   │   ├── dispatch_remote_datasource.dart
│       │   │   ├── dispatch_local_datasource.dart
│       │   │   ├── forms_remote_datasource.dart
│       │   │   ├── forms_local_datasource.dart
│       │   │   ├── attendance_remote_datasource.dart
│       │   │   ├── schedule_remote_datasource.dart
│       │   │   └── knowledge_remote_datasource.dart
│       │   ├── models/
│       │   │   ├── conversation_model.dart
│       │   │   ├── message_model.dart
│       │   │   ├── dispatch_job_model.dart
│       │   │   ├── mobile_form_model.dart
│       │   │   ├── form_submission_model.dart
│       │   │   ├── schedule_entry_model.dart
│       │   │   ├── attendance_model.dart
│       │   │   └── knowledge_article_model.dart
│       │   └── repositories/
│       │       ├── conversation_repository_impl.dart
│       │       ├── dispatch_repository_impl.dart
│       │       ├── forms_repository_impl.dart
│       │       ├── attendance_repository_impl.dart
│       │       └── schedule_repository_impl.dart
│       │
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── conversation.dart
│       │   │   ├── dispatch_job.dart
│       │   │   ├── mobile_form.dart
│       │   │   └── schedule_entry.dart
│       │   ├── repositories/
│       │   │   ├── conversation_repository.dart
│       │   │   ├── dispatch_repository.dart
│       │   │   └── forms_repository.dart
│       │   └── usecases/
│       │       ├── send_message.dart
│       │       ├── clock_in.dart
│       │       ├── submit_form.dart
│       │       └── update_job_status.dart
│       │
│       └── presentation/
│           ├── cubits/
│           │   ├── inbox/
│           │   │   ├── inbox_cubit.dart
│           │   │   └── inbox_state.dart
│           │   ├── dispatch/
│           │   │   ├── dispatch_cubit.dart
│           │   │   └── dispatch_state.dart
│           │   ├── forms/
│           │   │   ├── forms_cubit.dart
│           │   │   └── forms_state.dart
│           │   ├── clock/
│           │   │   ├── clock_cubit.dart
│           │   │   └── clock_state.dart
│           │   └── schedule/
│           │       ├── schedule_cubit.dart
│           │       └── schedule_state.dart
│           │
│           ├── screens/
│           │   ├── inbox/
│           │   │   ├── inbox_screen.dart
│           │   │   └── conversation_detail_screen.dart
│           │   ├── dispatch/
│           │   │   ├── dispatch_map_screen.dart
│           │   │   ├── job_list_screen.dart
│           │   │   └── job_detail_screen.dart
│           │   ├── forms/
│           │   │   ├── form_list_screen.dart
│           │   │   ├── form_fill_screen.dart
│           │   │   └── form_submission_screen.dart
│           │   ├── clock/
│           │   │   └── clock_screen.dart
│           │   ├── schedule/
│           │   │   ├── my_schedule_screen.dart
│           │   │   └── swap_marketplace_screen.dart
│           │   └── knowledge/
│           │       ├── knowledge_search_screen.dart
│           │       └── article_detail_screen.dart
│           │
│           └── widgets/
│               ├── conversation_tile.dart
│               ├── job_card.dart
│               ├── form_field_widget.dart
│               ├── signature_pad.dart
│               ├── photo_capture.dart
│               ├── location_validator.dart
│               └── schedule_calendar.dart
```

---

## 8.3 Key Flutter Implementations

### Clock In/Out Screen

```dart
// presentation/screens/clock/clock_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:geolocator/geolocator.dart';

class ClockScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ClockCubit(
        attendanceRepository: context.read<AttendanceRepository>(),
        locationService: context.read<LocationService>(),
      )..loadStatus(),
      child: ClockScreenContent(),
    );
  }
}

class ClockScreenContent extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Clock In/Out')),
      body: BlocBuilder<ClockCubit, ClockState>(
        builder: (context, state) {
          if (state is ClockLoading) {
            return Center(child: CircularProgressIndicator());
          }

          if (state is ClockError) {
            return _buildError(context, state.message);
          }

          if (state is ClockStatus) {
            return _buildClockUI(context, state);
          }

          return Container();
        },
      ),
    );
  }

  Widget _buildClockUI(BuildContext context, ClockStatus state) {
    final isClockedIn = state.isClockedIn;
    final currentTime = DateTime.now();

    return Padding(
      padding: EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Greeting
          Text(
            isClockedIn ? 'Welcome back!' : 'Good ${_getTimeOfDay()}!',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          SizedBox(height: 8),
          Text(
            state.employeeName,
            style: Theme.of(context).textTheme.titleLarge,
          ),

          SizedBox(height: 32),

          // Location status
          if (state.workLocation != null) ...[
            Icon(Icons.location_on, color: Colors.green),
            Text('📍 ${state.workLocation}'),
            Text(
              state.locationVerified ? '✓ Location Verified' : '⚠ Verifying...',
              style: TextStyle(
                color: state.locationVerified ? Colors.green : Colors.orange,
              ),
            ),
          ],

          SizedBox(height: 48),

          // Clock button
          GestureDetector(
            onTap: state.locationVerified
                ? () => _handleClockAction(context, isClockedIn)
                : null,
            child: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isClockedIn ? Colors.red : Colors.green,
                boxShadow: [
                  BoxShadow(
                    color: (isClockedIn ? Colors.red : Colors.green)
                        .withOpacity(0.3),
                    blurRadius: 20,
                    spreadRadius: 5,
                  ),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    isClockedIn ? Icons.logout : Icons.login,
                    size: 48,
                    color: Colors.white,
                  ),
                  SizedBox(height: 8),
                  Text(
                    isClockedIn ? 'CLOCK OUT' : 'CLOCK IN',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    DateFormat('h:mm a').format(currentTime),
                    style: TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
          ),

          SizedBox(height: 32),

          // Today's info
          if (isClockedIn && state.clockInTime != null) ...[
            Text('Clocked in at ${DateFormat('h:mm a').format(state.clockInTime!)}'),
            Text('Working: ${_formatDuration(currentTime.difference(state.clockInTime!))}'),
          ],

          // Schedule info
          if (state.todaySchedule != null) ...[
            SizedBox(height: 16),
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Text("Today's Schedule", style: TextStyle(fontWeight: FontWeight.bold)),
                    Text('${state.todaySchedule!.startTime} - ${state.todaySchedule!.endTime}'),
                    Text(state.todaySchedule!.shiftName),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  void _handleClockAction(BuildContext context, bool isClockedIn) {
    if (isClockedIn) {
      context.read<ClockCubit>().clockOut();
    } else {
      context.read<ClockCubit>().clockIn();
    }
  }
}
```

### Clock Cubit with Location Validation

```dart
// presentation/cubits/clock/clock_cubit.dart
class ClockCubit extends Cubit<ClockState> {
  final AttendanceRepository _attendanceRepo;
  final LocationService _locationService;

  ClockCubit({
    required AttendanceRepository attendanceRepository,
    required LocationService locationService,
  }) : _attendanceRepo = attendanceRepository,
       _locationService = locationService,
       super(ClockInitial());

  Future<void> loadStatus() async {
    emit(ClockLoading());

    try {
      // Get current attendance status
      final status = await _attendanceRepo.getTodayStatus();

      // Get current location
      final position = await _locationService.getCurrentPosition();

      // Get today's schedule
      final schedule = await _attendanceRepo.getTodaySchedule();

      // Validate location against work location
      bool locationVerified = false;
      String? workLocationName;

      if (schedule?.workLocation != null) {
        final validation = await _attendanceRepo.validateLocation(
          latitude: position.latitude,
          longitude: position.longitude,
          workLocationId: schedule!.workLocation!,
        );
        locationVerified = validation.isValid;
        workLocationName = validation.locationName;
      } else {
        // No location requirement
        locationVerified = true;
      }

      emit(ClockStatus(
        isClockedIn: status.isClockedIn,
        clockInTime: status.clockInTime,
        employeeName: status.employeeName,
        workLocation: workLocationName,
        locationVerified: locationVerified,
        todaySchedule: schedule,
      ));
    } catch (e) {
      emit(ClockError(message: e.toString()));
    }
  }

  Future<void> clockIn() async {
    final currentState = state;
    if (currentState is! ClockStatus) return;

    emit(ClockLoading());

    try {
      // Get fresh location
      final position = await _locationService.getCurrentPosition();

      // Get WiFi SSID if available
      final wifiInfo = await _locationService.getWifiInfo();

      // Call API
      final result = await _attendanceRepo.clockIn(
        latitude: position.latitude,
        longitude: position.longitude,
        wifiSsid: wifiInfo?.ssid,
      );

      if (result.success) {
        emit(ClockSuccess(message: result.message));
        await loadStatus(); // Refresh
      } else {
        emit(ClockError(
          message: result.error!,
          canRequestOverride: result.canRequestOverride,
        ));
      }
    } catch (e) {
      emit(ClockError(message: e.toString()));
    }
  }

  Future<void> clockOut() async {
    emit(ClockLoading());

    try {
      final position = await _locationService.getCurrentPosition();

      final result = await _attendanceRepo.clockOut(
        latitude: position.latitude,
        longitude: position.longitude,
      );

      if (result.success) {
        emit(ClockSuccess(message: result.message));
        await loadStatus();
      } else {
        emit(ClockError(message: result.error!));
      }
    } catch (e) {
      emit(ClockError(message: e.toString()));
    }
  }
}
```

### Dispatch Job Screen with Map

```dart
// presentation/screens/dispatch/dispatch_map_screen.dart
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class DispatchMapScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => DispatchCubit(
        dispatchRepository: context.read<DispatchRepository>(),
      )..loadJobs(),
      child: DispatchMapContent(),
    );
  }
}

class DispatchMapContent extends StatefulWidget {
  @override
  _DispatchMapContentState createState() => _DispatchMapContentState();
}

class _DispatchMapContentState extends State<DispatchMapContent> {
  GoogleMapController? _mapController;
  Set<Marker> _markers = {};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Jobs'),
        actions: [
          IconButton(
            icon: Icon(Icons.list),
            onPressed: () => Navigator.pushNamed(context, '/jobs/list'),
          ),
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () => context.read<DispatchCubit>().loadJobs(),
          ),
        ],
      ),
      body: BlocConsumer<DispatchCubit, DispatchState>(
        listener: (context, state) {
          if (state is DispatchLoaded) {
            _updateMarkers(state.jobs);
          }
        },
        builder: (context, state) {
          if (state is DispatchLoading) {
            return Center(child: CircularProgressIndicator());
          }

          if (state is DispatchLoaded) {
            return Stack(
              children: [
                // Map
                GoogleMap(
                  initialCameraPosition: CameraPosition(
                    target: _getInitialPosition(state.jobs),
                    zoom: 12,
                  ),
                  markers: _markers,
                  myLocationEnabled: true,
                  onMapCreated: (controller) => _mapController = controller,
                ),

                // Job cards at bottom
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: _buildJobCards(state.jobs),
                ),
              ],
            );
          }

          return Container();
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _optimizeRoute(context),
        icon: Icon(Icons.route),
        label: Text('Optimize Route'),
      ),
    );
  }

  void _updateMarkers(List<DispatchJob> jobs) {
    setState(() {
      _markers = jobs.map((job) {
        return Marker(
          markerId: MarkerId(job.id),
          position: LatLng(job.latitude, job.longitude),
          infoWindow: InfoWindow(
            title: job.title,
            snippet: job.customerName,
          ),
          icon: _getMarkerIcon(job.status),
          onTap: () => _showJobDetail(job),
        );
      }).toSet();
    });
  }

  Widget _buildJobCards(List<DispatchJob> jobs) {
    return Container(
      height: 150,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.all(8),
        itemCount: jobs.length,
        itemBuilder: (context, index) {
          final job = jobs[index];
          return _JobCard(
            job: job,
            onTap: () => _navigateToJob(job),
            onNavigate: () => _launchNavigation(job),
          );
        },
      ),
    );
  }
}

class _JobCard extends StatelessWidget {
  final DispatchJob job;
  final VoidCallback onTap;
  final VoidCallback onNavigate;

  const _JobCard({
    required this.job,
    required this.onTap,
    required this.onNavigate,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.only(right: 12),
      child: Container(
        width: 280,
        padding: EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                _StatusBadge(status: job.status),
                Spacer(),
                Text(job.scheduledTime, style: TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            SizedBox(height: 8),
            Text(job.title, style: Theme.of(context).textTheme.titleMedium),
            Text(job.customerName),
            Text(job.address, maxLines: 1, overflow: TextOverflow.ellipsis),
            Spacer(),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: onTap,
                    child: Text('Details'),
                  ),
                ),
                SizedBox(width: 8),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: onNavigate,
                    icon: Icon(Icons.navigation, size: 16),
                    label: Text('Go'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

### Offline Form Submission

```dart
// data/datasources/forms_local_datasource.dart
import 'package:sqflite/sqflite.dart';

class FormsLocalDatasource {
  final Database _db;

  FormsLocalDatasource(this._db);

  /// Save form submission locally when offline
  Future<void> saveOfflineSubmission(FormSubmission submission) async {
    await _db.insert(
      'offline_submissions',
      {
        'id': submission.id,
        'form_id': submission.formId,
        'data': jsonEncode(submission.data),
        'photos': jsonEncode(submission.photos),
        'signature': submission.signature,
        'location': jsonEncode(submission.location),
        'created_at': submission.createdAt.toIso8601String(),
        'sync_status': 'pending',
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  /// Get all pending submissions
  Future<List<FormSubmission>> getPendingSubmissions() async {
    final rows = await _db.query(
      'offline_submissions',
      where: 'sync_status = ?',
      whereArgs: ['pending'],
    );

    return rows.map((row) => FormSubmission.fromJson(row)).toList();
  }

  /// Mark submission as synced
  Future<void> markSynced(String submissionId) async {
    await _db.update(
      'offline_submissions',
      {'sync_status': 'synced'},
      where: 'id = ?',
      whereArgs: [submissionId],
    );
  }

  /// Cache form schemas for offline use
  Future<void> cacheForms(List<MobileForm> forms) async {
    final batch = _db.batch();

    for (final form in forms) {
      batch.insert(
        'cached_forms',
        {
          'id': form.id,
          'name': form.name,
          'schema': jsonEncode(form.schema),
          'cached_at': DateTime.now().toIso8601String(),
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }

    await batch.commit();
  }

  /// Get cached form by ID
  Future<MobileForm?> getCachedForm(String formId) async {
    final rows = await _db.query(
      'cached_forms',
      where: 'id = ?',
      whereArgs: [formId],
    );

    if (rows.isEmpty) return null;
    return MobileForm.fromJson(rows.first);
  }
}

// Sync service
class FormSyncService {
  final FormsLocalDatasource _localDs;
  final FormsRemoteDatasource _remoteDs;
  final ConnectivityService _connectivity;

  FormSyncService(this._localDs, this._remoteDs, this._connectivity);

  /// Sync all pending submissions when online
  Future<SyncResult> syncPendingSubmissions() async {
    if (!await _connectivity.isOnline) {
      return SyncResult(synced: 0, failed: 0, pending: -1);
    }

    final pending = await _localDs.getPendingSubmissions();
    int synced = 0;
    int failed = 0;

    for (final submission in pending) {
      try {
        // Upload photos first
        final uploadedPhotos = <String>[];
        for (final photoPath in submission.photos) {
          final url = await _remoteDs.uploadPhoto(photoPath);
          uploadedPhotos.add(url);
        }

        // Submit form
        await _remoteDs.submitForm(
          submission.copyWith(photos: uploadedPhotos),
        );

        await _localDs.markSynced(submission.id);
        synced++;
      } catch (e) {
        failed++;
        // Log error but continue with next
      }
    }

    return SyncResult(synced: synced, failed: failed, pending: pending.length - synced);
  }
}
```

---

## 8.4 API Integration

### Remote Datasource Pattern

```dart
// data/datasources/attendance_remote_datasource.dart
class AttendanceRemoteDatasource {
  final DartwingApiClient _client;

  AttendanceRemoteDatasource(this._client);

  Future<ClockResult> clockIn({
    required double latitude,
    required double longitude,
    String? wifiSsid,
    String? qrCode,
    String? photoPath,
  }) async {
    // Upload photo if provided
    String? photoUrl;
    if (photoPath != null) {
      photoUrl = await _client.uploadFile(photoPath);
    }

    final response = await _client.post(
      'dartwing_company.api.v1.attendance.clock_in',
      data: {
        'latitude': latitude,
        'longitude': longitude,
        'wifi_ssid': wifiSsid,
        'qr_code': qrCode,
        'photo': photoUrl,
      },
    );

    return ClockResult.fromJson(response.data);
  }

  Future<ClockResult> clockOut({
    required double latitude,
    required double longitude,
  }) async {
    final response = await _client.post(
      'dartwing_company.api.v1.attendance.clock_out',
      data: {
        'latitude': latitude,
        'longitude': longitude,
      },
    );

    return ClockResult.fromJson(response.data);
  }

  Future<AttendanceStatus> getTodayStatus() async {
    final response = await _client.get(
      'dartwing_company.api.v1.attendance.status',
    );

    return AttendanceStatus.fromJson(response.data);
  }

  Future<LocationValidation> validateLocation({
    required double latitude,
    required double longitude,
    required String workLocationId,
  }) async {
    final response = await _client.post(
      'dartwing_company.api.v1.attendance.validate_location',
      data: {
        'latitude': latitude,
        'longitude': longitude,
        'work_location': workLocationId,
      },
    );

    return LocationValidation.fromJson(response.data);
  }
}
```

### Push Notifications

```dart
// services/push_notification_service.dart
class CompanyPushNotificationService {
  final FirebaseMessaging _fcm;
  final FlutterLocalNotificationsPlugin _localNotifications;

  Future<void> initialize() async {
    // Request permission
    await _fcm.requestPermission();

    // Get token and register with backend
    final token = await _fcm.getToken();
    await _registerToken(token);

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

    // Handle background messages
    FirebaseMessaging.onBackgroundMessage(_handleBackgroundMessage);

    // Handle notification taps
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);
  }

  void _handleForegroundMessage(RemoteMessage message) {
    final type = message.data['type'];

    switch (type) {
      case 'new_job':
        _showJobNotification(message);
        break;
      case 'new_message':
        _showMessageNotification(message);
        break;
      case 'schedule_change':
        _showScheduleNotification(message);
        break;
      case 'swap_request':
        _showSwapNotification(message);
        break;
    }
  }

  void _showJobNotification(RemoteMessage message) {
    final jobId = message.data['job_id'];
    final title = message.data['title'];
    final address = message.data['address'];

    _localNotifications.show(
      jobId.hashCode,
      'New Job Assignment',
      '$title at $address',
      NotificationDetails(
        android: AndroidNotificationDetails(
          'jobs',
          'Job Notifications',
          importance: Importance.high,
          priority: Priority.high,
        ),
      ),
      payload: 'job:$jobId',
    );
  }
}
```

---

**Next: Section 9 - API Architecture**
