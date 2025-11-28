# Dartwing User Module - Product Requirements Document

**Version 1.0 | November 2025**

**Product Owner:** Brett  
**Target Release:** Q1 2026 (Phase 1)  
**Status:** Draft

---

## Table of Contents

1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Personas
5. Feature Requirements
6. User Stories & Acceptance Criteria
7. User Flows
8. Non-Functional Requirements
9. Dependencies & Integrations
10. Risks & Mitigations
11. Release Plan
12. Appendices

---

## 1. Executive Summary

### 1.1 Product Vision

The Dartwing User Module provides a **unified personal identity layer** that enables individuals to seamlessly navigate across all their organizations—families, companies, nonprofits, clubs, and associations—with a single login and personalized experience.

Unlike traditional identity systems that treat users as accounts within isolated applications, Dartwing User treats each human as a **first-class citizen** whose identity, preferences, and digital life transcend organizational boundaries.

### 1.2 Value Proposition

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
- Premium upsell opportunities (AI voice clone, advanced privacy features)

### 1.3 Scope

**In Scope:**

- Authentication (Keycloak SSO, magic-link, social login)
- Personal identity management (profile, preferences, devices)
- Cross-organization features (org switcher, unified search, dashboard)
- Privacy controls (block list, travel mode, data export)
- AI personalization (voice clone, shortcuts, daily briefing)
- Emergency features (digital will, location sharing)

**Out of Scope:**

- Organization-specific features (handled by Family, Company, etc. modules)
- Billing and subscriptions (separate Billing module)
- Content creation tools (handled by respective modules)
- Third-party app integrations (future API module)

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

### 2.2 Target Users

Primary: Adults managing multiple life contexts (work, family, community)
Secondary: Organization administrators who onboard/manage members
Tertiary: IT administrators handling enterprise SSO integration

### 2.3 Market Opportunity

- 2.5B people use multiple productivity/collaboration tools daily
- Enterprise SSO market: $2.3B (2024) → $5.8B (2030)
- Consumer identity market: Largely untapped outside social login
- Privacy-conscious users willing to pay for control

---

## 3. Goals & Success Metrics

### 3.1 Business Goals

| Goal               | Target                    | Timeframe |
| ------------------ | ------------------------- | --------- |
| User Registration  | 10,000 active users       | Q2 2026   |
| Multi-Org Adoption | 60% of users in 2+ orgs   | Q3 2026   |
| SSO Integration    | 50 enterprise customers   | Q4 2026   |
| Premium Conversion | 15% of users on paid tier | Q4 2026   |

### 3.2 Product Goals

| Goal               | Metric                             | Target      |
| ------------------ | ---------------------------------- | ----------- |
| Frictionless Auth  | Time to login                      | < 5 seconds |
| Cross-Org Utility  | Org switches per session           | 2.5 average |
| Privacy Confidence | Users enabling 2+ privacy features | 40%         |
| AI Engagement      | Daily briefing open rate           | 35%         |

### 3.3 Key Performance Indicators (KPIs)

**Acquisition:**

- New user registrations per week
- Invite acceptance rate
- Social login adoption rate

**Activation:**

- Users completing profile setup
- Users connecting 2+ organizations
- Users enabling push notifications

**Engagement:**

- Daily active users (DAU)
- Org switches per session
- Cross-org searches per user
- Daily briefing engagement

**Retention:**

- 7-day retention rate
- 30-day retention rate
- Churn rate by org count

**Revenue (Future):**

- Premium tier conversion rate
- AI voice clone adoption
- Enterprise SSO contracts

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

### 4.3 Tertiary Persona: Privacy-Conscious User

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

**Quote:** _"I'll use your platform if I own my data and can delete everything with one click."_

---

### 4.4 Edge Persona: Elderly Family Member

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

## 5. Feature Requirements

### 5.1 Feature Priority Matrix

| Priority | Feature                         | Effort | Impact | Phase |
| -------- | ------------------------------- | ------ | ------ | ----- |
| P0       | Magic-Link Login                | M      | High   | 1     |
| P0       | Keycloak SSO                    | L      | High   | 1     |
| P0       | Global Person ↔ User Link       | M      | High   | 1     |
| P0       | Basic User Profile              | M      | High   | 1     |
| P0       | Device Registration             | M      | High   | 1     |
| P1       | Social Login (Google, Apple)    | M      | High   | 1     |
| P1       | Multi-Org Switcher              | M      | High   | 1     |
| P1       | Smart Invite Flow               | L      | High   | 1     |
| P1       | Theme & Language Preferences    | S      | Medium | 1     |
| P1       | Device Trust & Revoke           | M      | High   | 2     |
| P1       | Push-to-Approve Logins          | L      | Medium | 2     |
| P2       | Enterprise SSO (Azure AD, Okta) | L      | High   | 2     |
| P2       | Global Block List               | M      | Medium | 2     |
| P2       | Travel Mode                     | M      | Medium | 2     |
| P2       | Unified Personal Dashboard      | L      | High   | 2     |
| P2       | Cross-Org Search                | L      | High   | 2     |
| P2       | Data Export (GDPR)              | M      | Medium | 2     |
| P2       | Account Deletion                | M      | Medium | 2     |
| P3       | Daily AI Briefing               | L      | Medium | 3     |
| P3       | Personal Shortcut Commands      | M      | Medium | 3     |
| P3       | Contacts Auto-Match             | M      | Medium | 3     |
| P3       | Live Location Share             | L      | Medium | 3     |
| P3       | Personal AI Voice Clone         | XL     | Medium | 4     |
| P3       | Digital Will                    | L      | Low    | 4     |

**Effort Key:** S = Small (1-2 days), M = Medium (3-5 days), L = Large (1-2 weeks), XL = Extra Large (3+ weeks)

---

### 5.2 Detailed Feature Specifications

#### Feature 1: Magic-Link Login

**Priority:** P0  
**Phase:** 1  
**Effort:** Medium

**Description:**
Users authenticate by receiving a one-time link via email. Clicking the link logs them in without entering a password. This is the default and recommended authentication method.

**Requirements:**

| ID     | Requirement                                                  | Priority |
| ------ | ------------------------------------------------------------ | -------- |
| ML-001 | User enters email address on login screen                    | Must     |
| ML-002 | System sends magic link within 5 seconds                     | Must     |
| ML-003 | Magic link expires after 15 minutes                          | Must     |
| ML-004 | Magic link is single-use                                     | Must     |
| ML-005 | Clicking link opens app (deep link) on mobile                | Must     |
| ML-006 | Clicking link opens web app in browser                       | Must     |
| ML-007 | User is fully authenticated after clicking link              | Must     |
| ML-008 | System issues access + refresh tokens                        | Must     |
| ML-009 | "Resend link" option available after 60 seconds              | Should   |
| ML-010 | Link works across devices (email on phone, click on desktop) | Should   |
| ML-011 | Branded email template with organization context             | Should   |
| ML-012 | Rate limiting: max 5 links per email per hour                | Must     |

**User Flow:**

```
1. User opens app → sees "Enter your email"
2. User enters email → taps "Send Magic Link"
3. User sees "Check your email" screen with:
   - Animated mail icon
   - "Didn't receive it? Resend" (greyed out for 60s)
   - "Try a different email" link
4. User opens email → sees branded message with "Log In" button
5. User taps button → deep link opens app
6. User is logged in → sees dashboard or onboarding
```

**Error Handling:**

- Invalid email format: "Please enter a valid email address"
- Email not found (new user): Redirect to signup flow
- Rate limited: "Too many requests. Please try again in X minutes."
- Expired link: "This link has expired. Request a new one."
- Already used link: "This link has already been used. Request a new one."

**Technical Notes:**

- Keycloak "magic-link" authenticator extension required
- Deep links: `io.dartwing.app://auth/callback?token=xxx`
- Universal links for iOS, App Links for Android
- Fallback to web if app not installed

---

#### Feature 2: Keycloak SSO

**Priority:** P0  
**Phase:** 1  
**Effort:** Large

**Description:**
All Dartwing applications authenticate through a centralized Keycloak instance. Users log in once and have seamless access to all Dartwing services (mobile app, web portal, Frappe backend, future apps).

**Requirements:**

| ID     | Requirement                                                 | Priority |
| ------ | ----------------------------------------------------------- | -------- |
| KC-001 | Single Keycloak realm per environment (dev, test, prod)     | Must     |
| KC-002 | OAuth2 Authorization Code flow with PKCE for all clients    | Must     |
| KC-003 | Support for OpenID Connect (OIDC) protocol                  | Must     |
| KC-004 | Access tokens expire in 5 minutes                           | Must     |
| KC-005 | Refresh tokens expire in 30 days                            | Must     |
| KC-006 | Offline tokens for background sync                          | Should   |
| KC-007 | Token introspection endpoint for API validation             | Must     |
| KC-008 | User info endpoint returns email, name, groups              | Must     |
| KC-009 | Brute force protection (5 failed attempts = 15 min lockout) | Must     |
| KC-010 | SSL/TLS required for all connections                        | Must     |
| KC-011 | Session idle timeout: 30 minutes                            | Should   |
| KC-012 | Session max lifetime: 10 hours                              | Should   |
| KC-013 | Concurrent session limit: 10 per user                       | Should   |

**Keycloak Clients:**

| Client ID        | Type         | Purpose                  |
| ---------------- | ------------ | ------------------------ |
| dartwing-mobile  | Public       | Flutter iOS/Android apps |
| dartwing-web     | Public       | Flutter web app          |
| dartwing-desktop | Public       | Flutter desktop apps     |
| frappe-backend   | Confidential | Frappe API server        |
| admin-cli        | Confidential | Admin automation         |

**Token Claims:**

```json
{
  "sub": "uuid-keycloak-user-id",
  "email": "user@example.com",
  "email_verified": true,
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "groups": ["/dartwing/users", "/org-123/members"],
  "org_context": "org-123"
}
```

---

#### Feature 3: Social + Enterprise Login

**Priority:** P1 (Social), P2 (Enterprise)  
**Phase:** 1 (Social), 2 (Enterprise)  
**Effort:** Medium (Social), Large (Enterprise)

**Description:**
Users can authenticate using existing social accounts (Google, Apple, Microsoft, Facebook) or enterprise identity providers (Azure AD, Okta, Google Workspace).

**Social Login Requirements:**

| ID     | Requirement                                                | Priority |
| ------ | ---------------------------------------------------------- | -------- |
| SL-001 | "Continue with Google" button on login screen              | Must     |
| SL-002 | "Continue with Apple" button on login screen               | Must     |
| SL-003 | "Continue with Microsoft" button on login screen           | Should   |
| SL-004 | "Continue with Facebook" button on login screen            | Could    |
| SL-005 | First-time social login creates new Person record          | Must     |
| SL-006 | Returning social login links to existing Person (by email) | Must     |
| SL-007 | Profile photo imported from social provider                | Should   |
| SL-008 | Name imported from social provider                         | Must     |
| SL-009 | User can unlink social account later                       | Should   |

**Enterprise SSO Requirements:**

| ID     | Requirement                                 | Priority |
| ------ | ------------------------------------------- | -------- |
| ES-001 | Azure AD integration via SAML or OIDC       | Must     |
| ES-002 | Okta integration via SAML or OIDC           | Must     |
| ES-003 | Google Workspace integration                | Should   |
| ES-004 | LDAP integration for on-premise AD          | Could    |
| ES-005 | Automatic user provisioning (SCIM)          | Should   |
| ES-006 | Group-to-role mapping from IdP              | Must     |
| ES-007 | Just-in-time user creation                  | Must     |
| ES-008 | Forced SSO (disable password login for org) | Should   |

**Social Login Flow:**

```
1. User taps "Continue with Google"
2. Redirect to Google OAuth consent screen
3. User grants permission
4. Redirect back to app with auth code
5. Exchange code for tokens via Keycloak
6. Keycloak creates/links user
7. User is logged in
```

---

#### Feature 4: Global Person ↔ User Link

**Priority:** P0  
**Phase:** 1  
**Effort:** Medium

**Description:**
Every authenticated user is linked to exactly one Person record in Dartwing Core. This creates a permanent, universal identity that persists across all organizations and applications.

**Requirements:**

| ID     | Requirement                                                            | Priority |
| ------ | ---------------------------------------------------------------------- | -------- |
| PU-001 | Frappe User linked to Person via `frappe_user` field                   | Must     |
| PU-002 | Person linked to Keycloak via `keycloak_user_id` field                 | Must     |
| PU-003 | One Person per human (no duplicates)                                   | Must     |
| PU-004 | Person created automatically on first login                            | Must     |
| PU-005 | Person record survives org membership changes                          | Must     |
| PU-006 | Email change syncs between Keycloak, User, Person                      | Must     |
| PU-007 | Name change syncs between Keycloak, User, Person                       | Should   |
| PU-008 | Person can exist before Keycloak user (invited but not yet registered) | Must     |
| PU-009 | Merging duplicate Persons (admin function)                             | Should   |

**Identity Chain:**

```
Keycloak User (authentication)
      ↓ keycloak_user_id
Frappe User (authorization)
      ↓ frappe_user
Person (identity)
      ↓ person
User Profile (preferences)
```

**Sync Rules:**

- Keycloak is source of truth for authentication
- Person is source of truth for identity attributes
- Changes in Keycloak trigger sync to Person
- Changes in Person UI trigger sync to Keycloak (admin only)

---

#### Feature 5: Smart Invite Flow

**Priority:** P1  
**Phase:** 1  
**Effort:** Large

**Description:**
Organization members can invite new users with pre-filled information. Invitees simply tap a magic link to join—no forms to fill out if the inviter provided details.

**Requirements:**

| ID     | Requirement                                            | Priority |
| ------ | ------------------------------------------------------ | -------- |
| SI-001 | Inviter can enter: first name, last name, email, phone | Must     |
| SI-002 | Only email is required                                 | Must     |
| SI-003 | Inviter can select role template for invitee           | Must     |
| SI-004 | Inviter can add personal message                       | Should   |
| SI-005 | Invite sent via email with magic link                  | Must     |
| SI-006 | Invite expires after 7 days                            | Must     |
| SI-007 | Inviter can revoke pending invite                      | Must     |
| SI-008 | Inviter can resend invite                              | Must     |
| SI-009 | Invitee tapping link creates account + joins org       | Must     |
| SI-010 | If invitee already has account, just joins org         | Must     |
| SI-011 | Pre-filled info populates Person record                | Must     |
| SI-012 | Invitee can edit pre-filled info before confirming     | Should   |
| SI-013 | Bulk invite via CSV upload                             | Should   |
| SI-014 | QR code invite for in-person onboarding                | Could    |
| SI-015 | Invite tracking dashboard for admins                   | Should   |

**Invite Email Content:**

```
Subject: [Inviter Name] invited you to join [Organization Name]

Hi [First Name],

[Inviter Name] has invited you to join [Organization Name] on Dartwing.

[Personal message if provided]

Tap the button below to accept:

[Join Organization]

This invitation expires on [Date].

---
Dartwing - One identity, all your organizations
```

**Invite Acceptance Flow:**

```
1. Invitee receives email
2. Invitee taps "Join Organization"
3. Deep link opens app (or web)
4. System checks if email matches existing account:

   [Existing User]
   - Show: "Welcome back! Join [Org] as [Role]?"
   - User confirms → Org Member created
   - Redirect to org dashboard

   [New User]
   - Show: "Create your account"
   - Pre-fill: name, email, phone from invite
   - User reviews/edits → confirms
   - Person + User + Org Member created
   - Redirect to onboarding
```

**CSV Bulk Invite Format:**

```csv
email,first_name,last_name,phone,role_template,message
john@example.com,John,Doe,+1-555-0100,Employee,Welcome to the team!
jane@example.com,Jane,Smith,,Manager,
```

---

#### Feature 6: Multi-Org Switcher

**Priority:** P1  
**Phase:** 1  
**Effort:** Medium

**Description:**
Users can instantly switch between their organizations without logging out. The current org context affects what data they see and what actions are available.

**Requirements:**

| ID     | Requirement                            | Priority |
| ------ | -------------------------------------- | -------- |
| MO-001 | Org switcher visible in app header/nav | Must     |
| MO-002 | Shows all orgs user belongs to         | Must     |
| MO-003 | Shows org name + type icon             | Must     |
| MO-004 | Shows org logo if available            | Should   |
| MO-005 | Shows user's role in each org          | Should   |
| MO-006 | One-tap to switch orgs                 | Must     |
| MO-007 | Current org highlighted                | Must     |
| MO-008 | Switch completes in < 500ms            | Must     |
| MO-009 | Data refreshes for new org context     | Must     |
| MO-010 | "Personal" context for cross-org view  | Should   |
| MO-011 | Recent orgs at top of list             | Should   |
| MO-012 | Search/filter for users with 10+ orgs  | Could    |

**Org Type Icons:**

- Family: 👨‍👩‍👧‍👦 (family emoji) or house icon
- Company: 🏢 (building emoji) or briefcase icon
- Nonprofit: 💚 (heart emoji) or hands icon
- Club: 👥 (people emoji) or groups icon
- Association: 🏛️ (building emoji) or handshake icon

**Switcher UI:**

```
┌─────────────────────────────┐
│ ┌───┐                       │
│ │ 🏢│ Acme Corp        ✓   │ ← Current
│ └───┘ Company · Admin       │
├─────────────────────────────┤
│ ┌───┐                       │
│ │👨‍👩‍👧│ Chen Family          │
│ └───┘ Family · Member       │
├─────────────────────────────┤
│ ┌───┐                       │
│ │ 🏠│ Oakwood HOA           │
│ └───┘ Club · Board Member   │
├─────────────────────────────┤
│ ┌───┐                       │
│ │ 🌐│ Personal View         │
│ └───┘ All organizations     │
└─────────────────────────────┘
```

---

#### Feature 7: Personal AI Voice Clone

**Priority:** P3  
**Phase:** 4  
**Effort:** Extra Large

**Description:**
Users can train an AI model on their voice and personality. This clone is used by all AI personas across all organizations, providing a consistent personal touch to automated communications.

**Requirements:**

| ID     | Requirement                                                 | Priority |
| ------ | ----------------------------------------------------------- | -------- |
| VC-001 | Voice training wizard in app                                | Must     |
| VC-002 | User records 5-10 sample phrases                            | Must     |
| VC-003 | Training completes within 24 hours                          | Must     |
| VC-004 | Preview cloned voice before enabling                        | Must     |
| VC-005 | Enable/disable voice clone per org                          | Should   |
| VC-006 | Personality questionnaire (formal/casual, humor, verbosity) | Must     |
| VC-007 | Custom personality prompt                                   | Should   |
| VC-008 | Voice used for AI-generated calls                           | Must     |
| VC-009 | Voice used for AI-generated voice messages                  | Must     |
| VC-010 | Voice used for text-to-speech in app                        | Should   |
| VC-011 | Delete voice clone and all data                             | Must     |
| VC-012 | Re-train voice clone                                        | Should   |

**Voice Training Flow:**

```
1. User opens "AI Voice Clone" settings
2. Intro screen explains feature + privacy
3. User records 10 prompted phrases:
   - "Hello, this is [Name]"
   - "I'm calling about your appointment"
   - "Please call me back at your convenience"
   - [7 more varied phrases]
4. Upload progress indicator
5. "Training in progress" status
6. Push notification when complete
7. User previews with custom text
8. User enables or re-records
```

**Privacy Considerations:**

- Voice data encrypted at rest (AES-256)
- Voice data never shared with organizations
- User can delete all voice data instantly
- Voice clone only used for user-initiated actions

---

#### Feature 8: Unified Personal Dashboard

**Priority:** P2  
**Phase:** 2  
**Effort:** Large

**Description:**
A single view showing everything the user needs across all organizations: pending tasks, upcoming events, unread notifications, and AI-curated highlights.

**Requirements:**

| ID     | Requirement                                    | Priority |
| ------ | ---------------------------------------------- | -------- |
| PD-001 | Dashboard is default home screen               | Must     |
| PD-002 | Shows items from all user's organizations      | Must     |
| PD-003 | Grouped by type (tasks, events, notifications) | Must     |
| PD-004 | Or grouped by organization (toggle)            | Should   |
| PD-005 | Color-coded by organization                    | Should   |
| PD-006 | Pending approvals section                      | Must     |
| PD-007 | Upcoming events (next 7 days)                  | Must     |
| PD-008 | Unread notifications                           | Must     |
| PD-009 | Quick actions (frequent tasks)                 | Should   |
| PD-010 | AI summary at top                              | Should   |
| PD-011 | Pull-to-refresh                                | Must     |
| PD-012 | Filter by organization                         | Should   |
| PD-013 | Filter by type                                 | Should   |
| PD-014 | Mark items as done/dismiss                     | Must     |
| PD-015 | Tap item to navigate to detail                 | Must     |

**Dashboard Layout:**

```
┌─────────────────────────────────────┐
│ Good morning, Sarah                 │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 📋 You have 3 items needing     │ │
│ │ attention: HOA vote, expense    │ │
│ │ report, and dentist at 3pm.     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ⏰ UPCOMING                         │
│ ├─ 3:00 PM  Kids' dentist (Family) │
│ ├─ Tomorrow  HOA Board Mtg (HOA)   │
│ └─ Friday    Quarterly Review (Work)│
│                                     │
│ ✅ NEEDS ACTION                     │
│ ├─ 🗳️ Vote: Pool renovation (HOA)  │
│ ├─ 💰 Approve: Travel expense (Work)│
│ └─ 📝 Sign: PTO request (Work)     │
│                                     │
│ 🔔 NOTIFICATIONS                    │
│ ├─ New photo album shared (Family) │
│ └─ Meeting rescheduled (Work)      │
└─────────────────────────────────────┘
```

---

#### Feature 9: Travel Mode

**Priority:** P2  
**Phase:** 2  
**Effort:** Medium

**Description:**
One toggle that prepares the user for travel: pauses non-critical notifications, sets auto-reply messages, and optionally hides sensitive data when crossing borders.

**Requirements:**

| ID     | Requirement                              | Priority |
| ------ | ---------------------------------------- | -------- |
| TM-001 | Single toggle to enable/disable          | Must     |
| TM-002 | Quick access from dashboard or settings  | Must     |
| TM-003 | Pauses non-critical push notifications   | Must     |
| TM-004 | Sets auto-reply for messages             | Should   |
| TM-005 | Auto-reply customizable                  | Should   |
| TM-006 | Hides sensitive data (configurable)      | Should   |
| TM-007 | Sensitive data: financials, SSN, medical | Should   |
| TM-008 | Travel mode indicator in UI              | Must     |
| TM-009 | Auto-disable after X days (configurable) | Should   |
| TM-010 | Critical notifications still delivered   | Must     |
| TM-011 | Notify org admins that user is traveling | Could    |

**Travel Mode Settings:**

```
┌─────────────────────────────────────┐
│ ✈️ Travel Mode                      │
│                                     │
│ [=========] ON                      │
│                                     │
│ Auto-reply message:                 │
│ ┌─────────────────────────────────┐ │
│ │ I'm currently traveling with    │ │
│ │ limited availability. I'll      │ │
│ │ respond when I return.          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Hide sensitive data:                │
│ [✓] Financial information           │
│ [✓] Personal documents              │
│ [ ] Contact details                 │
│                                     │
│ Auto-disable after: [7 days ▼]     │
│                                     │
│ Critical notifications:             │
│ [✓] Emergency contacts              │
│ [✓] Security alerts                 │
│ [ ] Org announcements               │
└─────────────────────────────────────┘
```

---

#### Feature 10: Global Block List

**Priority:** P2  
**Phase:** 2  
**Effort:** Medium

**Description:**
Users can block a person, phone number, or email once and have that block enforced across all organizations they belong to.

**Requirements:**

| ID     | Requirement                                | Priority |
| ------ | ------------------------------------------ | -------- |
| BL-001 | Block by Person record                     | Must     |
| BL-002 | Block by phone number                      | Must     |
| BL-003 | Block by email address                     | Must     |
| BL-004 | Block syncs to all orgs instantly          | Must     |
| BL-005 | Blocked contact can't call via Dartwing    | Must     |
| BL-006 | Blocked contact can't message via Dartwing | Must     |
| BL-007 | Blocked contact can't see user's location  | Must     |
| BL-008 | View all blocked contacts                  | Must     |
| BL-009 | Unblock contact                            | Must     |
| BL-010 | Block reason (optional)                    | Should   |
| BL-011 | Block date shown                           | Should   |
| BL-012 | Import blocks from phone contacts          | Could    |

**Block Flow:**

```
1. User views contact profile
2. User taps "..." menu → "Block"
3. Confirmation: "Block [Name]? They won't be able to contact you in any organization."
4. User confirms → block applied
5. Block syncs to all orgs
6. Toast: "[Name] has been blocked"
```

---

#### Feature 11: Device Trust & Revoke

**Priority:** P1  
**Phase:** 2  
**Effort:** Medium

**Description:**
Users can view all devices that have access to their account and revoke access instantly. Devices can be trusted (skip future verification) or untrusted (require verification each login).

**Requirements:**

| ID     | Requirement                                      | Priority |
| ------ | ------------------------------------------------ | -------- |
| DT-001 | List all devices with active sessions            | Must     |
| DT-002 | Show device name (user-editable)                 | Must     |
| DT-003 | Show device type (iPhone, Android, Desktop, Web) | Must     |
| DT-004 | Show last active time                            | Must     |
| DT-005 | Show last known location (city-level)            | Should   |
| DT-006 | Show IP address                                  | Should   |
| DT-007 | Mark device as trusted                           | Must     |
| DT-008 | Revoke device access                             | Must     |
| DT-009 | Revoke requires reason (optional)                | Should   |
| DT-010 | Revoke instantly invalidates all sessions        | Must     |
| DT-011 | Push notification when new device logs in        | Must     |
| DT-012 | "Revoke all other devices" button                | Should   |
| DT-013 | Trust score based on usage patterns              | Could    |

**Device List UI:**

```
┌─────────────────────────────────────┐
│ 📱 My Devices                       │
│                                     │
│ This device                         │
│ ┌─────────────────────────────────┐ │
│ │ 📱 iPhone 15 Pro          ✓    │ │
│ │ Last active: Just now           │ │
│ │ San Francisco, CA               │ │
│ │ Trusted                         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Other devices                       │
│ ┌─────────────────────────────────┐ │
│ │ 💻 MacBook Pro                  │ │
│ │ Last active: 2 hours ago        │ │
│ │ San Francisco, CA               │ │
│ │ Trusted · [Revoke]              │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🌐 Chrome on Windows            │ │
│ │ Last active: 3 days ago         │ │
│ │ New York, NY                    │ │
│ │ Not trusted · [Revoke]          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Revoke All Other Devices]          │
└─────────────────────────────────────┘
```

---

#### Feature 12: Daily AI Briefing

**Priority:** P3  
**Phase:** 3  
**Effort:** Large

**Description:**
Every morning, users receive a push notification with a personalized summary of what needs their attention across all organizations.

**Requirements:**

| ID     | Requirement                               | Priority |
| ------ | ----------------------------------------- | -------- |
| DB-001 | Push notification at user-configured time | Must     |
| DB-002 | Default time: 7:00 AM local               | Must     |
| DB-003 | Summarizes all orgs in one message        | Must     |
| DB-004 | Includes: pending approvals               | Must     |
| DB-005 | Includes: today's events                  | Must     |
| DB-006 | Includes: urgent notifications            | Must     |
| DB-007 | Includes: weather (optional)              | Could    |
| DB-008 | AI-generated natural language summary     | Must     |
| DB-009 | Tap notification → open dashboard         | Must     |
| DB-010 | Configure which orgs to include           | Should   |
| DB-011 | Configure which item types to include     | Should   |
| DB-012 | Disable briefing entirely                 | Must     |
| DB-013 | "Snooze" option (remind in 1 hour)        | Could    |

**Briefing Content Example:**

```
Good morning, Sarah! ☀️

Today you have:
• HOA vote on pool renovation closes at 5pm
• Quarterly review meeting at 2pm (Acme Corp)
• Kids' dentist appointment at 3:30pm

Action needed:
• Approve Marcus's expense report ($450)
• Sign updated employment agreement

Have a great day! 🚀
```

---

#### Feature 13: Cross-Org Search

**Priority:** P2  
**Phase:** 2  
**Effort:** Large

**Description:**
Users can search across all their organizations at once, finding documents, contacts, messages, and other content regardless of which org it belongs to.

**Requirements:**

| ID     | Requirement                                        | Priority |
| ------ | -------------------------------------------------- | -------- |
| CS-001 | Global search bar in app header                    | Must     |
| CS-002 | Searches all user's organizations                  | Must     |
| CS-003 | Results grouped by organization                    | Should   |
| CS-004 | Results grouped by type (contacts, docs, messages) | Should   |
| CS-005 | Filter by organization                             | Must     |
| CS-006 | Filter by content type                             | Must     |
| CS-007 | Filter by date range                               | Should   |
| CS-008 | Full-text search in documents                      | Must     |
| CS-009 | Search in: contacts, files, messages, events       | Must     |
| CS-010 | Respect per-org permissions                        | Must     |
| CS-011 | Recent searches saved                              | Should   |
| CS-012 | Search suggestions/autocomplete                    | Should   |
| CS-013 | Voice search                                       | Could    |

**Search Results UI:**

```
┌─────────────────────────────────────┐
│ 🔍 "quarterly report"               │
│ ──────────────────────────────────  │
│ Filters: [All Orgs ▼] [All Types ▼] │
│                                     │
│ 📄 Documents (3)                    │
│ ├─ Q3 Quarterly Report.pdf (Work)   │
│ ├─ HOA Quarterly Financials (HOA)   │
│ └─ Family Budget Q3.xlsx (Family)   │
│                                     │
│ 📅 Events (1)                       │
│ └─ Quarterly Review - Nov 15 (Work) │
│                                     │
│ 💬 Messages (2)                     │
│ ├─ "...quarterly report is ready..."│
│ └─ "...review the quarterly..."     │
└─────────────────────────────────────┘
```

---

#### Feature 14: Personal Shortcut Commands

**Priority:** P3  
**Phase:** 3  
**Effort:** Medium

**Description:**
Users can create personal voice/text commands that work across all organizations. For example, "Call Mom" always dials their mother regardless of which org context they're in.

**Requirements:**

| ID     | Requirement                                           | Priority |
| ------ | ----------------------------------------------------- | -------- |
| SC-001 | Create shortcut with trigger phrase                   | Must     |
| SC-002 | Shortcut actions: Call, Message, Open Screen, Web URL | Must     |
| SC-003 | Trigger via voice command                             | Must     |
| SC-004 | Trigger via text in AI chat                           | Must     |
| SC-005 | Trigger via search bar                                | Should   |
| SC-006 | Shortcuts work in any org context                     | Must     |
| SC-007 | Edit/delete shortcuts                                 | Must     |
| SC-008 | Import suggested shortcuts                            | Could    |
| SC-009 | Max 50 shortcuts per user                             | Should   |
| SC-010 | Case-insensitive matching                             | Must     |
| SC-011 | Fuzzy matching ("call mom" = "call mother")           | Could    |

**Shortcut Examples:**

```
"Call Mom" → Call Person: [Mom's Person record]
"Show PTO" → Open Screen: /hr/leave-balance
"Team standup" → Web URL: https://meet.google.com/xyz
"Send report" → Run Command: generate_weekly_report
```

---

#### Feature 15: Data Export / Self-Delete

**Priority:** P2  
**Phase:** 2  
**Effort:** Medium

**Description:**
Users can export all their data in a portable format (GDPR compliance) or permanently delete their account and all associated data (right to erasure).

**Requirements:**

| ID     | Requirement                                    | Priority |
| ------ | ---------------------------------------------- | -------- |
| DE-001 | Export all personal data                       | Must     |
| DE-002 | Export includes: profile, preferences, devices | Must     |
| DE-003 | Export includes: org memberships               | Must     |
| DE-004 | Export includes: communications                | Should   |
| DE-005 | Export includes: files/documents owned         | Should   |
| DE-006 | Export format: JSON + ZIP of files             | Must     |
| DE-007 | Export available for download 24 hours         | Must     |
| DE-008 | Email notification when export ready           | Must     |
| DE-009 | Delete account permanently                     | Must     |
| DE-010 | Delete requires email confirmation code        | Must     |
| DE-011 | Delete removes: User, Person, User Profile     | Must     |
| DE-012 | Delete removes: all org memberships            | Must     |
| DE-013 | Delete revokes Keycloak session                | Must     |
| DE-014 | 7-day grace period before deletion             | Should   |
| DE-015 | Cannot delete if sole org admin                | Must     |

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

#### Feature 16: Emergency Digital Will

**Priority:** P3  
**Phase:** 4  
**Effort:** Large

**Description:**
Users can designate a trusted contact who gains read-only access to their account if they're inactive for a specified period (default 90 days).

**Requirements:**

| ID     | Requirement                                | Priority |
| ------ | ------------------------------------------ | -------- |
| DW-001 | Enable/disable digital will                | Must     |
| DW-002 | Select trusted contact (Person)            | Must     |
| DW-003 | Set inactive days threshold (30-365)       | Must     |
| DW-004 | Warning notification at 50% of threshold   | Must     |
| DW-005 | Warning notification at 75% of threshold   | Must     |
| DW-006 | Trusted contact notified when activated    | Must     |
| DW-007 | Trusted contact gets read-only access      | Must     |
| DW-008 | Configure which orgs to grant access       | Should   |
| DW-009 | Configure which data types to share        | Should   |
| DW-010 | User can deactivate will after activation  | Must     |
| DW-011 | Activity = any login or API call           | Must     |
| DW-012 | Require trusted contact to verify identity | Should   |

**Digital Will Settings:**

```
┌─────────────────────────────────────┐
│ 🔐 Digital Will                     │
│                                     │
│ [=========] ENABLED                 │
│                                     │
│ Trusted Contact:                    │
│ [👤 Jane Doe (Sister)          ▼]  │
│                                     │
│ Activate after inactive for:        │
│ [90 days                       ▼]  │
│                                     │
│ Grant access to:                    │
│ [✓] Personal organization           │
│ [ ] Work organizations              │
│ [✓] Family organizations            │
│                                     │
│ Allow trusted contact to:           │
│ [✓] View contacts                   │
│ [✓] View documents                  │
│ [✓] Download data export            │
│ [ ] Post on my behalf               │
└─────────────────────────────────────┘
```

---

#### Feature 17: Push-to-Approve Logins

**Priority:** P1  
**Phase:** 2  
**Effort:** Large

**Description:**
When a new device attempts to log in, the user receives a push notification on their trusted devices asking to approve or deny the login.

**Requirements:**

| ID     | Requirement                                      | Priority |
| ------ | ------------------------------------------------ | -------- |
| PA-001 | Push notification sent to all trusted devices    | Must     |
| PA-002 | Notification shows: device type, location, time  | Must     |
| PA-003 | "Approve" action completes login on new device   | Must     |
| PA-004 | "Deny" action blocks login + alerts user         | Must     |
| PA-005 | Notification expires after 5 minutes             | Must     |
| PA-006 | If no response, login denied                     | Must     |
| PA-007 | User can disable feature (security tradeoff)     | Should   |
| PA-008 | Fallback to email approval if no trusted devices | Should   |
| PA-009 | Log all approval requests                        | Must     |
| PA-010 | "This was me" option after denial (unblock)      | Should   |

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

---

#### Feature 18: Theme & Language Preference

**Priority:** P1  
**Phase:** 1  
**Effort:** Small

**Description:**
Users set their visual preferences once, and they apply across all Dartwing apps and organizations.

**Requirements:**

| ID     | Requirement                                      | Priority |
| ------ | ------------------------------------------------ | -------- |
| TL-001 | Theme options: Light, Dark, AMOLED Black, System | Must     |
| TL-002 | Theme applies to all Dartwing apps               | Must     |
| TL-003 | Theme syncs across devices                       | Must     |
| TL-004 | Language selection from available languages      | Must     |
| TL-005 | Language applies to all UI text                  | Must     |
| TL-006 | Font size: Small, Medium, Large, Extra Large     | Should   |
| TL-007 | Timezone selection                               | Must     |
| TL-008 | Date format preference                           | Should   |
| TL-009 | Time format: 12-hour / 24-hour                   | Should   |
| TL-010 | Preferences persist on logout/login              | Must     |

---

#### Feature 19: Live Location Share

**Priority:** P3  
**Phase:** 3  
**Effort:** Large

**Description:**
Users can share their real-time location with specific people or organizations for a limited time. Useful for family safety, work check-ins, or emergency situations.

**Requirements:**

| ID     | Requirement                                           | Priority |
| ------ | ----------------------------------------------------- | -------- |
| LS-001 | Share location with specific Person                   | Must     |
| LS-002 | Share location with entire Organization               | Must     |
| LS-003 | Set duration: 1h, 4h, 8h, 24h, Until I stop           | Must     |
| LS-004 | Real-time updates (every 30 seconds)                  | Must     |
| LS-005 | Battery-efficient background tracking                 | Must     |
| LS-006 | Recipient sees location on map                        | Must     |
| LS-007 | Stop sharing anytime                                  | Must     |
| LS-008 | Notification when sharing starts/stops                | Must     |
| LS-009 | Share "last known" location (less battery)            | Should   |
| LS-010 | Emergency share: one tap, notifies emergency contacts | Should   |
| LS-011 | Geofence alerts (notify when entering/leaving area)   | Could    |

**Location Share Flow:**

```
1. User taps "Share My Location" in quick actions
2. Select recipient: Person or Organization
3. Select duration: 1h, 4h, 8h, 24h, Until I stop
4. Confirm → sharing begins
5. Indicator in status bar shows sharing active
6. Recipient receives notification
7. Recipient can view live location on map
8. User can stop sharing anytime
9. Auto-stops when duration expires
```

---

#### Feature 20: Contacts Auto-Match

**Priority:** P3  
**Phase:** 3  
**Effort:** Medium

**Description:**
On first login to the mobile app, users can optionally scan their phone contacts to automatically link existing Person records, instantly connecting them to people they know who already use Dartwing.

**Requirements:**

| ID     | Requirement                                                 | Priority |
| ------ | ----------------------------------------------------------- | -------- |
| CM-001 | Opt-in prompt during onboarding                             | Must     |
| CM-002 | Explain privacy implications clearly                        | Must     |
| CM-003 | Match by phone number (primary)                             | Must     |
| CM-004 | Match by email (secondary)                                  | Must     |
| CM-005 | Show matches for user approval                              | Must     |
| CM-006 | User can skip individual matches                            | Must     |
| CM-007 | User can skip entire feature                                | Must     |
| CM-008 | Contacts never uploaded to server (matching done on device) | Must     |
| CM-009 | Re-run matching from settings                               | Should   |
| CM-010 | Suggest inviting unmatched contacts                         | Could    |

**Matching Flow:**

```
1. Onboarding screen: "Connect with people you know"
2. Explanation: "We'll check if your contacts use Dartwing. Your contacts never leave your device."
3. User taps "Scan Contacts"
4. Permission prompt for contacts access
5. Processing indicator
6. Results screen: "We found 5 matches!"
   - [✓] Mom (matched by phone)
   - [✓] John Smith (matched by email)
   - [✓] Sarah at Work (matched by phone)
   - [  ] Skip this one
   - [✓] Neighbor Bob (matched by phone)
7. User confirms selections
8. Connections created
```

---

## 6. User Stories & Acceptance Criteria

### 6.1 Authentication Stories

**US-001: Magic-Link Login**

```
As a user
I want to log in by clicking a link in my email
So that I don't have to remember a password

Acceptance Criteria:
- Given I enter my registered email
- When I submit the login form
- Then I receive an email within 5 seconds
- And the email contains a "Log In" button
- When I click the button
- Then I am logged into the app
- And I see my dashboard
```

**US-002: Social Login**

```
As a new user
I want to sign up using my Google account
So that I can get started quickly

Acceptance Criteria:
- Given I tap "Continue with Google"
- When I authorize the app in Google
- Then a new account is created with my Google name and email
- And I am logged in
- And I see the onboarding flow
```

**US-003: New Device Approval**

```
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

### 6.2 Organization Stories

**US-004: Join Organization via Invite**

```
As an invitee
I want to join an organization by clicking a link
So that I don't have to manually find and request access

Acceptance Criteria:
- Given I received an invite email from Sarah
- When I click "Join Organization"
- And I already have a Dartwing account
- Then I am added to the organization with the assigned role
- And I see the organization dashboard
- When I don't have an account
- Then I am prompted to create one
- And my name/email are pre-filled from the invite
```

**US-005: Switch Organizations**

```
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
- And the switch completes in under 500ms
```

### 6.3 Privacy Stories

**US-006: Block Contact Globally**

```
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
```

**US-007: Export My Data**

```
As a privacy-conscious user
I want to export all my data
So that I have a portable copy

Acceptance Criteria:
- Given I navigate to Privacy settings
- When I tap "Export My Data"
- Then I see a progress indicator
- And I receive an email when the export is ready
- When I download the export
- Then it contains a JSON file with my profile and settings
- And it contains any documents I own
- And the download link expires after 24 hours
```

**US-008: Delete My Account**

```
As a user
I want to permanently delete my account
So that my data is erased

Acceptance Criteria:
- Given I navigate to Privacy settings
- When I tap "Delete Account"
- Then I see a warning explaining consequences
- When I type "DELETE" and request confirmation
- Then I receive an email with a confirmation code
- When I enter the code
- Then my account enters "pending deletion" state
- And I have 7 days to cancel
- After 7 days
- Then my User, Person, and all org memberships are deleted
- And I cannot log in
```

### 6.4 AI & Personalization Stories

**US-009: Daily Briefing**

```
As a busy professional
I want a morning summary of everything I need to know
So that I can plan my day

Acceptance Criteria:
- Given I have daily briefing enabled at 7:00 AM
- When it becomes 7:00 AM in my timezone
- Then I receive a push notification
- And the notification summarizes:
  - Pending approvals
  - Today's events
  - Urgent items
- When I tap the notification
- Then I see my full dashboard
```

**US-010: Personal Shortcut**

```
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

### 6.5 Emergency Stories

**US-011: Digital Will Activation**

```
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
- And Jane can access my account in read-only mode
- When I log in after activation
- Then Jane's access is revoked
- And I see a notification explaining what happened
```

---

## 7. User Flows

### 7.1 New User Registration Flow

```
┌─────────────────┐
│   App Launch    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Welcome Screen  │
│                 │
│ [Get Started]   │
│ [I have account]│
└────────┬────────┘
         │ Get Started
         ▼
┌─────────────────┐
│ Choose Method   │
│                 │
│ [📧 Email]      │
│ [🔵 Google]     │
│ [📱 Apple]      │
└────────┬────────┘
         │ Email
         ▼
┌─────────────────┐
│ Enter Email     │
│                 │
│ [____________]  │
│ [Send Link]     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Email     │
│                 │
│ 📧 Sent to      │
│ user@email.com  │
│                 │
│ [Open Email App]│
└────────┬────────┘
         │ Tap link in email
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
│ Contacts Match  │
│ (Optional)      │
│                 │
│ [Scan Contacts] │
│ [Skip]          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preferences     │
│                 │
│ Theme [Dark ▼]  │
│ Language [EN ▼] │
│                 │
│ [Finish Setup]  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│   (Empty State) │
│                 │
│ Create or join  │
│ an organization │
└─────────────────┘
```

### 7.2 Invite Acceptance Flow

```
┌─────────────────┐
│ Email Inbox     │
│                 │
│ "Sarah invited  │
│ you to join..." │
└────────┬────────┘
         │ Tap "Join"
         ▼
┌─────────────────┐
│ Deep Link Opens │
│ Dartwing App    │
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │ Account │
    │ Exists? │
    └────┬────┘
    Yes  │  No
    ┌────┴────────────────────┐
    ▼                         ▼
┌──────────────┐      ┌──────────────┐
│ Welcome Back │      │ Create       │
│              │      │ Account      │
│ Join [Org]   │      │              │
│ as [Role]?   │      │ Name: [____] │ ← Pre-filled
│              │      │ Email: [___] │ ← Pre-filled
│ [Confirm]    │      │ Phone: [___] │ ← Pre-filled
└──────┬───────┘      │              │
       │              │ [Create]     │
       │              └──────┬───────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
         ┌───────────────┐
         │ Org Dashboard │
         │               │
         │ "Welcome to   │
         │ [Org Name]!"  │
         └───────────────┘
```

### 7.3 Device Approval Flow

```
┌─────────────────┐        ┌─────────────────┐
│   New Device    │        │  Trusted Device │
│   (Logging in)  │        │  (User's phone) │
└────────┬────────┘        └────────┬────────┘
         │                          │
         │ 1. Enter email           │
         │    Send magic link       │
         │                          │
         │ 2. Click link            │
         │    (in email)            │
         │                          │
         │ 3. Token exchange        │
         │                          │
         │ 4. Push approval needed  │
         │────────────────────────►│
         │                          │
         │                    ┌─────┴─────┐
         │                    │ Push:     │
         │                    │ New login │
         │                    │ request   │
         │                    │           │
         │                    │ [Approve] │
         │                    │ [Deny]    │
         │                    └─────┬─────┘
         │                          │
         │                          │ Approve
         │◄─────────────────────────│
         │                          │
         │ 5. Login completes       │
         │                          │
         ▼                          ▼
┌─────────────────┐        ┌─────────────────┐
│   Dashboard     │        │ "Login approved"│
│   (New device)  │        │ notification    │
└─────────────────┘        └─────────────────┘
```

### 7.4 Cross-Org Search Flow

```
┌─────────────────┐
│ Any Screen      │
│                 │
│ [🔍 Search...]  │
└────────┬────────┘
         │ Tap search
         ▼
┌─────────────────┐
│ Search Screen   │
│                 │
│ [quarterly___]  │ ← User types
│                 │
│ Recent:         │
│ - budget        │
│ - meeting notes │
└────────┬────────┘
         │ Submit
         ▼
┌─────────────────┐
│ Results         │
│                 │
│ Filters:        │
│ [All Orgs ▼]    │
│ [All Types ▼]   │
│                 │
│ 📄 Documents    │
│ ├─ Q3 Report    │
│ │   (Work)      │
│ └─ HOA Budget   │
│     (HOA)       │
│                 │
│ 📅 Events       │
│ └─ Quarterly    │
│     Review      │
│     (Work)      │
└────────┬────────┘
         │ Tap result
         ▼
┌─────────────────┐
│ Document Detail │
│ (in Work org    │
│  context)       │
└─────────────────┘
```

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Metric                     | Target      | Measurement                           |
| -------------------------- | ----------- | ------------------------------------- |
| Magic link delivery        | < 5 seconds | Time from submit to email received    |
| Login completion           | < 3 seconds | Time from link click to dashboard     |
| Org switch                 | < 500ms     | Time from tap to new org loaded       |
| Search results             | < 2 seconds | Time from submit to results displayed |
| Push notification delivery | < 1 second  | Time from trigger to device receipt   |
| App cold start             | < 3 seconds | Time from tap to interactive          |
| App warm start             | < 1 second  | Time from background to foreground    |

### 8.2 Scalability

| Dimension              | Target  | Notes                     |
| ---------------------- | ------- | ------------------------- |
| Concurrent users       | 100,000 | Per Keycloak realm        |
| Organizations per user | 50      | Soft limit, can be raised |
| Devices per user       | 20      | Active devices            |
| Searches per minute    | 10,000  | Across all users          |
| Invites per day        | 50,000  | System-wide               |

### 8.3 Availability

| Metric                         | Target                            |
| ------------------------------ | --------------------------------- |
| Uptime                         | 99.9% (8.76 hours downtime/year)  |
| Keycloak availability          | 99.99% (52 minutes downtime/year) |
| Planned maintenance window     | Sundays 2-4 AM UTC                |
| Recovery Time Objective (RTO)  | 1 hour                            |
| Recovery Point Objective (RPO) | 5 minutes                         |

### 8.4 Security

| Requirement            | Implementation                     |
| ---------------------- | ---------------------------------- |
| Authentication         | OAuth2 + PKCE, no password storage |
| Token encryption       | JWT with RS256 signing             |
| Data at rest           | AES-256 encryption                 |
| Data in transit        | TLS 1.3 minimum                    |
| Session management     | Redis with encryption              |
| Audit logging          | All auth events logged             |
| Brute force protection | 5 attempts, 15-minute lockout      |
| CSRF protection        | State parameter in OAuth flows     |

### 8.5 Compliance

| Standard      | Status          | Notes                          |
| ------------- | --------------- | ------------------------------ |
| GDPR          | Required        | Data export, deletion, consent |
| CCPA          | Required        | Similar to GDPR                |
| SOC 2 Type II | Planned Q3 2026 | For enterprise customers       |
| HIPAA         | Future          | For healthcare orgs            |
| ISO 27001     | Future          | For enterprise credibility     |

### 8.6 Accessibility

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

## 9. Dependencies & Integrations

### 9.1 Internal Dependencies

| Dependency       | Type     | Description                               |
| ---------------- | -------- | ----------------------------------------- |
| Dartwing Core    | Module   | Person, Organization, Org Member doctypes |
| Frappe Framework | Platform | User, Role, Permission infrastructure     |
| Dartwing Comms   | Module   | For notifications, messages (Phase 2+)    |
| Dartwing AI      | Module   | For briefings, voice clone (Phase 3+)     |

### 9.2 External Dependencies

| Service            | Purpose                  | Criticality      |
| ------------------ | ------------------------ | ---------------- |
| Keycloak           | Identity Provider        | Critical         |
| Redis              | Session storage, caching | Critical         |
| MariaDB            | Data persistence         | Critical         |
| SendGrid/SES       | Email delivery           | Critical         |
| Firebase/APNs      | Push notifications       | High             |
| ElevenLabs         | Voice cloning            | Medium (Phase 4) |
| Twilio             | SMS for MFA              | Medium           |
| Google/Apple OAuth | Social login             | Medium           |

### 9.3 Integration Points

```
┌───────────────────────────────────────────────────────────────┐
│                     Dartwing User Module                       │
└───────────────────────────────────────────────────────────────┘
         │              │               │              │
         ▼              ▼               ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Keycloak   │ │   Frappe    │ │   Dartwing  │ │  External   │
│    SSO      │ │   Backend   │ │    Core     │ │  Services   │
│             │ │             │ │             │ │             │
│ - Auth      │ │ - User CRUD │ │ - Person    │ │ - Email     │
│ - Tokens    │ │ - API       │ │ - Org       │ │ - Push      │
│ - Sessions  │ │ - Hooks     │ │ - Member    │ │ - Voice     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 10. Risks & Mitigations

### 10.1 Technical Risks

| Risk                              | Probability | Impact   | Mitigation                             |
| --------------------------------- | ----------- | -------- | -------------------------------------- |
| Keycloak downtime blocks all auth | Low         | Critical | Multi-region deployment, cached tokens |
| Magic link email deliverability   | Medium      | High     | Multiple email providers, monitoring   |
| Cross-org search performance      | Medium      | Medium   | Elasticsearch, query optimization      |
| Voice clone quality               | Medium      | Low      | Beta testing, user feedback            |
| Mobile deep link failures         | Medium      | Medium   | Universal links, fallback web          |

### 10.2 Business Risks

| Risk                         | Probability | Impact | Mitigation                                   |
| ---------------------------- | ----------- | ------ | -------------------------------------------- |
| Low multi-org adoption       | Medium      | High   | Incentivize org creation, invite flows       |
| Privacy concerns deter users | Low         | High   | Transparency, data controls, no selling data |
| Enterprise SSO complexity    | Medium      | Medium | Dedicated integration support                |
| Competitor copies features   | High        | Medium | Execution speed, network effects             |

### 10.3 Compliance Risks

| Risk                      | Probability | Impact   | Mitigation                          |
| ------------------------- | ----------- | -------- | ----------------------------------- |
| GDPR violation            | Low         | Critical | Legal review, automated compliance  |
| Data breach               | Low         | Critical | Encryption, access controls, audits |
| User data request backlog | Medium      | Medium   | Automated export, self-service      |

---

## 11. Release Plan

### 11.1 Phase 1: Foundation (Q1 2026)

**Goal:** Basic authentication and identity management

**Features:**

- Magic-Link Login
- Keycloak SSO
- Social Login (Google, Apple)
- Global Person ↔ User Link
- Basic User Profile
- Device Registration
- Smart Invite Flow
- Multi-Org Switcher
- Theme & Language Preferences

**Success Criteria:**

- 1,000 registered users
- 90% login success rate
- < 5 second magic link delivery
- 50% of users in 2+ orgs

### 11.2 Phase 2: Security & Privacy (Q2 2026)

**Goal:** Enterprise-ready security and user control

**Features:**

- Device Trust & Revoke
- Push-to-Approve Logins
- Enterprise SSO (Azure AD, Okta)
- Global Block List
- Travel Mode
- Unified Personal Dashboard
- Cross-Org Search
- Data Export / Self-Delete

**Success Criteria:**

- 5,000 registered users
- 10 enterprise SSO customers
- 25% of users enable 2+ privacy features
- < 2 second search results

### 11.3 Phase 3: AI & Engagement (Q3 2026)

**Goal:** Personalized experience and daily engagement

**Features:**

- Daily AI Briefing
- Personal Shortcut Commands
- Contacts Auto-Match
- Live Location Share

**Success Criteria:**

- 10,000 registered users
- 35% daily briefing open rate
- 50 shortcuts per 100 users
- 20% of users share location at least once

### 11.4 Phase 4: Advanced Personalization (Q4 2026)

**Goal:** Premium features and long-term retention

**Features:**

- Personal AI Voice Clone
- Digital Will

**Success Criteria:**

- 15,000 registered users
- 10% voice clone adoption
- 5% digital will enabled
- 15% on paid tier

---

## 12. Appendices

### Appendix A: Glossary

| Term           | Definition                                                        |
| -------------- | ----------------------------------------------------------------- |
| Person         | Master identity record in Dartwing Core representing a human      |
| User Profile   | Personal preferences and settings in User module                  |
| Org Member     | Link between Person and Organization with role                    |
| Magic Link     | One-time authentication link sent via email                       |
| PKCE           | Proof Key for Code Exchange, OAuth2 security extension            |
| Trusted Device | Device approved by user for login without additional verification |
| Digital Will   | Emergency access grant to trusted contact after inactivity        |
| Cross-Org      | Features that work across multiple organizations                  |

### Appendix B: API Endpoint Summary

| Endpoint                                   | Method | Purpose              |
| ------------------------------------------ | ------ | -------------------- |
| `dartwing_user.api.get_my_profile`         | GET    | Get user profile     |
| `dartwing_user.api.update_preferences`     | POST   | Update preferences   |
| `dartwing_user.api.toggle_travel_mode`     | POST   | Toggle travel mode   |
| `dartwing_user.api.get_my_devices`         | GET    | List devices         |
| `dartwing_user.api.register_device`        | POST   | Register device      |
| `dartwing_user.api.revoke_device`          | POST   | Revoke device        |
| `dartwing_user.api.approve_device`         | POST   | Approve login        |
| `dartwing_user.api.get_block_list`         | GET    | Get blocked contacts |
| `dartwing_user.api.block_contact`          | POST   | Block contact        |
| `dartwing_user.api.unblock_contact`        | POST   | Unblock contact      |
| `dartwing_user.api.get_user_organizations` | GET    | List orgs            |
| `dartwing_user.api.cross_org_search`       | POST   | Search all orgs      |
| `dartwing_user.api.match_contacts`         | POST   | Match contacts       |
| `dartwing_user.api.send_invite`            | POST   | Send invite          |
| `dartwing_user.api.export_all_data`        | GET    | GDPR export          |
| `dartwing_user.api.delete_account`         | POST   | Delete account       |
| `dartwing_user.api.generate_briefing`      | GET    | Get briefing         |

### Appendix C: Wireframe References

_Note: Detailed wireframes to be created in Figma_

| Screen                   | Description                             | Priority |
| ------------------------ | --------------------------------------- | -------- |
| Login Screen             | Email entry, social buttons, magic link | P0       |
| Magic Link Sent          | Waiting screen with resend              | P0       |
| Onboarding - Profile     | Name, phone entry                       | P0       |
| Onboarding - Contacts    | Contact matching opt-in                 | P3       |
| Onboarding - Preferences | Theme, language selection               | P1       |
| Dashboard                | Unified view of all orgs                | P2       |
| Org Switcher             | Dropdown/modal of organizations         | P1       |
| Settings - Profile       | Edit personal info                      | P0       |
| Settings - Preferences   | Theme, language, briefing               | P1       |
| Settings - Devices       | List with revoke actions                | P1       |
| Settings - Privacy       | Export, delete, blocks                  | P2       |
| Settings - Travel Mode   | Toggle and options                      | P2       |
| Settings - Digital Will  | Trusted contact setup                   | P3       |
| Settings - Voice Clone   | Recording wizard                        | P3       |
| Search                   | Global search with filters              | P2       |
| Invite Flow              | Send invite form                        | P1       |
| Device Approval          | Push notification UI                    | P1       |

### Appendix D: Competitive Analysis

| Feature               | Dartwing | Google | Apple | Okta | Auth0 |
| --------------------- | -------- | ------ | ----- | ---- | ----- |
| Magic-link login      | ✅       | ❌     | ❌    | ✅   | ✅    |
| Multi-org identity    | ✅       | ❌     | ❌    | ⚠️   | ⚠️    |
| Cross-org search      | ✅       | ❌     | ❌    | ❌   | ❌    |
| Personal AI assistant | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Voice clone           | ✅       | ❌     | ❌    | ❌   | ❌    |
| Digital will          | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Travel mode           | ✅       | ❌     | ❌    | ❌   | ❌    |
| Global block list     | ✅       | ⚠️     | ⚠️    | ❌   | ❌    |
| Privacy controls      | ✅       | ⚠️     | ✅    | ⚠️   | ⚠️    |
| Enterprise SSO        | ✅       | ✅     | ⚠️    | ✅   | ✅    |

✅ = Full support | ⚠️ = Partial/limited | ❌ = Not available

### Appendix E: Success Metrics Dashboard

**Acquisition Metrics:**

- New registrations (daily, weekly, monthly)
- Registration method breakdown (email, Google, Apple)
- Invite acceptance rate
- Time to first org join

**Activation Metrics:**

- Profile completion rate
- Preferences configured
- Second org joined
- First cross-org search

**Engagement Metrics:**

- DAU / WAU / MAU
- Org switches per session
- Daily briefing opens
- Shortcuts created
- Searches performed

**Retention Metrics:**

- D1 / D7 / D30 retention
- Churn rate
- Feature adoption over time
- NPS score

**Revenue Metrics (Future):**

- Premium conversion rate
- Enterprise contract value
- Voice clone upsell rate

---

## Document History

| Version | Date          | Author         | Changes     |
| ------- | ------------- | -------------- | ----------- |
| 1.0     | November 2025 | Claude + Brett | Initial PRD |

---

_End of Document_
