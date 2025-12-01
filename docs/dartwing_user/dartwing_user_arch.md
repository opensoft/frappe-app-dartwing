# Dartwing User Module Architecture

**Version 2.0 | November 2025**

_Personal Identity Layer for the Dartwing Platform_

---

## Table of Contents

1. Overview & Design Principles
2. Relationship to Core & Auth Modules
3. Data Model & Doctypes
4. Service Layer Architecture
5. API Design & Endpoints
6. Flutter Client Architecture
7. Security & Privacy Architecture
8. External Service Integrations
9. Background Jobs & Scheduled Tasks
10. Implementation Patterns
11. Migration & Deployment
12. Appendices

**Architecture Hardening (November 2025 - Post-Critique):**

13. Key Management System
14. Travel Mode Enforcement Framework
15. Provider Abstraction & Error Handling

**Spec-Kit Ready Sections (December 2025):**

20. Feature Implementation Status
21. Notification Delivery Requirements
22. AI Voice Storage Requirements
23. User Audit Trail Requirements
24. Permission Registration Requirements

---

## 1. Overview & Design Principles

### 1.1 Module Purpose

The **Dartwing User Module** (`dartwing_user`) provides the personal identity layer that sits atop Dartwing Core. While Core manages universal constructs (Organization, Person, Org Member), the User module handles everything **personal** and **cross-organizational**:

- Personal preferences that follow the user everywhere
- Device trust and session management
- Privacy controls and data sovereignty
- AI personalization (voice clone, briefing, memory)
- Emergency features (digital will, location sharing)
- Identity verification and reputation

### 1.2 Module Boundaries

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING USER MODULE                               │
│                                                                              │
│   Personal identity, cross-org features, preferences, privacy, AI           │
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
│   ┌────────────┐ ┌────────────┐ ┌────────────┐                             │
│   │ Emergency  │ │ Notification│ │ Invitations│                             │
│   │ Contacts   │ │ Prefs      │ │            │                             │
│   └────────────┘ └────────────┘ └────────────┘                             │
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
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐              │
│   │   Org Member   │  │ Role Template  │  │   Equipment    │              │
│   └────────────────┘  └────────────────┘  └────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ Authenticates via
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              KEYCLOAK                                        │
│                                                                              │
│   SSO, OAuth2/OIDC, Magic-Link, Social Login, MFA, Passkeys                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Design Principles

#### Principle 1: One Human = One Identity

Every human has exactly ONE permanent identity chain:

```
Keycloak User (authentication)
      │
      │ keycloak_user_id
      ▼
Person (Core - master identity)
      │
      │ 1:1 link
      ▼
User Profile (User Module - preferences)
```

These records are created atomically and never duplicated.

#### Principle 2: Personal ≠ Organizational

User module features belong to the **human**, not any organization:

| User Module (Personal) | Core/Org Modules (Organizational) |
| ---------------------- | --------------------------------- |
| AI voice clone         | Company phone scripts             |
| Theme preference       | Company branding                  |
| Global block list      | Org contact blacklist             |
| Digital will           | Org succession planning           |
| Travel mode            | Org leave requests                |
| Device trust           | Org device management             |
| Personal vault         | Org document storage              |

#### Principle 3: Cross-Org by Design

All User module features work across ALL organizations the person belongs to:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Family    │     │   Company    │     │     HOA      │
│  (org_type:  │     │  (org_type:  │     │  (org_type:  │
│   Family)    │     │   Company)   │     │    Club)     │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │    Org Member      │     Org Member     │
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Person     │
                    │  (Core)       │
                    └───────┬───────┘
                            │ 1:1
                            ▼
                    ┌───────────────┐
                    │  User Profile │
                    │  (User Module)│
                    │               │
                    │ • Theme       │
                    │ • Shortcuts   │
                    │ • Block List  │
                    │ • AI Voice    │
                    │ • etc.        │
                    └───────────────┘
```

#### Principle 4: Privacy-First

- Personal data is NEVER exposed to organizations without explicit consent
- Users control exactly what each org can see via Privacy Settings
- GDPR/CCPA compliance is built into every data operation
- Right to erasure is automatic and complete

#### Principle 5: Defense in Depth

Security features layer on each other:

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

---

## 2. Relationship to Core & Auth Modules

### 2.1 Module Dependency Chain

```
dartwing_user
    ├── depends on: dartwing_core
    │                   └── depends on: frappe
    └── integrates with: Keycloak (via dartwing_auth hooks)
```

### 2.2 Doctype Ownership Matrix

| Doctype                     | Owner Module      | Purpose               | Links To                   |
| --------------------------- | ----------------- | --------------------- | -------------------------- |
| Person                      | dartwing_core     | Master identity       | Keycloak User, Frappe User |
| Organization                | dartwing_core     | Polymorphic org shell | Concrete types             |
| Org Member                  | dartwing_core     | Person ↔ Org link     | Person, Organization       |
| **User Profile**            | **dartwing_user** | Personal preferences  | Person (1:1)               |
| **User Device**             | **dartwing_user** | Trusted devices       | Person                     |
| **User Session**            | **dartwing_user** | Active sessions       | Person, User Device        |
| **User Block**              | **dartwing_user** | Global block list     | Person (owner)             |
| **User Shortcut**           | **dartwing_user** | Personal commands     | User Profile (child)       |
| **User Location Share**     | **dartwing_user** | Live location         | Person                     |
| **AI Voice Profile**        | **dartwing_user** | Voice clone           | Person (1:1)               |
| **Digital Will**            | **dartwing_user** | Succession            | Person (1:1)               |
| **Digital Will Trustee**    | **dartwing_user** | Trusted contacts      | Digital Will (child)       |
| **Personal Vault Item**     | **dartwing_user** | Encrypted storage     | Person                     |
| **Emergency Contact**       | **dartwing_user** | ICE contacts          | User Profile (child)       |
| **Verification Record**     | **dartwing_user** | ID verification       | Person (1:1)               |
| **Privacy Setting**         | **dartwing_user** | Per-org permissions   | Person, Organization       |
| **AI Memory Entry**         | **dartwing_user** | AI context            | Person                     |
| **Reputation Score**        | **dartwing_user** | Trust metric          | Person (1:1)               |
| **Notification Preference** | **dartwing_user** | Per-org notifications | Person, Organization       |
| **User Invite**             | **dartwing_user** | Pending invitations   | Person, Organization       |

### 2.3 Identity Chain Implementation

The User module extends the Core identity chain:

```python
# Core module establishes: Keycloak → Frappe User → Person
# User module adds: Person → User Profile

# dartwing_user/hooks.py
doc_events = {
    "Person": {
        "after_insert": "dartwing_user.events.person.create_user_profile",
    }
}

# dartwing_user/events/person.py
def create_user_profile(doc, method):
    """
    Automatically create User Profile when Person is created.
    Maintains 1:1 relationship.
    """
    if not frappe.db.exists("User Profile", {"person": doc.name}):
        profile = frappe.get_doc({
            "doctype": "User Profile",
            "person": doc.name,
            "theme": "system",  # Default to system theme
            "language": frappe.local.lang or "en",
            "timezone": "UTC",
            "travel_mode": 0,
            "privacy_score": 50,  # Starting score
        })
        profile.insert(ignore_permissions=True)
        frappe.db.commit()
```

### 2.4 Authentication Integration Points

The User module hooks into Keycloak authentication events:

```python
# dartwing_user/auth_hooks.py

def on_login_success(user, token_data):
    """
    Called after successful Keycloak authentication.
    Registered via keycloak_callback_hooks in hooks.py
    """
    person = get_person_for_frappe_user(user)
    if not person:
        return

    # Register/update device
    device_info = extract_device_info(frappe.request)
    register_or_update_device(person, device_info)

    # Check if push-to-approve needed
    device = get_device_for_request(person)
    if device and not device.is_trusted:
        if requires_push_approval(person):
            raise PushApprovalRequired(device.name)

    # Update session tracking
    create_user_session(person, device, token_data)

    # Check travel mode
    profile = get_user_profile(person)
    if profile.travel_mode:
        apply_travel_mode_filters()

def on_logout(user):
    """Called on logout to clean up session."""
    person = get_person_for_frappe_user(user)
    if person:
        end_user_session(person, frappe.request)
```

---

## 3. Data Model & Doctypes

### 3.1 Complete Data Model Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER MODULE DATA MODEL                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Person (from Core Module)                         │   │
│  │  name: P-XXXXX | keycloak_user_id | primary_email | frappe_user     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      │ 1:1 (person field)                   │
│                                      ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         User Profile                                 │   │
│  │  name: UP-XXXXX                                                      │   │
│  │  person (Link) ────────────────────────────────────────────────────► │   │
│  │                                                                      │   │
│  │  PREFERENCES                    SECURITY                            │   │
│  │  ─────────────                  ────────                            │   │
│  │  theme: Select                  travel_mode: Check                  │   │
│  │  accent_color: Color            duress_pin: Password                │   │
│  │  language: Link                 push_approval_required: Check       │   │
│  │  timezone: Select               biometric_enabled: Check            │   │
│  │  date_format: Select            last_activity: Datetime             │   │
│  │  time_format: Select                                                │   │
│  │                                 METRICS                             │   │
│  │  ACCESSIBILITY                  ───────                             │   │
│  │  ─────────────                  privacy_score: Int                  │   │
│  │  font_size: Select              profile_completion: Percent         │   │
│  │  high_contrast: Check                                               │   │
│  │  reduce_motion: Check           CHILD TABLES                        │   │
│  │                                 ────────────                        │   │
│  │                                 shortcuts: Table → User Shortcut    │   │
│  │                                 emergency_contacts: Table → Emergency Contact │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│         ┌────────────────────────────┼────────────────────────────┐        │
│         │                            │                            │        │
│         ▼                            ▼                            ▼        │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐    │
│  │   User Device   │      │   User Session  │      │    User Block   │    │
│  │                 │      │                 │      │                 │    │
│  │ person ─────────┼──────┼─► Person        │      │ owner ──────────┼──► │
│  │ device_id       │      │ device ─────────┼──►   │ block_type      │    │
│  │ device_name     │      │ token_hash      │      │ blocked_person  │    │
│  │ device_type     │      │ ip_address      │      │ blocked_phone   │    │
│  │ os_name         │      │ location_city   │      │ blocked_email   │    │
│  │ os_version      │      │ started_at      │      │ reason          │    │
│  │ is_trusted      │      │ expires_at      │      │ created_at      │    │
│  │ trust_score     │      │ is_active       │      │                 │    │
│  │ last_active     │      │                 │      │                 │    │
│  │ last_location   │      │                 │      │                 │    │
│  │ approval_status │      │                 │      │                 │    │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘    │
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐    │
│  │ AI Voice Profile│      │   Digital Will  │      │User Location    │    │
│  │                 │      │                 │      │Share            │    │
│  │ person ─────────┼──►   │ person ─────────┼──►   │                 │    │
│  │ voice_model_id  │      │ inactive_days   │      │ person ─────────┼──► │
│  │ voice_sample    │      │ status          │      │ shared_with_person   │
│  │ personality     │      │ activated_at    │      │ shared_with_org │    │
│  │ training_status │      │ last_warning    │      │ latitude        │    │
│  │ watermark_key   │      │                 │      │ longitude       │    │
│  │ permissions     │      │ trustees: Table │      │ accuracy        │    │
│  │ usage_count     │      │ → Digital Will  │      │ expires_at      │    │
│  │                 │      │   Trustee       │      │ is_active       │    │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘    │
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐    │
│  │Personal Vault   │      │ Verification    │      │ Privacy Setting │    │
│  │Item             │      │ Record          │      │                 │    │
│  │                 │      │                 │      │                 │    │
│  │ person ─────────┼──►   │ person ─────────┼──►   │ person ─────────┼──► │
│  │ file            │      │ level           │      │ organization ───┼──► │
│  │ category        │      │ provider        │      │ data_type       │    │
│  │ folder          │      │ document_type   │      │ is_allowed      │    │
│  │ encryption_key  │      │ verified_at     │      │ updated_at      │    │
│  │ is_favorite     │      │ expires_at      │      │                 │    │
│  │ offline_enabled │      │ document_data   │      │                 │    │
│  │ shared_until    │      │                 │      │                 │    │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘    │
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐    │
│  │ AI Memory Entry │      │ Reputation Score│      │ Notification    │    │
│  │                 │      │                 │      │ Preference      │    │
│  │ person ─────────┼──►   │ person ─────────┼──►   │                 │    │
│  │ context_type    │      │ overall_score   │      │ person ─────────┼──► │
│  │ category        │      │ identity_score  │      │ organization ───┼──► │
│  │ memory_text     │      │ payment_score   │      │ channel         │    │
│  │ confidence      │      │ feedback_score  │      │ event_type      │    │
│  │ source          │      │ activity_score  │      │ is_enabled      │    │
│  │ expires_at      │      │ updated_at      │      │ quiet_hours     │    │
│  │ is_user_visible │      │                 │      │ digest_frequency│    │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘    │
│                                                                              │
│  ┌─────────────────┐                                                        │
│  │   User Invite   │                                                        │
│  │                 │                                                        │
│  │ email           │                                                        │
│  │ organization ───┼──► Organization                                        │
│  │ inviter ────────┼──► Person                                              │
│  │ role_template   │                                                        │
│  │ invite_token    │                                                        │
│  │ pre_filled_data │                                                        │
│  │ status          │                                                        │
│  │ expires_at      │                                                        │
│  │ accepted_at     │                                                        │
│  │ accepted_by ────┼──► Person (when accepted)                              │
│  └─────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Core Doctypes - JSON Definitions

#### User Profile (Master - 1:1 with Person)

```json
{
  "doctype": "User Profile",
  "module": "Dartwing User",
  "autoname": "naming_series:",
  "naming_series": "UP-.#####",
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1,
      "in_standard_filter": 1
    },
    {
      "fieldname": "section_appearance",
      "label": "Appearance",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "theme",
      "label": "Theme",
      "fieldtype": "Select",
      "options": "light\ndark\namoled\nsystem",
      "default": "system"
    },
    {
      "fieldname": "accent_color",
      "label": "Accent Color",
      "fieldtype": "Color",
      "default": "#4F46E5"
    },
    {
      "fieldname": "column_break_appearance",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "font_size",
      "label": "Font Size",
      "fieldtype": "Select",
      "options": "small\nmedium\nlarge\nextra_large",
      "default": "medium"
    },
    {
      "fieldname": "high_contrast",
      "label": "High Contrast Mode",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "reduce_motion",
      "label": "Reduce Motion",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_localization",
      "label": "Localization",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "language",
      "label": "Language",
      "fieldtype": "Link",
      "options": "Language",
      "default": "en"
    },
    {
      "fieldname": "timezone",
      "label": "Timezone",
      "fieldtype": "Select",
      "options": "",
      "default": "UTC"
    },
    {
      "fieldname": "column_break_localization",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "date_format",
      "label": "Date Format",
      "fieldtype": "Select",
      "options": "MM/DD/YYYY\nDD/MM/YYYY\nYYYY-MM-DD",
      "default": "MM/DD/YYYY"
    },
    {
      "fieldname": "time_format",
      "label": "Time Format",
      "fieldtype": "Select",
      "options": "12-hour\n24-hour",
      "default": "12-hour"
    },
    {
      "fieldname": "section_security",
      "label": "Security",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "travel_mode",
      "label": "Travel Mode Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "travel_mode_activated_at",
      "label": "Travel Mode Activated At",
      "fieldtype": "Datetime",
      "read_only": 1,
      "depends_on": "eval:doc.travel_mode"
    },
    {
      "fieldname": "travel_mode_auto_disable_days",
      "label": "Auto-Disable After (Days)",
      "fieldtype": "Int",
      "default": 7,
      "depends_on": "eval:doc.travel_mode"
    },
    {
      "fieldname": "column_break_security",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "duress_pin_hash",
      "label": "Duress PIN (Hashed)",
      "fieldtype": "Password",
      "hidden": 1
    },
    {
      "fieldname": "push_approval_required",
      "label": "Require Push Approval for New Devices",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "biometric_enabled",
      "label": "Biometric Unlock Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_data_hiding",
      "label": "Travel Mode - Hidden Data Types",
      "fieldtype": "Section Break",
      "depends_on": "eval:doc.travel_mode",
      "collapsible": 1
    },
    {
      "fieldname": "hide_financial",
      "label": "Hide Financial Data",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "hide_medical",
      "label": "Hide Medical Records",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "hide_business",
      "label": "Hide Business Documents",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_metrics",
      "label": "Metrics",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "privacy_score",
      "label": "Privacy Score",
      "fieldtype": "Int",
      "default": 50,
      "read_only": 1,
      "description": "0-100 score based on enabled privacy features"
    },
    {
      "fieldname": "profile_completion",
      "label": "Profile Completion",
      "fieldtype": "Percent",
      "default": 0,
      "read_only": 1
    },
    {
      "fieldname": "column_break_metrics",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "last_activity",
      "label": "Last Activity",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_shortcuts",
      "label": "Personal Shortcuts",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "shortcuts",
      "label": "Shortcuts",
      "fieldtype": "Table",
      "options": "User Shortcut"
    },
    {
      "fieldname": "section_emergency",
      "label": "Emergency Contacts",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "emergency_contacts",
      "label": "Emergency Contacts",
      "fieldtype": "Table",
      "options": "Emergency Contact"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 0,
      "delete": 0
    }
  ]
}
```

#### User Device

```json
{
  "doctype": "User Device",
  "module": "Dartwing User",
  "autoname": "hash",
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "device_id",
      "label": "Device ID",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "device_name",
      "label": "Device Name",
      "fieldtype": "Data",
      "in_list_view": 1
    },
    {
      "fieldname": "device_type",
      "label": "Device Type",
      "fieldtype": "Select",
      "options": "mobile_ios\nmobile_android\nweb\ndesktop_macos\ndesktop_windows\ndesktop_linux",
      "in_list_view": 1
    },
    {
      "fieldname": "column_break_device",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "os_name",
      "label": "OS Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "os_version",
      "label": "OS Version",
      "fieldtype": "Data"
    },
    {
      "fieldname": "app_version",
      "label": "App Version",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_trust",
      "label": "Trust Status",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "is_trusted",
      "label": "Is Trusted",
      "fieldtype": "Check",
      "default": 0,
      "in_list_view": 1
    },
    {
      "fieldname": "trust_score",
      "label": "Trust Score",
      "fieldtype": "Int",
      "default": 50,
      "description": "0-100 calculated trust score"
    },
    {
      "fieldname": "approval_status",
      "label": "Approval Status",
      "fieldtype": "Select",
      "options": "pending\napproved\ndenied\nrevoked",
      "default": "pending"
    },
    {
      "fieldname": "column_break_trust",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "trusted_at",
      "label": "Trusted At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "revoked_at",
      "label": "Revoked At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "revoke_reason",
      "label": "Revoke Reason",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "section_activity",
      "label": "Activity",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "first_seen",
      "label": "First Seen",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "last_active",
      "label": "Last Active",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "last_ip",
      "label": "Last IP Address",
      "fieldtype": "Data"
    },
    {
      "fieldname": "column_break_activity",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "last_location_city",
      "label": "Last Location (City)",
      "fieldtype": "Data"
    },
    {
      "fieldname": "last_location_country",
      "label": "Last Location (Country)",
      "fieldtype": "Data"
    },
    {
      "fieldname": "login_count",
      "label": "Login Count",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "failed_login_count",
      "label": "Failed Login Count",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "section_trust_factors",
      "label": "Trust Score Factors",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "factor_device_age",
      "label": "Device Age Score (20%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "factor_login_frequency",
      "label": "Login Frequency Score (15%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "factor_location_consistency",
      "label": "Location Consistency Score (20%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "column_break_factors",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "factor_biometric_enabled",
      "label": "Biometric Enabled Score (15%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "factor_os_updated",
      "label": "OS Updated Score (10%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "factor_no_failures",
      "label": "No Failures Score (10%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "factor_mfa_enabled",
      "label": "MFA Enabled Score (10%)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "section_push_token",
      "label": "Push Notifications",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "push_token",
      "label": "Push Token",
      "fieldtype": "Small Text",
      "hidden": 1
    },
    {
      "fieldname": "push_provider",
      "label": "Push Provider",
      "fieldtype": "Select",
      "options": "\napns\nfcm"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

#### User Shortcut (Child Table)

```json
{
  "doctype": "User Shortcut",
  "module": "Dartwing User",
  "istable": 1,
  "fields": [
    {
      "fieldname": "trigger_phrase",
      "label": "Trigger Phrase",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "action_type",
      "label": "Action Type",
      "fieldtype": "Select",
      "reqd": 1,
      "options": "navigate\napi_call\nexternal_url\nmulti_action",
      "in_list_view": 1
    },
    {
      "fieldname": "target",
      "label": "Target",
      "fieldtype": "Small Text",
      "reqd": 1,
      "description": "Route path, API endpoint, URL, or JSON for multi-action"
    },
    {
      "fieldname": "variables",
      "label": "Variables",
      "fieldtype": "JSON",
      "description": "Variable substitutions for the target"
    },
    {
      "fieldname": "location_trigger",
      "label": "Location Trigger",
      "fieldtype": "JSON",
      "description": "{lat, lng, radius_meters}"
    },
    {
      "fieldname": "time_trigger",
      "label": "Time Trigger",
      "fieldtype": "JSON",
      "description": "{time: '17:00', days: ['mon','tue','wed','thu','fri']}"
    },
    {
      "fieldname": "is_enabled",
      "label": "Enabled",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "usage_count",
      "label": "Usage Count",
      "fieldtype": "Int",
      "default": 0,
      "read_only": 1
    }
  ]
}
```

#### Emergency Contact (Child Table)

```json
{
  "doctype": "Emergency Contact",
  "module": "Dartwing User",
  "istable": 1,
  "fields": [
    {
      "fieldname": "contact_person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "in_list_view": 1
    },
    {
      "fieldname": "contact_name",
      "label": "Name (if not in system)",
      "fieldtype": "Data",
      "depends_on": "eval:!doc.contact_person"
    },
    {
      "fieldname": "relationship",
      "label": "Relationship",
      "fieldtype": "Select",
      "reqd": 1,
      "options": "Spouse\nParent\nChild\nSibling\nPartner\nFriend\nDoctor\nOther",
      "in_list_view": 1
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Int",
      "reqd": 1,
      "default": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "phone_primary",
      "label": "Primary Phone",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "phone_secondary",
      "label": "Secondary Phone",
      "fieldtype": "Data"
    },
    {
      "fieldname": "email",
      "label": "Email",
      "fieldtype": "Data",
      "options": "Email"
    },
    {
      "fieldname": "notes",
      "label": "Notes",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "visible_to_orgs",
      "label": "Visible to Organizations",
      "fieldtype": "Check",
      "default": 0,
      "description": "Allow organizations to see this emergency contact"
    }
  ]
}
```

#### User Block

```json
{
  "doctype": "User Block",
  "module": "Dartwing User",
  "autoname": "hash",
  "fields": [
    {
      "fieldname": "owner_person",
      "label": "Owner",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "block_type",
      "label": "Block Type",
      "fieldtype": "Select",
      "reqd": 1,
      "options": "person\nphone\nemail",
      "in_list_view": 1
    },
    {
      "fieldname": "blocked_person",
      "label": "Blocked Person",
      "fieldtype": "Link",
      "options": "Person",
      "depends_on": "eval:doc.block_type=='person'"
    },
    {
      "fieldname": "blocked_phone",
      "label": "Blocked Phone",
      "fieldtype": "Data",
      "depends_on": "eval:doc.block_type=='phone'"
    },
    {
      "fieldname": "blocked_email",
      "label": "Blocked Email",
      "fieldtype": "Data",
      "depends_on": "eval:doc.block_type=='email'"
    },
    {
      "fieldname": "reason",
      "label": "Reason (Private)",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "report_to_platform",
      "label": "Reported to Platform",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "created_at",
      "label": "Blocked At",
      "fieldtype": "Datetime",
      "default": "Now"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

### 3.3 Advanced Feature Doctypes

#### AI Voice Profile

```json
{
  "doctype": "AI Voice Profile",
  "module": "Dartwing User",
  "autoname": "naming_series:",
  "naming_series": "AVP-.#####",
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "section_voice",
      "label": "Voice Model",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "training_status",
      "label": "Training Status",
      "fieldtype": "Select",
      "options": "not_started\nuploading\ntraining\ncompleted\nfailed",
      "default": "not_started",
      "in_list_view": 1
    },
    {
      "fieldname": "voice_sample",
      "label": "Voice Sample",
      "fieldtype": "Attach Audio"
    },
    {
      "fieldname": "voice_model_id",
      "label": "Voice Model ID (External)",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "voice_provider",
      "label": "Voice Provider",
      "fieldtype": "Select",
      "options": "elevenlabs\nplayht",
      "default": "elevenlabs"
    },
    {
      "fieldname": "column_break_voice",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "sample_duration_seconds",
      "label": "Sample Duration (seconds)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "training_started_at",
      "label": "Training Started",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "training_completed_at",
      "label": "Training Completed",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "section_personality",
      "label": "Personality",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "personality_prompt",
      "label": "Personality Description",
      "fieldtype": "Text",
      "description": "Describe your communication style for AI to emulate"
    },
    {
      "fieldname": "formality_level",
      "label": "Formality Level",
      "fieldtype": "Select",
      "options": "very_casual\ncasual\nneutral\nformal\nvery_formal",
      "default": "neutral"
    },
    {
      "fieldname": "humor_level",
      "label": "Humor Level",
      "fieldtype": "Select",
      "options": "none\nsubtle\nmoderate\nfrequent",
      "default": "subtle"
    },
    {
      "fieldname": "section_permissions",
      "label": "Usage Permissions",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "allow_voicemail",
      "label": "Voicemail Greetings",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "allow_outbound_calls",
      "label": "Outbound Calls (Requires Approval)",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "allow_reading_aloud",
      "label": "Reading Documents Aloud",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "allow_voice_messages",
      "label": "Voice Messages to Contacts",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_security",
      "label": "Security",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "watermark_key",
      "label": "Watermark Key",
      "fieldtype": "Data",
      "hidden": 1,
      "description": "Unique key embedded in all AI-generated audio"
    },
    {
      "fieldname": "consent_given_at",
      "label": "Consent Given At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "consent_ip",
      "label": "Consent IP Address",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_usage",
      "label": "Usage Statistics",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "total_usage_count",
      "label": "Total Usage Count",
      "fieldtype": "Int",
      "default": 0,
      "read_only": 1
    },
    {
      "fieldname": "last_used_at",
      "label": "Last Used At",
      "fieldtype": "Datetime",
      "read_only": 1
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

#### Digital Will

```json
{
  "doctype": "Digital Will",
  "module": "Dartwing User",
  "autoname": "naming_series:",
  "naming_series": "DW-.#####",
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "draft\nactive\nwarning_sent\nrequested\ngranted\ncancelled",
      "default": "draft",
      "in_list_view": 1
    },
    {
      "fieldname": "section_config",
      "label": "Configuration",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "inactive_days",
      "label": "Inactivity Threshold (Days)",
      "fieldtype": "Int",
      "reqd": 1,
      "default": 90,
      "description": "Days of inactivity before trusted contacts are notified (30-365)"
    },
    {
      "fieldname": "warning_threshold_percent",
      "label": "First Warning At (%)",
      "fieldtype": "Int",
      "default": 50,
      "description": "Send first warning at this percentage of inactivity threshold"
    },
    {
      "fieldname": "second_warning_percent",
      "label": "Second Warning At (%)",
      "fieldtype": "Int",
      "default": 75
    },
    {
      "fieldname": "waiting_period_days",
      "label": "Waiting Period (Days)",
      "fieldtype": "Int",
      "default": 7,
      "description": "Days to wait after trustee requests access before granting"
    },
    {
      "fieldname": "section_activity",
      "label": "Activity Tracking",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "last_activity_at",
      "label": "Last Activity",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "last_warning_at",
      "label": "Last Warning Sent",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "warnings_sent_count",
      "label": "Warnings Sent",
      "fieldtype": "Int",
      "default": 0,
      "read_only": 1
    },
    {
      "fieldname": "column_break_activity",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "activated_at",
      "label": "Activated At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "requested_at",
      "label": "Access Requested At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "granted_at",
      "label": "Access Granted At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "section_access",
      "label": "Access Levels",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "grant_personal_org",
      "label": "Grant Access to Personal Data",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "grant_family_orgs",
      "label": "Grant Access to Family Organizations",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "grant_work_orgs",
      "label": "Grant Access to Work Organizations",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "grant_vault",
      "label": "Grant Access to Personal Vault",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_trustees",
      "label": "Trusted Contacts",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "trustees",
      "label": "Trustees",
      "fieldtype": "Table",
      "options": "Digital Will Trustee",
      "reqd": 1
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

#### Digital Will Trustee (Child Table)

```json
{
  "doctype": "Digital Will Trustee",
  "module": "Dartwing User",
  "istable": 1,
  "fields": [
    {
      "fieldname": "trustee_person",
      "label": "Trustee",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "priority",
      "label": "Priority",
      "fieldtype": "Int",
      "reqd": 1,
      "default": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "relationship",
      "label": "Relationship",
      "fieldtype": "Data",
      "in_list_view": 1
    },
    {
      "fieldname": "verification_required",
      "label": "Require Identity Verification",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "notified_at",
      "label": "Notified At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "requested_access_at",
      "label": "Requested Access At",
      "fieldtype": "Datetime",
      "read_only": 1
    }
  ]
}
```

#### Personal Vault Item

```json
{
  "doctype": "Personal Vault Item",
  "module": "Dartwing User",
  "autoname": "hash",
  "fields": [
    {
      "fieldname": "person",
      "label": "Owner",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "file_name",
      "label": "File Name",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "file",
      "label": "File",
      "fieldtype": "Attach",
      "reqd": 1
    },
    {
      "fieldname": "category",
      "label": "Category",
      "fieldtype": "Select",
      "options": "identity\nfinancial\nmedical\nlegal\nproperty\neducation\nother",
      "in_list_view": 1
    },
    {
      "fieldname": "folder",
      "label": "Folder",
      "fieldtype": "Data"
    },
    {
      "fieldname": "column_break_file",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "file_size_bytes",
      "label": "File Size (Bytes)",
      "fieldtype": "Int",
      "read_only": 1
    },
    {
      "fieldname": "mime_type",
      "label": "MIME Type",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "section_encryption",
      "label": "Encryption",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "is_encrypted",
      "label": "Is Encrypted",
      "fieldtype": "Check",
      "default": 1,
      "read_only": 1
    },
    {
      "fieldname": "encryption_key_id",
      "label": "Encryption Key ID",
      "fieldtype": "Data",
      "hidden": 1
    },
    {
      "fieldname": "section_access",
      "label": "Access & Sharing",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "is_favorite",
      "label": "Favorite",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "offline_enabled",
      "label": "Available Offline",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "share_token",
      "label": "Share Token",
      "fieldtype": "Data",
      "hidden": 1
    },
    {
      "fieldname": "share_expires_at",
      "label": "Share Expires At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "include_in_digital_will",
      "label": "Include in Digital Will",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_audit",
      "label": "Audit",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "created_at",
      "label": "Uploaded At",
      "fieldtype": "Datetime",
      "default": "Now"
    },
    {
      "fieldname": "last_accessed_at",
      "label": "Last Accessed",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "access_count",
      "label": "Access Count",
      "fieldtype": "Int",
      "default": 0
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

#### Verification Record

```json
{
  "doctype": "Verification Record",
  "module": "Dartwing User",
  "autoname": "naming_series:",
  "naming_series": "VRF-.#####",
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "level",
      "label": "Verification Level",
      "fieldtype": "Select",
      "options": "none\nbasic\nstandard\nenhanced",
      "default": "none",
      "in_list_view": 1
    },
    {
      "fieldname": "section_email_phone",
      "label": "Basic Verification",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "email_verified",
      "label": "Email Verified",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "email_verified_at",
      "label": "Email Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "phone_verified",
      "label": "Phone Verified",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "phone_verified_at",
      "label": "Phone Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "section_id",
      "label": "Standard Verification (Government ID)",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "id_verified",
      "label": "Government ID Verified",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "document_type",
      "label": "Document Type",
      "fieldtype": "Select",
      "options": "\ndrivers_license\npassport\nnational_id\nresidence_permit"
    },
    {
      "fieldname": "document_country",
      "label": "Document Country",
      "fieldtype": "Link",
      "options": "Country"
    },
    {
      "fieldname": "id_verified_at",
      "label": "ID Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "section_enhanced",
      "label": "Enhanced Verification",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "address_verified",
      "label": "Address Verified",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "address_verified_at",
      "label": "Address Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "liveness_verified",
      "label": "Liveness Check Passed",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "liveness_verified_at",
      "label": "Liveness Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "section_provider",
      "label": "Provider Info",
      "fieldtype": "Section Break",
      "collapsible": 1
    },
    {
      "fieldname": "provider",
      "label": "Verification Provider",
      "fieldtype": "Select",
      "options": "\npersona\njumio\nonfido"
    },
    {
      "fieldname": "provider_verification_id",
      "label": "Provider Verification ID",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "provider_response",
      "label": "Provider Response",
      "fieldtype": "JSON",
      "hidden": 1
    },
    {
      "fieldname": "section_validity",
      "label": "Validity",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "verified_at",
      "label": "Overall Verified At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "expires_at",
      "label": "Expires At",
      "fieldtype": "Datetime",
      "description": "Annual re-verification required"
    },
    {
      "fieldname": "is_expired",
      "label": "Is Expired",
      "fieldtype": "Check",
      "read_only": 1
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    },
    {
      "role": "Dartwing User",
      "read": 1,
      "write": 1,
      "create": 0,
      "delete": 0
    }
  ]
}
```

#### Additional Doctypes (Summary)

| Doctype                     | Key Fields                                                                                        | Purpose                    |
| --------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------- |
| **User Session**            | person, device, token_hash, ip_address, started_at, expires_at, is_active                         | Active session tracking    |
| **User Location Share**     | person, shared_with_person, shared_with_org, latitude, longitude, accuracy, expires_at, is_active | Live location sharing      |
| **Privacy Setting**         | person, organization, data_type, is_allowed, updated_at                                           | Per-org data visibility    |
| **AI Memory Entry**         | person, context_type, category, memory_text, confidence, source, expires_at                       | AI personalization context |
| **Reputation Score**        | person, overall_score, identity_score, payment_score, feedback_score, activity_score              | Portable trust metric      |
| **Notification Preference** | person, organization, channel, event_type, is_enabled, quiet_hours_start/end, digest_frequency    | Notification settings      |
| **User Invite**             | email, organization, inviter, role_template, invite_token, pre_filled_data, status, expires_at    | Pending org invitations    |

---

## 4. Service Layer Architecture

### 4.1 Service Overview

The User module implements a clean service layer that encapsulates business logic:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SERVICE LAYER                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        UserProfileService                            │   │
│  │  get_profile() | update_preferences() | calculate_privacy_score()   │   │
│  │  calculate_completion() | apply_travel_mode()                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DeviceTrustService                            │   │
│  │  register_device() | calculate_trust_score() | approve_device()     │   │
│  │  revoke_device() | check_push_approval() | update_activity()        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        SessionService                                │   │
│  │  create_session() | end_session() | list_sessions()                 │   │
│  │  end_all_sessions() | validate_session()                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        PrivacyService                                │   │
│  │  get_privacy_settings() | update_privacy() | calculate_score()      │   │
│  │  export_data() | schedule_deletion() | get_org_data_access()        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        BlockService                                  │   │
│  │  add_block() | remove_block() | is_blocked() | get_blocks()         │   │
│  │  check_can_contact() | check_can_see_in_directory()                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        TravelModeService                             │   │
│  │  enable() | disable() | check_duress_pin() | get_visible_data()     │   │
│  │  get_decoy_data() | check_auto_disable()                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DigitalWillService                            │   │
│  │  setup() | update_activity() | check_inactivity() | send_warning() │   │
│  │  request_access() | grant_access() | cancel()                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        VaultService                                  │   │
│  │  upload() | download() | delete() | share() | encrypt() | decrypt()│   │
│  │  get_items() | generate_share_link() | revoke_share()              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        VerificationService                           │   │
│  │  start_verification() | check_status() | handle_callback()          │   │
│  │  calculate_level() | is_expired() | get_badge()                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CrossOrgService                               │   │
│  │  search() | get_activity_feed() | get_organizations()              │   │
│  │  switch_org_context() | get_unified_tasks()                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        BriefingService                               │   │
│  │  generate() | get_tasks() | get_events() | get_notifications()     │   │
│  │  generate_audio() | get_weather() | personalize()                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        AIVoiceService                                │   │
│  │  upload_sample() | start_training() | check_training()             │   │
│  │  generate_audio() | add_watermark() | verify_watermark()           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        ShortcutService                               │   │
│  │  create() | execute() | suggest() | check_triggers()               │   │
│  │  import_export() | match_voice_command()                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        InviteService                                 │   │
│  │  create() | send() | accept() | decline() | resend() | revoke()    │   │
│  │  bulk_invite() | generate_qr() | match_existing_user()             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Core Service Implementations

#### DeviceTrustService

```python
# dartwing_user/services/device_trust.py

import frappe
from datetime import datetime, timedelta
from typing import Optional, Dict
import hashlib

class DeviceTrustService:
    """
    Manages device registration, trust scoring, and approval workflows.
    """

    # Trust score weights (total = 100)
    WEIGHTS = {
        'device_age': 20,
        'login_frequency': 15,
        'location_consistency': 20,
        'biometric_enabled': 15,
        'os_updated': 10,
        'no_failures': 10,
        'mfa_enabled': 10,
    }

    @staticmethod
    def register_device(person: str, device_info: Dict) -> str:
        """
        Register a new device or update existing one.
        Returns device document name.
        """
        device_id = device_info.get('device_id')

        existing = frappe.db.get_value(
            "User Device",
            {"person": person, "device_id": device_id},
            "name"
        )

        if existing:
            # Update existing device
            device = frappe.get_doc("User Device", existing)
            device.update({
                "last_active": datetime.now(),
                "last_ip": device_info.get('ip_address'),
                "last_location_city": device_info.get('city'),
                "last_location_country": device_info.get('country'),
                "app_version": device_info.get('app_version'),
                "login_count": device.login_count + 1,
            })
            device.save(ignore_permissions=True)
            return device.name

        # Create new device
        device = frappe.get_doc({
            "doctype": "User Device",
            "person": person,
            "device_id": device_id,
            "device_name": device_info.get('device_name', 'Unknown Device'),
            "device_type": device_info.get('device_type'),
            "os_name": device_info.get('os_name'),
            "os_version": device_info.get('os_version'),
            "app_version": device_info.get('app_version'),
            "first_seen": datetime.now(),
            "last_active": datetime.now(),
            "last_ip": device_info.get('ip_address'),
            "last_location_city": device_info.get('city'),
            "last_location_country": device_info.get('country'),
            "is_trusted": False,
            "approval_status": "pending",
            "trust_score": 30,  # Starting score for new devices
        })
        device.insert(ignore_permissions=True)

        # Check if push approval is needed
        profile = frappe.get_doc("User Profile", {"person": person})
        if profile.push_approval_required:
            DeviceTrustService._send_approval_request(person, device.name)

        return device.name

    @staticmethod
    def calculate_trust_score(device_name: str) -> int:
        """
        Calculate trust score based on multiple factors.
        Returns score 0-100.
        """
        device = frappe.get_doc("User Device", device_name)
        scores = {}

        # Factor 1: Device Age (20%)
        days_registered = (datetime.now() - device.first_seen).days
        if days_registered >= 365:
            scores['device_age'] = 100
        elif days_registered >= 90:
            scores['device_age'] = 80
        elif days_registered >= 30:
            scores['device_age'] = 60
        elif days_registered >= 7:
            scores['device_age'] = 40
        else:
            scores['device_age'] = 20

        # Factor 2: Login Frequency (15%)
        if device.login_count >= 100:
            scores['login_frequency'] = 100
        elif device.login_count >= 50:
            scores['login_frequency'] = 80
        elif device.login_count >= 20:
            scores['login_frequency'] = 60
        elif device.login_count >= 5:
            scores['login_frequency'] = 40
        else:
            scores['login_frequency'] = 20

        # Factor 3: Location Consistency (20%)
        # Check if device typically logs in from same location
        location_score = DeviceTrustService._calculate_location_consistency(device)
        scores['location_consistency'] = location_score

        # Factor 4: Biometric Enabled (15%)
        profile = frappe.get_doc("User Profile", {"person": device.person})
        scores['biometric_enabled'] = 100 if profile.biometric_enabled else 0

        # Factor 5: OS Updated (10%)
        scores['os_updated'] = DeviceTrustService._check_os_updated(device)

        # Factor 6: No Failed Attempts (10%)
        if device.failed_login_count == 0:
            scores['no_failures'] = 100
        elif device.failed_login_count <= 2:
            scores['no_failures'] = 60
        else:
            scores['no_failures'] = 20

        # Factor 7: MFA Enabled (10%)
        # Check Keycloak for MFA status
        has_mfa = DeviceTrustService._check_mfa_enabled(device.person)
        scores['mfa_enabled'] = 100 if has_mfa else 0

        # Calculate weighted score
        total_score = 0
        for factor, weight in DeviceTrustService.WEIGHTS.items():
            factor_score = scores.get(factor, 0)
            total_score += (factor_score * weight) / 100

            # Update factor scores on device
            device.set(f"factor_{factor}", factor_score)

        device.trust_score = int(total_score)
        device.save(ignore_permissions=True)

        return device.trust_score

    @staticmethod
    def approve_device(device_name: str, approver_device: str = None) -> bool:
        """
        Approve a pending device.
        """
        device = frappe.get_doc("User Device", device_name)

        if device.approval_status != "pending":
            return False

        device.approval_status = "approved"
        device.is_trusted = True
        device.trusted_at = datetime.now()
        device.save(ignore_permissions=True)

        # Notify the new device
        DeviceTrustService._send_approval_notification(device, approved=True)

        return True

    @staticmethod
    def deny_device(device_name: str, reason: str = None) -> bool:
        """
        Deny a pending device request.
        """
        device = frappe.get_doc("User Device", device_name)

        if device.approval_status != "pending":
            return False

        device.approval_status = "denied"
        device.revoke_reason = reason
        device.save(ignore_permissions=True)

        # Notify the device
        DeviceTrustService._send_approval_notification(device, approved=False)

        return True

    @staticmethod
    def revoke_device(device_name: str, reason: str = None) -> bool:
        """
        Revoke access from a trusted device.
        """
        device = frappe.get_doc("User Device", device_name)

        device.is_trusted = False
        device.approval_status = "revoked"
        device.revoked_at = datetime.now()
        device.revoke_reason = reason
        device.save(ignore_permissions=True)

        # End all sessions for this device
        from dartwing_user.services.session import SessionService
        SessionService.end_sessions_for_device(device_name)

        return True

    @staticmethod
    def _send_approval_request(person: str, device_name: str):
        """Send push notification to trusted devices for approval."""
        trusted_devices = frappe.get_all(
            "User Device",
            filters={"person": person, "is_trusted": 1, "push_token": ["!=", ""]},
            fields=["push_token", "push_provider"]
        )

        device = frappe.get_doc("User Device", device_name)

        for td in trusted_devices:
            # Send push notification via appropriate provider
            from dartwing_user.services.push import PushService
            PushService.send_approval_request(
                push_token=td.push_token,
                provider=td.push_provider,
                new_device=device.as_dict()
            )

    @staticmethod
    def _calculate_location_consistency(device) -> int:
        """Calculate how consistent login locations are."""
        # Get last 30 days of sessions
        sessions = frappe.get_all(
            "User Session",
            filters={
                "device": device.name,
                "started_at": [">", datetime.now() - timedelta(days=30)]
            },
            fields=["location_city", "location_country"]
        )

        if not sessions:
            return 50  # Neutral score for new devices

        # Count unique locations
        locations = set()
        for s in sessions:
            if s.location_city and s.location_country:
                locations.add(f"{s.location_city},{s.location_country}")

        if len(locations) <= 2:
            return 100
        elif len(locations) <= 5:
            return 70
        else:
            return 40

    @staticmethod
    def _check_os_updated(device) -> int:
        """Check if device OS is reasonably up to date."""
        # This would integrate with known OS version data
        # Simplified implementation
        return 80  # Assume reasonably updated

    @staticmethod
    def _check_mfa_enabled(person: str) -> bool:
        """Check if user has MFA enabled in Keycloak."""
        # Would query Keycloak Admin API
        return False  # Default to false
```

#### TravelModeService

```python
# dartwing_user/services/travel_mode.py

import frappe
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import hashlib

class TravelModeService:
    """
    Manages travel mode activation, data hiding, and duress PIN.
    """

    @staticmethod
    def enable(person: str, config: Dict = None) -> bool:
        """
        Enable travel mode for user.
        """
        profile = frappe.get_doc("User Profile", {"person": person})

        config = config or {}

        profile.travel_mode = 1
        profile.travel_mode_activated_at = datetime.now()
        profile.travel_mode_auto_disable_days = config.get('auto_disable_days', 7)
        profile.hide_financial = config.get('hide_financial', True)
        profile.hide_medical = config.get('hide_medical', True)
        profile.hide_business = config.get('hide_business', True)

        # Set duress PIN if provided
        if config.get('duress_pin'):
            profile.duress_pin_hash = TravelModeService._hash_pin(config['duress_pin'])

        profile.save(ignore_permissions=True)

        # Notify trusted contact if configured
        if config.get('notify_trusted_contact'):
            TravelModeService._notify_trusted_contact(person)

        frappe.log_security_event(
            "travel_mode_enabled",
            user=frappe.db.get_value("Person", person, "frappe_user"),
            details={"person": person}
        )

        return True

    @staticmethod
    def disable(person: str) -> bool:
        """
        Disable travel mode.
        """
        profile = frappe.get_doc("User Profile", {"person": person})

        profile.travel_mode = 0
        profile.travel_mode_activated_at = None
        profile.save(ignore_permissions=True)

        frappe.log_security_event(
            "travel_mode_disabled",
            user=frappe.db.get_value("Person", person, "frappe_user"),
            details={"person": person}
        )

        return True

    @staticmethod
    def check_duress_pin(person: str, pin: str) -> bool:
        """
        Check if the provided PIN is the duress PIN.
        Returns True if duress PIN matches (indicating coercion).
        """
        profile = frappe.get_doc("User Profile", {"person": person})

        if not profile.duress_pin_hash:
            return False

        pin_hash = TravelModeService._hash_pin(pin)
        is_duress = pin_hash == profile.duress_pin_hash

        if is_duress:
            # Log duress activation (silent - don't alert attacker)
            frappe.log_security_event(
                "duress_pin_entered",
                user=frappe.db.get_value("Person", person, "frappe_user"),
                details={"person": person},
                severity="critical"
            )
            # Silently notify trusted contacts
            TravelModeService._silent_duress_alert(person)

        return is_duress

    @staticmethod
    def get_visible_data(person: str, data_type: str, is_duress: bool = False) -> Any:
        """
        Get data with travel mode filters applied.
        Returns decoy data if duress mode.
        """
        profile = frappe.get_doc("User Profile", {"person": person})

        if not profile.travel_mode:
            return None  # No filtering needed

        # Check if data type should be hidden
        hidden_types = []
        if profile.hide_financial:
            hidden_types.append('financial')
        if profile.hide_medical:
            hidden_types.append('medical')
        if profile.hide_business:
            hidden_types.append('business')

        if data_type in hidden_types:
            if is_duress:
                return TravelModeService._get_decoy_data(person, data_type)
            else:
                return None  # Hidden

        return None  # Not filtered

    @staticmethod
    def check_auto_disable() -> None:
        """
        Scheduled job to auto-disable expired travel modes.
        """
        expired_profiles = frappe.get_all(
            "User Profile",
            filters={
                "travel_mode": 1,
                "travel_mode_activated_at": ["<", datetime.now() - timedelta(days=1)]
            },
            fields=["name", "person", "travel_mode_activated_at", "travel_mode_auto_disable_days"]
        )

        for profile_data in expired_profiles:
            activated = profile_data.travel_mode_activated_at
            auto_days = profile_data.travel_mode_auto_disable_days or 7

            if datetime.now() > activated + timedelta(days=auto_days):
                TravelModeService.disable(profile_data.person)

    @staticmethod
    def _hash_pin(pin: str) -> str:
        """Hash PIN with salt."""
        salt = frappe.conf.get("encryption_key", "dartwing-salt")
        return hashlib.sha256(f"{pin}{salt}".encode()).hexdigest()

    @staticmethod
    def _notify_trusted_contact(person: str):
        """Notify trusted contact that travel mode was enabled."""
        will = frappe.db.get_value("Digital Will", {"person": person}, "name")
        if not will:
            return

        trustees = frappe.get_all(
            "Digital Will Trustee",
            filters={"parent": will},
            fields=["trustee_person"],
            order_by="priority"
        )

        if trustees:
            from dartwing_user.services.notification import NotificationService
            NotificationService.send(
                person=trustees[0].trustee_person,
                title="Travel Mode Activated",
                message=f"Your contact has enabled travel mode.",
                category="security"
            )

    @staticmethod
    def _silent_duress_alert(person: str):
        """
        Silently alert trusted contacts of duress situation.
        This must NOT be visible to the user or potential attacker.
        """
        will = frappe.db.get_value("Digital Will", {"person": person}, "name")
        if not will:
            return

        trustees = frappe.get_all(
            "Digital Will Trustee",
            filters={"parent": will},
            fields=["trustee_person"],
            order_by="priority"
        )

        for trustee in trustees:
            # Send via backend channel only (not visible in UI)
            frappe.enqueue(
                'dartwing_user.services.emergency.send_duress_alert',
                trustee_person=trustee.trustee_person,
                subject_person=person,
                queue='critical'
            )

    @staticmethod
    def _get_decoy_data(person: str, data_type: str) -> Dict:
        """
        Generate believable decoy data for duress situations.
        """
        # Return minimal, believable decoy data
        decoy_data = {
            'financial': {
                'accounts': [
                    {'name': 'Checking', 'balance': 1234.56},
                ],
                'recent_transactions': []
            },
            'medical': {
                'conditions': [],
                'medications': []
            },
            'business': {
                'documents': [],
                'recent_activity': []
            }
        }

        return decoy_data.get(data_type, {})
```

---

## 5. API Design & Endpoints

### 5.1 API Design Principles

Following Dartwing Core conventions:

1. **RESTful Resources:** Standard HTTP methods for CRUD
2. **Frappe API Convention:** Use `/api/method/dartwing_user.api.*`
3. **Consistent Response Format:** `{message: {data, success, errors}}`
4. **Rate Limiting:** Applied per-user, per-endpoint
5. **Audit Logging:** All sensitive operations logged

### 5.2 Complete API Endpoint Specification

#### Profile APIs

```python
# dartwing_user/api/profile.py

@frappe.whitelist()
def get_my_profile() -> Dict:
    """
    GET /api/method/dartwing_user.api.profile.get_my_profile

    Returns the current user's profile with all preferences.
    """
    person = get_person_for_current_user()
    profile = frappe.get_doc("User Profile", {"person": person})

    return {
        "profile": profile.as_dict(),
        "person": frappe.get_doc("Person", person).as_dict(),
        "verification_level": get_verification_level(person),
        "organizations_count": get_org_count(person),
    }

@frappe.whitelist()
def update_preferences(preferences: Dict) -> Dict:
    """
    POST /api/method/dartwing_user.api.profile.update_preferences

    Update user preferences (theme, language, etc.)
    """
    person = get_person_for_current_user()
    profile = frappe.get_doc("User Profile", {"person": person})

    allowed_fields = [
        'theme', 'accent_color', 'font_size', 'high_contrast',
        'reduce_motion', 'language', 'timezone', 'date_format', 'time_format'
    ]

    for field in allowed_fields:
        if field in preferences:
            profile.set(field, preferences[field])

    profile.save()

    return {"success": True, "profile": profile.as_dict()}

@frappe.whitelist()
def upload_avatar() -> Dict:
    """
    POST /api/method/dartwing_user.api.profile.upload_avatar

    Upload profile avatar. File in request.files['avatar']
    """
    person = get_person_for_current_user()

    if 'avatar' not in frappe.request.files:
        frappe.throw("No avatar file provided")

    file = frappe.request.files['avatar']

    # Save file and update Person
    file_doc = save_file(
        file.filename,
        file.read(),
        "Person",
        person,
        is_private=0
    )

    frappe.db.set_value("Person", person, "image", file_doc.file_url)

    return {"success": True, "avatar_url": file_doc.file_url}
```

#### Device APIs

```python
# dartwing_user/api/devices.py

@frappe.whitelist()
def get_my_devices() -> Dict:
    """
    GET /api/method/dartwing_user.api.devices.get_my_devices

    List all devices for current user.
    """
    person = get_person_for_current_user()

    devices = frappe.get_all(
        "User Device",
        filters={"person": person},
        fields=["*"],
        order_by="last_active desc"
    )

    # Mark current device
    current_device_id = get_current_device_id()
    for device in devices:
        device['is_current'] = device['device_id'] == current_device_id

    return {"devices": devices}

@frappe.whitelist()
def register_device(device_info: Dict) -> Dict:
    """
    POST /api/method/dartwing_user.api.devices.register_device

    Register a new device.
    """
    person = get_person_for_current_user()

    device_name = DeviceTrustService.register_device(person, device_info)
    device = frappe.get_doc("User Device", device_name)

    return {
        "device": device.as_dict(),
        "requires_approval": device.approval_status == "pending"
    }

@frappe.whitelist()
def trust_device(device_name: str) -> Dict:
    """
    POST /api/method/dartwing_user.api.devices.trust_device

    Mark a device as trusted (from another trusted device).
    """
    person = get_person_for_current_user()
    device = frappe.get_doc("User Device", device_name)

    # Verify ownership
    if device.person != person:
        frappe.throw("Not your device", frappe.PermissionError)

    # Verify caller is on a trusted device
    current_device = get_current_device()
    if not current_device or not current_device.is_trusted:
        frappe.throw("Must approve from a trusted device")

    DeviceTrustService.approve_device(device_name, current_device.name)

    return {"success": True}

@frappe.whitelist()
def revoke_device(device_name: str, reason: str = None) -> Dict:
    """
    DELETE /api/method/dartwing_user.api.devices.revoke_device

    Revoke access from a device.
    """
    person = get_person_for_current_user()
    device = frappe.get_doc("User Device", device_name)

    if device.person != person:
        frappe.throw("Not your device", frappe.PermissionError)

    DeviceTrustService.revoke_device(device_name, reason)

    return {"success": True}

@frappe.whitelist()
def approve_pending_device(device_name: str, approve: bool) -> Dict:
    """
    POST /api/method/dartwing_user.api.devices.approve_pending_device

    Approve or deny a pending device login from a trusted device.
    """
    person = get_person_for_current_user()
    device = frappe.get_doc("User Device", device_name)

    if device.person != person:
        frappe.throw("Not your device", frappe.PermissionError)

    if approve:
        DeviceTrustService.approve_device(device_name)
    else:
        DeviceTrustService.deny_device(device_name)

    return {"success": True, "approved": approve}

@frappe.whitelist()
def sign_out_all_devices() -> Dict:
    """
    POST /api/method/dartwing_user.api.devices.sign_out_all_devices

    Sign out from all devices except current.
    """
    person = get_person_for_current_user()
    current_device_id = get_current_device_id()

    # Revoke all other devices
    devices = frappe.get_all(
        "User Device",
        filters={"person": person, "device_id": ["!=", current_device_id]},
        pluck="name"
    )

    for device_name in devices:
        DeviceTrustService.revoke_device(device_name, "Signed out from all devices")

    return {"success": True, "devices_revoked": len(devices)}
```

#### Privacy APIs

```python
# dartwing_user/api/privacy.py

@frappe.whitelist()
def get_privacy_dashboard() -> Dict:
    """
    GET /api/method/dartwing_user.api.privacy.get_privacy_dashboard

    Get privacy dashboard with score and org data access.
    """
    person = get_person_for_current_user()
    profile = frappe.get_doc("User Profile", {"person": person})

    # Get privacy settings per org
    orgs = frappe.get_all(
        "Org Member",
        filters={"person": person, "status": "Active"},
        fields=["organization"]
    )

    org_access = []
    for org in orgs:
        org_doc = frappe.get_doc("Organization", org.organization)
        settings = frappe.get_all(
            "Privacy Setting",
            filters={"person": person, "organization": org.organization},
            fields=["data_type", "is_allowed"]
        )

        org_access.append({
            "organization": org.organization,
            "org_name": org_doc.org_name,
            "org_type": org_doc.org_type,
            "settings": settings
        })

    # Get connected third-party apps (future)
    connected_apps = []

    # Calculate recommendations
    recommendations = PrivacyService.get_recommendations(person)

    return {
        "privacy_score": profile.privacy_score,
        "org_access": org_access,
        "connected_apps": connected_apps,
        "recommendations": recommendations
    }

@frappe.whitelist()
def update_privacy_setting(organization: str, data_type: str, is_allowed: bool) -> Dict:
    """
    PUT /api/method/dartwing_user.api.privacy.update_privacy_setting

    Update privacy setting for specific org and data type.
    """
    person = get_person_for_current_user()

    # Verify membership
    if not frappe.db.exists("Org Member", {"person": person, "organization": organization}):
        frappe.throw("Not a member of this organization")

    PrivacyService.update_setting(person, organization, data_type, is_allowed)

    return {"success": True}

@frappe.whitelist()
def request_data_export() -> Dict:
    """
    POST /api/method/dartwing_user.api.privacy.request_data_export

    Request GDPR data export.
    """
    person = get_person_for_current_user()

    # Queue export job
    export_id = PrivacyService.queue_data_export(person)

    return {
        "success": True,
        "export_id": export_id,
        "message": "Export started. You'll receive an email when ready."
    }

@frappe.whitelist()
def request_account_deletion() -> Dict:
    """
    POST /api/method/dartwing_user.api.privacy.request_account_deletion

    Request account deletion (starts 7-day grace period).
    """
    person = get_person_for_current_user()

    # Check if sole admin of any org
    sole_admin_orgs = PrivacyService.check_sole_admin(person)
    if sole_admin_orgs:
        frappe.throw(f"Cannot delete: sole admin of {', '.join(sole_admin_orgs)}")

    # Schedule deletion
    deletion_date = PrivacyService.schedule_deletion(person)

    return {
        "success": True,
        "deletion_scheduled_for": deletion_date,
        "message": "Account deletion scheduled. You have 7 days to cancel."
    }

@frappe.whitelist()
def cancel_deletion() -> Dict:
    """
    POST /api/method/dartwing_user.api.privacy.cancel_deletion

    Cancel pending account deletion.
    """
    person = get_person_for_current_user()

    PrivacyService.cancel_deletion(person)

    return {"success": True}
```

#### Security APIs

```python
# dartwing_user/api/security.py

@frappe.whitelist()
def toggle_travel_mode(enabled: bool, config: Dict = None) -> Dict:
    """
    POST /api/method/dartwing_user.api.security.toggle_travel_mode
    """
    person = get_person_for_current_user()

    if enabled:
        TravelModeService.enable(person, config)
    else:
        TravelModeService.disable(person)

    return {"success": True, "travel_mode": enabled}

@frappe.whitelist()
def get_sessions() -> Dict:
    """
    GET /api/method/dartwing_user.api.security.get_sessions
    """
    person = get_person_for_current_user()

    sessions = SessionService.list_sessions(person)

    return {"sessions": sessions}

@frappe.whitelist()
def end_session(session_id: str) -> Dict:
    """
    DELETE /api/method/dartwing_user.api.security.end_session
    """
    person = get_person_for_current_user()

    SessionService.end_session(session_id, person)

    return {"success": True}
```

#### Cross-Org APIs

```python
# dartwing_user/api/cross_org.py

@frappe.whitelist()
def search(query: str, filters: Dict = None) -> Dict:
    """
    POST /api/method/dartwing_user.api.cross_org.search

    Search across all user's organizations.
    """
    person = get_person_for_current_user()

    results = CrossOrgService.search(
        person=person,
        query=query,
        org_filter=filters.get('organizations'),
        type_filter=filters.get('types'),
        date_range=filters.get('date_range')
    )

    return {"results": results}

@frappe.whitelist()
def get_activity_feed(page: int = 1, page_size: int = 20) -> Dict:
    """
    GET /api/method/dartwing_user.api.cross_org.get_activity_feed
    """
    person = get_person_for_current_user()

    feed = CrossOrgService.get_activity_feed(
        person=person,
        page=page,
        page_size=page_size
    )

    return {"feed": feed}

@frappe.whitelist()
def get_organizations() -> Dict:
    """
    GET /api/method/dartwing_user.api.cross_org.get_organizations
    """
    person = get_person_for_current_user()

    orgs = CrossOrgService.get_organizations(person)

    return {"organizations": orgs}
```

### 5.3 API Endpoint Summary Table

| Category         | Endpoint                            | Method | Purpose              |
| ---------------- | ----------------------------------- | ------ | -------------------- |
| **Profile**      | `/profile.get_my_profile`           | GET    | Get user profile     |
|                  | `/profile.update_preferences`       | POST   | Update preferences   |
|                  | `/profile.upload_avatar`            | POST   | Upload avatar        |
| **Devices**      | `/devices.get_my_devices`           | GET    | List devices         |
|                  | `/devices.register_device`          | POST   | Register device      |
|                  | `/devices.trust_device`             | POST   | Trust device         |
|                  | `/devices.revoke_device`            | DELETE | Revoke device        |
|                  | `/devices.approve_pending_device`   | POST   | Approve/deny pending |
|                  | `/devices.sign_out_all_devices`     | POST   | Sign out all         |
| **Sessions**     | `/security.get_sessions`            | GET    | List sessions        |
|                  | `/security.end_session`             | DELETE | End session          |
| **Privacy**      | `/privacy.get_privacy_dashboard`    | GET    | Privacy dashboard    |
|                  | `/privacy.update_privacy_setting`   | PUT    | Update setting       |
|                  | `/privacy.request_data_export`      | POST   | Request export       |
|                  | `/privacy.request_account_deletion` | POST   | Request deletion     |
|                  | `/privacy.cancel_deletion`          | POST   | Cancel deletion      |
| **Security**     | `/security.toggle_travel_mode`      | POST   | Toggle travel mode   |
| **Blocks**       | `/blocks.get_blocks`                | GET    | List blocks          |
|                  | `/blocks.add_block`                 | POST   | Add block            |
|                  | `/blocks.remove_block`              | DELETE | Remove block         |
| **Cross-Org**    | `/cross_org.search`                 | POST   | Cross-org search     |
|                  | `/cross_org.get_activity_feed`      | GET    | Activity feed        |
|                  | `/cross_org.get_organizations`      | GET    | List organizations   |
| **Briefing**     | `/briefing.get_daily`               | GET    | Get daily briefing   |
|                  | `/briefing.get_audio`               | GET    | Get audio briefing   |
| **Shortcuts**    | `/shortcuts.list`                   | GET    | List shortcuts       |
|                  | `/shortcuts.create`                 | POST   | Create shortcut      |
|                  | `/shortcuts.update`                 | PUT    | Update shortcut      |
|                  | `/shortcuts.delete`                 | DELETE | Delete shortcut      |
|                  | `/shortcuts.execute`                | POST   | Execute shortcut     |
| **Location**     | `/location.start_share`             | POST   | Start sharing        |
|                  | `/location.stop_share`              | DELETE | Stop sharing         |
|                  | `/location.get_shares`              | GET    | Get active shares    |
|                  | `/location.update_position`         | POST   | Update position      |
| **Emergency**    | `/emergency.get_contacts`           | GET    | List contacts        |
|                  | `/emergency.update_contacts`        | PUT    | Update contacts      |
|                  | `/emergency.broadcast`              | POST   | Emergency broadcast  |
| **Vault**        | `/vault.list`                       | GET    | List vault items     |
|                  | `/vault.upload`                     | POST   | Upload file          |
|                  | `/vault.download`                   | GET    | Download file        |
|                  | `/vault.delete`                     | DELETE | Delete file          |
|                  | `/vault.share`                      | POST   | Generate share link  |
| **Verification** | `/verification.start`               | POST   | Start verification   |
|                  | `/verification.status`              | GET    | Check status         |
|                  | `/verification.callback`            | POST   | Provider callback    |
| **Voice**        | `/voice.upload_sample`              | POST   | Upload voice sample  |
|                  | `/voice.get_status`                 | GET    | Training status      |
|                  | `/voice.generate`                   | POST   | Generate audio       |
|                  | `/voice.delete`                     | DELETE | Delete profile       |
| **Digital Will** | `/will.get`                         | GET    | Get will config      |
|                  | `/will.update`                      | PUT    | Update will          |
|                  | `/will.request_access`              | POST   | Trustee requests     |
|                  | `/will.cancel_access`               | POST   | Cancel access        |
| **Invites**      | `/invites.list`                     | GET    | List pending         |
|                  | `/invites.accept`                   | POST   | Accept invite        |
|                  | `/invites.decline`                  | POST   | Decline invite       |
| **AI Memory**    | `/ai_memory.list`                   | GET    | List memories        |
|                  | `/ai_memory.delete`                 | DELETE | Delete memory        |
|                  | `/ai_memory.clear_all`              | DELETE | Clear all            |
| **Reputation**   | `/reputation.get`                   | GET    | Get score            |

---

## 6. Flutter Client Architecture

### 6.1 Feature-First Structure

Following Dartwing Core patterns, the User module Flutter code uses feature-first organization:

```
lib/
├── features/
│   └── user/
│       ├── data/
│       │   ├── repositories/
│       │   │   ├── user_profile_repository.dart
│       │   │   ├── device_repository.dart
│       │   │   ├── session_repository.dart
│       │   │   ├── privacy_repository.dart
│       │   │   ├── vault_repository.dart
│       │   │   ├── verification_repository.dart
│       │   │   └── cross_org_repository.dart
│       │   ├── datasources/
│       │   │   ├── user_remote_datasource.dart
│       │   │   └── user_local_datasource.dart
│       │   └── models/
│       │       ├── user_profile_dto.dart
│       │       ├── user_device_dto.dart
│       │       ├── privacy_setting_dto.dart
│       │       └── ...
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── user_profile.dart
│       │   │   ├── user_device.dart
│       │   │   ├── user_session.dart
│       │   │   ├── privacy_setting.dart
│       │   │   ├── vault_item.dart
│       │   │   ├── verification_record.dart
│       │   │   ├── digital_will.dart
│       │   │   ├── ai_voice_profile.dart
│       │   │   └── ...
│       │   ├── repositories/
│       │   │   └── i_user_repository.dart
│       │   └── usecases/
│       │       ├── get_profile_usecase.dart
│       │       ├── update_preferences_usecase.dart
│       │       ├── manage_devices_usecase.dart
│       │       ├── toggle_travel_mode_usecase.dart
│       │       └── ...
│       └── presentation/
│           ├── providers/
│           │   ├── user_profile_provider.dart
│           │   ├── devices_provider.dart
│           │   ├── sessions_provider.dart
│           │   ├── privacy_provider.dart
│           │   ├── travel_mode_provider.dart
│           │   ├── vault_provider.dart
│           │   ├── verification_provider.dart
│           │   ├── briefing_provider.dart
│           │   ├── shortcuts_provider.dart
│           │   └── cross_org_provider.dart
│           ├── screens/
│           │   ├── profile/
│           │   │   ├── profile_screen.dart
│           │   │   ├── edit_profile_screen.dart
│           │   │   └── preferences_screen.dart
│           │   ├── devices/
│           │   │   ├── devices_screen.dart
│           │   │   ├── device_detail_screen.dart
│           │   │   └── pending_approval_screen.dart
│           │   ├── sessions/
│           │   │   └── sessions_screen.dart
│           │   ├── privacy/
│           │   │   ├── privacy_dashboard_screen.dart
│           │   │   ├── org_permissions_screen.dart
│           │   │   └── data_export_screen.dart
│           │   ├── security/
│           │   │   ├── travel_mode_screen.dart
│           │   │   └── block_list_screen.dart
│           │   ├── vault/
│           │   │   ├── vault_screen.dart
│           │   │   ├── vault_item_screen.dart
│           │   │   └── vault_upload_screen.dart
│           │   ├── verification/
│           │   │   ├── verification_screen.dart
│           │   │   └── verification_flow_screen.dart
│           │   ├── emergency/
│           │   │   ├── emergency_contacts_screen.dart
│           │   │   └── location_share_screen.dart
│           │   ├── briefing/
│           │   │   └── daily_briefing_screen.dart
│           │   ├── shortcuts/
│           │   │   ├── shortcuts_screen.dart
│           │   │   └── shortcut_editor_screen.dart
│           │   ├── voice/
│           │   │   ├── voice_profile_screen.dart
│           │   │   └── voice_training_screen.dart
│           │   ├── will/
│           │   │   ├── digital_will_screen.dart
│           │   │   └── will_setup_screen.dart
│           │   ├── organizations/
│           │   │   ├── org_switcher_screen.dart
│           │   │   └── org_list_screen.dart
│           │   ├── search/
│           │   │   └── cross_org_search_screen.dart
│           │   └── activity/
│           │       └── activity_feed_screen.dart
│           └── widgets/
│               ├── profile_avatar.dart
│               ├── device_card.dart
│               ├── session_tile.dart
│               ├── privacy_score_gauge.dart
│               ├── travel_mode_banner.dart
│               ├── org_switcher_fab.dart
│               ├── verification_badge.dart
│               ├── vault_item_tile.dart
│               └── ...
```

### 6.2 Core Entities (Freezed Models)

```dart
// lib/features/user/domain/entities/user_profile.dart

import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_profile.freezed.dart';
part 'user_profile.g.dart';

@freezed
class UserProfile with _$UserProfile {
  const factory UserProfile({
    required String name,
    required String person,

    // Appearance
    @Default('system') String theme,
    String? accentColor,
    @Default('medium') String fontSize,
    @Default(false) bool highContrast,
    @Default(false) bool reduceMotion,

    // Localization
    @Default('en') String language,
    @Default('UTC') String timezone,
    @Default('MM/DD/YYYY') String dateFormat,
    @Default('12-hour') String timeFormat,

    // Security
    @Default(false) bool travelMode,
    DateTime? travelModeActivatedAt,
    @Default(false) bool pushApprovalRequired,
    @Default(false) bool biometricEnabled,

    // Travel Mode Data Hiding
    @Default(true) bool hideFinancial,
    @Default(true) bool hideMedical,
    @Default(true) bool hideBusiness,

    // Metrics
    @Default(50) int privacyScore,
    @Default(0) double profileCompletion,
    DateTime? lastActivity,

    // Child tables
    @Default([]) List<UserShortcut> shortcuts,
    @Default([]) List<EmergencyContact> emergencyContacts,
  }) = _UserProfile;

  factory UserProfile.fromJson(Map<String, dynamic> json) =>
      _$UserProfileFromJson(json);
}

@freezed
class UserShortcut with _$UserShortcut {
  const factory UserShortcut({
    required String triggerPhrase,
    required String actionType,
    required String target,
    Map<String, dynamic>? variables,
    Map<String, dynamic>? locationTrigger,
    Map<String, dynamic>? timeTrigger,
    @Default(true) bool isEnabled,
    @Default(0) int usageCount,
  }) = _UserShortcut;

  factory UserShortcut.fromJson(Map<String, dynamic> json) =>
      _$UserShortcutFromJson(json);
}

@freezed
class EmergencyContact with _$EmergencyContact {
  const factory EmergencyContact({
    String? contactPerson,
    String? contactName,
    required String relationship,
    required int priority,
    required String phonePrimary,
    String? phoneSecondary,
    String? email,
    String? notes,
    @Default(false) bool visibleToOrgs,
  }) = _EmergencyContact;

  factory EmergencyContact.fromJson(Map<String, dynamic> json) =>
      _$EmergencyContactFromJson(json);
}
```

```dart
// lib/features/user/domain/entities/user_device.dart

@freezed
class UserDevice with _$UserDevice {
  const factory UserDevice({
    required String name,
    required String person,
    required String deviceId,
    String? deviceName,
    required String deviceType,
    String? osName,
    String? osVersion,
    String? appVersion,

    // Trust
    @Default(false) bool isTrusted,
    @Default(50) int trustScore,
    @Default('pending') String approvalStatus,
    DateTime? trustedAt,
    DateTime? revokedAt,
    String? revokeReason,

    // Activity
    DateTime? firstSeen,
    DateTime? lastActive,
    String? lastIp,
    String? lastLocationCity,
    String? lastLocationCountry,
    @Default(0) int loginCount,
    @Default(0) int failedLoginCount,

    // Trust factors
    int? factorDeviceAge,
    int? factorLoginFrequency,
    int? factorLocationConsistency,
    int? factorBiometricEnabled,
    int? factorOsUpdated,
    int? factorNoFailures,
    int? factorMfaEnabled,

    // Computed
    @Default(false) bool isCurrent,
  }) = _UserDevice;

  factory UserDevice.fromJson(Map<String, dynamic> json) =>
      _$UserDeviceFromJson(json);
}
```

### 6.3 Riverpod Providers

```dart
// lib/features/user/presentation/providers/user_profile_provider.dart

import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'user_profile_provider.g.dart';

@riverpod
class UserProfileNotifier extends _$UserProfileNotifier {
  @override
  Future<UserProfile> build() async {
    final repository = ref.watch(userProfileRepositoryProvider);
    return repository.getMyProfile();
  }

  Future<void> updatePreferences(Map<String, dynamic> preferences) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(userProfileRepositoryProvider);
      return repository.updatePreferences(preferences);
    });
  }

  Future<void> uploadAvatar(File file) async {
    final repository = ref.read(userProfileRepositoryProvider);
    final updatedProfile = await repository.uploadAvatar(file);
    state = AsyncValue.data(updatedProfile);
  }
}

@riverpod
Future<int> privacyScore(PrivacyScoreRef ref) async {
  final profile = await ref.watch(userProfileNotifierProvider.future);
  return profile.privacyScore;
}

@riverpod
bool isTravelModeEnabled(IsTravelModeEnabledRef ref) {
  final profileAsync = ref.watch(userProfileNotifierProvider);
  return profileAsync.maybeWhen(
    data: (profile) => profile.travelMode,
    orElse: () => false,
  );
}
```

```dart
// lib/features/user/presentation/providers/devices_provider.dart

@riverpod
class DevicesNotifier extends _$DevicesNotifier {
  @override
  Future<List<UserDevice>> build() async {
    final repository = ref.watch(deviceRepositoryProvider);
    return repository.getMyDevices();
  }

  Future<void> trustDevice(String deviceName) async {
    final repository = ref.read(deviceRepositoryProvider);
    await repository.trustDevice(deviceName);
    ref.invalidateSelf();
  }

  Future<void> revokeDevice(String deviceName, {String? reason}) async {
    final repository = ref.read(deviceRepositoryProvider);
    await repository.revokeDevice(deviceName, reason: reason);
    ref.invalidateSelf();
  }

  Future<void> approveDevice(String deviceName, bool approve) async {
    final repository = ref.read(deviceRepositoryProvider);
    await repository.approvePendingDevice(deviceName, approve);
    ref.invalidateSelf();
  }

  Future<void> signOutAllDevices() async {
    final repository = ref.read(deviceRepositoryProvider);
    await repository.signOutAllDevices();
    ref.invalidateSelf();
  }
}

@riverpod
List<UserDevice> trustedDevices(TrustedDevicesRef ref) {
  final devicesAsync = ref.watch(devicesNotifierProvider);
  return devicesAsync.maybeWhen(
    data: (devices) => devices.where((d) => d.isTrusted).toList(),
    orElse: () => [],
  );
}

@riverpod
List<UserDevice> pendingDevices(PendingDevicesRef ref) {
  final devicesAsync = ref.watch(devicesNotifierProvider);
  return devicesAsync.maybeWhen(
    data: (devices) => devices.where((d) => d.approvalStatus == 'pending').toList(),
    orElse: () => [],
  );
}
```

```dart
// lib/features/user/presentation/providers/travel_mode_provider.dart

@riverpod
class TravelModeNotifier extends _$TravelModeNotifier {
  @override
  TravelModeState build() {
    final profileAsync = ref.watch(userProfileNotifierProvider);
    return profileAsync.maybeWhen(
      data: (profile) => TravelModeState(
        isEnabled: profile.travelMode,
        activatedAt: profile.travelModeActivatedAt,
        hideFinancial: profile.hideFinancial,
        hideMedical: profile.hideMedical,
        hideBusiness: profile.hideBusiness,
      ),
      orElse: () => const TravelModeState(),
    );
  }

  Future<void> enable({
    bool hideFinancial = true,
    bool hideMedical = true,
    bool hideBusiness = true,
    String? duressPin,
    int autoDisableDays = 7,
    bool notifyTrustedContact = false,
  }) async {
    final repository = ref.read(securityRepositoryProvider);
    await repository.toggleTravelMode(
      enabled: true,
      config: {
        'hide_financial': hideFinancial,
        'hide_medical': hideMedical,
        'hide_business': hideBusiness,
        'duress_pin': duressPin,
        'auto_disable_days': autoDisableDays,
        'notify_trusted_contact': notifyTrustedContact,
      },
    );
    ref.invalidate(userProfileNotifierProvider);
  }

  Future<void> disable() async {
    final repository = ref.read(securityRepositoryProvider);
    await repository.toggleTravelMode(enabled: false);
    ref.invalidate(userProfileNotifierProvider);
  }
}

@freezed
class TravelModeState with _$TravelModeState {
  const factory TravelModeState({
    @Default(false) bool isEnabled,
    DateTime? activatedAt,
    @Default(true) bool hideFinancial,
    @Default(true) bool hideMedical,
    @Default(true) bool hideBusiness,
  }) = _TravelModeState;
}
```

```dart
// lib/features/user/presentation/providers/cross_org_provider.dart

@riverpod
class CrossOrgSearchNotifier extends _$CrossOrgSearchNotifier {
  @override
  CrossOrgSearchState build() {
    return const CrossOrgSearchState();
  }

  Future<void> search(String query, {List<String>? organizations}) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final repository = ref.read(crossOrgRepositoryProvider);
      final results = await repository.search(
        query: query,
        organizations: organizations,
      );
      state = state.copyWith(
        isLoading: false,
        results: results,
        lastQuery: query,
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  void clearResults() {
    state = const CrossOrgSearchState();
  }
}

@riverpod
Future<List<Organization>> userOrganizations(UserOrganizationsRef ref) async {
  final repository = ref.watch(crossOrgRepositoryProvider);
  return repository.getOrganizations();
}

@riverpod
class ActivityFeedNotifier extends _$ActivityFeedNotifier {
  int _currentPage = 1;
  bool _hasMore = true;

  @override
  Future<List<ActivityItem>> build() async {
    _currentPage = 1;
    _hasMore = true;
    return _fetchPage(1);
  }

  Future<List<ActivityItem>> _fetchPage(int page) async {
    final repository = ref.read(crossOrgRepositoryProvider);
    final items = await repository.getActivityFeed(page: page);
    _hasMore = items.length >= 20;
    return items;
  }

  Future<void> loadMore() async {
    if (!_hasMore) return;

    final currentItems = state.valueOrNull ?? [];
    _currentPage++;
    final newItems = await _fetchPage(_currentPage);
    state = AsyncValue.data([...currentItems, ...newItems]);
  }

  Future<void> refresh() async {
    ref.invalidateSelf();
  }
}
```

### 6.4 Key Screens

```dart
// lib/features/user/presentation/screens/privacy/privacy_dashboard_screen.dart

class PrivacyDashboardScreen extends ConsumerWidget {
  const PrivacyDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final privacyAsync = ref.watch(privacyDashboardProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Privacy')),
      body: privacyAsync.when(
        data: (dashboard) => _buildContent(context, ref, dashboard),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => ErrorWidget(e.toString()),
      ),
    );
  }

  Widget _buildContent(BuildContext context, WidgetRef ref, PrivacyDashboard dashboard) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Privacy Score Card
        _PrivacyScoreCard(score: dashboard.privacyScore),
        const SizedBox(height: 24),

        // Recommendations
        if (dashboard.recommendations.isNotEmpty) ...[
          Text('Recommendations', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ...dashboard.recommendations.map((r) => _RecommendationTile(
            recommendation: r,
            onTap: () => _handleRecommendation(context, r),
          )),
          const SizedBox(height: 24),
        ],

        // Organization Access
        Text('Organization Data Access', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        ...dashboard.orgAccess.map((org) => _OrgAccessCard(
          orgAccess: org,
          onManage: () => _navigateToOrgPermissions(context, org.organization),
        )),
        const SizedBox(height: 24),

        // Data Actions
        Text('Your Data', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        ListTile(
          leading: const Icon(Icons.download),
          title: const Text('Export All My Data'),
          subtitle: const Text('Download a copy of all your data'),
          onTap: () => _requestDataExport(context, ref),
        ),
        ListTile(
          leading: const Icon(Icons.delete_forever, color: Colors.red),
          title: const Text('Delete My Account'),
          subtitle: const Text('Permanently delete your account and all data'),
          onTap: () => _confirmAccountDeletion(context, ref),
        ),
      ],
    );
  }
}

class _PrivacyScoreCard extends StatelessWidget {
  final int score;

  const _PrivacyScoreCard({required this.score});

  @override
  Widget build(BuildContext context) {
    final color = score >= 80 ? Colors.green
                : score >= 60 ? Colors.orange
                : Colors.red;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            SizedBox(
              width: 120,
              height: 120,
              child: Stack(
                alignment: Alignment.center,
                children: [
                  CircularProgressIndicator(
                    value: score / 100,
                    strokeWidth: 12,
                    backgroundColor: Colors.grey.shade200,
                    valueColor: AlwaysStoppedAnimation(color),
                  ),
                  Text(
                    '$score',
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Text(
              'Privacy Score',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            Text(
              _getScoreDescription(score),
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }

  String _getScoreDescription(int score) {
    if (score >= 80) return 'Excellent! Your privacy is well protected.';
    if (score >= 60) return 'Good, but there\'s room for improvement.';
    return 'Consider enabling more privacy features.';
  }
}
```

```dart
// lib/features/user/presentation/screens/devices/devices_screen.dart

class DevicesScreen extends ConsumerWidget {
  const DevicesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final devicesAsync = ref.watch(devicesNotifierProvider);
    final pendingDevices = ref.watch(pendingDevicesProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Devices'),
        actions: [
          PopupMenuButton(
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'sign_out_all',
                child: Text('Sign out all other devices'),
              ),
            ],
            onSelected: (value) {
              if (value == 'sign_out_all') {
                _confirmSignOutAll(context, ref);
              }
            },
          ),
        ],
      ),
      body: devicesAsync.when(
        data: (devices) => _buildDeviceList(context, ref, devices, pendingDevices),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => ErrorWidget(e.toString()),
      ),
    );
  }

  Widget _buildDeviceList(
    BuildContext context,
    WidgetRef ref,
    List<UserDevice> devices,
    List<UserDevice> pending,
  ) {
    final trusted = devices.where((d) => d.isTrusted).toList();
    final other = devices.where((d) => !d.isTrusted && d.approvalStatus != 'pending').toList();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Pending Approvals Banner
        if (pending.isNotEmpty) ...[
          Card(
            color: Colors.orange.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.warning_amber, color: Colors.orange),
                      const SizedBox(width: 8),
                      Text(
                        '${pending.length} device(s) awaiting approval',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ...pending.map((d) => _PendingDeviceTile(
                    device: d,
                    onApprove: () => ref.read(devicesNotifierProvider.notifier)
                        .approveDevice(d.name, true),
                    onDeny: () => ref.read(devicesNotifierProvider.notifier)
                        .approveDevice(d.name, false),
                  )),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],

        // Trusted Devices
        Text('Trusted Devices', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        ...trusted.map((d) => DeviceCard(
          device: d,
          onRevoke: () => _confirmRevoke(context, ref, d),
        )),

        // Other Devices
        if (other.isNotEmpty) ...[
          const SizedBox(height: 24),
          Text('Other Devices', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ...other.map((d) => DeviceCard(
            device: d,
            onTrust: () => ref.read(devicesNotifierProvider.notifier)
                .trustDevice(d.name),
          )),
        ],
      ],
    );
  }
}
```

### 6.5 Platform-Specific Implementations

```dart
// lib/features/user/services/biometric_service.dart

import 'package:local_auth/local_auth.dart';

class BiometricService {
  final LocalAuthentication _auth = LocalAuthentication();

  Future<bool> isAvailable() async {
    return await _auth.canCheckBiometrics || await _auth.isDeviceSupported();
  }

  Future<List<BiometricType>> getAvailableTypes() async {
    return await _auth.getAvailableBiometrics();
  }

  Future<bool> authenticate({String reason = 'Authenticate to continue'}) async {
    try {
      return await _auth.authenticate(
        localizedReason: reason,
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: false,
        ),
      );
    } catch (e) {
      return false;
    }
  }
}
```

```dart
// lib/features/user/services/device_info_service.dart

import 'dart:io';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:uuid/uuid.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class DeviceInfoService {
  final DeviceInfoPlugin _deviceInfo = DeviceInfoPlugin();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static const _deviceIdKey = 'dartwing_device_id';

  Future<Map<String, dynamic>> getDeviceInfo() async {
    final deviceId = await _getOrCreateDeviceId();

    if (Platform.isIOS) {
      final info = await _deviceInfo.iosInfo;
      return {
        'device_id': deviceId,
        'device_name': info.name,
        'device_type': 'mobile_ios',
        'os_name': 'iOS',
        'os_version': info.systemVersion,
        'model': info.model,
      };
    } else if (Platform.isAndroid) {
      final info = await _deviceInfo.androidInfo;
      return {
        'device_id': deviceId,
        'device_name': '${info.brand} ${info.model}',
        'device_type': 'mobile_android',
        'os_name': 'Android',
        'os_version': info.version.release,
        'model': info.model,
      };
    } else if (Platform.isMacOS) {
      final info = await _deviceInfo.macOsInfo;
      return {
        'device_id': deviceId,
        'device_name': info.computerName,
        'device_type': 'desktop_macos',
        'os_name': 'macOS',
        'os_version': info.osRelease,
      };
    } else if (Platform.isWindows) {
      final info = await _deviceInfo.windowsInfo;
      return {
        'device_id': deviceId,
        'device_name': info.computerName,
        'device_type': 'desktop_windows',
        'os_name': 'Windows',
        'os_version': info.productName,
      };
    } else if (Platform.isLinux) {
      final info = await _deviceInfo.linuxInfo;
      return {
        'device_id': deviceId,
        'device_name': info.prettyName,
        'device_type': 'desktop_linux',
        'os_name': 'Linux',
        'os_version': info.version ?? 'Unknown',
      };
    }

    // Web fallback
    return {
      'device_id': deviceId,
      'device_type': 'web',
      'os_name': 'Web',
    };
  }

  Future<String> _getOrCreateDeviceId() async {
    String? deviceId = await _storage.read(key: _deviceIdKey);

    if (deviceId == null) {
      deviceId = const Uuid().v4();
      await _storage.write(key: _deviceIdKey, value: deviceId);
    }

    return deviceId;
  }
}
```

---

## 7. Security & Privacy Architecture

### 7.1 Permission Model

User module doctypes have **owner-only** access by default:

```python
# dartwing_user/permissions.py

def has_permission(doc, ptype, user):
    """
    User module doctypes are strictly personal.
    Only the owning user can access their own data.
    """
    # System Manager always has access
    if "System Manager" in frappe.get_roles(user):
        return True

    # Get person for current user
    person = get_person_for_user(user)
    if not person:
        return False

    # Owner-only doctypes
    owner_only_doctypes = [
        "User Profile",
        "User Device",
        "AI Voice Profile",
        "Digital Will",
        "Personal Vault Item",
        "Verification Record",
        "AI Memory Entry",
        "Reputation Score",
        "User Block",
    ]

    if doc.doctype in owner_only_doctypes:
        return doc.person == person

    # User Session - owner only
    if doc.doctype == "User Session":
        device = frappe.get_doc("User Device", doc.device)
        return device.person == person

    # Privacy Setting - owner can manage
    if doc.doctype == "Privacy Setting":
        return doc.person == person

    # Notification Preference - owner can manage
    if doc.doctype == "Notification Preference":
        return doc.person == person

    # User Location Share - owner or recipient
    if doc.doctype == "User Location Share":
        if doc.person == person:
            return True
        if ptype == "read":
            if doc.shared_with_person == person:
                return True
            if doc.shared_with_org:
                return is_org_member(person, doc.shared_with_org)
        return False

    # User Invite - inviter or invitee
    if doc.doctype == "User Invite":
        if doc.inviter == person:
            return True
        if ptype == "read" and doc.email == get_user_email(user):
            return True
        return False

    return False


def get_permission_query_conditions(user):
    """
    SQL conditions for list views.
    Returns only the current user's records.
    """
    if "System Manager" in frappe.get_roles(user):
        return ""

    person = get_person_for_user(user)
    if not person:
        return "1=0"  # No access

    return f"`person` = '{person}'"
```

### 7.2 Data Access Matrix

| Doctype             | Owner | Org Admin         | Other User        | System |
| ------------------- | ----- | ----------------- | ----------------- | ------ |
| User Profile        | Full  | None              | None              | Full   |
| User Device         | Full  | None              | None              | Full   |
| User Session        | Full  | None              | None              | Full   |
| User Block          | Full  | None              | None              | Full   |
| AI Voice Profile    | Full  | None              | None              | Full   |
| Digital Will        | Full  | None              | None              | Full   |
| Personal Vault Item | Full  | None              | None              | Full   |
| Emergency Contact   | Full  | Read (if visible) | None              | Full   |
| Verification Record | Read  | Read (badge only) | Read (badge only) | Full   |
| Privacy Setting     | Full  | None              | None              | Full   |
| Location Share      | Full  | Read (if shared)  | Read (if shared)  | Full   |
| AI Memory Entry     | Full  | None              | None              | Full   |
| Reputation Score    | Read  | Read (score only) | Read (score only) | Full   |

### 7.3 Encryption Strategy

```python
# dartwing_user/encryption.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class VaultEncryption:
    """
    E2E encryption for Personal Vault items.
    User's encryption key is derived from their password + salt.
    Key is never stored on server.
    """

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key from user password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def generate_salt() -> bytes:
        """Generate random salt for key derivation."""
        return os.urandom(16)

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """Encrypt data with user's key."""
        f = Fernet(key)
        return f.encrypt(data)

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypt data with user's key."""
        f = Fernet(key)
        return f.decrypt(encrypted_data)


class DuressPinHandler:
    """
    Handles duress PIN logic without exposing actual PIN.
    """

    @staticmethod
    def hash_pin(pin: str) -> str:
        """Hash PIN with site-specific salt."""
        import hashlib
        salt = frappe.conf.get("encryption_key", "dartwing")[:16]
        return hashlib.pbkdf2_hmac(
            'sha256',
            pin.encode(),
            salt.encode(),
            100000
        ).hex()

    @staticmethod
    def verify_duress(person: str, pin: str) -> bool:
        """
        Check if PIN matches duress PIN.
        Returns True if this IS the duress PIN (user is being coerced).
        """
        profile = frappe.get_doc("User Profile", {"person": person})
        if not profile.duress_pin_hash:
            return False

        return DuressPinHandler.hash_pin(pin) == profile.duress_pin_hash
```

### 7.4 Audit Logging

```python
# dartwing_user/audit.py

import frappe
from datetime import datetime

SECURITY_EVENTS = [
    "device_registered",
    "device_trusted",
    "device_revoked",
    "device_approval_requested",
    "device_approved",
    "device_denied",
    "travel_mode_enabled",
    "travel_mode_disabled",
    "duress_pin_entered",
    "data_export_requested",
    "account_deletion_requested",
    "account_deletion_cancelled",
    "digital_will_activated",
    "digital_will_access_granted",
    "vault_item_accessed",
    "vault_item_shared",
    "verification_completed",
    "block_added",
    "block_removed",
    "privacy_setting_changed",
]

def log_security_event(event_type: str, person: str, details: dict = None, severity: str = "info"):
    """
    Log security event for audit trail.
    """
    if event_type not in SECURITY_EVENTS:
        frappe.throw(f"Unknown security event type: {event_type}")

    frappe.get_doc({
        "doctype": "User Security Log",
        "person": person,
        "event_type": event_type,
        "severity": severity,
        "timestamp": datetime.now(),
        "ip_address": frappe.local.request_ip if hasattr(frappe.local, 'request_ip') else None,
        "user_agent": frappe.request.headers.get('User-Agent') if frappe.request else None,
        "details": frappe.as_json(details) if details else None,
    }).insert(ignore_permissions=True)

    # Critical events trigger immediate notification
    if severity == "critical":
        notify_security_team(event_type, person, details)


def notify_security_team(event_type: str, person: str, details: dict):
    """Send immediate notification for critical security events."""
    # Send to configured security contacts
    frappe.enqueue(
        'dartwing_user.notifications.send_security_alert',
        event_type=event_type,
        person=person,
        details=details,
        queue='critical'
    )
```

---

## 8. External Service Integrations

### 8.1 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL INTEGRATIONS                                │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Voice Clone    │  │  IDV Providers  │  │  Push Services  │             │
│  │                 │  │                 │  │                 │             │
│  │  • ElevenLabs   │  │  • Persona      │  │  • APNs         │             │
│  │  • Play.ht      │  │  • Jumio        │  │  • FCM          │             │
│  │                 │  │  • Onfido       │  │                 │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                       │
│           ▼                    ▼                    ▼                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Integration Layer                               │   │
│  │                                                                      │   │
│  │  VoiceCloneProvider  |  IDVProvider  |  PushProvider                │   │
│  │  (abstract)          |  (abstract)   |  (abstract)                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Health Data    │  │  Geolocation    │  │  Email/SMS      │             │
│  │                 │  │                 │  │                 │             │
│  │  • Apple Health │  │  • IP Geoloc    │  │  • SendGrid     │             │
│  │  • Google Fit   │  │  • MaxMind      │  │  • Twilio       │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Voice Clone Integration

```python
# dartwing_user/integrations/voice_clone.py

from abc import ABC, abstractmethod
import requests

class VoiceCloneProvider(ABC):
    """Abstract base for voice clone providers."""

    @abstractmethod
    def upload_sample(self, audio_data: bytes, format: str) -> str:
        """Upload voice sample, return sample ID."""
        pass

    @abstractmethod
    def start_training(self, sample_id: str, name: str) -> str:
        """Start voice training, return model ID."""
        pass

    @abstractmethod
    def check_training_status(self, model_id: str) -> dict:
        """Check training status."""
        pass

    @abstractmethod
    def generate_audio(self, model_id: str, text: str) -> bytes:
        """Generate audio from text using trained model."""
        pass

    @abstractmethod
    def delete_model(self, model_id: str) -> bool:
        """Delete voice model."""
        pass


class ElevenLabsProvider(VoiceCloneProvider):
    """ElevenLabs voice clone implementation."""

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self):
        self.api_key = frappe.conf.get("elevenlabs_api_key")
        if not self.api_key:
            frappe.throw("ElevenLabs API key not configured")

    def _headers(self):
        return {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def upload_sample(self, audio_data: bytes, format: str) -> str:
        # ElevenLabs accepts sample during voice creation
        return None  # Sample uploaded during training

    def start_training(self, sample_id: str, name: str, audio_data: bytes) -> str:
        """Create voice clone with instant voice cloning."""
        url = f"{self.BASE_URL}/voices/add"

        files = {
            'files': (f'sample.mp3', audio_data, 'audio/mpeg'),
        }
        data = {
            'name': name,
            'description': f'Dartwing voice clone for {name}',
        }

        response = requests.post(
            url,
            headers={"xi-api-key": self.api_key},
            files=files,
            data=data,
        )
        response.raise_for_status()

        return response.json()['voice_id']

    def check_training_status(self, model_id: str) -> dict:
        """ElevenLabs instant cloning is immediate."""
        return {"status": "completed", "model_id": model_id}

    def generate_audio(self, model_id: str, text: str,
                       stability: float = 0.5,
                       similarity_boost: float = 0.75) -> bytes:
        url = f"{self.BASE_URL}/text-to-speech/{model_id}"

        response = requests.post(
            url,
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                }
            }
        )
        response.raise_for_status()

        return response.content

    def delete_model(self, model_id: str) -> bool:
        url = f"{self.BASE_URL}/voices/{model_id}"
        response = requests.delete(url, headers=self._headers())
        return response.status_code == 200


def get_voice_provider() -> VoiceCloneProvider:
    """Factory to get configured voice clone provider."""
    provider = frappe.conf.get("voice_clone_provider", "elevenlabs")

    if provider == "elevenlabs":
        return ElevenLabsProvider()
    elif provider == "playht":
        return PlayHTProvider()
    else:
        frappe.throw(f"Unknown voice clone provider: {provider}")
```

### 8.3 Identity Verification Integration

```python
# dartwing_user/integrations/idv.py

from abc import ABC, abstractmethod

class IDVProvider(ABC):
    """Abstract base for identity verification providers."""

    @abstractmethod
    def create_verification(self, person: str, level: str) -> dict:
        """Create verification session, return {session_id, redirect_url}."""
        pass

    @abstractmethod
    def check_status(self, session_id: str) -> dict:
        """Check verification status."""
        pass

    @abstractmethod
    def handle_webhook(self, payload: dict) -> dict:
        """Handle webhook callback from provider."""
        pass


class PersonaProvider(IDVProvider):
    """Persona identity verification implementation."""

    BASE_URL = "https://withpersona.com/api/v1"

    def __init__(self):
        self.api_key = frappe.conf.get("persona_api_key")
        self.template_id = frappe.conf.get("persona_template_id")

    def create_verification(self, person: str, level: str) -> dict:
        """Create Persona inquiry."""
        import requests

        person_doc = frappe.get_doc("Person", person)

        # Select template based on verification level
        template_id = self._get_template_for_level(level)

        response = requests.post(
            f"{self.BASE_URL}/inquiries",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "data": {
                    "type": "inquiry",
                    "attributes": {
                        "inquiry-template-id": template_id,
                        "reference-id": person,
                        "fields": {
                            "name-first": person_doc.first_name,
                            "name-last": person_doc.last_name,
                            "email-address": person_doc.primary_email,
                        }
                    }
                }
            }
        )
        response.raise_for_status()

        data = response.json()['data']
        return {
            "session_id": data['id'],
            "redirect_url": data['attributes']['redirect-url'],
        }

    def check_status(self, session_id: str) -> dict:
        import requests

        response = requests.get(
            f"{self.BASE_URL}/inquiries/{session_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()

        data = response.json()['data']['attributes']

        return {
            "status": data['status'],  # pending, completed, failed, expired
            "verification_level": self._map_status_to_level(data),
        }

    def handle_webhook(self, payload: dict) -> dict:
        """Process Persona webhook."""
        event_type = payload['data']['attributes']['name']
        inquiry_id = payload['data']['attributes']['payload']['data']['id']

        if event_type == 'inquiry.completed':
            return self._process_completed(inquiry_id, payload)
        elif event_type == 'inquiry.failed':
            return self._process_failed(inquiry_id, payload)

        return {"processed": False}

    def _get_template_for_level(self, level: str) -> str:
        templates = frappe.conf.get("persona_templates", {})
        return templates.get(level, self.template_id)

    def _map_status_to_level(self, data: dict) -> str:
        # Map Persona verification checks to our levels
        checks = data.get('checks', [])

        has_email = any(c.get('name') == 'email_verified' and c.get('status') == 'passed' for c in checks)
        has_phone = any(c.get('name') == 'phone_verified' and c.get('status') == 'passed' for c in checks)
        has_id = any(c.get('name') == 'government_id' and c.get('status') == 'passed' for c in checks)
        has_address = any(c.get('name') == 'address_verified' and c.get('status') == 'passed' for c in checks)
        has_liveness = any(c.get('name') == 'selfie' and c.get('status') == 'passed' for c in checks)

        if has_id and has_address and has_liveness:
            return 'enhanced'
        elif has_id:
            return 'standard'
        elif has_email and has_phone:
            return 'basic'

        return 'none'


def get_idv_provider() -> IDVProvider:
    """Factory to get configured IDV provider."""
    provider = frappe.conf.get("idv_provider", "persona")

    if provider == "persona":
        return PersonaProvider()
    elif provider == "jumio":
        return JumioProvider()
    elif provider == "onfido":
        return OnfidoProvider()
    else:
        frappe.throw(f"Unknown IDV provider: {provider}")
```

---

## 9. Background Jobs & Scheduled Tasks

### 9.1 Scheduled Jobs Configuration

```python
# dartwing_user/hooks.py

scheduler_events = {
    # Every minute
    "cron": {
        "* * * * *": [
            "dartwing_user.tasks.location.broadcast_active_locations",
        ],
    },

    # Every hour
    "hourly": [
        "dartwing_user.tasks.sessions.cleanup_expired_sessions",
        "dartwing_user.tasks.devices.recalculate_trust_scores",
    ],

    # Daily at midnight
    "daily": [
        "dartwing_user.tasks.digital_will.check_inactivity",
        "dartwing_user.tasks.travel_mode.auto_disable_expired",
        "dartwing_user.tasks.privacy.process_scheduled_deletions",
        "dartwing_user.tasks.metrics.update_privacy_scores",
        "dartwing_user.tasks.verification.check_expiring_verifications",
    ],

    # Weekly on Sunday
    "weekly": [
        "dartwing_user.tasks.cleanup.purge_old_sessions",
        "dartwing_user.tasks.cleanup.purge_old_locations",
        "dartwing_user.tasks.reports.generate_security_report",
    ],
}
```

### 9.2 Key Background Tasks

```python
# dartwing_user/tasks/digital_will.py

import frappe
from datetime import datetime, timedelta

def check_inactivity():
    """
    Daily job to check digital will inactivity thresholds.
    Sends warnings and activates wills as needed.
    """
    active_wills = frappe.get_all(
        "Digital Will",
        filters={"status": ["in", ["active", "warning_sent"]]},
        fields=["name", "person", "inactive_days", "warning_threshold_percent",
                "second_warning_percent", "last_activity_at", "warnings_sent_count"]
    )

    for will_data in active_wills:
        will = frappe.get_doc("Digital Will", will_data.name)
        person = will.person

        # Get last activity from User Profile
        profile = frappe.get_doc("User Profile", {"person": person})
        last_activity = profile.last_activity or will.last_activity_at

        if not last_activity:
            continue

        days_inactive = (datetime.now() - last_activity).days
        threshold = will.inactive_days

        # Calculate warning thresholds
        first_warning_days = int(threshold * will.warning_threshold_percent / 100)
        second_warning_days = int(threshold * will.second_warning_percent / 100)

        # Check if threshold reached
        if days_inactive >= threshold:
            _activate_digital_will(will)
        elif days_inactive >= second_warning_days and will.warnings_sent_count < 2:
            _send_inactivity_warning(will, person, days_inactive, 2)
        elif days_inactive >= first_warning_days and will.warnings_sent_count < 1:
            _send_inactivity_warning(will, person, days_inactive, 1)


def _send_inactivity_warning(will, person: str, days_inactive: int, warning_number: int):
    """Send warning notification to user."""
    from dartwing_user.services.notification import NotificationService

    person_doc = frappe.get_doc("Person", person)

    NotificationService.send(
        person=person,
        title="Digital Will Inactivity Warning",
        message=f"You haven't been active for {days_inactive} days. "
                f"Your digital will may be activated in {will.inactive_days - days_inactive} days.",
        category="security",
        priority="high",
        channels=["push", "email", "sms"]
    )

    will.warnings_sent_count = warning_number
    will.last_warning_at = datetime.now()
    will.save(ignore_permissions=True)


def _activate_digital_will(will):
    """Activate digital will and notify trustees."""
    will.status = "requested"
    will.requested_at = datetime.now()
    will.save(ignore_permissions=True)

    # Notify all trustees
    for trustee in will.trustees:
        from dartwing_user.services.notification import NotificationService

        NotificationService.send(
            person=trustee.trustee_person,
            title="Digital Will Access Available",
            message=f"Your contact has been inactive. You may request access to their account.",
            category="security",
            priority="critical",
            channels=["push", "email", "sms"],
            action_url=f"/digital-will/request/{will.name}"
        )

        trustee.notified_at = datetime.now()

    will.save(ignore_permissions=True)

    # Log security event
    from dartwing_user.audit import log_security_event
    log_security_event(
        "digital_will_activated",
        person=will.person,
        details={"will": will.name},
        severity="critical"
    )
```

```python
# dartwing_user/tasks/metrics.py

import frappe

def update_privacy_scores():
    """
    Daily job to recalculate privacy scores for all users.
    """
    profiles = frappe.get_all(
        "User Profile",
        fields=["name", "person"]
    )

    for profile_data in profiles:
        try:
            score = calculate_privacy_score(profile_data.person)
            frappe.db.set_value(
                "User Profile",
                profile_data.name,
                "privacy_score",
                score
            )
        except Exception as e:
            frappe.log_error(f"Failed to update privacy score for {profile_data.person}: {e}")

    frappe.db.commit()


def calculate_privacy_score(person: str) -> int:
    """
    Calculate privacy score based on enabled features.
    Returns 0-100.
    """
    score = 0
    max_score = 100

    profile = frappe.get_doc("User Profile", {"person": person})

    # Biometric enabled (+10)
    if profile.biometric_enabled:
        score += 10

    # Push approval required (+15)
    if profile.push_approval_required:
        score += 15

    # Travel mode configured (+10)
    if profile.duress_pin_hash:
        score += 10

    # Check MFA in Keycloak (+15)
    if has_mfa_enabled(person):
        score += 15

    # Identity verification level
    verification = frappe.db.get_value(
        "Verification Record",
        {"person": person},
        "level"
    )
    if verification == "enhanced":
        score += 15
    elif verification == "standard":
        score += 10
    elif verification == "basic":
        score += 5

    # Digital will configured (+10)
    if frappe.db.exists("Digital Will", {"person": person, "status": "active"}):
        score += 10

    # Emergency contacts set (+5)
    if profile.emergency_contacts:
        score += 5

    # Privacy settings customized (+10)
    custom_settings = frappe.db.count(
        "Privacy Setting",
        {"person": person}
    )
    if custom_settings > 0:
        score += 10

    return min(score, max_score)
```

---

## 10. Implementation Patterns

### 10.1 Service Pattern

All business logic goes through services:

```python
# Pattern: Service encapsulates business logic
# API → Service → Repository → Database

# Good ✓
@frappe.whitelist()
def toggle_travel_mode(enabled: bool, config: Dict = None):
    person = get_person_for_current_user()
    if enabled:
        TravelModeService.enable(person, config)
    else:
        TravelModeService.disable(person)

# Bad ✗ - Logic in API
@frappe.whitelist()
def toggle_travel_mode(enabled: bool):
    person = get_person_for_current_user()
    profile = frappe.get_doc("User Profile", {"person": person})
    profile.travel_mode = enabled
    profile.save()  # Missing audit, notifications, etc.
```

### 10.2 Owner Verification Pattern

Always verify document ownership:

```python
def verify_ownership(doctype: str, name: str, person: str) -> bool:
    """Verify the current user owns this document."""
    doc = frappe.get_doc(doctype, name)

    if hasattr(doc, 'person'):
        return doc.person == person
    elif hasattr(doc, 'owner_person'):
        return doc.owner_person == person

    return False

# Usage in API
@frappe.whitelist()
def delete_vault_item(item_name: str):
    person = get_person_for_current_user()

    if not verify_ownership("Personal Vault Item", item_name, person):
        frappe.throw("Not your vault item", frappe.PermissionError)

    VaultService.delete(item_name)
```

### 10.3 Cross-Org Query Pattern

For cross-org features, always filter by user's organizations:

```python
def get_user_organizations(person: str) -> list:
    """Get all organizations the person is a member of."""
    return frappe.get_all(
        "Org Member",
        filters={"person": person, "status": "Active"},
        pluck="organization"
    )

def cross_org_search(person: str, query: str) -> list:
    """Search across all user's organizations."""
    orgs = get_user_organizations(person)

    if not orgs:
        return []

    # Build OR conditions for each org
    results = []
    for org in orgs:
        org_results = frappe.get_all(
            "Task",  # Example doctype
            filters={
                "organization": org,
                "subject": ["like", f"%{query}%"]
            },
            fields=["name", "subject", "organization"]
        )
        results.extend(org_results)

    return results
```

### 10.4 Privacy-Aware Data Access Pattern

Always check privacy settings before returning data to organizations:

```python
def get_person_data_for_org(person: str, organization: str, data_types: list) -> dict:
    """
    Get person data respecting privacy settings.
    """
    result = {}

    for data_type in data_types:
        # Check if person allows this org to see this data type
        setting = frappe.db.get_value(
            "Privacy Setting",
            {"person": person, "organization": organization, "data_type": data_type},
            "is_allowed"
        )

        # Default to allowed if no explicit setting
        if setting is None:
            setting = True

        if setting:
            result[data_type] = get_data(person, data_type)
        else:
            result[data_type] = None  # Hidden

    return result
```

### 10.5 Async Job Pattern

Use background jobs for long-running operations:

```python
@frappe.whitelist()
def request_data_export():
    """Queue data export job."""
    person = get_person_for_current_user()

    # Create export request record
    export_id = create_export_request(person)

    # Queue background job
    frappe.enqueue(
        'dartwing_user.tasks.privacy.generate_data_export',
        person=person,
        export_id=export_id,
        queue='long',
        timeout=3600  # 1 hour max
    )

    return {"export_id": export_id, "status": "queued"}

# In tasks/privacy.py
def generate_data_export(person: str, export_id: str):
    """Background job to generate data export."""
    try:
        # Collect all user data
        data = collect_all_user_data(person)

        # Generate ZIP file
        zip_path = create_export_zip(data)

        # Store and notify
        update_export_request(export_id, "completed", zip_path)
        send_export_ready_notification(person, export_id)

    except Exception as e:
        update_export_request(export_id, "failed", str(e))
        frappe.log_error(f"Data export failed for {person}: {e}")
```

---

## 11. Migration & Deployment

### 11.1 Module Installation

```python
# dartwing_user/install.py

def after_install():
    """Post-installation setup."""
    # Create default roles
    create_roles()

    # Set up scheduled jobs
    setup_scheduler()

    # Create system settings
    create_default_settings()

    # Migrate existing users
    migrate_existing_users()


def create_roles():
    """Create User module specific roles."""
    roles = [
        {"role_name": "Dartwing User", "desk_access": 1},
        {"role_name": "Dartwing Guest", "desk_access": 0},
    ]

    for role in roles:
        if not frappe.db.exists("Role", role["role_name"]):
            frappe.get_doc({
                "doctype": "Role",
                **role
            }).insert(ignore_permissions=True)


def migrate_existing_users():
    """
    Create User Profile for any Person that doesn't have one.
    Run during upgrade from pre-User-module version.
    """
    persons_without_profile = frappe.db.sql("""
        SELECT p.name
        FROM `tabPerson` p
        LEFT JOIN `tabUser Profile` up ON up.person = p.name
        WHERE up.name IS NULL
    """, as_dict=True)

    for person in persons_without_profile:
        frappe.get_doc({
            "doctype": "User Profile",
            "person": person.name,
            "theme": "system",
            "language": "en",
            "timezone": "UTC",
        }).insert(ignore_permissions=True)

    frappe.db.commit()
```

### 11.2 Database Migrations

```python
# dartwing_user/patches/v1_1/add_trust_score_factors.py

import frappe

def execute():
    """Add trust score factor fields to User Device."""

    # Check if already migrated
    if frappe.db.has_column("User Device", "factor_device_age"):
        return

    # Add columns
    frappe.db.sql("""
        ALTER TABLE `tabUser Device`
        ADD COLUMN `factor_device_age` INT DEFAULT 0,
        ADD COLUMN `factor_login_frequency` INT DEFAULT 0,
        ADD COLUMN `factor_location_consistency` INT DEFAULT 0,
        ADD COLUMN `factor_biometric_enabled` INT DEFAULT 0,
        ADD COLUMN `factor_os_updated` INT DEFAULT 0,
        ADD COLUMN `factor_no_failures` INT DEFAULT 0,
        ADD COLUMN `factor_mfa_enabled` INT DEFAULT 0
    """)

    # Recalculate scores for existing devices
    devices = frappe.get_all("User Device", pluck="name")
    for device in devices:
        from dartwing_user.services.device_trust import DeviceTrustService
        DeviceTrustService.calculate_trust_score(device)
```

### 11.3 Configuration

```python
# site_config.json additions for User module

{
    # Voice clone provider
    "voice_clone_provider": "elevenlabs",
    "elevenlabs_api_key": "sk-xxx",

    # Identity verification provider
    "idv_provider": "persona",
    "persona_api_key": "xxx",
    "persona_templates": {
        "basic": "tmpl_basic",
        "standard": "tmpl_standard",
        "enhanced": "tmpl_enhanced"
    },

    # Push notifications
    "apns_key_id": "xxx",
    "apns_team_id": "xxx",
    "apns_bundle_id": "io.dartwing.app",
    "fcm_server_key": "xxx",

    # Encryption
    "encryption_key": "32-byte-key-here",

    # Feature flags
    "user_features": {
        "voice_clone_enabled": true,
        "vault_enabled": true,
        "digital_will_enabled": true,
        "health_data_enabled": false
    }
}
```

---

## 12. Appendices

### Appendix A: Complete Doctype List

| Doctype                 | Type        | Naming     | Key Links            |
| ----------------------- | ----------- | ---------- | -------------------- |
| User Profile            | Master      | UP-.#####  | Person (1:1)         |
| User Device             | Master      | hash       | Person               |
| User Session            | Master      | hash       | Person, User Device  |
| User Shortcut           | Child Table | -          | User Profile         |
| User Block              | Master      | hash       | Person (owner)       |
| User Location Share     | Master      | hash       | Person               |
| AI Voice Profile        | Master      | AVP-.##### | Person (1:1)         |
| Digital Will            | Master      | DW-.#####  | Person (1:1)         |
| Digital Will Trustee    | Child Table | -          | Digital Will         |
| Personal Vault Item     | Master      | hash       | Person               |
| Emergency Contact       | Child Table | -          | User Profile         |
| Verification Record     | Master      | VRF-.##### | Person               |
| Privacy Setting         | Master      | hash       | Person, Organization |
| AI Memory Entry         | Master      | hash       | Person               |
| Reputation Score        | Master      | hash       | Person (1:1)         |
| Notification Preference | Master      | hash       | Person, Organization |
| User Invite             | Master      | hash       | Organization, Person |
| User Security Log       | Master      | hash       | Person               |

### Appendix B: API Endpoint Quick Reference

```
# Profile
GET  /api/method/dartwing_user.api.profile.get_my_profile
POST /api/method/dartwing_user.api.profile.update_preferences
POST /api/method/dartwing_user.api.profile.upload_avatar

# Devices
GET  /api/method/dartwing_user.api.devices.get_my_devices
POST /api/method/dartwing_user.api.devices.register_device
POST /api/method/dartwing_user.api.devices.trust_device
POST /api/method/dartwing_user.api.devices.revoke_device
POST /api/method/dartwing_user.api.devices.approve_pending_device
POST /api/method/dartwing_user.api.devices.sign_out_all_devices

# Privacy
GET  /api/method/dartwing_user.api.privacy.get_privacy_dashboard
PUT  /api/method/dartwing_user.api.privacy.update_privacy_setting
POST /api/method/dartwing_user.api.privacy.request_data_export
POST /api/method/dartwing_user.api.privacy.request_account_deletion
POST /api/method/dartwing_user.api.privacy.cancel_deletion

# Security
POST /api/method/dartwing_user.api.security.toggle_travel_mode
GET  /api/method/dartwing_user.api.security.get_sessions
DEL  /api/method/dartwing_user.api.security.end_session

# Cross-Org
POST /api/method/dartwing_user.api.cross_org.search
GET  /api/method/dartwing_user.api.cross_org.get_activity_feed
GET  /api/method/dartwing_user.api.cross_org.get_organizations

# Features
GET  /api/method/dartwing_user.api.briefing.get_daily
GET  /api/method/dartwing_user.api.vault.list
POST /api/method/dartwing_user.api.vault.upload
POST /api/method/dartwing_user.api.verification.start
GET  /api/method/dartwing_user.api.will.get
```

### Appendix C: Flutter Package Dependencies

```yaml
# pubspec.yaml additions for User module

dependencies:
  # State Management
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0

  # Data
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

  # Storage
  flutter_secure_storage: ^9.0.0
  hive_flutter: ^1.1.0

  # Auth & Security
  local_auth: ^2.1.0

  # Device Info
  device_info_plus: ^9.0.0

  # Location
  geolocator: ^10.0.0

  # Push Notifications
  firebase_messaging: ^14.0.0
  flutter_local_notifications: ^16.0.0

  # File Handling
  file_picker: ^6.0.0
  path_provider: ^2.1.0

  # UI
  cached_network_image: ^3.3.0
  flutter_svg: ^2.0.0

dev_dependencies:
  riverpod_generator: ^2.3.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  build_runner: ^2.4.0
```

### Appendix D: Glossary

| Term               | Definition                                            |
| ------------------ | ----------------------------------------------------- |
| Person             | Master identity record in Core module                 |
| User Profile       | Personal preferences in User module (1:1 with Person) |
| Trust Score        | 0-100 calculated device trustworthiness               |
| Travel Mode        | Security mode hiding sensitive data while traveling   |
| Duress PIN         | Secondary PIN showing decoy data under coercion       |
| Digital Will       | Emergency access grant after inactivity               |
| Personal Vault     | E2E encrypted document storage                        |
| Cross-Org          | Features working across multiple organizations        |
| Privacy Score      | 0-100 rating of enabled privacy features              |
| Verification Level | Basic/Standard/Enhanced identity verification tier    |

### Appendix E: Architecture Cross-Reference

| Topic                   | Reference Document               |
| ----------------------- | -------------------------------- |
| Person doctype          | dartwing_core_arch.md, Section 3 |
| Organization model      | dartwing_core_arch.md, Section 3 |
| Keycloak authentication | dartwing_auth_arch.md            |
| Flutter patterns        | dartwing_core_arch.md, Section 4 |
| API conventions         | dartwing_core_arch.md, Section 2 |
| Permission model        | dartwing_core_arch.md, Section 8 |

---

## 13. Key Management System

*Added: November 2025 (Post-Critique Hardening)*

**Issue Sources:** Claude §2.2, Jeni §Vault key handling, Gemi §3.3

### 13.1 Problem Statement

The Personal Vault promises "end-to-end encryption" but the original architecture lacked:
- Key derivation from user credentials
- Key storage strategy (client vs server)
- Key rotation procedures
- Recovery mechanisms when user forgets password
- Storing `encryption_key` in database alongside data is a security weakness

### 13.2 Key Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KEY MANAGEMENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User Password (never leaves client)                                         │
│       │                                                                      │
│       ▼                                                                      │
│  ┌───────────────────────────────────────┐                                  │
│  │ Key Derivation Function (KDF)         │                                  │
│  │ Algorithm: Argon2id                   │                                  │
│  │ Memory: 64MB, Iterations: 3           │                                  │
│  │ Salt: Per-user (stored server-side)   │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│                    ▼                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Key Encryption Key (KEK)              │                                  │
│  │ • Derived client-side from password   │                                  │
│  │ • Used to encrypt/decrypt MEK         │                                  │
│  │ • Never stored or transmitted         │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│                    ▼                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Master Encryption Key (MEK)           │                                  │
│  │ • Generated client-side (random)      │                                  │
│  │ • Encrypted with KEK before storage   │                                  │
│  │ • Stored server-side (encrypted)      │                                  │
│  │ • Never exists in plaintext on server │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│                    ▼                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Data Encryption Keys (DEKs)           │                                  │
│  │ • Per-item unique keys (random)       │                                  │
│  │ • Encrypted with MEK                  │                                  │
│  │ • Stored alongside encrypted data     │                                  │
│  └───────────────────────────────────────┘                                  │
│                                                                              │
│  RECOVERY MECHANISM:                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Shamir's Secret Sharing               │                                  │
│  │ • MEK split into N shares (e.g., 5)   │                                  │
│  │ • K-of-N required for recovery (e.g., 3) │                               │
│  │ • Shares encrypted & sent to trustees │                                  │
│  │ • Integrates with Digital Will        │                                  │
│  └───────────────────────────────────────┘                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 13.3 Security Invariants

| Invariant | Description | Enforcement |
|-----------|-------------|-------------|
| **I-1** | MEK never exists in plaintext on server | Client-side encryption only |
| **I-2** | Password never transmitted to server | KDF runs in Flutter client |
| **I-3** | Key rotation without full re-encryption | Only re-encrypt MEK with new KEK |
| **I-4** | Recovery possible without password | Shamir shares held by trustees |
| **I-5** | Compromise of single trustee insufficient | K-of-N threshold (e.g., 3-of-5) |

### 13.4 New DocTypes

#### User Key Material

```json
{
  "doctype": "User Key Material",
  "module": "Dartwing User",
  "autoname": "field:person",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person", "unique": 1, "reqd": 1},
    {"fieldname": "kdf_salt", "fieldtype": "Data", "length": 64, "hidden": 1},
    {"fieldname": "encrypted_mek", "fieldtype": "Text", "hidden": 1},
    {"fieldname": "mek_version", "fieldtype": "Int", "default": 1},
    {"fieldname": "key_algorithm", "fieldtype": "Data", "default": "AES-256-GCM", "read_only": 1},
    {"fieldname": "kdf_algorithm", "fieldtype": "Data", "default": "Argon2id", "read_only": 1},
    {"fieldname": "kdf_params", "fieldtype": "JSON", "default": "{\"memory_kb\": 65536, \"iterations\": 3, \"parallelism\": 4}"},
    {"fieldname": "key_created", "fieldtype": "Datetime"},
    {"fieldname": "last_rotation", "fieldtype": "Datetime"}
  ],
  "permissions": [{"role": "System Manager", "read": 0, "write": 0, "delete": 0}]
}
```

#### Key Recovery Share

```json
{
  "doctype": "Key Recovery Share",
  "module": "Dartwing User",
  "autoname": "hash",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person", "reqd": 1},
    {"fieldname": "trustee", "fieldtype": "Link", "options": "Person", "reqd": 1},
    {"fieldname": "encrypted_share", "fieldtype": "Text", "hidden": 1},
    {"fieldname": "share_index", "fieldtype": "Int", "reqd": 1},
    {"fieldname": "threshold", "fieldtype": "Int", "reqd": 1},
    {"fieldname": "total_shares", "fieldtype": "Int", "reqd": 1},
    {"fieldname": "mek_version", "fieldtype": "Int"},
    {"fieldname": "status", "fieldtype": "Select", "options": "Active\nRevoked\nUsed", "default": "Active"}
  ],
  "permissions": [{"role": "System Manager", "read": 1, "write": 0, "delete": 0}]
}
```

### 13.5 Key Management Service

```python
# dartwing_user/services/key_management.py

import frappe
import secrets
from dataclasses import dataclass

@dataclass
class KeyMaterial:
    kdf_salt: bytes
    encrypted_mek: bytes
    mek_version: int
    kdf_params: dict

class KeyManagementService:
    """
    Server-side key management for Personal Vault.

    SECURITY MODEL:
    - Server stores: salt, encrypted MEK, recovery shares
    - Server NEVER sees: password, KEK, plaintext MEK
    """

    DEFAULT_KDF_PARAMS = {"memory_kb": 65536, "iterations": 3, "parallelism": 4, "hash_length": 32}
    SALT_LENGTH = 32

    def initialize_key_material(self, person: str) -> KeyMaterial:
        """Initialize key material for new user. Returns salt to client."""
        if frappe.db.exists("User Key Material", {"person": person}):
            frappe.throw("Key material already initialized")

        salt = secrets.token_bytes(self.SALT_LENGTH)

        frappe.get_doc({
            "doctype": "User Key Material",
            "person": person,
            "kdf_salt": salt.hex(),
            "kdf_params": frappe.as_json(self.DEFAULT_KDF_PARAMS),
            "key_created": frappe.utils.now_datetime(),
            "mek_version": 1
        }).insert(ignore_permissions=True)

        return KeyMaterial(kdf_salt=salt, encrypted_mek=b"", mek_version=1, kdf_params=self.DEFAULT_KDF_PARAMS)

    def store_encrypted_mek(self, person: str, encrypted_mek: bytes) -> None:
        """Store client-encrypted MEK."""
        frappe.db.set_value("User Key Material", {"person": person}, {
            "encrypted_mek": encrypted_mek.hex(),
            "key_created": frappe.utils.now_datetime()
        })

    def get_key_material(self, person: str) -> KeyMaterial:
        """Get key material for client-side decryption."""
        data = frappe.db.get_value("User Key Material", {"person": person},
            ["kdf_salt", "encrypted_mek", "mek_version", "kdf_params"], as_dict=True)
        if not data:
            return None
        return KeyMaterial(
            kdf_salt=bytes.fromhex(data.kdf_salt),
            encrypted_mek=bytes.fromhex(data.encrypted_mek) if data.encrypted_mek else b"",
            mek_version=data.mek_version,
            kdf_params=frappe.parse_json(data.kdf_params)
        )

    def rotate_mek(self, person: str, new_encrypted_mek: bytes) -> int:
        """Rotate MEK. Returns new version."""
        current = frappe.db.get_value("User Key Material", {"person": person}, "mek_version")
        new_version = (current or 0) + 1
        frappe.db.set_value("User Key Material", {"person": person}, {
            "encrypted_mek": new_encrypted_mek.hex(),
            "mek_version": new_version,
            "last_rotation": frappe.utils.now_datetime()
        })
        # Invalidate old recovery shares
        frappe.db.set_value("Key Recovery Share",
            {"person": person, "mek_version": ["<", new_version]}, "status", "Revoked")
        return new_version

    def create_recovery_shares(self, person: str, trustees: list, encrypted_shares: list, threshold: int):
        """Store recovery shares for trustees."""
        mek_version = frappe.db.get_value("User Key Material", {"person": person}, "mek_version")
        frappe.db.set_value("Key Recovery Share", {"person": person, "status": "Active"}, "status", "Revoked")

        for i, (trustee, share) in enumerate(zip(trustees, encrypted_shares)):
            frappe.get_doc({
                "doctype": "Key Recovery Share",
                "person": person, "trustee": trustee, "encrypted_share": share.hex(),
                "share_index": i + 1, "threshold": threshold, "total_shares": len(trustees),
                "mek_version": mek_version, "status": "Active"
            }).insert(ignore_permissions=True)
```

### 13.6 Vault Encryption Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VAULT ITEM ENCRYPTION FLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. USER CREATES VAULT ITEM (Flutter Client)                                 │
│     a) Generate random DEK (256-bit)                                         │
│     b) Encrypt item data with DEK (AES-256-GCM)                              │
│     c) Encrypt DEK with MEK (AES-256-GCM)                                    │
│     d) Send to server: {encrypted_data, encrypted_dek, metadata}             │
│                                                                              │
│  2. SERVER STORES (Cannot decrypt)                                           │
│     Store encrypted_data and encrypted_dek in Personal Vault Item            │
│                                                                              │
│  3. USER RETRIEVES VAULT ITEM (Flutter Client)                               │
│     a) Fetch {encrypted_data, encrypted_dek} from server                     │
│     b) Get MEK from secure storage (or derive from password)                 │
│     c) Decrypt DEK with MEK                                                  │
│     d) Decrypt data with DEK                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 13.7 Key Recovery Flow (via Digital Will)

```
SETUP: Owner creates recovery shares
  1. Owner selects 5 trustees in Digital Will
  2. Client splits MEK using Shamir's Secret Sharing (3-of-5)
  3. Each share encrypted with trustee's public key
  4. Encrypted shares stored server-side

RECOVERY: After Digital Will activation
  1. Will activation triggers share release to approved trustees
  2. Each trustee decrypts their share with private key
  3. 3+ trustees combine shares to reconstruct MEK
  4. Reconstructed MEK can decrypt vault items

SECURITY PROPERTIES:
  • No single trustee can access vault
  • Server cannot reconstruct MEK
  • Lost shares regeneratable while owner has password
```

*End of Section 13: Key Management System*

---

## 14. Travel Mode Enforcement Framework

*Added: November 2025 (Post-Critique Hardening)*

**Issue Sources:** Claude §2.1, Jeni §Policy enforcement, Gemi §3.1

### 14.1 Problem Statement

Travel Mode is described but lacks:
- Mechanism for dynamic hiding across ALL modules (not just User module)
- Data type classification/taxonomy
- Integration with other modules' query layers
- Risk of developers forgetting to add checks to new doctypes

### 14.2 Data Sensitivity Taxonomy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATA SENSITIVITY TAXONOMY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Level 5: VAULT                                                              │
│  ├── Personal Vault items                                                    │
│  ├── Always hidden in travel mode                                            │
│  └── Requires vault unlock to access                                         │
│                                                                              │
│  Level 4: FINANCIAL                                                          │
│  ├── Bank accounts, transactions                                             │
│  ├── Invoices, payments                                                      │
│  ├── Salary information                                                      │
│  └── Cryptocurrency wallets                                                  │
│                                                                              │
│  Level 3: MEDICAL                                                            │
│  ├── Health records                                                          │
│  ├── Prescriptions                                                           │
│  ├── Vitals history                                                          │
│  └── Insurance information                                                   │
│                                                                              │
│  Level 2: BUSINESS                                                           │
│  ├── Contracts                                                               │
│  ├── Performance reviews                                                     │
│  ├── Confidential projects                                                   │
│  └── Trade secrets                                                           │
│                                                                              │
│  Level 1: PERSONAL                                                           │
│  ├── AI memories                                                             │
│  ├── Private notes                                                           │
│  ├── Location history                                                        │
│  └── Private messages                                                        │
│                                                                              │
│  Level 0: PUBLIC                                                             │
│  ├── Profile photo                                                           │
│  ├── Display name                                                            │
│  └── Organization membership                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 14.3 Enforcement Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRAVEL MODE ENFORCEMENT LAYERS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER 1: DocType Registration                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Each sensitive DocType registers with TravelModeRegistry:           │    │
│  │   - doctype: "Bank Account"                                         │    │
│  │   - sensitivity_level: 4 (FINANCIAL)                                │    │
│  │   - hidden_fields: ["balance", "account_number"]                    │    │
│  │   - decoy_generator: generate_fake_balance (optional)               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LAYER 2: Query Condition Injection                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ get_permission_query_conditions for registered doctypes             │    │
│  │ Returns "1=0" to hide all records when travel_mode = true           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LAYER 3: Document Read Hook                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Before returning document data, check travel mode:                  │    │
│  │   a) Return 404 (record hidden)                                     │    │
│  │   b) Return decoy data (duress mode)                                │    │
│  │   c) Redact sensitive fields only                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LAYER 4: API Response Filter                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Final filter on all API responses to catch any leakage              │    │
│  │ Belt-and-suspenders approach for defense in depth                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 14.4 Travel Mode Registry

```python
# dartwing_user/travel_mode/registry.py

from dataclasses import dataclass, field
from typing import Callable, Optional, List
from enum import IntEnum

class SensitivityLevel(IntEnum):
    PUBLIC = 0
    PERSONAL = 1
    BUSINESS = 2
    MEDICAL = 3
    FINANCIAL = 4
    VAULT = 5

@dataclass
class SensitiveDocTypeConfig:
    """Configuration for a sensitive doctype."""
    doctype: str
    sensitivity_level: SensitivityLevel
    hidden_fields: List[str] = field(default_factory=list)
    hide_entire_record: bool = True
    decoy_generator: Optional[Callable] = None
    org_field: str = "organization"

class TravelModeRegistry:
    """Central registry of doctypes subject to travel mode filtering."""

    _registry: dict[str, SensitiveDocTypeConfig] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, config: SensitiveDocTypeConfig) -> None:
        """Register a doctype for travel mode filtering."""
        cls._registry[config.doctype] = config

    @classmethod
    def get_config(cls, doctype: str) -> Optional[SensitiveDocTypeConfig]:
        return cls._registry.get(doctype)

    @classmethod
    def is_registered(cls, doctype: str) -> bool:
        return doctype in cls._registry

    @classmethod
    def get_all_registered(cls) -> List[str]:
        return list(cls._registry.keys())

    @classmethod
    def initialize(cls):
        """Register all sensitive doctypes. Called at module load."""
        if cls._initialized:
            return

        # User module doctypes
        cls.register(SensitiveDocTypeConfig(
            doctype="Personal Vault Item",
            sensitivity_level=SensitivityLevel.VAULT,
            hide_entire_record=True
        ))
        cls.register(SensitiveDocTypeConfig(
            doctype="AI Memory Entry",
            sensitivity_level=SensitivityLevel.PERSONAL,
            hide_entire_record=True
        ))
        cls.register(SensitiveDocTypeConfig(
            doctype="Location Share",
            sensitivity_level=SensitivityLevel.PERSONAL,
            hide_entire_record=True
        ))

        # Other modules register via their __init__.py
        # dartwing_family registers: Medical Record, etc.
        # dartwing_company registers: Sales Invoice, Bank Account, etc.

        cls._initialized = True
```

### 14.5 Travel Mode Enforcement Service

```python
# dartwing_user/travel_mode/enforcement.py

import frappe
from .registry import TravelModeRegistry, SensitivityLevel

def is_travel_mode_active(user: str = None) -> bool:
    """Check if travel mode is active for user."""
    user = user or frappe.session.user
    if user == "Administrator" or user == "Guest":
        return False

    person = frappe.db.get_value("Frappe User", user, "person")
    if not person:
        return False

    profile = frappe.db.get_value("User Profile", {"person": person},
        ["travel_mode", "travel_mode_expires"], as_dict=True)

    if not profile or not profile.travel_mode:
        return False

    # Check expiry
    if profile.travel_mode_expires:
        if frappe.utils.now_datetime() > frappe.utils.get_datetime(profile.travel_mode_expires):
            frappe.db.set_value("User Profile", {"person": person}, "travel_mode", 0)
            return False

    return True

def is_duress_mode_active(user: str = None) -> bool:
    """Check if duress PIN was used (show decoy data instead of hiding)."""
    user = user or frappe.session.user
    return frappe.cache().get_value(f"duress_mode:{user}") == True

def get_user_sensitivity_threshold(user: str = None) -> int:
    """Get user's configured sensitivity threshold for travel mode."""
    user = user or frappe.session.user
    person = frappe.db.get_value("Frappe User", user, "person")
    if not person:
        return SensitivityLevel.PERSONAL

    threshold = frappe.db.get_value("User Profile", {"person": person},
        "travel_mode_sensitivity_threshold")

    return threshold or SensitivityLevel.PERSONAL

def get_travel_mode_query_condition(doctype: str, user: str = None) -> str:
    """
    Return SQL condition to filter out sensitive records during travel mode.
    Used by get_permission_query_conditions hook.
    """
    if not is_travel_mode_active(user):
        return ""

    config = TravelModeRegistry.get_config(doctype)
    if not config:
        return ""

    threshold = get_user_sensitivity_threshold(user)

    # If doctype sensitivity >= user threshold, hide all
    if config.sensitivity_level >= threshold:
        if config.hide_entire_record:
            return "1=0"  # Hide all records

    return ""

def filter_document_for_travel_mode(doc: dict, doctype: str) -> dict:
    """Filter document fields based on travel mode. Called by doc read hooks."""
    if not is_travel_mode_active():
        return doc

    config = TravelModeRegistry.get_config(doctype)
    if not config:
        return doc

    threshold = get_user_sensitivity_threshold()
    if config.sensitivity_level < threshold:
        return doc

    # Duress mode: show decoy data
    if is_duress_mode_active():
        if config.decoy_generator:
            return config.decoy_generator(doc)
        return doc

    # Redact hidden fields
    if config.hidden_fields and not config.hide_entire_record:
        filtered = doc.copy()
        for field in config.hidden_fields:
            if field in filtered:
                filtered[field] = "[REDACTED]"
        return filtered

    return doc

def activate_duress_mode(user: str = None) -> None:
    """Activate duress mode (triggered by duress PIN)."""
    user = user or frappe.session.user
    frappe.cache().set_value(f"duress_mode:{user}", True, expires_in_sec=86400)

    # Silent alert to emergency contacts
    person = frappe.db.get_value("Frappe User", user, "person")
    send_silent_duress_alert(person)

def send_silent_duress_alert(person: str) -> None:
    """Send silent alert to emergency contacts."""
    contacts = frappe.get_all("Emergency Contact",
        filters={"parent": person, "notify_on_duress": 1},
        fields=["contact_person", "contact_method"])

    for contact in contacts:
        frappe.enqueue(
            "dartwing_user.services.notifications.send_duress_alert",
            contact=contact,
            person=person,
            queue="short"
        )
```

### 14.6 Sensitive Data Mixin

```python
# dartwing_user/travel_mode/mixin.py

import frappe
from .enforcement import is_travel_mode_active, filter_document_for_travel_mode
from .registry import TravelModeRegistry

class SensitiveDataMixin:
    """
    Mixin for DocType controllers that handle sensitive data.
    Inherit from this to get automatic travel mode checking.
    """

    def check_permission(self, permission_type=None):
        """Override to add travel mode check."""
        super().check_permission(permission_type)

        if is_travel_mode_active():
            config = TravelModeRegistry.get_config(self.doctype)
            if config and config.hide_entire_record:
                from .enforcement import get_user_sensitivity_threshold
                threshold = get_user_sensitivity_threshold()
                if config.sensitivity_level >= threshold:
                    frappe.throw("Access restricted in Travel Mode", frappe.PermissionError)

    def as_dict(self, *args, **kwargs):
        """Override to filter fields in travel mode."""
        data = super().as_dict(*args, **kwargs)
        return filter_document_for_travel_mode(data, self.doctype)
```

### 14.7 hooks.py Integration

```python
# dartwing_user/hooks.py additions

# Import registry initialization
from dartwing_user.travel_mode.registry import TravelModeRegistry

# Initialize on module load
TravelModeRegistry.initialize()

# Permission query conditions for travel mode
# Auto-generated from registry at runtime
def get_travel_mode_doctypes():
    return TravelModeRegistry.get_all_registered()

permission_query_conditions = {
    "Personal Vault Item": "dartwing_user.travel_mode.enforcement.get_travel_mode_query_condition",
    "AI Memory Entry": "dartwing_user.travel_mode.enforcement.get_travel_mode_query_condition",
    "Location Share": "dartwing_user.travel_mode.enforcement.get_travel_mode_query_condition",
    # Additional doctypes added by other modules via registry
}

# Document event hooks for travel mode filtering
doc_events = {
    "*": {
        "after_load": "dartwing_user.travel_mode.enforcement.apply_travel_mode_filter"
    }
}
```

### 14.8 Cross-Module Registration

Other Dartwing modules register their sensitive doctypes:

```python
# dartwing_family/__init__.py
from dartwing_user.travel_mode.registry import TravelModeRegistry, SensitivityLevel, SensitiveDocTypeConfig

TravelModeRegistry.register(SensitiveDocTypeConfig(
    doctype="Medical Record",
    sensitivity_level=SensitivityLevel.MEDICAL,
    hide_entire_record=True
))

# dartwing_company/__init__.py
TravelModeRegistry.register(SensitiveDocTypeConfig(
    doctype="Bank Account",
    sensitivity_level=SensitivityLevel.FINANCIAL,
    hidden_fields=["balance", "account_number"],
    hide_entire_record=False,
    decoy_generator=generate_decoy_bank_account
))

def generate_decoy_bank_account(doc: dict) -> dict:
    """Generate decoy bank data for duress mode."""
    import random
    decoy = doc.copy()
    decoy["balance"] = round(random.uniform(100, 5000), 2)
    decoy["account_number"] = "****" + str(random.randint(1000, 9999))
    return decoy
```

### 14.9 Travel Mode User Profile Fields

```json
{
  "fieldname": "travel_mode_section",
  "fieldtype": "Section Break",
  "label": "Travel Mode Settings"
},
{
  "fieldname": "travel_mode",
  "label": "Travel Mode Active",
  "fieldtype": "Check",
  "default": 0
},
{
  "fieldname": "travel_mode_expires",
  "label": "Travel Mode Expires",
  "fieldtype": "Datetime",
  "depends_on": "travel_mode"
},
{
  "fieldname": "travel_mode_sensitivity_threshold",
  "label": "Sensitivity Threshold",
  "fieldtype": "Select",
  "options": "1 - Personal\n2 - Business\n3 - Medical\n4 - Financial\n5 - Vault",
  "default": "1 - Personal",
  "description": "Hide data at or above this sensitivity level"
},
{
  "fieldname": "duress_pin",
  "label": "Duress PIN",
  "fieldtype": "Password",
  "description": "Alternative PIN that shows decoy data and alerts contacts"
},
{
  "fieldname": "auto_travel_mode_countries",
  "label": "Auto-Enable Countries",
  "fieldtype": "Table MultiSelect",
  "options": "Travel Mode Country",
  "description": "Automatically enable travel mode when in these countries"
}
```

### 14.10 Integration Tests

```python
# tests/test_travel_mode_enforcement.py

import frappe
import unittest

class TestTravelModeEnforcement(unittest.TestCase):

    def test_travel_mode_hides_vault_items(self):
        """Vault items should not appear when travel mode is active."""
        # Setup
        person = create_test_person()
        vault_item = create_vault_item(person)

        # Enable travel mode
        frappe.db.set_value("User Profile", {"person": person}, "travel_mode", 1)

        # Assert hidden
        frappe.set_user(get_user_for_person(person))
        items = frappe.get_all("Personal Vault Item", filters={"person": person})
        self.assertEqual(len(items), 0)

    def test_travel_mode_respects_threshold(self):
        """Only data at/above threshold should be hidden."""
        person = create_test_person()

        # Set threshold to FINANCIAL (4)
        frappe.db.set_value("User Profile", {"person": person},
            "travel_mode_sensitivity_threshold", 4)
        frappe.db.set_value("User Profile", {"person": person}, "travel_mode", 1)

        # PERSONAL (1) data should be visible
        # FINANCIAL (4) data should be hidden

    def test_duress_mode_shows_decoy_data(self):
        """Duress PIN should show fake data, not hide."""
        person = create_test_person()
        bank = create_bank_account(person, balance=50000)

        # Activate duress mode
        frappe.cache().set_value(f"duress_mode:{person}", True)

        # Should return decoy balance, not real
        doc = frappe.get_doc("Bank Account", bank)
        self.assertNotEqual(doc.balance, 50000)

    def test_cross_module_registration(self):
        """Doctypes from other modules should be filtered."""
        from dartwing_user.travel_mode.registry import TravelModeRegistry

        # Family module should have registered Medical Record
        self.assertTrue(TravelModeRegistry.is_registered("Medical Record"))
```

*End of Section 14: Travel Mode Enforcement Framework*

---

## 15. Provider Abstraction & Error Handling

*Added: November 2025 (Post-Critique Hardening)*

**Issue Sources:** Claude §2.3, §2.8, §4.2, §4.4

### 15.1 Problem Statement

Multiple features depend on external services without proper abstraction:
- AI Voice Clone: ElevenLabs, PlayHT
- Identity Verification: Persona, Jumio, Onfido
- Push Notifications: APNS, FCM
- No circuit breaker patterns or fallback strategies
- No standardized error handling across services

### 15.2 Provider Interface Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PROVIDER ABSTRACTION ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Application Code                                                            │
│       │                                                                      │
│       ▼                                                                      │
│  ┌───────────────────────────────────────┐                                  │
│  │ Provider Factory                       │                                  │
│  │ get_voice_provider()                   │ ← Reads config, checks circuit  │
│  │ get_idv_provider()                     │   breakers, returns provider    │
│  │ get_push_provider()                    │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│                    ▼                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Circuit Breaker                        │                                  │
│  │ • Tracks failures per provider         │                                  │
│  │ • Opens after N failures               │                                  │
│  │ • Half-open after timeout              │                                  │
│  │ • Routes to fallback when open         │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│       ┌────────────┼────────────┐                                           │
│       ▼            ▼            ▼                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                                      │
│  │ElevenLabs│  │ PlayHT  │  │ MockProv│  ← Implement same interface         │
│  │Provider │  │Provider │  │ (test)  │                                      │
│  └─────────┘  └─────────┘  └─────────┘                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 15.3 Provider Interfaces

```python
# dartwing_user/providers/base.py

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ProviderStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class ProviderResult:
    """Standard result from provider operations."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    provider: Optional[str] = None
    latency_ms: Optional[int] = None

# Voice Clone Provider Interface
class VoiceCloneProvider(Protocol):
    """Interface for voice cloning services."""

    def upload_sample(self, audio_data: bytes, metadata: Dict) -> ProviderResult:
        """Upload voice sample, return external ID."""
        ...

    def get_training_status(self, external_id: str) -> ProviderResult:
        """Check training progress."""
        ...

    def generate_audio(self, external_id: str, text: str) -> ProviderResult:
        """Generate audio from text."""
        ...

    def delete_model(self, external_id: str) -> ProviderResult:
        """Delete voice model (GDPR compliance)."""
        ...

# Identity Verification Provider Interface
class IdentityVerificationProvider(Protocol):
    """Interface for IDV services."""

    def create_session(self, person_data: Dict) -> ProviderResult:
        """Create verification session."""
        ...

    def get_session_status(self, session_id: str) -> ProviderResult:
        """Get verification status."""
        ...

    def get_verification_result(self, session_id: str) -> ProviderResult:
        """Get detailed verification data."""
        ...

# Push Notification Provider Interface
class PushNotificationProvider(Protocol):
    """Interface for push notification services."""

    def send(self, device_token: str, payload: Dict) -> ProviderResult:
        """Send push notification."""
        ...

    def send_batch(self, tokens: list, payload: Dict) -> ProviderResult:
        """Send to multiple devices."""
        ...
```

### 15.4 Circuit Breaker Implementation

```python
# dartwing_user/providers/circuit_breaker.py

import time
import frappe
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # Failures before opening
    recovery_timeout: int = 60       # Seconds before half-open
    half_open_max_calls: int = 3     # Test calls in half-open
    success_threshold: int = 2       # Successes to close

class CircuitBreaker:
    """Circuit breaker for external service calls."""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._cache_key = f"circuit_breaker:{name}"

    def _get_state(self) -> dict:
        """Get current state from cache."""
        state = frappe.cache().get_value(self._cache_key)
        if not state:
            return {
                "state": CircuitState.CLOSED.value,
                "failure_count": 0,
                "success_count": 0,
                "last_failure_time": None
            }
        return state

    def _set_state(self, state: dict):
        """Persist state to cache."""
        frappe.cache().set_value(self._cache_key, state, expires_in_sec=3600)

    def is_open(self) -> bool:
        """Check if circuit is open (should reject requests)."""
        state = self._get_state()

        if state["state"] == CircuitState.OPEN.value:
            # Check if recovery timeout has passed
            if state["last_failure_time"]:
                elapsed = time.time() - state["last_failure_time"]
                if elapsed > self.config.recovery_timeout:
                    # Transition to half-open
                    state["state"] = CircuitState.HALF_OPEN.value
                    state["success_count"] = 0
                    self._set_state(state)
                    return False
            return True

        return False

    def record_success(self):
        """Record successful call."""
        state = self._get_state()

        if state["state"] == CircuitState.HALF_OPEN.value:
            state["success_count"] += 1
            if state["success_count"] >= self.config.success_threshold:
                # Close circuit
                state["state"] = CircuitState.CLOSED.value
                state["failure_count"] = 0

        elif state["state"] == CircuitState.CLOSED.value:
            # Reset failure count on success
            state["failure_count"] = 0

        self._set_state(state)

    def record_failure(self):
        """Record failed call."""
        state = self._get_state()
        state["failure_count"] += 1
        state["last_failure_time"] = time.time()

        if state["failure_count"] >= self.config.failure_threshold:
            state["state"] = CircuitState.OPEN.value
            frappe.logger().warning(f"Circuit breaker {self.name} opened after {state['failure_count']} failures")

        self._set_state(state)

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.is_open():
            raise CircuitBreakerOpenError(f"Circuit breaker {self.name} is open")

        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise

class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass
```

### 15.5 Provider Implementations

```python
# dartwing_user/providers/voice/elevenlabs.py

import requests
import frappe
from ..base import VoiceCloneProvider, ProviderResult
from ..circuit_breaker import CircuitBreaker

class ElevenLabsProvider:
    """ElevenLabs voice cloning implementation."""

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self):
        self.api_key = frappe.conf.get("elevenlabs_api_key")
        self.circuit_breaker = CircuitBreaker("elevenlabs")

    def upload_sample(self, audio_data: bytes, metadata: dict) -> ProviderResult:
        if self.circuit_breaker.is_open():
            return ProviderResult(success=False, error="Service temporarily unavailable", provider="elevenlabs")

        try:
            start = time.time()
            response = requests.post(
                f"{self.BASE_URL}/voices/add",
                headers={"xi-api-key": self.api_key},
                files={"files": audio_data},
                data={"name": metadata.get("name", "voice_clone")},
                timeout=30
            )
            response.raise_for_status()
            self.circuit_breaker.record_success()

            return ProviderResult(
                success=True,
                data={"voice_id": response.json()["voice_id"]},
                provider="elevenlabs",
                latency_ms=int((time.time() - start) * 1000)
            )
        except Exception as e:
            self.circuit_breaker.record_failure()
            return ProviderResult(success=False, error=str(e), provider="elevenlabs")

    def generate_audio(self, voice_id: str, text: str) -> ProviderResult:
        if self.circuit_breaker.is_open():
            return ProviderResult(success=False, error="Service temporarily unavailable")

        try:
            response = requests.post(
                f"{self.BASE_URL}/text-to-speech/{voice_id}",
                headers={"xi-api-key": self.api_key, "Content-Type": "application/json"},
                json={"text": text, "model_id": "eleven_monolingual_v1"},
                timeout=60
            )
            response.raise_for_status()
            self.circuit_breaker.record_success()

            return ProviderResult(success=True, data=response.content, provider="elevenlabs")
        except Exception as e:
            self.circuit_breaker.record_failure()
            return ProviderResult(success=False, error=str(e))

    def delete_model(self, voice_id: str) -> ProviderResult:
        try:
            response = requests.delete(
                f"{self.BASE_URL}/voices/{voice_id}",
                headers={"xi-api-key": self.api_key},
                timeout=30
            )
            response.raise_for_status()
            return ProviderResult(success=True, provider="elevenlabs")
        except Exception as e:
            return ProviderResult(success=False, error=str(e))
```

### 15.6 Provider Factory with Fallback

```python
# dartwing_user/providers/factory.py

import frappe
from .voice.elevenlabs import ElevenLabsProvider
from .voice.playht import PlayHTProvider
from .idv.persona import PersonaProvider
from .idv.jumio import JumioProvider
from .push.firebase import FirebaseProvider
from .push.apns import APNSProvider

VOICE_PROVIDERS = {"elevenlabs": ElevenLabsProvider, "playht": PlayHTProvider}
IDV_PROVIDERS = {"persona": PersonaProvider, "jumio": JumioProvider}
PUSH_PROVIDERS = {"firebase": FirebaseProvider, "apns": APNSProvider}

def get_voice_provider() -> VoiceCloneProvider:
    """Get voice provider with automatic fallback."""
    primary = frappe.conf.get("voice_provider", "elevenlabs")
    fallback = "playht" if primary == "elevenlabs" else "elevenlabs"

    primary_provider = VOICE_PROVIDERS[primary]()

    if primary_provider.circuit_breaker.is_open():
        frappe.logger().warning(f"Voice provider {primary} unavailable, using fallback {fallback}")
        return VOICE_PROVIDERS[fallback]()

    return primary_provider

def get_idv_provider() -> IdentityVerificationProvider:
    """Get identity verification provider."""
    provider = frappe.conf.get("idv_provider", "persona")
    return IDV_PROVIDERS[provider]()

def get_push_provider(platform: str) -> PushNotificationProvider:
    """Get push provider for platform."""
    if platform == "ios":
        return APNSProvider()
    return FirebaseProvider()
```

### 15.7 Error Handling Framework

```python
# dartwing_user/exceptions.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict

class ErrorCategory(Enum):
    VALIDATION = "validation"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    EXTERNAL_SERVICE = "external_service"
    RATE_LIMIT = "rate_limit"
    SECURITY = "security"
    INTERNAL = "internal"

@dataclass
class ErrorContext:
    """Context for error handling."""
    recoverable: bool = True
    retry_after_seconds: Optional[int] = None
    suggestion: Optional[str] = None
    details: Dict = field(default_factory=dict)

class DartwingUserError(Exception):
    """Base exception for User module."""

    category: ErrorCategory = ErrorCategory.INTERNAL
    code: str = "UNKNOWN_ERROR"
    http_status: int = 500

    def __init__(self, message: str, context: ErrorContext = None):
        self.message = message
        self.context = context or ErrorContext()
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "category": self.category.value,
                "message": self.message,
                "recoverable": self.context.recoverable,
                "retry_after": self.context.retry_after_seconds,
                "suggestion": self.context.suggestion,
                "details": self.context.details
            }
        }

# Specific Exceptions
class DeviceNotTrustedError(DartwingUserError):
    category = ErrorCategory.PERMISSION
    code = "DEVICE_NOT_TRUSTED"
    http_status = 403

    def __init__(self, device_id: str):
        super().__init__(
            "Operation requires a trusted device",
            ErrorContext(recoverable=True, suggestion="Approve this device from a trusted device first",
                        details={"device_id": device_id})
        )

class TravelModeActiveError(DartwingUserError):
    category = ErrorCategory.SECURITY
    code = "TRAVEL_MODE_ACTIVE"
    http_status = 403

    def __init__(self):
        super().__init__(
            "Access restricted in Travel Mode",
            ErrorContext(recoverable=True, suggestion="Disable Travel Mode to access this data")
        )

class ExternalServiceError(DartwingUserError):
    category = ErrorCategory.EXTERNAL_SERVICE
    code = "EXTERNAL_SERVICE_UNAVAILABLE"
    http_status = 503

    def __init__(self, service: str, retry_after: int = 60):
        super().__init__(
            f"External service temporarily unavailable: {service}",
            ErrorContext(recoverable=True, retry_after_seconds=retry_after)
        )

class RateLimitError(DartwingUserError):
    category = ErrorCategory.RATE_LIMIT
    code = "RATE_LIMIT_EXCEEDED"
    http_status = 429

    def __init__(self, retry_after: int = 60):
        super().__init__(
            "Too many requests",
            ErrorContext(recoverable=True, retry_after_seconds=retry_after)
        )

class VaultLockedError(DartwingUserError):
    category = ErrorCategory.PERMISSION
    code = "VAULT_LOCKED"
    http_status = 403

    def __init__(self):
        super().__init__(
            "Vault is locked",
            ErrorContext(recoverable=True, suggestion="Unlock vault with your password")
        )
```

### 15.8 Retry Decorator

```python
# dartwing_user/utils/retry.py

import time
import functools
from typing import Type, Tuple, Callable

def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Decorator for retrying functions with exponential backoff."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        delay = min(base_delay * (exponential_base ** attempt), max_delay)
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

# Usage example
@retry_with_backoff(max_attempts=3, retryable_exceptions=(requests.RequestException, TimeoutError))
def call_external_api():
    ...
```

### 15.9 API Error Handler Decorator

```python
# dartwing_user/api/error_handler.py

import functools
import frappe
from ..exceptions import DartwingUserError

def handle_api_errors(func):
    """Decorator to standardize API error responses."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DartwingUserError as e:
            frappe.local.response.http_status_code = e.http_status
            return e.to_dict()
        except frappe.PermissionError as e:
            frappe.local.response.http_status_code = 403
            return {"success": False, "error": {"code": "PERMISSION_DENIED", "message": str(e)}}
        except frappe.DoesNotExistError as e:
            frappe.local.response.http_status_code = 404
            return {"success": False, "error": {"code": "NOT_FOUND", "message": str(e)}}
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "User Module API Error")
            frappe.local.response.http_status_code = 500
            return {"success": False, "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}}

    return wrapper

# Usage in API endpoints
@frappe.whitelist()
@handle_api_errors
def get_vault_items():
    ...
```

### 15.10 Provider Health Monitoring

```python
# dartwing_user/providers/health.py

import frappe

def check_provider_health() -> dict:
    """Check health of all external providers."""
    from .factory import VOICE_PROVIDERS, IDV_PROVIDERS, PUSH_PROVIDERS
    from .circuit_breaker import CircuitBreaker

    results = {}

    for name in VOICE_PROVIDERS:
        cb = CircuitBreaker(name)
        state = cb._get_state()
        results[f"voice_{name}"] = {
            "status": "unhealthy" if cb.is_open() else "healthy",
            "failure_count": state["failure_count"],
            "circuit_state": state["state"]
        }

    for name in IDV_PROVIDERS:
        cb = CircuitBreaker(name)
        results[f"idv_{name}"] = {
            "status": "unhealthy" if cb.is_open() else "healthy",
            "circuit_state": cb._get_state()["state"]
        }

    return results

# Scheduled job to log provider health
def log_provider_health():
    """Log provider health metrics (runs every 5 minutes)."""
    health = check_provider_health()
    for provider, status in health.items():
        if status["status"] == "unhealthy":
            frappe.logger().warning(f"Provider {provider} is unhealthy: {status}")
```

*End of Section 15: Provider Abstraction & Error Handling*

---

## 20. Feature Implementation Status

*Spec-Kit Ready Section: Defines which features are ready for implementation planning vs deferred.*

### 20.1 Deferred Features (Do Not Plan Yet)

The following PRD features require external dependencies, compliance reviews, or architecture decisions before implementation planning can begin:

| Feature | PRD ID | Priority | Deferral Reason | Prerequisite |
|---------|--------|----------|-----------------|--------------|
| Passkey Support | U-24 | P1 | Requires Keycloak WebAuthn plugin integration | External: Keycloak config |
| Achievements & Gamification | U-26 | P2 | Needs cross-module event bus architecture | Architecture decision |
| Reputation Score | U-27 | P2 | Bias/gaming risk, requires data science review | Design review complete |
| Personal AI Memory | U-28 | P2 | Privacy impact assessment required | Compliance review |
| Health Data Integration | U-29 | P2 | HIPAA compliance requirements | Legal/BAA agreements |
| Wearable Device Sync | U-30 | P2 | Native platform SDK development | Mobile team availability |

### 20.2 Features Requiring Implementation Planning

The following features are ready for detailed implementation planning:

| Feature | PRD ID | Priority | Phase | Dependencies | Key DocTypes |
|---------|--------|----------|-------|--------------|--------------|
| Daily AI Briefing | U-10 | P1 | 3 | AI Voice Profile, Cross-Org Search | Briefing Session, Briefing Preference |
| Unified Activity Feed | U-20 | P1 | 2 | None | Activity Feed Item |
| Contact Auto-Match | U-21 | P1 | 3 | Person DocType | Contact Match Cache |

### 20.3 Feature Planning Guidance

When planning deferred features, ensure:

- **U-24 Passkey**: Coordinate with Keycloak team; reference WebAuthn spec; integrate with existing `User Device` trust model
- **U-10 Daily Briefing**: Aggregate from all organizations; support text and audio output; honor notification preferences
- **U-20 Activity Feed**: Real-time via Socket.IO; pagination; mark read/unread; org-filtered views
- **U-21 Contact Auto-Match**: Privacy-first (hash-based matching); never upload raw contacts; on-device processing

---

## 21. Notification Delivery Requirements

*Spec-Kit Ready Section: Requirements for multi-channel notification delivery system.*

### 21.1 Functional Requirements

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| REQ-N1 | Support multi-channel delivery: push (FCM/APNS), SMS, email | Must |
| REQ-N2 | Implement fallback cascade when primary channel fails | Must |
| REQ-N3 | Track delivery status for each attempt | Must |
| REQ-N4 | Honor user preferences (quiet hours, channel preferences) | Must |
| REQ-N5 | Rate limit per person per channel | Must |
| REQ-N6 | Support notification batching/digest mode | Should |

### 21.2 Constraints

- **Integration**: Must integrate with Provider Abstraction (Section 15)
- **Resilience**: Must use CircuitBreaker pattern for external services
- **Audit**: Must log all delivery attempts to User Audit Log
- **Privacy**: Must not include sensitive content in push notification previews

### 21.3 Pattern References

- Service structure: Follow `dartwing/permissions/family.py` pattern
- External calls: Follow Section 15 Provider Abstraction patterns
- Existing DocType: Reference `Notification Preference` from Section 3

### 21.4 Success Criteria

- Notifications delivered within 5 seconds for push, 30 seconds for SMS/email
- Fallback triggers automatically when primary channel fails
- All delivery attempts logged with status, timestamp, error details
- User preferences respected 100% (no notifications during quiet hours)

---

## 22. AI Voice Storage Requirements

*Spec-Kit Ready Section: Storage optimization for voice samples.*

### 22.1 Problem Statement

Voice samples should be stored as files (using Frappe's file attachment system) rather than binary data in the database to optimize query performance and enable CDN delivery.

### 22.2 Schema Requirements

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| REQ-V1 | Voice samples stored as files, not binary in database | Must |
| REQ-V2 | Use Frappe `Attach` field type for file storage | Must |
| REQ-V3 | Support multiple samples per profile (child table) | Must |
| REQ-V4 | Track sample metadata: duration, type, quality score | Must |
| REQ-V5 | Support S3/CDN storage backend | Should |

### 22.3 Required Schema Changes

**Parent DocType Update: AI Voice Profile**
- Remove: `voice_sample` (Long Text/binary field)
- Add: `voice_samples` (Table field → Voice Sample Attachment)

**New Child DocType: Voice Sample Attachment**
```
Fields:
- sample_file: Attach (required)
- duration_seconds: Float
- sample_type: Select [Training, Verification, Test]
- quality_score: Float (0-100)
- uploaded_at: Datetime (default: Now)
```

### 22.4 Pattern References

- File storage: Follow Frappe File attachment pattern
- Similar implementation: `Personal Vault Item.file` field from Section 3
- Child table pattern: Follow `Digital Will Trustee` structure

### 22.5 Constraints

- Maximum 10 samples per profile
- Supported formats: WAV, MP3, M4A
- Minimum duration: 30 seconds per sample
- Maximum file size: 50MB per sample

---

## 23. User Audit Trail Requirements

*Spec-Kit Ready Section: Compliance-focused audit logging system.*

### 23.1 Compliance Requirements

| Req ID | Requirement | Regulation | Priority |
|--------|-------------|------------|----------|
| REQ-A1 | Maintain record of all processing activities | GDPR Article 30 | Must |
| REQ-A2 | Log all data access requests | CCPA | Must |
| REQ-A3 | Retain audit logs for minimum 7 years | SOC 2 | Must |
| REQ-A4 | Tamper-evident logging (hash chain) | Best Practice | Should |
| REQ-A5 | Support audit log export for compliance requests | GDPR/CCPA | Must |

### 23.2 Event Taxonomy

**Authentication Events:**
- `login_success`, `login_failure`, `session_created`, `session_terminated`

**Device Events:**
- `device_registered`, `device_revoked`, `device_trusted`, `device_approval_requested`

**Security Events:**
- `travel_mode_enabled`, `travel_mode_disabled`, `duress_pin_entered`, `mfa_enabled`, `mfa_disabled`

**Privacy Events:**
- `data_export_requested`, `account_deletion_requested`, `privacy_setting_changed`

**Vault Events:**
- `vault_item_accessed`, `vault_item_created`, `vault_item_deleted`, `vault_item_shared`

**Digital Will Events:**
- `will_access_requested`, `will_access_granted`, `will_contested`, `will_activated`

### 23.3 DocType Specification

**DocType: User Audit Log**
```
Module: Dartwing User
Auto-name: hash (for tamper evidence)
Track Changes: No (we are the audit log)

Fields:
- person: Link → Person (required, indexed)
- event_type: Select [see taxonomy above]
- event_data: JSON (event-specific details)
- ip_address: Data
- user_agent: Small Text
- device: Link → User Device
- organization: Link → Organization (context)
- timestamp: Datetime (default: Now, indexed)
- previous_hash: Data (hidden, for chain integrity)
- record_hash: Data (hidden, computed)

Permissions:
- System Manager: read only (no write, no delete)
- All others: no access
```

### 23.4 Service Interface

```python
class AuditService:
    @staticmethod
    def log_event(person: str, event_type: str, event_data: dict = None,
                  device: str = None, organization: str = None) -> str:
        """Log audit event. Returns audit log name."""

    @staticmethod
    def get_audit_trail(person: str, event_types: list = None,
                        from_date: str = None, to_date: str = None) -> list:
        """Retrieve audit trail with optional filters."""

    @staticmethod
    def export_audit_trail(person: str, format: str = "json") -> str:
        """Export audit trail for compliance request. Returns file path."""
```

### 23.5 Integration Points

- All User module services must call `AuditService.log_event()` for relevant actions
- Background job for hash chain verification (weekly)
- Background job for archival to cold storage (monthly, records >1 year old)

---

## 24. Permission Registration Requirements

*Spec-Kit Ready Section: Security permissions for all User module DocTypes.*

### 24.1 Security Requirements

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| REQ-P1 | All personal data DocTypes must enforce owner-only access | Must |
| REQ-P2 | Users can only read/write their own records | Must |
| REQ-P3 | System Manager and Administrator bypass allowed | Must |
| REQ-P4 | Query conditions must filter list views (no data leakage) | Must |
| REQ-P5 | Special permissions for shared data (Location Share, Will Trustee) | Must |

### 24.2 DocTypes Requiring Owner-Only Permissions

**Standard Owner-Only Access:**
- User Profile
- User Device
- User Session
- Block List Entry
- Personal Vault Item
- Digital Will
- AI Voice Profile
- AI Memory Entry
- Privacy Setting
- Notification Preference
- Emergency Contact
- Personal Shortcut

**Special Permission Logic:**
- User Location Share: owner OR recipient
- Digital Will Trustee: will owner OR trustee
- User Invite: inviter OR invitee
- Verification Record: owner (read-only for verifier)
- User Audit Log: System Manager only, read-only

### 24.3 Pattern References

**Implementation Pattern:** Follow `dartwing/permissions/family.py`
```python
def has_owner_permission(doc, ptype="read", user=None):
    """Check if user owns this personal data record."""
    user = user or frappe.session.user
    if user == "Administrator": return True
    if "System Manager" in frappe.get_roles(user): return True
    person = frappe.db.get_value("Frappe User", user, "person")
    if not person: return False
    return doc.person == person

def get_owner_query_condition(user=None):
    """Filter list view to owner's records only."""
    user = user or frappe.session.user
    if user == "Administrator": return ""
    if "System Manager" in frappe.get_roles(user): return ""
    person = frappe.db.get_value("Frappe User", user, "person")
    if not person: return "1=0"  # Impossible condition
    return f"`person` = '{frappe.db.escape(person)}'"
```

**Registration Pattern:** Follow `dartwing/hooks.py` lines 121-128
```python
has_permission = {
    "User Profile": "dartwing_user.permissions.has_owner_permission",
    "User Device": "dartwing_user.permissions.has_owner_permission",
    # ... all owner-only DocTypes
}

permission_query_conditions = {
    "User Profile": "dartwing_user.permissions.get_owner_query_condition",
    "User Device": "dartwing_user.permissions.get_owner_query_condition",
    # ... all owner-only DocTypes
}
```

### 24.4 Verification Checklist

When implementing permissions, verify:
- [ ] All 12 standard owner-only DocTypes registered in hooks.py
- [ ] All 4 special permission DocTypes have custom logic
- [ ] Query conditions prevent list view data leakage
- [ ] API endpoints honor permissions (no bypass via direct API call)
- [ ] Travel mode combines with owner permissions correctly

---

## Document History

| Version | Date          | Author         | Changes                                           |
| ------- | ------------- | -------------- | ------------------------------------------------- |
| 1.0     | November 2025 | Claude + Brett | Initial architecture                              |
| 2.0     | November 2025 | Claude + Brett | Complete rewrite aligned with PRD v2, 30 features |
| 2.1     | December 2025 | Claude + Brett | Added spec-kit ready sections 20-24 for MEDIUM priority fixes |

---

_End of Document_
