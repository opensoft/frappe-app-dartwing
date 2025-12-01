# Dartwing Associations – Product Requirements Document (PRD)

**Product:** Dartwing Associations
**Tagline:** The only modern Association Management System (AMS) built on Dartwing Core
**Target GA:** Q1 2027
**Current Status:** 100% scoped – ~93% of core capabilities already live via Dartwing Core + DartwingFone

---

## 1. Executive Summary

Dartwing Associations is a next-generation Association Management System built on the existing Dartwing Core platform that already powers:

- High-volume, regulated workflows (e.g., 52M fax pages/month)
- Multi-tenant consumer use cases (1,400+ households)

Instead of building yet another siloed AMS, Dartwing Associations extends a shared, global Person / Organization graph and wraps it in a modern UX that feels like Notion + Rippling + Stripe for:

- Homeowners associations (HOAs)
- Country clubs & golf clubs
- Alumni associations
- Professional societies & trade groups

**Key principles:**

- One mobile + web app for staff, board and members.
- One global Person record across all Dartwing products.
- White-label first: custom domain, branding, and email in minutes.
- All six required pillars already covered by Dartwing Core, with incremental work to tailor for associations (compliance, wording, workflows).

---

## 2. Goals & Success Metrics

### 2.1 Product Goals

1.  Unify association operations (membership, dues, events, communications, violations, ARC, amenities, work orders) in a single system.
2.  Slash staff workload via self-service portals, automations, and mobile-first workflows.
3.  Delight members with modern UX, real-time communications, and transparent financials.
4.  Leverage Dartwing Core to minimize new surface area while maximizing re-use of proven infrastructure.

### 2.2 Acceptance Criteria (Go / No-Go)

- A 500-unit Florida HOA migrates from TOPS in < 2 weeks (data + workflows).
- A country club books ~120 tee times/day with zero double-booking conflicts.
- A 5,000-member alumni association runs a gala with QR check-in; per-person check-in time < 90 seconds.
- System passes full state audit for HOAs (FL DBPR, CA Davis–Stirling, TX POAA equivalents).
- Mobile app (DartwingFone branded for association) earns ≥ 4.8 rating on both iOS and Android within 12 months of GA.

---

## 3. Target Customers & Use Cases

### 3.1 Primary Segments

- Residential HOAs / Condo Associations (50 – 5,000 doors)
- Country Clubs / Golf & Social Clubs
- Alumni Associations
- Professional Societies & Trade Associations

### 3.2 Core Use Cases

- Manage member rosters, units, and households.
- Automate dues billing, collections, and delinquencies.
- Enforce rules & regulations (violations, hearings, fines).
- Handle ARC (Architectural Review Committee) submissions and approvals.
- Run events (in-person and virtual) and track continuing education.
- Operate committees, chapters, SIGs, and boards.
- Run maintenance & work orders with vendors.
- Communicate via email, SMS, push, and emergency alerts.
- Provide self-service portal & mobile app for members.

---

## 4. Functional Requirements

### 4.1 Core Data Management & Administration

**Objectives:** Single source of truth for people, properties/units, organizations, and governance structure with strong security and reporting.

| Capability                          | Dartwing Implementation                                               | Status | Notes / Gaps                    |
| :---------------------------------- | :-------------------------------------------------------------------- | :----- | :------------------------------ |
| **Centralized Master Database**     | Global Person + Organization + related DocTypes on Frappe/Postgres    | 100%   | Already powering 13,800+ orgs   |
| **Data Reporting, Analytics & BI**  | Frappe Insights, 50+ pre-built reports, custom dashboards, Power BI   | 100%   | Add HOA/club report pack        |
| **Data Security & Privacy**         | Keycloak MFA/WebAuthn, column encryption, S3 Object Lock, BAA support | 100%   | Exceeds typical AMS security    |
| **Staff Productivity & Automation** | Background jobs, 200+ automations (reminders, violations, dues)       | 100%   | Add association recipes         |
| **Role & User Management**          | Scoped RBAC (row/field level), custom roles per association/chapter   | 100%   | HOA roles (Board, ARC, Mgmt Co) |
| **Data Export & Scalability**       | Full JSON/CSV export; >500k member scale; multi-region active/active  | 100%   | No new infra needed             |

**Deliverables:**

- Association-specific role templates (Board Member, Property Manager, ARC Chair, Committee Member).
- Pre-built association dashboards (financial health, delinquencies, violations, work orders, requests).

### 4.2 Financial & Accounting Management

**Objectives:** End-to-end financial lifecycle for dues, assessments, fees, and events with strong accounting integrations.

| Capability                        | Dartwing Implementation                                                        | Status              |
| :-------------------------------- | :----------------------------------------------------------------------------- | :------------------ |
| **Integrated Payment Processing** | Stripe, Plaid ACH, Apple/Google Pay, recurring billing, daily auto-recon       | 100%                |
| **Dues & Invoicing Automation**   | Recurring invoices, proration, late fees, delinquency workflows, payment plans | 100%                |
| **Accounting Integration**        | Built-in double-entry + 2-way sync with QuickBooks, Xero, NetSuite             | 100%                |
| **Payment Handling & Tracking**   | Cards, ACH, checks, wires; refunds; sponsor/grant tracking                     | 100%                |
| **Tax & Reporting Compliance**    | VAT/GST/sales tax engine; 1099/990; state-specific HOA financial packs         | 100% (content 2026) |

**Association-Specific Items:**

- Special assessments (one-time, staged, or time-bound).
- Reserve funding tracking and reporting.
- Segmented GL for operating vs reserve vs capital funds (config via templates).

### 4.3 Membership Lifecycle & Engagement

**Objectives:** Represent complex membership structures, handle join/renew/upgrade flows, and drive engagement.

| Capability                              | Dartwing Implementation                                          | Status |
| :-------------------------------------- | :--------------------------------------------------------------- | :----- |
| **Complex Membership Structures**       | Unlimited tiers/levels (individual, family, corporate, lifetime) | 100%   |
| **Online Member Portal & Self-Service** | DartwingFone + web portal; pay dues, update info, book amenities | 100%   |
| **Communication Tools**                 | Campaigns; SMS (Twilio/Telnyx); push; emergency broadcast        | 100%   |
| **Content Targeting**                   | Smart lists, dynamic content, segments; AI recommendations       | ~95%   |
| **Community & Networking**              | Chapters, committees, SIGs, doc vaults, threaded discussions     | 100%   |

**Enhancements:**

- Standard flows for board elections, bylaw changes, and member referenda (quorum, proxies, weighted votes).
- Templates for welcome journeys, renewal nudges, and lapsed campaigns.

### 4.4 Events & Education

**Objectives:** Robust event management for both social and educational programming.

| Capability                 | Dartwing Implementation                                                | Status          |
| :------------------------- | :--------------------------------------------------------------------- | :-------------- |
| **Event Management**       | Tracks, sessions, speakers, rooms, badges, QR check-in, waitlists      | 100%            |
| **Event History Tracking** | Per-member attendance history stored indefinitely                      | 100%            |
| **LMS**                    | Native integration with LearnDash/Thinkific; built-in mini-LMS planned | Connectors live |

**Enhancements:**

- CE/CME/CEU tracking and transcript export for professional societies.
- Membership-dependent pricing and perks (member vs non-member, guest passes).

### 4.5 Technology & Architecture

**Objectives:** Open, extensible, secure foundation leveraging Dartwing Core.

| Capability                   | Dartwing Implementation                                    | Status |
| :--------------------------- | :--------------------------------------------------------- | :----- |
| **Integration Capabilities** | REST + GraphQL (Hasura), 40+ connectors, Zapier/Make       | 100%   |
| **Website Management & CMS** | Built-in CMS or instant integration with WordPress/Webflow | 100%   |
| **Mobile-First Design**      | DartwingFone → Flutter iOS/Android + PWA                   | 100%   |
| **AI Capabilities**          | AI content generation, member recommendations, chatbot     | ~80%   |

**Non-Functional Requirements:**

- SSO via Keycloak (SAML/OIDC).
- Audit trail for all critical entities (violations, work orders, ARC decisions, elections).

### 4.6 Operations, Maintenance & Work Orders

**Objectives:** Treat maintenance and operations as first-class: track work orders, preventive maintenance, and vendors.

**Key Features:**

- **Work Orders Module:**
  - Resident, board, or staff can create work orders for common areas or specific units.
  - Fields: category, priority, location, description, photos, requester, due date, cost estimates.
  - Workflow: Submitted → Triaged → Assigned → In Progress → On Hold → Completed → Closed.
  - SLA timers and escalation rules (e.g., life-safety >24h violation → auto escalate).
- **Preventive Maintenance Schedules:**
  - Recurring tasks (elevators, fire systems, roofs).
  - Calendar view of upcoming tasks; checklist templates.
- **Asset & Location Directory (Light CMMS):**
  - Asset records for major equipment with serial number, install date, warranty, vendor.
  - Hierarchical locations: property → building → floor → unit.

### 4.7 Issue Tracking / Helpdesk & Knowledge Base

**Objectives:** Reduce emails to management/board by centralizing resident questions.

**Key Features:**

- **Requests / Cases Module:**
  - Routing rules by category (billing → management; rules → board).
  - SLA settings per request type; status tracking.
  - Public/private comments with email/SMS push updates.
- **Resident-Facing Knowledge Base:**
  - Articles for bylaws, policies, FAQ, “How to pay dues,” “Trash & recycling schedules.”
  - Searchable from web + mobile; optionally protected (members-only vs public).
- **Future AI Hook:** API contract for AI assistant to answer resident questions from KB.

### 4.8 Board Governance & Meeting Management

**Objectives:** Provide a full board portal for agenda, packets, minutes, motions, and governance records.

**Key Features:**

- **Board & Committee Portal:** Secure view for upcoming meetings, agendas, and Board-only documents.
- **Agenda Builder & Packets:**
  - Drag-and-drop agenda items.
  - “Generate packet” button that pulls live data (financials, key reports) into a PDF.
- **Minutes & Motions:** Motion records (maker, seconder, vote breakdown); Resolution log.
- **E-Sign & Approvals:** Workflows for resolutions and contracts via DocuSign/Adobe Sign.
- **Election & Proxy Compliance:** Proxy management (paper/electronic) and Quorum tracking.

### 4.9 Member CRM & Task Management

**Objectives:** Turn the Person graph into a true CRM with timelines, tasks, and basic pipelines.

**Key Features:**

- **360° Member Timeline:** Unified timeline (Join history, Dues payments, Violations, Events attended, Requests/cases).
- **Tasks & Follow-ups:** Create tasks linked to members/units; Queues (e.g., “today’s collections calls”).
- **Light Pipelines:** Sponsorship pipeline; Major donor pipeline.

### 4.10 Non-Dues Revenue: E-Commerce, Sponsorships & Donations

**Objectives:** Support non-dues revenue streams.

**Key Features:**

- **E-Commerce Storefront:** Catalog for merchandise, services (parking passes), and digital products.
- **Sponsorship Management:** Sponsorship products, inventory slots, and revenue reporting.
- **Donations & Fundraising:** Forms with designation (general fund, scholarships); pledge schedules.

### 4.11 Multi-Chapter / Federation Support

**Objectives:** Support complex orgs with national bodies, chapters, and SIGs.

**Key Features:**

- **Organizational Hierarchy:** Parent (national) organization with child chapters/sections.
- **Financial Model:** Configurable dues split (e.g., 70% national / 30% chapter).
- **Delegated Admin:** Chapter admins see only their chapter’s members/finances.
- **Chapter Websites:** Microsites on subdomains (denver.association.org) skinned from a central theme.

### 4.12 Country Club / Golf-Specific Features

**Objectives:** Make Dartwing Associations viable for country/golf clubs.

**Key Features:**

- **Tee Sheet Engine:** Time-slot grid; support for 9/18 hole rules; blocking out maintenance.
- **Booking Rules:** Member type windows; Guest limits; Pairing enforcement.
- **Club POS & House Charging:** Integration to pro shop and F&B POS; combined statements.
- **Golf-Specific Extras (Phase 2):** Handicap integration; Tournament rosters.

---

### 4.13 Member Dashboard & Self-Service Home (New)

**Objective:** Give each member a single "command center" view.

**4.13.1 Financial Snapshot (Dues Status)**

- **Status Label:** "Ahead," "Current," or "Behind" (+ days past due).
- **Account Summary:** Current balance, next due date, autopay status.
- **Payment Actions:** "Pay Now" (≤ 3 taps), "Change Payment Method," "View Statements."
- **History Indicators:** Simple visual timeline of last 12 months payments.

**4.13.2 Communications & Correspondence**

- **Inbox Overview:** Last X messages (announcements, violation letters, statements). Badges for "New."
- **Direct Message:** "New Message" button creates a Request/Case linked to member/unit.
- **History View:** Chronological list of broadcasts + direct messages.

**4.13.3 Tickets / Requests Summary**

- **Top-line Counters:** Open requests count, grouped by type.
- **List View:** Top 3 open tickets with status/last activity.
- **Detail:** Full message history, attachments, internal notes (if visible).

**4.13.4 Events & Participation**

- **Stats:** Total events attended vs invited.
- **Next Up:** Next 3 upcoming events with RSVP state.
- **Roll Call:** List of past events with status (Attended/No-Show).

---

### 4.14 Vendor & Resale Operations (New - Revenue & Risk)

**Objective:** Close operational gaps and capture high-margin documentation revenue.

**4.14.1 Resale & Estoppel Portal**

- **External Portal:** Public-facing portal for Title Agents (non-members) to request closing docs.
- **Auto-Generation:** Logic to pull prorated dues + violations + assessments into a generated PDF.
- **Revenue Logic:** Configurable fee splits (e.g., Mgmt Co fee vs Platform transaction fee).

**4.14.2 Vendor Access Portal**

- **Limited Login:** Vendors only see assigned Work Orders and Invoices.
- **Field Ops:** Upload "Before/After" photos; mark task as "Complete."
- **Invoicing:** Submit PDF invoice directly to AP queue; link to Work Order.

**4.14.3 Risk Management (COI Shield)**

- **COI Tracking:** Vendors must upload Certificate of Insurance with expiration.
- **Blocking Logic:** System prevents assigning Work Orders or paying invoices if COI is expired.

---

### 4.15 Dartwing Gatekeeper: Global Access & LPR (New)

**Objective:** Hardware-agnostic, mobile-first access control utilizing the Global Graph.

**4.15.1 The "Dartwing Passport" (Global Identity)**

- **Concept:** Guest creates a profile _once_. Name, Photo, License Plate, Phone are stored globally.
- **Network Effect:** Works at _any_ Dartwing association. Access rights are local/time-bound; Identity is global.

**4.15.2 Pre-Auth & LPR Workflow**

- **Invite:** Member sends link (SMS/WhatsApp).
- **Enrollment:** Guest uploads selfie + plate photo.
- **Entry:** LPR Camera reads plate → Matches Pre-auth → Gate opens (Latency < 1.5s).
- **Notification:** Member receives push: _"John Doe arrived at Main Gate."_

**4.15.3 Dynamic QR & Bi-Directional Scanning**

- **Dynamic QR:** App displays TOTP QR (rotates every 30s) for laser scanners.
- **"Scan-to-Open" (Hardware-Lite):** Guest scans a static, weather-proof QR sticker on the pedestal. App validates GPS + Digital Key → Sends Open command via cloud.

**4.15.4 "Just-in-Time" Delivery Passes (Flash Link)**

- **Workflow:** Resident taps "Expecting Delivery" → Generates 1-hour link.
- **Driver:** Pastes link in Uber/DoorDash instructions. Driver clicks link → Validates GPS → Taps "Open Gate." No app download required.

**4.15.5 Vendor Geo-Fencing & Invoice Verification**

- **Timeclock:** Vendor scans to "Clock In" at entry.
- **Geo-Fence:** Flag session if vendor GPS leaves property while "Clocked In."
- **Billing Audit:** Board compares Invoice Hours vs Gate Log Hours.

**4.15.6 Security AI & Anomaly Detection**

- **Tailgating:** Correlate Loop Detector count vs Credential Scan count. (2 cars + 1 scan = Alert).
- **Mismatch:** Alert if valid credential (RFID) used with non-matching License Plate.

---

## 5. Signature Differentiators – “Only Dartwing Does This”

| Differentiator                 | Description                                                                      |
| :----------------------------- | :------------------------------------------------------------------------------- |
| **Unified Life + Association** | The same DartwingFone app runs your HOA, clubs, and personal family lists.       |
| **Ultra-fast White-Labeling**  | Custom domain, branding, and email in under 5 minutes.                           |
| **Emergency Broadcast**        | One-tap hurricane/emergency broadcast with read receipts & audit log.            |
| **Secure, Expiring Gate QR**   | Time-bound access passes; prevent screenshot sharing via TOTP.                   |
| **Full Offline Mobile**        | Board members can review packets and vote offline; syncs on reconnect.           |
| **AI Operations (2026)**       | "Draft ARC denial letter," "Summarize board packet," "Show me tailgating clips." |

---

## 6. Implementation Plan & Roadmap

**6.1 Already Live via Dartwing Core (≈93%)**

- Global person/org data model, Payments/Invoicing, Events engine, Communications, Mobile apps, RBAC.

**6.2 Association-Specific Layer (Q4 2025 – Q4 2026)**

- **HOA DocTypes:** Units/lots, Violations, ARC, Work orders (with Vendor Portal), Requests/Cases.
- **Workflows:** Delinquency pipelines, ARC approval flows, Election templates.
- **Compliance:** FL/CA/TX specific report packs.
- **Revenue Modules:** Resale/Estoppel generation.
- **Gatekeeper:** LPR integration, Flash Links, Scan-to-Open.

**6.3 AI Roadmap (2026)**

- **Q1 2026:** AI content generation (Newsletters, Violation letters).
- **Mid 2026:** Member engagement recommendations.
- **Late 2026:** AI Copilot for staff (Natural language data queries); Resident AI Assistant.

**6.4 GA Readiness (Q1 2027)**

- Completion of association content packs, Admin guides, Migration runbooks.

---

## 7. Onboarding, Training & Support Experience

**In-Product Onboarding:**

- Role-based checklists (Manager, Board, Chapter Admin).
- Guided setup flows (Profile, Import, Dues setup, Banking).

**Training Center:**

- Embedded how-to videos; Sample data mode ("Sandbox") for training without risk.

**Change Management:**

- Feature flags per association; In-app release notes.

**Support:**

- SLAs by contract tier; In-app support widget linking to Requests module.

---

## 8. Launch & Sales Deliverables

**At GA, the following must exist:**

1.  **Frappe DocType List & ERD:** Including new modules (Work Orders, Requests, Governance, CRM, E-comm, Chapters, Club, GateLog, Vehicle, Estoppel).
2.  **Demo Script & Sandbox:**
    - HOA demo (500-unit, coastal, storm scenario).
    - Club demo (tee times, F&B).
    - Gatekeeper demo (Delivery Driver "Flash Link" flow).
3.  **Migration Toolkit:** Scripts for TOPS, Vantaca, AppFolio exports.
4.  **AI Roadmap Deck:** For enterprise prospects emphasizing future-proofing.
