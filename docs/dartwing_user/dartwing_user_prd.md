# Dartwing User Module – Product Requirements Document

**Version 2.0 | November 2025**

**Product Owner:** Brett  
**Target Release:** Q2 2026 (Phase 1)  
**Status:** Complete

---

## Table of Contents

1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Personas
5. Feature Requirements
6. Detailed Feature Specifications
7. User Stories & Acceptance Criteria
8. User Flows
9. Non-Functional Requirements
10. Dependencies & Integrations
11. Risks & Mitigations
12. Release Plan
13. Data Model
14. API Specification
15. Appendices

---

## 1. Executive Summary

### 1.1 Product Vision

The Dartwing User Module provides a **unified personal identity layer** that enables individuals to seamlessly navigate across all their organizations—families, companies, nonprofits, clubs, and associations—with a single login and personalized experience.

Unlike traditional identity systems that treat users as accounts within isolated applications, Dartwing User treats each human as a **first-class citizen** whose identity, preferences, and digital life transcend organizational boundaries.

**Tagline:** _"Your Identity, Your Control, Everywhere."_

### 1.2 Philosophy: "One Human = One Identity"

Every human in Dartwing has exactly ONE:

- **Keycloak User** (authentication) → Managed by Core
- **Frappe User** (authorization) → Managed by Core
- **Person** (identity record) → Managed by Core
- **User Profile** (preferences) → **Managed by User Module**

These are permanently linked and never duplicated. When you join your Family org, your Company, your HOA, and your Golf Club—you're the same person everywhere.

### 1.3 Value Proposition

**For End Users:**

- One login for everything (family app, work portal, HOA voting, club scheduling)
- Personal preferences follow you everywhere (theme, language, AI voice)
- Complete control over your digital identity and privacy
- AI assistant that understands all your contexts

**For Organizations:**

- Zero-friction onboarding (smart invites with pre-filled data)
- Reduced support burden (users manage their own devices, preferences)
- Built-in compliance (GDPR, CCPA export/delete)
- Cross-org collaboration without security compromises

**For Dartwing Platform:**

- Sticky user base (personal identity creates lock-in)
- Network effects (users invite others across orgs)
- Premium upsell opportunities (AI voice clone, personal vault, advanced privacy)

### 1.4 Scope

**In Scope (User Module):**

- Personal identity management (profile, preferences, devices)
- Cross-organization features (org switcher, unified search, dashboard)
- Privacy controls (block list, travel mode, data export, privacy dashboard)
- AI personalization (voice clone, shortcuts, daily briefing, AI memory)
- Security features (device trust, push-to-approve, session management)
- Emergency features (digital will, emergency contacts, location sharing)
- Personal storage (vault, health data, wearables)
- Identity verification and reputation

**Out of Scope (Handled by Core Module):**

- Authentication (Keycloak SSO, magic-link, social login)
- Person doctype and Global Person ↔ User Link
- Organization and Org Member doctypes
- Billing and subscriptions (separate Billing module)

### 1.5 Key Differentiators

| User Module (Personal) | Core/Org Modules (Organizational) |
| ---------------------- | --------------------------------- |
| AI voice clone         | Company phone scripts             |
| Theme preference       | Company branding                  |
| Global block list      | Org contact blacklist             |
| Digital will           | Org succession planning           |
| Travel mode            | Org leave requests                |
| Device trust           | Org device management             |
| Personal vault         | Org document storage              |
| Identity verification  | Org member verification           |
| Reputation score       | Org rating systems                |

---

## 2. Problem Statement

### 2.1 Current Pain Points

**Fragmented Identity:**
Users today maintain separate accounts for work tools, family apps, community platforms, and social networks. This creates:

- Password fatigue (average user has 100+ online accounts)
- Context-switching overhead (logging in/out constantly)
- Inconsistent experiences (different UIs, preferences reset)
- Data silos (can't search across all your information)

**Privacy Erosion:**
Current platforms either:

- Force users to share personal data with employers (work accounts)
- Provide no visibility into connected devices
- Make data export/deletion difficult or impossible
- Lack emergency succession planning

**Onboarding Friction:**
Joining a new organization requires:

- Creating yet another account
- Re-entering personal information
- Configuring preferences from scratch
- Learning a new interface

**Security Gaps:**

- No way to verify identity portably across organizations
- No duress protection when traveling
- Limited visibility into device access
- No personal encrypted storage

### 2.2 Target Users

- **Primary:** Adults managing multiple life contexts (work, family, community)
- **Secondary:** Organization administrators who onboard/manage members
- **Tertiary:** Privacy-conscious users who demand data control

### 2.3 Market Opportunity

- 2.5B people use multiple productivity/collaboration tools daily
- Enterprise SSO market: $2.3B (2024) → $5.8B (2030)
- Consumer identity market: Largely untapped outside social login
- Privacy-conscious users willing to pay for control
- Personal vault market growing with digital asset awareness

---

## 3. Goals & Success Metrics

### 3.1 Business Goals

| Goal               | Target                    | Timeframe |
| ------------------ | ------------------------- | --------- |
| User Registration  | 10,000 active users       | Q3 2026   |
| Multi-Org Adoption | 60% of users in 2+ orgs   | Q4 2026   |
| Premium Conversion | 15% of users on paid tier | Q4 2026   |
| Profile Completion | 80% complete profiles     | Q3 2026   |

### 3.2 Product Goals

| Goal                  | Metric                             | Target      |
| --------------------- | ---------------------------------- | ----------- |
| Cross-Org Utility     | Org switches per session           | 2.5 average |
| Privacy Confidence    | Users enabling 3+ privacy features | 40%         |
| AI Engagement         | Daily briefing open rate           | 35%         |
| Security Adoption     | Push-to-approve enabled            | 60%         |
| Identity Verification | Users with Standard+ verification  | 30%         |

### 3.3 Key Performance Indicators (KPIs)

**Acquisition:**

- New user registrations per week
- Invite acceptance rate
- Time to profile completion

**Activation:**

- Users completing profile setup
- Users connecting 2+ organizations
- Users enabling push notifications
- Users completing identity verification

**Engagement:**

- Daily active users (DAU)
- Org switches per session
- Cross-org searches per user
- Daily briefing engagement
- Shortcut usage

**Retention:**

- 7-day / 30-day retention rate
- Churn rate by org count
- Feature adoption over time

**Revenue (Future):**

- Premium tier conversion rate
- AI voice clone adoption
- Personal vault storage upgrades

---

## 4. User Personas

### 4.1 Primary Persona: Multi-Context Professional

**Name:** Sarah Chen  
**Age:** 38  
**Role:** Marketing Director + Parent + HOA Board Member

**Background:**
Sarah juggles a demanding career at a tech company, raises two children with her spouse, and serves on her HOA board. She uses 12+ apps daily across these contexts.

**Pain Points:**

- Constantly switching between work Slack, family calendar, HOA portal
- Forgot her HOA password (used only quarterly for votes)
- Work laptop has personal photos mixed with client files
- No single view of "what do I need to do today"

**Goals:**

- Single login across all life contexts
- Clear separation between work and personal
- Quick access to whatever org needs attention
- AI that understands "remind me about the HOA vote" without clarification

**Quote:** _"I don't want to be three different people in three different apps. I'm one person with a complicated life."_

---

### 4.2 Secondary Persona: Organization Administrator

**Name:** Marcus Johnson  
**Age:** 45  
**Role:** HR Director at Manufacturing Company

**Background:**
Marcus manages onboarding for a 500-person manufacturing company. Workers range from factory floor to executive suite, with varying tech literacy.

**Pain Points:**

- New hire onboarding takes 2+ days for system access
- Factory workers forget passwords constantly (no desk = no password manager)
- Offboarding requires touching 8 different systems
- Can't verify if terminated employees still have access

**Goals:**

- One-click onboarding with pre-filled employee data
- Passwordless login for frontline workers
- Instant access revocation across all systems
- Audit trail of who has access to what

**Quote:** _"I need to get people working on day one, not day three. And I need to sleep at night knowing ex-employees can't access our systems."_

---

### 4.3 Privacy-Conscious User

**Name:** Akiko Tanaka  
**Age:** 29  
**Role:** Software Engineer

**Background:**
Akiko is technically sophisticated and deeply concerned about digital privacy. She uses VPNs, encrypted messaging, and minimal social media.

**Pain Points:**

- Doesn't trust "Sign in with Google" (gives Google more data)
- Worried about employer monitoring personal activity
- Wants to know exactly what data apps collect
- No plan for digital assets if something happens to her

**Goals:**

- Login without Big Tech involvement
- Complete separation of work and personal identity
- Full data export in open format
- Digital will for trusted contact access
- Personal encrypted vault for sensitive documents

**Quote:** _"I'll use your platform if I own my data and can delete everything with one click."_

---

### 4.4 Elderly Family Member

**Name:** Robert Williams  
**Age:** 72  
**Role:** Retired, Family Patriarch

**Background:**
Robert was invited to the family's Dartwing group by his daughter. He's comfortable with his iPhone but struggles with passwords and new apps.

**Pain Points:**

- Can't remember passwords (uses same one everywhere)
- Intimidated by "enterprise-looking" software
- Just wants to see family photos and events
- Worried about scams and security

**Goals:**

- Login by tapping email link (no password)
- Large text, simple interface
- Only sees family stuff (not work features)
- Grandkids can help if he's locked out

**Quote:** _"Just make it work like my email. I tap it and I'm in."_

---

### 4.5 Traveling Professional

**Name:** David Park  
**Age:** 34  
**Role:** International Sales Consultant

**Background:**
David travels internationally 60% of the year, crossing borders frequently. He handles sensitive client data and proprietary pricing information.

**Pain Points:**

- Worried about border searches of his devices
- Needs to access work data from untrusted networks
- Can't remember which VPN to use where
- Colleagues need to reach him in emergencies

**Goals:**

- One-tap "travel mode" that hides sensitive data
- Duress PIN that shows decoy data if forced to unlock
- Trusted device that can approve logins remotely
- Emergency contacts who can reach him anywhere

**Quote:** _"When I cross a border, I need to know my client's pricing won't end up in a competitor's hands—even if I'm forced to unlock my phone."_

---

## 5. Feature Requirements

### 5.1 Feature Catalog

| ID   | Feature                       | Priority | Tier | Phase |
| ---- | ----------------------------- | -------- | ---- | ----- |
| U-01 | User Profile & Preferences    | P0       | Free | 1     |
| U-02 | Multi-Organization Management | P0       | Free | 1     |
| U-03 | Device Trust & Management     | P0       | Free | 1     |
| U-04 | Global Block List             | P1       | Free | 2     |
| U-05 | Personal Shortcuts            | P1       | Free | 3     |
| U-06 | Travel Mode                   | P1       | Pro  | 2     |
| U-07 | Push-to-Approve Login         | P1       | Pro  | 2     |
| U-08 | Digital Will & Succession     | P2       | Pro  | 4     |
| U-09 | AI Voice Profile              | P2       | Pro  | 4     |
| U-10 | Daily AI Briefing             | P1       | Pro  | 3     |
| U-11 | Live Location Sharing         | P2       | Pro  | 3     |
| U-12 | Identity Verification         | P1       | Free | 2     |
| U-13 | Personal Vault                | P1       | Pro  | 2     |
| U-14 | Emergency Contacts            | P0       | Free | 1     |
| U-15 | Notification Preferences      | P0       | Free | 1     |
| U-16 | Privacy Dashboard             | P1       | Free | 2     |
| U-17 | Data Export & Portability     | P0       | Free | 2     |
| U-18 | Account Deletion              | P0       | Free | 2     |
| U-19 | Cross-Org Search              | P1       | Pro  | 2     |
| U-20 | Unified Activity Feed         | P1       | Pro  | 2     |
| U-21 | Contact Auto-Match            | P1       | Free | 3     |
| U-22 | Smart Invitations             | P1       | Free | 1     |
| U-23 | Biometric Unlock              | P0       | Free | 1     |
| U-24 | Passkey Support               | P1       | Free | 2     |
| U-25 | Session Management            | P0       | Free | 1     |
| U-26 | Achievements & Gamification   | P2       | Free | 4     |
| U-27 | Reputation Score              | P2       | Pro  | 4     |
| U-28 | Personal AI Memory            | P2       | Pro  | 4     |
| U-29 | Health Data Integration       | P2       | Pro  | 4     |
| U-30 | Wearable Device Sync          | P2       | Pro  | 4     |

### 5.2 Feature Priority Matrix

| Priority | Features                                                                     | Effort | Impact |
| -------- | ---------------------------------------------------------------------------- | ------ | ------ |
| P0       | U-01, U-02, U-03, U-14, U-15, U-17, U-18, U-23, U-25                         | M-L    | High   |
| P1       | U-04, U-05, U-06, U-07, U-10, U-12, U-13, U-16, U-19, U-20, U-21, U-22, U-24 | M-XL   | High   |
| P2       | U-08, U-09, U-11, U-26, U-27, U-28, U-29, U-30                               | L-XL   | Medium |

**Effort Key:** S = Small (1-2 days), M = Medium (3-5 days), L = Large (1-2 weeks), XL = Extra Large (3+ weeks)

---

## 6. Detailed Feature Specifications

### 6.1 U-01: User Profile & Preferences

**Priority:** P0 | **Phase:** 1 | **Effort:** Medium | **Tier:** Free

**Description:**
Central hub for personal settings that apply across all organizations. User-owned data that travels with them.

**Requirements:**

| ID       | Requirement                                  | Priority |
| -------- | -------------------------------------------- | -------- |
| U-01-001 | Display name editable by user                | Must     |
| U-01-002 | Profile photo with crop/filter               | Must     |
| U-01-003 | Bio/About section (500 chars)                | Should   |
| U-01-004 | Theme selection (light/dark/AMOLED/system)   | Must     |
| U-01-005 | Accent color picker                          | Should   |
| U-01-006 | Language preference                          | Must     |
| U-01-007 | Timezone auto-detect with override           | Must     |
| U-01-008 | Date/time format preferences                 | Should   |
| U-01-009 | Accessibility settings (font size, contrast) | Must     |
| U-01-010 | Haptic feedback toggle                       | Should   |
| U-01-011 | Sound effects toggle                         | Should   |
| U-01-012 | Default calendar (Google/Apple/Outlook)      | Should   |
| U-01-013 | Pronouns field (optional)                    | Should   |
| U-01-014 | Birthday (for age verification, optional)    | Should   |
| U-01-015 | Preferences sync across all devices          | Must     |
| U-01-016 | Preferences persist on logout/login          | Must     |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Profile                                             [Save]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────┐                             │
│                    │              │                             │
│                    │    [Photo]   │                             │
│                    │              │                             │
│                    └──────────────┘                             │
│                    [Change Photo]                               │
│                                                                  │
│  Display Name                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Brett Johnson                                               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Bio                                                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Software developer, pilot, and coffee enthusiast.          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  APPEARANCE                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  Theme                              [System ▼]                  │
│  Accent Color                       [🔵 Blue ▼]                 │
│  Font Size                          [Medium ▼]                  │
│                                                                  │
│  LOCALIZATION                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  Language                           [English (US) ▼]            │
│  Timezone                           [America/New_York ▼]        │
│  Date Format                        [MM/DD/YYYY ▼]              │
│  Time Format                        [12-hour ▼]                 │
│                                                                  │
│  ACCESSIBILITY                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  High Contrast Mode                 [━━━━━━●] OFF               │
│  Reduce Motion                      [━━━━━━●] OFF               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.2 U-02: Multi-Organization Management

**Priority:** P0 | **Phase:** 1 | **Effort:** Medium | **Tier:** Free

**Description:**
View, switch between, and manage memberships across all organizations.

**Requirements:**

| ID       | Requirement                            | Priority |
| -------- | -------------------------------------- | -------- |
| U-02-001 | List all organizations user belongs to | Must     |
| U-02-002 | Show role/status in each organization  | Must     |
| U-02-003 | Quick-switch between orgs (<400ms)     | Must     |
| U-02-004 | Pin favorite organizations             | Should   |
| U-02-005 | Show pending invitations               | Must     |
| U-02-006 | Leave organization (with confirmation) | Must     |
| U-02-007 | View what data each org can access     | Must     |
| U-02-008 | Request to join public organizations   | Should   |
| U-02-009 | Organization activity summary          | Should   |
| U-02-010 | Notification badge per organization    | Must     |
| U-02-011 | Recent orgs at top of list             | Should   |
| U-02-012 | Search/filter for users with 10+ orgs  | Could    |

**Org Type Icons:**

- Family: 👨‍👩‍👧‍👦 / house icon
- Company: 🏢 / briefcase icon
- Nonprofit: 💚 / hands icon
- Club: 👥 / groups icon
- Association: 🏛️ / handshake icon

**Switcher UI:**

```
┌─────────────────────────────────────┐
│ Organizations                       │
├─────────────────────────────────────┤
│ ┌───┐                               │
│ │ 🏢│ Acme Corp              ✓ 3🔔 │ ← Current + badges
│ └───┘ Company · Admin   ⭐ Pinned   │
├─────────────────────────────────────┤
│ ┌───┐                               │
│ │👨‍👩‍👧│ Chen Family                  │
│ └───┘ Family · Member               │
├─────────────────────────────────────┤
│ ┌───┐                               │
│ │ 🏠│ Oakwood HOA            1🔔   │
│ └───┘ Club · Board Member           │
├─────────────────────────────────────┤
│ PENDING INVITATIONS                 │
│ ┌───────────────────────────────────┐
│ │ ⛳ Memphis Country Club           │
│ │ Invited by: John Smith · Member   │
│ │ [Accept]  [Decline]               │
│ └───────────────────────────────────┘
├─────────────────────────────────────┤
│ ┌───┐                               │
│ │ 🌐│ Personal View                 │
│ └───┘ All organizations             │
└─────────────────────────────────────┘
```

---

### 6.3 U-03: Device Trust & Management

**Priority:** P0 | **Phase:** 1 | **Effort:** Medium | **Tier:** Free

**Description:**
Manage trusted devices with security scoring and remote revocation.

**Requirements:**

| ID       | Requirement                             | Priority |
| -------- | --------------------------------------- | -------- |
| U-03-001 | List all registered devices             | Must     |
| U-03-002 | Show device type, OS, last active       | Must     |
| U-03-003 | Mark devices as trusted                 | Must     |
| U-03-004 | Revoke device access remotely           | Must     |
| U-03-005 | Require approval for new device login   | Should   |
| U-03-006 | Device trust score (based on behavior)  | Should   |
| U-03-007 | Alert on login from new device          | Must     |
| U-03-008 | Alert on login from new location        | Should   |
| U-03-009 | Show active sessions per device         | Should   |
| U-03-010 | "Sign out all devices" emergency option | Must     |
| U-03-011 | Show last known location (city-level)   | Should   |
| U-03-012 | Show IP address                         | Should   |
| U-03-013 | Device name user-editable               | Should   |

**Device Trust Score Algorithm:**

| Factor               | Weight | Description                      |
| -------------------- | ------ | -------------------------------- |
| Device age           | 20%    | Longer registered = more trusted |
| Login frequency      | 15%    | Regular use = more trusted       |
| Location consistency | 20%    | Same locations = more trusted    |
| Biometric enabled    | 15%    | More secure                      |
| OS up to date        | 10%    | Security updates installed       |
| No failed attempts   | 10%    | No brute force attempts          |
| MFA enabled          | 10%    | Additional verification          |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Devices                                   [Sign Out All]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  THIS DEVICE                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 📱 iPhone 15 Pro                           ✓ Trusted     │  │
│  │    iOS 18.1 • Last active: Now                           │  │
│  │    San Juan, PR • 192.168.1.x                            │  │
│  │    Trust Score: 95/100 ████████████████████░              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  OTHER DEVICES                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 💻 MacBook Pro                             ✓ Trusted     │  │
│  │    macOS 15.0 • Last active: 2 hours ago                 │  │
│  │    Memphis, TN                                           │  │
│  │    Trust Score: 88/100 █████████████████░░░              │  │
│  │                                              [Revoke]    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🌐 Chrome on Windows                      ⚠️ Untrusted   │  │
│  │    Windows 11 • Last active: 3 days ago                  │  │
│  │    New York, NY (unusual location)                       │  │
│  │    Trust Score: 45/100 █████████░░░░░░░░░░░              │  │
│  │                                    [Trust] [Revoke]      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  PENDING APPROVAL                                               │
│  ─────────────────────────────────────────────────────────────  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 📱 Android Phone                          🕐 Pending     │  │
│  │    Login attempt: 5 minutes ago                          │  │
│  │    San Juan, PR                                          │  │
│  │                                   [Approve] [Deny]       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.4 U-04: Global Block List

**Priority:** P1 | **Phase:** 2 | **Effort:** Medium | **Tier:** Free

**Description:**
Block contacts across ALL organizations—harassment protection that follows you.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| U-04-001 | Block by Person record                          | Must     |
| U-04-002 | Block by phone number                           | Must     |
| U-04-003 | Block by email address                          | Must     |
| U-04-004 | Blocked person cannot message user              | Must     |
| U-04-005 | Blocked person cannot see user in directories   | Should   |
| U-04-006 | Blocked person cannot invite user to orgs       | Should   |
| U-04-007 | User doesn't receive notifications from blocked | Must     |
| U-04-008 | Block is silent (blocked person not notified)   | Must     |
| U-04-009 | Unblock with confirmation                       | Must     |
| U-04-010 | Report to platform option                       | Should   |
| U-04-011 | Block reason (optional, private)                | Should   |
| U-04-012 | Block date shown                                | Should   |

**Block Types:**

| Type         | Scope      | Effect                          |
| ------------ | ---------- | ------------------------------- |
| Person Block | Global     | Complete block across all orgs  |
| Phone Block  | Global     | Block unknown callers by number |
| Email Block  | Global     | Block unknown senders by email  |
| Org-Specific | Single org | Hide from one org only          |

---

### 6.5 U-05: Personal Shortcuts

**Priority:** P1 | **Phase:** 3 | **Effort:** Medium | **Tier:** Free

**Description:**
Custom voice/text commands for frequent actions with location and time triggers.

**Requirements:**

| ID       | Requirement                               | Priority |
| -------- | ----------------------------------------- | -------- |
| U-05-001 | Create custom trigger phrases             | Must     |
| U-05-002 | Map to API actions                        | Must     |
| U-05-003 | Map to navigation targets                 | Must     |
| U-05-004 | Map to external URLs                      | Should   |
| U-05-005 | Variable substitution in actions          | Should   |
| U-05-006 | Time-based shortcuts (trigger at time)    | Should   |
| U-05-007 | Location-based shortcuts (trigger at GPS) | Should   |
| U-05-008 | Multi-action shortcuts (chain actions)    | Should   |
| U-05-009 | Import/export shortcuts                   | Should   |
| U-05-010 | Share shortcuts with family               | Could    |
| U-05-011 | Voice activation                          | Should   |
| U-05-012 | Suggested shortcuts based on usage        | Could    |
| U-05-013 | Max 50 shortcuts per user                 | Should   |
| U-05-014 | Case-insensitive matching                 | Must     |

**Example Shortcuts:**

| Trigger            | Action Type     | Target                          |
| ------------------ | --------------- | ------------------------------- |
| "Show my tasks"    | Navigate        | /tasks?assigned_to=me           |
| "Log my mileage"   | API Call        | create_mileage_log              |
| "Call the office"  | External        | tel:+15551234567                |
| "Start focus mode" | Multi-Action    | Enable DND + hide notifications |
| "I'm leaving work" | Location + Time | Trigger at 5pm at office GPS    |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Shortcuts                                       [+ New]      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MY SHORTCUTS                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🎤 "Show my tasks"                                        │  │
│  │    → Navigate to Tasks (filtered to me)                  │  │
│  │                                              [Edit] [🗑️] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🎤 "Log my mileage"                                       │  │
│  │    → Create Mileage Log entry                            │  │
│  │    Variables: {from}, {to}, {miles}                      │  │
│  │                                              [Edit] [🗑️] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 📍 "I'm leaving work" (Location + Time)                   │  │
│  │    Triggers: 5pm + at office GPS                         │  │
│  │    Actions: Set status "Commuting", Notify family        │  │
│  │                                              [Edit] [🗑️] │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  SUGGESTED SHORTCUTS                                            │
│  ─────────────────────────────────────────────────────────────  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 💡 "What's on my calendar today?"                         │  │
│  │    Based on your frequent navigation                     │  │
│  │                                                  [Add]   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.6 U-06: Travel Mode

**Priority:** P1 | **Phase:** 2 | **Effort:** Medium | **Tier:** Pro

**Description:**
Protect sensitive data when crossing borders or in untrusted environments. Includes duress PIN for coerced situations.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| U-06-001 | One-tap travel mode activation           | Must     |
| U-06-002 | Hide financial data                      | Must     |
| U-06-003 | Hide medical records                     | Must     |
| U-06-004 | Hide business documents                  | Should   |
| U-06-005 | Duress PIN shows decoy data              | Should   |
| U-06-006 | Auto-activate based on international GPS | Could    |
| U-06-007 | Travel mode indicator visible to user    | Must     |
| U-06-008 | Scheduled travel mode (flight times)     | Should   |
| U-06-009 | Notify trusted contact when activated    | Should   |
| U-06-010 | Auto-disable after X days (configurable) | Should   |
| U-06-011 | Critical notifications still delivered   | Must     |
| U-06-012 | Auto-reply for messages                  | Should   |

**Data Visibility Matrix:**

| Data Type | Normal Mode | Travel Mode     | Duress PIN    |
| --------- | ----------- | --------------- | ------------- |
| Tasks     | ✓ All       | ✓ Non-sensitive | ✓ All         |
| Financial | ✓ All       | ✗ Hidden        | ✗ Decoy data  |
| Medical   | ✓ All       | ✗ Hidden        | ✗ Hidden      |
| Documents | ✓ All       | ✓ Public only   | ✓ All         |
| Contacts  | ✓ All       | ✓ All           | ✓ All         |
| Messages  | ✓ All       | ✗ Last 24h only | ✓ All         |
| Vault     | ✓ All       | ✗ Hidden        | ✗ Decoy vault |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ✈️ Travel Mode                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [═══════════════════●] ENABLED                                 │
│                                                                  │
│  Travel mode hides sensitive data when you're traveling.        │
│  Enable before crossing borders or in untrusted environments.   │
│                                                                  │
│  HIDDEN DATA                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ Financial information                                        │
│  ☑ Medical records                                              │
│  ☑ Business documents                                           │
│  ☐ Contact details                                              │
│                                                                  │
│  AUTO-REPLY MESSAGE                                             │
│  ─────────────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ I'm currently traveling with limited availability. I'll    ││
│  │ respond when I return.                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  DURESS PROTECTION                                              │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ Enable duress PIN                                            │
│  Duress PIN: [••••••]  [Change]                                │
│  When entered, shows decoy data instead of real data.          │
│                                                                  │
│  SCHEDULE                                                       │
│  ─────────────────────────────────────────────────────────────  │
│  Auto-disable after: [7 days ▼]                                │
│  ☐ Auto-activate when leaving home country                     │
│                                                                  │
│  NOTIFICATIONS                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ Notify trusted contact when enabled                         │
│  Contact: [Jane Doe (Sister) ▼]                                │
│                                                                  │
│  Critical notifications still delivered:                        │
│  ☑ Emergency contacts                                           │
│  ☑ Security alerts                                              │
│  ☐ Org announcements                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.7 U-07: Push-to-Approve Login

**Priority:** P1 | **Phase:** 2 | **Effort:** Large | **Tier:** Pro

**Description:**
Approve logins from new devices via push notification on trusted device.

**Requirements:**

| ID       | Requirement                                | Priority |
| -------- | ------------------------------------------ | -------- |
| U-07-001 | Push notification for new device login     | Must     |
| U-07-002 | Show device info, location, time           | Must     |
| U-07-003 | One-tap approve from notification          | Must     |
| U-07-004 | One-tap deny from notification             | Must     |
| U-07-005 | Timeout after 5 minutes                    | Must     |
| U-07-006 | Fallback to email/SMS if no push           | Should   |
| U-07-007 | "Always approve from this location" option | Should   |
| U-07-008 | Rich notification with map                 | Could    |
| U-07-009 | Deny + report suspicious option            | Should   |
| U-07-010 | Audit log of all approvals/denials         | Must     |

**Push Notification Content:**

```
┌─────────────────────────────────────┐
│ 🔐 New Login Request                │
│                                     │
│ Someone is trying to log in:        │
│                                     │
│ 📱 iPhone 15 Pro                    │
│ 📍 New York, NY                     │
│ 🕐 Just now                         │
│                                     │
│ Was this you?                       │
│                                     │
│ [✓ Approve]      [✗ Deny]          │
└─────────────────────────────────────┘
```

**Flow Diagram:**

```
New Device                    Keycloak              Trusted Device
    │                            │                        │
    │ 1. Login attempt           │                        │
    │───────────────────────────►│                        │
    │                            │                        │
    │ 2. Hold (pending approval) │                        │
    │◄───────────────────────────│                        │
    │                            │                        │
    │                            │ 3. Push notification   │
    │                            │───────────────────────►│
    │                            │                        │
    │                            │        4. User reviews │
    │                            │                        │
    │                            │ 5. Approve / Deny      │
    │                            │◄───────────────────────│
    │                            │                        │
    │ 6a. Login granted          │                        │
    │◄───────────────────────────│ (if approved)         │
    │                            │                        │
    │ 6b. Login denied + alert   │                        │
    │◄───────────────────────────│ (if denied)           │
```

---

### 6.8 U-08: Digital Will & Succession

**Priority:** P2 | **Phase:** 4 | **Effort:** Large | **Tier:** Pro

**Description:**
Designate trusted contacts who gain access if user becomes incapacitated.

**Requirements:**

| ID       | Requirement                                    | Priority |
| -------- | ---------------------------------------------- | -------- |
| U-08-001 | Designate 1-3 trusted contacts                 | Must     |
| U-08-002 | Set inactivity period (30-365 days)            | Must     |
| U-08-003 | Trusted contact can request access             | Must     |
| U-08-004 | User notified of access request                | Must     |
| U-08-005 | Waiting period before access granted (7 days)  | Must     |
| U-08-006 | User can cancel during waiting period          | Must     |
| U-08-007 | Define what data successor can access          | Should   |
| U-08-008 | Successor can download data                    | Should   |
| U-08-009 | Successor cannot delete or modify              | Must     |
| U-08-010 | Legal documentation template                   | Could    |
| U-08-011 | Warning at 50% and 75% of inactivity threshold | Must     |
| U-08-012 | Require trusted contact to verify identity     | Should   |

**Digital Will States:**

```
┌────────────────────────────────────────────────────────────────┐
│                     DIGITAL WILL LIFECYCLE                      │
│                                                                 │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐     ┌─────────┐│
│  │ Active  │─────►│Inactive │─────►│Requested│────►│ Granted ││
│  │         │      │(counting)│     │(waiting)│     │         ││
│  └─────────┘      └────┬────┘      └────┬────┘     └─────────┘│
│       ▲                │                │                      │
│       │                │                │                      │
│       └────────────────┴────────────────┘                      │
│           User activity cancels process                        │
│                                                                 │
│  Timeline Example (90-day threshold):                          │
│  Day 0:  User last active                                      │
│  Day 45: Warning notification (50%)                            │
│  Day 68: Warning notification (75%)                            │
│  Day 90: Inactivity threshold reached                          │
│  Day 90: Trusted contact notified, can request access          │
│  Day 91: Trusted contact requests access                       │
│  Day 91: User notified via all channels                        │
│  Day 98: 7-day waiting period expires                          │
│  Day 98: Access granted to trusted contact                     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 6.9 U-09: AI Voice Profile

**Priority:** P2 | **Phase:** 4 | **Effort:** Extra Large | **Tier:** Pro

**Description:**
Clone user's voice for AI to use in calls and voice messages. All AI-generated audio is watermarked.

**Requirements:**

| ID       | Requirement                          | Priority |
| -------- | ------------------------------------ | -------- |
| U-09-001 | Record 30-second voice sample        | Must     |
| U-09-002 | Generate voice model from sample     | Must     |
| U-09-003 | AI can use voice for outbound calls  | Should   |
| U-09-004 | AI can generate voice messages       | Should   |
| U-09-005 | User approves each use of voice      | Must     |
| U-09-006 | Watermark ALL AI-generated audio     | Must     |
| U-09-007 | Define personality traits for AI     | Should   |
| U-09-008 | Custom personality prompt            | Should   |
| U-09-009 | Delete voice model on request        | Must     |
| U-09-010 | Voice model never shared with orgs   | Must     |
| U-09-011 | Explicit consent with legal terms    | Must     |
| U-09-012 | Preview cloned voice before enabling | Must     |
| U-09-013 | Re-train voice clone                 | Should   |

**Voice Training Flow:**

```
1. User opens "AI Voice Clone" settings
2. Intro screen explains feature + privacy
3. User records prompted text (30 seconds total):
   - "Hello, this is [Name]"
   - "I'm calling about your appointment"
   - "Please call me back at your convenience"
   - [Additional varied phrases]
4. Upload progress indicator
5. "Training in progress" status (up to 24 hours)
6. Push notification when complete
7. User previews with custom text
8. User enables or re-records
```

**Privacy Considerations:**

- Voice data encrypted at rest (AES-256)
- Voice data never shared with organizations
- User can delete all voice data instantly
- Voice clone only used for user-initiated actions
- All generated audio contains inaudible watermark

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  AI Voice Profile                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Your AI assistant can speak in your voice for:                 │
│  • Automated call responses                                     │
│  • Voice messages when you're unavailable                       │
│  • Reading documents aloud                                      │
│                                                                  │
│  All AI-generated audio is watermarked and you approve          │
│  each use.                                                      │
│                                                                  │
│  VOICE SAMPLE                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  Status: ✓ Recorded (32 seconds)                               │
│                                                                  │
│  [▶️ Play Sample]  [🔄 Re-record]  [🗑️ Delete]                   │
│                                                                  │
│  PERSONALITY                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  Describe your communication style:                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Professional but friendly. I prefer to get to the point   ││
│  │ quickly. I use humor occasionally but stay focused on     ││
│  │ business during work hours.                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  AI USAGE PERMISSIONS                                           │
│  ─────────────────────────────────────────────────────────────  │
│  ☑ Voicemail greetings                                         │
│  ☐ Outbound calls (requires approval each time)                │
│  ☑ Reading documents aloud                                      │
│  ☐ Voice messages to contacts                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.10 U-10: Daily AI Briefing

**Priority:** P1 | **Phase:** 3 | **Effort:** Large | **Tier:** Pro

**Description:**
Personalized morning briefing aggregating information across all organizations. Available as text and audio.

**Requirements:**

| ID       | Requirement                           | Priority |
| -------- | ------------------------------------- | -------- |
| U-10-001 | Aggregate tasks from all orgs         | Must     |
| U-10-002 | Show today's calendar events          | Must     |
| U-10-003 | Highlight overdue items               | Must     |
| U-10-004 | Show unread messages summary          | Should   |
| U-10-005 | Weather for user's locations          | Should   |
| U-10-006 | Commute time estimate                 | Could    |
| U-10-007 | Custom sections (stocks, news)        | Could    |
| U-10-008 | Delivery time preference              | Must     |
| U-10-009 | Text AND audio versions               | Should   |
| U-10-010 | "Snooze" for 1 hour option            | Should   |
| U-10-011 | Configure which orgs to include       | Should   |
| U-10-012 | Configure which item types to include | Should   |
| U-10-013 | Disable briefing entirely             | Must     |
| U-10-014 | AI-generated natural language summary | Must     |

**Briefing Content:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Good morning, Brett! ☀️                    Tuesday, Nov 29     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🌡️ WEATHER                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  San Juan: 82°F, Partly cloudy                                  │
│  Memphis: 45°F, Rain expected                                   │
│                                                                  │
│  📅 TODAY'S SCHEDULE (4 events)                                 │
│  ─────────────────────────────────────────────────────────────  │
│  9:00 AM   Team standup (Opensoft)                              │
│  11:00 AM  Dentist appointment (Personal)                       │
│  2:00 PM   Board meeting (Lakewood HOA)                         │
│  5:00 PM   Soccer practice - pick up kids (Family)              │
│                                                                  │
│  ✅ TASKS DUE TODAY (3 items)                                   │
│  ─────────────────────────────────────────────────────────────  │
│  • Review Q4 budget proposal (Opensoft) - High priority         │
│  • Submit expense report (Personal)                             │
│  • Vote on landscaping proposal (HOA) - Deadline 6pm            │
│                                                                  │
│  ⚠️ ATTENTION NEEDED (2 items)                                  │
│  ─────────────────────────────────────────────────────────────  │
│  • 3 unread messages from HOA Board                             │
│  • Invoice #1234 pending your approval                          │
│                                                                  │
│  [🔊 Listen to Briefing]                    [Snooze 1 hour]    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.11 U-11: Live Location Sharing

**Priority:** P2 | **Phase:** 3 | **Effort:** Large | **Tier:** Pro

**Description:**
Share real-time location with trusted contacts for safety or coordination.

**Requirements:**

| ID       | Requirement                                           | Priority |
| -------- | ----------------------------------------------------- | -------- |
| U-11-001 | Share location with specific person                   | Must     |
| U-11-002 | Share location with organization                      | Should   |
| U-11-003 | Set expiration (1hr, 4hr, 8hr, 24hr, until cancelled) | Must     |
| U-11-004 | View who can see your location                        | Must     |
| U-11-005 | Stop sharing instantly                                | Must     |
| U-11-006 | Battery-efficient location updates                    | Must     |
| U-11-007 | Works in background                                   | Must     |
| U-11-008 | Location history (last 24hr)                          | Should   |
| U-11-009 | Geofence alerts (arrived/left)                        | Should   |
| U-11-010 | Emergency broadcast location                          | Should   |
| U-11-011 | Real-time updates every 30 seconds                    | Must     |

---

### 6.12 U-12: Identity Verification

**Priority:** P1 | **Phase:** 2 | **Effort:** Large | **Tier:** Free

**Description:**
Verify user identity for high-trust scenarios. Verification is portable across all organizations.

**Requirements:**

| ID       | Requirement                                     | Priority |
| -------- | ----------------------------------------------- | -------- |
| U-12-001 | Government ID scan (driver's license, passport) | Must     |
| U-12-002 | Selfie liveness check                           | Must     |
| U-12-003 | Address verification                            | Should   |
| U-12-004 | Phone number verification                       | Must     |
| U-12-005 | Email verification                              | Must     |
| U-12-006 | Verification badge on profile                   | Should   |
| U-12-007 | Verification level (basic, standard, enhanced)  | Should   |
| U-12-008 | Re-verification reminder (annual)               | Should   |
| U-12-009 | Verification portable across orgs               | Must     |
| U-12-010 | Integration with IDV providers (Persona, Jumio) | Must     |

**Verification Levels:**

| Level        | Requirements                  | Use Cases                                |
| ------------ | ----------------------------- | ---------------------------------------- |
| **Basic**    | Email + Phone verified        | General membership                       |
| **Standard** | Basic + Government ID scan    | Financial transactions, voting           |
| **Enhanced** | Standard + Address + Liveness | Board positions, high-value transactions |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Identity Verification                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VERIFICATION STATUS                                            │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Current Level: Standard ✓                                      │
│  Verified: November 15, 2024                                    │
│  Next verification due: November 15, 2025                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ✓ Email verified         brett@example.com               │  │
│  │ ✓ Phone verified         +1 (555) 123-4567              │  │
│  │ ✓ Government ID          Driver's License (TN)          │  │
│  │ ○ Address verification   Not completed                   │  │
│  │ ○ Liveness check         Not completed                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Upgrade to Enhanced →]                                        │
│                                                                  │
│  VERIFICATION BENEFITS                                          │
│  ─────────────────────────────────────────────────────────────  │
│  ✓ Trusted badge on your profile                               │
│  ✓ Join organizations faster (skip manual review)              │
│  ✓ Access financial features                                   │
│  ✓ Eligible for board positions                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.13 U-13: Personal Vault

**Priority:** P1 | **Phase:** 2 | **Effort:** Large | **Tier:** Pro

**Description:**
End-to-end encrypted storage for sensitive personal documents accessible only to user.

**Requirements:**

| ID       | Requirement                      | Priority |
| -------- | -------------------------------- | -------- |
| U-13-001 | End-to-end encrypted storage     | Must     |
| U-13-002 | Upload any file type             | Must     |
| U-13-003 | 1GB free storage, expandable     | Must     |
| U-13-004 | Organize with folders/tags       | Should   |
| U-13-005 | Search within documents          | Should   |
| U-13-006 | Share specific files temporarily | Should   |
| U-13-007 | Expiring share links             | Should   |
| U-13-008 | Access from any device           | Must     |
| U-13-009 | Offline access to pinned files   | Should   |
| U-13-010 | Include in Digital Will          | Should   |
| U-13-011 | Virus scanning on upload         | Must     |
| U-13-012 | Version history                  | Should   |

**Suggested Vault Categories:**

| Category      | Example Documents                                   |
| ------------- | --------------------------------------------------- |
| **Identity**  | Passport, Driver's license, Birth certificate       |
| **Financial** | Tax returns, Bank statements, Investment records    |
| **Medical**   | Vaccination records, Prescriptions, Insurance cards |
| **Legal**     | Will, Power of attorney, Contracts                  |
| **Property**  | Deeds, Vehicle titles, Insurance policies           |
| **Education** | Diplomas, Transcripts, Certifications               |

---

### 6.14 U-14: Emergency Contacts

**Priority:** P0 | **Phase:** 1 | **Effort:** Small | **Tier:** Free

**Description:**
Designate contacts for emergencies, accessible across all organizations.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| U-14-001 | Add up to 5 emergency contacts           | Must     |
| U-14-002 | Priority order                           | Must     |
| U-14-003 | Relationship type                        | Must     |
| U-14-004 | Multiple contact methods per person      | Should   |
| U-14-005 | Organizations can view (with permission) | Should   |
| U-14-006 | One-tap emergency call                   | Must     |
| U-14-007 | Emergency broadcast to all contacts      | Should   |
| U-14-008 | Medical info (allergies, conditions)     | Should   |
| U-14-009 | ICE lock screen widget                   | Could    |
| U-14-010 | Auto-notify on SOS activation            | Should   |

---

### 6.15 U-15: Notification Preferences

**Priority:** P0 | **Phase:** 1 | **Effort:** Medium | **Tier:** Free

**Description:**
Granular control over how and when notifications are delivered.

**Requirements:**

| ID       | Requirement                               | Priority |
| -------- | ----------------------------------------- | -------- |
| U-15-001 | Per-organization notification settings    | Must     |
| U-15-002 | Per-channel settings (push, email, SMS)   | Must     |
| U-15-003 | Quiet hours schedule                      | Must     |
| U-15-004 | Priority override during quiet hours      | Should   |
| U-15-005 | Notification grouping preferences         | Should   |
| U-15-006 | Digest frequency (instant, hourly, daily) | Should   |
| U-15-007 | Mute specific conversations               | Should   |
| U-15-008 | Vacation mode (auto-reply)                | Should   |
| U-15-009 | Focus modes (Work, Personal, Sleep)       | Should   |
| U-15-010 | Smart delivery timing                     | Could    |

---

### 6.16 U-16: Privacy Dashboard

**Priority:** P1 | **Phase:** 2 | **Effort:** Medium | **Tier:** Free

**Description:**
Central view of all data shared and privacy settings with privacy health score.

**Requirements:**

| ID       | Requirement                        | Priority |
| -------- | ---------------------------------- | -------- |
| U-16-001 | Show all organizations with access | Must     |
| U-16-002 | Show what data each org can see    | Must     |
| U-16-003 | Revoke org access to specific data | Should   |
| U-16-004 | Activity log of data access        | Should   |
| U-16-005 | Third-party app connections        | Should   |
| U-16-006 | Data download request              | Must     |
| U-16-007 | Account deletion request           | Must     |
| U-16-008 | Privacy score/health check         | Should   |
| U-16-009 | Recommendations to improve privacy | Should   |
| U-16-010 | GDPR/CCPA rights explanation       | Should   |

**UI Wireframe:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Privacy Dashboard                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRIVACY SCORE                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ████████████████████████░░░░░░ 78/100 Good                    │
│                                                                  │
│  💡 Enable 2FA for +10 points                                   │
│  💡 Review third-party apps for +5 points                       │
│                                                                  │
│  DATA SHARING BY ORGANIZATION                                   │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🏢 Opensoft Inc                                           │  │
│  │    Can access: Name, Email, Phone, Profile Photo         │  │
│  │    Cannot access: Financial, Medical, Location           │  │
│  │                                              [Manage →]  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 🏠 Lakewood HOA                                           │  │
│  │    Can access: Name, Email, Address, Vehicles            │  │
│  │    Cannot access: Financial (except dues), Medical       │  │
│  │                                              [Manage →]  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  CONNECTED APPS                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  Google Calendar    Connected Nov 1, 2024      [Disconnect]    │
│  Slack              Connected Oct 15, 2024     [Disconnect]    │
│                                                                  │
│  YOUR DATA RIGHTS                                               │
│  ─────────────────────────────────────────────────────────────  │
│  [📥 Download All My Data]  [🗑️ Delete My Account]              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.17 U-17: Data Export & Portability

**Priority:** P0 | **Phase:** 2 | **Effort:** Medium | **Tier:** Free

**Description:**
Export all personal data in portable format (GDPR/CCPA compliance).

**Requirements:**

| ID       | Requirement                                    | Priority |
| -------- | ---------------------------------------------- | -------- |
| U-17-001 | Export all personal data                       | Must     |
| U-17-002 | Export includes: profile, preferences, devices | Must     |
| U-17-003 | Export includes: org memberships               | Must     |
| U-17-004 | Export includes: communications                | Should   |
| U-17-005 | Export includes: files/documents owned         | Should   |
| U-17-006 | Export format: JSON + ZIP of files             | Must     |
| U-17-007 | Export available for download 24 hours         | Must     |
| U-17-008 | Email notification when export ready           | Must     |
| U-17-009 | Processing time < 24 hours                     | Must     |

---

### 6.18 U-18: Account Deletion

**Priority:** P0 | **Phase:** 2 | **Effort:** Medium | **Tier:** Free

**Description:**
Permanently delete account and all associated data (right to erasure).

**Requirements:**

| ID       | Requirement                                | Priority |
| -------- | ------------------------------------------ | -------- |
| U-18-001 | Delete account permanently                 | Must     |
| U-18-002 | Delete requires email confirmation code    | Must     |
| U-18-003 | Delete removes: User, Person, User Profile | Must     |
| U-18-004 | Delete removes: all org memberships        | Must     |
| U-18-005 | Delete revokes Keycloak session            | Must     |
| U-18-006 | 7-day grace period before deletion         | Should   |
| U-18-007 | Cannot delete if sole org admin            | Must     |
| U-18-008 | User types "DELETE" to confirm intent      | Must     |
| U-18-009 | Confirmation email sent after deletion     | Must     |

**Delete Flow:**

```
1. User opens Privacy settings → "Delete Account"
2. Warning screen explains consequences
3. User types "DELETE" to confirm intent
4. Email sent with confirmation code
5. User enters code
6. Account enters "Pending Deletion" state
7. User has 7 days to cancel
8. After 7 days, permanent deletion executes
9. Confirmation email sent
```

---

### 6.19 U-19: Cross-Org Search

**Priority:** P1 | **Phase:** 2 | **Effort:** Large | **Tier:** Pro

**Description:**
Search across all organizations simultaneously with unified results.

**Requirements:**

| ID       | Requirement                                        | Priority |
| -------- | -------------------------------------------------- | -------- |
| U-19-001 | Global search bar in app header                    | Must     |
| U-19-002 | Searches all user's organizations                  | Must     |
| U-19-003 | Results grouped by organization                    | Should   |
| U-19-004 | Results grouped by type (contacts, docs, messages) | Should   |
| U-19-005 | Filter by organization                             | Must     |
| U-19-006 | Filter by content type                             | Must     |
| U-19-007 | Filter by date range                               | Should   |
| U-19-008 | Full-text search in documents                      | Must     |
| U-19-009 | Search in: contacts, files, messages, events       | Must     |
| U-19-010 | Respect per-org permissions                        | Must     |
| U-19-011 | Recent searches saved                              | Should   |
| U-19-012 | Search suggestions/autocomplete                    | Should   |
| U-19-013 | Voice search                                       | Could    |

---

### 6.20 U-20: Unified Activity Feed

**Priority:** P1 | **Phase:** 2 | **Effort:** Medium | **Tier:** Pro

**Description:**
Combined activity feed from all organizations.

**Requirements:**

| ID       | Requirement                          | Priority |
| -------- | ------------------------------------ | -------- |
| U-20-001 | Combined feed from all organizations | Must     |
| U-20-002 | Filter by org or activity type       | Must     |
| U-20-003 | Real-time updates                    | Must     |
| U-20-004 | Mark as read/unread                  | Must     |
| U-20-005 | Tap to navigate to source            | Must     |
| U-20-006 | Color-coded by organization          | Should   |
| U-20-007 | Group similar activities             | Should   |

---

### 6.21 U-21: Contact Auto-Match

**Priority:** P1 | **Phase:** 3 | **Effort:** Medium | **Tier:** Free

**Description:**
Match phone contacts to existing Dartwing users.

**Requirements:**

| ID       | Requirement                                            | Priority |
| -------- | ------------------------------------------------------ | -------- |
| U-21-001 | Opt-in prompt during onboarding                        | Must     |
| U-21-002 | Explain privacy implications clearly                   | Must     |
| U-21-003 | Match by phone number (primary)                        | Must     |
| U-21-004 | Match by email (secondary)                             | Must     |
| U-21-005 | Show matches for user approval                         | Must     |
| U-21-006 | User can skip individual matches                       | Must     |
| U-21-007 | User can skip entire feature                           | Must     |
| U-21-008 | Contacts never uploaded to server (on-device matching) | Must     |
| U-21-009 | Re-run matching from settings                          | Should   |
| U-21-010 | Suggest inviting unmatched contacts                    | Could    |

---

### 6.22 U-22: Smart Invitations

**Priority:** P1 | **Phase:** 1 | **Effort:** Large | **Tier:** Free

**Description:**
Invite contacts to organizations with pre-filled information.

**Requirements:**

| ID       | Requirement                                            | Priority |
| -------- | ------------------------------------------------------ | -------- |
| U-22-001 | Inviter can enter: first name, last name, email, phone | Must     |
| U-22-002 | Only email is required                                 | Must     |
| U-22-003 | Inviter can select role template for invitee           | Must     |
| U-22-004 | Inviter can add personal message                       | Should   |
| U-22-005 | Invite sent via email with magic link                  | Must     |
| U-22-006 | Invite expires after 7 days                            | Must     |
| U-22-007 | Inviter can revoke pending invite                      | Must     |
| U-22-008 | Inviter can resend invite                              | Must     |
| U-22-009 | Invitee tapping link creates account + joins org       | Must     |
| U-22-010 | If invitee already has account, just joins org         | Must     |
| U-22-011 | Pre-filled info populates Person record                | Must     |
| U-22-012 | Invitee can edit pre-filled info before confirming     | Should   |
| U-22-013 | Bulk invite via CSV upload                             | Should   |
| U-22-014 | QR code invite for in-person onboarding                | Could    |
| U-22-015 | Invite tracking dashboard for admins                   | Should   |

---

### 6.23 U-23: Biometric Unlock

**Priority:** P0 | **Phase:** 1 | **Effort:** Small | **Tier:** Free

**Description:**
Use device biometrics for app unlock.

**Requirements:**

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------- |
| U-23-001 | Face ID support (iOS)                            | Must     |
| U-23-002 | Touch ID support (iOS)                           | Must     |
| U-23-003 | Fingerprint support (Android)                    | Must     |
| U-23-004 | Face unlock support (Android)                    | Should   |
| U-23-005 | Configurable timeout (1min, 5min, 15min, always) | Must     |
| U-23-006 | Fallback to PIN                                  | Must     |
| U-23-007 | Require biometric for sensitive actions          | Should   |

---

### 6.24 U-24: Passkey Support

**Priority:** P1 | **Phase:** 2 | **Effort:** Large | **Tier:** Free

**Description:**
FIDO2/WebAuthn passwordless authentication.

**Requirements:**

| ID       | Requirement                       | Priority |
| -------- | --------------------------------- | -------- |
| U-24-001 | FIDO2/WebAuthn support            | Must     |
| U-24-002 | Cross-device passkeys             | Should   |
| U-24-003 | Phishing-resistant authentication | Must     |
| U-24-004 | Works on web and mobile           | Must     |
| U-24-005 | Register multiple passkeys        | Should   |
| U-24-006 | Revoke individual passkeys        | Must     |

---

### 6.25 U-25: Session Management

**Priority:** P0 | **Phase:** 1 | **Effort:** Medium | **Tier:** Free

**Description:**
View and manage active sessions.

**Requirements:**

| ID       | Requirement                    | Priority |
| -------- | ------------------------------ | -------- |
| U-25-001 | View all active sessions       | Must     |
| U-25-002 | Session duration limits        | Should   |
| U-25-003 | Force logout specific sessions | Must     |
| U-25-004 | Session activity log           | Should   |
| U-25-005 | Session location (city-level)  | Should   |

---

### 6.26 U-26: Achievements & Gamification

**Priority:** P2 | **Phase:** 4 | **Effort:** Medium | **Tier:** Free

**Description:**
Profile badges and engagement milestones.

**Requirements:**

| ID       | Requirement                        | Priority |
| -------- | ---------------------------------- | -------- |
| U-26-001 | Profile completion badges          | Should   |
| U-26-002 | Engagement milestones              | Should   |
| U-26-003 | Organization-specific achievements | Could    |
| U-26-004 | Leaderboards (opt-in)              | Could    |
| U-26-005 | Badge showcase on profile          | Should   |

---

### 6.27 U-27: Reputation Score

**Priority:** P2 | **Phase:** 4 | **Effort:** Large | **Tier:** Pro

**Description:**
Portable trust metric across organizations.

**Requirements:**

| ID       | Requirement                                  | Priority |
| -------- | -------------------------------------------- | -------- |
| U-27-001 | Based on verified identity                   | Must     |
| U-27-002 | Community feedback component                 | Should   |
| U-27-003 | Payment history component                    | Should   |
| U-27-004 | Portable across organizations                | Must     |
| U-27-005 | Visible to organizations (with user consent) | Must     |
| U-27-006 | Appeal/dispute process                       | Should   |

---

### 6.28 U-28: Personal AI Memory

**Priority:** P2 | **Phase:** 4 | **Effort:** Large | **Tier:** Pro

**Description:**
AI remembers user preferences across sessions.

**Requirements:**

| ID       | Requirement                              | Priority |
| -------- | ---------------------------------------- | -------- |
| U-28-001 | AI remembers preferences across sessions | Must     |
| U-28-002 | Learns communication style               | Should   |
| U-28-003 | Stores context for better assistance     | Must     |
| U-28-004 | User can view all memories               | Must     |
| U-28-005 | User can delete individual memories      | Must     |
| U-28-006 | User can delete all memories             | Must     |
| U-28-007 | Memories never shared with orgs          | Must     |

---

### 6.29 U-29: Health Data Integration

**Priority:** P2 | **Phase:** 4 | **Effort:** Large | **Tier:** Pro

**Description:**
Sync health data from wearables and health apps.

**Requirements:**

| ID       | Requirement                               | Priority |
| -------- | ----------------------------------------- | -------- |
| U-29-001 | Apple Health sync                         | Should   |
| U-29-002 | Google Fit sync                           | Should   |
| U-29-003 | Emergency medical info                    | Should   |
| U-29-004 | Medication reminders                      | Could    |
| U-29-005 | Share with healthcare orgs (with consent) | Should   |
| U-29-006 | Data encrypted at rest                    | Must     |

---

### 6.30 U-30: Wearable Device Sync

**Priority:** P2 | **Phase:** 4 | **Effort:** Extra Large | **Tier:** Pro

**Description:**
Companion apps for smartwatches.

**Requirements:**

| ID       | Requirement              | Priority |
| -------- | ------------------------ | -------- |
| U-30-001 | Apple Watch app          | Should   |
| U-30-002 | Wear OS app              | Should   |
| U-30-003 | Quick actions from wrist | Should   |
| U-30-004 | Notification mirroring   | Must     |
| U-30-005 | Briefing on watch face   | Could    |
| U-30-006 | Complication support     | Could    |

---

## 7. User Stories & Acceptance Criteria

### 7.1 Profile & Preferences Stories

**US-001: Edit Profile**

```gherkin
As a user
I want to edit my profile information
So that my identity is accurate across all organizations

Acceptance Criteria:
- Given I am logged in
- When I navigate to Profile settings
- Then I can edit my display name, bio, and photo
- And changes sync to all my organizations within 5 seconds
- And my theme preference applies immediately
```

**US-002: Switch Organizations**

```gherkin
As a user with multiple organizations
I want to quickly switch between them
So that I can manage different areas of my life

Acceptance Criteria:
- Given I am logged in and viewing Work dashboard
- When I tap the org switcher in the header
- Then I see a list of all my organizations
- And each shows name, type, and my role
- When I tap "Family"
- Then I see the Family dashboard
- And the switch completes in under 400ms
```

### 7.2 Security Stories

**US-003: Device Management**

```gherkin
As a security-conscious user
I want to manage my trusted devices
So that I can revoke access if a device is lost

Acceptance Criteria:
- Given I navigate to Devices settings
- Then I see all devices with active sessions
- And each shows device type, last active, and location
- When I tap "Revoke" on a device
- Then that device is immediately logged out
- And I see a confirmation message
```

**US-004: Push-to-Approve Login**

```gherkin
As a security-conscious user
I want to approve new device logins from my phone
So that I know when someone accesses my account

Acceptance Criteria:
- Given I have "Push to Approve" enabled
- And I have at least one trusted device
- When someone logs in from a new device
- Then I receive a push notification on my trusted device
- And the notification shows device type and location
- When I tap "Approve"
- Then the new device is logged in
- When I tap "Deny"
- Then the new device login fails
- And I receive a security alert
```

**US-005: Enable Travel Mode**

```gherkin
As a traveling professional
I want to hide sensitive data when crossing borders
So that my confidential information is protected

Acceptance Criteria:
- Given I am in Settings
- When I enable Travel Mode
- Then financial data is hidden from all views
- And medical records are hidden
- And a travel mode indicator appears in the UI
- When I enter my duress PIN instead of regular PIN
- Then decoy data is shown instead of real data
```

### 7.3 Privacy Stories

**US-006: Block Contact Globally**

```gherkin
As a user
I want to block someone across all my organizations
So that they cannot contact me anywhere

Acceptance Criteria:
- Given I view a contact's profile
- When I tap "Block"
- Then I see a confirmation dialog
- When I confirm
- Then the contact is blocked in all organizations
- And they cannot call or message me via Dartwing
- And they cannot see my shared location
- And they are not notified of the block
```

**US-007: Export My Data**

```gherkin
As a privacy-conscious user
I want to export all my data
So that I have a portable copy

Acceptance Criteria:
- Given I navigate to Privacy Dashboard
- When I tap "Download All My Data"
- Then I see a confirmation that export is processing
- And I receive an email within 24 hours when ready
- When I download the export
- Then it contains a JSON file with my profile and settings
- And it contains any documents I own
- And the download link expires after 24 hours
```

**US-008: Delete My Account**

```gherkin
As a user
I want to permanently delete my account
So that my data is erased

Acceptance Criteria:
- Given I navigate to Privacy Dashboard
- When I tap "Delete My Account"
- Then I see a warning explaining consequences
- When I type "DELETE" and request confirmation
- Then I receive an email with a confirmation code
- When I enter the code
- Then my account enters "pending deletion" state
- And I have 7 days to cancel
- After 7 days, my User, Person, and all org memberships are deleted
- And I cannot log in
```

**US-009: View Privacy Dashboard**

```gherkin
As a privacy-conscious user
I want to see what data organizations can access
So that I can control my privacy

Acceptance Criteria:
- Given I navigate to Privacy Dashboard
- Then I see my privacy score
- And I see all organizations I belong to
- And for each org, I see what data they can access
- And I see recommendations to improve my privacy score
```

### 7.4 AI & Personalization Stories

**US-010: Daily Briefing**

```gherkin
As a busy professional
I want a morning summary of everything I need to know
So that I can plan my day

Acceptance Criteria:
- Given I have daily briefing enabled at 7:00 AM
- When it becomes 7:00 AM in my timezone
- Then I receive a push notification
- And the notification summarizes:
  - Pending approvals
  - Today's events from all orgs
  - Urgent items
- When I tap the notification
- Then I see my full briefing with details
- And I can tap "Listen" to hear audio version
```

**US-011: Personal Shortcut**

```gherkin
As a user
I want to create a shortcut for "Call Mom"
So that I can quickly call her from any context

Acceptance Criteria:
- Given I create a shortcut with trigger "Call Mom"
- And I set the action to call my mother's Person record
- When I say "Call Mom" to the AI
- Then my mother is called
- When I'm in any organization
- Then the shortcut still works
```

**US-012: Location-Based Shortcut**

```gherkin
As a user
I want a shortcut that triggers when I leave work
So that my family knows I'm on my way

Acceptance Criteria:
- Given I create a shortcut with trigger "I'm leaving work"
- And I set location trigger to my office address
- And I set time trigger to after 5pm
- When I leave my office after 5pm
- Then the shortcut triggers automatically
- And my family receives a notification
```

**US-013: Train Voice Clone**

```gherkin
As a user
I want to train an AI voice clone
So that my AI assistant sounds like me

Acceptance Criteria:
- Given I navigate to AI Voice settings
- When I tap "Create Voice Clone"
- Then I see a privacy explanation
- When I record 30 seconds of sample phrases
- Then I see "Training in progress"
- When training completes (within 24 hours)
- Then I receive a notification
- And I can preview my cloned voice
- And all AI-generated audio is watermarked
```

### 7.5 Emergency Stories

**US-014: Digital Will Activation**

```gherkin
As a user with a digital will
I want my trusted contact to gain access if I'm incapacitated
So that someone can manage my affairs

Acceptance Criteria:
- Given I have digital will enabled with 90-day threshold
- And Jane is my trusted contact
- When I haven't logged in for 45 days
- Then I receive a warning notification
- When I haven't logged in for 68 days
- Then I receive another warning
- When I haven't logged in for 90 days
- Then Jane receives a notification
- And Jane can request access
- When Jane requests access
- Then I'm notified via all channels
- And there's a 7-day waiting period
- After 7 days, Jane gains read-only access
- When I log in after activation
- Then Jane's access is revoked
```

**US-015: Emergency Contacts**

```gherkin
As a user
I want to set up emergency contacts
So that they can be reached in an emergency

Acceptance Criteria:
- Given I navigate to Emergency Contacts
- When I add a contact with phone and relationship
- Then they appear in my emergency contacts list
- And they are prioritized by order
- When I tap the emergency call button
- Then my first emergency contact is called
- And organizations with permission can see my emergency contacts
```

### 7.6 Identity Verification Stories

**US-016: Complete Identity Verification**

```gherkin
As a user
I want to verify my identity
So that I can access trusted features

Acceptance Criteria:
- Given I navigate to Identity Verification
- When I complete email verification
- And I complete phone verification
- Then my verification level is "Basic"
- When I scan my government ID
- And the ID matches my profile
- Then my verification level is "Standard"
- And a verification badge appears on my profile
- And my verification is valid across all organizations
```

### 7.7 Personal Vault Stories

**US-017: Upload to Personal Vault**

```gherkin
As a user
I want to store sensitive documents securely
So that only I can access them

Acceptance Criteria:
- Given I navigate to Personal Vault
- When I upload a document
- Then it is encrypted end-to-end
- And it appears in my vault with a category
- And I can access it from any device
- When I enable offline access
- Then the document is cached locally
- And organizations cannot see my vault contents
```

---

## 8. User Flows

### 8.1 Profile Setup Flow

```
┌─────────────────┐
│   First Login   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Complete Profile│
│                 │
│ First Name [__] │
│ Last Name [___] │
│ Phone [_______] │
│                 │
│ [Continue]      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preferences     │
│                 │
│ Theme [Dark ▼]  │
│ Language [EN ▼] │
│ Timezone [Auto] │
│                 │
│ [Continue]      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Contacts Match  │
│ (Optional)      │
│                 │
│ [Scan Contacts] │
│ [Skip]          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
└─────────────────┘
```

### 8.2 Device Approval Flow

```
┌─────────────────┐        ┌─────────────────┐
│   New Device    │        │  Trusted Device │
│   (Logging in)  │        │  (User's phone) │
└────────┬────────┘        └────────┬────────┘
         │                          │
         │ 1. Login attempt         │
         │                          │
         │ 2. System detects        │
         │    new device            │
         │                          │
         │ 3. Login held pending    │
         │                          │
         │                          │ 4. Push notification
         │                    ┌─────┴─────┐
         │                    │ New login │
         │                    │ request   │
         │                    │           │
         │                    │ iPhone 15 │
         │                    │ New York  │
         │                    │           │
         │                    │ [Approve] │
         │                    │ [Deny]    │
         │                    └─────┬─────┘
         │                          │
         │                          │ 5. User taps Approve
         │◄─────────────────────────│
         │                          │
         │ 6. Login completes       │
         │                          │
         ▼                          ▼
┌─────────────────┐        ┌─────────────────┐
│   Dashboard     │        │ "Login approved"│
│   (New device)  │        │ notification    │
└─────────────────┘        └─────────────────┘
```

### 8.3 Travel Mode Activation Flow

```
┌─────────────────┐
│ User traveling  │
│ internationally │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Open Settings   │
│ → Travel Mode   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Review hidden   │
│ data types      │
│                 │
│ ☑ Financial     │
│ ☑ Medical       │
│ ☑ Business docs │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Set duress PIN  │
│ (optional)      │
│                 │
│ PIN: [••••••]   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Enable Travel   │
│ Mode            │
│                 │
│ [Enable]        │
└────────┬────────┘
         │
         ├──────────────────────┐
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│ Trusted contact │    │ ✈️ Travel mode  │
│ notified        │    │ indicator shown │
│ (if configured) │    │ in app header   │
└─────────────────┘    └─────────────────┘
```

### 8.4 Privacy Dashboard Flow

```
┌─────────────────┐
│ Settings →      │
│ Privacy         │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Privacy Dashboard           │
│                             │
│ Score: 78/100 [████████░░]  │
│                             │
│ 💡 Recommendations:         │
│ • Enable 2FA (+10)          │
│ • Review apps (+5)          │
│                             │
│ Organizations:              │
│ ┌─────────────────────────┐ │
│ │ 🏢 Work                 │ │
│ │ Can see: Name, Email    │ │
│ │ [Manage →]              │ │
│ └─────────────────────────┘ │
│                             │
│ [Export Data]               │
│ [Delete Account]            │
└─────────────────────────────┘
```

---

## 9. Non-Functional Requirements

### 9.1 Performance

| Metric                     | Target      | Measurement                        |
| -------------------------- | ----------- | ---------------------------------- |
| Profile load               | < 1 second  | Time to display profile screen     |
| Org switch                 | < 400ms     | Time from tap to new org loaded    |
| Search results             | < 2 seconds | Time from submit to results        |
| Push notification delivery | < 1 second  | Time from trigger to device        |
| App cold start             | < 3 seconds | Time from tap to interactive       |
| App warm start             | < 1 second  | Time from background to foreground |
| Briefing generation        | < 5 seconds | Time to generate daily briefing    |
| Voice clone training       | < 24 hours  | Time from sample upload to ready   |

### 9.2 Scalability

| Dimension              | Target   | Notes                  |
| ---------------------- | -------- | ---------------------- |
| Concurrent users       | 100,000  | Per environment        |
| Organizations per user | 50       | Soft limit             |
| Devices per user       | 20       | Active devices         |
| Shortcuts per user     | 50       | Personal shortcuts     |
| Vault storage          | 1GB base | Expandable via upgrade |
| Emergency contacts     | 5        | Per user               |
| Blocked contacts       | 500      | Per user               |

### 9.3 Availability

| Metric                         | Target                           |
| ------------------------------ | -------------------------------- |
| Uptime                         | 99.9% (8.76 hours downtime/year) |
| Planned maintenance window     | Sundays 2-4 AM UTC               |
| Recovery Time Objective (RTO)  | 1 hour                           |
| Recovery Point Objective (RPO) | 5 minutes                        |

### 9.4 Security

| Requirement        | Implementation                  |
| ------------------ | ------------------------------- |
| Data at rest       | AES-256 encryption              |
| Data in transit    | TLS 1.3 minimum                 |
| Personal vault     | E2E encryption (user holds key) |
| Session management | Secure tokens in Redis          |
| Audit logging      | All security events logged      |
| Voice data         | Encrypted, user-deletable       |
| AI memory          | Encrypted, user-deletable       |

### 9.5 Compliance

| Standard      | Status          | Notes                          |
| ------------- | --------------- | ------------------------------ |
| GDPR          | Required        | Data export, deletion, consent |
| CCPA          | Required        | Similar to GDPR                |
| SOC 2 Type II | Planned Q4 2026 | For enterprise customers       |
| HIPAA         | Future          | For health data features       |

### 9.6 Accessibility

| Requirement           | Target                |
| --------------------- | --------------------- |
| WCAG Level            | AA                    |
| Screen reader support | Full                  |
| Keyboard navigation   | Full                  |
| Color contrast        | 4.5:1 minimum         |
| Touch targets         | 44x44pt minimum       |
| Font scaling          | Supports 200%         |
| Motion sensitivity    | Reduced motion option |

---

## 10. Dependencies & Integrations

### 10.1 Internal Dependencies

| Dependency       | Type     | Description                               |
| ---------------- | -------- | ----------------------------------------- |
| Dartwing Core    | Module   | Person, Organization, Org Member doctypes |
| Frappe Framework | Platform | User, Role, Permission infrastructure     |
| Dartwing Comms   | Module   | For notifications, messages               |
| Dartwing AI      | Module   | For briefings, voice clone, AI memory     |

### 10.2 External Dependencies

| Service            | Purpose                  | Criticality      |
| ------------------ | ------------------------ | ---------------- |
| Redis              | Session storage, caching | Critical         |
| MariaDB/PostgreSQL | Data persistence         | Critical         |
| SendGrid/SES       | Email delivery           | Critical         |
| Firebase/APNs      | Push notifications       | High             |
| ElevenLabs/Play.ht | Voice cloning            | Medium (Phase 4) |
| Twilio             | SMS verification         | Medium           |
| Persona/Jumio      | Identity verification    | Medium (Phase 2) |
| Apple Health API   | Health data              | Low (Phase 4)    |
| Google Fit API     | Health data              | Low (Phase 4)    |

### 10.3 Architecture Integration

```
┌───────────────────────────────────────────────────────────────┐
│                     Dartwing User Module                       │
└───────────────────────────────────────────────────────────────┘
         │              │               │              │
         ▼              ▼               ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Core       │ │   Frappe    │ │    AI       │ │  External   │
│  Module     │ │   Backend   │ │   Module    │ │  Services   │
│             │ │             │ │             │ │             │
│ - Person    │ │ - User CRUD │ │ - Briefing  │ │ - Email     │
│ - Org       │ │ - API       │ │ - Voice     │ │ - Push      │
│ - Member    │ │ - Hooks     │ │ - Memory    │ │ - IDV       │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 11. Risks & Mitigations

### 11.1 Technical Risks

| Risk                                  | Probability | Impact | Mitigation                                     |
| ------------------------------------- | ----------- | ------ | ---------------------------------------------- |
| Cross-org search performance degrades | Medium      | Medium | Elasticsearch, query optimization, caching     |
| Voice clone quality inconsistent      | Medium      | Low    | Multiple providers, user feedback, re-training |
| Device trust score gaming             | Low         | Medium | ML-based anomaly detection, manual review      |
| E2E encryption key loss               | Low         | High   | Key recovery options, warning prompts          |
| Mobile deep link failures             | Medium      | Medium | Universal links, fallback web                  |

### 11.2 Business Risks

| Risk                         | Probability | Impact | Mitigation                                   |
| ---------------------------- | ----------- | ------ | -------------------------------------------- |
| Low multi-org adoption       | Medium      | High   | Incentivize org creation, showcase value     |
| Privacy concerns deter users | Low         | High   | Transparency, data controls, no selling data |
| Competitor copies features   | High        | Medium | Execution speed, network effects             |
| Premium conversion too low   | Medium      | Medium | Free tier value + clear premium benefits     |

### 11.3 Compliance Risks

| Risk                  | Probability | Impact   | Mitigation                            |
| --------------------- | ----------- | -------- | ------------------------------------- |
| GDPR violation        | Low         | Critical | Legal review, automated compliance    |
| Data breach           | Low         | Critical | Encryption, access controls, audits   |
| Voice clone misuse    | Medium      | High     | Watermarking, consent, usage tracking |
| Health data liability | Low         | High     | Clear consent, HIPAA planning         |

---

## 12. Release Plan

### 12.1 Phase 1: Foundation (Q1 2026)

**Goal:** Core identity and security features

**Features:**

- U-01: User Profile & Preferences
- U-02: Multi-Organization Management
- U-03: Device Trust & Management
- U-14: Emergency Contacts
- U-15: Notification Preferences
- U-22: Smart Invitations
- U-23: Biometric Unlock
- U-25: Session Management

**Success Criteria:**

- 2,000 registered users
- 80% profile completion rate
- 50% of users in 2+ orgs
- < 400ms org switch time

### 12.2 Phase 2: Security & Privacy (Q2 2026)

**Goal:** Enterprise-ready security and privacy controls

**Features:**

- U-04: Global Block List
- U-06: Travel Mode (with Duress PIN)
- U-07: Push-to-Approve Login
- U-12: Identity Verification
- U-13: Personal Vault
- U-16: Privacy Dashboard
- U-17: Data Export
- U-18: Account Deletion
- U-19: Cross-Org Search
- U-20: Unified Activity Feed
- U-24: Passkey Support

**Success Criteria:**

- 5,000 registered users
- 40% with privacy features enabled
- 30% with Standard+ verification
- < 2 second search results

### 12.3 Phase 3: AI & Engagement (Q3 2026)

**Goal:** Personalized experience and daily engagement

**Features:**

- U-05: Personal Shortcuts (with location/time triggers)
- U-10: Daily AI Briefing (with audio)
- U-11: Live Location Sharing
- U-21: Contact Auto-Match

**Success Criteria:**

- 10,000 registered users
- 35% daily briefing open rate
- 50 shortcuts per 100 users
- 20% location share usage

### 12.4 Phase 4: Advanced Personalization (Q4 2026)

**Goal:** Premium features and long-term engagement

**Features:**

- U-08: Digital Will
- U-09: AI Voice Profile (with watermarking)
- U-26: Achievements & Gamification
- U-27: Reputation Score
- U-28: Personal AI Memory
- U-29: Health Data Integration
- U-30: Wearable Device Sync

**Success Criteria:**

- 15,000 registered users
- 10% voice clone adoption
- 5% digital will enabled
- 15% on paid tier

---

## 13. Data Model

### 13.1 Doctype Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER MODULE DATA MODEL                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Person (Core Module)                      ││
│  │              The master identity record                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              │ 1:1                               │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      User Profile                            ││
│  │  person, theme, language, timezone, travel_mode, ...        ││
│  │                                                              ││
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         ││
│  │  │ shortcuts[]  │ │  blocks[]    │ │ emergency[]  │         ││
│  │  └──────────────┘ └──────────────┘ └──────────────┘         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │ User Device │      │AI Voice     │      │ Digital Will│     │
│  │             │      │Profile      │      │             │     │
│  │ person      │      │ person      │      │ person      │     │
│  │ device_id   │      │ voice_model │      │ trusted_    │     │
│  │ is_trusted  │      │ personality │      │   contacts  │     │
│  │ trust_score │      │ permissions │      │ inactive_   │     │
│  │ last_active │      │ watermark   │      │   days      │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │ Location    │      │ Personal    │      │ Verification│     │
│  │ Share       │      │ Vault Item  │      │ Record      │     │
│  │             │      │             │      │             │     │
│  │ person      │      │ person      │      │ person      │     │
│  │ shared_with │      │ file        │      │ level       │     │
│  │ expires_at  │      │ category    │      │ verified_at │     │
│  │ lat/lng     │      │ encrypted   │      │ provider    │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │ Privacy     │      │ AI Memory   │      │ Reputation  │     │
│  │ Setting     │      │ Entry       │      │ Score       │     │
│  │             │      │             │      │             │     │
│  │ person      │      │ person      │      │ person      │     │
│  │ organization│      │ context     │      │ score       │     │
│  │ data_type   │      │ memory_text │      │ components  │     │
│  │ allowed     │      │ expires_at  │      │ updated_at  │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 13.2 Key Doctypes

| Doctype             | Purpose              | Key Fields                                                          |
| ------------------- | -------------------- | ------------------------------------------------------------------- |
| User Profile        | Personal preferences | theme, language, timezone, travel_mode, duress_pin                  |
| User Device         | Trusted devices      | device_id, device_name, is_trusted, trust_score, last_active        |
| User Shortcut       | Custom commands      | trigger_phrase, action_type, target, location_trigger, time_trigger |
| User Block          | Blocked contacts     | block_type, blocked_person/phone/email, reason                      |
| User Location Share | Live location        | shared_with, expires_at, latitude, longitude                        |
| AI Voice Profile    | Voice clone          | voice_model_id, personality_prompt, permissions, watermark_key      |
| Digital Will        | Succession           | trusted_contacts[], inactive_days, access_level, status             |
| Personal Vault Item | Secure storage       | file, category, is_encrypted, encryption_key                        |
| Emergency Contact   | ICE contacts         | contact_person, relationship, priority, phone                       |
| Verification Record | ID verification      | level, verified_at, provider, document_type, expires_at             |
| Privacy Setting     | Per-org permissions  | organization, data_type, is_allowed                                 |
| AI Memory Entry     | AI context           | context_type, memory_text, expires_at                               |
| Reputation Score    | Trust metric         | score, identity_component, payment_component, feedback_component    |

---

## 14. API Specification

### 14.1 Profile APIs

| Endpoint            | Method | Purpose            |
| ------------------- | ------ | ------------------ |
| `/user/profile`     | GET    | Get user profile   |
| `/user/profile`     | PUT    | Update profile     |
| `/user/preferences` | GET    | Get preferences    |
| `/user/preferences` | PUT    | Update preferences |
| `/user/avatar`      | POST   | Upload avatar      |

### 14.2 Device APIs

| Endpoint                     | Method | Purpose         |
| ---------------------------- | ------ | --------------- |
| `/user/devices`              | GET    | List devices    |
| `/user/devices`              | POST   | Register device |
| `/user/devices/{id}`         | DELETE | Revoke device   |
| `/user/devices/{id}/trust`   | POST   | Trust device    |
| `/user/devices/{id}/approve` | POST   | Approve pending |
| `/user/devices/sign-out-all` | POST   | Sign out all    |

### 14.3 Organization APIs

| Endpoint                         | Method | Purpose                  |
| -------------------------------- | ------ | ------------------------ |
| `/user/organizations`            | GET    | List organizations       |
| `/user/organizations/{id}/leave` | POST   | Leave organization       |
| `/user/invitations`              | GET    | List pending invitations |
| `/user/invitations/{id}/accept`  | POST   | Accept invitation        |
| `/user/invitations/{id}/decline` | POST   | Decline invitation       |

### 14.4 Privacy APIs

| Endpoint                 | Method | Purpose                  |
| ------------------------ | ------ | ------------------------ |
| `/user/privacy/settings` | GET    | Get all privacy settings |
| `/user/privacy/settings` | PUT    | Update privacy settings  |
| `/user/privacy/export`   | POST   | Request data export      |
| `/user/privacy/delete`   | POST   | Request account deletion |
| `/user/privacy/score`    | GET    | Get privacy score        |
| `/user/blocks`           | GET    | Get block list           |
| `/user/blocks`           | POST   | Add block                |
| `/user/blocks/{id}`      | DELETE | Remove block             |

### 14.5 Security APIs

| Endpoint                   | Method | Purpose                |
| -------------------------- | ------ | ---------------------- |
| `/user/travel-mode`        | POST   | Toggle travel mode     |
| `/user/travel-mode/status` | GET    | Get travel mode status |
| `/user/sessions`           | GET    | List active sessions   |
| `/user/sessions/{id}`      | DELETE | End session            |

### 14.6 Feature APIs

| Endpoint                    | Method              | Purpose                   |
| --------------------------- | ------------------- | ------------------------- |
| `/user/briefing`            | GET                 | Get daily briefing        |
| `/user/briefing/audio`      | GET                 | Get audio briefing        |
| `/user/shortcuts`           | GET/POST/PUT/DELETE | Manage shortcuts          |
| `/user/location-share`      | POST                | Start location share      |
| `/user/location-share/{id}` | DELETE              | Stop sharing              |
| `/user/emergency-contacts`  | GET/POST/PUT/DELETE | Manage contacts           |
| `/user/vault`               | GET/POST/DELETE     | Manage vault items        |
| `/user/voice-profile`       | GET/POST/DELETE     | Manage voice profile      |
| `/user/digital-will`        | GET/PUT             | Manage digital will       |
| `/user/verification/start`  | POST                | Start ID verification     |
| `/user/verification/status` | GET                 | Check verification status |
| `/user/ai-memory`           | GET/DELETE          | View/clear AI memory      |
| `/user/cross-org-search`    | POST                | Search across orgs        |
| `/user/activity-feed`       | GET                 | Get unified feed          |
| `/user/reputation`          | GET                 | Get reputation score      |

---

## 15. Appendices

### Appendix A: Glossary

| Term               | Definition                                                        |
| ------------------ | ----------------------------------------------------------------- |
| Person             | Master identity record in Dartwing Core representing a human      |
| User Profile       | Personal preferences and settings in User module                  |
| Org Member         | Link between Person and Organization with role                    |
| Trusted Device     | Device approved by user for login without additional verification |
| Trust Score        | Calculated score (0-100) of device trustworthiness                |
| Digital Will       | Emergency access grant to trusted contact after inactivity        |
| Duress PIN         | Secondary PIN that shows decoy data when entered under coercion   |
| Travel Mode        | Security mode that hides sensitive data while traveling           |
| Cross-Org          | Features that work across multiple organizations                  |
| Verification Level | Tier of identity verification (Basic, Standard, Enhanced)         |
| Personal Vault     | E2E encrypted document storage                                    |
| AI Memory          | Persistent AI context that remembers user preferences             |
| Reputation Score   | Portable trust metric based on identity, payments, feedback       |

### Appendix B: Competitive Analysis

| Feature               | Dartwing | Google | Apple | Okta | Auth0 |
| --------------------- | -------- | ------ | ----- | ---- | ----- |
| Multi-org identity    | ✅       | ❌     | ❌    | ⚠️   | ⚠️    |
| Cross-org search      | ✅       | ❌     | ❌    | ❌   | ❌    |
| Personal AI assistant | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Voice clone           | ✅       | ❌     | ❌    | ❌   | ❌    |
| Digital will          | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Travel mode / Duress  | ✅       | ❌     | ❌    | ❌   | ❌    |
| Global block list     | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Privacy dashboard     | ✅       | ⚠️     | ✅    | ⚠️   | ⚠️    |
| Personal vault        | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Identity verification | ✅       | ⚠️     | ⚠️    | ⚠️   | ⚠️    |
| Reputation score      | ✅       | ❌     | ❌    | ❌   | ❌    |
| Device trust score    | ✅       | ⚠️     | ⚠️    | ⚠️   | ⚠️    |
| Passkey support       | ✅       | ✅     | ✅    | ✅   | ✅    |

✅ = Full support | ⚠️ = Partial/limited | ❌ = Not available

### Appendix C: Screen Inventory

| Screen                | Route                     | Priority | Phase |
| --------------------- | ------------------------- | -------- | ----- |
| Profile               | `/profile`                | P0       | 1     |
| Preferences           | `/settings/preferences`   | P1       | 1     |
| Organizations         | `/organizations`          | P0       | 1     |
| Devices               | `/settings/devices`       | P0       | 1     |
| Sessions              | `/settings/sessions`      | P0       | 1     |
| Privacy Dashboard     | `/settings/privacy`       | P1       | 2     |
| Block List            | `/settings/blocks`        | P1       | 2     |
| Travel Mode           | `/settings/travel`        | P1       | 2     |
| Identity Verification | `/verify`                 | P1       | 2     |
| Personal Vault        | `/vault`                  | P1       | 2     |
| Emergency Contacts    | `/emergency`              | P0       | 1     |
| Notifications         | `/settings/notifications` | P0       | 1     |
| Shortcuts             | `/settings/shortcuts`     | P1       | 3     |
| Daily Briefing        | `/briefing`               | P1       | 3     |
| Activity Feed         | `/activity`               | P1       | 2     |
| Cross-Org Search      | `/search`                 | P1       | 2     |
| Digital Will          | `/settings/will`          | P2       | 4     |
| Voice Profile         | `/settings/voice`         | P2       | 4     |
| AI Memory             | `/settings/ai-memory`     | P2       | 4     |
| Reputation            | `/reputation`             | P2       | 4     |

### Appendix D: Architecture Cross-Reference

| Component           | Reference Document               |
| ------------------- | -------------------------------- |
| Person doctype      | dartwing_core_prd.md, Section 3  |
| Authentication      | dartwing_core_prd.md, Section 4  |
| Notification system | dartwing_core_prd.md, Section 8  |
| AI features         | dartwing_core_prd.md, Section 12 |
| Privacy/GDPR        | dartwing_core_prd.md, Section 9  |
| File storage        | dartwing_core_prd.md, Section 7  |

---

## Document History

| Version | Date          | Author         | Changes                                                                     |
| ------- | ------------- | -------------- | --------------------------------------------------------------------------- |
| 1.0     | November 2025 | Claude + Brett | Initial PRD                                                                 |
| 2.0     | November 2025 | Claude + Brett | Merged best of both PRDs, added 14 new features, enhanced existing features |

---

_End of Document_
