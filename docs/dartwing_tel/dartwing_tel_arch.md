# DartwingTel

## Architecture Document

**The Global Telephony Engine for the Dartwing Platform**

---

|                   |                                                     |
| ----------------- | --------------------------------------------------- |
| **Product**       | DartwingTel                                         |
| **Module**        | dartwing_tel                                        |
| **Version**       | 1.0                                                 |
| **Date**          | November 2025                                       |
| **Status**        | Architecture Definition                             |
| **PRD Reference** | dartwing_tel_prd.md (78 features, 52 API endpoints) |
| **Core Arch Ref** | dartwing_core_arch.md                               |

---

## Document Overview

This Architecture Document defines the technical design and implementation patterns for DartwingTel, the carrier-grade telephony backbone for the Dartwing platform. It provides the blueprint for implementing all 78 features defined in the DartwingTel PRD while leveraging the patterns established in the Dartwing Core Architecture.

---

## Table of Contents

| Section | Title                        |
| ------- | ---------------------------- |
| 1       | System Overview              |
| 2       | System Architecture          |
| 3       | Data Model                   |
| 4       | Service Architecture         |
| 5       | Carrier Integration Layer    |
| 6       | Voice Pipeline Architecture  |
| 7       | SMS & Messaging Architecture |
| 8       | Fax Architecture             |
| 9       | API Design                   |
| 10      | Flutter SDK Architecture     |
| 11      | Security & Compliance        |
| 12      | Deployment Architecture      |
| 13      | Operational Runbooks         |
| 14      | Appendices                   |

---

# Section 1: System Overview

## 1.1 Architecture Philosophy

DartwingTel follows a **hybrid architecture** combining the strengths of Frappe (Python) for data management and business logic with .NET Core microservices for real-time voice/media operations. This approach provides:

| Layer               | Technology      | Responsibility                                   |
| ------------------- | --------------- | ------------------------------------------------ |
| **Data & Business** | Frappe (Python) | DocTypes, permissions, audit trails, API surface |
| **Real-Time Voice** | .NET Core       | Sub-millisecond voice routing, WebRTC, SIP       |
| **SIP Proxy**       | Kamailio        | Load balancing, carrier failover, NAT traversal  |
| **Message Queue**   | RabbitMQ        | Async processing, guaranteed delivery            |
| **Client SDK**      | Flutter (Dart)  | Cross-platform native apps with WebRTC           |

### Why Hybrid?

| Concern                   | Frappe (Python)               | .NET Core                             |
| ------------------------- | ----------------------------- | ------------------------------------- |
| **CRUD Operations**       | ✅ Excellent (DocType system) | Overkill                              |
| **Permissions/Audit**     | ✅ Built-in, battle-tested    | Must implement from scratch           |
| **Sub-ms Voice Routing**  | ❌ GIL limits concurrency     | ✅ Async/await, zero-allocation paths |
| **WebRTC/SIP**            | ❌ Limited library ecosystem  | ✅ Mature .NET SIP/WebRTC libraries   |
| **Frappe Integration**    | ✅ Native                     | Requires gRPC/REST bridge             |
| **Developer Familiarity** | ✅ Dartwing team knows Frappe | Learning curve but worth it for voice |

**Decision:** Use Frappe for everything except real-time voice/media, where .NET Core microservices handle the critical path.

## 1.2 Design Principles

### Principle 1: Single Source of Truth

All telephony state persists in Frappe DocTypes. The .NET microservices are stateless workers that read from and write to Frappe via gRPC/REST.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SINGLE SOURCE OF TRUTH                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                      ┌─────────────────────┐  │
│   │   Frappe    │◄────── gRPC ────────►│  .NET Microservice  │  │
│   │   DocType   │                      │                     │  │
│   │             │      Read/Write      │   Stateless Worker  │  │
│   │  TEL Call   │◄────────────────────►│   Voice Gateway     │  │
│   │  TEL SMS    │                      │                     │  │
│   └─────────────┘                      └─────────────────────┘  │
│         │                                                        │
│         │ Persistence                                            │
│         ▼                                                        │
│   ┌─────────────┐                                               │
│   │   MariaDB   │                                               │
│   └─────────────┘                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Principle 2: Carrier Abstraction

Consumer modules never know which carrier (Telnyx, Bandwidth, Sinch, DIDWW) handles their request. All carrier selection, failover, and cost optimization happens in DartwingTel's routing layer.

```python
# Consumer module code - carrier-agnostic
result = tel.send_sms(
    to="+14155551234",
    body="Your verification code is 123456"
)
# DartwingTel internally: Selects Telnyx (cheapest for US),
# fails over to Bandwidth if needed, logs to CDR
```

### Principle 3: Event-Driven Architecture

All telephony operations emit events to a message queue. Webhooks, analytics, and downstream processing consume these events asynchronously.

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   tel.send_sms() ──► SMS Router ──► RabbitMQ ──► Consumers      │
│                           │              │                       │
│                           │              ├──► Webhook Delivery   │
│                           │              ├──► CDR Writer         │
│                           │              ├──► Analytics          │
│                           │              └──► Audit Logger       │
│                           │                                      │
│                           ▼                                      │
│                      Carrier API                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Principle 4: Compliance by Default

Every SMS, call, and fax automatically passes through compliance checks. STIR/SHAKEN attestation, 10DLC enforcement, TCPA quiet hours, and DNC screening happen transparently.

### Principle 5: Flutter-First SDK

The primary integration path is the Dart SDK for Flutter apps. The SDK provides:

- Type-safe API wrappers
- WebRTC integration for in-app calling
- Offline queue for SMS
- Real-time event streams via Socket.IO

## 1.3 Technology Stack

| Component            | Technology       | Version  | Purpose                           |
| -------------------- | ---------------- | -------- | --------------------------------- |
| **Frontend**         | Flutter          | 3.24+    | Cross-platform native apps        |
| **Frontend Lang**    | Dart             | 3.5+     | Type-safe client code             |
| **API Gateway**      | Frappe           | 16.x     | REST API, permissions, DocTypes   |
| **Backend Lang**     | Python           | 3.11+    | Business logic, integrations      |
| **Microservices**    | .NET Core        | 8.0      | Real-time voice, media processing |
| **SIP Proxy**        | Kamailio         | 5.7+     | SIP routing, load balancing       |
| **Media Server**     | Asterisk / Janus | 20.x/1.x | WebRTC gateway, conferencing      |
| **Message Queue**    | RabbitMQ         | 3.12+    | Async event processing            |
| **Cache**            | Redis            | 7.x      | Rate limiting, session state      |
| **Database**         | MariaDB          | 10.6+    | Persistent storage                |
| **Search/Analytics** | OpenSearch       | 2.x      | CDR search, log analytics         |
| **Identity**         | Keycloak         | 24.x     | SSO, OAuth2/OIDC                  |

## 1.4 Module Boundaries

DartwingTel is a **platform module** consumed by other Dartwing modules. It does not have its own user-facing UI except for admin dashboards.

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODULE BOUNDARIES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Consumer Modules (User-Facing)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  DartwingVA    DartwingFax    DartwingFamily             │  │
│  │  DartwingHealth  DartwingCompany  DartwingUser           │  │
│  │                                                           │  │
│  └─────────────────────────┬─────────────────────────────────┘  │
│                            │                                     │
│                            │ Internal API                        │
│                            ▼                                     │
│  Platform Module (Infrastructure)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                      DARTWINGTEL                          │  │
│  │                                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ SMS Engine  │  │Voice Engine │  │ Fax Engine  │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            │ Carrier APIs                        │
│                            ▼                                     │
│  External Carriers                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Telnyx    Bandwidth    Sinch    DIDWW                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 1.5 Integration Patterns

### Pattern 1: Synchronous API Call (Simple Operations)

For simple operations like sending an SMS, consumer modules make synchronous REST calls.

```
Consumer ──► POST /api/method/dartwing_tel.api.send_sms
         ◄── 200 OK {message_id: "SMS-2026-00001", status: "queued"}
```

### Pattern 2: Async with Webhooks (Status Updates)

For operations with delayed results (delivery confirmations, call completion), DartwingTel sends webhooks.

```
Consumer ──► POST /api/method/dartwing_tel.api.send_sms
         ◄── 200 OK {message_id: "...", status: "queued"}

[Later - Carrier confirms delivery]

DartwingTel ──► POST {consumer_webhook_url}
               Body: {event: "sms.delivered", message_id: "..."}
```

### Pattern 3: Real-Time Streams (Voice/WebRTC)

For real-time voice operations, the Flutter SDK maintains WebSocket connections for signaling.

```
Flutter SDK ◄──────► Socket.IO ◄──────► Voice Gateway
                                              │
                                              ▼
                                        WebRTC / SIP
```

### Pattern 4: gRPC (Inter-Service)

Frappe and .NET microservices communicate via gRPC for low-latency internal calls.

```
Frappe API ──► gRPC ──► .NET Voice Gateway ──► Kamailio ──► Carrier
```

---

# Section 2: System Architecture

## 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DARTWINGTEL SYSTEM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       CONSUMER MODULES                               │   │
│  │                                                                      │   │
│  │   DartwingVA   DartwingFax   DartwingFamily   DartwingHealth        │   │
│  │   DartwingUser DartwingCompany  [Future Modules]                    │   │
│  │                                                                      │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │                                          │
│                    REST API / gRPC / Socket.IO                              │
│                                  │                                          │
│  ┌───────────────────────────────▼─────────────────────────────────────┐   │
│  │                       API GATEWAY LAYER                              │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │                   Frappe (dartwing_tel)                       │  │   │
│  │  │                                                               │  │   │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │  │   │
│  │  │  │    API     │ │   Rate     │ │ Permission │ │   Audit    │ │  │   │
│  │  │  │  Handlers  │ │  Limiter   │ │   Check    │ │   Logger   │ │  │   │
│  │  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘ │  │   │
│  │  │                                                               │  │   │
│  │  │  ┌────────────────────────────────────────────────────────┐  │  │   │
│  │  │  │                    DocType Layer                        │  │  │   │
│  │  │  │  TEL DID | TEL Call | TEL SMS | TEL Fax | TEL CDR      │  │  │   │
│  │  │  └────────────────────────────────────────────────────────┘  │  │   │
│  │  │                                                               │  │   │
│  │  └──────────────────────────────┬────────────────────────────────┘  │   │
│  │                                 │                                    │   │
│  └─────────────────────────────────┼────────────────────────────────────┘   │
│                                    │                                        │
│                              gRPC / REST                                    │
│                                    │                                        │
│  ┌─────────────────────────────────▼────────────────────────────────────┐   │
│  │                    .NET MICROSERVICES LAYER                          │   │
│  │                                                                      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │   │
│  │  │    Voice     │ │     SMS      │ │     Fax      │ │   Webhook   │ │   │
│  │  │   Gateway    │ │    Router    │ │  Processor   │ │  Delivery   │ │   │
│  │  │              │ │              │ │              │ │             │ │   │
│  │  │  • SIP/RTP   │ │  • Routing   │ │  • T.38      │ │  • Retry    │ │   │
│  │  │  • WebRTC    │ │  • Failover  │ │  • PDF→TIFF  │ │  • Signing  │ │   │
│  │  │  • Recording │ │  • SMPP      │ │  • OCR       │ │  • Queue    │ │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └─────────────┘ │   │
│  │                                                                      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │   │
│  │  │   Routing    │ │    Media     │ │     CDR      │                 │   │
│  │  │   Engine     │ │  Processor   │ │   Indexer    │                 │   │
│  │  │              │ │              │ │              │                 │   │
│  │  │  • LCR       │ │  • TTS/STT   │ │  • OpenSearch│                 │   │
│  │  │  • Failover  │ │  • Transcode │ │  • Aggregate │                 │   │
│  │  │  • Health    │ │  • Storage   │ │  • Archive   │                 │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                 │   │
│  │                                                                      │   │
│  └─────────────────────────────────┬────────────────────────────────────┘   │
│                                    │                                        │
│                              SIP / REST                                     │
│                                    │                                        │
│  ┌─────────────────────────────────▼────────────────────────────────────┐   │
│  │                  CARRIER INTEGRATION LAYER                           │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │            Kamailio Session Border Controller                   │ │   │
│  │  │                                                                 │ │   │
│  │  │  • SIP Proxy         • NAT Traversal      • TLS Termination   │ │   │
│  │  │  • Load Balancing    • Failover           • Rate Limiting     │ │   │
│  │  │  • Dispatcher        • Topology Hiding    • Header Manip      │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │   │
│  │  │   Telnyx     │ │  Bandwidth   │ │    Sinch     │ │    DIDWW    │ │   │
│  │  │   Adapter    │ │   Adapter    │ │   Adapter    │ │   Adapter   │ │   │
│  │  │              │ │              │ │              │ │             │ │   │
│  │  │ • Voice/SMS  │ │ • Voice/SMS  │ │ • SMS        │ │ • Numbers   │ │   │
│  │  │ • Fax/T.38   │ │ • E911       │ │ • Voice      │ │ • Voice     │ │   │
│  │  │ • Numbers    │ │ • Numbers    │ │              │ │             │ │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └─────────────┘ │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│                          Global PSTN Network                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Request Flow Patterns

### 2.2.1 SMS Send Flow (Synchronous + Async Webhook)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SMS SEND FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. API Request                                                              │
│  ─────────────                                                               │
│  Consumer Module ──POST──► Frappe API (/api/method/dartwing_tel.api.send_sms)│
│                                │                                             │
│                                ▼                                             │
│  2. Validation & Recording                                                   │
│  ─────────────────────────                                                   │
│                         ┌─────────────────────────────────────┐             │
│                         │  • Validate API key & permissions   │             │
│                         │  • Check rate limits (Redis)        │             │
│                         │  • Validate E.164 phone numbers     │             │
│                         │  • Check DNC list                   │             │
│                         │  • Check TCPA quiet hours           │             │
│                         │  • Create TEL SMS Message DocType   │             │
│                         └──────────────────┬──────────────────┘             │
│                                            │                                 │
│                                            ▼                                 │
│  3. Route to Carrier                                                         │
│  ──────────────────                                                          │
│                         ┌─────────────────────────────────────┐             │
│                         │  Routing Engine (.NET)              │             │
│                         │  • Select carrier (LCR + health)    │             │
│                         │  • Apply carrier-specific format    │             │
│                         │  • Submit to carrier API            │             │
│                         └──────────────────┬──────────────────┘             │
│                                            │                                 │
│                                            ▼                                 │
│  4. Carrier Submission                                                       │
│  ────────────────────                                                        │
│                         Telnyx API ◄── POST /v2/messages                    │
│                                │                                             │
│                                ▼                                             │
│  5. Sync Response                                                            │
│  ───────────────                                                             │
│                         ◄── 200 OK {carrier_message_id: "..."}              │
│                                │                                             │
│                                ▼                                             │
│  6. Update DocType & Respond                                                 │
│  ──────────────────────────                                                  │
│                         • Update TEL SMS Message status="sent"              │
│                         • Return to consumer: {message_id, status, cost}    │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  7. Async: Delivery Webhook (Later)                                          │
│  ─────────────────────────────────                                           │
│                                                                              │
│  Telnyx ──POST──► /api/method/dartwing_tel.webhook.telnyx_sms              │
│                         │                                                    │
│                         ▼                                                    │
│                  ┌─────────────────────────────────────┐                    │
│                  │  • Verify webhook signature          │                    │
│                  │  • Update TEL SMS Message status     │                    │
│                  │  • Publish event to RabbitMQ         │                    │
│                  └──────────────────┬──────────────────┘                    │
│                                     │                                        │
│                                     ▼                                        │
│                  Webhook Delivery Service ──POST──► Consumer webhook_url    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2 Voice Call Flow (Outbound PSTN)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OUTBOUND VOICE CALL FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. API Request                                                              │
│  ─────────────                                                               │
│  Consumer ──POST──► Frappe API (/api/method/dartwing_tel.api.make_call)     │
│                         │                                                    │
│                         ▼                                                    │
│  2. Create Call Record                                                       │
│  ────────────────────                                                        │
│                  ┌─────────────────────────────────────┐                    │
│                  │  • Validate API key & permissions   │                    │
│                  │  • Validate E.164 numbers           │                    │
│                  │  • Create TEL Call DocType          │                    │
│                  │  • Status: "initiating"             │                    │
│                  └──────────────────┬──────────────────┘                    │
│                                     │                                        │
│                                     │ gRPC                                   │
│                                     ▼                                        │
│  3. Voice Gateway Processing                                                 │
│  ──────────────────────────                                                  │
│                  ┌─────────────────────────────────────┐                    │
│                  │  Voice Gateway (.NET)               │                    │
│                  │  • Select carrier via Routing Engine│                    │
│                  │  • Build SIP INVITE                 │                    │
│                  │  • Set STIR/SHAKEN headers          │                    │
│                  │  • Configure caller ID              │                    │
│                  └──────────────────┬──────────────────┘                    │
│                                     │                                        │
│                                     │ SIP                                    │
│                                     ▼                                        │
│  4. Kamailio SBC                                                             │
│  ──────────────                                                              │
│                  ┌─────────────────────────────────────┐                    │
│                  │  Kamailio                           │                    │
│                  │  • Route to selected carrier trunk  │                    │
│                  │  • Handle NAT traversal             │                    │
│                  │  • Apply header manipulation        │                    │
│                  └──────────────────┬──────────────────┘                    │
│                                     │                                        │
│                                     │ SIP INVITE                             │
│                                     ▼                                        │
│  5. Carrier & PSTN                                                           │
│  ───────────────                                                             │
│                  Telnyx SIP ──► PSTN ──► Destination Phone                  │
│                                     │                                        │
│                                     │ SIP 180 Ringing                        │
│                                     ▼                                        │
│  6. Call Progress Events                                                     │
│  ─────────────────────                                                       │
│                  ┌─────────────────────────────────────┐                    │
│                  │  Voice Gateway receives:            │                    │
│                  │  • 180 Ringing → Update DocType     │                    │
│                  │  • 200 OK → Call answered           │                    │
│                  │  • BYE → Call completed             │                    │
│                  │                                     │                    │
│                  │  Each event:                        │                    │
│                  │  • Update TEL Call DocType          │                    │
│                  │  • Publish to RabbitMQ              │                    │
│                  │  • Push via Socket.IO (real-time)   │                    │
│                  └─────────────────────────────────────┘                    │
│                                                                              │
│  7. Post-Call Processing                                                     │
│  ─────────────────────                                                       │
│                  ┌─────────────────────────────────────┐                    │
│                  │  • Calculate duration & cost        │                    │
│                  │  • Store recording (if enabled)     │                    │
│                  │  • Create CDR entry                 │                    │
│                  │  • Deliver webhook to consumer      │                    │
│                  └─────────────────────────────────────┘                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3 WebRTC Call Flow (Flutter App to PSTN)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     WEBRTC TO PSTN CALL FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────┐                           ┌──────────────────┐           │
│  │  Flutter App  │                           │  Destination     │           │
│  │  (WebRTC)     │                           │  PSTN Phone      │           │
│  └───────┬───────┘                           └────────▲─────────┘           │
│          │                                            │                      │
│          │ 1. Socket.IO: initiate_call                │                      │
│          ▼                                            │                      │
│  ┌───────────────────────────────────────────────────┐│                      │
│  │              Voice Gateway (.NET)                 ││                      │
│  │                                                   ││                      │
│  │  2. Create TEL Call DocType                       ││                      │
│  │  3. Send SDP Offer to Flutter                     ││                      │
│  │  4. Receive SDP Answer                            ││                      │
│  │  5. Establish WebRTC connection                   ││                      │
│  │                                                   ││                      │
│  │  ┌─────────────────────────────────────────────┐ ││                      │
│  │  │         Media Bridge                        │ ││                      │
│  │  │                                             │ ││                      │
│  │  │   WebRTC (Opus) ◄──────────► SIP (G.711)   │ ││                      │
│  │  │        │                          │        │ ││                      │
│  │  │        │    Transcode + Bridge    │        │ ││                      │
│  │  │        │                          │        │ ││                      │
│  │  └────────┼──────────────────────────┼────────┘ ││                      │
│  │           │                          │          ││                      │
│  └───────────┼──────────────────────────┼──────────┘│                      │
│              │                          │           │                       │
│              │                          │ 6. SIP INVITE                     │
│              │                          ▼           │                       │
│  ┌───────────┼──────────────────────────────────────┼─────────────────────┐ │
│  │           │           Kamailio SBC               │                     │ │
│  │           │                                      │                     │ │
│  │           │  7. Route to Carrier                 │                     │ │
│  │           │                                      │                     │ │
│  └───────────┼──────────────────────────────────────┼─────────────────────┘ │
│              │                                      │                       │
│              │                          ┌───────────┘                       │
│              │                          ▼                                   │
│  ┌───────────┼──────────────────────────────────────┐                       │
│  │           │        Telnyx / Bandwidth            │                       │
│  │           │                                      │──────► PSTN ─────────┘
│  │           │  8. SIP to PSTN                      │                       │
│  │           │                                      │                       │
│  └───────────┼──────────────────────────────────────┘                       │
│              │                                                               │
│              │ WebRTC Media (Opus/SRTP)                                      │
│              │                                                               │
│  ┌───────────▼───────────────────────────────────────────────────────────┐  │
│  │                         TURN/STUN Servers                             │  │
│  │                                                                       │  │
│  │  • ICE negotiation                                                    │  │
│  │  • NAT traversal                                                      │  │
│  │  • Media relay (when direct P2P fails)                                │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.3 Service Boundaries

| Service                | Technology | Port | Responsibility                         | Scaling    |
| ---------------------- | ---------- | ---- | -------------------------------------- | ---------- |
| `dartwing_tel`         | Frappe     | 8000 | API gateway, DocTypes, business logic  | Horizontal |
| `tel-voice-gateway`    | .NET Core  | 5001 | SIP signaling, WebRTC, call control    | Horizontal |
| `tel-media-processor`  | .NET Core  | 5002 | Recording, transcoding, TTS/STT        | Horizontal |
| `tel-sms-router`       | .NET Core  | 5003 | SMS routing, carrier selection, SMPP   | Horizontal |
| `tel-fax-processor`    | .NET Core  | 5004 | T.38 handling, PDF conversion, OCR     | Horizontal |
| `tel-webhook-delivery` | .NET Core  | 5005 | Guaranteed webhook delivery with retry | Horizontal |
| `tel-routing-engine`   | .NET Core  | 5006 | Carrier selection, LCR, failover logic | Horizontal |
| `tel-cdr-indexer`      | .NET Core  | 5007 | CDR indexing to OpenSearch             | Horizontal |
| `kamailio`             | Kamailio   | 5060 | SIP proxy, load balancing, failover    | Cluster    |
| `rabbitmq`             | RabbitMQ   | 5672 | Message queue for async processing     | Cluster    |
| `redis`                | Redis      | 6379 | Rate limiting, session cache           | Sentinel   |

## 2.4 Data Flow Patterns

### Pattern A: Synchronous Request-Response

```
Consumer ──► Frappe API ──► Return response
                │
                └──► Create/Update DocType (async via background job)
```

Used for: Simple SMS send, number lookup, status queries

### Pattern B: Fire-and-Forget with Webhook

```
Consumer ──► Frappe API ──► Return {id, status: "queued"}
                │
                └──► RabbitMQ ──► Worker ──► Carrier
                                    │
                                    └──► Webhook to Consumer
```

Used for: Batch SMS, fax send, voice calls

### Pattern C: Real-Time Bidirectional

```
Consumer ◄──────────► Socket.IO ◄──────────► Voice Gateway
                                                   │
                                                   └──► Kamailio ──► Carrier
```

Used for: WebRTC calls, real-time call events, DTMF

### Pattern D: Event Sourcing for CDR

```
All Operations ──► RabbitMQ ──► CDR Indexer ──► OpenSearch
                                    │
                                    └──► MariaDB (TEL CDR DocType)
```

Used for: Call detail records, analytics, billing

---

# Section 3: Data Model

## 3.1 DocType Overview

DartwingTel defines the following Frappe DocTypes organized by function:

### Core Operational DocTypes

| DocType         | Module       | Purpose                   | Volume      |
| --------------- | ------------ | ------------------------- | ----------- |
| TEL DID         | dartwing_tel | Phone number inventory    | 100K+       |
| TEL Call        | dartwing_tel | Voice call records        | 10M+/month  |
| TEL SMS Message | dartwing_tel | SMS/MMS message records   | 50M+/month  |
| TEL Fax         | dartwing_tel | Fax transmission records  | 5M+/month   |
| TEL Recording   | dartwing_tel | Call/voicemail recordings | 1M+/month   |
| TEL Conference  | dartwing_tel | Conference call sessions  | 100K+/month |
| TEL Voicemail   | dartwing_tel | Voicemail messages        | 500K+/month |

### Configuration DocTypes

| DocType            | Module       | Purpose                          |
| ------------------ | ------------ | -------------------------------- |
| TEL API Key        | dartwing_tel | Module-level API credentials     |
| TEL Webhook Config | dartwing_tel | Webhook endpoint configurations  |
| TEL Number Pool    | dartwing_tel | Grouped numbers for routing      |
| TEL IVR Flow       | dartwing_tel | Interactive voice response flows |
| TEL Route Rule     | dartwing_tel | Custom routing rules             |
| TEL Campaign       | dartwing_tel | 10DLC campaign registrations     |
| TEL Sender ID      | dartwing_tel | Branded sender ID registrations  |

### Compliance DocTypes

| DocType            | Module       | Purpose                         |
| ------------------ | ------------ | ------------------------------- |
| TEL E911 Address   | dartwing_tel | Emergency service registrations |
| TEL DNC Entry      | dartwing_tel | Do Not Call list entries        |
| TEL Consent Record | dartwing_tel | TCPA consent tracking           |
| TEL Audit Log      | dartwing_tel | Compliance audit trail          |

### Analytics DocTypes

| DocType           | Module       | Purpose                           |
| ----------------- | ------------ | --------------------------------- |
| TEL CDR           | dartwing_tel | Call detail records (high volume) |
| TEL Usage Summary | dartwing_tel | Aggregated usage statistics       |
| TEL Cost Report   | dartwing_tel | Cost allocation reports           |

### Administrative DocTypes

| DocType            | Module       | Purpose                     |
| ------------------ | ------------ | --------------------------- |
| TEL Carrier Config | dartwing_tel | Carrier connection settings |
| TEL Rate Table     | dartwing_tel | Pricing by destination      |
| TEL Feature Flag   | dartwing_tel | Feature toggles per module  |
| TEL Port Request   | dartwing_tel | Number porting requests     |

## 3.2 Core DocType Definitions

### 3.2.1 TEL DID (Phone Number)

```json
{
  "doctype": "TEL DID",
  "module": "Dartwing Tel",
  "autoname": "field:phone_number",
  "fields": [
    {
      "fieldname": "phone_number",
      "label": "Phone Number",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1,
      "description": "E.164 format: +14155551234"
    },
    {
      "fieldname": "country_code",
      "label": "Country Code",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "number_type",
      "label": "Number Type",
      "fieldtype": "Select",
      "options": "Local\nToll-Free\nMobile\nShortcode",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Active\nPending\nSuspended\nReleased\nPorted Out",
      "default": "Pending",
      "in_list_view": 1
    },
    {
      "fieldname": "section_capabilities",
      "fieldtype": "Section Break",
      "label": "Capabilities"
    },
    {
      "fieldname": "sms_enabled",
      "label": "SMS Enabled",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "mms_enabled",
      "label": "MMS Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "voice_enabled",
      "label": "Voice Enabled",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "fax_enabled",
      "label": "Fax Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_routing",
      "fieldtype": "Section Break",
      "label": "Routing Configuration"
    },
    {
      "fieldname": "assigned_module",
      "label": "Assigned Module",
      "fieldtype": "Data",
      "description": "dartwing_va, dartwing_fax, etc."
    },
    {
      "fieldname": "assigned_organization",
      "label": "Assigned Organization",
      "fieldtype": "Link",
      "options": "Organization"
    },
    {
      "fieldname": "inbound_voice_route",
      "label": "Inbound Voice Route",
      "fieldtype": "Select",
      "options": "Webhook\nSIP Endpoint\nIVR Flow\nVoicemail\nForward",
      "default": "Webhook"
    },
    {
      "fieldname": "inbound_sms_route",
      "label": "Inbound SMS Route",
      "fieldtype": "Select",
      "options": "Webhook\nAuto-Reply\nForward",
      "default": "Webhook"
    },
    {
      "fieldname": "webhook_url",
      "label": "Webhook URL",
      "fieldtype": "Data",
      "depends_on": "eval:doc.inbound_voice_route=='Webhook' || doc.inbound_sms_route=='Webhook'"
    },
    {
      "fieldname": "forward_to",
      "label": "Forward To",
      "fieldtype": "Data",
      "depends_on": "eval:doc.inbound_voice_route=='Forward' || doc.inbound_sms_route=='Forward'",
      "description": "E.164 phone number"
    },
    {
      "fieldname": "ivr_flow",
      "label": "IVR Flow",
      "fieldtype": "Link",
      "options": "TEL IVR Flow",
      "depends_on": "eval:doc.inbound_voice_route=='IVR Flow'"
    },
    {
      "fieldname": "section_e911",
      "fieldtype": "Section Break",
      "label": "E911 Configuration"
    },
    {
      "fieldname": "e911_enabled",
      "label": "E911 Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "e911_address",
      "label": "E911 Address",
      "fieldtype": "Link",
      "options": "TEL E911 Address",
      "depends_on": "eval:doc.e911_enabled"
    },
    {
      "fieldname": "section_cnam",
      "fieldtype": "Section Break",
      "label": "Caller ID (CNAM)"
    },
    {
      "fieldname": "cnam_display_name",
      "label": "CNAM Display Name",
      "fieldtype": "Data",
      "max_length": 15,
      "description": "Max 15 characters for caller ID"
    },
    {
      "fieldname": "section_carrier",
      "fieldtype": "Section Break",
      "label": "Carrier Information"
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Telnyx\nBandwidth\nSinch\nDIDWW",
      "read_only": 1
    },
    {
      "fieldname": "carrier_number_id",
      "label": "Carrier Number ID",
      "fieldtype": "Data",
      "read_only": 1
    },
    {
      "fieldname": "monthly_cost",
      "label": "Monthly Cost",
      "fieldtype": "Currency",
      "read_only": 1
    },
    {
      "fieldname": "section_metadata",
      "fieldtype": "Section Break",
      "label": "Metadata"
    },
    {
      "fieldname": "provisioned_at",
      "label": "Provisioned At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "released_at",
      "label": "Released At",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "tags",
      "label": "Tags",
      "fieldtype": "Table MultiSelect",
      "options": "TEL Number Tag"
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Dartwing Tel User",
      "read": 1,
      "write": 0,
      "create": 0,
      "delete": 0
    }
  ],
  "track_changes": 1,
  "index_web_pages_for_search": 0
}
```

### 3.2.2 TEL Call

```json
{
  "doctype": "TEL Call",
  "module": "Dartwing Tel",
  "autoname": "naming_series:",
  "naming_series": "CALL-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "CALL-.YYYY.-.#####",
      "default": "CALL-.YYYY.-.#####",
      "hidden": 1
    },
    {
      "fieldname": "direction",
      "label": "Direction",
      "fieldtype": "Select",
      "options": "Outbound\nInbound",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Initiating\nRinging\nIn Progress\nCompleted\nFailed\nBusy\nNo Answer\nCanceled",
      "default": "Initiating",
      "in_list_view": 1
    },
    {
      "fieldname": "from_number",
      "label": "From",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "to_number",
      "label": "To",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "caller_id_name",
      "label": "Caller ID Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_timing",
      "fieldtype": "Section Break",
      "label": "Timing"
    },
    {
      "fieldname": "initiated_at",
      "label": "Initiated At",
      "fieldtype": "Datetime",
      "reqd": 1
    },
    {
      "fieldname": "answered_at",
      "label": "Answered At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "ended_at",
      "label": "Ended At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "billable_seconds",
      "label": "Billable (seconds)",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "section_quality",
      "fieldtype": "Section Break",
      "label": "Quality Metrics"
    },
    {
      "fieldname": "mos_score",
      "label": "MOS Score",
      "fieldtype": "Float",
      "description": "Mean Opinion Score (1.0-5.0)"
    },
    {
      "fieldname": "jitter_ms",
      "label": "Jitter (ms)",
      "fieldtype": "Float"
    },
    {
      "fieldname": "packet_loss_percent",
      "label": "Packet Loss (%)",
      "fieldtype": "Float"
    },
    {
      "fieldname": "section_recording",
      "fieldtype": "Section Break",
      "label": "Recording"
    },
    {
      "fieldname": "recording_enabled",
      "label": "Recording Enabled",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "recording",
      "label": "Recording",
      "fieldtype": "Link",
      "options": "TEL Recording",
      "depends_on": "eval:doc.recording_enabled"
    },
    {
      "fieldname": "section_carrier",
      "fieldtype": "Section Break",
      "label": "Carrier Information"
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Telnyx\nBandwidth\nSinch\nDIDWW"
    },
    {
      "fieldname": "carrier_call_id",
      "label": "Carrier Call ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "sip_call_id",
      "label": "SIP Call-ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_cost",
      "fieldtype": "Section Break",
      "label": "Cost"
    },
    {
      "fieldname": "cost_amount",
      "label": "Cost",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "cost_currency",
      "label": "Currency",
      "fieldtype": "Select",
      "options": "USD\nEUR\nGBP",
      "default": "USD"
    },
    {
      "fieldname": "cost_center",
      "label": "Cost Center",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_context",
      "fieldtype": "Section Break",
      "label": "Context"
    },
    {
      "fieldname": "api_key",
      "label": "API Key",
      "fieldtype": "Link",
      "options": "TEL API Key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data",
      "description": "dartwing_va, dartwing_fax, etc."
    },
    {
      "fieldname": "context_json",
      "label": "Context",
      "fieldtype": "JSON",
      "description": "Arbitrary context from calling module"
    },
    {
      "fieldname": "section_failure",
      "fieldtype": "Section Break",
      "label": "Failure Information",
      "depends_on": "eval:doc.status=='Failed'"
    },
    {
      "fieldname": "hangup_cause",
      "label": "Hangup Cause",
      "fieldtype": "Data"
    },
    {
      "fieldname": "sip_response_code",
      "label": "SIP Response Code",
      "fieldtype": "Int"
    },
    {
      "fieldname": "error_message",
      "label": "Error Message",
      "fieldtype": "Small Text"
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Dartwing Tel User",
      "read": 1,
      "write": 0,
      "create": 0,
      "delete": 0
    }
  ],
  "track_changes": 1,
  "sort_field": "initiated_at",
  "sort_order": "DESC"
}
```

### 3.2.3 TEL SMS Message

```json
{
  "doctype": "TEL SMS Message",
  "module": "Dartwing Tel",
  "autoname": "naming_series:",
  "naming_series": "SMS-.YYYY.-.######",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "SMS-.YYYY.-.######",
      "default": "SMS-.YYYY.-.######",
      "hidden": 1
    },
    {
      "fieldname": "direction",
      "label": "Direction",
      "fieldtype": "Select",
      "options": "Outbound\nInbound",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Queued\nSent\nDelivered\nFailed\nUndelivered\nReceived",
      "default": "Queued",
      "in_list_view": 1
    },
    {
      "fieldname": "from_number",
      "label": "From",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "to_number",
      "label": "To",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "body",
      "label": "Body",
      "fieldtype": "Text",
      "reqd": 1
    },
    {
      "fieldname": "section_encoding",
      "fieldtype": "Section Break",
      "label": "Encoding"
    },
    {
      "fieldname": "encoding",
      "label": "Encoding",
      "fieldtype": "Select",
      "options": "GSM-7\nUCS-2",
      "default": "GSM-7"
    },
    {
      "fieldname": "segments",
      "label": "Segments",
      "fieldtype": "Int",
      "default": 1,
      "description": "Number of SMS segments"
    },
    {
      "fieldname": "character_count",
      "label": "Characters",
      "fieldtype": "Int"
    },
    {
      "fieldname": "section_mms",
      "fieldtype": "Section Break",
      "label": "MMS Media",
      "depends_on": "eval:doc.is_mms"
    },
    {
      "fieldname": "is_mms",
      "label": "Is MMS",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "media_urls",
      "label": "Media URLs",
      "fieldtype": "JSON",
      "depends_on": "eval:doc.is_mms"
    },
    {
      "fieldname": "section_timing",
      "fieldtype": "Section Break",
      "label": "Timing"
    },
    {
      "fieldname": "created_at",
      "label": "Created At",
      "fieldtype": "Datetime",
      "default": "Now"
    },
    {
      "fieldname": "sent_at",
      "label": "Sent At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "delivered_at",
      "label": "Delivered At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "scheduled_for",
      "label": "Scheduled For",
      "fieldtype": "Datetime",
      "description": "If set, message will be sent at this time"
    },
    {
      "fieldname": "section_carrier",
      "fieldtype": "Section Break",
      "label": "Carrier Information"
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Telnyx\nBandwidth\nSinch\nDIDWW"
    },
    {
      "fieldname": "carrier_message_id",
      "label": "Carrier Message ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_cost",
      "fieldtype": "Section Break",
      "label": "Cost"
    },
    {
      "fieldname": "cost_amount",
      "label": "Cost",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "cost_currency",
      "label": "Currency",
      "fieldtype": "Select",
      "options": "USD\nEUR\nGBP",
      "default": "USD"
    },
    {
      "fieldname": "cost_center",
      "label": "Cost Center",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_context",
      "fieldtype": "Section Break",
      "label": "Context"
    },
    {
      "fieldname": "api_key",
      "label": "API Key",
      "fieldtype": "Link",
      "options": "TEL API Key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data"
    },
    {
      "fieldname": "context_json",
      "label": "Context",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "idempotency_key",
      "label": "Idempotency Key",
      "fieldtype": "Data",
      "unique": 1
    },
    {
      "fieldname": "section_compliance",
      "fieldtype": "Section Break",
      "label": "Compliance"
    },
    {
      "fieldname": "campaign",
      "label": "10DLC Campaign",
      "fieldtype": "Link",
      "options": "TEL Campaign"
    },
    {
      "fieldname": "hipaa_mode",
      "label": "HIPAA Mode",
      "fieldtype": "Check",
      "default": 0,
      "description": "If enabled, body is encrypted at rest"
    },
    {
      "fieldname": "section_failure",
      "fieldtype": "Section Break",
      "label": "Failure Information",
      "depends_on": "eval:['Failed','Undelivered'].includes(doc.status)"
    },
    {
      "fieldname": "error_code",
      "label": "Error Code",
      "fieldtype": "Data"
    },
    {
      "fieldname": "error_message",
      "label": "Error Message",
      "fieldtype": "Small Text"
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Dartwing Tel User",
      "read": 1,
      "write": 0,
      "create": 0,
      "delete": 0
    }
  ],
  "track_changes": 1,
  "sort_field": "created_at",
  "sort_order": "DESC"
}
```

### 3.2.4 TEL Fax

```json
{
  "doctype": "TEL Fax",
  "module": "Dartwing Tel",
  "autoname": "naming_series:",
  "naming_series": "FAX-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "FAX-.YYYY.-.#####",
      "hidden": 1
    },
    {
      "fieldname": "direction",
      "label": "Direction",
      "fieldtype": "Select",
      "options": "Outbound\nInbound",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Queued\nSending\nDelivered\nFailed\nPartial\nReceived",
      "default": "Queued",
      "in_list_view": 1
    },
    {
      "fieldname": "from_number",
      "label": "From",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "to_number",
      "label": "To",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "section_document",
      "fieldtype": "Section Break",
      "label": "Document"
    },
    {
      "fieldname": "document_file",
      "label": "Document",
      "fieldtype": "Attach",
      "description": "PDF file to send"
    },
    {
      "fieldname": "page_count",
      "label": "Page Count",
      "fieldtype": "Int"
    },
    {
      "fieldname": "pages_sent",
      "label": "Pages Sent",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "cover_page_enabled",
      "label": "Include Cover Page",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "cover_page_template",
      "label": "Cover Page Template",
      "fieldtype": "Select",
      "options": "Standard\nMinimal\nMedical\nLegal",
      "depends_on": "eval:doc.cover_page_enabled"
    },
    {
      "fieldname": "section_t38",
      "fieldtype": "Section Break",
      "label": "T.38 Information"
    },
    {
      "fieldname": "t38_used",
      "label": "T.38 Used",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "remote_station_id",
      "label": "Remote Station ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "transfer_rate",
      "label": "Transfer Rate (bps)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "section_timing",
      "fieldtype": "Section Break",
      "label": "Timing"
    },
    {
      "fieldname": "created_at",
      "label": "Created At",
      "fieldtype": "Datetime",
      "default": "Now"
    },
    {
      "fieldname": "started_at",
      "label": "Started At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "completed_at",
      "label": "Completed At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "section_carrier",
      "fieldtype": "Section Break",
      "label": "Carrier Information"
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Telnyx\nBandwidth"
    },
    {
      "fieldname": "carrier_fax_id",
      "label": "Carrier Fax ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_cost",
      "fieldtype": "Section Break",
      "label": "Cost"
    },
    {
      "fieldname": "cost_amount",
      "label": "Cost",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "cost_per_page",
      "label": "Cost Per Page",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "section_context",
      "fieldtype": "Section Break",
      "label": "Context"
    },
    {
      "fieldname": "api_key",
      "label": "API Key",
      "fieldtype": "Link",
      "options": "TEL API Key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data"
    },
    {
      "fieldname": "context_json",
      "label": "Context",
      "fieldtype": "JSON"
    },
    {
      "fieldname": "hipaa_mode",
      "label": "HIPAA Mode",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_failure",
      "fieldtype": "Section Break",
      "label": "Failure Information",
      "depends_on": "eval:['Failed','Partial'].includes(doc.status)"
    },
    {
      "fieldname": "error_code",
      "label": "Error Code",
      "fieldtype": "Data"
    },
    {
      "fieldname": "error_message",
      "label": "Error Message",
      "fieldtype": "Small Text"
    },
    {
      "fieldname": "retry_count",
      "label": "Retry Count",
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Dartwing Tel User",
      "read": 1,
      "write": 0,
      "create": 0,
      "delete": 0
    }
  ],
  "track_changes": 1,
  "sort_field": "created_at",
  "sort_order": "DESC"
}
```

### 3.2.5 TEL API Key

```json
{
  "doctype": "TEL API Key",
  "module": "Dartwing Tel",
  "autoname": "field:key_prefix",
  "fields": [
    {
      "fieldname": "key_prefix",
      "label": "Key Prefix",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1,
      "description": "First 8 chars of key: tel_xxxx",
      "in_list_view": 1
    },
    {
      "fieldname": "key_hash",
      "label": "Key Hash",
      "fieldtype": "Password",
      "reqd": 1,
      "description": "SHA-256 hash of full key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data",
      "reqd": 1,
      "in_list_view": 1,
      "description": "dartwing_va, dartwing_fax, etc."
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Active\nSuspended\nRevoked",
      "default": "Active",
      "in_list_view": 1
    },
    {
      "fieldname": "section_permissions",
      "fieldtype": "Section Break",
      "label": "Permissions"
    },
    {
      "fieldname": "permissions",
      "label": "Permissions",
      "fieldtype": "JSON",
      "description": "{sms: {send: true, receive: true}, voice: {...}}"
    },
    {
      "fieldname": "section_limits",
      "fieldtype": "Section Break",
      "label": "Rate Limits"
    },
    {
      "fieldname": "rate_limits",
      "label": "Rate Limits",
      "fieldtype": "JSON",
      "description": "{sms: {per_second: 10, per_day: 10000}, ...}"
    },
    {
      "fieldname": "section_webhook",
      "fieldtype": "Section Break",
      "label": "Webhook Configuration"
    },
    {
      "fieldname": "webhook_url",
      "label": "Webhook URL",
      "fieldtype": "Data"
    },
    {
      "fieldname": "webhook_secret",
      "label": "Webhook Secret",
      "fieldtype": "Password"
    },
    {
      "fieldname": "section_security",
      "fieldtype": "Section Break",
      "label": "Security"
    },
    {
      "fieldname": "ip_whitelist",
      "label": "IP Whitelist",
      "fieldtype": "JSON",
      "description": "[\"10.0.0.0/8\", \"192.168.1.100\"]"
    },
    {
      "fieldname": "last_used_at",
      "label": "Last Used",
      "fieldtype": "Datetime",
      "read_only": 1
    },
    {
      "fieldname": "created_at",
      "label": "Created At",
      "fieldtype": "Datetime",
      "default": "Now",
      "read_only": 1
    },
    {
      "fieldname": "section_cost",
      "fieldtype": "Section Break",
      "label": "Cost Allocation"
    },
    {
      "fieldname": "cost_center",
      "label": "Cost Center",
      "fieldtype": "Data"
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    }
  ],
  "track_changes": 1
}
```

### 3.2.6 TEL Recording

```json
{
  "doctype": "TEL Recording",
  "module": "Dartwing Tel",
  "autoname": "naming_series:",
  "naming_series": "REC-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "REC-.YYYY.-.#####",
      "hidden": 1
    },
    {
      "fieldname": "recording_type",
      "label": "Type",
      "fieldtype": "Select",
      "options": "Call\nVoicemail\nConference\nIVR",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Recording\nProcessing\nCompleted\nFailed\nDeleted",
      "default": "Recording",
      "in_list_view": 1
    },
    {
      "fieldname": "call",
      "label": "Call",
      "fieldtype": "Link",
      "options": "TEL Call",
      "depends_on": "eval:doc.recording_type=='Call'"
    },
    {
      "fieldname": "conference",
      "label": "Conference",
      "fieldtype": "Link",
      "options": "TEL Conference",
      "depends_on": "eval:doc.recording_type=='Conference'"
    },
    {
      "fieldname": "section_file",
      "fieldtype": "Section Break",
      "label": "Recording File"
    },
    {
      "fieldname": "file_url",
      "label": "File URL",
      "fieldtype": "Data",
      "description": "S3/GCS URL"
    },
    {
      "fieldname": "file_format",
      "label": "Format",
      "fieldtype": "Select",
      "options": "mp3\nwav\nogg",
      "default": "mp3"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "file_size_bytes",
      "label": "File Size (bytes)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "channels",
      "label": "Channels",
      "fieldtype": "Select",
      "options": "mono\nstereo\ndual",
      "default": "mono",
      "description": "dual = separate tracks for each party"
    },
    {
      "fieldname": "section_transcription",
      "fieldtype": "Section Break",
      "label": "Transcription"
    },
    {
      "fieldname": "transcription_status",
      "label": "Transcription Status",
      "fieldtype": "Select",
      "options": "None\nPending\nCompleted\nFailed",
      "default": "None"
    },
    {
      "fieldname": "transcription_text",
      "label": "Transcription",
      "fieldtype": "Long Text"
    },
    {
      "fieldname": "transcription_json",
      "label": "Transcription JSON",
      "fieldtype": "JSON",
      "description": "Word-level timestamps and speaker diarization"
    },
    {
      "fieldname": "transcription_provider",
      "label": "Transcription Provider",
      "fieldtype": "Select",
      "options": "Deepgram\nWhisper\nGoogle\nAWS"
    },
    {
      "fieldname": "section_security",
      "fieldtype": "Section Break",
      "label": "Security"
    },
    {
      "fieldname": "encrypted",
      "label": "Encrypted",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "encryption_key_id",
      "label": "Encryption Key ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "retention_days",
      "label": "Retention (days)",
      "fieldtype": "Int",
      "default": 90
    },
    {
      "fieldname": "delete_after",
      "label": "Delete After",
      "fieldtype": "Date"
    },
    {
      "fieldname": "hipaa_mode",
      "label": "HIPAA Mode",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "section_context",
      "fieldtype": "Section Break",
      "label": "Context"
    },
    {
      "fieldname": "api_key",
      "label": "API Key",
      "fieldtype": "Link",
      "options": "TEL API Key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data"
    },
    {
      "fieldname": "created_at",
      "label": "Created At",
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 0,
      "delete": 0
    }
  ],
  "track_changes": 1
}
```

### 3.2.7 TEL E911 Address

```json
{
  "doctype": "TEL E911 Address",
  "module": "Dartwing Tel",
  "autoname": "naming_series:",
  "naming_series": "E911-.#####",
  "fields": [
    {
      "fieldname": "naming_series",
      "label": "Series",
      "fieldtype": "Select",
      "options": "E911-.#####",
      "hidden": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Pending Validation\nValidated\nFailed\nActive\nExpired",
      "default": "Pending Validation",
      "in_list_view": 1
    },
    {
      "fieldname": "section_address",
      "fieldtype": "Section Break",
      "label": "Address"
    },
    {
      "fieldname": "street_address",
      "label": "Street Address",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "street_address_2",
      "label": "Street Address 2",
      "fieldtype": "Data"
    },
    {
      "fieldname": "city",
      "label": "City",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "state",
      "label": "State/Province",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "postal_code",
      "label": "Postal Code",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "country",
      "label": "Country",
      "fieldtype": "Link",
      "options": "Country",
      "reqd": 1
    },
    {
      "fieldname": "section_caller",
      "fieldtype": "Section Break",
      "label": "Caller Information"
    },
    {
      "fieldname": "caller_name",
      "label": "Caller Name",
      "fieldtype": "Data",
      "reqd": 1,
      "description": "Name provided to 911 dispatcher"
    },
    {
      "fieldname": "callback_number",
      "label": "Callback Number",
      "fieldtype": "Data",
      "reqd": 1,
      "description": "E.164 format"
    },
    {
      "fieldname": "section_validation",
      "fieldtype": "Section Break",
      "label": "Validation"
    },
    {
      "fieldname": "validated_at",
      "label": "Validated At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "validation_provider",
      "label": "Validation Provider",
      "fieldtype": "Select",
      "options": "Bandwidth\nIntrado\nWest"
    },
    {
      "fieldname": "psap_id",
      "label": "PSAP ID",
      "fieldtype": "Data",
      "description": "Public Safety Answering Point"
    },
    {
      "fieldname": "section_carrier",
      "fieldtype": "Section Break",
      "label": "Carrier"
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Bandwidth\nTelnyx"
    },
    {
      "fieldname": "carrier_address_id",
      "label": "Carrier Address ID",
      "fieldtype": "Data"
    },
    {
      "fieldname": "section_assignment",
      "fieldtype": "Section Break",
      "label": "Assignment"
    },
    {
      "fieldname": "assigned_did",
      "label": "Assigned DID",
      "fieldtype": "Link",
      "options": "TEL DID"
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization"
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
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    }
  ],
  "track_changes": 1
}
```

### 3.2.8 TEL CDR (Call Detail Record)

```json
{
  "doctype": "TEL CDR",
  "module": "Dartwing Tel",
  "autoname": "hash",
  "fields": [
    {
      "fieldname": "cdr_type",
      "label": "Type",
      "fieldtype": "Select",
      "options": "Call\nSMS\nFax",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "record_id",
      "label": "Record ID",
      "fieldtype": "Data",
      "reqd": 1,
      "description": "Reference to TEL Call, TEL SMS Message, or TEL Fax"
    },
    {
      "fieldname": "direction",
      "label": "Direction",
      "fieldtype": "Select",
      "options": "Outbound\nInbound",
      "reqd": 1
    },
    {
      "fieldname": "from_number",
      "label": "From",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "to_number",
      "label": "To",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "initiated_at",
      "label": "Initiated At",
      "fieldtype": "Datetime",
      "reqd": 1
    },
    {
      "fieldname": "ended_at",
      "label": "Ended At",
      "fieldtype": "Datetime"
    },
    {
      "fieldname": "duration_seconds",
      "label": "Duration (seconds)",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "billable_seconds",
      "label": "Billable (seconds)",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "Completed\nFailed\nBusy\nNo Answer\nCanceled\nDelivered\nUndelivered",
      "reqd": 1
    },
    {
      "fieldname": "carrier",
      "label": "Carrier",
      "fieldtype": "Select",
      "options": "Telnyx\nBandwidth\nSinch\nDIDWW"
    },
    {
      "fieldname": "cost_amount",
      "label": "Cost",
      "fieldtype": "Currency"
    },
    {
      "fieldname": "cost_currency",
      "label": "Currency",
      "fieldtype": "Select",
      "options": "USD\nEUR\nGBP",
      "default": "USD"
    },
    {
      "fieldname": "api_key",
      "label": "API Key",
      "fieldtype": "Link",
      "options": "TEL API Key"
    },
    {
      "fieldname": "module",
      "label": "Module",
      "fieldtype": "Data"
    },
    {
      "fieldname": "organization",
      "label": "Organization",
      "fieldtype": "Link",
      "options": "Organization"
    },
    {
      "fieldname": "cost_center",
      "label": "Cost Center",
      "fieldtype": "Data"
    },
    {
      "fieldname": "country_code",
      "label": "Country Code",
      "fieldtype": "Data"
    },
    {
      "fieldname": "carrier_record_id",
      "label": "Carrier Record ID",
      "fieldtype": "Data"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 0,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Dartwing Tel Admin",
      "read": 1,
      "write": 0,
      "create": 0,
      "delete": 0
    }
  ],
  "sort_field": "initiated_at",
  "sort_order": "DESC"
}
```

## 3.3 Database Optimizations

### 3.3.1 High-Volume Table Partitioning

For TEL CDR and TEL SMS Message tables (50M+ records/month), use MariaDB partitioning:

```sql
-- Partition TEL CDR by month
ALTER TABLE `tabTEL CDR`
PARTITION BY RANGE (TO_DAYS(initiated_at)) (
    PARTITION p_2026_01 VALUES LESS THAN (TO_DAYS('2026-02-01')),
    PARTITION p_2026_02 VALUES LESS THAN (TO_DAYS('2026-03-01')),
    PARTITION p_2026_03 VALUES LESS THAN (TO_DAYS('2026-04-01')),
    -- Add partitions monthly via scheduled job
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Indexes for common queries
CREATE INDEX idx_cdr_api_key_time ON `tabTEL CDR` (api_key, initiated_at);
CREATE INDEX idx_cdr_from_number ON `tabTEL CDR` (from_number, initiated_at);
CREATE INDEX idx_cdr_to_number ON `tabTEL CDR` (to_number, initiated_at);
CREATE INDEX idx_cdr_carrier ON `tabTEL CDR` (carrier, initiated_at);
CREATE INDEX idx_cdr_status ON `tabTEL CDR` (status, initiated_at);
```

### 3.3.2 Active Call State (In-Memory)

For real-time call state, use a separate in-memory table:

```sql
CREATE TABLE tel_active_calls (
    call_id VARCHAR(255) PRIMARY KEY,
    sip_call_id VARCHAR(255),
    status VARCHAR(50),
    from_number VARCHAR(50),
    to_number VARCHAR(50),
    carrier VARCHAR(50),
    started_at DATETIME(3),
    last_updated DATETIME(3),
    metadata JSON,
    INDEX idx_sip_call_id (sip_call_id),
    INDEX idx_status (status)
) ENGINE=MEMORY;
```

### 3.3.3 OpenSearch Indexing

CDRs are also indexed to OpenSearch for fast analytics queries:

```json
{
  "index": "tel_cdr",
  "mappings": {
    "properties": {
      "cdr_type": { "type": "keyword" },
      "direction": { "type": "keyword" },
      "from_number": { "type": "keyword" },
      "to_number": { "type": "keyword" },
      "initiated_at": { "type": "date" },
      "duration_seconds": { "type": "integer" },
      "status": { "type": "keyword" },
      "carrier": { "type": "keyword" },
      "cost_amount": { "type": "float" },
      "api_key": { "type": "keyword" },
      "module": { "type": "keyword" },
      "organization": { "type": "keyword" },
      "country_code": { "type": "keyword" }
    }
  },
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 1
  }
}
```

## 3.4 DocType Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DOCTYPE RELATIONSHIP DIAGRAM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                          ┌─────────────────┐                                │
│                          │  Organization   │ (from dartwing_core)           │
│                          │                 │                                │
│                          └────────┬────────┘                                │
│                                   │                                          │
│                    ┌──────────────┼──────────────┐                          │
│                    │              │              │                          │
│                    ▼              ▼              ▼                          │
│            ┌───────────┐  ┌───────────┐  ┌───────────────┐                  │
│            │  TEL DID  │  │TEL API Key│  │TEL E911 Address│                 │
│            │           │  │           │  │               │                  │
│            └─────┬─────┘  └─────┬─────┘  └───────────────┘                  │
│                  │              │                                            │
│     ┌────────────┼──────────────┼────────────┐                              │
│     │            │              │            │                              │
│     ▼            ▼              ▼            ▼                              │
│ ┌────────┐  ┌─────────┐  ┌───────────┐  ┌────────┐                         │
│ │TEL Call│  │TEL SMS  │  │  TEL Fax  │  │TEL CDR │                         │
│ │        │  │ Message │  │           │  │        │                         │
│ └────┬───┘  └─────────┘  └───────────┘  └────────┘                         │
│      │                                                                       │
│      │                                                                       │
│      ▼                                                                       │
│ ┌────────────┐   ┌──────────────┐                                           │
│ │TEL Recording│  │TEL Conference │                                          │
│ │            │   │              │                                           │
│ └────────────┘   └──────────────┘                                           │
│                                                                              │
│ Configuration Layer:                                                         │
│ ┌────────────┐  ┌───────────────┐  ┌────────────┐  ┌───────────────┐       │
│ │TEL Webhook │  │TEL Number Pool│  │TEL IVR Flow│  │TEL Route Rule │       │
│ │   Config   │  │               │  │            │  │               │       │
│ └────────────┘  └───────────────┘  └────────────┘  └───────────────┘       │
│                                                                              │
│ Compliance Layer:                                                            │
│ ┌────────────┐  ┌───────────────┐  ┌─────────────┐  ┌──────────────┐       │
│ │TEL Campaign│  │TEL Consent Rec│  │TEL DNC Entry│  │TEL Audit Log │       │
│ │  (10DLC)   │  │               │  │             │  │              │       │
│ └────────────┘  └───────────────┘  └─────────────┘  └──────────────┘       │
│                                                                              │
│ Admin Layer:                                                                 │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│ │TEL Carrier   │  │TEL Rate Table│  │TEL Port Req  │                       │
│ │   Config     │  │              │  │              │                       │
│ └──────────────┘  └──────────────┘  └──────────────┘                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# Section 4: Service Architecture

## 4.1 Frappe Module Structure

The `dartwing_tel` Frappe app follows standard Frappe conventions with additional organization for the telephony domain:

```
dartwing_tel/
├── dartwing_tel/
│   ├── __init__.py
│   ├── hooks.py                    # Frappe hooks
│   ├── patches/                    # Database migrations
│   │
│   ├── api/                        # Whitelisted API methods
│   │   ├── __init__.py
│   │   ├── sms.py                  # SMS endpoints
│   │   ├── voice.py                # Voice endpoints
│   │   ├── fax.py                  # Fax endpoints
│   │   ├── numbers.py              # Number management
│   │   ├── emergency.py            # E911/NG911
│   │   ├── analytics.py            # CDR and reports
│   │   └── admin.py                # Admin operations
│   │
│   ├── doctype/                    # DocType definitions
│   │   ├── tel_did/
│   │   ├── tel_call/
│   │   ├── tel_sms_message/
│   │   ├── tel_fax/
│   │   ├── tel_recording/
│   │   ├── tel_api_key/
│   │   ├── tel_e911_address/
│   │   ├── tel_cdr/
│   │   ├── tel_webhook_config/
│   │   ├── tel_campaign/
│   │   └── ... (other doctypes)
│   │
│   ├── services/                   # Business logic services
│   │   ├── __init__.py
│   │   ├── routing_service.py      # Carrier selection logic
│   │   ├── compliance_service.py   # TCPA, DNC, 10DLC checks
│   │   ├── rate_limiter.py         # Rate limiting logic
│   │   ├── cost_calculator.py      # Cost calculation
│   │   └── webhook_service.py      # Webhook management
│   │
│   ├── carriers/                   # Carrier adapters
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract carrier interface
│   │   ├── telnyx.py               # Telnyx adapter
│   │   ├── bandwidth.py            # Bandwidth adapter
│   │   ├── sinch.py                # Sinch adapter
│   │   └── didww.py                # DIDWW adapter
│   │
│   ├── grpc/                       # gRPC client for .NET services
│   │   ├── __init__.py
│   │   ├── protos/                 # Protocol buffer definitions
│   │   │   ├── tel_services.proto
│   │   │   └── tel_services_pb2.py
│   │   └── client.py               # gRPC client wrapper
│   │
│   ├── webhooks/                   # Inbound webhook handlers
│   │   ├── __init__.py
│   │   ├── telnyx_webhook.py
│   │   ├── bandwidth_webhook.py
│   │   └── sinch_webhook.py
│   │
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       ├── phone_utils.py          # E.164 validation, formatting
│       ├── webhook_signer.py       # HMAC signing
│       └── encryption.py           # PHI encryption
│
├── setup.py
└── requirements.txt
```

## 4.2 Frappe Hooks Configuration

```python
# dartwing_tel/hooks.py

app_name = "dartwing_tel"
app_title = "Dartwing Tel"
app_publisher = "Dartwing"
app_description = "Carrier-grade telephony backbone for Dartwing"
app_version = "1.0.0"

# Document events
doc_events = {
    "TEL Call": {
        "on_update": "dartwing_tel.events.call_events.on_call_update",
        "after_insert": "dartwing_tel.events.call_events.on_call_insert"
    },
    "TEL SMS Message": {
        "on_update": "dartwing_tel.events.sms_events.on_sms_update",
        "after_insert": "dartwing_tel.events.sms_events.on_sms_insert"
    },
    "TEL Fax": {
        "on_update": "dartwing_tel.events.fax_events.on_fax_update",
        "after_insert": "dartwing_tel.events.fax_events.on_fax_insert"
    },
    "TEL DID": {
        "on_update": "dartwing_tel.events.did_events.on_did_update"
    }
}

# Scheduled tasks
scheduler_events = {
    "cron": {
        # Process scheduled SMS every minute
        "* * * * *": [
            "dartwing_tel.tasks.process_scheduled_sms"
        ],
        # Check carrier health every 5 minutes
        "*/5 * * * *": [
            "dartwing_tel.tasks.check_carrier_health"
        ],
        # Update number reputation hourly
        "0 * * * *": [
            "dartwing_tel.tasks.update_number_reputation"
        ],
        # Generate CDR summaries daily at 2 AM
        "0 2 * * *": [
            "dartwing_tel.tasks.generate_cdr_summaries"
        ],
        # Cleanup expired recordings daily at 3 AM
        "0 3 * * *": [
            "dartwing_tel.tasks.cleanup_expired_recordings"
        ],
        # Add CDR partitions monthly
        "0 0 1 * *": [
            "dartwing_tel.tasks.add_cdr_partitions"
        ]
    }
}

# Permission query conditions
permission_query_conditions = {
    "TEL Call": "dartwing_tel.permissions.get_call_permission_query",
    "TEL SMS Message": "dartwing_tel.permissions.get_sms_permission_query",
    "TEL Fax": "dartwing_tel.permissions.get_fax_permission_query",
    "TEL DID": "dartwing_tel.permissions.get_did_permission_query",
    "TEL Recording": "dartwing_tel.permissions.get_recording_permission_query"
}

# Website routes for webhooks
website_route_rules = [
    {"from_route": "/api/tel/webhook/telnyx/<path:event_type>", "to_route": "dartwing_tel.webhooks.telnyx_webhook.handle"},
    {"from_route": "/api/tel/webhook/bandwidth/<path:event_type>", "to_route": "dartwing_tel.webhooks.bandwidth_webhook.handle"},
    {"from_route": "/api/tel/webhook/sinch/<path:event_type>", "to_route": "dartwing_tel.webhooks.sinch_webhook.handle"}
]

# Fixtures
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["Dartwing Tel Admin", "Dartwing Tel User"]]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Dartwing Tel"]]}
]
```

## 4.3 API Layer Implementation

### 4.3.1 SMS API Example

```python
# dartwing_tel/api/sms.py

import frappe
from frappe import _
from dartwing_tel.services.routing_service import RoutingService
from dartwing_tel.services.compliance_service import ComplianceService
from dartwing_tel.services.rate_limiter import RateLimiter
from dartwing_tel.utils.phone_utils import validate_e164, format_e164
from dartwing_tel.grpc.client import TelGrpcClient
import json


def get_api_key_from_request():
    """Extract and validate API key from Authorization header."""
    auth_header = frappe.request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer tel_"):
        frappe.throw(_("Invalid API key format"), frappe.AuthenticationError)

    key = auth_header.replace("Bearer ", "")
    key_prefix = key[:12]  # tel_xxxxxxxx

    api_key_doc = frappe.get_value(
        "TEL API Key",
        {"key_prefix": key_prefix, "status": "Active"},
        ["name", "key_hash", "module", "permissions", "rate_limits", "organization"],
        as_dict=True
    )

    if not api_key_doc:
        frappe.throw(_("Invalid or inactive API key"), frappe.AuthenticationError)

    # Verify hash
    import hashlib
    provided_hash = hashlib.sha256(key.encode()).hexdigest()
    if provided_hash != api_key_doc.key_hash:
        frappe.throw(_("Invalid API key"), frappe.AuthenticationError)

    return api_key_doc


def require_api_key(func):
    """Decorator to require valid API key."""
    def wrapper(*args, **kwargs):
        api_key = get_api_key_from_request()
        frappe.local.tel_api_key = api_key
        return func(*args, **kwargs)
    return wrapper


@frappe.whitelist(allow_guest=True, methods=["POST"])
@require_api_key
def send_sms(
    to: str,
    body: str,
    from_number: str = None,
    sender_id: str = None,
    status_callback: str = None,
    scheduled_for: str = None,
    tags: list = None,
    context: dict = None,
    idempotency_key: str = None,
    hipaa_mode: bool = False
):
    """
    Send an SMS message.

    Args:
        to: Destination phone number (E.164 format)
        body: Message content
        from_number: Source phone number (optional, auto-selected if not provided)
        sender_id: Alphanumeric sender ID (where supported)
        status_callback: URL for delivery status webhooks
        scheduled_for: ISO datetime for scheduled send
        tags: List of tags for tracking
        context: Arbitrary context data
        idempotency_key: Unique key for idempotent requests
        hipaa_mode: Enable HIPAA-compliant mode (encrypted at rest)

    Returns:
        dict: {message_id, status, segments, cost}
    """
    api_key = frappe.local.tel_api_key

    # Check permissions
    permissions = json.loads(api_key.permissions or "{}")
    if not permissions.get("sms", {}).get("send", False):
        frappe.throw(_("API key does not have SMS send permission"), frappe.PermissionError)

    # Check idempotency
    if idempotency_key:
        existing = frappe.get_value("TEL SMS Message", {"idempotency_key": idempotency_key})
        if existing:
            doc = frappe.get_doc("TEL SMS Message", existing)
            return {
                "message_id": doc.name,
                "status": doc.status,
                "segments": doc.segments,
                "cost": {"amount": doc.cost_amount, "currency": doc.cost_currency}
            }

    # Rate limiting
    rate_limiter = RateLimiter()
    rate_limits = json.loads(api_key.rate_limits or "{}")
    sms_limits = rate_limits.get("sms", {"per_second": 10, "per_day": 10000})

    if not rate_limiter.check(f"tel:sms:{api_key.name}", sms_limits):
        frappe.throw(_("Rate limit exceeded"), frappe.RateLimitExceededError)

    # Validate phone numbers
    to = format_e164(to)
    if not validate_e164(to):
        frappe.throw(_("Invalid destination phone number"), frappe.ValidationError)

    # Auto-select from number if not provided
    if not from_number:
        from_number = RoutingService.select_outbound_number(
            api_key.name,
            destination=to,
            capability="sms"
        )
    else:
        from_number = format_e164(from_number)
        if not validate_e164(from_number):
            frappe.throw(_("Invalid source phone number"), frappe.ValidationError)

    # Compliance checks
    compliance = ComplianceService()
    compliance.check_tcpa(to, api_key.name)  # Raises if blocked
    compliance.check_dnc(to, api_key.organization)  # Raises if on DNC

    # Calculate segments
    encoding, segments, char_count = calculate_sms_encoding(body)

    # Create SMS Message record
    sms_doc = frappe.new_doc("TEL SMS Message")
    sms_doc.direction = "Outbound"
    sms_doc.status = "Queued"
    sms_doc.from_number = from_number
    sms_doc.to_number = to
    sms_doc.body = body
    sms_doc.encoding = encoding
    sms_doc.segments = segments
    sms_doc.character_count = char_count
    sms_doc.api_key = api_key.name
    sms_doc.module = api_key.module
    sms_doc.idempotency_key = idempotency_key
    sms_doc.hipaa_mode = hipaa_mode
    sms_doc.scheduled_for = scheduled_for
    sms_doc.context_json = json.dumps(context or {})

    if status_callback:
        sms_doc.webhook_url = status_callback

    sms_doc.insert(ignore_permissions=True)

    # If scheduled, return immediately
    if scheduled_for:
        return {
            "message_id": sms_doc.name,
            "status": "scheduled",
            "scheduled_for": scheduled_for,
            "segments": segments
        }

    # Route to carrier via gRPC
    grpc_client = TelGrpcClient()
    try:
        result = grpc_client.route_sms(
            message_id=sms_doc.name,
            from_number=from_number,
            to_number=to,
            body=body,
            encoding=encoding
        )

        # Update with carrier info
        sms_doc.db_set("carrier", result.carrier)
        sms_doc.db_set("carrier_message_id", result.carrier_message_id)
        sms_doc.db_set("status", "Sent")
        sms_doc.db_set("sent_at", frappe.utils.now_datetime())
        sms_doc.db_set("cost_amount", result.cost)

        return {
            "message_id": sms_doc.name,
            "status": "sent",
            "segments": segments,
            "cost": {"amount": result.cost, "currency": "USD"}
        }

    except Exception as e:
        sms_doc.db_set("status", "Failed")
        sms_doc.db_set("error_message", str(e))
        frappe.throw(str(e))


def calculate_sms_encoding(body: str) -> tuple:
    """Calculate SMS encoding and segment count."""
    # Check for non-GSM-7 characters
    gsm7_chars = set(
        '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ !"#¤%&\'()*+,-./0123456789:;<=>?'
        '¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà'
    )

    is_unicode = any(c not in gsm7_chars for c in body)
    char_count = len(body)

    if is_unicode:
        encoding = "UCS-2"
        if char_count <= 70:
            segments = 1
        else:
            segments = (char_count + 66) // 67  # 67 chars per segment for concatenated
    else:
        encoding = "GSM-7"
        if char_count <= 160:
            segments = 1
        else:
            segments = (char_count + 152) // 153  # 153 chars per segment for concatenated

    return encoding, segments, char_count


@frappe.whitelist(allow_guest=True, methods=["GET"])
@require_api_key
def get_sms_status(message_id: str):
    """
    Get SMS delivery status.

    Args:
        message_id: The SMS message ID

    Returns:
        dict: {message_id, status, delivered_at, error_code, error_message}
    """
    api_key = frappe.local.tel_api_key

    sms = frappe.get_doc("TEL SMS Message", message_id)

    # Verify ownership
    if sms.api_key != api_key.name:
        frappe.throw(_("Access denied"), frappe.PermissionError)

    return {
        "message_id": sms.name,
        "status": sms.status,
        "sent_at": sms.sent_at,
        "delivered_at": sms.delivered_at,
        "segments": sms.segments,
        "cost": {"amount": sms.cost_amount, "currency": sms.cost_currency},
        "error_code": sms.error_code,
        "error_message": sms.error_message
    }
```

### 4.3.2 Voice API Example

```python
# dartwing_tel/api/voice.py

import frappe
from frappe import _
from dartwing_tel.api.sms import require_api_key, get_api_key_from_request
from dartwing_tel.grpc.client import TelGrpcClient
from dartwing_tel.services.routing_service import RoutingService
from dartwing_tel.utils.phone_utils import validate_e164, format_e164
import json


@frappe.whitelist(allow_guest=True, methods=["POST"])
@require_api_key
def make_call(
    to: str,
    from_number: str = None,
    caller_id_name: str = None,
    timeout_seconds: int = 60,
    recording_enabled: bool = False,
    machine_detection: bool = False,
    audio_url: str = None,
    tts_text: str = None,
    tts_voice: str = "en-US-Neural2-J",
    webhook_url: str = None,
    context: dict = None
):
    """
    Initiate an outbound voice call.

    Args:
        to: Destination phone number (E.164)
        from_number: Caller ID number (E.164, auto-selected if not provided)
        caller_id_name: CNAM display name
        timeout_seconds: Ring timeout
        recording_enabled: Enable call recording
        machine_detection: Enable answering machine detection
        audio_url: URL of audio file to play
        tts_text: Text-to-speech content
        tts_voice: TTS voice identifier
        webhook_url: URL for call status webhooks
        context: Arbitrary context data

    Returns:
        dict: {call_id, status, from_number, to_number}
    """
    api_key = frappe.local.tel_api_key

    # Check permissions
    permissions = json.loads(api_key.permissions or "{}")
    if not permissions.get("voice", {}).get("call", False):
        frappe.throw(_("API key does not have voice call permission"), frappe.PermissionError)

    # Validate destination
    to = format_e164(to)
    if not validate_e164(to):
        frappe.throw(_("Invalid destination phone number"), frappe.ValidationError)

    # Auto-select from number if not provided
    if not from_number:
        from_number = RoutingService.select_outbound_number(
            api_key.name,
            destination=to,
            capability="voice"
        )
    else:
        from_number = format_e164(from_number)

    # Create call record
    call_doc = frappe.new_doc("TEL Call")
    call_doc.direction = "Outbound"
    call_doc.status = "Initiating"
    call_doc.from_number = from_number
    call_doc.to_number = to
    call_doc.caller_id_name = caller_id_name
    call_doc.initiated_at = frappe.utils.now_datetime()
    call_doc.recording_enabled = recording_enabled
    call_doc.api_key = api_key.name
    call_doc.module = api_key.module
    call_doc.context_json = json.dumps(context or {})
    call_doc.insert(ignore_permissions=True)

    # Initiate via gRPC to Voice Gateway
    grpc_client = TelGrpcClient()
    try:
        result = grpc_client.initiate_call(
            call_id=call_doc.name,
            from_number=from_number,
            to_number=to,
            caller_id_name=caller_id_name,
            timeout_seconds=timeout_seconds,
            recording_enabled=recording_enabled,
            machine_detection=machine_detection,
            audio_url=audio_url,
            tts_text=tts_text,
            tts_voice=tts_voice
        )

        # Update with carrier info
        call_doc.db_set("carrier", result.carrier)
        call_doc.db_set("carrier_call_id", result.carrier_call_id)
        call_doc.db_set("sip_call_id", result.sip_call_id)
        call_doc.db_set("status", "Ringing")

        return {
            "call_id": call_doc.name,
            "status": "ringing",
            "from_number": from_number,
            "to_number": to,
            "carrier": result.carrier
        }

    except Exception as e:
        call_doc.db_set("status", "Failed")
        call_doc.db_set("error_message", str(e))
        frappe.throw(str(e))


@frappe.whitelist(allow_guest=True, methods=["POST"])
@require_api_key
def hangup_call(call_id: str, reason: str = None):
    """Terminate an active call."""
    api_key = frappe.local.tel_api_key

    call = frappe.get_doc("TEL Call", call_id)
    if call.api_key != api_key.name:
        frappe.throw(_("Access denied"), frappe.PermissionError)

    if call.status not in ["Initiating", "Ringing", "In Progress"]:
        frappe.throw(_("Call is not active"))

    grpc_client = TelGrpcClient()
    grpc_client.hangup_call(
        call_id=call_id,
        sip_call_id=call.sip_call_id,
        reason=reason
    )

    return {"call_id": call_id, "status": "terminating"}


@frappe.whitelist(allow_guest=True, methods=["POST"])
@require_api_key
def start_recording(call_id: str, channels: str = "mono"):
    """Start recording an active call."""
    api_key = frappe.local.tel_api_key

    permissions = json.loads(api_key.permissions or "{}")
    if not permissions.get("voice", {}).get("record", False):
        frappe.throw(_("API key does not have recording permission"), frappe.PermissionError)

    call = frappe.get_doc("TEL Call", call_id)
    if call.api_key != api_key.name:
        frappe.throw(_("Access denied"), frappe.PermissionError)

    if call.status != "In Progress":
        frappe.throw(_("Call must be in progress to start recording"))

    # Create recording record
    recording_doc = frappe.new_doc("TEL Recording")
    recording_doc.recording_type = "Call"
    recording_doc.status = "Recording"
    recording_doc.call = call_id
    recording_doc.channels = channels
    recording_doc.api_key = api_key.name
    recording_doc.module = api_key.module
    recording_doc.insert(ignore_permissions=True)

    # Start recording via gRPC
    grpc_client = TelGrpcClient()
    grpc_client.start_recording(
        call_id=call_id,
        recording_id=recording_doc.name,
        channels=channels
    )

    # Update call
    call.db_set("recording_enabled", 1)
    call.db_set("recording", recording_doc.name)

    return {"recording_id": recording_doc.name, "status": "recording"}
```

## 4.4 .NET Microservices Architecture

### 4.4.1 Solution Structure

```
DartwingTel/
├── src/
│   ├── Dartwing.Tel.Common/               # Shared DTOs, interfaces
│   │   ├── Models/
│   │   │   ├── CallRequest.cs
│   │   │   ├── SmsRequest.cs
│   │   │   ├── FaxRequest.cs
│   │   │   └── CarrierResponse.cs
│   │   ├── Interfaces/
│   │   │   ├── ICarrierAdapter.cs
│   │   │   ├── IRoutingEngine.cs
│   │   │   └── IMessageQueue.cs
│   │   └── Extensions/
│   │
│   ├── Dartwing.Tel.Carriers/             # Carrier adapters
│   │   ├── Abstractions/
│   │   │   └── CarrierAdapterBase.cs
│   │   ├── Telnyx/
│   │   │   ├── TelnyxAdapter.cs
│   │   │   └── TelnyxModels.cs
│   │   ├── Bandwidth/
│   │   │   ├── BandwidthAdapter.cs
│   │   │   └── BandwidthModels.cs
│   │   ├── Sinch/
│   │   └── DIDWW/
│   │
│   ├── Dartwing.Tel.VoiceGateway/         # Voice service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── VoiceGatewayService.cs
│   │   │   ├── SipService.cs
│   │   │   ├── WebRtcService.cs
│   │   │   └── RecordingService.cs
│   │   ├── Hubs/
│   │   │   └── CallSignalingHub.cs
│   │   └── Workers/
│   │       └── CallEventWorker.cs
│   │
│   ├── Dartwing.Tel.SmsRouter/            # SMS service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── SmsRouterService.cs
│   │   │   └── SmppService.cs
│   │   └── Workers/
│   │       └── SmsStatusWorker.cs
│   │
│   ├── Dartwing.Tel.FaxProcessor/         # Fax service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── FaxProcessorService.cs
│   │   │   ├── PdfService.cs
│   │   │   └── T38Service.cs
│   │   └── Workers/
│   │       └── FaxStatusWorker.cs
│   │
│   ├── Dartwing.Tel.WebhookDelivery/      # Webhook service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   └── WebhookDeliveryService.cs
│   │   └── Workers/
│   │       └── WebhookWorker.cs
│   │
│   ├── Dartwing.Tel.RoutingEngine/        # Routing service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── RoutingEngineService.cs
│   │   │   ├── LcrService.cs
│   │   │   └── HealthMonitorService.cs
│   │   └── Workers/
│   │       └── HealthCheckWorker.cs
│   │
│   ├── Dartwing.Tel.MediaProcessor/       # Media service
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── TranscriptionService.cs
│   │   │   ├── TtsService.cs
│   │   │   └── StorageService.cs
│   │   └── Workers/
│   │       └── TranscriptionWorker.cs
│   │
│   └── Dartwing.Tel.Protos/               # gRPC definitions
│       ├── tel_services.proto
│       ├── voice.proto
│       ├── sms.proto
│       └── fax.proto
│
├── tests/
│   ├── Dartwing.Tel.VoiceGateway.Tests/
│   ├── Dartwing.Tel.SmsRouter.Tests/
│   └── Dartwing.Tel.Integration.Tests/
│
└── DartwingTel.sln
```

### 4.4.2 gRPC Service Definitions

```protobuf
// Dartwing.Tel.Protos/tel_services.proto

syntax = "proto3";

package dartwing.tel;

option csharp_namespace = "Dartwing.Tel.Protos";

// SMS Routing Service
service SmsRouter {
    rpc RouteSms(RouteSmsRequest) returns (RouteSmsResponse);
    rpc GetSmsStatus(GetSmsStatusRequest) returns (GetSmsStatusResponse);
}

message RouteSmsRequest {
    string message_id = 1;
    string from_number = 2;
    string to_number = 3;
    string body = 4;
    string encoding = 5;
    string preferred_carrier = 6;
    bool hipaa_mode = 7;
}

message RouteSmsResponse {
    string carrier = 1;
    string carrier_message_id = 2;
    string status = 3;
    double cost = 4;
}

// Voice Gateway Service
service VoiceGateway {
    rpc InitiateCall(InitiateCallRequest) returns (InitiateCallResponse);
    rpc HangupCall(HangupCallRequest) returns (HangupCallResponse);
    rpc TransferCall(TransferCallRequest) returns (TransferCallResponse);
    rpc StartRecording(StartRecordingRequest) returns (StartRecordingResponse);
    rpc StopRecording(StopRecordingRequest) returns (StopRecordingResponse);
    rpc PlayAudio(PlayAudioRequest) returns (PlayAudioResponse);
    rpc StreamCallEvents(StreamCallEventsRequest) returns (stream CallEvent);
}

message InitiateCallRequest {
    string call_id = 1;
    string from_number = 2;
    string to_number = 3;
    string caller_id_name = 4;
    int32 timeout_seconds = 5;
    bool recording_enabled = 6;
    bool machine_detection = 7;
    string audio_url = 8;
    string tts_text = 9;
    string tts_voice = 10;
}

message InitiateCallResponse {
    string carrier = 1;
    string carrier_call_id = 2;
    string sip_call_id = 3;
    string status = 4;
}

message CallEvent {
    string call_id = 1;
    string event_type = 2;  // initiated, ringing, answered, completed, failed
    string timestamp = 3;
    map<string, string> data = 4;
}

// Fax Processor Service
service FaxProcessor {
    rpc SendFax(SendFaxRequest) returns (SendFaxResponse);
    rpc GetFaxStatus(GetFaxStatusRequest) returns (GetFaxStatusResponse);
    rpc CancelFax(CancelFaxRequest) returns (CancelFaxResponse);
}

message SendFaxRequest {
    string fax_id = 1;
    string from_number = 2;
    string to_number = 3;
    string document_url = 4;
    bool cover_page_enabled = 5;
    string cover_page_template = 6;
    bool hipaa_mode = 7;
}

message SendFaxResponse {
    string carrier = 1;
    string carrier_fax_id = 2;
    int32 page_count = 3;
    int32 estimated_duration_seconds = 4;
}

// Routing Engine Service
service RoutingEngine {
    rpc SelectCarrier(SelectCarrierRequest) returns (SelectCarrierResponse);
    rpc GetCarrierHealth(GetCarrierHealthRequest) returns (GetCarrierHealthResponse);
    rpc ReportCarrierIssue(ReportCarrierIssueRequest) returns (ReportCarrierIssueResponse);
}

message SelectCarrierRequest {
    string operation_type = 1;  // sms, voice, fax
    string destination = 2;
    string preferred_carrier = 3;
    bool allow_fallback = 4;
}

message SelectCarrierResponse {
    string carrier = 1;
    double estimated_cost = 2;
    int32 health_score = 3;
}
```

### 4.4.3 SMS Router Service Implementation

```csharp
// Dartwing.Tel.SmsRouter/Services/SmsRouterService.cs

using Dartwing.Tel.Carriers;
using Dartwing.Tel.Common.Interfaces;
using Dartwing.Tel.Protos;
using Grpc.Core;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;

namespace Dartwing.Tel.SmsRouter.Services;

public class SmsRouterService : Protos.SmsRouter.SmsRouterBase
{
    private readonly ILogger<SmsRouterService> _logger;
    private readonly IRoutingEngine _routingEngine;
    private readonly ICarrierAdapterFactory _carrierFactory;
    private readonly IConnection _rabbitConnection;

    public SmsRouterService(
        ILogger<SmsRouterService> logger,
        IRoutingEngine routingEngine,
        ICarrierAdapterFactory carrierFactory,
        IConnection rabbitConnection)
    {
        _logger = logger;
        _routingEngine = routingEngine;
        _carrierFactory = carrierFactory;
        _rabbitConnection = rabbitConnection;
    }

    public override async Task<RouteSmsResponse> RouteSms(
        RouteSmsRequest request,
        ServerCallContext context)
    {
        _logger.LogInformation(
            "Routing SMS {MessageId} from {From} to {To}",
            request.MessageId, request.FromNumber, request.ToNumber);

        // Select optimal carrier
        var carrierSelection = await _routingEngine.SelectCarrierAsync(
            operationType: "sms",
            destination: request.ToNumber,
            preferredCarrier: request.PreferredCarrier);

        var carrier = _carrierFactory.GetAdapter(carrierSelection.Carrier);

        try
        {
            // Send via selected carrier
            var result = await carrier.SendSmsAsync(new SmsRequest
            {
                MessageId = request.MessageId,
                From = request.FromNumber,
                To = request.ToNumber,
                Body = request.Body,
                Encoding = request.Encoding
            });

            // Publish success event
            await PublishSmsEventAsync(new SmsStatusEvent
            {
                MessageId = request.MessageId,
                Status = "sent",
                Carrier = carrierSelection.Carrier,
                CarrierMessageId = result.CarrierMessageId,
                Cost = result.Cost,
                Timestamp = DateTime.UtcNow
            });

            return new RouteSmsResponse
            {
                Carrier = carrierSelection.Carrier,
                CarrierMessageId = result.CarrierMessageId,
                Status = "sent",
                Cost = result.Cost
            };
        }
        catch (CarrierException ex) when (ex.IsRetryable)
        {
            _logger.LogWarning(
                ex, "Carrier {Carrier} failed, attempting failover for {MessageId}",
                carrierSelection.Carrier, request.MessageId);

            // Report issue and try fallback
            await _routingEngine.ReportCarrierIssueAsync(
                carrierSelection.Carrier, "sms", ex.ErrorCode);

            return await RouteWithFallbackAsync(request, carrierSelection.Carrier);
        }
    }

    private async Task<RouteSmsResponse> RouteWithFallbackAsync(
        RouteSmsRequest request,
        string failedCarrier)
    {
        var fallbackSelection = await _routingEngine.SelectCarrierAsync(
            operationType: "sms",
            destination: request.ToNumber,
            excludeCarriers: new[] { failedCarrier });

        var carrier = _carrierFactory.GetAdapter(fallbackSelection.Carrier);

        var result = await carrier.SendSmsAsync(new SmsRequest
        {
            MessageId = request.MessageId,
            From = request.FromNumber,
            To = request.ToNumber,
            Body = request.Body,
            Encoding = request.Encoding
        });

        await PublishSmsEventAsync(new SmsStatusEvent
        {
            MessageId = request.MessageId,
            Status = "sent",
            Carrier = fallbackSelection.Carrier,
            CarrierMessageId = result.CarrierMessageId,
            Cost = result.Cost,
            Timestamp = DateTime.UtcNow,
            FailoverFrom = failedCarrier
        });

        return new RouteSmsResponse
        {
            Carrier = fallbackSelection.Carrier,
            CarrierMessageId = result.CarrierMessageId,
            Status = "sent",
            Cost = result.Cost
        };
    }

    private async Task PublishSmsEventAsync(SmsStatusEvent evt)
    {
        using var channel = _rabbitConnection.CreateModel();
        var body = System.Text.Json.JsonSerializer.SerializeToUtf8Bytes(evt);

        channel.BasicPublish(
            exchange: "tel.events",
            routingKey: "sms.status",
            body: body);
    }
}
```

### 4.4.4 Carrier Adapter Interface

```csharp
// Dartwing.Tel.Common/Interfaces/ICarrierAdapter.cs

namespace Dartwing.Tel.Common.Interfaces;

public interface ICarrierAdapter
{
    string CarrierName { get; }

    // SMS
    Task<SmsResult> SendSmsAsync(SmsRequest request);
    Task<SmsStatusResult> GetSmsStatusAsync(string carrierMessageId);

    // Voice
    Task<CallResult> InitiateCallAsync(CallRequest request);
    Task HangupCallAsync(string carrierCallId, string reason);
    Task<CallStatusResult> GetCallStatusAsync(string carrierCallId);

    // Fax
    Task<FaxResult> SendFaxAsync(FaxRequest request);
    Task<FaxStatusResult> GetFaxStatusAsync(string carrierFaxId);
    Task CancelFaxAsync(string carrierFaxId);

    // Numbers
    Task<IEnumerable<AvailableNumber>> SearchNumbersAsync(NumberSearchRequest request);
    Task<ProvisionedNumber> ProvisionNumberAsync(string phoneNumber);
    Task ReleaseNumberAsync(string phoneNumber);

    // Health
    Task<HealthStatus> GetHealthStatusAsync();
}

public record SmsRequest(
    string MessageId,
    string From,
    string To,
    string Body,
    string Encoding,
    string? CallbackUrl = null);

public record SmsResult(
    string CarrierMessageId,
    string Status,
    double Cost);

public record CallRequest(
    string CallId,
    string From,
    string To,
    string? CallerIdName,
    int TimeoutSeconds,
    bool RecordingEnabled,
    string? AudioUrl,
    string? TtsText,
    string? TtsVoice);

public record CallResult(
    string CarrierCallId,
    string SipCallId,
    string Status);
```

### 4.4.5 Telnyx Carrier Adapter

```csharp
// Dartwing.Tel.Carriers/Telnyx/TelnyxAdapter.cs

using System.Net.Http.Json;
using Dartwing.Tel.Common.Interfaces;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Dartwing.Tel.Carriers.Telnyx;

public class TelnyxAdapter : ICarrierAdapter
{
    public string CarrierName => "Telnyx";

    private readonly HttpClient _httpClient;
    private readonly ILogger<TelnyxAdapter> _logger;
    private readonly TelnyxOptions _options;

    public TelnyxAdapter(
        HttpClient httpClient,
        ILogger<TelnyxAdapter> logger,
        IOptions<TelnyxOptions> options)
    {
        _httpClient = httpClient;
        _logger = logger;
        _options = options.Value;

        _httpClient.BaseAddress = new Uri("https://api.telnyx.com/v2/");
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_options.ApiKey}");
    }

    public async Task<SmsResult> SendSmsAsync(SmsRequest request)
    {
        var telnyxRequest = new TelnyxSmsRequest
        {
            From = request.From,
            To = request.To,
            Text = request.Body,
            MessagingProfileId = _options.MessagingProfileId,
            WebhookUrl = request.CallbackUrl ?? _options.DefaultWebhookUrl
        };

        var response = await _httpClient.PostAsJsonAsync("messages", telnyxRequest);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<TelnyxSmsResponse>();

        return new SmsResult(
            CarrierMessageId: result!.Data.Id,
            Status: MapStatus(result.Data.To[0].Status),
            Cost: result.Data.Cost?.Amount ?? 0);
    }

    public async Task<CallResult> InitiateCallAsync(CallRequest request)
    {
        var telnyxRequest = new TelnyxCallRequest
        {
            ConnectionId = _options.SipConnectionId,
            From = request.From,
            To = request.To,
            FromDisplayName = request.CallerIdName,
            TimeoutSecs = request.TimeoutSeconds,
            WebhookUrl = _options.VoiceWebhookUrl,
            Record = request.RecordingEnabled ? "record-from-answer" : null
        };

        if (!string.IsNullOrEmpty(request.AudioUrl))
        {
            telnyxRequest.AudioUrl = request.AudioUrl;
        }

        var response = await _httpClient.PostAsJsonAsync("calls", telnyxRequest);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<TelnyxCallResponse>();

        return new CallResult(
            CarrierCallId: result!.Data.CallControlId,
            SipCallId: result.Data.CallSessionId,
            Status: "initiated");
    }

    public async Task<FaxResult> SendFaxAsync(FaxRequest request)
    {
        var telnyxRequest = new TelnyxFaxRequest
        {
            ConnectionId = _options.FaxConnectionId,
            From = request.From,
            To = request.To,
            MediaUrl = request.DocumentUrl,
            Quality = "high",
            StoreMedia = true,
            WebhookUrl = _options.FaxWebhookUrl
        };

        var response = await _httpClient.PostAsJsonAsync("faxes", telnyxRequest);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<TelnyxFaxResponse>();

        return new FaxResult(
            CarrierFaxId: result!.Data.Id,
            PageCount: result.Data.PageCount,
            Status: "queued");
    }

    public async Task<HealthStatus> GetHealthStatusAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("health");
            return new HealthStatus(
                IsHealthy: response.IsSuccessStatusCode,
                Latency: (int)response.Headers.Age?.TotalMilliseconds ?? 0,
                LastChecked: DateTime.UtcNow);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Telnyx health check failed");
            return new HealthStatus(
                IsHealthy: false,
                Latency: -1,
                LastChecked: DateTime.UtcNow,
                Error: ex.Message);
        }
    }

    private static string MapStatus(string telnyxStatus) => telnyxStatus switch
    {
        "queued" => "Queued",
        "sending" => "Sent",
        "sent" => "Sent",
        "delivered" => "Delivered",
        "delivery_failed" => "Failed",
        _ => telnyxStatus
    };
}
```

---

# Section 5: Carrier Integration Layer

## 5.1 Carrier Abstraction Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CARRIER INTEGRATION ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        Routing Engine                                 │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   LCR       │  │   Health    │  │  Failover   │  │    Cost     │ │   │
│  │  │  Engine     │  │  Monitor    │  │   Manager   │  │ Calculator  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────────┬───────────────────────────────────┘   │
│                                      │                                       │
│                              Carrier Selection                               │
│                                      │                                       │
│         ┌───────────────┬────────────┼────────────┬───────────────┐         │
│         │               │            │            │               │         │
│         ▼               ▼            ▼            ▼               ▼         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Telnyx    │ │  Bandwidth  │ │    Sinch    │ │    DIDWW    │           │
│  │   Adapter   │ │   Adapter   │ │   Adapter   │ │   Adapter   │           │
│  │             │ │             │ │             │ │             │           │
│  │ • SMS ✓     │ │ • SMS ✓     │ │ • SMS ✓     │ │ • Voice ✓   │           │
│  │ • Voice ✓   │ │ • Voice ✓   │ │ • Voice ✓   │ │ • Numbers ✓ │           │
│  │ • Fax ✓     │ │ • E911 ✓    │ │             │ │             │           │
│  │ • Numbers ✓ │ │ • Numbers ✓ │ │             │ │             │           │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
│         │               │               │               │                   │
│         └───────────────┴───────────────┴───────────────┘                   │
│                                │                                             │
│                          SIP / REST                                          │
│                                │                                             │
│  ┌─────────────────────────────▼─────────────────────────────────────────┐  │
│  │                     Kamailio SBC (SIP Traffic)                        │  │
│  │                                                                       │  │
│  │  • SIP Proxy & Load Balancing    • NAT Traversal (STUN/TURN)        │  │
│  │  • TLS/SRTP Termination          • Header Manipulation               │  │
│  │  • Topology Hiding               • Rate Limiting                     │  │
│  │  • Failover & Health Checks      • SIP-I/SIP-T Translation          │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 5.2 Routing Engine Implementation

```csharp
// Dartwing.Tel.RoutingEngine/Services/RoutingEngineService.cs

using Dartwing.Tel.Common.Interfaces;
using Dartwing.Tel.Protos;
using Grpc.Core;
using Microsoft.Extensions.Caching.Distributed;

namespace Dartwing.Tel.RoutingEngine.Services;

public class RoutingEngineService : Protos.RoutingEngine.RoutingEngineBase
{
    private readonly IDistributedCache _cache;
    private readonly ICarrierHealthService _healthService;
    private readonly IRateTableService _rateService;
    private readonly ILogger<RoutingEngineService> _logger;

    // Carrier capabilities matrix
    private static readonly Dictionary<string, CarrierCapabilities> CarrierMatrix = new()
    {
        ["Telnyx"] = new CarrierCapabilities
        {
            Sms = true, Voice = true, Fax = true, Numbers = true,
            SupportedCountries = new[] { "US", "CA", "GB", "AU", "DE", "FR" },
            Priority = 1
        },
        ["Bandwidth"] = new CarrierCapabilities
        {
            Sms = true, Voice = true, Fax = false, Numbers = true, E911 = true,
            SupportedCountries = new[] { "US", "CA" },
            Priority = 2
        },
        ["Sinch"] = new CarrierCapabilities
        {
            Sms = true, Voice = true, Fax = false, Numbers = false,
            SupportedCountries = new[] { "US", "CA", "GB", "AU", "DE", "FR", "ES", "IT" },
            Priority = 3
        },
        ["DIDWW"] = new CarrierCapabilities
        {
            Sms = false, Voice = true, Fax = false, Numbers = true,
            SupportedCountries = new[] { "US", "CA", "GB", "DE", "FR", "ES", "IT", "NL", "BE" },
            Priority = 4
        }
    };

    public override async Task<SelectCarrierResponse> SelectCarrier(
        SelectCarrierRequest request,
        ServerCallContext context)
    {
        var countryCode = ExtractCountryCode(request.Destination);

        // Get eligible carriers for this operation and destination
        var eligibleCarriers = CarrierMatrix
            .Where(c => IsCapable(c.Value, request.OperationType))
            .Where(c => c.Value.SupportedCountries.Contains(countryCode))
            .ToList();

        if (!eligibleCarriers.Any())
        {
            throw new RpcException(new Status(
                StatusCode.NotFound,
                $"No carrier available for {request.OperationType} to {countryCode}"));
        }

        // Get health scores
        var healthScores = await _healthService.GetHealthScoresAsync(
            eligibleCarriers.Select(c => c.Key));

        // Get costs
        var costs = await _rateService.GetRatesAsync(
            eligibleCarriers.Select(c => c.Key),
            request.OperationType,
            countryCode);

        // Apply LCR algorithm with health weighting
        var selected = eligibleCarriers
            .Select(c => new
            {
                Carrier = c.Key,
                Score = CalculateScore(
                    c.Value.Priority,
                    healthScores.GetValueOrDefault(c.Key, 0),
                    costs.GetValueOrDefault(c.Key, decimal.MaxValue))
            })
            .OrderByDescending(c => c.Score)
            .First();

        // If preferred carrier specified and healthy, use it
        if (!string.IsNullOrEmpty(request.PreferredCarrier))
        {
            var preferredHealth = healthScores.GetValueOrDefault(request.PreferredCarrier, 0);
            if (preferredHealth >= 80) // Healthy threshold
            {
                return new SelectCarrierResponse
                {
                    Carrier = request.PreferredCarrier,
                    EstimatedCost = (double)costs.GetValueOrDefault(request.PreferredCarrier, 0),
                    HealthScore = preferredHealth
                };
            }
        }

        return new SelectCarrierResponse
        {
            Carrier = selected.Carrier,
            EstimatedCost = (double)costs.GetValueOrDefault(selected.Carrier, 0),
            HealthScore = healthScores.GetValueOrDefault(selected.Carrier, 0)
        };
    }

    private static double CalculateScore(int priority, int health, decimal cost)
    {
        // Weighted scoring: 40% health, 40% cost, 20% priority
        var healthScore = health / 100.0 * 40;
        var costScore = Math.Max(0, 40 - (double)cost * 1000); // Lower cost = higher score
        var priorityScore = (5 - priority) / 4.0 * 20;

        return healthScore + costScore + priorityScore;
    }

    private static bool IsCapable(CarrierCapabilities caps, string operation) => operation switch
    {
        "sms" => caps.Sms,
        "voice" => caps.Voice,
        "fax" => caps.Fax,
        "numbers" => caps.Numbers,
        "e911" => caps.E911,
        _ => false
    };

    private static string ExtractCountryCode(string phoneNumber)
    {
        // E.164: +1... = US/CA, +44... = GB, etc.
        if (phoneNumber.StartsWith("+1")) return phoneNumber[2] == '8' ? "CA" : "US"; // Simplified
        if (phoneNumber.StartsWith("+44")) return "GB";
        if (phoneNumber.StartsWith("+49")) return "DE";
        if (phoneNumber.StartsWith("+33")) return "FR";
        // ... more mappings
        return "US"; // Default
    }
}

public record CarrierCapabilities
{
    public bool Sms { get; init; }
    public bool Voice { get; init; }
    public bool Fax { get; init; }
    public bool Numbers { get; init; }
    public bool E911 { get; init; }
    public string[] SupportedCountries { get; init; } = Array.Empty<string>();
    public int Priority { get; init; }
}
```

## 5.3 Kamailio SBC Configuration

```
# /etc/kamailio/kamailio.cfg

#!KAMAILIO
#!define WITH_TLS
#!define WITH_ANTIFLOOD

####### Global Parameters #########

debug=2
log_stderror=no
memdbg=5
memlog=5
log_facility=LOG_LOCAL0
fork=yes
children=8
auto_aliases=no

listen=udp:0.0.0.0:5060
listen=tcp:0.0.0.0:5060
listen=tls:0.0.0.0:5061

####### Modules Section ########

loadmodule "sl.so"
loadmodule "tm.so"
loadmodule "rr.so"
loadmodule "pv.so"
loadmodule "maxfwd.so"
loadmodule "textops.so"
loadmodule "siputils.so"
loadmodule "xlog.so"
loadmodule "sanity.so"
loadmodule "nathelper.so"
loadmodule "rtpproxy.so"
loadmodule "dispatcher.so"
loadmodule "htable.so"
loadmodule "pike.so"
loadmodule "dialog.so"
loadmodule "tls.so"
loadmodule "http_async_client.so"

####### Dispatcher Configuration ########

# Carrier groups
modparam("dispatcher", "list_file", "/etc/kamailio/dispatcher.list")
modparam("dispatcher", "flags", 2)
modparam("dispatcher", "dst_avp", "$avp(ds_dst)")
modparam("dispatcher", "grp_avp", "$avp(ds_grp)")
modparam("dispatcher", "cnt_avp", "$avp(ds_cnt)")
modparam("dispatcher", "ds_ping_method", "OPTIONS")
modparam("dispatcher", "ds_ping_interval", 30)
modparam("dispatcher", "ds_probing_mode", 1)
modparam("dispatcher", "ds_ping_latency_stats", 1)

####### TLS Configuration ########

modparam("tls", "config", "/etc/kamailio/tls.cfg")

####### Rate Limiting ########

modparam("pike", "sampling_time_unit", 2)
modparam("pike", "reqs_density_per_unit", 30)
modparam("pike", "remove_latency", 4)

modparam("htable", "htable", "ipban=>size=8;autoexpire=300")

####### Request Routing Logic ########

request_route {
    # Per-IP rate limiting
    if (!pike_check_req()) {
        xlog("L_WARN", "PIKE: blocking $si\n");
        $sht(ipban=>$si) = 1;
        exit;
    }

    if ($sht(ipban=>$si) != $null) {
        xlog("L_WARN", "IPBAN: blocking $si\n");
        exit;
    }

    # Initial checks
    if (!mf_process_maxfwd_header("10")) {
        sl_send_reply("483", "Too Many Hops");
        exit;
    }

    if (!sanity_check("1511", "7")) {
        xlog("L_WARN", "Malformed SIP message from $si:$sp\n");
        exit;
    }

    # NAT detection
    if (nat_uac_test("19")) {
        if (is_method("REGISTER")) {
            fix_nated_register();
        } else {
            fix_nated_contact();
        }
        setflag(5); # NAT flag
    }

    # Record-Route
    if (is_method("INVITE|SUBSCRIBE")) {
        record_route();
    }

    # Handle in-dialog requests
    if (has_totag()) {
        if (loose_route()) {
            if (is_method("BYE")) {
                # Account for call end
            }
            route(RELAY);
            exit;
        }
    }

    # CANCEL handling
    if (is_method("CANCEL")) {
        if (t_check_trans()) {
            route(RELAY);
        }
        exit;
    }

    # Handle ACK
    if (is_method("ACK")) {
        if (t_check_trans()) {
            route(RELAY);
        }
        exit;
    }

    # New requests
    if (is_method("INVITE")) {
        route(HANDLE_INVITE);
        exit;
    }

    if (is_method("REGISTER")) {
        sl_send_reply("503", "Registration Not Supported");
        exit;
    }

    route(RELAY);
}

route[HANDLE_INVITE] {
    # Determine routing based on source
    if ($si == "10.0.0.10") {
        # From Voice Gateway - route to carrier
        route(ROUTE_TO_CARRIER);
    } else {
        # From carrier - route to Voice Gateway
        route(ROUTE_TO_GATEWAY);
    }
}

route[ROUTE_TO_CARRIER] {
    # Select carrier using dispatcher
    # Group 1 = Telnyx, Group 2 = Bandwidth, Group 3 = DIDWW

    if (!ds_select_dst("1", "4")) {  # Algorithm 4 = round-robin with weights
        if (!ds_select_dst("2", "4")) {
            if (!ds_select_dst("3", "4")) {
                sl_send_reply("503", "Service Unavailable");
                exit;
            }
        }
    }

    # Add STIR/SHAKEN headers if not present
    if ($hdr(Identity) == $null) {
        # Call authentication service
        route(ADD_STIR_SHAKEN);
    }

    # Set failure route for failover
    t_on_failure("CARRIER_FAILOVER");

    route(RELAY);
}

route[ROUTE_TO_GATEWAY] {
    # Route inbound calls to Voice Gateway
    $du = "sip:10.0.0.10:5060";
    route(RELAY);
}

route[RELAY] {
    # RTP proxy for NAT traversal
    if (isflagset(5)) {
        rtpproxy_manage("co");
    }

    if (!t_relay()) {
        sl_reply_error();
    }
}

failure_route[CARRIER_FAILOVER] {
    if (t_is_canceled()) exit;

    # Try next carrier in the dispatcher set
    if (t_check_status("5[0-9][0-9]|6[0-9][0-9]")) {
        xlog("L_WARN", "Carrier failed, trying next\n");

        if (ds_next_dst()) {
            t_on_failure("CARRIER_FAILOVER");
            route(RELAY);
            exit;
        }
    }

    # All carriers failed
    send_reply("503", "All Carriers Unavailable");
}

route[ADD_STIR_SHAKEN] {
    # Integration with STIR/SHAKEN signing service
    # This would call an external service to sign the call
    $var(attestation) = "A";  # Full attestation
    # Add Identity header
}
```

### Dispatcher List Configuration

```
# /etc/kamailio/dispatcher.list

# Group 1: Telnyx
1 sip:sip.telnyx.com:5060 2 0 weight=60

# Group 2: Bandwidth
2 sip:sip.bandwidth.com:5060 2 0 weight=30

# Group 3: DIDWW
3 sip:sip.didww.com:5060 2 0 weight=10
```

## 5.4 Carrier Health Monitoring

```csharp
// Dartwing.Tel.RoutingEngine/Services/CarrierHealthService.cs

using Microsoft.Extensions.Caching.Distributed;
using System.Text.Json;

namespace Dartwing.Tel.RoutingEngine.Services;

public interface ICarrierHealthService
{
    Task<Dictionary<string, int>> GetHealthScoresAsync(IEnumerable<string> carriers);
    Task UpdateHealthScoreAsync(string carrier, HealthMetrics metrics);
    Task ReportIncidentAsync(string carrier, string incidentType, string details);
}

public class CarrierHealthService : ICarrierHealthService
{
    private readonly IDistributedCache _cache;
    private readonly ILogger<CarrierHealthService> _logger;

    private const int HealthyThreshold = 80;
    private const int DegradedThreshold = 50;
    private const string CacheKeyPrefix = "carrier:health:";

    public async Task<Dictionary<string, int>> GetHealthScoresAsync(IEnumerable<string> carriers)
    {
        var results = new Dictionary<string, int>();

        foreach (var carrier in carriers)
        {
            var cached = await _cache.GetStringAsync($"{CacheKeyPrefix}{carrier}");
            if (cached != null)
            {
                var metrics = JsonSerializer.Deserialize<HealthMetrics>(cached);
                results[carrier] = CalculateHealthScore(metrics!);
            }
            else
            {
                results[carrier] = 100; // Assume healthy if no data
            }
        }

        return results;
    }

    public async Task UpdateHealthScoreAsync(string carrier, HealthMetrics metrics)
    {
        var json = JsonSerializer.Serialize(metrics);
        await _cache.SetStringAsync(
            $"{CacheKeyPrefix}{carrier}",
            json,
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
            });

        var score = CalculateHealthScore(metrics);

        if (score < DegradedThreshold)
        {
            _logger.LogWarning(
                "Carrier {Carrier} health degraded: {Score}% (latency={Latency}ms, errors={ErrorRate}%)",
                carrier, score, metrics.AvgLatencyMs, metrics.ErrorRatePercent);
        }
    }

    private static int CalculateHealthScore(HealthMetrics metrics)
    {
        // Scoring: 100 = perfect, 0 = completely down
        var score = 100;

        // Latency penalty: -1 point per 10ms over 100ms
        if (metrics.AvgLatencyMs > 100)
        {
            score -= (int)((metrics.AvgLatencyMs - 100) / 10);
        }

        // Error rate penalty: -2 points per 1% error rate
        score -= (int)(metrics.ErrorRatePercent * 2);

        // Recent incident penalty
        if (metrics.LastIncidentMinutesAgo < 30)
        {
            score -= 20;
        }
        else if (metrics.LastIncidentMinutesAgo < 60)
        {
            score -= 10;
        }

        return Math.Max(0, Math.Min(100, score));
    }
}

public record HealthMetrics
{
    public double AvgLatencyMs { get; init; }
    public double ErrorRatePercent { get; init; }
    public int RequestsLastMinute { get; init; }
    public int LastIncidentMinutesAgo { get; init; }
    public DateTime LastUpdated { get; init; }
}
```

---

# Section 6: Voice Pipeline Architecture

## 6.1 Voice Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VOICE PIPELINE ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Flutter App                                   │   │
│  │                                                                       │   │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │   │
│  │   │  Call UI    │    │  WebRTC     │    │  Socket.IO  │             │   │
│  │   │  Widget     │────│  Plugin     │────│   Client    │             │   │
│  │   └─────────────┘    └─────────────┘    └─────────────┘             │   │
│  │                             │                   │                     │   │
│  └─────────────────────────────┼───────────────────┼─────────────────────┘   │
│                                │                   │                         │
│                          RTP/SRTP           WebSocket (signaling)           │
│                                │                   │                         │
│  ┌─────────────────────────────▼───────────────────▼─────────────────────┐   │
│  │                     Voice Gateway (.NET)                              │   │
│  │                                                                       │   │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │   │
│  │   │  SignalR    │    │   WebRTC    │    │    SIP      │             │   │
│  │   │    Hub      │────│   Engine    │────│   Client    │             │   │
│  │   └─────────────┘    └─────────────┘    └─────────────┘             │   │
│  │          │                  │                   │                     │   │
│  │   ┌──────▼──────────────────▼───────────────────▼──────┐             │   │
│  │   │              Media Bridge                          │             │   │
│  │   │                                                    │             │   │
│  │   │  WebRTC (Opus) ◄──────► RTP (G.711/G.722)         │             │   │
│  │   │                                                    │             │   │
│  │   │  ┌─────────┐  ┌─────────┐  ┌─────────┐           │             │   │
│  │   │  │Transcode│  │ Mixer   │  │Recording│           │             │   │
│  │   │  └─────────┘  └─────────┘  └─────────┘           │             │   │
│  │   └────────────────────────────────────────────────────┘             │   │
│  │                                                                       │   │
│  └───────────────────────────────┬───────────────────────────────────────┘   │
│                                  │                                           │
│                             SIP/RTP                                          │
│                                  │                                           │
│  ┌───────────────────────────────▼───────────────────────────────────────┐   │
│  │                     Kamailio SBC                                      │   │
│  │                                                                       │   │
│  │   • SIP Routing      • TLS Termination    • NAT Traversal            │   │
│  │   • Load Balancing   • STIR/SHAKEN        • Failover                 │   │
│  │                                                                       │   │
│  └───────────────────────────────┬───────────────────────────────────────┘   │
│                                  │                                           │
│         ┌────────────────────────┼────────────────────────┐                 │
│         │                        │                        │                 │
│         ▼                        ▼                        ▼                 │
│    ┌─────────┐             ┌─────────┐             ┌─────────┐            │
│    │ Telnyx  │             │Bandwidth│             │  DIDWW  │            │
│    │  SIP    │             │   SIP   │             │   SIP   │            │
│    └────┬────┘             └────┬────┘             └────┬────┘            │
│         │                       │                       │                  │
│         └───────────────────────┴───────────────────────┘                  │
│                                 │                                           │
│                                 ▼                                           │
│                          Global PSTN                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Voice Gateway Service

```csharp
// Dartwing.Tel.VoiceGateway/Services/VoiceGatewayService.cs

using Dartwing.Tel.Protos;
using Grpc.Core;
using SIPSorcery.SIP;
using SIPSorcery.SIP.App;

namespace Dartwing.Tel.VoiceGateway.Services;

public class VoiceGatewayService : Protos.VoiceGateway.VoiceGatewayBase
{
    private readonly ILogger<VoiceGatewayService> _logger;
    private readonly ISipService _sipService;
    private readonly IRoutingEngine _routingEngine;
    private readonly ICallStateManager _callStateManager;
    private readonly IRecordingService _recordingService;

    public override async Task<InitiateCallResponse> InitiateCall(
        InitiateCallRequest request,
        ServerCallContext context)
    {
        _logger.LogInformation(
            "Initiating call {CallId} from {From} to {To}",
            request.CallId, request.FromNumber, request.ToNumber);

        // Select carrier
        var carrier = await _routingEngine.SelectCarrierAsync(
            operationType: "voice",
            destination: request.ToNumber);

        // Build SIP INVITE
        var sipUri = BuildCarrierUri(carrier.Carrier, request.ToNumber);

        var invite = new SIPRequest(SIPMethodsEnum.INVITE, sipUri)
        {
            Header = new SIPHeader(
                new SIPFromHeader(request.CallerIdName, new SIPURI(request.FromNumber), null),
                new SIPToHeader(null, sipUri, null),
                1,
                CallProperties.CreateNewCallId())
        };

        // Add STIR/SHAKEN Identity header
        var identityHeader = await GenerateStirShakenHeader(
            request.FromNumber,
            request.ToNumber,
            invite.Header.CallId);
        invite.Header.UnknownHeaders.Add($"Identity: {identityHeader}");

        // Store call state
        var callState = new CallState
        {
            CallId = request.CallId,
            SipCallId = invite.Header.CallId,
            FromNumber = request.FromNumber,
            ToNumber = request.ToNumber,
            Carrier = carrier.Carrier,
            Status = CallStatus.Initiating,
            RecordingEnabled = request.RecordingEnabled,
            StartedAt = DateTime.UtcNow
        };
        await _callStateManager.SetCallStateAsync(callState);

        // Send INVITE
        var sipResult = await _sipService.SendInviteAsync(
            invite,
            carrier.Carrier,
            request.TimeoutSeconds);

        // Update state
        callState.CarrierCallId = sipResult.CarrierCallId;
        await _callStateManager.SetCallStateAsync(callState);

        return new InitiateCallResponse
        {
            Carrier = carrier.Carrier,
            CarrierCallId = sipResult.CarrierCallId,
            SipCallId = invite.Header.CallId,
            Status = "initiated"
        };
    }

    public override async Task StreamCallEvents(
        StreamCallEventsRequest request,
        IServerStreamWriter<CallEvent> responseStream,
        ServerCallContext context)
    {
        var callId = request.CallId;

        // Subscribe to call events
        await foreach (var evt in _callStateManager.SubscribeToEventsAsync(
            callId, context.CancellationToken))
        {
            await responseStream.WriteAsync(new CallEvent
            {
                CallId = callId,
                EventType = evt.Type,
                Timestamp = evt.Timestamp.ToString("O"),
                Data = { evt.Data }
            });
        }
    }

    public override async Task<StartRecordingResponse> StartRecording(
        StartRecordingRequest request,
        ServerCallContext context)
    {
        var callState = await _callStateManager.GetCallStateAsync(request.CallId);
        if (callState == null)
        {
            throw new RpcException(new Status(StatusCode.NotFound, "Call not found"));
        }

        var result = await _recordingService.StartRecordingAsync(
            request.CallId,
            request.RecordingId,
            request.Channels);

        callState.RecordingEnabled = true;
        callState.RecordingId = request.RecordingId;
        await _callStateManager.SetCallStateAsync(callState);

        return new StartRecordingResponse
        {
            RecordingId = request.RecordingId,
            Status = "recording"
        };
    }

    private SIPURI BuildCarrierUri(string carrier, string toNumber)
    {
        var host = carrier switch
        {
            "Telnyx" => "sip.telnyx.com",
            "Bandwidth" => "sip.bandwidth.com",
            "DIDWW" => "sip.didww.com",
            _ => throw new ArgumentException($"Unknown carrier: {carrier}")
        };

        return new SIPURI(toNumber, host, null, SIPSchemesEnum.sip);
    }

    private async Task<string> GenerateStirShakenHeader(
        string from,
        string to,
        string callId)
    {
        // Generate STIR/SHAKEN PASSporT token
        // This would integrate with a signing service
        var attestation = "A"; // Full attestation - we own the number
        var origId = Guid.NewGuid().ToString();

        // In production, this calls the STIR/SHAKEN signing service
        return $"eyJhbGciOiJFUzI1NiIsInR5cCI6InBhc3Nwb3J0IiwieDV1IjoiaHR0cHM6Ly9jZXJ0LmRhcnR3aW5nLmNvbS9zdGlyLmNydCJ9...;info=<https://cert.dartwing.com/stir.crt>;alg=ES256;ppt=shaken";
    }
}
```

## 6.3 WebRTC Signaling Hub

```csharp
// Dartwing.Tel.VoiceGateway/Hubs/CallSignalingHub.cs

using Microsoft.AspNetCore.SignalR;
using System.Text.Json;

namespace Dartwing.Tel.VoiceGateway.Hubs;

public class CallSignalingHub : Hub
{
    private readonly ILogger<CallSignalingHub> _logger;
    private readonly IWebRtcService _webRtcService;
    private readonly ICallStateManager _callStateManager;

    public async Task JoinCall(string callId, string clientId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, callId);

        _logger.LogInformation(
            "Client {ClientId} joined call {CallId}",
            clientId, callId);

        // Get current call state
        var callState = await _callStateManager.GetCallStateAsync(callId);
        if (callState != null)
        {
            await Clients.Caller.SendAsync("CallState", JsonSerializer.Serialize(callState));
        }
    }

    public async Task LeaveCall(string callId)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, callId);
    }

    public async Task SendOffer(string callId, string sdpOffer)
    {
        _logger.LogDebug("Received SDP offer for call {CallId}", callId);

        // Process offer and generate answer
        var sdpAnswer = await _webRtcService.ProcessOfferAsync(callId, sdpOffer);

        await Clients.Caller.SendAsync("SdpAnswer", sdpAnswer);
    }

    public async Task SendAnswer(string callId, string sdpAnswer)
    {
        _logger.LogDebug("Received SDP answer for call {CallId}", callId);

        await _webRtcService.ProcessAnswerAsync(callId, sdpAnswer);
    }

    public async Task SendIceCandidate(string callId, string candidate)
    {
        await _webRtcService.AddIceCandidateAsync(callId, candidate);

        // Forward to other participants
        await Clients.OthersInGroup(callId).SendAsync("IceCandidate", candidate);
    }

    public async Task SendDtmf(string callId, string digit)
    {
        _logger.LogDebug("DTMF {Digit} for call {CallId}", digit, callId);

        await _webRtcService.SendDtmfAsync(callId, digit);
    }

    public async Task Mute(string callId, bool muted)
    {
        await _webRtcService.SetMuteAsync(callId, Context.ConnectionId, muted);

        await Clients.OthersInGroup(callId).SendAsync("ParticipantMuted", new
        {
            ConnectionId = Context.ConnectionId,
            Muted = muted
        });
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        _logger.LogInformation("Client disconnected: {ConnectionId}", Context.ConnectionId);

        // Cleanup any active calls for this connection
        await _webRtcService.CleanupConnectionAsync(Context.ConnectionId);

        await base.OnDisconnectedAsync(exception);
    }
}
```

## 6.4 Recording Service

```csharp
// Dartwing.Tel.VoiceGateway/Services/RecordingService.cs

using Amazon.S3;
using Amazon.S3.Transfer;

namespace Dartwing.Tel.VoiceGateway.Services;

public interface IRecordingService
{
    Task<RecordingResult> StartRecordingAsync(string callId, string recordingId, string channels);
    Task<RecordingResult> StopRecordingAsync(string recordingId);
    Task<TranscriptionResult> TranscribeAsync(string recordingId);
}

public class RecordingService : IRecordingService
{
    private readonly ILogger<RecordingService> _logger;
    private readonly IAmazonS3 _s3Client;
    private readonly IMediaServer _mediaServer;
    private readonly ITranscriptionProvider _transcriptionProvider;
    private readonly RecordingOptions _options;

    public async Task<RecordingResult> StartRecordingAsync(
        string callId,
        string recordingId,
        string channels)
    {
        // Configure recording format
        var format = new RecordingFormat
        {
            Codec = "mp3",
            SampleRate = 16000,
            Bitrate = 64000,
            Channels = channels switch
            {
                "mono" => 1,
                "stereo" => 2,
                "dual" => 2, // Separate tracks
                _ => 1
            }
        };

        // Start recording on media server
        var localPath = Path.Combine(_options.TempPath, $"{recordingId}.mp3");

        await _mediaServer.StartRecordingAsync(callId, localPath, format);

        _logger.LogInformation(
            "Started recording {RecordingId} for call {CallId}",
            recordingId, callId);

        return new RecordingResult
        {
            RecordingId = recordingId,
            Status = "recording",
            Format = format
        };
    }

    public async Task<RecordingResult> StopRecordingAsync(string recordingId)
    {
        // Stop recording on media server
        var localPath = await _mediaServer.StopRecordingAsync(recordingId);

        // Get file info
        var fileInfo = new FileInfo(localPath);

        // Upload to S3
        var s3Key = $"recordings/{DateTime.UtcNow:yyyy/MM/dd}/{recordingId}.mp3";

        using var fileTransfer = new TransferUtility(_s3Client);
        await fileTransfer.UploadAsync(localPath, _options.S3Bucket, s3Key);

        var s3Url = $"s3://{_options.S3Bucket}/{s3Key}";

        // Calculate duration
        var duration = await GetAudioDurationAsync(localPath);

        // Cleanup local file
        File.Delete(localPath);

        _logger.LogInformation(
            "Recording {RecordingId} completed: {Duration}s, {Size} bytes",
            recordingId, duration, fileInfo.Length);

        return new RecordingResult
        {
            RecordingId = recordingId,
            Status = "completed",
            FileUrl = s3Url,
            DurationSeconds = duration,
            FileSizeBytes = fileInfo.Length
        };
    }

    public async Task<TranscriptionResult> TranscribeAsync(string recordingId)
    {
        // Get recording from S3
        var recording = await GetRecordingMetadataAsync(recordingId);

        // Transcribe using configured provider (Deepgram, Whisper, etc.)
        var transcription = await _transcriptionProvider.TranscribeAsync(
            recording.FileUrl,
            new TranscriptionOptions
            {
                Language = "en",
                SpeakerDiarization = true,
                Punctuation = true,
                WordTimestamps = true
            });

        return new TranscriptionResult
        {
            RecordingId = recordingId,
            Text = transcription.Text,
            Segments = transcription.Segments,
            Speakers = transcription.Speakers,
            Provider = _transcriptionProvider.Name
        };
    }

    private async Task<int> GetAudioDurationAsync(string filePath)
    {
        // Use ffprobe to get duration
        var process = new System.Diagnostics.Process
        {
            StartInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "ffprobe",
                Arguments = $"-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{filePath}\"",
                RedirectStandardOutput = true,
                UseShellExecute = false
            }
        };

        process.Start();
        var output = await process.StandardOutput.ReadToEndAsync();
        await process.WaitForExitAsync();

        return (int)Math.Round(double.Parse(output));
    }
}

public record RecordingFormat
{
    public string Codec { get; init; } = "mp3";
    public int SampleRate { get; init; } = 16000;
    public int Bitrate { get; init; } = 64000;
    public int Channels { get; init; } = 1;
}

public record RecordingResult
{
    public string RecordingId { get; init; } = "";
    public string Status { get; init; } = "";
    public string? FileUrl { get; init; }
    public int? DurationSeconds { get; init; }
    public long? FileSizeBytes { get; init; }
    public RecordingFormat? Format { get; init; }
}
```

## 6.5 Call State Management

```csharp
// Dartwing.Tel.VoiceGateway/Services/CallStateManager.cs

using Microsoft.Extensions.Caching.Distributed;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Threading.Channels;

namespace Dartwing.Tel.VoiceGateway.Services;

public interface ICallStateManager
{
    Task<CallState?> GetCallStateAsync(string callId);
    Task SetCallStateAsync(CallState state);
    Task RemoveCallStateAsync(string callId);
    Task PublishEventAsync(string callId, CallStateEvent evt);
    IAsyncEnumerable<CallStateEvent> SubscribeToEventsAsync(string callId, CancellationToken ct);
}

public class CallStateManager : ICallStateManager
{
    private readonly IDistributedCache _cache;
    private readonly ILogger<CallStateManager> _logger;
    private readonly Dictionary<string, Channel<CallStateEvent>> _eventChannels = new();
    private readonly object _channelLock = new();

    private const string CacheKeyPrefix = "call:state:";
    private static readonly TimeSpan CallStateTtl = TimeSpan.FromHours(24);

    public async Task<CallState?> GetCallStateAsync(string callId)
    {
        var json = await _cache.GetStringAsync($"{CacheKeyPrefix}{callId}");
        return json == null ? null : JsonSerializer.Deserialize<CallState>(json);
    }

    public async Task SetCallStateAsync(CallState state)
    {
        var json = JsonSerializer.Serialize(state);
        await _cache.SetStringAsync(
            $"{CacheKeyPrefix}{state.CallId}",
            json,
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = CallStateTtl
            });
    }

    public async Task RemoveCallStateAsync(string callId)
    {
        await _cache.RemoveAsync($"{CacheKeyPrefix}{callId}");

        lock (_channelLock)
        {
            if (_eventChannels.TryGetValue(callId, out var channel))
            {
                channel.Writer.Complete();
                _eventChannels.Remove(callId);
            }
        }
    }

    public async Task PublishEventAsync(string callId, CallStateEvent evt)
    {
        Channel<CallStateEvent>? channel;

        lock (_channelLock)
        {
            _eventChannels.TryGetValue(callId, out channel);
        }

        if (channel != null)
        {
            await channel.Writer.WriteAsync(evt);
        }

        _logger.LogDebug(
            "Published event {EventType} for call {CallId}",
            evt.Type, callId);
    }

    public async IAsyncEnumerable<CallStateEvent> SubscribeToEventsAsync(
        string callId,
        [EnumeratorCancellation] CancellationToken ct)
    {
        var channel = Channel.CreateUnbounded<CallStateEvent>();

        lock (_channelLock)
        {
            _eventChannels[callId] = channel;
        }

        try
        {
            await foreach (var evt in channel.Reader.ReadAllAsync(ct))
            {
                yield return evt;
            }
        }
        finally
        {
            lock (_channelLock)
            {
                _eventChannels.Remove(callId);
            }
        }
    }
}

public record CallState
{
    public string CallId { get; init; } = "";
    public string SipCallId { get; init; } = "";
    public string? CarrierCallId { get; set; }
    public string FromNumber { get; init; } = "";
    public string ToNumber { get; init; } = "";
    public string Carrier { get; init; } = "";
    public CallStatus Status { get; set; }
    public bool RecordingEnabled { get; set; }
    public string? RecordingId { get; set; }
    public DateTime StartedAt { get; init; }
    public DateTime? AnsweredAt { get; set; }
    public DateTime? EndedAt { get; set; }
}

public enum CallStatus
{
    Initiating,
    Ringing,
    InProgress,
    Completed,
    Failed,
    Busy,
    NoAnswer,
    Canceled
}

public record CallStateEvent
{
    public string Type { get; init; } = "";
    public DateTime Timestamp { get; init; } = DateTime.UtcNow;
    public Dictionary<string, string> Data { get; init; } = new();
}
```

---

# Section 7: SMS & Messaging Architecture

## 7.1 SMS Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SMS PIPELINE ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      Consumer Modules                                 │   │
│  │   DartwingVA | DartwingUser | DartwingHealth | DartwingFamily        │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│                          POST /api/method/...send_sms                       │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │                      Frappe API Layer                                 │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Validate  │  │   Rate      │  │ Compliance  │  │   Create    │ │   │
│  │  │   API Key   │──│   Limit     │──│   Check     │──│  DocType    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│                              gRPC                                           │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │                      SMS Router (.NET)                                │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Message    │  │   Carrier   │  │   Segment   │  │   Delivery  │ │   │
│  │  │  Analyzer   │──│  Selector   │──│  Calculator │──│   Manager   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│              ┌───────────────────┼───────────────────┐                      │
│              │                   │                   │                      │
│              ▼                   ▼                   ▼                      │
│       ┌───────────┐       ┌───────────┐       ┌───────────┐                │
│       │  Telnyx   │       │ Bandwidth │       │   Sinch   │                │
│       │  REST API │       │  REST API │       │  REST API │                │
│       └─────┬─────┘       └─────┬─────┘       └─────┬─────┘                │
│             │                   │                   │                      │
│             └───────────────────┴───────────────────┘                      │
│                                 │                                          │
│                                 ▼                                          │
│                          Carrier Network                                   │
│                                 │                                          │
│                                 ▼                                          │
│                         Destination Phone                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 7.2 SMS Router Service

```csharp
// Dartwing.Tel.SmsRouter/Services/SmsProcessorService.cs

namespace Dartwing.Tel.SmsRouter.Services;

public class SmsProcessorService
{
    private readonly IRoutingEngine _routingEngine;
    private readonly ICarrierAdapterFactory _carrierFactory;
    private readonly IMessageQueue _messageQueue;
    private readonly ILogger<SmsProcessorService> _logger;

    public async Task<SmsRouteResult> ProcessSmsAsync(SmsRouteRequest request)
    {
        // Analyze message
        var analysis = AnalyzeMessage(request.Body);

        // Select carrier with failover
        var carriers = await GetCarrierPriorityListAsync(request.ToNumber);

        Exception? lastException = null;

        foreach (var carrier in carriers)
        {
            try
            {
                var adapter = _carrierFactory.GetAdapter(carrier);

                var result = await adapter.SendSmsAsync(new SmsRequest(
                    MessageId: request.MessageId,
                    From: request.FromNumber,
                    To: request.ToNumber,
                    Body: request.Body,
                    Encoding: analysis.Encoding,
                    CallbackUrl: $"https://api.dartwing.com/tel/webhook/{carrier.ToLower()}/sms"
                ));

                // Publish success event
                await _messageQueue.PublishAsync("tel.events", "sms.sent", new
                {
                    MessageId = request.MessageId,
                    Carrier = carrier,
                    CarrierMessageId = result.CarrierMessageId,
                    Segments = analysis.Segments,
                    Cost = result.Cost,
                    Timestamp = DateTime.UtcNow
                });

                return new SmsRouteResult
                {
                    Success = true,
                    Carrier = carrier,
                    CarrierMessageId = result.CarrierMessageId,
                    Segments = analysis.Segments,
                    Cost = result.Cost
                };
            }
            catch (CarrierException ex) when (ex.IsRetryable)
            {
                _logger.LogWarning(ex, "Carrier {Carrier} failed, trying next", carrier);
                lastException = ex;

                // Report carrier issue
                await _routingEngine.ReportCarrierIssueAsync(carrier, "sms", ex.ErrorCode);
            }
        }

        // All carriers failed
        await _messageQueue.PublishAsync("tel.events", "sms.failed", new
        {
            MessageId = request.MessageId,
            Error = lastException?.Message ?? "All carriers failed",
            Timestamp = DateTime.UtcNow
        });

        throw new AllCarriersFailedException("SMS delivery failed on all carriers", lastException);
    }

    private MessageAnalysis AnalyzeMessage(string body)
    {
        var hasUnicode = body.Any(c => c > 127);

        if (hasUnicode)
        {
            // UCS-2 encoding
            var charCount = body.Length;
            var segments = charCount <= 70 ? 1 : (int)Math.Ceiling(charCount / 67.0);

            return new MessageAnalysis
            {
                Encoding = "UCS-2",
                CharacterCount = charCount,
                Segments = segments,
                HasUnicode = true
            };
        }
        else
        {
            // GSM-7 encoding
            var charCount = body.Length;
            var segments = charCount <= 160 ? 1 : (int)Math.Ceiling(charCount / 153.0);

            return new MessageAnalysis
            {
                Encoding = "GSM-7",
                CharacterCount = charCount,
                Segments = segments,
                HasUnicode = false
            };
        }
    }

    private async Task<List<string>> GetCarrierPriorityListAsync(string destination)
    {
        var countryCode = PhoneUtils.GetCountryCode(destination);

        // Get health scores
        var healthScores = await _routingEngine.GetCarrierHealthAsync();

        // Priority list based on destination and health
        return countryCode switch
        {
            "US" or "CA" => new[] { "Telnyx", "Bandwidth", "Sinch" }
                .Where(c => healthScores.GetValueOrDefault(c, 0) > 50)
                .OrderByDescending(c => healthScores.GetValueOrDefault(c, 0))
                .ToList(),

            "GB" or "DE" or "FR" => new[] { "Sinch", "Telnyx" }
                .Where(c => healthScores.GetValueOrDefault(c, 0) > 50)
                .OrderByDescending(c => healthScores.GetValueOrDefault(c, 0))
                .ToList(),

            _ => new[] { "Telnyx", "Sinch" }
                .Where(c => healthScores.GetValueOrDefault(c, 0) > 50)
                .ToList()
        };
    }
}

public record MessageAnalysis
{
    public string Encoding { get; init; } = "";
    public int CharacterCount { get; init; }
    public int Segments { get; init; }
    public bool HasUnicode { get; init; }
}

public record SmsRouteResult
{
    public bool Success { get; init; }
    public string Carrier { get; init; } = "";
    public string CarrierMessageId { get; init; } = "";
    public int Segments { get; init; }
    public decimal Cost { get; init; }
}
```

## 7.3 Inbound SMS Handling

```python
# dartwing_tel/webhooks/telnyx_webhook.py

import frappe
import hmac
import hashlib
import json
from datetime import datetime


def verify_telnyx_signature(payload: bytes, signature: str, timestamp: str) -> bool:
    """Verify Telnyx webhook signature."""
    secret = frappe.get_single("TEL Carrier Config").telnyx_webhook_secret

    signed_payload = f"{timestamp}.{payload.decode()}"
    expected_signature = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def handle_sms_webhook():
    """Handle inbound SMS webhook from Telnyx."""
    # Get raw payload
    payload = frappe.request.get_data()
    signature = frappe.request.headers.get("telnyx-signature-ed25519", "")
    timestamp = frappe.request.headers.get("telnyx-timestamp", "")

    # Verify signature
    if not verify_telnyx_signature(payload, signature, timestamp):
        frappe.throw("Invalid webhook signature", frappe.AuthenticationError)

    data = json.loads(payload)
    event_type = data.get("data", {}).get("event_type", "")

    if event_type == "message.received":
        handle_inbound_sms(data["data"]["payload"])
    elif event_type == "message.sent":
        handle_status_update(data["data"]["payload"], "Sent")
    elif event_type == "message.delivered":
        handle_status_update(data["data"]["payload"], "Delivered")
    elif event_type == "message.delivery_failed":
        handle_delivery_failure(data["data"]["payload"])

    return {"status": "ok"}


def handle_inbound_sms(payload: dict):
    """Process inbound SMS message."""
    from_number = payload["from"]["phone_number"]
    to_number = payload["to"][0]["phone_number"]
    body = payload["text"]
    carrier_message_id = payload["id"]

    # Find the DID
    did = frappe.get_value("TEL DID", {"phone_number": to_number})
    if not did:
        frappe.log_error(f"Inbound SMS to unknown DID: {to_number}")
        return

    did_doc = frappe.get_doc("TEL DID", did)

    # Create inbound SMS record
    sms_doc = frappe.new_doc("TEL SMS Message")
    sms_doc.direction = "Inbound"
    sms_doc.status = "Received"
    sms_doc.from_number = from_number
    sms_doc.to_number = to_number
    sms_doc.body = body
    sms_doc.carrier = "Telnyx"
    sms_doc.carrier_message_id = carrier_message_id
    sms_doc.api_key = did_doc.assigned_api_key
    sms_doc.module = did_doc.assigned_module
    sms_doc.created_at = datetime.utcnow()
    sms_doc.insert(ignore_permissions=True)

    # Check for keywords (STOP, HELP)
    upper_body = body.strip().upper()
    if upper_body in ["STOP", "UNSUBSCRIBE", "CANCEL"]:
        handle_opt_out(from_number, to_number, did_doc)
    elif upper_body in ["HELP", "INFO"]:
        handle_help_request(from_number, to_number, did_doc)

    # Deliver to consumer webhook
    if did_doc.webhook_url:
        frappe.enqueue(
            "dartwing_tel.services.webhook_service.deliver_webhook",
            webhook_url=did_doc.webhook_url,
            event_type="sms.received",
            payload={
                "message_id": sms_doc.name,
                "from": from_number,
                "to": to_number,
                "body": body,
                "received_at": sms_doc.created_at.isoformat()
            },
            api_key=did_doc.assigned_api_key
        )

    # Publish event
    frappe.publish_realtime(
        "tel_event",
        {
            "event": "sms.received",
            "message_id": sms_doc.name,
            "from": from_number,
            "to": to_number
        },
        doctype="TEL DID",
        docname=did
    )


def handle_status_update(payload: dict, status: str):
    """Update SMS delivery status."""
    carrier_message_id = payload["id"]

    sms = frappe.get_value(
        "TEL SMS Message",
        {"carrier_message_id": carrier_message_id},
        ["name", "api_key", "webhook_url"],
        as_dict=True
    )

    if not sms:
        return

    updates = {"status": status}
    if status == "Delivered":
        updates["delivered_at"] = datetime.utcnow()

    frappe.db.set_value("TEL SMS Message", sms.name, updates)

    # Deliver webhook
    if sms.webhook_url:
        frappe.enqueue(
            "dartwing_tel.services.webhook_service.deliver_webhook",
            webhook_url=sms.webhook_url,
            event_type="sms.status",
            payload={
                "message_id": sms.name,
                "status": status.lower(),
                "timestamp": datetime.utcnow().isoformat()
            },
            api_key=sms.api_key
        )


def handle_opt_out(from_number: str, to_number: str, did_doc):
    """Handle STOP/unsubscribe request."""
    # Add to DNC list
    if not frappe.db.exists("TEL DNC Entry", {"phone_number": from_number}):
        dnc = frappe.new_doc("TEL DNC Entry")
        dnc.phone_number = from_number
        dnc.source = "SMS Opt-Out"
        dnc.organization = did_doc.assigned_organization
        dnc.insert(ignore_permissions=True)

    # Send confirmation
    frappe.enqueue(
        "dartwing_tel.api.sms.send_sms",
        to=from_number,
        body="You have been unsubscribed and will not receive further messages.",
        from_number=to_number
    )
```

## 7.4 Batch SMS Processing

```python
# dartwing_tel/api/sms.py (batch operations)

@frappe.whitelist(allow_guest=True, methods=["POST"])
@require_api_key
def send_batch_sms(
    recipients: list,
    body: str,
    from_number: str = None,
    batch_name: str = None,
    messages_per_second: int = 10,
    scheduled_for: str = None
):
    """
    Send SMS to multiple recipients.

    Args:
        recipients: List of phone numbers or dicts with {to, body} for personalization
        body: Default message body (used if recipient doesn't have custom body)
        from_number: Source number (auto-selected if not provided)
        batch_name: Human-readable batch identifier
        messages_per_second: Throttle rate
        scheduled_for: ISO datetime for scheduled send

    Returns:
        dict: {batch_id, total_recipients, status}
    """
    api_key = frappe.local.tel_api_key

    # Check permissions
    permissions = json.loads(api_key.permissions or "{}")
    if not permissions.get("sms", {}).get("batch", False):
        frappe.throw(_("API key does not have batch SMS permission"), frappe.PermissionError)

    # Validate recipient count
    if len(recipients) > 100000:
        frappe.throw(_("Maximum 100,000 recipients per batch"))

    # Create batch record
    batch_doc = frappe.new_doc("TEL SMS Batch")
    batch_doc.batch_name = batch_name or f"Batch-{frappe.utils.now_datetime().isoformat()}"
    batch_doc.api_key = api_key.name
    batch_doc.module = api_key.module
    batch_doc.total_recipients = len(recipients)
    batch_doc.messages_per_second = messages_per_second
    batch_doc.default_body = body
    batch_doc.from_number = from_number
    batch_doc.scheduled_for = scheduled_for
    batch_doc.status = "Queued"
    batch_doc.insert(ignore_permissions=True)

    # Queue batch processing
    frappe.enqueue(
        "dartwing_tel.tasks.process_batch_sms",
        batch_id=batch_doc.name,
        recipients=recipients,
        queue="long",
        timeout=3600  # 1 hour max
    )

    return {
        "batch_id": batch_doc.name,
        "total_recipients": len(recipients),
        "status": "queued",
        "scheduled_for": scheduled_for
    }


# dartwing_tel/tasks.py

def process_batch_sms(batch_id: str, recipients: list):
    """Background job to process batch SMS."""
    import time

    batch = frappe.get_doc("TEL SMS Batch", batch_id)
    batch.db_set("status", "Processing")
    batch.db_set("started_at", frappe.utils.now_datetime())

    from_number = batch.from_number
    if not from_number:
        from_number = RoutingService.select_outbound_number(
            batch.api_key,
            capability="sms"
        )

    success_count = 0
    failed_count = 0
    interval = 1.0 / batch.messages_per_second

    grpc_client = TelGrpcClient()

    for i, recipient in enumerate(recipients):
        try:
            # Handle dict or string recipient
            if isinstance(recipient, dict):
                to = recipient.get("to")
                body = recipient.get("body", batch.default_body)
            else:
                to = recipient
                body = batch.default_body

            # Validate and format
            to = format_e164(to)
            if not validate_e164(to):
                failed_count += 1
                continue

            # Create SMS record
            sms_doc = frappe.new_doc("TEL SMS Message")
            sms_doc.direction = "Outbound"
            sms_doc.status = "Queued"
            sms_doc.from_number = from_number
            sms_doc.to_number = to
            sms_doc.body = body
            sms_doc.api_key = batch.api_key
            sms_doc.module = batch.module
            sms_doc.batch = batch_id
            sms_doc.insert(ignore_permissions=True)

            # Route to carrier
            result = grpc_client.route_sms(
                message_id=sms_doc.name,
                from_number=from_number,
                to_number=to,
                body=body
            )

            sms_doc.db_set("carrier", result.carrier)
            sms_doc.db_set("carrier_message_id", result.carrier_message_id)
            sms_doc.db_set("status", "Sent")
            sms_doc.db_set("cost_amount", result.cost)

            success_count += 1

        except Exception as e:
            frappe.log_error(f"Batch SMS failed: {str(e)}", "Batch SMS Error")
            failed_count += 1

        # Update progress periodically
        if i % 100 == 0:
            batch.db_set("sent_count", success_count)
            batch.db_set("failed_count", failed_count)
            frappe.db.commit()

        # Throttle
        time.sleep(interval)

    # Final update
    batch.db_set("sent_count", success_count)
    batch.db_set("failed_count", failed_count)
    batch.db_set("status", "Completed")
    batch.db_set("completed_at", frappe.utils.now_datetime())
    frappe.db.commit()

    # Deliver completion webhook
    if batch.webhook_url:
        frappe.enqueue(
            "dartwing_tel.services.webhook_service.deliver_webhook",
            webhook_url=batch.webhook_url,
            event_type="batch.completed",
            payload={
                "batch_id": batch_id,
                "total": len(recipients),
                "sent": success_count,
                "failed": failed_count
            },
            api_key=batch.api_key
        )
```

---

# Section 8: Fax Architecture

## 8.1 Fax Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FAX PIPELINE ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      Consumer Module                                  │   │
│  │                    (dartwing_fax)                                     │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│                          POST /api/.../send_fax                             │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │                      Frappe API Layer                                 │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Validate  │  │   Create    │  │   Store     │  │   Queue     │ │   │
│  │  │   Request   │──│  TEL Fax    │──│    PDF      │──│   Send      │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│                              gRPC                                           │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │                    Fax Processor (.NET)                               │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │    PDF      │  │  Cover Page │  │    TIFF     │  │    T.38     │ │   │
│  │  │  Validator  │──│  Generator  │──│  Converter  │──│   Sender    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│                             SIP + T.38                                      │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │                     Kamailio SBC                                      │   │
│  │              (T.38 Gateway / Fax Relay)                               │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│              ┌───────────────────┴───────────────────┐                      │
│              ▼                                       ▼                      │
│       ┌───────────┐                           ┌───────────┐                │
│       │  Telnyx   │                           │ Bandwidth │                │
│       │  Fax API  │                           │  Fax API  │                │
│       └─────┬─────┘                           └─────┬─────┘                │
│             │                                       │                      │
│             └───────────────────┬───────────────────┘                      │
│                                 │                                          │
│                                 ▼                                          │
│                     Destination Fax Machine                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8.2 Fax Processor Service

```csharp
// Dartwing.Tel.FaxProcessor/Services/FaxProcessorService.cs

using Dartwing.Tel.Protos;
using Grpc.Core;
using iText.Kernel.Pdf;
using ImageMagick;

namespace Dartwing.Tel.FaxProcessor.Services;

public class FaxProcessorService : Protos.FaxProcessor.FaxProcessorBase
{
    private readonly ILogger<FaxProcessorService> _logger;
    private readonly IRoutingEngine _routingEngine;
    private readonly ICarrierAdapterFactory _carrierFactory;
    private readonly IStorageService _storage;
    private readonly FaxOptions _options;

    public override async Task<SendFaxResponse> SendFax(
        SendFaxRequest request,
        ServerCallContext context)
    {
        _logger.LogInformation(
            "Processing fax {FaxId} from {From} to {To}",
            request.FaxId, request.FromNumber, request.ToNumber);

        // Download and validate PDF
        var pdfBytes = await _storage.DownloadAsync(request.DocumentUrl);
        var pageCount = await ValidatePdfAsync(pdfBytes);

        // Generate cover page if requested
        byte[] finalPdf;
        if (request.CoverPageEnabled)
        {
            var coverPdf = await GenerateCoverPageAsync(
                request.CoverPageTemplate,
                request.FromNumber,
                request.ToNumber,
                pageCount);

            finalPdf = await MergePdfsAsync(coverPdf, pdfBytes);
            pageCount += 1;
        }
        else
        {
            finalPdf = pdfBytes;
        }

        // Convert to fax-optimized TIFF
        var tiffBytes = await ConvertToTiffAsync(finalPdf);

        // Upload TIFF for carrier
        var tiffUrl = await _storage.UploadAsync(
            $"fax/{request.FaxId}.tiff",
            tiffBytes,
            "image/tiff");

        // Select carrier and send
        var carrier = await _routingEngine.SelectCarrierAsync("fax", request.ToNumber);
        var adapter = _carrierFactory.GetAdapter(carrier.Carrier);

        var result = await adapter.SendFaxAsync(new FaxRequest(
            FaxId: request.FaxId,
            From: request.FromNumber,
            To: request.ToNumber,
            DocumentUrl: tiffUrl,
            Quality: "high"
        ));

        // Estimate duration (approx 30 seconds per page)
        var estimatedDuration = pageCount * 30;

        return new SendFaxResponse
        {
            Carrier = carrier.Carrier,
            CarrierFaxId = result.CarrierFaxId,
            PageCount = pageCount,
            EstimatedDurationSeconds = estimatedDuration
        };
    }

    private async Task<int> ValidatePdfAsync(byte[] pdfBytes)
    {
        using var stream = new MemoryStream(pdfBytes);
        using var reader = new PdfReader(stream);
        using var document = new PdfDocument(reader);

        var pageCount = document.GetNumberOfPages();

        if (pageCount > _options.MaxPages)
        {
            throw new FaxException($"PDF exceeds maximum page count ({_options.MaxPages})");
        }

        // Check for encrypted/protected PDFs
        if (reader.IsEncrypted())
        {
            throw new FaxException("Encrypted PDFs are not supported");
        }

        return pageCount;
    }

    private async Task<byte[]> GenerateCoverPageAsync(
        string template,
        string from,
        string to,
        int pageCount)
    {
        var templatePath = Path.Combine(_options.TemplatesPath, $"{template}.html");
        var html = await File.ReadAllTextAsync(templatePath);

        // Replace placeholders
        html = html
            .Replace("{{FROM}}", from)
            .Replace("{{TO}}", to)
            .Replace("{{PAGES}}", pageCount.ToString())
            .Replace("{{DATE}}", DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm UTC"));

        // Convert HTML to PDF using wkhtmltopdf or similar
        return await ConvertHtmlToPdfAsync(html);
    }

    private async Task<byte[]> ConvertToTiffAsync(byte[] pdfBytes)
    {
        // Use ImageMagick to convert PDF to Group 4 TIFF
        // Resolution: 200 DPI (standard fax)
        // Compression: CCITT Group 4

        using var images = new MagickImageCollection();
        var settings = new MagickReadSettings
        {
            Density = new Density(200),
            ColorType = ColorType.Bilevel
        };

        images.Read(pdfBytes, settings);

        using var output = new MemoryStream();

        foreach (var image in images)
        {
            image.Format = MagickFormat.Tiff;
            image.SetCompression(CompressionMethod.Fax);
            image.SetAttribute("tiff:rows-per-strip", "0");
        }

        images.Write(output, MagickFormat.Tiff);

        return output.ToArray();
    }

    private async Task<byte[]> MergePdfsAsync(byte[] pdf1, byte[] pdf2)
    {
        using var output = new MemoryStream();
        using var writer = new PdfWriter(output);
        using var merger = new PdfDocument(writer);

        using (var reader1 = new PdfReader(new MemoryStream(pdf1)))
        using (var doc1 = new PdfDocument(reader1))
        {
            doc1.CopyPagesTo(1, doc1.GetNumberOfPages(), merger);
        }

        using (var reader2 = new PdfReader(new MemoryStream(pdf2)))
        using (var doc2 = new PdfDocument(reader2))
        {
            doc2.CopyPagesTo(1, doc2.GetNumberOfPages(), merger);
        }

        merger.Close();
        return output.ToArray();
    }
}
```

## 8.3 Inbound Fax Processing

```python
# dartwing_tel/webhooks/telnyx_webhook.py (fax handlers)

@frappe.whitelist(allow_guest=True, methods=["POST"])
def handle_fax_webhook():
    """Handle fax webhook from Telnyx."""
    payload = frappe.request.get_data()
    data = json.loads(payload)

    event_type = data.get("data", {}).get("event_type", "")

    if event_type == "fax.received":
        handle_inbound_fax(data["data"]["payload"])
    elif event_type == "fax.sent":
        handle_fax_status(data["data"]["payload"], "Delivered")
    elif event_type == "fax.failed":
        handle_fax_failure(data["data"]["payload"])

    return {"status": "ok"}


def handle_inbound_fax(payload: dict):
    """Process inbound fax."""
    from_number = payload["from"]
    to_number = payload["to"]
    carrier_fax_id = payload["fax_id"]
    media_url = payload["media_url"]
    page_count = payload.get("page_count", 0)

    # Find the DID
    did = frappe.get_value("TEL DID", {"phone_number": to_number, "fax_enabled": 1})
    if not did:
        frappe.log_error(f"Inbound fax to unknown DID: {to_number}")
        return

    did_doc = frappe.get_doc("TEL DID", did)

    # Download the fax TIFF
    import requests
    response = requests.get(media_url)
    tiff_content = response.content

    # Convert to PDF
    pdf_content = convert_tiff_to_pdf(tiff_content)

    # Upload to file storage
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": f"fax_{carrier_fax_id}.pdf",
        "content": pdf_content,
        "is_private": 1
    })
    file_doc.insert(ignore_permissions=True)

    # Create fax record
    fax_doc = frappe.new_doc("TEL Fax")
    fax_doc.direction = "Inbound"
    fax_doc.status = "Received"
    fax_doc.from_number = from_number
    fax_doc.to_number = to_number
    fax_doc.carrier = "Telnyx"
    fax_doc.carrier_fax_id = carrier_fax_id
    fax_doc.page_count = page_count
    fax_doc.pages_sent = page_count
    fax_doc.document_file = file_doc.file_url
    fax_doc.api_key = did_doc.assigned_api_key
    fax_doc.module = did_doc.assigned_module
    fax_doc.completed_at = frappe.utils.now_datetime()
    fax_doc.insert(ignore_permissions=True)

    # Optional: OCR the fax
    if did_doc.ocr_enabled:
        frappe.enqueue(
            "dartwing_tel.services.ocr_service.ocr_fax",
            fax_id=fax_doc.name,
            pdf_url=file_doc.file_url
        )

    # Deliver webhook
    if did_doc.webhook_url:
        frappe.enqueue(
            "dartwing_tel.services.webhook_service.deliver_webhook",
            webhook_url=did_doc.webhook_url,
            event_type="fax.received",
            payload={
                "fax_id": fax_doc.name,
                "from": from_number,
                "to": to_number,
                "page_count": page_count,
                "pdf_url": file_doc.file_url
            },
            api_key=did_doc.assigned_api_key
        )


def convert_tiff_to_pdf(tiff_content: bytes) -> bytes:
    """Convert TIFF to PDF using img2pdf."""
    import img2pdf
    from io import BytesIO

    return img2pdf.convert(BytesIO(tiff_content))
```

---

# Section 9: API Design

## 9.1 API Structure Overview

All DartwingTel APIs follow RESTful conventions through Frappe's whitelisted method pattern:

```
Base URL: https://api.dartwing.com

Endpoints Pattern:
  POST /api/method/dartwing_tel.api.{module}.{function}

Authentication:
  Header: Authorization: Bearer tel_live_xxxxxxxxxxxxxxxxx

Response Format:
  {
    "message": { ... response data ... }
  }

Error Format:
  {
    "exc_type": "ValidationError",
    "exception": "Invalid phone number format",
    "_error_message": "Invalid phone number format"
  }
```

## 9.2 API Endpoint Reference

### SMS Endpoints

| Method | Endpoint                                            | Description          |
| ------ | --------------------------------------------------- | -------------------- |
| POST   | `/api/method/dartwing_tel.api.sms.send_sms`         | Send single SMS      |
| POST   | `/api/method/dartwing_tel.api.sms.send_mms`         | Send MMS with media  |
| GET    | `/api/method/dartwing_tel.api.sms.get_status`       | Get message status   |
| POST   | `/api/method/dartwing_tel.api.sms.send_batch_sms`   | Send batch SMS       |
| DELETE | `/api/method/dartwing_tel.api.sms.cancel_scheduled` | Cancel scheduled SMS |

### Voice Endpoints

| Method | Endpoint                                               | Description            |
| ------ | ------------------------------------------------------ | ---------------------- |
| POST   | `/api/method/dartwing_tel.api.voice.make_call`         | Initiate outbound call |
| GET    | `/api/method/dartwing_tel.api.voice.get_call`          | Get call details       |
| POST   | `/api/method/dartwing_tel.api.voice.hangup`            | Terminate call         |
| POST   | `/api/method/dartwing_tel.api.voice.transfer`          | Transfer call          |
| POST   | `/api/method/dartwing_tel.api.voice.start_recording`   | Start recording        |
| POST   | `/api/method/dartwing_tel.api.voice.stop_recording`    | Stop recording         |
| POST   | `/api/method/dartwing_tel.api.voice.play_audio`        | Play audio in call     |
| POST   | `/api/method/dartwing_tel.api.voice.gather_dtmf`       | Collect DTMF input     |
| POST   | `/api/method/dartwing_tel.api.voice.create_conference` | Create conference      |

### Fax Endpoints

| Method | Endpoint                                      | Description       |
| ------ | --------------------------------------------- | ----------------- |
| POST   | `/api/method/dartwing_tel.api.fax.send_fax`   | Send fax          |
| GET    | `/api/method/dartwing_tel.api.fax.get_status` | Get fax status    |
| POST   | `/api/method/dartwing_tel.api.fax.send_batch` | Send batch fax    |
| DELETE | `/api/method/dartwing_tel.api.fax.cancel`     | Cancel queued fax |

### Number Management Endpoints

| Method | Endpoint                                           | Description              |
| ------ | -------------------------------------------------- | ------------------------ |
| GET    | `/api/method/dartwing_tel.api.numbers.search`      | Search available numbers |
| POST   | `/api/method/dartwing_tel.api.numbers.purchase`    | Purchase number          |
| DELETE | `/api/method/dartwing_tel.api.numbers.release`     | Release number           |
| POST   | `/api/method/dartwing_tel.api.numbers.port_in`     | Initiate port-in         |
| GET    | `/api/method/dartwing_tel.api.numbers.port_status` | Get port status          |
| PUT    | `/api/method/dartwing_tel.api.numbers.configure`   | Configure number         |
| GET    | `/api/method/dartwing_tel.api.numbers.lookup`      | Carrier lookup           |

### Emergency Endpoints

| Method | Endpoint                                                 | Description           |
| ------ | -------------------------------------------------------- | --------------------- |
| POST   | `/api/method/dartwing_tel.api.emergency.broadcast`       | Emergency broadcast   |
| POST   | `/api/method/dartwing_tel.api.emergency.register_e911`   | Register E911 address |
| PUT    | `/api/method/dartwing_tel.api.emergency.update_location` | Update E911 location  |

### Analytics Endpoints

| Method | Endpoint                                           | Description        |
| ------ | -------------------------------------------------- | ------------------ |
| GET    | `/api/method/dartwing_tel.api.analytics.get_cdrs`  | Query CDRs         |
| GET    | `/api/method/dartwing_tel.api.analytics.get_usage` | Get usage summary  |
| GET    | `/api/method/dartwing_tel.api.analytics.get_costs` | Get cost breakdown |

## 9.3 Request/Response Examples

### Send SMS

```http
POST /api/method/dartwing_tel.api.sms.send_sms HTTP/1.1
Host: api.dartwing.com
Authorization: Bearer tel_live_xxxxxxxxxxxx
Content-Type: application/json

{
  "to": "+14155551234",
  "body": "Your verification code is 123456",
  "from_number": "+18005559999",
  "status_callback": "https://myapp.com/webhooks/sms",
  "context": {
    "user_id": "USR-001",
    "type": "verification"
  }
}
```

```json
{
  "message": {
    "message_id": "SMS-2026-000001",
    "status": "sent",
    "segments": 1,
    "cost": {
      "amount": 0.003,
      "currency": "USD"
    },
    "carrier": "Telnyx"
  }
}
```

### Make Call

```http
POST /api/method/dartwing_tel.api.voice.make_call HTTP/1.1
Host: api.dartwing.com
Authorization: Bearer tel_live_xxxxxxxxxxxx
Content-Type: application/json

{
  "to": "+14155551234",
  "from_number": "+18005559999",
  "caller_id_name": "Dartwing VA",
  "timeout_seconds": 45,
  "recording_enabled": true,
  "tts_text": "Hello, this is your daily briefing from Dartwing.",
  "tts_voice": "en-US-Neural2-J",
  "webhook_url": "https://myapp.com/webhooks/voice"
}
```

```json
{
  "message": {
    "call_id": "CALL-2026-000001",
    "status": "ringing",
    "from_number": "+18005559999",
    "to_number": "+14155551234",
    "carrier": "Telnyx"
  }
}
```

### Send Fax

```http
POST /api/method/dartwing_tel.api.fax.send_fax HTTP/1.1
Host: api.dartwing.com
Authorization: Bearer tel_live_xxxxxxxxxxxx
Content-Type: application/json

{
  "to": "+14155551234",
  "from_number": "+18005559999",
  "document_url": "https://storage.dartwing.com/docs/invoice.pdf",
  "cover_page_enabled": true,
  "cover_page_template": "standard",
  "hipaa_mode": true
}
```

```json
{
  "message": {
    "fax_id": "FAX-2026-000001",
    "status": "queued",
    "page_count": 5,
    "estimated_duration_seconds": 150
  }
}
```

## 9.4 Webhook Delivery

### Webhook Payload Structure

```json
{
  "event": "sms.delivered",
  "timestamp": "2026-01-15T10:30:00Z",
  "webhook_id": "WH-2026-000001",
  "api_version": "2026-01-01",
  "data": {
    "message_id": "SMS-2026-000001",
    "status": "delivered",
    "delivered_at": "2026-01-15T10:29:58Z"
  }
}
```

### Webhook Signature Verification

```python
# Consumer-side verification example

import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify DartwingTel webhook signature.

    Signature header format: t=timestamp,v1=signature
    """
    parts = dict(p.split("=") for p in signature.split(","))
    timestamp = parts.get("t")
    provided_sig = parts.get("v1")

    # Check timestamp tolerance (5 minutes)
    import time
    if abs(time.time() - int(timestamp)) > 300:
        return False

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload.decode()}"
    expected_sig = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(provided_sig, expected_sig)
```

## 9.5 Rate Limiting

Rate limits are enforced per API key and returned in response headers:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705315200
```

Default limits by operation type:

| Operation       | Per Second | Per Minute | Per Day |
| --------------- | ---------- | ---------- | ------- |
| SMS Send        | 10         | 300        | 10,000  |
| Voice Call      | 5          | 100        | 1,000   |
| Fax Send        | 2          | 30         | 500     |
| Number Search   | 10         | 100        | 1,000   |
| Analytics Query | 20         | 200        | 5,000   |

---

# Section 10: Flutter SDK Architecture

## 10.1 SDK Package Structure

```
dartwing_tel_sdk/
├── lib/
│   ├── dartwing_tel.dart              # Main export
│   ├── src/
│   │   ├── client/
│   │   │   ├── tel_client.dart        # Main client
│   │   │   ├── tel_config.dart        # Configuration
│   │   │   └── tel_exception.dart     # Exceptions
│   │   │
│   │   ├── api/
│   │   │   ├── sms_api.dart           # SMS operations
│   │   │   ├── voice_api.dart         # Voice operations
│   │   │   ├── fax_api.dart           # Fax operations
│   │   │   ├── numbers_api.dart       # Number management
│   │   │   └── analytics_api.dart     # Analytics
│   │   │
│   │   ├── models/
│   │   │   ├── sms_message.dart
│   │   │   ├── call.dart
│   │   │   ├── fax.dart
│   │   │   ├── phone_number.dart
│   │   │   └── webhook_event.dart
│   │   │
│   │   ├── webrtc/
│   │   │   ├── call_manager.dart      # WebRTC call management
│   │   │   ├── signaling_client.dart  # SignalR/Socket.IO
│   │   │   └── audio_handler.dart     # Audio routing
│   │   │
│   │   └── realtime/
│   │       ├── event_stream.dart      # Real-time events
│   │       └── socket_manager.dart    # Socket.IO client
│   │
├── test/
│   ├── sms_api_test.dart
│   ├── voice_api_test.dart
│   └── webrtc_test.dart
│
└── pubspec.yaml
```

## 10.2 Main Client Implementation

```dart
// lib/src/client/tel_client.dart

import 'package:dio/dio.dart';
import 'package:socket_io_client/socket_io_client.dart' as io;

class TelClient {
  final TelConfig config;
  late final Dio _dio;
  late final io.Socket _socket;

  // API accessors
  late final SmsApi sms;
  late final VoiceApi voice;
  late final FaxApi fax;
  late final NumbersApi numbers;
  late final AnalyticsApi analytics;

  TelClient(this.config) {
    _initDio();
    _initSocket();
    _initApis();
  }

  void _initDio() {
    _dio = Dio(BaseOptions(
      baseUrl: config.baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Authorization': 'Bearer ${config.apiKey}',
        'Content-Type': 'application/json',
      },
    ));

    // Add interceptors
    _dio.interceptors.add(LogInterceptor(
      requestBody: config.enableLogging,
      responseBody: config.enableLogging,
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onError: (error, handler) {
        if (error.response?.statusCode == 429) {
          // Rate limited - extract retry-after
          final retryAfter = error.response?.headers['retry-after']?.first;
          throw TelRateLimitException(
            message: 'Rate limit exceeded',
            retryAfter: int.tryParse(retryAfter ?? '60') ?? 60,
          );
        }
        handler.next(error);
      },
    ));
  }

  void _initSocket() {
    _socket = io.io(
      config.realtimeUrl,
      io.OptionBuilder()
          .setTransports(['websocket'])
          .setAuth({'token': config.apiKey})
          .build(),
    );

    _socket.onConnect((_) {
      print('Tel SDK: Connected to realtime server');
    });

    _socket.onDisconnect((_) {
      print('Tel SDK: Disconnected from realtime server');
    });
  }

  void _initApis() {
    sms = SmsApi(_dio);
    voice = VoiceApi(_dio, _socket);
    fax = FaxApi(_dio);
    numbers = NumbersApi(_dio);
    analytics = AnalyticsApi(_dio);
  }

  /// Subscribe to real-time events for a resource
  Stream<TelEvent> subscribe(String doctype, String docname) {
    return Stream.multi((controller) {
      _socket.emit('subscribe', {
        'doctype': doctype,
        'document': docname,
      });

      void handler(dynamic data) {
        controller.add(TelEvent.fromJson(data));
      }

      _socket.on('tel_event', handler);

      controller.onCancel = () {
        _socket.emit('unsubscribe', {
          'doctype': doctype,
          'document': docname,
        });
        _socket.off('tel_event', handler);
      };
    });
  }

  void dispose() {
    _socket.dispose();
    _dio.close();
  }
}

class TelConfig {
  final String apiKey;
  final String baseUrl;
  final String realtimeUrl;
  final bool enableLogging;

  const TelConfig({
    required this.apiKey,
    this.baseUrl = 'https://api.dartwing.com',
    this.realtimeUrl = 'wss://realtime.dartwing.com',
    this.enableLogging = false,
  });
}
```

## 10.3 SMS API Implementation

```dart
// lib/src/api/sms_api.dart

import 'package:dio/dio.dart';
import '../models/sms_message.dart';

class SmsApi {
  final Dio _dio;

  SmsApi(this._dio);

  /// Send a single SMS message
  Future<SmsMessage> send({
    required String to,
    required String body,
    String? from,
    String? senderId,
    String? statusCallback,
    DateTime? scheduledFor,
    Map<String, dynamic>? context,
    String? idempotencyKey,
    bool hipaaMode = false,
  }) async {
    final response = await _dio.post(
      '/api/method/dartwing_tel.api.sms.send_sms',
      data: {
        'to': to,
        'body': body,
        if (from != null) 'from_number': from,
        if (senderId != null) 'sender_id': senderId,
        if (statusCallback != null) 'status_callback': statusCallback,
        if (scheduledFor != null) 'scheduled_for': scheduledFor.toIso8601String(),
        if (context != null) 'context': context,
        if (idempotencyKey != null) 'idempotency_key': idempotencyKey,
        'hipaa_mode': hipaaMode,
      },
    );

    return SmsMessage.fromJson(response.data['message']);
  }

  /// Send MMS with media attachments
  Future<SmsMessage> sendMms({
    required String to,
    String? body,
    required List<String> mediaUrls,
    String? from,
  }) async {
    final response = await _dio.post(
      '/api/method/dartwing_tel.api.sms.send_mms',
      data: {
        'to': to,
        if (body != null) 'body': body,
        'media_urls': mediaUrls,
        if (from != null) 'from_number': from,
      },
    );

    return SmsMessage.fromJson(response.data['message']);
  }

  /// Get message delivery status
  Future<SmsMessage> getStatus(String messageId) async {
    final response = await _dio.get(
      '/api/method/dartwing_tel.api.sms.get_status',
      queryParameters: {'message_id': messageId},
    );

    return SmsMessage.fromJson(response.data['message']);
  }

  /// Send batch SMS
  Future<BatchSmsResult> sendBatch({
    required List<SmsRecipient> recipients,
    required String body,
    String? from,
    int messagesPerSecond = 10,
  }) async {
    final response = await _dio.post(
      '/api/method/dartwing_tel.api.sms.send_batch_sms',
      data: {
        'recipients': recipients.map((r) => r.toJson()).toList(),
        'body': body,
        if (from != null) 'from_number': from,
        'messages_per_second': messagesPerSecond,
      },
    );

    return BatchSmsResult.fromJson(response.data['message']);
  }

  /// Cancel a scheduled message
  Future<void> cancelScheduled(String messageId) async {
    await _dio.delete(
      '/api/method/dartwing_tel.api.sms.cancel_scheduled',
      data: {'message_id': messageId},
    );
  }
}

class SmsRecipient {
  final String to;
  final String? body;

  const SmsRecipient({required this.to, this.body});

  Map<String, dynamic> toJson() => {
    'to': to,
    if (body != null) 'body': body,
  };
}
```

## 10.4 Voice API with WebRTC

```dart
// lib/src/api/voice_api.dart

import 'package:dio/dio.dart';
import 'package:socket_io_client/socket_io_client.dart' as io;
import '../models/call.dart';
import '../webrtc/call_manager.dart';

class VoiceApi {
  final Dio _dio;
  final io.Socket _socket;
  CallManager? _activeCallManager;

  VoiceApi(this._dio, this._socket);

  /// Initiate an outbound call
  Future<Call> makeCall({
    required String to,
    String? from,
    String? callerIdName,
    int timeoutSeconds = 60,
    bool recordingEnabled = false,
    String? audioUrl,
    String? ttsText,
    String? ttsVoice,
    Map<String, dynamic>? context,
  }) async {
    final response = await _dio.post(
      '/api/method/dartwing_tel.api.voice.make_call',
      data: {
        'to': to,
        if (from != null) 'from_number': from,
        if (callerIdName != null) 'caller_id_name': callerIdName,
        'timeout_seconds': timeoutSeconds,
        'recording_enabled': recordingEnabled,
        if (audioUrl != null) 'audio_url': audioUrl,
        if (ttsText != null) 'tts_text': ttsText,
        if (ttsVoice != null) 'tts_voice': ttsVoice,
        if (context != null) 'context': context,
      },
    );

    return Call.fromJson(response.data['message']);
  }

  /// Start a WebRTC call from the app
  Future<CallSession> startWebRtcCall({
    required String to,
    String? from,
    String? callerIdName,
  }) async {
    // First, create the call via API
    final call = await makeCall(
      to: to,
      from: from,
      callerIdName: callerIdName,
    );

    // Initialize WebRTC call manager
    _activeCallManager = CallManager(
      socket: _socket,
      callId: call.callId,
    );

    await _activeCallManager!.initialize();
    await _activeCallManager!.startCall();

    return CallSession(
      call: call,
      manager: _activeCallManager!,
    );
  }

  /// Get call details
  Future<Call> getCall(String callId) async {
    final response = await _dio.get(
      '/api/method/dartwing_tel.api.voice.get_call',
      queryParameters: {'call_id': callId},
    );

    return Call.fromJson(response.data['message']);
  }

  /// Hang up a call
  Future<void> hangup(String callId, {String? reason}) async {
    // If we have an active WebRTC session, close it
    if (_activeCallManager?.callId == callId) {
      await _activeCallManager!.endCall();
      _activeCallManager = null;
    }

    await _dio.post(
      '/api/method/dartwing_tel.api.voice.hangup',
      data: {
        'call_id': callId,
        if (reason != null) 'reason': reason,
      },
    );
  }

  /// Transfer call to another number
  Future<void> transfer(String callId, String destination) async {
    await _dio.post(
      '/api/method/dartwing_tel.api.voice.transfer',
      data: {
        'call_id': callId,
        'destination': destination,
      },
    );
  }

  /// Start call recording
  Future<Recording> startRecording(String callId, {String channels = 'mono'}) async {
    final response = await _dio.post(
      '/api/method/dartwing_tel.api.voice.start_recording',
      data: {
        'call_id': callId,
        'channels': channels,
      },
    );

    return Recording.fromJson(response.data['message']);
  }

  /// Send DTMF tones
  Future<void> sendDtmf(String callId, String digits) async {
    if (_activeCallManager?.callId == callId) {
      // Send via WebRTC
      await _activeCallManager!.sendDtmf(digits);
    } else {
      // Send via API
      await _dio.post(
        '/api/method/dartwing_tel.api.voice.send_dtmf',
        data: {
          'call_id': callId,
          'digits': digits,
        },
      );
    }
  }
}

class CallSession {
  final Call call;
  final CallManager manager;

  CallSession({required this.call, required this.manager});

  String get callId => call.callId;

  Stream<CallState> get stateStream => manager.stateStream;

  Future<void> mute(bool muted) => manager.setMute(muted);

  Future<void> setSpeaker(bool enabled) => manager.setSpeaker(enabled);

  Future<void> sendDtmf(String digits) => manager.sendDtmf(digits);

  Future<void> hangup() => manager.endCall();
}
```

## 10.5 WebRTC Call Manager

```dart
// lib/src/webrtc/call_manager.dart

import 'dart:async';
import 'package:flutter_webrtc/flutter_webrtc.dart';
import 'package:socket_io_client/socket_io_client.dart' as io;

class CallManager {
  final io.Socket socket;
  final String callId;

  RTCPeerConnection? _peerConnection;
  MediaStream? _localStream;
  MediaStream? _remoteStream;

  final _stateController = StreamController<CallState>.broadcast();
  Stream<CallState> get stateStream => _stateController.stream;

  CallState _currentState = CallState.initializing;
  bool _isMuted = false;
  bool _isSpeakerOn = false;

  CallManager({
    required this.socket,
    required this.callId,
  });

  Future<void> initialize() async {
    // Create peer connection
    final config = {
      'iceServers': [
        {'urls': 'stun:stun.dartwing.com:3478'},
        {
          'urls': 'turn:turn.dartwing.com:3478',
          'username': 'dartwing',
          'credential': 'turnpassword',
        },
      ],
    };

    _peerConnection = await createPeerConnection(config);

    // Set up event handlers
    _peerConnection!.onIceCandidate = (candidate) {
      socket.emit('ice_candidate', {
        'call_id': callId,
        'candidate': candidate.toMap(),
      });
    };

    _peerConnection!.onTrack = (event) {
      if (event.streams.isNotEmpty) {
        _remoteStream = event.streams[0];
        _updateState(CallState.connected);
      }
    };

    _peerConnection!.onConnectionState = (state) {
      switch (state) {
        case RTCPeerConnectionState.RTCPeerConnectionStateConnected:
          _updateState(CallState.connected);
          break;
        case RTCPeerConnectionState.RTCPeerConnectionStateDisconnected:
        case RTCPeerConnectionState.RTCPeerConnectionStateFailed:
          _updateState(CallState.disconnected);
          break;
        default:
          break;
      }
    };

    // Set up socket handlers
    socket.on('sdp_answer', _handleSdpAnswer);
    socket.on('ice_candidate', _handleIceCandidate);
    socket.on('call_ended', _handleCallEnded);
  }

  Future<void> startCall() async {
    _updateState(CallState.connecting);

    // Get local media
    _localStream = await navigator.mediaDevices.getUserMedia({
      'audio': true,
      'video': false,
    });

    // Add tracks to peer connection
    for (var track in _localStream!.getTracks()) {
      await _peerConnection!.addTrack(track, _localStream!);
    }

    // Create and send offer
    final offer = await _peerConnection!.createOffer();
    await _peerConnection!.setLocalDescription(offer);

    socket.emit('sdp_offer', {
      'call_id': callId,
      'sdp': offer.toMap(),
    });

    _updateState(CallState.ringing);
  }

  Future<void> endCall() async {
    socket.emit('leave_call', {'call_id': callId});

    await _cleanup();
    _updateState(CallState.ended);
  }

  Future<void> setMute(bool muted) async {
    _isMuted = muted;
    _localStream?.getAudioTracks().forEach((track) {
      track.enabled = !muted;
    });
  }

  Future<void> setSpeaker(bool enabled) async {
    _isSpeakerOn = enabled;
    // Platform-specific speaker control would go here
  }

  Future<void> sendDtmf(String digits) async {
    final senders = await _peerConnection?.getSenders();
    final audioSender = senders?.firstWhere(
      (s) => s.track?.kind == 'audio',
      orElse: () => throw Exception('No audio sender'),
    );

    // Send DTMF via RTP
    for (var digit in digits.split('')) {
      await audioSender?.dtmfSender?.insertDTMF(digit);
      await Future.delayed(const Duration(milliseconds: 200));
    }
  }

  void _handleSdpAnswer(dynamic data) async {
    final sdp = RTCSessionDescription(
      data['sdp']['sdp'],
      data['sdp']['type'],
    );
    await _peerConnection!.setRemoteDescription(sdp);
  }

  void _handleIceCandidate(dynamic data) async {
    final candidate = RTCIceCandidate(
      data['candidate']['candidate'],
      data['candidate']['sdpMid'],
      data['candidate']['sdpMLineIndex'],
    );
    await _peerConnection!.addCandidate(candidate);
  }

  void _handleCallEnded(dynamic data) async {
    await _cleanup();
    _updateState(CallState.ended);
  }

  Future<void> _cleanup() async {
    _localStream?.getTracks().forEach((track) => track.stop());
    await _localStream?.dispose();
    await _peerConnection?.close();

    socket.off('sdp_answer', _handleSdpAnswer);
    socket.off('ice_candidate', _handleIceCandidate);
    socket.off('call_ended', _handleCallEnded);
  }

  void _updateState(CallState state) {
    _currentState = state;
    _stateController.add(state);
  }

  void dispose() {
    _cleanup();
    _stateController.close();
  }
}

enum CallState {
  initializing,
  connecting,
  ringing,
  connected,
  disconnected,
  ended,
}
```

## 10.6 Provider/Riverpod Integration

```dart
// lib/src/providers/tel_providers.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../client/tel_client.dart';
import '../models/call.dart';

/// Provider for the Tel client instance
final telClientProvider = Provider<TelClient>((ref) {
  final config = ref.watch(telConfigProvider);
  return TelClient(config);
});

/// Provider for Tel configuration
final telConfigProvider = Provider<TelConfig>((ref) {
  throw UnimplementedError('Override this provider with your API key');
});

/// State for active call
class ActiveCallState {
  final Call? call;
  final CallState connectionState;
  final bool isMuted;
  final bool isSpeakerOn;
  final Duration duration;

  const ActiveCallState({
    this.call,
    this.connectionState = CallState.initializing,
    this.isMuted = false,
    this.isSpeakerOn = false,
    this.duration = Duration.zero,
  });

  ActiveCallState copyWith({
    Call? call,
    CallState? connectionState,
    bool? isMuted,
    bool? isSpeakerOn,
    Duration? duration,
  }) {
    return ActiveCallState(
      call: call ?? this.call,
      connectionState: connectionState ?? this.connectionState,
      isMuted: isMuted ?? this.isMuted,
      isSpeakerOn: isSpeakerOn ?? this.isSpeakerOn,
      duration: duration ?? this.duration,
    );
  }
}

/// Notifier for managing active call state
class ActiveCallNotifier extends StateNotifier<ActiveCallState> {
  final TelClient _client;
  CallSession? _session;
  Timer? _durationTimer;

  ActiveCallNotifier(this._client) : super(const ActiveCallState());

  Future<void> startCall(String to, {String? from}) async {
    try {
      _session = await _client.voice.startWebRtcCall(
        to: to,
        from: from,
      );

      state = state.copyWith(
        call: _session!.call,
        connectionState: CallState.connecting,
      );

      // Listen to state changes
      _session!.stateStream.listen((callState) {
        state = state.copyWith(connectionState: callState);

        if (callState == CallState.connected) {
          _startDurationTimer();
        } else if (callState == CallState.ended) {
          _stopDurationTimer();
        }
      });
    } catch (e) {
      state = state.copyWith(connectionState: CallState.ended);
      rethrow;
    }
  }

  Future<void> endCall() async {
    await _session?.hangup();
    _stopDurationTimer();
    state = const ActiveCallState();
  }

  Future<void> toggleMute() async {
    final newMuted = !state.isMuted;
    await _session?.mute(newMuted);
    state = state.copyWith(isMuted: newMuted);
  }

  Future<void> toggleSpeaker() async {
    final newSpeaker = !state.isSpeakerOn;
    await _session?.setSpeaker(newSpeaker);
    state = state.copyWith(isSpeakerOn: newSpeaker);
  }

  Future<void> sendDtmf(String digits) async {
    await _session?.sendDtmf(digits);
  }

  void _startDurationTimer() {
    _durationTimer = Timer.periodic(const Duration(seconds: 1), (_) {
      state = state.copyWith(
        duration: state.duration + const Duration(seconds: 1),
      );
    });
  }

  void _stopDurationTimer() {
    _durationTimer?.cancel();
    _durationTimer = null;
  }

  @override
  void dispose() {
    _stopDurationTimer();
    _session?.hangup();
    super.dispose();
  }
}

/// Provider for active call state
final activeCallProvider = StateNotifierProvider<ActiveCallNotifier, ActiveCallState>((ref) {
  final client = ref.watch(telClientProvider);
  return ActiveCallNotifier(client);
});
```

---

# Section 11: Security & Compliance

## 11.1 Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SECURITY ARCHITECTURE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    AUTHENTICATION LAYER                               │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │  API Keys   │  │  Keycloak   │  │   mTLS      │                  │   │
│  │  │  (Modules)  │  │   (Users)   │  │ (Services)  │                  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│  ┌──────────────────────────────▼───────────────────────────────────────┐   │
│  │                    AUTHORIZATION LAYER                                │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │ Permission  │  │    Rate     │  │     IP      │  │   Feature   │ │   │
│  │  │   Matrix    │  │   Limits    │  │  Whitelist  │  │    Flags    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│  ┌──────────────────────────────▼───────────────────────────────────────┐   │
│  │                    DATA PROTECTION LAYER                              │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  TLS 1.3    │  │  AES-256    │  │   Field     │  │   Key       │ │   │
│  │  │ (Transit)   │  │  (At Rest)  │  │ Encryption  │  │ Management  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│  ┌──────────────────────────────▼───────────────────────────────────────┐   │
│  │                    AUDIT & MONITORING LAYER                           │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │    CDR      │  │   Access    │  │   Anomaly   │  │   SIEM      │ │   │
│  │  │   Logging   │  │    Logs     │  │  Detection  │  │Integration  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 11.2 API Key Security

```python
# dartwing_tel/services/api_key_service.py

import frappe
import secrets
import hashlib
from datetime import datetime, timedelta


class ApiKeyService:
    """Manage TEL API key lifecycle."""

    KEY_PREFIX = "tel_live_"
    KEY_LENGTH = 32  # 256 bits

    @classmethod
    def generate_api_key(cls, module: str, organization: str = None) -> tuple:
        """
        Generate a new API key.

        Returns:
            tuple: (key_prefix, full_key, key_hash)

        The full_key is returned only once and must be stored by the caller.
        Only the key_hash is stored in the database.
        """
        # Generate random key
        random_bytes = secrets.token_bytes(cls.KEY_LENGTH)
        key_suffix = secrets.token_hex(cls.KEY_LENGTH)
        full_key = f"{cls.KEY_PREFIX}{key_suffix}"

        # Create prefix for identification
        key_prefix = full_key[:12]  # tel_live_xxxx

        # Hash for storage
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()

        return key_prefix, full_key, key_hash

    @classmethod
    def validate_api_key(cls, provided_key: str) -> dict:
        """
        Validate an API key and return the associated record.

        Raises:
            frappe.AuthenticationError: If key is invalid
        """
        if not provided_key.startswith(cls.KEY_PREFIX):
            raise frappe.AuthenticationError("Invalid API key format")

        key_prefix = provided_key[:12]
        provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()

        # Fetch key record
        api_key = frappe.db.get_value(
            "TEL API Key",
            {"key_prefix": key_prefix, "status": "Active"},
            ["name", "key_hash", "module", "organization", "permissions",
             "rate_limits", "ip_whitelist"],
            as_dict=True
        )

        if not api_key:
            raise frappe.AuthenticationError("Invalid or inactive API key")

        # Constant-time comparison
        if not secrets.compare_digest(provided_hash, api_key.key_hash):
            raise frappe.AuthenticationError("Invalid API key")

        # Update last used
        frappe.db.set_value(
            "TEL API Key",
            api_key.name,
            "last_used_at",
            datetime.utcnow(),
            update_modified=False
        )

        return api_key

    @classmethod
    def rotate_api_key(cls, api_key_name: str) -> tuple:
        """
        Rotate an API key, generating a new one.

        The old key remains valid for a grace period (24 hours).
        """
        api_key = frappe.get_doc("TEL API Key", api_key_name)

        # Store old hash with expiry
        frappe.cache().set_value(
            f"tel_old_key:{api_key.key_hash}",
            api_key_name,
            expires_in_sec=86400  # 24 hours
        )

        # Generate new key
        key_prefix, full_key, key_hash = cls.generate_api_key(
            api_key.module,
            api_key.organization
        )

        # Update record
        api_key.key_prefix = key_prefix
        api_key.key_hash = key_hash
        api_key.save(ignore_permissions=True)

        return key_prefix, full_key

    @classmethod
    def revoke_api_key(cls, api_key_name: str):
        """Revoke an API key immediately."""
        frappe.db.set_value("TEL API Key", api_key_name, "status", "Revoked")
```

## 11.3 Rate Limiting Implementation

```python
# dartwing_tel/services/rate_limiter.py

import frappe
import redis
import time


class RateLimiter:
    """Token bucket rate limiter using Redis."""

    def __init__(self):
        self.redis = frappe.cache()

    def check(self, key: str, limits: dict) -> bool:
        """
        Check if request is within rate limits.

        Args:
            key: Rate limit key (e.g., "tel:sms:API-KEY-001")
            limits: {per_second: int, per_minute: int, per_day: int}

        Returns:
            bool: True if allowed, False if rate limited
        """
        current_time = int(time.time())

        # Check per-second limit
        if limits.get("per_second"):
            second_key = f"{key}:second:{current_time}"
            count = self.redis.incr(second_key)
            self.redis.expire(second_key, 2)

            if count > limits["per_second"]:
                return False

        # Check per-minute limit
        if limits.get("per_minute"):
            minute = current_time // 60
            minute_key = f"{key}:minute:{minute}"
            count = self.redis.incr(minute_key)
            self.redis.expire(minute_key, 120)

            if count > limits["per_minute"]:
                return False

        # Check per-day limit
        if limits.get("per_day"):
            day = current_time // 86400
            day_key = f"{key}:day:{day}"
            count = self.redis.incr(day_key)
            self.redis.expire(day_key, 172800)

            if count > limits["per_day"]:
                return False

        return True

    def get_remaining(self, key: str, limits: dict) -> dict:
        """Get remaining requests for each window."""
        current_time = int(time.time())
        remaining = {}

        if limits.get("per_second"):
            second_key = f"{key}:second:{current_time}"
            used = int(self.redis.get(second_key) or 0)
            remaining["per_second"] = max(0, limits["per_second"] - used)

        if limits.get("per_minute"):
            minute = current_time // 60
            minute_key = f"{key}:minute:{minute}"
            used = int(self.redis.get(minute_key) or 0)
            remaining["per_minute"] = max(0, limits["per_minute"] - used)

        if limits.get("per_day"):
            day = current_time // 86400
            day_key = f"{key}:day:{day}"
            used = int(self.redis.get(day_key) or 0)
            remaining["per_day"] = max(0, limits["per_day"] - used)

        return remaining

    def get_rate_limit_headers(self, key: str, limits: dict) -> dict:
        """Generate rate limit headers for response."""
        remaining = self.get_remaining(key, limits)
        current_time = int(time.time())

        # Use the most restrictive limit for headers
        if limits.get("per_second"):
            return {
                "X-RateLimit-Limit": str(limits["per_second"]),
                "X-RateLimit-Remaining": str(remaining.get("per_second", 0)),
                "X-RateLimit-Reset": str(current_time + 1)
            }
        elif limits.get("per_minute"):
            reset_time = (current_time // 60 + 1) * 60
            return {
                "X-RateLimit-Limit": str(limits["per_minute"]),
                "X-RateLimit-Remaining": str(remaining.get("per_minute", 0)),
                "X-RateLimit-Reset": str(reset_time)
            }

        return {}
```

## 11.4 HIPAA Compliance

```python
# dartwing_tel/services/hipaa_service.py

import frappe
from cryptography.fernet import Fernet
import base64
import hashlib


class HipaaService:
    """HIPAA compliance utilities for PHI handling."""

    @staticmethod
    def encrypt_phi(data: str, organization: str = None) -> str:
        """
        Encrypt Protected Health Information (PHI).

        Uses organization-specific keys when available,
        falls back to system key.
        """
        key = HipaaService._get_encryption_key(organization)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def decrypt_phi(encrypted_data: str, organization: str = None) -> str:
        """Decrypt PHI data."""
        key = HipaaService._get_encryption_key(organization)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(base64.b64decode(encrypted_data))
        return decrypted.decode()

    @staticmethod
    def _get_encryption_key(organization: str = None) -> bytes:
        """Get encryption key for organization or system default."""
        if organization:
            key = frappe.db.get_value(
                "Organization",
                organization,
                "hipaa_encryption_key"
            )
            if key:
                return base64.b64decode(key)

        # System default key
        return base64.b64decode(
            frappe.get_single("TEL Settings").hipaa_encryption_key
        )

    @staticmethod
    def log_phi_access(
        doctype: str,
        docname: str,
        action: str,
        user: str = None,
        reason: str = None
    ):
        """Log access to PHI for audit trail."""
        frappe.get_doc({
            "doctype": "TEL Audit Log",
            "log_type": "PHI Access",
            "reference_doctype": doctype,
            "reference_name": docname,
            "action": action,
            "user": user or frappe.session.user,
            "reason": reason,
            "ip_address": frappe.local.request_ip,
            "timestamp": frappe.utils.now_datetime()
        }).insert(ignore_permissions=True)

    @staticmethod
    def check_baa_status(organization: str) -> bool:
        """Check if organization has active BAA on file."""
        baa = frappe.db.get_value(
            "TEL BAA Agreement",
            {
                "organization": organization,
                "status": "Active",
                "expires_on": [">", frappe.utils.today()]
            }
        )
        return bool(baa)

    @staticmethod
    def validate_hipaa_request(api_key: str, data: dict):
        """
        Validate HIPAA mode request.

        Raises:
            frappe.ValidationError: If HIPAA requirements not met
        """
        api_key_doc = frappe.get_doc("TEL API Key", api_key)

        if not api_key_doc.organization:
            frappe.throw("HIPAA mode requires organization assignment")

        if not HipaaService.check_baa_status(api_key_doc.organization):
            frappe.throw("Active BAA required for HIPAA mode")

        # Check for PHI patterns in message body
        if "body" in data:
            HipaaService._detect_phi_patterns(data["body"])

    @staticmethod
    def _detect_phi_patterns(text: str):
        """Detect potential PHI patterns and log warning."""
        import re

        patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "mrn": r"\bMRN[:\s]?\d+\b",
            "dob": r"\bDOB[:\s]?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        }

        for phi_type, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                frappe.log_error(
                    f"Potential {phi_type.upper()} detected in message",
                    "PHI Detection Warning"
                )
```

## 11.5 Compliance Matrix

| Requirement     | Implementation                                                 | Status         |
| --------------- | -------------------------------------------------------------- | -------------- |
| **STIR/SHAKEN** | Automatic A-level attestation on all outbound calls            | ✅ Active      |
| **10DLC**       | Campaign registration API, throughput enforcement              | ✅ Active      |
| **TCPA**        | Consent records, quiet hours (9 PM - 8 AM local), DNC checking | ✅ Active      |
| **E911**        | Address registration, PSAP routing, callback verification      | ✅ Active      |
| **HIPAA**       | PHI encryption, access logging, BAA tracking                   | ✅ Active      |
| **GDPR**        | Data export, deletion, consent management                      | ✅ Active      |
| **SOC 2**       | Access controls, audit logs, encryption                        | 🔄 In Progress |
| **PCI DSS**     | Payment IVR isolation, no card storage                         | ✅ Active      |

## 11.6 STIR/SHAKEN Implementation

```csharp
// Dartwing.Tel.VoiceGateway/Services/StirShakenService.cs

using System.Security.Cryptography;
using System.Text.Json;
using Microsoft.IdentityModel.Tokens;

namespace Dartwing.Tel.VoiceGateway.Services;

public class StirShakenService
{
    private readonly ECDsa _signingKey;
    private readonly string _certificateUrl;
    private readonly INumberOwnershipService _ownershipService;

    public async Task<string> GenerateIdentityHeader(
        string callingNumber,
        string calledNumber,
        string callId)
    {
        // Determine attestation level
        var attestation = await DetermineAttestationAsync(callingNumber);

        // Create PASSporT header
        var header = new
        {
            alg = "ES256",
            typ = "passport",
            ppt = "shaken",
            x5u = _certificateUrl
        };

        // Create PASSporT payload
        var origId = Guid.NewGuid().ToString();
        var iat = DateTimeOffset.UtcNow.ToUnixTimeSeconds();

        var payload = new
        {
            attest = attestation,
            dest = new { tn = new[] { calledNumber.TrimStart('+') } },
            iat = iat,
            orig = new { tn = callingNumber.TrimStart('+') },
            origid = origId
        };

        // Encode and sign
        var headerB64 = Base64UrlEncoder.Encode(JsonSerializer.SerializeToUtf8Bytes(header));
        var payloadB64 = Base64UrlEncoder.Encode(JsonSerializer.SerializeToUtf8Bytes(payload));

        var dataToSign = $"{headerB64}.{payloadB64}";
        var signature = _signingKey.SignData(
            Encoding.UTF8.GetBytes(dataToSign),
            HashAlgorithmName.SHA256);
        var signatureB64 = Base64UrlEncoder.Encode(signature);

        var token = $"{headerB64}.{payloadB64}.{signatureB64}";

        // Format as Identity header
        return $"{token};info=<{_certificateUrl}>;alg=ES256;ppt=shaken";
    }

    private async Task<string> DetermineAttestationAsync(string callingNumber)
    {
        // A = Full attestation: We are the service provider and can verify the caller
        // B = Partial attestation: We know the customer but can't verify specific number
        // C = Gateway attestation: Call entered our network from another provider

        var ownership = await _ownershipService.CheckOwnershipAsync(callingNumber);

        return ownership switch
        {
            NumberOwnership.Owned => "A",
            NumberOwnership.Customer => "B",
            _ => "C"
        };
    }
}
```

---

# Section 12: Deployment Architecture

## 12.1 Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    KUBERNETES CLUSTER                                 │   │
│  │                                                                       │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    INGRESS LAYER                              │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │   NGINX     │  │   Cert      │  │   WAF       │          │   │   │
│  │  │  │   Ingress   │  │  Manager    │  │  (ModSec)   │          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    APPLICATION LAYER                          │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │   Frappe    │  │   Frappe    │  │   Frappe    │          │   │   │
│  │  │  │   Web (3x)  │  │  Worker(5x) │  │ Scheduler   │          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │   Voice     │  │    SMS      │  │    Fax      │          │   │   │
│  │  │  │ Gateway(3x) │  │  Router(3x) │  │Processor(2x)│          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │  Routing    │  │   Webhook   │  │    CDR      │          │   │   │
│  │  │  │ Engine(2x)  │  │ Delivery(3x)│  │ Indexer(2x) │          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    SIP/MEDIA LAYER                            │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │  Kamailio   │  │  Kamailio   │  │   TURN/     │          │   │   │
│  │  │  │  SBC (3x)   │  │  RTP Proxy  │  │   STUN      │          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    DATA LAYER                                 │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │   │
│  │  │  │  MariaDB    │  │   Redis     │  │  RabbitMQ   │          │   │   │
│  │  │  │  (Galera)   │  │  Sentinel   │  │   Cluster   │          │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │   │
│  │  │                                                               │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐                           │   │   │
│  │  │  │ OpenSearch  │  │    MinIO    │                           │   │   │
│  │  │  │  Cluster    │  │  (S3-compat)│                           │   │   │
│  │  │  └─────────────┘  └─────────────┘                           │   │   │
│  │  │                                                               │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 12.2 Kubernetes Manifests

### Frappe Deployment

```yaml
# k8s/frappe/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: dartwing-tel-web
  namespace: dartwing-tel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dartwing-tel-web
  template:
    metadata:
      labels:
        app: dartwing-tel-web
    spec:
      containers:
        - name: frappe
          image: dartwing/tel-frappe:latest
          ports:
            - containerPort: 8000
          env:
            - name: FRAPPE_SITE_NAME
              value: "tel.dartwing.com"
            - name: REDIS_CACHE
              valueFrom:
                secretKeyRef:
                  name: dartwing-tel-secrets
                  key: redis-cache-url
            - name: REDIS_QUEUE
              valueFrom:
                secretKeyRef:
                  name: dartwing-tel-secrets
                  key: redis-queue-url
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: dartwing-tel-secrets
                  key: db-host
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
          livenessProbe:
            httpGet:
              path: /api/method/ping
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /api/method/ping
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: sites
              mountPath: /home/frappe/frappe-bench/sites
      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: frappe-sites-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: dartwing-tel-web
  namespace: dartwing-tel
spec:
  selector:
    app: dartwing-tel-web
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP
```

### Voice Gateway Deployment

```yaml
# k8s/voice-gateway/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: tel-voice-gateway
  namespace: dartwing-tel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tel-voice-gateway
  template:
    metadata:
      labels:
        app: tel-voice-gateway
    spec:
      containers:
        - name: voice-gateway
          image: dartwing/tel-voice-gateway:latest
          ports:
            - containerPort: 5001
              name: grpc
            - containerPort: 5060
              name: sip-udp
              protocol: UDP
            - containerPort: 5061
              name: sip-tls
          env:
            - name: ASPNETCORE_ENVIRONMENT
              value: "Production"
            - name: ConnectionStrings__Redis
              valueFrom:
                secretKeyRef:
                  name: dartwing-tel-secrets
                  key: redis-url
            - name: RabbitMQ__Host
              valueFrom:
                secretKeyRef:
                  name: dartwing-tel-secrets
                  key: rabbitmq-host
            - name: Kamailio__Host
              value: "kamailio-sbc"
          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "2000m"
          livenessProbe:
            grpc:
              port: 5001
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            grpc:
              port: 5001
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: tel-voice-gateway
  namespace: dartwing-tel
spec:
  selector:
    app: tel-voice-gateway
  ports:
    - port: 5001
      targetPort: 5001
      name: grpc
    - port: 5060
      targetPort: 5060
      protocol: UDP
      name: sip-udp
    - port: 5061
      targetPort: 5061
      name: sip-tls
  type: ClusterIP
```

### Kamailio SBC Deployment

```yaml
# k8s/kamailio/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: kamailio-sbc
  namespace: dartwing-tel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kamailio-sbc
  template:
    metadata:
      labels:
        app: kamailio-sbc
    spec:
      hostNetwork: true # Required for SIP
      dnsPolicy: ClusterFirstWithHostNet
      containers:
        - name: kamailio
          image: dartwing/kamailio:5.7
          ports:
            - containerPort: 5060
              protocol: UDP
              hostPort: 5060
            - containerPort: 5060
              protocol: TCP
              hostPort: 5060
            - containerPort: 5061
              protocol: TCP
              hostPort: 5061
          env:
            - name: KAMAILIO_SHM_MEMORY
              value: "256"
            - name: KAMAILIO_PKG_MEMORY
              value: "32"
          resources:
            requests:
              memory: "512Mi"
              cpu: "1000m"
            limits:
              memory: "2Gi"
              cpu: "4000m"
          volumeMounts:
            - name: config
              mountPath: /etc/kamailio
            - name: tls
              mountPath: /etc/kamailio/tls
      volumes:
        - name: config
          configMap:
            name: kamailio-config
        - name: tls
          secret:
            secretName: kamailio-tls
---
apiVersion: v1
kind: Service
metadata:
  name: kamailio-sbc
  namespace: dartwing-tel
  annotations:
    metallb.universe.tf/allow-shared-ip: "sip-pool"
spec:
  type: LoadBalancer
  loadBalancerIP: 203.0.113.10 # Static IP for SIP
  selector:
    app: kamailio-sbc
  ports:
    - port: 5060
      targetPort: 5060
      protocol: UDP
      name: sip-udp
    - port: 5060
      targetPort: 5060
      protocol: TCP
      name: sip-tcp
    - port: 5061
      targetPort: 5061
      protocol: TCP
      name: sip-tls
```

## 12.3 Horizontal Pod Autoscaling

```yaml
# k8s/hpa/voice-gateway-hpa.yaml

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: tel-voice-gateway-hpa
  namespace: dartwing-tel
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: tel-voice-gateway
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: active_calls
        target:
          type: AverageValue
          averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 2
          periodSeconds: 120
```

## 12.4 Database Configuration

### MariaDB Galera Cluster

```yaml
# k8s/mariadb/statefulset.yaml

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mariadb-galera
  namespace: dartwing-tel
spec:
  serviceName: mariadb-galera
  replicas: 3
  selector:
    matchLabels:
      app: mariadb-galera
  template:
    metadata:
      labels:
        app: mariadb-galera
    spec:
      containers:
        - name: mariadb
          image: mariadb:10.6
          ports:
            - containerPort: 3306
              name: mysql
            - containerPort: 4567
              name: galera-repl
            - containerPort: 4568
              name: galera-ist
            - containerPort: 4444
              name: galera-sst
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mariadb-secrets
                  key: root-password
            - name: WSREP_CLUSTER_ADDRESS
              value: "gcomm://mariadb-galera-0.mariadb-galera,mariadb-galera-1.mariadb-galera,mariadb-galera-2.mariadb-galera"
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
            - name: config
              mountPath: /etc/mysql/conf.d
          resources:
            requests:
              memory: "2Gi"
              cpu: "1000m"
            limits:
              memory: "8Gi"
              cpu: "4000m"
      volumes:
        - name: config
          configMap:
            name: mariadb-config
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 100Gi
```

---

# Section 13: Operational Runbooks

## 13.1 Incident Response Procedures

### Carrier Failover Incident

````markdown
# Runbook: Carrier Failover Incident

## Trigger

- Carrier health score drops below 50%
- Error rate exceeds 5% for 5 minutes
- Alert: "tel-carrier-degraded"

## Severity

- P1 if primary carrier (Telnyx)
- P2 if secondary carrier

## Response Steps

1. **Acknowledge Alert** (within 5 minutes)

   - Acknowledge in PagerDuty
   - Join #tel-incidents Slack channel

2. **Verify Failover** (within 10 minutes)

   ```bash
   # Check current routing
   kubectl exec -it deploy/tel-routing-engine -- \
     curl localhost:5006/health/carriers

   # Verify traffic shifted
   kubectl logs -l app=tel-sms-router --since=5m | \
     grep "carrier=" | sort | uniq -c
   ```
````

3. **Confirm Impact**

   - Check SMS delivery rates in Grafana
   - Check voice call success rates
   - Review error logs for patterns

4. **Manual Override (if needed)**

   ```bash
   # Force disable carrier
   kubectl exec -it deploy/tel-routing-engine -- \
     curl -X POST localhost:5006/admin/carriers/telnyx/disable

   # Or adjust weights
   kubectl exec -it deploy/tel-routing-engine -- \
     curl -X POST localhost:5006/admin/carriers/telnyx/weight \
       -d '{"weight": 0}'
   ```

5. **Monitor Recovery**

   - Watch carrier health dashboard
   - Re-enable when error rate < 1% for 10 minutes

   ```bash
   kubectl exec -it deploy/tel-routing-engine -- \
     curl -X POST localhost:5006/admin/carriers/telnyx/enable
   ```

6. **Post-Incident**
   - Create incident report
   - Update carrier health thresholds if needed
   - Review failover timing

````

### High Call Volume Incident

```markdown
# Runbook: High Call Volume / Capacity Alert

## Trigger
- Active calls > 80% of capacity
- Call queue depth > 100
- Alert: "tel-capacity-warning"

## Response Steps

1. **Scale Voice Gateway**
   ```bash
   # Check current replicas
   kubectl get hpa tel-voice-gateway-hpa

   # Manual scale if HPA too slow
   kubectl scale deployment tel-voice-gateway --replicas=15
````

2. **Check Kamailio Load**

   ```bash
   # Get dispatcher stats
   kubectl exec -it deploy/kamailio-sbc -- \
     kamcmd dispatcher.list

   # Check active dialogs
   kubectl exec -it deploy/kamailio-sbc -- \
     kamcmd dlg.list
   ```

3. **Enable Rate Limiting**

   ```bash
   # Reduce per-module limits temporarily
   kubectl exec -it deploy/dartwing-tel-web -- \
     bench --site tel.dartwing.com execute \
       dartwing_tel.admin.set_emergency_limits
   ```

4. **Monitor Queue Depth**

   ```bash
   # RabbitMQ queue status
   kubectl exec -it statefulset/rabbitmq -- \
     rabbitmqctl list_queues name messages
   ```

5. **Scale Back After Peak**
   - Wait for call volume to stabilize
   - Let HPA handle scale-down
   - Remove emergency rate limits

````

## 13.2 Health Check Scripts

```python
# scripts/health_check.py

import requests
import sys
from datetime import datetime


class TelHealthChecker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []

    def check_frappe_api(self):
        """Check Frappe API health."""
        try:
            r = requests.get(f"{self.base_url}/api/method/ping", timeout=5)
            self.results.append({
                "service": "frappe-api",
                "status": "healthy" if r.status_code == 200 else "degraded",
                "latency_ms": r.elapsed.total_seconds() * 1000
            })
        except Exception as e:
            self.results.append({
                "service": "frappe-api",
                "status": "unhealthy",
                "error": str(e)
            })

    def check_voice_gateway(self):
        """Check Voice Gateway gRPC health."""
        try:
            import grpc
            from grpc_health.v1 import health_pb2, health_pb2_grpc

            channel = grpc.insecure_channel("tel-voice-gateway:5001")
            stub = health_pb2_grpc.HealthStub(channel)
            response = stub.Check(health_pb2.HealthCheckRequest())

            self.results.append({
                "service": "voice-gateway",
                "status": "healthy" if response.status == 1 else "unhealthy"
            })
        except Exception as e:
            self.results.append({
                "service": "voice-gateway",
                "status": "unhealthy",
                "error": str(e)
            })

    def check_carriers(self):
        """Check carrier connectivity."""
        carriers = ["telnyx", "bandwidth", "sinch"]

        for carrier in carriers:
            try:
                r = requests.get(
                    f"{self.base_url}/api/method/dartwing_tel.admin.carrier_health",
                    params={"carrier": carrier},
                    timeout=10
                )
                data = r.json().get("message", {})
                self.results.append({
                    "service": f"carrier-{carrier}",
                    "status": "healthy" if data.get("health_score", 0) > 80 else "degraded",
                    "health_score": data.get("health_score")
                })
            except Exception as e:
                self.results.append({
                    "service": f"carrier-{carrier}",
                    "status": "unknown",
                    "error": str(e)
                })

    def check_database(self):
        """Check MariaDB connectivity."""
        try:
            r = requests.get(
                f"{self.base_url}/api/method/dartwing_tel.admin.db_health",
                timeout=5
            )
            self.results.append({
                "service": "mariadb",
                "status": "healthy" if r.status_code == 200 else "unhealthy"
            })
        except Exception as e:
            self.results.append({
                "service": "mariadb",
                "status": "unhealthy",
                "error": str(e)
            })

    def check_redis(self):
        """Check Redis connectivity."""
        try:
            r = requests.get(
                f"{self.base_url}/api/method/dartwing_tel.admin.redis_health",
                timeout=5
            )
            self.results.append({
                "service": "redis",
                "status": "healthy" if r.status_code == 200 else "unhealthy"
            })
        except Exception as e:
            self.results.append({
                "service": "redis",
                "status": "unhealthy",
                "error": str(e)
            })

    def run_all_checks(self):
        """Run all health checks."""
        self.check_frappe_api()
        self.check_voice_gateway()
        self.check_carriers()
        self.check_database()
        self.check_redis()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": self._calculate_overall_status(),
            "checks": self.results
        }

    def _calculate_overall_status(self):
        statuses = [r["status"] for r in self.results]
        if all(s == "healthy" for s in statuses):
            return "healthy"
        elif any(s == "unhealthy" for s in statuses):
            return "unhealthy"
        return "degraded"


if __name__ == "__main__":
    checker = TelHealthChecker("https://api.dartwing.com")
    result = checker.run_all_checks()

    import json
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["overall_status"] == "healthy" else 1)
````

## 13.3 Monitoring & Alerting

### Prometheus Alerts

```yaml
# prometheus/tel-alerts.yaml

groups:
  - name: dartwing-tel
    rules:
      # SMS delivery rate alert
      - alert: TelSmsDeliveryRateLow
        expr: |
          (
            sum(rate(tel_sms_delivered_total[5m])) /
            sum(rate(tel_sms_sent_total[5m]))
          ) < 0.95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "SMS delivery rate below 95%"
          description: "SMS delivery rate is {{ $value | humanizePercentage }}"

      # Voice call failure alert
      - alert: TelVoiceFailureRateHigh
        expr: |
          (
            sum(rate(tel_voice_failed_total[5m])) /
            sum(rate(tel_voice_initiated_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Voice call failure rate above 5%"
          description: "Voice failure rate is {{ $value | humanizePercentage }}"

      # Carrier health alert
      - alert: TelCarrierDegraded
        expr: tel_carrier_health_score < 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Carrier {{ $labels.carrier }} health degraded"
          description: "Health score: {{ $value }}"

      # Active calls capacity alert
      - alert: TelHighCallVolume
        expr: tel_active_calls_total > 40000
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High active call volume"
          description: "{{ $value }} active calls (80% capacity)"

      # API latency alert
      - alert: TelApiLatencyHigh
        expr: |
          histogram_quantile(0.95, 
            sum(rate(tel_api_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API P95 latency above 500ms"
          description: "P95 latency: {{ $value | humanizeDuration }}"
```

---

# Section 14: Appendices

## Appendix A: Error Codes Reference

| Code    | Category   | Description                 | HTTP Status |
| ------- | ---------- | --------------------------- | ----------- |
| TEL-001 | Validation | Invalid phone number format | 400         |
| TEL-002 | Delivery   | Number not reachable        | 422         |
| TEL-003 | Rate Limit | Rate limit exceeded         | 429         |
| TEL-004 | Billing    | Insufficient balance        | 402         |
| TEL-005 | Auth       | Permission denied           | 403         |
| TEL-006 | Carrier    | Carrier error               | 502         |
| TEL-007 | Timeout    | Operation timeout           | 504         |
| TEL-008 | Auth       | Invalid API key             | 401         |
| TEL-009 | Config     | Feature not enabled         | 403         |
| TEL-010 | Compliance | Compliance block            | 403         |
| TEL-101 | SMS        | Invalid sender ID           | 400         |
| TEL-102 | SMS        | Content blocked             | 403         |
| TEL-103 | SMS        | DNC list match              | 403         |
| TEL-201 | Voice      | Call failed                 | 502         |
| TEL-202 | Voice      | Busy                        | 486         |
| TEL-203 | Voice      | No answer                   | 480         |
| TEL-204 | Voice      | Rejected                    | 603         |
| TEL-301 | Fax        | Negotiation failed          | 502         |
| TEL-302 | Fax        | Transmission error          | 502         |
| TEL-303 | Fax        | Invalid document            | 400         |
| TEL-401 | Number     | Not available               | 404         |
| TEL-402 | Number     | Port rejected               | 422         |
| TEL-501 | E911       | Invalid address             | 400         |
| TEL-502 | E911       | PSAP unreachable            | 503         |

## Appendix B: Webhook Event Types

| Event                      | Description              | Payload                    |
| -------------------------- | ------------------------ | -------------------------- |
| `sms.queued`               | SMS queued for delivery  | message_id, to, from       |
| `sms.sent`                 | SMS sent to carrier      | message_id, carrier        |
| `sms.delivered`            | SMS delivered            | message_id, delivered_at   |
| `sms.failed`               | SMS delivery failed      | message_id, error_code     |
| `sms.received`             | Inbound SMS received     | message_id, from, to, body |
| `call.initiated`           | Call started             | call_id, from, to          |
| `call.ringing`             | Call ringing             | call_id                    |
| `call.answered`            | Call answered            | call_id, answered_at       |
| `call.completed`           | Call ended               | call_id, duration, cost    |
| `call.failed`              | Call failed              | call_id, error_code        |
| `call.recording.ready`     | Recording available      | call_id, recording_url     |
| `call.transcription.ready` | Transcription complete   | call_id, text              |
| `fax.queued`               | Fax queued               | fax_id, page_count         |
| `fax.sending`              | Fax transmission started | fax_id                     |
| `fax.delivered`            | Fax delivered            | fax_id, pages_sent         |
| `fax.failed`               | Fax failed               | fax_id, error_code         |
| `fax.received`             | Inbound fax              | fax_id, from, pdf_url      |
| `number.provisioned`       | Number activated         | phone_number               |
| `number.released`          | Number released          | phone_number               |
| `port.submitted`           | Port request submitted   | port_id                    |
| `port.completed`           | Port completed           | port_id, phone_number      |
| `reputation.alert`         | Number reputation issue  | phone_number, score        |

## Appendix C: Rate Limit Tiers

| Tier       | SMS/sec | SMS/day | Voice/sec | Voice concurrent | Fax/min |
| ---------- | ------- | ------- | --------- | ---------------- | ------- |
| Starter    | 1       | 1,000   | 1         | 5                | 1       |
| Growth     | 10      | 10,000  | 5         | 50               | 5       |
| Business   | 50      | 100,000 | 20        | 200              | 20      |
| Enterprise | 100     | 500,000 | 50        | 1,000            | 50      |
| Unlimited  | Custom  | Custom  | Custom    | Custom           | Custom  |

## Appendix D: Carrier Capabilities Matrix

| Capability  | Telnyx | Bandwidth | Sinch | DIDWW |
| ----------- | ------ | --------- | ----- | ----- |
| SMS         | ✅     | ✅        | ✅    | ❌    |
| MMS         | ✅     | ✅        | ✅    | ❌    |
| Voice       | ✅     | ✅        | ✅    | ✅    |
| Fax/T.38    | ✅     | ❌        | ❌    | ❌    |
| Numbers     | ✅     | ✅        | ❌    | ✅    |
| Toll-Free   | ✅     | ✅        | ❌    | ✅    |
| E911        | ✅     | ✅        | ❌    | ❌    |
| STIR/SHAKEN | ✅     | ✅        | ✅    | ✅    |
| 10DLC       | ✅     | ✅        | ✅    | ❌    |
| US Coverage | ✅     | ✅        | ✅    | ✅    |
| CA Coverage | ✅     | ✅        | ✅    | ✅    |
| UK Coverage | ✅     | ❌        | ✅    | ✅    |
| EU Coverage | ✅     | ❌        | ✅    | ✅    |

## Appendix E: Glossary

| Term            | Definition                                               |
| --------------- | -------------------------------------------------------- |
| **10DLC**       | 10-Digit Long Code - US A2P SMS registration requirement |
| **AML**         | Advanced Mobile Location - Emergency location service    |
| **CDR**         | Call Detail Record - Detailed log of telephony events    |
| **CNAM**        | Caller ID Name - Display name for caller ID              |
| **DID**         | Direct Inward Dialing - Individual phone number          |
| **DNC**         | Do Not Call - List of opted-out phone numbers            |
| **E.164**       | International phone number format (+1XXXXXXXXXX)         |
| **E911**        | Enhanced 911 - Location-enabled emergency calling        |
| **FoIP**        | Fax over IP - Digital fax transmission                   |
| **gRPC**        | Google Remote Procedure Call - Binary RPC protocol       |
| **GSM-7**       | 7-bit character encoding for SMS (160 chars)             |
| **IVR**         | Interactive Voice Response - Automated phone menu        |
| **LCR**         | Least Cost Routing - Cost-optimized carrier selection    |
| **MOS**         | Mean Opinion Score - Voice quality metric (1-5)          |
| **NG911**       | Next Generation 911 - IP-based emergency services        |
| **PSAP**        | Public Safety Answering Point - 911 call center          |
| **SBC**         | Session Border Controller - SIP security/routing         |
| **SIP**         | Session Initiation Protocol - VoIP signaling             |
| **SMPP**        | Short Message Peer-to-Peer - SMS protocol                |
| **STIR/SHAKEN** | Call authentication standard for caller ID               |
| **T.38**        | ITU standard for real-time fax over IP                   |
| **TCPA**        | Telephone Consumer Protection Act - US SMS regulations   |
| **TTS**         | Text-to-Speech - Synthetic voice generation              |
| **UCS-2**       | 16-bit character encoding for SMS (70 chars)             |
| **WebRTC**      | Web Real-Time Communication - Browser-based voice/video  |

---

_End of Document_

---

## Document Summary

| Section | Title                 | Key Content                                            |
| ------- | --------------------- | ------------------------------------------------------ |
| 1       | System Overview       | Architecture philosophy, tech stack, design principles |
| 2       | System Architecture   | High-level diagrams, request flows, service boundaries |
| 3       | Data Model            | 20+ Frappe DocTypes with JSON schemas                  |
| 4       | Service Architecture  | Frappe module structure, .NET microservices, gRPC      |
| 5       | Carrier Integration   | Routing engine, Kamailio SBC, health monitoring        |
| 6       | Voice Pipeline        | WebRTC, SIP, recording service, call state             |
| 7       | SMS & Messaging       | SMS processor, inbound handling, batch processing      |
| 8       | Fax Architecture      | PDF processing, T.38, cover pages, OCR                 |
| 9       | API Design            | Endpoint reference, request/response examples          |
| 10      | Flutter SDK           | Client architecture, WebRTC integration, Riverpod      |
| 11      | Security & Compliance | API keys, rate limiting, HIPAA, STIR/SHAKEN            |
| 12      | Deployment            | Kubernetes manifests, HPA, database config             |
| 13      | Operational Runbooks  | Incident response, health checks, monitoring           |
| 14      | Appendices            | Error codes, webhook events, glossary                  |

**Total Features Supported:** 78 (from PRD)
**Total API Endpoints:** 52
**Technology Stack:** Frappe + .NET Core + Kamailio + Flutter
