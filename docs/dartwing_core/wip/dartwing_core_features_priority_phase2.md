# Dartwing Core - Features 11-20 Implementation Queue

**Purpose:** Prioritized implementation order for Phase 2 features (continuation from features 1-10).

**Date:** December 14, 2025

---

## Quick Reference

| Feat # | C-ID | Feature Name | Phase |
|--------|------|--------------|-------|
| 11 | C-16 | Background Job Engine | Platform |
| 12 | C-14 | Plugin / Module System | Platform |
| 13 | C-22 | Feature Flags Per Organization | Platform |
| 14 | C-06 | Automatic Native UI Generation | UI |
| 15 | C-19 | Navigation & Routing Framework | UI |
| 16 | C-18 | Theme & Branding Engine | UI |
| 17 | C-07 | Unified File Storage | Data |
| 18 | C-10 | Real-Time Notifications Engine | Data |
| 19 | C-04 | Offline-First Mobile Apps | Sync |
| 20 | C-05 | Real-Time Collaboration | Sync |

---

## Feature 11: Background Job Engine

**C-ID:** C-16
**Priority:** P1 - CRITICAL (Platform Foundation)
**Blocks:** C-04 (Offline), C-24 (Fax), C-25 (Scheduler), notifications, OCR
**PRD Section:** 5.10

**Description:**
OCR, fax sending, PDF generation, AI tasks, reminders — guaranteed execution with progress UI.

**Why This Order:**
- Foundation for all async processing
- Required before offline sync can work properly
- Notifications, fax, and scheduled tasks all depend on this

**Key Deliverables:**
- Job queue implementation (Redis/RQ or Frappe background jobs)
- Job status tracking and progress reporting
- Retry logic with exponential backoff
- Job monitoring UI
- API for enqueuing jobs from any module

**Acceptance Criteria:**
- [ ] Jobs can be enqueued and executed asynchronously
- [ ] Job status visible in UI (pending/running/completed/failed)
- [ ] Failed jobs retry automatically with configurable limits
- [ ] Progress percentage exposed for long-running jobs
- [ ] Jobs scoped to organization for multi-tenancy

---

## Feature 12: Plugin / Module System

**C-ID:** C-14
**Priority:** P1 - CRITICAL (Platform Foundation)
**Blocks:** C-15 (Integrations), C-24 (Fax Engine)
**PRD Section:** 10

**Description:**
Install DartwingFax, DartwingFamily, DartwingLegal, etc. as simple plugins on the same instance.

**Why This Order:**
- Enables modular architecture for vertical apps
- Must exist before building integration marketplace
- Fax engine is implemented as a plugin

**Key Deliverables:**
- Module manifest format (module.json)
- Module discovery and registration
- Module enable/disable per organization
- Module dependency resolution
- Hot-reload support for development

**Acceptance Criteria:**
- [ ] Modules can be installed/uninstalled without restart
- [ ] Module dependencies validated on install
- [ ] Modules can be enabled/disabled per organization
- [ ] Module APIs exposed through standard endpoints
- [ ] Module assets (UI components) lazy-loaded

---

## Feature 13: Feature Flags Per Organization

**C-ID:** C-22
**Priority:** P1 - HIGH (Platform Foundation)
**Depends On:** C-01 (done)
**PRD Section:** 10.6

**Description:**
Turn any feature on/off instantly for one Company/Family or globally.

**Why This Order:**
- Enables safe rollout of all subsequent features
- Low complexity, high value
- Only depends on Organization (already done)

**Key Deliverables:**
- Feature Flag DocType
- Global vs per-organization flag scoping
- Flag evaluation API (`is_feature_enabled(flag, org)`)
- Admin UI for managing flags
- Percentage rollout support

**Acceptance Criteria:**
- [ ] Flags can be toggled globally or per organization
- [ ] Flag changes take effect immediately (no restart)
- [ ] API returns flag state in <10ms
- [ ] Percentage-based rollout works correctly
- [ ] Flag audit log maintained

---

## Feature 14: Automatic Native UI Generation

**C-ID:** C-06
**Priority:** P1 - CRITICAL (UI Foundation)
**Blocks:** C-19 (Navigation), C-18 (Theming)
**PRD Section:** 6

**Description:**
Every Frappe DocType instantly becomes beautiful, native Flutter forms, lists, kanban, calendars — zero code.

**Why This Order:**
- Core of the Flutter mobile experience
- Navigation and theming build on top of this
- Enables rapid development of all future features

**Key Deliverables:**
- DocType metadata → Flutter widget mapping
- Form renderer (all field types)
- List view renderer
- Kanban view renderer
- Calendar view renderer
- Conditional field visibility (`depends_on`)

**Acceptance Criteria:**
- [ ] All Frappe field types render correctly in Flutter
- [ ] Forms validate according to DocType rules
- [ ] List views support sorting, filtering, pagination
- [ ] Kanban boards work with any Select field
- [ ] Calendar views work with any Date/Datetime field
- [ ] `depends_on` expressions evaluated client-side

---

## Feature 15: Navigation & Routing Framework

**C-ID:** C-19
**Priority:** P1 - HIGH (UI Foundation)
**Depends On:** C-06
**PRD Section:** 6.8

**Description:**
Dynamic sidebar, bottom nav, deep linking, role-based menus — same code works web + mobile.

**Why This Order:**
- Completes the UI layer with C-06
- Required for proper mobile app structure
- Deep linking needed for notifications

**Key Deliverables:**
- Dynamic sidebar generation from modules
- Bottom navigation for mobile
- Deep link handling (app links / universal links)
- Role-based menu filtering
- Breadcrumb navigation
- Back stack management

**Acceptance Criteria:**
- [ ] Sidebar reflects installed/enabled modules
- [ ] Menu items filtered by user role
- [ ] Deep links open correct screen with parameters
- [ ] Navigation state preserved across app restart
- [ ] Same navigation config works on web and mobile

---

## Feature 16: Theme & Branding Engine

**C-ID:** C-18
**Priority:** P2 - HIGH (UI Enhancement)
**Depends On:** C-06
**PRD Section:** 6.10

**Description:**
Per-organization colors, logos, fonts, dark mode — instantly applied everywhere.

**Why This Order:**
- Completes the UI layer
- Enhances user experience for all organizations
- Foundation for white-label (C-11) later

**Key Deliverables:**
- Theme configuration DocType
- Per-organization theme overrides
- Dark mode support
- Logo/favicon configuration
- Font selection
- CSS variable injection (web)
- Flutter ThemeData generation (mobile)

**Acceptance Criteria:**
- [ ] Organizations can set custom primary/secondary colors
- [ ] Logo appears in header/sidebar
- [ ] Dark mode toggle works globally and per-user
- [ ] Theme changes apply without app restart
- [ ] Themes render consistently on web and mobile

---

## Feature 17: Unified File Storage

**C-ID:** C-07
**Priority:** P1 - CRITICAL (Data Foundation)
**Blocks:** C-08 (E-Signature), C-23 (Emergency Binder)
**PRD Section:** 7

**Description:**
One API works with Google Drive, SharePoint, OneDrive, Dropbox, or S3 + automatic virus scanning.

**Why This Order:**
- Foundation for all document features
- E-signature and export features depend on this
- Critical for mobile offline file caching

**Key Deliverables:**
- Storage provider abstraction layer
- S3 provider implementation
- Google Drive provider implementation
- File upload with virus scanning
- File metadata indexing
- Per-organization storage configuration
- Storage usage metering

**Acceptance Criteria:**
- [ ] Files upload/download through unified API
- [ ] Storage provider switchable per organization
- [ ] Virus scanning runs on all uploads
- [ ] File metadata searchable
- [ ] Storage usage tracked per organization
- [ ] Large files support chunked upload

---

## Feature 18: Real-Time Notifications Engine

**C-ID:** C-10
**Priority:** P1 - HIGH (Cross-Cutting)
**Depends On:** C-16 (Background Jobs)
**PRD Section:** 8

**Description:**
Push, SMS, email, in-app — rule-based (keywords, assignees, urgency).

**Why This Order:**
- Cross-cutting concern that enhances all features
- Required for real-time collaboration
- Depends on background jobs (Feature 11)

**Key Deliverables:**
- Notification DocType
- Push notification service (FCM/APNs)
- Email notification templates
- SMS integration (Twilio)
- In-app notification center
- Notification rules engine
- User notification preferences

**Acceptance Criteria:**
- [ ] Push notifications delivered to iOS and Android
- [ ] Email notifications use organization branding
- [ ] SMS notifications work for critical alerts
- [ ] In-app notification center shows history
- [ ] Users can configure notification preferences
- [ ] Rules can trigger on keywords, assignees, doc events

---

## Feature 19: Offline-First Mobile Apps

**C-ID:** C-04
**Priority:** P1 - CRITICAL (Sync Foundation)
**Depends On:** C-16 (Background Jobs), C-06 (UI Generation)
**Blocks:** C-05 (Real-Time Collaboration)
**PRD Section:** 5

**Description:**
Full native iOS/Android apps work 100% offline (forms, lists, signatures, camera) with background sync.

**Why This Order:**
- Core mobile experience
- Requires background jobs for sync queue
- Requires UI generation for rendering
- Real-time collaboration builds on this

**Key Deliverables:**
- Local SQLite database
- Offline CRUD operations
- Sync queue with retry logic
- Conflict detection
- Background sync service
- Sync status indicators
- Delta sync (30-day change log)

**Acceptance Criteria:**
- [ ] All CRUD operations work offline
- [ ] Changes sync when connectivity restored
- [ ] Conflicts detected and flagged for resolution
- [ ] Sync progress visible to user
- [ ] Background sync works when app minimized
- [ ] Camera/signature capture works offline

---

## Feature 20: Real-Time Collaboration

**C-ID:** C-05
**Priority:** P1 - HIGH (Sync Enhancement)
**Depends On:** C-04 (Offline-First), C-10 (Notifications)
**PRD Section:** 5

**Description:**
Live cursors, comments, @mentions, and presence across web + mobile via Socket.IO.

**Why This Order:**
- Builds on offline-first sync infrastructure
- Enhances collaboration across all features
- Requires notifications for @mentions

**Key Deliverables:**
- Socket.IO server integration
- Presence indicators (who's viewing)
- Live cursor positions
- Real-time document updates
- @mention parsing and notification
- Comment threads on any DocType
- Typing indicators

**Acceptance Criteria:**
- [ ] Users see who else is viewing a document
- [ ] Changes from other users appear in <500ms
- [ ] @mentions trigger push notifications
- [ ] Comments can be added to any record
- [ ] Presence updates within 2 seconds
- [ ] Works across web and mobile clients

---

## Implementation Order Summary

| Order | Feat # | C-ID | Feature | Phase | Depends On |
|-------|--------|------|---------|-------|------------|
| 1 | 11 | C-16 | Background Job Engine | Platform | None |
| 2 | 12 | C-14 | Plugin / Module System | Platform | None |
| 3 | 13 | C-22 | Feature Flags | Platform | C-01 (done) |
| 4 | 14 | C-06 | Auto UI Generation | UI | None |
| 5 | 15 | C-19 | Navigation & Routing | UI | C-06 |
| 6 | 16 | C-18 | Theme & Branding | UI | C-06 |
| 7 | 17 | C-07 | Unified File Storage | Data | None |
| 8 | 18 | C-10 | Notifications Engine | Data | C-16 |
| 9 | 19 | C-04 | Offline-First Mobile | Sync | C-16, C-06 |
| 10 | 20 | C-05 | Real-Time Collaboration | Sync | C-04, C-10 |

---

## Dependency Diagram

```
Feature 11 (C-16 Background Jobs)
    │
    ├──────────────────────┬─────────────────────┐
    │                      │                     │
    ▼                      ▼                     │
Feature 18 (C-10)    Feature 19 (C-04)          │
Notifications        Offline-First               │
    │                      │                     │
    │                      │                     │
    └──────────┬───────────┘                     │
               │                                 │
               ▼                                 │
         Feature 20 (C-05)                       │
         Real-Time Collab                        │
                                                 │
Feature 14 (C-06 Auto UI) ◄──────────────────────┘
    │
    ├─────────────────┐
    │                 │
    ▼                 ▼
Feature 15 (C-19)  Feature 16 (C-18)
Navigation         Theming


Feature 12 (C-14 Plugins)     Feature 13 (C-22 Flags)
    │                              │
    │ (unblocks future)            │ (enables rollout)
    ▼                              ▼
C-15, C-24 (Phase 3)          All features


Feature 17 (C-07 File Storage)
    │
    │ (unblocks future)
    ▼
C-08, C-23 (Phase 3)
```

---

## Remaining Features (Phase 3: Features 21-31)

After completing Features 11-20, these 11 features remain:

| Future # | C-ID | Feature | Blocked By |
|----------|------|---------|------------|
| 21 | C-08 | Electronic Signature & Annotation | C-07 |
| 22 | C-09 | Global Full-Text + Metadata Search | - |
| 23 | C-11 | White-Label & Custom Domain | C-18 |
| 24 | C-12 | Per-Organization Billing | - |
| 25 | C-13 | Compliance-Ready Mode | C-20 |
| 26 | C-15 | 40+ Pre-Built Integrations | C-14 |
| 27 | C-20 | Immutable 7-Year Audit Trail | - |
| 28 | C-21 | Data Residency Selection | C-13 |
| 29 | C-23 | Emergency Binder / Export | C-07 |
| 30 | C-24 | Fax-over-IP Engine | C-14, C-16 |
| 31 | C-25 | Maintenance & Reminder Scheduler | C-16, C-10 |

---

## Usage

To implement a feature, reference it by number:

```
"Implement Feature 16" → Theme & Branding Engine (C-18)
"Implement Feature 11" → Background Job Engine (C-16)
```

Each feature section contains:
- **C-ID**: Maps to PRD feature catalog
- **Priority**: P1 (Critical) or P2 (High)
- **Depends On**: Prerequisites that must be done first
- **Blocks**: Features that cannot start until this is done
- **Key Deliverables**: What must be built
- **Acceptance Criteria**: Definition of done
