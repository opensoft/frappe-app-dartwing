**DartwingFax – Technical Specification & Implementation Detail**  
**Version:** 1.1-TechSpec  
**Date:** November 26, 2025  
**Purpose:** This document translates every PRD feature into concrete technical requirements, APIs, data models, processing rules, latencies, and third-party dependencies.

## Module A: AI-Powered Intelligent Fax Routing

| Sub-feature            | Technical Implementation Details                                                                                                                                                                                           |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A.1 OCR/ICR            | Tesseract 5.4 + ABBYY FineReader SDK fallback for handwritten; run in parallel, pick highest confidence. Output: plain text + hOCR bounding boxes.                                                                         |
| A.2 NLP Classification | Fine-tuned DistilBERT / MiniLM model (12 categories at launch). Confidence threshold configurable 50–95%. Hosted on AWS SageMaker multi-model endpoint.                                                                    |
| A.3 Entity Extraction  | SpaCy large model + custom regex post-processor. Entities: NAME, ORG, INVOICE#, AMOUNT, DATE, POLICY#, CUSTOMER_ID, PHONE, EMAIL. Output JSON stored in fax record.                                                        |
| A.4 AI Routing Engine  | Rule engine (Drools or custom) that takes AI category + entities + staff directory (LDAP/SCIM sync) + current workload (active fax count per user). Returns owner_id + confidence %. <70% → route to “human_review_queue”. |
| A.5 Hard Route Rules   | JSON-based rule DSL stored in PostgreSQL. Evaluated in order: 1. Blacklist/Whitelist → 2. Hard rules → 3. AI routing. Supports wildcards (\*, ?), regex, time windows (cron).                                              |
| A.6 Advanced Actions   | Webhook: POST JSON payload (fax metadata + extracted entities) with retry (exponential backoff 5×). Task creation via direct REST APIs of Jira/Asana/Zendesk with OAuth2 tokens per customer.                              |
| Latency Requirement    | Full pipeline (OCR → NLP → Routing) ≤ 8 seconds for 10-page fax (99th percentile).                                                                                                                                         |

## Module B: Digital Document Annotation & Signature Toolkit

| Sub-feature             | Technical Implementation Details                                                                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B.1 Signature Creation  | Type-to-signature: Google Fonts “Dancing Script” + random stroke variation. Draw: HTML5 Canvas → SVG → PNG (2048×2048 transparent). Upload: Remove.bg API → manual crop fallback. |
| B.2 Signature Placement | PDF.js + Fabric.js overlay. All annotations stored as separate PDF Layer (OCG) + AP (Appearance Stream). On save → flatten + embed XMP metadata (creator, timestamp, user_id).    |
| B.3 Custom Stamps       | Stamp designer: Konva.js canvas. Saved as SVG template with placeholders {{DATE}}, {{USER}}, {{TIME}}. Rendering engine replaces placeholders at application time.                |
| B.4 Auto Metadata Stamp | Inject 1-inch stamp on page 1 top-right: “Received via Fax – 2025-11-26 14:33 EST – DartwingFax ID: DF-20251126-AB12”.                                                            |
| B.5 Return-via-Fax      | Extract original CSID/T.30 sender number → create outbound job using that exact number as destination. PDF is the signed/flattened version.                                       |
| B.6 Return-via-Email    | Parse original fax for email (OCR + header). Pre-fill SMTP with signed PDF attached (MIME multipart). User can edit subject/body before send.                                     |
| Immutability            | Once “Save Final” clicked → generate new PDF/A-3b with embedded hash + timestamp + user_id → store as separate immutable artifact. Old version preserved as “Draft”.              |

## Module C: Three-Tier Inbound Fax Validation

| Tier / Feature                     | Technical Implementation Details                                                                                                                                            |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C.1 Tier 1 Whitelist/Blacklist     | Redis Bloom Filter for O(1) lookup (10 M numbers). Hourly sync with AbuseIPDB + custom fraud DB via S3 import. Personal blacklist per user stored in PostgreSQL.            |
| C.2 Tier 2 AI Spam Scoring         | Gradient-boosting model (LightGBM) trained on 5M labeled faxes. Features: keyword density, overnight timing, CSID patterns, OCR entropy. Score 0–100.                       |
| C.3 Tier 3 Questionnaire Challenge | Challenge fax generated as 1-page PDF with QR code containing UUID + 6-digit code. Response matched by exact CSID + code via fuzzy OCR + regex. Timeout 24 h → auto-delete. |
| Held Faxes Queue                   | Separate DynamoDB table “held_faxes” with TTL 48 h. Admin console can force release or permanent block.                                                                     |
| Latency                            | Tier 1 + Tier 2 ≤ 5 s end-to-end (measured from S3 fax arrival → routing decision).                                                                                         |

## Module D: Outbound Security & Anti-Spoofing

| Feature                      | Technical Implementation Details                                                                                                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D.1 MFA & Source Locking     | Web: WebAuthn + TOTP. Email-to-Fax: SPF/DKIM/DMARC check + only from verified_addresses table.                                                                                |
| D.2 Confirmation Loop        | On email-to-fax → generate preview PDF → 6-char code → send via SES or Twilio SMS (customer preference). Redis key expiry 10 min. Success → trigger outbound fax immediately. |
| D.3 API Authentication       | Bearer token (JWT HS256) + optional Ed25519 signature on payload hash. Rate limit 500 faxes/hour/account (Redis sliding window).                                              |
| D.4 Internal Verifiable CSID | Inject “DFX-20251126-AB12” as CSID prefix on every outbound fax (T.30 header manipulation via FoIP gateway).                                                                  |
| Audit Logs                   | Immutable append-only logs in CloudTrail + S3 Object Lock (Governance mode) for 7 years.                                                                                      |

## Module F: Search, Retrieval & Knowledge Layer

| Feature          | Technical Implementation Details                                                              |
| ---------------- | --------------------------------------------------------------------------------------------- |
| Full-Text Search | Amazon OpenSearch Service (k-NN + ICU analyzer). Index updated within 10 s of OCR completion. |
| Saved Filters    | Stored as JSON in PostgreSQL “saved_searches” with sharing via team_id.                       |
| Re-OCR           | Celery/RQ task “reprocess_fax” → new version stored with version number.                      |

## Module G: Compliance & Redaction

| Feature                | Technical Implementation Details                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| Retention & Legal Hold | S3 Glacier Deep Archive + Object Lock (Compliance mode). Legal hold = S3 tag “legal_hold=true”. |
| Redaction              | PDF redaction via PyMuPDF → black rectangle + remove text from text layer. Audit log who/when.  |

## Module H–Q: Remaining Modules – Key Technical Notes

| Module                         | Critical Implementation Details                                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| H. Number Provisioning         | Integration with BWKS (Bandwidth) & Telnyx APIs for instant search/purchase. Webhook → auto-create DID routing rule.               |
| I. Cover Pages                 | Stored as Handlebars templates in S3. Rendered server-side at send time.                                                           |
| J. Notifications               | Rule engine → SNS → FCM/APNs (mobile), Twilio (SMS), SES (email), Slack/Teams via Incoming Webhooks.                               |
| K. Mobile Apps                 | React Native base + Expo. Signature via react-native-signature-capture. Camera → OpenCV deskew → send.                             |
| N. Integrations Marketplace    | OAuth2 + pre-built connectors in separate microservices (salesforce-connector, gdrive-connector, etc.).                            |
| N. Customer-Controlled Storage | SSE-C (customer provides AES-256 key) or SSE-KMS with customer-managed key. Daily batch push of finalized faxes.                   |
| O. Bulk Fax                    | CSV + PDF upload → SQS queue → 100 parallel outbound workers. Opt-out stored in Redis set.                                         |
| P. Form Parsing                | Document Understanding model (LayoutLMv3 fine-tuned) + form template registry in DynamoDB.                                         |
| Q. External Signature          | Generate secure one-time link (JWT 15-min expiry) → recipient signs via web viewer → callback signs PDF with embedded certificate. |
| Q. Redundancy                  | Two active FoIP regions (us-east-1 & us-west-2) with anycast IP. Automatic carrier failover via least-cost routing table.          |

## Global Technical Standards

| Item            | Specification                                                           |
| --------------- | ----------------------------------------------------------------------- |
| Primary Storage | PostgreSQL 16 (Aurora) + DynamoDB for queues                            |
| File Storage    | S3 Intelligent-Tiering + Object Lock where required                     |
| Fax Transport   | FoIP via SignalWire / Twilio Elastic SIP Trunking + custom T.38 gateway |
| OCR/AI Workers  | AWS Fargate 8 vCPU / 16 GB tasks                                        |
| Encryption      | TLS 1.3 everywhere; AES-256-GCM at rest                                 |
| Observability   | OpenTelemetry → Jaeger + CloudWatch + Datadog RUM                       |
| CI/CD           | GitHub Actions → ArgoCD → EKS/Kubernetes                                |

This TechSpec is now complete, unambiguous, and ready for architecture review and sprint planning.

**End of Document**
