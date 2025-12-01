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

Instead of building yet another siloed AMS, Dartwing Associations extends a shared, global **Person / Organization** graph and wraps it in a modern UX that feels like **Notion + Rippling + Stripe** for:

- Homeowners associations (HOAs)
- Country clubs & golf clubs
- Alumni associations
- Professional societies & trade groups

Key principles:

- **One mobile + web app** for staff, board and members
- **One global `Person` record** across all Dartwing products
- **White-label first:** custom domain, branding, and email in minutes
- **All six required pillars already covered** by Dartwing Core, with incremental work to tailor for associations (compliance, wording, workflows).

---

## 2. Goals & Success Metrics

### 2.1 Product Goals

1. **Unify association operations** (membership, dues, events, communications, violations, ARC, amenities, work orders) in a single system.
2. **Slash staff workload** via self-service portals, automations, and mobile-first workflows.
3. **Delight members** with modern UX, real-time communications, and transparent financials.
4. **Leverage Dartwing Core** to minimize new surface area while maximizing re-use of proven infrastructure.

### 2.2 Acceptance Criteria (Go / No-Go)

- A **500-unit Florida HOA** migrates from TOPS in < 2 weeks (data + workflows).
- A **country club** books ~120 tee times/day with zero double-booking conflicts.
- A **5,000-member alumni association** runs a gala with QR check-in; per-person check-in time < 90 seconds.
- System passes **full state audit** for HOAs (FL DBPR, CA Davis–Stirling, TX POAA equivalents).
- Mobile app (DartwingFone branded for association) earns **≥ 4.8 rating** on both iOS and Android within 12 months of GA.

---

## 3. Target Customers & Use Cases

### 3.1 Primary Segments

- **Residential HOAs / Condo Associations** (50 – 5,000 doors)
- **Country Clubs / Golf & Social Clubs**
- **Alumni Associations**
- **Professional Societies & Trade Associations**

### 3.2 Core Use Cases

- Manage member rosters, units, and households
- Automate dues billing, collections, and delinquencies
- Enforce rules & regulations (violations, hearings, fines)
- Handle ARC (Architectural Review Committee) submissions and approvals
- Run events (in-person and virtual) and track continuing education
- Operate committees, chapters, SIGs, and boards
- Run maintenance & work orders with vendors
- Communicate via email, SMS, push, and emergency alerts
- Provide self-service portal & mobile app for members

---

## 4. Functional Requirements

### 4.1 Core Data Management & Administration

**Objectives:** Single source of truth for people, properties/units, organizations, and governance structure with strong security and reporting.

| Capability                      | Dartwing Implementation                                                | Status | Notes / Gaps                    |
| ------------------------------- | ---------------------------------------------------------------------- | ------ | ------------------------------- |
| Centralized Master Database     | Global `Person` + `Organization` + related DocTypes on Frappe/Postgres | 100%   | Already powering 13,800+ orgs   |
| Data Reporting, Analytics & BI  | Frappe Insights, 50+ pre-built reports, custom dashboards, Power BI    | 100%   | Add HOA/club report pack        |
| Data Security & Privacy         | Keycloak MFA/WebAuthn, column encryption, S3 Object Lock, BAA support  | 100%   | Exceeds typical AMS security    |
| Staff Productivity & Automation | Background jobs, 200+ automations (reminders, violations, dues)        | 100%   | Add association recipes         |
| Role & User Management          | Scoped RBAC (row/field level), custom roles per association/chapter    | 100%   | HOA roles (Board, ARC, Mgmt Co) |
| Data Export & Scalability       | Full JSON/CSV export; >500k member scale; multi-region active/active   | 100%   | No new infra needed             |

**Deliverables:**

- Association-specific role templates (Board Member, Property Manager, ARC Chair, Committee Member).
- Pre-built association dashboards (financial health, delinquencies, violations, work orders, requests).

---

### 4.2 Financial & Accounting Management

**Objectives:** End-to-end financial lifecycle for dues, assessments, fees, and events with strong accounting integrations.

| Capability                    | Dartwing Implementation                                                           | Status              |
| ----------------------------- | --------------------------------------------------------------------------------- | ------------------- |
| Integrated Payment Processing | Stripe, Plaid ACH, Apple/Google Pay, recurring billing, daily auto-recon          | 100%                |
| Dues & Invoicing Automation   | Recurring invoices, proration, late fees, delinquency workflows, payment plans    | 100%                |
| Accounting Integration        | Built-in double-entry + 2-way sync with QuickBooks, Xero, NetSuite                | 100%                |
| Payment Handling & Tracking   | Cards, ACH, checks, wires; refunds; sponsor/grant tracking                        | 100%                |
| Tax & Reporting Compliance    | VAT/GST/sales tax engine; 1099/990; state-specific HOA financial packs (FL/CA/TX) | 100% (content 2026) |

**Association-Specific Items:**

- **Special assessments** (one-time, staged, or time-bound).
- **Reserve funding** tracking and reporting.
- Segmented GL for **operating vs reserve vs capital** funds (config via templates).

---

### 4.3 Membership Lifecycle & Engagement

**Objectives:** Represent complex membership structures, handle join/renew/upgrade flows, and drive engagement.

| Capability                           | Dartwing Implementation                                                                     | Status   |
| ------------------------------------ | ------------------------------------------------------------------------------------------- | -------- |
| Complex Membership Structures        | Unlimited tiers/levels (individual, family, corporate, lifetime, student) + household links | 100%     |
| Online Member Portal & Self-Service  | DartwingFone + web portal; pay dues, update info, book amenities, vote, submit ARC          | 100%     |
| Communication Tools (Email/SMS/Push) | Campaigns; SMS (Twilio/Telnyx); push; emergency broadcast with read receipts                | 100%     |
| Content Targeting & Personalization  | Smart lists, dynamic content, segments; AI recommendations                                  | ~95%     |
| Career & Professional Development    | Job board, career center, LMS integration, certification tracking                           | 100%     |
| Community & Networking               | Chapters, committees, SIGs, doc vaults, threaded discussions, @mentions                     | 100%     |
| Voting & Elections                   | Secure member voting (simple majority, supermajority), ballots, results dashboards          | v1 scope |

**Enhancements:**

- Standard flows for **board elections**, **bylaw changes**, and **member referenda** (quorum, proxies, weighted votes).
- Templates for **welcome journeys**, **renewal nudges**, and **lapsed campaigns**.

---

### 4.4 Events & Education

**Objectives:** Robust event management for both social and educational programming.

| Capability                       | Dartwing Implementation                                                           | Status                         |
| -------------------------------- | --------------------------------------------------------------------------------- | ------------------------------ |
| Event Management & Registration  | Tracks, sessions, speakers, rooms, badges, QR check-in, waitlists, discount codes | 100%                           |
| Event History Tracking           | Per-member attendance history stored indefinitely                                 | 100%                           |
| Learning Management System (LMS) | Native integration with LearnDash, Thinkific; built-in mini-LMS planned           | Connectors live; mini-LMS 2026 |

**Enhancements:**

- CE/CME/CEU tracking and transcript export for professional societies.
- Membership-dependent pricing and perks (member vs non-member, guest passes).

---

### 4.5 Technology & Architecture

**Objectives:** Open, extensible, secure foundation leveraging Dartwing Core.

| Capability                        | Dartwing Implementation                                               | Status |
| --------------------------------- | --------------------------------------------------------------------- | ------ |
| Integration Capabilities (APIs)   | REST + GraphQL (Hasura), 40+ pre-built connectors, Zapier/Make/n8n    | 100%   |
| Website Management & CMS          | Built-in CMS or instant integration with WordPress/Webflow/Framer     | 100%   |
| Mobile-First Design & Native Apps | DartwingFone → Flutter iOS/Android + PWA                              | 100%   |
| AI Capabilities                   | AI content generation, member recommendations, chatbot                | ~80%   |
| Marketing Automation              | Native sequences; integration with ActiveCampaign, HubSpot, Mailchimp | 100%   |

**Non-Functional Requirements:**

- SSO via Keycloak (SAML/OIDC) for large orgs and universities.
- Regional hosting options; data residency documentation.
- SLA tiers (baseline 99.9% with higher available).
- Audit trail for all critical entities (violations, work orders, ARC decisions, elections, financials).

---

### 4.6 Operations, Maintenance & Work Orders

**Objectives:** Treat maintenance and operations as first-class: track work orders, preventive maintenance, and vendors.

**Key Features:**

1. **Work Orders Module**

   - Resident, board, or staff can create work orders for:

     - Common areas (pool, lobby, elevators, landscaping, etc.)
     - Buildings and specific units/lots.

   - Fields: category, priority, location, description, photos, requester, due date, cost estimates.
   - Workflow: Submitted → Triaged → Assigned → In Progress → On Hold → Completed → Closed.
   - SLA timers and escalation rules (e.g., life-safety >24h violation → auto escalate).
   - Link to **vendors**, **contracts**, and **GL accounts**; ability to record time & materials.

2. **Preventive Maintenance Schedules**

   - Recurring tasks (elevators inspections, fire systems, roofs, generators, HVAC).
   - Calendar view of upcoming tasks; checklist templates by asset type.
   - Completion logging with photos and documents (e.g., inspection reports).
   - Reporting: overdue tasks, compliance status by building/asset.

3. **Asset & Location Directory (Light CMMS)**

   - Asset records for major equipment with serial number, install date, warranty, vendor.
   - Hierarchical locations: property → building → floor → unit → room/area.

---

### 4.7 Issue Tracking / Helpdesk & Knowledge Base

**Objectives:** Reduce emails to management/board by centralizing resident questions, complaints, and requests.

**Key Features:**

1. **Requests / Cases Module**

   - Types: general question, complaint, service request, document request, billing inquiry, etc.
   - Routing rules:

     - By category (billing → management; rules → board; amenities → concierge).
     - By building or chapter.

   - SLA settings per request type; status tracking (new, in review, waiting on member, resolved, closed).
   - Public/private comments with email/SMS push updates.

2. **Resident-Facing Knowledge Base**

   - Articles for bylaws, policies, FAQ, “How to pay dues,” “Trash & recycling schedules,” “Pool rules.”
   - Searchable from web + mobile; optionally protected (members-only vs public).
   - Versioning (policy updates); effective dates.

3. **Future AI Hook**

   - API contract for AI assistant to answer resident questions from KB + bylaws without staff intervention.

---

### 4.8 Board Governance & Meeting Management

**Objectives:** Provide a full **board portal** for agenda, packets, minutes, motions, and governance records.

**Key Features:**

1. **Board & Committee Portal**

   - Secure board view in web + mobile with:

     - Upcoming meetings and agendas.
     - Packets: automatically generated PDF with financial reports, violations summary, ARC queue, work orders, etc.

   - Board-only documents vs owner-visible documents.

2. **Agenda Builder & Packets**

   - Agenda templates (regular meeting, annual meeting, emergency meeting).
   - Drag-and-drop agenda items; attach supporting docs.
   - “Generate packet” button that pulls live data (financials, key reports) and attaches static snapshots.

3. **Minutes & Motions**

   - Minute-taking tool linked to agenda items and motions.
   - Motion records: maker, seconder, vote breakdown, result, effective date.
   - Resolution log per association with searchable history.

4. **E-Sign & Approvals**

   - E-signature workflows for resolutions, contracts, and meeting minutes via DocuSign/Adobe Sign connectors.
   - Approval routing (e.g., President + Secretary must sign; property manager counter-signs).

5. **Election & Proxy Compliance**

   - Proxy management (paper and electronic).
   - Quorum tracking (live and final).
   - Certified results record attached to minutes.

---

### 4.9 Member CRM & Task Management

**Objectives:** Turn the `Person` graph into a true CRM with timelines, tasks, and basic pipelines.

**Key Features:**

1. **360° Member Timeline**

   - Unified timeline per person/household:

     - Join/renewal history, membership tier changes.
     - Dues invoices and payments, delinquencies.
     - Violations, ARC requests, work orders tied to the unit.
     - Events attended, committees, roles held.
     - Requests/cases, email/SMS campaigns, notes.

   - Configurable view by role (manager vs board vs chapter admin).

2. **Tasks & Follow-ups**

   - Create tasks linked to members, units, sponsors, or cases.
   - Assign to staff/volunteers with due dates, reminders, and status.
   - Queues (e.g., “today’s collections calls,” “follow up with sponsors”).

3. **Light Pipelines (Phase 2, configuration via Core)**

   - Sponsorship pipeline (prospect → proposal → committed → invoiced → paid).
   - Major donor or partner pipeline for professional societies and alumni orgs.

---

### 4.10 Non-Dues Revenue: E-Commerce, Sponsorships & Donations

**Objectives:** Support non-dues revenue streams: merch, services, sponsorships, and donations.

**Key Features:**

1. **E-Commerce Storefront**

   - Catalog: merchandise (shirts, decals), services (parking passes, guest passes), digital products (reports).
   - Member vs public pricing; visibility controls (members-only items).
   - Order management: status, fulfillment notes, shipping vs pickup, taxes.

2. **Sponsorship Management**

   - Sponsorship products tied to events, newsletters, websites, amenities.
   - Inventory (number of “Gold Sponsor” slots).
   - Reporting: sponsor revenue by period, sponsor mix, renewal prompts.

3. **Donations & Fundraising (for alumni & societies)**

   - Donation forms with designation (general fund, scholarships, capital projects).
   - One-time and recurring gifts; pledge schedules.
   - Acknowledgment letters, tax receipts, and campaign roll-up reporting.

---

### 4.11 Multi-Chapter / Federation Support

**Objectives:** Support complex orgs with national bodies, chapters, and SIGs, including financial flows and delegated admin.

**Key Features:**

1. **Organizational Hierarchy**

   - Parent (national) organization with child chapters, sections, SIGs.
   - Ability to assign members to one or multiple chapters; primary affiliation flag.

2. **Financial Model**

   - Configurable dues split (e.g., 70% national / 30% chapter).
   - Local assessments created by chapters, billed centrally or locally.
   - Roll-up reporting: per-chapter membership, events, and P&L plus global overview.

3. **Delegated Administration & Data Scoping**

   - Chapter admins see only their chapter’s members, finances, events, and content.
   - National staff can impersonate chapter admins (support mode) with full audit trail.

4. **Chapter Websites & Branding**

   - Chapter microsites on subdomains (e.g., `denver.association.org`) skinned from a central theme.
   - Content sharing: national content pushes down; local content stays local.

---

### 4.12 Country Club / Golf-Specific Features

**Objectives:** Make Dartwing Associations viable for country/golf clubs by handling tee times, member charging, and golf workflows.

**Key Features (v1 may be “integrate with existing systems,” v2 native):**

1. **Tee Sheet Engine**

   - Time-slot grid per course/9; support for 9/18 hole rules and blocking out maintenance/tournament days.
   - Booking rules:

     - Different windows by member type (e.g., Full Golf vs Social).
     - Guest limits per member, per day/week.
     - Enforcement of pairings and cart sharing.

   - Waitlists with auto-promotion; no-show and cancellation tracking.

2. **Club POS & House Charging**

   - Integration to pro shop and F&B POS to post charges to member accounts.
   - Fees linked to tee times (carts, caddies, guest rounds).
   - Statements with dues + house charges combined.

3. **Golf-Specific Extras (Phase 2)**

   - Handicap integration via GHIN/other APIs.
   - Tournament rosters and scoring import.
   - Cart fleet utilization reports.

---

## 5. Signature Differentiators – “Only Dartwing Does This”

| Differentiator                                 | Description                                                                                                        |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Unified Life + Association in One App          | The same DartwingFone app can run your HOA, clubs, and your personal family lists/workflows from one login.        |
| Ultra-fast White-Labeling                      | Custom domain, branding, and email (e.g., `app.yourhoa.com`, `hello@yourhoa.com`) in under 5 minutes.              |
| Emergency Broadcast with Read Receipts         | One-tap hurricanes / emergencies broadcast; owners confirm receipt; full audit log.                                |
| Secure, Expiring Gate QR Codes                 | Time-bound access passes (e.g., 4-hour QR codes) for guests, vendors, or events; guards scan resident phones.      |
| Full Offline Mobile Experience                 | Board members can review packets, documents, and vote while offline; syncs on reconnect.                           |
| AI-Assisted Communications & Operations (2026) | “Generate March newsletter,” “Draft ARC denial letter,” “Summarize this board packet” → AI drafts, staff approves. |

---

## 6. Implementation Plan & Roadmap

### 6.1 Already Live via Dartwing Core / DartwingFone (≈93%)

- Global person/org data model
- Payments, invoicing, accounting integrations
- Events engine + check-in
- Communications (email/SMS/push, emergency broadcast)
- Mobile apps (DartwingFone)
- Role-based access control and automations

### 6.2 Association-Specific Layer (Q4 2025 – Q4 2026)

- HOA / association DocTypes:

  - Units/lots, buildings, common areas, assets
  - Violations, hearings, ARC requests, inspections
  - Board structure, terms, committees, chapters
  - Work orders, preventive maintenance, vendors, contracts
  - Requests/cases, knowledge base articles

- Out-of-the-box workflows:

  - Delinquency handling
  - Violations lifecycle
  - ARC approval flows
  - Election and ballot templates
  - Work order SLAs and maintenance plans
  - Requests/cases routing and SLAs

- Compliance Packs:

  - FL, CA, TX HOA / condo compliance templates (reports, notices, logs).

### 6.3 AI Roadmap (2026)

- **Q1 2026:** AI content generation for newsletters, announcements, event pages, and common letters (violation, ARC, delinquency).
- **Mid 2026:** Member and donor engagement recommendations (“at-risk members,” “likely to upgrade,” “lapsed donors”).
- **Late 2026:**

  - AI copilot for staff: natural language queries on data (e.g., “show all violations on Building C in last 90 days”).
  - Resident AI assistant tied to KB + bylaws (“How do I submit an ARC?” “What are pool hours?”).
  - Experimental: AI pre-screening of uploaded photos for potential violations.

### 6.4 GA Readiness (Q1 2027)

- Completion of association content packs and templates
- Documentation: admin guide, onboarding playbooks, migration runbooks
- Reference customers in each target segment (HOA, club, alumni, professional society)

---

## 7. Onboarding, Training & Support Experience

**Objectives:** Make implementation and ongoing change management a selling point, not a risk.

**Key Elements:**

1. **In-Product Onboarding**

   - Role-based checklists for:

     - Management company admin
     - Board member
     - Chapter admin

   - Guided setup flows:

     - Association profile, units, members import
     - Dues schedules and assessments
     - Payment gateways and accounting connection

2. **Training Center**

   - Embedded how-to videos, interactive tours, link to sandbox environment.
   - Sample data mode for training board members and staff without touching live data.

3. **Change Management & Releases**

   - Feature flags per association and per role.
   - In-app release notes with “What’s new” notifications.

4. **Support**

   - SLAs defined by contract tier.
   - In-app support widget linking to tickets (Requests/Cases module) with contextual metadata.

---

## 8. Launch & Sales Deliverables

At GA, the following must exist:

1. **Frappe DocType List & ERD** for Dartwing Associations (including new modules: Work Orders, Requests, Governance, CRM, E-comm, Chapters, Club).
2. **Demo Script & Demo Sandbox**

   - HOA demo (500-unit, coastal, with maintenance and storm scenario).
   - Club demo (tee times, F&B charges, events).
   - Alumni/professional association demo (events, CE, chapters, donations).

3. **Migration Toolkit**

   - Data mappings and scripts from TOPS, Vantaca, AppFolio, and generic AMS exports.
   - Checklist and templated communication plan for cutover.

4. **AI Roadmap Deck (2026+)**

   - For enterprise prospects emphasizing AI-driven operations.

---

If you want, next step I can pull out just the **new sections (4.6–4.12)** into a separate doc you can hand to engineering as a “delta spec” against existing Dartwing Core.

Dashboard additions to add to the prd
Let me define it cleanly so you can drop it into the PRD.

---

## New Section: 4.13 Member Dashboard & Self-Service Home

**Objective:** Give each member a single “command center” view (web + mobile) showing financial status, communications, tickets, and participation.

### 4.13.1 Financial Snapshot (Dues Status)

On login, the member sees a card with:

- **Current status label:**

  - “Ahead” (prepaid through >1 period in the future)
  - “Current” (fully paid through current period)
  - “Behind” (outstanding balance + days past due)

- **Account summary row:**

  - Current balance (credit or debit)
  - Next due date & amount
  - Oldest past-due amount (if any)
  - Autopay status (on/off; payment method)

- **History indicators:**

  - Last 12 months: count of **on-time vs late vs early** payments
  - Simple visual (e.g., 12-dot timeline with colors)

- **Payment actions (always visible):**

  - “Pay Now” → one-tap payment using saved method
  - “Change Payment Method” → manage cards/ACH
  - “View Statements” → list of invoices/receipts

**Acceptance criteria:**

- Member can tell in **one glance** whether they are ahead/current/behind and by how much.
- Member can complete a payment in **≤ 3 taps** from dashboard (with saved method).

---

### 4.13.2 Communications & Correspondence

Dedicated “Communications” card/section on the dashboard:

- **Inbox overview:**

  - Last X messages from association (announcements, violation letters, ARC decisions, statements, etc.).
  - Clear badges for “New” vs “Read”.

- **Direct communication with management/board:**

  - “Message Management” or “New Message” button → creates a **Request/Case** linked to the member and unit.
  - Category selection (billing, maintenance, rules, general).

- **History view:**

  - Chronological list of all communications: broadcast messages + direct messages.
  - Filters: “Announcements”, “Billing”, “Rules/Violations”, “My Tickets”.

- **Metrics surfaced:**

  - Total number of tickets ever created.
  - Currently open tickets (by status).
  - Last response time (e.g., “management replied 2 days ago”).

**Acceptance criteria:**

- Member can see all prior communications (broadcast + direct) in one place, filterable.
- Member can start a new conversation with management without hunting for email addresses.

---

### 4.13.3 Tickets / Requests Summary

Pulling from the **Requests/Cases** module:

- **Top-line counters on dashboard:**

  - Open requests: count, grouped by type (billing, maintenance, general).
  - Recently updated: “3 updated in last 7 days”.

- **List view snippet:**

  - Top 3 open tickets with:

    - Subject, type, created date, last activity, current status.
    - Quick action to open detail.

- **Detail (behind click/tap):**

  - Full message history, attachments, status changes, internal notes (where appropriate).

**Acceptance criteria:**

- Member can answer: “How many open tickets do I have, and what’s happening with each?” within **one click** from dashboard.

---

### 4.13.4 Events & Participation (“Roll Call”)

Dashboard card summarizing engagement:

- **Stats:**

  - Total events invited to vs attended vs missed (configurable window, e.g., last 12 months).
  - Next 3 upcoming events (with RSVP/registration state).

- **Attendance roll-call detail (behind tap):**

  - List of past events with:

    - Status: “Attended”, “Registered – No Show”, “Invited – Did Not Register”.
    - CE/credit earned (if applicable).

- **Actions:**

  - “View All Events” → opens event listing filtered to member’s org/chapter.
  - “Download Transcript” (for professional societies/CE).

**Acceptance criteria:**

- Member can understand their **engagement history** at a glance.
- For CE/education use cases, member can export an attendance/credit summary.

---

### 4.13.5 UX & Integration Notes

- **One Home Screen:** Dashboard is the **default landing page** for members in both web and DartwingFone.
- All data is powered by existing modules:

  - Financial snapshot → invoices/payments ledger.
  - Communications → broadcasts + Requests/Cases.
  - Tickets → Requests/Cases.
  - Participation → Events attendance records.

- **Configurable by association:** Admins can toggle cards (e.g., clubs show tee time stats later; HOAs surface violations history in v2).

---

### Where This Fits in the PRD

You can drop it into the PRD as:

> **4.13 Member Dashboard & Self-Service Home**
> (with the subsections above)

And cross-link it from:

- 4.3 Membership Lifecycle & Engagement (“Member dashboard/home is the primary entry point for all self-service”).
- 4.7 Issue Tracking / Helpdesk (“New ticket creation and ticket summary are surfaced on the member dashboard”).
- 4.10 Non-Dues Revenue (“Storefront offers and upcoming events can surface as promos on the dashboard card if enabled”).

---

If you’d like, I can now splice this verbatim into the latest PRD draft you and I just built, so you have one clean, updated document.
