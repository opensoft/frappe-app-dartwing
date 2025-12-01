# Dartwing Family Architecture: Consolidated Issues

**Date:** November 2025
**Sources:** Combined analysis from Gemi (Antigravity Agent), Jeni, and Claude (Opus 4.5)
**Status:** Comprehensive Issue Catalog

---

## Executive Summary

This document consolidates all architectural issues, risks, and concerns identified across three independent reviews of the Dartwing Family architecture. Issues are organized by severity and category to facilitate prioritization and remediation planning.

**Overall Assessment:** The architecture is conceptually sound but faces significant implementation risks due to scope, complexity, and external dependencies.

---

## Critical Severity Issues

### 1. Massive Feature Scope

**Source:** Claude, Gemi

**Description:** The PRD describes replacing 15+ separate applications with a single platform. The feature surface area is enormous, spanning family management, parental controls, AI voice assistant, calendar, chores, finance, medical, location, home automation, inventory, education, teen driving, and meal planning.

**Risks:**
- Delayed time-to-market
- Compromised quality across features
- Developer burnout
- Incomplete integrations
- This represents a 3-5 year product roadmap presented as a single architecture

**Recommendation:** Implement in distinct phases. Focus on being the best Family Organizer (Calendar + Chores + Privacy) first. Let "Magic Integrations" come later as the platform matures.

---

### 2. Integration Fragility & Dependency Hell

**Source:** Gemi, Jeni, Claude

**Description:** The architecture promises integrations with 20+ third-party services including Amazon Orders, Walmart, PowerSchool, Canvas, Home Assistant, HomeKit, Google Home, Alexa, SmartThings, Tesla API, Ford Pass, and more.

**Risks:**
- Many services (especially Retail and EdTech) do not have open, stable public APIs for consumer aggregators
- Relying on scraping or reverse-engineered APIs creates a maintenance nightmare
- API changes can break integrations unexpectedly
- Rate limiting issues at scale
- OAuth token management complexity
- Different availability across regions
- Maintenance burden grows linearly with integrations
- No sequencing, error handling, or degraded-mode behavior specified

**Recommendation:**
- Drop "Direct Retail Integration" (Amazon scraping) for V1
- Use email parsing (like TripIt) for receipts/orders
- Ship integrations in waves (core chores/allowance/calendar → location/geofence → custody → selected adapters → voice/telemetry)
- Add degraded-mode behavior and health checks for each adapter
- Support iCal feeds (universal) for education schedules; integrate only with top 2 LMS (Google Classroom, Canvas)

---

### 3. Voice Assistant Complexity

**Source:** Gemi, Claude

**Description:** The "Voice Cloning" and "Child-Safe AI" features are technically extremely demanding.

**Technical Risks:**
- Running custom voice models and LLM inference with low latency (<500ms) is expensive and hard
- High GPU costs for consumer app
- Requires specialized ML pipelines

**Legal/Ethical Risks:**
- Deepfake misuse potential
- Complex consent requirements vary by jurisdiction
- Children cannot legally consent
- Voice samples are biometric data (GDPR/BIPA implications)
- Emotional manipulation concerns (deceased grandparent voices)
- PR disasters if AI says something inappropriate to a child

**Recommendation:**
- Launch with standard high-quality TTS voices first
- Make "Voice Cloning" a Phase 2 or "Pro" feature
- Focus on the intelligence (Child-Safe filtering) first
- Require video consent (not just checkbox)
- Watermark generated audio for forensic tracing
- Prohibit cloning deceased family members initially
- Age-gate to 18+ for voice donors

---

## High Severity Issues

### 4. Permission Enforcement Thin

**Source:** Jeni

**Description:** The architecture relies on custom permission manager but lacks comprehensive enforcement across all access points.

**Gaps:**
- Missing `user_permission_doctypes` for all family-scoped doctypes
- No list filters for all doctypes
- Socket.IO and job enforcement missing
- PHI and sensitive data (medical, location) need stricter role separation

**Recommendation:**
- Add `user_permission_doctypes` to all family-scoped doctypes
- Use shared permission utilities across REST, Socket.IO, and jobs
- Separate roles for medical/location/voice data
- Ensure org filter in all list queries

---

### 5. Offline/Real-Time Sync Undefined

**Source:** Jeni, Claude

**Description:** PRD promises offline-first and conflict resolution, but no change-feed/batch-upsert/tombstone spec exists for family doctypes.

**Gaps:**
- No module-level sync specification
- Relies on core docs implicitly
- No defined conflict handling for sensitive data (location/medical)
- Risk of data leakage with real-time + offline across sensitive data

**Recommendation:**
- Define offline/sync spec for Family doctypes aligned with core sync (change feed, batch upsert, tombstones, conflict policy, attachment handling)
- Document client responsibilities
- Implement Last-Write-Wins (LWW) with field-level granularity for 99% of cases
- Only use manual resolution for critical, unmergeable data

---

### 6. Real-Time Location Tracking Privacy

**Source:** Claude

**Description:** Continuous location tracking creates substantial privacy and technical risks.

**Risks:**
- Location data is highly sensitive
- Storage of location history creates honeypot for attackers
- Children's location data requires extra protection
- Custody disputes could weaponize location data
- Battery drain concerns on mobile devices
- Data volume: 10,000 families × 5,760 points/day = 57.6 MILLION points/day

**Recommendation:**
- Default to "check-in" model instead of continuous tracking
- Automatic data expiry (7 days for teens, 24 hours for adults)
- "Fuzzy location" option (neighborhood level, not exact)
- Transparency dashboard showing who viewed location when
- Court order workflow for custody dispute data requests
- Battery-aware tracking with configurable intervals

---

### 7. Compliance Details Missing

**Source:** Jeni

**Description:** Critical compliance details are not fully specified in the architecture.

**Gaps:**
- COPPA/GDPR/PHI retention windows not defined
- Soft-delete policies for sensitive records missing
- Consent logging for voice/location/medical not specified
- Audit trails for vault/drive assets not documented

**Recommendation:**
- Document COPPA/GDPR/PHI policies
- Define retention windows
- Implement soft-delete for sensitive records
- Create consent logs for voice/location/medical
- Add audit access to vault/drive assets

---

### 8. Operational Safety

**Source:** Jeni

**Description:** Background jobs and schedulers lack safety documentation.

**Gaps:**
- Schedulers (age check, allowance, geofence, grade sync) lack idempotency/alerting docs
- Background jobs could cross-org leak without shared permission guard

**Recommendation:**
- Add per-org rate limits for location/real-time events
- Implement DLQ for scheduler failures
- Add metrics/alerts for sync lag, geofence checks, allowance payouts, and adapter errors

---

## Medium Severity Issues

### 9. "Super App" Frontend Complexity

**Source:** Gemi

**Description:** The Flutter app is expected to handle Maps/Geofencing (Life360), Banking/Ledgers (Greenlight), Calendar/Scheduling (Cozi), Home Control (HomeAssistant), and Chat (WhatsApp).

**Risks:**
- Building a UI that does all of this without being cluttered and slow is a massive design challenge
- State management (Riverpod) will get very complex

---

### 10. Multi-Tenant Controls Need Depth

**Source:** Jeni

**Description:** Multi-tenancy implementation lacks depth for advanced scenarios.

**Gaps:**
- No hierarchy/linked families for blended/extended scenarios
- No per-tenant rate limits/backpressure for real-time or location feeds
- No Drive namespace strategy for shared assets

**Recommendation:**
- Consider parent/linked families for blended/extended scenarios
- Namespace Drive/storage per family
- Add per-tenant search indices if using vector DB for knowledge/voice

---

### 11. DocType Proliferation

**Source:** Claude

**Description:** The architecture describes 45+ DocTypes for Family module alone.

**Risks:**
- Complex migration management
- Increased query complexity
- Higher learning curve for developers
- Maintenance burden
- Performance concerns with many joined queries

**Recommendation:** Consolidate to ~25 core DocTypes. Use embedded JSON or child tables for related data (e.g., allergies, conditions, medications in single Medical Profile).

---

### 12. Custody Schedule Edge Cases

**Source:** Claude

**Description:** Real-world custody is messier than the model suggests.

**Edge Cases Not Addressed:**
- Multi-household scenarios (3+ parents)
- Court order modifications mid-schedule
- Emergency custody changes
- International custody across timezones
- Grandparent visitation rights
- Foster care temporary placements

**Recommendation:** Implement priority-based rule engine with precedence levels (Base Schedule → Seasonal → Holiday Rotation → Holiday Fixed → Emergency → Manual Override).

---

### 13. Gamification Balance Concerns

**Source:** Claude

**Description:** The reward economy is complex and could be gamed.

**Risks:**
- Children may optimize for points over actual learning
- Inflation over time requires constant rebalancing
- Sibling comparison could create unhealthy competition
- Parents may feel pressured to maintain economy

**Recommendation:**
- Set max points per day (100) and max money per week ($50)
- Disable sibling leaderboards by default
- Set max same chore streak (14 days) to force variety
- Add parent veto window (24 hours)

---

## Feature Implementation Difficulty Summary

### Easy (1-2 Sprints)
| Feature | Notes |
|---------|-------|
| Family Calendar | Standard CRUD, well-documented sync with Google/Apple |
| Chores & Allowance | Self-contained logic, no external dependencies |
| Inventory/Assets | Basic database records + photo storage |
| Age-based permissions | Controller logic and profiles already mapped |

### Medium (3-6 Sprints)
| Feature | Challenges |
|---------|------------|
| Location/Geofencing | Mobile OS restrictions, battery drain |
| Meal Planning | Data heavy (recipes, ingredients) |
| Custody Schedules | Complex rule modeling |
| Offline sync for core flows | Requires defined sync protocol |

### Hard (6-12 Sprints)
| Feature | Challenges |
|---------|------------|
| Home Automation | IoT fragmentation (Matter, Zigbee, proprietary APIs) |
| Education Sync | Thousands of different school systems |
| Vehicle Telematics | Safety implications, consent, anomaly detection |
| Voice Cloning | ML pipelines, GPU costs, safety guardrails |
| Retail Integration | Amazon actively fights scrapers/bots |
| COPPA/PHI compliance end-to-end | Auditability, data minimization, retention/erasure flows |

---

## Recommended Implementation Phases

### Phase 1: Foundation (MVP)
- Family Member management
- Basic relationships
- Permission system
- Chore assignments (no gamification)
- Simple allowance tracking
- Emergency contacts

### Phase 2: Core Features
- Custody schedules
- Family calendar
- Savings goals
- Medical profiles
- Basic location (check-in, not real-time)
- Screen time (manual tracking)

### Phase 3: Advanced Features
- Real-time location
- Geofencing
- Grade tracking (manual first)
- Chore gamification
- Offline sync
- Push notifications

### Phase 4: Integrations (Ongoing)
- Calendar sync (one platform at a time)
- Home automation (Home Assistant first)
- Education platforms (one at a time)
- Health integration

### Phase 5: AI Features (Future)
- Voice assistant (basic)
- Voice cloning (optional add-on)
- Camera recognition
- Smart recommendations

---

## Must-Do Before Launch

1. Security audit by third-party firm (children's data sensitivity)
2. COPPA legal review by specialized counsel
3. Privacy impact assessment for location features
4. Load testing for real-time features at scale
5. Accessibility audit for age-diverse users

---

## Features to Defer or Kill

### Defer to Future Releases
- Voice cloning
- Camera-based inventory recognition
- Vehicle telematics integration
- Advanced home automation
- AI meal planning

### Kill or Radically Simplify
- Point economy complexity (start simple, add gamification later)
- 20+ integrations (launch with 2-3, add incrementally)
- Weather automation (too niche)
- Smart irrigation (not core to family management)

---

## Summary

The Dartwing Family architecture has strong foundational elements (hybrid organization model, age-based permissions, multi-tenant isolation) but must be implemented with aggressive scope management to succeed. The "Offline-First" and "Privacy-First" pillars are the strongest differentiators and should be prioritized.

**Key Success Factors:**
1. Ruthless prioritization - Ship a focused MVP, expand iteratively
2. Integration discipline - Add integrations one at a time with thorough testing
3. Privacy-first defaults - Earn trust before enabling invasive features
4. Legal caution - Voice cloning and children's data require expert guidance
5. Performance monitoring - 45+ DocTypes with real-time sync needs careful optimization
