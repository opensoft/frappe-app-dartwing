# DartwingTel

## Product Requirements Document

**The Global Telephony Engine for the Dartwing Platform**

---

|               |                   |
| ------------- | ----------------- |
| **Product**   | DartwingTel       |
| **Module**    | dartwing_tel      |
| **Version**   | 1.0               |
| **Date**      | November 29, 2025 |
| **Target GA** | Q3 2026           |
| **Status**    | 60% Implemented   |
| **Owner**     | Platform Team     |

---

## Document Overview

This Product Requirements Document (PRD) defines the complete specifications for DartwingTel, the carrier-grade, globally redundant telephony backbone that powers all voice, SMS, MMS, and fax capabilities across the entire Dartwing platform.

**Note:** This module was previously referred to as `dartwing_fone` in earlier documentation. The canonical name is now `dartwing_tel`.

**Total Features:** 78
**Total API Endpoints:** 52

---

## Table of Contents

| Section | Title                                                                            | Page |
| ------- | -------------------------------------------------------------------------------- | ---- |
| 1       | [Executive Summary](#section-1-executive-summary)                                | 3    |
| 2       | [Consumer Modules & Personas](#section-2-consumer-modules--personas)             | 8    |
| 3       | [SMS & MMS Features](#section-3-sms--mms-features)                               | 15   |
| 4       | [Voice & Calling Features](#section-4-voice--calling-features)                   | 35   |
| 5       | [Fax Features](#section-5-fax-features)                                          | 55   |
| 6       | [Number Management Features](#section-6-number-management-features)              | 70   |
| 7       | [Emergency Services Features](#section-7-emergency-services-features)            | 85   |
| 8       | [Compliance & Reputation Features](#section-8-compliance--reputation-features)   | 100  |
| 9       | [Analytics & Reporting Features](#section-9-analytics--reporting-features)       | 115  |
| 10      | [AI & Voice Intelligence Features](#section-10-ai--voice-intelligence-features)  | 130  |
| 11      | [Hardware Integration Features](#section-11-hardware-integration-features)       | 145  |
| 12      | [Platform Administration Features](#section-12-platform-administration-features) | 155  |
| 13      | [Technical Requirements](#section-13-technical-requirements)                     | 170  |
| 14      | [Implementation Roadmap](#section-14-implementation-roadmap)                     | 185  |

---

## Feature Index

### SMS & MMS (SMS)

- SMS-01: Global SMS Sending
- SMS-02: MMS with Media Attachments
- SMS-03: Branded Sender IDs
- SMS-04: SMS Templates & Personalization
- SMS-05: Concatenated Long Messages
- SMS-06: Delivery Status Tracking
- SMS-07: Inbound SMS & Webhooks
- SMS-08: Two-Way Conversations
- SMS-09: Bulk SMS Campaigns
- SMS-10: SMS Scheduling
- SMS-11: Unicode & Emoji Support
- SMS-12: Link Shortening & Tracking

### Voice & Calling (VOC)

- VOC-01: Outbound PSTN Calls
- VOC-02: Inbound Call Routing
- VOC-03: VoIP-to-PSTN Bridging
- VOC-04: Call Recording
- VOC-05: Voicemail Detection & Handling
- VOC-06: DTMF Input Collection
- VOC-07: Call Forwarding & Transfer
- VOC-08: Conference Calling
- VOC-09: Call Queuing
- VOC-10: Interactive Voice Response (IVR)
- VOC-11: Whisper & Barge
- VOC-12: Call Analytics & Metrics

### Fax (FAX)

- FAX-01: Outbound Fax Sending
- FAX-02: Inbound Fax Reception
- FAX-03: T.38 Protocol Support
- FAX-04: PDF Conversion & Normalization
- FAX-05: Cover Page Generation
- FAX-06: Fax Status Tracking
- FAX-07: Batch Fax Sending
- FAX-08: Fax-to-Email Delivery
- FAX-09: Legacy Device Support

### Number Management (NUM)

- NUM-01: DID Search & Purchase
- NUM-02: Number Porting
- NUM-03: Toll-Free Numbers
- NUM-04: Vanity Number Search
- NUM-05: Temporary Numbers
- NUM-06: Number Release & Recycling
- NUM-07: CNAM Management
- NUM-08: Caller ID Configuration
- NUM-09: Number Capabilities Query
- NUM-10: Multi-Region Number Pools

### Emergency Services (EMG)

- EMG-01: E911 Registration
- EMG-02: NG911 Support
- EMG-03: Advanced Mobile Location (AML)
- EMG-04: Emergency Broadcast Voice
- EMG-05: Emergency Broadcast SMS
- EMG-06: Priority Routing
- EMG-07: PSAP Integration
- EMG-08: Location Updates

### Compliance & Reputation (CMP)

- CMP-01: STIR/SHAKEN Attestation
- CMP-02: 10DLC Campaign Registration
- CMP-03: TCPA Compliance Tools
- CMP-04: DNC List Management
- CMP-05: Number Reputation Monitoring
- CMP-06: Spam Detection & Prevention
- CMP-07: Rate Limiting & Throttling
- CMP-08: HIPAA Mode
- CMP-09: Audit Logging

### Analytics & Reporting (ANL)

- ANL-01: Call Detail Records (CDR)
- ANL-02: Real-Time Webhooks
- ANL-03: Usage Dashboards
- ANL-04: Cost Analytics
- ANL-05: Delivery Reports
- ANL-06: Quality Metrics
- ANL-07: Carrier Performance
- ANL-08: Export & API Access

### AI & Voice Intelligence (AVI)

- AVI-01: Text-to-Speech Calls
- AVI-02: Voice Cloning Integration
- AVI-03: Speech-to-Text Transcription
- AVI-04: Real-Time Translation
- AVI-05: Sentiment Analysis
- AVI-06: Voice Biometrics
- AVI-07: AI Call Agents
- AVI-08: Conversation Intelligence

### Hardware Integration (HWI)

- HWI-01: ATA Device Support
- HWI-02: Gate/Intercom Boxes
- HWI-03: SIP Phone Provisioning
- HWI-04: Alarm Panel Integration

### Platform Administration (ADM)

- ADM-01: Module API Keys
- ADM-02: Rate Limit Configuration
- ADM-03: Carrier Routing Rules
- ADM-04: Failover Configuration
- ADM-05: Cost Center Management
- ADM-06: Feature Flags
- ADM-07: BYOC Trunk Management

---

## Feature ID Reference (T-XX Codes)

For traceability across engineering and product documentation, features are assigned T-XX identifiers:

| ID       | Feature                   | API                          |
| -------- | ------------------------- | ---------------------------- |
| **T-01** | Global SMS/MMS Sending    | `tel.send_sms()`             |
| **T-02** | AI Voice Messages         | `tel.send_voice_message()`   |
| **T-03** | Outbound Voice Calls      | `tel.make_call()`            |
| **T-04** | Conference Calling        | `tel.initiate_conference()`  |
| **T-05** | Outbound Fax              | `tel.send_fax()`             |
| **T-06** | Inbound Fax               | `tel.receive_fax()`          |
| **T-07** | DID Purchase/Provisioning | `tel.buy_number()`           |
| **T-08** | Number Porting            | `tel.port_number()`          |
| **T-09** | CNAM/Caller ID            | `tel.set_caller_id()`        |
| **T-10** | Emergency Broadcast       | `tel.emergency_broadcast()`  |
| **T-11** | Phone Verification/OTP    | `tel.verify_phone()`         |
| **T-12** | E911/NG911/AML            | `tel.request_location()`     |
| **T-13** | Call Recording            | `tel.start_recording()`      |
| **T-14** | Spoof Protection          | `tel.spoof_protect()`        |
| **T-15** | QR Call Codes             | `tel.generate_qr_call()`     |
| **T-16** | Temporary Numbers         | `tel.create_temp_number()`   |
| **T-17** | Route to Human Agent      | `tel.route_to_human_agent()` |
| **T-18** | Voice Cloning             | `tel.create_voice_clone()`   |
| **T-19** | Priority/Silent Ringing   | `tel.priority_ring()`        |
| **T-20** | Carrier Lookup            | `tel.get_carrier_lookup()`   |
| **T-50** | WebRTC Direct Calling     | `tel.webrtc_call()`          |
| **T-51** | AI Voice Streaming        | `tel.stream_ai_voice()`      |
| **T-52** | Satellite SMS Fallback    | `tel.send_satellite_sms()`   |
| **T-53** | Hardware/ATA Support      | `tel.provision_ata()`        |

---

## Priority Legend

| Priority | Meaning             | Timeline |
| -------- | ------------------- | -------- |
| **P0**   | Must have for Alpha | Q1 2026  |
| **P1**   | Must have for Beta  | Q2 2026  |
| **P2**   | Must have for GA    | Q3 2026  |
| **P3**   | Nice to have        | Post-GA  |

---

# Section 1: Executive Summary

## 1.1 Vision Statement

**One API for all telephony. Zero carrier complexity.**

DartwingTel is the single, carrier-grade, globally redundant telephony backbone for the entire Dartwing platform. It is not a user-facing application—it is the shared platform utility that any Dartwing module calls when it needs to interact with the global phone network (PSTN, SMS, fax).

**Core Promise:**

> Any Dartwing module can send/receive SMS, voice, or fax with one line of code—and it will be carrier-grade, compliant, audited, and 40-60% cheaper than Twilio.

## 1.2 What DartwingTel Does

| User Experience (in other modules)     | What DartwingTel Does Behind the Scenes                    |
| -------------------------------------- | ---------------------------------------------------------- |
| "Send magic login link" → SMS fallback | Sends carrier SMS with OTP/link via optimal route          |
| HOA emergency broadcast → voice + SMS  | Places 10,000+ outbound calls/SMS across multiple carriers |
| Gate guard scans guest QR              | Calls resident with caller ID "Front Gate" + optional SMS  |
| DartwingVA "Call Mom"                  | Initiates VoIP → PSTN call with chosen caller ID           |
| DartwingFax sends/receives faxes       | Runs all T.38 FoIP trunks and DID routing                  |
| AI voice clone reads daily briefing    | Streams synthesized audio into an outbound voice call      |
| Two-factor SMS or voice OTP            | Delivers OTP globally with carrier redundancy              |
| Telehealth nurse callback              | Initiates HIPAA-compliant recorded call with transcription |

## 1.3 Problem Statement

| Problem                      | Current State                                      | Impact                                 |
| ---------------------------- | -------------------------------------------------- | -------------------------------------- |
| **Carrier Complexity**       | Each module integrates directly with Twilio/Telnyx | Duplicated code, inconsistent behavior |
| **Cost Overhead**            | Retail CPaaS pricing with markups                  | 60-80% higher costs than wholesale     |
| **Compliance Fragmentation** | Each module handles STIR/SHAKEN, 10DLC separately  | Compliance gaps, carrier blocks        |
| **No Unified Audit**         | Scattered CDRs across carriers                     | Can't trace end-to-end                 |
| **Emergency Services Gap**   | Inconsistent E911 implementation                   | Life-safety risk                       |
| **Reputation Risk**          | No centralized spam monitoring                     | Numbers get flagged/blocked            |

## 1.4 Solution Overview

DartwingTel provides:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DARTWINGTEL VALUE PROPOSITION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BEFORE (Direct Carrier Integration)    AFTER (DartwingTel)                 │
│  ──────────────────────────────────     ─────────────────────               │
│                                                                              │
│  ┌─────────────┐                        ┌─────────────────────────────────┐ │
│  │ DartwingVA  │──┬── Twilio            │                                 │ │
│  ├─────────────┤  │                     │         tel.send_sms()          │ │
│  │ DartwingFax │──┼── Telnyx            │         tel.make_call()         │ │
│  ├─────────────┤  │                     │         tel.send_fax()          │ │
│  │ DartwingHOA │──┼── Bandwidth         │                                 │ │
│  ├─────────────┤  │                     │         DARTWINGTEL             │ │
│  │DartwingHealth──┴── DIDWW             │     (handles everything)        │ │
│  └─────────────┘                        │                                 │ │
│                                         └─────────────────────────────────┘ │
│  Problems:                              Benefits:                            │
│  • 4 different SDKs                     • 1 unified API                     │
│  • 4 billing relationships              • 1 cost center                     │
│  • 4 compliance implementations         • Centralized compliance            │
│  • No cross-module visibility           • Full audit trail                  │
│  • Retail pricing                       • 40-60% cost savings              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.5 Strategic Value

### Platform Benefits

| Benefit                    | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| **Single Integration**     | Modules use one SDK instead of multiple carrier SDKs   |
| **Cost Optimization**      | Wholesale rates + intelligent routing = 40-60% savings |
| **Centralized Compliance** | STIR/SHAKEN, 10DLC, TCPA handled once                  |
| **Unified Audit**          | Every call/SMS/fax traceable end-to-end                |
| **Carrier Abstraction**    | Swap carriers without module code changes              |
| **Redundancy**             | Automatic failover across multiple carriers            |
| **Reputation Management**  | Centralized monitoring prevents carrier blocks         |

### Business Value

| Metric               | Without DartwingTel   | With DartwingTel         |
| -------------------- | --------------------- | ------------------------ |
| **Integration Time** | 2-4 weeks per carrier | 1 day with SDK           |
| **Telephony Cost**   | $0.0075/SMS (Twilio)  | $0.003/SMS (wholesale)   |
| **Compliance Risk**  | High (fragmented)     | Low (centralized)        |
| **Carrier Blocks**   | Per-module issue      | Platform-wide prevention |
| **E911 Coverage**    | Inconsistent          | 100% compliant           |

## 1.6 Current Status (December 2025)

| Capability          | Status         | Volume                 |
| ------------------- | -------------- | ---------------------- |
| Global SMS/MMS      | ✅ Live        | 42M+ messages sent     |
| Outbound Voice      | ✅ Live        | 8M minutes/month       |
| Fax-over-IP         | ✅ Live        | 52M pages/month        |
| SIP Trunks          | ✅ Live        | 4 carriers, 6 regions  |
| DID Inventory       | ✅ Live        | 70+ countries          |
| E911/NG911          | ✅ Live        | US/Canada/EU           |
| STIR/SHAKEN         | ✅ Live        | A-level attestation    |
| OTP/2FA             | ✅ Live        | 5M verifications/month |
| Emergency Broadcast | ✅ Live        | 100K+ recipients/month |
| AML (Location)      | 🔄 In Progress | Q2 2026                |
| Hardware (ATA)      | 📋 Planned     | Q3 2026                |
| WebRTC Direct       | 📋 Planned     | Q4 2026                |

## 1.7 Key Metrics & Targets

### Reliability Targets

| Metric                     | Target            | Current  |
| -------------------------- | ----------------- | -------- |
| SMS Delivery Success       | ≥99.9%            | 99.7%    |
| Voice Answer Seizure Ratio | ≥99.7%            | 99.5%    |
| Fax Success Rate           | ≥99.9%            | 99.8%    |
| Webhook Delivery P99       | ≤800ms            | 650ms    |
| Telephony Plane Uptime     | 99.999% (5 nines) | 99.99%   |
| Emergency Call Routing     | ≤5 seconds        | 3.2s avg |

### Cost Targets

| Service           | Twilio Price | DartwingTel Target | Savings |
| ----------------- | ------------ | ------------------ | ------- |
| SMS (US)          | $0.0079      | $0.003             | 62%     |
| Voice (US/min)    | $0.014       | $0.006             | 57%     |
| Fax (page)        | $0.07        | $0.025             | 64%     |
| DID (US/mo)       | $1.15        | $0.50              | 57%     |
| Toll-Free (US/mo) | $2.15        | $1.00              | 53%     |

### Adoption Targets (GA + 12 Months)

| Metric                | Target                           |
| --------------------- | -------------------------------- |
| Module Adoption       | 100% of Dartwing modules         |
| Features per Module   | ≥5 telephony features each       |
| Internal Revenue Rank | Top 5 module by transfer pricing |
| External API (Future) | 10 pilot customers               |

## 1.8 Dependencies

| Dependency       | Type          | Status         |
| ---------------- | ------------- | -------------- |
| Telnyx           | Carrier       | ✅ Production  |
| Bandwidth        | Carrier       | ✅ Production  |
| DIDWW            | Carrier       | ✅ Production  |
| Sinch            | Carrier       | ✅ Production  |
| Kamailio         | SIP Proxy     | ✅ Production  |
| dartwing_core    | Platform      | ✅ Production  |
| Frappe Framework | Backend       | ✅ Production  |
| ElevenLabs       | TTS           | ✅ Integration |
| Deepgram         | STT           | ✅ Integration |
| OpenAI Whisper   | Transcription | ✅ Integration |

## 1.9 Goals, Non-Goals & Success Metrics

### Product Goals

1. **Single Telephony Backbone** - All Dartwing modules use DartwingTel; no module talks directly to carriers like Twilio/Telnyx/Bandwidth.

2. **Carrier-Grade Reliability & Compliance** - Match or exceed tier-1 CPaaS standards on delivery rates, latency, uptime, and regulatory compliance (E911/NG911, STIR/SHAKEN, 10DLC, TCPA, HIPAA where needed).

3. **Platform-Level Abstractions** - Simple APIs like `tel.send_sms`, `tel.make_call`, `tel.send_fax` that hide carrier complexity and country-specific rules.

4. **Cost Advantage vs 3rd-Party CPaaS** - Internal transfer pricing per unit is 40-60% lower than Twilio/Telnyx equivalents.

5. **Future-Proofed Telephony** - Clean path to WebRTC, AI voice, satellite SMS fallback, and hardware (ATA/gate boxes) without breaking API contracts.

### Non-Goals (v1.0)

| Non-Goal                   | Rationale                                                      |
| -------------------------- | -------------------------------------------------------------- |
| Public CPaaS offering      | Only internal Dartwing modules + whitelabel platform customers |
| Full CCaaS UI              | Basic routing/queues only; no skills-based ACD configuration   |
| On-premise-only deployment | Cloud-native with optional regional hosting                    |
| Campaign registration UI   | Separate compliance admin module handles 10DLC registration    |

### Success Metrics (GA + 12 Months)

| Category        | Metric                                | Target                           |
| --------------- | ------------------------------------- | -------------------------------- |
| **Adoption**    | Telephony traffic through DartwingTel | 100% of Dartwing modules         |
| **Adoption**    | Features per module                   | ≥5 telephony features each       |
| **Reliability** | SMS delivery success                  | ≥99.9%                           |
| **Reliability** | Voice answer seizure ratio            | ≥99.7%                           |
| **Reliability** | Fax success rate                      | ≥99.9%                           |
| **Reliability** | Webhook delivery P99                  | ≤800ms                           |
| **Reliability** | Telephony plane uptime                | 99.999% (five 9s)                |
| **Economics**   | Cost vs Twilio                        | 40-60% lower                     |
| **Economics**   | Revenue rank                          | Top-5 module by transfer pricing |

## 1.10 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DARTWINGTEL SYSTEM ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    CONSUMER MODULES                                  │   │
│  │                                                                      │   │
│  │   DartwingVA    DartwingFax    DartwingFamily    DartwingHealth     │   │
│  │   DartwingUser  DartwingCompany                                      │   │
│  │                                                                      │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DARTWINGTEL API GATEWAY                           │   │
│  │                                                                      │   │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │   │   Auth   │  │   Rate   │  │  Routing │  │Observabil│           │   │
│  │   │  Module  │  │  Limiter │  │  Engine  │  │   ity    │           │   │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │                                                                      │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DARTWINGTEL CORE SERVICES                         │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │   │
│  │  │  Messaging   │  │    Voice     │  │     Fax      │               │   │
│  │  │   Service    │  │   Service    │  │   Service    │               │   │
│  │  │  (SMS/MMS)   │  │(Calls/Conf)  │  │ (T.38/FoIP)  │               │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │   │
│  │  │   Number     │  │  Emergency   │  │  Reputation  │               │   │
│  │  │   Service    │  │   Service    │  │  & Compliance│               │   │
│  │  │ (DID/Port)   │  │(E911/AML)    │  │   Service    │               │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │   │
│  │  │     CDR      │  │   Webhook    │  │  AI Voice    │               │   │
│  │  │  & Analytics │  │   Engine     │  │   Service    │               │   │
│  │  │   Service    │  │              │  │ (TTS/Clone)  │               │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │   │
│  │                                                                      │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │               CARRIER INTEGRATION LAYER                              │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │         Kamailio / OpenSIPS Session Border Controller        │    │   │
│  │  │              (SIP Proxy, Load Balancing, Failover)           │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │  SMPP    │  │  SIP     │  │  REST    │  │  T.38    │           │   │
│  │  │ Gateway  │  │ Gateway  │  │ Gateway  │  │ Gateway  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │                                                                      │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │                                          │
│         ┌────────────────────────┼────────────────────────┐                │
│         ▼                        ▼                        ▼                │
│    ┌─────────┐             ┌─────────┐             ┌─────────┐            │
│    │ TELNYX  │             │BANDWIDTH│             │  DIDWW  │            │
│    │         │             │         │             │         │            │
│    │ SMS     │             │ SMS     │             │ Voice   │            │
│    │ Voice   │             │ Voice   │             │ Numbers │            │
│    │ Fax     │             │ E911    │             │         │            │
│    └─────────┘             └─────────┘             └─────────┘            │
│         │                        │                        │                │
│         └────────────────────────┴────────────────────────┘                │
│                                  │                                          │
│                                  ▼                                          │
│                         Global PSTN Network                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.11 GA Deliverables (Q3 2026)

By GA, DartwingTel must ship:

| Deliverable                  | Description                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| **DartwingTel API 1.0**      | All T-01 through T-20 features stable and documented              |
| **SDKs**                     | Python + Dart + Node.js (minimum)                                 |
| **Admin Console**            | Telephony Ops console with dashboards, routing, config, CDR views |
| **Compliance Documentation** | E911/NG911, STIR/SHAKEN, 10DLC, HIPAA guidance                    |
| **Integration Guides**       | Migration guides from Twilio/Telnyx for each module               |
| **Example Flows**            | OTP, fax, emergency broadcast, gate access                        |
| **SLO & Incident Playbooks** | Telephony-specific incident runbooks                              |
| **Monitoring Stack**         | 24/7 alerting, on-call rotation, carrier health dashboards        |

---

# Section 2: Consumer Modules & Personas

## 2.1 Overview

DartwingTel is consumed by internal Dartwing modules, not directly by end users. Each consuming module has specific telephony needs that DartwingTel must satisfy.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONSUMER MODULE ECOSYSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                           DARTWINGTEL                                        │
│                    (Telephony Platform Layer)                                │
│                              │                                               │
│         ┌───────────────────┼───────────────────┐                           │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │ DartwingVA  │    │ DartwingFax │    │DartwingFamily│                    │
│  │             │    │             │    │             │                     │
│  │ • AI Calls  │    │ • Fax Send  │    │ • Gate Calls│                     │
│  │ • Briefings │    │ • Fax Recv  │    │ • Emergency │                     │
│  │ • Voice OTP │    │ • Broadcast │    │ • Location  │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │DartwingHealth│   │DartwingCompany│  │DartwingUser │                     │
│  │             │    │             │    │             │                     │
│  │ • Telehealth│    │ • IVR       │    │ • SMS OTP   │                     │
│  │ • Reminders │    │ • Conference│    │ • 2FA Voice │                     │
│  │ • HIPAA SMS │    │ • Recording │    │ • Verify    │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Capability Layering Model

Some capabilities are accessed through intermediate modules rather than directly from DartwingTel:

| Capability            | Direct Access         | Via Intermediate Module                  |
| --------------------- | --------------------- | ---------------------------------------- |
| SMS, Voice, Fax       | Most modules          | —                                        |
| AI Voice (TTS, Clone) | DartwingVA only       | Other modules → DartwingVA → DartwingTel |
| Emergency Broadcast   | DartwingFamily, Admin | —                                        |

**Why layer AI Voice through DartwingVA?**

- Consistent voice personality across all modules
- Centralized voice clone management and consent tracking
- Single point for AI voice billing and usage limits
- Cleaner security model (fewer modules with AI access)

## 2.2 Consumer Module: DartwingVA

### Module Overview

The AI-powered virtual assistant that provides voice-first access to all company systems.

### Telephony Requirements

| Requirement                   | Priority | Features Used          |
| ----------------------------- | -------- | ---------------------- |
| AI voice calls to users       | P0       | VOC-01, AVI-01, AVI-02 |
| Voice message delivery        | P0       | VOC-01, VOC-05         |
| SMS notifications             | P0       | SMS-01, SMS-04         |
| Voice OTP for login           | P1       | VOC-01, VOC-06         |
| Conference calls              | P1       | VOC-08                 |
| Call recording                | P1       | VOC-04                 |
| Real-time transcription       | P2       | AVI-03                 |
| Fax sending on behalf of user | P2       | FAX-01, FAX-04, FAX-05 |

### Use Cases

**UC-VA-01: AI Briefing Call**

```
User: "Have Alex call me with my morning briefing"

DartwingVA → DartwingTel:
  tel.make_call(
    to="+14155551234",
    from=user.assigned_did,
    audio_stream=ai_briefing_stream,
    caller_id_name="Dartwing Alex",
    context={"module": "dartwing_va", "type": "briefing"}
  )

Result: User receives call, AI voice reads briefing
```

**UC-VA-02: Voice Authentication**

```
User: Requests sensitive action

DartwingVA → DartwingTel:
  tel.verify_phone(
    number="+14155551234",
    method="voice",  # Speak OTP code
    code_length=6,
    language="en-US"
  )

Result: User receives voice call with spoken OTP
```

**UC-VA-03: Fax Document**

```
User: "Alex, fax my signed contract to the client"

DartwingVA → DartwingTel:
  tel.send_fax(
    to="+14155551234",
    from=user.assigned_fax_did,
    pdf_url="s3://user-docs/signed_contract.pdf",
    cover_page={
      "to_name": "Acme Corp Legal",
      "from_name": user.name,
      "subject": "Signed Contract"
    },
    context={"module": "dartwing_va", "document_id": "doc_123"}
  )

Result: Contract faxed with cover page, user notified of delivery
```

### Volume Estimates

| Metric             | Monthly Volume |
| ------------------ | -------------- |
| AI Calls           | 500K           |
| Voice Messages     | 200K           |
| SMS Notifications  | 2M             |
| Voice OTPs         | 100K           |
| Conference Minutes | 50K            |
| Faxes Sent         | 50K            |

---

## 2.3 Consumer Module: DartwingFax

### Module Overview

Enterprise-grade digital fax platform with healthcare specialization (MedxFax variant).

### Telephony Requirements

| Requirement             | Priority | Features Used  |
| ----------------------- | -------- | -------------- |
| Outbound fax sending    | P0       | FAX-01, FAX-04 |
| Inbound fax reception   | P0       | FAX-02         |
| T.38 protocol           | P0       | FAX-03         |
| Batch fax operations    | P0       | FAX-07         |
| Fax number provisioning | P0       | NUM-01         |
| HIPAA compliance        | P0       | CMP-08         |
| Cover page generation   | P1       | FAX-05         |

### Use Cases

**UC-FAX-01: Healthcare Fax Sending**

```
User: Sends prescription to pharmacy

DartwingFax → DartwingTel:
  tel.send_fax(
    to="+18005551234",
    from=clinic.fax_did,
    pdf_url="s3://faxes/rx_encrypted.pdf",
    cover_page={
      "to_name": "Main Street Pharmacy",
      "from_name": "Dr. Smith, MD",
      "urgent": true
    },
    hipaa_mode=true,
    retry_config={"max_retries": 3, "retry_delay": 300}
  )

Result: Fax sent with HIPAA audit trail
```

**UC-FAX-02: High-Volume Insurance Fax**

```
Billing: Sends 500 claims to insurers

DartwingFax → DartwingTel:
  tel.batch_fax(
    faxes=[
      {"to": "+18001234567", "pdf_url": "...", "reference": "CLM-001"},
      {"to": "+18001234568", "pdf_url": "...", "reference": "CLM-002"},
      ...
    ],
    from=billing.fax_did,
    pacing={"per_minute": 50},
    webhook_url="https://fax.dartwing.com/webhook/batch"
  )

Result: 500 faxes queued and sent with status tracking
```

### Volume Estimates

| Metric             | Monthly Volume |
| ------------------ | -------------- |
| Outbound Fax Pages | 35M            |
| Inbound Fax Pages  | 17M            |
| Unique Fax DIDs    | 50K            |
| HIPAA Faxes        | 40M pages      |

---

## 2.4 Consumer Module: DartwingFamily

### Module Overview

Comprehensive family management platform with safety, location, and communication features.

**AI Voice Integration:** DartwingFamily accesses AI voice capabilities (TTS, voice synthesis) through DartwingVA rather than directly from DartwingTel. This provides consistent voice personality across the platform while keeping the telephony permission model clean.

```
DartwingFamily → DartwingVA (AI voice generation) → DartwingTel (call delivery)
```

### Telephony Requirements

| Requirement             | Priority | Features Used  |
| ----------------------- | -------- | -------------- |
| Emergency broadcast     | P0       | EMG-04, EMG-05 |
| Gate/intercom calls     | P0       | VOC-01, VOC-02 |
| Family conference calls | P1       | VOC-08         |
| Location-triggered SMS  | P1       | SMS-01         |
| Temporary guest numbers | P1       | NUM-05         |
| E911 with location      | P0       | EMG-01, EMG-03 |
| Panic button calls      | P0       | EMG-06, VOC-01 |
| AI voice announcements  | P1       | Via DartwingVA |

### Use Cases

**UC-FAM-01: Gate Access Call**

```
Guest: Arrives at community gate, scans QR

DartwingFamily → DartwingTel:
  tel.make_call(
    to=resident.phone,
    from=gate.did,
    caller_id_name="Front Gate - John Doe",
    context={"module": "dartwing_family", "type": "gate_access"},
    dtmf_menu={
      "1": "grant_access",
      "2": "deny_access",
      "9": "speak_to_guard"
    },
    timeout=30,
    fallback_action="voicemail"
  )

Result: Resident receives call, presses 1 to open gate
```

**UC-FAM-02: Emergency Broadcast**

```
HOA Board: Hurricane warning to all residents

DartwingFamily → DartwingTel:
  tel.emergency_broadcast(
    recipients=community.all_residents,  # 2,500 numbers
    message="Hurricane warning. Evacuation recommended.",
    channels=["voice", "sms"],
    voice_config={
      "tts_voice": "emergency_female",
      "repeat_count": 2,
      "require_ack": true  # Press 1 to acknowledge
    },
    sms_config={
      "include_link": "https://hoa.dartwing.com/emergency/123"
    },
    priority="critical",
    bypass_dnd=true
  )

Result: All residents receive voice call + SMS within 60 seconds
```

**UC-FAM-03: Child Panic Button**

```
Child: Presses panic button on watch

DartwingFamily → DartwingTel:
  tel.emergency_call(
    to=parents.phone_numbers,
    from=child.assigned_did,
    caller_id_name="EMERGENCY - Emma",
    priority="critical",
    location=child.current_location,
    recording=true,
    escalation_chain=[
      parents.phones,
      emergency_contacts,
      "911"  # If no answer after 60s
    ]
  )

Result: Parents called immediately with location info
```

**UC-FAM-04: Elderly Check-In Call (via DartwingVA)**

```
Schedule: Daily wellness check for grandma

DartwingFamily → DartwingVA:
  va.schedule_wellness_call(
    recipient=grandma.phone,
    schedule="daily@9am",
    personality="warm_caring",
    script="wellness_checkin",
    escalation=family_contacts
  )

DartwingVA → DartwingTel:
  tel.make_call(
    to=grandma.phone,
    audio_stream=va.generate_conversation(),  # AI-driven
    context={"module": "dartwing_family", "type": "wellness_check"}
  )

Result: Grandma receives friendly AI call, family notified if no response
```

### Volume Estimates

| Metric               | Monthly Volume           |
| -------------------- | ------------------------ |
| Gate Calls           | 500K                     |
| Emergency Broadcasts | 50 events, 200K messages |
| Family SMS           | 1M                       |
| Panic Calls          | 5K                       |
| Conference Calls     | 10K                      |

---

## 2.5 Consumer Module: DartwingHealth

### Module Overview

Healthcare platform with telehealth, appointment management, and patient communication.

### Telephony Requirements

| Requirement                | Priority | Features Used  |
| -------------------------- | -------- | -------------- |
| Telehealth calls           | P0       | VOC-01, VOC-04 |
| Appointment reminders      | P0       | SMS-01, VOC-01 |
| HIPAA SMS                  | P0       | SMS-01, CMP-08 |
| Nurse callback             | P1       | VOC-02, VOC-09 |
| Prescription notifications | P1       | SMS-01         |
| Call transcription         | P2       | AVI-03         |
| Voice biometrics           | P3       | AVI-06         |

### Use Cases

**UC-HEALTH-01: Appointment Reminder**

```
System: 24-hour appointment reminder

DartwingHealth → DartwingTel:
  tel.send_appointment_reminder(
    patient=patient.phone,
    appointment={
      "date": "2026-01-15",
      "time": "10:30 AM",
      "provider": "Dr. Smith",
      "location": "Main Clinic"
    },
    channels=["sms", "voice_fallback"],
    confirmation_options={
      "sms_reply": {"C": "confirm", "R": "reschedule"},
      "voice_dtmf": {"1": "confirm", "2": "reschedule"}
    },
    hipaa_mode=true
  )

Result: Patient receives SMS, can reply C to confirm
```

**UC-HEALTH-02: Telehealth Session**

```
Provider: Initiates telehealth call

DartwingHealth → DartwingTel:
  tel.make_call(
    to=patient.phone,
    from=provider.did,
    caller_id_name="Dr. Smith - Telehealth",
    recording={
      "enabled": true,
      "consent_prompt": "This call may be recorded for quality...",
      "storage": "hipaa_compliant"
    },
    transcription={
      "enabled": true,
      "real_time": false,
      "medical_vocabulary": true
    },
    hipaa_mode=true
  )

Result: HIPAA-compliant recorded call with transcription
```

### Volume Estimates

| Metric               | Monthly Volume |
| -------------------- | -------------- |
| Appointment SMS      | 5M             |
| Reminder Calls       | 500K           |
| Telehealth Minutes   | 200K           |
| Nurse Line Calls     | 100K           |
| HIPAA Transcriptions | 50K            |

---

## 2.6 Consumer Module: DartwingCompany

### Module Overview

Business operations platform with CRM, HR, and workflow management.

### Telephony Requirements

| Requirement             | Priority | Features Used  |
| ----------------------- | -------- | -------------- |
| Business IVR            | P1       | VOC-10, VOC-02 |
| Sales call recording    | P1       | VOC-04         |
| Customer SMS            | P1       | SMS-01, SMS-08 |
| Board conference calls  | P1       | VOC-08         |
| HR interview scheduling | P2       | SMS-01, VOC-01 |
| Click-to-call CRM       | P2       | VOC-01         |

### Use Cases

**UC-COMP-01: Sales Call with Recording**

```
Sales Rep: Calls prospect from CRM

DartwingCompany → DartwingTel:
  tel.make_call(
    to=prospect.phone,
    from=rep.did,
    caller_id_name="Acme Corp Sales",
    recording={
      "enabled": true,
      "consent_type": "one_party",  # Check state laws
      "webhook": "https://crm.dartwing.com/recording"
    },
    crm_context={
      "lead_id": "LEAD-12345",
      "opportunity_id": "OPP-6789"
    },
    analytics={
      "track_sentiment": true,
      "extract_action_items": true
    }
  )

Result: Call recorded, transcribed, analyzed, linked to CRM
```

**UC-COMP-02: Business IVR**

```
Customer: Calls main business line

DartwingCompany → DartwingTel:
  tel.create_ivr(
    did=company.main_number,
    greeting="Welcome to Acme Corp. For sales, press 1...",
    menu={
      "1": {"action": "queue", "queue": "sales"},
      "2": {"action": "queue", "queue": "support"},
      "3": {"action": "voicemail", "box": "general"},
      "0": {"action": "transfer", "to": "operator"}
    },
    business_hours={
      "mon-fri": "9:00-17:00",
      "after_hours": {"action": "voicemail"}
    },
    hold_music="professional_1",
    estimated_wait=true
  )

Result: Professional IVR with intelligent routing
```

### Volume Estimates

| Metric             | Monthly Volume |
| ------------------ | -------------- |
| Business Calls     | 200K           |
| CRM SMS            | 500K           |
| Conference Minutes | 100K           |
| IVR Interactions   | 150K           |
| Recording Minutes  | 80K            |

---

## 2.7 Consumer Module: DartwingUser

### Module Overview

Core user management module with authentication and identity services.

### Telephony Requirements

| Requirement        | Priority | Features Used  |
| ------------------ | -------- | -------------- |
| SMS OTP            | P0       | SMS-01         |
| Voice OTP          | P0       | VOC-01, AVI-01 |
| Phone verification | P0       | NUM-09, CMP-01 |
| Magic link SMS     | P0       | SMS-01         |
| Account alerts     | P1       | SMS-01         |

### Use Cases

**UC-USER-01: Multi-Channel OTP**

```
User: Requests login OTP

DartwingUser → DartwingTel:
  tel.verify_phone(
    number="+14155551234",
    method="auto",  # SMS first, voice fallback
    code={
      "length": 6,
      "expires_in": 300,
      "max_attempts": 3
    },
    sms_template="Your Dartwing code is {code}. Expires in 5 min.",
    voice_script="Your verification code is {code_spelled}. Repeating...",
    fallback_chain=["sms", "voice", "whatsapp"],
    rate_limit={
      "per_number": {"count": 5, "period": 3600},
      "per_ip": {"count": 10, "period": 3600}
    }
  )

Result: User receives OTP via best available channel
```

**UC-USER-02: Phone Number Verification**

```
User: Adds new phone number to account

DartwingUser → DartwingTel:
  verification = tel.start_verification(
    number="+14155551234",
    checks=["valid_format", "carrier_lookup", "fraud_score"],
    verification_method="sms"
  )

  # Returns:
  {
    "verification_id": "ver_abc123",
    "number": "+14155551234",
    "valid": true,
    "carrier": "Verizon Wireless",
    "line_type": "mobile",
    "fraud_score": 0.12,  # Low risk
    "status": "pending_code"
  }

Result: Number validated and OTP sent
```

### Volume Estimates

| Metric              | Monthly Volume |
| ------------------- | -------------- |
| SMS OTPs            | 3M             |
| Voice OTPs          | 200K           |
| Phone Verifications | 500K           |
| Account Alert SMS   | 1M             |

---

## 2.8 API Credential Model

Each consuming module receives dedicated API credentials with configured permissions and limits.

```yaml
# Example Module Configuration
module: dartwing_va
api_key: tel_live_va_xxxxxxxxxxxx
permissions:
  sms:
    - send
    - templates
    - delivery_status
  voice:
    - outbound
    - recording
    - conference
    - ai_tts
  fax: [] # No fax access
  numbers:
    - query
    - assign_from_pool
  emergency: [] # No emergency access

rate_limits:
  sms_per_second: 100
  calls_per_second: 50
  concurrent_calls: 500

cost_center: "CC-VA-001"
webhook_url: "https://va.dartwing.com/webhooks/tel"
```

---

## 2.9 Consumer Requirements Matrix

| Module          | SMS | Voice | Fax | Numbers | Emergency | AI Voice | HIPAA |
| --------------- | --- | ----- | --- | ------- | --------- | -------- | ----- |
| DartwingVA      | ✅  | ✅    | ✅  | ✅      | ❌        | ✅       | ❌    |
| DartwingFax     | ❌  | ❌    | ✅  | ✅      | ❌        | ❌       | ✅    |
| DartwingFamily  | ✅  | ✅    | ❌  | ✅      | ✅        | ⚡       | ❌    |
| DartwingHealth  | ✅  | ✅    | ✅  | ✅      | ❌        | ✅       | ✅    |
| DartwingCompany | ✅  | ✅    | ✅  | ✅      | ❌        | ❌       | ❌    |
| DartwingUser    | ✅  | ✅    | ❌  | ✅      | ❌        | ✅       | ❌    |

**Legend:**

- ✅ Direct DartwingTel access
- ❌ Not required / not permitted
- ⚡ Access via DartwingVA (not direct DartwingTel)

**Note:** DartwingFamily uses AI voice features (TTS, voice synthesis) for elderly check-ins, gate announcements, and emergency broadcasts by calling DartwingVA, which then invokes DartwingTel. This keeps AI voice capabilities centralized while allowing all modules to benefit from consistent voice personality.

---

_End of Section 2_

---

# Section 3: SMS & MMS Features

## 3.1 Feature Overview

DartwingTel provides enterprise-grade SMS and MMS capabilities with global reach, carrier redundancy, and full compliance.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SMS/MMS ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Consumer Module                                                             │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DartwingTel SMS Gateway                           │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Message  │  │ Template │  │  Route   │  │ Delivery │            │   │
│  │  │ Parser   │  │  Engine  │  │ Selector │  │ Tracker  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐            │
│         ▼                          ▼                          ▼            │
│    ┌─────────┐              ┌─────────┐              ┌─────────┐          │
│    │ Telnyx  │              │ Bandwidth│              │  Sinch  │          │
│    │  SMPP   │              │   REST   │              │  REST   │          │
│    └─────────┘              └─────────┘              └─────────┘          │
│         │                          │                          │            │
│         └──────────────────────────┴──────────────────────────┘            │
│                                    │                                        │
│                                    ▼                                        │
│                          Global PSTN / Carriers                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## SMS-01: Global SMS Sending

**Priority:** P0 | **Status:** Live | **Category:** SMS

### Description

Send SMS messages to phone numbers in 190+ countries with automatic carrier routing, Unicode support, and delivery tracking.

### User Stories

| ID        | As a...          | I want to...                   | So that...                             |
| --------- | ---------------- | ------------------------------ | -------------------------------------- |
| SMS-01-01 | Module developer | Send SMS with one API call     | I can notify users quickly             |
| SMS-01-02 | Module developer | Receive delivery confirmations | I know the message was delivered       |
| SMS-01-03 | Operations team  | Route messages optimally       | We minimize cost and maximize delivery |

### API Specification

```python
# Python SDK
response = tel.send_sms(
    to="+14155551234",
    from_="+18005559999",  # Or sender_id="Dartwing"
    body="Your verification code is 123456",

    # Optional parameters
    status_callback="https://app.dartwing.com/sms/status",
    validity_period=3600,  # Seconds until message expires
    priority="high",  # high, normal, low

    # Tracking
    tags={"campaign": "onboarding", "user_id": "usr_123"},
    idempotency_key="sms_unique_123",

    # Module context
    context={
        "module": "dartwing_user",
        "action": "otp_send"
    }
)

# Response
{
    "message_id": "msg_abc123xyz",
    "to": "+14155551234",
    "from": "+18005559999",
    "status": "queued",
    "segments": 1,
    "cost": {
        "amount": 0.003,
        "currency": "USD"
    },
    "carrier": "telnyx",
    "created_at": "2026-01-15T10:30:00Z"
}
```

### Webhook Events

```json
// Delivery Status Webhook
{
  "event": "sms.status",
  "message_id": "msg_abc123xyz",
  "status": "delivered",
  "status_details": {
    "carrier_status": "DeliveredToTerminal",
    "delivered_at": "2026-01-15T10:30:05Z"
  },
  "to": "+14155551234",
  "from": "+18005559999",
  "segments": 1,
  "cost": {
    "amount": 0.003,
    "currency": "USD"
  },
  "context": {
    "module": "dartwing_user",
    "action": "otp_send"
  }
}
```

### Status Transitions

```
queued → sending → sent → delivered
                      ↘ failed
                      ↘ undelivered
```

### Acceptance Criteria

- [ ] SMS sent to US numbers delivered within 3 seconds (P95)
- [ ] International SMS delivered within 10 seconds (P95)
- [ ] Delivery success rate ≥99.9% for valid numbers
- [ ] Failed messages include actionable error codes
- [ ] All messages traceable by message_id

### Error Codes

| Code        | Description                 | Resolution                   |
| ----------- | --------------------------- | ---------------------------- |
| TEL-SMS-001 | Invalid phone number format | Validate E.164 format        |
| TEL-SMS-002 | Number not SMS-capable      | Use voice or check line type |
| TEL-SMS-003 | Carrier rejected            | Check spam filters, content  |
| TEL-SMS-004 | Rate limit exceeded         | Slow down, request increase  |
| TEL-SMS-005 | Insufficient balance        | Add credits                  |
| TEL-SMS-006 | Invalid sender ID           | Use approved sender ID       |

---

## SMS-02: MMS with Media Attachments

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Send MMS messages with images, audio, video, and other media attachments.

### API Specification

```python
response = tel.send_mms(
    to="+14155551234",
    from_="+18005559999",
    body="Check out this document",
    media_urls=[
        "https://cdn.dartwing.com/docs/report.pdf",
        "https://cdn.dartwing.com/images/chart.png"
    ],

    # Media options
    media_options={
        "resize_images": true,  # Optimize for MMS
        "max_size_kb": 600,     # Carrier limit
        "fallback_to_link": true  # Send link if too large
    }
)
```

### Supported Media Types

| Type     | Extensions    | Max Size |
| -------- | ------------- | -------- |
| Image    | jpg, png, gif | 600 KB   |
| Audio    | mp3, wav, ogg | 600 KB   |
| Video    | mp4, 3gp      | 600 KB   |
| Document | pdf, vcf      | 600 KB   |

### Acceptance Criteria

- [ ] MMS with images delivered to all major US carriers
- [ ] Large media automatically resized or converted to link
- [ ] Media URLs validated before sending
- [ ] Fallback to SMS + link when MMS not supported

---

## SMS-03: Branded Sender IDs

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Send SMS with alphanumeric sender IDs (e.g., "Dartwing", "HOA Alert") in supported countries.

### API Specification

```python
# Register sender ID
sender = tel.register_sender_id(
    sender_id="DartwingHOA",
    countries=["US", "CA", "GB"],
    use_case="transactional",
    company_name="Dartwing Inc.",
    sample_messages=[
        "Your gate access code is {code}",
        "Board meeting reminder: {date} at {time}"
    ]
)

# Use sender ID
response = tel.send_sms(
    to="+14155551234",
    sender_id="DartwingHOA",  # Instead of phone number
    body="Your gate code is 1234"
)
```

### Country Support Matrix

| Country   | Alphanumeric | Registration Required | Max Length |
| --------- | ------------ | --------------------- | ---------- |
| US        | ✅           | Yes (10DLC)           | 11 chars   |
| Canada    | ✅           | Yes                   | 11 chars   |
| UK        | ✅           | No                    | 11 chars   |
| Australia | ✅           | Yes                   | 11 chars   |
| Germany   | ✅           | No                    | 11 chars   |
| France    | ✅           | Yes                   | 11 chars   |

### Acceptance Criteria

- [ ] Sender IDs work in 30+ countries
- [ ] Registration workflow for required countries
- [ ] Automatic fallback to long code if sender ID blocked
- [ ] Character limit enforced (11 alphanumeric)

---

## SMS-04: SMS Templates & Personalization

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Create reusable SMS templates with variable substitution and approval workflow.

### API Specification

```python
# Create template
template = tel.create_sms_template(
    name="appointment_reminder",
    body="Hi {first_name}, reminder: Your appointment with {provider} is on {date} at {time}. Reply C to confirm or R to reschedule.",
    variables=["first_name", "provider", "date", "time"],
    category="transactional",

    # Compliance
    opt_out_footer=true,  # Adds "Reply STOP to unsubscribe"
    requires_approval=true
)

# Send using template
response = tel.send_sms_template(
    to="+14155551234",
    template_id="tmpl_appointment_reminder",
    variables={
        "first_name": "John",
        "provider": "Dr. Smith",
        "date": "January 15",
        "time": "10:30 AM"
    }
)
```

### Template Features

- Variable substitution with fallback values
- Automatic character count with segment estimation
- A/B testing support
- Version history
- Approval workflow for marketing templates
- Auto opt-out footer insertion

### Acceptance Criteria

- [ ] Templates with unlimited variables
- [ ] Preview with sample data before sending
- [ ] Segment count estimation accurate within 1 segment
- [ ] Template versioning with rollback
- [ ] Approval workflow for 10DLC compliance

---

## SMS-05: Concatenated Long Messages

**Priority:** P0 | **Status:** Live | **Category:** SMS

### Description

Automatically handle messages longer than 160 characters by splitting into concatenated segments.

### Behavior

| Encoding | Single Segment | Multi-Segment     |
| -------- | -------------- | ----------------- |
| GSM-7    | 160 chars      | 153 chars/segment |
| Unicode  | 70 chars       | 67 chars/segment  |

### API Response

```json
{
  "message_id": "msg_abc123xyz",
  "body": "This is a very long message that exceeds...",
  "encoding": "GSM-7",
  "segments": 3,
  "character_count": 425,
  "cost": {
    "amount": 0.009, // 3 × $0.003
    "currency": "USD"
  }
}
```

### Acceptance Criteria

- [ ] Messages up to 1600 characters (10 segments)
- [ ] Accurate segment counting for GSM-7 and Unicode
- [ ] Warning when emoji forces Unicode encoding
- [ ] Cost reflects actual segment count

---

## SMS-06: Delivery Status Tracking

**Priority:** P0 | **Status:** Live | **Category:** SMS

### Description

Real-time delivery status updates via webhooks and API polling.

### Status Values

| Status        | Description             | Final? |
| ------------- | ----------------------- | ------ |
| `queued`      | Accepted by DartwingTel | No     |
| `sending`     | Submitted to carrier    | No     |
| `sent`        | Accepted by carrier     | No     |
| `delivered`   | Delivered to handset    | Yes    |
| `failed`      | Permanent failure       | Yes    |
| `undelivered` | Could not deliver       | Yes    |

### API: Check Status

```python
status = tel.get_sms_status("msg_abc123xyz")

# Response
{
    "message_id": "msg_abc123xyz",
    "status": "delivered",
    "status_history": [
        {"status": "queued", "at": "2026-01-15T10:30:00Z"},
        {"status": "sending", "at": "2026-01-15T10:30:01Z"},
        {"status": "sent", "at": "2026-01-15T10:30:02Z"},
        {"status": "delivered", "at": "2026-01-15T10:30:05Z"}
    ],
    "carrier_info": {
        "carrier": "Verizon Wireless",
        "carrier_status": "DeliveredToTerminal"
    }
}
```

### Acceptance Criteria

- [ ] Webhook delivery within 800ms of status change
- [ ] Status polling API available
- [ ] Status history retained for 90 days
- [ ] Carrier-specific status codes mapped to standard values

---

## SMS-07: Inbound SMS & Webhooks

**Priority:** P0 | **Status:** Live | **Category:** SMS

### Description

Receive incoming SMS messages on DartwingTel numbers with automatic routing to consuming modules.

### Webhook Payload

```json
{
  "event": "sms.received",
  "message_id": "msg_inbound_xyz",
  "to": "+18005559999", // DartwingTel number
  "from": "+14155551234",
  "body": "C", // User's reply
  "received_at": "2026-01-15T10:35:00Z",

  "carrier_info": {
    "carrier": "Verizon Wireless",
    "line_type": "mobile"
  },

  // Context from original outbound (if conversation)
  "conversation": {
    "original_message_id": "msg_abc123xyz",
    "thread_id": "conv_thread_456"
  }
}
```

### Routing Configuration

```yaml
# Per-number routing
did: "+18005559999"
inbound_sms:
  webhook_url: "https://health.dartwing.com/sms/inbound"
  fallback_url: "https://api.dartwing.com/sms/unhandled"
  keyword_routing:
    "STOP": "https://compliance.dartwing.com/opt-out"
    "HELP": "https://api.dartwing.com/sms/help"
    "C": "https://health.dartwing.com/sms/confirm"
    "R": "https://health.dartwing.com/sms/reschedule"
```

### Acceptance Criteria

- [ ] Inbound SMS delivered to webhook within 500ms
- [ ] Keyword-based routing works
- [ ] Conversation threading maintained
- [ ] Auto-reply for STOP/HELP keywords

---

## SMS-08: Two-Way Conversations

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Maintain conversational context across multiple SMS exchanges with the same user.

### API: Send in Conversation

```python
# Start conversation
conversation = tel.start_sms_conversation(
    to="+14155551234",
    from_="+18005559999",
    body="Hi! How can we help you today?",
    session_timeout=3600,  # 1 hour
    context={
        "module": "dartwing_company",
        "lead_id": "lead_123"
    }
)

# Continue conversation
tel.reply_to_conversation(
    conversation_id=conversation.id,
    body="Thanks for your interest! A rep will call you shortly."
)
```

### Conversation State

```json
{
  "conversation_id": "conv_abc123",
  "participants": {
    "customer": "+14155551234",
    "business": "+18005559999"
  },
  "messages": [
    { "direction": "outbound", "body": "Hi! How can we help?", "at": "..." },
    { "direction": "inbound", "body": "Interested in pricing", "at": "..." },
    { "direction": "outbound", "body": "Thanks! A rep will call.", "at": "..." }
  ],
  "status": "active",
  "expires_at": "2026-01-15T11:30:00Z"
}
```

### Acceptance Criteria

- [ ] Conversations tracked for 24 hours
- [ ] Inbound messages routed to correct conversation
- [ ] Context available in webhooks
- [ ] Conversation history queryable

---

## SMS-09: Bulk SMS Campaigns

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Send SMS to large recipient lists with pacing, tracking, and analytics.

### API Specification

```python
campaign = tel.create_sms_campaign(
    name="January Newsletter",
    from_="+18005559999",
    recipients=[
        {"to": "+14155551234", "vars": {"name": "John"}},
        {"to": "+14155551235", "vars": {"name": "Jane"}},
        # ... up to 100,000 recipients
    ],
    body="Hi {name}, check out our January updates: {link}",

    # Pacing
    pacing={
        "strategy": "rate_limited",
        "messages_per_second": 100
    },

    # Scheduling
    schedule={
        "send_at": "2026-01-15T09:00:00Z",
        "timezone": "America/New_York",
        "respect_quiet_hours": true
    },

    # Tracking
    link_tracking=true,
    webhook_url="https://marketing.dartwing.com/campaign/webhook"
)
```

### Campaign Analytics

```json
{
  "campaign_id": "camp_abc123",
  "status": "completed",
  "stats": {
    "total": 10000,
    "sent": 9950,
    "delivered": 9800,
    "failed": 150,
    "unsubscribed": 25,
    "link_clicks": 1234
  },
  "cost": {
    "amount": 29.85,
    "currency": "USD"
  },
  "duration_seconds": 120
}
```

### Acceptance Criteria

- [ ] Handle 100,000+ recipients per campaign
- [ ] Configurable pacing (1-1000 msg/sec)
- [ ] Real-time progress tracking
- [ ] Auto-removal of opt-outs
- [ ] A/B testing support

---

## SMS-10: SMS Scheduling

**Priority:** P1 | **Status:** Live | **Category:** SMS

### Description

Schedule SMS messages for future delivery with timezone support.

### API Specification

```python
response = tel.send_sms(
    to="+14155551234",
    from_="+18005559999",
    body="Your appointment is in 1 hour!",

    schedule={
        "send_at": "2026-01-15T09:30:00",
        "timezone": "America/New_York"
    }
)

# Response
{
    "message_id": "msg_scheduled_123",
    "status": "scheduled",
    "scheduled_for": "2026-01-15T14:30:00Z",  # UTC
    "cancelable_until": "2026-01-15T14:25:00Z"
}

# Cancel scheduled message
tel.cancel_scheduled_sms("msg_scheduled_123")
```

### Acceptance Criteria

- [ ] Schedule up to 7 days in advance
- [ ] Timezone-aware scheduling
- [ ] Cancel/reschedule support
- [ ] Quiet hours enforcement option

---

## SMS-11: Unicode & Emoji Support

**Priority:** P0 | **Status:** Live | **Category:** SMS

### Description

Full support for Unicode characters, emojis, and international scripts.

### Behavior

```python
# Emoji message (Unicode encoding)
response = tel.send_sms(
    to="+14155551234",
    body="Hello! 👋 Your code is 1234 🔐"
)

# Response includes encoding info
{
    "encoding": "UCS-2",  # Unicode
    "character_count": 32,
    "segments": 1,  # 70 chars/segment for Unicode
    "cost_multiplier": 1.0
}
```

### Smart Encoding

- Automatic detection of encoding needs
- Warning when single emoji forces Unicode (higher cost)
- Transliteration option for cost savings

### Acceptance Criteria

- [ ] All Unicode supported
- [ ] Accurate encoding detection
- [ ] Emoji rendering on all carriers
- [ ] Cost impact clearly communicated

---

## SMS-12: Link Shortening & Tracking

**Priority:** P2 | **Status:** In Progress | **Category:** SMS

### Description

Automatically shorten URLs and track clicks for analytics.

### API Specification

```python
response = tel.send_sms(
    to="+14155551234",
    body="Check out our new feature: {link}",
    link_tracking={
        "enabled": true,
        "domain": "dtw.link",  # Custom short domain
        "original_url": "https://dartwing.com/features/new?utm_source=sms"
    }
)

# Message body becomes:
# "Check out our new feature: https://dtw.link/x7kQ9"
```

### Click Analytics

```json
{
  "link_id": "lnk_abc123",
  "short_url": "https://dtw.link/x7kQ9",
  "original_url": "https://dartwing.com/features/new",
  "clicks": 45,
  "unique_clicks": 38,
  "click_events": [
    {
      "clicked_at": "2026-01-15T10:35:00Z",
      "user_agent": "...",
      "ip_country": "US"
    }
  ]
}
```

### Acceptance Criteria

- [ ] URLs shortened automatically
- [ ] Custom short domains supported
- [ ] Click tracking with analytics
- [ ] Links expire after configurable period

---

_End of Section 3_

---

# Section 4: Voice & Calling Features

## 4.1 Feature Overview

DartwingTel provides carrier-grade voice capabilities including outbound calling, inbound routing, conferencing, recording, and IVR functionality.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VOICE ARCHITECTURE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Consumer Module                                                             │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                  DartwingTel Voice Gateway                           │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Call    │  │  Media   │  │   IVR    │  │Recording │            │   │
│  │  │ Control  │  │  Bridge  │  │  Engine  │  │  Engine  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │                     Kamailio / OpenSIPS SBC                          │   │
│  │           (SIP Proxy, Load Balancing, Failover)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐            │
│         ▼                          ▼                          ▼            │
│    ┌─────────┐              ┌─────────┐              ┌─────────┐          │
│    │ Telnyx  │              │Bandwidth│              │  DIDWW  │          │
│    │   SIP   │              │   SIP   │              │   SIP   │          │
│    └─────────┘              └─────────┘              └─────────┘          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## VOC-01: Outbound PSTN Calls

**Priority:** P0 | **Status:** Live | **Category:** Voice

### Description

Initiate outbound calls to any phone number worldwide with full caller ID control and call state management.

### API Specification

```python
# Simple outbound call
call = tel.make_call(
    to="+14155551234",
    from_="+18005559999",

    # Caller ID
    caller_id_name="Dartwing Support",

    # Call behavior
    answer_timeout=30,  # Ring for 30 seconds
    machine_detection="detect",  # Detect answering machines

    # Audio
    audio_url="https://cdn.dartwing.com/audio/greeting.mp3",
    # OR
    tts={
        "text": "Hello, this is a reminder about your appointment.",
        "voice": "en-US-Neural2-F",
        "speed": 1.0
    },

    # Webhooks
    status_callback="https://app.dartwing.com/calls/status",

    # Context
    context={
        "module": "dartwing_health",
        "appointment_id": "apt_123"
    }
)

# Response
{
    "call_id": "call_abc123xyz",
    "to": "+14155551234",
    "from": "+18005559999",
    "status": "queued",
    "direction": "outbound",
    "created_at": "2026-01-15T10:30:00Z"
}
```

### Call Control During Active Call

```python
# Get active call
call = tel.get_call("call_abc123xyz")

# Play audio
tel.call_play_audio("call_abc123xyz", audio_url="...")

# Speak text
tel.call_speak("call_abc123xyz", text="Please hold...")

# Collect DTMF
digits = tel.call_gather_dtmf("call_abc123xyz",
    prompt="Press 1 to confirm, 2 to cancel",
    num_digits=1,
    timeout=10
)

# Transfer call
tel.call_transfer("call_abc123xyz", to="+18005551111")

# Hang up
tel.call_hangup("call_abc123xyz")
```

### Call Status Webhook

```json
{
  "event": "call.status",
  "call_id": "call_abc123xyz",
  "status": "answered",
  "direction": "outbound",
  "to": "+14155551234",
  "from": "+18005559999",
  "duration": 0,
  "answered_at": "2026-01-15T10:30:15Z",
  "answering_machine": false
}
```

### Call States

```
initiated → ringing → answered → active → completed
                 ↘ busy
                 ↘ no_answer
                 ↘ failed
                 ↘ canceled
```

### Acceptance Criteria

- [ ] Call setup time <2 seconds (US/EU)
- [ ] Supports 80+ countries
- [ ] STIR/SHAKEN A-level attestation (US)
- [ ] Answering machine detection >95% accuracy
- [ ] Call control available during active call

---

## VOC-02: Inbound Call Routing

**Priority:** P0 | **Status:** Live | **Category:** Voice

### Description

Route incoming calls on DartwingTel numbers to webhooks, SIP endpoints, or phone numbers.

### Routing Configuration

```python
# Configure inbound routing
tel.configure_inbound_routing(
    did="+18005559999",

    # Webhook routing (most flexible)
    webhook={
        "url": "https://app.dartwing.com/calls/inbound",
        "fallback_url": "https://app.dartwing.com/calls/fallback",
        "timeout": 10
    },

    # OR Direct forwarding
    forward_to="+14155551234",

    # OR SIP endpoint
    sip_endpoint="sip:queue@pbx.company.com",

    # Failover chain
    failover=[
        {"type": "sip", "endpoint": "sip:primary@pbx.company.com"},
        {"type": "number", "to": "+14155551234"},
        {"type": "voicemail", "box": "main"}
    ]
)
```

### Inbound Call Webhook

```json
{
  "event": "call.incoming",
  "call_id": "call_inbound_xyz",
  "to": "+18005559999",
  "from": "+14155551234",
  "caller_id_name": "JOHN SMITH",
  "direction": "inbound",

  "routing_context": {
    "did_label": "Main Support Line",
    "department": "support"
  }
}
```

### Webhook Response (Call Instructions)

```json
{
  "action": "dial",
  "dial": {
    "number": "+14155559999",
    "caller_id": "+18005559999",
    "timeout": 30,
    "record": true
  },
  "fallback_action": {
    "action": "voicemail",
    "greeting": "https://cdn.dartwing.com/audio/vm_greeting.mp3"
  }
}
```

### Acceptance Criteria

- [ ] Inbound calls trigger webhook within 500ms
- [ ] Failover chains work correctly
- [ ] SIP forwarding with low latency
- [ ] Time-based routing support

---

## VOC-03: VoIP-to-PSTN Bridging

**Priority:** P0 | **Status:** Live | **Category:** Voice

### Description

Bridge WebRTC/SIP calls from apps to the PSTN network.

### API Specification

```python
# Generate SIP credentials for app
sip_creds = tel.create_sip_connection(
    type="webrtc",
    allowed_dids=["+18005559999"],

    # Security
    ip_whitelist=["192.168.1.0/24"],
    max_concurrent_calls=10,

    # Codec preferences
    codecs=["opus", "g711u", "g711a"]
)

# Response
{
    "sip_username": "dartwing_app_123",
    "sip_password": "secure_password",
    "sip_domain": "sip.dartwingtel.com",
    "stun_servers": ["stun:stun.dartwingtel.com:3478"],
    "turn_servers": ["turn:turn.dartwingtel.com:3478"]
}
```

### WebRTC Integration

```javascript
// Browser/App SDK
const call = await DartwingTel.dial({
  to: "+14155551234",
  from: "+18005559999",
  video: false,
});

call.on("ringing", () => console.log("Ringing..."));
call.on("answered", () => console.log("Connected!"));
call.on("ended", (reason) => console.log("Call ended:", reason));

// Mute/unmute
call.mute();
call.unmute();

// DTMF
call.sendDTMF("1");

// Hang up
call.hangup();
```

### Acceptance Criteria

- [ ] WebRTC to PSTN latency <200ms
- [ ] Support Opus, G.711 codecs
- [ ] ICE/STUN/TURN for NAT traversal
- [ ] Works on mobile browsers

---

## VOC-04: Call Recording

**Priority:** P0 | **Status:** Live | **Category:** Voice

### Description

Record calls with configurable consent, stereo/mono options, and secure storage.

### API Specification

```python
# Start recording on active call
recording = tel.start_recording(
    call_id="call_abc123xyz",

    # Recording options
    channels="dual",  # "single" or "dual" (stereo)
    format="mp3",  # "mp3", "wav", "ogg"

    # Consent
    consent_type="two_party",  # or "one_party"
    consent_prompt={
        "play_before_record": true,
        "audio_url": "https://cdn.dartwing.com/audio/recording_notice.mp3"
    },

    # Storage
    storage={
        "retention_days": 90,
        "encryption": "aes-256",
        "hipaa_mode": true
    },

    # Transcription
    transcription={
        "enabled": true,
        "language": "en-US",
        "speaker_diarization": true
    }
)

# Stop recording
tel.stop_recording("call_abc123xyz")

# Get recording
recording = tel.get_recording("rec_xyz123")
{
    "recording_id": "rec_xyz123",
    "call_id": "call_abc123xyz",
    "duration": 245,
    "format": "mp3",
    "size_bytes": 1945600,
    "download_url": "https://recordings.dartwingtel.com/...",
    "expires_at": "2026-01-16T10:30:00Z",
    "transcription": {
        "status": "completed",
        "text_url": "https://transcripts.dartwingtel.com/..."
    }
}
```

### Recording Webhook

```json
{
  "event": "recording.completed",
  "recording_id": "rec_xyz123",
  "call_id": "call_abc123xyz",
  "duration": 245,
  "download_url": "...",
  "transcription_status": "processing"
}
```

### Acceptance Criteria

- [ ] Recording available within 60 seconds of call end
- [ ] Dual-channel (stereo) recording for analytics
- [ ] HIPAA-compliant storage option
- [ ] Auto-transcription with speaker labels
- [ ] Consent prompt injection

---

## VOC-05: Voicemail Detection & Handling

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Detect answering machines and voicemail systems with configurable actions.

### API Specification

```python
call = tel.make_call(
    to="+14155551234",
    from_="+18005559999",

    machine_detection={
        "enabled": true,
        "mode": "detect",  # "detect" or "detect_and_wait"
        "timeout": 30,

        # Actions based on detection
        "on_human": {
            "action": "continue",
            "audio_url": "https://cdn.dartwing.com/audio/human_greeting.mp3"
        },
        "on_machine": {
            "action": "leave_message",
            "audio_url": "https://cdn.dartwing.com/audio/voicemail_message.mp3",
            "wait_for_beep": true
        }
    }
)
```

### Detection Webhook

```json
{
  "event": "call.machine_detection",
  "call_id": "call_abc123xyz",
  "result": "machine",
  "confidence": 0.94,
  "detection_time_ms": 2500
}
```

### Acceptance Criteria

- [ ] Detection accuracy >95%
- [ ] Detection within 3 seconds of answer
- [ ] Beep detection for voicemail systems
- [ ] Configurable human vs machine actions

---

## VOC-06: DTMF Input Collection

**Priority:** P0 | **Status:** Live | **Category:** Voice

### Description

Collect touch-tone (DTMF) input from callers for IVR menus and verification.

### API Specification

```python
# Gather DTMF during call
result = tel.call_gather_dtmf(
    call_id="call_abc123xyz",

    prompt={
        "text": "Please enter your 4-digit PIN, followed by pound.",
        "voice": "en-US-Neural2-F"
    },

    # Input configuration
    num_digits=4,
    finish_on_key="#",
    timeout=10,

    # Validation
    valid_digits="0123456789",

    # Retries
    retries=3,
    retry_prompt="Invalid input. Please try again."
)

# Response
{
    "digits": "1234",
    "finish_reason": "complete",  # or "timeout", "hangup"
    "duration_ms": 4500
}
```

### Webhook for Async Gather

```json
{
  "event": "call.dtmf_gathered",
  "call_id": "call_abc123xyz",
  "digits": "1234",
  "finish_reason": "complete"
}
```

### Acceptance Criteria

- [ ] Accurate DTMF detection
- [ ] Support for # and \* keys
- [ ] Configurable timeout and retries
- [ ] Real-time digit streaming option

---

## VOC-07: Call Forwarding & Transfer

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Forward or transfer active calls to other numbers or endpoints.

### API Specification

```python
# Blind transfer (immediate)
tel.call_transfer(
    call_id="call_abc123xyz",
    type="blind",
    to="+14155559999"
)

# Warm transfer (announce first)
tel.call_transfer(
    call_id="call_abc123xyz",
    type="warm",
    to="+14155559999",
    announce={
        "text": "Transferring a call about account inquiry",
        "wait_for_answer": true
    }
)

# Transfer to SIP
tel.call_transfer(
    call_id="call_abc123xyz",
    type="blind",
    sip_endpoint="sip:support@company.com"
)
```

### Transfer Events

```json
{
  "event": "call.transferred",
  "call_id": "call_abc123xyz",
  "transfer_type": "warm",
  "transferred_to": "+14155559999",
  "new_call_id": "call_def456"
}
```

### Acceptance Criteria

- [ ] Blind transfer completes in <1 second
- [ ] Warm transfer with announcement
- [ ] Transfer to SIP endpoints
- [ ] Transfer reason tracking

---

## VOC-08: Conference Calling

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Create and manage multi-party conference calls with moderation controls.

### API Specification

```python
# Create conference
conference = tel.create_conference(
    name="Board Meeting Q1",

    # Participants
    participants=[
        {"number": "+14155551234", "role": "moderator"},
        {"number": "+14155551235", "role": "participant"},
        {"number": "+14155551236", "role": "participant"},
    ],

    # Conference settings
    settings={
        "max_participants": 50,
        "entry_tone": true,
        "exit_tone": true,
        "mute_on_join": true,
        "start_on_moderator": true
    },

    # Recording
    recording={
        "enabled": true,
        "format": "mp3"
    },

    # Scheduling (optional)
    schedule={
        "start_at": "2026-01-15T14:00:00Z",
        "duration_minutes": 60,
        "send_invites": true
    }
)

# Response
{
    "conference_id": "conf_abc123",
    "dial_in": {
        "number": "+18005559999",
        "pin": "123456"
    },
    "participant_links": [
        {"number": "+14155551234", "link": "tel:+18005559999,,123456#"}
    ]
}
```

### Conference Controls

```python
# Mute participant
tel.conference_mute("conf_abc123", participant="+14155551234")

# Unmute
tel.conference_unmute("conf_abc123", participant="+14155551234")

# Remove participant
tel.conference_kick("conf_abc123", participant="+14155551234")

# Add participant mid-call
tel.conference_add("conf_abc123", number="+14155551237")

# End conference
tel.conference_end("conf_abc123")
```

### Acceptance Criteria

- [ ] Support 50+ participants
- [ ] Moderator controls (mute all, lock)
- [ ] Dial-in with PIN
- [ ] Recording with speaker labels
- [ ] Stable audio for 2+ hours

---

## VOC-09: Call Queuing

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Queue incoming calls with hold music, position announcements, and callback options.

### API Specification

```python
# Create queue
queue = tel.create_call_queue(
    name="Support Queue",

    # Hold experience
    hold_music="https://cdn.dartwing.com/music/hold.mp3",
    announce_position=true,
    announce_wait_time=true,
    position_interval=60,  # Seconds between announcements

    # Routing
    agents=[
        {"endpoint": "sip:agent1@company.com", "priority": 1},
        {"endpoint": "+14155551234", "priority": 2},
    ],
    routing_strategy="round_robin",  # or "longest_idle", "skills_based"

    # Limits
    max_wait_time=600,  # 10 minutes
    max_queue_size=50,

    # Callback option
    callback={
        "enabled": true,
        "offer_after_seconds": 120,
        "prompt": "Press 1 to receive a callback instead of waiting"
    }
)
```

### Queue Events

```json
{
  "event": "queue.caller_joined",
  "queue_id": "queue_support",
  "call_id": "call_abc123xyz",
  "position": 5,
  "estimated_wait": 180
}
```

### Acceptance Criteria

- [ ] Queue 100+ concurrent callers
- [ ] Position and wait time announcements
- [ ] Callback scheduling
- [ ] Agent presence tracking
- [ ] SLA monitoring

---

## VOC-10: Interactive Voice Response (IVR)

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Build voice menu systems with DTMF and speech input.

### API Specification

```python
# Create IVR flow
ivr = tel.create_ivr(
    name="Main Menu",
    did="+18005559999",

    greeting={
        "text": "Welcome to Acme Corp. For sales, press 1. For support, press 2. For billing, press 3.",
        "voice": "en-US-Neural2-F"
    },

    menu={
        "1": {
            "action": "transfer",
            "to": "queue:sales"
        },
        "2": {
            "action": "submenu",
            "prompt": "For technical support, press 1. For account help, press 2.",
            "options": {
                "1": {"action": "transfer", "to": "queue:tech_support"},
                "2": {"action": "transfer", "to": "queue:account_support"}
            }
        },
        "3": {
            "action": "transfer",
            "to": "+14155559999"
        },
        "0": {
            "action": "transfer",
            "to": "operator"
        },
        "timeout": {
            "action": "repeat",
            "max_repeats": 3,
            "then": {"action": "transfer", "to": "operator"}
        }
    },

    # Business hours
    schedule={
        "timezone": "America/New_York",
        "hours": {
            "mon-fri": "09:00-17:00"
        },
        "after_hours": {
            "action": "voicemail",
            "greeting": "We're currently closed. Please leave a message."
        }
    }
)
```

### IVR Events

```json
{
  "event": "ivr.selection",
  "ivr_id": "ivr_main_menu",
  "call_id": "call_abc123xyz",
  "selection": "2",
  "path": ["main_menu", "support_submenu"]
}
```

### Acceptance Criteria

- [ ] Multi-level menus
- [ ] DTMF and voice input
- [ ] Business hours routing
- [ ] Analytics on menu paths
- [ ] Visual IVR builder (P3)

---

## VOC-11: Whisper & Barge

**Priority:** P2 | **Status:** In Progress | **Category:** Voice

### Description

Allow supervisors to whisper to agents or barge into active calls.

### API Specification

```python
# Whisper (only agent hears)
tel.call_whisper(
    call_id="call_abc123xyz",
    audio={
        "text": "Offer the 20% discount",
        "voice": "en-US-Neural2-D"
    }
)

# Barge (all parties hear)
tel.call_barge(
    call_id="call_abc123xyz",
    mode="full"  # or "listen_only"
)
```

### Acceptance Criteria

- [ ] Whisper audible only to agent
- [ ] Barge-in with <500ms latency
- [ ] Permission controls for supervisors

---

## VOC-12: Call Analytics & Metrics

**Priority:** P1 | **Status:** Live | **Category:** Voice

### Description

Comprehensive call analytics including duration, disposition, and quality metrics.

### Metrics Available

```json
{
  "call_id": "call_abc123xyz",
  "metrics": {
    "duration": {
      "total_seconds": 245,
      "ring_seconds": 12,
      "talk_seconds": 233
    },
    "quality": {
      "mos_score": 4.2,
      "jitter_ms": 15,
      "packet_loss": 0.1,
      "latency_ms": 85
    },
    "disposition": "completed",
    "hangup_cause": "normal_clearing",
    "hangup_party": "remote"
  }
}
```

### Acceptance Criteria

- [ ] Real-time quality metrics
- [ ] Historical analytics dashboard
- [ ] Exportable CDRs
- [ ] Alert on quality degradation

---

_End of Section 4_

---

# Section 5: Fax Features

## 5.1 Feature Overview

DartwingTel provides enterprise-grade fax capabilities using T.38 Fax-over-IP protocol.

---

## FAX-01: Outbound Fax Sending

**Priority:** P0 | **Status:** Live | **Category:** Fax

### Description

Send faxes to any fax-capable number worldwide with PDF support and delivery tracking.

### API Specification

```python
fax = tel.send_fax(
    to="+14155551234",
    from_="+18005559999",

    # Document
    pdf_url="https://cdn.dartwing.com/docs/invoice.pdf",
    # OR base64
    pdf_base64="JVBERi0xLjQKJeLjz9...",

    # Cover page (optional)
    cover_page={
        "enabled": true,
        "to_name": "Accounts Payable",
        "to_company": "Acme Corp",
        "from_name": "Jane Smith",
        "from_company": "Dartwing Inc",
        "subject": "Invoice #12345",
        "notes": "Please process by end of week"
    },

    # Quality settings
    quality="fine",  # "standard", "fine", "superfine"

    # Retry configuration
    retry={
        "enabled": true,
        "max_attempts": 3,
        "retry_delay_minutes": 5
    },

    # HIPAA mode for healthcare
    hipaa_mode=true,

    # Context
    context={
        "module": "dartwing_fax",
        "document_id": "doc_123"
    }
)

# Response
{
    "fax_id": "fax_abc123xyz",
    "to": "+14155551234",
    "from": "+18005559999",
    "status": "queued",
    "pages": 5,
    "estimated_duration": 150,  # seconds
    "cost_estimate": {
        "amount": 0.125,
        "currency": "USD"
    }
}
```

### Fax Status Webhook

```json
{
  "event": "fax.status",
  "fax_id": "fax_abc123xyz",
  "status": "delivered",
  "pages_sent": 5,
  "duration_seconds": 142,
  "remote_station_id": "FAX 555-1234",
  "cost": {
    "amount": 0.125,
    "currency": "USD"
  }
}
```

### Fax States

```
queued → dialing → negotiating → transmitting → delivered
                                           ↘ failed
                                           ↘ busy
                                           ↘ no_answer
```

### Acceptance Criteria

- [ ] PDF up to 200 pages supported
- [ ] T.38 and fallback to G.711
- [ ] Delivery success rate ≥99.9%
- [ ] Status updates every 10 seconds during transmission

---

## FAX-02: Inbound Fax Reception

**Priority:** P0 | **Status:** Live | **Category:** Fax

### Description

Receive faxes on DartwingTel numbers with automatic PDF conversion.

### Configuration

```python
tel.configure_inbound_fax(
    did="+18005559999",

    webhook_url="https://fax.dartwing.com/inbound",

    # PDF options
    pdf_options={
        "dpi": 200,
        "color": "monochrome",
        "compression": "lzw"
    },

    # Storage
    storage={
        "retention_days": 90,
        "encrypt": true,
        "hipaa_mode": true
    }
)
```

### Inbound Fax Webhook

```json
{
  "event": "fax.received",
  "fax_id": "fax_inbound_xyz",
  "to": "+18005559999",
  "from": "+14155551234",
  "remote_station_id": "DR SMITH OFFICE",
  "pages": 3,
  "received_at": "2026-01-15T10:30:00Z",
  "pdf_url": "https://fax.dartwingtel.com/download/...",
  "expires_at": "2026-01-22T10:30:00Z"
}
```

### Acceptance Criteria

- [ ] PDF available within 30 seconds of completion
- [ ] OCR text extraction option
- [ ] Caller ID / CSID captured
- [ ] HIPAA-compliant storage

---

## FAX-03: T.38 Protocol Support

**Priority:** P0 | **Status:** Live | **Category:** Fax

### Description

Native T.38 Fax-over-IP with automatic G.711 passthrough fallback.

### Protocol Features

| Feature                | Support     |
| ---------------------- | ----------- |
| T.38                   | ✅ Primary  |
| G.711 Passthrough      | ✅ Fallback |
| V.17 (14.4 kbps)       | ✅          |
| V.29 (9.6 kbps)        | ✅          |
| V.27ter (4.8 kbps)     | ✅          |
| ECM (Error Correction) | ✅          |

### Acceptance Criteria

- [ ] T.38 negotiation successful >95%
- [ ] Automatic fallback to G.711
- [ ] ECM enabled by default
- [ ] Compatible with legacy fax machines

---

## FAX-04: PDF Conversion & Normalization

**Priority:** P0 | **Status:** Live | **Category:** Fax

### Description

Convert and normalize PDFs for optimal fax transmission.

### Conversion Features

- Multi-page PDF support
- Color to monochrome conversion
- Resolution adjustment (100-400 DPI)
- Page size normalization (Letter, Legal, A4)
- Text sharpening for readability

### API

```python
# Pre-validate and convert
result = tel.validate_fax_document(
    pdf_url="https://cdn.dartwing.com/docs/invoice.pdf"
)

# Response
{
    "valid": true,
    "pages": 5,
    "estimated_duration": 150,
    "warnings": [
        "Color images will be converted to grayscale",
        "Page 3 has small text that may be hard to read"
    ],
    "optimized_url": "https://cdn.dartwingtel.com/optimized/..."
}
```

---

## FAX-05: Cover Page Generation

**Priority:** P1 | **Status:** Live | **Category:** Fax

### Description

Generate professional fax cover pages automatically.

### API

```python
cover = tel.generate_cover_page(
    template="professional",  # or "simple", "medical", "legal"

    to={
        "name": "John Smith",
        "company": "Acme Corp",
        "fax": "+14155551234",
        "phone": "+14155559999"
    },
    from_={
        "name": "Jane Doe",
        "company": "Dartwing Inc",
        "fax": "+18005559999",
        "phone": "+18005551234"
    },

    subject="Contract for Review",
    message="Please review and sign the attached contract.",

    pages=5,  # Pages to follow
    urgent=false,
    confidential=true
)
```

---

## FAX-06: Fax Status Tracking

**Priority:** P0 | **Status:** Live | **Category:** Fax

### Description

Real-time status tracking for fax transmissions.

### API

```python
status = tel.get_fax_status("fax_abc123xyz")

# Response
{
    "fax_id": "fax_abc123xyz",
    "status": "transmitting",
    "progress": {
        "pages_sent": 3,
        "total_pages": 5,
        "percent_complete": 60
    },
    "timing": {
        "queued_at": "2026-01-15T10:30:00Z",
        "started_at": "2026-01-15T10:30:05Z",
        "estimated_completion": "2026-01-15T10:32:30Z"
    },
    "attempts": 1,
    "last_error": null
}
```

---

## FAX-07: Batch Fax Sending

**Priority:** P1 | **Status:** Live | **Category:** Fax

### Description

Send faxes to multiple recipients with pacing and tracking.

### API

```python
batch = tel.create_fax_batch(
    name="Insurance Claims Batch",
    from_="+18005559999",

    faxes=[
        {"to": "+14155551234", "pdf_url": "...", "reference": "CLM-001"},
        {"to": "+14155551235", "pdf_url": "...", "reference": "CLM-002"},
        # Up to 10,000 faxes
    ],

    pacing={
        "concurrent_faxes": 10,
        "per_minute": 50
    },

    webhook_url="https://fax.dartwing.com/batch/webhook"
)
```

---

## FAX-08: Fax-to-Email Delivery

**Priority:** P2 | **Status:** In Progress | **Category:** Fax

### Description

Forward received faxes to email addresses.

### Configuration

```python
tel.configure_fax_to_email(
    did="+18005559999",

    recipients=["fax@company.com", "admin@company.com"],

    email_template={
        "subject": "Fax received from {from_number}",
        "body": "You have received a {pages} page fax.",
        "attach_pdf": true
    }
)
```

---

## FAX-09: Legacy Device Support

**Priority:** P2 | **Status:** Planned | **Category:** Fax

### Description

Support physical fax machines via ATA devices.

### Features

- ATA device provisioning
- Automatic registration
- Quality optimization
- Remote management

---

_End of Section 5_

---

# Section 6: Number Management Features

## 6.1 Feature Overview

DartwingTel provides comprehensive phone number management including search, purchase, porting, and configuration.

---

## NUM-01: DID Search & Purchase

**Priority:** P0 | **Status:** Live | **Category:** Numbers

### Description

Search and purchase phone numbers from global inventory.

### API Specification

```python
# Search for numbers
results = tel.search_numbers(
    country="US",
    type="local",  # "local", "toll_free", "mobile"

    # Search criteria
    area_code="415",
    contains="555",  # Pattern matching

    # Capabilities required
    capabilities=["voice", "sms", "fax"],

    limit=20
)

# Response
{
    "numbers": [
        {
            "number": "+14155551234",
            "type": "local",
            "locality": "San Francisco, CA",
            "capabilities": ["voice", "sms", "fax"],
            "monthly_cost": 1.00,
            "setup_cost": 0.00
        }
    ],
    "total_available": 150
}

# Purchase number
purchase = tel.purchase_number(
    number="+14155551234",

    # Assignment
    label="Main Office",
    module="dartwing_company",

    # Configuration
    voice_url="https://app.dartwing.com/voice/inbound",
    sms_url="https://app.dartwing.com/sms/inbound",

    # Compliance
    address_requirement={
        "type": "local",
        "address_id": "addr_123"
    }
)
```

### Acceptance Criteria

- [ ] Numbers from 70+ countries
- [ ] Purchase and activation in <60 seconds
- [ ] Pattern matching search
- [ ] Capability filtering

---

## NUM-02: Number Porting

**Priority:** P1 | **Status:** Live | **Category:** Numbers

### Description

Port existing phone numbers to DartwingTel.

### API Specification

```python
# Create port request
port = tel.create_port_request(
    numbers=["+14155551234", "+14155551235"],

    # Authorization
    loa={
        "authorized_name": "John Smith",
        "authorized_title": "CEO",
        "company_name": "Acme Corp",
        "billing_phone": "+14155559999",
        "account_number": "ACC123456"
    },

    # Documents
    documents=[
        {"type": "loa", "file_url": "https://..."},
        {"type": "bill", "file_url": "https://..."}
    ],

    # Target date
    requested_foc_date="2026-02-01"
)

# Response
{
    "port_id": "port_abc123",
    "status": "submitted",
    "numbers": ["+14155551234", "+14155551235"],
    "current_carrier": "AT&T",
    "estimated_foc_date": "2026-02-01"
}

# Check status
status = tel.get_port_status("port_abc123")
```

### Port States

```
submitted → accepted → scheduled → in_progress → completed
                  ↘ rejected (with reason)
```

### Acceptance Criteria

- [ ] Support 80%+ US/CA carriers
- [ ] Document upload and validation
- [ ] Status tracking
- [ ] FOC date management

---

## NUM-03: Toll-Free Numbers

**Priority:** P1 | **Status:** Live | **Category:** Numbers

### Description

Search and purchase toll-free numbers (800, 888, 877, 866, 855, 844, 833).

### API

```python
results = tel.search_numbers(
    country="US",
    type="toll_free",
    prefix="800",  # Specific toll-free prefix
    vanity="SUPPORT"  # Vanity search
)
```

---

## NUM-04: Vanity Number Search

**Priority:** P2 | **Status:** In Progress | **Category:** Numbers

### Description

Search for numbers that spell words or contain patterns.

### API

```python
results = tel.search_vanity_numbers(
    word="FLOWERS",  # 1-800-FLOWERS
    prefixes=["800", "888", "877"],

    # Options
    allow_partial=true,  # Allow partial matches
    min_match=5  # At least 5 characters match
)
```

---

## NUM-05: Temporary Numbers

**Priority:** P1 | **Status:** Live | **Category:** Numbers

### Description

Create disposable numbers for temporary use cases.

### API Specification

```python
# Create temporary number
temp = tel.create_temporary_number(
    country="US",
    capabilities=["voice", "sms"],

    # Expiration
    expires_in_hours=24,
    auto_extend=false,

    # Routing
    voice_forward_to="+14155559999",
    sms_forward_to="https://app.dartwing.com/sms/temp",

    # Privacy
    mask_caller_id=true,

    # Usage
    max_calls=10,
    max_sms=20
)

# Response
{
    "temp_number_id": "tmp_abc123",
    "number": "+14155551234",
    "expires_at": "2026-01-16T10:30:00Z",
    "status": "active"
}

# Extend or release
tel.extend_temporary_number("tmp_abc123", hours=12)
tel.release_temporary_number("tmp_abc123")
```

### Use Cases

- Guest gate access codes
- Anonymous buyer/seller communication
- Short-term campaigns
- Safety scenarios

### Acceptance Criteria

- [ ] Provision in <10 seconds
- [ ] Configurable expiration
- [ ] Usage limits
- [ ] Automatic cleanup

---

## NUM-06: Number Release & Recycling

**Priority:** P1 | **Status:** Live | **Category:** Numbers

### Description

Release numbers with quarantine period and data cleanup.

### API

```python
tel.release_number(
    number="+14155551234",

    # Options
    immediate=false,  # Quarantine for 30 days
    data_retention="delete",  # or "archive"
    reason="no_longer_needed"
)
```

---

## NUM-07: CNAM Management

**Priority:** P1 | **Status:** Live | **Category:** Numbers

### Description

Manage Caller ID Name (CNAM) for outbound calls.

### API

```python
# Set CNAM
tel.set_cnam(
    number="+18005559999",
    cnam_name="DARTWING SUPPORT"  # Max 15 characters
)

# Query CNAM
result = tel.query_cnam("+14155551234")

# Response
{
    "number": "+14155551234",
    "cnam": "JOHN SMITH",
    "carrier": "Verizon Wireless",
    "line_type": "mobile"
}
```

---

## NUM-08: Caller ID Configuration

**Priority:** P0 | **Status:** Live | **Category:** Numbers

### Description

Configure caller ID presentation for outbound calls.

### API

```python
tel.configure_caller_id(
    did="+18005559999",

    # Name displayed
    caller_id_name="Dartwing Support",

    # Verification
    verified=true,  # STIR/SHAKEN attestation

    # Rules
    rules=[
        {
            "condition": {"module": "dartwing_health"},
            "caller_id_name": "Dr Smith Office"
        },
        {
            "condition": {"context.type": "emergency"},
            "caller_id_name": "EMERGENCY"
        }
    ]
)
```

---

## NUM-09: Number Capabilities Query

**Priority:** P0 | **Status:** Live | **Category:** Numbers

### Description

Query capabilities and metadata for any phone number.

### API Specification

```python
info = tel.lookup_number("+14155551234")

# Response
{
    "number": "+14155551234",
    "valid": true,
    "country": "US",
    "country_code": "1",
    "national_format": "(415) 555-1234",
    "e164_format": "+14155551234",

    "carrier": {
        "name": "Verizon Wireless",
        "type": "mobile",
        "mcc": "311",
        "mnc": "480"
    },

    "capabilities": {
        "voice": true,
        "sms": true,
        "mms": true,
        "fax": false
    },

    "fraud_score": 0.15,  # 0-1, lower is better
    "reachability": "reachable"
}
```

### Acceptance Criteria

- [ ] Carrier lookup for 200+ countries
- [ ] Line type detection
- [ ] Fraud scoring
- [ ] Real-time reachability

---

## NUM-10: Multi-Region Number Pools

**Priority:** P2 | **Status:** In Progress | **Category:** Numbers

### Description

Manage pools of numbers across regions for automatic selection.

### API

```python
pool = tel.create_number_pool(
    name="Support Numbers",

    numbers=[
        "+14155551234",  # West Coast
        "+12125551234",  # East Coast
        "+13125551234",  # Midwest
    ],

    selection_strategy="geographic",  # or "round_robin", "sticky"

    # Geographic matching
    geo_rules={
        "default": "+14155551234",
        "states": {
            "NY": "+12125551234",
            "IL": "+13125551234"
        }
    }
)

# Use pool for outbound
tel.send_sms(
    to="+14155559999",
    from_pool="pool_support",  # Auto-selects best number
    body="Hello!"
)
```

---

_End of Section 6_

---

# Section 7: Emergency Services Features

## 7.1 Feature Overview

DartwingTel provides carrier-grade emergency services including E911, NG911, emergency broadcast, and location services.

---

## EMG-01: E911 Registration

**Priority:** P0 | **Status:** Live | **Category:** Emergency

### Description

Register and maintain E911 address information for all voice-capable numbers.

### API Specification

```python
# Register E911 address
e911 = tel.register_e911(
    number="+14155551234",

    address={
        "name": "John Smith",
        "street1": "123 Main Street",
        "street2": "Suite 400",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94102",
        "country": "US"
    },

    # Callback for 911 returns
    callback_number="+14155559999"
)

# Response
{
    "e911_id": "e911_abc123",
    "number": "+14155551234",
    "status": "registered",
    "address_validated": true,
    "psap": "San Francisco 911 Center"
}

# Update address (for nomadic users)
tel.update_e911_address(
    number="+14155551234",
    address={...new_address...}
)
```

### Acceptance Criteria

- [ ] Address validation with USPS/Canada Post
- [ ] PSAP routing verification
- [ ] Address updates within 60 seconds
- [ ] Callback number registration

---

## EMG-02: NG911 Support

**Priority:** P1 | **Status:** Live | **Category:** Emergency

### Description

Next-Generation 911 support with enhanced location and multimedia capabilities.

### Features

- IP-based routing to PSAP
- Additional data (health info, photos) when supported
- Text-to-911 where available
- Location accuracy improvements

### API

```python
# Check NG911 availability
ng911 = tel.check_ng911_support(
    location={
        "lat": 37.7749,
        "lng": -122.4194
    }
)

# Response
{
    "ng911_available": true,
    "psap": "San Francisco NG911",
    "capabilities": ["voice", "text", "video", "data"],
    "text_to_911": true
}
```

---

## EMG-03: Advanced Mobile Location (AML)

**Priority:** P1 | **Status:** In Progress | **Category:** Emergency

### Description

Request and transmit precise device location during emergency calls.

### API Specification

```python
# Request location from device
location = tel.request_emergency_location(
    call_id="call_emergency_123",
    device_id="device_abc",

    # Location options
    accuracy="high",  # GPS when available
    timeout=10
)

# Response
{
    "location_id": "loc_xyz",
    "coordinates": {
        "lat": 37.7749,
        "lng": -122.4194,
        "accuracy_meters": 10,
        "altitude_meters": 50
    },
    "source": "device_gps",  # or "cell_tower", "wifi"
    "timestamp": "2026-01-15T10:30:00Z"
}

# Location transmitted to PSAP automatically
```

### Acceptance Criteria

- [ ] GPS accuracy when available
- [ ] Fallback to cell/WiFi
- [ ] Location transmitted to PSAP
- [ ] Works on iOS and Android

---

## EMG-04: Emergency Broadcast Voice

**Priority:** P0 | **Status:** Live | **Category:** Emergency

### Description

Send emergency voice broadcasts to large groups rapidly.

### API Specification

```python
broadcast = tel.emergency_broadcast(
    name="Hurricane Evacuation Notice",

    recipients=["+14155551234", "+14155551235", ...],  # Up to 100,000
    # OR
    recipient_list_id="list_all_residents",

    # Voice message
    voice={
        "message": "This is an emergency evacuation notice. Hurricane Maria...",
        "voice": "en-US-Neural2-F",
        "repeat_count": 2,
        "slow_speed": true  # Slower for clarity
    },

    # Caller ID
    from_number="+18005559999",
    caller_id_name="EMERGENCY ALERT",

    # Delivery options
    options={
        "require_acknowledgment": true,  # Press 1 to acknowledge
        "retry_no_answer": true,
        "max_attempts": 3,
        "bypass_dnd": true  # Attempt to bypass Do Not Disturb
    },

    # Priority
    priority="critical",  # Overrides rate limits

    # Reporting
    webhook_url="https://emergency.dartwing.com/broadcast/webhook"
)

# Response
{
    "broadcast_id": "broadcast_emergency_123",
    "status": "in_progress",
    "total_recipients": 5000,
    "stats": {
        "queued": 5000,
        "in_progress": 0,
        "completed": 0,
        "acknowledged": 0,
        "failed": 0
    }
}
```

### Broadcast Progress Webhook

```json
{
  "event": "broadcast.progress",
  "broadcast_id": "broadcast_emergency_123",
  "stats": {
    "total": 5000,
    "completed": 2500,
    "acknowledged": 2100,
    "no_answer": 300,
    "failed": 100,
    "in_progress": 2500
  },
  "estimated_completion": "2026-01-15T10:35:00Z"
}
```

### Acceptance Criteria

- [ ] 10,000+ calls within 60 seconds
- [ ] Acknowledgment tracking
- [ ] Retry logic for no-answer
- [ ] Real-time progress dashboard
- [ ] DND bypass where legally permitted

---

## EMG-05: Emergency Broadcast SMS

**Priority:** P0 | **Status:** Live | **Category:** Emergency

### Description

Send emergency SMS broadcasts with high-priority routing.

### API Specification

```python
broadcast = tel.emergency_sms_broadcast(
    recipients=[...],

    message="EMERGENCY: Hurricane evacuation ordered for Zone A. Evacuate immediately. Info: https://emergency.gov/maria",

    from_number="+18005559999",
    sender_id="EMERGENCY",  # Where supported

    options={
        "priority": "critical",
        "delivery_report": true,
        "include_opt_out": false  # Emergency exemption
    }
)
```

### Acceptance Criteria

- [ ] 10,000+ SMS within 30 seconds
- [ ] Carrier priority routing
- [ ] Delivery tracking per recipient
- [ ] No opt-out required for true emergencies

---

## EMG-06: Priority Routing

**Priority:** P0 | **Status:** Live | **Category:** Emergency

### Description

Priority call routing for emergency and safety scenarios.

### Features

- Dedicated carrier capacity
- Queue bypassing
- Priority STIR/SHAKEN attestation
- Enhanced caller ID ("EMERGENCY")

### API

```python
# Mark call as priority
call = tel.make_call(
    to="+14155551234",
    from_="+18005559999",
    priority="emergency",

    context={
        "emergency_type": "safety",
        "reference": "panic_button_123"
    }
)
```

---

## EMG-07: PSAP Integration

**Priority:** P1 | **Status:** Live | **Category:** Emergency

### Description

Direct integration with Public Safety Answering Points.

### Features

- Verified PSAP routing
- Callback number registration
- Location data transmission
- Call metadata for dispatchers

---

## EMG-08: Location Updates

**Priority:** P1 | **Status:** Live | **Category:** Emergency

### Description

Real-time E911 location updates for nomadic VoIP users.

### API

```python
# Update location (from mobile app)
tel.update_user_location(
    user_id="user_123",
    location={
        "lat": 37.7749,
        "lng": -122.4194,
        "address": "123 Main St, San Francisco, CA"
    },
    source="device_gps"
)

# Location used for next E911 call
```

---

_End of Section 7_

---

# Section 8: Compliance & Reputation Features

## 8.1 Feature Overview

DartwingTel provides comprehensive compliance tools for STIR/SHAKEN, 10DLC, TCPA, and number reputation management.

---

## CMP-01: STIR/SHAKEN Attestation

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Full STIR/SHAKEN implementation for caller ID authentication.

### Attestation Levels

| Level | Meaning             | When Used                             |
| ----- | ------------------- | ------------------------------------- |
| **A** | Full attestation    | DartwingTel owns number, knows caller |
| **B** | Partial attestation | Knows customer, not specific caller   |
| **C** | Gateway attestation | Pass-through, limited verification    |

### API

```python
# Check attestation for a number
attestation = tel.get_attestation_level(
    from_number="+18005559999",
    to_number="+14155551234"
)

# Response
{
    "attestation_level": "A",
    "certificate_valid": true,
    "expires_at": "2027-01-15T00:00:00Z"
}
```

### Acceptance Criteria

- [ ] A-level attestation for all DartwingTel numbers
- [ ] Valid SHAKEN certificates
- [ ] Inbound verification
- [ ] Attestation in CDRs

---

## CMP-02: 10DLC Campaign Registration

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Register and manage 10DLC campaigns for A2P SMS.

### API Specification

```python
# Register brand
brand = tel.register_10dlc_brand(
    company_name="Acme Corp",
    ein="12-3456789",
    vertical="HEALTHCARE",

    contact={
        "name": "John Smith",
        "email": "john@acme.com",
        "phone": "+14155551234"
    },

    website="https://acme.com"
)

# Register campaign
campaign = tel.register_10dlc_campaign(
    brand_id="brand_abc123",
    use_case="ACCOUNT_NOTIFICATION",

    description="Appointment reminders and health notifications",

    sample_messages=[
        "Your appointment is scheduled for {date} at {time}. Reply C to confirm.",
        "Your prescription is ready for pickup at {pharmacy}."
    ],

    opt_in_method="VERBAL",
    opt_in_description="Patients consent during registration",

    numbers=["+18005559999"]
)

# Response
{
    "campaign_id": "camp_xyz789",
    "status": "pending_review",
    "trust_score": 75,
    "throughput": {
        "sms_per_second": 10,
        "daily_limit": 100000
    }
}
```

### Campaign States

```
pending_review → approved → active
            ↘ rejected (with reason)
```

### Acceptance Criteria

- [ ] TCR integration
- [ ] Brand vetting
- [ ] Campaign approval workflow
- [ ] Throughput tier management

---

## CMP-03: TCPA Compliance Tools

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Tools for TCPA compliance including consent tracking and quiet hours.

### API Specification

```python
# Check compliance before sending
check = tel.check_tcpa_compliance(
    to="+14155551234",
    message_type="marketing",

    consent={
        "type": "express_written",
        "obtained_at": "2026-01-01T00:00:00Z",
        "method": "web_form",
        "proof_url": "https://..."
    }
)

# Response
{
    "compliant": true,
    "warnings": [],
    "quiet_hours": {
        "applies": false,
        "recipient_timezone": "America/Los_Angeles",
        "current_time": "14:30"
    }
}

# Quiet hours configuration
tel.configure_quiet_hours(
    module="dartwing_company",

    rules={
        "marketing": {
            "start": "21:00",
            "end": "08:00",
            "timezone": "recipient"  # Use recipient's timezone
        },
        "transactional": {
            "exempt": true  # No quiet hours
        },
        "emergency": {
            "exempt": true
        }
    }
)
```

### Acceptance Criteria

- [ ] Quiet hours enforcement (9 PM - 8 AM local)
- [ ] Consent tracking
- [ ] Message type classification
- [ ] Compliance audit logs

---

## CMP-04: DNC List Management

**Priority:** P1 | **Status:** Live | **Category:** Compliance

### Description

Manage internal Do Not Call lists and check against national registries.

### API

```python
# Add to DNC
tel.add_to_dnc(
    number="+14155551234",
    reason="user_request",
    source="sms_stop_keyword"
)

# Check DNC
check = tel.check_dnc("+14155551234")

# Response
{
    "on_internal_dnc": true,
    "on_national_dnc": false,
    "added_at": "2026-01-15T10:30:00Z",
    "reason": "user_request"
}

# Bulk DNC check
results = tel.bulk_dnc_check(["+14155551234", "+14155551235", ...])
```

---

## CMP-05: Number Reputation Monitoring

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Monitor and protect number reputation across carriers.

### API Specification

```python
# Get reputation
reputation = tel.get_number_reputation("+18005559999")

# Response
{
    "number": "+18005559999",
    "reputation_score": 85,  # 0-100, higher is better
    "status": "healthy",

    "carrier_status": {
        "att": {"status": "clean", "score": 90},
        "verizon": {"status": "clean", "score": 88},
        "tmobile": {"status": "flagged", "score": 65, "reason": "high_volume"}
    },

    "metrics": {
        "spam_reports_7d": 2,
        "delivery_rate_7d": 0.98,
        "complaint_rate_7d": 0.001
    },

    "recommendations": [
        "Reduce sending volume to T-Mobile numbers",
        "Review content for spam triggers"
    ]
}

# Subscribe to reputation alerts
tel.subscribe_reputation_alerts(
    numbers=["+18005559999"],
    threshold=70,  # Alert if score drops below
    webhook_url="https://app.dartwing.com/reputation/alerts"
)
```

### Acceptance Criteria

- [ ] Real-time reputation scoring
- [ ] Per-carrier status
- [ ] Proactive alerts
- [ ] Remediation recommendations

---

## CMP-06: Spam Detection & Prevention

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Detect and prevent spam/fraud from DartwingTel numbers.

### Features

- Content analysis for spam patterns
- Volume anomaly detection
- Automatic throttling
- Number quarantine

### API

```python
# Analyze message for spam
analysis = tel.analyze_content(
    message="Congratulations! You've won $1,000,000! Click here...",
    type="sms"
)

# Response
{
    "spam_score": 0.95,  # High spam probability
    "flags": [
        "prize_scam_pattern",
        "suspicious_url",
        "excessive_punctuation"
    ],
    "action": "block",
    "recommendation": "Do not send - high spam score"
}
```

---

## CMP-07: Rate Limiting & Throttling

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Configurable rate limiting per module, number, and recipient.

### Configuration

```python
tel.configure_rate_limits(
    module="dartwing_company",

    limits={
        "sms": {
            "per_second": 100,
            "per_minute": 5000,
            "per_day": 100000,
            "per_recipient_per_day": 10
        },
        "voice": {
            "concurrent_calls": 100,
            "per_second": 10,
            "per_day": 10000
        }
    },

    burst={
        "allowed": true,
        "multiplier": 2,
        "duration_seconds": 60
    },

    on_limit_exceeded="queue"  # or "reject", "alert"
)
```

---

## CMP-08: HIPAA Mode

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

HIPAA-compliant mode for healthcare communications.

### Features

- Encrypted storage
- Restricted access
- Audit logging
- BAA documentation
- PHI handling

### API

```python
# Enable HIPAA mode for module
tel.enable_hipaa_mode(
    module="dartwing_health",

    settings={
        "encryption": "aes-256",
        "access_logging": true,
        "retention_days": 2555,  # 7 years
        "auto_redact_phi": true
    },

    # Business Associate Agreement
    baa_reference="BAA-2026-001"
)

# Send HIPAA-compliant SMS
tel.send_sms(
    to="+14155551234",
    body="Your test results are ready. Login to view.",
    hipaa_mode=true,

    # No PHI in message
    phi_check={
        "enabled": true,
        "action": "block"  # Block if PHI detected
    }
)
```

---

## CMP-09: Audit Logging

**Priority:** P0 | **Status:** Live | **Category:** Compliance

### Description

Comprehensive audit logs for all telephony operations.

### Log Contents

```json
{
  "audit_id": "aud_abc123",
  "timestamp": "2026-01-15T10:30:00Z",
  "module": "dartwing_health",
  "api_key": "tel_live_health_xxx",

  "operation": "send_sms",
  "resource_id": "msg_xyz789",

  "request": {
    "to": "+14155551234",
    "body_length": 45,
    "hipaa_mode": true
  },

  "response": {
    "status": "queued",
    "message_id": "msg_xyz789"
  },

  "caller": {
    "ip": "192.168.1.100",
    "user_agent": "dartwing-health/1.0"
  },

  "compliance": {
    "tcpa_check": "passed",
    "dnc_check": "passed",
    "consent_verified": true
  }
}
```

### Acceptance Criteria

- [ ] All operations logged
- [ ] Immutable audit trail
- [ ] Searchable by any field
- [ ] Export for compliance audits
- [ ] Retention per requirements

---

_End of Section 8_

---

# Section 9: Analytics & Reporting Features

## 9.1 Feature Overview

DartwingTel provides comprehensive analytics, CDRs, and reporting for all telephony operations.

---

## ANL-01: Call Detail Records (CDR)

**Priority:** P0 | **Status:** Live | **Category:** Analytics

### Description

Detailed records for every call, SMS, and fax with full metadata.

### CDR Schema

```json
{
  "cdr_id": "cdr_abc123xyz",
  "type": "voice",
  "direction": "outbound",

  "parties": {
    "from": "+18005559999",
    "to": "+14155551234",
    "caller_id_name": "Dartwing Support"
  },

  "timing": {
    "initiated_at": "2026-01-15T10:30:00Z",
    "answered_at": "2026-01-15T10:30:12Z",
    "ended_at": "2026-01-15T10:35:45Z",
    "duration_seconds": 333,
    "ring_seconds": 12,
    "talk_seconds": 321
  },

  "routing": {
    "carrier": "telnyx",
    "region": "us-west",
    "route_id": "route_123"
  },

  "quality": {
    "mos_score": 4.2,
    "jitter_ms": 15,
    "packet_loss_percent": 0.1
  },

  "disposition": {
    "status": "completed",
    "hangup_cause": "normal_clearing",
    "hangup_party": "remote"
  },

  "cost": {
    "amount": 0.048,
    "currency": "USD",
    "breakdown": {
      "base": 0.036,
      "recording": 0.012
    }
  },

  "context": {
    "module": "dartwing_va",
    "api_key": "tel_live_va_xxx",
    "custom_tags": {
      "user_id": "usr_123",
      "campaign": "onboarding"
    }
  },

  "features_used": ["recording", "transcription", "dtmf"]
}
```

### API: Query CDRs

```python
cdrs = tel.list_cdrs(
    # Filters
    start_date="2026-01-01",
    end_date="2026-01-31",
    type="voice",
    direction="outbound",
    module="dartwing_va",

    # Pagination
    limit=100,
    offset=0,

    # Sorting
    sort_by="initiated_at",
    sort_order="desc"
)
```

### Acceptance Criteria

- [ ] CDR for every operation
- [ ] Available within 60 seconds
- [ ] Queryable by any field
- [ ] Retained for 2+ years
- [ ] Export to CSV/JSON

---

## ANL-02: Real-Time Webhooks

**Priority:** P0 | **Status:** Live | **Category:** Analytics

### Description

Real-time event delivery via webhooks with retry and monitoring.

### Webhook Configuration

```python
tel.configure_webhooks(
    module="dartwing_va",

    webhooks={
        "default": {
            "url": "https://va.dartwing.com/tel/webhook",
            "events": ["*"],  # All events
            "secret": "whsec_xxx"  # For signature verification
        },
        "sms": {
            "url": "https://va.dartwing.com/tel/sms",
            "events": ["sms.status", "sms.received"]
        },
        "voice": {
            "url": "https://va.dartwing.com/tel/voice",
            "events": ["call.*"]
        }
    },

    retry={
        "enabled": true,
        "max_attempts": 5,
        "backoff": "exponential"
    }
)
```

### Webhook Signature Verification

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### Acceptance Criteria

- [ ] P99 delivery <800ms
- [ ] Automatic retry on failure
- [ ] Signature verification
- [ ] Event filtering
- [ ] Delivery monitoring

---

## ANL-03: Usage Dashboards

**Priority:** P1 | **Status:** Live | **Category:** Analytics

### Description

Real-time and historical dashboards for telephony usage.

### Dashboard Metrics

```json
{
    "period": "2026-01",
    "module": "dartwing_va",

    "summary": {
        "sms_sent": 125000,
        "sms_received": 45000,
        "voice_minutes": 8500,
        "fax_pages": 0,
        "total_cost": 1250.00
    },

    "trends": {
        "sms_daily": [4200, 4500, 4100, ...],
        "voice_daily": [280, 295, 310, ...]
    },

    "top_destinations": [
        {"country": "US", "count": 115000, "cost": 345.00},
        {"country": "CA", "count": 8500, "cost": 42.50}
    ],

    "delivery_rates": {
        "sms": 0.997,
        "voice": 0.994
    }
}
```

### Acceptance Criteria

- [ ] Real-time metrics (1-minute delay)
- [ ] Historical trends
- [ ] Per-module breakdown
- [ ] Embeddable widgets
- [ ] Export functionality

---

## ANL-04: Cost Analytics

**Priority:** P1 | **Status:** Live | **Category:** Analytics

### Description

Detailed cost tracking and forecasting.

### API

```python
costs = tel.get_cost_analytics(
    module="dartwing_va",
    period="2026-01",
    group_by=["type", "country"]
)

# Response
{
    "period": "2026-01",
    "total_cost": 1250.00,
    "currency": "USD",

    "by_type": {
        "sms": 375.00,
        "voice": 850.00,
        "fax": 0,
        "numbers": 25.00
    },

    "by_country": [
        {"country": "US", "cost": 1100.00},
        {"country": "CA", "cost": 125.00},
        {"country": "GB", "cost": 25.00}
    ],

    "forecast": {
        "next_month": 1350.00,
        "confidence": 0.85
    }
}
```

---

## ANL-05: Delivery Reports

**Priority:** P0 | **Status:** Live | **Category:** Analytics

### Description

Aggregate delivery success rates and failure analysis.

### Report Structure

```json
{
  "period": "2026-01-15",
  "module": "dartwing_health",
  "type": "sms",

  "totals": {
    "sent": 5000,
    "delivered": 4950,
    "failed": 30,
    "pending": 20
  },

  "delivery_rate": 0.99,

  "failures_by_reason": [
    { "reason": "invalid_number", "count": 15 },
    { "reason": "carrier_rejected", "count": 10 },
    { "reason": "timeout", "count": 5 }
  ],

  "latency": {
    "p50_ms": 1500,
    "p95_ms": 3200,
    "p99_ms": 5100
  }
}
```

---

## ANL-06: Quality Metrics

**Priority:** P1 | **Status:** Live | **Category:** Analytics

### Description

Voice and fax quality monitoring and reporting.

### Metrics

```json
{
  "period": "2026-01-15",
  "type": "voice",

  "quality": {
    "mos_average": 4.1,
    "mos_p5": 3.2, // 5th percentile (worst)
    "jitter_avg_ms": 18,
    "packet_loss_avg": 0.2,
    "latency_avg_ms": 95
  },

  "call_completion": {
    "asr": 0.994, // Answer seizure ratio
    "acd_seconds": 180 // Average call duration
  },

  "issues": [
    {
      "type": "high_packet_loss",
      "occurrences": 12,
      "affected_calls": ["call_123", "call_456"]
    }
  ]
}
```

---

## ANL-07: Carrier Performance

**Priority:** P1 | **Status:** Live | **Category:** Analytics

### Description

Per-carrier performance tracking for routing optimization.

### Report

```json
{
  "period": "2026-01",

  "carriers": [
    {
      "carrier": "telnyx",
      "volume": {
        "sms": 80000,
        "voice_minutes": 5000
      },
      "performance": {
        "sms_delivery_rate": 0.998,
        "voice_asr": 0.996,
        "avg_latency_ms": 85
      },
      "cost_per_unit": {
        "sms": 0.003,
        "voice_minute": 0.006
      }
    },
    {
      "carrier": "bandwidth",
      "volume": {
        "sms": 45000,
        "voice_minutes": 3500
      },
      "performance": {
        "sms_delivery_rate": 0.995,
        "voice_asr": 0.992,
        "avg_latency_ms": 95
      }
    }
  ],

  "recommendations": [
    "Increase Telnyx allocation for US SMS - better delivery rate",
    "Use Bandwidth as backup for voice - slightly lower ASR"
  ]
}
```

---

## ANL-08: Export & API Access

**Priority:** P1 | **Status:** Live | **Category:** Analytics

### Description

Export data and access analytics via API.

### Export Formats

- CSV
- JSON
- Parquet (for large datasets)
- Direct S3/GCS delivery

### API

```python
# Create export job
export = tel.create_export(
    type="cdrs",

    filters={
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "module": "dartwing_va"
    },

    format="parquet",

    destination={
        "type": "s3",
        "bucket": "dartwing-analytics",
        "prefix": "exports/va/2026-01/"
    }
)

# Check status
status = tel.get_export_status(export.id)
```

---

_End of Section 9_

---

# Section 10: AI & Voice Intelligence Features

## 10.1 Feature Overview

DartwingTel provides AI-powered voice capabilities including TTS, voice cloning, transcription, and conversation intelligence.

---

## AVI-01: Text-to-Speech Calls

**Priority:** P0 | **Status:** Live | **Category:** AI Voice

### Description

Generate natural voice audio from text for outbound calls.

### API Specification

```python
call = tel.make_call(
    to="+14155551234",
    from_="+18005559999",

    # TTS configuration
    tts={
        "text": "Hello John, this is a reminder about your appointment tomorrow at 2 PM with Dr. Smith.",

        "voice": "en-US-Neural2-F",  # Google/ElevenLabs voice ID
        "provider": "elevenlabs",  # or "google", "aws", "azure"

        "settings": {
            "speed": 1.0,
            "pitch": 0,
            "volume": 0,
            "emphasis": ["appointment", "2 PM"]  # Words to emphasize
        }
    }
)
```

### Available Voices

| Provider   | Languages | Voice Count | Quality |
| ---------- | --------- | ----------- | ------- |
| ElevenLabs | 30+       | 100+        | Premium |
| Google     | 50+       | 200+        | Good    |
| AWS Polly  | 30+       | 60+         | Good    |
| Azure      | 70+       | 300+        | Good    |

### Acceptance Criteria

- [ ] <500ms to first audio
- [ ] Natural prosody
- [ ] SSML support
- [ ] Multi-language support

---

## AVI-02: Voice Cloning Integration

**Priority:** P1 | **Status:** Live | **Category:** AI Voice

### Description

Use cloned voices for personalized AI calls.

### API Specification

```python
# Create voice clone
clone = tel.create_voice_clone(
    name="Alex - VA Voice",

    samples=[
        "https://cdn.dartwing.com/voice/sample1.mp3",
        "https://cdn.dartwing.com/voice/sample2.mp3",
        "https://cdn.dartwing.com/voice/sample3.mp3"
    ],

    description="Professional, warm, helpful assistant voice",

    consent={
        "obtained": true,
        "consent_url": "https://...",
        "voice_owner": "Alex Smith"
    }
)

# Use cloned voice in call
call = tel.make_call(
    to="+14155551234",
    tts={
        "text": "Good morning! Here's your daily briefing...",
        "voice_clone_id": "clone_alex_123"
    }
)
```

### Acceptance Criteria

- [ ] Clone from 3-5 minute samples
- [ ] Consent verification required
- [ ] Real-time streaming
- [ ] Emotion/tone control

---

## AVI-03: Speech-to-Text Transcription

**Priority:** P0 | **Status:** Live | **Category:** AI Voice

### Description

Real-time and batch transcription for calls and voicemails.

### API Specification

```python
# Enable transcription on call
call = tel.make_call(
    to="+14155551234",
    recording=true,

    transcription={
        "enabled": true,
        "provider": "deepgram",  # or "whisper", "google", "aws"

        "options": {
            "language": "en-US",
            "speaker_diarization": true,  # Identify speakers
            "punctuation": true,
            "profanity_filter": false,
            "medical_vocabulary": true  # For healthcare
        },

        "real_time": false  # Post-call transcription
    }
)

# Batch transcription
result = tel.transcribe_audio(
    audio_url="https://recordings.dartwingtel.com/rec_123.mp3",

    options={
        "language": "en-US",
        "speaker_diarization": true
    }
)

# Response
{
    "transcription_id": "trans_xyz",
    "status": "completed",
    "duration_seconds": 245,

    "text": "Hello, this is John calling about my appointment...",

    "segments": [
        {
            "speaker": "speaker_1",
            "start": 0.0,
            "end": 3.5,
            "text": "Hello, this is John calling about my appointment."
        },
        {
            "speaker": "speaker_2",
            "start": 3.8,
            "end": 8.2,
            "text": "Hi John, let me pull up your account."
        }
    ],

    "confidence": 0.94
}
```

### Acceptance Criteria

- [ ] Real-time transcription option
- [ ] Speaker diarization
- [ ] Medical/legal vocabulary
- [ ] > 95% accuracy

---

## AVI-04: Real-Time Translation

**Priority:** P2 | **Status:** Planned | **Category:** AI Voice

### Description

Real-time speech translation during calls.

### API

```python
call = tel.make_call(
    to="+14155551234",

    translation={
        "enabled": true,
        "source_language": "en",
        "target_language": "es",
        "mode": "bidirectional"  # Both parties translated
    }
)
```

---

## AVI-05: Sentiment Analysis

**Priority:** P2 | **Status:** In Progress | **Category:** AI Voice

### Description

Analyze caller sentiment during and after calls.

### API

```python
# Get sentiment for call
sentiment = tel.get_call_sentiment("call_abc123xyz")

# Response
{
    "call_id": "call_abc123xyz",
    "overall_sentiment": "positive",
    "score": 0.72,  # -1 to 1

    "timeline": [
        {"time": 0, "sentiment": "neutral", "score": 0.1},
        {"time": 30, "sentiment": "negative", "score": -0.3},
        {"time": 60, "sentiment": "positive", "score": 0.5},
        {"time": 120, "sentiment": "positive", "score": 0.8}
    ],

    "emotions": {
        "joy": 0.4,
        "anger": 0.1,
        "frustration": 0.2,
        "satisfaction": 0.6
    },

    "key_moments": [
        {
            "time": 35,
            "type": "negative_peak",
            "transcript": "This has been really frustrating..."
        },
        {
            "time": 95,
            "type": "resolution",
            "transcript": "Oh great, that solves my problem!"
        }
    ]
}
```

---

## AVI-06: Voice Biometrics

**Priority:** P3 | **Status:** Planned | **Category:** AI Voice

### Description

Voice-based authentication and identification.

### API

```python
# Enroll voice print
enrollment = tel.enroll_voice_print(
    user_id="usr_123",
    audio_samples=[
        "https://cdn.dartwing.com/voice/enroll1.mp3",
        "https://cdn.dartwing.com/voice/enroll2.mp3"
    ]
)

# Verify during call
verification = tel.verify_voice_print(
    call_id="call_abc123xyz",
    user_id="usr_123"
)

# Response
{
    "verified": true,
    "confidence": 0.94,
    "liveness_check": "passed"
}
```

---

## AVI-07: AI Call Agents

**Priority:** P1 | **Status:** In Progress | **Category:** AI Voice

### Description

AI agents that can handle entire calls autonomously.

### API Specification

```python
# Create AI agent call
call = tel.create_ai_call(
    to="+14155551234",
    from_="+18005559999",

    agent={
        "type": "appointment_confirmation",
        "persona": "friendly_professional",

        "script": {
            "greeting": "Hi, this is Sarah from Dr. Smith's office calling to confirm your appointment.",
            "goal": "Confirm or reschedule appointment",
            "fallback": "transfer_to_human"
        },

        "context": {
            "patient_name": "John",
            "appointment_date": "January 16",
            "appointment_time": "2:00 PM",
            "provider": "Dr. Smith"
        },

        "capabilities": [
            "confirm_appointment",
            "reschedule_appointment",
            "take_message",
            "transfer_to_human"
        ]
    },

    # Escalation
    human_transfer={
        "enabled": true,
        "trigger": ["request", "complex_question", "frustration"],
        "target": "queue:scheduling"
    }
)
```

### Acceptance Criteria

- [ ] Natural conversation flow
- [ ] Goal completion tracking
- [ ] Human escalation
- [ ] Conversation logging

---

## AVI-08: Conversation Intelligence

**Priority:** P2 | **Status:** In Progress | **Category:** AI Voice

### Description

Extract insights, action items, and summaries from calls.

### API

```python
analysis = tel.analyze_call("call_abc123xyz")

# Response
{
    "call_id": "call_abc123xyz",

    "summary": "Customer called about billing issue. Agent credited $50 to account and explained upcoming charges.",

    "topics": [
        {"topic": "billing", "relevance": 0.9},
        {"topic": "account_credit", "relevance": 0.7}
    ],

    "action_items": [
        {
            "action": "Credit $50 to account",
            "owner": "agent",
            "status": "completed",
            "timestamp": "2026-01-15T10:32:00Z"
        },
        {
            "action": "Send billing explanation email",
            "owner": "agent",
            "status": "pending"
        }
    ],

    "questions_asked": [
        "Why was I charged $75 this month?",
        "Can I get a credit for the overcharge?"
    ],

    "compliance": {
        "disclosures_given": ["recording_notice"],
        "pii_detected": ["credit_card_last_four"],
        "issues": []
    }
}
```

---

_End of Section 10_

---

# Section 11: Hardware Integration Features

## 11.1 Feature Overview

DartwingTel supports hardware devices including ATA adapters, gate/intercom boxes, and SIP phones.

---

## HWI-01: ATA Device Support

**Priority:** P2 | **Status:** Planned | **Category:** Hardware

### Description

Support analog telephone adapters for legacy devices.

### Supported Devices

- Grandstream HT801/802
- Cisco SPA112
- Obihai OBi200
- Poly OBi300

### Provisioning API

```python
# Provision ATA device
device = tel.provision_ata(
    mac_address="00:0B:82:XX:XX:XX",
    model="grandstream_ht802",

    lines=[
        {
            "port": 1,
            "did": "+18005559999",
            "name": "Main Fax"
        },
        {
            "port": 2,
            "did": "+18005559998",
            "name": "Backup Line"
        }
    ],

    features={
        "caller_id": true,
        "voicemail": true,
        "fax_detect": true
    }
)

# Response includes provisioning URL
{
    "device_id": "dev_abc123",
    "provision_url": "https://prov.dartwingtel.com/ata/abc123",
    "status": "pending_provision"
}
```

---

## HWI-02: Gate/Intercom Boxes

**Priority:** P2 | **Status:** Planned | **Category:** Hardware

### Description

DartwingTel hardware for gate access and intercom systems.

### Features

- Direct integration with DartwingFamily
- Video intercom support
- QR code scanner
- Keypad entry
- Two-way audio

### API

```python
# Register gate box
gate = tel.register_gate_device(
    device_id="gate_main_entrance",
    location="Main Entrance",

    did="+18005559999",

    features={
        "video": true,
        "qr_scanner": true,
        "keypad": true
    },

    routing={
        "default_action": "call_resident",
        "after_hours": "guard_station",
        "emergency": "+911"
    }
)
```

---

## HWI-03: SIP Phone Provisioning

**Priority:** P2 | **Status:** In Progress | **Category:** Hardware

### Description

Auto-provision SIP phones for business use.

### Supported Phones

- Poly VVX series
- Yealink T4x/T5x series
- Cisco 78xx/88xx series
- Grandstream GRP series

### API

```python
phone = tel.provision_sip_phone(
    mac_address="00:04:F2:XX:XX:XX",
    model="yealink_t54w",

    user={
        "extension": "101",
        "name": "John Smith",
        "did": "+14155551234"
    },

    features={
        "voicemail": true,
        "presence": true,
        "blf_keys": [
            {"key": 1, "extension": "102", "label": "Jane"},
            {"key": 2, "extension": "103", "label": "Bob"}
        ]
    }
)
```

---

## HWI-04: Alarm Panel Integration

**Priority:** P3 | **Status:** Planned | **Category:** Hardware

### Description

Support alarm panels that communicate via phone line.

### Features

- POTS line emulation
- Alarm signal relay
- Central station communication
- Backup cellular failover

---

_End of Section 11_

---

# Section 12: Platform Administration Features

## 12.1 Feature Overview

DartwingTel provides administration tools for managing modules, credentials, routing, and platform configuration.

---

## ADM-01: Module API Keys

**Priority:** P0 | **Status:** Live | **Category:** Admin

### Description

Manage API credentials for consuming modules.

### API Specification

```python
# Create API key for module
key = tel.create_api_key(
    module="dartwing_va",
    name="VA Production",

    permissions={
        "sms": ["send", "receive", "templates"],
        "voice": ["outbound", "inbound", "recording", "conference"],
        "fax": [],
        "numbers": ["query", "assign"],
        "emergency": []
    },

    rate_limits={
        "sms_per_second": 100,
        "voice_per_second": 50
    },

    ip_whitelist=["192.168.1.0/24"],

    expires_at="2027-01-01T00:00:00Z"
)

# Response
{
    "api_key_id": "key_abc123",
    "api_key": "tel_live_va_xxxxxxxxxxxxxxxx",  # Only shown once
    "module": "dartwing_va",
    "created_at": "2026-01-15T10:30:00Z"
}

# Rotate key
new_key = tel.rotate_api_key("key_abc123")

# Revoke key
tel.revoke_api_key("key_abc123")
```

---

## ADM-02: Rate Limit Configuration

**Priority:** P0 | **Status:** Live | **Category:** Admin

### Description

Configure rate limits per module, feature, and destination.

### Configuration

```python
tel.configure_rate_limits(
    module="dartwing_company",

    global_limits={
        "requests_per_second": 1000,
        "concurrent_calls": 500
    },

    feature_limits={
        "sms": {
            "per_second": 100,
            "per_day": 100000
        },
        "voice": {
            "concurrent": 100,
            "per_second": 20
        }
    },

    destination_limits={
        "per_number_per_day": 10,  # Max 10 messages to same number
        "per_country_per_day": {
            "US": 50000,
            "CA": 10000,
            "*": 1000  # Default for other countries
        }
    },

    on_limit_exceeded="queue"  # or "reject", "alert"
)
```

---

## ADM-03: Carrier Routing Rules

**Priority:** P0 | **Status:** Live | **Category:** Admin

### Description

Configure carrier selection and routing priorities.

### Configuration

```python
tel.configure_routing(
    # Default routing
    default={
        "primary": "telnyx",
        "secondary": "bandwidth",
        "tertiary": "sinch"
    },

    # Country-specific routing
    country_routes={
        "US": {
            "primary": "telnyx",
            "secondary": "bandwidth"
        },
        "CA": {
            "primary": "bandwidth",
            "secondary": "telnyx"
        },
        "GB": {
            "primary": "sinch",
            "secondary": "telnyx"
        }
    },

    # Feature-specific routing
    feature_routes={
        "fax": {
            "primary": "telnyx",  # Best T.38 support
            "secondary": "bandwidth"
        },
        "toll_free": {
            "primary": "bandwidth"
        }
    },

    # Cost optimization
    cost_optimization={
        "enabled": true,
        "max_cost_increase_percent": 10  # Accept 10% higher cost for better quality
    }
)
```

---

## ADM-04: Failover Configuration

**Priority:** P0 | **Status:** Live | **Category:** Admin

### Description

Configure automatic failover between carriers.

### Configuration

```python
tel.configure_failover(
    # Health checks
    health_checks={
        "interval_seconds": 30,
        "timeout_seconds": 5,
        "failure_threshold": 3,
        "success_threshold": 2
    },

    # Failover triggers
    triggers={
        "error_rate_threshold": 0.05,  # 5% error rate
        "latency_threshold_ms": 2000,
        "carrier_down": true
    },

    # Failover behavior
    behavior={
        "mode": "automatic",
        "cooldown_seconds": 300,
        "notify": ["ops@dartwing.com"]
    },

    # Carrier health weights
    carrier_weights={
        "telnyx": 0.6,
        "bandwidth": 0.3,
        "sinch": 0.1
    }
)
```

---

## ADM-05: Cost Center Management

**Priority:** P1 | **Status:** Live | **Category:** Admin

### Description

Allocate and track costs per module and department.

### Configuration

```python
# Create cost center
cost_center = tel.create_cost_center(
    name="DartwingHealth - Telehealth",
    code="CC-HEALTH-TH-001",

    budget={
        "monthly": 5000.00,
        "currency": "USD"
    },

    alerts=[
        {"threshold_percent": 80, "notify": ["health-ops@dartwing.com"]},
        {"threshold_percent": 100, "action": "alert_and_throttle"}
    ]
)

# Assign module to cost center
tel.assign_cost_center(
    module="dartwing_health",
    cost_center="CC-HEALTH-TH-001",

    # Optional: subset of operations
    filter={
        "context.type": "telehealth"
    }
)

# Get cost report
report = tel.get_cost_report(
    cost_center="CC-HEALTH-TH-001",
    period="2026-01"
)
```

---

## ADM-06: Feature Flags

**Priority:** P1 | **Status:** Live | **Category:** Admin

### Description

Enable/disable features per module.

### Configuration

```python
tel.configure_feature_flags(
    module="dartwing_va",

    flags={
        "ai_voice_clone": true,
        "emergency_broadcast": false,  # Not enabled for VA
        "hipaa_mode": false,
        "batch_sms": true,
        "conference_calls": true,
        "international_sms": true,
        "premium_tts_voices": true
    }
)
```

---

## ADM-07: BYOC Trunk Management

**Priority:** P2 | **Status:** In Progress | **Category:** Admin

### Description

Allow enterprise customers to bring their own carrier trunks.

### Configuration

```python
# Register BYOC trunk
trunk = tel.register_byoc_trunk(
    name="Customer SIP Trunk",

    # SIP configuration
    sip={
        "host": "sip.customer.com",
        "port": 5060,
        "transport": "tls",
        "username": "dartwing",
        "password": "secure_password"
    },

    # Number ranges
    numbers={
        "ranges": ["+14155550000-+14155559999"],
        "verification_required": true
    },

    # Routing
    routing={
        "inbound": "webhook",
        "outbound_prefixes": ["+1415"]
    }
)
```

---

_End of Section 12_

---

# Section 13: Technical Requirements

## 13.1 Performance Requirements

| Metric                     | Target     |
| -------------------------- | ---------- |
| SMS delivery success       | ≥99.9%     |
| Voice answer seizure ratio | ≥99.7%     |
| Fax success rate           | ≥99.9%     |
| API response time P95      | <200ms     |
| Webhook delivery P99       | <800ms     |
| Voice setup time           | <2 seconds |
| TTS first audio            | <500ms     |

## 13.2 Scalability Requirements

| Metric                   | Target         |
| ------------------------ | -------------- |
| Concurrent voice calls   | 50,000         |
| SMS throughput           | 10,000/second  |
| Fax throughput           | 1,000/minute   |
| API requests             | 100,000/second |
| Numbers under management | 1,000,000      |

## 13.3 Availability Requirements

| Component        | Target            |
| ---------------- | ----------------- |
| Telephony plane  | 99.999% (5 nines) |
| API layer        | 99.99%            |
| Webhook delivery | 99.9%             |
| Admin console    | 99.9%             |

## 13.4 Security Requirements

| Requirement               | Implementation              |
| ------------------------- | --------------------------- |
| Encryption in transit     | TLS 1.3                     |
| Encryption at rest        | AES-256                     |
| API authentication        | API keys + OAuth2           |
| Call recording encryption | AES-256, HIPAA-ready        |
| Audit logging             | Immutable, 7-year retention |
| Vulnerability scanning    | Weekly automated scans      |
| Penetration testing       | Annual third-party          |

## 13.5 Compliance Requirements

| Standard      | Status                    |
| ------------- | ------------------------- |
| STIR/SHAKEN   | Required                  |
| 10DLC         | Required                  |
| TCPA          | Required                  |
| E911/NG911    | Required                  |
| HIPAA         | Required (optional mode)  |
| SOC 2 Type II | Required                  |
| GDPR          | Required                  |
| PCI DSS       | Level 1 (for payment IVR) |

## 13.6 Integration Requirements

### Carrier Integrations

| Carrier   | Protocol   | Features                  |
| --------- | ---------- | ------------------------- |
| Telnyx    | SIP + REST | Voice, SMS, Fax, Numbers  |
| Bandwidth | SIP + REST | Voice, SMS, Numbers, E911 |
| Sinch     | REST       | SMS, Voice                |
| DIDWW     | SIP + REST | Numbers, Voice            |

### Internal Integrations

| Module           | Integration Type    |
| ---------------- | ------------------- |
| dartwing_core    | Frappe API          |
| dartwing_user    | Authentication, OTP |
| dartwing_va      | Voice, SMS, AI      |
| dartwing_fax     | Fax API             |
| dartwing_family  | Emergency, Gate     |
| dartwing_health  | HIPAA, Telehealth   |
| dartwing_company | Business voice      |

## 13.7 SDK Requirements

| Language           | Priority | Status      |
| ------------------ | -------- | ----------- |
| Python             | P0       | Live        |
| Dart/Flutter       | P0       | Live        |
| Node.js/TypeScript | P1       | In Progress |
| Go                 | P2       | Planned     |
| Java/Kotlin        | P3       | Planned     |

---

_End of Section 13_

---

# Section 14: Implementation Roadmap

## 14.1 Roadmap Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IMPLEMENTATION TIMELINE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  2025 Q4         2026 Q1         2026 Q2         2026 Q3         2026 Q4    │
│  ────────        ────────        ────────        ────────        ────────   │
│                                                                              │
│  Current         Alpha           Beta            GA              Scale       │
│  ─────────       ─────           ────            ──              ─────       │
│  • 60% done      • SDK v1        • AI Voice      • Full API      • WebRTC   │
│  • Core SMS      • Full voice    • Voice clone   • All SDKs      • Sat SMS  │
│  • Core Voice    • Full fax      • Sentiment     • Hardware      • CCaaS    │
│  • Core Fax      • 10DLC auto    • Translation   • Full docs     • Global   │
│  • E911 live     • NG911         • AML           • SOC 2         │          │
│                                                                              │
│  ────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  Consumers:      Consumers:      Consumers:      Consumers:                  │
│  Fax, User       +VA, Health     +Family, Comp   All modules                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 14.2 Phase Details

### Phase 1: Current State (Q4 2025)

**Status:** 60% Complete

| Feature          | Status  |
| ---------------- | ------- |
| Global SMS/MMS   | ✅ Live |
| Outbound Voice   | ✅ Live |
| Inbound Voice    | ✅ Live |
| Fax Send/Receive | ✅ Live |
| E911             | ✅ Live |
| STIR/SHAKEN      | ✅ Live |
| Basic Analytics  | ✅ Live |
| Python SDK       | ✅ Live |
| Dart SDK         | ✅ Live |

**Consumers:** DartwingFax, DartwingUser

---

### Phase 2: Alpha (Q1 2026)

**Goal:** Complete core platform, onboard DartwingVA and DartwingHealth

| Feature                        | Priority | Target |
| ------------------------------ | -------- | ------ |
| SDK v1.0 (Python, Dart)        | P0       | Jan    |
| Full voice API                 | P0       | Jan    |
| Full fax API                   | P0       | Jan    |
| Automated 10DLC registration   | P0       | Feb    |
| NG911 support                  | P1       | Feb    |
| Conference calling             | P1       | Feb    |
| Call recording + transcription | P0       | Mar    |
| Admin console v1               | P1       | Mar    |

**Success Criteria:**

- DartwingVA fully integrated
- DartwingHealth telehealth working
- 99.9% SMS delivery rate
- <2s voice setup time

---

### Phase 3: Beta (Q2 2026)

**Goal:** AI voice features, sentiment, translation

| Feature               | Priority | Target |
| --------------------- | -------- | ------ |
| AI voice calls (TTS)  | P0       | Apr    |
| Voice cloning         | P1       | Apr    |
| Sentiment analysis    | P2       | May    |
| Real-time translation | P2       | May    |
| AML (location)        | P1       | May    |
| Node.js SDK           | P1       | Jun    |
| Cost analytics v2     | P1       | Jun    |

**Success Criteria:**

- DartwingVA AI calls working
- DartwingFamily gate integration
- Voice quality MOS >4.0

---

### Phase 4: GA (Q3 2026)

**Goal:** Full platform release

| Feature              | Priority | Target |
| -------------------- | -------- | ------ |
| Full API v1.0        | P0       | Jul    |
| All SDKs             | P0       | Jul    |
| Hardware (ATA, gate) | P2       | Aug    |
| Full documentation   | P0       | Aug    |
| SOC 2 Type II        | P0       | Sep    |
| AI call agents       | P1       | Sep    |

**Success Criteria:**

- All Dartwing modules integrated
- 99.999% uptime achieved
- SOC 2 certified
- Full documentation published

---

### Phase 5: Scale (Q4 2026+)

**Goal:** Advanced features, global expansion

| Feature                | Priority | Target  |
| ---------------------- | -------- | ------- |
| WebRTC direct calling  | P2       | Q4 2026 |
| Satellite SMS fallback | P3       | Q1 2027 |
| Light CCaaS layer      | P3       | Q1 2027 |
| Additional carriers    | P2       | Ongoing |
| Geographic expansion   | P2       | Ongoing |

---

## 14.3 Dependencies & Risks

### Critical Dependencies

| Dependency         | Owner      | Risk   |
| ------------------ | ---------- | ------ |
| Carrier contracts  | Ops        | Low    |
| E911 provider      | Legal      | Low    |
| AI voice providers | Platform   | Medium |
| 10DLC registration | Compliance | Medium |

### Key Risks

| Risk                   | Probability | Impact | Mitigation             |
| ---------------------- | ----------- | ------ | ---------------------- |
| Carrier rate increases | Medium      | Medium | Multi-carrier strategy |
| 10DLC delays           | Medium      | High   | Early registration     |
| AI voice cost overruns | Medium      | Medium | Usage caps, caching    |
| E911 compliance gaps   | Low         | High   | Third-party audit      |

---

## 14.4 Success Metrics (GA + 12 Months)

| Metric                 | Target                |
| ---------------------- | --------------------- |
| Module adoption        | 100% Dartwing modules |
| SMS volume             | 100M+ messages/month  |
| Voice minutes          | 20M+ minutes/month    |
| Fax pages              | 100M+ pages/month     |
| Uptime                 | 99.999%               |
| Cost savings vs Twilio | 40-60%                |
| Customer NPS           | >50                   |

---

_End of Section 14_

---

# Appendix A: API Error Codes

| Code    | Description                  |
| ------- | ---------------------------- |
| TEL-001 | Invalid phone number format  |
| TEL-002 | Number not reachable         |
| TEL-003 | Rate limit exceeded          |
| TEL-004 | Insufficient balance         |
| TEL-005 | Permission denied            |
| TEL-006 | Carrier error                |
| TEL-007 | Timeout                      |
| TEL-008 | Invalid API key              |
| TEL-009 | Feature not enabled          |
| TEL-010 | Compliance block             |
| TEL-101 | SMS - Invalid sender ID      |
| TEL-102 | SMS - Content blocked        |
| TEL-103 | SMS - DNC list match         |
| TEL-201 | Voice - Call failed          |
| TEL-202 | Voice - Busy                 |
| TEL-203 | Voice - No answer            |
| TEL-204 | Voice - Rejected             |
| TEL-301 | Fax - Negotiation failed     |
| TEL-302 | Fax - Transmission error     |
| TEL-303 | Fax - Invalid document       |
| TEL-401 | Number - Not available       |
| TEL-402 | Number - Port rejected       |
| TEL-501 | Emergency - Invalid address  |
| TEL-502 | Emergency - PSAP unreachable |

---

# Appendix B: Webhook Events

| Event                      | Description                |
| -------------------------- | -------------------------- |
| `sms.status`               | SMS delivery status change |
| `sms.received`             | Inbound SMS received       |
| `call.initiated`           | Call started               |
| `call.ringing`             | Call ringing               |
| `call.answered`            | Call answered              |
| `call.completed`           | Call ended                 |
| `call.failed`              | Call failed                |
| `call.recording.ready`     | Recording available        |
| `call.transcription.ready` | Transcription complete     |
| `call.dtmf`                | DTMF digits received       |
| `fax.status`               | Fax status change          |
| `fax.received`             | Inbound fax received       |
| `number.provisioned`       | Number activated           |
| `number.released`          | Number released            |
| `port.status`              | Port request status change |
| `broadcast.progress`       | Broadcast progress update  |
| `broadcast.completed`      | Broadcast finished         |
| `reputation.alert`         | Number reputation alert    |

---

_End of Document_
