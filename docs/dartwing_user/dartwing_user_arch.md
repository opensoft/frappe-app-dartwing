# Dartwing User Module Architecture

**Version 1.0 | November 2025**

_The single digital identity that powers every Dartwing experience_

---

## Table of Contents

1. Overview
2. Architecture Principles
3. Relationship to Core Module
4. Doctype Design
5. Feature Specifications
6. Authentication Flows
7. API Endpoints
8. Flutter Implementation
9. Data Model Diagrams
10. Security & Privacy
11. Implementation Roadmap

---

## 1. Overview

The **User Module** (`dartwing_user`) is the personal identity layer that sits on top of Dartwing Core. While Core provides the universal Organization and Person doctypes, the User module handles everything personal, cross-organizational, and identity-related.

### 1.1 Module Boundaries

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING USER MODULE                               │
│                                                                              │
│   Personal identity, cross-org features, preferences, authentication        │
│                                                                              │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│   │ User Prefs  │ │ Device Trust│ │ Block List  │ │ Digital Will│          │
│   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│   │ AI Voice    │ │ Shortcuts   │ │ Location    │ │ Travel Mode │          │
│   │ Clone       │ │             │ │ Share       │ │             │          │
│   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    │ Links to
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING CORE MODULE                               │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                         Person (Master)                              │  │
│   │   - keycloak_user_id                                                 │  │
│   │   - primary_email                                                    │  │
│   │   - frappe_user → User                                              │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      Organization (Universal)                        │  │
│   │   - org_type: Family | Company | Nonprofit | Club | Association     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│   │   Org Member    │  │ Role Template   │  │   Equipment     │           │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Principle: Personal ≠ Organizational

Features in the User module are **never** org-specific. They belong to the human, not to any organization:

| User Module (Personal) | Core/Org Modules (Organizational) |
| ---------------------- | --------------------------------- |
| AI voice clone         | Company phone scripts             |
| Theme preference       | Company branding                  |
| Block list             | Org contact blacklist             |
| Digital will           | Org succession planning           |
| Travel mode            | Org leave requests                |
| Device trust           | Org device management             |

---

## 2. Architecture Principles

### 2.1 One Human = One Identity

Every human in Dartwing has exactly ONE:

- **Keycloak User** (authentication)
- **Frappe User** (authorization)
- **Person** (identity record in Core)
- **User Profile** (preferences in User module)

These are permanently linked and never duplicated.

### 2.2 Cross-Org by Design

User module features work across ALL organizations the person belongs to:

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
                            │
                            │ 1:1 Link
                            ▼
                    ┌───────────────┐
                    │  User Profile │
                    │  (User Module)│
                    │               │
                    │ - Theme       │
                    │ - Block List  │
                    │ - AI Voice    │
                    │ - Shortcuts   │
                    │ - etc.        │
                    └───────────────┘
```

### 2.3 Privacy-First

- Personal data never exposed to organizations
- User controls what orgs can see
- GDPR/CCPA compliance built-in
- Right to erasure respected

---

## 3. Relationship to Core Module

### 3.1 Dependency Chain

```
dartwing_user
    └── depends on: dartwing_core
                        └── depends on: frappe
```

### 3.2 Doctype Ownership

| Doctype             | Module | Purpose                 |
| ------------------- | ------ | ----------------------- |
| Person              | Core   | Master identity record  |
| Organization        | Core   | Universal org container |
| Org Member          | Core   | Person ↔ Org link       |
| User Profile        | User   | Personal preferences    |
| User Device         | User   | Trusted devices         |
| User Block          | User   | Global block list       |
| User Shortcut       | User   | Personal commands       |
| User Location Share | User   | Live location sessions  |
| Digital Will        | User   | Emergency succession    |
| AI Voice Profile    | User   | Voice clone data        |

### 3.3 Frappe User Extension

The User module extends Frappe's built-in User doctype via linked doctypes (not inheritance):

```python
# Core module links Frappe User to Person
Person.frappe_user → User

# User module links Person to User Profile
User Profile.person → Person

# Effective chain:
Frappe User ← Person ← User Profile
```

---

## 4. Doctype Design

### 4.1 User Profile (Main Doctype)

```json
{
  "doctype": "User Profile",
  "module": "Dartwing User",
  "is_single": false,
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "section_preferences",
      "label": "Preferences",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "theme",
      "label": "Theme",
      "fieldtype": "Select",
      "options": "\nLight\nDark\nAMOLED Black\nSystem",
      "default": "System"
    },
    {
      "fieldname": "language",
      "label": "Language",
      "fieldtype": "Link",
      "options": "Language"
    },
    {
      "fieldname": "font_size",
      "label": "Font Size",
      "fieldtype": "Select",
      "options": "Small\nMedium\nLarge\nExtra Large",
      "default": "Medium"
    },
    {
      "fieldname": "timezone",
      "label": "Timezone",
      "fieldtype": "Select",
      "options": "America/New_York\nAmerica/Chicago\nAmerica/Denver\nAmerica/Los_Angeles\nUTC"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "travel_mode",
      "label": "Travel Mode",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "travel_mode_auto_reply",
      "label": "Travel Auto-Reply Message",
      "fieldtype": "Small Text",
      "depends_on": "eval:doc.travel_mode==1"
    },
    {
      "fieldname": "section_notifications",
      "label": "Notifications",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "daily_briefing_enabled",
      "label": "Daily Briefing Enabled",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "daily_briefing_time",
      "label": "Briefing Time",
      "fieldtype": "Time",
      "default": "07:00:00",
      "depends_on": "eval:doc.daily_briefing_enabled==1"
    },
    {
      "fieldname": "push_notifications",
      "label": "Push Notifications",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_ai",
      "label": "AI Personalization",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "ai_voice_profile",
      "label": "AI Voice Profile",
      "fieldtype": "Link",
      "options": "AI Voice Profile"
    },
    {
      "fieldname": "ai_personality_notes",
      "label": "AI Personality Notes",
      "fieldtype": "Text",
      "description": "Describe your communication style for AI personas"
    },
    {
      "fieldname": "section_privacy",
      "label": "Privacy & Security",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "require_push_approve_new_device",
      "label": "Require Push Approval for New Devices",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "hide_sensitive_in_travel_mode",
      "label": "Hide Sensitive Data in Travel Mode",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_digital_will",
      "label": "Digital Will",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "digital_will_enabled",
      "label": "Digital Will Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "digital_will_contact",
      "label": "Trusted Contact",
      "fieldtype": "Link",
      "options": "Person",
      "depends_on": "eval:doc.digital_will_enabled==1"
    },
    {
      "fieldname": "digital_will_inactive_days",
      "label": "Inactive Days Before Activation",
      "fieldtype": "Int",
      "default": 90,
      "depends_on": "eval:doc.digital_will_enabled==1"
    },
    {
      "fieldname": "section_shortcuts",
      "label": "Shortcuts",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "shortcuts",
      "label": "Personal Shortcuts",
      "fieldtype": "Table",
      "options": "User Shortcut"
    },
    {
      "fieldname": "section_blocks",
      "label": "Block List",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "blocks",
      "label": "Blocked Contacts",
      "fieldtype": "Table",
      "options": "User Block"
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
      "if_owner": 1
    }
  ]
}
```

### 4.2 User Device (Child/Standalone)

```json
{
  "doctype": "User Device",
  "module": "Dartwing User",
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
      "unique": 1
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
      "options": "iPhone\nAndroid Phone\niPad\nAndroid Tablet\nDesktop\nWeb Browser",
      "in_list_view": 1
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
      "fieldname": "push_token",
      "label": "Push Token",
      "fieldtype": "Text"
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
      "description": "0-100 based on usage patterns"
    },
    {
      "fieldname": "trusted_at",
      "label": "Trusted At",
      "fieldtype": "Datetime"
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
      "fieldname": "last_seen",
      "label": "Last Seen",
      "fieldtype": "Datetime",
      "in_list_view": 1
    },
    {
      "fieldname": "last_ip",
      "label": "Last IP Address",
      "fieldtype": "Data"
    },
    {
      "fieldname": "last_location",
      "label": "Last Known Location",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_revocation",
      "label": "Revocation",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "is_revoked",
      "label": "Is Revoked",
      "fieldtype": "Check",
      "default": 0
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
    }
  ]
}
```

### 4.3 User Shortcut (Child Table)

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
      "in_list_view": 1,
      "description": "e.g., 'Call Mom', 'Show PTO'"
    },
    {
      "fieldname": "action_type",
      "label": "Action Type",
      "fieldtype": "Select",
      "options": "Call Person\nSend Message\nOpen Screen\nRun Command\nWeb URL",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "target_person",
      "label": "Target Person",
      "fieldtype": "Link",
      "options": "Person",
      "depends_on": "eval:['Call Person', 'Send Message'].includes(doc.action_type)"
    },
    {
      "fieldname": "target_screen",
      "label": "Target Screen",
      "fieldtype": "Data",
      "depends_on": "eval:doc.action_type=='Open Screen'"
    },
    {
      "fieldname": "target_command",
      "label": "Command",
      "fieldtype": "Data",
      "depends_on": "eval:doc.action_type=='Run Command'"
    },
    {
      "fieldname": "target_url",
      "label": "URL",
      "fieldtype": "Data",
      "depends_on": "eval:doc.action_type=='Web URL'"
    },
    {
      "fieldname": "is_active",
      "label": "Active",
      "fieldtype": "Check",
      "default": 1
    }
  ]
}
```

### 4.4 User Block (Child Table)

```json
{
  "doctype": "User Block",
  "module": "Dartwing User",
  "istable": 1,
  "fields": [
    {
      "fieldname": "block_type",
      "label": "Block Type",
      "fieldtype": "Select",
      "options": "Person\nPhone Number\nEmail",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "blocked_person",
      "label": "Blocked Person",
      "fieldtype": "Link",
      "options": "Person",
      "depends_on": "eval:doc.block_type=='Person'",
      "in_list_view": 1
    },
    {
      "fieldname": "blocked_phone",
      "label": "Blocked Phone",
      "fieldtype": "Data",
      "depends_on": "eval:doc.block_type=='Phone Number'"
    },
    {
      "fieldname": "blocked_email",
      "label": "Blocked Email",
      "fieldtype": "Data",
      "depends_on": "eval:doc.block_type=='Email'"
    },
    {
      "fieldname": "blocked_at",
      "label": "Blocked At",
      "fieldtype": "Datetime",
      "in_list_view": 1
    },
    {
      "fieldname": "reason",
      "label": "Reason",
      "fieldtype": "Small Text"
    }
  ]
}
```

### 4.5 User Location Share

```json
{
  "doctype": "User Location Share",
  "module": "Dartwing User",
  "fields": [
    {
      "fieldname": "person",
      "label": "Person",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "shared_with_org",
      "label": "Shared With Organization",
      "fieldtype": "Link",
      "options": "Organization"
    },
    {
      "fieldname": "shared_with_person",
      "label": "Shared With Person",
      "fieldtype": "Link",
      "options": "Person"
    },
    {
      "fieldname": "share_type",
      "label": "Share Type",
      "fieldtype": "Select",
      "options": "Real-time\nLast Known\nEmergency Only",
      "default": "Real-time"
    },
    {
      "fieldname": "started_at",
      "label": "Started At",
      "fieldtype": "Datetime",
      "reqd": 1
    },
    {
      "fieldname": "expires_at",
      "label": "Expires At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "is_active",
      "label": "Is Active",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "current_latitude",
      "label": "Current Latitude",
      "fieldtype": "Float",
      "precision": 8
    },
    {
      "fieldname": "current_longitude",
      "label": "Current Longitude",
      "fieldtype": "Float",
      "precision": 8
    },
    {
      "fieldname": "last_updated",
      "label": "Last Updated",
      "fieldtype": "Datetime"
    }
  ]
}
```

### 4.6 User Invite

```json
{
  "doctype": "User Invite",
  "module": "Dartwing User",
  "fields": [
    {
      "fieldname": "inviter",
      "label": "Invited By",
      "fieldtype": "Link",
      "options": "Person",
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
      "fieldname": "section_invitee",
      "label": "Invitee Details",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "first_name",
      "label": "First Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "last_name",
      "label": "Last Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "email",
      "label": "Email",
      "fieldtype": "Data",
      "options": "Email",
      "reqd": 1
    },
    {
      "fieldname": "phone",
      "label": "Phone",
      "fieldtype": "Data",
      "options": "Phone"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "role_template",
      "label": "Role Template",
      "fieldtype": "Link",
      "options": "Role Template"
    },
    {
      "fieldname": "personal_message",
      "label": "Personal Message",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "section_status",
      "label": "Status",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Pending\nSent\nAccepted\nExpired\nRevoked",
      "default": "Pending",
      "in_list_view": 1
    },
    {
      "fieldname": "invite_token",
      "label": "Invite Token",
      "fieldtype": "Data",
      "unique": 1,
      "read_only": 1
    },
    {
      "fieldname": "sent_at",
      "label": "Sent At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "expires_at",
      "label": "Expires At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "accepted_at",
      "label": "Accepted At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "created_person",
      "label": "Created Person",
      "fieldtype": "Link",
      "options": "Person",
      "read_only": 1
    }
  ]
}
```

### 4.7 AI Voice Profile

```json
{
  "doctype": "AI Voice Profile",
  "module": "Dartwing User",
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
      "fieldname": "voice_sample_url",
      "label": "Voice Sample URL",
      "fieldtype": "Data",
      "description": "URL to stored voice sample"
    },
    {
      "fieldname": "voice_model_id",
      "label": "Voice Model ID",
      "fieldtype": "Data",
      "description": "ID from ElevenLabs/similar service"
    },
    {
      "fieldname": "voice_provider",
      "label": "Voice Provider",
      "fieldtype": "Select",
      "options": "ElevenLabs\nAzure Speech\nGoogle TTS\nOpenAI",
      "default": "ElevenLabs"
    },
    {
      "fieldname": "section_personality",
      "label": "Personality",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "communication_style",
      "label": "Communication Style",
      "fieldtype": "Select",
      "options": "Formal\nProfessional\nCasual\nFriendly\nDirect",
      "default": "Professional"
    },
    {
      "fieldname": "humor_level",
      "label": "Humor Level",
      "fieldtype": "Select",
      "options": "None\nSubtle\nModerate\nHigh",
      "default": "Subtle"
    },
    {
      "fieldname": "verbosity",
      "label": "Verbosity",
      "fieldtype": "Select",
      "options": "Concise\nBalanced\nDetailed",
      "default": "Balanced"
    },
    {
      "fieldname": "personality_prompt",
      "label": "Personality Prompt",
      "fieldtype": "Text",
      "description": "Custom prompt to inject into AI personas"
    },
    {
      "fieldname": "section_status",
      "label": "Status",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "is_trained",
      "label": "Is Trained",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "trained_at",
      "label": "Trained At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "training_status",
      "label": "Training Status",
      "fieldtype": "Select",
      "options": "Not Started\nProcessing\nCompleted\nFailed",
      "default": "Not Started"
    }
  ]
}
```

### 4.8 Digital Will

```json
{
  "doctype": "Digital Will",
  "module": "Dartwing User",
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
      "fieldname": "is_enabled",
      "label": "Is Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "trusted_contact",
      "label": "Trusted Contact",
      "fieldtype": "Link",
      "options": "Person",
      "reqd": 1
    },
    {
      "fieldname": "trusted_contact_email",
      "label": "Trusted Contact Email",
      "fieldtype": "Data",
      "options": "Email"
    },
    {
      "fieldname": "inactive_days_threshold",
      "label": "Inactive Days Before Activation",
      "fieldtype": "Int",
      "default": 90
    },
    {
      "fieldname": "section_access",
      "label": "Access Granted",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "grant_read_personal_org",
      "label": "Grant Read Access to Personal Org",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "grant_read_other_orgs",
      "label": "Grant Read Access to Other Orgs",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "grant_download_data",
      "label": "Allow Data Download",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "section_status",
      "label": "Status",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Inactive\nPending Activation\nActivated\nDeactivated",
      "default": "Inactive"
    },
    {
      "fieldname": "last_activity",
      "label": "Last Activity",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "activation_warning_sent",
      "label": "Warning Sent",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "activated_at",
      "label": "Activated At",
      "fieldtype": "Datetime"
    }
  ]
}
```

---

## 5. Feature Specifications

### 5.1 Feature Matrix

| #   | Feature                     | Doctype(s)          | API Endpoints                            | Flutter Screen      |
| --- | --------------------------- | ------------------- | ---------------------------------------- | ------------------- |
| 1   | Magic-Link Login            | -                   | Keycloak                                 | LoginScreen         |
| 2   | Keycloak SSO                | -                   | Keycloak                                 | AuthService         |
| 3   | Social + Enterprise Login   | -                   | Keycloak                                 | LoginScreen         |
| 4   | Global Person ↔ User Link   | Person              | /api/resource/Person                     | -                   |
| 5   | Smart Invite Flow           | User Invite         | /api/method/dartwing_user.invite         | InviteScreen        |
| 6   | Multi-Org Switcher          | Org Member          | /api/method/dartwing_user.orgs           | OrgSwitcher         |
| 7   | Personal AI Voice Clone     | AI Voice Profile    | /api/method/dartwing_user.voice          | VoiceSetupScreen    |
| 8   | Unified Personal Dashboard  | -                   | /api/method/dartwing_user.dashboard      | DashboardScreen     |
| 9   | Travel Mode                 | User Profile        | /api/method/dartwing_user.travel_mode    | SettingsScreen      |
| 10  | Global Block List           | User Block          | /api/method/dartwing_user.blocks         | BlockListScreen     |
| 11  | Device Trust & Revoke       | User Device         | /api/method/dartwing_user.devices        | DevicesScreen       |
| 12  | Daily AI Briefing           | User Profile        | /api/method/dartwing_user.briefing       | BriefingScreen      |
| 13  | Cross-Org Search            | -                   | /api/method/dartwing_user.search         | SearchScreen        |
| 14  | Personal Shortcut Commands  | User Shortcut       | /api/method/dartwing_user.shortcuts      | ShortcutsScreen     |
| 15  | Data Export / Self-Delete   | -                   | /api/method/dartwing_user.export         | PrivacyScreen       |
| 16  | Emergency Digital Will      | Digital Will        | /api/method/dartwing_user.will           | DigitalWillScreen   |
| 17  | Push-to-Approve Logins      | User Device         | /api/method/dartwing_user.approve_device | ApprovalSheet       |
| 18  | Theme & Language Preference | User Profile        | /api/method/dartwing_user.prefs          | PreferencesScreen   |
| 19  | Live Location Share         | User Location Share | /api/method/dartwing_user.location       | LocationShareScreen |
| 20  | Contacts Auto-Match         | -                   | /api/method/dartwing_user.match_contacts | OnboardingScreen    |

### 5.2 Feature Details

#### Feature 1: Magic-Link Login

**Flow:**

```
User enters email → Keycloak sends magic link → User taps link →
Keycloak validates → Returns tokens → App stores tokens → Logged in
```

**Keycloak Config:**

- Authentication Flow: `magic-link-browser`
- Authenticator: `magic-link-authenticator` (custom or extension)
- Token format: JWT with 15-minute expiry

#### Feature 5: Smart Invite Flow

**Flow:**

```
Inviter fills form (name, phone, email, role) →
System creates User Invite with token →
Magic link sent to invitee →
Invitee taps link → Auto-creates:
  - Frappe User
  - Person (Core)
  - User Profile (User)
  - Org Member (Core) with role template
→ Redirects to app with session
```

**API:**

```python
@frappe.whitelist()
def send_invite(organization, email, first_name=None, last_name=None,
                phone=None, role_template=None, message=None):
    """
    Creates User Invite and sends magic link.
    Returns invite token for tracking.
    """
    invite = frappe.get_doc({
        "doctype": "User Invite",
        "inviter": get_current_person(),
        "organization": organization,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "role_template": role_template,
        "personal_message": message,
        "invite_token": generate_token(),
        "expires_at": add_days(now(), 7)
    }).insert()

    send_invite_email(invite)
    return invite.invite_token
```

#### Feature 6: Multi-Org Switcher

**API:**

```python
@frappe.whitelist()
def get_user_organizations():
    """
    Returns all organizations the current user belongs to.
    """
    person = get_current_person()

    memberships = frappe.get_all(
        "Org Member",
        filters={"person": person, "is_active": 1},
        fields=["organization", "role_template", "joined_date"]
    )

    orgs = []
    for m in memberships:
        org = frappe.get_doc("Organization", m.organization)
        orgs.append({
            "name": org.name,
            "org_name": org.org_name,
            "org_type": org.org_type,
            "role": m.role_template,
            "logo": org.logo
        })

    return orgs
```

#### Feature 12: Daily AI Briefing

**Scheduled Task:**

```python
# hooks.py
scheduler_events = {
    "cron": {
        "0 * * * *": [  # Every hour, check for users whose briefing time matches
            "dartwing_user.tasks.send_daily_briefings"
        ]
    }
}
```

**Briefing Generator:**

```python
def generate_briefing(person):
    """
    Aggregates data from all user's organizations.
    """
    orgs = get_user_organizations(person)
    briefing_items = []

    for org in orgs:
        # Pending approvals
        approvals = get_pending_approvals(person, org.name)
        briefing_items.extend(approvals)

        # Upcoming events
        events = get_upcoming_events(person, org.name, days=1)
        briefing_items.extend(events)

        # Unread notifications
        notifications = get_unread_notifications(person, org.name)
        briefing_items.extend(notifications)

    # Generate AI summary
    summary = generate_ai_summary(briefing_items, person)

    return {
        "items": briefing_items,
        "summary": summary,
        "generated_at": now()
    }
```

#### Feature 15: Data Export / Self-Delete

**GDPR Compliance:**

```python
@frappe.whitelist()
def export_all_data():
    """
    Exports all user data across all organizations.
    Returns download URL for ZIP file.
    """
    person = get_current_person()

    export_data = {
        "person": frappe.get_doc("Person", person).as_dict(),
        "user_profile": get_user_profile(person),
        "organizations": [],
        "communications": [],
        "files": []
    }

    # Gather org-specific data
    for org in get_user_organizations(person):
        org_data = export_organization_data(person, org.name)
        export_data["organizations"].append(org_data)

    # Create ZIP
    zip_path = create_export_zip(export_data, person)

    return {
        "download_url": zip_path,
        "expires_at": add_hours(now(), 24)
    }

@frappe.whitelist()
def delete_account(confirmation_code):
    """
    Permanently deletes user account and all associated data.
    Requires confirmation code sent via email.
    """
    if not verify_confirmation_code(confirmation_code):
        frappe.throw("Invalid confirmation code")

    person = get_current_person()
    user = frappe.session.user

    # Remove from all organizations
    for membership in frappe.get_all("Org Member", {"person": person}):
        frappe.delete_doc("Org Member", membership.name)

    # Delete user module data
    for doctype in ["User Profile", "User Device", "Digital Will",
                    "AI Voice Profile", "User Location Share"]:
        for doc in frappe.get_all(doctype, {"person": person}):
            frappe.delete_doc(doctype, doc.name)

    # Delete Person
    frappe.delete_doc("Person", person)

    # Delete Frappe User
    frappe.delete_doc("User", user)

    # Revoke Keycloak session
    revoke_keycloak_user(user)

    return {"status": "deleted"}
```

---

## 6. Authentication Flows

### 6.1 New User Signup

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Flutter   │     │  Keycloak   │     │   Frappe    │     │   Frappe    │
│     App     │     │   Server    │     │   Backend   │     │   Hooks     │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │ 1. User taps "Sign Up"                │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │ 2. Keycloak registration form         │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │ 3. User submits (email, name)         │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │ 4. Keycloak creates user              │                   │
       │                   │ 5. Event: user-registered             │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │                   │ 6. Create Person  │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
       │                   │                   │ 7. Create User    │
       │                   │                   │    Profile        │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
       │                   │                   │ 8. Create Personal│
       │                   │                   │    Organization   │
       │                   │                   │    (Family type)  │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
       │ 9. Return tokens  │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │ 10. App loads dashboard               │                   │
       │                   │                   │                   │
```

### 6.2 Invite Acceptance

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Invitee   │     │  Keycloak   │     │   Frappe    │
│   (Email)   │     │   Server    │     │   Backend   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ 1. Tap magic link in email            │
       │──────────────────────────────────────►│
       │                   │                   │
       │                   │ 2. Validate token │
       │                   │◄──────────────────│
       │                   │                   │
       │                   │ 3. Check if user exists
       │                   │                   │
       │    ┌──────────────┴──────────────┐    │
       │    │ User exists?                │    │
       │    └──────────────┬──────────────┘    │
       │           │               │           │
       │        No │               │ Yes       │
       │           ▼               ▼           │
       │    ┌────────────┐  ┌────────────┐    │
       │    │ Create new │  │ Link to    │    │
       │    │ Keycloak   │  │ existing   │    │
       │    │ user       │  │ account    │    │
       │    └─────┬──────┘  └──────┬─────┘    │
       │          │                │          │
       │          └────────┬───────┘          │
       │                   │                   │
       │                   │ 4. Create/update  │
       │                   │    Person         │
       │                   │──────────────────►│
       │                   │                   │
       │                   │ 5. Create Org     │
       │                   │    Member         │
       │                   │──────────────────►│
       │                   │                   │
       │                   │ 6. Apply Role     │
       │                   │    Template       │
       │                   │──────────────────►│
       │                   │                   │
       │ 7. Redirect to app with tokens        │
       │◄──────────────────│                   │
       │                   │                   │
```

### 6.3 Push-to-Approve New Device

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  New Device │     │  Keycloak   │     │   Frappe    │     │  Trusted    │
│             │     │   Server    │     │   Backend   │     │   Device    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       │ 1. Login attempt  │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. User has push-approve enabled?     │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │◄──────────────────│ Yes               │
       │                   │                   │                   │
       │ 3. "Waiting for   │                   │                   │
       │    approval..."   │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │                   │ 4. Send push notification             │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
       │                   │                   │   "New login from │
       │                   │                   │    iPhone in NYC" │
       │                   │                   │   [Approve][Deny] │
       │                   │                   │                   │
       │                   │ 5. User taps Approve                  │
       │                   │◄──────────────────────────────────────│
       │                   │                   │                   │
       │                   │ 6. Mark device trusted                │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │ 7. Login succeeds │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

---

## 7. API Endpoints

### 7.1 User Profile APIs

```python
# dartwing_user/api.py

@frappe.whitelist()
def get_my_profile():
    """Get current user's profile with all preferences."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})
    return profile.as_dict()

@frappe.whitelist()
def update_preferences(theme=None, language=None, font_size=None,
                       timezone=None, daily_briefing_enabled=None,
                       daily_briefing_time=None):
    """Update user preferences."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})

    if theme: profile.theme = theme
    if language: profile.language = language
    if font_size: profile.font_size = font_size
    if timezone: profile.timezone = timezone
    if daily_briefing_enabled is not None:
        profile.daily_briefing_enabled = daily_briefing_enabled
    if daily_briefing_time:
        profile.daily_briefing_time = daily_briefing_time

    profile.save()
    return profile.as_dict()

@frappe.whitelist()
def toggle_travel_mode(enabled, auto_reply_message=None):
    """Toggle travel mode on/off."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})

    profile.travel_mode = enabled
    if auto_reply_message:
        profile.travel_mode_auto_reply = auto_reply_message

    profile.save()

    # Notify all orgs
    if enabled:
        notify_orgs_travel_mode(person)

    return {"travel_mode": enabled}
```

### 7.2 Device Management APIs

```python
@frappe.whitelist()
def get_my_devices():
    """Get all devices for current user."""
    person = get_current_person()
    devices = frappe.get_all(
        "User Device",
        filters={"person": person},
        fields=["*"],
        order_by="last_seen desc"
    )
    return devices

@frappe.whitelist()
def register_device(device_id, device_name, device_type,
                    os_version=None, app_version=None, push_token=None):
    """Register a new device."""
    person = get_current_person()

    # Check if device already exists
    existing = frappe.db.exists("User Device", {"device_id": device_id})
    if existing:
        device = frappe.get_doc("User Device", existing)
        device.last_seen = now()
        device.push_token = push_token
        device.app_version = app_version
        device.save()
        return device.as_dict()

    device = frappe.get_doc({
        "doctype": "User Device",
        "person": person,
        "device_id": device_id,
        "device_name": device_name,
        "device_type": device_type,
        "os_version": os_version,
        "app_version": app_version,
        "push_token": push_token,
        "first_seen": now(),
        "last_seen": now(),
        "is_trusted": False
    }).insert()

    # Check if push-approve required
    profile = frappe.get_doc("User Profile", {"person": person})
    if profile.require_push_approve_new_device:
        send_device_approval_push(person, device)

    return device.as_dict()

@frappe.whitelist()
def revoke_device(device_id, reason=None):
    """Revoke a device."""
    person = get_current_person()
    device = frappe.get_doc("User Device", {"device_id": device_id, "person": person})

    device.is_revoked = True
    device.revoked_at = now()
    device.revoke_reason = reason
    device.save()

    # Invalidate Keycloak sessions for this device
    revoke_keycloak_device_sessions(device_id)

    return {"status": "revoked"}

@frappe.whitelist()
def approve_device(device_id, approve=True):
    """Approve or deny a device login request."""
    person = get_current_person()
    device = frappe.get_doc("User Device", {"device_id": device_id, "person": person})

    if approve:
        device.is_trusted = True
        device.trusted_at = now()
        device.save()

        # Signal Keycloak to complete login
        complete_device_login(device_id)
        return {"status": "approved"}
    else:
        device.is_revoked = True
        device.revoked_at = now()
        device.revoke_reason = "Denied by user"
        device.save()
        return {"status": "denied"}
```

### 7.3 Block List APIs

```python
@frappe.whitelist()
def get_block_list():
    """Get current user's block list."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})
    return profile.blocks

@frappe.whitelist()
def block_contact(block_type, value, reason=None):
    """Block a person, phone, or email."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})

    block = {
        "block_type": block_type,
        "blocked_at": now(),
        "reason": reason
    }

    if block_type == "Person":
        block["blocked_person"] = value
    elif block_type == "Phone Number":
        block["blocked_phone"] = value
    elif block_type == "Email":
        block["blocked_email"] = value

    profile.append("blocks", block)
    profile.save()

    # Sync block to all orgs
    sync_block_to_orgs(person, block)

    return {"status": "blocked"}

@frappe.whitelist()
def unblock_contact(idx):
    """Remove a block by index."""
    person = get_current_person()
    profile = frappe.get_doc("User Profile", {"person": person})

    block = profile.blocks[idx]
    profile.blocks.remove(block)
    profile.save()

    return {"status": "unblocked"}
```

### 7.4 Cross-Org Search API

```python
@frappe.whitelist()
def cross_org_search(query, org_filter=None, doctype_filter=None, limit=20):
    """
    Search across all user's organizations.
    """
    person = get_current_person()
    orgs = get_user_organizations(person)

    if org_filter:
        orgs = [o for o in orgs if o.name in org_filter]

    results = []

    for org in orgs:
        # Search in each org's context
        org_results = search_organization(
            org.name,
            query,
            doctype_filter,
            limit_per_org=limit // len(orgs)
        )

        for r in org_results:
            r["organization"] = org.org_name
            r["org_type"] = org.org_type
            results.append(r)

    # Sort by relevance
    results.sort(key=lambda x: x.get("score", 0), reverse=True)

    return results[:limit]
```

### 7.5 Contacts Auto-Match API

```python
@frappe.whitelist()
def match_contacts(contacts):
    """
    Match phone contacts to existing Person records.

    Args:
        contacts: List of {name, phone, email} dicts from device

    Returns:
        List of matches with Person IDs
    """
    person = get_current_person()
    matches = []

    for contact in contacts:
        # Try phone match first
        if contact.get("phone"):
            phone_normalized = normalize_phone(contact["phone"])
            person_match = frappe.db.get_value(
                "Person",
                {"mobile_no": phone_normalized},
                ["name", "full_name", "primary_email"]
            )
            if person_match:
                matches.append({
                    "contact_name": contact["name"],
                    "contact_phone": contact["phone"],
                    "person_id": person_match[0],
                    "person_name": person_match[1],
                    "person_email": person_match[2],
                    "match_type": "phone"
                })
                continue

        # Try email match
        if contact.get("email"):
            person_match = frappe.db.get_value(
                "Person",
                {"primary_email": contact["email"]},
                ["name", "full_name", "mobile_no"]
            )
            if person_match:
                matches.append({
                    "contact_name": contact["name"],
                    "contact_email": contact["email"],
                    "person_id": person_match[0],
                    "person_name": person_match[1],
                    "person_phone": person_match[2],
                    "match_type": "email"
                })

    return matches
```

---

## 8. Flutter Implementation

### 8.1 User Profile Provider

```dart
// lib/providers/user_profile_provider.dart

import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../models/user_profile.dart';
import '../services/api_service.dart';

part 'user_profile_provider.g.dart';

@riverpod
class UserProfileNotifier extends _$UserProfileNotifier {
  @override
  Future<UserProfile> build() async {
    final api = ref.watch(apiServiceProvider);
    final response = await api.call('dartwing_user.api.get_my_profile');
    return UserProfile.fromJson(response);
  }

  Future<void> updateTheme(String theme) async {
    final api = ref.read(apiServiceProvider);
    await api.call('dartwing_user.api.update_preferences', {'theme': theme});
    ref.invalidateSelf();
  }

  Future<void> toggleTravelMode(bool enabled, {String? autoReply}) async {
    final api = ref.read(apiServiceProvider);
    await api.call('dartwing_user.api.toggle_travel_mode', {
      'enabled': enabled,
      'auto_reply_message': autoReply,
    });
    ref.invalidateSelf();
  }
}
```

### 8.2 Org Switcher Widget

```dart
// lib/widgets/org_switcher.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/organizations_provider.dart';

class OrgSwitcher extends ConsumerWidget {
  const OrgSwitcher({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orgsAsync = ref.watch(userOrganizationsProvider);
    final currentOrg = ref.watch(currentOrganizationProvider);

    return orgsAsync.when(
      data: (orgs) => PopupMenuButton<String>(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (currentOrg?.logo != null)
              CircleAvatar(
                backgroundImage: NetworkImage(currentOrg!.logo!),
                radius: 16,
              ),
            const SizedBox(width: 8),
            Text(currentOrg?.orgName ?? 'Select Organization'),
            const Icon(Icons.arrow_drop_down),
          ],
        ),
        itemBuilder: (context) => orgs.map((org) => PopupMenuItem(
          value: org.name,
          child: Row(
            children: [
              _orgTypeIcon(org.orgType),
              const SizedBox(width: 8),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(org.orgName),
                  Text(
                    org.orgType,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ],
          ),
        )).toList(),
        onSelected: (orgName) {
          ref.read(currentOrganizationProvider.notifier).switchTo(orgName);
        },
      ),
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => Text('Error: $e'),
    );
  }

  Icon _orgTypeIcon(String orgType) {
    switch (orgType) {
      case 'Family':
        return const Icon(Icons.family_restroom);
      case 'Company':
        return const Icon(Icons.business);
      case 'Nonprofit':
        return const Icon(Icons.volunteer_activism);
      case 'Club':
        return const Icon(Icons.groups);
      default:
        return const Icon(Icons.group_work);
    }
  }
}
```

### 8.3 Device Trust Screen

```dart
// lib/screens/devices_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/devices_provider.dart';

class DevicesScreen extends ConsumerWidget {
  const DevicesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final devicesAsync = ref.watch(userDevicesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('My Devices')),
      body: devicesAsync.when(
        data: (devices) => ListView.builder(
          itemCount: devices.length,
          itemBuilder: (context, index) {
            final device = devices[index];
            return ListTile(
              leading: Icon(_deviceIcon(device.deviceType)),
              title: Text(device.deviceName),
              subtitle: Text(
                device.isRevoked
                    ? 'Revoked'
                    : 'Last seen: ${_formatDate(device.lastSeen)}',
              ),
              trailing: device.isRevoked
                  ? const Icon(Icons.block, color: Colors.red)
                  : device.isTrusted
                      ? const Icon(Icons.verified, color: Colors.green)
                      : const Icon(Icons.pending, color: Colors.orange),
              onTap: () => _showDeviceActions(context, ref, device),
            );
          },
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Error: $e')),
      ),
    );
  }

  void _showDeviceActions(BuildContext context, WidgetRef ref, UserDevice device) {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.info),
              title: const Text('Device Details'),
              subtitle: Text('${device.deviceType} • ${device.osVersion}'),
            ),
            const Divider(),
            if (!device.isRevoked)
              ListTile(
                leading: const Icon(Icons.block, color: Colors.red),
                title: const Text('Revoke Access'),
                onTap: () async {
                  Navigator.pop(context);
                  final reason = await _askRevokeReason(context);
                  if (reason != null) {
                    await ref.read(userDevicesProvider.notifier)
                        .revokeDevice(device.deviceId, reason);
                  }
                },
              ),
          ],
        ),
      ),
    );
  }

  IconData _deviceIcon(String deviceType) {
    switch (deviceType) {
      case 'iPhone':
      case 'Android Phone':
        return Icons.phone_iphone;
      case 'iPad':
      case 'Android Tablet':
        return Icons.tablet;
      case 'Desktop':
        return Icons.computer;
      default:
        return Icons.devices;
    }
  }

  String _formatDate(DateTime date) {
    // Format relative time
    final diff = DateTime.now().difference(date);
    if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
    if (diff.inHours < 24) return '${diff.inHours}h ago';
    return '${diff.inDays}d ago';
  }

  Future<String?> _askRevokeReason(BuildContext context) async {
    final controller = TextEditingController();
    return showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Revoke Device'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Reason (optional)',
            hintText: 'e.g., Lost phone',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, controller.text),
            child: const Text('Revoke'),
          ),
        ],
      ),
    );
  }
}
```

---

## 9. Data Model Diagrams

### 9.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRAPPE CORE                                     │
│  ┌─────────────┐                                                            │
│  │    User     │◄─────────────────────────────────────────────┐             │
│  │  (Frappe)   │                                              │             │
│  └─────────────┘                                              │             │
└───────────────────────────────────────────────────────────────┼─────────────┘
                                                                │
┌───────────────────────────────────────────────────────────────┼─────────────┐
│                           DARTWING CORE                       │             │
│                                                               │             │
│  ┌─────────────┐        ┌─────────────────┐                  │             │
│  │Organization │◄───────│   Org Member    │                  │             │
│  │             │        │                 │                  │             │
│  │ - org_type  │   1:N  │ - role_template │                  │             │
│  │ - org_name  │        │ - is_active     │                  │             │
│  └─────────────┘        └────────┬────────┘                  │             │
│                                  │                           │             │
│                                  │ N:1                       │             │
│                                  ▼                           │             │
│                         ┌─────────────────┐                  │             │
│                         │     Person      │──────────────────┘             │
│                         │                 │  frappe_user                   │
│                         │ - keycloak_id   │                                │
│                         │ - primary_email │                                │
│                         │ - full_name     │                                │
│                         └────────┬────────┘                                │
└──────────────────────────────────┼─────────────────────────────────────────┘
                                   │
                                   │ 1:1
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DARTWING USER                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         User Profile                                 │   │
│  │                                                                      │   │
│  │  - person (Link to Person)                                          │   │
│  │  - theme, language, font_size, timezone                            │   │
│  │  - travel_mode, daily_briefing_enabled                             │   │
│  │  - ai_voice_profile (Link)                                         │   │
│  │  - shortcuts (Table: User Shortcut)                                │   │
│  │  - blocks (Table: User Block)                                      │   │
│  └──────────────────────────┬──────────────────────────────────────────┘   │
│                             │                                               │
│     ┌───────────────────────┼───────────────────────────────┐              │
│     │                       │                               │              │
│     ▼                       ▼                               ▼              │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────────────┐        │
│  │ User Device │    │ AI Voice Profile │    │ User Location Share │        │
│  │             │    │                  │    │                     │        │
│  │ - device_id │    │ - voice_model_id │    │ - shared_with_org   │        │
│  │ - is_trusted│    │ - personality    │    │ - current_lat/lng   │        │
│  │ - is_revoked│    │ - is_trained     │    │ - expires_at        │        │
│  └─────────────┘    └──────────────────┘    └─────────────────────┘        │
│                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐                                │
│  │  User Invite    │    │  Digital Will   │                                │
│  │                 │    │                 │                                │
│  │ - inviter       │    │ - trusted_contact│                               │
│  │ - organization  │    │ - inactive_days │                                │
│  │ - invite_token  │    │ - status        │                                │
│  └─────────────────┘    └─────────────────┘                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Authentication Flow Data

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEYCLOAK (External)                                 │
│                                                                              │
│  User Record:                                                               │
│  - id: "uuid-from-keycloak"                                                 │
│  - email: "john@example.com"                                                │
│  - firstName: "John"                                                        │
│  - lastName: "Doe"                                                          │
│  - groups: ["/dartwing/admins", "/org-123/members"]                        │
│                                                                              │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   │ Synced via OIDC
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRAPPE                                          │
│                                                                              │
│  Frappe User:                    Person (Core):        User Profile (User): │
│  - name: "john@example.com"      - keycloak_user_id    - person: "P-001"   │
│  - full_name: "John Doe"         - frappe_user         - theme: "Dark"     │
│  - enabled: 1                    - primary_email       - travel_mode: 0    │
│  - roles: [...]                  - full_name           - blocks: [...]     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Security & Privacy

### 10.1 Data Access Rules

| Data Type        | Owner Access | Org Admin Access | Other Users      |
| ---------------- | ------------ | ---------------- | ---------------- |
| User Profile     | Full         | None             | None             |
| User Devices     | Full         | None             | None             |
| Block List       | Full         | None             | None             |
| AI Voice Profile | Full         | None             | None             |
| Digital Will     | Full         | None             | None             |
| Location Share   | Full         | Read (if shared) | Read (if shared) |

### 10.2 Permission Rules (Python)

```python
# dartwing_user/permissions.py

def has_permission(doc, ptype, user):
    """
    User module doctypes are strictly personal.
    Only the owning user can access.
    """
    if doc.doctype in ["User Profile", "User Device", "AI Voice Profile",
                       "Digital Will"]:
        person = get_person_for_user(user)
        return doc.person == person

    if doc.doctype == "User Location Share":
        person = get_person_for_user(user)
        # Owner can always access
        if doc.person == person:
            return True
        # Shared person can read
        if ptype == "read" and doc.shared_with_person == person:
            return True
        # Org members can read if shared with org
        if ptype == "read" and doc.shared_with_org:
            return is_org_member(person, doc.shared_with_org)

    return False
```

### 10.3 GDPR Compliance Checklist

- [x] Right to Access: `export_all_data()` API
- [x] Right to Rectification: User can edit all their data
- [x] Right to Erasure: `delete_account()` API
- [x] Right to Portability: JSON/ZIP export format
- [x] Data Minimization: Only collect necessary data
- [x] Consent: Explicit opt-in for location sharing, AI voice
- [x] Breach Notification: Device revocation alerts

---

## 11. Implementation Roadmap

### Phase 1: Core Identity (Q1 2026)

- [ ] User Profile doctype
- [ ] User Device doctype
- [ ] Keycloak integration hooks
- [ ] Magic-link login flow
- [ ] Basic Flutter screens (Profile, Devices)

### Phase 2: Cross-Org Features (Q2 2026)

- [ ] Multi-Org Switcher
- [ ] Cross-Org Search
- [ ] Unified Dashboard
- [ ] Smart Invite Flow
- [ ] Contacts Auto-Match

### Phase 3: Privacy & Security (Q3 2026)

- [ ] Global Block List
- [ ] Travel Mode
- [ ] Push-to-Approve Logins
- [ ] Device Trust Scoring
- [ ] Data Export / Self-Delete

### Phase 4: AI Personalization (Q4 2026)

- [ ] AI Voice Profile
- [ ] Personal Shortcuts
- [ ] Daily AI Briefing
- [ ] Digital Will
- [ ] Live Location Share

---

## Appendix A: Doctype Summary

| Doctype             | Module        | Type   | Key Fields                                    |
| ------------------- | ------------- | ------ | --------------------------------------------- |
| User Profile        | dartwing_user | Master | person, theme, travel_mode, shortcuts, blocks |
| User Device         | dartwing_user | Master | person, device_id, is_trusted, is_revoked     |
| User Shortcut       | dartwing_user | Child  | trigger*phrase, action_type, target*\*        |
| User Block          | dartwing_user | Child  | block_type, blocked_person/phone/email        |
| User Invite         | dartwing_user | Master | inviter, organization, email, invite_token    |
| User Location Share | dartwing_user | Master | person, shared*with*\*, lat/lng, expires_at   |
| AI Voice Profile    | dartwing_user | Master | person, voice_model_id, personality_prompt    |
| Digital Will        | dartwing_user | Master | person, trusted_contact, inactive_days        |

---

## Appendix B: API Endpoint Summary

| Endpoint                                   | Method | Purpose                  |
| ------------------------------------------ | ------ | ------------------------ |
| `dartwing_user.api.get_my_profile`         | GET    | Get user profile         |
| `dartwing_user.api.update_preferences`     | POST   | Update preferences       |
| `dartwing_user.api.toggle_travel_mode`     | POST   | Toggle travel mode       |
| `dartwing_user.api.get_my_devices`         | GET    | List user devices        |
| `dartwing_user.api.register_device`        | POST   | Register new device      |
| `dartwing_user.api.revoke_device`          | POST   | Revoke device access     |
| `dartwing_user.api.approve_device`         | POST   | Approve pending device   |
| `dartwing_user.api.get_block_list`         | GET    | Get blocked contacts     |
| `dartwing_user.api.block_contact`          | POST   | Block person/phone/email |
| `dartwing_user.api.unblock_contact`        | POST   | Remove block             |
| `dartwing_user.api.get_user_organizations` | GET    | List user's orgs         |
| `dartwing_user.api.cross_org_search`       | POST   | Search across orgs       |
| `dartwing_user.api.match_contacts`         | POST   | Match phone contacts     |
| `dartwing_user.api.send_invite`            | POST   | Send org invite          |
| `dartwing_user.api.export_all_data`        | GET    | GDPR data export         |
| `dartwing_user.api.delete_account`         | POST   | Delete account           |
| `dartwing_user.api.generate_briefing`      | GET    | Get daily briefing       |
