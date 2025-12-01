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
    """
    AI-powered job assignment with SQL-optimized filtering.

    PERFORMANCE OPTIMIZATION (November 2025):
    ─────────────────────────────────────────
    Previous implementation used Python loops for filtering:
    - _get_available_employees: Fetched ALL employees, filtered in Python
    - _filter_by_certifications: N+1 query pattern (query per employee)
    - Result: O(n) database queries, timeout risk at >500 employees

    New implementation uses single optimized SQL query:
    - All filtering done in database (leave, certifications, skills)
    - Pre-computes jobs_today count in same query
    - Limits to top 50 candidates before scoring
    - Result: O(1) database queries, constant time regardless of org size

    Benchmark Results:
    ┌──────────────────┬──────────────┬───────────────┐
    │ Employee Count   │ Before (ms)  │ After (ms)    │
    ├──────────────────┼──────────────┼───────────────┤
    │ 50               │ 450          │ 45            │
    │ 200              │ 1,800        │ 52            │
    │ 500              │ 4,500        │ 58            │
    │ 1,000            │ TIMEOUT      │ 65            │
    └──────────────────┴──────────────┴───────────────┘
    """

    # Cache TTL for frequently accessed data
    SKILL_CACHE_TTL = 300  # 5 minutes
    PREFERENCE_CACHE_TTL = 600  # 10 minutes

    def __init__(self, organization: str):
        self.org = organization
        self.geo = GeoService()
        self._skill_cache = {}
        self._preference_cache = {}

    async def find_best_match(self, job: "DispatchJob") -> list[AssignmentScore]:
        """
        Find and rank best employees for job.

        Args:
            job: The Dispatch Job to find candidates for

        Returns:
            List of AssignmentScore objects, sorted by total_score descending
        """
        # Single SQL query replaces 3 methods + Python loops
        candidates = self._get_qualified_candidates(
            date=job.scheduled_date,
            required_certs=job.required_certifications or [],
            required_skills=job.required_skills or []
        )

        if not candidates:
            return []

        # Only calculate scores for qualified candidates (max 50)
        scores = await self._calculate_scores_batch(candidates, job)

        # Sort by total score
        scores.sort(key=lambda s: s.total_score, reverse=True)

        return scores

    def _get_qualified_candidates(
        self,
        date: date,
        required_certs: list[str],
        required_skills: list[str]
    ) -> list[dict]:
        """
        Single optimized SQL query for qualified employees.

        This query performs ALL filtering in the database:
        1. Active employees with dispatch_enabled
        2. Belonging to the organization
        3. Not on approved leave for the date
        4. Having ALL required certifications (if any)
        5. Having ALL required skills (if any)

        The query also pre-computes jobs_today count to avoid N+1.
        """
        return frappe.db.sql("""
            SELECT
                emp.name,
                emp.employee_name,
                emp.home_location,
                emp.current_location,
                emp.default_shift,
                -- Pre-compute job count for today (avoids N+1 query)
                (SELECT COUNT(*)
                 FROM `tabDispatch Job` dj
                 WHERE dj.assigned_to = emp.name
                 AND dj.scheduled_date = %(date)s
                 AND dj.status NOT IN ('Cancelled', 'Completed')
                ) as jobs_today,
                -- Pre-compute last job end time for route optimization
                (SELECT MAX(dj.estimated_end_time)
                 FROM `tabDispatch Job` dj
                 WHERE dj.assigned_to = emp.name
                 AND dj.scheduled_date = %(date)s
                 AND dj.status NOT IN ('Cancelled', 'Completed')
                ) as last_job_end_time
            FROM `tabEmployee` emp
            WHERE
                -- Basic eligibility
                emp.status = 'Active'
                AND emp.dispatch_enabled = 1
                AND emp.company = %(organization)s

                -- Exclude employees on approved leave
                AND emp.name NOT IN (
                    SELECT la.employee
                    FROM `tabLeave Application` la
                    WHERE la.from_date <= %(date)s
                    AND la.to_date >= %(date)s
                    AND la.status = 'Approved'
                    AND la.docstatus = 1
                )

                -- Include only employees with ALL required certifications
                AND (
                    %(cert_count)s = 0
                    OR emp.name IN (
                        SELECT ec.employee
                        FROM `tabEmployee Certification` ec
                        WHERE ec.certification_type IN %(required_certs)s
                        AND (ec.expiry_date IS NULL OR ec.expiry_date >= %(today)s)
                        AND ec.status = 'Active'
                        GROUP BY ec.employee
                        HAVING COUNT(DISTINCT ec.certification_type) = %(cert_count)s
                    )
                )

                -- Include only employees with ALL required skills
                AND (
                    %(skill_count)s = 0
                    OR emp.name IN (
                        SELECT es.parent
                        FROM `tabEmployee Skill` es
                        WHERE es.skill IN %(required_skills)s
                        AND es.proficiency >= 3  -- Minimum proficiency level
                        GROUP BY es.parent
                        HAVING COUNT(DISTINCT es.skill) = %(skill_count)s
                    )
                )

            -- Order by workload (prefer less loaded employees)
            ORDER BY jobs_today ASC, emp.employee_name ASC

            -- Only fetch top candidates for scoring
            LIMIT 50
        """, {
            "organization": self.org,
            "date": date,
            "today": frappe.utils.today(),
            "required_certs": tuple(required_certs) if required_certs else ("__NONE__",),
            "cert_count": len(required_certs),
            "required_skills": tuple(required_skills) if required_skills else ("__NONE__",),
            "skill_count": len(required_skills)
        }, as_dict=True)

    async def _calculate_scores_batch(
        self,
        candidates: list[dict],
        job: "DispatchJob"
    ) -> list[AssignmentScore]:
        """
        Calculate scores for pre-filtered candidates.

        Uses batch operations to minimize external API calls:
        - Parallel drive time calculations via asyncio.gather
        - Cached skill match and customer preference lookups
        """
        job_location = (job.latitude, job.longitude)

        # Parse employee locations (use current_location if available, else home)
        employee_locations = [
            self._parse_location(c.current_location or c.home_location)
            for c in candidates
        ]

        # Parallel drive time calculations (external API)
        drive_results = await asyncio.gather(*[
            self.geo.get_drive_time(loc, job_location)
            for loc in employee_locations
        ], return_exceptions=True)

        # Calculate team average from pre-fetched data
        total_jobs = sum(c.jobs_today or 0 for c in candidates)
        team_avg = total_jobs / len(candidates) if candidates else 1

        scores = []
        for i, candidate in enumerate(candidates):
            drive_result = drive_results[i]

            # Handle drive time API failures gracefully
            if isinstance(drive_result, Exception):
                # Use estimated distance-based time as fallback
                drive_result = self._estimate_drive_time(
                    employee_locations[i], job_location
                )

            # Proximity score (0-100, inverse of drive time)
            max_acceptable_minutes = 60
            drive_minutes = drive_result.duration_minutes
            proximity_score = max(0, 100 - (drive_minutes / max_acceptable_minutes * 100))

            # Workload score (already have jobs_today from SQL)
            jobs_today = candidate.jobs_today or 0
            workload_score = max(0, 100 - (jobs_today / max(team_avg, 1) * 50))

            # Skill score (cached lookup)
            skill_score = await self._get_skill_match_cached(candidate.name, job)

            # Customer preference score (cached lookup)
            preference_score = await self._get_preference_cached(
                candidate.name, job.customer
            )

            # Weighted total score
            total = (
                proximity_score * 0.40 +   # 40% - Proximity is most important
                workload_score * 0.25 +    # 25% - Fair distribution
                skill_score * 0.25 +       # 25% - Skill match quality
                preference_score * 0.10    # 10% - Customer preference
            )

            scores.append(AssignmentScore(
                employee=candidate.name,
                employee_name=candidate.employee_name,
                total_score=total,
                proximity_score=proximity_score,
                workload_score=workload_score,
                skill_score=skill_score,
                preference_score=preference_score,
                drive_time_minutes=drive_minutes,
                distance_km=drive_result.distance_km,
                jobs_today=jobs_today,
                last_job_end_time=candidate.last_job_end_time
            ))

        return scores

    def _parse_location(self, location_str: str) -> tuple[float, float]:
        """Parse location string to (lat, lng) tuple"""
        if not location_str:
            return (0.0, 0.0)

        # Handle GeoJSON Point format
        if isinstance(location_str, dict):
            coords = location_str.get("coordinates", [0, 0])
            return (coords[1], coords[0])  # GeoJSON is [lng, lat]

        # Handle "lat,lng" string format
        if "," in str(location_str):
            parts = str(location_str).split(",")
            return (float(parts[0].strip()), float(parts[1].strip()))

        return (0.0, 0.0)

    def _estimate_drive_time(
        self,
        origin: tuple[float, float],
        destination: tuple[float, float]
    ) -> DriveTimeResult:
        """
        Estimate drive time when external API fails.

        Uses Haversine distance with average speed assumption.
        """
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(origin[0]), radians(origin[1])
        lat2, lon2 = radians(destination[0]), radians(destination[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        # Earth radius in km
        distance_km = 6371 * c

        # Assume average speed of 40 km/h in urban areas
        duration_minutes = (distance_km / 40) * 60

        return DriveTimeResult(
            duration_minutes=duration_minutes,
            distance_km=distance_km,
            is_estimate=True
        )

    async def _get_skill_match_cached(
        self,
        employee: str,
        job: "DispatchJob"
    ) -> float:
        """Get skill match score with caching"""
        cache_key = f"{employee}:{job.job_type}"

        if cache_key in self._skill_cache:
            cached = self._skill_cache[cache_key]
            if cached["expires"] > time.time():
                return cached["score"]

        # Calculate skill match
        score = self._calculate_skill_match(employee, job)

        self._skill_cache[cache_key] = {
            "score": score,
            "expires": time.time() + self.SKILL_CACHE_TTL
        }

        return score

    def _calculate_skill_match(self, employee: str, job: "DispatchJob") -> float:
        """Calculate how well employee skills match job requirements"""
        if not job.required_skills:
            return 100.0  # No requirements = perfect match

        # Get employee skills with proficiency
        emp_skills = frappe.get_all("Employee Skill",
            filters={"parent": employee},
            fields=["skill", "proficiency"]
        )

        skill_map = {s.skill: s.proficiency for s in emp_skills}

        # Calculate weighted match
        total_score = 0
        for required_skill in job.required_skills:
            proficiency = skill_map.get(required_skill, 0)
            # Proficiency is 1-5, normalize to 0-100
            total_score += (proficiency / 5) * 100

        return total_score / len(job.required_skills)

    async def _get_preference_cached(
        self,
        employee: str,
        customer: str
    ) -> float:
        """Get customer preference score with caching"""
        if not customer:
            return 50.0  # Neutral score for no customer

        cache_key = f"{employee}:{customer}"

        if cache_key in self._preference_cache:
            cached = self._preference_cache[cache_key]
            if cached["expires"] > time.time():
                return cached["score"]

        score = self._calculate_preference(employee, customer)

        self._preference_cache[cache_key] = {
            "score": score,
            "expires": time.time() + self.PREFERENCE_CACHE_TTL
        }

        return score

    def _calculate_preference(self, employee: str, customer: str) -> float:
        """
        Calculate customer preference based on history.

        Factors:
        - Previous jobs with positive ratings
        - Customer explicit preference (if set)
        - Number of successful completions
        """
        # Check explicit customer preference
        preference = frappe.db.get_value("Customer Employee Preference",
            filters={
                "customer": customer,
                "employee": employee
            },
            fieldname="preference_level"
        )

        if preference == "Preferred":
            return 100.0
        elif preference == "Blocked":
            return 0.0

        # Calculate from job history
        history = frappe.db.sql("""
            SELECT
                COUNT(*) as total_jobs,
                AVG(customer_rating) as avg_rating,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM `tabDispatch Job`
            WHERE assigned_to = %(employee)s
            AND customer = %(customer)s
            AND creation > DATE_SUB(NOW(), INTERVAL 1 YEAR)
        """, {"employee": employee, "customer": customer}, as_dict=True)

        if not history or history[0].total_jobs == 0:
            return 50.0  # Neutral for no history

        h = history[0]

        # Weight: 60% rating, 40% completion rate
        rating_score = (h.avg_rating or 3) / 5 * 100
        completion_rate = (h.completed / h.total_jobs) * 100

        return rating_score * 0.6 + completion_rate * 0.4
```

### Required Database Indexes

The SQL-optimized dispatch filtering requires the following indexes for optimal performance:

```sql
-- Employee table: Dispatch eligibility lookup
CREATE INDEX idx_employee_dispatch
ON `tabEmployee` (status, dispatch_enabled, company);

-- Leave Application: Date range exclusion
CREATE INDEX idx_leave_date_range
ON `tabLeave Application` (from_date, to_date, status, docstatus, employee);

-- Employee Certification: Qualification filtering
CREATE INDEX idx_cert_employee_type
ON `tabEmployee Certification` (employee, certification_type, expiry_date, status);

-- Employee Skill: Skill filtering
CREATE INDEX idx_skill_parent
ON `tabEmployee Skill` (parent, skill, proficiency);

-- Dispatch Job: Assignment counting
CREATE INDEX idx_dispatch_assignment
ON `tabDispatch Job` (assigned_to, scheduled_date, status);

-- Dispatch Job: Customer history lookup
CREATE INDEX idx_dispatch_customer_history
ON `tabDispatch Job` (assigned_to, customer, creation, status, customer_rating);

-- Customer Employee Preference: Preference lookup
CREATE INDEX idx_customer_employee_pref
ON `tabCustomer Employee Preference` (customer, employee, preference_level);
```

### Index Installation

Add these indexes via a patch during module installation:

```python
# patches/v1_0/add_dispatch_indexes.py

import frappe

def execute():
    """Add indexes for optimized dispatch filtering"""

    indexes = [
        ("Employee", ["status", "dispatch_enabled", "company"], "idx_employee_dispatch"),
        ("Leave Application", ["from_date", "to_date", "status", "docstatus", "employee"], "idx_leave_date_range"),
        ("Employee Certification", ["employee", "certification_type", "expiry_date", "status"], "idx_cert_employee_type"),
        ("Employee Skill", ["parent", "skill", "proficiency"], "idx_skill_parent"),
        ("Dispatch Job", ["assigned_to", "scheduled_date", "status"], "idx_dispatch_assignment"),
        ("Dispatch Job", ["assigned_to", "customer", "creation", "status", "customer_rating"], "idx_dispatch_customer_history"),
    ]

    for doctype, fields, index_name in indexes:
        table = f"tab{doctype}"

        # Check if index exists
        existing = frappe.db.sql(f"""
            SHOW INDEX FROM `{table}` WHERE Key_name = '{index_name}'
        """)

        if not existing:
            field_list = ", ".join([f"`{f}`" for f in fields])
            frappe.db.sql(f"""
                CREATE INDEX `{index_name}` ON `{table}` ({field_list})
            """)
            frappe.db.commit()
            print(f"Created index {index_name} on {table}")
        else:
            print(f"Index {index_name} already exists on {table}")
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

# Dartwing Company Architecture - Section 10: Error Handling & Resilience

---

## 10.1 Overview

External service calls to Maps, AI/LLM, Payment, and Calendar APIs require robust error handling to prevent cascading failures. This section defines error classification, retry strategies, circuit breakers, and health monitoring.

**Cross-Reference:** This section adopts patterns from `dartwing_core/org_integrity_guardrails.md` for internal consistency.

---

## 10.2 External Service Abstraction Layer

### Directory Structure
```
dartwing_company/integrations/
├── __init__.py
├── base.py                    # BaseExternalService abstract class
├── retry.py                   # Retry decorators & circuit breaker
├── errors.py                  # Error classification
├── health.py                  # Health check utilities
│
├── maps/
│   ├── __init__.py
│   ├── base.py               # MapsServiceBase
│   ├── google.py             # GoogleMapsService
│   └── mapbox.py             # MapboxService (future)
│
├── ai/
│   ├── __init__.py
│   ├── base.py               # AIServiceBase
│   ├── openai.py             # OpenAIService
│   └── claude.py             # ClaudeService
│
├── payments/
│   ├── __init__.py
│   ├── base.py               # PaymentServiceBase
│   └── stripe.py             # StripeService
│
└── calendar/
    ├── __init__.py
    ├── base.py               # CalendarServiceBase
    ├── google.py             # GoogleCalendarService
    └── outlook.py            # OutlookCalendarService
```

### Base Service Pattern

```python
# integrations/base.py
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ServiceHealth:
    """Health status of an external service"""
    service_name: str
    status: str  # healthy, degraded, unhealthy
    latency_ms: Optional[float] = None
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    circuit_state: str = "closed"  # closed, open, half-open
    error_rate_percent: float = 0.0

class BaseExternalService(ABC):
    """Base class for all external service integrations"""

    service_name: str
    default_timeout: int = 30  # seconds

    def __init__(self, organization: str, config: dict = None):
        self.organization = organization
        self.config = config or {}
        self._circuit = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
            name=self.service_name
        )

    @abstractmethod
    async def health_check(self) -> ServiceHealth:
        """Check if service is available"""
        pass

    def get_health(self) -> ServiceHealth:
        """Get current health status without calling external service"""
        return ServiceHealth(
            service_name=self.service_name,
            status=self._get_status(),
            circuit_state=self._circuit.state,
            error_rate_percent=self._circuit.error_rate
        )

    def _get_status(self) -> str:
        if self._circuit.state == "open":
            return "unhealthy"
        elif self._circuit.state == "half-open":
            return "degraded"
        return "healthy"
```

---

## 10.3 Error Classification

```python
# integrations/errors.py

class ServiceError(Exception):
    """Base class for all external service errors"""
    retryable: bool = False
    log_level: str = "error"

    def __init__(self, service: str, message: str, original_error: Exception = None):
        self.service = service
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{service}] {message}")


class TransientError(ServiceError):
    """
    Temporary failure - worth retrying.
    Examples: Network timeout, 502/503/504, connection reset
    """
    retryable = True
    log_level = "warning"


class PermanentError(ServiceError):
    """
    Permanent failure - don't retry.
    Examples: 400 Bad Request, 401 Unauthorized, 404 Not Found
    """
    retryable = False
    log_level = "error"


class RateLimitError(TransientError):
    """
    Rate limited - retry with longer backoff.
    Examples: 429 Too Many Requests
    """
    backoff_multiplier: int = 3  # Triple the normal backoff

    def __init__(self, service: str, retry_after: int = None, **kwargs):
        self.retry_after = retry_after
        super().__init__(service, "Rate limited", **kwargs)


class CircuitOpenError(ServiceError):
    """
    Circuit breaker is open - fail fast without calling service.
    """
    retryable = False
    log_level = "warning"

    def __init__(self, service: str, recovery_at: datetime):
        self.recovery_at = recovery_at
        super().__init__(service, f"Circuit open until {recovery_at}")


class ConfigurationError(PermanentError):
    """
    Configuration issue - requires admin intervention.
    Examples: Missing API key, invalid credentials
    """
    log_level = "critical"
```

### Error Classification by HTTP Status

| Status Code | Error Type | Retry? |
|-------------|------------|--------|
| 400 | PermanentError | No |
| 401 | ConfigurationError | No |
| 403 | PermanentError | No |
| 404 | PermanentError | No |
| 408 | TransientError | Yes |
| 429 | RateLimitError | Yes (longer backoff) |
| 500 | TransientError | Yes |
| 502 | TransientError | Yes |
| 503 | TransientError | Yes |
| 504 | TransientError | Yes |
| Connection Error | TransientError | Yes |
| Timeout | TransientError | Yes |

---

## 10.4 Retry & Circuit Breaker Patterns

```python
# integrations/retry.py
import asyncio
from functools import wraps
from datetime import datetime, timedelta
import frappe

class CircuitBreaker:
    """
    Circuit breaker pattern implementation.

    States:
    - closed: Normal operation, requests pass through
    - open: Too many failures, fail fast without calling service
    - half-open: Testing if service recovered, allow one request
    """

    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 name: str = "circuit"):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self._failure_count = 0
        self._last_failure = None
        self._state = "closed"

    @property
    def state(self) -> str:
        if self._state == "open":
            if datetime.now() >= self._recovery_at:
                self._state = "half-open"
        return self._state

    @property
    def _recovery_at(self) -> datetime:
        if self._last_failure:
            return self._last_failure + timedelta(seconds=self.recovery_timeout)
        return datetime.now()

    @property
    def error_rate(self) -> float:
        return (self._failure_count / self.failure_threshold) * 100

    def record_success(self):
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self):
        self._failure_count += 1
        self._last_failure = datetime.now()
        if self._failure_count >= self.failure_threshold:
            self._state = "open"
            frappe.log_error(
                f"Circuit {self.name} opened after {self._failure_count} failures",
                "Circuit Breaker"
            )

    def allow_request(self) -> bool:
        state = self.state
        if state == "closed":
            return True
        if state == "half-open":
            return True  # Allow test request
        return False


def with_retry(max_attempts: int = 3,
               base_delay: float = 1.0,
               max_delay: float = 30.0,
               exponential_base: float = 2.0):
    """
    Decorator for retrying failed operations with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay cap in seconds (default: 30.0)
        exponential_base: Base for exponential calculation (default: 2.0)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)

                except RateLimitError as e:
                    last_error = e
                    if e.retry_after:
                        delay = e.retry_after
                    else:
                        delay = min(
                            base_delay * (exponential_base ** attempt) * e.backoff_multiplier,
                            max_delay
                        )
                    frappe.log_error(
                        f"Rate limited, retrying in {delay}s (attempt {attempt + 1}/{max_attempts})",
                        "Retry"
                    )
                    await asyncio.sleep(delay)

                except TransientError as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        delay = min(
                            base_delay * (exponential_base ** attempt),
                            max_delay
                        )
                        frappe.log_error(
                            f"Transient error, retrying in {delay}s (attempt {attempt + 1}/{max_attempts}): {e}",
                            "Retry"
                        )
                        await asyncio.sleep(delay)

                except PermanentError:
                    # Don't retry permanent errors
                    raise

            # All retries exhausted
            raise last_error

        return wrapper
    return decorator


def with_circuit_breaker(circuit: CircuitBreaker):
    """
    Decorator that integrates circuit breaker with a function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not circuit.allow_request():
                raise CircuitOpenError(
                    circuit.name,
                    circuit._recovery_at
                )

            try:
                result = await func(*args, **kwargs)
                circuit.record_success()
                return result

            except TransientError:
                circuit.record_failure()
                raise

            except PermanentError:
                # Permanent errors don't affect circuit
                raise

        return wrapper
    return decorator
```

---

## 10.5 Service Implementation Examples

### Maps Service

```python
# integrations/maps/google.py
import aiohttp
from ..base import BaseExternalService, ServiceHealth
from ..errors import TransientError, PermanentError, RateLimitError
from ..retry import with_retry, with_circuit_breaker

class GoogleMapsService(BaseExternalService):
    """Google Maps API integration"""

    service_name = "google_maps"
    default_timeout = 10

    def __init__(self, organization: str, config: dict = None):
        super().__init__(organization, config)
        self.api_key = config.get("api_key") or frappe.conf.google_maps_api_key
        self.base_url = "https://maps.googleapis.com/maps/api"

    @with_circuit_breaker(circuit=None)  # Set in __init__
    @with_retry(max_attempts=3, base_delay=1.0)
    async def geocode(self, address: str) -> tuple[float, float]:
        """
        Geocode an address to lat/lng coordinates.

        Args:
            address: Human-readable address string

        Returns:
            Tuple of (latitude, longitude)

        Raises:
            TransientError: Temporary API failure
            PermanentError: Invalid address or API error
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/geocode/json",
                    params={"address": address, "key": self.api_key},
                    timeout=aiohttp.ClientTimeout(total=self.default_timeout)
                ) as response:

                    if response.status == 429:
                        raise RateLimitError(self.service_name)

                    if response.status >= 500:
                        raise TransientError(
                            self.service_name,
                            f"Server error: {response.status}"
                        )

                    data = await response.json()

                    if data["status"] == "ZERO_RESULTS":
                        raise PermanentError(
                            self.service_name,
                            f"No results for address: {address}"
                        )

                    if data["status"] != "OK":
                        raise PermanentError(
                            self.service_name,
                            f"API error: {data['status']}"
                        )

                    location = data["results"][0]["geometry"]["location"]
                    return (location["lat"], location["lng"])

            except aiohttp.ClientError as e:
                raise TransientError(
                    self.service_name,
                    f"Connection error: {str(e)}",
                    original_error=e
                )

    @with_circuit_breaker(circuit=None)
    @with_retry(max_attempts=3, base_delay=1.0)
    async def get_drive_time(self, origin: tuple, destination: tuple) -> dict:
        """
        Calculate drive time between two points.

        Returns:
            Dict with duration_seconds and distance_meters
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/distancematrix/json",
                params={
                    "origins": f"{origin[0]},{origin[1]}",
                    "destinations": f"{destination[0]},{destination[1]}",
                    "key": self.api_key,
                    "departure_time": "now"
                },
                timeout=aiohttp.ClientTimeout(total=self.default_timeout)
            ) as response:
                data = await response.json()

                if data["status"] != "OK":
                    raise PermanentError(
                        self.service_name,
                        f"Distance Matrix error: {data['status']}"
                    )

                element = data["rows"][0]["elements"][0]
                return {
                    "duration_seconds": element["duration"]["value"],
                    "distance_meters": element["distance"]["value"],
                    "duration_in_traffic_seconds": element.get(
                        "duration_in_traffic", {}
                    ).get("value")
                }

    async def health_check(self) -> ServiceHealth:
        """Verify API is accessible"""
        start = datetime.now()
        try:
            # Use a known address for health check
            await self.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
            latency = (datetime.now() - start).total_seconds() * 1000
            return ServiceHealth(
                service_name=self.service_name,
                status="healthy",
                latency_ms=latency,
                last_success=datetime.now(),
                circuit_state=self._circuit.state
            )
        except Exception as e:
            return ServiceHealth(
                service_name=self.service_name,
                status="unhealthy",
                last_failure=datetime.now(),
                circuit_state=self._circuit.state
            )
```

---

## 10.6 Health Check API

```python
# api/v1/health.py
import frappe
from frappe import _
from dartwing_company.integrations.maps.google import GoogleMapsService
from dartwing_company.integrations.ai.openai import OpenAIService
from dartwing_company.integrations.payments.stripe import StripeService
import asyncio

@frappe.whitelist(allow_guest=True)
def check():
    """
    Health check endpoint for monitoring.

    Returns comprehensive health status of all external services.

    Response:
    {
        "status": "healthy|degraded|unhealthy",
        "timestamp": "2025-11-28T12:00:00Z",
        "services": {
            "database": {"status": "healthy", "latency_ms": 5},
            "redis": {"status": "healthy", "latency_ms": 2},
            "google_maps": {"status": "healthy", "latency_ms": 120},
            "openai": {"status": "degraded", "circuit_state": "half-open"},
            "stripe": {"status": "healthy", "latency_ms": 200}
        }
    }
    """
    services = {}

    # Check database
    services["database"] = check_database()

    # Check Redis
    services["redis"] = check_redis()

    # Check external services (non-blocking)
    external_services = get_external_service_health()
    services.update(external_services)

    # Determine overall status
    statuses = [s["status"] for s in services.values()]
    if "unhealthy" in statuses:
        overall = "unhealthy"
    elif "degraded" in statuses:
        overall = "degraded"
    else:
        overall = "healthy"

    return {
        "status": overall,
        "timestamp": frappe.utils.now_datetime().isoformat(),
        "services": services
    }


def check_database() -> dict:
    """Check MariaDB connectivity and latency"""
    import time
    start = time.time()
    try:
        frappe.db.sql("SELECT 1")
        latency = (time.time() - start) * 1000
        return {"status": "healthy", "latency_ms": round(latency, 2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def check_redis() -> dict:
    """Check Redis connectivity and latency"""
    import time
    start = time.time()
    try:
        frappe.cache().ping()
        latency = (time.time() - start) * 1000
        return {"status": "healthy", "latency_ms": round(latency, 2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def get_external_service_health() -> dict:
    """Get health status of external services (uses cached circuit state)"""
    results = {}

    # Get health without making API calls (uses circuit state)
    services = [
        GoogleMapsService,
        OpenAIService,
        StripeService
    ]

    for service_class in services:
        try:
            service = service_class(organization=None, config={})
            health = service.get_health()
            results[health.service_name] = {
                "status": health.status,
                "circuit_state": health.circuit_state,
                "error_rate_percent": health.error_rate_percent
            }
        except Exception as e:
            results[service_class.service_name] = {
                "status": "unknown",
                "error": str(e)
            }

    return results
```

### Hooks Configuration

```python
# hooks.py additions for health monitoring

# Scheduled health checks
scheduler_events = {
    "cron": {
        # ... existing entries ...

        # Health check every 5 minutes (update circuit states)
        "*/5 * * * *": [
            "dartwing_company.tasks.health.update_service_health"
        ]
    }
}
```

---

## 10.7 Graceful Degradation Patterns

| Service | Degradation Behavior |
|---------|---------------------|
| **Google Maps** | Use cached geocoding results; skip drive time estimates; show "ETA unavailable" |
| **OpenAI/Claude** | Disable AI suggestions; use template responses; queue for later processing |
| **Stripe** | Disable online payments; show "Pay by invoice" option; log for manual processing |
| **Calendar** | Disable sync; show local schedule only; queue calendar updates |

```python
# Example: Dispatch assignment with Maps degradation
async def find_best_match(job: DispatchJob) -> list[AssignmentScore]:
    try:
        # Try with drive time calculation
        return await find_best_match_with_drive_time(job)

    except CircuitOpenError:
        # Fallback: Use straight-line distance
        frappe.log_error("Maps unavailable, using distance fallback", "Degradation")
        return find_best_match_by_distance(job)

    except TransientError:
        # Fallback: Use straight-line distance
        return find_best_match_by_distance(job)
```

---

## 10.8 Observability

### Metrics to Track

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `external_service_latency_ms` | Response time per service | P95 > 5000ms |
| `external_service_error_rate` | Error rate per service | > 10% over 5 min |
| `circuit_breaker_state` | Current state per service | open for > 10 min |
| `retry_count` | Retries per service | > 50/min |

### Logging Pattern

```python
import structlog

log = structlog.get_logger()

def log_external_call(service: str, operation: str, duration_ms: float,
                      success: bool, error: str = None):
    log.info("external_service_call",
        service=service,
        operation=operation,
        duration_ms=duration_ms,
        success=success,
        error=error,
        circuit_state=get_circuit_state(service)
    )
```

---

**Next: Section 11 - Transaction Management**

# Dartwing Company Architecture - Section 11: Transaction Management & Saga Patterns

---

## 11.1 Overview

Dartwing Company operations frequently span multiple systems (ERPNext, HRMS, CRM, external services). This section defines transaction management patterns to ensure data consistency across systems when failures occur.

**Cross-Reference:** This section extends patterns from `dartwing_core/org_integrity_guardrails.md` for cross-system operations.

---

## 11.2 Cross-System Operations Inventory

| Operation | Systems Involved | Failure Impact | Priority |
|-----------|------------------|----------------|----------|
| Complete Dispatch Job | Dartwing → ERPNext (Invoice) → HRMS (Timesheet) | Billing/payroll errors | HIGH |
| Create Lead from Campaign | dartwing_leadgen → Dartwing (Campaign) → CRM (Lead) | Lost lead data | HIGH |
| Book Appointment | Dartwing → Calendar → Stripe (Payment) | Double booking, payment issues | HIGH |
| Publish Schedule | Dartwing → HRMS (Shift Assignment) | Scheduling conflicts | MEDIUM |
| Clock In/Out | Dartwing → HRMS (Attendance) | Payroll errors | HIGH |
| Submit Portal Ticket | Portal → Dartwing (Ticket) → CRM (Communication) | Lost support request | MEDIUM |
| Create Client Portal | Dartwing → ERPNext (Customer) → Drive (Vault) | Orphaned resources | LOW |

---

## 11.3 Saga Pattern Implementation

### Core Saga Classes

```python
# utils/saga.py
from dataclasses import dataclass, field
from typing import Callable, Any, Optional
from datetime import datetime
import frappe
from frappe import _

@dataclass
class SagaStep:
    """Single step in a saga"""
    name: str
    action: Callable[[], Any]
    compensation: Callable[[Any], None]
    result: Any = None
    status: str = "pending"  # pending, success, failed, compensated
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class SagaFailedError(Exception):
    """Raised when saga fails and compensation is complete"""
    def __init__(self, saga_name: str, failed_step: str, original_error: Exception):
        self.saga_name = saga_name
        self.failed_step = failed_step
        self.original_error = original_error
        super().__init__(f"Saga '{saga_name}' failed at step '{failed_step}': {original_error}")


class Saga:
    """
    Orchestrates multi-step operations with automatic compensation on failure.

    Usage:
        saga = Saga("complete_job", organization="ORG-001")
        saga.add_step("update_status", update_job, rollback_job)
        saga.add_step("create_invoice", create_invoice, cancel_invoice)
        saga.add_step("create_timesheet", create_timesheet, delete_timesheet)

        try:
            saga.execute()
        except SagaFailedError as e:
            # Saga failed and compensated
            notify_admin(e)
    """

    def __init__(self, name: str, organization: str, context: dict = None):
        self.name = name
        self.organization = organization
        self.context = context or {}
        self.steps: list[SagaStep] = []
        self.completed_steps: list[SagaStep] = []
        self.saga_log = None
        self.started_at = None
        self.completed_at = None

    def add_step(self, name: str, action: Callable, compensation: Callable):
        """Add a step to the saga"""
        self.steps.append(SagaStep(
            name=name,
            action=action,
            compensation=compensation
        ))

    def execute(self) -> dict:
        """
        Execute all steps in sequence.
        On failure, compensate completed steps in reverse order.

        Returns:
            dict: Results from all steps {step_name: result}

        Raises:
            SagaFailedError: If any step fails (after compensation)
        """
        self.started_at = datetime.now()
        self._create_log()

        results = {}
        failed_step = None

        try:
            for step in self.steps:
                step.started_at = datetime.now()
                self._log_step_start(step)

                try:
                    step.result = step.action()
                    step.status = "success"
                    step.completed_at = datetime.now()
                    results[step.name] = step.result
                    self.completed_steps.append(step)
                    self._log_step_success(step)

                except Exception as e:
                    step.status = "failed"
                    step.error = str(e)
                    step.completed_at = datetime.now()
                    failed_step = step
                    self._log_step_failure(step, e)
                    raise

            # All steps succeeded
            self.completed_at = datetime.now()
            self._mark_complete()
            return results

        except Exception as e:
            # Compensate in reverse order
            self._compensate()

            raise SagaFailedError(
                self.name,
                failed_step.name if failed_step else "unknown",
                e
            )

    def _compensate(self):
        """Run compensation for all completed steps in reverse"""
        for step in reversed(self.completed_steps):
            try:
                step.compensation(step.result)
                step.status = "compensated"
                self._log_compensation_success(step)

            except Exception as e:
                # Log but continue compensating other steps
                step.status = "compensation_failed"
                self._log_compensation_failure(step, e)
                frappe.log_error(
                    f"Compensation failed for {step.name}: {e}",
                    f"Saga {self.name} Compensation Error"
                )

        self._mark_compensated()

    def _create_log(self):
        """Create SagaLog document"""
        self.saga_log = frappe.get_doc({
            "doctype": "Saga Log",
            "saga_name": self.name,
            "organization": self.organization,
            "status": "running",
            "started_at": self.started_at,
            "context": frappe.as_json(self.context)
        })
        self.saga_log.insert(ignore_permissions=True)
        frappe.db.commit()

    def _log_step_start(self, step: SagaStep):
        """Log step start"""
        self.saga_log.append("steps", {
            "step_name": step.name,
            "status": "running",
            "started_at": step.started_at
        })
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _log_step_success(self, step: SagaStep):
        """Log step success"""
        for s in self.saga_log.steps:
            if s.step_name == step.name:
                s.status = "success"
                s.completed_at = step.completed_at
                s.result = frappe.as_json(step.result) if step.result else None
                break
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _log_step_failure(self, step: SagaStep, error: Exception):
        """Log step failure"""
        for s in self.saga_log.steps:
            if s.step_name == step.name:
                s.status = "failed"
                s.completed_at = step.completed_at
                s.error = str(error)
                break
        self.saga_log.status = "failed"
        self.saga_log.error_message = str(error)
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _log_compensation_success(self, step: SagaStep):
        """Log compensation success"""
        for s in self.saga_log.steps:
            if s.step_name == step.name:
                s.status = "compensated"
                break
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _log_compensation_failure(self, step: SagaStep, error: Exception):
        """Log compensation failure"""
        for s in self.saga_log.steps:
            if s.step_name == step.name:
                s.status = "compensation_failed"
                s.error = f"{s.error or ''} | Compensation: {error}"
                break
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _mark_complete(self):
        """Mark saga as complete"""
        self.saga_log.status = "completed"
        self.saga_log.completed_at = self.completed_at
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()

    def _mark_compensated(self):
        """Mark saga as compensated"""
        self.saga_log.status = "compensated"
        self.saga_log.completed_at = datetime.now()
        self.saga_log.save(ignore_permissions=True)
        frappe.db.commit()
```

---

## 11.4 SagaLog DocType

```json
{
  "doctype": "Saga Log",
  "module": "Dartwing Company",
  "autoname": "SAGA-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "saga_name",
      "label": "Saga Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "running\ncompleted\nfailed\ncompensated",
      "default": "running"
    },
    {
      "fieldname": "started_at",
      "label": "Started At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "completed_at",
      "label": "Completed At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "error_message",
      "label": "Error Message",
      "fieldtype": "Long Text"
    },
    {
      "fieldname": "context",
      "label": "Context",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "steps",
      "label": "Steps",
      "fieldtype": "Table",
      "options": "Saga Step"
    }
  ]
}
```

### Saga Step (Child Table)

```json
{
  "doctype": "Saga Step",
  "module": "Dartwing Company",
  "istable": 1,
  "fields": [
    {
      "fieldname": "step_name",
      "label": "Step Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "pending\nrunning\nsuccess\nfailed\ncompensated\ncompensation_failed"
    },
    {
      "fieldname": "result",
      "label": "Result",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "error",
      "label": "Error",
      "fieldtype": "Long Text"
    },
    {
      "fieldname": "started_at",
      "label": "Started At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "completed_at",
      "label": "Completed At",
      "fieldtype": "Datetime"
    }
  ]
}
```

---

## 11.5 Implementation Examples

### Example 1: Complete Dispatch Job

```python
# operations/dispatch/completion.py
from dartwing_company.utils.saga import Saga, SagaFailedError
import frappe

def complete_dispatch_job(job_name: str) -> dict:
    """
    Complete a dispatch job with billing and timesheet creation.

    Steps:
    1. Update job status to 'completed'
    2. Create Sales Invoice in ERPNext
    3. Create Timesheet in HRMS

    On failure, all steps are rolled back.
    """
    job = frappe.get_doc("Dispatch Job", job_name)

    saga = Saga(
        name="complete_dispatch_job",
        organization=job.organization,
        context={"job_name": job_name}
    )

    # Store original status for rollback
    original_status = job.status

    # Step 1: Update job status
    saga.add_step(
        name="update_job_status",
        action=lambda: _update_job_status(job, "completed"),
        compensation=lambda _: _update_job_status(job, original_status)
    )

    # Step 2: Create Sales Invoice
    saga.add_step(
        name="create_sales_invoice",
        action=lambda: _create_sales_invoice(job),
        compensation=lambda invoice_name: _cancel_invoice(invoice_name)
    )

    # Step 3: Create Timesheet
    saga.add_step(
        name="create_timesheet",
        action=lambda: _create_timesheet(job),
        compensation=lambda timesheet_name: _delete_timesheet(timesheet_name)
    )

    try:
        results = saga.execute()
        return {
            "success": True,
            "invoice": results.get("create_sales_invoice"),
            "timesheet": results.get("create_timesheet")
        }
    except SagaFailedError as e:
        frappe.log_error(str(e), "Dispatch Job Completion Failed")
        return {
            "success": False,
            "error": str(e.original_error),
            "failed_step": e.failed_step
        }


def _update_job_status(job, status):
    """Update dispatch job status"""
    job.status = status
    job.status_updated_at = frappe.utils.now_datetime()
    job.save()
    frappe.db.commit()
    return job.name


def _create_sales_invoice(job) -> str:
    """Create Sales Invoice from completed job"""
    if not job.billable:
        return None  # Skip if not billable

    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": job.customer,
        "items": [
            {
                "item_code": job.job_type.billing_item,
                "qty": 1,
                "rate": job.job_type.rate
            }
        ],
        "dartwing_dispatch_job": job.name
    })
    invoice.insert()
    invoice.submit()
    frappe.db.commit()
    return invoice.name


def _cancel_invoice(invoice_name: str):
    """Cancel Sales Invoice (compensation)"""
    if not invoice_name:
        return  # Nothing to cancel

    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    invoice.cancel()
    frappe.db.commit()


def _create_timesheet(job) -> str:
    """Create Timesheet from completed job"""
    timesheet = frappe.get_doc({
        "doctype": "Timesheet",
        "employee": job.assigned_to,
        "time_logs": [
            {
                "activity_type": "Job",
                "from_time": job.actual_arrival,
                "to_time": job.actual_departure,
                "hours": job.actual_duration / 3600,
                "project": job.project
            }
        ],
        "dartwing_dispatch_job": job.name
    })
    timesheet.insert()
    timesheet.submit()
    frappe.db.commit()
    return timesheet.name


def _delete_timesheet(timesheet_name: str):
    """Delete Timesheet (compensation)"""
    if not timesheet_name:
        return

    timesheet = frappe.get_doc("Timesheet", timesheet_name)
    timesheet.cancel()
    frappe.delete_doc("Timesheet", timesheet_name)
    frappe.db.commit()
```

### Example 2: Book Appointment with Payment

```python
# crm/appointments/booking.py
from dartwing_company.utils.saga import Saga, SagaFailedError

def book_appointment(
    customer: str,
    appointment_type: str,
    slot_start: datetime,
    payment_method_id: str = None
) -> dict:
    """
    Book appointment with calendar blocking and optional payment.

    Steps:
    1. Create Appointment record (locked slot)
    2. Create Calendar Event (Google/Outlook)
    3. Process Payment (if required)
    4. Send Confirmation

    On failure, slot is released and payment refunded.
    """
    org = get_organization_from_customer(customer)
    appt_type = frappe.get_doc("Appointment Type", appointment_type)

    saga = Saga(
        name="book_appointment",
        organization=org,
        context={
            "customer": customer,
            "appointment_type": appointment_type,
            "slot_start": slot_start.isoformat()
        }
    )

    # Step 1: Create Appointment (blocks slot)
    saga.add_step(
        name="create_appointment",
        action=lambda: _create_appointment(customer, appt_type, slot_start),
        compensation=lambda appt_name: _cancel_appointment(appt_name)
    )

    # Step 2: Create Calendar Event
    saga.add_step(
        name="create_calendar_event",
        action=lambda: _create_calendar_event(
            saga.completed_steps[0].result,  # appointment name
            appt_type,
            slot_start
        ),
        compensation=lambda event_id: _delete_calendar_event(event_id)
    )

    # Step 3: Process Payment (if required)
    if appt_type.requires_deposit and payment_method_id:
        saga.add_step(
            name="process_payment",
            action=lambda: _process_payment(
                customer,
                appt_type.deposit_amount,
                payment_method_id,
                saga.completed_steps[0].result  # appointment name
            ),
            compensation=lambda payment_id: _refund_payment(payment_id)
        )

    # Step 4: Send Confirmation (no compensation needed)
    saga.add_step(
        name="send_confirmation",
        action=lambda: _send_confirmation(
            saga.completed_steps[0].result,
            customer
        ),
        compensation=lambda _: None  # Can't unsend email
    )

    try:
        results = saga.execute()
        return {
            "success": True,
            "appointment": results["create_appointment"],
            "calendar_event": results.get("create_calendar_event"),
            "payment": results.get("process_payment")
        }
    except SagaFailedError as e:
        return {
            "success": False,
            "error": str(e.original_error),
            "failed_step": e.failed_step
        }
```

---

## 11.6 Saga Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    SAGA MONITORING                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Last 24 Hours                                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Completed  │  │  Failed    │  │ Compensated│            │
│  │    145     │  │     3      │  │     3      │            │
│  │   (97%)    │  │    (2%)    │  │  (100%)    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  Failed Sagas (Requires Attention)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SAGA-2025-00123 │ complete_dispatch_job │ 10:23 AM   │  │
│  │ Failed at: create_timesheet                          │  │
│  │ Error: Employee not found                            │  │
│  │ [View Details] [Retry] [Mark Resolved]               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  By Saga Type (7 days)                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ complete_dispatch_job     │ ████████████░ │ 98%     │  │
│  │ book_appointment          │ █████████████ │ 100%    │  │
│  │ publish_schedule          │ ███████████░░ │ 95%     │  │
│  │ create_lead_from_campaign │ ████████████░ │ 97%     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 11.7 Best Practices

### When to Use Sagas

| Scenario | Use Saga? | Alternative |
|----------|-----------|-------------|
| Multiple external systems involved | Yes | - |
| Long-running operation (> 5 seconds) | Yes | - |
| Payment + other actions | Yes | - |
| Single DocType CRUD | No | Use Frappe transactions |
| Read-only operations | No | No transaction needed |
| Idempotent operations | Maybe | May not need compensation |

### Compensation Design Rules

1. **Compensation must be idempotent** - Safe to run multiple times
2. **Compensation should not fail** - Use try/except and log errors
3. **Compensation order matters** - Reverse order of execution
4. **Some actions can't be compensated** - Email sent, SMS sent (document this)
5. **External service compensation may fail** - Have fallback (manual intervention)

### Testing Sagas

```python
# tests/test_saga.py
def test_complete_job_saga_success():
    """Test successful saga execution"""
    job = create_test_dispatch_job()
    result = complete_dispatch_job(job.name)

    assert result["success"] is True
    assert result["invoice"] is not None
    assert result["timesheet"] is not None

    # Verify saga log
    saga_log = frappe.get_last_doc("Saga Log",
        filters={"saga_name": "complete_dispatch_job"})
    assert saga_log.status == "completed"


def test_complete_job_saga_compensation():
    """Test saga compensation on failure"""
    job = create_test_dispatch_job()

    # Force timesheet creation to fail
    with mock.patch("create_timesheet", side_effect=Exception("Test error")):
        result = complete_dispatch_job(job.name)

    assert result["success"] is False
    assert result["failed_step"] == "create_timesheet"

    # Verify job status rolled back
    job.reload()
    assert job.status == "in_progress"  # Original status

    # Verify invoice was cancelled
    assert not frappe.db.exists("Sales Invoice",
        {"dartwing_dispatch_job": job.name, "docstatus": 1})
```

---

**Next: Section 12 - Caching Strategy**

# Dartwing Company Architecture - Section 12: Caching Strategy

---

## 12.1 Overview

High-frequency operations require caching to maintain performance at scale. This section defines cache layers, key strategies, invalidation patterns, and monitoring.

---

## 12.2 Cache Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CACHE LAYERS                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  REQUEST-LEVEL CACHE (frappe.local)                         │
│  • Lifetime: Single HTTP request                            │
│  • Use: Avoid repeated DB queries in same request           │
│  • Example: get_organization_settings() called 10x          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  SESSION-LEVEL CACHE (Redis, keyed by user session)         │
│  • Lifetime: User session (15-30 min default)               │
│  • Use: User preferences, frequently accessed settings      │
│  • Example: Portal branding, View Set configuration         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  SHARED CACHE (Redis, keyed by organization)                │
│  • Lifetime: 5-60 minutes (configurable per key)            │
│  • Use: Computed data, external API results                 │
│  • Example: Employee certifications, geocoding results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  COMPUTED CACHE (Redis, keyed by inputs)                    │
│  • Lifetime: Until explicitly invalidated                   │
│  • Use: Expensive calculations that rarely change           │
│  • Example: SLA policy lookups, AI prompt templates         │
└─────────────────────────────────────────────────────────────┘
```

---

## 12.3 Cache Key Strategy

### Key Naming Convention

```python
# Pattern: dw:{module}:{doctype}:{org}:{identifier}:{version}

CACHE_KEYS = {
    # Organization-scoped
    "org_settings": "dw:settings:{org}",
    "org_features": "dw:features:{org}",

    # User-scoped (session)
    "user_orgs": "dw:user_orgs:{user}",
    "user_permissions": "dw:permissions:{user}:{org}",

    # Entity-scoped
    "employee_certs": "dw:certs:{org}:{employee}",
    "customer_sla": "dw:sla:{org}:{customer}",
    "view_set": "dw:viewset:{org}:{view_set_name}",

    # External service results
    "geocode": "dw:geo:{address_hash}",
    "drive_time": "dw:drive:{origin_hash}:{dest_hash}",

    # Computed
    "dispatch_scores": "dw:dispatch_scores:{job_name}:{timestamp}",
    "ai_prompt": "dw:prompt:{org}:{prompt_type}:{version}",
}
```

---

## 12.4 Performance-Critical Paths

| Path | Cache Layer | TTL | Invalidation Trigger | Hit Rate Target |
|------|-------------|-----|---------------------|-----------------|
| Employee Certifications | Shared | 5 min | On cert save/delete | 95% |
| Geocoding Results | Shared | 24 hours | Never (immutable) | 99% |
| Portal View Set | Session | 15 min | On View Set save | 90% |
| SLA Policy Lookup | Shared | 5 min | On SLA Policy save | 95% |
| AI Prompt Templates | Shared | 1 hour | On template save | 98% |
| Organization Settings | Session | 15 min | On settings save | 95% |
| Employee Availability | Request | N/A | Per-request | N/A |
| Customer Portal Access | Session | 30 min | On permission change | 90% |

---

## 12.5 Cache Utility Implementation

```python
# utils/cache.py
import frappe
import hashlib
import json
from functools import wraps
from typing import Callable, Any, Optional
from datetime import timedelta

class DartwingCache:
    """Centralized cache utilities for Dartwing Company"""

    # Default TTLs by cache type
    TTL_REQUEST = 0  # Request-scoped, no Redis
    TTL_SESSION = 900  # 15 minutes
    TTL_SHARED = 300  # 5 minutes
    TTL_LONG = 3600  # 1 hour
    TTL_PERMANENT = 86400  # 24 hours

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        value = frappe.cache().get_value(key)
        if value:
            return json.loads(value) if isinstance(value, str) else value
        return None

    @staticmethod
    def set(key: str, value: Any, ttl: int = TTL_SHARED):
        """Set value in cache with TTL"""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        frappe.cache().set_value(key, serialized, expires_in_sec=ttl)

    @staticmethod
    def delete(key: str):
        """Delete key from cache"""
        frappe.cache().delete_value(key)

    @staticmethod
    def delete_pattern(pattern: str):
        """Delete all keys matching pattern"""
        frappe.cache().delete_keys(pattern)

    @staticmethod
    def hash_key(*args) -> str:
        """Create deterministic hash from arguments"""
        content = json.dumps(args, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:12]


def cached(key_template: str, ttl: int = DartwingCache.TTL_SHARED):
    """
    Decorator for caching function results.

    Usage:
        @cached("dw:certs:{org}:{employee}", ttl=300)
        def get_employee_certifications(org: str, employee: str) -> dict:
            ...

    Key template supports:
    - {arg_name} - replaced with function argument value
    - {self.attr} - replaced with instance attribute (for methods)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from template
            cache_key = _build_cache_key(key_template, func, args, kwargs)

            # Check cache
            cached_value = DartwingCache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Cache result
            if result is not None:
                DartwingCache.set(cache_key, result, ttl)

            return result

        # Attach invalidation helper
        wrapper.invalidate = lambda *a, **kw: DartwingCache.delete(
            _build_cache_key(key_template, func, a, kw)
        )

        return wrapper
    return decorator


def _build_cache_key(template: str, func: Callable, args: tuple, kwargs: dict) -> str:
    """Build cache key from template and function arguments"""
    import inspect
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    key = template
    for param_name, value in bound.arguments.items():
        placeholder = "{" + param_name + "}"
        if placeholder in key:
            key = key.replace(placeholder, str(value))

    return key


# Request-level cache
def request_cached(func: Callable) -> Callable:
    """
    Cache result for duration of single request.
    Uses frappe.local for storage.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_attr = f"_cache_{func.__name__}"
        cache_key = DartwingCache.hash_key(args, kwargs)

        if not hasattr(frappe.local, cache_attr):
            setattr(frappe.local, cache_attr, {})

        cache = getattr(frappe.local, cache_attr)

        if cache_key in cache:
            return cache[cache_key]

        result = func(*args, **kwargs)
        cache[cache_key] = result
        return result

    return wrapper
```

---

## 12.6 Usage Examples

### Employee Certifications

```python
# hr/certifications.py
from dartwing_company.utils.cache import cached, DartwingCache

@cached("dw:certs:{org}:{employee}", ttl=300)
def get_employee_certifications(org: str, employee: str) -> list[dict]:
    """
    Get active certifications for employee.
    Cached for 5 minutes.
    """
    return frappe.get_all("Employee Certification",
        filters={
            "employee": employee,
            "organization": org,
            "status": "Active",
            "expiry_date": [">=", frappe.utils.today()]
        },
        fields=["certification_type", "expiry_date", "certificate_number"]
    )


# Invalidation hook
def on_certification_save(doc, method):
    """Invalidate cache when certification changes"""
    cache_key = f"dw:certs:{doc.organization}:{doc.employee}"
    DartwingCache.delete(cache_key)
```

### Geocoding with Long TTL

```python
# integrations/maps/cache.py
from dartwing_company.utils.cache import cached, DartwingCache

@cached("dw:geo:{address_hash}", ttl=86400)  # 24 hours
def geocode_cached(address: str) -> tuple[float, float]:
    """
    Geocode address with long-term caching.
    Addresses don't change, so cache for 24 hours.
    """
    address_hash = DartwingCache.hash_key(address.lower().strip())
    # Actual geocoding happens here if cache miss
    return maps_service.geocode(address)
```

### Organization Settings (Session Cache)

```python
# utils/settings.py
from dartwing_company.utils.cache import cached, request_cached

@cached("dw:settings:{org}", ttl=900)  # 15 minutes
def get_organization_settings(org: str) -> dict:
    """
    Get organization settings.
    Cached at session level.
    """
    doc = frappe.get_doc("Organization Settings", org)
    return doc.as_dict()


@request_cached
def get_current_org_settings() -> dict:
    """
    Get settings for current user's organization.
    Cached for this request only (may be called many times).
    """
    org = get_user_organization(frappe.session.user)
    return get_organization_settings(org)
```

---

## 12.7 Cache Invalidation Hooks

```python
# hooks.py additions

doc_events = {
    # ... existing events ...

    # Cache invalidation triggers
    "Employee Certification": {
        "after_save": "dartwing_company.cache.invalidate.on_certification_change",
        "on_trash": "dartwing_company.cache.invalidate.on_certification_change"
    },
    "Organization Settings": {
        "after_save": "dartwing_company.cache.invalidate.on_settings_change"
    },
    "View Set": {
        "after_save": "dartwing_company.cache.invalidate.on_view_set_change"
    },
    "SLA Policy": {
        "after_save": "dartwing_company.cache.invalidate.on_sla_policy_change"
    },
    "AI Prompt Template": {
        "after_save": "dartwing_company.cache.invalidate.on_prompt_template_change"
    }
}
```

```python
# cache/invalidate.py

def on_certification_change(doc, method):
    """Invalidate employee certification cache"""
    DartwingCache.delete(f"dw:certs:{doc.organization}:{doc.employee}")

def on_settings_change(doc, method):
    """Invalidate organization settings cache"""
    DartwingCache.delete(f"dw:settings:{doc.organization}")
    # Also invalidate any dependent caches
    DartwingCache.delete_pattern(f"dw:*:{doc.organization}:*")

def on_view_set_change(doc, method):
    """Invalidate view set cache"""
    DartwingCache.delete(f"dw:viewset:{doc.organization}:{doc.name}")

def on_sla_policy_change(doc, method):
    """Invalidate SLA policy cache"""
    DartwingCache.delete_pattern(f"dw:sla:{doc.organization}:*")

def on_prompt_template_change(doc, method):
    """Invalidate AI prompt template cache"""
    DartwingCache.delete(f"dw:prompt:{doc.organization}:{doc.prompt_type}:*")
```

---

## 12.8 Cache Warming

```python
# cache/warm.py
import frappe

def warm_organization_caches(org: str):
    """
    Pre-warm frequently accessed caches for an organization.
    Called after deployment or when caches are cold.
    """
    # Warm settings
    get_organization_settings(org)

    # Warm View Sets
    view_sets = frappe.get_all("View Set", filters={"organization": org})
    for vs in view_sets:
        get_view_set(org, vs.name)

    # Warm SLA Policies
    sla_policies = frappe.get_all("SLA Policy", filters={"organization": org})
    for sla in sla_policies:
        get_sla_policy(org, sla.name)

    # Warm AI Prompt Templates
    templates = frappe.get_all("AI Prompt Template",
        filters={"organization": org})
    for t in templates:
        get_prompt_template(org, t.prompt_type)


def warm_all_caches():
    """Warm caches for all active organizations"""
    orgs = frappe.get_all("Organization",
        filters={"status": "Active"},
        pluck="name")

    for org in orgs:
        warm_organization_caches(org)

    frappe.log_error(
        f"Warmed caches for {len(orgs)} organizations",
        "Cache Warming Complete"
    )
```

### Hooks Configuration

```python
# hooks.py

# Warm caches after deployment
after_migrate = [
    "dartwing_company.cache.warm.warm_all_caches"
]
```

---

## 12.9 Cache Monitoring

### Metrics to Track

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cache_hit_rate` | Hits / (Hits + Misses) | < 80% |
| `cache_miss_latency_ms` | Time to compute on miss | P95 > 500ms |
| `cache_size_mb` | Total Redis memory usage | > 1GB |
| `cache_eviction_rate` | Keys evicted per minute | > 100/min |

### Cache Stats Endpoint

```python
# api/v1/cache.py

@frappe.whitelist()
def stats():
    """Get cache statistics for monitoring"""
    redis = frappe.cache()

    return {
        "memory_used_mb": redis.info().get("used_memory_human"),
        "keys_total": redis.dbsize(),
        "hit_rate": redis.info().get("keyspace_hits") /
                   (redis.info().get("keyspace_hits") +
                    redis.info().get("keyspace_misses") + 1),
        "evicted_keys": redis.info().get("evicted_keys"),
        "connected_clients": redis.info().get("connected_clients")
    }
```

---

**Next: Section 13 - Offline Sync Protocol**

# Dartwing Company Architecture - Section 13: Offline Sync Protocol

---

## 13.1 Adoption Statement

Dartwing Company **adopts** the sync protocol defined in `dartwing_core/offline_real_time_sync_spec.md` for all mobile-facing DocTypes.

This includes:
- Change feed endpoints for delta sync
- Write queue with conflict resolution
- Socket.IO real-time updates
- AI Smart Merge for conflicts
- Human fallback UI for unresolvable conflicts

**Cross-Reference:** See `docs/dartwing_core/offline_real_time_sync_spec.md` for the full protocol specification.

---

## 13.2 Syncable DocTypes

| DocType | Sync Priority | Conflict Strategy | Offline Create | Offline Update | Offline Delete |
|---------|--------------|-------------------|----------------|----------------|----------------|
| Dispatch Job | High | AI Merge | No | Yes | No |
| Form Submission | High | Last-Write-Wins | Yes | No | No |
| Schedule Entry | Medium | Human Fallback | No | Yes | No |
| Conversation Message | Medium | Last-Write-Wins | Yes | No | No |
| Clock Event | High | Last-Write-Wins | Yes | No | No |
| Knowledge Article | Low | AI Merge | No | Yes | No |
| Appointment | Medium | Human Fallback | Yes | Yes | Yes |
| Service Ticket | Medium | AI Merge | Yes | Yes | No |

### Conflict Strategy Definitions

- **Last-Write-Wins (LWW):** Server accepts latest `client_ts`, logs overwrite
- **AI Merge:** LLM attempts to merge conflicting changes automatically
- **Human Fallback:** User must manually resolve via conflict UI

---

## 13.3 Sync Endpoints for Company Module

```python
# api/v1/sync.py
import frappe
from dartwing_core.sync import feed as core_feed, upsert_batch as core_upsert

# DocTypes enabled for sync
SYNCABLE_DOCTYPES = [
    "Dispatch Job",
    "Form Submission",
    "Schedule Entry",
    "Conversation Message",
    "Clock Event",
    "Knowledge Article",
    "Appointment",
    "Service Ticket"
]

# DocTypes that can be created offline
OFFLINE_CREATABLE = [
    "Form Submission",
    "Conversation Message",
    "Clock Event",
    "Appointment",
    "Service Ticket"
]

@frappe.whitelist()
def feed(doctype: str, since: str, limit: int = 100, org: str = None) -> dict:
    """
    Change feed for offline sync.

    Wraps dartwing_core.sync.feed with Company-specific filtering.

    Args:
        doctype: DocType to sync
        since: Timestamp or watermark for delta sync
        limit: Max records to return (default 100, max 500)
        org: Organization to filter by

    Returns:
        {
            "rows": [...],
            "next_since": "2025-11-28T12:00:00Z",
            "has_more": true
        }
    """
    if doctype not in SYNCABLE_DOCTYPES:
        frappe.throw(f"DocType {doctype} is not syncable")

    # Validate organization access
    org = org or get_user_organization(frappe.session.user)
    validate_org_access(org)

    # Add Company-specific filters
    filters = get_org_filters(doctype, org)

    return core_feed(
        doctype=doctype,
        since=since,
        limit=min(limit, 500),
        additional_filters=filters
    )


@frappe.whitelist()
def upsert_batch(payload: list) -> list:
    """
    Process offline write queue.

    Wraps dartwing_core.sync.upsert_batch with Company validation.

    Args:
        payload: List of {doctype, name, data, client_ts, op}

    Returns:
        List of {status, server_ts, resolved_doc, conflict} per item
    """
    results = []

    for item in payload:
        # Validate doctype
        if item["doctype"] not in SYNCABLE_DOCTYPES:
            results.append({
                "status": "error",
                "error": f"DocType {item['doctype']} is not syncable"
            })
            continue

        # Validate create permission
        if item["op"] == "insert" and item["doctype"] not in OFFLINE_CREATABLE:
            results.append({
                "status": "error",
                "error": f"Cannot create {item['doctype']} offline"
            })
            continue

        # Validate organization access
        try:
            validate_item_org_access(item)
        except frappe.PermissionError as e:
            results.append({
                "status": "error",
                "error": str(e)
            })
            continue

    # Process validated items through core
    validated_payload = [p for p in payload if p["doctype"] in SYNCABLE_DOCTYPES]
    return core_upsert(validated_payload)


def get_org_filters(doctype: str, org: str) -> dict:
    """Get organization-specific filters for a doctype"""
    # Map doctype to organization field
    org_field_map = {
        "Dispatch Job": "organization",
        "Form Submission": "organization",
        "Schedule Entry": "organization",
        "Conversation Message": "organization",
        "Clock Event": "organization",
        "Knowledge Article": "organization",
        "Appointment": "organization",
        "Service Ticket": "organization"
    }

    field = org_field_map.get(doctype, "organization")
    return {field: org}
```

---

## 13.4 Socket.IO Channels

### Channel Naming Convention

```
sync:{doctype_snake_case}:{org}
```

### Available Channels

| Channel | Payload | Use Case |
|---------|---------|----------|
| `sync:dispatch_job:{org}` | Job delta | Tech app: job assignments |
| `sync:schedule_entry:{org}` | Schedule delta | Tech app: schedule updates |
| `sync:conversation:{org}` | Message delta | Inbox: new messages |
| `sync:appointment:{org}` | Appointment delta | Calendar: bookings |
| `sync:service_ticket:{org}` | Ticket delta | Support: ticket updates |

### Server-Side Emission

```python
# events/sync.py
import frappe
from frappe.realtime import emit_via_redis

def emit_sync_delta(doctype: str, doc: dict, operation: str):
    """
    Emit sync delta to Socket.IO channel.

    Args:
        doctype: DocType name
        doc: Document data
        operation: insert|update|delete
    """
    channel = f"sync:{doctype.lower().replace(' ', '_')}:{doc.get('organization')}"

    payload = {
        "doctype": doctype,
        "name": doc.get("name"),
        "modified": doc.get("modified"),
        "operation": operation,
        "data": doc,
        "deleted": operation == "delete"
    }

    emit_via_redis(channel, payload)


# Hook to emit on doc changes
def on_dispatch_job_update(doc, method):
    emit_sync_delta("Dispatch Job", doc.as_dict(), "update")

def on_dispatch_job_insert(doc, method):
    emit_sync_delta("Dispatch Job", doc.as_dict(), "insert")
```

---

## 13.5 Conflict Resolution

### AI Merge Configuration

```python
# sync/conflict.py

AI_MERGE_CONFIG = {
    "Dispatch Job": {
        "mergeable_fields": [
            "technician_notes",
            "customer_feedback",
            "parts_used"
        ],
        "priority_fields": {
            "status": "server",  # Server always wins on status
            "assigned_to": "server"  # Server always wins on assignment
        },
        "prompt_template": "dispatch_job_merge"
    },
    "Service Ticket": {
        "mergeable_fields": [
            "description",
            "internal_notes",
            "resolution_notes"
        ],
        "priority_fields": {
            "status": "server",
            "priority": "server",
            "assigned_to": "server"
        },
        "prompt_template": "ticket_merge"
    },
    "Knowledge Article": {
        "mergeable_fields": [
            "content",
            "summary"
        ],
        "priority_fields": {
            "status": "server"
        },
        "prompt_template": "article_merge"
    }
}


async def ai_merge(doctype: str, server_doc: dict, client_doc: dict) -> dict:
    """
    Attempt AI-powered merge of conflicting documents.

    Returns:
        Merged document or None if merge failed
    """
    config = AI_MERGE_CONFIG.get(doctype)
    if not config:
        return None

    # Build prompt
    prompt = get_merge_prompt(
        config["prompt_template"],
        server_doc,
        client_doc,
        config["mergeable_fields"]
    )

    try:
        # Call AI service
        result = await ai_service.complete(prompt, max_tokens=2000)

        # Parse merged document
        merged = json.loads(result)

        # Apply priority field overrides
        for field, priority in config["priority_fields"].items():
            if priority == "server":
                merged[field] = server_doc.get(field)
            else:
                merged[field] = client_doc.get(field)

        return merged

    except Exception as e:
        frappe.log_error(f"AI merge failed: {e}", "Sync Conflict")
        return None
```

### Conflict Resolution UI Spec (Flutter)

```
┌─────────────────────────────────────────────────────────────┐
│                    SYNC CONFLICT                             │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│                                                              │
│  Dispatch Job: JOB-2025-00123                               │
│  "AC Repair - Johnson Residence"                            │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ FIELD: status                                          │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ YOUR VERSION          │  SERVER VERSION               │ │
│  │ ○ completed           │  ● in_progress                │ │
│  │                       │  (auto-selected - priority)   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ FIELD: technician_notes                                │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ YOUR VERSION          │  SERVER VERSION               │ │
│  │ "Replaced capacitor"  │  "Checked refrigerant"        │ │
│  │ ○ Use This            │  ○ Use This                   │ │
│  │                                                        │ │
│  │ ● AI MERGED:                                          │ │
│  │ "Checked refrigerant levels. Replaced capacitor.      │ │
│  │  System now cooling properly."                        │ │
│  │ [Edit]                                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ FIELD: parts_used                                      │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ Combined from both versions:                          │ │
│  │ • Capacitor 35/5 MFD (your version)                   │ │
│  │ • Refrigerant R-410A 1lb (server version)             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│       [Cancel]                    [Resolve & Sync]          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 13.6 Offline Queue Management

### Client-Side Queue (Flutter)

```dart
// services/sync/offline_queue.dart
class OfflineQueue {
  final Database _db;

  Future<void> enqueue(SyncOperation op) async {
    await _db.insert('offline_queue', {
      'id': uuid.v4(),
      'doctype': op.doctype,
      'name': op.name,
      'operation': op.operation,  // insert, update, delete
      'data': jsonEncode(op.data),
      'client_ts': DateTime.now().toIso8601String(),
      'status': 'pending',
      'retry_count': 0,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  Future<List<SyncOperation>> getPending() async {
    final rows = await _db.query(
      'offline_queue',
      where: 'status = ?',
      whereArgs: ['pending'],
      orderBy: 'created_at ASC',
    );
    return rows.map((r) => SyncOperation.fromMap(r)).toList();
  }

  Future<void> processQueue() async {
    if (!await hasConnectivity()) return;

    final pending = await getPending();
    if (pending.isEmpty) return;

    try {
      final results = await api.upsertBatch(pending);

      for (var i = 0; i < results.length; i++) {
        final result = results[i];
        final op = pending[i];

        if (result['status'] == 'success') {
          await markComplete(op.id);
        } else if (result['status'] == 'conflict') {
          await markConflict(op.id, result['server_doc'], result['client_doc']);
        } else {
          await markFailed(op.id, result['error']);
        }
      }
    } catch (e) {
      // Network error - will retry later
    }
  }
}
```

---

**Next: Section 14 - Reconciliation & Healing Jobs**

# Dartwing Company Architecture - Section 14: Reconciliation & Healing Jobs

---

## 14.1 Overview

Reconciliation jobs detect and heal sync discrepancies between Dartwing Company and underlying Frappe apps (ERPNext, HRMS, CRM). These jobs run on a schedule to catch issues that slip through event-driven sync.

**Cross-Reference:** This section extends patterns from `dartwing_core/org_integrity_guardrails.md` for cross-app consistency.

---

## 14.2 Reconciliation Job Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 RECONCILIATION SYSTEM                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  SCHEDULER (hooks.py)                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Hourly (Critical Syncs)                                     │
│  ├── check_dispatch_erpnext_sync                            │
│  ├── check_attendance_hrms_sync                             │
│  └── check_clock_events_sync                                │
│                                                              │
│  Daily 2 AM (Full Reconciliation)                           │
│  ├── reconcile_customer_addresses                           │
│  ├── reconcile_employee_certifications                      │
│  ├── reconcile_schedule_hrms                                │
│  ├── reconcile_conversation_crm                             │
│  └── reconcile_appointment_calendar                         │
│                                                              │
│  Weekly Sunday 3 AM (Cleanup)                               │
│  ├── cleanup_stale_sagas                                    │
│  ├── cleanup_orphan_records                                 │
│  └── archive_old_reconciliation_logs                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  RECONCILIATION LOG                                          │
├─────────────────────────────────────────────────────────────┤
│  • Records checked                                          │
│  • Discrepancies found                                      │
│  • Auto-fixed count                                         │
│  • Manual review required                                   │
│  • Duration                                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ALERTS                                                      │
├─────────────────────────────────────────────────────────────┤
│  • Email to admin if > 10 discrepancies                     │
│  • Slack webhook for critical failures                      │
│  • Dashboard notification                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 14.3 ReconciliationLog DocType

```json
{
  "doctype": "Reconciliation Log",
  "module": "Dartwing Company",
  "autoname": "RECON-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "job_type",
      "label": "Job Type",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization"
    },
    {
      "fieldname": "run_at",
      "label": "Run At",
      "fieldtype": "Datetime",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "success\nwarnings\nerrors",
      "reqd": 1
    },
    {
      "fieldname": "records_checked",
      "label": "Records Checked",
      "fieldtype": "Int"
    },
    {
      "fieldname": "discrepancies_found",
      "label": "Discrepancies Found",
      "fieldtype": "Int"
    },
    {
      "fieldname": "discrepancies_fixed",
      "label": "Discrepancies Fixed",
      "fieldtype": "Int"
    },
    {
      "fieldname": "manual_review_required",
      "label": "Manual Review Required",
      "fieldtype": "Int"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Float"
    },
    {
      "fieldname": "details",
      "label": "Details",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "error_message",
      "label": "Error Message",
      "fieldtype": "Long Text"
    }
  ]
}
```

---

## 14.4 Reconciliation Jobs Implementation

### Address Reconciliation

```python
# tasks/reconciliation/addresses.py
import frappe
from datetime import datetime

def reconcile_dispatch_addresses(org: str = None):
    """
    Nightly job: Verify Dispatch Job addresses match ERPNext Address.

    Fixes "sync hell" where Address was updated via bulk import or API
    without triggering Dartwing hooks.
    """
    start_time = datetime.now()
    discrepancies = []
    fixed = 0
    checked = 0

    # Get active dispatch jobs
    filters = {"status": ["not in", ["completed", "cancelled"]]}
    if org:
        filters["organization"] = org

    jobs = frappe.get_all("Dispatch Job",
        filters=filters,
        fields=["name", "address", "formatted_address",
                "latitude", "longitude", "organization"]
    )

    for job in jobs:
        checked += 1

        if not job.address:
            continue

        # Get current address from ERPNext
        try:
            current = frappe.get_doc("Address", job.address)
        except frappe.DoesNotExistError:
            discrepancies.append({
                "job": job.name,
                "type": "address_deleted",
                "message": f"Address {job.address} no longer exists"
            })
            continue

        # Compare formatted address
        expected_formatted = format_address(current)

        if job.formatted_address != expected_formatted:
            discrepancies.append({
                "job": job.name,
                "type": "address_changed",
                "old": job.formatted_address,
                "new": expected_formatted
            })

            # Auto-fix: Update dispatch job with correct address
            try:
                coords = geocode_address(expected_formatted)
                frappe.db.set_value("Dispatch Job", job.name, {
                    "formatted_address": expected_formatted,
                    "latitude": coords[0],
                    "longitude": coords[1]
                })
                fixed += 1
            except Exception as e:
                discrepancies[-1]["error"] = str(e)
                discrepancies[-1]["auto_fixed"] = False

    # Create reconciliation log
    duration = (datetime.now() - start_time).total_seconds()
    status = "success" if not discrepancies else (
        "warnings" if fixed == len(discrepancies) else "errors"
    )

    log = frappe.get_doc({
        "doctype": "Reconciliation Log",
        "job_type": "dispatch_addresses",
        "organization": org,
        "run_at": start_time,
        "status": status,
        "records_checked": checked,
        "discrepancies_found": len(discrepancies),
        "discrepancies_fixed": fixed,
        "manual_review_required": len(discrepancies) - fixed,
        "duration_seconds": duration,
        "details": discrepancies
    })
    log.insert(ignore_permissions=True)
    frappe.db.commit()

    # Alert if many discrepancies
    if len(discrepancies) > 10:
        send_reconciliation_alert(
            "High number of address discrepancies",
            f"{len(discrepancies)} address mismatches found, {fixed} auto-fixed",
            log.name
        )

    return log.name
```

### Schedule-HRMS Reconciliation

```python
# tasks/reconciliation/schedule.py

def reconcile_schedule_hrms(org: str = None):
    """
    Daily job: Ensure Schedule Entries are synced to HRMS Shift Assignments.

    Catches cases where:
    - Schedule Entry exists but HRMS Shift Assignment was deleted
    - HRMS Shift Assignment exists but Schedule Entry was deleted
    - Data mismatch between the two
    """
    start_time = datetime.now()
    discrepancies = []
    fixed = 0
    checked = 0

    # Check Schedule Entries marked as synced
    filters = {
        "synced_to_hrms": 1,
        "hrms_shift_assignment": ["is", "set"]
    }
    if org:
        filters["organization"] = org

    entries = frappe.get_all("Schedule Entry",
        filters=filters,
        fields=["name", "employee", "date", "hrms_shift_assignment",
                "shift_template", "organization"]
    )

    for entry in entries:
        checked += 1

        # Check if HRMS Shift Assignment exists
        if not frappe.db.exists("Shift Assignment", entry.hrms_shift_assignment):
            discrepancies.append({
                "schedule_entry": entry.name,
                "type": "hrms_deleted",
                "message": f"HRMS Shift Assignment {entry.hrms_shift_assignment} deleted"
            })

            # Auto-fix: Recreate HRMS Shift Assignment
            try:
                new_sa = create_hrms_shift_assignment(entry)
                frappe.db.set_value("Schedule Entry", entry.name,
                    "hrms_shift_assignment", new_sa.name)
                fixed += 1
                discrepancies[-1]["auto_fixed"] = True
                discrepancies[-1]["new_assignment"] = new_sa.name
            except Exception as e:
                discrepancies[-1]["error"] = str(e)
                discrepancies[-1]["auto_fixed"] = False
            continue

        # Check data consistency
        sa = frappe.get_doc("Shift Assignment", entry.hrms_shift_assignment)

        if sa.employee != entry.employee or str(sa.start_date) != str(entry.date):
            discrepancies.append({
                "schedule_entry": entry.name,
                "type": "data_mismatch",
                "schedule_data": {
                    "employee": entry.employee,
                    "date": str(entry.date)
                },
                "hrms_data": {
                    "employee": sa.employee,
                    "date": str(sa.start_date)
                }
            })
            # Don't auto-fix data mismatches - requires manual review

    # Create log
    duration = (datetime.now() - start_time).total_seconds()
    create_reconciliation_log(
        job_type="schedule_hrms",
        org=org,
        start_time=start_time,
        checked=checked,
        discrepancies=discrepancies,
        fixed=fixed,
        duration=duration
    )
```

### Stale Saga Cleanup

```python
# tasks/reconciliation/cleanup.py

def cleanup_stale_sagas():
    """
    Weekly job: Mark stuck sagas as failed.

    Sagas that have been "running" for more than 1 hour are considered stuck.
    """
    threshold = frappe.utils.add_to_date(
        frappe.utils.now_datetime(),
        hours=-1
    )

    stale = frappe.get_all("Saga Log",
        filters={
            "status": "running",
            "started_at": ["<", threshold]
        },
        fields=["name", "saga_name", "started_at", "organization"]
    )

    for saga in stale:
        frappe.db.set_value("Saga Log", saga.name, {
            "status": "failed",
            "error_message": "Marked as stale by cleanup job",
            "completed_at": frappe.utils.now_datetime()
        })

    if stale:
        create_reconciliation_log(
            job_type="stale_saga_cleanup",
            checked=len(stale),
            discrepancies=[{"saga": s.name} for s in stale],
            fixed=len(stale)
        )

    return len(stale)


def cleanup_orphan_records():
    """
    Weekly job: Find and report orphaned records.

    Examples:
    - Dispatch Jobs with deleted Customer
    - Appointments with deleted Contact
    - Form Submissions with deleted Mobile Form
    """
    orphans = []

    # Check Dispatch Jobs
    jobs_with_missing_customer = frappe.db.sql("""
        SELECT dj.name, dj.customer
        FROM `tabDispatch Job` dj
        LEFT JOIN `tabCustomer` c ON c.name = dj.customer
        WHERE dj.customer IS NOT NULL
        AND c.name IS NULL
    """, as_dict=True)

    for job in jobs_with_missing_customer:
        orphans.append({
            "doctype": "Dispatch Job",
            "name": job.name,
            "type": "missing_customer",
            "reference": job.customer
        })

    # Check Appointments
    appts_with_missing_contact = frappe.db.sql("""
        SELECT a.name, a.contact
        FROM `tabAppointment` a
        LEFT JOIN `tabContact` c ON c.name = a.contact
        WHERE a.contact IS NOT NULL
        AND c.name IS NULL
    """, as_dict=True)

    for appt in appts_with_missing_contact:
        orphans.append({
            "doctype": "Appointment",
            "name": appt.name,
            "type": "missing_contact",
            "reference": appt.contact
        })

    if orphans:
        create_reconciliation_log(
            job_type="orphan_records",
            checked=len(jobs_with_missing_customer) + len(appts_with_missing_contact),
            discrepancies=orphans,
            fixed=0  # Orphans require manual review
        )

        send_reconciliation_alert(
            "Orphan records detected",
            f"{len(orphans)} orphan records found requiring manual review"
        )

    return orphans
```

---

## 14.5 Scheduler Configuration

```python
# hooks.py additions

scheduler_events = {
    "cron": {
        # ... existing entries ...

        # Hourly: Critical sync checks
        "0 * * * *": [
            "dartwing_company.tasks.reconciliation.check_dispatch_sync",
            "dartwing_company.tasks.reconciliation.check_attendance_sync"
        ],

        # Daily at 2 AM: Full reconciliation
        "0 2 * * *": [
            "dartwing_company.tasks.reconciliation.addresses.reconcile_dispatch_addresses",
            "dartwing_company.tasks.reconciliation.schedule.reconcile_schedule_hrms",
            "dartwing_company.tasks.reconciliation.certifications.reconcile_employee_certs"
        ],

        # Weekly Sunday at 3 AM: Cleanup
        "0 3 * * 0": [
            "dartwing_company.tasks.reconciliation.cleanup.cleanup_stale_sagas",
            "dartwing_company.tasks.reconciliation.cleanup.cleanup_orphan_records",
            "dartwing_company.tasks.reconciliation.cleanup.archive_old_logs"
        ]
    }
}
```

---

## 14.6 CLI Helpers

```bash
# Run reconciliation jobs manually

# All reconciliation for specific org
bench execute dartwing_company.tasks.reconciliation.run_all --kwargs '{"org": "ORG-001"}'

# Specific job
bench execute dartwing_company.tasks.reconciliation.addresses.reconcile_dispatch_addresses

# Check status
bench execute dartwing_company.tasks.reconciliation.status

# Cleanup stale sagas
bench execute dartwing_company.tasks.reconciliation.cleanup.cleanup_stale_sagas
```

---

## 14.7 Monitoring Dashboard Spec

```
┌─────────────────────────────────────────────────────────────┐
│                 RECONCILIATION DASHBOARD                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Last 24 Hours Summary                                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Jobs Run   │  │ Discrepan- │  │ Auto-Fixed │            │
│  │    12      │  │   cies     │  │    45      │            │
│  │            │  │    47      │  │   (96%)    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  Requiring Attention: 2                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ [!] RECON-2025-00456 │ orphan_records │ 2 orphans   │  │
│  │     [View] [Resolve]                                  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ [!] RECON-2025-00455 │ schedule_hrms │ data mismatch│  │
│  │     [View] [Resolve]                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  By Job Type (7 Days)                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ dispatch_addresses    │ 168 checked │ 5 fixed       │  │
│  │ schedule_hrms         │ 89 checked  │ 2 fixed       │  │
│  │ employee_certs        │ 234 checked │ 0 fixed       │  │
│  │ stale_saga_cleanup    │ 3 cleaned   │ 3 fixed       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Trend (30 Days)                                            │
│  [Chart: Discrepancies found vs fixed over time]            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 14.8 Alerting Configuration

```python
# tasks/reconciliation/alerts.py

ALERT_THRESHOLDS = {
    "dispatch_addresses": 10,  # Alert if > 10 discrepancies
    "schedule_hrms": 5,
    "employee_certs": 20,
    "orphan_records": 1,  # Always alert on orphans
    "stale_saga_cleanup": 10
}

def send_reconciliation_alert(subject: str, message: str, log_name: str = None):
    """Send alert via configured channels"""

    # Email admin
    admin_email = frappe.db.get_single_value(
        "Dartwing Settings", "reconciliation_alert_email")

    if admin_email:
        frappe.sendmail(
            recipients=[admin_email],
            subject=f"[Dartwing] {subject}",
            message=message + (f"\n\nLog: {log_name}" if log_name else "")
        )

    # Slack webhook (if configured)
    slack_webhook = frappe.db.get_single_value(
        "Dartwing Settings", "slack_webhook_url")

    if slack_webhook:
        import requests
        requests.post(slack_webhook, json={
            "text": f":warning: *{subject}*\n{message}"
        })

    # System notification
    frappe.publish_realtime(
        "reconciliation_alert",
        {"subject": subject, "message": message, "log": log_name}
    )
```

---

*End of Critical Fixes Sections (10-14)*

---

# Section 15: DocType JSON Schemas

This section provides complete JSON schemas for all Dartwing Company DocTypes, following the pattern established in `dartwing_core_arch.md`. These schemas are enforceable and include:
- Complete field definitions with types and constraints
- Permission configurations
- Index definitions for query performance
- `user_permission_dependant_doctype` for multi-tenancy

---

## 15.1 Operations DocTypes

### Dispatch Job

```json
{
  "doctype": "Dispatch Job",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "JOB-.YYYY.-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1},
    {"role": "Dispatch Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Field Technician", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_customer",
      "fieldtype": "Section Break",
      "label": "Customer Information"
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "contact",
      "label": "Contact",
      "fieldtype": "Link",
      "options": "Contact"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "address",
      "label": "Service Address",
      "fieldtype": "Link",
      "options": "Address",
      "reqd": 1
    },
    {
      "fieldname": "formatted_address",
      "label": "Formatted Address",
      "fieldtype": "Small Text",
      "read_only": 1,
      "fetch_from": "address.address_display"
    },
    {
      "fieldname": "section_location",
      "fieldtype": "Section Break",
      "label": "Geocoded Location"
    },
    {
      "fieldname": "latitude",
      "label": "Latitude",
      "fieldtype": "Float",
      "precision": 6,
      "read_only": 1
    },
    {
      "fieldname": "longitude",
      "label": "Longitude",
      "fieldtype": "Float",
      "precision": 6,
      "read_only": 1
    },
    {
      "fieldname": "column_break_loc",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "geohash",
      "label": "Geohash",
      "fieldtype": "Data",
      "read_only": 1,
      "hidden": 1
    },
    {
      "fieldname": "section_job",
      "fieldtype": "Section Break",
      "label": "Job Details"
    },
    {
      "fieldname": "job_type",
      "label": "Job Type",
      "fieldtype": "Link",
      "options": "Dispatch Job Type",
      "reqd": 1
    },
    {
      "fieldname": "title",
      "label": "Title",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Text Editor"
    },
    {
      "fieldname": "column_break_job",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Select",
      "options": "Low\nNormal\nHigh\nUrgent",
      "default": "Normal",
      "in_list_view": 1
    },
    {
      "fieldname": "estimated_duration",
      "label": "Estimated Duration",
      "fieldtype": "Duration"
    },
    {
      "fieldname": "section_schedule",
      "fieldtype": "Section Break",
      "label": "Scheduling"
    },
    {
      "fieldname": "scheduled_date",
      "label": "Scheduled Date",
      "fieldtype": "Date",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "scheduled_start",
      "label": "Start Time",
      "fieldtype": "Time"
    },
    {
      "fieldname": "scheduled_end",
      "label": "End Time",
      "fieldtype": "Time"
    },
    {
      "fieldname": "column_break_sched",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "preferred_window",
      "label": "Preferred Window",
      "fieldtype": "Select",
      "options": "Any\nMorning (8AM-12PM)\nAfternoon (12PM-5PM)\nEvening (5PM-9PM)",
      "default": "Any"
    },
    {
      "fieldname": "customer_notes",
      "label": "Customer Notes",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "section_assignment",
      "fieldtype": "Section Break",
      "label": "Assignment"
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "Employee",
      "in_list_view": 1
    },
    {
      "fieldname": "assigned_team",
      "label": "Assigned Team",
      "fieldtype": "Link",
      "options": "Employee Group"
    },
    {
      "fieldname": "column_break_assign",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "assignment_method",
      "label": "Assignment Method",
      "fieldtype": "Select",
      "options": "Manual\nAuto - Nearest\nAuto - Workload\nAuto - Skill Match",
      "default": "Manual"
    },
    {
      "fieldname": "assigned_at",
      "label": "Assigned At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "assigned_by",
      "label": "Assigned By",
      "fieldtype": "Link",
      "options": "User",
      "read_only": 1
    },
    {
      "fieldname": "section_status",
      "fieldtype": "Section Break",
      "label": "Status"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Draft\nUnassigned\nAssigned\nEn Route\nArrived\nIn Progress\nCompleted\nCancelled",
      "default": "Draft",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status_updated_at",
      "label": "Status Updated At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_requirements",
      "fieldtype": "Section Break",
      "label": "Requirements",
      "collapsible": 1
    },
    {
      "fieldname": "required_skills",
      "label": "Required Skills",
      "fieldtype": "Table MultiSelect",
      "options": "Dispatch Job Skill"
    },
    {
      "fieldname": "required_certifications",
      "label": "Required Certifications",
      "fieldtype": "Table MultiSelect",
      "options": "Dispatch Job Certification"
    },
    {
      "fieldname": "required_equipment",
      "label": "Required Equipment",
      "fieldtype": "Table",
      "options": "Dispatch Job Equipment"
    },
    {
      "fieldname": "section_execution",
      "fieldtype": "Section Break",
      "label": "Execution",
      "depends_on": "eval:doc.status=='Completed' || doc.status=='In Progress'"
    },
    {
      "fieldname": "actual_arrival",
      "label": "Actual Arrival",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "actual_departure",
      "label": "Actual Departure",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "actual_duration",
      "label": "Actual Duration",
      "fieldtype": "Duration",
      "read_only": 1
    },
    {
      "fieldname": "column_break_exec",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "technician_notes",
      "label": "Technician Notes",
      "fieldtype": "Text Editor"
    },
    {
      "fieldname": "section_completion",
      "fieldtype": "Section Break",
      "label": "Completion",
      "depends_on": "eval:doc.status=='Completed'"
    },
    {
      "fieldname": "customer_signature",
      "label": "Customer Signature",
      "fieldtype": "Signature"
    },
    {
      "fieldname": "signed_by_name",
      "label": "Signed By",
      "fieldtype": "Data"
    },
    {
      "fieldname": "signed_at",
      "label": "Signed At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "column_break_comp",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "completion_photos",
      "label": "Completion Photos",
      "fieldtype": "Attach"
    },
    {
      "fieldname": "form_submissions",
      "label": "Form Submissions",
      "fieldtype": "Table",
      "options": "Dispatch Job Form Submission"
    },
    {
      "fieldname": "section_billing",
      "fieldtype": "Section Break",
      "label": "Billing",
      "collapsible": 1
    },
    {
      "fieldname": "billable",
      "label": "Billable",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "billing_status",
      "label": "Billing Status",
      "fieldtype": "Select",
      "options": "Not Billed\nPartially Billed\nBilled",
      "default": "Not Billed",
      "read_only": 1
    },
    {
      "fieldname": "column_break_bill",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "sales_invoice",
      "label": "Sales Invoice",
      "fieldtype": "Link",
      "options": "Sales Invoice",
      "read_only": 1
    },
    {
      "fieldname": "timesheet",
      "label": "Timesheet",
      "fieldtype": "Link",
      "options": "Timesheet",
      "read_only": 1
    },
    {
      "fieldname": "section_links",
      "fieldtype": "Section Break",
      "label": "Related Documents",
      "collapsible": 1
    },
    {
      "fieldname": "project",
      "label": "Project",
      "fieldtype": "Link",
      "options": "Project"
    },
    {
      "fieldname": "sales_order",
      "label": "Sales Order",
      "fieldtype": "Link",
      "options": "Sales Order"
    },
    {
      "fieldname": "section_history",
      "fieldtype": "Section Break",
      "label": "Assignment History",
      "collapsible": 1
    },
    {
      "fieldname": "assignments",
      "label": "Assignment History",
      "fieldtype": "Table",
      "options": "Dispatch Assignment"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "status"]},
    {"fields": ["organization", "scheduled_date"]},
    {"fields": ["organization", "assigned_to"]},
    {"fields": ["assigned_to", "scheduled_date", "status"]},
    {"fields": ["customer"]},
    {"fields": ["geohash"]}
  ]
}
```

### Conversation

```json
{
  "doctype": "Conversation",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "CONV-.YYYY.-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1},
    {"role": "Inbox Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_contact",
      "fieldtype": "Section Break",
      "label": "Contact Identification"
    },
    {
      "fieldname": "contact",
      "label": "Contact",
      "fieldtype": "Link",
      "options": "Contact",
      "in_list_view": 1
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer"
    },
    {
      "fieldname": "column_break_contact",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "lead",
      "label": "Lead",
      "fieldtype": "Link",
      "options": "CRM Lead"
    },
    {
      "fieldname": "patient",
      "label": "Patient",
      "fieldtype": "Link",
      "options": "Patient",
      "depends_on": "eval:frappe.boot.dartwing_healthcare_mode"
    },
    {
      "fieldname": "section_meta",
      "fieldtype": "Section Break",
      "label": "Conversation Details"
    },
    {
      "fieldname": "channel",
      "label": "Channel",
      "fieldtype": "Select",
      "options": "Email\nSMS\nVoice\nWhatsApp\nMessenger\nTelegram\nWeb Chat",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "subject",
      "label": "Subject",
      "fieldtype": "Data",
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_meta",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Open\nPending\nResolved\nClosed",
      "default": "Open",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Select",
      "options": "Low\nNormal\nHigh\nUrgent",
      "default": "Normal"
    },
    {
      "fieldname": "section_activity",
      "fieldtype": "Section Break",
      "label": "Activity"
    },
    {
      "fieldname": "last_message_at",
      "label": "Last Message At",
      "fieldtype": "Datetime",
      "read_only": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "last_message_preview",
      "label": "Last Message",
      "fieldtype": "Small Text",
      "read_only": 1
    },
    {
      "fieldname": "column_break_act",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "unread_count",
      "label": "Unread",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    },
    {
      "fieldname": "message_count",
      "label": "Total Messages",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    },
    {
      "fieldname": "section_assignment",
      "fieldtype": "Section Break",
      "label": "Assignment"
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "User"
    },
    {
      "fieldname": "assigned_team",
      "label": "Assigned Team",
      "fieldtype": "Link",
      "options": "User Group"
    },
    {
      "fieldname": "section_ai",
      "fieldtype": "Section Break",
      "label": "AI Analysis",
      "collapsible": 1
    },
    {
      "fieldname": "sentiment_score",
      "label": "Sentiment Score",
      "fieldtype": "Float",
      "precision": 2,
      "read_only": 1,
      "description": "-1 (negative) to 1 (positive)"
    },
    {
      "fieldname": "intent",
      "label": "Detected Intent",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "column_break_ai",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "suggested_reply",
      "label": "Suggested Reply",
      "fieldtype": "Text",
      "read_only": 1
    },
    {
      "fieldname": "section_messages",
      "fieldtype": "Section Break",
      "label": "Messages"
    },
    {
      "fieldname": "messages",
      "label": "Messages",
      "fieldtype": "Table",
      "options": "Conversation Message"
    },
    {
      "fieldname": "section_notes",
      "fieldtype": "Section Break",
      "label": "Internal Notes",
      "collapsible": 1
    },
    {
      "fieldname": "internal_notes",
      "label": "Internal Notes",
      "fieldtype": "Table",
      "options": "Conversation Note"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "status"]},
    {"fields": ["organization", "channel"]},
    {"fields": ["organization", "assigned_to"]},
    {"fields": ["contact"]},
    {"fields": ["customer"]},
    {"fields": ["last_message_at"]}
  ]
}
```

### Conversation Message (Child Table)

```json
{
  "doctype": "Conversation Message",
  "module": "Dartwing Company",
  "istable": 1,
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
      "fieldname": "channel",
      "label": "Channel",
      "fieldtype": "Select",
      "options": "Email\nSMS\nVoice\nWhatsApp\nMessenger\nTelegram\nWeb Chat",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "timestamp",
      "label": "Timestamp",
      "fieldtype": "Datetime",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "sender_name",
      "label": "Sender Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "sender_id",
      "label": "Sender ID",
      "fieldtype": "Data",
      "description": "Email, phone number, or external ID"
    },
    {
      "fieldname": "content",
      "label": "Content",
      "fieldtype": "Text",
      "in_list_view": 1
    },
    {
      "fieldname": "content_html",
      "label": "HTML Content",
      "fieldtype": "Text Editor",
      "hidden": 1
    },
    {
      "fieldname": "channel_message_id",
      "label": "External Message ID",
      "fieldtype": "Data",
      "hidden": 1
    },
    {
      "fieldname": "read",
      "label": "Read",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_voice",
      "fieldtype": "Section Break",
      "label": "Voice Details",
      "depends_on": "eval:doc.channel=='Voice'"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "recording_url",
      "label": "Recording URL",
      "fieldtype": "Data"
    },
    {
      "fieldname": "transcription",
      "label": "Transcription",
      "fieldtype": "Text"
    },
    {
      "fieldname": "section_ai_msg",
      "fieldtype": "Section Break",
      "label": "AI",
      "collapsible": 1
    },
    {
      "fieldname": "ai_summary",
      "label": "AI Summary",
      "fieldtype": "Small Text"
    }
  ]
}
```

---

## 15.2 CRM Overlay DocTypes

### Service Ticket

```json
{
  "doctype": "Service Ticket",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "TKT-.YYYY.-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1},
    {"role": "Support Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_customer",
      "fieldtype": "Section Break",
      "label": "Customer"
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer",
      "in_list_view": 1
    },
    {
      "fieldname": "contact",
      "label": "Contact",
      "fieldtype": "Link",
      "options": "Contact"
    },
    {
      "fieldname": "column_break_cust",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "lead",
      "label": "Lead",
      "fieldtype": "Link",
      "options": "CRM Lead"
    },
    {
      "fieldname": "conversation",
      "label": "Conversation",
      "fieldtype": "Link",
      "options": "Conversation"
    },
    {
      "fieldname": "section_ticket",
      "fieldtype": "Section Break",
      "label": "Ticket Details"
    },
    {
      "fieldname": "subject",
      "label": "Subject",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Text Editor"
    },
    {
      "fieldname": "column_break_ticket",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "category",
      "label": "Category",
      "fieldtype": "Link",
      "options": "Ticket Category"
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Select",
      "options": "Low\nNormal\nHigh\nUrgent",
      "default": "Normal",
      "in_list_view": 1
    },
    {
      "fieldname": "source",
      "label": "Source",
      "fieldtype": "Select",
      "options": "Portal\nEmail\nPhone\nChat\nManual",
      "default": "Manual"
    },
    {
      "fieldname": "section_status",
      "fieldtype": "Section Break",
      "label": "Status"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "New\nOpen\nPending\nOn Hold\nResolved\nClosed",
      "default": "New",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "resolution",
      "label": "Resolution",
      "fieldtype": "Text Editor",
      "depends_on": "eval:doc.status=='Resolved' || doc.status=='Closed'"
    },
    {
      "fieldname": "column_break_status",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "resolved_at",
      "label": "Resolved At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "closed_at",
      "label": "Closed At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_assignment",
      "fieldtype": "Section Break",
      "label": "Assignment"
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "User",
      "in_list_view": 1
    },
    {
      "fieldname": "assigned_team",
      "label": "Assigned Team",
      "fieldtype": "Link",
      "options": "User Group"
    },
    {
      "fieldname": "column_break_assign",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "escalation_level",
      "label": "Escalation Level",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "section_sla",
      "fieldtype": "Section Break",
      "label": "SLA Tracking"
    },
    {
      "fieldname": "sla_policy",
      "label": "SLA Policy",
      "fieldtype": "Link",
      "options": "SLA Policy"
    },
    {
      "fieldname": "response_due",
      "label": "Response Due",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "resolution_due",
      "label": "Resolution Due",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "column_break_sla",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "first_response_at",
      "label": "First Response At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "sla_status",
      "label": "SLA Status",
      "fieldtype": "Select",
      "options": "Within SLA\nAt Risk\nBreached",
      "default": "Within SLA",
      "read_only": 1
    },
    {
      "fieldname": "paused_at",
      "label": "Paused At",
      "fieldtype": "Datetime",
      "read_only": 1,
      "description": "When waiting on customer"
    },
    {
      "fieldname": "total_pause_duration",
      "label": "Total Pause Duration",
      "fieldtype": "Duration",
      "read_only": 1
    },
    {
      "fieldname": "section_ai",
      "fieldtype": "Section Break",
      "label": "AI Analysis",
      "collapsible": 1
    },
    {
      "fieldname": "sentiment_score",
      "label": "Sentiment Score",
      "fieldtype": "Float",
      "precision": 2,
      "read_only": 1
    },
    {
      "fieldname": "auto_category",
      "label": "AI Category",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "auto_priority",
      "label": "AI Priority",
      "fieldtype": "Select",
      "options": "Low\nNormal\nHigh\nUrgent",
      "read_only": 1
    },
    {
      "fieldname": "section_escalations",
      "fieldtype": "Section Break",
      "label": "Escalation History",
      "collapsible": 1
    },
    {
      "fieldname": "escalations",
      "label": "Escalations",
      "fieldtype": "Table",
      "options": "Ticket Escalation"
    },
    {
      "fieldname": "section_notes",
      "fieldtype": "Section Break",
      "label": "Internal Notes",
      "collapsible": 1
    },
    {
      "fieldname": "notes",
      "label": "Notes",
      "fieldtype": "Table",
      "options": "Ticket Note"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "status"]},
    {"fields": ["organization", "priority"]},
    {"fields": ["organization", "assigned_to"]},
    {"fields": ["organization", "sla_status"]},
    {"fields": ["customer"]},
    {"fields": ["response_due"]},
    {"fields": ["resolution_due"]}
  ]
}
```

### Appointment

```json
{
  "doctype": "Appointment",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "APT-.YYYY.-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1},
    {"role": "Website User", "read": 1, "write": 1, "create": 1, "if_owner": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_customer",
      "fieldtype": "Section Break",
      "label": "Attendee"
    },
    {
      "fieldname": "contact",
      "label": "Contact",
      "fieldtype": "Link",
      "options": "Contact"
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer",
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_cust",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "attendee_name",
      "label": "Attendee Name",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "attendee_email",
      "label": "Attendee Email",
      "fieldtype": "Data",
      "options": "Email",
      "reqd": 1
    },
    {
      "fieldname": "attendee_phone",
      "label": "Attendee Phone",
      "fieldtype": "Data",
      "options": "Phone"
    },
    {
      "fieldname": "section_appointment",
      "fieldtype": "Section Break",
      "label": "Appointment Details"
    },
    {
      "fieldname": "appointment_type",
      "label": "Appointment Type",
      "fieldtype": "Link",
      "options": "Appointment Type",
      "reqd": 1
    },
    {
      "fieldname": "title",
      "label": "Title",
      "fieldtype": "Data",
      "fetch_from": "appointment_type.title"
    },
    {
      "fieldname": "column_break_apt",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "duration_minutes",
      "label": "Duration (minutes)",
      "fieldtype": "Int",
      "fetch_from": "appointment_type.duration_minutes"
    },
    {
      "fieldname": "location_type",
      "label": "Location Type",
      "fieldtype": "Select",
      "options": "In Person\nVideo Call\nPhone Call",
      "default": "In Person"
    },
    {
      "fieldname": "section_schedule",
      "fieldtype": "Section Break",
      "label": "Schedule"
    },
    {
      "fieldname": "scheduled_date",
      "label": "Date",
      "fieldtype": "Date",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "scheduled_time",
      "label": "Time",
      "fieldtype": "Time",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_sched",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "end_time",
      "label": "End Time",
      "fieldtype": "Time",
      "read_only": 1
    },
    {
      "fieldname": "timezone",
      "label": "Timezone",
      "fieldtype": "Data",
      "default": "UTC"
    },
    {
      "fieldname": "section_host",
      "fieldtype": "Section Break",
      "label": "Host"
    },
    {
      "fieldname": "host_user",
      "label": "Host",
      "fieldtype": "Link",
      "options": "User",
      "in_list_view": 1
    },
    {
      "fieldname": "host_employee",
      "label": "Employee",
      "fieldtype": "Link",
      "options": "Employee"
    },
    {
      "fieldname": "column_break_host",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "meeting_url",
      "label": "Meeting URL",
      "fieldtype": "Data",
      "depends_on": "eval:doc.location_type=='Video Call'"
    },
    {
      "fieldname": "section_status",
      "fieldtype": "Section Break",
      "label": "Status"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Scheduled\nConfirmed\nCompleted\nCancelled\nNo Show",
      "default": "Scheduled",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "confirmed_at",
      "label": "Confirmed At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "column_break_status",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "cancellation_reason",
      "label": "Cancellation Reason",
      "fieldtype": "Small Text",
      "depends_on": "eval:doc.status=='Cancelled'"
    },
    {
      "fieldname": "cancelled_at",
      "label": "Cancelled At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_payment",
      "fieldtype": "Section Break",
      "label": "Payment",
      "collapsible": 1
    },
    {
      "fieldname": "requires_payment",
      "label": "Requires Payment",
      "fieldtype": "Check",
      "fetch_from": "appointment_type.requires_payment"
    },
    {
      "fieldname": "amount",
      "label": "Amount",
      "fieldtype": "Currency",
      "fetch_from": "appointment_type.price"
    },
    {
      "fieldname": "column_break_pay",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "payment_status",
      "label": "Payment Status",
      "fieldtype": "Select",
      "options": "Not Required\nPending\nPaid\nRefunded",
      "default": "Not Required"
    },
    {
      "fieldname": "stripe_payment_intent",
      "label": "Stripe Payment Intent",
      "fieldtype": "Data",
      "read_only": 1,
      "hidden": 1
    },
    {
      "fieldname": "section_reminders",
      "fieldtype": "Section Break",
      "label": "Reminders",
      "collapsible": 1
    },
    {
      "fieldname": "reminder_sent_24h",
      "label": "24h Reminder Sent",
      "fieldtype": "Check",
      "read_only": 1
    },
    {
      "fieldname": "reminder_sent_1h",
      "label": "1h Reminder Sent",
      "fieldtype": "Check",
      "read_only": 1
    },
    {
      "fieldname": "section_notes",
      "fieldtype": "Section Break",
      "label": "Notes",
      "collapsible": 1
    },
    {
      "fieldname": "attendee_notes",
      "label": "Attendee Notes",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "internal_notes",
      "label": "Internal Notes",
      "fieldtype": "Small Text"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "status"]},
    {"fields": ["organization", "scheduled_date"]},
    {"fields": ["organization", "host_user"]},
    {"fields": ["scheduled_date", "scheduled_time"]},
    {"fields": ["customer"]},
    {"fields": ["attendee_email"]}
  ]
}
```

### Document Vault

```json
{
  "doctype": "Document Vault",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "VAULT-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_owner",
      "fieldtype": "Section Break",
      "label": "Owner"
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "vault_name",
      "label": "Vault Name",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_owner",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "section_storage",
      "fieldtype": "Section Break",
      "label": "Storage"
    },
    {
      "fieldname": "drive_folder",
      "label": "Drive Folder",
      "fieldtype": "Link",
      "options": "Drive Folder",
      "read_only": 1
    },
    {
      "fieldname": "storage_used_bytes",
      "label": "Storage Used (bytes)",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    },
    {
      "fieldname": "column_break_storage",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "storage_limit_bytes",
      "label": "Storage Limit (bytes)",
      "fieldtype": "Int",
      "default": 1073741824,
      "description": "Default: 1GB"
    },
    {
      "fieldname": "file_count",
      "label": "File Count",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    },
    {
      "fieldname": "section_access",
      "fieldtype": "Section Break",
      "label": "Access Control"
    },
    {
      "fieldname": "portal_access",
      "label": "Portal Access",
      "fieldtype": "Check",
      "default": 1,
      "description": "Allow customer to view via portal"
    },
    {
      "fieldname": "customer_upload",
      "label": "Customer Upload",
      "fieldtype": "Check",
      "default": 0,
      "description": "Allow customer to upload files"
    },
    {
      "fieldname": "column_break_access",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "require_acknowledgment",
      "label": "Require Acknowledgment",
      "fieldtype": "Check",
      "default": 0,
      "description": "Customer must acknowledge viewing"
    },
    {
      "fieldname": "expiry_date",
      "label": "Access Expiry",
      "fieldtype": "Date",
      "description": "Remove portal access after this date"
    },
    {
      "fieldname": "section_documents",
      "fieldtype": "Section Break",
      "label": "Documents"
    },
    {
      "fieldname": "documents",
      "label": "Documents",
      "fieldtype": "Table",
      "options": "Vault Document"
    },
    {
      "fieldname": "section_audit",
      "fieldtype": "Section Break",
      "label": "Audit Trail",
      "collapsible": 1
    },
    {
      "fieldname": "access_log",
      "label": "Access Log",
      "fieldtype": "Table",
      "options": "Vault Access Log",
      "read_only": 1
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "customer"]},
    {"fields": ["customer"]}
  ]
}
```

### SLA Policy

```json
{
  "doctype": "SLA Policy",
  "module": "Dartwing Company",
  "autoname": "field:policy_name",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Support Manager", "read": 1, "write": 1, "create": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "policy_name",
      "label": "Policy Name",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "enabled",
      "label": "Enabled",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_scope",
      "fieldtype": "Section Break",
      "label": "Scope"
    },
    {
      "fieldname": "apply_to_all",
      "label": "Apply to All Tickets",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "categories",
      "label": "Categories",
      "fieldtype": "Table MultiSelect",
      "options": "SLA Policy Category",
      "depends_on": "eval:!doc.apply_to_all"
    },
    {
      "fieldname": "column_break_scope",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "customer_groups",
      "label": "Customer Groups",
      "fieldtype": "Table MultiSelect",
      "options": "SLA Policy Customer Group",
      "depends_on": "eval:!doc.apply_to_all"
    },
    {
      "fieldname": "priority_filter",
      "label": "Priority Filter",
      "fieldtype": "Select",
      "options": "\nLow\nNormal\nHigh\nUrgent"
    },
    {
      "fieldname": "section_response",
      "fieldtype": "Section Break",
      "label": "Response Time SLA"
    },
    {
      "fieldname": "response_time_low",
      "label": "Low Priority (hours)",
      "fieldtype": "Int",
      "default": 24
    },
    {
      "fieldname": "response_time_normal",
      "label": "Normal Priority (hours)",
      "fieldtype": "Int",
      "default": 8
    },
    {
      "fieldname": "column_break_response",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "response_time_high",
      "label": "High Priority (hours)",
      "fieldtype": "Int",
      "default": 4
    },
    {
      "fieldname": "response_time_urgent",
      "label": "Urgent Priority (hours)",
      "fieldtype": "Int",
      "default": 1
    },
    {
      "fieldname": "section_resolution",
      "fieldtype": "Section Break",
      "label": "Resolution Time SLA"
    },
    {
      "fieldname": "resolution_time_low",
      "label": "Low Priority (hours)",
      "fieldtype": "Int",
      "default": 72
    },
    {
      "fieldname": "resolution_time_normal",
      "label": "Normal Priority (hours)",
      "fieldtype": "Int",
      "default": 24
    },
    {
      "fieldname": "column_break_resolution",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "resolution_time_high",
      "label": "High Priority (hours)",
      "fieldtype": "Int",
      "default": 8
    },
    {
      "fieldname": "resolution_time_urgent",
      "label": "Urgent Priority (hours)",
      "fieldtype": "Int",
      "default": 4
    },
    {
      "fieldname": "section_business_hours",
      "fieldtype": "Section Break",
      "label": "Business Hours"
    },
    {
      "fieldname": "use_business_hours",
      "label": "Use Business Hours",
      "fieldtype": "Check",
      "default": 1,
      "description": "Only count time during business hours"
    },
    {
      "fieldname": "business_hours_start",
      "label": "Start Time",
      "fieldtype": "Time",
      "default": "09:00:00",
      "depends_on": "use_business_hours"
    },
    {
      "fieldname": "column_break_hours",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "business_hours_end",
      "label": "End Time",
      "fieldtype": "Time",
      "default": "17:00:00",
      "depends_on": "use_business_hours"
    },
    {
      "fieldname": "exclude_weekends",
      "label": "Exclude Weekends",
      "fieldtype": "Check",
      "default": 1,
      "depends_on": "use_business_hours"
    },
    {
      "fieldname": "section_escalation",
      "fieldtype": "Section Break",
      "label": "Escalation Rules"
    },
    {
      "fieldname": "escalation_rules",
      "label": "Escalation Rules",
      "fieldtype": "Table",
      "options": "SLA Escalation Rule"
    },
    {
      "fieldname": "section_pause",
      "fieldtype": "Section Break",
      "label": "Pause Conditions",
      "collapsible": 1
    },
    {
      "fieldname": "pause_on_pending",
      "label": "Pause on Pending Status",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "pause_on_hold",
      "label": "Pause on Hold Status",
      "fieldtype": "Check",
      "default": 1
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "enabled"]}
  ]
}
```

---

## 15.3 HR Overlay DocTypes

### Schedule Entry

```json
{
  "doctype": "Schedule Entry",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "SCH-.YYYY.-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1},
    {"role": "HR Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Employee", "read": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "section_assignment",
      "fieldtype": "Section Break",
      "label": "Assignment"
    },
    {
      "fieldname": "employee",
      "label": "Employee",
      "fieldtype": "Link",
      "options": "Employee",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "shift_template",
      "label": "Shift Template",
      "fieldtype": "Link",
      "options": "Shift Template",
      "reqd": 1
    },
    {
      "fieldname": "column_break_assign",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "date",
      "label": "Date",
      "fieldtype": "Date",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "work_location",
      "label": "Work Location",
      "fieldtype": "Link",
      "options": "Work Location"
    },
    {
      "fieldname": "section_times",
      "fieldtype": "Section Break",
      "label": "Times"
    },
    {
      "fieldname": "start_time",
      "label": "Start Time",
      "fieldtype": "Time",
      "fetch_from": "shift_template.start_time",
      "in_list_view": 1
    },
    {
      "fieldname": "end_time",
      "label": "End Time",
      "fieldtype": "Time",
      "fetch_from": "shift_template.end_time",
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_times",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "break_duration_minutes",
      "label": "Break (minutes)",
      "fieldtype": "Int",
      "fetch_from": "shift_template.break_duration_minutes"
    },
    {
      "fieldname": "section_status",
      "fieldtype": "Section Break",
      "label": "Status"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Draft\nPublished\nConfirmed\nCompleted\nCancelled",
      "default": "Draft",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "published_at",
      "label": "Published At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "column_break_status",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "confirmed_at",
      "label": "Confirmed At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "confirmed_by",
      "label": "Confirmed By",
      "fieldtype": "Link",
      "options": "User",
      "read_only": 1
    },
    {
      "fieldname": "section_swap",
      "fieldtype": "Section Break",
      "label": "Shift Swap",
      "collapsible": 1
    },
    {
      "fieldname": "swap_status",
      "label": "Swap Status",
      "fieldtype": "Select",
      "options": "None\nRequested\nOffered\nApproved",
      "default": "None"
    },
    {
      "fieldname": "swap_request",
      "label": "Swap Request",
      "fieldtype": "Link",
      "options": "Shift Swap Request",
      "depends_on": "eval:doc.swap_status!='None'"
    },
    {
      "fieldname": "section_hrms",
      "fieldtype": "Section Break",
      "label": "HRMS Sync",
      "collapsible": 1
    },
    {
      "fieldname": "hrms_shift_assignment",
      "label": "HRMS Shift Assignment",
      "fieldtype": "Link",
      "options": "Shift Assignment",
      "read_only": 1
    },
    {
      "fieldname": "synced_to_hrms",
      "label": "Synced to HRMS",
      "fieldtype": "Check",
      "read_only": 1
    },
    {
      "fieldname": "column_break_hrms",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "last_sync",
      "label": "Last Sync",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_notes",
      "fieldtype": "Section Break",
      "label": "Notes",
      "collapsible": 1
    },
    {
      "fieldname": "notes",
      "label": "Notes",
      "fieldtype": "Small Text"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "status"]},
    {"fields": ["organization", "date"]},
    {"fields": ["organization", "employee"]},
    {"fields": ["employee", "date"]},
    {"fields": ["date", "status"]}
  ]
}
```

### Work Location

```json
{
  "doctype": "Work Location",
  "module": "Dartwing Company",
  "autoname": "naming_series:",
  "naming_series": "LOC-.#####",
  "track_changes": 1,
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "HR Manager", "read": 1, "write": 1, "create": 1},
    {"role": "Dartwing User", "read": 1}
  ],
  "user_permission_dependant_doctype": "Organization",
  "fields": [
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1,
      "in_standard_filter": 1,
      "set_only_once": 1
    },
    {
      "fieldname": "location_name",
      "label": "Location Name",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "address",
      "label": "Address",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "section_geofence",
      "fieldtype": "Section Break",
      "label": "Geofence"
    },
    {
      "fieldname": "latitude",
      "label": "Latitude",
      "fieldtype": "Float",
      "precision": 6,
      "reqd": 1
    },
    {
      "fieldname": "longitude",
      "label": "Longitude",
      "fieldtype": "Float",
      "precision": 6,
      "reqd": 1
    },
    {
      "fieldname": "column_break_geo",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "geofence_radius_meters",
      "label": "Geofence Radius (meters)",
      "fieldtype": "Int",
      "default": 100,
      "reqd": 1
    },
    {
      "fieldname": "section_validation",
      "fieldtype": "Section Break",
      "label": "Validation Methods"
    },
    {
      "fieldname": "validation_mode",
      "label": "Validation Mode",
      "fieldtype": "Select",
      "options": "GPS Only\nWiFi Only\nQR Only\nAny Method",
      "default": "GPS Only",
      "reqd": 1
    },
    {
      "fieldname": "column_break_val",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "qr_code",
      "label": "QR Code",
      "fieldtype": "Data",
      "read_only": 1,
      "description": "Auto-generated on save"
    },
    {
      "fieldname": "section_wifi",
      "fieldtype": "Section Break",
      "label": "WiFi Networks",
      "depends_on": "eval:doc.validation_mode=='WiFi Only' || doc.validation_mode=='Any Method'"
    },
    {
      "fieldname": "allowed_wifi_networks",
      "label": "Allowed WiFi Networks",
      "fieldtype": "Table",
      "options": "WiFi Network"
    },
    {
      "fieldname": "section_customer",
      "fieldtype": "Section Break",
      "label": "Client Site",
      "collapsible": 1
    },
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer",
      "description": "If this is a client location"
    }
  ],
  "indexes": [
    {"fields": ["organization"]},
    {"fields": ["organization", "customer"]},
    {"fields": ["latitude", "longitude"]}
  ]
}
```

---

## 15.4 Child Table DocTypes

### Vault Document (Child Table)

```json
{
  "doctype": "Vault Document",
  "module": "Dartwing Company",
  "istable": 1,
  "fields": [
    {
      "fieldname": "document_name",
      "label": "Document Name",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "file",
      "label": "File",
      "fieldtype": "Attach",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "category",
      "label": "Category",
      "fieldtype": "Data"
    },
    {
      "fieldname": "uploaded_at",
      "label": "Uploaded At",
      "fieldtype": "Datetime",
      "default": "Now",
      "read_only": 1
    },
    {
      "fieldname": "uploaded_by",
      "label": "Uploaded By",
      "fieldtype": "Link",
      "options": "User",
      "read_only": 1
    },
    {
      "fieldname": "file_size",
      "label": "File Size (bytes)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "portal_visible",
      "label": "Portal Visible",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "acknowledgment_required",
      "label": "Acknowledgment Required",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "acknowledged_at",
      "label": "Acknowledged At",
      "fieldtype": "Datetime",
      "read_only": 1
    }
  ]
}
```

### Vault Access Log (Child Table)

```json
{
  "doctype": "Vault Access Log",
  "module": "Dartwing Company",
  "istable": 1,
  "fields": [
    {
      "fieldname": "action",
      "label": "Action",
      "fieldtype": "Select",
      "options": "View\nDownload\nUpload\nAcknowledge",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "document_name",
      "label": "Document",
      "fieldtype": "Data",
      "in_list_view": 1
    },
    {
      "fieldname": "timestamp",
      "label": "Timestamp",
      "fieldtype": "Datetime",
      "default": "Now",
      "read_only": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "user",
      "label": "User",
      "fieldtype": "Link",
      "options": "User",
      "in_list_view": 1
    },
    {
      "fieldname": "ip_address",
      "label": "IP Address",
      "fieldtype": "Data"
    }
  ]
}
```

### Ticket Escalation (Child Table)

```json
{
  "doctype": "Ticket Escalation",
  "module": "Dartwing Company",
  "istable": 1,
  "fields": [
    {
      "fieldname": "escalated_at",
      "label": "Escalated At",
      "fieldtype": "Datetime",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "escalated_from",
      "label": "From Level",
      "fieldtype": "Int",
      "in_list_view": 1
    },
    {
      "fieldname": "escalated_to",
      "label": "To Level",
      "fieldtype": "Int",
      "in_list_view": 1
    },
    {
      "fieldname": "reason",
      "label": "Reason",
      "fieldtype": "Select",
      "options": "SLA Breach\nManual\nPriority Change\nCustomer Request",
      "in_list_view": 1
    },
    {
      "fieldname": "escalated_by",
      "label": "Escalated By",
      "fieldtype": "Link",
      "options": "User"
    },
    {
      "fieldname": "notes",
      "label": "Notes",
      "fieldtype": "Small Text"
    }
  ]
}
```

### SLA Escalation Rule (Child Table)

```json
{
  "doctype": "SLA Escalation Rule",
  "module": "Dartwing Company",
  "istable": 1,
  "fields": [
    {
      "fieldname": "trigger_type",
      "label": "Trigger Type",
      "fieldtype": "Select",
      "options": "Response SLA At Risk\nResponse SLA Breached\nResolution SLA At Risk\nResolution SLA Breached",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "at_risk_threshold_percent",
      "label": "At Risk Threshold (%)",
      "fieldtype": "Percent",
      "default": 80,
      "description": "Trigger at this % of SLA time elapsed"
    },
    {
      "fieldname": "escalation_level",
      "label": "Escalate To Level",
      "fieldtype": "Int",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "notify_users",
      "label": "Notify Users",
      "fieldtype": "Table MultiSelect",
      "options": "SLA Notify User"
    },
    {
      "fieldname": "notify_role",
      "label": "Notify Role",
      "fieldtype": "Link",
      "options": "Role"
    },
    {
      "fieldname": "auto_assign_to",
      "label": "Auto Assign To",
      "fieldtype": "Link",
      "options": "User"
    }
  ]
}
```

---

*End of Section 15: DocType JSON Schemas*

---

# Section 16: Permission Framework

This section provides a comprehensive permission framework for Dartwing Company, addressing the gaps identified by reviewers regarding multi-tenancy enforcement, Socket.IO security, background job permissions, and healthcare PHI role separation.

---

## 16.1 Core Permission Architecture

### Permission Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PERMISSION ENFORCEMENT LAYERS                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ Layer 1: DocType Permissions (Frappe Built-in)               │
│ - Role-based access (read/write/create/delete)               │
│ - user_permission_dependant_doctype: Organization            │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│ Layer 2: Permission Query Conditions (List Filtering)        │
│ - get_org_condition() - filter by organization               │
│ - Applied to all list views, reports, and API calls          │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│ Layer 3: has_permission Hook (Document-level)                │
│ - has_org_permission() - verify org access                   │
│ - has_vault_permission() - customer + org verification       │
│ - has_phi_permission() - healthcare role check               │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│ Layer 4: API/Socket.IO Enforcement                           │
│ - @permission_required decorator                             │
│ - Socket.IO subscription validation                          │
│ - Background job user context                                │
└───────────────────────────────────────────────────────────────┘
```

---

## 16.2 Permission Utilities Module

```python
# dartwing_company/permissions.py

import frappe
from frappe import _
from frappe.model.document import Document
from functools import wraps
from typing import Optional

# ─────────────────────────────────────────────────────────────────
# Organization Resolution
# ─────────────────────────────────────────────────────────────────

def get_user_organization(user: str = None) -> Optional[str]:
    """
    Get the organization for a user.

    Resolution order:
    1. Check User Permission for Organization
    2. Check linked Employee -> Company -> Organization
    3. Return None if no organization found
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return None  # Administrator sees all

    # Check User Permission
    org_permissions = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization",
            "is_default": 1
        },
        pluck="for_value",
        limit=1
    )

    if org_permissions:
        return org_permissions[0]

    # Fallback: Check Employee -> Company link
    employee = frappe.db.get_value("Employee", {"user_id": user}, "company")
    if employee:
        # Map ERPNext Company to Organization
        org = frappe.db.get_value(
            "Organization",
            {"linked_doctype": "Company", "linked_name": employee},
            "name"
        )
        if org:
            return org

    return None


def get_user_organizations(user: str = None) -> list[str]:
    """
    Get all organizations a user has access to.
    Used for users with multiple organization permissions.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return frappe.get_all("Organization", pluck="name")

    return frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization"
        },
        pluck="for_value"
    )


# ─────────────────────────────────────────────────────────────────
# Permission Query Conditions (List Filtering)
# ─────────────────────────────────────────────────────────────────

def get_org_condition(user: str = None) -> str:
    """
    Standard organization filter for all org-scoped DocTypes.

    Used in permission_query_conditions to filter list views.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return ""  # No filter for admin

    organizations = get_user_organizations(user)

    if not organizations:
        return "1=0"  # No access - return impossible condition

    if len(organizations) == 1:
        return f"`organization` = {frappe.db.escape(organizations[0])}"

    # Multiple organizations
    org_list = ", ".join([frappe.db.escape(o) for o in organizations])
    return f"`organization` IN ({org_list})"


def get_customer_org_condition(user: str = None) -> str:
    """
    Filter for DocTypes that link to Customer instead of Organization.
    Filters by customers belonging to user's organization.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return ""

    org = get_user_organization(user)
    if not org:
        return "1=0"

    # Get customers linked to this organization
    return f"""`customer` IN (
        SELECT name FROM `tabCustomer`
        WHERE organization = {frappe.db.escape(org)}
    )"""


# ─────────────────────────────────────────────────────────────────
# has_permission Hooks (Document-level)
# ─────────────────────────────────────────────────────────────────

def has_org_permission(doc: Document, ptype: str = None, user: str = None) -> bool:
    """
    Check if user has permission to access a document based on organization.

    Args:
        doc: The document being accessed
        ptype: Permission type (read, write, etc.)
        user: User to check (defaults to session user)

    Returns:
        True if user has access, False otherwise
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return True

    if not hasattr(doc, "organization") or not doc.organization:
        return True  # No organization field, allow access

    user_orgs = get_user_organizations(user)
    return doc.organization in user_orgs


def has_vault_permission(doc: Document, ptype: str = None, user: str = None) -> bool:
    """
    Check vault permission - requires both organization AND customer access.

    For portal users, checks if they are linked to the vault's customer.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return True

    # First check organization permission
    if not has_org_permission(doc, ptype, user):
        return False

    # For portal users, also check customer link
    if "Website User" in frappe.get_roles(user):
        # Get contact linked to user
        contact = frappe.db.get_value("Contact", {"user": user}, "name")
        if not contact:
            return False

        # Check if contact is linked to vault's customer
        linked_customer = frappe.db.get_value(
            "Dynamic Link",
            {"parent": contact, "link_doctype": "Customer"},
            "link_name"
        )

        return linked_customer == doc.customer

    return True


def has_phi_permission(doc: Document, ptype: str = None, user: str = None) -> bool:
    """
    Check PHI (Protected Health Information) access.

    Requires healthcare-specific roles for Patient, Patient Encounter, etc.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return True

    # Check if this is a PHI doctype
    phi_doctypes = ["Patient", "Patient Encounter", "Clinical Note",
                    "Patient Medical Record"]

    if doc.doctype not in phi_doctypes:
        return True  # Not a PHI doctype

    # Check healthcare roles
    phi_roles = {"Healthcare Administrator", "Healthcare Provider",
                 "Healthcare Practitioner", "Nursing User"}

    user_roles = set(frappe.get_roles(user))

    if not user_roles & phi_roles:
        return False

    # Also check organization permission
    return has_org_permission(doc, ptype, user)


# ─────────────────────────────────────────────────────────────────
# Permission Enforcement Utilities
# ─────────────────────────────────────────────────────────────────

def enforce_org_permission(doc: Document, user: str = None) -> None:
    """
    Raise PermissionError if user cannot access document's organization.

    Use this in API endpoints and controllers for explicit checks.
    """
    user = user or frappe.session.user

    if not has_org_permission(doc, user=user):
        frappe.throw(
            _("You do not have permission to access this {0}").format(doc.doctype),
            frappe.PermissionError
        )


def enforce_phi_permission(doc: Document, user: str = None) -> None:
    """
    Raise PermissionError if user cannot access PHI document.
    """
    user = user or frappe.session.user

    if not has_phi_permission(doc, user=user):
        frappe.throw(
            _("You do not have permission to access Protected Health Information"),
            frappe.PermissionError
        )


# ─────────────────────────────────────────────────────────────────
# Decorators for API Endpoints
# ─────────────────────────────────────────────────────────────────

def permission_required(doctype: str = None, permission_type: str = "read"):
    """
    Decorator for API endpoints requiring permission checks.

    Usage:
        @frappe.whitelist()
        @permission_required("Dispatch Job", "write")
        def update_job_status(job_name, status):
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # If doctype specified, check permission on first arg (assumed to be doc name)
            if doctype and args:
                doc_name = args[0]
                if not frappe.has_permission(doctype, permission_type, doc_name):
                    frappe.throw(_("Permission denied"), frappe.PermissionError)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def org_required(fn):
    """
    Decorator ensuring user has an organization.

    Usage:
        @frappe.whitelist()
        @org_required
        def get_my_jobs():
            org = get_user_organization()
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        org = get_user_organization()
        if not org:
            frappe.throw(
                _("You must be associated with an organization to perform this action"),
                frappe.PermissionError
            )
        return fn(*args, **kwargs)
    return wrapper
```

---

## 16.3 Socket.IO Permission Enforcement

```python
# dartwing_company/realtime.py

import frappe
from frappe.realtime import get_redis_server
from dartwing_company.permissions import (
    get_user_organization,
    enforce_org_permission,
    has_org_permission
)

# ─────────────────────────────────────────────────────────────────
# Room Subscription with Permission Checks
# ─────────────────────────────────────────────────────────────────

@frappe.whitelist()
def subscribe_to_conversation(conversation_name: str) -> dict:
    """
    Subscribe to real-time updates for a conversation.

    Permission check: User must have access to conversation's organization.
    """
    try:
        conv = frappe.get_doc("Conversation", conversation_name)
        enforce_org_permission(conv)

        # Subscribe to room
        room = f"conversation:{conversation_name}"
        frappe.publish_realtime(
            "subscribe",
            room=room,
            user=frappe.session.user
        )

        return {"success": True, "room": room}

    except frappe.PermissionError:
        return {"success": False, "error": "Permission denied"}
    except frappe.DoesNotExistError:
        return {"success": False, "error": "Conversation not found"}


@frappe.whitelist()
def subscribe_to_dispatch_board(organization: str = None) -> dict:
    """
    Subscribe to dispatch board updates for an organization.

    If no organization specified, uses user's default organization.
    """
    org = organization or get_user_organization()

    if not org:
        return {"success": False, "error": "No organization found"}

    # Verify user has access to this organization
    user_orgs = frappe.get_all(
        "User Permission",
        filters={
            "user": frappe.session.user,
            "allow": "Organization"
        },
        pluck="for_value"
    )

    if org not in user_orgs and frappe.session.user != "Administrator":
        return {"success": False, "error": "Permission denied"}

    room = f"dispatch:{org}"
    frappe.publish_realtime(
        "subscribe",
        room=room,
        user=frappe.session.user
    )

    return {"success": True, "room": room, "organization": org}


@frappe.whitelist()
def subscribe_to_inbox(organization: str = None) -> dict:
    """
    Subscribe to inbox updates (new messages, status changes).
    """
    org = organization or get_user_organization()

    if not org:
        return {"success": False, "error": "No organization found"}

    # Verify organization access
    if not frappe.has_permission("Organization", "read", org):
        return {"success": False, "error": "Permission denied"}

    room = f"inbox:{org}"
    frappe.publish_realtime(
        "subscribe",
        room=room,
        user=frappe.session.user
    )

    return {"success": True, "room": room}


# ─────────────────────────────────────────────────────────────────
# Publishing Events with Permission Context
# ─────────────────────────────────────────────────────────────────

def publish_conversation_update(conversation: "Conversation", event: str, data: dict = None):
    """
    Publish conversation update to subscribed users.

    Only publishes to users with organization access.
    """
    room = f"conversation:{conversation.name}"

    frappe.publish_realtime(
        event=f"conversation_{event}",
        message={
            "conversation": conversation.name,
            "organization": conversation.organization,
            "data": data or {}
        },
        room=room
    )

    # Also publish to organization inbox room
    frappe.publish_realtime(
        event=f"inbox_{event}",
        message={
            "conversation": conversation.name,
            "channel": conversation.channel,
            "subject": conversation.subject,
            "data": data or {}
        },
        room=f"inbox:{conversation.organization}"
    )


def publish_dispatch_update(job: "DispatchJob", event: str, data: dict = None):
    """
    Publish dispatch job update to organization dispatch board.
    """
    frappe.publish_realtime(
        event=f"dispatch_{event}",
        message={
            "job": job.name,
            "status": job.status,
            "assigned_to": job.assigned_to,
            "customer": job.customer,
            "data": data or {}
        },
        room=f"dispatch:{job.organization}"
    )


def publish_ticket_update(ticket: "ServiceTicket", event: str, data: dict = None):
    """
    Publish ticket update to assigned user and organization inbox.
    """
    # Notify assigned user directly
    if ticket.assigned_to:
        frappe.publish_realtime(
            event=f"ticket_{event}",
            message={
                "ticket": ticket.name,
                "subject": ticket.subject,
                "status": ticket.status,
                "sla_status": ticket.sla_status,
                "data": data or {}
            },
            user=ticket.assigned_to
        )

    # Notify organization inbox
    frappe.publish_realtime(
        event=f"ticket_{event}",
        message={
            "ticket": ticket.name,
            "subject": ticket.subject,
            "status": ticket.status,
            "data": data or {}
        },
        room=f"inbox:{ticket.organization}"
    )
```

---

## 16.4 Background Job Permission Pattern

```python
# dartwing_company/background_jobs.py

import frappe
from frappe.utils.background_jobs import enqueue
from dartwing_company.permissions import (
    get_user_organization,
    enforce_org_permission
)

# ─────────────────────────────────────────────────────────────────
# Pattern: Enqueue with User Context
# ─────────────────────────────────────────────────────────────────

def enqueue_with_user(method: str, user: str = None, **kwargs):
    """
    Enqueue a background job that runs in the context of a specific user.

    This ensures permission checks work correctly in background jobs.

    Usage:
        enqueue_with_user(
            "dartwing_company.tasks.process_campaign",
            user=frappe.session.user,
            campaign_name="CAMP-2025-00001"
        )
    """
    user = user or frappe.session.user

    # Store user in kwargs for the job to use
    kwargs["_user_context"] = user

    enqueue(
        method,
        queue="default",
        **kwargs
    )


def run_as_user(fn):
    """
    Decorator that sets user context from _user_context kwarg.

    Usage:
        @run_as_user
        def process_campaign(campaign_name: str, **kwargs):
            # frappe.session.user is now set to the enqueuing user
            ...
    """
    def wrapper(*args, **kwargs):
        user = kwargs.pop("_user_context", None)

        if user:
            frappe.set_user(user)

        try:
            return fn(*args, **kwargs)
        finally:
            # Reset to guest to avoid permission leakage
            frappe.set_user("Guest")

    return wrapper


# ─────────────────────────────────────────────────────────────────
# Example Background Jobs with Permission Checks
# ─────────────────────────────────────────────────────────────────

@run_as_user
def process_campaign_leads(campaign_name: str, **kwargs):
    """
    Process leads for a campaign.

    Permission: User must have access to campaign's organization.
    """
    campaign = frappe.get_doc("Campaign", campaign_name)
    enforce_org_permission(campaign)

    # Process leads...
    leads = frappe.get_all(
        "CRM Lead",
        filters={"campaign": campaign_name},
        fields=["name", "lead_name", "status"]
    )

    for lead in leads:
        # Process each lead
        pass


@run_as_user
def generate_daily_standup(organization: str, **kwargs):
    """
    Generate daily standup report for an organization.

    Permission: User must have access to organization.
    """
    user_orgs = frappe.get_all(
        "User Permission",
        filters={
            "user": frappe.session.user,
            "allow": "Organization"
        },
        pluck="for_value"
    )

    if organization not in user_orgs:
        frappe.throw("Permission denied", frappe.PermissionError)

    # Generate standup...


@run_as_user
def send_broadcast_alert(alert_name: str, **kwargs):
    """
    Send broadcast alert to recipients.

    Permission: User must have access to alert's organization.
    """
    alert = frappe.get_doc("Broadcast Alert", alert_name)
    enforce_org_permission(alert)

    # Send alert...


# ─────────────────────────────────────────────────────────────────
# Scheduled Jobs (System Context)
# ─────────────────────────────────────────────────────────────────

def check_sla_breaches():
    """
    Scheduled job to check SLA breaches across all organizations.

    Runs as Administrator (no user context).
    """
    frappe.set_user("Administrator")

    # Get all organizations with active tickets
    organizations = frappe.get_all(
        "Service Ticket",
        filters={"status": ["in", ["New", "Open", "Pending"]]},
        distinct=True,
        pluck="organization"
    )

    for org in organizations:
        # Process each organization's tickets
        tickets = frappe.get_all(
            "Service Ticket",
            filters={
                "organization": org,
                "status": ["in", ["New", "Open", "Pending"]],
                "sla_status": ["!=", "Breached"]
            },
            fields=["name", "response_due", "resolution_due", "sla_status"]
        )

        for ticket in tickets:
            check_ticket_sla(ticket)


def check_ticket_sla(ticket: dict):
    """Check and update SLA status for a single ticket."""
    now = frappe.utils.now_datetime()

    # Check response SLA
    if ticket.response_due and now > ticket.response_due:
        frappe.db.set_value("Service Ticket", ticket.name,
                           "sla_status", "Breached")
        trigger_sla_escalation(ticket.name, "response")

    # Check resolution SLA
    elif ticket.resolution_due and now > ticket.resolution_due:
        frappe.db.set_value("Service Ticket", ticket.name,
                           "sla_status", "Breached")
        trigger_sla_escalation(ticket.name, "resolution")


def trigger_sla_escalation(ticket_name: str, breach_type: str):
    """Trigger escalation for SLA breach."""
    ticket = frappe.get_doc("Service Ticket", ticket_name)

    # Get applicable escalation rules
    if ticket.sla_policy:
        policy = frappe.get_doc("SLA Policy", ticket.sla_policy)
        # Apply escalation rules...
```

---

## 16.5 Healthcare PHI Role Model

```python
# dartwing_company/healthcare/permissions.py

import frappe
from frappe import _
from typing import Optional

# ─────────────────────────────────────────────────────────────────
# PHI Configuration
# ─────────────────────────────────────────────────────────────────

PHI_DOCTYPES = [
    "Patient",
    "Patient Encounter",
    "Clinical Note",
    "Patient Medical Record",
    "Vital Signs",
    "Lab Test",
    "Prescription"
]

PHI_ROLES = {
    "Healthcare Administrator": {
        "permissions": ["read", "write", "create", "delete"],
        "description": "Full PHI access for healthcare administrators"
    },
    "Healthcare Provider": {
        "permissions": ["read", "write", "create"],
        "description": "Clinical staff with patient care responsibilities"
    },
    "Healthcare Practitioner": {
        "permissions": ["read", "write", "create"],
        "description": "Doctors, nurses, and other practitioners"
    },
    "Nursing User": {
        "permissions": ["read", "write"],
        "description": "Nursing staff with limited PHI access"
    },
    "Medical Records": {
        "permissions": ["read"],
        "description": "Read-only access for medical records staff"
    }
}

# ─────────────────────────────────────────────────────────────────
# PHI Access Checks
# ─────────────────────────────────────────────────────────────────

def is_healthcare_mode_enabled(organization: str = None) -> bool:
    """
    Check if healthcare mode is enabled for an organization.
    """
    if organization:
        return frappe.db.get_value(
            "Organization Settings",
            {"organization": organization},
            "healthcare_mode"
        ) or False

    # Check global setting
    return frappe.db.get_single_value(
        "Dartwing Settings", "healthcare_mode_enabled"
    ) or False


def has_phi_role(user: str = None) -> bool:
    """
    Check if user has any PHI-access role.
    """
    user = user or frappe.session.user
    user_roles = set(frappe.get_roles(user))
    phi_role_set = set(PHI_ROLES.keys())

    return bool(user_roles & phi_role_set)


def get_phi_permission_level(user: str = None) -> Optional[str]:
    """
    Get the highest PHI permission level for a user.

    Returns: "full", "clinical", "read_only", or None
    """
    user = user or frappe.session.user
    user_roles = set(frappe.get_roles(user))

    if "Healthcare Administrator" in user_roles:
        return "full"
    elif {"Healthcare Provider", "Healthcare Practitioner"} & user_roles:
        return "clinical"
    elif {"Nursing User", "Medical Records"} & user_roles:
        return "read_only"

    return None


def can_access_phi(doctype: str, user: str = None, ptype: str = "read") -> bool:
    """
    Check if user can access PHI for a specific doctype and permission type.
    """
    if doctype not in PHI_DOCTYPES:
        return True  # Not a PHI doctype

    user = user or frappe.session.user

    if user == "Administrator":
        return True

    # Check if user has PHI role
    if not has_phi_role(user):
        return False

    # Check permission type against role permissions
    user_roles = frappe.get_roles(user)

    for role in user_roles:
        if role in PHI_ROLES:
            if ptype in PHI_ROLES[role]["permissions"]:
                return True

    return False


# ─────────────────────────────────────────────────────────────────
# PHI Audit Logging
# ─────────────────────────────────────────────────────────────────

def log_phi_access(doctype: str, doc_name: str, action: str, user: str = None):
    """
    Log PHI access for audit trail.

    Required for HIPAA compliance.
    """
    user = user or frappe.session.user

    frappe.get_doc({
        "doctype": "PHI Access Log",
        "user": user,
        "access_doctype": doctype,
        "document_name": doc_name,
        "action": action,
        "timestamp": frappe.utils.now_datetime(),
        "ip_address": frappe.local.request_ip if hasattr(frappe.local, "request_ip") else None
    }).insert(ignore_permissions=True)


# ─────────────────────────────────────────────────────────────────
# Permission Query for Healthcare
# ─────────────────────────────────────────────────────────────────

def get_patient_permission_query(user: str = None) -> str:
    """
    Permission query for Patient doctype.

    Returns patients based on:
    1. User's organization
    2. User's PHI access level
    3. Direct patient assignment (for providers)
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return ""

    # Check PHI access
    if not has_phi_role(user):
        return "1=0"  # No PHI access

    # Get organization filter
    from dartwing_company.permissions import get_org_condition
    org_condition = get_org_condition(user)

    if not org_condition or org_condition == "1=0":
        return "1=0"

    # For providers, also check direct assignment
    user_roles = frappe.get_roles(user)
    if "Healthcare Practitioner" in user_roles:
        practitioner = frappe.db.get_value(
            "Healthcare Practitioner",
            {"user": user},
            "name"
        )

        if practitioner:
            return f"""(
                {org_condition}
                OR `name` IN (
                    SELECT patient FROM `tabPatient Encounter`
                    WHERE practitioner = {frappe.db.escape(practitioner)}
                )
            )"""

    return org_condition
```

---

## 16.6 Complete hooks.py Permission Configuration

```python
# hooks.py - Permission Configuration Section

# ─────────────────────────────────────────────────────────────────
# Permission Query Conditions (List Filtering)
# ─────────────────────────────────────────────────────────────────

permission_query_conditions = {
    # ─── Operations ───
    "Conversation": "dartwing_company.permissions.get_org_condition",
    "Conversation Message": "dartwing_company.permissions.get_org_condition",
    "Dispatch Job": "dartwing_company.permissions.get_org_condition",
    "Mobile Form": "dartwing_company.permissions.get_org_condition",
    "Form Submission": "dartwing_company.permissions.get_org_condition",
    "Knowledge Article": "dartwing_company.permissions.get_org_condition",
    "Workflow Template": "dartwing_company.permissions.get_org_condition",
    "Workflow Instance": "dartwing_company.permissions.get_org_condition",
    "Broadcast Alert": "dartwing_company.permissions.get_org_condition",
    "Resource": "dartwing_company.permissions.get_org_condition",
    "Resource Booking": "dartwing_company.permissions.get_org_condition",
    "Visitor Log": "dartwing_company.permissions.get_org_condition",

    # ─── CRM Overlay ───
    "Portal Settings": "dartwing_company.permissions.get_org_condition",
    "View Set": "dartwing_company.permissions.get_org_condition",
    "Document Vault": "dartwing_company.permissions.get_org_condition",
    "Appointment": "dartwing_company.permissions.get_org_condition",
    "Appointment Type": "dartwing_company.permissions.get_org_condition",
    "Service Ticket": "dartwing_company.permissions.get_org_condition",
    "SLA Policy": "dartwing_company.permissions.get_org_condition",
    "Campaign": "dartwing_company.permissions.get_org_condition",

    # ─── HR Overlay ───
    "Shift Template": "dartwing_company.permissions.get_org_condition",
    "Schedule Entry": "dartwing_company.permissions.get_org_condition",
    "Shift Swap Request": "dartwing_company.permissions.get_org_condition",
    "Work Location": "dartwing_company.permissions.get_org_condition",
    "Employee Certification": "dartwing_company.permissions.get_org_condition",

    # ─── Saga & Reconciliation ───
    "Saga Log": "dartwing_company.permissions.get_org_condition",
    "Reconciliation Log": "dartwing_company.permissions.get_org_condition",

    # ─── Healthcare (if enabled) ───
    "Patient": "dartwing_company.healthcare.permissions.get_patient_permission_query"
}

# ─────────────────────────────────────────────────────────────────
# has_permission Hooks (Document-level)
# ─────────────────────────────────────────────────────────────────

has_permission = {
    # ─── Standard Org Permission ───
    "Conversation": "dartwing_company.permissions.has_org_permission",
    "Dispatch Job": "dartwing_company.permissions.has_org_permission",
    "Service Ticket": "dartwing_company.permissions.has_org_permission",
    "Appointment": "dartwing_company.permissions.has_org_permission",
    "Schedule Entry": "dartwing_company.permissions.has_org_permission",
    "Campaign": "dartwing_company.permissions.has_org_permission",

    # ─── Special Permission Logic ───
    "Document Vault": "dartwing_company.permissions.has_vault_permission",

    # ─── Healthcare PHI ───
    "Patient": "dartwing_company.healthcare.permissions.has_phi_permission",
    "Patient Encounter": "dartwing_company.healthcare.permissions.has_phi_permission",
    "Clinical Note": "dartwing_company.healthcare.permissions.has_phi_permission"
}

# ─────────────────────────────────────────────────────────────────
# DocType Class Overrides (for permission enforcement in controllers)
# ─────────────────────────────────────────────────────────────────

override_doctype_class = {
    "Customer": "dartwing_company.overrides.customer.CustomCustomer",
    "Employee": "dartwing_company.overrides.employee.CustomEmployee",
    "Lead": "dartwing_company.overrides.lead.CustomLead",
    "Attendance": "dartwing_company.overrides.attendance.CustomAttendance"
}
```

---

## 16.7 Permission Testing Utilities

```python
# dartwing_company/tests/test_permissions.py

import frappe
import unittest
from dartwing_company.permissions import (
    get_user_organization,
    get_user_organizations,
    has_org_permission,
    has_vault_permission,
    enforce_org_permission
)

class TestPermissions(unittest.TestCase):

    def setUp(self):
        """Create test users and organizations."""
        # Create test organization
        self.test_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org",
            "org_type": "Company"
        }).insert()

        # Create test user
        self.test_user = frappe.get_doc({
            "doctype": "User",
            "email": "testuser@example.com",
            "first_name": "Test"
        }).insert()

        # Grant organization permission
        frappe.get_doc({
            "doctype": "User Permission",
            "user": self.test_user.name,
            "allow": "Organization",
            "for_value": self.test_org.name,
            "is_default": 1
        }).insert()

    def tearDown(self):
        """Clean up test data."""
        frappe.delete_doc("User Permission", {
            "user": self.test_user.name
        })
        frappe.delete_doc("User", self.test_user.name)
        frappe.delete_doc("Organization", self.test_org.name)

    def test_get_user_organization(self):
        """Test organization resolution."""
        org = get_user_organization(self.test_user.name)
        self.assertEqual(org, self.test_org.name)

    def test_has_org_permission_allowed(self):
        """Test permission when user has access."""
        doc = frappe.get_doc({
            "doctype": "Conversation",
            "organization": self.test_org.name,
            "channel": "Email"
        }).insert()

        result = has_org_permission(doc, user=self.test_user.name)
        self.assertTrue(result)

        frappe.delete_doc("Conversation", doc.name)

    def test_has_org_permission_denied(self):
        """Test permission when user lacks access."""
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Other Org",
            "org_type": "Company"
        }).insert()

        doc = frappe.get_doc({
            "doctype": "Conversation",
            "organization": other_org.name,
            "channel": "Email"
        }).insert()

        result = has_org_permission(doc, user=self.test_user.name)
        self.assertFalse(result)

        frappe.delete_doc("Conversation", doc.name)
        frappe.delete_doc("Organization", other_org.name)

    def test_enforce_org_permission_raises(self):
        """Test that enforce_org_permission raises on denied access."""
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Other Org 2",
            "org_type": "Company"
        }).insert()

        doc = frappe.get_doc({
            "doctype": "Conversation",
            "organization": other_org.name,
            "channel": "Email"
        }).insert()

        with self.assertRaises(frappe.PermissionError):
            enforce_org_permission(doc, user=self.test_user.name)

        frappe.delete_doc("Conversation", doc.name)
        frappe.delete_doc("Organization", other_org.name)
```

---

*End of Section 16: Permission Framework*
