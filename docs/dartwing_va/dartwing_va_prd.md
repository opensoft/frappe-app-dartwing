# Dartwing VA

## Product Requirements Document

**Your AI Wingman at Work**

---

|             |                                 |
| ----------- | ------------------------------- |
| **Product** | Dartwing VA (Virtual Assistant) |
| **Version** | 1.0                             |
| **Date**    | November 28, 2025               |
| **Status**  | Draft                           |
| **Owner**   | Product Team                    |

---

## Document Overview

This Product Requirements Document (PRD) defines the complete specifications for Dartwing VA, an AI-powered personal assistant that provides voice-first, personality-matched access to all company systems within the Dartwing ecosystem.

**Total Pages:** ~250  
**Total Features:** 52

---

## Table of Contents

| Section | Title                                                                            | Page |
| ------- | -------------------------------------------------------------------------------- | ---- |
| 1       | [Executive Summary](#section-1-executive-summary)                                | 4    |
| 2       | [User Personas](#section-2-user-personas)                                        | 12   |
| 3       | [Onboarding & Personality Features](#section-3-onboarding--personality-features) | 30   |
| 4       | [Voice Interface Features](#section-4-voice-interface-features)                  | 55   |
| 5       | [Sub-Agent System](#section-5-sub-agent-system)                                  | 85   |
| 6       | [Memory & Context Features](#section-6-memory--context-features)                 | 115  |
| 7       | [Privacy & Audit Features](#section-7-privacy--audit-features)                   | 140  |
| 8       | [Company Templates & Admin](#section-8-company-templates--admin)                 | 170  |
| 9       | [Platform Integration](#section-9-platform-integration)                          | 195  |
| 10      | [Technical Requirements](#section-10-technical-requirements)                     | 225  |
| 11      | [Implementation Roadmap](#section-11-implementation-roadmap)                     | 245  |

---

## Feature Index

### Onboarding & Personality (ONB)

- ONB-01: Personality Matching Quiz
- ONB-02: VA Voice Selection
- ONB-03: VA Avatar & Appearance
- ONB-04: VA Naming
- ONB-05: Personality Tuning
- ONB-06: Quick Start Mode
- ONB-07: Personality Import/Export

### Voice Interface (VOI)

- VOI-01: Real-Time Voice Conversation
- VOI-02: Wake Word Activation
- VOI-03: Interruption Handling
- VOI-04: Multi-Turn Dialogue
- VOI-05: Voice Commands & Shortcuts
- VOI-06: Voice Transcription Display
- VOI-07: Ambient Mode
- VOI-08: Voice Quality Adaptation
- VOI-09: Multilingual Voice
- VOI-10: Voice Biometrics

### Sub-Agent System (SUB)

- SUB-01: Coordinator Agent
- SUB-02: HR Sub-Agent
- SUB-03: CRM Sub-Agent
- SUB-04: Operations Sub-Agent
- SUB-05: Knowledge Sub-Agent
- SUB-06: Calendar Sub-Agent
- SUB-07: Finance Sub-Agent
- SUB-08: Custom Sub-Agents
- SUB-09: Sub-Agent Orchestration
- SUB-10: Sub-Agent Fallback Chain

### Memory & Context (MEM)

- MEM-01: Conversation History
- MEM-02: User Preferences Memory
- MEM-03: Action History
- MEM-04: Contextual Awareness
- MEM-05: Proactive Suggestions
- MEM-06: Learning from Corrections
- MEM-07: Cross-Session Memory
- MEM-08: Memory Privacy Controls

### Privacy & Audit (PRI)

- PRI-01: Privacy Modes
- PRI-02: Data Encryption
- PRI-03: Audit Trail
- PRI-04: Manager Oversight
- PRI-05: Compliance Controls
- PRI-06: Data Retention Policies
- PRI-07: Access Controls
- PRI-08: Consent Management

### Company Templates & Admin (ADM)

- ADM-01: VA Templates
- ADM-02: Template Deployment
- ADM-03: Company Settings
- ADM-04: Usage Analytics
- ADM-05: Cost Management
- ADM-06: Employee Onboarding
- ADM-07: Bulk Operations

### Platform Integration (INT)

- INT-01: Frappe Framework Integration
- INT-02: dartwing_fone Integration
- INT-03: dartwing_company Integration
- INT-04: ERPNext Integration
- INT-05: HRMS Integration
- INT-06: Frappe CRM Integration
- INT-07: Frappe Drive Integration
- INT-08: Frappe Health Integration
- INT-09: External Calendar Integration
- INT-10: Third-Party AI Providers

---

## Priority Legend

| Priority | Meaning             | Timeline |
| -------- | ------------------- | -------- |
| **P0**   | Must have for Alpha | Q1 2027  |
| **P1**   | Must have for Beta  | Q2 2027  |
| **P2**   | Must have for GA    | Q3 2027  |
| **P3**   | Nice to have        | Post-GA  |

---

# Dartwing VA - Product Requirements Document

**Module:** dartwing_va  
**Version:** 1.0  
**Date:** November 28, 2025  
**Target Launch:** Q3 2027

---

# Section 1: Executive Summary

## 1.1 Vision Statement

**Every employee gets their own personal AI co-worker.**

Dartwing VA is not another chatbot. It's a voice-first, personality-matched virtual assistant that becomes the employee's single interface to all company systems. It lives in the Dartwing app (Flutter desktop and mobile) and Frappe web interface, powered by the best available AI models with automatic switching.

**Tagline:** "Your AI Wingman at Work"

## 1.2 Problem Statement

| Problem                | Current State                          | Impact                                   |
| ---------------------- | -------------------------------------- | ---------------------------------------- |
| **App Overload**       | Employees juggle 8-15 apps daily       | Context switching costs 23% productivity |
| **AI Fragmentation**   | Different AI tools for different tasks | Inconsistent experience, no memory       |
| **Generic Assistants** | One-size-fits-all AI personalities     | Low adoption, feels robotic              |
| **No Unified Memory**  | Each tool forgets context              | Repeat yourself constantly               |
| **Audit Gaps**         | AI actions hard to track               | Compliance risk, no accountability       |

## 1.3 Solution Overview

Dartwing VA provides:

1. **Single Interface** - One assistant for HR, CRM, Operations, Finance, Calendar, Knowledge
2. **Personality Matching** - AI tuned to each employee's communication style
3. **Voice-First** - Natural conversation with real-time voice (OpenAI 4o)
4. **Local + Cloud AI** - Google Gems for privacy-sensitive tasks, frontier models for power
5. **Full Memory** - Remembers preferences, history, running jokes, context
6. **Auditable Actions** - Every action logged, reversible, manager-visible

## 1.4 Strategic Value

```
┌─────────────────────────────────────────────────────────────────┐
│                    DARTWING PLATFORM VALUE                       │
├─────────────────────────────────────────────────────────────────┤
│  Without VA:                    With VA:                         │
│  ┌─────────┐                    ┌─────────────────────────────┐ │
│  │ ERPNext │──┐                 │                             │ │
│  ├─────────┤  │                 │      "Hey Alex, book my     │ │
│  │  HRMS   │──┼── User          │       flight and submit     │ │
│  ├─────────┤  │   switches      │       yesterday's receipt"  │ │
│  │   CRM   │──┤   between       │                             │ │
│  ├─────────┤  │   apps          │         DARTWING VA         │ │
│  │ Dispatch│──┤                 │      (handles everything)   │ │
│  ├─────────┤  │                 │                             │ │
│  │ Calendar│──┘                 └─────────────────────────────┘ │
│  └─────────┘                                                     │
│                                                                  │
│  Result: 23% productivity       Result: Single conversation,    │
│  lost to context switching      all systems orchestrated        │
└─────────────────────────────────────────────────────────────────┘
```

## 1.5 Target Users

| User Type             | Count (Year 1) | Primary Use                           |
| --------------------- | -------------- | ------------------------------------- |
| **Knowledge Workers** | 3,000          | Calendar, expenses, knowledge lookup  |
| **Field Workers**     | 1,500          | Dispatch, clock-in, forms, directions |
| **Managers**          | 500            | Reports, approvals, team oversight    |
| **Executives**        | 100            | Briefings, decisions, communications  |
| **HR/Admin**          | 200            | VA templates, policy deployment       |

**Total Target:** 5,000 monthly active users by Q4 2027

## 1.6 Key Metrics

| Metric                      | Definition                    | Target   |
| --------------------------- | ----------------------------- | -------- |
| **DAU/MAU Ratio**           | Daily active / monthly active | >60%     |
| **Conversation Completion** | Tasks completed via VA        | >85%     |
| **Voice Adoption**          | % using voice vs text         | >40%     |
| **Time Saved**              | Hours saved per employee/week | 3+ hours |
| **NPS Score**               | Net Promoter Score            | >50      |
| **Fallback Rate**           | VA couldn't handle, escalated | <10%     |

## 1.7 Pricing Model

| Tier           | Price       | Includes                                          |
| -------------- | ----------- | ------------------------------------------------- |
| **Startup**    | Free        | 5 employees, basic VA, 100 voice min/mo           |
| **Team**       | $29/user/mo | Unlimited voice, custom personality, 5 sub-agents |
| **Business**   | $49/user/mo | All sub-agents, manager controls, audit logs      |
| **Enterprise** | Custom      | On-prem Gems, custom sub-agents, SLA              |

## 1.8 Platform Distribution

| Platform                     | Technology         | Features                                |
| ---------------------------- | ------------------ | --------------------------------------- |
| **dartwing-app Mobile**      | Flutter            | Full VA, voice, offline mode            |
| **dartwing-app Desktop**     | Flutter            | Full VA, voice, screen share            |
| **frappe-app-dartwing Web**  | Frappe UI + Vue.js | Full VA, text-first, voice optional     |
| **DartwingFone Integration** | Via dartwing_fone  | Inbound call handling, outbound dialing |

## 1.9 AI Model Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI MODEL ROUTING                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Input ──► Router ──┬──► Google Gems (Local)               │
│                          │    • Privacy-sensitive queries        │
│                          │    • Offline mode                     │
│                          │    • Fast simple tasks                │
│                          │                                       │
│                          ├──► OpenAI GPT-4o                      │
│                          │    • Voice generation/understanding   │
│                          │    • Complex reasoning                │
│                          │    • Default coordinator              │
│                          │                                       │
│                          ├──► Claude 3.5/4                       │
│                          │    • Long document analysis           │
│                          │    • Code generation                  │
│                          │    • Nuanced writing                  │
│                          │                                       │
│                          ├──► Gemini 2                           │
│                          │    • Multimodal (images, video)       │
│                          │    • Google Workspace integration     │
│                          │                                       │
│                          └──► Llama-405B (Self-hosted)           │
│                               • Enterprise on-prem option        │
│                               • No data leaves network           │
│                                                                  │
│  Model selection: automatic based on task + user preference      │
│  + cost optimization + latency requirements                      │
└─────────────────────────────────────────────────────────────────┘
```

## 1.10 Success Criteria

| Phase     | Timeline | Success Criteria                                     |
| --------- | -------- | ---------------------------------------------------- |
| **Alpha** | Q1 2027  | 50 employees, 80% task completion, <3s voice latency |
| **Beta**  | Q2 2027  | 10 companies, NPS >40, manager controls working      |
| **GA**    | Q3 2027  | 100 companies, 5,000 users, $150K MRR                |
| **Scale** | Q4 2027  | 500 companies, 25,000 users, $500K MRR               |

## 1.11 Dependencies

| Dependency             | Type     | Status         |
| ---------------------- | -------- | -------------- |
| dartwing_fone          | Required | Production     |
| dartwing_company       | Required | In Development |
| dartwing_core          | Required | Production     |
| dartwing-app (Flutter) | Required | Production     |
| frappe-app-dartwing    | Required | Production     |
| ERPNext                | Optional | Stable         |
| HRMS                   | Optional | Stable         |
| Frappe CRM             | Optional | Stable         |
| Frappe Health          | Optional | Stable         |
| OpenAI API             | Required | Available      |
| Google Gems            | Required | Available 2026 |

## 1.12 Document Structure

| Section | Contents                          |
| ------- | --------------------------------- |
| 1       | Executive Summary (this section)  |
| 2       | User Personas                     |
| 3       | Onboarding & Personality Features |
| 4       | Voice Interface Features          |
| 5       | Sub-Agent System                  |
| 6       | Memory & Context Features         |
| 7       | Privacy & Audit Features          |
| 8       | Company Templates & Admin         |
| 9       | Platform Integration              |
| 10      | Technical Requirements            |
| 11      | Implementation Roadmap            |

---

_Next: Section 2 - User Personas_

# Section 2: User Personas

## 2.1 Primary Personas

### Persona 1: Field Service Technician

**Name:** Marcus Chen  
**Role:** HVAC Service Technician  
**Age:** 34  
**Tech Comfort:** Medium  
**VA Name:** "Chief"

**Profile:**

- Works 8-10 jobs per day across metro area
- Hands often dirty/occupied - needs voice interface
- Limited time between jobs
- Needs quick access to job details, customer history, parts inventory

**Daily VA Interactions:**

| Time     | Marcus Says                                  | VA Does                                                   |
| -------- | -------------------------------------------- | --------------------------------------------------------- |
| 6:30 AM  | "Chief, what's my day look like?"            | Reads route: 8 jobs, first at 7:15, 47 miles total        |
| 7:10 AM  | "Running 10 minutes late to first job"       | Notifies customer via SMS, updates dispatch board         |
| 9:45 AM  | "What's the compressor model for this unit?" | Pulls equipment history from job record                   |
| 11:30 AM | "Order a capacitor for the Johnson job"      | Creates parts request, routes for approval                |
| 12:15 PM | "Submit my lunch receipt, $14.50"            | OCR receipt photo, creates expense, auto-categorizes      |
| 3:00 PM  | "Clock me out of this job, heading to next"  | Completes job, starts travel time, notifies next customer |
| 5:30 PM  | "How many hours this week?"                  | "42 hours logged, 3 hours overtime"                       |

**Pain Points Solved:**

- No more typing on phone with dirty hands
- No switching between dispatch, expense, timesheet apps
- Customer gets proactive updates without Marcus calling

**VA Personality:**

- Direct, no-nonsense
- Quick responses
- Military-style brevity ("Copy that", "Affirmative")

---

### Persona 2: Office Manager

**Name:** Sarah Okonkwo  
**Role:** Office Manager, Medical Practice  
**Age:** 42  
**Tech Comfort:** High  
**VA Name:** "Aria"

**Profile:**

- Manages scheduling for 5 providers, 12 staff
- Constant interruptions - needs hands-free help
- Handles patient communications, vendor orders, HR tasks
- Needs to context-switch rapidly

**Daily VA Interactions:**

| Time     | Sarah Says                                           | VA Does                                                              |
| -------- | ---------------------------------------------------- | -------------------------------------------------------------------- |
| 8:00 AM  | "Aria, any call-outs today?"                         | "Two: Jessica called in sick, and Dr. Patel is delayed until 10"     |
| 8:05 AM  | "Find coverage for Jessica's shift"                  | Checks availability, texts eligible staff, books first responder     |
| 9:30 AM  | "Reschedule Dr. Patel's 9 AM patients to afternoon"  | Moves 4 appointments, sends notifications to patients                |
| 11:00 AM | "What's our supply order status?"                    | "Gloves shipped yesterday, arriving Thursday. Syringes backordered." |
| 1:00 PM  | "Draft an email to staff about the holiday schedule" | Composes email based on policy, shows for approval                   |
| 2:30 PM  | "Who hasn't submitted timesheets?"                   | "Three people: Mike, Jennifer, and Carlos"                           |
| 4:00 PM  | "What's my PTO balance?"                             | "14 days remaining, 6 days scheduled in December"                    |

**Pain Points Solved:**

- Shift coverage found in minutes not hours
- No logging into HRMS for simple queries
- Draft communications without opening email

**VA Personality:**

- Warm but efficient
- Anticipates follow-up questions
- Slightly formal, professional

---

### Persona 3: Sales Representative

**Name:** David Park  
**Role:** Enterprise Sales, SaaS Company  
**Age:** 29  
**Tech Comfort:** Very High  
**VA Name:** "Max"

**Profile:**

- Manages 50+ active opportunities
- Lives in CRM, email, calendar
- Travels 40% of time
- Competitive, metrics-driven

**Daily VA Interactions:**

| Time     | David Says                                                                | VA Does                                                     |
| -------- | ------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 7:00 AM  | "Max, brief me on today"                                                  | "3 calls, demo at 2 PM, proposal due for Acme Corp"         |
| 7:05 AM  | "What do I need to know about the Acme deal?"                             | Summarizes: $250K, 3 stakeholders, competitor is Salesforce |
| 9:00 AM  | "After my call with Chen, log that they want a POC"                       | Updates CRM deal stage, creates POC task                    |
| 10:30 AM | "Find me flights to Chicago under $400 next Tuesday"                      | Searches, presents 3 options, books on selection            |
| 12:00 PM | "What's my quota attainment?"                                             | "68% of Q4, need $180K to hit 100%"                         |
| 3:00 PM  | "Draft a follow-up to the demo, mention their concern about integrations" | Composes personalized email referencing demo notes          |
| 5:00 PM  | "Submit my expenses from the Chicago trip"                                | Pulls receipts from photos, creates report, submits         |

**Pain Points Solved:**

- CRM updates happen conversationally
- Pre-call prep in 30 seconds
- Expenses submitted same-day

**VA Personality:**

- High energy, confident
- Uses sales terminology naturally
- Celebrates wins ("Nice! That puts you at 72%!")

---

### Persona 4: Executive

**Name:** Jennifer Walsh  
**Role:** VP of Operations  
**Age:** 51  
**Tech Comfort:** Medium  
**VA Name:** "James"

**Profile:**

- Oversees 200+ employees across 5 locations
- Back-to-back meetings all day
- Needs information distilled, not detailed
- Makes 20+ decisions per day

**Daily VA Interactions:**

| Time     | Jennifer Says                                           | VA Does                                                             |
| -------- | ------------------------------------------------------- | ------------------------------------------------------------------- |
| 6:00 AM  | "James, morning briefing"                               | 3-minute audio: key metrics, urgent items, today's schedule         |
| 8:30 AM  | "Approve the pending purchase orders"                   | Lists 4 POs, she approves by voice, done in 90 seconds              |
| 10:00 AM | "How's the Denver location performing?"                 | "Revenue up 12%, but overtime is 20% above budget"                  |
| 11:30 AM | "Get me a meeting with all location managers this week" | Finds first available slot, sends invites                           |
| 2:00 PM  | "What's the status on the new hire for Phoenix?"        | "Offer sent Monday, awaiting response, backup candidate identified" |
| 4:00 PM  | "Compare this quarter to last quarter"                  | Visual summary: revenue +8%, costs +3%, margin improved             |
| 6:00 PM  | "Anything I need to handle before tomorrow?"            | "One escalation: customer complaint at Memphis needs your call"     |

**Pain Points Solved:**

- No digging through dashboards
- Approvals done in transit
- Stays informed without meetings

**VA Personality:**

- British butler style - formal, composed
- Summarizes ruthlessly
- Never wastes her time

---

### Persona 5: HR Administrator

**Name:** Maria Santos  
**Role:** HR Coordinator  
**Age:** 38  
**Tech Comfort:** High  
**VA Name:** "Sunny"

**Profile:**

- Manages onboarding, benefits, compliance
- Answers same questions repeatedly
- Needs to deploy VA templates to new hires
- Handles sensitive employee information

**Daily VA Interactions:**

| Time     | Maria Says                                                              | VA Does                                                   |
| -------- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| 8:00 AM  | "Sunny, who's starting this week?"                                      | "Two new hires: Alex on Monday, Priya on Wednesday"       |
| 8:30 AM  | "Set up Alex's onboarding VA"                                           | Creates personalized VA instance with onboarding template |
| 10:00 AM | "What's the 401k match policy?"                                         | Recites policy, offers to send to employee                |
| 11:00 AM | "Who's up for annual review this month?"                                | Lists 8 employees with review dates                       |
| 1:00 PM  | "Draft an offer letter for the marketing role"                          | Pulls template, fills in compensation, generates PDF      |
| 3:00 PM  | "Show me attendance anomalies this week"                                | "3 flags: late clock-ins for Mike (3 days)"               |
| 4:00 PM  | "Send benefits enrollment reminder to everyone who hasn't completed it" | Identifies 23 employees, sends personalized reminders     |

**Pain Points Solved:**

- Onboarding VA handles 80% of new hire questions
- Policy lookup instant
- Compliance tracking automated

**VA Personality:**

- Warm, supportive, encouraging
- Patient with explanations
- Appropriate for sensitive topics

---

## 2.2 Secondary Personas

### Persona 6: Warehouse Worker

**Name:** James Thompson  
**Role:** Warehouse Associate  
**Age:** 26  
**Tech Comfort:** Low  
**VA Name:** "Buddy"

**Key Needs:**

- Simple voice commands while hands-on
- Clock in/out, break logging
- Safety incident reporting
- Shift swap requests

**VA Style:** Casual, patient, confirms everything

---

### Persona 7: Remote Contractor

**Name:** Aisha Patel  
**Role:** Freelance Designer  
**Age:** 31  
**Tech Comfort:** High  
**VA Name:** "Echo"

**Key Needs:**

- Time tracking for billable hours
- Invoice submission
- Project status updates
- Limited system access (contractor permissions)

**VA Style:** Creative, flexible, respects boundaries

---

### Persona 8: Retail Store Manager

**Name:** Carlos Mendez  
**Role:** Store Manager  
**Age:** 45  
**Tech Comfort:** Medium  
**VA Name:** "Sam"

**Key Needs:**

- Real-time sales numbers
- Staff scheduling and coverage
- Inventory alerts
- Customer escalation handling

**VA Style:** Bilingual (English/Spanish), retail-savvy

---

## 2.3 Persona-to-Feature Matrix

| Feature             | Marcus (Field) | Sarah (Office) | David (Sales) | Jennifer (Exec) | Maria (HR) |
| ------------------- | :------------: | :------------: | :-----------: | :-------------: | :--------: |
| Voice Interface     |      ★★★       |      ★★☆       |      ★★☆      |       ★★★       |    ★☆☆     |
| Dispatch/Jobs       |      ★★★       |      ★☆☆       |      ☆☆☆      |       ★☆☆       |    ☆☆☆     |
| Calendar/Scheduling |      ★☆☆       |      ★★★       |      ★★★      |       ★★★       |    ★★☆     |
| Expense/Finance     |      ★★☆       |      ★☆☆       |      ★★★      |       ★★☆       |    ★☆☆     |
| CRM/Sales           |      ☆☆☆       |      ★☆☆       |      ★★★      |       ★★☆       |    ☆☆☆     |
| HR/Time             |      ★★☆       |      ★★★       |      ★☆☆      |       ★☆☆       |    ★★★     |
| Knowledge Base      |      ★★☆       |      ★★☆       |      ★★☆      |       ★☆☆       |    ★★★     |
| Reports/Analytics   |      ★☆☆       |      ★★☆       |      ★★★      |       ★★★       |    ★★☆     |
| VA Templates        |      ☆☆☆       |      ★☆☆       |      ☆☆☆      |       ★☆☆       |    ★★★     |
| Privacy Modes       |      ★☆☆       |      ★★☆       |      ★★☆      |       ★★★       |    ★★★     |

★★★ = Critical | ★★☆ = Important | ★☆☆ = Nice to have | ☆☆☆ = Not needed

---

## 2.4 Persona Journey Maps

### Marcus (Field Technician) - First Week with VA

```
Day 1: Skeptical
├── "Another app to learn..."
├── Does personality quiz (voice) in truck
├── Names VA "Chief" (military background)
└── Tries one command: "What's my first job?"
    └── Works instantly → "Okay, not bad"

Day 2: Testing
├── Uses voice for job lookups (works)
├── Tries expense submission (works)
├── Asks about customer history (accurate)
└── Tells coworker about it

Day 3: Adopting
├── Morning briefing becomes habit
├── Stops opening dispatch app
├── "Chief, call the customer" (impressed)
└── Realizes hands-free value

Day 5: Dependent
├── "Can't imagine going back"
├── Uses for everything except complex issues
├── Teaches new tech how to use it
└── NPS: 9/10
```

### Jennifer (Executive) - First Month with VA

```
Week 1: Executive Skepticism
├── "I have an assistant for this"
├── IT sets up VA, she ignores it
├── Assistant suggests trying for morning briefing
└── Tries once: "Actually useful"

Week 2: Selective Use
├── Morning briefings daily
├── Approvals via voice (game changer)
├── Still uses assistant for complex tasks
└── "James, what's my 2 PM about?" becomes habit

Week 3: Integration
├── Uses in car during commute
├── Asks strategic questions ("Compare regions")
├── Board prep via VA + assistant
└── Shares with other VPs

Week 4: Advocacy
├── Mandates for her direct reports
├── Requests custom executive template
├── "Why didn't we have this before?"
└── NPS: 10/10
```

---

## 2.5 Anti-Personas (Who VA is NOT for)

| Anti-Persona            | Why Not                          | Alternative                    |
| ----------------------- | -------------------------------- | ------------------------------ |
| **Privacy Absolutist**  | Won't accept any AI logging      | Use system directly, no VA     |
| **Power User**          | Faster with keyboard shortcuts   | VA optional, not required      |
| **Offline-Only Worker** | No connectivity for cloud AI     | Local Gems mode (limited)      |
| **One-Time Visitor**    | No value in personality matching | Guest mode, no personalization |

---

_Next: Section 3 - Onboarding & Personality Features_

# Section 3: Onboarding & Personality Features

## 3.1 Feature Group Overview

| ID     | Feature                   | Priority | Phase |
| ------ | ------------------------- | -------- | ----- |
| ONB-01 | Personality Matching Quiz | P0       | Alpha |
| ONB-02 | VA Voice Selection        | P0       | Alpha |
| ONB-03 | VA Avatar & Appearance    | P1       | Beta  |
| ONB-04 | VA Naming                 | P0       | Alpha |
| ONB-05 | Personality Tuning        | P1       | Beta  |
| ONB-06 | Quick Start Mode          | P1       | Beta  |
| ONB-07 | Personality Import/Export | P2       | GA    |

---

## 3.2 ONB-01: Personality Matching Quiz

### Description

A conversational quiz (voice or text) that builds the employee's personality profile, determining how their VA will communicate, what it proactively suggests, and how it handles ambiguity.

### User Story

> As a new employee, I want my VA to match my communication style so that interactions feel natural, not robotic.

### Quiz Structure

**Format Options:**

- Voice conversation (recommended, 5-7 minutes)
- Text chat (3-5 minutes)
- Quick select cards (2 minutes, less accurate)

**20 Core Questions:**

| #   | Question                                   | Options                                                      | Maps To                |
| --- | ------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| 1   | Are you a morning person or night owl?     | Morning / Night / Depends                                    | `proactive_timing`     |
| 2   | Do you prefer direct feedback or softened? | Direct / Softened / Depends on topic                         | `feedback_style`       |
| 3   | What's your humor style?                   | Sarcastic / Dad jokes / Dry wit / Professional only          | `humor_type`           |
| 4   | How fast do you like responses?            | Instant & brief / Thorough & complete                        | `response_speed`       |
| 5   | Preferred tone?                            | Professional / Friendly / Playful / Military                 | `tone`                 |
| 6   | How much detail do you want?               | Just the answer / Some context / Full explanation            | `detail_level`         |
| 7   | Should VA speak first or wait for you?     | Proactive / Reactive / Balanced                              | `proactivity`          |
| 8   | How do you handle interruptions?           | Fine, interrupt me / Ask first / Never interrupt             | `interrupt_tolerance`  |
| 9   | Formality with your name?                  | First name / Mr./Ms. / Nickname / No name                    | `name_formality`       |
| 10  | How do you like reminders?                 | Gentle nudge / Direct reminder / Urgent alert                | `reminder_style`       |
| 11  | When VA doesn't know something?            | Admit it immediately / Try anyway / Ask clarifying questions | `uncertainty_handling` |
| 12  | Do you like small talk?                    | Yes, it's nice / Occasionally / No, just business            | `small_talk`           |
| 13  | How do you feel about emojis?              | Love them / Occasionally / Never                             | `emoji_usage`          |
| 14  | Celebratory moments?                       | Celebrate wins / Acknowledge briefly / Just move on          | `celebration_style`    |
| 15  | Handling bad news?                         | Rip the bandaid / Soften the blow / Let me discover it       | `bad_news_delivery`    |
| 16  | Cultural context?                          | American / British / Global neutral / [Select culture]       | `cultural_style`       |
| 17  | Industry jargon?                           | Use it heavily / Some is fine / Plain language               | `jargon_level`         |
| 18  | Multitasking preference?                   | One thing at a time / Queue multiple / Parallel processing   | `multitask_mode`       |
| 19  | Learning style?                            | Show me / Tell me / Let me try                               | `learning_style`       |
| 20  | How do you end conversations?              | Quick bye / Friendly wrap-up / Summary + next steps          | `conversation_close`   |

### Personality Profile Schema

```json
{
  "profile_id": "uuid",
  "employee": "Link to Employee",
  "version": 1,
  "created_at": "datetime",
  "updated_at": "datetime",

  "communication": {
    "tone": "professional|friendly|playful|military",
    "feedback_style": "direct|softened|contextual",
    "detail_level": "minimal|moderate|comprehensive",
    "response_speed": "instant|balanced|thorough",
    "formality": "formal|casual|adaptive"
  },

  "personality": {
    "humor_type": "sarcastic|dad_jokes|dry|none",
    "small_talk": "yes|occasional|no",
    "emoji_usage": "frequent|occasional|never",
    "celebration_style": "enthusiastic|brief|none",
    "bad_news_delivery": "direct|softened|discovery"
  },

  "behavior": {
    "proactivity": "high|medium|low",
    "interrupt_tolerance": "high|ask_first|never",
    "reminder_style": "gentle|direct|urgent",
    "uncertainty_handling": "admit|attempt|clarify",
    "multitask_mode": "sequential|queued|parallel"
  },

  "context": {
    "cultural_style": "american|british|global|custom",
    "jargon_level": "heavy|moderate|plain",
    "work_hours": { "start": "08:00", "end": "18:00" },
    "timezone": "America/Chicago",
    "language": "en-US"
  },

  "learning": {
    "style": "visual|auditory|kinesthetic",
    "conversation_close": "quick|friendly|summary"
  },

  "custom_traits": {},
  "encrypted": true
}
```

### Quiz UI Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEET YOUR VA                                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │    👋 "Hi! I'm going to be your personal assistant.    │    │
│  │        Let's spend a few minutes getting to know       │    │
│  │        each other so I can work the way you like."     │    │
│  │                                                         │    │
│  │    🎤 [Tap to speak] or type below                     │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Progress: ████████░░░░░░░░░░░░ 8/20                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ "When I give you information, do you want just the      │   │
│  │  answer, some context, or the full explanation?"        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐   │
│  │ Just answer │ │ Some context│ │ Full explanation        │   │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘   │
│                                                                  │
│                           [Skip this question]                   │
└─────────────────────────────────────────────────────────────────┘
```

### Voice Quiz Flow

1. VA speaks question naturally
2. User responds verbally
3. VA confirms understanding: "Got it - you prefer direct feedback"
4. Smooth transition to next question
5. Progress indicator (audio cue at 25%, 50%, 75%)
6. End with summary: "Here's what I learned about you..."

### Acceptance Criteria

- [ ] Quiz completable in <7 minutes via voice
- [ ] Quiz completable in <5 minutes via text
- [ ] All 20 questions have voice recordings in 4 voices
- [ ] Skipped questions use intelligent defaults
- [ ] Profile encrypted at rest
- [ ] Quiz can be retaken anytime
- [ ] Profile versioning (compare before/after)

---

## 3.3 ONB-02: VA Voice Selection

### Description

Employee chooses the voice their VA uses for all audio responses, with options for age, gender, accent, and energy level.

### User Story

> As an employee, I want to choose a voice that I find pleasant and easy to understand so that I enjoy talking to my VA.

### Voice Options

**Primary Voices (Launch):**

| Voice ID  | Name    | Description            | Gender  | Accent   | Energy |
| --------- | ------- | ---------------------- | ------- | -------- | ------ |
| `alloy`   | Alloy   | Warm, professional     | Neutral | American | Medium |
| `echo`    | Echo    | Clear, confident       | Male    | American | Medium |
| `fable`   | Fable   | Friendly, approachable | Female  | American | High   |
| `onyx`    | Onyx    | Deep, authoritative    | Male    | British  | Low    |
| `nova`    | Nova    | Energetic, youthful    | Female  | American | High   |
| `shimmer` | Shimmer | Calm, soothing         | Female  | British  | Low    |

**Extended Voices (Beta):**

| Voice ID | Name  | Description  | Accent                    |
| -------- | ----- | ------------ | ------------------------- |
| `chen`   | Chen  | Professional | Mandarin-accented English |
| `raj`    | Raj   | Warm         | Indian-accented English   |
| `sofia`  | Sofia | Friendly     | Spanish-accented English  |
| `hans`   | Hans  | Precise      | German-accented English   |
| `kenji`  | Kenji | Polite       | Japanese-accented English |

**Custom Voice (Enterprise):**

- Clone employee's own voice (opt-in, requires recording)
- Clone company spokesperson voice (with consent)

### Voice Preview UI

```
┌─────────────────────────────────────────────────────────────────┐
│                  CHOOSE YOUR VA'S VOICE                          │
│                                                                  │
│  Tap any voice to hear a sample:                                │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   🔊 Alloy  │ │   🔊 Echo   │ │   🔊 Fable  │               │
│  │   Warm,     │ │   Clear,    │ │  Friendly,  │               │
│  │ professional│ │  confident  │ │ approachable│               │
│  │  [Preview]  │ │  [Preview]  │ │  [Preview]  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   🔊 Onyx   │ │   🔊 Nova   │ │  🔊 Shimmer │               │
│  │    Deep,    │ │  Energetic, │ │    Calm,    │               │
│  │authoritative│ │   youthful  │ │   soothing  │               │
│  │  [Preview]  │ │  [Preview]  │ │  [Preview]  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
│  Preview text: "Good morning! You have 3 meetings today,        │
│  starting with the team standup at 9 AM."                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Custom preview: [Type something for VA to say]          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│                        [ Select Onyx ]                           │
└─────────────────────────────────────────────────────────────────┘
```

### Voice Customization (Advanced)

| Setting                 | Options                    | Default |
| ----------------------- | -------------------------- | ------- |
| Speaking Speed          | 0.75x - 1.5x               | 1.0x    |
| Pitch Adjustment        | -20% to +20%               | 0%      |
| Pause Between Sentences | Short / Medium / Long      | Medium  |
| Emphasis Style          | Subtle / Normal / Dramatic | Normal  |

### Technical Implementation

```
Voice Generation Pipeline:
1. Text response from Coordinator Agent
2. SSML markup applied based on personality
3. OpenAI 4o TTS API call
4. Audio streamed to client
5. Cached for repeated phrases

Latency Target: <500ms first byte
```

### Acceptance Criteria

- [ ] 6 voices available at launch
- [ ] Preview plays in <1 second
- [ ] Custom preview text works
- [ ] Voice selection persists across devices
- [ ] Speaking speed adjustable 0.75x-1.5x
- [ ] Voice changeable anytime in settings

---

## 3.4 ONB-03: VA Avatar & Appearance

### Description

Visual representation of the VA that appears during conversations, with customizable appearance options.

### User Story

> As an employee, I want to see a friendly face when talking to my VA so the interaction feels more personal.

### Avatar Types

**1. Animated Character (Default)**

- 3D rendered face
- Lip-sync to voice
- Expressions match sentiment
- Customizable features

**2. Abstract Visualization**

- Sound wave animation
- Pulsing orb
- For users who prefer non-human

**3. Company Mascot (Enterprise)**

- Custom 3D model
- Branded character

**4. No Avatar**

- Voice only
- Text indicator

### Character Customization

| Feature        | Options                                     |
| -------------- | ------------------------------------------- |
| Face Shape     | Round / Oval / Square / Heart               |
| Skin Tone      | 12 options                                  |
| Hair Style     | 20 options + bald                           |
| Hair Color     | 15 options                                  |
| Eye Color      | 10 options                                  |
| Accessories    | Glasses (8 styles), Earrings, Headphones    |
| Expression Set | Friendly / Professional / Playful / Neutral |

### Avatar States

| State     | Visual                             | Trigger             |
| --------- | ---------------------------------- | ------------------- |
| Idle      | Subtle breathing, occasional blink | Waiting for input   |
| Listening | Attentive expression, ear tilt     | User speaking       |
| Thinking  | Eyes up-left, processing indicator | Generating response |
| Speaking  | Lip-sync, hand gestures            | VA responding       |
| Happy     | Smile, slight bounce               | Good news delivered |
| Concerned | Furrowed brow, slower movement     | Bad news or issue   |
| Confused  | Head tilt, question mark           | Needs clarification |

### Avatar Display Modes

```
┌─────────────────────────────────────────────────────────────────┐
│ FULL MODE (Desktop)              COMPACT MODE (Mobile)          │
│                                                                  │
│ ┌───────────────────────┐        ┌───────┐                      │
│ │                       │        │       │ "You have 3         │
│ │     [Avatar Face]     │        │ [Face]│  meetings today"    │
│ │       Speaking        │        │       │                      │
│ │                       │        └───────┘                      │
│ │   "You have 3         │                                       │
│ │    meetings today,    │        MINI MODE (Widget)             │
│ │    starting at 9"     │                                       │
│ │                       │        ┌──┐                           │
│ └───────────────────────┘        │🤖│ 3 meetings               │
│                                  └──┘                           │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] 3 avatar types at launch (character, abstract, none)
- [ ] Lip-sync accuracy >90%
- [ ] Expression changes within 200ms of sentiment shift
- [ ] Customization changes preview in real-time
- [ ] Avatar renders at 60fps on mobile
- [ ] 30+ character customization combinations

---

## 3.5 ONB-04: VA Naming

### Description

Employee gives their VA a personal name, which the VA uses to introduce itself and the employee uses to invoke it.

### User Story

> As an employee, I want to give my VA a name so it feels like my personal assistant, not a generic tool.

### Naming Options

**1. Choose from Suggestions:**

- Alex, Max, Sam, Jamie (neutral)
- Aria, Nova, Luna, Mia (feminine)
- James, Oliver, Leo, Kai (masculine)
- Chief, Captain, Boss, Ace (title-style)
- Echo, Spark, Pixel, Byte (tech-style)
- 老王, 小美, さくら (localized)

**2. Custom Name:**

- Any name 2-20 characters
- Pronunciation guide option
- Phonetic spelling for voice

**3. No Name:**

- Use "Hey Dartwing" or "Assistant"

### Wake Word Integration

| Wake Word Style | Example                     |
| --------------- | --------------------------- |
| Name only       | "Alex"                      |
| Hey + Name      | "Hey Alex"                  |
| Name + please   | "Alex, please..."           |
| Dartwing + Name | "Dartwing Alex" (corporate) |

### Name Validation

- No profanity (multi-language check)
- No trademarked names (Alexa, Siri, Cortana)
- No names of other employees (optional)
- Pronunciation verification via TTS

### UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   NAME YOUR ASSISTANT                            │
│                                                                  │
│  What would you like to call me?                                │
│                                                                  │
│  Popular choices:                                                │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ Alex│ │ Max │ │ Aria│ │James│ │Chief│ │ Sam │              │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │
│                                                                  │
│  Or type your own:                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Captain                                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  🔊 [Hear how I'll say it]: "Hi, I'm Captain!"                  │
│                                                                  │
│                        [ Confirm Name ]                          │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] 20+ suggested names at launch
- [ ] Custom name 2-20 characters
- [ ] Pronunciation preview before confirm
- [ ] Profanity filter (multi-language)
- [ ] Name changeable anytime
- [ ] Wake word responds to name

---

## 3.6 ONB-05: Personality Tuning

### Description

Post-onboarding adjustments to VA personality based on feedback and usage patterns.

### User Story

> As an employee, I want to fine-tune my VA's personality over time so it gets better at matching how I work.

### Tuning Methods

**1. Explicit Feedback:**

- "Be more direct"
- "Less small talk"
- "Slower responses please"
- Thumbs up/down on interactions

**2. Implicit Learning:**

- Track which response styles get positive reactions
- Note when user interrupts (too slow?)
- Detect frustration patterns
- Observe time-of-day preferences

**3. Settings Panel:**

```
┌─────────────────────────────────────────────────────────────────┐
│                   PERSONALITY SETTINGS                           │
│                                                                  │
│  Communication Style                                             │
│  ├─ Directness     [━━━━━━●━━━━━━] More direct                  │
│  ├─ Detail Level   [━━━━●━━━━━━━━] Less detail                  │
│  ├─ Response Speed [━━━━━━━━●━━━━] Faster                       │
│  └─ Formality      [━━●━━━━━━━━━━] More casual                  │
│                                                                  │
│  Personality                                                     │
│  ├─ Humor          [━━━━━━━●━━━━━] Some humor                   │
│  ├─ Proactivity    [━━━━━━━━━●━━━] More proactive               │
│  └─ Celebration    [━━━━●━━━━━━━━] Brief acknowledgment         │
│                                                                  │
│  [Retake Personality Quiz]     [Reset to Defaults]               │
└─────────────────────────────────────────────────────────────────┘
```

**4. Contextual Overrides:**

- "When talking about finances, be more formal"
- "In the morning, be brief"
- "With clients on the line, no jokes"

### Personality Version History

| Date   | Change                 | Method            |
| ------ | ---------------------- | ----------------- |
| Nov 1  | Initial profile        | Quiz              |
| Nov 15 | +10% directness        | User slider       |
| Nov 22 | -5% proactivity        | Implicit learning |
| Dec 1  | "No humor before 10am" | Explicit rule     |

### Acceptance Criteria

- [ ] Sliders for all major personality dimensions
- [ ] Thumbs up/down on every interaction
- [ ] "Be more/less X" voice commands work
- [ ] Implicit learning adjusts ≤5% per week
- [ ] Version history viewable
- [ ] Reset to defaults option

---

## 3.7 ONB-06: Quick Start Mode

### Description

Skip the full quiz and get a working VA immediately with sensible defaults, then personalize over time.

### User Story

> As an employee in a hurry, I want to start using my VA immediately and personalize it later.

### Quick Start Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   GET STARTED QUICKLY                            │
│                                                                  │
│  Choose your style:                                              │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   PROFESSIONAL  │  │    FRIENDLY     │  │     MINIMAL     │  │
│  │                 │  │                 │  │                 │  │
│  │  Formal tone    │  │  Warm & casual  │  │  Just answers   │  │
│  │  Full details   │  │  Some humor     │  │  No small talk  │  │
│  │  Proactive      │  │  Balanced       │  │  Reactive only  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Your VA's name: [Alex                              ]    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│                    [ Start with Friendly ]                       │
│                                                                  │
│  You can personalize more later in Settings > Personality       │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Start Profiles

| Profile          | Key Traits                                                |
| ---------------- | --------------------------------------------------------- |
| **Professional** | Formal tone, comprehensive responses, proactive reminders |
| **Friendly**     | Warm tone, balanced detail, occasional humor              |
| **Minimal**      | Direct answers only, no proactivity, no small talk        |
| **Executive**    | Summary-first, time-conscious, approval-focused           |
| **Field**        | Voice-optimized, hands-free, location-aware               |

### Post-Quick-Start Prompts

After 10 interactions:

> "I notice you often ask for more detail. Want me to be more thorough by default?"

After 25 interactions:

> "You've been using me for a week! Want to take 5 minutes to personalize me better?"

### Acceptance Criteria

- [ ] Onboarding completable in <30 seconds
- [ ] 5 quick-start profiles
- [ ] Profile applicable in 1 tap
- [ ] Prompt to personalize after 10 interactions
- [ ] Quick start users have same NPS as full quiz users (within 10%)

---

## 3.8 ONB-07: Personality Import/Export

### Description

Save personality profile as a file, import to new device/account, or share template with team.

### User Story

> As an employee changing roles, I want to bring my VA personality to my new account.
> As a manager, I want to share my VA setup as a starting point for my team.

### Export Options

**Personal Export:**

- JSON file with full personality profile
- Encrypted with employee password
- Excludes company-specific data

**Template Export (Manager):**

- Anonymized personality settings
- Suggested voice/avatar
- Excludes personal customizations

### Import Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   IMPORT PERSONALITY                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Drop file here or [Browse]                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Found: "Marcus_VA_Profile_2027.json"                           │
│                                                                  │
│  Preview:                                                        │
│  • Tone: Direct, Military-style                                 │
│  • Detail: Minimal                                               │
│  • Proactivity: High                                             │
│  • Voice: Onyx                                                   │
│  • Name: Chief                                                   │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐                         │
│  │ Import All     │  │ Select Items   │                         │
│  └────────────────┘  └────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### Company Templates

HR can create and deploy templates:

- "Sales Team VA" - high energy, CRM-focused
- "Support Team VA" - patient, knowledge-focused
- "Executive VA" - summary-first, approval-focused
- "Warehouse VA" - simple, voice-optimized

### Acceptance Criteria

- [ ] Export creates encrypted JSON file
- [ ] Import validates file integrity
- [ ] Selective import (pick what to include)
- [ ] Company templates deployable by HR
- [ ] Template respects employee's existing name choice

---

_Next: Section 4 - Voice Interface Features_

# Section 4: Voice Interface Features

## 4.1 Feature Group Overview

| ID     | Feature                      | Priority | Phase |
| ------ | ---------------------------- | -------- | ----- |
| VOI-01 | Real-Time Voice Conversation | P0       | Alpha |
| VOI-02 | Wake Word Activation         | P0       | Alpha |
| VOI-03 | Interruption Handling        | P0       | Alpha |
| VOI-04 | Multi-Turn Dialogue          | P0       | Alpha |
| VOI-05 | Voice Commands & Shortcuts   | P1       | Beta  |
| VOI-06 | Voice Transcription Display  | P1       | Beta  |
| VOI-07 | Ambient Mode                 | P2       | GA    |
| VOI-08 | Voice Quality Adaptation     | P1       | Beta  |
| VOI-09 | Multilingual Voice           | P2       | GA    |
| VOI-10 | Voice Biometrics             | P2       | GA    |

---

## 4.2 VOI-01: Real-Time Voice Conversation

### Description

Natural, bi-directional voice conversation with sub-second latency, powered by OpenAI 4o for voice generation and understanding.

### User Story

> As an employee, I want to talk to my VA like I would a human colleague - naturally, with interruptions allowed, without waiting for "ding" sounds.

### Conversation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOICE CONVERSATION FLOW                       │
│                                                                  │
│  Employee        Network           VA                            │
│     │                │               │                           │
│     │ "Hey Alex"     │               │                           │
│     │───────────────>│──────────────>│ Wake detected            │
│     │                │               │ "Yes?"                    │
│     │                │<──────────────│                           │
│     │<───────────────│               │                           │
│     │                │               │                           │
│     │ "What's my     │               │                           │
│     │  first meeting │               │                           │
│     │  today?"       │               │                           │
│     │───────────────>│──────────────>│ Process query            │
│     │                │               │ Fetch calendar            │
│     │                │               │ Generate response         │
│     │                │<──────────────│ "Your first meeting is   │
│     │<───────────────│               │  the team standup at..."  │
│     │                │               │                           │
│     │ "Actually-"    │               │                           │
│     │───────────────>│──────────────>│ INTERRUPT detected       │
│     │                │               │ Stop speaking             │
│     │                │<──────────────│ "Go ahead"               │
│     │<───────────────│               │                           │
│     │                │               │                           │
│     │ "Move it to    │               │                           │
│     │  10 AM"        │               │                           │
│     │───────────────>│──────────────>│ Parse: reschedule        │
│     │                │               │ "it" = standup            │
│     │                │               │ Execute action            │
│     │                │<──────────────│ "Done. Standup moved to  │
│     │<───────────────│               │  10 AM, attendees notified│
└─────────────────────────────────────────────────────────────────┘
```

### Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOICE PIPELINE                                │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   Mic    │───>│  VAD     │───>│  ASR     │───>│  NLU     │  │
│  │ Capture  │    │ (Voice   │    │ (Speech  │    │ (Intent  │  │
│  │          │    │ Activity)│    │ to Text) │    │ Parsing) │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                        │         │
│                                                        ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Speaker  │<───│  TTS     │<───│ Response │<───│ Agent    │  │
│  │ Output   │    │ (OpenAI  │    │ Format   │    │ Process  │  │
│  │          │    │  4o)     │    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
│  Latency Budget:                                                │
│  • VAD detection: <50ms                                         │
│  • ASR streaming: <200ms (first word)                           │
│  • Agent processing: <500ms                                     │
│  • TTS first byte: <300ms                                       │
│  • Total perceived: <800ms                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Voice Activity Detection (VAD)

| Parameter              | Value    | Notes                     |
| ---------------------- | -------- | ------------------------- |
| Silence threshold      | 300ms    | Shorter = more responsive |
| Speech threshold       | 50ms     | Minimum speech to trigger |
| Background noise floor | Adaptive | Calibrated on startup     |
| Echo cancellation      | Required | Prevent feedback loops    |

### OpenAI 4o Integration

**Voice-to-Voice Mode:**

- Single API call handles speech → text → reasoning → speech
- Maintains conversation context
- Natural prosody and emotion in output

**API Configuration:**

```json
{
  "model": "gpt-4o-audio-preview",
  "modalities": ["text", "audio"],
  "audio": {
    "voice": "{user_selected_voice}",
    "format": "pcm16"
  },
  "messages": [
    { "role": "system", "content": "{personality_prompt}" },
    {
      "role": "user",
      "content": [
        { "type": "input_audio", "input_audio": { "data": "{base64_audio}" } }
      ]
    }
  ],
  "stream": true
}
```

### Audio Specifications

| Spec        | Input         | Output          |
| ----------- | ------------- | --------------- |
| Sample Rate | 16kHz         | 24kHz           |
| Bit Depth   | 16-bit        | 16-bit          |
| Channels    | Mono          | Mono            |
| Format      | PCM / Opus    | PCM / AAC       |
| Codec       | Opus (mobile) | AAC (streaming) |

### Latency Targets

| Metric                   | Target | Acceptable | Degraded |
| ------------------------ | ------ | ---------- | -------- |
| Time to first audio byte | <800ms | <1200ms    | <2000ms  |
| End-to-end response      | <2s    | <3s        | <5s      |
| Interruption detection   | <100ms | <200ms     | <500ms   |
| Wake word detection      | <300ms | <500ms     | <800ms   |

### UI During Voice

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                      ┌─────────────┐                            │
│                      │             │                            │
│                      │   [Avatar]  │                            │
│                      │  Listening  │                            │
│                      │             │                            │
│                      └─────────────┘                            │
│                                                                  │
│                   ●●●○○ (audio level indicator)                 │
│                                                                  │
│              "What's my first meeting today?"                   │
│                    (live transcription)                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    🎤 Listening...                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│           [Type instead]              [Cancel]                  │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Voice conversation works on Flutter mobile, desktop, web
- [ ] First audio byte <800ms on WiFi
- [ ] First audio byte <1500ms on LTE
- [ ] Conversation continues without re-activation for 30s
- [ ] Audio quality ≥16kHz output
- [ ] Works with Bluetooth headphones
- [ ] Works with speakerphone
- [ ] Echo cancellation prevents feedback

---

## 4.3 VOI-02: Wake Word Activation

### Description

VA activates when employee speaks their chosen wake word (VA's name), enabling hands-free initiation.

### User Story

> As a field technician with dirty hands, I want to activate my VA by saying its name without touching my phone.

### Wake Word Options

| Type            | Example         | Notes                  |
| --------------- | --------------- | ---------------------- |
| VA Name         | "Alex"          | Most natural           |
| Hey + Name      | "Hey Alex"      | More distinct          |
| Dartwing + Name | "Dartwing Alex" | Corporate environments |
| Custom phrase   | "Yo Chief"      | User-defined           |

### Wake Word Engine

**On-Device Processing:**

- Model runs locally (Google Gems / TensorFlow Lite)
- No audio sent to cloud until wake word detected
- Privacy-preserving: only sends speech after activation

**Detection Pipeline:**

```
Audio Stream → VAD → Wake Word Model → Confidence Score → Threshold Check
                                              │
                                              ▼
                                   ≥0.85: Activate VA
                                   0.70-0.85: "Did you say Alex?"
                                   <0.70: Ignore
```

### Wake Word Training

**Personalized Model (Optional):**

1. User records wake word 5 times
2. Model fine-tunes to user's voice
3. Improved accuracy in noisy environments
4. Stored locally, never uploaded

### False Positive Handling

| Scenario              | Detection                  | Response                |
| --------------------- | -------------------------- | ----------------------- |
| TV says "Alex"        | Different voice profile    | Ignore                  |
| Coworker says "Alex"  | Not primary user           | Optional: "Not my Alex" |
| Ambient noise         | Below confidence threshold | Ignore                  |
| Partial match "Alexa" | Blacklisted similar words  | Ignore                  |

### Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│                   WAKE WORD SETTINGS                             │
│                                                                  │
│  Wake Phrase: [Hey Alex                              ]          │
│                                                                  │
│  Sensitivity:                                                    │
│  [━━━━━━━━━●━━━━━] Higher (more activations)                    │
│                                                                  │
│  ☑ Train to my voice (improves accuracy)                        │
│      Status: Trained ✓ [Retrain]                                │
│                                                                  │
│  ☐ Allow activation during calls                                 │
│  ☑ Play confirmation sound on activation                        │
│  ☐ Require follow-up within 5 seconds                           │
│                                                                  │
│  Privacy: Wake word detection runs entirely on your device.     │
│           Audio is only sent to AI after activation.            │
└─────────────────────────────────────────────────────────────────┘
```

### Platform-Specific Behavior

| Platform                 | Background Wake | Notes                     |
| ------------------------ | --------------- | ------------------------- |
| Flutter Mobile (iOS)     | Limited         | Siri shortcut integration |
| Flutter Mobile (Android) | Yes             | Foreground service        |
| Flutter Desktop          | Yes             | Always-on option          |
| Frappe Web               | No              | Requires click to start   |

### Acceptance Criteria

- [ ] Wake word detected in <300ms
- [ ] False positive rate <1 per hour in quiet environment
- [ ] False positive rate <3 per hour in noisy environment
- [ ] Works up to 3 meters from device
- [ ] Personalized training improves accuracy by 20%+
- [ ] Zero audio sent to cloud before activation

---

## 4.4 VOI-03: Interruption Handling

### Description

Employee can interrupt VA mid-response, and VA gracefully stops speaking to listen.

### User Story

> As an employee, I want to cut off my VA when I realize I need to ask something different, just like I would a human.

### Interruption Types

| Type                  | Detection                 | VA Response               |
| --------------------- | ------------------------- | ------------------------- |
| **Barge-in**          | Speech while VA talking   | Stop immediately, listen  |
| **Course correction** | "Actually..." / "Wait..." | Stop, acknowledge, listen |
| **Urgency**           | Raised voice              | Stop, "What's urgent?"    |
| **Dismissal**         | "Never mind" / "Stop"     | Stop, confirm, reset      |

### Interruption Flow

```
VA: "Your first meeting today is the team standup at 9 AM,
     followed by the—"

Employee: "Actually—"

VA: [stops within 100ms]
VA: "Go ahead."

Employee: "Cancel the standup."

VA: "Canceling the team standup at 9 AM. Should I notify
     the other attendees?"
```

### Technical Implementation

**Simultaneous Listen + Speak:**

- Full-duplex audio: mic active during playback
- Echo cancellation removes VA's own voice
- VAD detects user speech over VA output

**State Machine:**

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONVERSATION STATE MACHINE                       │
│                                                                  │
│   ┌──────────┐      Wake word      ┌──────────┐                │
│   │  IDLE    │ ─────────────────>  │ LISTENING│                │
│   └──────────┘                     └──────────┘                │
│        ▲                                 │                      │
│        │                                 │ Speech complete      │
│        │                                 ▼                      │
│        │                           ┌──────────┐                │
│        │                           │PROCESSING│                │
│        │                           └──────────┘                │
│        │                                 │                      │
│        │                                 │ Response ready       │
│        │                                 ▼                      │
│        │    Timeout              ┌──────────┐                  │
│        │<─────────────────────── │ SPEAKING │                  │
│        │                         └──────────┘                  │
│        │                                │                       │
│        │                                │ User interrupts       │
│        │                                ▼                       │
│        │                         ┌──────────┐                  │
│        └─────────────────────────│INTERRUPTED│                 │
│                  Timeout         └──────────┘                  │
│                                        │                        │
│                                        │ Listen for new input   │
│                                        ▼                        │
│                                  ┌──────────┐                   │
│                                  │ LISTENING│ (loop)            │
│                                  └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Interruption Responses by Personality

| Personality  | Interruption Response     |
| ------------ | ------------------------- |
| Professional | "Of course."              |
| Friendly     | "Oh! Go ahead."           |
| Playful      | "Oops, sorry! What's up?" |
| Military     | "Copy. Go ahead."         |
| Minimal      | [silence, just listens]   |

### Acceptance Criteria

- [ ] Interruption detected within 100ms
- [ ] VA stops audio within 200ms of detection
- [ ] Partial response saved for context
- [ ] "Never mind" cancels entire interaction
- [ ] Echo cancellation prevents self-triggering
- [ ] Works with speakerphone and headphones

---

## 4.5 VOI-04: Multi-Turn Dialogue

### Description

VA maintains context across multiple conversation turns without requiring repetition.

### User Story

> As an employee, I want to have a natural back-and-forth conversation without re-explaining context every time.

### Context Retention

**Same Session:**

```
Turn 1: "What meetings do I have tomorrow?"
VA:     "You have 3 meetings: standup at 9, 1:1 with Lisa at 11,
         and project review at 2."

Turn 2: "Move the second one to 3 PM"
VA:     "Moving your 1:1 with Lisa to 3 PM. Done."
         (Understood "second one" = Lisa 1:1)

Turn 3: "Actually make it 3:30"
VA:     "Updated to 3:30 PM."
         (Understood "it" = same meeting)

Turn 4: "And add Sarah to it"
VA:     "Added Sarah to your 1:1 with Lisa at 3:30."
         (Maintained full context)
```

**Cross-Session Memory:**

```
Yesterday: "I'm working on the Henderson proposal"
VA:        Logged to memory: current_project = Henderson proposal

Today:     "How's my proposal going?"
VA:        "The Henderson proposal is at 60% complete.
            You have 2 sections left to write."
           (Retrieved from memory)
```

### Context Window Management

| Context Type     | Retention        | Example                          |
| ---------------- | ---------------- | -------------------------------- |
| Immediate (turn) | Current response | Pronouns, "this", "that"         |
| Conversation     | 30 minutes       | Topic threads, decisions         |
| Session          | Until app close  | Tasks started, preferences shown |
| Persistent       | Forever          | User preferences, history        |

### Anaphora Resolution

| User Says           | VA Understands                       |
| ------------------- | ------------------------------------ |
| "Move it"           | Most recent meeting/event mentioned  |
| "Call them"         | Most recent person/company mentioned |
| "The first one"     | First item in last list given        |
| "Same as last time" | Retrieved from action history        |
| "My usual"          | Learned preference pattern           |

### Conversation Threads

**Parallel Threads:**

```
Thread A: Scheduling
├── "Book a meeting with Tom"
├── "Make it Tuesday"
└── "Add an agenda about Q4"

Thread B: Expenses (started mid-conversation)
├── "By the way, submit my lunch receipt"
└── "It was at Panera"

Thread A: (continued)
├── "Send Tom the invite"
└── VA sends with full context
```

**Thread Detection:**

- "By the way" → new thread
- "Going back to" → return to previous thread
- "About that meeting" → explicit thread reference
- Pronoun clarity → infer thread from context

### UI: Conversation History

```
┌─────────────────────────────────────────────────────────────────┐
│  CONVERSATION WITH ALEX                                          │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  You (2:15 PM)                                                   │
│  "What meetings do I have tomorrow?"                             │
│                                                                  │
│  Alex (2:15 PM)                                                  │
│  "You have 3 meetings: standup at 9, 1:1 with Lisa at 11,       │
│   and project review at 2."                                      │
│                                                                  │
│  You (2:15 PM)                                                   │
│  "Move the second one to 3 PM"                                   │
│                                                                  │
│  Alex (2:15 PM)                                                  │
│  "Moving your 1:1 with Lisa to 3 PM."                           │
│  ✓ Calendar updated                                              │
│                                                                  │
│  You (2:16 PM)                                                   │
│  "And add Sarah"                                                 │
│                                                                  │
│  Alex (2:16 PM)                                                  │
│  "Added Sarah Martinez to your 1:1 with Lisa at 3 PM."          │
│  ✓ Invite sent to Sarah                                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  🎤 [Listening...]                              [Type instead]   │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Pronouns resolved correctly >95% of time
- [ ] "The first/second/third one" works for lists
- [ ] Context maintained for 30+ minutes of idle
- [ ] "By the way" correctly starts new thread
- [ ] Cross-session memory retrieves relevant context
- [ ] Conversation history viewable and searchable

---

## 4.6 VOI-05: Voice Commands & Shortcuts

### Description

Quick voice commands for common actions without full conversational flow.

### User Story

> As a power user, I want shortcut commands for frequent actions so I can work faster.

### Command Categories

**Navigation:**
| Command | Action |
|---------|--------|
| "Go to calendar" | Opens calendar view |
| "Show my tasks" | Opens task list |
| "Open [app name]" | Opens Frappe app |
| "Back" | Previous screen |

**Quick Actions:**
| Command | Action |
|---------|--------|
| "Clock in" | Start attendance |
| "Clock out" | End attendance |
| "Start break" | Log break start |
| "End break" | Log break end |
| "New expense" | Start expense entry |
| "Quick note: [text]" | Creates note |

**Information:**
| Command | Action |
|---------|--------|
| "Time" | Current time |
| "Weather" | Local weather |
| "My hours this week" | Timesheet summary |
| "PTO balance" | Leave balance |

**Communication:**
| Command | Action |
|---------|--------|
| "Call [name]" | Initiates call via dartwing_fone |
| "Text [name]: [message]" | Sends SMS |
| "Email [name] about [topic]" | Drafts email |

### Custom Shortcuts

Users can create personal shortcuts:

```
┌─────────────────────────────────────────────────────────────────┐
│                   MY VOICE SHORTCUTS                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ "Morning routine"                                          │ │
│  │ → Clock in + Show today's schedule + Read first 3 tasks    │ │
│  │                                               [Edit] [Del] │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ "On my way"                                                │ │
│  │ → Notify next customer ETA + Start travel time tracking    │ │
│  │                                               [Edit] [Del] │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ "End of day"                                               │ │
│  │ → Clock out + Submit pending expenses + Show tomorrow      │ │
│  │                                               [Edit] [Del] │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│                        [ + Add Shortcut ]                        │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] 20+ built-in commands at launch
- [ ] Custom shortcuts (up to 20)
- [ ] Shortcuts executable in <500ms
- [ ] "Help" or "What can you do?" lists commands
- [ ] Commands work mid-conversation

---

## 4.7 VOI-06: Voice Transcription Display

### Description

Real-time display of both user speech and VA responses as text, with corrections enabled.

### User Story

> As an employee, I want to see what my VA heard and said so I can catch misunderstandings.

### Transcription UI

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  You: "Schedule a meeting with John tomorrow at [three]"        │
│                                             ^^^^^^^^             │
│                                       [Correct: three / tree]   │
│                                                                  │
│  Alex: "I'll schedule a meeting with John tomorrow at 3 PM.     │
│         Which John - John Smith or John Davis?"                 │
│                                                                  │
│  You: "Smith"                                                    │
│                                                                  │
│  Alex: "Done. Meeting with John Smith tomorrow at 3 PM."        │
│         ✓ Calendar event created                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Features

| Feature                     | Description                      |
| --------------------------- | -------------------------------- |
| **Live transcription**      | Words appear as spoken           |
| **Confidence highlighting** | Low-confidence words highlighted |
| **Tap to correct**          | Fix misheard words               |
| **Learn from corrections**  | Improve ASR for user             |
| **Copy transcript**         | Export conversation              |
| **Hide transcript**         | Voice-only mode                  |

### Transcript Settings

| Setting                   | Options                               |
| ------------------------- | ------------------------------------- |
| Show transcript           | Always / On request / Never           |
| Show VA response          | Text + Voice / Voice only / Text only |
| Highlight uncertain words | Yes / No                              |
| Auto-scroll               | Yes / No                              |
| Font size                 | Small / Medium / Large                |

### Acceptance Criteria

- [ ] Transcription latency <200ms behind speech
- [ ] Tap-to-correct available for 10 seconds after utterance
- [ ] Corrections improve future accuracy
- [ ] Export transcript to text/PDF
- [ ] Works in all supported languages

---

## 4.8 VOI-07: Ambient Mode

### Description

VA listens continuously in background, ready to assist without wake word in specific contexts.

### User Story

> As a warehouse worker, I want my VA to hear everything and help proactively when I mention work stuff.

### Ambient Mode Contexts

| Context         | Behavior                                        |
| --------------- | ----------------------------------------------- |
| **Driving**     | Listens for requests, reads notifications aloud |
| **Meeting**     | Takes notes, tracks action items                |
| **Field work**  | Listens for job-related keywords                |
| **Home office** | Standard wake word required                     |

### Safety & Privacy

**Explicit Opt-In:**

- Must enable per-context
- Clear indicator when ambient listening active
- Audio processed locally until work-relevant detected
- Full conversation never stored unless actioned

**Visual Indicator:**

```
┌─────────────────────────────────────────────────────────────────┐
│  🔴 AMBIENT MODE ACTIVE                                          │
│                                                                  │
│  Alex is listening for work-related requests.                   │
│  Say "Alex, stop listening" to disable.                         │
│                                                                  │
│  Recent detections:                                              │
│  • 2:15 PM - "I need to call the Henderson client"              │
│    → Offered to dial                                            │
│  • 2:18 PM - "This part is broken"                              │
│    → Asked if should log equipment issue                        │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Explicit opt-in required
- [ ] Clear visual indicator when active
- [ ] Local processing for privacy
- [ ] Context-specific activation (driving vs office)
- [ ] "Stop listening" command always works
- [ ] No ambient mode for sensitive areas (HR, medical)

---

## 4.9 VOI-08: Voice Quality Adaptation

### Description

Automatically adjusts voice quality and processing based on network conditions and environment.

### User Story

> As a field worker in areas with poor signal, I want my VA to still work even if quality is reduced.

### Adaptation Levels

| Network              | Audio Quality   | Processing                    |
| -------------------- | --------------- | ----------------------------- |
| **Excellent** (WiFi) | 24kHz stereo    | Full cloud AI                 |
| **Good** (LTE)       | 16kHz mono      | Cloud AI                      |
| **Fair** (3G)        | 8kHz mono       | Cloud AI, longer latency      |
| **Poor** (Edge)      | 8kHz compressed | Local Gems for simple queries |
| **Offline**          | N/A             | Local Gems only               |

### Noise Adaptation

| Environment    | Processing                    |
| -------------- | ----------------------------- |
| Quiet office   | Minimal noise reduction       |
| Open office    | Moderate noise reduction      |
| Factory floor  | Aggressive noise reduction    |
| Moving vehicle | Wind/road noise cancellation  |
| Outdoors       | Environmental noise filtering |

### UI Feedback

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ⚠️ Limited connectivity                                         │
│                                                                  │
│  Alex is using local mode. Complex queries may not work.        │
│  Available: Clock in/out, simple lookups, notes                 │
│                                                                  │
│  [Continue with local mode]                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Automatic quality adjustment without user action
- [ ] Local mode for offline operation
- [ ] Noise cancellation adapts to environment
- [ ] Clear indication when degraded mode active
- [ ] Seamless transition as connectivity changes

---

## 4.10 VOI-09: Multilingual Voice

### Description

VA speaks and understands multiple languages, with per-user language preference and real-time translation.

### User Story

> As a bilingual employee, I want to speak to my VA in Spanish sometimes and English other times.

### Supported Languages (Launch)

| Language     | Speech Recognition | Voice Output |
| ------------ | ------------------ | ------------ |
| English (US) | ✓                  | ✓            |
| English (UK) | ✓                  | ✓            |
| Spanish      | ✓                  | ✓            |
| Mandarin     | ✓                  | ✓            |
| French       | ✓                  | ✓            |
| German       | ✓                  | ✓            |
| Japanese     | ✓                  | ✓            |
| Portuguese   | ✓                  | ✓            |

### Language Modes

| Mode               | Behavior                               |
| ------------------ | -------------------------------------- |
| **Fixed**          | Always use selected language           |
| **Auto-detect**    | Detect language per utterance          |
| **Code-switching** | Handle mixed language in same sentence |

### Translation Features

| Feature                   | Example                            |
| ------------------------- | ---------------------------------- |
| **Speak in X**            | "Say that in Spanish"              |
| **Translate document**    | "Translate this email to French"   |
| **Call with translation** | Real-time translation during calls |

### Acceptance Criteria

- [ ] 8 languages at launch
- [ ] Auto-detect language with >95% accuracy
- [ ] Code-switching for Spanish/English
- [ ] Voice output in selected language
- [ ] Translation available for all text fields

---

## 4.11 VOI-10: Voice Biometrics

### Description

Optional voice recognition to verify speaker identity before sensitive actions.

### User Story

> As a manager, I want my VA to verify it's really me before approving large expenses.

### Biometric Actions

| Action                 | Verification Level       |
| ---------------------- | ------------------------ |
| Clock in/out           | None (location verifies) |
| View calendar          | None                     |
| Submit expense <$100   | None                     |
| Submit expense >$100   | Voice verify             |
| Approve purchase order | Voice verify             |
| Access salary data     | Voice verify             |
| Send external message  | Optional verify          |

### Enrollment

1. User speaks 5 phrases
2. Voiceprint generated locally
3. Encrypted and stored
4. Never leaves device / org server

### Verification Flow

```
Employee: "Approve the equipment purchase"

VA: "That's a $5,000 purchase order. Please verify your identity.
     Say: 'I authorize this action'"

Employee: "I authorize this action"

VA: [Voiceprint match: 97% confidence]
    "Verified. Purchase order approved."
```

### Failure Handling

| Scenario            | Response                                              |
| ------------------- | ----------------------------------------------------- |
| Voice doesn't match | "I couldn't verify your voice. Try again or use PIN." |
| 3 failed attempts   | Lock action, notify IT                                |
| Different voice     | "That doesn't sound like you. Action blocked."        |

### Acceptance Criteria

- [ ] Voiceprint enrollment in <1 minute
- [ ] Verification in <2 seconds
- [ ] False rejection rate <3%
- [ ] False acceptance rate <0.1%
- [ ] PIN fallback always available
- [ ] Voiceprint stored encrypted, never uploaded

---

_Next: Section 5 - Sub-Agent System_

# Section 5: Sub-Agent System

## 5.1 Feature Group Overview

| ID     | Feature                  | Priority | Phase |
| ------ | ------------------------ | -------- | ----- |
| SUB-01 | Coordinator Agent        | P0       | Alpha |
| SUB-02 | HR Sub-Agent             | P0       | Alpha |
| SUB-03 | CRM Sub-Agent            | P0       | Alpha |
| SUB-04 | Operations Sub-Agent     | P0       | Alpha |
| SUB-05 | Knowledge Sub-Agent      | P0       | Alpha |
| SUB-06 | Calendar Sub-Agent       | P0       | Alpha |
| SUB-07 | Finance Sub-Agent        | P1       | Beta  |
| SUB-08 | Custom Sub-Agents        | P2       | GA    |
| SUB-09 | Sub-Agent Orchestration  | P0       | Alpha |
| SUB-10 | Sub-Agent Fallback Chain | P1       | Beta  |

---

## 5.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SUB-AGENT ARCHITECTURE                       │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   COORDINATOR AGENT                        │  │
│  │                   (GPT-4o / Claude 4)                      │  │
│  │                                                            │  │
│  │  • Personality layer                                       │  │
│  │  • Intent classification                                   │  │
│  │  • Context management                                      │  │
│  │  • Response synthesis                                      │  │
│  │  • Multi-agent orchestration                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              │ Routes to specialized agents      │
│                              ▼                                   │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐ │
│  │   HR    │   CRM   │   OPS   │  KNOW   │   CAL   │   FIN   │ │
│  │ Agent   │ Agent   │  Agent  │  Agent  │  Agent  │  Agent  │ │
│  │         │         │         │         │         │         │ │
│  │ Gems/   │ Gems/   │ Gems/   │ RAG +   │ Gems/   │ Gems/   │ │
│  │ Haiku   │ Haiku   │ Haiku   │ Embed   │ Haiku   │ Haiku   │ │
│  └────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘ │
│       │         │         │         │         │         │       │
│       ▼         ▼         ▼         ▼         ▼         ▼       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    FRAPPE ECOSYSTEM                      │    │
│  │  ┌───────┬───────┬───────┬───────┬───────┬───────────┐  │    │
│  │  │ HRMS  │ERPNext│  CRM  │Health │ Drive │ dartwing_ │  │    │
│  │  │       │       │       │       │       │ company   │  │    │
│  │  └───────┴───────┴───────┴───────┴───────┴───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5.3 SUB-01: Coordinator Agent

### Description

The main intelligence layer that receives all user requests, applies personality, routes to sub-agents, and synthesizes responses.

### User Story

> As an employee, I talk to one assistant that handles everything seamlessly, not multiple bots.

### Responsibilities

| Responsibility                | Description                                       |
| ----------------------------- | ------------------------------------------------- |
| **Intent Classification**     | Determine which sub-agent(s) to invoke            |
| **Context Management**        | Maintain conversation history and state           |
| **Personality Application**   | Apply user's personality profile to all responses |
| **Multi-Agent Orchestration** | Coordinate parallel or sequential sub-agent calls |
| **Response Synthesis**        | Combine sub-agent results into natural response   |
| **Fallback Handling**         | Handle cases where sub-agents can't help          |
| **Action Confirmation**       | Get user approval for important actions           |

### Model Configuration

| Scenario          | Model               | Rationale              |
| ----------------- | ------------------- | ---------------------- |
| Default           | GPT-4o              | Best voice + reasoning |
| Long documents    | Claude 4            | Larger context window  |
| Privacy-sensitive | Google Gems (local) | No cloud transmission  |
| Simple queries    | Claude Haiku        | Fast, cheap            |
| Cost optimization | Auto-select         | Route by complexity    |

### Intent Classification

```json
{
  "intents": [
    {
      "domain": "hr",
      "actions": [
        "pto_balance",
        "clock_in",
        "clock_out",
        "leave_request",
        "shift_schedule",
        "benefits",
        "payroll",
        "certification"
      ]
    },
    {
      "domain": "crm",
      "actions": [
        "customer_lookup",
        "deal_status",
        "lead_info",
        "contact_search",
        "ticket_status",
        "client_portal"
      ]
    },
    {
      "domain": "operations",
      "actions": [
        "dispatch_job",
        "task_status",
        "workflow_trigger",
        "form_submit",
        "resource_booking",
        "broadcast_alert"
      ]
    },
    {
      "domain": "knowledge",
      "actions": [
        "policy_lookup",
        "procedure_search",
        "document_find",
        "faq_answer",
        "training_material"
      ]
    },
    {
      "domain": "calendar",
      "actions": [
        "meeting_schedule",
        "meeting_reschedule",
        "availability_check",
        "appointment_book",
        "event_lookup"
      ]
    },
    {
      "domain": "finance",
      "actions": [
        "expense_submit",
        "expense_status",
        "invoice_lookup",
        "budget_check",
        "approval_request"
      ]
    },
    {
      "domain": "general",
      "actions": ["time", "weather", "calculator", "small_talk", "help"]
    }
  ]
}
```

### Coordinator Prompt Template

```
You are {va_name}, a personal AI assistant for {employee_name}.

PERSONALITY:
{personality_profile}

CURRENT CONTEXT:
- Time: {current_time} ({timezone})
- Location: {current_location}
- Active tasks: {active_tasks}
- Recent conversation: {recent_turns}

SUB-AGENTS AVAILABLE:
- HR: Leave, attendance, shifts, benefits, certifications
- CRM: Customers, deals, leads, tickets
- Operations: Jobs, tasks, workflows, forms
- Knowledge: Policies, procedures, documents
- Calendar: Meetings, appointments, availability
- Finance: Expenses, invoices, approvals

INSTRUCTIONS:
1. Classify the user's intent
2. Route to appropriate sub-agent(s)
3. Apply personality to response
4. Confirm destructive actions before executing
5. If uncertain, ask for clarification

USER REQUEST:
{user_message}
```

### Orchestration Patterns

**Sequential:**

```
User: "Book a meeting with John and send him the Henderson proposal"

Coordinator → Calendar Agent: Book meeting with John
           ← Result: Meeting booked for Tuesday 2 PM

Coordinator → Knowledge Agent: Find Henderson proposal
           ← Result: Document found at /proposals/henderson-v2.pdf

Coordinator → CRM Agent: Get John's email
           ← Result: john@client.com

Coordinator → Operations Agent: Send email with attachment
           ← Result: Email sent

Coordinator → User: "Done. I booked a meeting with John for Tuesday at 2 PM
                     and sent him the Henderson proposal."
```

**Parallel:**

```
User: "What's my PTO balance and how many deals closed this quarter?"

Coordinator → HR Agent: Get PTO balance        ─┐
           → CRM Agent: Get closed deals Q4     ─┼─ Parallel
                                                ─┘
           ← HR Result: 14 days
           ← CRM Result: 8 deals, $420K

Coordinator → User: "You have 14 days of PTO remaining,
                     and you've closed 8 deals this quarter worth $420,000."
```

### Acceptance Criteria

- [ ] Intent classification accuracy >95%
- [ ] Routes to correct sub-agent >98%
- [ ] Handles multi-intent requests
- [ ] Applies personality consistently
- [ ] Confirms destructive actions
- [ ] Graceful degradation when sub-agent fails

---

## 5.4 SUB-02: HR Sub-Agent

### Description

Specialized agent for HR-related queries and actions, integrated with Frappe HRMS and dartwing_company HR overlay.

### User Story

> As an employee, I want to ask about PTO, clock in, check my schedule, and manage HR tasks without logging into the HR system.

### Capabilities

| Capability     | Read | Write | Frappe DocType                    |
| -------------- | :--: | :---: | --------------------------------- |
| PTO Balance    |  ✓   |       | Leave Allocation                  |
| Leave Request  |  ✓   |   ✓   | Leave Application                 |
| Clock In/Out   |      |   ✓   | Attendance                        |
| Shift Schedule |  ✓   |       | Schedule Entry (dartwing)         |
| Shift Swap     |  ✓   |   ✓   | Shift Swap Request (dartwing)     |
| Benefits Info  |  ✓   |       | Employee, Custom                  |
| Pay Stubs      |  ✓   |       | Salary Slip                       |
| Certifications |  ✓   |       | Employee Certification (dartwing) |
| Training       |  ✓   |   ✓   | Training Event, Training Result   |
| Team Schedule  |  ✓   |       | Schedule Entry (manager only)     |

### Example Interactions

| User Says                           | Agent Action                 | Response                                             |
| ----------------------------------- | ---------------------------- | ---------------------------------------------------- |
| "How much PTO do I have?"           | Query Leave Allocation       | "You have 14 days remaining"                         |
| "Request Friday off"                | Create Leave Application     | "Leave request submitted for approval"               |
| "Clock me in"                       | Create Attendance with GPS   | "Clocked in at 8:47 AM"                              |
| "What's my schedule next week?"     | Query Schedule Entry         | Lists shifts                                         |
| "Can anyone swap my Tuesday shift?" | Create Shift Swap Request    | "Posted swap request, 3 eligible coworkers notified" |
| "When does my CPR cert expire?"     | Query Employee Certification | "Your CPR certification expires March 15, 2026"      |

### Tools Available

```json
{
  "hr_tools": [
    {
      "name": "get_leave_balance",
      "params": ["employee_id", "leave_type?"],
      "returns": { "remaining_days": "float", "used_days": "float" }
    },
    {
      "name": "submit_leave_request",
      "params": ["start_date", "end_date", "leave_type", "reason?"],
      "returns": { "request_id": "string", "status": "string" }
    },
    {
      "name": "clock_attendance",
      "params": ["action: in|out", "latitude?", "longitude?", "photo?"],
      "returns": { "attendance_id": "string", "time": "datetime" }
    },
    {
      "name": "get_schedule",
      "params": ["employee_id", "start_date", "end_date"],
      "returns": [{ "date": "date", "shift": "string", "location": "string" }]
    },
    {
      "name": "request_shift_swap",
      "params": ["schedule_entry_id", "reason?"],
      "returns": { "swap_request_id": "string", "eligible_count": "int" }
    },
    {
      "name": "get_certifications",
      "params": ["employee_id"],
      "returns": [
        { "cert_name": "string", "expiry": "date", "status": "string" }
      ]
    },
    {
      "name": "get_payslip",
      "params": ["employee_id", "period?"],
      "returns": { "gross": "float", "net": "float", "deductions": "object" }
    }
  ]
}
```

### Permissions

| Action              | Self | Direct Reports |   All   |
| ------------------- | :--: | :------------: | :-----: |
| View own PTO        |  ✓   |                |         |
| View team schedule  |  ✓   |       ✓        | HR only |
| Submit leave        |  ✓   |                |         |
| Approve leave       |      |       ✓        | HR only |
| View payslip        |  ✓   |                | HR only |
| Edit certifications |      |                | HR only |

### Acceptance Criteria

- [ ] All HRMS read operations work
- [ ] Leave request creates valid Leave Application
- [ ] Clock in/out creates valid Attendance with GPS
- [ ] Shift swap integrates with dartwing_company
- [ ] Respects HRMS permission model
- [ ] Manager can view team data

---

## 5.5 SUB-03: CRM Sub-Agent

### Description

Specialized agent for customer relationship management, integrated with Frappe CRM, ERPNext Sales, and dartwing_company CRM overlay.

### User Story

> As a sales rep, I want to look up customers, update deals, and manage client interactions through my VA.

### Capabilities

| Capability      | Read | Write | Frappe DocType             |
| --------------- | :--: | :---: | -------------------------- |
| Customer Lookup |  ✓   |       | Customer                   |
| Contact Search  |  ✓   |   ✓   | Contact                    |
| Lead Info       |  ✓   |   ✓   | Lead                       |
| Deal Status     |  ✓   |   ✓   | Deal                       |
| Activity Log    |  ✓   |   ✓   | CRM Activity               |
| Quote Create    |      |   ✓   | Quotation                  |
| Ticket Status   |  ✓   |   ✓   | Service Ticket (dartwing)  |
| Portal Access   |  ✓   |   ✓   | Portal Settings (dartwing) |
| Campaign Stats  |  ✓   |       | Campaign (dartwing)        |

### Example Interactions

| User Says                                   | Agent Action         | Response                                         |
| ------------------------------------------- | -------------------- | ------------------------------------------------ |
| "Look up Acme Corp"                         | Query Customer       | Customer details, recent activity                |
| "What deals are closing this month?"        | Query Deal           | List of deals with close dates                   |
| "Update the Chen deal to $50K"              | Update Deal          | "Updated Chen deal value to $50,000"             |
| "Log that I called Henderson"               | Create CRM Activity  | "Logged call with Henderson at 2:15 PM"          |
| "Create a quote for Acme, 10 units at $500" | Create Quotation     | "Quote QTN-2024-0142 created for $5,000"         |
| "What open tickets does Wilson have?"       | Query Service Ticket | Lists open support tickets                       |
| "How's our Growth campaign doing?"          | Query Campaign       | "47 leads, 12 qualified, 3 deals, $85K pipeline" |

### Tools Available

```json
{
  "crm_tools": [
    {
      "name": "search_customer",
      "params": ["query", "filters?"],
      "returns": [{ "name": "string", "contact": "string", "revenue": "float" }]
    },
    {
      "name": "get_customer_360",
      "params": ["customer_id"],
      "returns": {
        "info": "object",
        "deals": [],
        "tickets": [],
        "activity": []
      }
    },
    {
      "name": "search_leads",
      "params": ["query", "status?", "owner?"],
      "returns": [{ "name": "string", "company": "string", "score": "int" }]
    },
    {
      "name": "update_deal",
      "params": ["deal_id", "updates: object"],
      "returns": { "deal_id": "string", "updated_fields": [] }
    },
    {
      "name": "log_activity",
      "params": ["contact_id", "activity_type", "notes?"],
      "returns": { "activity_id": "string" }
    },
    {
      "name": "create_quotation",
      "params": ["customer_id", "items: []", "validity_days?"],
      "returns": { "quotation_id": "string", "total": "float" }
    },
    {
      "name": "get_tickets",
      "params": ["customer_id?", "status?", "assigned_to?"],
      "returns": [
        { "ticket_id": "string", "subject": "string", "priority": "string" }
      ]
    },
    {
      "name": "get_campaign_stats",
      "params": ["campaign_id"],
      "returns": {
        "leads": "int",
        "qualified": "int",
        "deals": "int",
        "revenue": "float"
      }
    }
  ]
}
```

### Acceptance Criteria

- [ ] Customer search returns relevant results
- [ ] Deal updates sync to Frappe CRM
- [ ] Activity logging creates proper CRM Activity
- [ ] Quotation creates valid ERPNext Quotation
- [ ] Respects CRM territory/assignment permissions
- [ ] Campaign stats pull from dartwing_company

---

## 5.6 SUB-04: Operations Sub-Agent

### Description

Specialized agent for operational tasks, integrated with dartwing_company operations features and ERPNext.

### User Story

> As a field worker, I want to manage my jobs, submit forms, and handle operational tasks through my VA.

### Capabilities

| Capability        | Read | Write | Frappe DocType               |
| ----------------- | :--: | :---: | ---------------------------- |
| Job Lookup        |  ✓   |       | Dispatch Job (dartwing)      |
| Job Status Update |      |   ✓   | Dispatch Job (dartwing)      |
| Form Submission   |      |   ✓   | Form Submission (dartwing)   |
| Task Management   |  ✓   |   ✓   | Task (ERPNext)               |
| Workflow Trigger  |      |   ✓   | Workflow Instance (dartwing) |
| Resource Booking  |  ✓   |   ✓   | Resource Booking (dartwing)  |
| Broadcast Alert   |      |   ✓   | Broadcast Alert (dartwing)   |
| Visitor Log       |  ✓   |   ✓   | Visitor Log (dartwing)       |

### Example Interactions

| User Says                                     | Agent Action                | Response                            |
| --------------------------------------------- | --------------------------- | ----------------------------------- |
| "What's my next job?"                         | Query Dispatch Job          | Job details, address, customer info |
| "I'm en route to the Henderson job"           | Update Dispatch Job status  | "Status updated, customer notified" |
| "Complete the job checklist"                  | Interactive form completion | Guides through form questions       |
| "Book the conference room for 2 PM"           | Create Resource Booking     | "Conference Room A booked 2-3 PM"   |
| "Send urgent alert: pipe burst at building 3" | Create Broadcast Alert      | "Alert sent to 12 team members"     |
| "Log visitor: John Smith from Acme"           | Create Visitor Log          | "Visitor checked in, badge #47"     |

### Tools Available

```json
{
  "ops_tools": [
    {
      "name": "get_my_jobs",
      "params": ["date?", "status?"],
      "returns": [
        {
          "job_id": "string",
          "customer": "string",
          "address": "string",
          "time": "datetime"
        }
      ]
    },
    {
      "name": "update_job_status",
      "params": ["job_id", "status", "notes?", "photos?"],
      "returns": { "job_id": "string", "new_status": "string" }
    },
    {
      "name": "submit_form",
      "params": ["form_id", "job_id?", "responses: object"],
      "returns": { "submission_id": "string" }
    },
    {
      "name": "get_tasks",
      "params": ["project?", "status?"],
      "returns": [{ "task_id": "string", "subject": "string", "due": "date" }]
    },
    {
      "name": "trigger_workflow",
      "params": ["workflow_id", "context: object"],
      "returns": { "instance_id": "string", "status": "string" }
    },
    {
      "name": "book_resource",
      "params": ["resource_id", "start_time", "end_time", "purpose?"],
      "returns": { "booking_id": "string" }
    },
    {
      "name": "send_broadcast",
      "params": ["message", "recipients: [] | 'all'", "priority"],
      "returns": { "alert_id": "string", "sent_count": "int" }
    },
    {
      "name": "log_visitor",
      "params": ["visitor_name", "company", "host", "purpose?"],
      "returns": { "visitor_id": "string", "badge": "string" }
    }
  ]
}
```

### Acceptance Criteria

- [ ] Job queries return relevant dispatch jobs
- [ ] Status updates notify customer via dartwing_fone
- [ ] Forms completed via voice with confirmation
- [ ] Resource booking prevents conflicts
- [ ] Broadcast alerts delivered via all channels
- [ ] Integrates with dartwing_company operations

---

## 5.7 SUB-05: Knowledge Sub-Agent

### Description

RAG-powered agent for answering questions from company knowledge base, policies, and documents.

### User Story

> As an employee, I want to ask questions about company policies and get accurate answers with sources.

### Capabilities

| Capability         | Source                       |
| ------------------ | ---------------------------- |
| Policy Q&A         | Knowledge Article (dartwing) |
| Procedure Lookup   | Knowledge Article (dartwing) |
| Document Search    | Frappe Drive                 |
| FAQ Answers        | Knowledge Article (dartwing) |
| Training Materials | Training Program (HRMS)      |
| Personal Notes     | Employee personal vault      |

### RAG Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE SUB-AGENT                           │
│                                                                  │
│  User Question                                                   │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Query        │ Expand query, generate embeddings              │
│  │ Processor    │                                               │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐     ┌─────────────────────────────────────┐   │
│  │ Vector       │────>│ OpenSearch                          │   │
│  │ Search       │     │ • knowledge_chunks (RAG index)      │   │
│  └──────────────┘     │ • drive_files (document index)      │   │
│       │               └─────────────────────────────────────┘   │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Context      │ Assemble top chunks, add metadata              │
│  │ Builder      │                                               │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Answer       │ Generate answer with citations                 │
│  │ Generator    │ (Claude / GPT-4o)                             │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  Response with sources                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Example Interactions

| User Says                              | Agent Action    | Response                                                            |
| -------------------------------------- | --------------- | ------------------------------------------------------------------- |
| "What's the expense policy for meals?" | RAG search      | "Meals up to $50 are reimbursable... [Source: Expense Policy v2.1]" |
| "How do I request FMLA leave?"         | RAG search      | Step-by-step procedure with form links                              |
| "Find the Henderson proposal"          | Document search | "Found 2 documents: Henderson-v2.pdf, Henderson-notes.docx"         |
| "What's the dress code?"               | RAG search      | Policy excerpt with source                                          |
| "Show me forklift safety training"     | Training search | Links to training materials                                         |

### Tools Available

```json
{
  "knowledge_tools": [
    {
      "name": "answer_question",
      "params": ["question", "sources?: []"],
      "returns": { "answer": "string", "sources": [], "confidence": "float" }
    },
    {
      "name": "search_documents",
      "params": ["query", "file_type?", "folder?"],
      "returns": [{ "name": "string", "path": "string", "snippet": "string" }]
    },
    {
      "name": "get_policy",
      "params": ["policy_name"],
      "returns": { "title": "string", "content": "string", "version": "string" }
    },
    {
      "name": "search_training",
      "params": ["topic"],
      "returns": [{ "program": "string", "materials": [], "required": "bool" }]
    },
    {
      "name": "get_personal_notes",
      "params": ["query"],
      "returns": [{ "title": "string", "content": "string", "created": "date" }]
    }
  ]
}
```

### Citation Format

```
"According to the Travel Policy (Section 3.2), flights must be booked
at least 14 days in advance for reimbursement.

📄 Source: Travel Policy v3.1, updated January 2025"
```

### Acceptance Criteria

- [ ] RAG answers accurate >90% of time
- [ ] Citations link to source documents
- [ ] Handles "I don't know" gracefully
- [ ] Personal vault searches employee's own docs
- [ ] Respects document permissions
- [ ] Indexes Knowledge Articles from dartwing_company

---

## 5.8 SUB-06: Calendar Sub-Agent

### Description

Specialized agent for calendar management, meeting scheduling, and appointment booking.

### User Story

> As an employee, I want to schedule meetings, check availability, and manage my calendar by voice.

### Capabilities

| Capability           | Read | Write | Integration                     |
| -------------------- | :--: | :---: | ------------------------------- |
| View Calendar        |  ✓   |       | Google Calendar / O365 / Frappe |
| Schedule Meeting     |      |   ✓   | Calendar + Email                |
| Reschedule           |      |   ✓   | Calendar + Notifications        |
| Cancel Meeting       |      |   ✓   | Calendar + Notifications        |
| Check Availability   |  ✓   |       | Multi-calendar lookup           |
| Book Appointment     |      |   ✓   | Appointment (dartwing)          |
| Resource Reservation |      |   ✓   | Resource Booking (dartwing)     |

### Example Interactions

| User Says                              | Agent Action                    | Response                                    |
| -------------------------------------- | ------------------------------- | ------------------------------------------- |
| "What's on my calendar today?"         | Query calendar                  | Lists meetings with times                   |
| "Schedule meeting with Lisa next week" | Find availability, create event | "Found Tuesday 2-3 PM works. Meeting sent." |
| "Am I free Friday afternoon?"          | Check availability              | "You're free 1-5 PM Friday"                 |
| "Move my 3 PM to 4 PM"                 | Update event, notify            | "Moved and attendees notified"              |
| "Cancel tomorrow's standup"            | Delete event, notify            | "Canceled, 5 people notified"               |
| "Book 30 min with Dr. Chen next week"  | Find appointment slots          | "Available: Mon 10 AM, Tue 2 PM, Wed 9 AM"  |

### Multi-Calendar Support

| Provider         | Read | Write | Availability |
| ---------------- | :--: | :---: | :----------: |
| Google Calendar  |  ✓   |   ✓   |      ✓       |
| Microsoft 365    |  ✓   |   ✓   |      ✓       |
| Frappe Calendar  |  ✓   |   ✓   |      ✓       |
| Apple Calendar   |  ✓   |   ✓   |      ✓       |
| CalDAV (generic) |  ✓   |   ✓   |      ✓       |

### Smart Scheduling

**Availability Algorithm:**

1. Get attendee calendars (with permission)
2. Find overlapping free slots
3. Prefer user's preferred meeting times (from personality)
4. Avoid back-to-back if user prefers buffer
5. Consider time zones
6. Rank by convenience score

**Conflict Handling:**

```
User: "Schedule meeting with Tom at 2 PM Tuesday"

VA: "You have a conflict - team standup is at 2 PM.
     Tom is free at 3 PM or Wednesday 2 PM.
     Which works better?"
```

### Tools Available

```json
{
  "calendar_tools": [
    {
      "name": "get_events",
      "params": ["start_date", "end_date", "calendar?"],
      "returns": [
        {
          "title": "string",
          "start": "datetime",
          "end": "datetime",
          "attendees": []
        }
      ]
    },
    {
      "name": "create_event",
      "params": [
        "title",
        "start",
        "end",
        "attendees?",
        "location?",
        "description?"
      ],
      "returns": { "event_id": "string", "calendar_link": "string" }
    },
    {
      "name": "update_event",
      "params": ["event_id", "updates: object", "notify_attendees?"],
      "returns": { "event_id": "string", "updated": "bool" }
    },
    {
      "name": "delete_event",
      "params": ["event_id", "notify_attendees?"],
      "returns": { "deleted": "bool" }
    },
    {
      "name": "find_availability",
      "params": [
        "attendees: []",
        "duration_minutes",
        "date_range",
        "preferences?"
      ],
      "returns": [{ "start": "datetime", "end": "datetime", "score": "float" }]
    },
    {
      "name": "book_appointment",
      "params": ["appointment_type", "provider?", "preferred_times?"],
      "returns": { "appointment_id": "string", "confirmed_time": "datetime" }
    }
  ]
}
```

### Acceptance Criteria

- [ ] Reads from Google/O365/Frappe calendars
- [ ] Creates events with proper invites
- [ ] Finds mutual availability for 2+ people
- [ ] Handles time zones correctly
- [ ] Reschedule notifies all attendees
- [ ] Integrates with dartwing_company appointments

---

## 5.9 SUB-07: Finance Sub-Agent

### Description

Specialized agent for expense management, invoices, budgets, and financial approvals.

### User Story

> As an employee, I want to submit expenses, check invoice status, and manage financial tasks through my VA.

### Capabilities

| Capability       | Read | Write | Frappe DocType                  |
| ---------------- | :--: | :---: | ------------------------------- |
| Submit Expense   |      |   ✓   | Expense Claim                   |
| Expense Status   |  ✓   |       | Expense Claim                   |
| Invoice Lookup   |  ✓   |       | Sales Invoice, Purchase Invoice |
| Payment Status   |  ✓   |       | Payment Entry                   |
| Budget Check     |  ✓   |       | Budget                          |
| Approval Request |  ✓   |   ✓   | Workflow Action                 |
| Corporate Card   |  ✓   |   ✓   | Expense Claim Item              |

### Example Interactions

| User Says                                | Agent Action                    | Response                                               |
| ---------------------------------------- | ------------------------------- | ------------------------------------------------------ |
| "Submit my lunch receipt for $15"        | OCR photo, create Expense Claim | "Expense submitted: Meals $15, pending approval"       |
| "What expenses am I waiting on?"         | Query Expense Claim             | "2 pending: $45 travel (3 days), $89 supplies (1 day)" |
| "What's the status of the Acme invoice?" | Query Sales Invoice             | "Invoice #1234 for $5,000 - Paid on Nov 15"            |
| "Can I spend $500 on marketing?"         | Check Budget                    | "Marketing budget: $2,340 remaining this quarter"      |
| "Approve the office supplies purchase"   | Update Workflow Action          | "Approved PO-2024-0089 for $234"                       |

### Receipt Processing

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECEIPT PROCESSING                            │
│                                                                  │
│  Photo Input                                                     │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ OCR          │ Extract text from receipt image               │
│  │ (Google Gems)│                                               │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Parser       │ Extract: vendor, date, amount, items          │
│  │              │                                               │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Categorizer  │ Auto-assign expense category                  │
│  │              │ Based on vendor, amount, user history         │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │ Validator    │ Check against policy limits                   │
│  │              │ Flag exceptions                               │
│  └──────────────┘                                               │
│       │                                                          │
│       ▼                                                          │
│  Expense Claim created with attachments                         │
└─────────────────────────────────────────────────────────────────┘
```

### Tools Available

```json
{
  "finance_tools": [
    {
      "name": "submit_expense",
      "params": [
        "amount",
        "category",
        "description",
        "receipt_image?",
        "date?"
      ],
      "returns": { "expense_id": "string", "status": "string" }
    },
    {
      "name": "get_expenses",
      "params": ["status?", "date_range?"],
      "returns": [
        {
          "expense_id": "string",
          "amount": "float",
          "status": "string",
          "days_pending": "int"
        }
      ]
    },
    {
      "name": "get_invoice",
      "params": ["invoice_id? | customer?"],
      "returns": {
        "invoice_id": "string",
        "amount": "float",
        "status": "string",
        "due_date": "date"
      }
    },
    {
      "name": "check_budget",
      "params": ["cost_center", "account?"],
      "returns": { "budget": "float", "spent": "float", "remaining": "float" }
    },
    {
      "name": "process_approval",
      "params": [
        "document_type",
        "document_id",
        "action: approve|reject",
        "comments?"
      ],
      "returns": { "status": "string" }
    },
    {
      "name": "get_pending_approvals",
      "params": [],
      "returns": [
        {
          "doc_type": "string",
          "doc_id": "string",
          "amount": "float",
          "requestor": "string"
        }
      ]
    }
  ]
}
```

### Acceptance Criteria

- [ ] Receipt OCR extracts vendor, amount, date
- [ ] Auto-categorization >85% accuracy
- [ ] Policy violations flagged before submission
- [ ] Approval workflow integrates with Frappe
- [ ] Budget checks against ERPNext Budget
- [ ] Corporate card reconciliation works

---

## 5.10 SUB-08: Custom Sub-Agents

### Description

Company-defined sub-agents for industry-specific or proprietary workflows.

### User Story

> As an HR admin, I want to create a custom onboarding agent that knows our specific processes.

### Custom Agent Configuration

```json
{
  "agent_id": "onboarding_agent",
  "name": "Onboarding Assistant",
  "description": "Helps new employees complete onboarding tasks",
  "model": "claude-3-haiku",
  "system_prompt": "You are an onboarding assistant for Acme Corp...",
  "tools": [
    {
      "name": "get_onboarding_tasks",
      "endpoint": "/api/method/custom.get_onboarding_tasks",
      "params": ["employee_id"]
    },
    {
      "name": "complete_task",
      "endpoint": "/api/method/custom.complete_task",
      "params": ["task_id", "data"]
    }
  ],
  "triggers": ["new employee", "onboarding", "first day", "getting started"],
  "permissions": ["Employee", "HR Manager"]
}
```

### Custom Agent Types

| Type                  | Use Case                         | Example               |
| --------------------- | -------------------------------- | --------------------- |
| **Workflow Agent**    | Guide through multi-step process | New hire onboarding   |
| **Domain Agent**      | Industry-specific knowledge      | Medical coding lookup |
| **Integration Agent** | Connect external system          | Salesforce sync       |
| **Compliance Agent**  | Regulatory Q&A                   | HIPAA questions       |

### Agent Builder UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   CUSTOM AGENT BUILDER                           │
│                                                                  │
│  Agent Name: [Safety Compliance Agent              ]             │
│                                                                  │
│  Description:                                                    │
│  [Answers safety questions and logs incidents      ]             │
│                                                                  │
│  Trigger Phrases:                                                │
│  [safety] [incident] [osha] [hazard] [injury]                   │
│  [+ Add]                                                         │
│                                                                  │
│  Knowledge Sources:                                              │
│  ☑ Safety Manual (Drive folder)                                 │
│  ☑ OSHA Guidelines (Knowledge Base)                             │
│  ☐ Incident History (Custom DocType)                            │
│                                                                  │
│  Tools:                                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ log_incident                                               │ │
│  │ POST /api/method/safety.log_incident                       │ │
│  │ Params: type, location, description, severity              │ │
│  └────────────────────────────────────────────────────────────┘ │
│  [+ Add Tool]                                                    │
│                                                                  │
│  Permissions: [HR Manager ▼] [Safety Officer ▼]                 │
│                                                                  │
│                   [Test Agent]    [Deploy Agent]                 │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Custom agents configurable via UI
- [ ] Support custom API endpoints as tools
- [ ] RAG over custom document folders
- [ ] Trigger phrase detection routes correctly
- [ ] Permission model respected
- [ ] Audit log for custom agent actions

---

## 5.11 SUB-09: Sub-Agent Orchestration

### Description

System for routing requests to appropriate sub-agents and coordinating multi-agent responses.

### Orchestration Modes

**Single Agent:**

```
User: "What's my PTO balance?"
Coordinator → HR Agent → "14 days"
```

**Sequential:**

```
User: "Book meeting with the Henderson contact"
Coordinator → CRM Agent: Who is Henderson contact? → John Smith
           → Calendar Agent: Book with John Smith → Done
```

**Parallel:**

```
User: "Morning briefing"
Coordinator → HR Agent: Today's schedule      ─┐
           → CRM Agent: Deal updates          ─┼─ Parallel
           → Operations Agent: Pending tasks  ─┘
           → Synthesize: "Good morning! Here's your day..."
```

**Fallback:**

```
User: "What's our policy on pets in the office?"
Coordinator → Knowledge Agent: No results
           → Custom Agent (Company FAQ): No results
           → Coordinator: "I couldn't find a pet policy.
                          Want me to ask HR to clarify?"
```

### Routing Logic

```python
def route_request(user_message, context):
    # 1. Intent classification
    intent = classify_intent(user_message)

    # 2. Determine required agents
    agents = []
    if intent.domain == "hr":
        agents.append("hr_agent")
    if intent.domain == "crm":
        agents.append("crm_agent")
    # ... etc

    # 3. Check for multi-domain
    if len(agents) > 1:
        mode = "parallel" if agents_independent(agents) else "sequential"

    # 4. Check for custom agent triggers
    for custom in get_custom_agents():
        if matches_trigger(user_message, custom.triggers):
            agents.append(custom.agent_id)

    # 5. Execute
    if mode == "parallel":
        results = parallel_execute(agents, user_message, context)
    else:
        results = sequential_execute(agents, user_message, context)

    # 6. Synthesize response
    return synthesize(results, personality)
```

### Acceptance Criteria

- [ ] Routes to correct agent(s) >98%
- [ ] Parallel execution where possible
- [ ] Sequential chains maintain context
- [ ] Fallback chain tries alternatives
- [ ] Custom agents integrated into routing

---

## 5.12 SUB-10: Sub-Agent Fallback Chain

### Description

Graceful degradation when primary sub-agent can't fulfill request.

### Fallback Strategy

| Level | Action                                |
| ----- | ------------------------------------- |
| 1     | Primary sub-agent attempts            |
| 2     | Alternative sub-agent (if applicable) |
| 3     | Knowledge base search                 |
| 4     | Web search (if enabled)               |
| 5     | Admit inability, offer alternatives   |

### Fallback Examples

**HR → Knowledge:**

```
User: "What's the bereavement leave policy?"
HR Agent: No specific tool for this
Knowledge Agent: Found in Employee Handbook, Section 8.3
Response: "According to the Employee Handbook, bereavement leave is..."
```

**CRM → Operations → Human:**

```
User: "Update the Henderson contract terms"
CRM Agent: Can view but not edit contracts
Operations Agent: No contract editing capability
Response: "I can't edit contracts directly. Should I create a task
          for Legal to update the Henderson terms?"
```

### Acceptance Criteria

- [ ] Fallback chain tries all relevant options
- [ ] Clear explanation when can't help
- [ ] Offers alternative paths (human, task, etc.)
- [ ] Logs fallback for improvement

---

_Next: Section 6 - Memory & Context Features_

# Section 6: Memory & Context Features

## 6.1 Feature Group Overview

| ID     | Feature                   | Priority | Phase |
| ------ | ------------------------- | -------- | ----- |
| MEM-01 | Conversation History      | P0       | Alpha |
| MEM-02 | User Preferences Memory   | P0       | Alpha |
| MEM-03 | Action History            | P0       | Alpha |
| MEM-04 | Contextual Awareness      | P1       | Beta  |
| MEM-05 | Proactive Suggestions     | P1       | Beta  |
| MEM-06 | Learning from Corrections | P1       | Beta  |
| MEM-07 | Cross-Session Memory      | P0       | Alpha |
| MEM-08 | Memory Privacy Controls   | P0       | Alpha |

---

## 6.2 Memory Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY ARCHITECTURE                           │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MEMORY LAYERS                           │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │  IMMEDIATE  │  │   SESSION   │  │ PERSISTENT  │       │  │
│  │  │  (Turn)     │  │  (Convo)    │  │  (Forever)  │       │  │
│  │  │             │  │             │  │             │       │  │
│  │  │ • Pronouns  │  │ • Topic     │  │ • Prefs     │       │  │
│  │  │ • References│  │ • Decisions │  │ • History   │       │  │
│  │  │ • Lists     │  │ • Tasks     │  │ • Patterns  │       │  │
│  │  │             │  │ • State     │  │ • Facts     │       │  │
│  │  │ TTL: 30s    │  │ TTL: 30min  │  │ TTL: ∞      │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MEMORY STORES                           │  │
│  │                                                            │  │
│  │  ┌─────────────────┐  ┌─────────────────────────────────┐ │  │
│  │  │ Redis           │  │ MariaDB / PostgreSQL            │ │  │
│  │  │                 │  │                                 │ │  │
│  │  │ • Session state │  │ • VA Memory (DocType)           │ │  │
│  │  │ • Conversation  │  │ • VA Conversation Log           │ │  │
│  │  │   context       │  │ • VA Action History             │ │  │
│  │  │ • TTL managed   │  │ • User Preferences              │ │  │
│  │  └─────────────────┘  └─────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ OpenSearch (Vector Store)                           │  │  │
│  │  │                                                     │  │  │
│  │  │ • Semantic memory (embedded facts)                  │  │  │
│  │  │ • Conversation embeddings (for retrieval)           │  │  │
│  │  │ • Action patterns (for suggestions)                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6.3 MEM-01: Conversation History

### Description

Full history of conversations between employee and VA, searchable and referenceable.

### User Story

> As an employee, I want my VA to remember what we talked about yesterday so I don't have to repeat myself.

### Data Model

```json
{
  "doctype": "VA Conversation",
  "fields": [
    { "fieldname": "conversation_id", "fieldtype": "Data", "unique": true },
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    { "fieldname": "started_at", "fieldtype": "Datetime" },
    { "fieldname": "ended_at", "fieldtype": "Datetime" },
    {
      "fieldname": "platform",
      "fieldtype": "Select",
      "options": "Mobile\nDesktop\nWeb"
    },
    { "fieldname": "turn_count", "fieldtype": "Int" },
    { "fieldname": "summary", "fieldtype": "Text" },
    { "fieldname": "topics", "fieldtype": "JSON" },
    { "fieldname": "actions_taken", "fieldtype": "JSON" }
  ]
}
```

```json
{
  "doctype": "VA Conversation Turn",
  "fields": [
    {
      "fieldname": "conversation",
      "fieldtype": "Link",
      "options": "VA Conversation"
    },
    { "fieldname": "turn_number", "fieldtype": "Int" },
    {
      "fieldname": "role",
      "fieldtype": "Select",
      "options": "User\nAssistant\nSystem"
    },
    { "fieldname": "content", "fieldtype": "Long Text" },
    { "fieldname": "audio_url", "fieldtype": "Data" },
    { "fieldname": "timestamp", "fieldtype": "Datetime" },
    { "fieldname": "sub_agent", "fieldtype": "Data" },
    { "fieldname": "tools_called", "fieldtype": "JSON" },
    { "fieldname": "sentiment", "fieldtype": "Float" },
    {
      "fieldname": "feedback",
      "fieldtype": "Select",
      "options": "None\nPositive\nNegative"
    }
  ]
}
```

### Conversation Summary Generation

After each conversation ends (30 min idle or explicit close):

```
Conversation with Alex - Nov 28, 2025

SUMMARY:
Marcus checked his schedule for the day (8 jobs), submitted a lunch
expense ($14.50), and asked about his certification renewal.

TOPICS:
• Schedule/Jobs (3 turns)
• Expenses (2 turns)
• Certifications (1 turn)

ACTIONS TAKEN:
✓ Retrieved daily schedule
✓ Submitted expense claim EXP-2024-0892
✓ Looked up CPR certification (expires March 15)

DECISIONS:
• Will schedule CPR renewal class this week
```

### Search Capabilities

| Search Type | Example Query                                 |
| ----------- | --------------------------------------------- |
| Keyword     | "Henderson proposal"                          |
| Date range  | "Last week's conversations"                   |
| Topic       | "All talks about expenses"                    |
| Action      | "When did I submit expenses?"                 |
| Semantic    | "What did we discuss about the Chicago trip?" |

### UI: Conversation History

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONVERSATION HISTORY                           │
│                                                                  │
│  🔍 [Search conversations...                              ]      │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  TODAY                                                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2:15 PM - Schedule & Expenses                              │ │
│  │ Checked schedule, submitted lunch expense                  │ │
│  │ 6 turns • ✓ 2 actions                            [Open]    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 8:30 AM - Morning Briefing                                 │ │
│  │ Daily schedule review, weather update                      │ │
│  │ 4 turns • ✓ 1 action                             [Open]    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  YESTERDAY                                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 4:45 PM - Henderson Project                                │ │
│  │ Found proposal, discussed timeline, booked meeting         │ │
│  │ 12 turns • ✓ 3 actions                           [Open]    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│                       [Load More]                                │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] All conversations stored with full turns
- [ ] Auto-summary generated after conversation ends
- [ ] Search by keyword, date, topic works
- [ ] Conversation referenceable: "Remember yesterday's Henderson talk?"
- [ ] Export conversation to text/PDF
- [ ] Retention configurable (default: 1 year)

---

## 6.4 MEM-02: User Preferences Memory

### Description

Long-term memory of user preferences, habits, and personal information shared with VA.

### User Story

> As an employee, I want my VA to remember that I prefer morning meetings and always book Delta flights.

### Preference Categories

| Category          | Examples                                               |
| ----------------- | ------------------------------------------------------ |
| **Communication** | "I prefer text over calls", "Email me summaries"       |
| **Scheduling**    | "No meetings before 10 AM", "Buffer between meetings"  |
| **Travel**        | "Prefer Delta", "Window seat", "No red-eyes"           |
| **Work Style**    | "Don't interrupt during focus time", "Brief responses" |
| **Personal**      | "Birthday: March 15", "Vegetarian", "Kids' names"      |
| **Finance**       | "Round up expenses", "Categorize Uber as travel"       |

### Preference Learning

**Explicit:**

```
User: "Always book me window seats"
VA: [Stores preference: travel.seat_preference = "window"]
VA: "Got it! I'll always look for window seats when booking flights."
```

**Implicit (with confirmation):**

```
VA: "I noticed you've booked Delta for your last 5 trips.
     Should I make Delta your default airline?"
User: "Yes"
VA: [Stores preference: travel.preferred_airline = "Delta"]
```

### Preference Data Model

```json
{
  "doctype": "VA User Preference",
  "fields": [
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "category",
      "fieldtype": "Select",
      "options": "Communication\nScheduling\nTravel\nWork Style\nPersonal\nFinance\nCustom"
    },
    { "fieldname": "key", "fieldtype": "Data" },
    { "fieldname": "value", "fieldtype": "JSON" },
    {
      "fieldname": "source",
      "fieldtype": "Select",
      "options": "Explicit\nLearned\nImported"
    },
    { "fieldname": "confidence", "fieldtype": "Float" },
    { "fieldname": "last_used", "fieldtype": "Datetime" },
    { "fieldname": "use_count", "fieldtype": "Int" }
  ]
}
```

### Preference Application

When VA takes action, it checks relevant preferences:

```python
def book_flight(employee, destination, date):
    prefs = get_preferences(employee, category="travel")

    search_params = {
        "destination": destination,
        "date": date,
        "airline": prefs.get("preferred_airline"),
        "seat": prefs.get("seat_preference"),
        "class": prefs.get("travel_class", "economy"),
        "avoid_redeye": prefs.get("no_redeyes", True)
    }

    results = search_flights(**search_params)
    return results
```

### UI: Preference Management

```
┌─────────────────────────────────────────────────────────────────┐
│                   MY PREFERENCES                                 │
│                                                                  │
│  Alex uses these to personalize your experience:                │
│                                                                  │
│  SCHEDULING                                                      │
│  ├─ No meetings before 10 AM                           [Edit]   │
│  ├─ 15-minute buffer between meetings                  [Edit]   │
│  └─ Prefer Tuesday/Thursday for external              [Edit]    │
│                                                                  │
│  TRAVEL                                                          │
│  ├─ Preferred airline: Delta                          [Edit]    │
│  ├─ Seat preference: Window                           [Edit]    │
│  └─ Hotel chain: Marriott                             [Edit]    │
│                                                                  │
│  COMMUNICATION                                                   │
│  ├─ Brief responses preferred                         [Edit]    │
│  └─ Send daily summary at 6 PM                        [Edit]    │
│                                                                  │
│  PERSONAL                                                        │
│  ├─ Birthday: March 15                                [Edit]    │
│  └─ Dietary: Vegetarian                               [Edit]    │
│                                                                  │
│  [+ Add Preference]                     [Clear All]              │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Explicit preferences stored immediately
- [ ] Implicit learning with confirmation
- [ ] Preferences applied automatically
- [ ] Preferences editable/deletable
- [ ] Confidence scoring for learned preferences
- [ ] Decay unused preferences over time

---

## 6.5 MEM-03: Action History

### Description

Complete log of all actions VA has taken on behalf of the employee.

### User Story

> As an employee, I want to see everything my VA has done so I can verify and trust it.

### Action Types

| Action Type | Examples                                       |
| ----------- | ---------------------------------------------- |
| **Read**    | Looked up calendar, checked PTO balance        |
| **Create**  | Created meeting, submitted expense, sent email |
| **Update**  | Rescheduled meeting, updated deal value        |
| **Delete**  | Canceled meeting, removed task                 |
| **Send**    | Sent email, SMS, notification                  |
| **Approve** | Approved expense, approved time off            |

### Action Log Data Model

```json
{
  "doctype": "VA Action Log",
  "fields": [
    { "fieldname": "action_id", "fieldtype": "Data", "unique": true },
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "conversation",
      "fieldtype": "Link",
      "options": "VA Conversation"
    },
    { "fieldname": "timestamp", "fieldtype": "Datetime" },
    {
      "fieldname": "action_type",
      "fieldtype": "Select",
      "options": "Read\nCreate\nUpdate\nDelete\nSend\nApprove"
    },
    { "fieldname": "sub_agent", "fieldtype": "Data" },
    { "fieldname": "target_doctype", "fieldtype": "Data" },
    { "fieldname": "target_document", "fieldtype": "Data" },
    { "fieldname": "description", "fieldtype": "Text" },
    { "fieldname": "details", "fieldtype": "JSON" },
    { "fieldname": "reversible", "fieldtype": "Check" },
    { "fieldname": "reversed", "fieldtype": "Check" },
    { "fieldname": "reversed_at", "fieldtype": "Datetime" }
  ]
}
```

### Action Log UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION HISTORY                                │
│                                                                  │
│  Filter: [All Actions ▼] [Today ▼]                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  2:30 PM  ✓ Created expense claim                               │
│           EXP-2024-0892 • $14.50 • Meals                        │
│           [View] [Undo]                                          │
│                                                                  │
│  2:28 PM  📖 Retrieved daily schedule                           │
│           8 jobs found for today                                 │
│           [View Details]                                         │
│                                                                  │
│  11:45 AM ✓ Sent SMS to customer                                │
│           "Running 10 minutes late" → Johnson Residence         │
│           [View]                                                 │
│                                                                  │
│  11:30 AM ✓ Updated job status                                  │
│           JOB-2024-1234 → "En Route"                            │
│           [View] [Undo]                                          │
│                                                                  │
│  8:35 AM  ✓ Created attendance record                           │
│           Clocked in at 8:35 AM • GPS verified                  │
│           [View]                                                 │
│                                                                  │
│                       [Export Log]                               │
└─────────────────────────────────────────────────────────────────┘
```

### Undo Capability

| Action         | Reversible | Undo Method                    |
| -------------- | :--------: | ------------------------------ |
| Create meeting |     ✓      | Cancel/delete event            |
| Submit expense |     ✓      | Cancel claim (if not approved) |
| Send email     |     ✗      | N/A (can't unsend)             |
| Update status  |     ✓      | Revert to previous status      |
| Clock in       |     ⚠️     | Requires manager approval      |
| Approve PO     |     ✗      | Requires formal reversal       |

### Acceptance Criteria

- [ ] All VA actions logged
- [ ] Action details include before/after state
- [ ] Reversible actions can be undone
- [ ] Non-reversible actions marked
- [ ] Export log to CSV/PDF
- [ ] Search actions by type, date, target

---

## 6.6 MEM-04: Contextual Awareness

### Description

VA understands current context (time, location, activity, calendar) to provide relevant responses.

### User Story

> As an employee, I want my VA to understand my current situation without me explaining it every time.

### Context Signals

| Signal              | Source         | Example Use                            |
| ------------------- | -------------- | -------------------------------------- |
| **Time**            | Device clock   | "Good morning" vs "Good evening"       |
| **Day of week**     | Calendar       | "Have a great weekend!" on Friday      |
| **Location**        | GPS            | "You're at the Henderson site"         |
| **Calendar**        | Active events  | "You're in a meeting right now"        |
| **Recent activity** | Action history | "Back to the Henderson proposal?"      |
| **Device**          | Platform       | Voice-first on mobile, text on desktop |
| **Network**         | Connectivity   | Degrade gracefully on poor signal      |

### Context-Aware Responses

**Time-based:**

```
6:00 AM: "Good morning, Marcus! Here's your day..."
12:00 PM: "Lunchtime! You have a job at 1 PM."
6:00 PM: "Wrapping up? Here's what you accomplished today..."
```

**Location-based:**

```
At office: "Welcome back to the office. You have a package at reception."
At client site: "You're at Henderson's. Their contact is John (555-1234)."
In car: "Want me to start navigation to your next job?"
```

**Calendar-based:**

```
In meeting: [Whisper mode automatically enabled]
Before meeting: "Your 2 PM with Lisa starts in 10 minutes.
                Here's the agenda we discussed."
After meeting: "How did the meeting with Lisa go? Should I send notes?"
```

**Activity-based:**

```
Just clocked in: "Good morning! Here's your schedule for today."
On break: "Enjoy your break! I'll remind you in 15 minutes."
Between jobs: "Next job is 15 minutes away. Weather is clear."
```

### Context Data Model

```json
{
  "employee_context": {
    "employee_id": "EMP-001",
    "timestamp": "2025-11-28T14:30:00Z",

    "temporal": {
      "time_of_day": "afternoon",
      "day_type": "workday",
      "week_position": "mid_week"
    },

    "location": {
      "coordinates": { "lat": 35.1234, "lng": -89.9876 },
      "type": "client_site",
      "site_name": "Henderson Residence",
      "travel_status": "stationary"
    },

    "calendar": {
      "current_event": null,
      "next_event": { "title": "Team Standup", "in_minutes": 45 },
      "busy_until": null
    },

    "activity": {
      "last_action": "completed_job",
      "current_task": "JOB-2024-1235",
      "active_conversation_topic": "job_completion"
    },

    "device": {
      "platform": "mobile",
      "connectivity": "lte",
      "battery": 67
    }
  }
}
```

### Acceptance Criteria

- [ ] Time-appropriate greetings
- [ ] Location detected and used appropriately
- [ ] Calendar events influence VA behavior
- [ ] Recent activity referenced naturally
- [ ] Context updates in real-time
- [ ] Context-switching handled gracefully

---

## 6.7 MEM-05: Proactive Suggestions

### Description

VA anticipates needs and offers suggestions based on patterns, schedule, and context.

### User Story

> As an employee, I want my VA to remind me of things I might forget before I have to ask.

### Suggestion Types

| Type               | Trigger           | Example                                  |
| ------------------ | ----------------- | ---------------------------------------- |
| **Pattern-based**  | Repeated behavior | "You usually submit expenses on Fridays" |
| **Calendar-based** | Upcoming events   | "Your meeting with Lisa needs an agenda" |
| **Time-based**     | Specific times    | "Certification expires in 30 days"       |
| **Location-based** | Arrival/departure | "You're near the Henderson site"         |
| **Workflow-based** | Process steps     | "Don't forget to log completion photos"  |

### Proactive Notification Examples

**Morning Briefing (opt-in):**

```
"Good morning, Marcus!

📅 Today: 8 jobs, first at 7:15 AM (Johnson Residence)
⚠️ Weather: Rain expected this afternoon - plan accordingly
📋 Action needed: 2 expenses pending from yesterday
🏆 Progress: 3 more jobs to hit your weekly target"
```

**Before Meeting:**

```
"Your 2 PM with Lisa starts in 10 minutes.

📎 Last time: You discussed the Henderson timeline
📋 Prep: I found 3 documents you might need
❓ She asked about budget approval last time"
```

**Pattern Recognition:**

```
"I noticed you usually book a hotel when flying to Chicago.
The Marriott downtown has availability at $189/night.
Should I book it?"
```

**Deadline Approaching:**

```
"Heads up: Your CPR certification expires in 30 days.
I found a renewal class on February 10th.
Want me to register you?"
```

### Suggestion Engine

```python
class SuggestionEngine:
    def generate_suggestions(self, employee, context):
        suggestions = []

        # Pattern-based
        patterns = self.analyze_patterns(employee)
        for pattern in patterns:
            if pattern.is_triggered(context):
                suggestions.append(pattern.suggestion)

        # Calendar-based
        upcoming = self.get_upcoming_events(employee, hours=4)
        for event in upcoming:
            prep = self.get_meeting_prep(event)
            if prep:
                suggestions.append(prep)

        # Time-based deadlines
        deadlines = self.get_approaching_deadlines(employee)
        for deadline in deadlines:
            suggestions.append(deadline.reminder)

        # Location-based
        if context.location.is_near_client:
            client_context = self.get_client_context(context.location)
            suggestions.append(client_context)

        # Rank by relevance and urgency
        return self.rank_suggestions(suggestions, context)
```

### Suggestion Preferences

Users can control proactivity level:

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROACTIVE SUGGESTIONS                          │
│                                                                  │
│  How proactive should Alex be?                                  │
│                                                                  │
│  [━━━━━━━━━●━━━━━] More proactive                               │
│                                                                  │
│  Types of suggestions:                                           │
│  ☑ Morning briefing (6:30 AM)                                   │
│  ☑ Meeting preparation (10 min before)                          │
│  ☑ Deadline reminders (30, 7, 1 day before)                     │
│  ☑ Pattern-based suggestions                                     │
│  ☐ Location-based suggestions                                    │
│  ☐ Social suggestions ("Wish John happy birthday")              │
│                                                                  │
│  Quiet hours: [9 PM] to [7 AM]                                  │
│                                                                  │
│  ☑ Bundle suggestions (max 3 per interruption)                  │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Morning briefing delivered at preferred time
- [ ] Meeting prep 10 minutes before
- [ ] Deadline reminders at configurable intervals
- [ ] Pattern detection with >70% accuracy
- [ ] User can adjust proactivity level
- [ ] Quiet hours respected

---

## 6.8 MEM-06: Learning from Corrections

### Description

VA improves based on user corrections, feedback, and demonstrated preferences.

### User Story

> As an employee, I want my VA to learn from mistakes so it doesn't repeat them.

### Correction Types

| Type           | Example                              | Learning                  |
| -------------- | ------------------------------------ | ------------------------- |
| **Factual**    | "His name is Tom, not Tim"           | Correct entity reference  |
| **Preference** | "I meant the other John"             | Disambiguate contacts     |
| **Behavioral** | "Don't notify me for small expenses" | Adjust notification rules |
| **Formatting** | "Give me shorter summaries"          | Adjust response length    |
| **Timing**     | "Don't interrupt during standup"     | Respect calendar events   |

### Correction Flow

```
VA: "I've scheduled a meeting with John Davis for Tuesday."

User: "No, I meant John Smith."

VA: [Records correction: "John" in this context → John Smith]
VA: "Got it! I've updated the meeting to John Smith.
     I'll remember you work more with John Smith."

--- Later ---

User: "Set up a call with John"

VA: [Checks correction history: John → John Smith (confidence: high)]
VA: "Setting up a call with John Smith. Is that right?"

User: "Yes"

VA: [Increases confidence for John → John Smith mapping]
```

### Feedback Mechanisms

| Mechanism               | Action                  | Result                       |
| ----------------------- | ----------------------- | ---------------------------- |
| **Thumbs up**           | Tap 👍                  | Reinforce behavior           |
| **Thumbs down**         | Tap 👎                  | Prompt for correction        |
| **Explicit correction** | "Actually..."           | Direct correction            |
| **Interruption**        | Interrupt mid-response  | Response too long/wrong      |
| **Retry**               | "Try again"             | Previous response inadequate |
| **Ignore**              | No action on suggestion | Suggestion not useful        |

### Learning Data Model

```json
{
  "doctype": "VA Learning Event",
  "fields": [
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "event_type",
      "fieldtype": "Select",
      "options": "Correction\nPositive Feedback\nNegative Feedback\nIgnored Suggestion"
    },
    { "fieldname": "context", "fieldtype": "JSON" },
    { "fieldname": "original_response", "fieldtype": "Text" },
    { "fieldname": "corrected_response", "fieldtype": "Text" },
    {
      "fieldname": "learning_category",
      "fieldtype": "Select",
      "options": "Entity Resolution\nPreference\nBehavior\nFormatting\nTiming"
    },
    { "fieldname": "applied_count", "fieldtype": "Int" },
    { "fieldname": "confidence", "fieldtype": "Float" }
  ]
}
```

### Learning Application

```python
class LearningEngine:
    def apply_learnings(self, employee, response, context):
        learnings = self.get_learnings(employee, context.topic)

        for learning in learnings:
            if learning.category == "entity_resolution":
                # Apply entity disambiguation
                response = self.apply_entity_learning(response, learning)

            elif learning.category == "formatting":
                # Adjust response format
                response = self.apply_format_learning(response, learning)

            elif learning.category == "timing":
                # Check if should suppress
                if self.should_suppress(context, learning):
                    return None

        return response

    def record_correction(self, employee, original, corrected, context):
        # Extract what changed
        diff = self.analyze_correction(original, corrected)

        # Store learning
        learning = frappe.new_doc("VA Learning Event")
        learning.employee = employee
        learning.event_type = "Correction"
        learning.context = context
        learning.original_response = original
        learning.corrected_response = corrected
        learning.learning_category = diff.category
        learning.confidence = 0.7  # Initial confidence
        learning.save()

        return learning
```

### Acceptance Criteria

- [ ] Corrections stored and applied in future
- [ ] Thumbs up/down on every response
- [ ] Confidence increases with repeated corrections
- [ ] Learning decays if contradicted
- [ ] User can view/delete learned behaviors
- [ ] Learning exportable with personality

---

## 6.9 MEM-07: Cross-Session Memory

### Description

Important facts and context persist across separate conversations.

### User Story

> As an employee, I want my VA to remember important things I mentioned last week without me having to remind it.

### Memory Extraction

After each conversation, extract memorable facts:

```
Conversation:
User: "I'm working on the Henderson proposal this week"
User: "My daughter's recital is Friday evening"
User: "I prefer to fly Delta when going to Chicago"

Extracted Memories:
• Current project: Henderson proposal (expires: 1 week)
• Personal: Daughter's recital Friday evening (expires: after Friday)
• Preference: Delta for Chicago flights (permanent)
```

### Memory Types

| Type                    | Duration    | Example                         |
| ----------------------- | ----------- | ------------------------------- |
| **Working memory**      | 1-7 days    | "Working on Henderson proposal" |
| **Event memory**        | Until event | "Daughter's recital Friday"     |
| **Preference memory**   | Permanent   | "Prefers Delta flights"         |
| **Fact memory**         | Permanent   | "Has 2 kids"                    |
| **Relationship memory** | Permanent   | "Lisa is their manager"         |

### Memory Data Model

```json
{
  "doctype": "VA Memory",
  "fields": [
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "memory_type",
      "fieldtype": "Select",
      "options": "Working\nEvent\nPreference\nFact\nRelationship"
    },
    { "fieldname": "content", "fieldtype": "Text" },
    { "fieldname": "structured_data", "fieldtype": "JSON" },
    {
      "fieldname": "source_conversation",
      "fieldtype": "Link",
      "options": "VA Conversation"
    },
    { "fieldname": "created_at", "fieldtype": "Datetime" },
    { "fieldname": "expires_at", "fieldtype": "Datetime" },
    { "fieldname": "confidence", "fieldtype": "Float" },
    { "fieldname": "access_count", "fieldtype": "Int" },
    { "fieldname": "last_accessed", "fieldtype": "Datetime" },
    { "fieldname": "embedding", "fieldtype": "JSON" }
  ]
}
```

### Memory Retrieval

When processing new request:

```python
def retrieve_relevant_memories(employee, query, context):
    # 1. Embed the query
    query_embedding = embed(query)

    # 2. Vector search for relevant memories
    memories = opensearch.search(
        index="va_memories",
        query={
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 10
                }
            }
        },
        filter={"employee": employee}
    )

    # 3. Filter by recency and type
    relevant = []
    for memory in memories:
        if memory.expires_at and memory.expires_at < now():
            continue  # Expired
        if memory.relevance_score(query, context) > 0.7:
            relevant.append(memory)

    # 4. Update access stats
    for memory in relevant:
        memory.access_count += 1
        memory.last_accessed = now()

    return relevant[:5]  # Top 5 relevant memories
```

### Memory in Conversation

```
User: "What am I working on?"

VA: [Retrieves memory: "Working on Henderson proposal"]
VA: "You're working on the Henderson proposal.
     You mentioned it's due this week. How's it going?"
```

```
User: "Book my Chicago flight"

VA: [Retrieves memory: "Prefers Delta for Chicago"]
VA: "Looking for Delta flights to Chicago.
     Same preferences as last time?"
```

### Acceptance Criteria

- [ ] Facts extracted from conversations automatically
- [ ] Working memories expire appropriately
- [ ] Preferences persist permanently
- [ ] Memory retrieval based on semantic relevance
- [ ] User can view/edit/delete memories
- [ ] Memory used naturally in conversation

---

## 6.10 MEM-08: Memory Privacy Controls

### Description

User controls over what VA remembers and how long.

### User Story

> As an employee, I want control over what my VA remembers about me.

### Privacy Controls

```
┌─────────────────────────────────────────────────────────────────┐
│                   MEMORY & PRIVACY                               │
│                                                                  │
│  What should Alex remember?                                      │
│                                                                  │
│  REMEMBER TYPES                                                  │
│  ☑ Work preferences (calendar, travel, communication)           │
│  ☑ Work facts (projects, colleagues, clients)                   │
│  ☐ Personal facts (family, hobbies, birthdays)                  │
│  ☐ Conversation history (what we discussed)                     │
│                                                                  │
│  RETENTION                                                       │
│  Conversation history: [90 days ▼]                              │
│  Action history: [1 year ▼]                                     │
│  Preferences: [Forever ▼]                                       │
│                                                                  │
│  PRIVACY MODES                                                   │
│  ☐ Incognito mode (nothing logged this session)                 │
│  ☐ Off-the-record (don't remember this conversation)            │
│                                                                  │
│  MANAGER ACCESS                                                  │
│  ☑ Manager can view action log                                  │
│  ☐ Manager can view conversation history                        │
│  ☐ Manager can view preferences                                 │
│                                                                  │
│  DATA MANAGEMENT                                                 │
│  [View All Memories]  [Export Data]  [Delete All Data]          │
└─────────────────────────────────────────────────────────────────┘
```

### Privacy Modes

| Mode               | Effect                           |
| ------------------ | -------------------------------- |
| **Normal**         | Everything logged and remembered |
| **Whisper**        | Text-only, no voice recorded     |
| **Off-the-record** | Conversation not saved           |
| **Incognito**      | Nothing saved, no learning       |

### Voice Commands

| Command                           | Action                       |
| --------------------------------- | ---------------------------- |
| "Forget that"                     | Delete last exchange         |
| "Don't remember this"             | Mark conversation off-record |
| "Go incognito"                    | Enable incognito mode        |
| "What do you know about me?"      | List stored memories         |
| "Forget everything about [topic]" | Delete specific memories     |

### Data Export

```
┌─────────────────────────────────────────────────────────────────┐
│                   EXPORT MY DATA                                 │
│                                                                  │
│  Select what to export:                                          │
│                                                                  │
│  ☑ Conversation history (426 conversations)                     │
│  ☑ Action history (1,247 actions)                               │
│  ☑ Preferences (34 items)                                       │
│  ☑ Memories (89 items)                                          │
│  ☑ Learning events (156 corrections)                            │
│  ☑ Personality profile                                          │
│                                                                  │
│  Format: [JSON ▼]                                               │
│                                                                  │
│  ⚠️ This may take a few minutes to prepare.                     │
│                                                                  │
│                        [Export]                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] User can disable specific memory types
- [ ] Retention periods configurable
- [ ] Incognito mode prevents all storage
- [ ] "Forget that" deletes immediately
- [ ] Full data export available
- [ ] Delete all data option (with confirmation)
- [ ] Manager access controls enforced

---

_Next: Section 7 - Privacy & Audit Features_

# Section 7: Privacy & Audit Features

## 7.1 Feature Group Overview

| ID     | Feature                 | Priority | Phase |
| ------ | ----------------------- | -------- | ----- |
| PRI-01 | Privacy Modes           | P0       | Alpha |
| PRI-02 | Data Encryption         | P0       | Alpha |
| PRI-03 | Manager Audit Access    | P1       | Beta  |
| PRI-04 | Action Reversal         | P1       | Beta  |
| PRI-05 | Compliance Logging      | P1       | Beta  |
| PRI-06 | Data Retention Policies | P1       | Beta  |
| PRI-07 | Access Controls         | P0       | Alpha |
| PRI-08 | Consent Management      | P0       | Alpha |

---

## 7.2 PRI-01: Privacy Modes

### Description

Multiple privacy levels allowing employees to control VA data collection in real-time.

### User Story

> As an employee, I want to have a private conversation with my VA that my manager can't see.

### Privacy Levels

| Mode           | Voice Recording | Transcript | Action Log | Memory | Manager Visible |
| -------------- | :-------------: | :--------: | :--------: | :----: | :-------------: |
| **Normal**     |        ✓        |     ✓      |     ✓      |   ✓    |  Configurable   |
| **Whisper**    |        ✗        |     ✓      |     ✓      |   ✓    |  Configurable   |
| **Off-Record** |        ✗        |     ✗      |     ✓      |   ✗    |  Actions only   |
| **Incognito**  |        ✗        |     ✗      |     ✗      |   ✗    |        ✗        |

### Mode Activation

**Voice Commands:**

```
"Alex, go incognito" → Incognito mode
"Alex, off the record" → Off-record mode
"Alex, whisper mode" → Whisper mode
"Alex, normal mode" → Return to normal
```

**UI Toggle:**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Privacy Mode: [Normal ▼]                                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ ○ Normal - Full logging and memory                      │    │
│  │ ○ Whisper - No voice recording                          │    │
│  │ ○ Off-Record - No transcript saved                      │    │
│  │ ● Incognito - Nothing saved                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  🔒 Incognito active - This conversation will not be saved      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Visual Indicators

| Mode       | Indicator                         |
| ---------- | --------------------------------- |
| Normal     | Green dot                         |
| Whisper    | Yellow dot + "No audio recording" |
| Off-Record | Orange dot + "Off the record"     |
| Incognito  | Red dot + "🔒 Incognito"          |

### Mode Restrictions

| Action               | Normal | Whisper | Off-Record | Incognito |
| -------------------- | :----: | :-----: | :--------: | :-------: |
| Clock in/out         |   ✓    |    ✓    |     ✓      |     ✗     |
| Submit expense       |   ✓    |    ✓    |     ✓      |     ✗     |
| Send email           |   ✓    |    ✓    |     ✓      |     ✗     |
| Query information    |   ✓    |    ✓    |     ✓      |     ✓     |
| Personal questions   |   ✓    |    ✓    |     ✓      |     ✓     |
| Approve transactions |   ✓    |    ✓    |     ✗      |     ✗     |

### Acceptance Criteria

- [ ] All 4 privacy modes functional
- [ ] Voice command activation works
- [ ] Visual indicator always visible
- [ ] Mode persists until changed
- [ ] Incognito blocks write actions
- [ ] Manager cannot override incognito

---

## 7.3 PRI-02: Data Encryption

### Description

End-to-end encryption for sensitive VA data at rest and in transit.

### Encryption Scope

| Data Type           | At Rest | In Transit | Key Management   |
| ------------------- | :-----: | :--------: | ---------------- |
| Voice recordings    | AES-256 |  TLS 1.3   | Per-employee key |
| Transcripts         | AES-256 |  TLS 1.3   | Per-employee key |
| Personality profile | AES-256 |  TLS 1.3   | Per-employee key |
| Memories            | AES-256 |  TLS 1.3   | Per-employee key |
| Action logs         | AES-256 |  TLS 1.3   | Company key      |
| Preferences         | AES-256 |  TLS 1.3   | Per-employee key |

### Key Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    KEY HIERARCHY                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Master Key (HSM / AWS KMS / Azure Key Vault)            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐         │
│  │ Company Key   │ │ Company Key   │ │ Company Key   │         │
│  │ (Tenant A)    │ │ (Tenant B)    │ │ (Tenant C)    │         │
│  └───────────────┘ └───────────────┘ └───────────────┘         │
│          │                                                       │
│          ├──────────────────────────────────────┐               │
│          ▼                                      ▼               │
│  ┌───────────────┐                    ┌───────────────┐         │
│  │ Employee Key  │        ...         │ Employee Key  │         │
│  │ (EMP-001)     │                    │ (EMP-500)     │         │
│  └───────────────┘                    └───────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Encryption Implementation

**Voice Data:**

```python
def store_voice_recording(employee_id, audio_data):
    # Get employee's encryption key
    key = get_employee_key(employee_id)

    # Encrypt audio
    encrypted = encrypt_aes256(audio_data, key)

    # Store with metadata
    recording = {
        "employee": employee_id,
        "encrypted_data": encrypted,
        "encryption_version": "v1",
        "key_id": key.id,
        "created_at": now()
    }

    # Store in secure storage
    store_encrypted_blob(recording)
```

**Zero-Knowledge Option (Enterprise):**

- Employee-held keys
- Dartwing cannot decrypt
- Recovery via employee's master password

### Acceptance Criteria

- [ ] All sensitive data encrypted at rest
- [ ] TLS 1.3 for all API calls
- [ ] Per-employee key isolation
- [ ] Key rotation supported
- [ ] Encryption transparent to user
- [ ] SOC 2 / HIPAA compliant

---

## 7.4 PRI-03: Manager Audit Access

### Description

Configurable manager access to employee VA activity with full audit trail.

### User Story

> As a manager, I want to see what actions my team's VAs have taken so I can ensure compliance.

### Access Levels

| Level            | See Actions | See Transcripts | See Preferences | See Memories |
| ---------------- | :---------: | :-------------: | :-------------: | :----------: |
| **None**         |      ✗      |        ✗        |        ✗        |      ✗       |
| **Actions Only** |      ✓      |        ✗        |        ✗        |      ✗       |
| **Operational**  |      ✓      |    Work only    |        ✗        |      ✗       |
| **Full**         |      ✓      |        ✓        |        ✓        |      ✓       |

### Manager Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                   TEAM VA ACTIVITY                               │
│                                                                  │
│  Team: Operations (12 members)         [Export] [Settings]      │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  TODAY'S SUMMARY                                                 │
│  ├─ Total VA interactions: 156                                  │
│  ├─ Actions taken: 89                                           │
│  ├─ Approvals processed: 7                                      │
│  └─ Alerts triggered: 2                                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ⚠️ FLAGGED ACTIVITY                                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Marcus Chen - 2:30 PM                                      │ │
│  │ Submitted expense $450 (exceeds $100 auto-approve)         │ │
│  │ Status: Pending your approval                     [Review] │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  TEAM MEMBER ACTIVITY                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Name           │ Interactions │ Actions │ Last Active   │    │
│  │────────────────┼──────────────┼─────────┼───────────────│    │
│  │ Marcus Chen    │     23       │   12    │ 10 min ago    │    │
│  │ Sarah Johnson  │     18       │    8    │ 25 min ago    │    │
│  │ David Park     │     31       │   15    │ 5 min ago     │    │
│  │ ...            │              │         │               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  [View All Activity]                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Manager Access Audit

Every manager access is logged:

```json
{
  "doctype": "VA Manager Access Log",
  "fields": [
    { "fieldname": "manager", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "employee_viewed",
      "fieldtype": "Link",
      "options": "Employee"
    },
    {
      "fieldname": "access_type",
      "fieldtype": "Select",
      "options": "Actions\nTranscripts\nPreferences\nMemories"
    },
    { "fieldname": "timestamp", "fieldtype": "Datetime" },
    { "fieldname": "ip_address", "fieldtype": "Data" },
    { "fieldname": "reason", "fieldtype": "Text" }
  ]
}
```

### Employee Notification

When manager accesses sensitive data:

```
┌─────────────────────────────────────────────────────────────────┐
│  🔔 Your manager viewed your VA activity                        │
│                                                                  │
│  Lisa Martinez viewed your action history for Nov 28, 2025.     │
│  This is part of standard operational oversight.                │
│                                                                  │
│  [View Details]                              [Privacy Settings] │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Manager access configurable by company
- [ ] 4 access levels supported
- [ ] All manager access logged
- [ ] Employee notified of access (configurable)
- [ ] Manager cannot access incognito sessions
- [ ] Audit log immutable

---

## 7.5 PRI-04: Action Reversal

### Description

Ability to undo VA actions with full audit trail.

### User Story

> As an employee, I want to undo an action my VA took by mistake.

### Reversible Actions

| Action Type    | Reversible | Reversal Method  | Time Limit       |
| -------------- | :--------: | ---------------- | ---------------- |
| Create meeting |     ✓      | Delete event     | 24 hours         |
| Submit expense |     ✓      | Cancel claim     | Until approved   |
| Send email     |     ✗      | N/A              | N/A              |
| Send SMS       |     ✗      | N/A              | N/A              |
| Update status  |     ✓      | Restore previous | 24 hours         |
| Book resource  |     ✓      | Cancel booking   | Until start time |
| Clock in/out   |     ⚠️     | Manager approval | Same day         |
| Approve PO     |     ✗      | Formal reversal  | N/A              |

### Reversal Flow

```
User: "Undo that expense submission"

VA: [Checks: EXP-2024-0892, status: Pending, reversible: Yes]

VA: "I'll cancel expense EXP-2024-0892 for $14.50.
     This will remove it from approval queue.
     Confirm?"

User: "Yes"

VA: [Executes reversal]
    [Logs: Reversal of EXP-2024-0892 by employee request]

VA: "Done. The expense has been canceled."
```

### Reversal Audit Log

```json
{
  "doctype": "VA Action Reversal",
  "fields": [
    {
      "fieldname": "original_action",
      "fieldtype": "Link",
      "options": "VA Action Log"
    },
    { "fieldname": "reversed_by", "fieldtype": "Link", "options": "Employee" },
    {
      "fieldname": "reversal_type",
      "fieldtype": "Select",
      "options": "Employee Request\nManager Override\nSystem Auto"
    },
    { "fieldname": "reason", "fieldtype": "Text" },
    { "fieldname": "timestamp", "fieldtype": "Datetime" },
    { "fieldname": "approval_required", "fieldtype": "Check" },
    { "fieldname": "approved_by", "fieldtype": "Link", "options": "Employee" }
  ]
}
```

### Acceptance Criteria

- [ ] Reversible actions marked in UI
- [ ] "Undo" command works for recent actions
- [ ] Time limits enforced
- [ ] Manager approval for sensitive reversals
- [ ] Reversal fully logged
- [ ] Original action marked as reversed

---

## 7.6 PRI-05: Compliance Logging

### Description

Comprehensive logging for regulatory compliance (SOC 2, HIPAA, GDPR).

### User Story

> As a compliance officer, I want complete audit trails of all VA activity.

### Log Categories

| Category              | Contents                         | Retention |
| --------------------- | -------------------------------- | --------- |
| **Authentication**    | Login, logout, session start     | 2 years   |
| **Authorization**     | Permission checks, access grants | 2 years   |
| **Data Access**       | What data was read               | 7 years   |
| **Data Modification** | What data was changed            | 7 years   |
| **Admin Actions**     | Config changes, user management  | 7 years   |
| **Security Events**   | Failed auth, suspicious activity | 7 years   |

### Log Format

```json
{
  "timestamp": "2025-11-28T14:30:00.000Z",
  "event_type": "data_modification",
  "event_subtype": "expense_created",
  "actor": {
    "type": "va_agent",
    "employee_id": "EMP-001",
    "session_id": "sess_abc123"
  },
  "target": {
    "doctype": "Expense Claim",
    "document_id": "EXP-2024-0892"
  },
  "action": "create",
  "details": {
    "amount": 14.5,
    "category": "meals"
  },
  "context": {
    "conversation_id": "conv_xyz789",
    "platform": "mobile",
    "ip_address": "192.168.1.100",
    "user_agent": "DartwingApp/2.1.0"
  },
  "outcome": "success"
}
```

### Compliance Reports

| Report                    | Contents                   | Schedule         |
| ------------------------- | -------------------------- | ---------------- |
| **Access Report**         | Who accessed what data     | Weekly/On-demand |
| **Modification Report**   | All data changes           | Weekly/On-demand |
| **Authentication Report** | Login patterns, failures   | Daily            |
| **Privilege Report**      | Permission changes         | On change        |
| **Data Export Report**    | GDPR data subject requests | On-demand        |

### HIPAA-Specific Logging

For healthcare deployments:

```json
{
  "phi_access_log": {
    "timestamp": "2025-11-28T14:30:00.000Z",
    "user": "EMP-001",
    "patient_id": "PAT-12345",
    "data_type": "appointment_history",
    "purpose": "scheduling",
    "access_method": "va_query",
    "minimum_necessary": true
  }
}
```

### Acceptance Criteria

- [ ] All events logged with required fields
- [ ] Logs immutable (append-only)
- [ ] Log retention configurable per category
- [ ] Compliance reports auto-generated
- [ ] HIPAA mode for healthcare
- [ ] GDPR data export supported

---

## 7.7 PRI-06: Data Retention Policies

### Description

Configurable retention periods for different data types with automatic purging.

### User Story

> As an HR admin, I want to ensure VA data is retained appropriately and deleted when no longer needed.

### Default Retention Periods

| Data Type        | Default | Min     | Max      | Configurable By |
| ---------------- | ------- | ------- | -------- | --------------- |
| Voice recordings | 90 days | 0       | 2 years  | Company         |
| Transcripts      | 1 year  | 30 days | 7 years  | Company         |
| Action logs      | 2 years | 1 year  | 7 years  | Compliance      |
| Preferences      | Forever | 1 year  | Forever  | Employee        |
| Memories         | Forever | 30 days | Forever  | Employee        |
| Compliance logs  | 7 years | 2 years | 10 years | Compliance      |

### Retention Configuration UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   DATA RETENTION POLICIES                        │
│                                                                  │
│  ⚠️ Changes require Compliance Officer approval                  │
│                                                                  │
│  EMPLOYEE DATA                                                   │
│  ├─ Voice recordings:     [90 days ▼]                           │
│  ├─ Conversation transcripts: [1 year ▼]                        │
│  ├─ Employee preferences: [Forever ▼]                           │
│  └─ VA memories:          [Forever ▼]                           │
│                                                                  │
│  OPERATIONAL DATA                                                │
│  ├─ Action logs:          [2 years ▼]                           │
│  ├─ Manager access logs:  [2 years ▼]                           │
│  └─ System logs:          [1 year ▼]                            │
│                                                                  │
│  COMPLIANCE DATA                                                 │
│  ├─ Audit logs:           [7 years ▼] 🔒                        │
│  ├─ Security events:      [7 years ▼] 🔒                        │
│  └─ Access logs:          [7 years ▼] 🔒                        │
│                                                                  │
│  🔒 = Minimum retention required by compliance                  │
│                                                                  │
│  Auto-purge schedule: [Weekly ▼] at [Sunday 2 AM ▼]             │
│                                                                  │
│                   [Save Changes]                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Auto-Purge Process

```python
def run_data_purge():
    """Weekly purge of expired data"""

    policies = get_retention_policies()

    for data_type, retention in policies.items():
        cutoff_date = now() - retention.period

        # Get expired records
        expired = frappe.get_all(
            data_type.doctype,
            filters={"created_at": ["<", cutoff_date]},
            pluck="name"
        )

        # Log purge intent
        log_purge_batch(data_type, len(expired), cutoff_date)

        # Delete in batches
        for batch in chunks(expired, 1000):
            frappe.db.delete(data_type.doctype, {"name": ["in", batch]})
            frappe.db.commit()

        # Log completion
        log_purge_complete(data_type, len(expired))
```

### Acceptance Criteria

- [ ] Retention periods configurable per data type
- [ ] Auto-purge runs on schedule
- [ ] Purge logged for compliance
- [ ] Compliance minimums enforced
- [ ] Employee can request early deletion
- [ ] Legal hold overrides auto-purge

---

## 7.8 PRI-07: Access Controls

### Description

Fine-grained permissions controlling what each employee can do via VA.

### User Story

> As an IT admin, I want to control which employees can use which VA features.

### Permission Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION HIERARCHY                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Company Settings (Global defaults)                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Role Templates (Sales, Operations, HR, Executive)       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Individual Overrides (Per-employee)                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Permission Categories

| Category        | Permissions                                       |
| --------------- | ------------------------------------------------- |
| **Voice**       | Use voice, use wake word, voice biometrics        |
| **Sub-Agents**  | HR, CRM, Operations, Knowledge, Calendar, Finance |
| **Actions**     | Read, Create, Update, Delete, Approve             |
| **Data Access** | Own data, Team data, All data                     |
| **Privacy**     | Use incognito, off-record, export data            |
| **Admin**       | Manage templates, view team, access reports       |

### Role Templates

**Field Worker:**

```json
{
  "role": "Field Worker",
  "permissions": {
    "voice": ["use_voice", "wake_word"],
    "sub_agents": ["hr", "operations", "knowledge"],
    "actions": {
      "hr": ["read", "create_attendance"],
      "operations": ["read", "update_job_status", "submit_form"],
      "knowledge": ["read"]
    },
    "data_access": "own",
    "privacy": ["incognito"],
    "admin": []
  }
}
```

**Manager:**

```json
{
  "role": "Manager",
  "permissions": {
    "voice": ["use_voice", "wake_word", "voice_biometrics"],
    "sub_agents": [
      "hr",
      "crm",
      "operations",
      "knowledge",
      "calendar",
      "finance"
    ],
    "actions": {
      "hr": ["read", "create", "approve_leave", "view_team"],
      "crm": ["read", "create", "update"],
      "operations": ["read", "create", "update", "delete"],
      "knowledge": ["read", "create"],
      "calendar": ["read", "create", "update", "delete"],
      "finance": ["read", "create", "approve"]
    },
    "data_access": "team",
    "privacy": ["incognito", "off_record"],
    "admin": ["view_team_activity"]
  }
}
```

### Permission Check

```python
def check_va_permission(employee, action, target=None):
    """Check if employee can perform action via VA"""

    # Get effective permissions (company → role → individual)
    permissions = get_effective_permissions(employee)

    # Check action permission
    if action not in permissions.actions:
        raise PermissionError(f"VA action '{action}' not permitted")

    # Check data access scope
    if target and target.owner != employee:
        if not can_access_data(employee, target, permissions.data_access):
            raise PermissionError(f"Cannot access {target.doctype} owned by {target.owner}")

    return True
```

### Acceptance Criteria

- [ ] Permission hierarchy enforced
- [ ] Role templates for common roles
- [ ] Individual overrides supported
- [ ] Permission denied handled gracefully
- [ ] Audit log for permission denials
- [ ] UI shows available actions only

---

## 7.9 PRI-08: Consent Management

### Description

Explicit consent collection and management for VA features.

### User Story

> As an employee, I want to understand and control what I'm agreeing to when using the VA.

### Consent Types

| Consent                   | Required | Revocable | Impact if Declined         |
| ------------------------- | :------: | :-------: | -------------------------- |
| **Terms of Service**      |    ✓     |     ✗     | Cannot use VA              |
| **Voice Recording**       |    ✗     |     ✓     | Text-only mode             |
| **Conversation Logging**  |    ✗     |     ✓     | No history, no learning    |
| **Proactive Suggestions** |    ✗     |     ✓     | Reactive only              |
| **Manager Visibility**    | Company  |  Company  | N/A                        |
| **Analytics**             |    ✗     |     ✓     | No usage analytics         |
| **AI Training**           |    ✗     |     ✓     | Data not used for training |

### Consent Collection Flow

**Initial Setup:**

```
┌─────────────────────────────────────────────────────────────────┐
│                   WELCOME TO DARTWING VA                         │
│                                                                  │
│  Before we get started, please review these settings:           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ☑ I agree to the Terms of Service and Privacy Policy           │
│    [Read Terms] [Read Privacy Policy]                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  OPTIONAL FEATURES (you can change these anytime)               │
│                                                                  │
│  ☑ Allow voice recording                                        │
│    Your voice is recorded for transcription and quality.        │
│    [Learn More]                                                  │
│                                                                  │
│  ☑ Save conversation history                                    │
│    Alex remembers past conversations to help you better.        │
│    [Learn More]                                                  │
│                                                                  │
│  ☑ Enable proactive suggestions                                 │
│    Alex can offer helpful suggestions before you ask.           │
│    [Learn More]                                                  │
│                                                                  │
│  ☐ Share anonymized usage data to improve the product           │
│    [Learn More]                                                  │
│                                                                  │
│                      [ Get Started ]                             │
└─────────────────────────────────────────────────────────────────┘
```

### Consent Record

```json
{
  "doctype": "VA Consent Record",
  "fields": [
    { "fieldname": "employee", "fieldtype": "Link", "options": "Employee" },
    { "fieldname": "consent_type", "fieldtype": "Data" },
    { "fieldname": "version", "fieldtype": "Data" },
    { "fieldname": "granted", "fieldtype": "Check" },
    { "fieldname": "granted_at", "fieldtype": "Datetime" },
    { "fieldname": "revoked_at", "fieldtype": "Datetime" },
    { "fieldname": "ip_address", "fieldtype": "Data" },
    { "fieldname": "user_agent", "fieldtype": "Data" }
  ]
}
```

### Consent Withdrawal

```
User: "Alex, stop recording my voice"

VA: "I'll disable voice recording. You can still use me via text.
     To re-enable voice, go to Settings > Privacy > Voice Recording.

     Confirm you want to disable voice recording?"

User: "Yes"

VA: [Updates consent: voice_recording = revoked]
VA: "Done. Voice recording is now disabled.
     You're now in text-only mode."
```

### Acceptance Criteria

- [ ] All consents collected before use
- [ ] Consent version tracked
- [ ] Revocable consents revocable anytime
- [ ] Revocation takes effect immediately
- [ ] Consent history exportable
- [ ] Re-consent required for policy changes

---

_Next: Section 8 - Company Templates & Admin_

# Section 8: Company Templates & Admin

## 8.1 Feature Group Overview

| ID     | Feature             | Priority | Phase |
| ------ | ------------------- | -------- | ----- |
| ADM-01 | VA Templates        | P1       | Beta  |
| ADM-02 | Template Deployment | P1       | Beta  |
| ADM-03 | Company Settings    | P0       | Alpha |
| ADM-04 | Usage Analytics     | P1       | Beta  |
| ADM-05 | Cost Management     | P1       | Beta  |
| ADM-06 | Employee Onboarding | P0       | Alpha |
| ADM-07 | Bulk Operations     | P2       | GA    |

---

## 8.2 ADM-01: VA Templates

### Description

Pre-configured VA personalities and capabilities that HR/Admin can create and deploy to employee groups.

### User Story

> As an HR admin, I want to create VA templates for different roles so new employees get a properly configured assistant from day one.

### Template Components

| Component              | Description                | Customizable by Employee |
| ---------------------- | -------------------------- | :----------------------: |
| **Base Personality**   | Communication style, tone  |        Partially         |
| **Sub-Agents Enabled** | Which sub-agents available |            No            |
| **Voice Options**      | Available voice choices    |           Yes            |
| **Proactivity Level**  | Suggestion frequency       |           Yes            |
| **Privacy Defaults**   | Default privacy settings   |        Partially         |
| **Knowledge Sources**  | RAG document folders       |            No            |
| **Spending Limits**    | Expense/approval limits    |            No            |
| **Custom Prompts**     | Role-specific instructions |            No            |

### Template Schema

```json
{
  "doctype": "VA Template",
  "fields": [
    { "fieldname": "template_name", "fieldtype": "Data", "reqd": true },
    { "fieldname": "description", "fieldtype": "Text" },
    {
      "fieldname": "target_roles",
      "fieldtype": "Table MultiSelect",
      "options": "Role"
    },
    { "fieldname": "department", "fieldtype": "Link", "options": "Department" },
    { "fieldname": "is_default", "fieldtype": "Check" },
    { "fieldname": "enabled", "fieldtype": "Check", "default": 1 },

    { "fieldname": "personality_section", "fieldtype": "Section Break" },
    {
      "fieldname": "base_tone",
      "fieldtype": "Select",
      "options": "Professional\nFriendly\nPlayful\nMinimal\nMilitary"
    },
    {
      "fieldname": "proactivity",
      "fieldtype": "Select",
      "options": "High\nMedium\nLow\nNone"
    },
    {
      "fieldname": "detail_level",
      "fieldtype": "Select",
      "options": "Comprehensive\nModerate\nMinimal"
    },
    { "fieldname": "custom_personality_prompt", "fieldtype": "Long Text" },

    { "fieldname": "capabilities_section", "fieldtype": "Section Break" },
    { "fieldname": "enabled_sub_agents", "fieldtype": "JSON" },
    { "fieldname": "voice_options", "fieldtype": "JSON" },
    { "fieldname": "knowledge_folders", "fieldtype": "JSON" },

    { "fieldname": "limits_section", "fieldtype": "Section Break" },
    { "fieldname": "expense_limit", "fieldtype": "Currency" },
    { "fieldname": "approval_limit", "fieldtype": "Currency" },
    { "fieldname": "daily_action_limit", "fieldtype": "Int" },

    { "fieldname": "privacy_section", "fieldtype": "Section Break" },
    {
      "fieldname": "default_privacy_mode",
      "fieldtype": "Select",
      "options": "Normal\nWhisper\nOff-Record"
    },
    { "fieldname": "voice_recording_enabled", "fieldtype": "Check" },
    {
      "fieldname": "manager_oversight_level",
      "fieldtype": "Select",
      "options": "None\nActions Only\nSummary\nFull"
    }
  ]
}
```

### Pre-Built Templates

| Template                   | Target              | Key Settings                                        |
| -------------------------- | ------------------- | --------------------------------------------------- |
| **Field Service VA**       | Technicians         | Voice-first, operations-heavy, minimal detail       |
| **Office Professional VA** | Office workers      | Balanced, all sub-agents, standard detail           |
| **Sales VA**               | Sales reps          | High energy, CRM-focused, proactive                 |
| **Executive VA**           | Executives          | Summary-first, approval-focused, minimal            |
| **Onboarding VA**          | New hires           | Friendly, knowledge-focused, high proactivity       |
| **Factory Floor VA**       | Warehouse workers   | Simple commands, safety-focused, loud environment   |
| **Healthcare VA**          | Clinical staff      | HIPAA-compliant, whisper default, medical knowledge |
| **Travel VA**              | Traveling employees | Booking-focused, proactive reminders                |

### Template Builder UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   VA TEMPLATE BUILDER                            │
│                                                                  │
│  Template Name: [Field Service VA                          ]     │
│  Description:   [Optimized for field technicians           ]     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ASSIGN TO                                                       │
│  Roles: [Field Technician ▼] [Service Engineer ▼] [+ Add]       │
│  Departments: [Service ▼] [Maintenance ▼]                       │
│  ☑ Set as default for these roles                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PERSONALITY                                                     │
│  Base Tone:        [Military ▼]                                 │
│  Proactivity:      [High ▼]                                     │
│  Detail Level:     [Minimal ▼]                                  │
│                                                                  │
│  Custom Instructions:                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Keep responses brief and actionable. Use radio-style    │    │
│  │ confirmations ("Copy", "Affirmative"). Prioritize job   │    │
│  │ information and customer details.                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SUB-AGENTS                                                      │
│  ☑ HR (clock in/out, schedule, leave)                           │
│  ☑ Operations (jobs, forms, status updates)                     │
│  ☑ Knowledge (procedures, equipment manuals)                    │
│  ☐ CRM (customer management)                                     │
│  ☐ Calendar (meeting scheduling)                                 │
│  ☑ Finance (expenses only, no approvals)                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  LIMITS                                                          │
│  Expense submission limit: [$100        ]                       │
│  Daily action limit:       [100 actions ]                       │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  KNOWLEDGE SOURCES                                               │
│  ☑ /Company Policies                                            │
│  ☑ /Service Procedures                                          │
│  ☑ /Equipment Manuals                                           │
│  ☐ /Sales Materials                                              │
│  ☐ /HR Documents (sensitive)                                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  [Preview Template]  [Save Draft]  [Deploy Template]            │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] 8 pre-built templates available
- [ ] Custom template builder functional
- [ ] Templates assignable to roles/departments
- [ ] Sub-agent enable/disable per template
- [ ] Spending limits enforced
- [ ] Knowledge source restrictions work

---

## 8.3 ADM-02: Template Deployment

### Description

Deploy VA templates to employees individually, by role, or company-wide.

### User Story

> As an HR admin, I want to deploy the new Safety VA template to all warehouse workers at once.

### Deployment Options

| Method           | Scope             | Use Case                 |
| ---------------- | ----------------- | ------------------------ |
| **Individual**   | Single employee   | Executive VIP setup      |
| **Role-based**   | All in role       | Standard role deployment |
| **Department**   | All in department | Department-specific VA   |
| **Company-wide** | Everyone          | Policy update            |
| **Automatic**    | New hires in role | Onboarding automation    |

### Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEPLOY TEMPLATE                                │
│                                                                  │
│  Template: Safety Compliance VA                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DEPLOYMENT SCOPE                                                │
│                                                                  │
│  ○ Individual employees                                          │
│     [Search employees...]                                        │
│                                                                  │
│  ● Role-based                                                    │
│     ☑ Warehouse Associate (45 employees)                        │
│     ☑ Forklift Operator (12 employees)                          │
│     ☐ Warehouse Manager (3 employees)                           │
│                                                                  │
│  ○ Department                                                    │
│     [Select department...]                                       │
│                                                                  │
│  ○ Company-wide (all 234 employees)                             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DEPLOYMENT OPTIONS                                              │
│                                                                  │
│  ☑ Override existing VA settings                                │
│  ☐ Preserve employee customizations (name, voice)               │
│  ☑ Notify employees of new VA capabilities                      │
│  ☐ Require re-consent for new features                          │
│                                                                  │
│  Schedule: [Deploy immediately ▼]                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PREVIEW                                                         │
│  • 57 employees will receive this template                      │
│  • 12 will have existing settings overridden                    │
│  • Estimated completion: 2 minutes                              │
│                                                                  │
│  [Cancel]                              [Deploy to 57 Employees] │
└─────────────────────────────────────────────────────────────────┘
```

### Automatic Deployment

Configure templates to auto-deploy to new hires:

```python
# Hook on Employee creation
def on_employee_create(doc, method):
    # Find applicable template
    template = get_template_for_role(doc.role)

    if template:
        # Create VA instance for employee
        create_va_instance(
            employee=doc.name,
            template=template.name,
            trigger_onboarding=True
        )

        # Send welcome notification
        notify_employee_va_ready(doc)
```

### Deployment Status Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT STATUS                              │
│                                                                  │
│  Deployment: Safety Compliance VA → Warehouse Roles             │
│  Started: Nov 28, 2025 2:15 PM                                  │
│                                                                  │
│  Progress: ████████████████████░░░░ 85% (49/57)                 │
│                                                                  │
│  ✓ Completed: 49                                                │
│  ⏳ In Progress: 3                                               │
│  ⚠️ Failed: 5                                                    │
│                                                                  │
│  FAILURES:                                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ John Smith - Account suspended                             │ │
│  │ Mary Johnson - Consent not yet granted                     │ │
│  │ ... 3 more                                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Retry Failed]  [Skip Failed]  [Cancel Deployment]             │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Individual, role, department, company deployment
- [ ] Automatic deployment for new hires
- [ ] Preserve/override customization options
- [ ] Progress tracking for large deployments
- [ ] Failure handling and retry
- [ ] Rollback capability

---

## 8.4 ADM-03: Company Settings

### Description

Company-wide configuration for VA behavior, limits, and policies.

### User Story

> As a company admin, I want to configure VA settings that apply to all employees.

### Settings Categories

| Category         | Settings                                    |
| ---------------- | ------------------------------------------- |
| **General**      | Company name, timezone, working hours       |
| **AI Models**    | Default models, fallback order, cost limits |
| **Privacy**      | Default modes, retention, manager access    |
| **Limits**       | Expense limits, action limits, API limits   |
| **Integrations** | Connected systems, API keys                 |
| **Branding**     | VA name, avatar, voice options              |

### Company Settings UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   COMPANY VA SETTINGS                            │
│                                                                  │
│  Company: Acme Corp                                              │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  GENERAL                                                         │
│  ├─ Company timezone: [America/Chicago ▼]                       │
│  ├─ Working hours: [8:00 AM] to [6:00 PM]                       │
│  ├─ Working days: ☑M ☑T ☑W ☑T ☑F ☐S ☐S                         │
│  └─ Default language: [English (US) ▼]                          │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  AI MODELS                                                       │
│  ├─ Primary coordinator: [GPT-4o ▼]                             │
│  ├─ Sub-agent model: [Claude 3 Haiku ▼]                         │
│  ├─ Voice model: [OpenAI 4o Audio ▼]                            │
│  ├─ Fallback order: GPT-4o → Claude 4 → Gemini 2               │
│  └─ Monthly AI budget: [$5,000   ] ⚠️ 78% used                  │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  PRIVACY DEFAULTS                                                │
│  ├─ Default privacy mode: [Normal ▼]                            │
│  ├─ Voice recording: [Transcribe only ▼]                        │
│  ├─ Conversation retention: [90 days ▼]                         │
│  ├─ Manager oversight: [Actions only ▼]                         │
│  └─ Employee can disable oversight: ☐                           │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  LIMITS                                                          │
│  ├─ Max expense via VA: [$500      ]                            │
│  ├─ Max approval via VA: [$1,000   ]                            │
│  ├─ Max actions per employee/day: [200    ]                     │
│  └─ Max voice minutes per employee/month: [500    ]             │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  BRANDING                                                        │
│  ├─ Default VA name: [Assistant    ]                            │
│  ├─ Allow custom names: ☑                                       │
│  ├─ Company avatar: [Upload]                                    │
│  └─ Available voices: ☑Alloy ☑Echo ☑Nova ☐Onyx ☐Shimmer        │
│                                                                  │
│  [Save Settings]  [Reset to Defaults]  [Export Config]          │
└─────────────────────────────────────────────────────────────────┘
```

### Settings Hierarchy

```
System Defaults
    │
    └── Company Settings (override)
            │
            └── Template Settings (override)
                    │
                    └── Employee Preferences (override where allowed)
```

### Acceptance Criteria

- [ ] All company settings configurable
- [ ] Settings apply to new employees automatically
- [ ] AI budget tracking and alerts
- [ ] Limits enforced across all employees
- [ ] Export/import configuration
- [ ] Change audit log

---

## 8.5 ADM-04: Usage Analytics

### Description

Dashboards and reports on VA usage across the company.

### User Story

> As an admin, I want to understand how employees are using the VA so I can optimize our investment.

### Analytics Dashboards

**Overview Dashboard:**

```
┌─────────────────────────────────────────────────────────────────┐
│                   VA USAGE ANALYTICS                             │
│                                                                  │
│  Period: [Last 30 Days ▼]                                       │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  KEY METRICS                                                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ Active Users│ │Conversations│ │   Actions   │ │Time Saved │ │
│  │    187      │ │   12,456    │ │   45,892    │ │  892 hrs  │ │
│  │   ▲ 12%     │ │    ▲ 23%    │ │    ▲ 18%    │ │   ▲ 15%   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  USAGE BY SUB-AGENT                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ HR          ████████████████████░░░░░░░░░░  42%        │    │
│  │ Operations  ██████████████░░░░░░░░░░░░░░░░  28%        │    │
│  │ Calendar    ██████████░░░░░░░░░░░░░░░░░░░░  18%        │    │
│  │ Finance     ████░░░░░░░░░░░░░░░░░░░░░░░░░░   8%        │    │
│  │ Knowledge   ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4%        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  DAILY ACTIVE USERS                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │    200 ┤                                    ╭───╮       │    │
│  │    150 ┤              ╭───────────────╮   ╭╯   ╰╮      │    │
│  │    100 ┤    ╭────────╯               ╰───╯      ╰╮     │    │
│  │     50 ┤───╯                                      ╰──  │    │
│  │      0 ┼────┴────┴────┴────┴────┴────┴────┴────┴────  │    │
│  │        Nov 1    8    15    22    28                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  [Export Report]  [Schedule Report]  [Configure Alerts]         │
└─────────────────────────────────────────────────────────────────┘
```

### Metrics Tracked

| Metric              | Description                         |
| ------------------- | ----------------------------------- |
| **Active Users**    | Unique users with VA interaction    |
| **Conversations**   | Total conversation sessions         |
| **Actions**         | VA actions executed                 |
| **Time Saved**      | Estimated time saved (action-based) |
| **Voice Usage**     | Minutes of voice interaction        |
| **Task Completion** | % of requests fulfilled             |
| **Fallback Rate**   | % escalated to human                |
| **NPS Score**       | User satisfaction                   |

### Reports

| Report            | Frequency | Recipients |
| ----------------- | --------- | ---------- |
| Executive Summary | Weekly    | Leadership |
| Department Usage  | Weekly    | Managers   |
| Cost Analysis     | Monthly   | Finance    |
| Compliance Status | Monthly   | Legal      |
| Adoption Trends   | Monthly   | HR         |

### Acceptance Criteria

- [ ] Real-time usage dashboard
- [ ] Historical trend analysis
- [ ] Department/role breakdown
- [ ] Scheduled reports via email
- [ ] Export to CSV/PDF
- [ ] Custom date ranges

---

## 8.6 ADM-05: Cost Management

### Description

Track and control AI costs across the organization.

### User Story

> As a finance admin, I need to monitor and control our VA AI spending.

### Cost Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                   AI COST MANAGEMENT                             │
│                                                                  │
│  Period: November 2025                                           │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  BUDGET STATUS                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │  Budget: $5,000    Spent: $3,892    Remaining: $1,108  │    │
│  │                                                         │    │
│  │  ████████████████████████████████░░░░░░░░░░ 78%        │    │
│  │                                                         │    │
│  │  ⚠️ At current rate, budget exhausted by Nov 25        │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  COST BY MODEL                                                   │
│  │ Model          │ Tokens (M) │  Cost   │ % of Total │        │
│  ├────────────────┼────────────┼─────────┼────────────┤        │
│  │ GPT-4o         │    45.2    │ $2,260  │    58%     │        │
│  │ GPT-4o Audio   │    12.8    │   $890  │    23%     │        │
│  │ Claude Haiku   │    89.4    │   $536  │    14%     │        │
│  │ Embeddings     │   234.5    │   $206  │     5%     │        │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  COST BY DEPARTMENT                                              │
│  │ Department     │   Users   │  Cost   │ Per User  │          │
│  ├────────────────┼───────────┼─────────┼───────────┤          │
│  │ Sales          │     45    │ $1,234  │   $27.42  │          │
│  │ Service        │     67    │ $1,102  │   $16.45  │          │
│  │ Operations     │     52    │   $892  │   $17.15  │          │
│  │ HR             │     12    │   $423  │   $35.25  │          │
│  │ Executive      │     11    │   $241  │   $21.91  │          │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  TOP USERS BY COST                                               │
│  1. Jennifer Walsh (Exec)      $89.45                           │
│  2. David Park (Sales)         $67.23                           │
│  3. Sarah Okonkwo (HR)         $54.12                           │
│                                                                  │
│  [Set Budget Alerts]  [Adjust Limits]  [Export Report]          │
└─────────────────────────────────────────────────────────────────┘
```

### Cost Controls

| Control                | Description                      |
| ---------------------- | -------------------------------- |
| **Monthly budget**     | Hard cap on total spend          |
| **Per-user limit**     | Max cost per employee            |
| **Model restrictions** | Limit expensive models           |
| **Alert thresholds**   | Notify at 50%, 75%, 90%          |
| **Automatic fallback** | Switch to cheaper model at limit |

### Cost Optimization Suggestions

```
┌─────────────────────────────────────────────────────────────────┐
│                   COST OPTIMIZATION                              │
│                                                                  │
│  Potential Monthly Savings: $892                                │
│                                                                  │
│  RECOMMENDATIONS:                                                │
│                                                                  │
│  1. Switch simple queries to Claude Haiku           -$340/mo    │
│     Currently 45% of GPT-4o queries are simple lookups          │
│     [Apply Recommendation]                                       │
│                                                                  │
│  2. Enable response caching                         -$280/mo    │
│     23% of queries are repeated across users                    │
│     [Enable Caching]                                             │
│                                                                  │
│  3. Reduce voice transcription quality              -$180/mo    │
│     Current: HD (24kHz) → Suggested: Standard (16kHz)          │
│     [Adjust Quality]                                             │
│                                                                  │
│  4. Batch non-urgent operations                      -$92/mo    │
│     Daily summaries can use batch API (50% cheaper)             │
│     [Enable Batching]                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Real-time cost tracking
- [ ] Budget alerts at configurable thresholds
- [ ] Cost breakdown by model, department, user
- [ ] Automatic fallback to cheaper models
- [ ] Cost optimization recommendations
- [ ] Monthly cost reports

---

## 8.7 ADM-06: Employee Onboarding

### Description

Automated VA setup for new employees joining the company.

### User Story

> As an HR admin, I want new employees to have their VA ready and personalized on their first day.

### Onboarding Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   NEW EMPLOYEE VA ONBOARDING                     │
│                                                                  │
│  Employee: Alex Johnson                                          │
│  Start Date: December 1, 2025                                   │
│  Role: Field Technician                                          │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  AUTOMATIC SETUP (Day 1)                                         │
│                                                                  │
│  ☑ Create VA instance                                           │
│  ☑ Apply template: Field Service VA                             │
│  ☑ Grant permissions for role                                   │
│  ☑ Add to department knowledge base                             │
│  ☑ Enable HR sub-agent for onboarding tasks                     │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  FIRST LOGIN EXPERIENCE                                          │
│                                                                  │
│  1. Welcome message from VA                                      │
│  2. Consent collection                                           │
│  3. Quick personality quiz (optional)                            │
│  4. Voice and name selection                                     │
│  5. Guided tour of VA capabilities                              │
│  6. First task: Complete onboarding checklist                   │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  ONBOARDING CHECKLIST (VA-assisted)                             │
│                                                                  │
│  ☐ Complete I-9 verification                                    │
│  ☐ Set up direct deposit                                        │
│  ☐ Review company policies                                       │
│  ☐ Complete safety training                                      │
│  ☐ Set up equipment                                              │
│  ☐ Meet with manager                                             │
│                                                                  │
│  [Preview First Login]  [Customize Onboarding]  [Schedule]      │
└─────────────────────────────────────────────────────────────────┘
```

### Onboarding VA Conversation

```
VA: "Welcome to Acme Corp, Alex! 👋

     I'm your personal AI assistant. My job is to help you
     get things done faster and easier.

     Before we start, I'd like to learn a bit about how
     you like to communicate. It'll take about 5 minutes.

     Ready to begin?"

Alex: "Sure"

VA: "Great! First question: Are you a morning person
     or a night owl?"

[... personality quiz ...]

VA: "Perfect! Now, what would you like to call me?
     Popular names are Alex, Max, Aria, or you can
     pick your own."

Alex: "Chief"

VA: "Chief it is! 💪

     Alright, Chief reporting for duty. Here's what I
     can help you with:

     • Clock in and out
     • Check your schedule
     • Submit expenses
     • Look up procedures
     • Get job details

     You have 6 onboarding tasks to complete.
     Want to start with the first one?"
```

### Acceptance Criteria

- [ ] VA created automatically on employee creation
- [ ] Template applied based on role
- [ ] First login triggers onboarding flow
- [ ] Onboarding checklist VA-assisted
- [ ] Progress tracked and reported to HR
- [ ] Manager notified when onboarding complete

---

## 8.8 ADM-07: Bulk Operations

### Description

Perform administrative operations on multiple employees at once.

### User Story

> As an admin, I want to update settings for all employees at once instead of one by one.

### Bulk Operations Available

| Operation                   | Description              |
| --------------------------- | ------------------------ |
| **Deploy template**         | Apply template to group  |
| **Update settings**         | Change specific settings |
| **Reset personality**       | Clear learned behaviors  |
| **Export data**             | Bulk data export         |
| **Delete data**             | Bulk data deletion       |
| **Enable/disable features** | Toggle features          |
| **Send announcement**       | VA delivers message      |

### Bulk Operation UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   BULK OPERATIONS                                │
│                                                                  │
│  Operation: [Update Settings ▼]                                 │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  SELECT EMPLOYEES                                                │
│                                                                  │
│  ○ All employees (234)                                          │
│  ○ By role: [Select roles...]                                   │
│  ● By department: Sales (45), Marketing (23)                    │
│  ○ By template: [Select template...]                            │
│  ○ Custom selection: [Search...]                                │
│                                                                  │
│  Selected: 68 employees                                          │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  SETTINGS TO UPDATE                                              │
│                                                                  │
│  ☑ Proactivity level: [High ▼]                                  │
│  ☐ Default privacy mode                                         │
│  ☐ Voice recording                                               │
│  ☑ Daily action limit: [150    ]                                │
│  ☐ Enable CRM sub-agent                                         │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  PREVIEW                                                         │
│  • 68 employees will be updated                                 │
│  • 2 settings will change                                       │
│  • Estimated time: 30 seconds                                   │
│                                                                  │
│  [Cancel]                              [Apply to 68 Employees]  │
└─────────────────────────────────────────────────────────────────┘
```

### Bulk Announcement

```
┌─────────────────────────────────────────────────────────────────┐
│                   SEND VA ANNOUNCEMENT                           │
│                                                                  │
│  Recipients: All employees (234)                                │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  MESSAGE                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Important: New expense policy takes effect December 1.  │    │
│  │ All expenses over $50 now require receipt photos.       │    │
│  │                                                         │    │
│  │ Your VA has been updated to remind you when submitting  │    │
│  │ expenses without photos.                                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  DELIVERY                                                        │
│  ○ Immediately                                                   │
│  ● Next VA interaction                                          │
│  ○ Scheduled: [Date/Time picker]                                │
│                                                                  │
│  ☑ Require acknowledgment                                       │
│  ☐ High priority (interrupt current task)                       │
│                                                                  │
│  [Preview]                                      [Send to 234]   │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Select by role, department, template, or custom
- [ ] Preview changes before applying
- [ ] Progress tracking for large operations
- [ ] Rollback for failed operations
- [ ] Bulk announcements via VA
- [ ] Operation audit log

---

_Next: Section 9 - Platform Integration_

# Section 9: Platform Integration

## 9.1 Feature Group Overview

| ID     | Feature                       | Priority | Phase |
| ------ | ----------------------------- | -------- | ----- |
| INT-01 | Frappe Framework Integration  | P0       | Alpha |
| INT-02 | dartwing_fone Integration     | P0       | Alpha |
| INT-03 | dartwing_company Integration  | P0       | Alpha |
| INT-04 | ERPNext Integration           | P1       | Beta  |
| INT-05 | HRMS Integration              | P0       | Alpha |
| INT-06 | Frappe CRM Integration        | P1       | Beta  |
| INT-07 | Frappe Drive Integration      | P1       | Beta  |
| INT-08 | Frappe Health Integration     | P2       | GA    |
| INT-09 | External Calendar Integration | P1       | Beta  |
| INT-10 | Third-Party AI Providers      | P0       | Alpha |

---

## 9.2 INT-01: Frappe Framework Integration

### Description

Deep integration with Frappe Framework for authentication, permissions, DocTypes, and APIs.

### User Story

> As a developer, I want the VA to use Frappe's native features so it integrates seamlessly with our existing system.

### Integration Points

| Component           | Integration                                  |
| ------------------- | -------------------------------------------- |
| **Authentication**  | Frappe session, OAuth 2.0, API keys          |
| **Permissions**     | Frappe role permissions, DocType permissions |
| **DocTypes**        | VA-specific DocTypes in Frappe               |
| **API**             | Frappe REST API, Whitelisted methods         |
| **Background Jobs** | Frappe job queue (RQ)                        |
| **Caching**         | Redis via Frappe cache                       |
| **File Storage**    | Frappe File DocType                          |
| **Notifications**   | Frappe notification system                   |

### VA DocTypes

```python
# All VA DocTypes follow Frappe conventions

doctype_list = [
    "VA Instance",           # Per-employee VA configuration
    "VA Conversation",       # Conversation sessions
    "VA Conversation Turn",  # Individual messages
    "VA Memory",             # Long-term memories
    "VA User Preference",    # User preferences
    "VA Action Log",         # Action audit trail
    "VA Audit Log",          # Security audit trail
    "VA Template",           # Company templates
    "VA Learning Event",     # Corrections and feedback
    "VA Consent Record",     # Consent tracking
    "VA Sub-Agent Config",   # Sub-agent configurations
    "VA Custom Agent",       # User-defined agents
]
```

### Permission Model

```python
# VA permissions inherit from Employee

def has_permission(doc, ptype, user):
    """Check VA document permissions"""

    # User can access own VA data
    if doc.employee == get_employee(user):
        return True

    # Manager can access direct reports (if oversight enabled)
    if is_manager_of(user, doc.employee):
        oversight = get_oversight_level(doc.employee)
        if oversight in ["Actions Only", "Summary", "Full"]:
            return ptype == "read"

    # HR Admin can access all
    if "HR Admin" in frappe.get_roles(user):
        return True

    return False
```

### API Endpoints

```python
# VA API endpoints (whitelisted)

@frappe.whitelist()
def process_message(message: str, conversation_id: str = None) -> dict:
    """Process a VA message"""
    pass

@frappe.whitelist()
def get_conversation_history(conversation_id: str) -> list:
    """Get conversation turns"""
    pass

@frappe.whitelist()
def set_preference(key: str, value: any) -> dict:
    """Set user preference"""
    pass

@frappe.whitelist()
def get_memories(limit: int = 10) -> list:
    """Get user memories"""
    pass

@frappe.whitelist()
def execute_action(action: str, params: dict) -> dict:
    """Execute VA action"""
    pass
```

### Hooks Integration

```python
# hooks.py

app_name = "dartwing_va"
app_title = "Dartwing VA"

# DocType events
doc_events = {
    "Employee": {
        "after_insert": "dartwing_va.events.create_va_instance",
        "on_trash": "dartwing_va.events.cleanup_va_instance"
    }
}

# Scheduled tasks
scheduler_events = {
    "daily": [
        "dartwing_va.tasks.enforce_retention_policies",
        "dartwing_va.tasks.generate_daily_summaries"
    ],
    "hourly": [
        "dartwing_va.tasks.process_learning_queue",
        "dartwing_va.tasks.sync_external_calendars"
    ],
    "cron": {
        "0 6 * * *": [
            "dartwing_va.tasks.send_morning_briefings"
        ]
    }
}

# Website routes
website_route_rules = [
    {"from_route": "/va/<path:app_path>", "to_route": "va"}
]
```

### Acceptance Criteria

- [ ] VA DocTypes created via Frappe
- [ ] Permissions use Frappe role system
- [ ] APIs follow Frappe conventions
- [ ] Background jobs use Frappe queue
- [ ] Caching via Frappe Redis
- [ ] Notifications via Frappe system

---

## 9.3 INT-02: dartwing_fone Integration

### Description

Integration with dartwing_fone for voice calls, SMS, and telephony features.

### User Story

> As an employee, I want my VA to make calls and send texts using my company's phone system.

### Integration Capabilities

| Capability             | Description                        |
| ---------------------- | ---------------------------------- |
| **Outbound calls**     | VA initiates calls to contacts     |
| **Inbound handling**   | VA acts as receptionist            |
| **SMS sending**        | VA sends text messages             |
| **SMS receiving**      | VA processes incoming texts        |
| **Call transcription** | Real-time call transcription       |
| **Call recording**     | Store calls (with consent)         |
| **Voicemail**          | VA checks and summarizes voicemail |

### Voice Call Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    VA-INITIATED CALL FLOW                        │
│                                                                  │
│  Employee: "Call the Henderson contact about the delay"         │
│                                                                  │
│  VA:                                                             │
│  1. Look up Henderson contact (John Smith, 555-123-4567)        │
│  2. Confirm: "Calling John Smith at Henderson. Topic: delay"    │
│  3. Initiate call via dartwing_fone API                         │
│  4. Connect employee to call                                     │
│  5. Transcribe call in real-time                                │
│  6. After call: "Call completed. Want me to log it?"            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │  📞 Calling John Smith (Henderson)                      │    │
│  │                                                         │    │
│  │  555-123-4567                                           │    │
│  │                                                         │    │
│  │  Topic: Project delay discussion                        │    │
│  │                                                         │    │
│  │  [🔇 Mute]  [⏸️ Hold]  [📝 Notes]  [🔴 End Call]        │    │
│  │                                                         │    │
│  │  Live Transcription:                                    │    │
│  │  "Hi John, this is Marcus from Acme..."                │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### SMS Integration

```python
# VA sends SMS via dartwing_fone

@frappe.whitelist()
def send_sms_via_va(recipient: str, message: str, context: dict):
    """Send SMS through VA with dartwing_fone"""

    # Get employee's assigned phone number
    phone_config = get_employee_phone_config(context.employee)

    # Send via dartwing_fone
    result = dartwing_fone.send_sms(
        from_number=phone_config.number,
        to_number=recipient,
        message=message,
        carrier=phone_config.carrier
    )

    # Log action
    log_va_action(
        employee=context.employee,
        action_type="Send",
        target_doctype="SMS",
        details={
            "recipient": recipient,
            "message": message,
            "status": result.status
        }
    )

    return result
```

### AI Receptionist Integration

When configured, VA handles incoming calls:

```
Caller → dartwing_fone → AI Receptionist (VA)
                              │
                              ├── "Schedule appointment" → Calendar Sub-Agent
                              ├── "Speak to [employee]" → Route call
                              ├── "Leave message" → Voicemail
                              └── "General inquiry" → Knowledge Sub-Agent
```

### Acceptance Criteria

- [ ] Outbound calls via VA voice command
- [ ] SMS sending with confirmation
- [ ] Inbound call handling (receptionist)
- [ ] Call transcription available
- [ ] Call logging to CRM
- [ ] Voicemail summary via VA

---

## 9.4 INT-03: dartwing_company Integration

### Description

Integration with dartwing_company for operations, CRM overlay, and HR overlay features.

### User Story

> As an employee, I want my VA to access all my company's operational systems through dartwing_company.

### Integration Points

| Module              | VA Integration                |
| ------------------- | ----------------------------- |
| **Universal Inbox** | VA reads/responds to messages |
| **Smart Dispatch**  | VA manages job assignments    |
| **Workflow Engine** | VA triggers workflows         |
| **Knowledge Base**  | VA queries for answers        |
| **Client Portal**   | VA manages portal requests    |
| **SLA Engine**      | VA tracks SLA status          |
| **Shift Scheduler** | VA manages schedules          |
| **Geo Clock-In**    | VA handles attendance         |

### Operations Sub-Agent Tools

```python
# dartwing_company operations tools

operations_tools = {
    "get_dispatch_jobs": {
        "doctype": "Dispatch Job",
        "method": "get_assigned_jobs",
        "params": ["employee_id", "date", "status"]
    },
    "update_job_status": {
        "doctype": "Dispatch Job",
        "method": "update_status",
        "params": ["job_id", "status", "notes", "photos"]
    },
    "submit_form": {
        "doctype": "Form Submission",
        "method": "submit",
        "params": ["form_id", "job_id", "responses"]
    },
    "trigger_workflow": {
        "doctype": "Workflow Instance",
        "method": "trigger",
        "params": ["workflow_id", "context"]
    },
    "book_resource": {
        "doctype": "Resource Booking",
        "method": "create",
        "params": ["resource_id", "start", "end", "purpose"]
    },
    "send_broadcast": {
        "doctype": "Broadcast Alert",
        "method": "send",
        "params": ["message", "recipients", "priority"]
    }
}
```

### CRM Overlay Integration

```python
# dartwing_company CRM overlay tools

crm_tools = {
    "get_client_360": {
        "method": "dartwing_company.crm.get_client_360",
        "params": ["customer_id"]
    },
    "create_service_ticket": {
        "doctype": "Service Ticket",
        "method": "create",
        "params": ["customer_id", "subject", "description", "priority"]
    },
    "update_ticket_status": {
        "doctype": "Service Ticket",
        "method": "update_status",
        "params": ["ticket_id", "status", "resolution"]
    },
    "get_sla_status": {
        "method": "dartwing_company.sla.get_status",
        "params": ["customer_id", "ticket_id"]
    }
}
```

### HR Overlay Integration

```python
# dartwing_company HR overlay tools

hr_tools = {
    "get_schedule": {
        "doctype": "Schedule Entry",
        "method": "get_employee_schedule",
        "params": ["employee_id", "start_date", "end_date"]
    },
    "request_shift_swap": {
        "doctype": "Shift Swap Request",
        "method": "create",
        "params": ["schedule_entry_id", "reason"]
    },
    "clock_attendance": {
        "doctype": "Attendance",
        "method": "dartwing_company.hr.geo_clock",
        "params": ["action", "latitude", "longitude", "photo"]
    }
}
```

### Acceptance Criteria

- [ ] Dispatch job management via VA
- [ ] Form submission voice-guided
- [ ] Workflow triggers from VA
- [ ] Knowledge base RAG queries
- [ ] Service ticket creation/update
- [ ] Shift schedule and swap requests
- [ ] Geo clock-in via VA

---

## 9.5 INT-04: ERPNext Integration

### Description

Integration with ERPNext for sales, purchasing, inventory, and financial operations.

### User Story

> As an employee, I want my VA to access ERPNext data for quotes, invoices, and inventory.

### Integration Points

| ERPNext Module | VA Access                           |
| -------------- | ----------------------------------- |
| **Selling**    | Quotations, Sales Orders, Customers |
| **Buying**     | Purchase Orders, Suppliers          |
| **Stock**      | Item availability, Warehouses       |
| **Accounts**   | Invoices, Payment status            |
| **Projects**   | Project status, Tasks               |
| **Assets**     | Asset information                   |

### ERPNext Tools

```python
# ERPNext integration tools

erpnext_tools = {
    # Selling
    "create_quotation": {
        "doctype": "Quotation",
        "method": "create",
        "permissions": ["Sales User"]
    },
    "get_customer": {
        "doctype": "Customer",
        "method": "get",
        "permissions": ["Sales User", "Sales Manager"]
    },

    # Stock
    "check_stock": {
        "method": "erpnext.stock.utils.get_stock_balance",
        "params": ["item_code", "warehouse"]
    },

    # Accounts
    "get_invoice_status": {
        "doctype": "Sales Invoice",
        "method": "get_payment_status",
        "permissions": ["Accounts User"]
    },

    # Projects
    "get_project_status": {
        "doctype": "Project",
        "method": "get_status",
        "permissions": ["Projects User"]
    },
    "update_task": {
        "doctype": "Task",
        "method": "update",
        "permissions": ["Projects User"]
    }
}
```

### Example Interactions

| User Says                                    | ERPNext Action             |
| -------------------------------------------- | -------------------------- |
| "Create a quote for Acme, 10 widgets at $50" | Create Quotation DocType   |
| "Is the Henderson invoice paid?"             | Query Sales Invoice status |
| "Do we have any widgets in stock?"           | Check Stock Balance        |
| "What's the status of Project Alpha?"        | Query Project DocType      |
| "Mark the design task complete"              | Update Task status         |

### Acceptance Criteria

- [ ] Quotation creation via VA
- [ ] Customer/supplier lookup
- [ ] Stock availability check
- [ ] Invoice status query
- [ ] Project and task management
- [ ] Respects ERPNext permissions

---

## 9.6 INT-05: HRMS Integration

### Description

Deep integration with Frappe HRMS for all HR-related VA functionality.

### User Story

> As an employee, I want my VA to handle all my HR tasks like leave requests, attendance, and benefits.

### Integration Points

| HRMS Feature   | VA Capability                   |
| -------------- | ------------------------------- |
| **Attendance** | Clock in/out, view records      |
| **Leave**      | Request, check balance, approve |
| **Shift**      | View schedule, request swap     |
| **Payroll**    | View payslip, tax info          |
| **Benefits**   | Enrollment status, info         |
| **Training**   | Assigned courses, completion    |
| **Employee**   | Profile info, documents         |

### HRMS Tools

```python
# HRMS integration tools

hrms_tools = {
    # Attendance
    "mark_attendance": {
        "doctype": "Attendance",
        "method": "create_or_update",
        "params": ["employee", "status", "attendance_date"]
    },
    "get_attendance": {
        "doctype": "Attendance",
        "method": "get_list",
        "params": ["employee", "from_date", "to_date"]
    },

    # Leave
    "get_leave_balance": {
        "method": "hrms.hr.doctype.leave_application.leave_application.get_leave_balance_on",
        "params": ["employee", "leave_type", "date"]
    },
    "apply_leave": {
        "doctype": "Leave Application",
        "method": "create",
        "params": ["employee", "leave_type", "from_date", "to_date", "reason"]
    },
    "approve_leave": {
        "doctype": "Leave Application",
        "method": "approve",
        "permissions": ["Leave Approver"]
    },

    # Payroll
    "get_salary_slip": {
        "doctype": "Salary Slip",
        "method": "get_latest",
        "params": ["employee"]
    },

    # Training
    "get_training_events": {
        "doctype": "Training Event",
        "method": "get_assigned",
        "params": ["employee"]
    },
    "complete_training": {
        "doctype": "Training Result",
        "method": "mark_complete",
        "params": ["employee", "training_event"]
    }
}
```

### Leave Request Flow

```
Employee: "Request Friday off"

VA:
1. Check leave balance
2. Check for conflicts (scheduled shifts, meetings)
3. Confirm: "Request Friday Dec 5 as PTO? You have 14 days remaining"
4. Create Leave Application
5. Notify approver
6. Confirm: "Leave request submitted. Lisa (your manager) will review."

[Later]

VA: "Good news! Your leave for Friday has been approved."
```

### Acceptance Criteria

- [ ] Attendance marking via VA
- [ ] Leave balance queries
- [ ] Leave application creation
- [ ] Leave approval (for managers)
- [ ] Payslip access
- [ ] Training tracking
- [ ] Respects HRMS workflow

---

## 9.7 INT-06: Frappe CRM Integration

### Description

Integration with Frappe CRM for lead and deal management.

### User Story

> As a sales rep, I want my VA to manage my leads and deals in Frappe CRM.

### Integration Points

| CRM Feature    | VA Capability               |
| -------------- | --------------------------- |
| **Leads**      | Create, update, qualify     |
| **Deals**      | Track, update stage, close  |
| **Contacts**   | Search, create, update      |
| **Activities** | Log calls, emails, meetings |
| **Tasks**      | Create, complete            |
| **Notes**      | Add to records              |

### CRM Tools

```python
# Frappe CRM integration tools

crm_tools = {
    "search_leads": {
        "doctype": "CRM Lead",
        "method": "search",
        "params": ["query", "status", "owner"]
    },
    "create_lead": {
        "doctype": "CRM Lead",
        "method": "create",
        "params": ["name", "company", "email", "phone", "source"]
    },
    "update_lead_status": {
        "doctype": "CRM Lead",
        "method": "update_status",
        "params": ["lead_id", "status"]
    },
    "get_deals": {
        "doctype": "CRM Deal",
        "method": "get_list",
        "params": ["owner", "stage", "close_date"]
    },
    "update_deal": {
        "doctype": "CRM Deal",
        "method": "update",
        "params": ["deal_id", "stage", "value", "probability"]
    },
    "log_activity": {
        "doctype": "CRM Activity",
        "method": "create",
        "params": ["contact", "activity_type", "summary"]
    }
}
```

### Example Interactions

| User Says                             | CRM Action                   |
| ------------------------------------- | ---------------------------- |
| "Create a lead for John at Acme Corp" | Create CRM Lead              |
| "What deals are closing this month?"  | Query CRM Deal by close_date |
| "Move the Acme deal to negotiation"   | Update CRM Deal stage        |
| "Log that I called John today"        | Create CRM Activity          |
| "What's my pipeline total?"           | Aggregate CRM Deal values    |

### Acceptance Criteria

- [ ] Lead creation and management
- [ ] Deal tracking and updates
- [ ] Activity logging
- [ ] Pipeline queries
- [ ] Contact search
- [ ] Respects CRM permissions

---

## 9.8 INT-07: Frappe Drive Integration

### Description

Integration with Frappe Drive for document storage and retrieval.

### User Story

> As an employee, I want my VA to find and access documents stored in company Drive.

### Integration Points

| Drive Feature   | VA Capability                  |
| --------------- | ------------------------------ |
| **Search**      | Find documents by name/content |
| **Browse**      | Navigate folder structure      |
| **Read**        | Access document content        |
| **Upload**      | Store new documents            |
| **Share**       | Generate share links           |
| **Permissions** | Respect Drive permissions      |

### Knowledge RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DRIVE RAG PIPELINE                            │
│                                                                  │
│  User Query: "What's our refund policy?"                        │
│                                                                  │
│  1. SEARCH                                                       │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Query Frappe Drive API                              │     │
│     │ Filter: folders = [/Policies, /Procedures]          │     │
│     │ Results: 3 documents                                │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│  2. CHUNK                                                        │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Split documents into chunks (512 tokens)            │     │
│     │ Total: 47 chunks                                    │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│  3. EMBED                                                        │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Generate embeddings for query and chunks            │     │
│     │ Model: text-embedding-3-small                       │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│  4. RETRIEVE                                                     │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Vector similarity search                            │     │
│     │ Top 5 relevant chunks                               │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│  5. GENERATE                                                     │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ LLM generates answer with context                   │     │
│     │ Include source citations                            │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│  Response: "According to the Customer Policy Guide (v3.2),     │
│             refunds are available within 30 days..."            │
└─────────────────────────────────────────────────────────────────┘
```

### Drive Tools

```python
# Frappe Drive integration tools

drive_tools = {
    "search_documents": {
        "method": "frappe_drive.api.search",
        "params": ["query", "folder", "file_type"]
    },
    "get_document": {
        "method": "frappe_drive.api.get_file",
        "params": ["file_id"]
    },
    "get_folder_contents": {
        "method": "frappe_drive.api.list_folder",
        "params": ["folder_id"]
    },
    "upload_document": {
        "method": "frappe_drive.api.upload",
        "params": ["file", "folder_id", "name"]
    },
    "share_document": {
        "method": "frappe_drive.api.share",
        "params": ["file_id", "users", "permission"]
    }
}
```

### Acceptance Criteria

- [ ] Document search by name and content
- [ ] RAG-based Q&A from documents
- [ ] Folder browsing
- [ ] Document upload via VA
- [ ] Share link generation
- [ ] Respects Drive permissions

---

## 9.9 INT-08: Frappe Health Integration

### Description

Integration with Frappe Health for healthcare-specific VA features.

### User Story

> As a clinical staff member, I want my VA to access patient information and help with clinical workflows.

### Integration Points

| Health Feature    | VA Capability           |
| ----------------- | ----------------------- |
| **Patient**       | Lookup, demographics    |
| **Appointments**  | Schedule, reschedule    |
| **Encounters**    | View history, summaries |
| **Vitals**        | Record, query           |
| **Prescriptions** | View (not create)       |
| **Lab Orders**    | Status, results         |

### HIPAA Compliance

All Frappe Health interactions:

- Require HIPAA-compliant mode
- Log to audit trail
- Enforce minimum necessary
- Support break-glass access

```python
# Health integration with HIPAA compliance

@hipaa_compliant
def get_patient_summary(patient_id: str, employee: str) -> dict:
    """Get patient summary with HIPAA logging"""

    # Log access
    log_phi_access(
        patient=patient_id,
        accessor=employee,
        purpose="VA patient lookup",
        data_accessed=["demographics", "appointments"]
    )

    # Get minimum necessary data
    patient = frappe.get_doc("Patient", patient_id)

    return {
        "name": patient.patient_name,
        "dob": patient.dob,
        "upcoming_appointments": get_upcoming_appointments(patient_id),
        "last_encounter": get_last_encounter_summary(patient_id)
    }
```

### Health Tools

```python
# Frappe Health integration tools (HIPAA-compliant)

health_tools = {
    "search_patient": {
        "doctype": "Patient",
        "method": "search",
        "hipaa": True
    },
    "get_patient_appointments": {
        "doctype": "Patient Appointment",
        "method": "get_upcoming",
        "hipaa": True
    },
    "schedule_appointment": {
        "doctype": "Patient Appointment",
        "method": "create",
        "hipaa": True
    },
    "get_encounter_summary": {
        "doctype": "Patient Encounter",
        "method": "get_summary",
        "hipaa": True
    },
    "record_vitals": {
        "doctype": "Vital Signs",
        "method": "create",
        "hipaa": True
    }
}
```

### Acceptance Criteria

- [ ] Patient lookup with HIPAA logging
- [ ] Appointment scheduling
- [ ] Encounter summary (no detailed notes)
- [ ] Vitals recording
- [ ] Automatic whisper mode for PHI
- [ ] Full audit trail for Health access

---

## 9.10 INT-09: External Calendar Integration

### Description

Integration with Google Calendar, Microsoft 365, and other calendar providers.

### User Story

> As an employee, I want my VA to see and manage my Google Calendar alongside my work calendar.

### Supported Providers

| Provider         | Read | Write | Availability |
| ---------------- | :--: | :---: | :----------: |
| Google Calendar  |  ✓   |   ✓   |      ✓       |
| Microsoft 365    |  ✓   |   ✓   |      ✓       |
| Apple iCloud     |  ✓   |   ✓   |      ✓       |
| CalDAV (generic) |  ✓   |   ✓   |      ✓       |
| Frappe Calendar  |  ✓   |   ✓   |      ✓       |

### OAuth Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CALENDAR OAUTH FLOW                           │
│                                                                  │
│  1. Employee clicks "Connect Google Calendar"                   │
│  2. Redirect to Google OAuth consent screen                     │
│  3. Employee grants calendar.read, calendar.write               │
│  4. Google returns authorization code                           │
│  5. Exchange code for access + refresh tokens                   │
│  6. Store encrypted tokens in VA Instance                       │
│  7. VA can now read/write Google Calendar                       │
│                                                                  │
│  Token refresh happens automatically before expiry              │
└─────────────────────────────────────────────────────────────────┘
```

### Calendar Sync

```python
# Multi-calendar aggregation

def get_unified_calendar(employee: str, start: date, end: date) -> list:
    """Get events from all connected calendars"""

    va_instance = get_va_instance(employee)
    events = []

    # Frappe Calendar (always)
    events.extend(get_frappe_events(employee, start, end))

    # External calendars
    for connection in va_instance.calendar_connections:
        if connection.provider == "Google":
            events.extend(get_google_events(connection, start, end))
        elif connection.provider == "Microsoft":
            events.extend(get_microsoft_events(connection, start, end))
        # ...

    # Deduplicate and sort
    events = deduplicate_events(events)
    events.sort(key=lambda e: e.start)

    return events
```

### Connection UI

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONNECTED CALENDARS                            │
│                                                                  │
│  Your VA can see events from these calendars:                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 📅 Google Calendar                                         │ │
│  │    marcus@gmail.com                                        │ │
│  │    Last sync: 5 minutes ago                                │ │
│  │    [Sync Now] [Disconnect]                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 📅 Microsoft 365                                           │ │
│  │    marcus@acmecorp.com                                     │ │
│  │    Last sync: 2 minutes ago                                │ │
│  │    [Sync Now] [Disconnect]                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [+ Connect Another Calendar]                                   │
│                                                                  │
│  Sync frequency: [Every 5 minutes ▼]                            │
│  ☑ Include personal calendars in availability check             │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Google Calendar OAuth connection
- [ ] Microsoft 365 OAuth connection
- [ ] Read events from all calendars
- [ ] Create events in preferred calendar
- [ ] Unified availability check
- [ ] Token refresh handling

---

## 9.11 INT-10: Third-Party AI Providers

### Description

Integration with multiple AI providers for model flexibility and redundancy.

### User Story

> As an admin, I want to use different AI models for different tasks based on cost and capability.

### Supported Providers

| Provider      | Models                 | Use Case           |
| ------------- | ---------------------- | ------------------ |
| **OpenAI**    | GPT-4o, GPT-4o Audio   | Coordinator, voice |
| **Anthropic** | Claude 4, Claude Haiku | Long context, fast |
| **Google**    | Gemini 2, Gems         | Multimodal, local  |
| **Meta**      | Llama 405B             | Self-hosted        |
| **Custom**    | Any OpenAI-compatible  | Enterprise         |

### Model Router

```python
class ModelRouter:
    """Route requests to appropriate AI model"""

    def route(self, request: VARequest) -> str:
        """Determine best model for request"""

        # Voice requests → OpenAI 4o
        if request.modality == "voice":
            return "openai/gpt-4o-audio"

        # Long documents → Claude
        if request.context_length > 100000:
            return "anthropic/claude-4"

        # Privacy-sensitive → Local Gems
        if request.privacy_mode == "local":
            return "google/gems-local"

        # Simple queries → Haiku (cheap)
        if request.complexity == "simple":
            return "anthropic/claude-3-haiku"

        # Default → Primary coordinator
        return self.company_config.primary_model

    def fallback_chain(self, primary: str) -> list:
        """Get fallback models if primary fails"""
        return [
            primary,
            "anthropic/claude-4",
            "openai/gpt-4o",
            "google/gemini-2",
            "anthropic/claude-3-haiku"  # Last resort
        ]
```

### Provider Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│                   AI PROVIDER CONFIGURATION                      │
│                                                                  │
│  OPENAI                                                          │
│  ├─ API Key: [sk-...••••••••••••        ] [Test]               │
│  ├─ Organization: [org-...              ]                       │
│  ├─ Models enabled: ☑GPT-4o ☑GPT-4o-audio ☐GPT-4-turbo        │
│  └─ Monthly limit: [$3,000     ]                                │
│                                                                  │
│  ANTHROPIC                                                       │
│  ├─ API Key: [sk-ant-...••••••••        ] [Test]               │
│  ├─ Models enabled: ☑Claude-4 ☑Claude-3-Haiku                  │
│  └─ Monthly limit: [$2,000     ]                                │
│                                                                  │
│  GOOGLE                                                          │
│  ├─ API Key: [AIza...••••••••           ] [Test]               │
│  ├─ Models enabled: ☑Gemini-2 ☑Gems                            │
│  ├─ Local Gems: [Enabled ▼]                                     │
│  └─ Monthly limit: [$1,000     ]                                │
│                                                                  │
│  SELF-HOSTED                                                     │
│  ├─ Endpoint: [https://llm.internal.acme.com/v1]               │
│  ├─ Model: [llama-405b-instruct]                                │
│  └─ Auth: [Bearer token ▼]                                      │
│                                                                  │
│  ROUTING                                                         │
│  ├─ Primary coordinator: [OpenAI GPT-4o ▼]                      │
│  ├─ Sub-agents: [Anthropic Claude Haiku ▼]                      │
│  ├─ Voice: [OpenAI GPT-4o Audio ▼]                              │
│  └─ Fallback order: [GPT-4o → Claude-4 → Gemini-2]             │
│                                                                  │
│  [Save Configuration]  [Test All Providers]                     │
└─────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] OpenAI integration (GPT-4o, audio)
- [ ] Anthropic integration (Claude)
- [ ] Google integration (Gemini, Gems)
- [ ] Self-hosted model support
- [ ] Automatic model routing
- [ ] Fallback chain on failure
- [ ] Cost tracking per provider

---

_Next: Section 10 - Technical Requirements_

# Section 10: Technical Requirements

## 10.1 System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DARTWING VA ARCHITECTURE                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    CLIENT LAYER                          │    │
│  │                                                          │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │    │
│  │  │ Flutter │  │ Flutter │  │ Frappe  │  │ Widget  │    │    │
│  │  │ Mobile  │  │ Desktop │  │   Web   │  │ Embed   │    │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │    │
│  │       │            │            │            │          │    │
│  └───────┼────────────┼────────────┼────────────┼──────────┘    │
│          │            │            │            │                │
│          └────────────┴─────┬──────┴────────────┘                │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │                      API GATEWAY                         │    │
│  │            (REST + WebSocket + gRPC)                     │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │                    SERVICE LAYER                         │    │
│  │                                                          │    │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐    │    │
│  │  │Coordinator│  │ Sub-Agent │  │    Voice          │    │    │
│  │  │  Service  │  │  Service  │  │   Pipeline        │    │    │
│  │  └─────┬─────┘  └─────┬─────┘  └─────────┬─────────┘    │    │
│  │        │              │                  │              │    │
│  │  ┌─────┴──────────────┴──────────────────┴─────┐       │    │
│  │  │              AGENT ORCHESTRATOR              │       │    │
│  │  └─────┬──────────────┬──────────────────┬─────┘       │    │
│  │        │              │                  │              │    │
│  │  ┌─────┴─────┐  ┌─────┴─────┐  ┌────────┴────────┐    │    │
│  │  │  Memory   │  │  Action   │  │    Learning     │    │    │
│  │  │  Service  │  │  Service  │  │    Service      │    │    │
│  │  └───────────┘  └───────────┘  └─────────────────┘    │    │
│  │                                                          │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                    │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │                    DATA LAYER                            │    │
│  │                                                          │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │    │
│  │  │ MariaDB │  │  Redis  │  │OpenSearch│ │  Files  │    │    │
│  │  │(Frappe) │  │ Cache   │  │ Vectors │  │ Storage │    │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   EXTERNAL SERVICES                       │   │
│  │                                                           │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │   │
│  │  │ OpenAI │ │Anthropic│ │ Google │ │Calendar│ │dartwing│ │   │
│  │  │  API   │ │  API   │ │  API   │ │  APIs  │ │ _fone  │ │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10.2 Infrastructure Requirements

### Production Environment

| Component          | Specification    | Quantity | Purpose                        |
| ------------------ | ---------------- | -------- | ------------------------------ |
| **Web Servers**    | 4 vCPU, 8GB RAM  | 3        | Frappe + API Gateway           |
| **Worker Servers** | 4 vCPU, 8GB RAM  | 5        | Background jobs, AI calls      |
| **Voice Servers**  | 8 vCPU, 16GB RAM | 2        | Real-time voice processing     |
| **Database**       | 8 vCPU, 32GB RAM | 2        | MariaDB primary + replica      |
| **Redis**          | 2 vCPU, 8GB RAM  | 3        | Cache cluster                  |
| **OpenSearch**     | 4 vCPU, 16GB RAM | 3        | Vector store cluster           |
| **Object Storage** | -                | -        | S3/GCS for files, audio        |
| **CDN**            | -                | -        | Static assets, audio streaming |

### Scaling Triggers

| Metric             | Threshold | Action                  |
| ------------------ | --------- | ----------------------- |
| API latency P99    | >500ms    | Add web server          |
| Worker queue depth | >1000     | Add worker server       |
| Voice latency      | >1s       | Add voice server        |
| DB CPU             | >70%      | Scale up or add replica |
| OpenSearch latency | >200ms    | Add node                |
| Storage            | >80%      | Expand storage          |

### High Availability

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIGH AVAILABILITY SETUP                       │
│                                                                  │
│  Region: US-East                    Region: US-West             │
│  ┌────────────────────────┐        ┌────────────────────────┐  │
│  │                        │        │                        │  │
│  │  Load Balancer (Primary)│◄──────►│ Load Balancer (DR)    │  │
│  │         │              │        │         │              │  │
│  │    ┌────┴────┐         │        │    ┌────┴────┐        │  │
│  │    │ Web x3  │         │        │    │ Web x2  │        │  │
│  │    └────┬────┘         │        │    └────┬────┘        │  │
│  │         │              │        │         │              │  │
│  │  ┌──────┴──────┐       │        │  ┌──────┴──────┐      │  │
│  │  │DB Primary   │───────┼────────┼──│ DB Replica  │      │  │
│  │  └─────────────┘       │        │  └─────────────┘      │  │
│  │                        │        │                        │  │
│  └────────────────────────┘        └────────────────────────┘  │
│                                                                  │
│  RTO: 15 minutes    RPO: 5 minutes                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10.3 Performance Requirements

### Latency Targets

| Operation               | P50    | P95    | P99    | Max    |
| ----------------------- | ------ | ------ | ------ | ------ |
| Wake word detection     | 200ms  | 300ms  | 400ms  | 500ms  |
| Voice-to-text           | 300ms  | 500ms  | 800ms  | 1000ms |
| Text response (simple)  | 500ms  | 800ms  | 1200ms | 2000ms |
| Text response (complex) | 1500ms | 2500ms | 4000ms | 6000ms |
| Text-to-voice           | 300ms  | 500ms  | 700ms  | 1000ms |
| End-to-end voice        | 800ms  | 1500ms | 2500ms | 4000ms |
| Action execution        | 200ms  | 500ms  | 800ms  | 1500ms |
| Memory retrieval        | 50ms   | 100ms  | 200ms  | 500ms  |

### Throughput Targets

| Metric                   | Target | Burst |
| ------------------------ | ------ | ----- |
| Concurrent conversations | 1,000  | 2,500 |
| Messages per second      | 500    | 1,500 |
| Voice streams            | 200    | 500   |
| Actions per second       | 100    | 300   |
| API requests per second  | 2,000  | 5,000 |

### Resource Utilization

| Resource       | Normal | Alert | Critical |
| -------------- | ------ | ----- | -------- |
| CPU            | <60%   | >75%  | >90%     |
| Memory         | <70%   | >80%  | >95%     |
| Disk I/O       | <50%   | >70%  | >90%     |
| Network        | <40%   | >60%  | >80%     |
| DB connections | <70%   | >85%  | >95%     |

---

## 10.4 Security Requirements

### Authentication

| Method         | Use Case              | Implementation       |
| -------------- | --------------------- | -------------------- |
| Frappe Session | Web interface         | Cookie-based session |
| OAuth 2.0      | Mobile/Desktop apps   | JWT tokens           |
| API Key        | Server-to-server      | Encrypted key        |
| Biometric      | Voice verification    | Voiceprint match     |
| MFA            | High-security actions | TOTP/Push            |

### Encryption

| Data             | At Rest     | In Transit |
| ---------------- | ----------- | ---------- |
| Conversations    | AES-256-GCM | TLS 1.3    |
| Voice recordings | AES-256-GCM | TLS 1.3    |
| User preferences | AES-256-GCM | TLS 1.3    |
| API keys         | AES-256-GCM | TLS 1.3    |
| Database         | TDE         | TLS 1.3    |
| Backups          | AES-256     | N/A        |

### Security Controls

| Control             | Implementation           |
| ------------------- | ------------------------ |
| Input validation    | Sanitize all user input  |
| Rate limiting       | 100 req/min per user     |
| SQL injection       | Parameterized queries    |
| XSS prevention      | Content Security Policy  |
| CSRF protection     | Frappe CSRF tokens       |
| Session management  | Secure, HttpOnly cookies |
| Audit logging       | All access logged        |
| Penetration testing | Annual third-party test  |

### Compliance

| Standard      | Status                | Audit         |
| ------------- | --------------------- | ------------- |
| SOC 2 Type II | Required              | Annual        |
| HIPAA         | Required (healthcare) | Annual        |
| GDPR          | Required (EU)         | Ongoing       |
| CCPA          | Required (CA)         | Ongoing       |
| ISO 27001     | Optional              | Every 3 years |

---

## 10.5 Data Requirements

### Data Models

```python
# Core VA DocTypes

va_doctypes = {
    "VA Instance": {
        "description": "Per-employee VA configuration",
        "fields": 22,
        "indexes": ["employee", "company"],
        "estimated_rows": 10000
    },
    "VA Conversation": {
        "description": "Conversation sessions",
        "fields": 12,
        "indexes": ["employee", "started_at"],
        "estimated_rows": 1000000,
        "retention": "90 days"
    },
    "VA Conversation Turn": {
        "description": "Individual messages",
        "fields": 15,
        "indexes": ["conversation", "timestamp"],
        "estimated_rows": 10000000,
        "retention": "90 days"
    },
    "VA Memory": {
        "description": "Long-term memories",
        "fields": 14,
        "indexes": ["employee", "memory_type"],
        "estimated_rows": 500000
    },
    "VA Action Log": {
        "description": "Action audit trail",
        "fields": 16,
        "indexes": ["employee", "timestamp", "action_type"],
        "estimated_rows": 5000000,
        "retention": "1 year"
    },
    "VA Audit Log": {
        "description": "Security audit trail",
        "fields": 18,
        "indexes": ["timestamp", "employee", "event_type"],
        "estimated_rows": 20000000,
        "retention": "7 years"
    }
}
```

### Storage Estimates

| Data Type         | Per User/Month | 10K Users/Year |
| ----------------- | -------------- | -------------- |
| Conversations     | 5 MB           | 600 GB         |
| Voice recordings  | 50 MB          | 6 TB           |
| Memories          | 1 MB           | 120 GB         |
| Action logs       | 2 MB           | 240 GB         |
| Audit logs        | 10 MB          | 1.2 TB         |
| Vector embeddings | 20 MB          | 2.4 TB         |
| **Total**         | **88 MB**      | **10.5 TB**    |

### Backup Strategy

| Data       | Frequency  | Retention | Location        |
| ---------- | ---------- | --------- | --------------- |
| Database   | Continuous | 30 days   | Cross-region    |
| Files      | Daily      | 90 days   | Cross-region    |
| Audit logs | Daily      | 7 years   | Archive storage |
| Configs    | On change  | Forever   | Git + backup    |

---

## 10.6 API Specifications

### REST API

```yaml
openapi: 3.0.0
info:
  title: Dartwing VA API
  version: 1.0.0

paths:
  /api/method/dartwing_va.api.process_message:
    post:
      summary: Process a VA message
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                conversation_id:
                  type: string
                modality:
                  type: string
                  enum: [text, voice]
      responses:
        200:
          description: VA response
          content:
            application/json:
              schema:
                type: object
                properties:
                  response:
                    type: string
                  actions:
                    type: array
                  conversation_id:
                    type: string

  /api/method/dartwing_va.api.get_memories:
    get:
      summary: Get user memories
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        200:
          description: List of memories

  /api/method/dartwing_va.api.execute_action:
    post:
      summary: Execute VA action
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                action:
                  type: string
                params:
                  type: object
      responses:
        200:
          description: Action result
```

### WebSocket API

```javascript
// WebSocket connection for real-time voice

const ws = new WebSocket('wss://api.dartwing.com/va/voice');

// Client → Server messages
ws.send(JSON.stringify({
  type: 'audio_chunk',
  data: base64AudioData,
  timestamp: Date.now()
}));

ws.send(JSON.stringify({
  type: 'interrupt',
  timestamp: Date.now()
}));

// Server → Client messages
{
  type: 'transcription',
  text: 'partial transcription...',
  is_final: false
}

{
  type: 'response_audio',
  data: base64AudioData,
  is_final: false
}

{
  type: 'action_result',
  action: 'create_expense',
  result: { expense_id: 'EXP-001', status: 'submitted' }
}
```

### Rate Limits

| Endpoint        | Limit        | Window   |
| --------------- | ------------ | -------- |
| Process message | 60           | 1 minute |
| Execute action  | 30           | 1 minute |
| Get memories    | 100          | 1 minute |
| Voice stream    | 5 concurrent | -        |
| Bulk operations | 10           | 1 hour   |

---

## 10.7 Client Requirements

### Flutter Mobile (iOS/Android)

| Requirement     | iOS                                 | Android              |
| --------------- | ----------------------------------- | -------------------- |
| **Minimum OS**  | iOS 14.0                            | Android 8.0 (API 26) |
| **Target OS**   | iOS 17.0                            | Android 14 (API 34)  |
| **Storage**     | 200 MB                              | 200 MB               |
| **RAM**         | 2 GB                                | 2 GB                 |
| **Permissions** | Microphone, Location, Notifications | Same                 |
| **Background**  | Limited                             | Foreground service   |

### Flutter Desktop

| Requirement    | macOS  | Windows   | Linux        |
| -------------- | ------ | --------- | ------------ |
| **Minimum OS** | 11.0   | 10 (1903) | Ubuntu 20.04 |
| **Target OS**  | 14.0   | 11        | Ubuntu 22.04 |
| **Storage**    | 300 MB | 300 MB    | 300 MB       |
| **RAM**        | 4 GB   | 4 GB      | 4 GB         |

### Web (Frappe)

| Requirement    | Specification                                 |
| -------------- | --------------------------------------------- |
| **Browsers**   | Chrome 90+, Firefox 90+, Safari 15+, Edge 90+ |
| **JavaScript** | ES2020                                        |
| **WebSocket**  | Required                                      |
| **WebRTC**     | Required for voice                            |
| **Storage**    | IndexedDB for offline                         |

---

## 10.8 Integration Requirements

### AI Provider APIs

| Provider  | API Version | Rate Limit | Fallback |
| --------- | ----------- | ---------- | -------- |
| OpenAI    | v1          | 10K RPM    | Claude   |
| Anthropic | 2024-01-01  | 4K RPM     | GPT-4o   |
| Google    | v1          | 60 RPM     | Claude   |

### Frappe Integration

| Requirement      | Version |
| ---------------- | ------- |
| Frappe Framework | 15.x    |
| ERPNext          | 15.x    |
| HRMS             | 15.x    |
| Frappe CRM       | 1.x     |
| Frappe Drive     | 1.x     |
| Frappe Health    | 15.x    |
| dartwing_fone    | 1.x     |
| dartwing_company | 1.x     |
| dartwing_core    | 1.x     |

### External Services

| Service              | Purpose        | SLA    |
| -------------------- | -------------- | ------ |
| Google Calendar API  | Calendar sync  | 99.9%  |
| Microsoft Graph API  | O365 calendar  | 99.9%  |
| Twilio/dartwing_fone | Voice/SMS      | 99.95% |
| AWS S3/GCS           | File storage   | 99.99% |
| SendGrid             | Email delivery | 99.9%  |

---

## 10.9 Testing Requirements

### Test Coverage

| Component         | Unit | Integration | E2E |
| ----------------- | :--: | :---------: | :-: |
| Coordinator Agent | 90%  |     80%     | 70% |
| Sub-Agents        | 90%  |     80%     | 70% |
| Voice Pipeline    | 85%  |     75%     | 60% |
| Memory System     | 90%  |     85%     | 75% |
| Action Engine     | 95%  |     90%     | 80% |
| API Layer         | 95%  |     90%     | 80% |

### Test Types

| Type              | Frequency    | Tools               |
| ----------------- | ------------ | ------------------- |
| Unit tests        | Every commit | pytest, Jest        |
| Integration tests | Every PR     | pytest, Frappe test |
| E2E tests         | Daily        | Playwright          |
| Load tests        | Weekly       | Locust, k6          |
| Security tests    | Monthly      | OWASP ZAP           |
| Chaos tests       | Monthly      | Chaos Monkey        |

### Performance Benchmarks

```python
# Performance test scenarios

scenarios = [
    {
        "name": "Simple query",
        "users": 100,
        "duration": "5m",
        "target_p95": "800ms"
    },
    {
        "name": "Complex query",
        "users": 50,
        "duration": "5m",
        "target_p95": "2500ms"
    },
    {
        "name": "Voice conversation",
        "users": 20,
        "duration": "10m",
        "target_p95": "1500ms"
    },
    {
        "name": "Peak load",
        "users": 500,
        "duration": "15m",
        "target_error_rate": "<1%"
    }
]
```

---

## 10.10 Monitoring Requirements

### Metrics

| Category           | Metrics                                             |
| ------------------ | --------------------------------------------------- |
| **Application**    | Request rate, latency, errors, queue depth          |
| **AI**             | Token usage, model latency, fallback rate           |
| **Voice**          | Stream count, audio quality, transcription accuracy |
| **Business**       | DAU, conversations, actions, NPS                    |
| **Infrastructure** | CPU, memory, disk, network                          |

### Alerts

| Alert                  | Condition               | Severity | Response     |
| ---------------------- | ----------------------- | -------- | ------------ |
| High latency           | P95 > 2x target         | Warning  | Investigate  |
| Error spike            | Error rate > 1%         | Critical | On-call page |
| AI provider down       | 3 consecutive failures  | Critical | Failover     |
| Voice quality degraded | MOS < 3.5               | Warning  | Investigate  |
| Cost anomaly           | Daily cost > 2x average | Warning  | Review       |

### Dashboards

| Dashboard  | Audience           | Refresh   |
| ---------- | ------------------ | --------- |
| Operations | Engineering        | Real-time |
| Business   | Product/Leadership | Hourly    |
| Cost       | Finance            | Daily     |
| Security   | Security team      | Real-time |

### Logging

| Log Type         | Retention | Storage                |
| ---------------- | --------- | ---------------------- |
| Application logs | 30 days   | CloudWatch/Stackdriver |
| Audit logs       | 7 years   | Cold storage           |
| Access logs      | 90 days   | SIEM                   |
| AI request logs  | 30 days   | CloudWatch             |

---

## 10.11 Disaster Recovery

### Recovery Objectives

| Metric                         | Target     |
| ------------------------------ | ---------- |
| RTO (Recovery Time Objective)  | 15 minutes |
| RPO (Recovery Point Objective) | 5 minutes  |
| MTTR (Mean Time to Recovery)   | 30 minutes |

### Failure Scenarios

| Scenario           | Detection       | Recovery               |
| ------------------ | --------------- | ---------------------- |
| Web server failure | Health check    | Auto-replace from ASG  |
| Database failure   | Replication lag | Promote replica        |
| AI provider outage | API errors      | Automatic fallback     |
| Region outage      | Health check    | DNS failover to DR     |
| Data corruption    | Integrity check | Point-in-time recovery |

### DR Procedures

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISASTER RECOVERY RUNBOOK                     │
│                                                                  │
│  1. DETECTION                                                    │
│     • Automated alerts from monitoring                          │
│     • Manual escalation if needed                               │
│                                                                  │
│  2. ASSESSMENT (5 min)                                          │
│     • Identify scope of failure                                 │
│     • Determine if DR failover needed                           │
│     • Notify stakeholders                                       │
│                                                                  │
│  3. FAILOVER (10 min)                                           │
│     • Promote DR database                                       │
│     • Update DNS to DR region                                   │
│     • Verify services healthy                                   │
│                                                                  │
│  4. VERIFICATION (5 min)                                        │
│     • Run smoke tests                                           │
│     • Verify critical flows                                     │
│     • Monitor for errors                                        │
│                                                                  │
│  5. COMMUNICATION                                                │
│     • Update status page                                        │
│     • Notify customers if needed                                │
│     • Internal post-mortem scheduled                            │
└─────────────────────────────────────────────────────────────────┘
```

---

_Next: Section 11 - Implementation Roadmap_

# Section 11: Implementation Roadmap

## 11.1 Release Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DARTWING VA RELEASE TIMELINE                  │
│                                                                  │
│  2026                                    2027                    │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  Q3 2026        Q4 2026        Q1 2027        Q2 2027           │
│  ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐            │
│  │ DEV  │──────│ DEV  │──────│ALPHA │──────│ BETA │            │
│  │      │      │      │      │      │      │      │            │
│  └──────┘      └──────┘      └──────┘      └──────┘            │
│                                                                  │
│         Q3 2027        Q4 2027        2028+                     │
│        ┌──────┐      ┌──────┐      ┌──────┐                    │
│  ──────│  GA  │──────│SCALE │──────│EXPAND│                    │
│        │      │      │      │      │      │                    │
│        └──────┘      └──────┘      └──────┘                    │
│                                                                  │
│  Milestones:                                                     │
│  • Q1 2027: Alpha (50 employees, internal)                      │
│  • Q2 2027: Beta (10 companies, 500 employees)                  │
│  • Q3 2027: GA (100 companies, 5,000 employees)                 │
│  • Q4 2027: Scale (500 companies, 25,000 employees)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11.2 Phase 1: Foundation (Q3-Q4 2026)

### Goals

- Core VA architecture
- Basic conversation capability
- Frappe integration foundation
- Initial sub-agents

### Deliverables

| Sprint    | Duration | Deliverables                                       |
| --------- | -------- | -------------------------------------------------- |
| **1-2**   | 4 weeks  | Project setup, DocTypes, basic API                 |
| **3-4**   | 4 weeks  | Coordinator agent, text conversation               |
| **5-6**   | 4 weeks  | HR sub-agent, HRMS integration                     |
| **7-8**   | 4 weeks  | Operations sub-agent, dartwing_company integration |
| **9-10**  | 4 weeks  | Memory system, conversation history                |
| **11-12** | 4 weeks  | Basic web UI, Flutter mobile shell                 |

### Feature Scope

| Feature              | Status | Notes                         |
| -------------------- | ------ | ----------------------------- |
| Text conversation    | ✓      | Basic coordinator             |
| HR sub-agent         | ✓      | Clock in/out, leave, schedule |
| Operations sub-agent | ✓      | Jobs, forms, status           |
| Conversation history | ✓      | Store and retrieve            |
| Basic memory         | ✓      | Preferences only              |
| Web interface        | ✓      | Text-only                     |
| Mobile shell         | ✓      | Text-only                     |
| Voice interface      | ✗      | Phase 2                       |
| Personality quiz     | ✗      | Phase 2                       |
| Custom agents        | ✗      | Phase 3                       |

### Team Requirements

| Role              | Count | Focus                        |
| ----------------- | ----- | ---------------------------- |
| Tech Lead         | 1     | Architecture, AI integration |
| Backend Engineer  | 2     | Frappe, sub-agents           |
| AI/ML Engineer    | 1     | Coordinator, prompts         |
| Frontend Engineer | 1     | Web UI                       |
| Flutter Engineer  | 1     | Mobile app                   |
| QA Engineer       | 1     | Testing                      |

### Exit Criteria

- [ ] Text conversations work end-to-end
- [ ] HR sub-agent handles clock in/out, leave requests
- [ ] Operations sub-agent handles job lookup/updates
- [ ] Conversations stored and retrievable
- [ ] Basic web and mobile interfaces functional
- [ ] 80% unit test coverage

---

## 11.3 Phase 2: Alpha (Q1 2027)

### Goals

- Voice interface
- Personality matching
- Full sub-agent suite
- Internal testing with 50 employees

### Deliverables

| Sprint    | Duration | Deliverables                      |
| --------- | -------- | --------------------------------- |
| **13-14** | 4 weeks  | Voice pipeline (OpenAI 4o)        |
| **15-16** | 4 weeks  | Wake word, interruption handling  |
| **17-18** | 4 weeks  | Personality quiz, voice selection |
| **19-20** | 4 weeks  | CRM sub-agent, Calendar sub-agent |
| **21-22** | 4 weeks  | Knowledge sub-agent (RAG)         |
| **23-24** | 4 weeks  | Alpha testing, bug fixes          |

### Feature Scope

| Feature               | Status | Notes                  |
| --------------------- | ------ | ---------------------- |
| Voice conversation    | ✓      | OpenAI 4o integration  |
| Wake word             | ✓      | On-device detection    |
| Interruption handling | ✓      | Barge-in support       |
| Personality quiz      | ✓      | 20 questions           |
| Voice selection       | ✓      | 6 voices               |
| CRM sub-agent         | ✓      | Leads, deals, contacts |
| Calendar sub-agent    | ✓      | Schedule, availability |
| Knowledge sub-agent   | ✓      | RAG from Drive         |
| Finance sub-agent     | ✗      | Phase 3                |
| Manager oversight     | ✗      | Phase 3                |
| Company templates     | ✗      | Phase 3                |

### Alpha Criteria

| Criteria             | Target       |
| -------------------- | ------------ |
| Internal testers     | 50 employees |
| Task completion rate | >80%         |
| Voice latency P95    | <1.5s        |
| Daily active users   | >30          |
| NPS score            | >30          |
| Critical bugs        | 0            |

### Exit Criteria

- [ ] Voice conversations work reliably
- [ ] Personality quiz generates usable profiles
- [ ] All 5 core sub-agents functional
- [ ] 50 employees actively using daily
- [ ] No critical bugs in production
- [ ] Latency targets met

---

## 11.4 Phase 3: Beta (Q2 2027)

### Goals

- External beta customers
- Manager controls and oversight
- Finance sub-agent
- Company templates

### Deliverables

| Sprint    | Duration | Deliverables                      |
| --------- | -------- | --------------------------------- |
| **25-26** | 4 weeks  | Finance sub-agent, expense OCR    |
| **27-28** | 4 weeks  | Manager oversight, audit trail    |
| **29-30** | 4 weeks  | Company templates, deployment     |
| **31-32** | 4 weeks  | Privacy modes, consent management |
| **33-34** | 4 weeks  | External calendar integration     |
| **35-36** | 4 weeks  | Beta onboarding, support          |

### Feature Scope

| Feature            | Status | Notes                          |
| ------------------ | ------ | ------------------------------ |
| Finance sub-agent  | ✓      | Expenses, approvals            |
| Receipt OCR        | ✓      | Auto-categorization            |
| Manager oversight  | ✓      | Action logs, alerts            |
| Audit trail        | ✓      | Tamper-proof logging           |
| Company templates  | ✓      | Create and deploy              |
| Privacy modes      | ✓      | Whisper, off-record, incognito |
| Consent management | ✓      | Granular controls              |
| External calendars | ✓      | Google, Microsoft              |
| Custom agents      | ✗      | GA                             |
| Multi-language     | ✗      | Post-GA                        |

### Beta Criteria

| Criteria             | Target |
| -------------------- | ------ |
| Beta companies       | 10     |
| Total employees      | 500    |
| Task completion rate | >85%   |
| Voice adoption       | >30%   |
| Manager satisfaction | >4.0/5 |
| NPS score            | >40    |

### Exit Criteria

- [ ] 10 companies actively using
- [ ] 500+ employees on platform
- [ ] Finance sub-agent handling expenses
- [ ] Manager oversight working correctly
- [ ] Templates deployable
- [ ] Privacy modes tested and compliant
- [ ] External calendar sync reliable

---

## 11.5 Phase 4: GA (Q3 2027)

### Goals

- Public launch
- Custom sub-agents
- Full analytics
- Production hardening

### Deliverables

| Sprint    | Duration | Deliverables                |
| --------- | -------- | --------------------------- |
| **37-38** | 4 weeks  | Custom sub-agent builder    |
| **39-40** | 4 weeks  | Usage analytics dashboard   |
| **41-42** | 4 weeks  | Cost management tools       |
| **43-44** | 4 weeks  | SOC 2 compliance completion |
| **45-46** | 4 weeks  | Performance optimization    |
| **47-48** | 4 weeks  | GA launch, marketing        |

### Feature Scope

| Feature              | Status |
| -------------------- | ------ |
| Custom sub-agents    | ✓      |
| Usage analytics      | ✓      |
| Cost management      | ✓      |
| Bulk operations      | ✓      |
| Full compliance      | ✓      |
| All privacy features | ✓      |
| Production SLA       | ✓      |

### GA Criteria

| Criteria        | Target   |
| --------------- | -------- |
| Companies       | 100      |
| Employees       | 5,000    |
| MRR             | $150,000 |
| Task completion | >85%     |
| Voice adoption  | >40%     |
| Uptime          | 99.9%    |
| NPS             | >50      |

### Exit Criteria

- [ ] 100 paying companies
- [ ] 5,000 MAU
- [ ] $150K MRR
- [ ] SOC 2 Type II certified
- [ ] 99.9% uptime achieved
- [ ] All features documented
- [ ] Support team trained

---

## 11.6 Phase 5: Scale (Q4 2027+)

### Goals

- Rapid customer growth
- Multi-language support
- Advanced AI features
- Enterprise features

### Roadmap

| Quarter     | Focus          | Key Features                                 |
| ----------- | -------------- | -------------------------------------------- |
| **Q4 2027** | Scale          | Self-service signup, improved onboarding     |
| **Q1 2028** | International  | Spanish, French, German, Mandarin            |
| **Q2 2028** | Enterprise     | On-prem deployment, SSO, advanced compliance |
| **Q3 2028** | AI Advancement | Proactive insights, predictive suggestions   |
| **Q4 2028** | Platform       | Marketplace for custom agents, integrations  |

### Scale Targets

| Metric    | Q4 2027 | Q4 2028 |
| --------- | ------- | ------- |
| Companies | 500     | 2,000   |
| Employees | 25,000  | 100,000 |
| MRR       | $500K   | $2M     |
| Countries | 5       | 20      |
| Languages | 1       | 8       |

---

## 11.7 Risk Mitigation

### Technical Risks

| Risk                   | Probability | Impact   | Mitigation                              |
| ---------------------- | ----------- | -------- | --------------------------------------- |
| AI model quality       | Medium      | High     | Multiple providers, fallback chain      |
| Voice latency          | Medium      | High     | Edge processing, caching                |
| Scale issues           | Medium      | Medium   | Load testing, auto-scaling              |
| Integration complexity | High        | Medium   | Incremental integration, mocking        |
| Data security breach   | Low         | Critical | Encryption, audits, penetration testing |

### Business Risks

| Risk                  | Probability | Impact | Mitigation                         |
| --------------------- | ----------- | ------ | ---------------------------------- |
| Slow adoption         | Medium      | High   | Free tier, compelling demos        |
| Competition           | High        | Medium | Differentiation, speed to market   |
| AI cost overruns      | Medium      | Medium | Cost controls, efficient routing   |
| Regulatory changes    | Low         | High   | Compliance monitoring, flexibility |
| Key person dependency | Medium      | Medium | Documentation, cross-training      |

### Mitigation Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│                    RISK MITIGATION STRATEGIES                    │
│                                                                  │
│  AI QUALITY                                                      │
│  • Multi-provider support from day 1                            │
│  • Automatic fallback on failures                               │
│  • Human escalation path                                        │
│  • Continuous prompt optimization                               │
│                                                                  │
│  VOICE LATENCY                                                   │
│  • Edge processing for wake word                                │
│  • Streaming responses                                          │
│  • Response caching for common queries                          │
│  • Regional deployment                                          │
│                                                                  │
│  ADOPTION                                                        │
│  • Free tier for small teams                                    │
│  • ROI calculator and case studies                              │
│  • White-glove onboarding for enterprise                        │
│  • Integration with existing workflows                          │
│                                                                  │
│  SECURITY                                                        │
│  • SOC 2 from launch                                            │
│  • Regular penetration testing                                  │
│  • Bug bounty program                                           │
│  • Security-first architecture                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11.8 Success Metrics

### Product Metrics

| Metric                | Alpha | Beta | GA  | Scale |
| --------------------- | ----- | ---- | --- | ----- |
| DAU/MAU ratio         | 40%   | 50%  | 60% | 65%   |
| Task completion       | 80%   | 85%  | 85% | 90%   |
| Voice adoption        | 20%   | 30%  | 40% | 50%   |
| Avg sessions/user/day | 3     | 5    | 7   | 10    |
| Actions per session   | 2     | 3    | 4   | 5     |

### Business Metrics

| Metric          | Alpha | Beta  | GA    | Scale  |
| --------------- | ----- | ----- | ----- | ------ |
| Companies       | 1     | 10    | 100   | 500    |
| Employees       | 50    | 500   | 5,000 | 25,000 |
| MRR             | $0    | $15K  | $150K | $500K  |
| ARR             | $0    | $180K | $1.8M | $6M    |
| Churn (monthly) | -     | <5%   | <3%   | <2%    |

### Quality Metrics

| Metric          | Alpha | Beta  | GA    | Scale  |
| --------------- | ----- | ----- | ----- | ------ |
| Uptime          | 99%   | 99.5% | 99.9% | 99.95% |
| P95 latency     | 2s    | 1.5s  | 1.2s  | 1s     |
| Bug escape rate | <5%   | <3%   | <1%   | <0.5%  |
| NPS             | 30    | 40    | 50    | 60     |
| CSAT            | 3.5   | 4.0   | 4.2   | 4.5    |

---

## 11.9 Resource Plan

### Team Growth

| Role              | Phase 1 | Phase 2 | Phase 3 | GA     | Scale  |
| ----------------- | ------- | ------- | ------- | ------ | ------ |
| Tech Lead         | 1       | 1       | 1       | 1      | 2      |
| Backend Engineer  | 2       | 3       | 4       | 5      | 8      |
| AI/ML Engineer    | 1       | 2       | 2       | 3      | 4      |
| Frontend Engineer | 1       | 1       | 2       | 2      | 3      |
| Flutter Engineer  | 1       | 2       | 2       | 3      | 4      |
| QA Engineer       | 1       | 2       | 2       | 3      | 4      |
| DevOps            | 0       | 1       | 1       | 2      | 3      |
| Product Manager   | 0       | 1       | 1       | 1      | 2      |
| Designer          | 0       | 1       | 1       | 1      | 2      |
| **Total**         | **7**   | **14**  | **16**  | **21** | **32** |

### Infrastructure Costs

| Component  | Phase 1    | Phase 2     | GA          | Scale        |
| ---------- | ---------- | ----------- | ----------- | ------------ |
| Compute    | $2K/mo     | $5K/mo      | $15K/mo     | $40K/mo      |
| Database   | $500/mo    | $1K/mo      | $3K/mo      | $8K/mo       |
| AI APIs    | $1K/mo     | $5K/mo      | $20K/mo     | $60K/mo      |
| Storage    | $200/mo    | $500/mo     | $2K/mo      | $5K/mo       |
| Monitoring | $200/mo    | $500/mo     | $1K/mo      | $2K/mo       |
| **Total**  | **$4K/mo** | **$12K/mo** | **$41K/mo** | **$115K/mo** |

### Total Investment

| Category         | Year 1  | Year 2  |
| ---------------- | ------- | ------- |
| Personnel        | $1.5M   | $2.5M   |
| Infrastructure   | $250K   | $800K   |
| Tools & Services | $100K   | $200K   |
| Marketing        | $100K   | $500K   |
| **Total**        | **$2M** | **$4M** |

---

## 11.10 Go-to-Market Strategy

### Target Segments

| Segment        | Size               | Focus                       | Pricing     |
| -------------- | ------------------ | --------------------------- | ----------- |
| **SMB**        | 10-100 employees   | Self-service, quick ROI     | $29/user/mo |
| **Mid-Market** | 100-1000 employees | Templates, manager controls | $39/user/mo |
| **Enterprise** | 1000+ employees    | Custom agents, on-prem      | Custom      |

### Launch Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    GO-TO-MARKET STRATEGY                         │
│                                                                  │
│  ALPHA (Q1 2027)                                                │
│  • Internal employees only                                      │
│  • Focus on product-market fit                                  │
│  • Weekly feedback sessions                                     │
│                                                                  │
│  BETA (Q2 2027)                                                 │
│  • Invite-only beta                                             │
│  • 10 design partners (free)                                    │
│  • Case study development                                       │
│  • Pricing validation                                           │
│                                                                  │
│  GA (Q3 2027)                                                   │
│  • Product Hunt launch                                          │
│  • Content marketing (blog, videos)                             │
│  • Integration marketplace                                       │
│  • Referral program                                             │
│                                                                  │
│  SCALE (Q4 2027+)                                               │
│  • Paid acquisition (Google, LinkedIn)                          │
│  • Partner channel (Frappe ecosystem)                           │
│  • Enterprise sales team                                        │
│  • Conference presence                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Competitive Positioning

| Competitor                       | Weakness                       | Our Advantage                    |
| -------------------------------- | ------------------------------ | -------------------------------- |
| Generic AI assistants            | No business integration        | Deep Frappe/ERPNext integration  |
| Enterprise AI (Salesforce, etc.) | Expensive, complex             | Affordable, easy setup           |
| Point solutions                  | Fragmented experience          | Unified single assistant         |
| Chatbots                         | No voice, limited intelligence | Voice-first, personality-matched |

---

## 11.11 Dependencies & Assumptions

### Dependencies

| Dependency                  | Owner    | Risk   | Mitigation               |
| --------------------------- | -------- | ------ | ------------------------ |
| OpenAI GPT-4o availability  | OpenAI   | Medium | Multi-provider support   |
| dartwing_fone readiness     | Internal | Low    | Existing production      |
| dartwing_company completion | Internal | Medium | Parallel development     |
| Frappe 15.x stability       | Frappe   | Low    | Active community         |
| Google Gems availability    | Google   | Medium | Alternative local models |

### Assumptions

| Assumption                           | Confidence | Impact if Wrong       |
| ------------------------------------ | ---------- | --------------------- |
| Voice AI latency continues improving | High       | Degrade to text-first |
| AI costs decrease over time          | High       | Adjust pricing        |
| Employees will adopt voice           | Medium     | Text-first fallback   |
| Companies want AI oversight          | High       | Simplify controls     |
| Frappe ecosystem grows               | Medium     | Standalone mode       |

---

## 11.12 Document Approval

### Stakeholders

| Name               | Role        | Approval |
| ------------------ | ----------- | -------- |
| [Product Owner]    | Product     | ☐        |
| [Engineering Lead] | Engineering | ☐        |
| [Design Lead]      | Design      | ☐        |
| [Business Owner]   | Business    | ☐        |

### Version History

| Version | Date         | Author | Changes     |
| ------- | ------------ | ------ | ----------- |
| 1.0     | Nov 28, 2025 | Claude | Initial PRD |

### Next Steps

1. ☐ Stakeholder review and approval
2. ☐ Technical architecture document
3. ☐ Detailed sprint planning for Phase 1
4. ☐ Team hiring/allocation
5. ☐ Development environment setup
6. ☐ Sprint 1 kickoff

---

_End of Dartwing VA Product Requirements Document_
