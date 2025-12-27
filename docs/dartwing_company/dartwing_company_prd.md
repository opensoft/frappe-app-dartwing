# Dartwing Company Module - Product Requirements Document

**Version:** 1.0  
**Date:** November 28, 2025  
**Status:** Draft

---

## Section 1: Executive Summary

### 1.1 Product Vision

Dartwing Company is an **AI-First Operations Platform** that transforms how businesses operate. Built as an intelligent overlay on Frappe Framework, ERPNext, and Frappe CRM, it provides:

- **Unified Operations Hub** - Single platform for all business activities
- **AI-Powered Automation** - Intelligent routing, scheduling, and decision support
- **Growth Engine** - Integrated lead generation and CRM orchestration
- **Mobile-First Workforce** - Field operations with offline capability

### 1.2 Architecture Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                    DARTWING COMPANY                              │
│              (AI-First Operations Layer)                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  OPS: Operations Core    │  CRM: Growth Strategy          │  │
│  │  • Receptionist          │  • Client Portal               │  │
│  │  • Universal Inbox       │  • Growth Orchestrator         │  │
│  │  • Workflow Builder      │  • Meeting Booker              │  │
│  │  • Smart Dispatch        │  • Service Tickets             │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  HR: Workforce Overlay   │  INTEGRATIONS                  │  │
│  │  • Shift Scheduler       │  • dartwing_leadgen            │  │
│  │  • Geo Clock-In          │  • dartwingFone (Voice/SMS)    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
        │  Frappe   │   │  ERPNext  │   │  Frappe   │
        │  Framework│   │           │   │    CRM    │
        └───────────┘   └───────────┘   └───────────┘
```

**Key Principle:** Overlay, don't extend. We ADD functions on top of Frappe CRM and ERPNext rather than modifying their core.

### 1.3 Target Markets

| Market                    | Use Cases                            | Key Features                             |
| ------------------------- | ------------------------------------ | ---------------------------------------- |
| **Service Businesses**    | HVAC, Plumbing, Electrical, Cleaning | Dispatch, Mobile Forms, Scheduling       |
| **Professional Services** | Consulting, Legal, Accounting        | Client Portal, Time Tracking, Billing    |
| **Healthcare Practices**  | Clinics, Therapy, Home Health        | Appointments, HIPAA Compliance, Forms    |
| **Property Management**   | HOAs, Rentals, Commercial            | Maintenance, Vendor Management, Portals  |
| **Agencies**              | Marketing, Staffing, Creative        | Project Management, Client Collaboration |

### 1.4 Success Metrics

| Metric               | Target        | Timeframe |
| -------------------- | ------------- | --------- |
| Active Companies     | 500           | Year 1    |
| Monthly Active Users | 5,000         | Year 1    |
| Tasks Automated      | 1M+           | Year 1    |
| Client Portal Logins | 50,000/month  | Year 1    |
| AI Interactions      | 100,000/month | Year 1    |
| NPS Score            | >50           | Quarterly |

### 1.5 Module Dependencies

```
dartwing_company
    │
    ├── dartwing_core (required)
    │   └── Organization, Person, Settings
    │
    ├── dartwing_user (required)
    │   └── User profiles, Preferences
    │
    ├── dartwing_leadgen (required)
    │   └── Search, Enrichment, Matching
    │
    ├── dartwing_fone (optional)
    │   └── Voice, SMS, Call routing
    │
    ├── frappe (required)
    │   └── Framework foundation
    │
    ├── erpnext (optional)
    │   └── Accounting, Inventory, HR
    │
    └── crm (optional)
        └── Frappe CRM - Leads, Deals
```

---

**Next: Section 2 - User Personas**

# Dartwing Company PRD - Section 2: User Personas

---

## 2.1 Primary Personas

### Persona 1: Operations Manager (Sarah)

**Profile:**

- Age: 35-45
- Role: Operations Manager at 50-person service company
- Tech Savvy: Medium
- Pain Points: Drowning in coordination, can't see what's happening in the field

**Daily Challenges:**

- Manually dispatching 20+ field technicians
- Juggling phone calls, emails, texts from multiple sources
- No visibility into job status until techs return
- Creating schedules in Excel, manually updating calendars
- Answering "Where's my technician?" calls from clients

**Success Looks Like:**

- Single dashboard showing all jobs and technician locations
- Automated dispatch based on proximity and skills
- Real-time job status updates from the field
- Clients can self-serve status checks
- Morning standup takes 5 minutes, not 30

**Key Features:** OPS-01, OPS-02, OPS-04, OPS-06, OPS-09

---

### Persona 2: Business Owner (Michael)

**Profile:**

- Age: 40-55
- Role: Owner of growing professional services firm
- Tech Savvy: Low-Medium
- Pain Points: No time for systems, needs things to just work

**Daily Challenges:**

- Losing leads because follow-up falls through cracks
- Can't find the proposal he sent last month
- Doesn't know which clients are most profitable
- Sales team has their own spreadsheets
- Marketing spend feels like guessing

**Success Looks Like:**

- AI tells him which leads to focus on today
- Every client interaction logged automatically
- Dashboard shows pipeline and revenue forecast
- Lead generation runs on autopilot
- Can answer any question with a search

**Key Features:** CRM-07, OPS-12, OPS-09, CRM-01, CRM-04

---

### Persona 3: Field Technician (Carlos)

**Profile:**

- Age: 25-40
- Role: Field Service Technician
- Tech Savvy: Mobile-native, desktop-averse
- Pain Points: Paper forms, unclear schedules, no support in field

**Daily Challenges:**

- Gets schedule changes via text/call while driving
- Paper forms get lost or are illegible
- Can't access equipment history at job site
- Has to call office for every question
- Forgets to clock in/out

**Success Looks Like:**

- Mobile app shows his route for the day
- Digital forms auto-save, work offline
- Can search knowledge base for troubleshooting
- GPS clock-in happens automatically
- Customers sign on his phone

**Key Features:** OPS-05, HR-02, OPS-07, OPS-04

---

### Persona 4: Client/Customer (Jennifer)

**Profile:**

- Age: 30-60
- Role: Customer of a service company
- Tech Savvy: Varies widely
- Pain Points: Can't get status, has to call for everything

**Daily Challenges:**

- "When will my technician arrive?"
- Can't find invoices or receipts
- Has to explain problem multiple times
- No way to share photos/documents securely
- Scheduling requires phone tag

**Success Looks Like:**

- Portal shows appointment time and tech en route
- All invoices and documents in one place
- Can submit service requests anytime
- Self-service appointment booking
- Gets proactive status updates

**Key Features:** CRM-01, CRM-02, CRM-03, CRM-04

---

### Persona 5: HR/Office Manager (Patricia)

**Profile:**

- Age: 30-50
- Role: Office Manager handling HR, admin, and everything else
- Tech Savvy: Medium
- Pain Points: Manual processes, compliance tracking, coverage gaps

**Daily Challenges:**

- Building schedules takes hours every week
- Tracking certifications and expirations manually
- Employees clock in late, dispute hours
- Shift swaps create chaos
- Visitor log is a paper notebook

**Success Looks Like:**

- Drag-and-drop schedule builder
- Auto-alerts before certifications expire
- GPS-verified clock-in, no disputes
- Self-service shift swap with approvals
- Digital visitor log with notifications

**Key Features:** HR-01, HR-02, OPS-10, OPS-11

---

## 2.2 Persona Feature Matrix

| Feature                        | Sarah (Ops) | Michael (Owner) | Carlos (Field) | Jennifer (Client) | Patricia (HR) |
| ------------------------------ | :---------: | :-------------: | :------------: | :---------------: | :-----------: |
| **OPS-01** Receptionist        |     ●●●     |       ●●○       |      ○○○       |        ●●○        |      ●●○      |
| **OPS-02** Universal Inbox     |     ●●●     |       ●●●       |      ●○○       |        ○○○        |      ●●○      |
| **OPS-03** Workflow Builder    |     ●●●     |       ●●○       |      ○○○       |        ○○○        |      ●●○      |
| **OPS-04** Smart Dispatch      |     ●●●     |       ●○○       |      ●●●       |        ●○○        |      ○○○      |
| **OPS-05** Mobile Forms        |     ●●○     |       ○○○       |      ●●●       |        ●○○        |      ●○○      |
| **OPS-06** Status Boards       |     ●●●     |       ●●●       |      ●○○       |        ○○○        |      ●●○      |
| **OPS-07** Knowledge Base      |     ●●○     |       ●○○       |      ●●●       |        ○○○        |      ●●○      |
| **OPS-08** Broadcast Alerts    |     ●●●     |       ●●○       |      ●●○       |        ●○○        |      ●●●      |
| **OPS-09** Daily Standup       |     ●●●     |       ●●●       |      ●●○       |        ○○○        |      ●●○      |
| **OPS-10** Visitor Mgmt        |     ●○○     |       ○○○       |      ○○○       |        ●●○        |      ●●●      |
| **OPS-11** Resource Booking    |     ●●○     |       ●○○       |      ●○○       |        ○○○        |      ●●●      |
| **OPS-12** Ask Anything        |     ●●●     |       ●●●       |      ●●○       |        ○○○        |      ●●○      |
| **CRM-01** Client Portal       |     ●●○     |       ●●●       |      ○○○       |        ●●●        |      ●○○      |
| **CRM-02** Document Vault      |     ●●○     |       ●●●       |      ●○○       |        ●●●        |      ●●○      |
| **CRM-03** Meeting Booker      |     ●●○     |       ●●●       |      ○○○       |        ●●●        |      ●●○      |
| **CRM-04** Service Tickets     |     ●●●     |       ●●○       |      ●●○       |        ●●●        |      ●●○      |
| **CRM-05** Custom Fields       |     ●●○     |       ●●●       |      ○○○       |        ○○○        |      ●●○      |
| **CRM-06** SLA Tracking        |     ●●●     |       ●●●       |      ○○○       |        ○○○        |      ●○○      |
| **CRM-07** Growth Orchestrator |     ●○○     |       ●●●       |      ○○○       |        ○○○        |      ○○○      |
| **HR-01** Shift Scheduler      |     ●●●     |       ●○○       |      ●●○       |        ○○○        |      ●●●      |
| **HR-02** Geo Clock-In         |     ●●○     |       ●○○       |      ●●●       |        ○○○        |      ●●●      |

**Legend:** ●●● Primary User | ●●○ Regular User | ●○○ Occasional | ○○○ Not Applicable

---

## 2.3 User Roles & Permissions

| Role                   | Description              | Feature Access                 |
| ---------------------- | ------------------------ | ------------------------------ |
| **System Admin**       | Full platform access     | All features + settings        |
| **Company Admin**      | Org-level administrator  | All features for org           |
| **Operations Manager** | Manages daily operations | OPS-\*, CRM-04, HR-01          |
| **Sales Manager**      | Manages pipeline & leads | CRM-\*, OPS-02, OPS-12         |
| **HR Manager**         | Manages workforce        | HR-\*, OPS-08, OPS-10, OPS-11  |
| **Team Lead**          | Supervises field team    | OPS-04, OPS-05, OPS-06, HR-01  |
| **Field Worker**       | Mobile field user        | OPS-05, OPS-07, HR-02          |
| **Office Staff**       | General office user      | OPS-02, OPS-10, OPS-11, OPS-12 |
| **Client Portal User** | External customer        | CRM-01, CRM-02, CRM-03, CRM-04 |
| **Vendor Portal User** | External vendor          | Restricted CRM-01, CRM-02      |

---

**Next: Section 3 - OPS Features (Operations Core)**

# Dartwing Company PRD - Section 3: Operations Core (OPS)

_"The Operating System for the company. Industry-agnostic execution engines."_

---

## OPS-01: Dartwing Receptionist (Voice/Text)

### Description

AI-powered auto-attendant that screens calls, routes based on intent, and executes voice commands. Integrates with `dartwing_fone` for SIP/voice capabilities.

### User Stories

- As a caller, I want to reach the right person without navigating menus
- As a manager, I want calls screened and announced before I answer
- As a business, I want after-hours calls handled intelligently

### Functional Requirements

| ID        | Requirement                                              | Priority |
| --------- | -------------------------------------------------------- | -------- |
| OPS-01-01 | Answer inbound calls with customizable greeting          | Must     |
| OPS-01-02 | Transcribe caller intent using speech-to-text            | Must     |
| OPS-01-03 | Route calls based on intent classification               | Must     |
| OPS-01-04 | "Whisper" caller info to agent before connection         | Must     |
| OPS-01-05 | Handle after-hours with voicemail or callback scheduling | Must     |
| OPS-01-06 | Execute voice commands ("Schedule appointment for...")   | Should   |
| OPS-01-07 | Screen unknown callers ("Who may I say is calling?")     | Should   |
| OPS-01-08 | Integrate caller ID with CRM for context                 | Should   |
| OPS-01-09 | Support SMS auto-response when unavailable               | Could    |
| OPS-01-10 | Multi-language support                                   | Could    |

### Technical Implementation

```
Inbound Call (dartwing_fone)
        │
        ▼
┌───────────────┐
│ SIP Webhook   │ ← Call received event
└───────┬───────┘
        │
┌───────▼───────┐
│ AI Greeting   │ "Thank you for calling [Company]"
│ + Intent      │ Speech-to-text → intent classification
└───────┬───────┘
        │
┌───────▼───────┐
│ CRM Lookup    │ Match caller ID to Contact/Lead
└───────┬───────┘
        │
┌───────▼───────┐
│ Route Engine  │ Skills-based routing + availability
└───────┬───────┘
        │
┌───────▼───────┐
│ Whisper →     │ "Call from John Smith, existing customer,
│ Agent         │  last order $5,000, calling about invoice"
└───────────────┘
```

### Acceptance Criteria

- [ ] Answers calls within 2 rings
- [ ] Intent classification >85% accuracy
- [ ] Whisper delivered before agent answers
- [ ] After-hours routing works correctly
- [ ] Call logs created in CRM automatically

---

## OPS-02: Universal Company Inbox

### Description

Unified communication feed merging Email, SMS, Voice, and Social channels into a single timeline per contact.

### User Stories

- As a user, I want to see all communications with a contact in one place
- As a team, I want to collaborate on client messages with internal notes
- As a manager, I want visibility into all client communications

### Functional Requirements

| ID        | Requirement                                      | Priority |
| --------- | ------------------------------------------------ | -------- |
| OPS-02-01 | Aggregate Email into unified inbox               | Must     |
| OPS-02-02 | Aggregate SMS/MMS into unified inbox             | Must     |
| OPS-02-03 | Aggregate Voice calls (with transcripts)         | Must     |
| OPS-02-04 | Merge messages into Contact "Sessions"           | Must     |
| OPS-02-05 | Internal side-panel for private notes/discussion | Must     |
| OPS-02-06 | Assign conversations to users/teams              | Must     |
| OPS-02-07 | WhatsApp Business integration                    | Should   |
| OPS-02-08 | Facebook Messenger integration                   | Should   |
| OPS-02-09 | Instagram DM integration                         | Could    |
| OPS-02-10 | Telegram integration                             | Could    |
| OPS-02-11 | AI-suggested replies                             | Should   |
| OPS-02-12 | Sentiment analysis per message                   | Should   |

### Technical Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    CHANNEL PLUGINS                           │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │ Email  │ │  SMS   │ │ Voice  │ │WhatsApp│ │   FB   │   │
│  │ IMAP/  │ │dartwing│ │dartwing│ │  API   │ │  API   │   │
│  │ SMTP   │ │ _fone  │ │ _fone  │ │        │ │        │   │
│  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘   │
└──────┼──────────┼──────────┼──────────┼──────────┼─────────┘
       │          │          │          │          │
       └──────────┴──────────┴──────────┴──────────┘
                             │
                    ┌────────▼────────┐
                    │ Message Router  │
                    │ • Match Contact │
                    │ • Create Session│
                    │ • Notify Owner  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Unified Inbox   │
                    │ (Conversation   │
                    │  DocType)       │
                    └─────────────────┘
```

### Data Model

```
Conversation
├── contact (Link → Contact)
├── organization (Link → Organization)
├── channel (Select: email/sms/voice/whatsapp/messenger)
├── status (Select: open/pending/resolved/closed)
├── assigned_to (Link → User)
├── sentiment (Float: -1 to 1)
├── messages (Table → Conversation Message)
│   ├── direction (in/out)
│   ├── content (Text)
│   ├── timestamp (Datetime)
│   ├── channel_message_id (Data)
│   └── attachments (Table)
└── internal_notes (Table → Conversation Note)
    ├── user (Link → User)
    ├── note (Text)
    └── timestamp (Datetime)
```

---

## OPS-03: No-Code Workflow & Task Builder

### Description

Master execution engine for business processes. Visual workflow builder with external app sync.

### User Stories

- As a manager, I want to automate repetitive multi-step processes
- As a user, I want tasks to sync to my preferred task app
- As an admin, I want to build workflows without coding

### Functional Requirements

| ID        | Requirement                                        | Priority |
| --------- | -------------------------------------------------- | -------- |
| OPS-03-01 | Visual drag-drop workflow builder                  | Must     |
| OPS-03-02 | Trigger workflows from DocType events              | Must     |
| OPS-03-03 | Conditional branching (if/then/else)               | Must     |
| OPS-03-04 | Create tasks and assign to users                   | Must     |
| OPS-03-05 | Due date calculation (business days)               | Must     |
| OPS-03-06 | Bi-directional sync with Microsoft Planner         | Should   |
| OPS-03-07 | Bi-directional sync with Trello                    | Should   |
| OPS-03-08 | Auto-block calendar time for tasks                 | Should   |
| OPS-03-09 | "Learning Mode" - record clicks to create workflow | Could    |
| OPS-03-10 | Parallel task execution                            | Should   |
| OPS-03-11 | SLA timers with escalation                         | Must     |
| OPS-03-12 | Webhook actions for external systems               | Must     |

### Workflow Components

```
TRIGGERS                    ACTIONS                    CONDITIONS
─────────                   ───────                    ──────────
• DocType created           • Create Task              • Field equals
• DocType updated           • Assign to User           • Field contains
• Field changed             • Send Email               • Field > / <
• Date reached              • Send SMS                 • Role is
• Manual start              • Call Webhook             • Time is
• Webhook received          • Update Field             • Day of week
• Schedule (cron)           • Create Document          • Custom formula
                            • Wait (delay)
                            • Branch (if/else)
                            • Approve/Reject
```

---

## OPS-04: AI Dispatch & GIS Smart Routing

### Description

Map-based job assignment using real-time location, drive-time calculations, and skill matching.

### User Stories

- As a dispatcher, I want to see all technicians and jobs on a map
- As a business, I want jobs assigned to minimize drive time
- As a technician, I want an optimized route for my day

### Functional Requirements

| ID        | Requirement                                 | Priority |
| --------- | ------------------------------------------- | -------- |
| OPS-04-01 | Interactive map showing jobs and workers    | Must     |
| OPS-04-02 | Geocode addresses automatically             | Must     |
| OPS-04-03 | Calculate drive time between points         | Must     |
| OPS-04-04 | Drag-drop job assignment on map             | Must     |
| OPS-04-05 | Auto-suggest best worker for job            | Must     |
| OPS-04-06 | Real-time worker location tracking (opt-in) | Should   |
| OPS-04-07 | Route optimization for multiple stops       | Should   |
| OPS-04-08 | Traffic-aware time estimates                | Should   |
| OPS-04-09 | Territory/zone management                   | Should   |
| OPS-04-10 | Skill/certification matching                | Must     |
| OPS-04-11 | Customer time-window preferences            | Should   |
| OPS-04-12 | "Send ETA" to customer automatically        | Should   |

### Technical Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    DISPATCH DASHBOARD                        │
│  ┌─────────────────────────────┐ ┌────────────────────────┐ │
│  │         MAP VIEW            │ │     UNASSIGNED JOBS    │ │
│  │    ┌─────┐                  │ │ ┌──────────────────┐   │ │
│  │    │ 🔧  │ Tech A           │ │ │ Job #1234        │   │ │
│  │    └─────┘                  │ │ │ 123 Main St      │   │ │
│  │         ┌─────┐             │ │ │ HVAC Repair      │   │ │
│  │         │ 📍  │ Job         │ │ │ [Assign ▼]       │   │ │
│  │         └─────┘             │ │ └──────────────────┘   │ │
│  │    ┌─────┐                  │ │ ┌──────────────────┐   │ │
│  │    │ 🔧  │ Tech B           │ │ │ Job #1235        │   │ │
│  │    └─────┘                  │ │ └──────────────────┘   │ │
│  └─────────────────────────────┘ └────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ AI Suggestion: Assign Job #1234 to Tech A            │   │
│  │ Reason: 12 min away, has HVAC cert, 2hr slot open   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## OPS-05: Form Builder + Mobile Submission

### Description

Custom mobile forms for field data collection. Offline-capable with rich media support.

### User Stories

- As an admin, I want to create custom forms without coding
- As a field worker, I want forms that work without internet
- As a manager, I want photos and signatures captured in the field

### Functional Requirements

| ID        | Requirement                                           | Priority |
| --------- | ----------------------------------------------------- | -------- |
| OPS-05-01 | Drag-drop form builder                                | Must     |
| OPS-05-02 | Field types: text, number, date, select, multi-select | Must     |
| OPS-05-03 | Photo/video capture fields                            | Must     |
| OPS-05-04 | Signature capture field                               | Must     |
| OPS-05-05 | GPS location capture                                  | Must     |
| OPS-05-06 | Offline mode with local storage                       | Must     |
| OPS-05-07 | Auto-sync when back online                            | Must     |
| OPS-05-08 | Conditional field visibility                          | Should   |
| OPS-05-09 | Calculations and formulas                             | Should   |
| OPS-05-10 | Barcode/QR code scanning                              | Should   |
| OPS-05-11 | Voice-to-text input                                   | Could    |
| OPS-05-12 | Pre-fill from linked records                          | Should   |

---

## OPS-06: Live Status Boards

### Description

Visual dashboard layer showing work in Kanban, Gantt, Calendar, and Map views.

### User Stories

- As a manager, I want to see work status at a glance
- As a team, I want to update status by dragging cards
- As executives, I want to see project timelines

### Functional Requirements

| ID        | Requirement                         | Priority |
| --------- | ----------------------------------- | -------- |
| OPS-06-01 | Kanban board view                   | Must     |
| OPS-06-02 | Gantt chart view                    | Should   |
| OPS-06-03 | Calendar view                       | Must     |
| OPS-06-04 | Map view (for location-based work)  | Should   |
| OPS-06-05 | Drag-drop to change status          | Must     |
| OPS-06-06 | Drag-drop triggers workflow actions | Should   |
| OPS-06-07 | Configurable columns/lanes          | Must     |
| OPS-06-08 | Filtering and grouping              | Must     |
| OPS-06-09 | Real-time updates (WebSocket)       | Should   |
| OPS-06-10 | Swimlanes by assignee/team          | Should   |

---

## OPS-07: Company Knowledge Base + AI (RAG)

### Description

Internal wiki with AI-powered search and question answering.

### User Stories

- As an employee, I want to find answers without asking colleagues
- As a field tech, I want troubleshooting guides on my phone
- As a manager, I want SOPs accessible and searchable

### Functional Requirements

| ID        | Requirement                               | Priority |
| --------- | ----------------------------------------- | -------- |
| OPS-07-01 | Wiki-style article editor (Markdown)      | Must     |
| OPS-07-02 | Folder/category organization              | Must     |
| OPS-07-03 | Full-text search                          | Must     |
| OPS-07-04 | AI Q&A with source citations              | Must     |
| OPS-07-05 | Upload and index PDFs                     | Must     |
| OPS-07-06 | Upload and index videos (transcribe)      | Should   |
| OPS-07-07 | Role-based access (public/internal/admin) | Must     |
| OPS-07-08 | Version history                           | Should   |
| OPS-07-09 | "Was this helpful?" feedback              | Should   |
| OPS-07-10 | Auto-suggest related articles             | Could    |

### Technical Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────┘

User Question: "How do I reset the XYZ controller?"
        │
        ▼
┌───────────────┐
│ Embed Query   │ → Vector representation
└───────┬───────┘
        │
┌───────▼───────┐
│ Vector Search │ → Find similar chunks
│ (pgvector /   │    from Knowledge Base
│  OpenSearch)  │
└───────┬───────┘
        │
┌───────▼───────┐
│ Retrieve Top  │ → 5 most relevant chunks
│ K Chunks      │    with source metadata
└───────┬───────┘
        │
┌───────▼───────┐
│ LLM Generate  │ → Answer with citations
│ Answer        │    "[According to SOP-123...]"
└───────────────┘
```

---

## OPS-08: Broadcast & Emergency Alerts

### Description

Mass notification system for critical communications.

### User Stories

- As a manager, I want to alert all staff instantly
- As safety officer, I want emergency broadcasts with acknowledgment
- As HR, I want to notify teams about schedule changes

### Functional Requirements

| ID        | Requirement                                    | Priority |
| --------- | ---------------------------------------------- | -------- |
| OPS-08-01 | Multi-channel blast (Push, SMS, Voice, Email)  | Must     |
| OPS-08-02 | Recipient groups (teams, locations, all)       | Must     |
| OPS-08-03 | Acknowledgment tracking dashboard              | Must     |
| OPS-08-04 | Escalation if no acknowledgment                | Should   |
| OPS-08-05 | Geofenced targeting                            | Should   |
| OPS-08-06 | Pre-built templates (Emergency, Weather, etc.) | Should   |
| OPS-08-07 | Schedule broadcasts in advance                 | Should   |
| OPS-08-08 | Text-to-speech for voice calls                 | Should   |

---

## OPS-09: AI Daily Standup Summary

### Description

Automated morning briefing agent that summarizes activity and flags issues.

### User Stories

- As a manager, I want a summary of yesterday's activity
- As a user, I want to know my priorities for today
- As a team lead, I want to see flagged issues requiring attention

### Functional Requirements

| ID        | Requirement                         | Priority |
| --------- | ----------------------------------- | -------- |
| OPS-09-01 | Auto-generate daily summary         | Must     |
| OPS-09-02 | Include yesterday's completed tasks | Must     |
| OPS-09-03 | Include today's scheduled tasks     | Must     |
| OPS-09-04 | Flag overdue items                  | Must     |
| OPS-09-05 | Flag negative customer sentiment    | Should   |
| OPS-09-06 | Delivery via email digest           | Must     |
| OPS-09-07 | Delivery via in-app notification    | Should   |
| OPS-09-08 | Voice summary via phone (call me)   | Could    |
| OPS-09-09 | Customizable per user               | Should   |

---

## OPS-10: Visitor & Delivery Management

### Description

Digital front desk for guest check-in and package tracking.

### User Stories

- As a visitor, I want easy self-service check-in
- As a host, I want notification when my visitor arrives
- As office manager, I want to track all deliveries

### Functional Requirements

| ID        | Requirement                             | Priority |
| --------- | --------------------------------------- | -------- |
| OPS-10-01 | Kiosk mode for self check-in            | Must     |
| OPS-10-02 | Capture visitor photo                   | Should   |
| OPS-10-03 | Capture visitor signature (NDA, policy) | Should   |
| OPS-10-04 | Auto-notify host via push/SMS/email     | Must     |
| OPS-10-05 | Print visitor badge                     | Should   |
| OPS-10-06 | Package barcode scanning                | Should   |
| OPS-10-07 | Package photo capture                   | Should   |
| OPS-10-08 | Notify recipient of package arrival     | Must     |
| OPS-10-09 | Visitor log history/reports             | Must     |
| OPS-10-10 | Pre-registration for expected visitors  | Should   |

---

## OPS-11: Resource & Room Booking

### Description

Reservation system for shared company assets.

### User Stories

- As an employee, I want to book a conference room
- As a manager, I want to reserve company vehicles
- As equipment manager, I want to track tool checkouts

### Functional Requirements

| ID        | Requirement                                   | Priority |
| --------- | --------------------------------------------- | -------- |
| OPS-11-01 | Resource catalog (rooms, vehicles, equipment) | Must     |
| OPS-11-02 | Calendar view of availability                 | Must     |
| OPS-11-03 | Book with date/time range                     | Must     |
| OPS-11-04 | Conflict detection                            | Must     |
| OPS-11-05 | Approval workflow for high-value items        | Should   |
| OPS-11-06 | Buffer time between bookings (cleaning)       | Should   |
| OPS-11-07 | QR code check-in/check-out                    | Should   |
| OPS-11-08 | Recurring reservations                        | Should   |
| OPS-11-09 | Integration with room displays                | Could    |
| OPS-11-10 | Auto-release if no check-in                   | Should   |

---

## OPS-12: Company-Wide "Ask Anything" Bar

### Description

Global search and command center accessible from anywhere.

### User Stories

- As a user, I want to find anything by typing a query
- As a power user, I want slash commands for quick actions
- As anyone, I want AI to answer questions about our data

### Functional Requirements

| ID        | Requirement                                  | Priority |
| --------- | -------------------------------------------- | -------- |
| OPS-12-01 | Global search hotkey (Cmd+K / Ctrl+K)        | Must     |
| OPS-12-02 | Search across all DocTypes                   | Must     |
| OPS-12-03 | Search file contents (PDFs, docs)            | Should   |
| OPS-12-04 | Search chat/message history                  | Should   |
| OPS-12-05 | Slash commands (/create, /assign, /schedule) | Should   |
| OPS-12-06 | AI natural language queries                  | Should   |
| OPS-12-07 | Recent searches history                      | Should   |
| OPS-12-08 | Keyboard navigation                          | Must     |
| OPS-12-09 | Quick actions from results                   | Should   |

---

**Next: Section 4 - CRM Features**

# Dartwing Company PRD - Section 4: CRM & Growth Strategy

_"The Context Layer. Manages external relationships and defines WHO we target."_

**Note:** These features are OVERLAYS on Frappe CRM, not extensions. They add functionality without modifying CRM core.

---

## CRM-01: Branded Client Portal

### Description

Secure, white-labeled login area for clients to access their information, documents, and services.

### User Stories

- As a client, I want to see my invoices and project status anytime
- As a business, I want clients to self-serve instead of calling
- As an admin, I want to customize the portal per client type

### Functional Requirements

| ID        | Requirement                                        | Priority |
| --------- | -------------------------------------------------- | -------- |
| CRM-01-01 | Secure login with email/password                   | Must     |
| CRM-01-02 | SSO integration (Google, Microsoft)                | Should   |
| CRM-01-03 | White-label branding (logo, colors, domain)        | Must     |
| CRM-01-04 | Configurable widget dashboard                      | Must     |
| CRM-01-05 | View invoices and payment history                  | Must     |
| CRM-01-06 | View project/job status                            | Must     |
| CRM-01-07 | View and download documents                        | Must     |
| CRM-01-08 | Submit service requests                            | Must     |
| CRM-01-09 | Schedule appointments                              | Should   |
| CRM-01-10 | Secure messaging to company                        | Should   |
| CRM-01-11 | View technician ETA/location                       | Should   |
| CRM-01-12 | Pay invoices online                                | Should   |
| CRM-01-13 | "View Sets" - configure widgets per customer group | Must     |
| CRM-01-14 | Mobile-responsive design                           | Must     |

### View Set Architecture

```
View Set Configuration
├── name: "Premium Client View"
├── applies_to: Customer Group = "VIP"
├── widgets:
│   ├── dashboard_summary (enabled, position: 1)
│   ├── open_invoices (enabled, position: 2)
│   ├── active_projects (enabled, position: 3)
│   ├── document_vault (enabled, position: 4)
│   ├── support_tickets (enabled, position: 5)
│   ├── appointment_scheduler (enabled, position: 6)
│   └── team_contacts (enabled, position: 7)
└── branding:
    ├── logo: "/files/client-logo.png"
    ├── primary_color: "#2563eb"
    └── welcome_message: "Welcome back!"
```

### Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo]        Client Portal          [John Smith ▼] [⚙️]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome back, John!                                        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Open        │  │ Active      │  │ Next        │        │
│  │ Balance     │  │ Projects    │  │ Appointment │        │
│  │             │  │             │  │             │        │
│  │   $2,450    │  │      3      │  │  Dec 5      │        │
│  │             │  │             │  │  10:00 AM   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Recent Invoices                                [View All]│
│  │ ──────────────────────────────────────────────────── │  │
│  │ INV-2025-0123  │  $1,200  │  Nov 15  │  [Pay Now]   │  │
│  │ INV-2025-0098  │    $850  │  Oct 28  │  Paid ✓      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Your Projects                                         │  │
│  │ ──────────────────────────────────────────────────── │  │
│  │ 🔵 Website Redesign      │  In Progress  │  75%      │  │
│  │ 🟢 SEO Campaign          │  Active       │  Running   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│           [📞 Contact Us]    [📅 Schedule Call]            │
└─────────────────────────────────────────────────────────────┘
```

---

## CRM-02: File & Document Vault (Client Scoped)

### Description

Secure file sharing with granular permissions and audit logging.

### User Stories

- As a client, I want easy access to all my documents
- As a company, I want to share files securely with audit trail
- As compliance, I want to know who viewed what and when

### Functional Requirements

| ID        | Requirement                                    | Priority |
| --------- | ---------------------------------------------- | -------- |
| CRM-02-01 | Upload files with drag-drop                    | Must     |
| CRM-02-02 | Organize files in folders                      | Must     |
| CRM-02-03 | "Document Sets" - pre-defined folder templates | Should   |
| CRM-02-04 | Share files to client portal                   | Must     |
| CRM-02-05 | Expiring share links                           | Should   |
| CRM-02-06 | Password-protected links                       | Should   |
| CRM-02-07 | Download watermarking                          | Could    |
| CRM-02-08 | Audit log: view, download, share events        | Must     |
| CRM-02-09 | Bulk upload (ZIP extraction)                   | Should   |
| CRM-02-10 | Version control                                | Should   |
| CRM-02-11 | E-signature request integration                | Should   |
| CRM-02-12 | Storage quota per customer                     | Should   |

### Document Set Templates

```
Document Set: "Client Onboarding"
├── 01-Contracts/
│   ├── Service Agreement (required)
│   └── NDA (optional)
├── 02-Credentials/
│   ├── Login Information
│   └── API Keys
├── 03-Brand Assets/
│   ├── Logo Files
│   └── Brand Guidelines
└── 04-Project Files/
    └── (dynamic)
```

---

## CRM-03: AI Meeting & Appointment Booker

### Description

Automated scheduling that handles availability, resources, and payments.

### User Stories

- As a client, I want to book a meeting without phone tag
- As a service provider, I want double-booking prevented
- As a business, I want deposits collected at booking

### Functional Requirements

| ID        | Requirement                                      | Priority |
| --------- | ------------------------------------------------ | -------- |
| CRM-03-01 | Calendar availability display                    | Must     |
| CRM-03-02 | Book appointments by selecting time slot         | Must     |
| CRM-03-03 | Lock user calendar + room simultaneously         | Must     |
| CRM-03-04 | Buffer time between appointments                 | Should   |
| CRM-03-05 | Appointment type configuration (duration, price) | Must     |
| CRM-03-06 | Collect payment/deposit at booking               | Should   |
| CRM-03-07 | Confirmation and reminder emails/SMS             | Must     |
| CRM-03-08 | Reschedule and cancellation self-service         | Must     |
| CRM-03-09 | Timezone handling                                | Must     |
| CRM-03-10 | Round-robin assignment to team members           | Should   |
| CRM-03-11 | Intake form before booking                       | Should   |
| CRM-03-12 | Integration with Google/Outlook Calendar         | Should   |
| CRM-03-13 | Video meeting link generation (Zoom/Meet)        | Should   |

### Booking Flow

```
Client selects "Consultation Call (30 min)"
        │
        ▼
┌───────────────┐
│ Show Calendar │ ← Pull availability from:
│               │   • User calendar
└───────┬───────┘   • Room calendar (if needed)
        │           • Business hours
        │
┌───────▼───────┐
│ Select Slot   │ "Tuesday, Dec 5, 10:00 AM"
└───────┬───────┘
        │
┌───────▼───────┐
│ Intake Form   │ Name, Email, Phone, "What's this about?"
└───────┬───────┘
        │
┌───────▼───────────────┐
│ Payment Gate          │ $50 deposit (if configured)
│ (Stripe integration)  │
└───────┬───────────────┘
        │
┌───────▼───────┐
│ Lock Slots    │ → Create Calendar Event
└───────┬───────┘ → Create CRM record
        │         → Send confirmations
        ▼
   Booking Complete
```

---

## CRM-04: Service Ticket Workflow

### Description

Smart support routing with sentiment analysis and VIP escalation.

### User Stories

- As a client, I want to report issues and track status
- As support, I want tickets routed based on type and priority
- As management, I want VIP clients handled with priority

### Functional Requirements

| ID        | Requirement                              | Priority |
| --------- | ---------------------------------------- | -------- |
| CRM-04-01 | Submit ticket via portal, email, or chat | Must     |
| CRM-04-02 | Auto-categorize by keywords              | Should   |
| CRM-04-03 | Auto-assign based on category/skills     | Should   |
| CRM-04-04 | VIP escalation (check Customer Group)    | Must     |
| CRM-04-05 | Sentiment analysis on ticket content     | Should   |
| CRM-04-06 | Negative sentiment auto-escalation       | Should   |
| CRM-04-07 | SLA timer per priority level             | Must     |
| CRM-04-08 | Internal notes (not visible to client)   | Must     |
| CRM-04-09 | File attachments                         | Must     |
| CRM-04-10 | Status updates via email/portal          | Must     |
| CRM-04-11 | Merge duplicate tickets                  | Should   |
| CRM-04-12 | Link to OPS-03 workflow engine           | Must     |
| CRM-04-13 | Customer satisfaction survey on close    | Should   |

### Ticket Routing Logic

```python
def route_ticket(ticket):
    customer = get_customer(ticket.contact)

    # VIP Check
    if customer.customer_group in ["VIP", "Enterprise"]:
        ticket.priority = "Urgent"
        ticket.assigned_to = get_account_manager(customer)
        send_alert("VIP ticket created", managers)

    # Sentiment Check
    sentiment = analyze_sentiment(ticket.description)
    if sentiment.score < -0.5:  # Negative
        ticket.priority = max(ticket.priority, "High")
        ticket.flags.append("negative_sentiment")

    # Category Routing
    if not ticket.assigned_to:
        team = get_team_for_category(ticket.category)
        ticket.assigned_to = get_available_agent(team)

    # Start SLA Timer
    ticket.sla_deadline = calculate_sla(ticket.priority)
```

---

## CRM-05: Custom Fields & Business Objects

### Description

Store industry-specific data without schema modifications.

### User Stories

- As a healthcare provider, I want to store Patient IDs
- As a property manager, I want to store Unit Numbers
- As any business, I want custom fields searchable and reportable

### Functional Requirements

| ID        | Requirement                                                 | Priority |
| --------- | ----------------------------------------------------------- | -------- |
| CRM-05-01 | Define custom field schemas per DocType                     | Must     |
| CRM-05-02 | Field types: text, number, date, select, multi-select, link | Must     |
| CRM-05-03 | Store in JSON with typed validation                         | Must     |
| CRM-05-04 | Index custom fields for search                              | Must     |
| CRM-05-05 | Include in reports and filters                              | Should   |
| CRM-05-06 | Conditional visibility rules                                | Should   |
| CRM-05-07 | Field-level permissions                                     | Should   |
| CRM-05-08 | Import/export custom field data                             | Should   |
| CRM-05-09 | Custom field templates per industry                         | Could    |

### Data Model

```
Custom Field Schema
├── doctype: "Customer"
├── organization: "ORG-001"
├── fields:
│   ├── patient_id:
│   │   ├── type: "Data"
│   │   ├── label: "Patient ID"
│   │   ├── required: true
│   │   ├── unique: true
│   │   └── indexed: true
│   ├── insurance_provider:
│   │   ├── type: "Link"
│   │   ├── options: "Insurance Provider"
│   │   └── indexed: true
│   └── date_of_birth:
│       ├── type: "Date"
│       └── indexed: true

Customer Document
├── name: "CUST-001"
├── customer_name: "John Smith"
├── ... (standard fields)
└── custom_data: {
        "patient_id": "PT-12345",
        "insurance_provider": "Blue Cross",
        "date_of_birth": "1985-03-15"
    }
```

---

## CRM-06: SLA & Response Tracking

### Description

Accountability engine for response time commitments.

### User Stories

- As a manager, I want to track if we meet response commitments
- As a client, I want to know when to expect a response
- As an agent, I want alerts before SLA breach

### Functional Requirements

| ID        | Requirement                                     | Priority |
| --------- | ----------------------------------------------- | -------- |
| CRM-06-01 | Define SLA policies per priority/customer group | Must     |
| CRM-06-02 | Track time to first response                    | Must     |
| CRM-06-03 | Track time to resolution                        | Must     |
| CRM-06-04 | Pause SLA during "waiting on customer"          | Must     |
| CRM-06-05 | Business hours calculation                      | Must     |
| CRM-06-06 | Holiday calendar integration                    | Should   |
| CRM-06-07 | Warning alerts before breach (75%, 90%)         | Must     |
| CRM-06-08 | Auto-escalation on breach                       | Must     |
| CRM-06-09 | SLA compliance dashboard                        | Must     |
| CRM-06-10 | Historical SLA performance reports              | Should   |

### SLA Policy Configuration

```
SLA Policy: "Enterprise Support"
├── applies_to:
│   └── Customer Group: ["Enterprise", "VIP"]
├── response_times:
│   ├── Urgent: 1 hour
│   ├── High: 4 hours
│   ├── Medium: 8 hours
│   └── Low: 24 hours
├── resolution_times:
│   ├── Urgent: 4 hours
│   ├── High: 24 hours
│   ├── Medium: 72 hours
│   └── Low: 120 hours
├── business_hours: "Mon-Fri 8AM-6PM EST"
├── escalation_path:
│   ├── 75%: notify_assignee
│   ├── 90%: notify_manager
│   └── 100%: reassign_to_manager
```

---

## CRM-07: Growth Orchestrator (The Strategist)

### Description

AI Agent that interviews users to build Lead Generation campaigns, then interfaces with `dartwing_leadgen` to execute.

### User Stories

- As a business owner, I want AI to help me define my target market
- As a sales manager, I want automated lead generation
- As marketing, I want campaigns built from business context

### Functional Requirements

| ID        | Requirement                                   | Priority |
| --------- | --------------------------------------------- | -------- |
| CRM-07-01 | AI interview flow ("20 Questions")            | Must     |
| CRM-07-02 | Auto-populate defaults from Company settings  | Must     |
| CRM-07-03 | Define Ideal Customer Profile (ICP)           | Must     |
| CRM-07-04 | Define Geographic targets                     | Must     |
| CRM-07-05 | Define Persona/Role targets                   | Must     |
| CRM-07-06 | Define Campaign offers/hooks                  | Should   |
| CRM-07-07 | Generate Search_Job JSON for dartwing_leadgen | Must     |
| CRM-07-08 | Send jobs to GEN-01 (Universal Search)        | Must     |
| CRM-07-09 | Receive raw results from GEN-01               | Must     |
| CRM-07-10 | Send for enrichment via GEN-02                | Should   |
| CRM-07-11 | Score/filter via GEN-03 (Profile Matcher)     | Must     |
| CRM-07-12 | Create Leads in Frappe CRM from results       | Must     |
| CRM-07-13 | Campaign performance tracking                 | Should   |
| CRM-07-14 | A/B test different ICPs                       | Could    |

### AI Interview Flow

```
Growth Orchestrator: "Let's build your lead generation strategy."

Step 1: Context Gathering
├── "What does your company do?" (or read from Company.description)
├── "What products/services are you selling?" (read from Item catalog)
└── "What's your typical deal size?"

Step 2: Ideal Customer Profile
├── "What industry are your best customers in?"
├── "What company size (employees/revenue)?"
├── "What technology do they typically use?"
└── "What problems do they have that you solve?"

Step 3: Geographic Targeting
├── "What locations do you serve?"
├── "Any specific cities or regions to focus on?"
└── "Exclude any areas?"

Step 4: Persona Definition
├── "What job titles do you typically sell to?"
├── "Who is the decision maker vs. user?"
└── "What departments?"

Step 5: Campaign Setup
├── "What offer will you lead with?" (free consultation, demo, etc.)
├── "What's your follow-up cadence?"
└── "Budget for this campaign?"

Output: Search_Job JSON + Campaign Record
```

### Integration with dartwing_leadgen

```
┌─────────────────────────────────────────────────────────────┐
│                    dartwing_company                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               CRM-07: Growth Orchestrator             │   │
│  │                                                       │   │
│  │  1. AI Interview → Build ICP                         │   │
│  │  2. Generate Search_Job JSON                         │   │
│  │  3. Send to dartwing_leadgen                         │   │
│  │  4. Receive results                                  │   │
│  │  5. Create Leads in Frappe CRM                       │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ Search_Job JSON
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    dartwing_leadgen                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ GEN-01: Universal Search                             │    │
│  │ • LinkedIn, Google Maps, Directories                │    │
│  │ • Returns: Raw entity list                          │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│  ┌─────────────────────▼───────────────────────────────┐    │
│  │ GEN-02: Data Enrichment                              │    │
│  │ • Email finder, phone lookup                        │    │
│  │ • SMTP validation                                   │    │
│  │ • Returns: Enriched entities                        │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│  ┌─────────────────────▼───────────────────────────────┐    │
│  │ GEN-03: Profile Matcher                              │    │
│  │ • Score against ICP                                 │    │
│  │ • Filter by constraints                             │    │
│  │ • Returns: Qualified leads                          │    │
│  └─────────────────────┬───────────────────────────────┘    │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ Qualified Leads
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frappe CRM                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Lead DocType                                         │    │
│  │ • source: "Growth Orchestrator"                     │    │
│  │ • campaign: "Q4-2025-Enterprise"                    │    │
│  │ • icp_score: 85                                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Search_Job JSON Schema

```json
{
  "job_id": "SJ-2025-001234",
  "requestor": {
    "module": "dartwing_company",
    "organization": "ORG-001",
    "campaign": "CAMP-001"
  },
  "search_parameters": {
    "keywords": ["HVAC contractor", "commercial HVAC"],
    "industries": ["Construction", "Facilities Management"],
    "company_size": {
      "employees_min": 10,
      "employees_max": 500,
      "revenue_min": 1000000,
      "revenue_max": 50000000
    },
    "technologies": ["Salesforce", "ServiceTitan"]
  },
  "geographic": {
    "countries": ["US"],
    "states": ["TX", "FL", "CA"],
    "cities": ["Houston", "Miami", "Los Angeles"],
    "radius_miles": 50
  },
  "personas": {
    "titles": ["Owner", "Operations Manager", "Facilities Director"],
    "departments": ["Operations", "Facilities", "Maintenance"]
  },
  "limits": {
    "max_results": 500,
    "budget_usd": 100
  },
  "enrichment": {
    "find_emails": true,
    "find_phones": true,
    "verify_emails": true
  },
  "scoring": {
    "icp_criteria": {
      "must_have": ["commercial_focus"],
      "nice_to_have": ["multi_location", "growth_signals"]
    },
    "minimum_score": 60
  }
}
```

---

**Next: Section 5 - HR Features**

# Dartwing Company PRD - Section 5: HRMS Overlay (HR)

_"The Logistics Layer. Manages workforce availability feeding into Frappe HR."_

**Note:** These features overlay Frappe HR / ERPNext HR module, syncing data to standard HR DocTypes.

---

## HR-01: Shift & On-Call Scheduler

### Description

Advanced rostering system with shift swapping marketplace and qualification tracking.

### User Stories

- As a scheduler, I want to build complex rotating schedules
- As an employee, I want to request shift swaps easily
- As a manager, I want to ensure only qualified staff are scheduled

### Functional Requirements

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------- |
| HR-01-01 | Create shift templates (Morning, Evening, Night) | Must     |
| HR-01-02 | Drag-drop schedule builder (week/month view)     | Must     |
| HR-01-03 | Copy schedules from previous periods             | Should   |
| HR-01-04 | Rotating schedule patterns (4-on-3-off, etc.)    | Should   |
| HR-01-05 | Employee availability preferences                | Must     |
| HR-01-06 | Shift swap marketplace (employee requests)       | Must     |
| HR-01-07 | Manager approval workflow for swaps              | Must     |
| HR-01-08 | On-call rotation scheduling                      | Should   |
| HR-01-09 | Qualification/certification blocking             | Must     |
| HR-01-10 | Expiring certification alerts                    | Must     |
| HR-01-11 | Overtime alerts and limits                       | Should   |
| HR-01-12 | Publish schedule to employees (push/email)       | Must     |
| HR-01-13 | Sync final roster to Frappe HR Shift Assignment  | Must     |
| HR-01-14 | Mobile schedule view for employees               | Must     |
| HR-01-15 | Open shift posting (employees can claim)         | Should   |
| HR-01-16 | Minimum staffing requirements per shift          | Should   |

### Shift Swap Marketplace

```
┌─────────────────────────────────────────────────────────────┐
│                    SHIFT SWAP MARKETPLACE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔄 Available Swaps                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Carlos needs coverage:                                │  │
│  │ 📅 Tuesday, Dec 10  │  🕐 7:00 AM - 3:00 PM         │  │
│  │ 📍 Downtown Location │  💼 Field Technician          │  │
│  │                                                       │  │
│  │ Requirements: HVAC Certified ✓                       │  │
│  │                                                       │  │
│  │ [I Can Cover This] [Not Available]                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Maria needs coverage:                                 │  │
│  │ 📅 Wednesday, Dec 11 │  🕐 3:00 PM - 11:00 PM       │  │
│  │ 📍 Airport Branch    │  💼 Customer Service          │  │
│  │                                                       │  │
│  │ [I Can Cover This] [Not Available]                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 📤 My Swap Requests                                   │  │
│  │ ──────────────────────────────────────────────────── │  │
│  │ Friday, Dec 13  │  Awaiting offers  │  [Cancel]      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Qualification Blocking Logic

```python
def can_work_shift(employee, shift):
    """Check if employee can be scheduled for shift"""

    # Get required qualifications for shift role
    required = get_shift_requirements(shift.role)

    # Get employee's current certifications
    employee_certs = get_employee_certifications(employee)

    for req in required:
        cert = employee_certs.get(req.certification)

        if not cert:
            return False, f"Missing certification: {req.certification}"

        if cert.expiry_date and cert.expiry_date < shift.date:
            return False, f"Certification expires before shift: {req.certification}"

    return True, None

# Alert for expiring certifications
def check_expiring_certifications():
    """Daily job to alert about expiring certs"""

    threshold = today() + timedelta(days=30)

    expiring = get_certifications_expiring_before(threshold)

    for cert in expiring:
        notify_employee(cert.employee,
            f"Your {cert.certification} expires on {cert.expiry_date}")
        notify_manager(cert.employee.reports_to,
            f"{cert.employee} {cert.certification} expires on {cert.expiry_date}")
```

### Data Model

```
Shift Template
├── name: "Morning Shift"
├── start_time: "07:00"
├── end_time: "15:00"
├── break_duration: 30 (minutes)
├── roles: ["Field Technician", "Dispatcher"]
└── default_location: "Main Office"

Schedule Entry
├── employee (Link → Employee)
├── shift_template (Link → Shift Template)
├── date (Date)
├── actual_start_time (Time) [optional override]
├── actual_end_time (Time) [optional override]
├── location (Link → Location)
├── status (Draft/Published/Confirmed/Completed)
├── swap_status (None/Requested/Offered/Approved)
└── synced_to_hr (Check) [synced to Frappe HR]

Shift Swap Request
├── requesting_employee (Link → Employee)
├── original_schedule (Link → Schedule Entry)
├── status (Open/Offered/Accepted/Rejected/Cancelled)
├── offered_by (Link → Employee)
├── approved_by (Link → User)
└── approved_at (Datetime)

Employee Certification
├── employee (Link → Employee)
├── certification (Link → Certification Type)
├── issue_date (Date)
├── expiry_date (Date)
├── certificate_number (Data)
├── document (Attach)
└── status (Active/Expired/Revoked)
```

---

## HR-02: Mobile Clock-In + Geo-Fencing

### Description

Trust-verified attendance system with multiple validation methods.

### User Stories

- As a field worker, I want to clock in from job sites
- As a manager, I want proof that workers are where they say they are
- As payroll, I want accurate hours without disputes

### Functional Requirements

| ID       | Requirement                                       | Priority |
| -------- | ------------------------------------------------- | -------- |
| HR-02-01 | Clock in/out from mobile app                      | Must     |
| HR-02-02 | GPS location capture at clock-in                  | Must     |
| HR-02-03 | Geofence validation (must be within defined area) | Must     |
| HR-02-04 | Alternative: WiFi network validation              | Should   |
| HR-02-05 | Alternative: Selfie verification                  | Should   |
| HR-02-06 | Alternative: QR code scan at location             | Should   |
| HR-02-07 | Offline clock-in with buffered upload             | Must     |
| HR-02-08 | Break tracking (start/end break)                  | Should   |
| HR-02-09 | Project/job code selection at clock-in            | Should   |
| HR-02-10 | Auto clock-out reminder                           | Should   |
| HR-02-11 | Manager override for missed punches               | Must     |
| HR-02-12 | Sync to Frappe HR Attendance DocType              | Must     |
| HR-02-13 | Timesheet generation from clock data              | Should   |
| HR-02-14 | Anomaly detection (long shifts, unusual times)    | Should   |
| HR-02-15 | Clock-in from desktop (for office workers)        | Should   |

### Geofence Configuration

```
Work Location: "Downtown Office"
├── address: "123 Main St, City, ST 12345"
├── coordinates:
│   ├── latitude: 29.7604
│   └── longitude: -95.3698
├── geofence_radius: 100 (meters)
├── allowed_wifi_networks: ["OfficeWiFi", "OfficeGuest"]
├── qr_code: "LOC-DOWNTOWN-001"
└── validation_mode: "any" (gps OR wifi OR qr)

Work Location: "Client Site - ABC Corp"
├── address: "456 Corporate Blvd"
├── coordinates: {...}
├── geofence_radius: 200 (meters)
├── validation_mode: "gps_required"
└── linked_customer: "ABC Corporation"
```

### Clock-In Flow

```
Employee opens mobile app
        │
        ▼
┌───────────────┐
│ Tap "Clock In"│
└───────┬───────┘
        │
┌───────▼───────┐
│ Get GPS       │ ← Request location permission
│ Location      │
└───────┬───────┘
        │
┌───────▼───────────────────────────────────────┐
│ Validate Location                              │
│                                                │
│ Option A: Inside geofence?                     │
│   ✓ Within 100m of "Downtown Office"           │
│                                                │
│ Option B: Connected to known WiFi?             │
│   ✓ Connected to "OfficeWiFi"                  │
│                                                │
│ Option C: QR Code Scanned?                     │
│   ✓ Scanned "LOC-DOWNTOWN-001"                 │
└───────┬───────────────────────────────────────┘
        │
        ├── Validation PASSED
        │           │
        │   ┌───────▼───────┐
        │   │ Select Job    │ (optional)
        │   │ Code / Project│
        │   └───────┬───────┘
        │           │
        │   ┌───────▼───────┐
        │   │ Record        │ → Create Attendance record
        │   │ Clock-In      │ → Status: "Present"
        │   └───────────────┘
        │
        └── Validation FAILED
                    │
            ┌───────▼───────┐
            │ Show Error    │ "You appear to be outside
            │               │  the allowed work area."
            │               │
            │ [Try Again]   │ [Request Override]
            └───────────────┘
```

### Offline Handling

```
┌─────────────────────────────────────────────────────────────┐
│                    OFFLINE CLOCK-IN                          │
└─────────────────────────────────────────────────────────────┘

1. Employee clocks in while offline
   ├── GPS captured (if available)
   ├── Timestamp recorded
   └── Stored in local SQLite

2. App shows "Pending Sync" badge

3. When connectivity restored:
   ├── Upload all buffered records
   ├── Server validates each:
   │   ├── GPS within geofence? → Approved
   │   └── GPS outside/missing? → Flagged for review
   └── Mark as synced

4. Flagged records:
   ├── Notify manager
   └── Require approval/rejection
```

### Data Model

```
Attendance Entry (extends Frappe Attendance)
├── employee (Link → Employee)
├── attendance_date (Date)
├── status (Present/Absent/Half Day/On Leave)
├── in_time (Time)
├── out_time (Time)
├── working_hours (Float)
│
├── # Dartwing Extensions
├── clock_in_location (Geolocation)
├── clock_out_location (Geolocation)
├── validation_method (GPS/WiFi/QR/Manual)
├── validation_status (Verified/Flagged/Overridden)
├── work_location (Link → Work Location)
├── job_code (Link → Project/Job)
├── clock_in_photo (Attach) [selfie]
├── offline_entry (Check)
├── synced_at (Datetime)
└── breaks (Table → Break Entry)
    ├── start_time (Time)
    ├── end_time (Time)
    └── duration_minutes (Int)
```

### Anomaly Detection Rules

```python
ANOMALY_RULES = [
    {
        "name": "Long Shift",
        "condition": "working_hours > 12",
        "action": "flag_for_review",
        "alert": "manager"
    },
    {
        "name": "Early Clock-In",
        "condition": "clock_in_time < shift_start - 30min",
        "action": "flag_for_review",
        "alert": "manager"
    },
    {
        "name": "Missed Clock-Out",
        "condition": "clock_out_time IS NULL AND now() > shift_end + 2hr",
        "action": "auto_clock_out",
        "alert": "employee"
    },
    {
        "name": "Location Mismatch",
        "condition": "clock_in_location != scheduled_location",
        "action": "flag_for_review",
        "alert": "manager"
    },
    {
        "name": "Weekend Clock-In",
        "condition": "day_of_week IN (SAT, SUN) AND NOT scheduled",
        "action": "flag_for_review",
        "alert": "manager"
    }
]
```

### Mobile UI Wireframe

```
┌─────────────────────────────────────────┐
│ ◀  Clock In                         ⚙️  │
├─────────────────────────────────────────┤
│                                         │
│              Good Morning,              │
│               Carlos!                   │
│                                         │
│         📍 Downtown Office              │
│         ✓ Location Verified             │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │       ┌─────────────────┐        │  │
│  │       │                 │        │  │
│  │       │    CLOCK IN     │        │  │
│  │       │                 │        │  │
│  │       │     7:58 AM     │        │  │
│  │       │                 │        │  │
│  │       └─────────────────┘        │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Select Job (optional):                 │
│  ┌───────────────────────────────────┐  │
│  │ JOB-2025-1234: ABC Corp Install ▼ │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Today's Schedule:                      │
│  7:00 AM - 3:00 PM                      │
│  Field Technician                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## HR Feature Summary

| Feature                   | Input                                  | Processing                                              | Output (Frappe HR)    |
| ------------------------- | -------------------------------------- | ------------------------------------------------------- | --------------------- |
| **HR-01** Shift Scheduler | Shift templates, Employee availability | Schedule builder, Swap marketplace, Qualification check | Shift Assignment      |
| **HR-02** Geo Clock-In    | GPS, WiFi, QR, Selfie                  | Location validation, Offline buffer, Anomaly detection  | Attendance, Timesheet |

---

**Next: Section 6 - LeadGen Integration**

# Dartwing Company PRD - Section 6: LeadGen Integration

_"The Muscle. A standalone utility module usable by Company, HOA, or Family apps."_

**Note:** `dartwing_leadgen` is a SEPARATE Frappe app. This section documents the interface between `dartwing_company` and `dartwing_leadgen`.

---

## 6.1 Module Separation Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE RESPONSIBILITIES                       │
└─────────────────────────────────────────────────────────────────┘

dartwing_company (THE BRAIN)               dartwing_leadgen (THE MUSCLE)
────────────────────────────               ──────────────────────────────
• Knows the business context              • Has NO business context
• Understands "We sell HVAC services"     • Only knows "Find entities matching X"
• Defines WHO we're looking for           • Executes the search
• Decides WHAT to do with results         • Returns raw results
• Creates Leads in CRM                    • Has no idea what a "Lead" is
• Tracks campaigns and ROI                • Tracks API credits and quotas

ANALOGY:
dartwing_company = Marketing Director     dartwing_leadgen = Research Assistant
"Find me companies that fit              "Here are 500 companies matching
 our ideal customer profile"              those search parameters"
```

---

## 6.2 dartwing_leadgen Features (Reference)

### GEN-01: Universal Search & Scraper

**Purpose:** Execute searches across multiple data sources.

**Sources:**

- LinkedIn (via RapidAPI/Phantombuster)
- Google Maps / Places API
- Standard business directories (D&B, ZoomInfo API)
- Company websites (scraping)
- Government registries (SOS filings)

**Input:** `Search_Job` JSON
**Output:** List of raw entity records

### GEN-02: Data Enrichment API

**Purpose:** Find and validate contact information.

**Capabilities:**

- Email discovery (Hunter, Clearbit, etc.)
- Phone number lookup
- LinkedIn profile matching
- Company data enrichment (revenue, employees, tech stack)
- Email deliverability validation (SMTP ping)

**Input:** Entity with company/name
**Output:** Enriched entity with emails, phones, metadata

### GEN-03: Profile Matcher

**Purpose:** Score and filter results against criteria.

**Modes:**

- **Company Mode:** Match against Ideal Customer Profile (ICP)
- **HOA Mode:** Match against vendor requirements
- **Family Mode:** Match against review sentiment

**Input:** Enriched entities + matching criteria
**Output:** Scored and filtered entities

---

## 6.3 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

dartwing_company                                        dartwing_leadgen
================                                        ================

┌──────────────────────┐
│ Growth Orchestrator  │
│ (CRM-07)             │
│                      │
│ 1. AI Interview      │
│ 2. Build ICP         │
│ 3. Create Campaign   │
└──────────┬───────────┘
           │
           │ Search_Job JSON
           │
           ▼
┌──────────────────────┐         ┌──────────────────────┐
│ LeadGen Client       │────────▶│ LeadGen API          │
│ (API wrapper)        │         │                      │
└──────────────────────┘         └──────────┬───────────┘
                                            │
                                 ┌──────────▼───────────┐
                                 │ GEN-01: Search       │
                                 │ • LinkedIn           │
                                 │ • Google Maps        │
                                 │ • Directories        │
                                 └──────────┬───────────┘
                                            │
                                 ┌──────────▼───────────┐
                                 │ GEN-02: Enrich       │
                                 │ • Find emails        │
                                 │ • Verify contacts    │
                                 └──────────┬───────────┘
                                            │
                                 ┌──────────▼───────────┐
                                 │ GEN-03: Match        │
                                 │ • Score vs ICP       │
                                 │ • Filter             │
                                 └──────────┬───────────┘
                                            │
           ┌────────────────────────────────┘
           │ Qualified Results
           │
           ▼
┌──────────────────────┐
│ Lead Creator         │
│                      │
│ • Map to Lead fields │
│ • Link to Campaign   │
│ • Set source/score   │
│ • Deduplicate        │
│ • Create in CRM      │
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│ Frappe CRM           │
│ Lead DocType         │
│ Deal Pipeline        │
└──────────────────────┘
```

---

## 6.4 API Interface Definition

### Search Job Request

```python
# dartwing_company/integrations/leadgen_client.py

class LeadGenClient:
    """Client for interacting with dartwing_leadgen module"""

    def __init__(self, organization: str):
        self.organization = organization
        self.api_base = frappe.conf.get("leadgen_api_url", "/api/method/dartwing_leadgen")

    def create_search_job(self, job: SearchJob) -> str:
        """
        Submit a search job to dartwing_leadgen.

        Returns: job_id for tracking
        """
        response = frappe.call(
            f"{self.api_base}.api.search.create_job",
            job=job.to_dict()
        )
        return response.get("job_id")

    def get_job_status(self, job_id: str) -> JobStatus:
        """Check status of a search job"""
        response = frappe.call(
            f"{self.api_base}.api.search.get_status",
            job_id=job_id
        )
        return JobStatus.from_dict(response)

    def get_results(self, job_id: str) -> list[Entity]:
        """Retrieve results from completed job"""
        response = frappe.call(
            f"{self.api_base}.api.search.get_results",
            job_id=job_id
        )
        return [Entity.from_dict(e) for e in response.get("results", [])]
```

### Search Job Schema

```python
@dataclass
class SearchJob:
    """Search job definition sent to dartwing_leadgen"""

    # Requestor info
    organization: str
    campaign_id: str
    callback_url: str = None

    # Search parameters
    keywords: list[str] = field(default_factory=list)
    industries: list[str] = field(default_factory=list)

    # Company criteria
    company_size: CompanySize = None
    technologies: list[str] = field(default_factory=list)

    # Geographic
    countries: list[str] = field(default_factory=list)
    states: list[str] = field(default_factory=list)
    cities: list[str] = field(default_factory=list)
    radius_miles: int = None

    # Personas
    titles: list[str] = field(default_factory=list)
    departments: list[str] = field(default_factory=list)
    seniority_levels: list[str] = field(default_factory=list)

    # Limits
    max_results: int = 500
    budget_usd: float = None

    # Enrichment options
    find_emails: bool = True
    find_phones: bool = False
    verify_emails: bool = True

    # Scoring criteria (for GEN-03)
    icp_criteria: dict = field(default_factory=dict)
    minimum_score: int = 0

@dataclass
class CompanySize:
    employees_min: int = None
    employees_max: int = None
    revenue_min: int = None
    revenue_max: int = None
```

### Entity Result Schema

```python
@dataclass
class Entity:
    """Entity returned from dartwing_leadgen"""

    entity_id: str
    entity_type: str  # "company" or "person"

    # Company info
    company_name: str = None
    company_domain: str = None
    company_linkedin: str = None
    industry: str = None
    employee_count: int = None
    estimated_revenue: int = None
    technologies: list[str] = field(default_factory=list)

    # Location
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    coordinates: tuple = None

    # Person info (if entity_type == "person")
    first_name: str = None
    last_name: str = None
    title: str = None
    department: str = None
    seniority: str = None
    linkedin_url: str = None

    # Contact info (from GEN-02)
    emails: list[EmailContact] = field(default_factory=list)
    phones: list[PhoneContact] = field(default_factory=list)

    # Scoring (from GEN-03)
    icp_score: int = 0
    score_breakdown: dict = field(default_factory=dict)

    # Metadata
    source: str = None  # "linkedin", "google_maps", etc.
    confidence: float = 0.0
    last_updated: str = None

@dataclass
class EmailContact:
    email: str
    type: str  # "work", "personal"
    confidence: float
    verified: bool = False
    verification_status: str = None  # "valid", "invalid", "unknown"

@dataclass
class PhoneContact:
    phone: str
    type: str  # "direct", "mobile", "office"
    confidence: float
```

---

## 6.5 Lead Creation Flow

```python
# dartwing_company/crm/lead_creator.py

class LeadCreator:
    """Creates Frappe CRM Leads from LeadGen results"""

    def __init__(self, organization: str, campaign: str):
        self.organization = organization
        self.campaign = campaign

    def create_leads(self, entities: list[Entity]) -> CreationResult:
        """
        Create Leads from entity list.

        Returns: Summary of created, skipped, errors
        """
        results = CreationResult()

        for entity in entities:
            try:
                # Check for duplicates
                existing = self._find_duplicate(entity)
                if existing:
                    results.skipped.append({
                        "entity": entity.entity_id,
                        "reason": "duplicate",
                        "existing_lead": existing
                    })
                    continue

                # Create Lead
                lead = self._create_lead(entity)
                results.created.append(lead.name)

            except Exception as e:
                results.errors.append({
                    "entity": entity.entity_id,
                    "error": str(e)
                })

        return results

    def _find_duplicate(self, entity: Entity) -> str | None:
        """Check if Lead already exists"""
        # Check by email
        for email in entity.emails:
            existing = frappe.db.get_value("Lead",
                {"email_id": email.email}, "name")
            if existing:
                return existing

        # Check by company + name
        if entity.company_name and entity.first_name:
            existing = frappe.db.get_value("Lead", {
                "company_name": entity.company_name,
                "first_name": entity.first_name,
                "last_name": entity.last_name
            }, "name")
            if existing:
                return existing

        return None

    def _create_lead(self, entity: Entity) -> "Lead":
        """Map entity to Frappe CRM Lead"""

        # Get primary email
        primary_email = None
        if entity.emails:
            verified = [e for e in entity.emails if e.verified]
            primary_email = verified[0].email if verified else entity.emails[0].email

        # Get primary phone
        primary_phone = None
        if entity.phones:
            direct = [p for p in entity.phones if p.type == "direct"]
            primary_phone = direct[0].phone if direct else entity.phones[0].phone

        lead = frappe.get_doc({
            "doctype": "Lead",

            # Standard fields
            "first_name": entity.first_name,
            "last_name": entity.last_name,
            "email_id": primary_email,
            "mobile_no": primary_phone,
            "company_name": entity.company_name,
            "job_title": entity.title,
            "website": entity.company_domain,
            "industry": entity.industry,
            "city": entity.city,
            "state": entity.state,
            "country": entity.country,

            # Source tracking
            "source": "Growth Orchestrator",
            "campaign_name": self.campaign,

            # Custom fields (via CRM-05)
            "custom_data": {
                "leadgen_entity_id": entity.entity_id,
                "leadgen_source": entity.source,
                "icp_score": entity.icp_score,
                "score_breakdown": entity.score_breakdown,
                "employee_count": entity.employee_count,
                "estimated_revenue": entity.estimated_revenue,
                "technologies": entity.technologies,
                "linkedin_url": entity.linkedin_url,
                "all_emails": [e.__dict__ for e in entity.emails],
                "all_phones": [p.__dict__ for p in entity.phones]
            },

            # Workflow
            "status": "New",
            "lead_owner": self._get_lead_owner()
        })

        lead.insert(ignore_permissions=True)

        # Create Lead Activity
        frappe.get_doc({
            "doctype": "CRM Activity",
            "lead": lead.name,
            "activity_type": "System",
            "notes": f"Lead created from Growth Orchestrator campaign: {self.campaign}"
        }).insert(ignore_permissions=True)

        return lead
```

---

## 6.6 Campaign Tracking

```
Campaign DocType (dartwing_company)
├── campaign_name: "Q4 2025 Enterprise HVAC"
├── organization (Link → Organization)
├── status (Draft/Active/Paused/Completed)
│
├── # Search Configuration (becomes Search_Job)
├── target_industries (Table MultiSelect)
├── target_company_size (JSON)
├── target_geographies (Table MultiSelect)
├── target_personas (Table → Campaign Persona)
├── icp_criteria (JSON)
│
├── # LeadGen Execution
├── search_job_id (Data) [from dartwing_leadgen]
├── job_status (Data)
├── last_sync (Datetime)
│
├── # Results Summary
├── entities_found (Int)
├── entities_enriched (Int)
├── entities_matched (Int)
├── leads_created (Int)
├── leads_converted (Int)
├── deals_won (Int)
│
├── # Budget
├── budget_usd (Currency)
├── spent_usd (Currency)
│
├── # Performance Metrics
├── cost_per_lead (Currency) [calculated]
├── conversion_rate (Percent) [calculated]
└── roi (Percent) [calculated]
```

---

## 6.7 Webhook Callbacks

`dartwing_leadgen` can send webhook notifications to `dartwing_company`:

```python
# Webhook events from dartwing_leadgen
LEADGEN_EVENTS = {
    "job.started": "Search job execution started",
    "job.progress": "Search job progress update",
    "job.completed": "Search job completed",
    "job.failed": "Search job failed",
    "enrichment.completed": "Enrichment batch completed",
    "credits.low": "API credits running low"
}

# dartwing_company/api/webhooks/leadgen.py
@frappe.whitelist(allow_guest=True)
def handle_leadgen_webhook():
    """Handle webhooks from dartwing_leadgen"""
    payload = frappe.request.get_json()

    # Validate signature
    signature = frappe.request.headers.get("X-LeadGen-Signature")
    if not validate_signature(payload, signature):
        frappe.throw("Invalid signature", frappe.AuthenticationError)

    event = payload.get("event")

    if event == "job.completed":
        handle_job_completed(payload)
    elif event == "job.failed":
        handle_job_failed(payload)
    elif event == "credits.low":
        handle_credits_low(payload)

    return {"status": "ok"}

def handle_job_completed(payload):
    """Process completed search job"""
    job_id = payload["job_id"]

    # Find campaign
    campaign = frappe.get_value("Campaign", {"search_job_id": job_id}, "name")
    if not campaign:
        return

    # Fetch results
    client = LeadGenClient(frappe.get_value("Campaign", campaign, "organization"))
    results = client.get_results(job_id)

    # Create leads
    creator = LeadCreator(
        organization=campaign.organization,
        campaign=campaign
    )
    creation_result = creator.create_leads(results)

    # Update campaign stats
    campaign_doc = frappe.get_doc("Campaign", campaign)
    campaign_doc.entities_found = payload.get("total_found", 0)
    campaign_doc.entities_matched = len(results)
    campaign_doc.leads_created += len(creation_result.created)
    campaign_doc.job_status = "Completed"
    campaign_doc.last_sync = now()
    campaign_doc.save()

    # Notify campaign owner
    notify(
        campaign_doc.owner,
        f"Campaign '{campaign_doc.campaign_name}' completed",
        f"{len(creation_result.created)} new leads created"
    )
```

---

## 6.8 Usage Scenarios

### Scenario 1: Company Lead Generation

```
dartwing_company user → Growth Orchestrator
├── "I sell commercial HVAC services in Texas"
├── Target: Facilities Managers at companies 50-500 employees
└── Generates Search_Job → dartwing_leadgen
    └── Returns: 350 qualified leads → Creates in Frappe CRM
```

### Scenario 2: HOA Vendor Search (future)

```
dartwing_hoa user → Vendor Finder
├── "I need a licensed landscaper in Miami"
├── Target: Landscaping companies with 4+ star reviews
└── Generates Search_Job → dartwing_leadgen
    └── Returns: 25 qualified vendors → Creates Vendor proposals
```

### Scenario 3: Family Service Search (future)

```
dartwing_family user → Service Finder
├── "I need a math tutor for my high schooler"
├── Target: Tutors with calculus experience and good reviews
└── Generates Search_Job → dartwing_leadgen
    └── Returns: 10 qualified tutors → Shows comparison view
```

---

**Next: Section 7 - Technical Architecture**

# Dartwing Company PRD - Section 7: Technical Architecture

---

## 7.1 Module Structure

```
apps/dartwing/dartwing/dartwing_company/
│
├── __init__.py
├── hooks.py
├── patches/
│
├── doctype/                          # Frappe DocTypes
│   ├── # Operations Core
│   ├── conversation/
│   ├── conversation_message/
│   ├── workflow_template/
│   ├── workflow_instance/
│   ├── task_template/
│   ├── dispatch_job/
│   ├── mobile_form/
│   ├── form_submission/
│   ├── knowledge_article/
│   ├── broadcast_alert/
│   ├── visitor_log/
│   ├── resource_booking/
│   │
│   ├── # CRM Overlay
│   ├── client_portal_settings/
│   ├── view_set/
│   ├── document_vault/
│   ├── appointment_type/
│   ├── appointment/
│   ├── service_ticket/
│   ├── sla_policy/
│   ├── custom_field_schema/
│   ├── campaign/
│   │
│   ├── # HR Overlay
│   ├── shift_template/
│   ├── schedule_entry/
│   ├── shift_swap_request/
│   ├── work_location/
│   └── attendance_extension/
│
├── operations/                       # OPS Feature Engines
│   ├── __init__.py
│   ├── receptionist/
│   │   ├── call_handler.py
│   │   ├── intent_classifier.py
│   │   └── router.py
│   ├── inbox/
│   │   ├── aggregator.py
│   │   ├── channels/
│   │   │   ├── email.py
│   │   │   ├── sms.py
│   │   │   ├── voice.py
│   │   │   └── whatsapp.py
│   │   └── session_manager.py
│   ├── workflow/
│   │   ├── engine.py
│   │   ├── builder.py
│   │   └── external_sync.py
│   ├── dispatch/
│   │   ├── engine.py
│   │   ├── geo_service.py
│   │   └── optimizer.py
│   ├── forms/
│   │   ├── builder.py
│   │   ├── offline_sync.py
│   │   └── validator.py
│   ├── knowledge/
│   │   ├── rag_engine.py
│   │   ├── indexer.py
│   │   └── embeddings.py
│   └── search/
│       └── global_search.py
│
├── crm/                              # CRM Feature Engines
│   ├── __init__.py
│   ├── portal/
│   │   ├── views.py
│   │   ├── widgets.py
│   │   └── auth.py
│   ├── appointments/
│   │   ├── scheduler.py
│   │   ├── availability.py
│   │   └── payments.py
│   ├── tickets/
│   │   ├── router.py
│   │   ├── sentiment.py
│   │   └── sla_engine.py
│   └── growth/
│       ├── orchestrator.py
│       ├── interview_agent.py
│       └── lead_creator.py
│
├── hr/                               # HR Feature Engines
│   ├── __init__.py
│   ├── scheduling/
│   │   ├── builder.py
│   │   ├── swap_marketplace.py
│   │   └── qualifications.py
│   └── attendance/
│       ├── clock_manager.py
│       ├── geofence.py
│       └── anomaly_detector.py
│
├── integrations/                     # External Integrations
│   ├── __init__.py
│   ├── leadgen_client.py            # dartwing_leadgen
│   ├── fone_client.py               # dartwing_fone
│   ├── calendar/
│   │   ├── google.py
│   │   └── outlook.py
│   ├── task_sync/
│   │   ├── planner.py
│   │   └── trello.py
│   └── payments/
│       └── stripe.py
│
├── api/                              # REST APIs
│   ├── v1/
│   │   ├── conversations.py
│   │   ├── tasks.py
│   │   ├── dispatch.py
│   │   ├── forms.py
│   │   ├── appointments.py
│   │   ├── tickets.py
│   │   ├── campaigns.py
│   │   ├── schedule.py
│   │   └── attendance.py
│   └── webhooks/
│       ├── fone.py
│       ├── leadgen.py
│       └── channels.py
│
├── portal/                           # Client Portal
│   ├── www/
│   │   ├── portal/
│   │   │   ├── index.html
│   │   │   ├── dashboard.html
│   │   │   ├── invoices.html
│   │   │   ├── projects.html
│   │   │   ├── documents.html
│   │   │   ├── tickets.html
│   │   │   └── appointments.html
│   │   └── portal.py
│   ├── templates/
│   └── api.py
│
├── mobile/                           # Mobile-specific
│   ├── api_schema.py
│   ├── push_notifications.py
│   └── offline_sync.py
│
├── tasks/                            # Background Jobs
│   ├── inbox_sync.py
│   ├── sla_monitor.py
│   ├── standup_generator.py
│   ├── schedule_publisher.py
│   └── attendance_anomalies.py
│
└── tests/
```

---

## 7.2 DocType Summary

### Operations DocTypes

| DocType                  | Purpose                      | Parent       |
| ------------------------ | ---------------------------- | ------------ |
| **Conversation**         | Unified message thread       | -            |
| **Conversation Message** | Individual message           | Conversation |
| **Workflow Template**    | Reusable workflow definition | -            |
| **Workflow Instance**    | Running workflow             | -            |
| **Task Template**        | Task type definition         | -            |
| **Dispatch Job**         | Field job assignment         | -            |
| **Mobile Form**          | Form schema definition       | -            |
| **Form Submission**      | Completed form data          | Mobile Form  |
| **Knowledge Article**    | Wiki/SOP content             | -            |
| **Broadcast Alert**      | Mass notification record     | -            |
| **Visitor Log**          | Guest check-in record        | -            |
| **Resource**             | Bookable asset               | -            |
| **Resource Booking**     | Reservation record           | Resource     |

### CRM Overlay DocTypes

| DocType                    | Purpose                                | Overlays        |
| -------------------------- | -------------------------------------- | --------------- |
| **Client Portal Settings** | Portal configuration                   | -               |
| **View Set**               | Widget configuration per customer type | -               |
| **Document Vault**         | Secure file container                  | Customer        |
| **Appointment Type**       | Appointment configuration              | -               |
| **Appointment**            | Scheduled meeting                      | Contact         |
| **Service Ticket**         | Support ticket                         | Issue (ERPNext) |
| **SLA Policy**             | Response time rules                    | -               |
| **Custom Field Schema**    | Dynamic fields definition              | -               |
| **Campaign**               | Lead gen campaign                      | Frappe CRM      |

### HR Overlay DocTypes

| DocType                  | Purpose                        | Syncs To         |
| ------------------------ | ------------------------------ | ---------------- |
| **Shift Template**       | Shift definition               | -                |
| **Schedule Entry**       | Individual schedule assignment | Shift Assignment |
| **Shift Swap Request**   | Swap marketplace               | -                |
| **Work Location**        | Location with geofence         | -                |
| **Attendance Extension** | Extra attendance data          | Attendance       |

---

## 7.3 Key DocType Schemas

### Conversation

```
Conversation
├── name (autoname: CONV-.YYYY.-.#####)
├── organization (Link → Organization)
├── contact (Link → Contact)
├── lead (Link → Lead)
├── customer (Link → Customer)
│
├── channel (Select: email/sms/voice/whatsapp/messenger/telegram)
├── status (Select: open/pending/resolved/closed)
├── priority (Select: low/normal/high/urgent)
│
├── assigned_to (Link → User)
├── assigned_team (Link → User Group)
│
├── subject (Data)
├── last_message_at (Datetime)
├── last_message_preview (Small Text)
├── unread_count (Int)
├── sentiment_score (Float: -1 to 1)
│
├── messages (Table → Conversation Message)
│   ├── direction (Select: in/out)
│   ├── channel (Select)
│   ├── content (Long Text)
│   ├── content_html (Long Text)
│   ├── timestamp (Datetime)
│   ├── sender_name (Data)
│   ├── sender_id (Data)
│   ├── channel_message_id (Data)
│   ├── attachments (Table → Message Attachment)
│   └── ai_summary (Text)
│
└── internal_notes (Table → Conversation Note)
    ├── user (Link → User)
    ├── note (Long Text)
    └── timestamp (Datetime)
```

### Dispatch Job

```
Dispatch Job
├── name (autoname: JOB-.YYYY.-.#####)
├── organization (Link → Organization)
│
├── # Source
├── linked_doctype (Data)
├── linked_name (Dynamic Link)
├── customer (Link → Customer)
│
├── # Location
├── address (Link → Address)
├── latitude (Float)
├── longitude (Float)
├── geohash (Data) [for spatial queries]
│
├── # Assignment
├── status (Select: unassigned/assigned/en_route/arrived/in_progress/completed/cancelled)
├── assigned_to (Link → Employee)
├── assigned_at (Datetime)
├── assignment_method (Select: manual/auto_nearest/auto_workload)
│
├── # Timing
├── scheduled_date (Date)
├── scheduled_start (Time)
├── scheduled_end (Time)
├── preferred_window (Select: morning/afternoon/evening/any)
├── actual_arrival (Datetime)
├── actual_departure (Datetime)
│
├── # Requirements
├── required_skills (Table MultiSelect → Skill)
├── estimated_duration (Duration)
├── priority (Select: low/normal/high/urgent)
│
├── # Execution
├── technician_notes (Long Text)
├── customer_signature (Signature)
├── photos (Table → Job Photo)
└── form_submissions (Table → Form Submission Link)
```

### Campaign (Growth Orchestrator)

```
Campaign
├── name (autoname: CAMP-.YYYY.-.#####)
├── campaign_name (Data)
├── organization (Link → Organization)
├── owner (Link → User)
├── status (Select: draft/active/paused/completed)
│
├── # ICP Definition
├── target_industries (Table MultiSelect → Industry)
├── company_size_min (Int)
├── company_size_max (Int)
├── revenue_min (Currency)
├── revenue_max (Currency)
├── target_technologies (Table MultiSelect)
│
├── # Geographic
├── target_countries (Table MultiSelect → Country)
├── target_states (Table MultiSelect)
├── target_cities (Table MultiSelect)
├── radius_miles (Int)
│
├── # Personas
├── personas (Table → Campaign Persona)
│   ├── title (Data)
│   ├── department (Data)
│   └── seniority (Select)
│
├── # LeadGen Integration
├── search_job_id (Data) [from dartwing_leadgen]
├── job_status (Select: pending/running/completed/failed)
├── last_sync (Datetime)
│
├── # Results
├── entities_found (Int)
├── entities_enriched (Int)
├── entities_matched (Int)
├── leads_created (Int)
├── leads_contacted (Int)
├── leads_qualified (Int)
├── deals_created (Int)
├── deals_won (Int)
├── revenue_generated (Currency)
│
├── # Budget
├── budget (Currency)
├── spent (Currency)
│
└── # Calculated
├── cost_per_lead (Currency)
├── conversion_rate (Percent)
└── roi (Percent)
```

---

## 7.4 API Endpoints

### Conversations API

| Endpoint                              | Method | Purpose             |
| ------------------------------------- | ------ | ------------------- |
| `/api/v1/conversations`               | GET    | List conversations  |
| `/api/v1/conversations`               | POST   | Create conversation |
| `/api/v1/conversations/{id}`          | GET    | Get conversation    |
| `/api/v1/conversations/{id}/messages` | GET    | Get messages        |
| `/api/v1/conversations/{id}/messages` | POST   | Send message        |
| `/api/v1/conversations/{id}/assign`   | POST   | Assign to user/team |
| `/api/v1/conversations/{id}/resolve`  | POST   | Mark resolved       |

### Dispatch API

| Endpoint                            | Method | Purpose                    |
| ----------------------------------- | ------ | -------------------------- |
| `/api/v1/dispatch/jobs`             | GET    | List jobs                  |
| `/api/v1/dispatch/jobs`             | POST   | Create job                 |
| `/api/v1/dispatch/jobs/{id}/assign` | POST   | Assign to technician       |
| `/api/v1/dispatch/jobs/{id}/status` | PUT    | Update status              |
| `/api/v1/dispatch/optimize`         | POST   | Get optimized routes       |
| `/api/v1/dispatch/technicians`      | GET    | List available technicians |
| `/api/v1/dispatch/map`              | GET    | Map data (jobs + techs)    |

### Appointments API

| Endpoint                               | Method | Purpose                |
| -------------------------------------- | ------ | ---------------------- |
| `/api/v1/appointments/types`           | GET    | List appointment types |
| `/api/v1/appointments/availability`    | GET    | Get available slots    |
| `/api/v1/appointments`                 | POST   | Book appointment       |
| `/api/v1/appointments/{id}`            | GET    | Get appointment        |
| `/api/v1/appointments/{id}/reschedule` | POST   | Reschedule             |
| `/api/v1/appointments/{id}/cancel`     | POST   | Cancel                 |

### Campaigns API

| Endpoint                         | Method | Purpose          |
| -------------------------------- | ------ | ---------------- |
| `/api/v1/campaigns`              | GET    | List campaigns   |
| `/api/v1/campaigns`              | POST   | Create campaign  |
| `/api/v1/campaigns/{id}`         | GET    | Get campaign     |
| `/api/v1/campaigns/{id}/launch`  | POST   | Launch search    |
| `/api/v1/campaigns/{id}/pause`   | POST   | Pause campaign   |
| `/api/v1/campaigns/{id}/results` | GET    | Get lead results |

### Attendance API

| Endpoint                         | Method | Purpose        |
| -------------------------------- | ------ | -------------- |
| `/api/v1/attendance/clock-in`    | POST   | Clock in       |
| `/api/v1/attendance/clock-out`   | POST   | Clock out      |
| `/api/v1/attendance/break/start` | POST   | Start break    |
| `/api/v1/attendance/break/end`   | POST   | End break      |
| `/api/v1/attendance/status`      | GET    | Current status |
| `/api/v1/attendance/history`     | GET    | History        |

---

## 7.5 Background Jobs

```python
# hooks.py scheduler_events

scheduler_events = {
    "cron": {
        # Every minute
        "* * * * *": [
            "dartwing_company.tasks.inbox_sync.sync_channels",
            "dartwing_company.tasks.sla_monitor.check_sla"
        ],
        # Every 5 minutes
        "*/5 * * * *": [
            "dartwing_company.tasks.attendance_anomalies.detect"
        ],
        # Every hour
        "0 * * * *": [
            "dartwing_company.tasks.external_sync.sync_calendars",
            "dartwing_company.tasks.external_sync.sync_tasks"
        ],
        # Daily at 6 AM
        "0 6 * * *": [
            "dartwing_company.tasks.standup_generator.generate_all"
        ],
        # Daily at midnight
        "0 0 * * *": [
            "dartwing_company.tasks.schedule_publisher.publish_upcoming"
        ]
    }
}
```

---

## 7.6 Event Hooks

```python
# hooks.py doc_events

doc_events = {
    "Conversation": {
        "after_insert": "dartwing_company.events.conversation.on_create",
        "on_update": "dartwing_company.events.conversation.on_update"
    },
    "Service Ticket": {
        "after_insert": "dartwing_company.events.ticket.on_create",
        "on_update": "dartwing_company.events.ticket.check_sla"
    },
    "Dispatch Job": {
        "on_update": "dartwing_company.events.dispatch.on_status_change"
    },
    "Schedule Entry": {
        "after_insert": "dartwing_company.events.schedule.sync_to_hr",
        "on_update": "dartwing_company.events.schedule.sync_to_hr"
    },
    # Listen to Frappe CRM events
    "Lead": {
        "after_insert": "dartwing_company.events.crm.on_lead_create",
        "on_update": "dartwing_company.events.crm.on_lead_update"
    },
    "Deal": {
        "on_update": "dartwing_company.events.crm.on_deal_update"
    }
}
```

---

## 7.7 Technology Stack

| Component         | Technology            | Purpose                  |
| ----------------- | --------------------- | ------------------------ |
| **Framework**     | Frappe 16.x           | Application foundation   |
| **Database**      | MariaDB 10.11+        | Primary data store       |
| **Cache**         | Redis 7.x             | Caching, queues, pub/sub |
| **Search**        | OpenSearch 2.x        | Full-text, vector search |
| **Vector DB**     | pgvector / OpenSearch | RAG embeddings           |
| **Maps**          | Google Maps / Mapbox  | Geocoding, routing       |
| **Voice**         | dartwing_fone         | SIP, SMS, Voice AI       |
| **Payments**      | Stripe                | Appointment deposits     |
| **Calendar Sync** | Google/Outlook APIs   | Calendar integration     |
| **Task Sync**     | Planner/Trello APIs   | Task management          |
| **AI/LLM**        | OpenAI / Claude       | Intent, RAG, summaries   |
| **Mobile**        | Flutter               | Cross-platform app       |

---

**Next: Section 8 - Implementation Roadmap**

# Dartwing Company PRD - Section 8: Implementation Roadmap

---

## 8.1 Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION TIMELINE                               │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 1: Foundation         Phase 2: Automation        Phase 3: Intelligence
Months 1-3                  Months 4-6                 Months 7-9
─────────────────           ────────────────           ──────────────────
• Universal Inbox           • Workflow Engine          • AI Receptionist
• Basic Dispatch            • Smart Routing            • RAG Knowledge Base
• Mobile Forms              • SLA Engine               • Growth Orchestrator
• Client Portal             • Scheduling               • Daily Standup AI
• Geo Clock-In              • Shift Swap               • Sentiment Analysis

Phase 4: Scale & Polish
Months 10-12
────────────────────────
• External Integrations
• Advanced Analytics
• Mobile App Polish
• Performance Optimization
```

---

## 8.2 Phase 1: Foundation (Months 1-3)

### Goals

- Core communication and dispatch working
- Basic client portal live
- Mobile attendance functional
- Foundation for CRM overlay

### Deliverables

| ID         | Feature                 | Description                                       | Effort  |
| ---------- | ----------------------- | ------------------------------------------------- | ------- |
| **OPS-02** | Universal Inbox (Basic) | Email + SMS aggregation, manual routing           | 3 weeks |
| **OPS-04** | Dispatch (Basic)        | Map view, manual assignment, status tracking      | 3 weeks |
| **OPS-05** | Mobile Forms            | Form builder, offline submission, photo/signature | 3 weeks |
| **CRM-01** | Client Portal (Basic)   | Login, dashboard, invoices, documents             | 3 weeks |
| **CRM-04** | Service Tickets (Basic) | Create, assign, status, portal view               | 2 weeks |
| **HR-02**  | Geo Clock-In            | GPS validation, offline buffer, sync to HR        | 2 weeks |

### Technical Foundation

- Module scaffolding and DocTypes
- API structure
- Mobile API endpoints
- Basic portal routes
- Redis pub/sub for real-time

### Success Criteria

- [ ] Receive and respond to messages from email/SMS
- [ ] Create and assign dispatch jobs on map
- [ ] Submit forms from mobile with photos
- [ ] Client can log into portal and see invoices
- [ ] Employees can clock in with GPS validation
- [ ] 90% test coverage on core modules

---

## 8.3 Phase 2: Automation (Months 4-6)

### Goals

- Workflow automation live
- Smart dispatch routing
- SLA tracking active
- Shift scheduling functional

### Deliverables

| ID         | Feature            | Description                                                  | Effort  |
| ---------- | ------------------ | ------------------------------------------------------------ | ------- |
| **OPS-03** | Workflow Engine    | Visual builder, triggers, actions, conditions                | 4 weeks |
| **OPS-04** | Smart Dispatch     | Auto-suggest, drive-time calculation, skill matching         | 3 weeks |
| **OPS-06** | Status Boards      | Kanban, calendar views with drag-drop                        | 2 weeks |
| **CRM-03** | Appointment Booker | Availability, booking, reminders, payments                   | 3 weeks |
| **CRM-06** | SLA Engine         | Policy config, timers, escalation, reporting                 | 2 weeks |
| **HR-01**  | Shift Scheduler    | Templates, builder, swap marketplace, certification blocking | 4 weeks |

### Integrations

- Google/Outlook calendar sync
- Stripe for appointment payments
- External task sync (Planner/Trello)

### Success Criteria

- [ ] Create workflow that triggers on ticket creation
- [ ] Auto-assign job to nearest qualified technician
- [ ] Client books appointment through portal
- [ ] SLA breach triggers escalation automatically
- [ ] Employee requests and completes shift swap
- [ ] 85% of jobs auto-assigned within 30 seconds

---

## 8.4 Phase 3: Intelligence (Months 7-9)

### Goals

- AI features operational
- Lead generation pipeline working
- Voice automation live
- Knowledge base with RAG

### Deliverables

| ID         | Feature              | Description                                    | Effort  |
| ---------- | -------------------- | ---------------------------------------------- | ------- |
| **OPS-01** | AI Receptionist      | Intent classification, routing, whisper        | 4 weeks |
| **OPS-07** | Knowledge Base + RAG | Wiki, PDF indexing, AI Q&A                     | 4 weeks |
| **OPS-09** | Daily Standup AI     | Auto-generate summaries, flag issues           | 2 weeks |
| **OPS-12** | Ask Anything Bar     | Global search, slash commands, AI queries      | 2 weeks |
| **CRM-04** | Sentiment Analysis   | Ticket/message sentiment, auto-escalation      | 2 weeks |
| **CRM-07** | Growth Orchestrator  | AI interview, ICP builder, LeadGen integration | 4 weeks |

### AI/ML Components

- Intent classification model (fine-tuned)
- Embedding model for RAG
- Sentiment analysis model
- Integration with dartwing_leadgen

### Success Criteria

- [ ] AI answers phone and routes correctly 85% of time
- [ ] Ask knowledge base question, get cited answer
- [ ] Daily standup generated and delivered by 7 AM
- [ ] Growth Orchestrator creates 100+ leads from campaign
- [ ] Negative sentiment tickets auto-escalated
- [ ] Global search finds records in <500ms

---

## 8.5 Phase 4: Scale & Polish (Months 10-12)

### Goals

- Production-ready quality
- Full integration suite
- Mobile app polished
- Analytics and reporting

### Deliverables

| ID         | Feature             | Description                             | Effort  |
| ---------- | ------------------- | --------------------------------------- | ------- |
| **OPS-02** | Social Channels     | WhatsApp, Messenger, Instagram          | 3 weeks |
| **OPS-08** | Broadcast Alerts    | Multi-channel blast, acknowledgment     | 2 weeks |
| **OPS-10** | Visitor Management  | Kiosk mode, notifications, badges       | 2 weeks |
| **OPS-11** | Resource Booking    | Rooms, vehicles, equipment              | 2 weeks |
| **CRM-02** | Document Vault      | Advanced sharing, expiring links, audit | 2 weeks |
| **CRM-05** | Custom Fields       | Schema builder, search indexing         | 2 weeks |
| **--**     | Analytics Dashboard | Executive reporting, KPIs               | 3 weeks |
| **--**     | Mobile App Polish   | UX refinement, performance              | 4 weeks |

### Performance & Scale

- Query optimization
- Caching strategy
- Background job scaling
- Load testing

### Success Criteria

- [ ] WhatsApp messages appear in Universal Inbox
- [ ] Emergency broadcast reaches 100% in <2 minutes
- [ ] Visitor checks in and host notified in <30 seconds
- [ ] Custom fields searchable in global search
- [ ] Mobile app rating 4.5+ on app stores
- [ ] System handles 10,000 concurrent users

---

## 8.6 Feature Priority Matrix

| Feature             | Business Value | Technical Complexity | Phase |
| ------------------- | -------------- | -------------------- | ----- |
| Universal Inbox     | ●●●●●          | ●●●○○                | 1     |
| Dispatch Map        | ●●●●●          | ●●●○○                | 1     |
| Mobile Forms        | ●●●●○          | ●●○○○                | 1     |
| Client Portal       | ●●●●●          | ●●●○○                | 1     |
| Geo Clock-In        | ●●●●○          | ●●○○○                | 1     |
| Workflow Engine     | ●●●●●          | ●●●●○                | 2     |
| Smart Dispatch      | ●●●●○          | ●●●●○                | 2     |
| Appointment Booker  | ●●●●○          | ●●●○○                | 2     |
| SLA Engine          | ●●●●○          | ●●●○○                | 2     |
| Shift Scheduler     | ●●●○○          | ●●●●○                | 2     |
| AI Receptionist     | ●●●●○          | ●●●●●                | 3     |
| Knowledge Base RAG  | ●●●●○          | ●●●●○                | 3     |
| Growth Orchestrator | ●●●●●          | ●●●●●                | 3     |
| Daily Standup AI    | ●●●○○          | ●●●○○                | 3     |
| Social Channels     | ●●●○○          | ●●●○○                | 4     |
| Analytics Dashboard | ●●●●○          | ●●●○○                | 4     |

---

## 8.7 Team Structure

### Recommended Team

| Role                   | Count | Responsibilities                               |
| ---------------------- | ----- | ---------------------------------------------- |
| **Tech Lead**          | 1     | Architecture, code review, technical decisions |
| **Backend Developer**  | 2     | Frappe DocTypes, APIs, background jobs         |
| **Frontend Developer** | 1     | Portal, Frappe UI customization                |
| **Flutter Developer**  | 1     | Mobile app development                         |
| **AI/ML Engineer**     | 1     | RAG, intent classification, sentiment          |
| **QA Engineer**        | 1     | Testing, automation                            |
| **DevOps**             | 0.5   | Infrastructure, deployment                     |

### Phase Allocation

```
Phase 1 (Foundation):    Backend x2, Frontend x1, Flutter x1, QA x1
Phase 2 (Automation):    Backend x2, Frontend x1, Flutter x1, QA x1
Phase 3 (Intelligence):  Backend x1, AI/ML x1, Flutter x0.5, QA x1
Phase 4 (Scale):         Backend x2, Frontend x1, Flutter x1, DevOps x1
```

---

## 8.8 Risk Mitigation

| Risk                          | Impact | Probability | Mitigation                                      |
| ----------------------------- | ------ | ----------- | ----------------------------------------------- |
| AI accuracy below target      | High   | Medium      | Fallback to rules, human-in-loop                |
| Voice integration complexity  | Medium | Medium      | Start with SMS, add voice later                 |
| External API rate limits      | Medium | Medium      | Caching, queue management                       |
| Mobile offline sync conflicts | Medium | High        | Conflict resolution UI, server wins             |
| LeadGen API availability      | High   | Low         | Mock data for development, graceful degradation |
| Performance at scale          | High   | Medium      | Load testing early, horizontal scaling          |
| Frappe CRM API changes        | Medium | Low         | Abstraction layer, version pinning              |

---

## 8.9 Success Metrics by Phase

### Phase 1 Metrics

| Metric                 | Target |
| ---------------------- | ------ |
| Messages processed/day | 1,000+ |
| Jobs dispatched/day    | 100+   |
| Form submissions/day   | 200+   |
| Portal active users    | 500+   |
| Clock-in success rate  | 95%    |

### Phase 2 Metrics

| Metric                    | Target     |
| ------------------------- | ---------- |
| Workflow automations      | 50+ active |
| Auto-assignment rate      | 80%        |
| SLA compliance            | 90%        |
| Appointments booked/month | 500+       |
| Shift swaps completed     | 50/month   |

### Phase 3 Metrics

| Metric                       | Target      |
| ---------------------------- | ----------- |
| AI routing accuracy          | 85%         |
| RAG answer satisfaction      | 80%         |
| Leads generated              | 1,000/month |
| Standup email open rate      | 70%         |
| Sentiment detection accuracy | 85%         |

### Phase 4 Metrics

| Metric                | Target |
| --------------------- | ------ |
| Active companies      | 100+   |
| Monthly active users  | 2,000+ |
| Mobile app rating     | 4.5+   |
| System uptime         | 99.9%  |
| API response time p95 | <200ms |

---

## 8.10 Document Summary

| Section | File                            | Content                       |
| ------- | ------------------------------- | ----------------------------- |
| 1       | `prd-01-executive-summary.md`   | Vision, architecture, markets |
| 2       | `prd-02-personas.md`            | User personas, role matrix    |
| 3       | `prd-03-ops-features.md`        | 12 OPS features detailed      |
| 4       | `prd-04-crm-features.md`        | 7 CRM features detailed       |
| 5       | `prd-05-hr-features.md`         | 2 HR features detailed        |
| 6       | `prd-06-leadgen-integration.md` | LeadGen interface             |
| 7       | `prd-07-architecture.md`        | Technical architecture        |
| 8       | `prd-08-roadmap.md`             | Implementation phases         |

---

## 8.11 Next Steps

1. **Immediate:** Review and approve PRD
2. **Week 1:** Set up development environment, create module scaffold
3. **Week 2:** Begin Phase 1 DocTypes and APIs
4. **Week 3:** Begin Universal Inbox channel plugins
5. **Week 4:** Begin Dispatch and Mobile Forms

---

**End of Dartwing Company PRD**
