# Dartwing Family Module

## Product Requirements Document

**One App for Your Whole Family**

---

|                    |                                    |
| ------------------ | ---------------------------------- |
| **Product**        | Dartwing Family                    |
| **Version**        | 1.0                                |
| **Date**           | November 28, 2025                  |
| **Status**         | Draft                              |
| **Activates When** | `Organization.org_type = "Family"` |

---

## Executive Summary

Dartwing Family transforms the Dartwing platform into a comprehensive family management system that replaces 15+ separate apps with one unified, AI-native, privacy-first experience. When an organization is created with `org_type = "Family"`, the entire UI, feature set, and AI personality shift to support the unique needs of modern families.

### Products Replaced

| Category                | Apps Replaced                                |
| ----------------------- | -------------------------------------------- |
| **Family Organization** | Cozi, FamilyWall, OurHome                    |
| **Location & Safety**   | Life360, Find My Friends                     |
| **Parental Controls**   | Bark, Qustodio, Screen Time                  |
| **Kids Finance**        | Greenlight, GoHenry, FamZoo                  |
| **Health Tracking**     | Apple Health, MyFitnessPal (family features) |
| **Home Management**     | HomeAssistant, SmartThings (UI layer)        |
| **Calendar**            | Google Calendar, Apple Calendar              |
| **Shopping**            | AnyList, OurGroceries                        |
| **Asset Tracking**      | Sortly, Home Inventory                       |

### Target Users

| User Type      | Age   | Key Needs                               |
| -------------- | ----- | --------------------------------------- |
| Parents        | 25-55 | Organization, oversight, peace of mind  |
| Grandparents   | 55-85 | Connection, emergency access, simple UI |
| Teens          | 13-17 | Independence with guardrails, allowance |
| Children       | 6-12  | Fun interface, chore tracking, rewards  |
| Young Children | 0-5   | Parent-managed profiles only            |
| Caregivers     | Any   | Temporary access, emergency info        |

---

# Section 1: Family Relationship Engine

## 1.1 Overview

The Family Relationship Engine is the core data model that defines how family members relate to each other, enforces age-based permissions, and manages custody/guardianship rules.

## 1.2 Relationship Types

### Primary Relationships

| Relationship             | Bidirectional Link | Age Rules                                        |
| ------------------------ | ------------------ | ------------------------------------------------ |
| Parent ↔ Child           | Yes                | Parent must be 16+ years older or legal guardian |
| Spouse ↔ Spouse          | Yes                | Both must be 18+                                 |
| Grandparent ↔ Grandchild | Yes                | Auto-created when parent has parent              |
| Sibling ↔ Sibling        | Yes                | Auto-created for shared parents                  |
| Guardian ↔ Ward          | Yes                | Legal document upload required                   |
| Step-Parent ↔ Step-Child | Yes                | Created via spouse relationship                  |

### Extended Relationships

| Relationship                 | Notes                                |
| ---------------------------- | ------------------------------------ |
| Aunt/Uncle ↔ Niece/Nephew    | Auto-created from sibling's children |
| Cousin ↔ Cousin              | Auto-created                         |
| In-Laws                      | Created via spouse relationships     |
| Godparent ↔ Godchild         | Manual designation                   |
| Foster Parent ↔ Foster Child | Time-limited, document required      |

## 1.3 Data Model

```python
class FamilyRelationship(Document):
    doctype = "Family Relationship"

    # Core Fields
    person_a: Link["Family Member"]
    person_b: Link["Family Member"]
    relationship_type: Select[
        "Parent-Child", "Spouse", "Sibling",
        "Grandparent-Grandchild", "Guardian-Ward",
        "Aunt/Uncle-Niece/Nephew", "Cousin", "Godparent"
    ]

    # Directional Info
    a_role: Data  # e.g., "Parent", "Grandparent"
    b_role: Data  # e.g., "Child", "Grandchild"

    # Legal/Custody
    is_legal_guardian: Check
    custody_schedule: Link["Custody Schedule"]
    legal_documents: Table["Family Legal Document"]

    # Status
    status: Select["Active", "Separated", "Divorced", "Deceased"]
    start_date: Date
    end_date: Date

    # Reverse Link
    reverse_relationship: Link["Family Relationship"]
```

```python
class FamilyMember(Document):
    doctype = "Family Member"

    # Identity
    first_name: Data
    last_name: Data
    nickname: Data
    date_of_birth: Date
    gender: Select["Male", "Female", "Non-Binary", "Prefer not to say"]
    photo: Attach Image

    # Computed
    age: Int  # Calculated
    age_category: Select["Infant", "Toddler", "Child", "Tween", "Teen", "Adult", "Senior"]
    is_minor: Check  # Under 18
    is_coppa_protected: Check  # Under 13

    # Linked User
    user_account: Link["User"]
    dartwing_user: Link["Dartwing User"]

    # Permissions (based on age)
    permission_profile: Link["Family Permission Profile"]

    # Medical
    medical_profile: Link["Family Medical Profile"]

    # Relationships (child table)
    relationships: Table["Family Relationship Link"]
```

## 1.4 Age-Based Role Enforcement

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGE-BASED PERMISSIONS                         │
│                                                                  │
│  Age 0-5 (Young Child)                                          │
│  ├─ No app access (parent-managed profile only)                 │
│  ├─ Location shared with all guardians                          │
│  └─ Medical info visible to all adults                          │
│                                                                  │
│  Age 6-12 (Child)                                                │
│  ├─ Kid-mode app access                                          │
│  ├─ Chore completion with photo proof                           │
│  ├─ Allowance visible (read-only)                               │
│  ├─ Location shared with guardians                              │
│  └─ COPPA-compliant (no external data sharing)                  │
│                                                                  │
│  Age 13-15 (Tween)                                               │
│  ├─ Full app access with parental controls                      │
│  ├─ Limited location sharing controls                           │
│  ├─ Allowance spending (with limits)                            │
│  ├─ Social features (parent-approved)                           │
│  └─ No longer COPPA-protected (GDPR-K still applies)            │
│                                                                  │
│  Age 16-17 (Teen)                                                │
│  ├─ Most features unlocked                                       │
│  ├─ Driver monitoring (if applicable)                           │
│  ├─ Higher spending limits                                       │
│  ├─ Location sharing can be limited                             │
│  └─ Preparing for adult transition                              │
│                                                                  │
│  Age 18+ (Adult)                                                 │
│  ├─ Full autonomy                                                │
│  ├─ Optional family sharing                                      │
│  ├─ Can be guardian for others                                  │
│  └─ Emergency contact for family                                │
│                                                                  │
│  Age 65+ (Senior)                                                │
│  ├─ Same as adult                                                │
│  ├─ Optional simplified UI                                       │
│  ├─ Medical emergency quick-share                               │
│  └─ "Check-in" feature for family                               │
└─────────────────────────────────────────────────────────────────┘
```

## 1.5 Custody & Multi-Household Support

### Custody Schedule DocType

```python
class CustodySchedule(Document):
    doctype = "Custody Schedule"

    child: Link["Family Member"]
    parent_a: Link["Family Member"]
    parent_b: Link["Family Member"]

    # Schedule Type
    schedule_type: Select[
        "50/50 Weekly",
        "50/50 Bi-Weekly",
        "Primary/Visitation",
        "Custom"
    ]

    # Custom Schedule
    schedule_rules: Table["Custody Schedule Rule"]

    # Holiday Rules
    holiday_schedule: Link["Holiday Custody Schedule"]

    # Visibility Rules
    parent_a_can_see_location_during_b_time: Check
    parent_b_can_see_location_during_a_time: Check

    # Notifications
    notify_handoff: Check
    notify_arrival: Check
```

### Multi-Calendar Visibility

```
Parent A's View:              Parent B's View:
┌─────────────────────┐      ┌─────────────────────┐
│ Mon │ Soccer @ 4pm  │      │ Mon │ (At Mom's)    │
│ Tue │ Dentist 2pm   │      │ Tue │ (At Mom's)    │
│ Wed │ (At Dad's)    │      │ Wed │ Piano @ 5pm   │
│ Thu │ (At Dad's)    │      │ Thu │ Science Fair  │
│ Fri │ School play   │      │ Fri │ School play   │
└─────────────────────┘      └─────────────────────┘

Both see: School play (shared event)
Each sees: Own-time activities only
```

## 1.6 Acceptance Criteria

- [ ] Bidirectional relationships auto-created
- [ ] Age calculated and permissions updated daily
- [ ] COPPA compliance for under-13
- [ ] Custody schedules affect visibility
- [ ] Relationship changes audit-logged
- [ ] Grandparent/extended family auto-linked

---

# Section 2: Parental Controls & Minor Safety

## 2.1 Overview

Comprehensive parental control system that protects children while respecting age-appropriate independence. COPPA and GDPR-K compliant by design.

## 2.2 Control Categories

| Category           | Under 6   | 6-12      | 13-15        | 16-17         |
| ------------------ | --------- | --------- | ------------ | ------------- |
| Screen time limits | N/A       | Enforced  | Soft limits  | Advisory      |
| App approval       | N/A       | Required  | Notify       | None          |
| Contact approval   | N/A       | Required  | Required     | Notify        |
| Location sharing   | Always on | Always on | Configurable | Configurable  |
| Purchase approval  | N/A       | Required  | Limits       | Higher limits |
| Content filtering  | N/A       | Strict    | Moderate     | Light         |

## 2.3 Screen Time Management

### Screen Time Profile

```python
class ScreenTimeProfile(Document):
    doctype = "Screen Time Profile"

    family_member: Link["Family Member"]

    # Daily Limits
    weekday_limit_minutes: Int
    weekend_limit_minutes: Int

    # Time Windows
    allowed_start_time: Time  # e.g., 7:00 AM
    allowed_end_time: Time    # e.g., 9:00 PM

    # Category Limits
    category_limits: Table["Screen Time Category Limit"]
    # e.g., Gaming: 2hr, Social: 1hr, Educational: Unlimited

    # App-Specific
    app_limits: Table["App Time Limit"]

    # Overrides
    school_mode_schedule: Table["School Mode Window"]
    bedtime_mode_schedule: Table["Bedtime Mode Window"]

    # Earning Extra Time
    chore_bonus_minutes: Int  # Minutes earned per chore
    homework_bonus_minutes: Int
```

### Screen Time UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOHNNY'S SCREEN TIME                          │
│                                                                  │
│  Today: 2h 34m of 4h                                            │
│  ████████████████████░░░░░░░░░░ 64%                             │
│                                                                  │
│  BY CATEGORY                                                     │
│  ├─ Gaming         1h 45m  ████████████░░░░ 87% of 2h limit    │
│  ├─ YouTube        0h 32m  ████░░░░░░░░░░░░ 32% of 1h limit    │
│  ├─ Educational    0h 17m  No limit                             │
│  └─ Other          0h 00m                                        │
│                                                                  │
│  UPCOMING                                                        │
│  ├─ 🏫 School Mode starts in 45 min (8:00 AM)                   │
│  └─ 🌙 Bedtime Mode at 9:00 PM                                  │
│                                                                  │
│  EARN MORE TIME                                                  │
│  ├─ 🧹 Clean room (+30 min) [Mark Complete]                     │
│  └─ 📚 Finish homework (+45 min) [Mark Complete]                │
│                                                                  │
│  [Request Extra Time]  [View Weekly Report]                     │
└─────────────────────────────────────────────────────────────────┘
```

## 2.4 App Approval System

### App Request Flow

```
Child installs app → App detected → Parent notified
                                         │
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
                      [Approve]     [Deny]      [Ask Questions]
                          │              │              │
                          ▼              ▼              ▼
                    App enabled    App blocked    "Why do you
                    + time limit   + message      want this?"
```

### App Categories

| Category       | Default (6-12)  | Default (13-15) |
| -------------- | --------------- | --------------- |
| Educational    | Auto-approve    | Auto-approve    |
| Productivity   | Auto-approve    | Auto-approve    |
| Entertainment  | Parent approval | Notify          |
| Social Media   | Blocked         | Parent approval |
| Messaging      | Parent approval | Parent approval |
| Gaming         | Parent approval | Notify          |
| Dating         | Blocked         | Blocked         |
| Mature Content | Blocked         | Blocked         |

## 2.5 Contact Approval

```python
class ApprovedContact(Document):
    doctype = "Approved Contact"

    child: Link["Family Member"]

    # Contact Info
    contact_name: Data
    phone_number: Data
    email: Data
    relationship: Data  # "School friend", "Coach", etc.

    # Approval
    approved_by: Link["Family Member"]  # Parent
    approved_date: Datetime

    # Permissions
    can_call: Check
    can_text: Check
    can_video: Check

    # Monitoring
    monitor_conversations: Check  # Age-appropriate
```

## 2.6 COPPA Compliance

| Requirement                        | Implementation                                       |
| ---------------------------------- | ---------------------------------------------------- |
| Verifiable parental consent        | Parent email verification + credit card micro-charge |
| No behavioral advertising          | Ads disabled for under-13                            |
| No data sharing with third parties | All processing internal                              |
| Parent can review/delete data      | Full export and delete in settings                   |
| Limited data collection            | Only essential data collected                        |
| No external contact                | No social features, no contact with non-approved     |

## 2.7 Automatic Age-Up Transitions

```python
def daily_age_check():
    """Run daily to update age-based permissions"""
    for member in get_all_family_members():
        old_age = member.age
        new_age = calculate_age(member.date_of_birth)

        if new_age != old_age:
            member.age = new_age

            # Check for milestone transitions
            if old_age < 13 and new_age >= 13:
                trigger_13th_birthday_transition(member)
                # - Remove COPPA restrictions
                # - Enable more features
                # - Notify parents

            elif old_age < 18 and new_age >= 18:
                trigger_18th_birthday_transition(member)
                # - Full adult permissions
                # - Convert to independent account option
                # - Remove parental oversight (optional)

            member.save()
```

## 2.8 Acceptance Criteria

- [ ] Screen time limits enforced across devices
- [ ] App approval workflow functional
- [ ] Contact approval for messaging/calling
- [ ] COPPA compliance verified
- [ ] Age transitions automatic
- [ ] School/bedtime modes work
- [ ] Extra time earning system works

---

# Section 3: Family AI Voice Assistant

## 3.1 Overview

The Family AI Voice Assistant provides a shared family assistant that can speak in multiple voice personas — parents, grandparents, or AI-generated voices — while maintaining child-safe responses and family-scoped knowledge.

## 3.2 Voice Persona Options

### Available Voice Types

| Voice Type                     | Description                   | Use Case                      |
| ------------------------------ | ----------------------------- | ----------------------------- |
| **Parent Voice (Cloned)**      | Mom or Dad's actual voice     | "Mom" answering questions     |
| **Grandparent Voice (Cloned)** | Grandma or Grandpa's voice    | Storytelling, comfort         |
| **AI Character Voice**         | Pre-built friendly characters | Kids who prefer fun character |
| **Standard VA Voice**          | Professional Dartwing voices  | Neutral assistant             |
| **Custom Character**           | User-created AI persona       | Family mascot, pet voice      |

### Voice Cloning Setup

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY VOICE SETUP                            │
│                                                                  │
│  Who should the family assistant sound like?                    │
│                                                                  │
│  CLONED VOICES (record 5 sentences each)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 👩 Mom (Sarah)                                              │ │
│  │    Status: ✅ Voice trained                                 │ │
│  │    [Preview] [Re-record]                                    │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 👨 Dad (Mike)                                               │ │
│  │    Status: ✅ Voice trained                                 │ │
│  │    [Preview] [Re-record]                                    │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 👵 Grandma (Betty)                                          │ │
│  │    Status: ⏳ Pending (needs 3 more sentences)              │ │
│  │    [Continue Recording]                                     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 👴 Grandpa (Bob)                                            │ │
│  │    Status: ⚪ Not set up                                    │ │
│  │    [Start Recording]                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  AI CHARACTER VOICES                                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🤖 Buddy      - Friendly robot helper                      │ │
│  │ 🧚 Sparkle    - Magical fairy guide                        │ │
│  │ 🐕 Max        - Wise dog companion                         │ │
│  │ 🦸 Captain    - Superhero mentor                           │ │
│  │ 🌟 Nova       - Space explorer                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  DEFAULT VOICE PER FAMILY MEMBER                                │
│  ├─ Johnny (8) prefers: 🤖 Buddy                               │
│  ├─ Emma (12) prefers: 👩 Mom                                  │
│  └─ Parents default: Standard VA                               │
│                                                                  │
│  [Save Preferences]                                             │
└─────────────────────────────────────────────────────────────────┘
```

## 3.3 Voice Cloning Technical Specs

```python
class FamilyVoiceProfile(Document):
    doctype = "Family Voice Profile"

    family_member: Link["Family Member"]
    voice_name: Data  # "Mom", "Grandpa Bob"

    # Training
    training_samples: Table["Voice Training Sample"]
    training_status: Select["Not Started", "Partial", "Complete", "Processing"]
    voice_model_id: Data  # External voice clone ID

    # Quality
    quality_score: Float  # 0-1
    last_quality_check: Datetime

    # Usage
    available_to: Table MultiSelect["Family Member"]  # Who can use this voice

    # Consent
    consent_given: Check
    consent_date: Datetime
    consent_recording: Attach  # Audio of consent
```

### Voice Training Flow

1. **Consent** - Adult records verbal consent
2. **Recording** - 5-10 sentences in quiet environment
3. **Processing** - Voice model generated (2-5 minutes)
4. **Quality Check** - System verifies quality
5. **Activation** - Voice available for family

## 3.4 Child-Safe Response System

### Content Filtering for Kids

| Topic            | Response Strategy                                |
| ---------------- | ------------------------------------------------ |
| Violence         | Age-appropriate explanation, redirect            |
| Adult content    | "That's a question for Mom or Dad"               |
| Scary topics     | Gentle, reassuring response                      |
| Death/illness    | Compassionate, honest, suggest talking to parent |
| Homework help    | Educational, doesn't give answers directly       |
| Family questions | "Let's ask your parents together"                |

### Example Interactions by Age

**Child (8 years old):**

```
Johnny: "Buddy, why is the sky blue?"

Buddy (AI Character): "Great question, space explorer!
The sky looks blue because sunlight bounces around in
our atmosphere in a special way. The blue light bounces
the most, so that's what we see! Want me to tell you
more about how light works?"
```

**Tween (12 years old):**

```
Emma: "Mom, can you help me with my history essay?"

Mom Voice: "Of course, sweetie. What's the topic?
I can help you organize your thoughts and find good
sources, but remember, the words need to be yours!"
```

## 3.5 Family Knowledge Vault Integration

The Family VA has access to family-specific knowledge:

| Knowledge Source | Examples                            |
| ---------------- | ----------------------------------- |
| Family Calendar  | "What time is soccer practice?"     |
| Chore List       | "What chores do I have today?"      |
| House Rules      | "What's the bedtime rule?"          |
| Family Recipes   | "How does Grandma make cookies?"    |
| Emergency Info   | "What's the doctor's number?"       |
| Family Stories   | "Tell me about when Dad was little" |

## 3.6 Acceptance Criteria

- [ ] Parent voice cloning with 5 sentences
- [ ] Grandparent voice cloning supported
- [ ] 5+ AI character voices available
- [ ] Per-child voice preference
- [ ] Child-safe response filtering
- [ ] Family knowledge integration
- [ ] Voice consent recorded and stored

---

# Section 4: Family Calendar System

## 4.1 Overview

Unified family calendar with color-coding per member, support for recurring events, school schedules, custody handoffs, and smart conflict detection.

## 4.2 Calendar Features

| Feature                | Description                          |
| ---------------------- | ------------------------------------ |
| **Shared View**        | See all family events in one place   |
| **Personal Calendars** | Each member has private events too   |
| **Color Coding**       | Each person gets a color             |
| **Recurring Events**   | "Every Tuesday piano lesson"         |
| **School Integration** | Auto-import school calendar          |
| **RSVP Tracking**      | Who's attending which event          |
| **Reminders**          | Customizable per person              |
| **Conflict Detection** | Alert when double-booked             |
| **Travel Time**        | Auto-add driving time between events |

## 4.3 Event Types

```python
class FamilyCalendarEvent(Document):
    doctype = "Family Calendar Event"

    # Basic Info
    title: Data
    description: Text
    location: Data

    # Timing
    start_datetime: Datetime
    end_datetime: Datetime
    all_day: Check

    # Recurrence
    is_recurring: Check
    recurrence_rule: Data  # RRULE format
    recurrence_end: Date

    # Participants
    primary_person: Link["Family Member"]
    additional_attendees: Table MultiSelect["Family Member"]
    requires_transportation: Check
    driver: Link["Family Member"]

    # Type
    event_type: Select[
        "Appointment",
        "School Event",
        "Sports/Activity",
        "Birthday/Anniversary",
        "Family Gathering",
        "Chore/Task",
        "Custody Handoff",
        "Vacation/Travel",
        "Work (Parent)",
        "Other"
    ]

    # External Sync
    external_calendar_id: Data
    external_source: Select["Google", "Apple", "Microsoft", "School"]

    # Reminders
    reminders: Table["Event Reminder"]
```

## 4.4 Calendar UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY CALENDAR - NOVEMBER                    │
│                                                                  │
│  [◀ Oct]  November 2025  [Dec ▶]    [Day] [Week] [Month]       │
│                                                                  │
│  Color Key: 🔵 Mom  🟢 Dad  🟡 Johnny  🟠 Emma  🟣 Family       │
│                                                                  │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐                   │
│  │ Sun │ Mon │ Tue │ Wed │ Thu │ Fri │ Sat │                   │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤                   │
│  │     │     │     │     │     │     │  1  │                   │
│  │     │     │     │     │     │     │     │                   │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤                   │
│  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │                   │
│  │     │🟡Soc│🟡Pia│🟠Den│🔵Wor│🟣Mov│     │                   │
│  │     │cer │no   │tist │k ev │ie   │     │                   │
│  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤                   │
│  │  9  │ 10  │ 11  │ 12  │ 13  │ 14  │ 15  │                   │
│  │     │🟡Soc│🟡Pia│     │🟠Sci│🟢Dad│🟣BBQ│                   │
│  │     │cer │no   │     │Fair│Trip │    │                      │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘                   │
│                                                                  │
│  TODAY - November 6                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 8:00 AM   🟡🟠 School drop-off                             │ │
│  │ 9:00 AM   🔵 Work meeting                                  │ │
│  │ 3:30 PM   🟡 Soccer practice @ Field B                     │ │
│  │           └─ 🟢 Dad driving                                │ │
│  │ 5:00 PM   🟠 Emma dentist @ Dr. Smith                      │ │
│  │           └─ 🔵 Mom driving                                │ │
│  │ 6:30 PM   🟣 Family dinner                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [+ Add Event]  [Sync Calendars]  [Print Week]                  │
└─────────────────────────────────────────────────────────────────┘
```

## 4.5 Smart Features

### Conflict Detection

```
⚠️ SCHEDULING CONFLICT DETECTED

Emma has two events at the same time on November 13:

├─ 3:30 PM - Science Fair Setup (School)
└─ 4:00 PM - Piano Lesson (Ms. Johnson's)

Options:
[Reschedule Piano] [Cancel Piano] [Notify Teacher] [Ignore]
```

### Transportation Coordination

```
TRANSPORTATION NEEDED - November 6

┌────────────────────────────────────────────────────────────────┐
│ 3:30 PM - Johnny's Soccer Practice                             │
│ Location: Sports Complex (15 min drive)                        │
│                                                                │
│ Who's driving?                                                  │
│ ○ 🟢 Dad (available)                                           │
│ ○ 🔵 Mom (has dentist with Emma at 5:00)                       │
│ ○ 👋 Request carpool (Johnson family offered)                  │
│                                                                │
│ [Assign Dad] [Request Carpool] [Need Help]                     │
└────────────────────────────────────────────────────────────────┘
```

## 4.6 External Calendar Sync

| Source          | Sync Type      | Notes      |
| --------------- | -------------- | ---------- |
| Google Calendar | Two-way        | Full OAuth |
| Apple iCloud    | Two-way        | Full OAuth |
| Microsoft 365   | Two-way        | Full OAuth |
| School Calendar | One-way import | iCal feed  |
| Sports League   | One-way import | iCal feed  |

## 4.7 Acceptance Criteria

- [ ] Color-coded family calendar
- [ ] Recurring events with RRULE
- [ ] External calendar sync (Google, Apple, Microsoft)
- [ ] School calendar import
- [ ] Conflict detection and alerts
- [ ] Transportation coordination
- [ ] Custody schedule integration
- [ ] Per-person reminders

---

# Section 5: Chores, Allowance & Academic Rewards System

## 5.1 Overview

Comprehensive system for managing household chores, tracking completion, tying rewards to performance, and integrating academic achievements into the family reward economy.

## 5.2 Chore Management

### Chore Template System

```python
class ChoreTemplate(Document):
    doctype = "Chore Template"

    # Basic Info
    chore_name: Data
    description: Text
    instructions: Text
    estimated_duration_minutes: Int

    # Categorization
    category: Select[
        "Bedroom", "Bathroom", "Kitchen", "Living Areas",
        "Outdoor", "Pet Care", "Laundry", "Dishes", "Other"
    ]
    difficulty: Select["Easy", "Medium", "Hard"]

    # Age Appropriateness
    minimum_age: Int
    maximum_age: Int

    # Verification
    requires_photo_proof: Check
    requires_parent_verification: Check
    verification_checklist: Table["Chore Checklist Item"]

    # Rewards
    base_points: Int
    base_money_reward: Currency
    bonus_for_early: Currency
    screen_time_bonus_minutes: Int

    # Scheduling
    default_frequency: Select["Daily", "Weekly", "Bi-Weekly", "Monthly", "As Needed"]
    default_day_of_week: Select
    default_time: Time
```

### Chore Assignment

```python
class ChoreAssignment(Document):
    doctype = "Chore Assignment"

    # What & Who
    chore_template: Link["Chore Template"]
    assigned_to: Link["Family Member"]
    assigned_by: Link["Family Member"]

    # When
    due_date: Date
    due_time: Time
    recurrence: Link["Chore Recurrence"]

    # Status
    status: Select["Pending", "In Progress", "Completed", "Verified", "Overdue", "Skipped"]

    # Completion
    completed_at: Datetime
    completion_photo: Attach Image
    completion_notes: Text

    # Verification
    verified_by: Link["Family Member"]
    verified_at: Datetime
    verification_status: Select["Approved", "Needs Redo", "Partial Credit"]
    verification_notes: Text

    # Rewards (calculated)
    points_earned: Int
    money_earned: Currency
    screen_time_earned: Int
    bonuses_applied: Table["Chore Bonus"]
```

### Chore Board UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOHNNY'S CHORE BOARD                          │
│                                                                  │
│  Week of November 4-10, 2025                                    │
│                                                                  │
│  EARNINGS THIS WEEK                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  💰 $12.50 earned    🎮 45 min screen time    ⭐ 85 pts  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  TODAY'S CHORES (November 6)                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ✅ Make bed                              $0.50  +5 pts     │ │
│  │    Completed 7:15 AM                                       │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ⏳ Clean room                            $2.00  +15 pts    │ │
│  │    Due by 6:00 PM                                          │ │
│  │    📸 Photo required                                       │ │
│  │    [Start] [I Need Help]                                   │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ⏳ Feed the dog                          $0.50  +5 pts     │ │
│  │    Due by 5:00 PM                                          │ │
│  │    [Mark Done]                                             │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ⭐ BONUS: Help with dishes               $1.00  +10 pts    │ │
│  │    Optional extra credit!                                  │ │
│  │    [I'll Do It!]                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  THIS WEEK                                                       │
│  │ Mon │ Tue │ Wed │ Thu │ Fri │ Sat │ Sun │                   │
│  │ ✅✅ │ ✅✅ │ ⏳⏳ │ ⬜⬜ │ ⬜⬜ │ ⬜⬜⬜│ ⬜⬜ │                   │
│                                                                  │
│  STREAKS 🔥                                                      │
│  ├─ "Make Bed" - 12 days in a row! (+$1 bonus at 14)           │
│  └─ "Feed Dog" - 8 days in a row!                              │
│                                                                  │
│  [View All Chores]  [Request New Chore]  [Chore Store]          │
└─────────────────────────────────────────────────────────────────┘
```

## 5.3 Academic Rewards Integration

### Grade Tracking

```python
class AcademicRecord(Document):
    doctype = "Academic Record"

    student: Link["Family Member"]
    school_year: Data  # "2025-2026"

    # External Integration
    integration_type: Select[
        "Manual Entry",
        "Google Classroom",
        "Canvas",
        "PowerSchool",
        "Seesaw",
        "School Dartwing Module",
        "Other LMS"
    ]
    external_id: Data
    last_sync: Datetime

    # Classes
    classes: Table["Academic Class"]

    # Overall
    current_gpa: Float
    grade_level: Data  # "3rd Grade", "8th Grade"
```

```python
class AcademicClass(Document):
    doctype = "Academic Class"

    class_name: Data  # "Math", "Science"
    teacher_name: Data

    # Grades
    current_grade_percent: Float
    current_letter_grade: Data

    # Assignments
    assignments: Table["Academic Assignment"]

    # Missing Work
    missing_assignments: Int
    late_assignments: Int
```

### Grade-Based Rewards

```python
class GradeRewardRule(Document):
    doctype = "Grade Reward Rule"

    family_member: Link["Family Member"]

    # Rule Type
    rule_type: Select[
        "Grade Threshold",      # A = $X
        "Improvement Bonus",    # +5% = $X
        "Perfect Score",        # 100% = $X
        "No Missing Work",      # Weekly bonus
        "GPA Target"           # End of term
    ]

    # Thresholds
    grade_threshold: Data  # "A", "B", "90%"
    improvement_percent: Float

    # Rewards
    money_reward: Currency
    points_reward: Int
    screen_time_reward: Int
    special_reward: Data  # "Pizza night choice"

    # Frequency
    frequency: Select["Per Assignment", "Per Class Weekly", "Per Report Card"]
```

### Academic Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    EMMA'S ACADEMIC TRACKER                       │
│                                                                  │
│  Current GPA: 3.7                                               │
│                                                                  │
│  CLASSES                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Math          │ 94% A  │ ✅ All work complete              │ │
│  │ Science       │ 88% B+ │ ⚠️ 1 missing assignment           │ │
│  │ English       │ 91% A- │ ✅ All work complete              │ │
│  │ History       │ 86% B  │ ✅ All work complete              │ │
│  │ Art           │ 95% A  │ ✅ All work complete              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ⚠️ MISSING WORK                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Science - "Ecosystem Lab Report"                           │ │
│  │ Due: November 4 (2 days overdue)                           │ │
│  │ Impact: Grade will drop to 85% if not submitted            │ │
│  │                                                            │ │
│  │ [Mark Submitted]  [Get Help]  [Message Teacher]            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  RECENT REWARDS                                                  │
│  ├─ Nov 5: Math test 98% → +$5.00 (A grade bonus)              │
│  ├─ Nov 3: English essay 100% → +$3.00 (Perfect score!)        │
│  └─ Oct 30: Weekly no-missing-work → +$2.00                    │
│                                                                  │
│  TERM GOALS                                                      │
│  ├─ 📊 Maintain GPA above 3.5 → +$25 at end of semester        │
│  └─ 📚 No missing work for month → Extra movie night           │
│                                                                  │
│  [Sync with School]  [View Full Report]  [Set New Goal]         │
└─────────────────────────────────────────────────────────────────┘
```

## 5.4 Educational Platform Integration

### Supported Platforms

| Platform                   | Integration Level     | Data Synced                       |
| -------------------------- | --------------------- | --------------------------------- |
| **Google Classroom**       | Full API              | Assignments, grades, missing work |
| **Canvas**                 | Full API              | Full gradebook, submissions       |
| **PowerSchool**            | API (where available) | Grades, attendance                |
| **Seesaw**                 | API                   | Activities, teacher messages      |
| **ClassDojo**              | API                   | Behavior points, messages         |
| **Khan Academy**           | API                   | Progress, mastery levels          |
| **IXL**                    | API                   | Skills, time spent                |
| **Duolingo**               | API                   | Streaks, lessons                  |
| **School Dartwing Module** | Full                  | Native integration                |

### AI Learning Platform Tracking

```python
class LearningPlatformProgress(Document):
    doctype = "Learning Platform Progress"

    student: Link["Family Member"]
    platform: Select[
        "Khan Academy",
        "IXL",
        "Duolingo",
        "ABCmouse",
        "Prodigy",
        "BrainPOP",
        "Coursera Kids",
        "Custom"
    ]

    # Progress
    current_level: Data
    total_time_minutes: Int
    lessons_completed: Int
    skills_mastered: Int
    current_streak: Int

    # Rewards
    reward_per_lesson: Currency
    reward_per_skill: Currency
    streak_bonus: Currency
```

## 5.5 Reward System Architecture

### Points Economy

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY POINTS ECONOMY                         │
│                                                                  │
│  EARNING POINTS                                                  │
│  ├─ Chores: 5-25 points based on difficulty                     │
│  ├─ Grades: 10-50 points based on achievement                   │
│  ├─ Learning: 5 points per lesson completed                     │
│  ├─ Good behavior: 10 points (parent discretion)                │
│  ├─ Helping others: 15 points                                   │
│  └─ Streaks: Bonus multiplier (1.5x after 7 days)               │
│                                                                  │
│  SPENDING POINTS                                                 │
│  ├─ Screen time: 10 points = 15 minutes                         │
│  ├─ Later bedtime: 50 points = 30 min on weekend                │
│  ├─ Pick dinner: 30 points                                      │
│  ├─ Movie choice: 40 points                                     │
│  ├─ Friend sleepover: 100 points                                │
│  └─ Special outing: 200 points                                  │
│                                                                  │
│  CONVERSION                                                      │
│  └─ 100 points = $5 (optional, parent-configured)               │
└─────────────────────────────────────────────────────────────────┘
```

### Allowance Payment

```python
class AllowancePayment(Document):
    doctype = "Allowance Payment"

    recipient: Link["Family Member"]

    # Amount
    amount: Currency

    # Source
    source_type: Select[
        "Base Allowance",    # Weekly/monthly base
        "Chore Completion",  # From chores
        "Grade Reward",      # From academics
        "Learning Reward",   # From educational apps
        "Bonus",             # Parent discretionary
        "Point Conversion"   # Points to money
    ]
    source_reference: Dynamic Link

    # Destination
    destination: Select[
        "Family Piggy Bank",
        "Savings Goal",
        "Spending Balance",
        "External Account"   # Greenlight, real bank
    ]

    # Status
    status: Select["Pending", "Approved", "Paid", "Declined"]
    approved_by: Link["Family Member"]
    paid_at: Datetime
```

## 5.6 Acceptance Criteria

- [ ] Chore templates with age-appropriate filtering
- [ ] Photo proof for chore completion
- [ ] Parent verification workflow
- [ ] Streak tracking with bonuses
- [ ] Grade sync from 5+ educational platforms
- [ ] Grade-based reward rules
- [ ] Points economy functional
- [ ] Allowance auto-payment on approval

---

# Section 6: Family Savings & Piggy Bank

## 6.1 Overview

Digital family savings system with individual "piggy banks," goal-based saving, gamification, and family savings challenges.

## 6.2 Account Types

| Account Type         | Owner      | Purpose                   |
| -------------------- | ---------- | ------------------------- |
| **Child Piggy Bank** | Each child | Personal savings          |
| **Teen Account**     | Each teen  | Higher limits, debit card |
| **Family Savings**   | Shared     | Vacation, big purchases   |
| **Emergency Fund**   | Parents    | Safety net                |
| **College Fund**     | Per child  | Long-term education       |

## 6.3 Savings Goal System

```python
class SavingsGoal(Document):
    doctype = "Savings Goal"

    # Owner
    owner_type: Select["Individual", "Family"]
    owner: Link["Family Member"]  # or null for family

    # Goal Details
    goal_name: Data
    description: Text
    goal_image: Attach Image  # Picture of what they're saving for

    # Target
    target_amount: Currency
    target_date: Date

    # Progress
    current_amount: Currency
    percent_complete: Float

    # Auto-Save
    auto_contribute: Check
    auto_contribute_amount: Currency
    auto_contribute_frequency: Select["Weekly", "Bi-Weekly", "Monthly"]
    auto_contribute_source: Select["Allowance", "Chore Earnings", "External"]

    # Gamification
    enable_gamification: Check
    milestone_rewards: Table["Savings Milestone Reward"]

    # Matching
    parent_match_enabled: Check
    parent_match_percent: Float  # 50% = parents add $0.50 for every $1
    parent_match_cap: Currency
```

### Savings Goal UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOHNNY'S PIGGY BANK                           │
│                                                                  │
│  Total Balance: $127.50                                         │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  🎮 NINTENDO SWITCH                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  [🎮 Switch Image]                                         │ │
│  │                                                            │ │
│  │  $89.50 of $299.00                                         │ │
│  │  █████████░░░░░░░░░░░░░░░░░░░░ 30%                        │ │
│  │                                                            │ │
│  │  🎯 Target: December 25, 2025 (49 days)                    │ │
│  │  📈 Need: $4.28/week to reach goal                         │ │
│  │                                                            │ │
│  │  💰 Parent Matching: 25% (Dad will add $0.25 per $1!)     │ │
│  │                                                            │ │
│  │  MILESTONES                                                │ │
│  │  ├─ ✅ 10% ($30) - Unlocked game recommendation            │ │
│  │  ├─ ✅ 25% ($75) - Chose Switch color (Red!)               │ │
│  │  ├─ ⏳ 50% ($150) - Pick first game to buy                 │ │
│  │  └─ ⏳ 100% - IT'S YOURS! 🎉                               │ │
│  │                                                            │ │
│  │  [Add Money]  [Auto-Save Settings]  [Edit Goal]           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  🏖️ FAMILY VACATION FUND (shared)                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  $1,250 of $5,000  ████████░░░░░░░░░░░░░░░░ 25%           │ │
│  │  🎯 Target: Summer 2026                                    │ │
│  │                                                            │ │
│  │  Family contributions this month:                          │ │
│  │  ├─ Mom & Dad: $200                                        │ │
│  │  ├─ Johnny: $5 (from allowance)                            │ │
│  │  └─ Emma: $8 (from allowance)                              │ │
│  │                                                            │ │
│  │  [Contribute]  [View History]                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  QUICK ACTIONS                                                   │
│  [+ New Goal]  [Transfer Between Goals]  [Cash Out]             │
└─────────────────────────────────────────────────────────────────┘
```

## 6.4 Gamification Features

### Savings Challenges

| Challenge         | Description                       | Reward                  |
| ----------------- | --------------------------------- | ----------------------- |
| **First $10**     | Save your first $10               | Badge + $1 bonus        |
| **Week Streak**   | Save something 7 days in a row    | 10% bonus               |
| **Goal Crusher**  | Reach a goal early                | Badge + surprise reward |
| **Family Saver**  | Everyone contributes in same week | Family pizza night      |
| **Round-Up Hero** | Use round-up feature for month    | Badge                   |

### Visual Progress

```
JOHNNY'S SAVINGS JOURNEY

Level 5 Saver ⭐⭐⭐⭐⭐
XP: 2,450 / 3,000 to Level 6

Badges Earned:
🥇 First Goal    🔥 30-Day Streak    💪 $100 Club
🎯 Goal Crusher  🏆 Family Saver     ⭐ Super Saver

Current Streak: 12 days 🔥
Best Streak: 34 days
```

## 6.5 Parent Matching Programs

```python
class ParentMatchProgram(Document):
    doctype = "Parent Match Program"

    child: Link["Family Member"]

    # Matching Rules
    match_type: Select[
        "Percentage",     # Match X% of deposits
        "Dollar for Dollar",  # 1:1 up to cap
        "Goal-Based"      # Only match toward specific goals
    ]

    match_percent: Float
    match_cap_per_deposit: Currency
    match_cap_per_month: Currency
    match_cap_total: Currency

    # Conditions
    require_chore_completion: Check
    require_grade_threshold: Data  # "B or higher"

    # Tracking
    total_matched: Currency
    remaining_cap: Currency
```

## 6.6 Acceptance Criteria

- [ ] Individual piggy banks per child
- [ ] Family shared savings goals
- [ ] Visual progress tracking
- [ ] Parent matching programs
- [ ] Gamification with badges/streaks
- [ ] Auto-save from allowance
- [ ] Milestone rewards
- [ ] Cash-out to real accounts (optional)

---

# Section 7: Emergency & Medical Hub

## 7.1 Overview

Centralized family health and emergency information system with one-tap sharing, QR code access for emergencies, and integration with MedxHealthLinc.

## 7.2 Medical Profile

```python
class FamilyMedicalProfile(Document):
    doctype = "Family Medical Profile"

    family_member: Link["Family Member"]

    # Basic Info
    blood_type: Select["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]
    height: Data
    weight: Data

    # Allergies
    allergies: Table["Medical Allergy"]
    allergy_severity: Select["Mild", "Moderate", "Severe", "Life-Threatening"]

    # Conditions
    medical_conditions: Table["Medical Condition"]

    # Medications
    current_medications: Table["Current Medication"]

    # Immunizations
    immunization_records: Table["Immunization Record"]

    # Insurance
    insurance_provider: Data
    insurance_policy_number: Data
    insurance_group: Data
    insurance_card_front: Attach Image
    insurance_card_back: Attach Image

    # Healthcare Providers
    primary_care_physician: Link["Healthcare Provider"]
    specialists: Table["Healthcare Provider Link"]
    preferred_hospital: Data
    preferred_pharmacy: Data

    # Emergency Contacts
    emergency_contacts: Table["Emergency Contact"]

    # Documents
    medical_documents: Table["Medical Document"]

    # MedxHealthLinc Integration
    healthlinc_connected: Check
    healthlinc_user_id: Data
    last_healthlinc_sync: Datetime
```

## 7.3 Emergency QR Code

```
┌─────────────────────────────────────────────────────────────────┐
│                    EMERGENCY MEDICAL QR                          │
│                                                                  │
│  JOHNNY SMITH - Age 8                                           │
│                                                                  │
│  ┌─────────────────────┐                                        │
│  │                     │                                        │
│  │    [QR CODE]        │  Scan in emergency to see:            │
│  │                     │  • Allergies (PEANUTS - severe)        │
│  │                     │  • Blood type (A+)                     │
│  │                     │  • Medications (Zyrtec daily)          │
│  │                     │  • Emergency contacts                  │
│  │                     │  • Insurance info                      │
│  └─────────────────────┘  • Primary doctor                      │
│                                                                  │
│  This QR provides LIMITED emergency info only.                  │
│  Full medical records require authentication.                    │
│                                                                  │
│  [Print Wallet Card]  [Add to Apple Wallet]  [Share with ER]   │
│                                                                  │
│  QUICK SHARE OPTIONS                                             │
│  ├─ 📱 Text to ER (includes location)                           │
│  ├─ 📧 Email to hospital                                        │
│  └─ 📋 Copy info to clipboard                                   │
│                                                                  │
│  ICE CONTACTS                                                    │
│  ├─ 1. Mom (Sarah): 555-123-4567                                │
│  ├─ 2. Dad (Mike): 555-234-5678                                 │
│  └─ 3. Grandma: 555-345-6789                                    │
└─────────────────────────────────────────────────────────────────┘
```

## 7.4 MedxHealthLinc Integration

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEDX HEALTHLINC INTEGRATION                   │
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────────────────┐   │
│  │ Dartwing Family │ ◄─────► │ MedxHealthLinc App          │   │
│  │                 │   API   │                             │   │
│  │ • Basic health  │         │ • Full health tracking      │   │
│  │ • Emergency info│         │ • Wearable integration      │   │
│  │ • Medications   │         │ • Telehealth                │   │
│  │ • Allergies     │         │ • Lab results               │   │
│  │ • Doctor info   │         │ • Detailed analytics        │   │
│  └─────────────────┘         └─────────────────────────────┘   │
│                                                                  │
│  DATA SYNC                                                       │
│  ├─ From HealthLinc → Dartwing: Vitals summary, alerts         │
│  └─ From Dartwing → HealthLinc: Family member profiles         │
│                                                                  │
│  PROMOTION                                                       │
│  "For advanced health tracking, weight management, and          │
│   wearable integration, download MedxHealthLinc!"               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Lightweight Health Features in Dartwing Family

| Feature               | Dartwing Family  | MedxHealthLinc |
| --------------------- | ---------------- | -------------- |
| Basic vitals tracking | ✓ (manual entry) | ✓ (automatic)  |
| Medication reminders  | ✓                | ✓ (advanced)   |
| Allergies             | ✓                | ✓              |
| Doctor appointments   | ✓                | ✓              |
| Immunization records  | ✓                | ✓              |
| Weight tracking       | Basic            | Full analytics |
| Diet tracking         | Plugin           | Full feature   |
| Wearable sync         | ✗                | ✓              |
| Telehealth            | ✗                | ✓              |
| Lab results           | ✗                | ✓              |

## 7.5 Health Plugin Architecture

```python
class HealthPlugin(Document):
    doctype = "Health Plugin"

    # Plugin Info
    plugin_name: Data
    plugin_type: Select[
        "Diet Tracking",
        "Weight Loss",
        "Fitness",
        "Mental Health",
        "Sleep",
        "Nutrition"
    ]

    # Configuration
    enabled: Check
    settings: JSON

    # External App Link
    external_app: Data  # "MedxHealthLinc", "MyFitnessPal", etc.
    connect_prompt: Text  # "Connect to MedxHealthLinc for full features"

    # Lightweight Features (in Dartwing)
    basic_tracking: Check
    basic_goals: Check

    # Full Features (in external app)
    full_feature_redirect: Check
```

### Diet Plugin Example

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIET & NUTRITION (Basic)                      │
│                                                                  │
│  SUPPORTED DIET TYPES                                            │
│  ├─ General Healthy Eating                                       │
│  ├─ Low Carb / Keto                                             │
│  ├─ Vegetarian / Vegan                                          │
│  ├─ Mediterranean                                                │
│  ├─ DASH (Heart Healthy)                                        │
│  ├─ Gluten-Free                                                 │
│  ├─ Diabetic-Friendly                                           │
│  └─ Custom                                                       │
│                                                                  │
│  BASIC FEATURES (in Dartwing)                                   │
│  ├─ Set diet type per family member                             │
│  ├─ Meal suggestions aligned to diet                            │
│  ├─ Grocery list filtering                                      │
│  └─ Basic calorie tracking                                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 💡 Want detailed meal plans, macro tracking, and AI        │ │
│  │    nutrition coaching?                                      │ │
│  │                                                            │ │
│  │    [Download MedxHealthLinc] - Full nutrition suite        │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 7.6 Acceptance Criteria

- [ ] Medical profile per family member
- [ ] Emergency QR code generation
- [ ] One-tap ER share
- [ ] ICE contacts with quick dial
- [ ] Insurance card storage
- [ ] Vaccination record tracking
- [ ] MedxHealthLinc API integration
- [ ] Diet plugin with type selection
- [ ] Graceful upsell to HealthLinc

---

# Section 8: Location Sharing & Family GIS

## 8.1 Overview

Real-time family location tracking with map visualization, geofencing, safety alerts, and privacy controls appropriate for each family member's age.

## 8.2 GIS Map Features

### Family Map View

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY MAP                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │           🏠 Home                                       │    │
│  │             │                                           │    │
│  │    🔵 Dad   │                                           │    │
│  │    "At work"│                                           │    │
│  │             │                    🏫 School              │    │
│  │             │                      │                    │    │
│  │             │                 🟡 Johnny                 │    │
│  │             │                 "At school"               │    │
│  │             │                      │                    │    │
│  │    🟣 Mom ──┘                     │                    │    │
│  │    "5 min from home"              │                    │    │
│  │             │                      │                    │    │
│  │             └──────────────────────┘                    │    │
│  │                                                         │    │
│  │                        ⚽ Soccer Field                  │    │
│  │                          │                              │    │
│  │                     🟠 Emma                             │    │
│  │                     "At soccer practice"                │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  FAMILY STATUS                                                   │
│  ├─ 🔵 Dad (Mike) - At Work (Downtown Office)                   │
│  │   └─ Last updated: 2 min ago                                 │
│  ├─ 🟣 Mom (Sarah) - Driving home                               │
│  │   └─ ETA: 5 minutes                                          │
│  ├─ 🟡 Johnny - At Lincoln Elementary                           │
│  │   └─ School ends: 3:30 PM (45 min)                          │
│  └─ 🟠 Emma - At soccer practice                                │
│      └─ Practice ends: 5:00 PM                                  │
│                                                                  │
│  [Center on Home]  [Traffic View]  [History]  [Alerts]          │
└─────────────────────────────────────────────────────────────────┘
```

## 8.3 Geofencing System

```python
class FamilyGeofence(Document):
    doctype = "Family Geofence"

    # Location
    name: Data  # "Home", "School", "Grandma's House"
    location_type: Select[
        "Home", "School", "Work", "Relative",
        "Friend", "Activity", "Restricted", "Custom"
    ]

    # Coordinates
    latitude: Float
    longitude: Float
    radius_meters: Int

    # Shape (for complex areas)
    shape_type: Select["Circle", "Polygon"]
    polygon_coordinates: JSON  # For polygon shapes

    # Alerts
    alert_on_arrival: Check
    alert_on_departure: Check
    alert_recipients: Table MultiSelect["Family Member"]

    # Time-based rules
    expected_arrival_time: Time
    expected_departure_time: Time
    alert_if_not_arrived_by: Time

    # Applicable members
    applies_to: Table MultiSelect["Family Member"]

    # Restrictions (for teens)
    is_restricted_zone: Check
    restriction_message: Text
```

### Geofence Alerts

| Event            | Alert Example                                 |
| ---------------- | --------------------------------------------- |
| Arrive Home      | "Johnny arrived home at 3:45 PM"              |
| Leave School     | "Emma left school at 3:32 PM"                 |
| Enter Restricted | "⚠️ Johnny entered restricted zone (Mall)"    |
| Late Arrival     | "⚠️ Emma hasn't arrived at soccer by 4:15 PM" |
| Curfew Zone      | "⚠️ Teen outside approved area after 10 PM"   |

## 8.4 Location History

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOHNNY'S LOCATION HISTORY                     │
│                                                                  │
│  November 6, 2025                                               │
│                                                                  │
│  TIMELINE                                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 7:15 AM │ 🏠 Left home                                     │ │
│  │         │ ↓ 12 min drive                                   │ │
│  │ 7:27 AM │ 🏫 Arrived at school                             │ │
│  │         │ At school for 8h 3m                              │ │
│  │ 3:30 PM │ 🏫 Left school                                   │ │
│  │         │ ↓ 8 min drive (Dad picked up)                    │ │
│  │ 3:38 PM │ ⚽ Arrived at soccer field                       │ │
│  │         │ At practice for 1h 30m                           │ │
│  │ 5:08 PM │ ⚽ Left soccer                                   │ │
│  │         │ ↓ 15 min drive                                   │ │
│  │ 5:23 PM │ 🏠 Arrived home                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  MAP VIEW                                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │    🏠───────────🏫                                         │ │
│  │                  │                                         │ │
│  │                  ⚽                                         │ │
│  │                                                            │ │
│  │    [Play Animation]  [Export]                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Previous Day]  [Select Date]  [Next Day]                     │
└─────────────────────────────────────────────────────────────────┘
```

## 8.5 Privacy Controls by Age

| Feature            | Child (6-12)      | Teen (13-15)        | Teen (16-17)              | Adult  |
| ------------------ | ----------------- | ------------------- | ------------------------- | ------ |
| Real-time location | Always shared     | Parent choice       | Can request privacy hours | Opt-in |
| Location history   | Full (to parents) | 7 days              | 24 hours                  | Opt-in |
| Geofence alerts    | All               | Parent configurable | Limited                   | Opt-in |
| "Ghost mode"       | Not available     | Not available       | 2 hours max               | Full   |

## 8.6 Safety Features

### Check-In Request

```
┌────────────────────────────────────────────────────────────────┐
│ 📍 CHECK-IN REQUEST                                            │
│                                                                │
│ Mom is requesting your location.                               │
│ "Just checking you got to practice safely!"                    │
│                                                                │
│ [Share Location]  [Call Mom]  [I'm Busy - Reply Later]        │
└────────────────────────────────────────────────────────────────┘
```

### Emergency SOS

```
┌────────────────────────────────────────────────────────────────┐
│ 🆘 EMERGENCY SOS                                               │
│                                                                │
│ Press and hold for 3 seconds to alert family                  │
│                                                                │
│      ┌───────────────────┐                                    │
│      │                   │                                    │
│      │    [SOS BUTTON]   │                                    │
│      │                   │                                    │
│      └───────────────────┘                                    │
│                                                                │
│ This will:                                                     │
│ • Share your exact location with all family members           │
│ • Send "I need help!" message                                 │
│ • Start recording audio (optional)                            │
│ • Call your #1 emergency contact                              │
└────────────────────────────────────────────────────────────────┘
```

## 8.7 Acceptance Criteria

- [ ] Real-time map with all family members
- [ ] Color-coded location pins
- [ ] Geofencing with arrival/departure alerts
- [ ] Location history with timeline view
- [ ] Age-appropriate privacy controls
- [ ] Check-in request feature
- [ ] Emergency SOS with location broadcast
- [ ] Battery-efficient location tracking

---

# Section 9: Home Automation Integration

## 9.1 Overview

Integration layer connecting Dartwing Family to popular home automation platforms, enabling voice control, automation triggers, and family-aware smart home features.

## 9.2 Supported Platforms

### Tier 1 Integrations (Full Support)

| Platform                | Integration Level    | Features                                        |
| ----------------------- | -------------------- | ----------------------------------------------- |
| **Home Assistant**      | Full API + Events    | Complete device control, automations, presence  |
| **Apple HomeKit**       | HomeKit API          | Device control, scenes, Siri integration        |
| **Google Home**         | Google Home API      | Device control, routines, Assistant integration |
| **Amazon Alexa**        | Alexa Smart Home API | Device control, routines, voice integration     |
| **Samsung SmartThings** | SmartThings API      | Device control, automations, scenes             |

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOME AUTOMATION INTEGRATION                   │
│                                                                  │
│  ┌─────────────────┐                                            │
│  │ Dartwing Family │                                            │
│  │     App         │                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │ Dartwing Home   │                                            │
│  │ Integration Hub │                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│     ┌─────┴─────┬──────────┬──────────┬──────────┐             │
│     ▼           ▼          ▼          ▼          ▼             │
│  ┌──────┐  ┌────────┐  ┌───────┐  ┌───────┐  ┌────────┐       │
│  │ Home │  │ Apple  │  │Google │  │Amazon │  │Samsung │       │
│  │Assist│  │HomeKit │  │ Home  │  │ Alexa │  │SmartTh.│       │
│  └──────┘  └────────┘  └───────┘  └───────┘  └────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 9.3 Family-Aware Home Features

### Presence-Based Automation

```python
class FamilyHomeAutomation(Document):
    doctype = "Family Home Automation"

    automation_name: Data

    # Trigger
    trigger_type: Select[
        "Family Member Arrives",
        "Family Member Leaves",
        "Last Person Leaves",
        "First Person Arrives",
        "Everyone Home",
        "Bedtime Triggered",
        "Morning Routine",
        "Schedule"
    ]

    trigger_member: Link["Family Member"]  # Optional
    trigger_location: Link["Family Geofence"]

    # Conditions
    conditions: Table["Automation Condition"]
    # e.g., "Only if after sunset", "Only on weekdays"

    # Actions
    actions: Table["Home Automation Action"]
    # e.g., "Turn on lights", "Set thermostat", "Lock doors"

    # Platform
    target_platform: Select["Home Assistant", "HomeKit", "Google Home", "Alexa", "SmartThings"]
```

### Example Automations

| Trigger                         | Action                                      |
| ------------------------------- | ------------------------------------------- |
| Last person leaves home         | Lock doors, arm security, adjust thermostat |
| First person arrives home       | Disarm security, turn on entry lights       |
| Johnny arrives home from school | Send notification to parents                |
| Bedtime for Johnny              | Dim lights in his room, turn off TV         |
| Mom arrives home                | Play her favorite music in kitchen          |
| Everyone home for dinner        | Dining room lights to 80%                   |

## 9.4 Voice Control Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY VOICE COMMANDS                         │
│                                                                  │
│  HOME CONTROL (via Family VA)                                   │
│                                                                  │
│  "Hey [VA Name], turn on the living room lights"               │
│  "Set the thermostat to 72"                                     │
│  "Lock all the doors"                                           │
│  "Is the garage door closed?"                                   │
│  "Turn on movie mode in the family room"                        │
│  "Set Johnny's room to bedtime mode"                            │
│                                                                  │
│  FAMILY-AWARE COMMANDS                                           │
│                                                                  │
│  "Is everyone home?"                                            │
│  "When did Dad get home?"                                       │
│  "Turn off the lights in empty rooms"                           │
│  "Announce dinner is ready"                                      │
│                                                                  │
│  CHILD-RESTRICTED COMMANDS                                       │
│                                                                  │
│  Kids cannot:                                                    │
│  ✗ Disarm security system                                       │
│  ✗ Unlock doors                                                 │
│  ✗ Adjust thermostat beyond ±3°                                 │
│  ✗ Control parent bedroom devices                               │
└─────────────────────────────────────────────────────────────────┘
```

## 9.5 Weather-Based Automation

### Integration with Weather Services

```python
class WeatherAutomation(Document):
    doctype = "Weather Automation"

    # Weather Conditions
    weather_trigger: Select[
        "Rain Expected",
        "Snow Expected",
        "Temperature Below",
        "Temperature Above",
        "Severe Weather Alert",
        "Frost Warning",
        "High UV Index"
    ]

    threshold_value: Float  # For temperature triggers

    # Actions
    action_type: Select[
        "Adjust Irrigation",
        "Create Chore",
        "Send Alert",
        "Adjust Thermostat",
        "Close Windows/Blinds",
        "Call Service"
    ]

    # Specific Actions
    irrigation_adjustment: Select["Cancel", "Reduce 50%", "Delay 24h"]
    chore_to_create: Link["Chore Template"]
    service_to_call: Link["Service Provider"]
    alert_message: Text
```

### Weather Automation Examples

| Condition          | Automatic Action                                    |
| ------------------ | --------------------------------------------------- |
| Rain forecast      | Cancel lawn irrigation                              |
| Snow >2 inches     | Create "shovel driveway" chore OR call snow service |
| Frost warning      | Notify to cover plants, adjust sprinklers           |
| Heat wave          | Adjust A/C schedule, close blinds midday            |
| Drought conditions | Reduce irrigation 50%, alert for water conservation |

### Smart Irrigation Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMART IRRIGATION                              │
│                                                                  │
│  CURRENT STATUS                                                  │
│  ├─ Lawn (Zone 1): Last watered 2 days ago                      │
│  ├─ Garden (Zone 2): Last watered yesterday                     │
│  └─ Planters (Zone 3): Last watered 3 days ago                  │
│                                                                  │
│  UPCOMING SCHEDULE                                               │
│  ├─ Tomorrow 6 AM: Lawn (Zone 1) - 20 min                       │
│  └─ Thursday 6 AM: All zones                                    │
│                                                                  │
│  WEATHER ADJUSTMENT                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🌧️ Rain forecast for tomorrow (0.5 inches)                 │ │
│  │                                                            │ │
│  │ ✅ Automatically skipped tomorrow's irrigation             │ │
│  │    Rescheduled to Friday if no more rain expected         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  WATER USAGE THIS MONTH                                          │
│  ├─ Used: 2,340 gallons                                         │
│  ├─ Saved by weather skips: 450 gallons                         │
│  └─ vs Last Year: -18%                                          │
│                                                                  │
│  [Adjust Schedule]  [Run Now]  [Settings]                       │
└─────────────────────────────────────────────────────────────────┘
```

## 9.6 Acceptance Criteria

- [ ] Home Assistant full integration
- [ ] Apple HomeKit integration
- [ ] Google Home integration
- [ ] Amazon Alexa integration
- [ ] Samsung SmartThings integration
- [ ] Presence-based automations
- [ ] Voice control via Family VA
- [ ] Weather-based irrigation adjustment
- [ ] Snow clearing automation
- [ ] Child-restricted commands

---

# Section 10: Home Organization & Inventory System

## 10.1 Overview

AI-powered home organization system that tracks what's stored where, monitors inventory levels, helps organize spaces, and integrates with shopping/delivery for seamless restocking.

## 10.2 Storage Location System

### Location Hierarchy

```
Home
├── Kitchen
│   ├── Pantry
│   │   ├── Shelf 1 (Canned goods)
│   │   ├── Shelf 2 (Dry goods)
│   │   └── Shelf 3 (Snacks)
│   ├── Refrigerator
│   │   ├── Main compartment
│   │   ├── Freezer
│   │   └── Door shelves
│   ├── Cabinets
│   │   ├── Upper Left (Dishes)
│   │   ├── Upper Right (Glasses)
│   │   └── Under Sink (Cleaning)
│   └── Drawers
├── Garage
│   ├── Tool Wall
│   ├── Storage Shelves
│   └── Overhead Storage
├── Bedrooms
│   ├── Master Closet
│   └── Kids' Closets
└── ...
```

### Storage Location DocType

```python
class StorageLocation(Document):
    doctype = "Storage Location"

    # Identity
    location_name: Data
    location_code: Data  # "KIT-PAN-S1" (Kitchen-Pantry-Shelf1)

    # Hierarchy
    parent_location: Link["Storage Location"]

    # Physical
    location_type: Select[
        "Room", "Closet", "Cabinet", "Drawer",
        "Shelf", "Bin", "Refrigerator", "Freezer",
        "Pantry", "Garage", "Storage Unit"
    ]

    # Identification
    qr_code: Data  # Generated QR code value
    visual_marker: Attach Image  # Custom marker image
    ai_recognition_training: JSON  # Training data for camera ID

    # Organization
    intended_contents: Text  # "Canned vegetables, soups"
    organization_guide: Text  # "Arrange by expiration date"
    max_capacity: Int  # Number of items

    # Current State
    last_inventoried: Datetime
    current_item_count: Int
    needs_organization: Check

    # Photo Reference
    organized_reference_photo: Attach Image  # "This is how it should look"
    current_state_photo: Attach Image
```

## 10.3 QR Code & Camera Recognition

### QR Code System

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LOCATION QR CODES                     │
│                                                                  │
│  HOW IT WORKS                                                    │
│                                                                  │
│  1. Print QR codes for each storage location                    │
│  2. Stick inside cabinet door or on shelf                       │
│  3. Scan QR to:                                                 │
│     • See what should be stored here                            │
│     • Log items added/removed                                   │
│     • Report organization issues                                │
│     • View organization guide                                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │    [QR CODE]        Pantry - Shelf 2                       │ │
│  │                     "Dry Goods"                            │ │
│  │                                                            │ │
│  │    Contents: Pasta, Rice, Cereal, Flour, Sugar            │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Print All QR Codes]  [Print Selected]  [Order Stickers]       │
└─────────────────────────────────────────────────────────────────┘
```

### Camera Recognition (No QR Required)

```python
class StorageRecognition:
    """AI-powered storage location recognition"""

    def identify_location(self, image: bytes) -> StorageLocation:
        """
        Identify storage location from photo without QR code.
        Uses visual features to match against trained locations.
        """
        # Extract visual features
        features = self.extract_features(image)

        # Match against known locations
        matches = self.match_locations(features)

        if matches[0].confidence > 0.85:
            return matches[0].location
        else:
            # Ask user to confirm
            return self.prompt_user_confirmation(matches[:3])

    def train_location(self, location: StorageLocation, images: list):
        """Train recognition for a new location"""
        # User takes 3-5 photos from different angles
        # System extracts and stores visual features
        pass

    def identify_contents(self, image: bytes) -> list:
        """Identify items visible in storage space"""
        # Uses object detection to find items
        # Matches against known inventory items
        pass
```

### Camera Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMART ORGANIZATION                            │
│                                                                  │
│  Point camera at cabinet/pantry/fridge...                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │              [CAMERA VIEWFINDER]                           │ │
│  │                                                            │ │
│  │    📍 Identified: Kitchen Pantry - Shelf 2                │ │
│  │                                                            │ │
│  │    Items detected:                                         │ │
│  │    ├─ ✅ Pasta (correct location)                         │ │
│  │    ├─ ✅ Rice (correct location)                          │ │
│  │    ├─ ⚠️ Chips (should be Shelf 3 - Snacks)              │ │
│  │    └─ ❓ Unknown item (tap to identify)                   │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ORGANIZATION SUGGESTIONS                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Move to correct location:                                  │ │
│  │ • Chips → Pantry Shelf 3 (Snacks)                         │ │
│  │                                                            │ │
│  │ Missing from this shelf:                                   │ │
│  │ • Flour (last seen: Shelf 1 - move here)                  │ │
│  │ • Sugar (not in inventory - add to shopping list?)        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Auto-Add to Shopping List]  [Mark as Organized]  [Skip]       │
└─────────────────────────────────────────────────────────────────┘
```

## 10.4 Inventory Management

### Household Item Inventory

```python
class HouseholdItem(Document):
    doctype = "Household Item"

    # Item Identity
    item_name: Data
    brand: Data
    model_number: Data
    barcode: Data  # UPC/EAN

    # Category
    category: Select[
        "Food & Pantry",
        "Cleaning Supplies",
        "Personal Care",
        "Medicine",
        "Electronics",
        "Tools",
        "Clothing",
        "Toys",
        "Books",
        "Kitchen Items",
        "Furniture",
        "Outdoor",
        "Pet Supplies",
        "Other"
    ]

    # Location
    storage_location: Link["Storage Location"]
    correct_location: Link["Storage Location"]  # Where it SHOULD be

    # Quantity
    quantity: Float
    unit: Select["Each", "Box", "Bottle", "Can", "Bag", "Pack"]

    # Tracking
    is_consumable: Check
    reorder_threshold: Float  # Reorder when below this
    auto_reorder: Check

    # Expiration (for food/medicine)
    expiration_date: Date

    # Purchase Info
    purchase_source: Select["Amazon", "Walmart", "Target", "Costco", "Other"]
    purchase_price: Currency
    purchase_date: Date
    purchase_order_link: Data  # Link to original order

    # Documentation
    manual_file: Attach
    manual_url: Data
    warranty_expiration: Date
```

### Inventory Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOME INVENTORY                                │
│                                                                  │
│  ALERTS                                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ⚠️ LOW STOCK (3 items)                                     │ │
│  │ ├─ Paper towels (1 roll left, need 6)                     │ │
│  │ ├─ Milk (expires tomorrow)                                │ │
│  │ └─ Dog food (2 days supply)                               │ │
│  │                                                            │ │
│  │ [Add All to Cart]  [View Details]                         │ │
│  │                                                            │ │
│  │ ⏰ EXPIRING SOON (5 items)                                 │ │
│  │ ├─ Yogurt (2 days)                                        │ │
│  │ ├─ Lunch meat (3 days)                                    │ │
│  │ └─ +3 more                                                │ │
│  │                                                            │ │
│  │ [View All]  [Add to Meal Plan]                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  BROWSE BY LOCATION                                              │
│  ├─ 🍳 Kitchen (234 items)                                      │
│  ├─ 🚗 Garage (89 items)                                        │
│  ├─ 🛏️ Bedrooms (156 items)                                    │
│  ├─ 🛁 Bathrooms (67 items)                                     │
│  └─ 📦 Storage (112 items)                                      │
│                                                                  │
│  RECENT ACTIVITY                                                 │
│  ├─ Today: Amazon order received (12 items)                    │
│  ├─ Yesterday: Walmart groceries added (28 items)              │
│  └─ Nov 4: Costco trip logged (15 items)                       │
│                                                                  │
│  [Scan Item]  [Manual Add]  [Full Inventory]  [Organization]    │
└─────────────────────────────────────────────────────────────────┘
```

## 10.5 Amazon & Walmart Integration

### Purchase Tracking Integration

```python
class RetailAccountIntegration(Document):
    doctype = "Retail Account Integration"

    platform: Select["Amazon", "Walmart", "Target", "Costco", "Other"]

    # OAuth Connection
    connected: Check
    access_token: Password
    refresh_token: Password
    last_sync: Datetime

    # Settings
    auto_import_orders: Check
    auto_assign_locations: Check
    import_start_date: Date

    # Order History
    orders_imported: Int
    items_tracked: Int
```

### Order Import & Receiving

```
┌─────────────────────────────────────────────────────────────────┐
│                    INCOMING ORDERS                               │
│                                                                  │
│  ARRIVING TODAY                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 📦 Amazon Order #112-4567890                               │ │
│  │    Arriving by 9 PM                                        │ │
│  │                                                            │ │
│  │    Items:                                                  │ │
│  │    ├─ Clorox Wipes (3-pack) → Cleaning Cabinet            │ │
│  │    ├─ AA Batteries (24-pack) → Utility Drawer             │ │
│  │    └─ Dog Treats → Pantry - Pet Shelf                     │ │
│  │                                                            │ │
│  │    [Mark Received]  [Change Locations]                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ARRIVING THIS WEEK                                              │
│  ├─ Wed: Walmart Grocery (18 items)                            │
│  └─ Fri: Amazon Subscribe & Save (6 items)                     │
│                                                                  │
│  PRE-ARRIVAL PREP                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ℹ️ 3 items need location assignment:                       │ │
│  │                                                            │ │
│  │ NEW: Instant Pot Air Fryer                                │ │
│  │ Suggested: Kitchen Counter or Cabinet                     │ │
│  │ [Assign Location]                                          │ │
│  │                                                            │ │
│  │ NEW: Kids' Art Supplies Set                               │ │
│  │ Suggested: Playroom Cabinet                               │ │
│  │ [Assign Location]                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [View Order History]  [Sync Now]  [Settings]                   │
└─────────────────────────────────────────────────────────────────┘
```

### Receiving Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECEIVE DELIVERY                              │
│                                                                  │
│  Amazon Order #112-4567890                                      │
│                                                                  │
│  Scan or check off each item:                                   │
│                                                                  │
│  ☑️ Clorox Wipes (3-pack)                                       │
│     └─ Put in: Cleaning Cabinet (Under Sink)                   │
│                                                                  │
│  ☑️ AA Batteries (24-pack)                                      │
│     └─ Put in: Utility Drawer (Kitchen)                        │
│                                                                  │
│  ☐ Dog Treats                                                   │
│     └─ Put in: Pantry - Pet Shelf                              │
│     [Scan Barcode]  [Mark Received]  [Missing]                 │
│                                                                  │
│  ───────────────────────────────────────────────────────────   │
│                                                                  │
│  NEED HELP FINDING LOCATIONS?                                   │
│  [Show Me Where] - AR guide to each location                   │
│                                                                  │
│  [Complete Receiving]  [Report Problem]                         │
└─────────────────────────────────────────────────────────────────┘
```

## 10.6 Manual & Documentation Storage

### Automatic Manual Retrieval

```python
def get_product_manual(item: HouseholdItem) -> dict:
    """Automatically find and store product manual"""

    # Try multiple sources
    manual_url = None

    # 1. Check manufacturer website
    if item.brand and item.model_number:
        manual_url = search_manufacturer_site(item.brand, item.model_number)

    # 2. Check ManualsLib
    if not manual_url:
        manual_url = search_manualslib(item.item_name, item.model_number)

    # 3. Check Amazon product page
    if not manual_url and item.purchase_source == "Amazon":
        manual_url = get_amazon_manual_link(item.purchase_order_link)

    if manual_url:
        # Download and store in Frappe Drive
        file_path = download_and_store(manual_url, item)
        item.manual_file = file_path
        item.manual_url = manual_url
        item.save()

        # Index for AI search
        index_manual_for_ai(item, file_path)

    return {"found": bool(manual_url), "url": manual_url}
```

### AI Manual Assistant (NotebookLM-Style)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCT HELP: INSTANT POT                     │
│                                                                  │
│  Ask me anything about your Instant Pot Duo Plus 6qt            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ You: How do I release pressure?                            │ │
│  │                                                            │ │
│  │ Assistant: There are two ways to release pressure:        │ │
│  │                                                            │ │
│  │ 1. Quick Release: Turn the pressure release valve from   │ │
│  │    "Sealing" to "Venting". Steam will release quickly.   │ │
│  │    ⚠️ Keep hands away from steam.                        │ │
│  │                                                            │ │
│  │ 2. Natural Release: Let it sit after cooking. Takes      │ │
│  │    10-30 minutes. Better for meats and beans.            │ │
│  │                                                            │ │
│  │ [📖 See page 15 of manual]  [▶️ Watch video]              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  QUICK HELP                                                      │
│  ├─ [How do I clean it?]                                        │
│  ├─ [What does E6 error mean?]                                  │
│  ├─ [Can I pressure fry?]                                       │
│  └─ [Recipe suggestions]                                        │
│                                                                  │
│  RELATED VIDEOS (from YouTube)                                   │
│  ├─ 🎬 "Instant Pot for Beginners" (12 min) - 2.3M views       │
│  ├─ 🎬 "15 Things You're Doing Wrong" (18 min)                 │
│  └─ 🎬 "Quick Release vs Natural Release" (5 min)              │
│                                                                  │
│  [View Full Manual]  [Download PDF]  [Add to Favorites]         │
└─────────────────────────────────────────────────────────────────┘
```

## 10.7 Organization Best Practices

### Built-In Organization Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORGANIZATION BEST PRACTICES                   │
│                                                                  │
│  KITCHEN                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ PANTRY ORGANIZATION (professional organizer tips)          │ │
│  │                                                            │ │
│  │ Top Shelf: Rarely used items (holiday, special occasion)  │ │
│  │ Eye Level: Daily items (cereal, snacks, coffee)           │ │
│  │ Lower: Heavy items (canned goods, bottles)                │ │
│  │ Floor: Bulk items, pet food, drinks                       │ │
│  │                                                            │ │
│  │ TIPS:                                                      │ │
│  │ • Group like items together                               │ │
│  │ • Use clear containers for loose items                    │ │
│  │ • Label everything                                        │ │
│  │ • FIFO: First In, First Out for perishables              │ │
│  │                                                            │ │
│  │ [Apply This Layout]  [Customize]                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  PERSONALIZED SUGGESTIONS                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Based on your family:                                      │ │
│  │                                                            │ │
│  │ • Kids' snacks: Keep at kid-height for independence       │ │
│  │ • Allergen items: Separate shelf, clearly labeled         │ │
│  │ • Frequently grabbed: Front of shelf                      │ │
│  │ • Baby items: Together in one accessible area             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [View All Rooms]  [Get Professional Consult]                   │
└─────────────────────────────────────────────────────────────────┘
```

## 10.8 Acceptance Criteria

- [ ] Storage location hierarchy
- [ ] QR code generation and scanning
- [ ] Camera-based location recognition
- [ ] Item inventory with categories
- [ ] Amazon/Walmart order import
- [ ] Pre-arrival location assignment
- [ ] Receiving process workflow
- [ ] Automatic manual retrieval
- [ ] AI manual chat assistant
- [ ] YouTube video curation
- [ ] Organization best practices
- [ ] "Where does this go" feature

---

# Section 11: Family Asset Manager

## 11.1 Overview

Track valuable family assets, equipment assignment, GPS-enabled device location, and maintenance schedules.

## 11.2 Asset Categories

| Category             | Examples                           | Tracking                |
| -------------------- | ---------------------------------- | ----------------------- |
| **Electronics**      | Phones, tablets, laptops, gaming   | GPS, assigned user      |
| **Vehicles**         | Cars, bikes, scooters              | GPS/OBD-II, maintenance |
| **Appliances**       | Washer, dryer, HVAC, water heater  | Location, maintenance   |
| **Tools**            | Power tools, lawn equipment        | Location, checkout      |
| **Sports Equipment** | Bikes, golf clubs, camping gear    | Checkout, location      |
| **Valuable Items**   | Jewelry, collectibles, instruments | Location, insurance     |

## 11.3 Asset DocType

```python
class FamilyAsset(Document):
    doctype = "Family Asset"

    # Identity
    asset_name: Data
    asset_type: Link["Asset Category"]
    brand: Data
    model: Data
    serial_number: Data

    # Value
    purchase_price: Currency
    current_value: Currency
    purchase_date: Date
    purchase_receipt: Attach

    # Location
    home_location: Link["Storage Location"]
    current_location: Link["Storage Location"]
    has_gps_tracker: Check
    gps_tracker_type: Select["Apple AirTag", "Tile", "Samsung SmartTag", "Built-in", "OBD-II", "Other"]
    gps_integration_id: Data
    last_known_coordinates: Geolocation

    # Assignment
    assigned_to: Link["Family Member"]
    assignment_type: Select["Permanent", "Temporary", "Shared"]
    checkout_log: Table["Asset Checkout Log"]

    # Maintenance
    warranty_expiration: Date
    warranty_document: Attach
    maintenance_schedule: Link["Maintenance Schedule"]
    next_maintenance: Date
    maintenance_history: Table["Maintenance Record"]

    # Documentation
    manual: Attach
    manual_url: Data
    photos: Table["Asset Photo"]

    # Insurance
    insured: Check
    insurance_policy: Data
    insurance_value: Currency
```

## 11.4 GPS Tracker Integration

### Supported Trackers

| Tracker          | Integration            |
| ---------------- | ---------------------- |
| Apple AirTag     | FindMy network API     |
| Tile             | Tile API               |
| Samsung SmartTag | SmartThings API        |
| Phone/Tablet     | Native device location |
| Vehicle OBD-II   | OBD-II dongle API      |
| Dedicated GPS    | Various APIs           |

### Asset Location Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY ASSETS MAP                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │         🏠 Home                                         │    │
│  │         ├─ 💻 Dad's Laptop (Office)                    │    │
│  │         ├─ 🎮 Nintendo Switch (Living Room)            │    │
│  │         └─ 🔧 Power Drill (Garage)                     │    │
│  │                                                         │    │
│  │                           📱 Johnny's iPad             │    │
│  │                              (At school)               │    │
│  │                                                         │    │
│  │    🚗 Honda Accord                                     │    │
│  │       (Dad at work)                                    │    │
│  │                                                         │    │
│  │                   📱 Emma's Phone                      │    │
│  │                      (At soccer field)                 │    │
│  │                                                         │    │
│  │           🚗 Toyota Sienna                             │    │
│  │              (Mom driving home)                        │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  AWAY FROM HOME                                                  │
│  ├─ 📱 Johnny's iPad - Lincoln Elementary (since 8:00 AM)       │
│  ├─ 📱 Emma's Phone - Sports Complex (since 3:30 PM)           │
│  ├─ 🚗 Honda Accord - Downtown Office (since 8:30 AM)          │
│  └─ 🚗 Toyota Sienna - En route home (ETA 10 min)              │
│                                                                  │
│  [Find My Asset]  [Check Out Asset]  [Report Lost]              │
└─────────────────────────────────────────────────────────────────┘
```

## 11.5 Checkout System

### Equipment Checkout Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHECK OUT: CAMPING TENT                       │
│                                                                  │
│  Item: REI Kingdom 6 Tent                                       │
│  Home Location: Garage - Storage Shelves                        │
│  Current Status: Available                                       │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Who is checking out?                                           │
│  ○ 👨 Dad (Mike)                                                │
│  ● 👩 Mom (Sarah)                                               │
│  ○ 🏠 Family Trip                                               │
│                                                                  │
│  Purpose:                                                        │
│  [Camping trip - Yosemite Nov 15-17      ]                     │
│                                                                  │
│  Expected return:                                                │
│  [November 18, 2025]                                            │
│                                                                  │
│  ☑️ Send reminder to return                                     │
│  ☑️ Add to packing list                                         │
│                                                                  │
│  [Check Out]  [Cancel]                                          │
└─────────────────────────────────────────────────────────────────┘
```

## 11.6 Appliance Maintenance

### Maintenance Schedule

```python
class MaintenanceSchedule(Document):
    doctype = "Maintenance Schedule"

    asset: Link["Family Asset"]

    # Maintenance Items
    maintenance_items: Table["Scheduled Maintenance Item"]

    # Example items:
    # - HVAC filter change: Monthly
    # - Water heater flush: Annually
    # - Dryer vent cleaning: Quarterly
    # - Refrigerator coil cleaning: Bi-annually
```

### Maintenance Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    APPLIANCE MAINTENANCE                         │
│                                                                  │
│  UPCOMING MAINTENANCE                                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ⚠️ OVERDUE                                                 │ │
│  │ ├─ HVAC Filter Change (2 weeks overdue)                   │ │
│  │ │   └─ Filter size: 20x25x1  [Order on Amazon]            │ │
│  │ └─ Smoke Detector Battery (1 month overdue)               │ │
│  │     └─ 9V batteries needed  [Order]                       │ │
│  │                                                            │ │
│  │ 📅 THIS MONTH                                              │ │
│  │ ├─ Nov 15: Dryer Vent Cleaning                            │ │
│  │ │   └─ [DIY Instructions] or [Schedule Service $89]       │ │
│  │ └─ Nov 20: Garbage Disposal Cleaning                      │ │
│  │     └─ [How-To Video]                                     │ │
│  │                                                            │ │
│  │ 📅 NEXT MONTH                                              │ │
│  │ ├─ Dec 1: HVAC Filter Change                              │ │
│  │ └─ Dec 15: Water Heater Inspection                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  APPLIANCES                                                      │
│  ├─ 🌡️ HVAC System (Carrier) - Kitchen Closet                  │
│  │   └─ Last serviced: June 2025 | Warranty: Dec 2027          │
│  ├─ 🧊 Refrigerator (Samsung) - Kitchen                        │
│  │   └─ Last serviced: Never | Warranty: Mar 2026              │
│  ├─ 🔥 Water Heater (Rheem) - Utility Room                     │
│  │   └─ Last serviced: Jan 2025 | Warranty: Jan 2030          │
│  └─ ... 12 more appliances                                     │
│                                                                  │
│  [Add Appliance]  [View All]  [Schedule Service]                │
└─────────────────────────────────────────────────────────────────┘
```

## 11.7 Acceptance Criteria

- [ ] Asset tracking with categories
- [ ] GPS tracker integration (AirTag, Tile, etc.)
- [ ] Device location via native APIs
- [ ] OBD-II vehicle integration
- [ ] Equipment checkout system
- [ ] Checkout reminders
- [ ] Appliance maintenance schedules
- [ ] Maintenance reminders
- [ ] DIY vs service provider options
- [ ] Parts ordering integration

---

# Section 12: Meal Planning & Shopping

## 12.1 Overview

AI-powered meal planning that considers family dietary needs, generates shopping lists, and integrates with inventory and grocery delivery.

## 12.2 Meal Planner

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEKLY MEAL PLAN                              │
│                                                                  │
│  Week of November 4-10, 2025                                    │
│                                                                  │
│  │ Day    │ Breakfast      │ Lunch          │ Dinner          │ │
│  ├────────┼────────────────┼────────────────┼─────────────────┤ │
│  │ Mon    │ Oatmeal        │ (Packed)       │ Tacos 🌮        │ │
│  │ Tue    │ Eggs & Toast   │ (Packed)       │ Pasta 🍝        │ │
│  │ Wed    │ Cereal         │ (Packed)       │ Stir Fry 🥡     │ │
│  │ Thu    │ Smoothies      │ (Packed)       │ Pizza Night 🍕  │ │
│  │ Fri    │ Pancakes       │ (School lunch) │ Fish Tacos 🐟   │ │
│  │ Sat    │ French Toast   │ Sandwiches     │ BBQ Chicken 🍗  │ │
│  │ Sun    │ Brunch Out     │ -              │ Soup & Bread 🍲 │ │
│                                                                  │
│  DIETARY CONSIDERATIONS                                          │
│  ├─ 🥜 Johnny: Peanut allergy (all meals peanut-free)           │
│  ├─ 🥗 Emma: Vegetarian (protein alternatives included)         │
│  └─ 🍞 Dad: Low-carb preference (options provided)              │
│                                                                  │
│  AI SUGGESTIONS                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 💡 Based on what's expiring in your fridge:                │ │
│  │    • Ground beef (expires Thu) - Used in Monday tacos ✓   │ │
│  │    • Spinach (expires Tue) - Added to Wednesday stir fry  │ │
│  │                                                            │ │
│  │ 💡 Based on your schedule:                                 │ │
│  │    • Thursday is busy - Pizza night is quick! ✓           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Generate Shopping List]  [Regenerate Plan]  [View Recipes]    │
└─────────────────────────────────────────────────────────────────┘
```

## 12.3 Collaborative Shopping List

```
┌─────────────────────────────────────────────────────────────────┐
│                    SHOPPING LIST                                 │
│                                                                  │
│  FOR: Walmart Grocery Pickup (Saturday 10 AM)                   │
│                                                                  │
│  FROM MEAL PLAN (auto-added)                                    │
│  ├─ ☐ Ground beef (2 lbs)                                      │
│  ├─ ☐ Taco shells (1 box)                                      │
│  ├─ ☐ Shredded cheese (1 bag)                                  │
│  ├─ ☐ Pasta (1 box)                                            │
│  ├─ ☐ Marinara sauce (1 jar)                                   │
│  └─ ... 12 more items                                          │
│                                                                  │
│  LOW STOCK ALERTS (auto-added)                                  │
│  ├─ ☐ Paper towels (6 pack)                                    │
│  ├─ ☐ Milk (1 gallon)                                          │
│  └─ ☐ Dog food (1 bag)                                         │
│                                                                  │
│  FAMILY REQUESTS                                                 │
│  ├─ ☐ Lucky Charms - added by Johnny 🟡                        │
│  ├─ ☐ Strawberries - added by Emma 🟠                          │
│  └─ ☐ Coffee creamer - added by Mom 🟣                         │
│                                                                  │
│  RECURRING ITEMS                                                 │
│  ├─ ☐ Bananas                                                  │
│  ├─ ☐ Bread                                                    │
│  └─ ☐ Eggs                                                     │
│                                                                  │
│  ───────────────────────────────────────────────────────────   │
│  Total items: 28 | Est. cost: $127.50                          │
│                                                                  │
│  [Send to Walmart]  [Send to Instacart]  [Print List]          │
│                                                                  │
│  + Add Item: [                    ] [Add]                      │
│              Kids can add (parent approval required)            │
└─────────────────────────────────────────────────────────────────┘
```

## 12.4 Acceptance Criteria

- [ ] AI meal plan generation
- [ ] Dietary restriction support
- [ ] Expiring food integration
- [ ] Collaborative shopping list
- [ ] Kid requests with approval
- [ ] Low stock auto-add
- [ ] Grocery delivery integration
- [ ] Recipe storage

---

# Section 13: Teen Driver Monitoring

## 13.1 Overview

Safe driving monitoring for teen drivers with speed alerts, curfew enforcement, and driving score that can affect privileges.

## 13.2 Vehicle Integration

### Supported Integrations

| Method               | Data Available                     |
| -------------------- | ---------------------------------- |
| **OBD-II Dongle**    | Speed, RPM, hard braking, location |
| **Tesla API**        | Full telematics                    |
| **Ford Pass**        | Location, trip history             |
| **GM OnStar**        | Location, diagnostics              |
| **Toyota Connected** | Location, trip history             |
| **Phone-Based**      | Location, speed (from GPS)         |

## 13.3 Teen Driving Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    EMMA'S DRIVING DASHBOARD                      │
│                                                                  │
│  DRIVING SCORE: 87/100 ⭐⭐⭐⭐                                  │
│  ████████████████████░░░ Good Driver!                           │
│                                                                  │
│  THIS WEEK                                                       │
│  ├─ Miles driven: 67                                            │
│  ├─ Trips: 12                                                   │
│  ├─ Hard brakes: 2 (⚠️ -3 points)                              │
│  ├─ Speed alerts: 1 (⚠️ -5 points)                             │
│  └─ Night driving: 0 hours (curfew respected ✓)                │
│                                                                  │
│  RECENT TRIPS                                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Today 3:45 PM - School → Soccer                            │ │
│  │ 8.2 miles | 18 min | Score: 95                            │ │
│  │ ✓ No issues                                                │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Today 7:30 AM - Home → School                              │ │
│  │ 5.1 miles | 12 min | Score: 82                            │ │
│  │ ⚠️ 1 hard brake on Main St                                 │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ Yesterday 9:15 PM - Friend's → Home                        │ │
│  │ 3.2 miles | 8 min | Score: 78                             │ │
│  │ ⚠️ 42 in 35 zone briefly                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  DRIVING PRIVILEGES                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Current status: Full privileges                            │ │
│  │                                                            │ │
│  │ ✓ Solo driving allowed                                     │ │
│  │ ✓ Friends as passengers (max 2)                           │ │
│  │ ⚠️ Curfew: Home by 10 PM                                   │ │
│  │                                                            │ │
│  │ Score requirements:                                        │ │
│  │ • Below 70: No passengers for 2 weeks                     │ │
│  │ • Below 60: Parent ride-along required                    │ │
│  │ • Below 50: Driving suspended                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [View Detailed Report]  [Adjust Rules]  [View Map]             │
└─────────────────────────────────────────────────────────────────┘
```

## 13.4 Acceptance Criteria

- [ ] OBD-II dongle integration
- [ ] Vehicle API integrations (Tesla, Ford, etc.)
- [ ] Speed monitoring with alerts
- [ ] Hard braking detection
- [ ] Curfew zone enforcement
- [ ] Driving score calculation
- [ ] Privilege system based on score
- [ ] Trip history with playback

---

# Section 14: Family Broadcast & Emergency

## 14.1 Overview

One-tap communication to all family members for announcements and emergencies.

## 14.2 Broadcast System

### Broadcast Types

| Type             | Use Case           | Delivery                |
| ---------------- | ------------------ | ----------------------- |
| **Announcement** | "Dinner in 10 min" | Push notification       |
| **Question**     | "Who wants pizza?" | Push + response options |
| **Poll**         | "Movie vote"       | Interactive poll        |
| **Check-In**     | "Everyone OK?"     | Requires response       |
| **Emergency**    | "Urgent - call me" | All channels, loud      |

### Broadcast UI

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAMILY BROADCAST                              │
│                                                                  │
│  QUICK MESSAGES                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ [🍽️ Dinner Ready]  [🏠 Heading Home]  [⏰ 5 Min Warning]   │ │
│  │ [❓ Call Me]       [🚗 Pick Up Time]  [💤 Goodnight]       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  CUSTOM MESSAGE                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ [                                                    ]     │ │
│  │                                                            │ │
│  │ Send to: ☑️ Everyone  ☐ Kids Only  ☐ Adults Only         │ │
│  │                                                            │ │
│  │ [Send Message]  [Send Voice Message]                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  EMERGENCY                                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │    [🆘 EMERGENCY BROADCAST]                                │ │
│  │                                                            │ │
│  │    Sends to ALL family with:                               │ │
│  │    • Loud notification (bypasses silent)                   │ │
│  │    • Your location                                         │ │
│  │    • "Respond SAFE or HELP"                               │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  RECENT BROADCASTS                                               │
│  ├─ 6:30 PM: "Dinner ready!" - All responded                   │
│  ├─ 5:15 PM: "Pick up Emma at 5:30" - Dad acknowledged         │
│  └─ 2:00 PM: "Snow day tomorrow!" - 4 responses               │
└─────────────────────────────────────────────────────────────────┘
```

## 14.3 Emergency Roll-Call

```
┌─────────────────────────────────────────────────────────────────┐
│                    🆘 EMERGENCY CHECK-IN                         │
│                                                                  │
│  Sent by: Mom at 3:45 PM                                        │
│  Message: "Earthquake! Everyone check in!"                      │
│                                                                  │
│  RESPONSES                                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ✅ Dad (Mike) - "Safe at office" - 3:46 PM                 │ │
│  │    📍 Downtown Office Building                             │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ✅ Emma - "I'm OK at school" - 3:47 PM                     │ │
│  │    📍 Lincoln High School                                  │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ⏳ Johnny - NO RESPONSE - Last seen 3:42 PM                │ │
│  │    📍 Last location: Lincoln Elementary                    │ │
│  │    [Call Johnny]  [Call School]                           │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ ✅ Grandma - "All fine here" - 3:48 PM                     │ │
│  │    📍 Home (Senior Living)                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Send Reminder to Non-Responders]  [Call 911]  [Close]         │
└─────────────────────────────────────────────────────────────────┘
```

## 14.4 Acceptance Criteria

- [ ] Quick message presets
- [ ] Custom broadcast messages
- [ ] Target group selection
- [ ] Emergency broadcast (loud, bypass silent)
- [ ] Roll-call with responses
- [ ] Location sharing in emergency
- [ ] Non-responder alerts
- [ ] Voice message support

---

# Section 15: Privacy & Safety Rules

## 15.1 Hardcoded Safety Rules

| Rule                                          | Enforcement          |
| --------------------------------------------- | -------------------- |
| Under 13 → No external data sharing           | COPPA automatic      |
| Only guardians see minor's location           | Permission matrix    |
| Allowance payments require parent approval    | Workflow + biometric |
| Emergency medical data shareable by any adult | One-tap override     |
| No social features for under-13               | Feature block        |
| Teen location "ghost mode" max 2 hours        | System limit         |
| All voice recordings deletable by parents     | Settings access      |

## 15.2 Data Minimization

```python
# Data collected by age group

DATA_COLLECTION = {
    "under_6": {
        "location": "always_share_guardians",
        "photos": "parent_managed",
        "voice": "none",
        "analytics": "none"
    },
    "6_to_12": {
        "location": "always_share_guardians",
        "photos": "parent_approval",
        "voice": "chore_verification_only",
        "analytics": "aggregated_only"
    },
    "13_to_17": {
        "location": "configurable",
        "photos": "own_control",
        "voice": "own_control",
        "analytics": "opt_in"
    },
    "adult": {
        "location": "opt_in",
        "photos": "own_control",
        "voice": "own_control",
        "analytics": "opt_in"
    }
}
```

## 15.3 Acceptance Criteria

- [ ] COPPA compliance verified
- [ ] GDPR-K compliance for EU
- [ ] Age-based permission matrix
- [ ] Parent control over all child data
- [ ] Data export for any family member
- [ ] Data deletion request handling
- [ ] No data sold to third parties
- [ ] Encryption at rest and in transit

---

# Section 16: Business Rules Summary

## 16.1 Family-Specific Business Rules

| Rule                                            | Enforcement                               |
| ----------------------------------------------- | ----------------------------------------- |
| Under 13 → no external data sharing             | COPPA / GDPR-K baked in                   |
| Only guardians can see minor's location/history | Automatic permission matrix               |
| Allowance payments require parent approval      | Workflow + biometric confirm              |
| Emergency medical data shareable by any adult   | One-tap override                          |
| Divorce/custody schedules                       | Multi-parent calendars + visibility rules |
| Chore completion requires verification          | Photo proof + parent approval             |
| Screen time limits enforced                     | Device-level controls                     |
| Teen driving score affects privileges           | Automated privilege system                |
| Savings matching has caps                       | Per-program configuration                 |
| Home automation restricted for kids             | Command whitelist by age                  |

## 16.2 Integration Summary

| System                 | Integration Type           |
| ---------------------- | -------------------------- |
| MedxHealthLinc         | API + deep linking         |
| Home Assistant         | Full API                   |
| Apple HomeKit          | HomeKit API                |
| Google Home            | Google Home API            |
| Amazon Alexa           | Alexa Smart Home API       |
| Samsung SmartThings    | SmartThings API            |
| Amazon (shopping)      | Order API                  |
| Walmart (shopping)     | Order API                  |
| Google Classroom       | OAuth API                  |
| Apple Find My          | FindMy network             |
| Vehicle telematics     | OBD-II + manufacturer APIs |
| School Dartwing Module | Native integration         |

---

# Section 17: Implementation Roadmap

## 17.1 Phase Summary

| Phase          | Timeline   | Focus                                      |
| -------------- | ---------- | ------------------------------------------ |
| **Foundation** | Q1-Q2 2026 | Core relationships, calendar, basic chores |
| **Alpha**      | Q3 2026    | Location, parental controls, allowance     |
| **Beta**       | Q4 2026    | Voice, home automation, meal planning      |
| **GA**         | Q1 2027    | Full feature set, integrations             |
| **Scale**      | Q2 2027+   | Advanced features, more integrations       |

## 17.2 Feature Priority

| Priority | Features                              |
| -------- | ------------------------------------- |
| **P0**   | Relationships, calendar, basic safety |
| **P1**   | Chores, allowance, grades, location   |
| **P2**   | Voice, home automation, inventory     |
| **P3**   | Advanced AI, third-party integrations |

---

_End of Dartwing Family Module PRD_

**Total Features:** 120+  
**Total DocTypes:** 45+  
**Integrations:** 20+

This document defines everything needed to make `org_type = "Family"` the most comprehensive, loving, AI-native family management experience ever built.
