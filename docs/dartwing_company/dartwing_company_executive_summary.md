# Dartwing Company Module - Executive Summary

**Version:** 1.0  
**Date:** November 28, 2025

---

## 1. Product Vision

**Dartwing Company** is an AI-First Operations Platform that transforms how businesses operate. Built as an intelligent overlay on the Frappe ecosystem, it unifies operations, CRM, and workforce management into a single platform.

### Value Proposition

| For                     | Pain Point                                 | Solution                                |
| ----------------------- | ------------------------------------------ | --------------------------------------- |
| **Operations Managers** | Drowning in coordination across tools      | Single dashboard, automated dispatch    |
| **Business Owners**     | Leads falling through cracks               | AI-powered growth engine                |
| **Field Workers**       | Paper forms, unclear schedules             | Mobile-first with offline capability    |
| **Clients**             | Can't get status, must call for everything | Self-service portal                     |
| **HR Managers**         | Manual scheduling, attendance disputes     | Geo-verified clock-in, swap marketplace |

---

## 2. Platform Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      DARTWING COMPANY                            │
│                   AI-First Operations Layer                      │
│  ┌───────────────┬───────────────┬───────────────┬───────────┐  │
│  │  OPERATIONS   │  CRM OVERLAY  │  HR OVERLAY   │ HEALTHCARE│  │
│  │  12 Features  │  7 Features   │  2 Features   │  OVERLAY  │  │
│  └───────────────┴───────────────┴───────────────┴───────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   DARTWING    │     │   DARTWING    │     │   DARTWING    │
│   FLUTTER     │     │   LEADGEN     │     │    FONE       │
│  Mobile App   │     │ Lead Engine   │     │  Voice/SMS    │
└───────────────┘     └───────────────┘     └───────────────┘
                              │
┌─────────────────────────────┴─────────────────────────────────┐
│                     FRAPPE ECOSYSTEM                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │ ERPNext │ │  HRMS   │ │   CRM   │ │ Health  │ │  Drive  │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### Core Principle: Overlay, Don't Extend

We **ADD** functionality on top of Frappe apps rather than modifying their core:

- Link to existing DocTypes (Customer, Employee, Lead)
- Extend with custom fields where needed
- React to doc_events to trigger our logic
- Sync our data back to Frappe apps

---

## 3. Feature Summary

### Operations Core (12 Features)

| ID     | Feature                | Description                                              | AI-Powered |
| ------ | ---------------------- | -------------------------------------------------------- | :--------: |
| OPS-01 | **AI Receptionist**    | Voice/text auto-attendant, intent routing, agent whisper |     ✓      |
| OPS-02 | **Universal Inbox**    | Unified Email, SMS, Voice, WhatsApp, Messenger           |     ✓      |
| OPS-03 | **Workflow Builder**   | No-code automation with external app sync                |            |
| OPS-04 | **Smart Dispatch**     | Map-based assignment with drive-time optimization        |     ✓      |
| OPS-05 | **Mobile Forms**       | Custom forms with offline capability                     |            |
| OPS-06 | **Status Boards**      | Kanban, Gantt, Calendar, Map views                       |            |
| OPS-07 | **Knowledge Base**     | Wiki + RAG-powered Q&A with citations                    |     ✓      |
| OPS-08 | **Broadcast Alerts**   | Multi-channel emergency notifications                    |            |
| OPS-09 | **Daily Standup**      | Automated morning briefing                               |     ✓      |
| OPS-10 | **Visitor Management** | Digital front desk with notifications                    |            |
| OPS-11 | **Resource Booking**   | Rooms, vehicles, equipment reservations                  |            |
| OPS-12 | **Ask Anything**       | Global search + slash commands                           |     ✓      |

### CRM Overlay (7 Features)

| ID     | Feature                 | Description                           | AI-Powered |
| ------ | ----------------------- | ------------------------------------- | :--------: |
| CRM-01 | **Client Portal**       | White-labeled customer self-service   |            |
| CRM-02 | **Document Vault**      | Secure file sharing with audit trail  |            |
| CRM-03 | **Appointment Booker**  | Scheduling with payments integration  |            |
| CRM-04 | **Service Tickets**     | Smart routing with VIP escalation     |     ✓      |
| CRM-05 | **Custom Fields**       | Industry-specific data storage        |            |
| CRM-06 | **SLA Engine**          | Response time tracking and escalation |            |
| CRM-07 | **Growth Orchestrator** | AI interview → ICP → Lead generation  |     ✓      |

### HR Overlay (2 Features)

| ID    | Feature             | Description                                        | AI-Powered |
| ----- | ------------------- | -------------------------------------------------- | :--------: |
| HR-01 | **Shift Scheduler** | Drag-drop builder, swap marketplace, cert blocking |            |
| HR-02 | **Geo Clock-In**    | GPS/WiFi/QR validation, anomaly detection          |     ✓      |

---

## 4. Integration Points

### ERPNext Integration

| ERPNext DocType   | How We Use It                                   |
| ----------------- | ----------------------------------------------- |
| **Customer**      | Portal access, dispatch jobs, tickets, invoices |
| **Contact**       | Conversation matching, appointments             |
| **Address**       | Dispatch job locations, geocoding               |
| **Sales Invoice** | Portal display, workflow triggers               |
| **Project**       | Workflow linking, status boards                 |
| **Item**          | Service catalog for dispatch                    |

**Data Flow:**

- Dispatch Job completion → Creates Sales Invoice
- Client Portal → Displays Customer invoices/projects
- Workflow Engine → Updates Project/Task status

### HRMS Integration

| HRMS DocType          | How We Use It                                   |
| --------------------- | ----------------------------------------------- |
| **Employee**          | Dispatch assignment, scheduling, certifications |
| **Attendance**        | Geo clock-in syncs here (with custom fields)    |
| **Shift Assignment**  | Schedule Entry syncs here on publish            |
| **Leave Application** | Check availability for scheduling               |

**Data Flow:**

- Schedule Entry (ours) → Syncs to Shift Assignment (HRMS)
- Geo Clock-In (ours) → Creates Attendance (HRMS) with GPS data
- Employee Certification (ours) → Blocks scheduling if expired

### Frappe CRM Integration

| CRM DocType       | How We Use It                          |
| ----------------- | -------------------------------------- |
| **Lead**          | Growth Orchestrator creates leads here |
| **Deal**          | Track campaign conversions and ROI     |
| **Contact**       | Conversation matching                  |
| **Communication** | Link to our Conversations              |

**Data Flow:**

- Growth Orchestrator → dartwing_leadgen → Creates CRM Lead
- Lead/Deal updates → Update Campaign metrics
- Inbound message → Creates Communication + Conversation

### Frappe Health Integration

| Health DocType              | How We Use It               |
| --------------------------- | --------------------------- |
| **Patient**                 | Portal access, appointments |
| **Patient Encounter**       | Clinical form submissions   |
| **Healthcare Practitioner** | Appointment scheduling      |

### Frappe Drive Integration

| Drive Feature | How We Use It                  |
| ------------- | ------------------------------ |
| **Folders**   | Document Vault storage backend |
| **Files**     | Client document storage        |
| **Sharing**   | Portal file access control     |

---

## 5. Key Differentiators

### 1. AI-First Design

Every feature enhanced by AI:

- **Receptionist:** Intent classification, smart routing
- **Inbox:** Sentiment analysis, suggested replies
- **Dispatch:** Optimal assignment scoring
- **Knowledge:** RAG-powered Q&A with citations
- **Growth:** AI interviews to build campaigns

### 2. Unified Platform

Single system replacing:

- Separate dispatch software
- Standalone CRM
- HR scheduling tools
- Client portal products
- Knowledge base systems

### 3. Mobile-First Workforce

- Offline-capable forms
- GPS-verified attendance
- Push notifications
- Camera/signature capture

### 4. Leverage Existing Investment

- Works with existing ERPNext data
- Enhances HRMS without replacing it
- Extends Frappe CRM capabilities
- Uses Frappe Drive for storage

---

## 6. Technical Summary

### Technology Stack

| Component   | Technology                          |
| ----------- | ----------------------------------- |
| Framework   | Frappe 15.x                         |
| Database    | MariaDB 10.11+                      |
| Cache/Queue | Redis 7.x                           |
| Search      | OpenSearch 2.x (full-text + vector) |
| AI/LLM      | OpenAI / Claude API                 |
| Mobile      | Flutter (Dartwing Flutter)          |
| Voice/SMS   | dartwing_fone                       |
| Maps        | Google Maps API                     |
| Payments    | Stripe                              |

### New DocTypes (25+)

| Category   | DocTypes                                                                                                              |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Operations | Conversation, Dispatch Job, Mobile Form, Knowledge Article, Workflow Template, Broadcast Alert, Resource, Visitor Log |
| CRM        | Portal Settings, View Set, Document Vault, Appointment, Service Ticket, SLA Policy, Campaign                          |
| HR         | Shift Template, Schedule Entry, Shift Swap Request, Work Location, Employee Certification                             |

### Custom Fields on Frappe Apps

| App              | Custom Fields Added                                                         |
| ---------------- | --------------------------------------------------------------------------- |
| ERPNext Customer | portal_enabled, view_set, document_vault, custom_data                       |
| HRMS Employee    | skills, home_location, dispatch_enabled                                     |
| HRMS Attendance  | clock_in_location, clock_out_location, validation_method, validation_status |
| CRM Lead         | leadgen_source, icp_score, campaign                                         |

---

## 7. Implementation Roadmap

| Phase               | Timeline     | Focus                         | Key Deliverables                                     |
| ------------------- | ------------ | ----------------------------- | ---------------------------------------------------- |
| **1: Foundation**   | Months 1-3   | Core communication & dispatch | Universal Inbox, Dispatch, Forms, Portal, Clock-In   |
| **2: Automation**   | Months 4-6   | Workflows & scheduling        | Workflow Engine, Smart Routing, SLA, Shift Scheduler |
| **3: Intelligence** | Months 7-9   | AI features                   | Receptionist, RAG, Growth Orchestrator, Sentiment    |
| **4: Scale**        | Months 10-12 | Polish & integrations         | Social channels, Analytics, Mobile polish            |

### Success Metrics

| Metric               | Year 1 Target |
| -------------------- | ------------- |
| Active Companies     | 500           |
| Monthly Active Users | 5,000         |
| Tasks Automated      | 1M+           |
| AI Interactions      | 100,000/month |
| NPS Score            | >50           |

---

## 8. Target Markets

| Market                    | Key Features                      | Example Use Case               |
| ------------------------- | --------------------------------- | ------------------------------ |
| **Service Businesses**    | Dispatch, Forms, Clock-In         | HVAC company dispatching techs |
| **Professional Services** | Portal, Appointments, Tickets     | Law firm client management     |
| **Healthcare Practices**  | Health integration, Forms, Portal | Clinic patient scheduling      |
| **Property Management**   | Dispatch, Portal, Tickets         | HOA maintenance requests       |
| **Agencies**              | Projects, Portal, Collaboration   | Marketing agency client work   |

---

## 9. Competitive Advantage

| Competitor Type       | Their Approach                          | Our Advantage                |
| --------------------- | --------------------------------------- | ---------------------------- |
| **Point Solutions**   | Single function (dispatch OR CRM OR HR) | Unified platform             |
| **Enterprise Suites** | Expensive, complex                      | Frappe ecosystem, lower cost |
| **Generic Tools**     | Requires customization                  | Purpose-built for operations |
| **Legacy Software**   | Desktop-first                           | Mobile-first, AI-powered     |

---

## 10. Investment Summary

### Development Resources

| Role               | Count | Duration  |
| ------------------ | ----- | --------- |
| Tech Lead          | 1     | 12 months |
| Backend Developer  | 2     | 12 months |
| Frontend Developer | 1     | 12 months |
| Flutter Developer  | 1     | 12 months |
| AI/ML Engineer     | 1     | 6 months  |
| QA Engineer        | 1     | 12 months |

### Infrastructure (Production)

| Component   | Specification              |
| ----------- | -------------------------- |
| Web Servers | 3x 4GB                     |
| Workers     | 10x 4GB                    |
| Database    | 2x 8GB (Primary + Replica) |
| Redis       | 3x 2GB (Cluster)           |
| OpenSearch  | 3x 8GB                     |
| Storage     | 2TB S3/MinIO               |

---

## 11. Summary

**Dartwing Company** transforms business operations by:

1. **Unifying** communications, dispatch, CRM, and HR into one platform
2. **Leveraging** existing Frappe ecosystem investments (ERPNext, HRMS, CRM, Health, Drive)
3. **Enhancing** every workflow with AI (intent, sentiment, routing, generation)
4. **Empowering** field workers with mobile-first, offline-capable tools
5. **Delighting** customers with self-service portals and proactive updates

**The result:** Businesses operate more efficiently, respond faster, and grow smarter.

---

**Related Documents:**

- [Full PRD](dartwing-company-prd-complete.md) - 3,081 lines
- [Full Architecture](dartwing-company-architecture-complete.md) - 4,960 lines
