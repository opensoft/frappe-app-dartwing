# Dartwing User Module - Executive Summary

**Version:** 1.0
**Date:** November 29, 2025

---

## 1. Product Vision

**Dartwing User** provides a **unified personal identity layer** that enables individuals to seamlessly navigate across all their organizations—families, companies, nonprofits, clubs, and associations—with a single login and personalized experience.

**Tagline:** _"Your Identity, Your Control, Everywhere."_

### Value Proposition

| For                     | Pain Point                                      | Solution                                 |
| ----------------------- | ----------------------------------------------- | ---------------------------------------- |
| **End Users**           | Fragmented identity across 100+ accounts        | One login, one identity everywhere       |
| **Privacy-Conscious**   | No control over personal data                   | Travel mode, duress PIN, personal vault  |
| **Traveling Professionals** | Border search risks, device coercion       | Data hiding, decoy accounts, trusted devices |
| **Elderly Users**       | Password fatigue, tech intimidation             | Magic-link, biometric, family assistance |
| **Org Administrators**  | Slow onboarding, security gaps                  | Smart invites, instant access revocation |

---

## 2. Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING USER MODULE                               │
│                        Personal Identity Layer                               │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                        USER PROFILE (1:1 with Person)                │  │
│   │  theme, language, timezone, travel_mode, duress_pin, privacy_score  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│   │  Devices   │ │   Blocks   │ │  Shortcuts │ │  Sessions  │              │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘              │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│   │ AI Voice   │ │Digital Will│ │ Location   │ │ Vault      │              │
│   │ Profile    │ │            │ │ Share      │ │ Items      │              │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘              │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│   │ Verification│ │ Privacy   │ │ AI Memory  │ │ Reputation │              │
│   │ Record     │ │ Settings  │ │ Entries    │ │ Score      │              │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘              │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │ Extends
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING CORE MODULE                               │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    Person (Master Identity Record)                   │  │
│   │   keycloak_user_id, primary_email, frappe_user, full_name           │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    Organization (Polymorphic Shell)                  │  │
│   │   org_type: Family | Company | Nonprofit | Club                     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ Authenticates via
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              KEYCLOAK                                        │
│                                                                              │
│   SSO, OAuth2/OIDC, Magic-Link, Social Login, MFA, Passkeys                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Principle: "One Human = One Identity"

Every human has exactly ONE permanent identity chain:

- **Keycloak User** → authentication
- **Frappe User** → authorization
- **Person** (Core) → master identity
- **User Profile** (User Module) → personal preferences

These are permanently linked and never duplicated across organizations.

---

## 3. Feature Summary

### Identity & Preferences (9 Features)

| ID   | Feature                      | Description                                    | AI-Powered |
| ---- | ---------------------------- | ---------------------------------------------- | :--------: |
| U-01 | **User Profile**             | Personal settings that follow you everywhere   |            |
| U-02 | **Multi-Org Switcher**       | Quick-switch between all organizations         |            |
| U-14 | **Emergency Contacts**       | ICE contacts accessible across all contexts    |            |
| U-15 | **Notification Preferences** | Per-org, per-channel notification control      |            |
| U-21 | **Contact Auto-Match**       | Automatic contact merging across orgs          |     ✓      |
| U-22 | **Smart Invitations**        | Pre-filled, role-specific org invites          |            |
| U-26 | **Achievements**             | Gamification badges and milestones             |            |
| U-27 | **Reputation Score**         | Cross-org trust metric based on behavior       |     ✓      |
| U-28 | **Personal AI Memory**       | AI remembers preferences and context           |     ✓      |

### Security & Privacy (9 Features)

| ID   | Feature                | Description                                    | AI-Powered |
| ---- | ---------------------- | ---------------------------------------------- | :--------: |
| U-03 | **Device Trust**       | Trust scoring with behavioral analysis         |     ✓      |
| U-04 | **Global Block List**  | Block users across all organizations           |            |
| U-06 | **Travel Mode**        | One-tap data hiding for border crossings       |            |
| U-07 | **Push-to-Approve**    | Approve new device logins from trusted device  |            |
| U-16 | **Privacy Dashboard**  | Full visibility into data access and sharing   |            |
| U-17 | **Data Export**        | GDPR-compliant data portability                |            |
| U-18 | **Account Deletion**   | Complete data erasure with cascade             |            |
| U-23 | **Biometric Unlock**   | Face ID / Touch ID / Fingerprint               |            |
| U-24 | **Passkey Support**    | Passwordless FIDO2/WebAuthn                    |            |

### AI & Personalization (4 Features)

| ID   | Feature               | Description                                    | AI-Powered |
| ---- | --------------------- | ---------------------------------------------- | :--------: |
| U-05 | **Personal Shortcuts** | Custom commands and quick actions              |     ✓      |
| U-09 | **AI Voice Profile**  | Voice clone for AI assistant interactions      |     ✓      |
| U-10 | **Daily AI Briefing** | Personalized morning summary across all orgs   |     ✓      |
| U-19 | **Cross-Org Search**  | Unified search across all organizations        |     ✓      |

### Emergency & Succession (4 Features)

| ID   | Feature                | Description                                    | AI-Powered |
| ---- | ---------------------- | ---------------------------------------------- | :--------: |
| U-08 | **Digital Will**       | Succession planning for digital assets         |            |
| U-11 | **Location Sharing**   | Live location with trusted contacts            |            |
| U-13 | **Personal Vault**     | End-to-end encrypted document storage          |            |
| U-25 | **Session Management** | View/revoke all active sessions                |            |

### Health & Wearables (2 Features)

| ID   | Feature                   | Description                                 | AI-Powered |
| ---- | ------------------------- | ------------------------------------------- | :--------: |
| U-29 | **Health Data**           | Sync health records with proper consent     |     ✓      |
| U-30 | **Wearable Device Sync**  | Apple Watch, Fitbit, Garmin integration     |            |

---

## 4. Security Architecture

### Defense in Depth (5 Layers)

```
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Travel Mode + Duress PIN (coercion protection) │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Push-to-Approve (new device verification)      │
├─────────────────────────────────────────────────────────┤
│ Layer 3: Device Trust Scoring (behavioral analysis)     │
├─────────────────────────────────────────────────────────┤
│ Layer 2: Biometric / Passkey (device-level auth)        │
├─────────────────────────────────────────────────────────┤
│ Layer 1: Keycloak SSO + MFA (identity verification)     │
└─────────────────────────────────────────────────────────┘
```

### Key Management System

- **Argon2id KDF** for password-derived keys
- **Envelope encryption** (KEK → MEK → DEK hierarchy)
- **Shamir's Secret Sharing** for recovery
- **Zero-knowledge architecture** - server never sees plaintext secrets

### Travel Mode Framework

| Sensitivity Level | Data Types                          | Travel Mode Behavior |
| ----------------- | ----------------------------------- | -------------------- |
| Level 0 (Public)  | Profile, public posts               | Always visible       |
| Level 1 (Personal)| Preferences, contacts               | Visible              |
| Level 2 (Business)| Work docs, org communications       | Hidden by default    |
| Level 3 (Medical) | Health records, prescriptions       | Always hidden        |
| Level 4 (Financial)| Bank accounts, investments         | Always hidden        |
| Level 5 (Vault)   | Personal vault items                | Always hidden        |

---

## 5. Integration Points

### Core Module Integration

| Core DocType    | How We Use It                                    |
| --------------- | ------------------------------------------------ |
| **Person**      | User Profile links 1:1, extends with preferences |
| **Organization**| Multi-org switcher, privacy settings per-org     |
| **Org Member**  | Role display, cross-org search permissions       |

### External Integrations

| Service        | Purpose                                          |
| -------------- | ------------------------------------------------ |
| **Keycloak**   | Authentication, SSO, MFA, magic-link             |
| **ElevenLabs** | Voice cloning for AI Voice Profile               |
| **Veriff/Onfido** | Identity verification                         |
| **FCM/APNS**   | Push notifications, push-to-approve              |
| **Apple Health/Google Fit** | Health data sync                    |
| **AWS KMS**    | Key management for vault encryption              |

---

## 6. Key Differentiators

### 1. Personal vs. Organizational Separation

| User Module (Personal)   | Core/Org Modules (Organizational) |
| ------------------------ | --------------------------------- |
| AI voice clone           | Company phone scripts             |
| Theme preference         | Company branding                  |
| Global block list        | Org contact blacklist             |
| Digital will             | Org succession planning           |
| Travel mode              | Org leave requests                |
| Device trust             | Org device management             |
| Personal vault           | Org document storage              |

### 2. Cross-Org by Design

All features work across ALL organizations:
- Single search queries all orgs
- One block list applies everywhere
- Preferences sync to every context
- AI remembers you across all roles

### 3. Privacy-First Architecture

- Travel mode hides sensitive data on demand
- Duress PIN shows decoy data under coercion
- Zero-knowledge vault encryption
- GDPR/CCPA compliance built-in
- Right to erasure is automatic and complete

### 4. AI Personalization

- Voice clone for natural interactions
- Cross-org briefing each morning
- AI memory persists context
- Smart contact matching and deduplication

---

## 7. Technical Summary

### Technology Stack

| Component      | Technology                          |
| -------------- | ----------------------------------- |
| Framework      | Frappe 16.x                         |
| Database       | MariaDB 10.11+                      |
| Cache/Queue    | Redis 7.x                           |
| Mobile         | Flutter (Dartwing Flutter)          |
| Authentication | Keycloak 24.x                       |
| Encryption     | Argon2id, AES-256-GCM, Shamir's SS  |
| AI/LLM         | OpenAI / Claude API                 |
| Voice Clone    | ElevenLabs API                      |

### New DocTypes (18)

| Category        | DocTypes                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------- |
| Identity        | User Profile, User Device, User Session, User Block, User Invite                          |
| AI Features     | AI Voice Profile, AI Memory Entry, User Shortcut                                          |
| Security        | Personal Vault Item, Privacy Setting, Verification Record, User Key Material              |
| Emergency       | Digital Will, Digital Will Trustee, Emergency Contact, User Location Share                |
| Metrics         | Reputation Score, Notification Preference                                                 |

### API Surface

| Category        | Endpoints                                                                    |
| --------------- | ---------------------------------------------------------------------------- |
| Profile         | `GET/PUT /api/user/profile`, `POST /api/user/avatar`                         |
| Devices         | `GET/DELETE /api/user/devices`, `POST /api/user/devices/trust`               |
| Security        | `POST /api/user/travel-mode`, `POST /api/user/sessions/revoke`               |
| Privacy         | `GET /api/user/privacy/dashboard`, `POST /api/user/data/export`              |
| AI              | `GET/PUT /api/user/ai/voice`, `GET /api/user/ai/briefing`                    |
| Cross-Org       | `GET /api/user/organizations`, `GET /api/user/search`                        |

---

## 8. Implementation Roadmap

| Phase               | Timeline     | Focus                         | Key Deliverables                                             |
| ------------------- | ------------ | ----------------------------- | ------------------------------------------------------------ |
| **1: Foundation**   | Months 1-3   | Core identity & security      | User Profile, Devices, Sessions, Biometric, Invitations      |
| **2: Privacy**      | Months 4-6   | Privacy & data control        | Travel Mode, Privacy Dashboard, Export/Delete, Vault         |
| **3: AI & Cross-Org** | Months 7-9 | Intelligence & integration    | AI Briefing, Voice Clone, Cross-Org Search, Memory           |
| **4: Advanced**     | Months 10-12 | Emergency & premium           | Digital Will, Location Sharing, Health Integration           |

### Success Metrics

| Metric               | Year 1 Target |
| -------------------- | ------------- |
| Active Users         | 10,000        |
| Multi-Org Users      | 60%           |
| Premium Conversion   | 15%           |
| Push-Approve Enabled | 60%           |
| Profile Completion   | 80%           |

---

## 9. Target Users

| Persona                     | Key Features                        | Example Use Case                     |
| --------------------------- | ----------------------------------- | ------------------------------------ |
| **Multi-Context Professional** | Org switcher, AI briefing, shortcuts | Marketing director managing work + family + HOA |
| **Privacy-Conscious User**  | Vault, data export, travel mode     | Engineer who demands data control    |
| **Traveling Professional**  | Travel mode, duress PIN, push-approve | Sales consultant crossing borders   |
| **Elderly Family Member**   | Magic-link, biometric, large text   | Grandfather joining family org       |
| **Organization Admin**      | Smart invites, session management   | HR director onboarding employees     |

---

## 10. Competitive Advantage

| Competitor Type       | Their Approach                          | Our Advantage                        |
| --------------------- | --------------------------------------- | ------------------------------------ |
| **Consumer Identity** | Social login (gives Big Tech more data) | Privacy-first, user-owned identity   |
| **Enterprise SSO**    | Work-only, no personal features         | Cross-org personal + work identity   |
| **Password Managers** | Store passwords, no identity            | Full identity with preferences + AI  |
| **Privacy Tools**     | Defensive only                          | Proactive features + usability       |

---

## 11. Summary

**Dartwing User** transforms personal digital identity by:

1. **Unifying** identity across all life contexts (work, family, community)
2. **Protecting** privacy with travel mode, duress PIN, and zero-knowledge vault
3. **Empowering** users with AI that understands all their contexts
4. **Enabling** seamless cross-org collaboration without security compromises
5. **Providing** complete data sovereignty with export, delete, and transparency

**The result:** Users own their identity, control their privacy, and experience a seamless digital life across all organizations.

---

**Related Documents:**

- [Full PRD](dartwing_user_prd.md) - 2,500+ lines
- [Full Architecture](dartwing_user_arch.md) - 7,300+ lines
