# Critique: Dartwing User Architecture

**Date:** November 29, 2025
**Reviewer:** Gemi (AI Agent)
**Documents Reviewed:**

- `dartwing_user_arch.md` (v2.0)
- `dartwing_user_prd.md` (v2.0)
- `dartwing_core_arch.md` (v1.0)

---

## 1. Executive Summary

The **Dartwing User Module** architecture is well-structured and strongly aligned with the product vision of "One Human = One Identity." The separation of **Personal** (User Module) vs. **Organizational** (Core/Family/Company) concerns is a critical design decision that solves the "fragmented identity" problem effectively.

However, the architecture faces significant implementation challenges regarding **Travel Mode (Data Hiding)** and **Cross-Module Synchronization**. While the data model is sound, the mechanisms for enforcing privacy controls across the entire platform (including other installed apps) need more rigorous technical definition to ensure they are fail-safe.

---

## 2. Strengths

### 2.1 Strong Conceptual Foundation ("One Human = One Identity")

The distinction between `Person` (Core identity) and `User Profile` (Personal preferences) is excellent. It allows the Core module to remain unopinionated about personal features while the User module handles the rich, user-centric functionality. This prevents the "God Object" anti-pattern in the Core module.

### 2.2 Privacy-First Design

The architecture treats privacy not as a setting but as a core capability. Features like **Travel Mode**, **Duress PIN**, and **Device Trust Scoring** are baked into the data model, which is a major differentiator. The "Defense in Depth" approach (Layer 1-5) is a robust security model.

### 2.3 Clear Module Boundaries

The dependency chain (`dartwing_user` -> `dartwing_core`) is clean. The User module extends functionality without modifying Core's schema destructively. The use of 1:1 links (`User Profile` -> `Person`) is the correct relational approach for this extension.

### 2.4 Comprehensive Device Management

The `User Device` and `User Session` doctypes provide a level of security visibility rarely seen in standard business apps. The "Trust Score" algorithm is a smart addition that adds nuance beyond simple "allow/deny" lists.

---

## 3. Weaknesses & Risks

### 3.1 Travel Mode Implementation Complexity (High Risk)

**The Problem:** The PRD requires Travel Mode to "Hide financial data" and "Hide medical records."
**The Gap:** The architecture mentions this but doesn't detail the _mechanism_. In Frappe, permissions are usually Role-based. Hiding specific _records_ or _fields_ dynamically based on a boolean flag (`travel_mode`) on a related doctype (`User Profile`) across _all_ modules is extremely difficult to implement securely.

- **Risk:** If a developer adds a new "Financial" doctype in another module and forgets to add the "Travel Mode check," data leaks.
- **Risk:** Standard list views might still show sensitive "name" fields even if details are hidden.

### 3.2 Hook-Based Integrity (Medium Risk)

The reliance on `after_insert` hooks to create the `User Profile` (1:1 with `Person`) is standard for Frappe but can be fragile.

- **Risk:** If the hook fails (e.g., error in `create_user_profile`), you end up with a `Person` without a `User Profile`, breaking the "One Identity" promise.
- **Mitigation:** Needs a reconciliation job (background task) to find and fix orphaned `Person` records.

### 3.3 Encryption Key Management (High Risk)

The **Personal Vault** feature (`U-13`) implies encryption. The architecture shows `encryption_key` as a field in `Personal Vault Item`.

- **Critique:** Storing the key in the database (even if encrypted) next to the data is a security weakness. If the DB is compromised, both are lost.
- **Missing:** A strategy for client-side encryption or a separate Key Management Service (KMS) integration is needed for true "Vault" security.

### 3.4 AI Voice Latency & Storage

The `AI Voice Profile` doctype stores `voice_sample`.

- **Critique:** Storing binary audio data in the database (MariaDB/Postgres) is bad for performance.
- **Improvement:** Should use Frappe's File API to store in S3/Filesystem, storing only the URL in the doctype.

---

## 4. Feature Implementation Analysis

Analysis of `dartwing_user_prd.md` features against the architecture.

| Feature                     | Difficulty  | Analysis                                                                                                                                                           |
| :-------------------------- | :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **U-01 User Profile**       | 🟢 Easy     | Standard Doctype implementation. Well defined.                                                                                                                     |
| **U-02 Multi-Org Switcher** | 🟡 Medium   | Requires efficient querying of `Org Member` across all org types. UI complexity in Flutter is higher than backend complexity.                                      |
| **U-03 Device Trust**       | 🟡 Medium   | Logic for "Trust Score" needs careful tuning. Getting accurate device info from Flutter to backend requires robust client-side code.                               |
| **U-04 Global Block List**  | 🟡 Medium   | Easy to store, but _enforcing_ it (preventing messages/invites) requires checks in every communication function across the platform.                               |
| **U-05 Shortcuts**          | 🟢 Easy     | Simple CRUD. Execution logic is client-side (Flutter).                                                                                                             |
| **U-06 Travel Mode**        | 🔴 **Hard** | **Major Challenge.** Requires a global "Permission Manager" that intercepts read requests for sensitive doctypes. Hard to get right without performance penalties. |
| **U-07 Push-to-Approve**    | 🔴 **Hard** | Requires real-time socket connection or reliable push notifications (FCM/APNS) and a secure handshake protocol.                                                    |
| **U-08 Digital Will**       | 🟡 Medium   | Logic is simple (timer based), but legal/security implications of "auto-transferring" access are high.                                                             |
| **U-13 Personal Vault**     | 🔴 **Hard** | Encryption is hard. "Zero-knowledge" (if attempted) is very hard. Simple server-side encryption is easier but less secure.                                         |
| **U-23 Biometric Unlock**   | 🟢 Easy     | handled primarily by Flutter `local_auth` package. Backend just sees a valid token.                                                                                |

---

## 5. Suggested Improvements

### 5.1 Robust "Travel Mode" Architecture

Instead of ad-hoc checks, introduce a **`SensitiveDataMixin`** for Python controllers.

```python
class SensitiveDataMixin:
    def check_permission(self, permission, user=None):
        # 1. Standard Frappe Check
        super().check_permission(permission, user)

        # 2. Travel Mode Check
        if self.is_sensitive_category(self.doctype) and is_travel_mode_active(user):
            frappe.throw("Access denied in Travel Mode", TravelModeError)
```

This enforces security at the controller level for any doctype inheriting the mixin.

### 5.2 Transactional Identity Creation

Move the creation logic from simple hooks to a **Service Class**.

```python
class IdentityService:
    def create_identity(self, email, full_name):
        # Atomic transaction
        person = create_person(...)
        profile = create_user_profile(person=person.name, ...)
        return person
```

Use this service everywhere instead of `frappe.new_doc("Person")`.

### 5.3 Externalize Large Assets

Explicitly define that `voice_sample` and `verification_document_data` must use **Frappe File** attachments (stored in S3/Disk), not Blob columns.

### 5.4 "Missing" Executive Summary

The file `dartwing_user_executive_summary.md` is referenced but missing. It should be created to align with the other modules.

---

## 6. Conclusion

The Dartwing User architecture is **APPROVED** for development, provided the **Travel Mode** implementation is prototyped early (Proof of Concept) to validate the data-hiding strategy. The "One Human" model is a winning architectural choice that will pay dividends in user experience and data integrity.
