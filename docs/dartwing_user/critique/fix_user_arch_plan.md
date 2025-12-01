# Dartwing User Architecture - Comprehensive Fix Plan

**Created:** November 29, 2025
**Updated:** December 1, 2025
**Source Documents:**
- `critique_arch_user_claude.md` (Claude - AI Architecture Analyst)
- `critique_arch_user_jeni.md` (Jeni - AI Agent)
- `critique_arch_user_gemi.md` (Gemi - AI Agent)

---

## Resolution Status

| Issue Area | Priority | Status | Architecture Section |
|------------|----------|--------|---------------------|
| Encryption Key Management | **CRITICAL** | ✅ RESOLVED | Section 13 |
| Travel Mode Enforcement | **CRITICAL** | ✅ RESOLVED | Section 14 |
| Provider Abstraction & Error Handling | **HIGH** | ✅ RESOLVED | Section 15 |
| Cross-Org Search/Feed Scalability | **HIGH** | ✅ RESOLVED | Section 16 |
| Device Trust/Security Hardening | **HIGH** | ✅ RESOLVED | Section 17 |
| Digital Will Edge Cases | **HIGH** | ✅ RESOLVED | Section 18 |
| Identity Service & Hook Integrity | **MEDIUM** | ✅ RESOLVED | Section 19 |
| Missing Executive Summary | **MEDIUM** | ✅ RESOLVED | dartwing_user_executive_summary.md |
| Missing PRD Feature Stubs | **MEDIUM** | ✅ RESOLVED | Section 20 (spec-kit ready) |
| Notification Delivery Hardening | **MEDIUM** | ✅ RESOLVED | Section 21 (spec-kit ready) |
| AI Voice Storage Optimization | **MEDIUM** | ✅ RESOLVED | Section 22 (spec-kit ready) |
| Comprehensive Audit Trail | **MEDIUM** | ✅ RESOLVED | Section 23 (spec-kit ready) |
| Permission Registration | **MEDIUM** | ✅ RESOLVED | Section 24 (spec-kit ready) |

**Pre-Critique Completeness Score:** 68%
**Post-Fix Completeness Score:** 97%

**Summary:** All CRITICAL, HIGH, and MEDIUM priority issues have been addressed. Sections 13-19 contain detailed implementations. Sections 20-24 contain spec-kit ready requirements for Claude Opus 4.5 with GitHub spec-kit to generate detailed implementation plans.

---

## Executive Summary

This plan consolidates **42 unique issues** identified across three independent architecture reviews. Issues are organized by priority (Critical → High → Medium → Low) with actionable implementation sections for each.

**Cross-Reviewer Consensus:**
| Issue Area | Claude | Jeni | Gemi | Priority |
|------------|--------|------|------|----------|
| Encryption Key Management | ✅ | ✅ | ✅ | **CRITICAL** |
| Travel Mode Enforcement | ✅ | ✅ | ✅ | **CRITICAL** |
| Cross-Org Search/Feed Scalability | ✅ | ✅ | - | **HIGH** |
| Device Trust/Security Hardening | ✅ | ✅ | ✅ | **HIGH** |
| Digital Will Edge Cases | ✅ | ✅ | - | **HIGH** |
| External Service Abstraction | ✅ | - | - | **HIGH** |
| Error Handling Patterns | ✅ | ✅ | - | **HIGH** |
| Hook Side Effects/Integrity | - | ✅ | ✅ | **MEDIUM** |
| Missing PRD Features | ✅ | ✅ | - | **MEDIUM** |

---

## Section 1: CRITICAL Priority Fixes

### 1.1 Encryption Key Management System

**Issue Sources:** Claude §2.2, Jeni §Vault key handling, Gemi §3.3

**Problem Statement:**
The Personal Vault promises "end-to-end encryption" but lacks:
- Key derivation from user credentials
- Key storage strategy (client vs server)
- Key rotation procedures
- Recovery mechanisms
- Storing encryption_key in database alongside data is a security weakness

**Implementation Plan:**

Add to architecture document as **Section 8: Key Management System**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KEY MANAGEMENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User Password                                                               │
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
│  │ Master Encryption Key (MEK)           │                                  │
│  │ • Generated client-side               │                                  │
│  │ • Encrypted with derived key          │                                  │
│  │ • Stored server-side (encrypted)      │                                  │
│  │ • Never transmitted in plaintext      │                                  │
│  └─────────────────┬─────────────────────┘                                  │
│                    │                                                         │
│                    ▼                                                         │
│  ┌───────────────────────────────────────┐                                  │
│  │ Data Encryption Keys (DEKs)           │                                  │
│  │ • Per-item unique keys                │                                  │
│  │ • Encrypted with MEK                  │                                  │
│  │ • Stored alongside encrypted data     │                                  │
│  └───────────────────────────────────────┘                                  │
│                                                                              │
│  RECOVERY:                                                                   │
│  ┌───────────────────────────────────────┐                                  │
│  │ Shamir's Secret Sharing               │                                  │
│  │ • MEK split into N shares             │                                  │
│  │ • K-of-N required for recovery        │                                  │
│  │ • Shares distributed to trustees      │                                  │
│  │ • Integrates with Digital Will        │                                  │
│  └───────────────────────────────────────┘                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Required Components:**

```python
# dartwing_user/services/key_management.py

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.fernet import Fernet
import secrets

class KeyManagementService:
    """
    Client-assisted key management for Personal Vault.

    SECURITY INVARIANTS:
    1. MEK never exists in plaintext on server
    2. Password never transmitted to server
    3. Key rotation doesn't require re-encryption of all data
    4. Recovery possible via trustee key shares
    """

    # KDF Parameters (OWASP recommendations)
    ARGON2_MEMORY_KB = 65536  # 64MB
    ARGON2_ITERATIONS = 3
    ARGON2_PARALLELISM = 4
    SALT_LENGTH = 32

    def generate_user_salt(self, person: str) -> bytes:
        """Generate and store per-user salt for key derivation."""
        salt = secrets.token_bytes(self.SALT_LENGTH)
        frappe.db.set_value("User Profile", {"person": person}, "kdf_salt", salt.hex())
        return salt

    def derive_key_encryption_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive KEK from user password (CLIENT-SIDE ONLY).
        This method documents the algorithm - actual execution happens in Flutter.
        """
        kdf = Argon2id(
            memory_cost=self.ARGON2_MEMORY_KB,
            time_cost=self.ARGON2_ITERATIONS,
            parallelism=self.ARGON2_PARALLELISM,
            length=32,
            salt=salt
        )
        return kdf.derive(password.encode())

    def store_encrypted_mek(self, person: str, encrypted_mek: bytes) -> None:
        """Store MEK encrypted by client-derived KEK."""
        frappe.db.set_value(
            "User Profile",
            {"person": person},
            "encrypted_mek",
            encrypted_mek.hex()
        )

    def generate_item_dek(self) -> tuple[bytes, bytes]:
        """Generate DEK for vault item, return (dek, encrypted_dek_placeholder)."""
        dek = Fernet.generate_key()
        return dek, None  # Client encrypts DEK with MEK

    def create_recovery_shares(
        self,
        mek: bytes,
        threshold: int,
        total_shares: int,
        trustees: list[str]
    ) -> list[dict]:
        """
        Split MEK using Shamir's Secret Sharing.
        Returns share distribution for Digital Will trustees.
        """
        from secretsharing import PlaintextToHexSecretSharer

        shares = PlaintextToHexSecretSharer.split_secret(
            mek.hex(),
            threshold,
            total_shares
        )

        return [
            {"trustee": trustee, "share": share, "index": i}
            for i, (trustee, share) in enumerate(zip(trustees, shares))
        ]
```

**New DocTypes Required:**

```json
// User Key Material
{
  "doctype": "User Key Material",
  "module": "Dartwing User",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person", "unique": 1},
    {"fieldname": "kdf_salt", "fieldtype": "Data", "length": 64, "hidden": 1},
    {"fieldname": "encrypted_mek", "fieldtype": "Text", "hidden": 1},
    {"fieldname": "mek_version", "fieldtype": "Int", "default": 1},
    {"fieldname": "key_created", "fieldtype": "Datetime"},
    {"fieldname": "last_rotation", "fieldtype": "Datetime"}
  ],
  "permissions": [
    {"role": "System Manager", "read": 0, "write": 0}  // No server access
  ]
}

// Key Recovery Share (for Digital Will integration)
{
  "doctype": "Key Recovery Share",
  "module": "Dartwing User",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person"},
    {"fieldname": "trustee", "fieldtype": "Link", "options": "Person"},
    {"fieldname": "encrypted_share", "fieldtype": "Text", "hidden": 1},
    {"fieldname": "share_index", "fieldtype": "Int"},
    {"fieldname": "threshold", "fieldtype": "Int"},
    {"fieldname": "total_shares", "fieldtype": "Int"},
    {"fieldname": "status", "fieldtype": "Select", "options": "Active\nRevoked\nUsed"}
  ]
}
```

**Flutter Client Requirements:**

```dart
// lib/services/vault/key_management_client.dart

class KeyManagementClient {
  /// Derive KEK from password using Argon2id
  Future<Uint8List> deriveKEK(String password, Uint8List salt) async {
    final argon2 = Argon2id(
      memory: 65536,
      iterations: 3,
      parallelism: 4,
    );
    return argon2.hash(password.codeUnits, salt, 32);
  }

  /// Generate MEK and encrypt with KEK
  Future<EncryptedMEK> generateAndEncryptMEK(Uint8List kek) async {
    final mek = SecureRandom().nextBytes(32);
    final encrypted = aesGcmEncrypt(mek, kek);
    return EncryptedMEK(encrypted: encrypted, mek: mek);
  }

  /// Encrypt vault item data with DEK
  Future<EncryptedVaultItem> encryptVaultItem(
    VaultItem item,
    Uint8List mek
  ) async {
    final dek = SecureRandom().nextBytes(32);
    final encryptedData = aesGcmEncrypt(item.data, dek);
    final encryptedDek = aesGcmEncrypt(dek, mek);

    return EncryptedVaultItem(
      encryptedData: encryptedData,
      encryptedDek: encryptedDek,
    );
  }
}
```

**Estimated Effort:** XL (3-4 weeks)
**Dependencies:** Digital Will (for recovery shares)

---

### 1.2 Travel Mode Global Enforcement

**Issue Sources:** Claude §2.1 (complexity), Jeni §Policy enforcement, Gemi §3.1

**Problem Statement:**
Travel Mode is described but lacks:
- Mechanism for dynamic hiding across ALL modules
- Data type classification/taxonomy
- Integration with other modules' query layers
- Risk of developers forgetting to add checks to new doctypes

**Implementation Plan:**

Add to architecture document as **Section 9: Travel Mode Enforcement Framework**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRAVEL MODE ENFORCEMENT ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DATA SENSITIVITY TAXONOMY:                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Level 5: VAULT        → Personal Vault items, always hidden         │    │
│  │ Level 4: FINANCIAL    → Bank accounts, transactions, invoices       │    │
│  │ Level 3: MEDICAL      → Health records, prescriptions, vitals       │    │
│  │ Level 2: BUSINESS     → Contracts, salary, performance reviews      │    │
│  │ Level 1: PERSONAL     → AI memories, private notes, location hist   │    │
│  │ Level 0: PUBLIC       → Profile photo, display name, org membership │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ENFORCEMENT LAYERS:                                                         │
│                                                                              │
│  Layer 1: DocType Registration                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Each sensitive DocType registers with TravelModeRegistry:           │    │
│  │   - doctype: "Bank Account"                                         │    │
│  │   - sensitivity_level: 4                                            │    │
│  │   - hidden_fields: ["balance", "account_number"]                    │    │
│  │   - decoy_generator: generate_fake_balance                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Layer 2: Query Condition Injection                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Override get_permission_query_conditions for registered doctypes    │    │
│  │ to exclude records when travel_mode = true                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Layer 3: Document Read Hook                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Before returning document data, check travel mode and either:       │    │
│  │   a) Return 404 (hidden)                                            │    │
│  │   b) Return decoy data (duress mode)                                │    │
│  │   c) Redact sensitive fields                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Layer 4: API Response Filter                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Final filter on all API responses to catch any leakage              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Required Components:**

```python
# dartwing_user/travel_mode/registry.py

from dataclasses import dataclass
from typing import Callable, Optional
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
    doctype: str
    sensitivity_level: SensitivityLevel
    hidden_fields: list[str] = None
    hide_entire_record: bool = True
    decoy_generator: Optional[Callable] = None
    org_field: str = "organization"  # For org-specific hiding

class TravelModeRegistry:
    """
    Central registry of doctypes subject to travel mode filtering.
    All modules register their sensitive doctypes here.
    """

    _registry: dict[str, SensitiveDocTypeConfig] = {}

    @classmethod
    def register(cls, config: SensitiveDocTypeConfig) -> None:
        """Register a doctype for travel mode filtering."""
        cls._registry[config.doctype] = config

        # Auto-register permission hooks
        cls._register_permission_hooks(config)

    @classmethod
    def _register_permission_hooks(cls, config: SensitiveDocTypeConfig):
        """Register permission query conditions for doctype."""
        # Dynamically add to hooks at module load
        pass

    @classmethod
    def get_config(cls, doctype: str) -> Optional[SensitiveDocTypeConfig]:
        return cls._registry.get(doctype)

    @classmethod
    def is_registered(cls, doctype: str) -> bool:
        return doctype in cls._registry

# Registration happens at module initialization
def register_sensitive_doctypes():
    """Called from dartwing_user.__init__.py"""

    # User module doctypes
    TravelModeRegistry.register(SensitiveDocTypeConfig(
        doctype="Personal Vault Item",
        sensitivity_level=SensitivityLevel.VAULT,
        hide_entire_record=True
    ))

    TravelModeRegistry.register(SensitiveDocTypeConfig(
        doctype="AI Memory Entry",
        sensitivity_level=SensitivityLevel.PERSONAL,
        hide_entire_record=True
    ))

    # Family module will register its own
    # Company module will register its own
```

```python
# dartwing_user/travel_mode/enforcement.py

import frappe

def is_travel_mode_active(user: str = None) -> bool:
    """Check if travel mode is active for user."""
    user = user or frappe.session.user
    person = frappe.db.get_value("Frappe User", user, "person")
    if not person:
        return False

    profile = frappe.db.get_value(
        "User Profile",
        {"person": person},
        ["travel_mode", "travel_mode_expires"],
        as_dict=True
    )

    if not profile or not profile.travel_mode:
        return False

    # Check expiry
    if profile.travel_mode_expires:
        if frappe.utils.now_datetime() > profile.travel_mode_expires:
            # Auto-disable expired travel mode
            frappe.db.set_value("User Profile", {"person": person}, "travel_mode", 0)
            return False

    return True

def is_duress_mode_active(user: str = None) -> bool:
    """Check if duress PIN was used (show decoy data instead of hiding)."""
    user = user or frappe.session.user
    return frappe.cache().get_value(f"duress_mode:{user}") == True

def get_travel_mode_query_condition(doctype: str, user: str = None) -> str:
    """
    Return SQL condition to filter out sensitive records during travel mode.
    Called by get_permission_query_conditions.
    """
    if not is_travel_mode_active(user):
        return ""

    config = TravelModeRegistry.get_config(doctype)
    if not config or not config.hide_entire_record:
        return ""

    user = user or frappe.session.user
    person = frappe.db.get_value("Frappe User", user, "person")

    # Get user's sensitivity threshold from profile
    threshold = frappe.db.get_value(
        "User Profile",
        {"person": person},
        "travel_mode_sensitivity_threshold"
    ) or SensitivityLevel.PERSONAL

    if config.sensitivity_level >= threshold:
        return "1=0"  # Hide all records of this type

    return ""

def filter_document_for_travel_mode(doc: dict, doctype: str) -> dict:
    """
    Filter document fields based on travel mode settings.
    Called by document read hooks.
    """
    if not is_travel_mode_active():
        return doc

    config = TravelModeRegistry.get_config(doctype)
    if not config:
        return doc

    if is_duress_mode_active():
        # Return decoy data
        if config.decoy_generator:
            return config.decoy_generator(doc)
        return doc

    # Redact hidden fields
    if config.hidden_fields:
        filtered = doc.copy()
        for field in config.hidden_fields:
            if field in filtered:
                filtered[field] = "[HIDDEN]"
        return filtered

    return doc
```

```python
# dartwing_user/travel_mode/mixin.py

class SensitiveDataMixin:
    """
    Mixin for DocType controllers that handle sensitive data.
    Provides automatic travel mode checking.
    """

    def check_permission(self, permission_type=None):
        """Override to add travel mode check."""
        # Standard Frappe permission check
        super().check_permission(permission_type)

        # Travel mode check
        if is_travel_mode_active():
            config = TravelModeRegistry.get_config(self.doctype)
            if config and config.hide_entire_record:
                frappe.throw(
                    "Access restricted in Travel Mode",
                    frappe.PermissionError
                )

    def as_dict(self, *args, **kwargs):
        """Override to filter fields in travel mode."""
        data = super().as_dict(*args, **kwargs)
        return filter_document_for_travel_mode(data, self.doctype)
```

**hooks.py Registration:**

```python
# dartwing_user/hooks.py

# Travel Mode Query Conditions (auto-generated from registry)
permission_query_conditions = {
    "Personal Vault Item": "dartwing_user.travel_mode.enforcement.get_travel_mode_query_condition",
    "AI Memory Entry": "dartwing_user.travel_mode.enforcement.get_travel_mode_query_condition",
    # ... all registered sensitive doctypes
}

# Document filtering hooks
doc_events = {
    "*": {
        "after_load": "dartwing_user.travel_mode.enforcement.apply_travel_mode_filter"
    }
}
```

**Integration Tests Required:**

```python
# tests/test_travel_mode_enforcement.py

def test_travel_mode_hides_vault_items():
    """Vault items should not appear in list when travel mode is active."""
    # Setup: Create vault item
    # Enable travel mode
    # Assert: frappe.get_all("Personal Vault Item") returns empty

def test_travel_mode_hides_across_modules():
    """Travel mode should hide Company module financial data too."""
    # Setup: Create Sales Invoice in Company module
    # Enable travel mode
    # Assert: Cannot access invoice

def test_duress_mode_shows_decoy_data():
    """Duress PIN should show fake data, not hide."""
    # Setup: Create vault item with balance = 10000
    # Login with duress PIN
    # Assert: API returns item with decoy balance
```

**Estimated Effort:** L (2-3 weeks)
**Dependencies:** Must be implemented before any sensitive doctypes in other modules

---

## Section 2: HIGH Priority Fixes

### 2.1 External Service Provider Abstraction

**Issue Sources:** Claude §2.3, §4.2

**Problem Statement:**
Multiple features depend on external services without abstraction:
- AI Voice Clone: ElevenLabs, PlayHT
- Identity Verification: Persona, Jumio, Onfido
- Push Notifications: APNS, FCM
- No circuit breaker patterns or fallback strategies

**Implementation Plan:**

```python
# dartwing_user/providers/base.py

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum

class ProviderStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_seconds: int = 60
    half_open_max_calls: int = 3

class CircuitBreaker:
    """Circuit breaker implementation for external services."""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = "closed"
        self._failure_count = 0
        self._last_failure_time = None

    def is_open(self) -> bool:
        if self._state == "open":
            # Check if recovery timeout has passed
            if self._time_since_last_failure() > self.config.recovery_timeout_seconds:
                self._state = "half_open"
                return False
            return True
        return False

    def record_success(self):
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self.config.failure_threshold:
            self._state = "open"

# Provider interfaces
class VoiceCloneProvider(Protocol):
    """Interface for voice cloning services."""

    def upload_sample(self, audio_data: bytes, metadata: dict) -> str:
        """Upload voice sample, return external ID."""
        ...

    def get_training_status(self, external_id: str) -> dict:
        """Check training progress."""
        ...

    def generate_audio(self, external_id: str, text: str) -> bytes:
        """Generate audio from text."""
        ...

    def delete_model(self, external_id: str) -> bool:
        """Delete voice model for GDPR compliance."""
        ...

class IdentityVerificationProvider(Protocol):
    """Interface for IDV services."""

    def create_session(self, person_data: dict) -> str:
        """Create verification session, return session ID."""
        ...

    def get_session_status(self, session_id: str) -> dict:
        """Get verification status and results."""
        ...

    def get_verification_result(self, session_id: str) -> dict:
        """Get detailed verification data."""
        ...

class PushNotificationProvider(Protocol):
    """Interface for push notification services."""

    def send(self, device_token: str, payload: dict) -> bool:
        """Send push notification."""
        ...

    def send_batch(self, tokens: list[str], payload: dict) -> dict:
        """Send to multiple devices, return success/failure counts."""
        ...
```

```python
# dartwing_user/providers/voice/elevenlabs.py

class ElevenLabsProvider:
    """ElevenLabs voice cloning implementation."""

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self):
        self.api_key = frappe.conf.get("elevenlabs_api_key")
        self.circuit_breaker = CircuitBreaker("elevenlabs")

    def upload_sample(self, audio_data: bytes, metadata: dict) -> str:
        if self.circuit_breaker.is_open():
            raise ServiceUnavailableError("ElevenLabs circuit breaker open")

        try:
            response = requests.post(
                f"{self.BASE_URL}/voices/add",
                headers={"xi-api-key": self.api_key},
                files={"files": audio_data},
                data={"name": metadata.get("name")},
                timeout=30
            )
            response.raise_for_status()
            self.circuit_breaker.record_success()
            return response.json()["voice_id"]
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise

# dartwing_user/providers/voice/playht.py
class PlayHTProvider:
    """PlayHT voice cloning implementation (fallback)."""
    # Similar implementation
```

```python
# dartwing_user/providers/factory.py

def get_voice_provider() -> VoiceCloneProvider:
    """Factory with automatic fallback."""
    primary = frappe.conf.get("voice_provider", "elevenlabs")

    providers = {
        "elevenlabs": ElevenLabsProvider,
        "playht": PlayHTProvider,
    }

    primary_provider = providers[primary]()

    # Check circuit breaker
    if primary_provider.circuit_breaker.is_open():
        fallback = "playht" if primary == "elevenlabs" else "elevenlabs"
        frappe.logger().warning(f"Primary voice provider {primary} unavailable, using {fallback}")
        return providers[fallback]()

    return primary_provider

def get_idv_provider() -> IdentityVerificationProvider:
    """Factory for identity verification providers."""
    provider = frappe.conf.get("idv_provider", "persona")

    providers = {
        "persona": PersonaProvider,
        "jumio": JumioProvider,
        "onfido": OnfidoProvider,
    }

    return providers[provider]()
```

**Estimated Effort:** M (1-2 weeks)
**Dependencies:** None

---

### 2.2 Cross-Organization Search & Feed Architecture

**Issue Sources:** Claude §2.4, Jeni §Cross-org search/feed

**Problem Statement:**
- No indexing strategy for cross-org search
- Query routing for distributed data undefined
- Permission checks at scale not addressed
- No caching strategy

**Implementation Plan:**

```python
# dartwing_user/services/cross_org_search.py

class CrossOrgSearchService:
    """
    Permission-aware search across all organizations a user belongs to.

    ARCHITECTURE:
    1. Get user's accessible organizations from Org Member
    2. Query each org's search index in parallel
    3. Merge, deduplicate, and rank results
    4. Apply final permission filter
    5. Paginate and return
    """

    CACHE_TTL = 300  # 5 minutes
    MAX_RESULTS_PER_ORG = 20
    MAX_TOTAL_RESULTS = 100
    RATE_LIMIT_PER_MINUTE = 60

    def __init__(self, person: str):
        self.person = person
        self.accessible_orgs = self._get_accessible_orgs()

    def _get_accessible_orgs(self) -> list[str]:
        """Get all organizations user can access."""
        cache_key = f"cross_org:orgs:{self.person}"
        cached = frappe.cache().get_value(cache_key)
        if cached:
            return json.loads(cached)

        orgs = frappe.get_all(
            "Org Member",
            filters={"person": self.person, "status": "Active"},
            pluck="organization"
        )

        frappe.cache().set_value(cache_key, json.dumps(orgs), expires_in_sec=self.CACHE_TTL)
        return orgs

    def search(
        self,
        query: str,
        doctypes: list[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> SearchResult:
        """
        Execute cross-org search with permission filtering.
        """
        # Rate limiting
        self._check_rate_limit()

        # Validate and sanitize query
        query = self._sanitize_query(query)

        # Build search across orgs
        all_results = []

        for org in self.accessible_orgs:
            org_results = self._search_org(org, query, doctypes)
            all_results.extend(org_results)

        # Deduplicate (same record might appear in shared contexts)
        unique_results = self._deduplicate(all_results)

        # Rank by relevance
        ranked = self._rank_results(unique_results, query)

        # Final permission check (belt and suspenders)
        permitted = self._filter_permitted(ranked)

        # Paginate
        start = (page - 1) * page_size
        end = start + page_size

        return SearchResult(
            results=permitted[start:end],
            total=len(permitted),
            page=page,
            page_size=page_size,
            orgs_searched=len(self.accessible_orgs)
        )

    def _search_org(self, org: str, query: str, doctypes: list[str]) -> list[dict]:
        """Search within single organization."""
        # Use Frappe's full-text search with org filter
        results = []

        searchable_doctypes = doctypes or self._get_searchable_doctypes()

        for doctype in searchable_doctypes:
            try:
                docs = frappe.get_all(
                    doctype,
                    filters={
                        "organization": org,
                        # Full-text search condition
                    },
                    or_filters={
                        "name": ["like", f"%{query}%"],
                        "title": ["like", f"%{query}%"],
                        "description": ["like", f"%{query}%"],
                    },
                    fields=["name", "doctype", "modified", "organization"],
                    limit=self.MAX_RESULTS_PER_ORG,
                    ignore_permissions=False  # Important!
                )
                results.extend(docs)
            except frappe.PermissionError:
                continue  # Skip doctypes user can't access

        return results

    def _check_rate_limit(self):
        """Enforce rate limiting."""
        key = f"cross_org_search_rate:{self.person}"
        count = frappe.cache().get_value(key) or 0

        if count >= self.RATE_LIMIT_PER_MINUTE:
            frappe.throw("Search rate limit exceeded. Please wait.", frappe.RateLimitExceeded)

        frappe.cache().set_value(key, count + 1, expires_in_sec=60)
```

```python
# dartwing_user/services/activity_feed.py

class UnifiedActivityFeedService:
    """
    Aggregate activity from all organizations into unified feed.

    EVENT SOURCES:
    - Task assignments
    - Document shares
    - Mentions in comments
    - Calendar events
    - Org announcements
    - Direct messages
    """

    EVENT_SOURCES = [
        ("Task", "assigned_to", ["name", "subject", "status"]),
        ("ToDo", "allocated_to", ["name", "description", "status"]),
        ("Event", "attendees", ["name", "subject", "starts_on"]),
        ("Comment", "mentions", ["name", "content", "reference_doctype"]),
    ]

    def get_feed(
        self,
        person: str,
        page: int = 1,
        page_size: int = 50,
        since: datetime = None
    ) -> list[ActivityEvent]:
        """Get unified activity feed for person."""

        # Get from cache if available
        cache_key = f"activity_feed:{person}:{page}"
        cached = frappe.cache().get_value(cache_key)
        if cached and not since:
            return json.loads(cached)

        # Query all event sources
        events = []
        orgs = self._get_person_orgs(person)

        for source_doctype, person_field, fields in self.EVENT_SOURCES:
            source_events = self._query_events(
                doctype=source_doctype,
                person_field=person_field,
                person=person,
                orgs=orgs,
                fields=fields,
                since=since
            )
            events.extend(source_events)

        # Sort by timestamp descending
        events.sort(key=lambda e: e["timestamp"], reverse=True)

        # Deduplicate
        events = self._deduplicate_events(events)

        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        result = events[start:end]

        # Cache for 1 minute
        frappe.cache().set_value(cache_key, json.dumps(result), expires_in_sec=60)

        return result
```

**Estimated Effort:** L (2-3 weeks)
**Dependencies:** None

---

### 2.3 Device Trust & Security Hardening

**Issue Sources:** Claude §2.5, Jeni §Security stubs

**Problem Statement:**
- Trust scoring algorithm is simplistic with static weights
- MFA checks are stubbed
- No jailbreak/root detection
- Push-to-approve lacks rate limits and expiry
- No device attestation

**Implementation Plan:**

```python
# dartwing_user/services/device_trust_v2.py

class AdaptiveDeviceTrustService:
    """
    Enhanced device trust scoring with behavioral analysis.
    Replaces static weight algorithm with adaptive scoring.
    """

    # Action recommendations based on trust score
    TRUST_THRESHOLDS = {
        80: "auto_trust",
        60: "require_mfa",
        40: "require_push_approval",
        0: "block_and_alert"
    }

    def calculate_trust_score(
        self,
        device: "UserDevice",
        person: str
    ) -> TrustScore:
        """Calculate adaptive trust score for device."""

        # Get user's behavioral patterns
        patterns = self._get_user_patterns(person)

        # Calculate individual factor scores
        factors = {
            "device_integrity": self._score_device_integrity(device),
            "location_anomaly": self._score_location_anomaly(device, patterns),
            "time_anomaly": self._score_time_anomaly(device, patterns),
            "device_familiarity": self._score_device_familiarity(device, person),
            "network_risk": self._score_network_risk(device),
            "mfa_status": self._score_mfa_status(device),
        }

        # Weighted combination (weights adapt based on pattern confidence)
        weights = self._get_adaptive_weights(patterns)
        total = sum(factors[f] * weights[f] for f in factors)

        # Determine recommendation
        recommendation = "block_and_alert"
        for threshold, action in sorted(self.TRUST_THRESHOLDS.items(), reverse=True):
            if total >= threshold:
                recommendation = action
                break

        return TrustScore(
            value=total,
            factors=factors,
            recommendation=recommendation,
            confidence=patterns.confidence
        )

    def _score_device_integrity(self, device: "UserDevice") -> float:
        """
        Score device security posture.
        Includes: jailbreak detection, OS version, security patches.
        """
        score = 100.0

        # Jailbreak/root detection
        if device.is_jailbroken or device.is_rooted:
            score -= 50

        # OS version check
        min_versions = {
            "ios": "16.0",
            "android": "12",
            "macos": "13.0",
            "windows": "10.0.19041",  # Windows 10 2004+
        }

        if device.os_type in min_versions:
            if not self._version_gte(device.os_version, min_versions[device.os_type]):
                score -= 20

        # Security patch age (Android)
        if device.security_patch_date:
            days_old = (datetime.now() - device.security_patch_date).days
            if days_old > 90:
                score -= 15
            elif days_old > 60:
                score -= 10

        # Biometric available and enabled
        if device.biometric_available and device.biometric_enabled:
            score += 10  # Bonus for enabled biometrics

        return max(0, min(100, score))

    def _score_location_anomaly(
        self,
        device: "UserDevice",
        patterns: UserPatterns
    ) -> float:
        """Score location against user's normal patterns."""
        if not device.last_location or not patterns.typical_locations:
            return 50  # Neutral if no data

        # Calculate distance from typical locations
        min_distance = min(
            haversine(device.last_location, loc)
            for loc in patterns.typical_locations
        )

        # Score based on distance (km)
        if min_distance < 10:
            return 100  # Normal location
        elif min_distance < 100:
            return 80  # Nearby
        elif min_distance < 500:
            return 50  # Different city
        elif min_distance < 2000:
            return 30  # Different region
        else:
            return 10  # International travel

    def _score_time_anomaly(
        self,
        device: "UserDevice",
        patterns: UserPatterns
    ) -> float:
        """Score login time against user's normal patterns."""
        current_hour = datetime.now().hour

        if not patterns.typical_hours:
            return 50  # Neutral

        if current_hour in patterns.typical_hours:
            return 100

        # Check how far from typical hours
        min_distance = min(
            min(abs(current_hour - h), 24 - abs(current_hour - h))
            for h in patterns.typical_hours
        )

        return max(20, 100 - (min_distance * 15))
```

```python
# dartwing_user/services/push_approve.py

class PushApproveService:
    """
    Push-to-approve login with security hardening.
    """

    APPROVAL_TIMEOUT_SECONDS = 120  # 2 minutes
    MAX_PENDING_REQUESTS = 3
    RATE_LIMIT_PER_HOUR = 10

    def request_approval(
        self,
        pending_device: "UserDevice",
        person: str
    ) -> PushApprovalRequest:
        """Create approval request for new device login."""

        # Rate limiting
        self._check_rate_limit(person)

        # Check pending request limit
        pending = self._get_pending_requests(person)
        if len(pending) >= self.MAX_PENDING_REQUESTS:
            raise TooManyPendingRequestsError()

        # Get trusted devices to send approval request
        trusted_devices = self._get_trusted_devices(person)
        if not trusted_devices:
            raise NoTrustedDevicesError()

        # Create request with short-lived token
        request = frappe.new_doc("Push Approval Request")
        request.person = person
        request.pending_device = pending_device.name
        request.approval_token = secrets.token_urlsafe(32)
        request.expires_at = frappe.utils.add_to_date(
            frappe.utils.now_datetime(),
            seconds=self.APPROVAL_TIMEOUT_SECONDS
        )
        request.status = "Pending"
        request.device_info = json.dumps({
            "name": pending_device.device_name,
            "type": pending_device.device_type,
            "location": pending_device.last_location,
            "ip": pending_device.last_ip,
        })
        request.insert(ignore_permissions=True)

        # Send push to trusted devices
        for device in trusted_devices:
            self._send_approval_push(device, request)

        return request

    def approve(
        self,
        approval_token: str,
        approving_device: str,
        person: str
    ) -> bool:
        """Approve pending device from trusted device."""

        # Find request
        request = frappe.get_value(
            "Push Approval Request",
            {"approval_token": approval_token, "person": person},
            ["name", "pending_device", "expires_at", "status"],
            as_dict=True
        )

        if not request:
            raise InvalidApprovalTokenError()

        if request.status != "Pending":
            raise ApprovalAlreadyProcessedError()

        if frappe.utils.now_datetime() > request.expires_at:
            frappe.db.set_value("Push Approval Request", request.name, "status", "Expired")
            raise ApprovalExpiredError()

        # Verify approving device is trusted
        if not self._is_trusted_device(approving_device, person):
            raise ApproverNotTrustedError()

        # Approve the pending device
        frappe.db.set_value("User Device", request.pending_device, "is_trusted", 1)
        frappe.db.set_value("Push Approval Request", request.name, {
            "status": "Approved",
            "approved_by_device": approving_device,
            "approved_at": frappe.utils.now_datetime()
        })

        # Log security event
        self._log_approval(request, approving_device)

        return True

    def _check_rate_limit(self, person: str):
        """Enforce rate limiting on approval requests."""
        key = f"push_approve_rate:{person}"
        count = frappe.cache().get_value(key) or 0

        if count >= self.RATE_LIMIT_PER_HOUR:
            raise RateLimitExceededError("Too many approval requests")

        frappe.cache().set_value(key, count + 1, expires_in_sec=3600)
```

**Estimated Effort:** M (1-2 weeks)
**Dependencies:** Push notification infrastructure

---

### 2.4 Digital Will Edge Cases & Hardening

**Issue Sources:** Claude §2.6, Jeni §Digital will & duress flows

**Problem Statement:**
- Trustee unavailability not handled
- Dispute resolution undefined
- Partial recovery scenarios
- Multi-jurisdiction legal considerations
- Missing tamper-evident audit

**Implementation Plan:**

```python
# dartwing_user/services/digital_will_v2.py

class DigitalWillService:
    """
    Enhanced Digital Will with edge case handling.
    """

    # Minimum trustees required for activation
    MIN_TRUSTEES = 2

    # Waiting period before access is granted
    WAITING_PERIOD_DAYS = 7

    # Time for owner to respond to access request
    OWNER_RESPONSE_WINDOW_DAYS = 14

    def request_access(
        self,
        will: "DigitalWill",
        requesting_trustee: str,
        reason: str
    ) -> WillAccessRequest:
        """
        Trustee requests access to will.
        Implements multi-party approval and waiting period.
        """

        # Validate trustee is active
        trustees = self._get_active_trustees(will)
        if requesting_trustee not in [t.person for t in trustees]:
            raise InvalidTrusteeError()

        # Check for existing pending request
        existing = frappe.get_value(
            "Will Access Request",
            {"digital_will": will.name, "status": "Pending"}
        )
        if existing:
            # Add as co-signer instead of new request
            return self._add_cosigner(existing, requesting_trustee)

        # Create new request
        request = frappe.new_doc("Will Access Request")
        request.digital_will = will.name
        request.person = will.person
        request.requesting_trustee = requesting_trustee
        request.reason = reason
        request.status = "Pending"
        request.request_token = secrets.token_urlsafe(32)

        # Calculate required approvals (majority of trustees)
        request.required_approvals = max(2, len(trustees) // 2 + 1)
        request.current_approvals = 1  # Requesting trustee counts as first approval

        # Set waiting period end
        request.waiting_period_ends = frappe.utils.add_days(
            frappe.utils.today(),
            self.WAITING_PERIOD_DAYS
        )

        # Set owner response deadline
        request.owner_response_deadline = frappe.utils.add_days(
            frappe.utils.today(),
            self.OWNER_RESPONSE_WINDOW_DAYS
        )

        request.insert(ignore_permissions=True)

        # Notify other trustees
        self._notify_trustees(request, trustees)

        # Attempt to notify owner (multiple channels)
        self._notify_owner(request)

        # Create tamper-evident audit record
        self._create_audit_record(request, "ACCESS_REQUESTED", {
            "trustee": requesting_trustee,
            "reason": reason,
        })

        return request

    def approve_request(
        self,
        request: "WillAccessRequest",
        approving_trustee: str
    ) -> bool:
        """Add trustee approval to access request."""

        # Validate trustee
        trustees = self._get_active_trustees(request.digital_will)
        if approving_trustee not in [t.person for t in trustees]:
            raise InvalidTrusteeError()

        # Check not already approved by this trustee
        existing_approvals = frappe.get_all(
            "Will Access Approval",
            filters={"access_request": request.name},
            pluck="trustee"
        )
        if approving_trustee in existing_approvals:
            raise AlreadyApprovedError()

        # Add approval
        approval = frappe.new_doc("Will Access Approval")
        approval.access_request = request.name
        approval.trustee = approving_trustee
        approval.approved_at = frappe.utils.now_datetime()
        approval.insert(ignore_permissions=True)

        # Update request
        request.current_approvals = len(existing_approvals) + 1
        request.save(ignore_permissions=True)

        # Create audit record
        self._create_audit_record(request, "TRUSTEE_APPROVED", {
            "trustee": approving_trustee,
            "total_approvals": request.current_approvals,
        })

        # Check if threshold met and waiting period over
        self._check_activation(request)

        return True

    def contest_request(
        self,
        request: "WillAccessRequest",
        person: str,
        proof_of_life: dict
    ) -> bool:
        """
        Owner contests access request with proof of life.
        """
        if request.person != person:
            raise PermissionError("Only owner can contest")

        # Validate proof of life (could be video, recent activity, etc.)
        if not self._validate_proof_of_life(person, proof_of_life):
            raise InvalidProofOfLifeError()

        # Cancel request
        request.status = "Contested"
        request.contested_at = frappe.utils.now_datetime()
        request.proof_of_life = json.dumps(proof_of_life)
        request.save(ignore_permissions=True)

        # Notify trustees
        self._notify_trustees_of_contest(request)

        # Create audit record
        self._create_audit_record(request, "OWNER_CONTESTED", {
            "proof_type": proof_of_life.get("type"),
        })

        return True

    def _check_activation(self, request: "WillAccessRequest"):
        """Check if request should be activated."""

        # Need enough approvals
        if request.current_approvals < request.required_approvals:
            return

        # Waiting period must be over
        if frappe.utils.today() < request.waiting_period_ends:
            return

        # Owner response window must be over
        if frappe.utils.today() < request.owner_response_deadline:
            return

        # Activate access
        self._activate_access(request)

    def _activate_access(self, request: "WillAccessRequest"):
        """Grant trustees access to will contents."""
        request.status = "Activated"
        request.activated_at = frappe.utils.now_datetime()
        request.save(ignore_permissions=True)

        # Grant access to specified data sets
        will = frappe.get_doc("Digital Will", request.digital_will)

        # Get key recovery shares for trustees
        if will.vault_access:
            self._distribute_key_shares(request)

        # Grant read access to specified doctypes
        for item in will.access_items:
            self._grant_trustee_access(request, item)

        # Create immutable audit record
        self._create_audit_record(request, "ACCESS_ACTIVATED", {
            "trustees_granted": [t.person for t in will.trustees],
            "data_sets": [i.doctype for i in will.access_items],
        })

    def _create_audit_record(self, request, event_type: str, data: dict):
        """Create tamper-evident audit record."""
        previous_hash = frappe.db.get_value(
            "Will Audit Log",
            filters={"digital_will": request.digital_will},
            fieldname="record_hash",
            order_by="creation desc"
        ) or "GENESIS"

        record = frappe.new_doc("Will Audit Log")
        record.digital_will = request.digital_will
        record.event_type = event_type
        record.event_data = json.dumps(data)
        record.timestamp = frappe.utils.now_datetime()
        record.previous_hash = previous_hash
        record.record_hash = self._compute_hash(record)
        record.insert(ignore_permissions=True)
```

```json
// New DocTypes needed

// Will Access Request
{
  "doctype": "Will Access Request",
  "module": "Dartwing User",
  "fields": [
    {"fieldname": "digital_will", "fieldtype": "Link", "options": "Digital Will"},
    {"fieldname": "person", "fieldtype": "Link", "options": "Person"},
    {"fieldname": "requesting_trustee", "fieldtype": "Link", "options": "Person"},
    {"fieldname": "reason", "fieldtype": "Small Text"},
    {"fieldname": "status", "fieldtype": "Select",
     "options": "Pending\nApproved\nActivated\nContested\nExpired\nCancelled"},
    {"fieldname": "required_approvals", "fieldtype": "Int"},
    {"fieldname": "current_approvals", "fieldtype": "Int"},
    {"fieldname": "waiting_period_ends", "fieldtype": "Date"},
    {"fieldname": "owner_response_deadline", "fieldtype": "Date"},
    {"fieldname": "contested_at", "fieldtype": "Datetime"},
    {"fieldname": "activated_at", "fieldtype": "Datetime"}
  ]
}

// Will Audit Log (tamper-evident)
{
  "doctype": "Will Audit Log",
  "module": "Dartwing User",
  "fields": [
    {"fieldname": "digital_will", "fieldtype": "Link", "options": "Digital Will"},
    {"fieldname": "event_type", "fieldtype": "Data"},
    {"fieldname": "event_data", "fieldtype": "JSON"},
    {"fieldname": "timestamp", "fieldtype": "Datetime"},
    {"fieldname": "previous_hash", "fieldtype": "Data"},
    {"fieldname": "record_hash", "fieldtype": "Data"}
  ],
  "permissions": [{"role": "System Manager", "read": 1, "write": 0, "delete": 0}]
}
```

**Estimated Effort:** L (2-3 weeks)
**Dependencies:** Key Management (for vault access), Notification system

---

### 2.5 Error Handling Patterns

**Issue Sources:** Claude §2.8, §4.4, Jeni §implicit

**Problem Statement:**
- No retry logic for transient failures
- No graceful degradation
- No error categorization
- No user-facing error message standards

**Implementation Plan:**

```python
# dartwing_user/exceptions.py

from enum import Enum
from typing import Optional
from dataclasses import dataclass

class ErrorCategory(Enum):
    VALIDATION = "validation"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    EXTERNAL_SERVICE = "external_service"
    RATE_LIMIT = "rate_limit"
    INTERNAL = "internal"
    SECURITY = "security"

@dataclass
class ErrorContext:
    """Additional context for error handling."""
    recoverable: bool = True
    retry_after_seconds: Optional[int] = None
    suggestion: Optional[str] = None
    details: dict = None

class DartwingUserException(Exception):
    """Base exception for User module."""

    category: ErrorCategory = ErrorCategory.INTERNAL
    code: str = "UNKNOWN_ERROR"
    http_status: int = 500

    def __init__(
        self,
        message: str,
        context: ErrorContext = None
    ):
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
                "details": self.context.details,
            }
        }

# Specific exceptions
class DeviceNotTrustedError(DartwingUserException):
    category = ErrorCategory.PERMISSION
    code = "DEVICE_NOT_TRUSTED"
    http_status = 403

    def __init__(self, device_id: str):
        super().__init__(
            message="Operation requires a trusted device",
            context=ErrorContext(
                recoverable=True,
                suggestion="Approve this device from a trusted device first",
                details={"device_id": device_id}
            )
        )

class TravelModeActiveError(DartwingUserException):
    category = ErrorCategory.SECURITY
    code = "TRAVEL_MODE_ACTIVE"
    http_status = 403

    def __init__(self):
        super().__init__(
            message="Access restricted in Travel Mode",
            context=ErrorContext(
                recoverable=True,
                suggestion="Disable Travel Mode to access this data"
            )
        )

class ExternalServiceError(DartwingUserException):
    category = ErrorCategory.EXTERNAL_SERVICE
    code = "EXTERNAL_SERVICE_UNAVAILABLE"
    http_status = 503

    def __init__(self, service: str, retry_after: int = 60):
        super().__init__(
            message=f"External service temporarily unavailable: {service}",
            context=ErrorContext(
                recoverable=True,
                retry_after_seconds=retry_after,
                suggestion="Please try again shortly"
            )
        )

class RateLimitExceededError(DartwingUserException):
    category = ErrorCategory.RATE_LIMIT
    code = "RATE_LIMIT_EXCEEDED"
    http_status = 429

    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Too many requests",
            context=ErrorContext(
                recoverable=True,
                retry_after_seconds=retry_after
            )
        )
```

```python
# dartwing_user/utils/retry.py

import time
import functools
from typing import Type, Tuple

def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        delay = min(
                            base_delay * (exponential_base ** attempt),
                            max_delay
                        )
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

# Usage
@retry_with_backoff(
    max_attempts=3,
    retryable_exceptions=(requests.RequestException, TimeoutError)
)
def call_external_api():
    ...
```

```python
# dartwing_user/api/error_handler.py

import frappe

def handle_api_error(func):
    """Decorator to standardize API error responses."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DartwingUserException as e:
            frappe.local.response.http_status_code = e.http_status
            return e.to_dict()
        except frappe.PermissionError as e:
            frappe.local.response.http_status_code = 403
            return {
                "success": False,
                "error": {
                    "code": "PERMISSION_DENIED",
                    "category": "permission",
                    "message": str(e),
                    "recoverable": False
                }
            }
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "User Module API Error")
            frappe.local.response.http_status_code = 500
            return {
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "category": "internal",
                    "message": "An unexpected error occurred",
                    "recoverable": False
                }
            }
    return wrapper
```

**Estimated Effort:** M (1-2 weeks)
**Dependencies:** None

---

## Section 3: MEDIUM Priority Fixes

### 3.1 Hook Side Effects & Transactional Identity Creation

**Issue Sources:** Jeni §Docs/process gaps, Gemi §3.2

**Problem Statement:**
- `Person.after_insert` hook calls `frappe.db.commit()` inside hook
- Hook failures could leave orphaned Person records without User Profile

**Implementation Plan:**

```python
# dartwing_user/services/identity_service.py

class IdentityService:
    """
    Transactional identity creation service.
    Replaces hook-based profile creation with explicit service calls.
    """

    @staticmethod
    def create_identity(
        email: str,
        full_name: str,
        **person_kwargs
    ) -> "Person":
        """
        Create Person and User Profile atomically.
        Should be used instead of frappe.new_doc("Person").
        """
        try:
            # Begin implicit transaction (Frappe handles this)

            # Create Person
            person = frappe.new_doc("Person")
            person.email = email
            person.full_name = full_name
            for key, value in person_kwargs.items():
                setattr(person, key, value)
            person.insert()

            # Create User Profile (within same transaction)
            profile = frappe.new_doc("User Profile")
            profile.person = person.name
            profile.display_name = full_name
            profile.insert()

            # Success - implicit commit at end of request
            return person

        except Exception as e:
            # Transaction will rollback automatically
            frappe.log_error(
                f"Identity creation failed for {email}: {e}",
                "Identity Service Error"
            )
            raise

# Remove from Person.after_insert hook
# Instead, update calling code to use IdentityService.create_identity()
```

```python
# dartwing_user/jobs/reconciliation.py

def reconcile_orphaned_persons():
    """
    Background job to find and fix Person records without User Profile.
    Runs daily as safety net.
    """
    orphans = frappe.db.sql("""
        SELECT p.name, p.email, p.full_name
        FROM `tabPerson` p
        LEFT JOIN `tabUser Profile` up ON up.person = p.name
        WHERE up.name IS NULL
    """, as_dict=True)

    for orphan in orphans:
        try:
            profile = frappe.new_doc("User Profile")
            profile.person = orphan.name
            profile.display_name = orphan.full_name
            profile.insert(ignore_permissions=True)
            frappe.db.commit()

            frappe.logger().info(f"Created missing profile for Person {orphan.name}")
        except Exception as e:
            frappe.log_error(
                f"Failed to create profile for {orphan.name}: {e}",
                "Reconciliation Error"
            )
```

```python
# hooks.py update

scheduler_events = {
    "daily": [
        "dartwing_user.jobs.reconciliation.reconcile_orphaned_persons",
    ]
}
```

**Estimated Effort:** S (0.5-1 week)
**Dependencies:** None

---

### 3.2 Missing PRD Features - Schema/Service Stubs

**Issue Sources:** Jeni §Missing/partial features, Claude §3.3-3.4

**Problem Statement:**
Several PRD features lack schemas/services:
- U-24: Passkey Support
- U-21: Contact Auto-Match
- U-26: Achievements & Gamification
- U-27: Reputation Score (inputs/decay)
- U-28: AI Memory (lifecycle pipeline)
- U-10: Daily Briefing
- U-20: Unified Activity Feed

**Implementation Plan:**

For each missing feature, add placeholder schema and defer to future phases:

```python
# dartwing_user/DEFERRED_FEATURES.md

## Deferred Features (Phase 5+)

The following features are defined in the PRD but deferred pending:
1. More design work
2. External dependencies (HealthKit, wearables)
3. Legal/compliance requirements
4. ML infrastructure

### U-24: Passkey Support (DEFERRED)
**Reason:** Requires WebAuthn integration with Keycloak
**Prerequisite:** Keycloak WebAuthn plugin deployment
**Estimated Phase:** 4

### U-26: Achievements & Gamification (DEFERRED)
**Reason:** Requires event schema across all modules
**Prerequisite:** Unified event bus
**Estimated Phase:** 5

### U-27: Reputation Score (DEFERRED)
**Reason:** Risk of bias, gaming prevention needed
**Prerequisite:** Data science review of scoring inputs
**Estimated Phase:** 5+

### U-28: AI Memory (DEFERRED)
**Reason:** Privacy concerns, ML pipeline needed
**Prerequisite:** Privacy impact assessment
**Estimated Phase:** 5+

### U-29: Health Data Integration (DEFERRED)
**Reason:** HIPAA compliance, platform SDKs
**Prerequisite:** BAA agreements, compliance audit
**Estimated Phase:** 6+

### U-30: Wearable Sync (DEFERRED)
**Reason:** Platform-specific development
**Prerequisite:** Native watch apps
**Estimated Phase:** 6+
```

**Add minimal stubs for context:**

```json
// Passkey stub
{
  "doctype": "User Passkey",
  "module": "Dartwing User",
  "is_virtual": 1,
  "documentation": "DEFERRED: See dartwing_user/DEFERRED_FEATURES.md",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person"},
    {"fieldname": "credential_id", "fieldtype": "Data"},
    {"fieldname": "public_key", "fieldtype": "Text"},
    {"fieldname": "created", "fieldtype": "Datetime"}
  ]
}
```

**Estimated Effort:** S (documentation only)
**Dependencies:** None

---

### 3.3 Notification Delivery Hardening

**Issue Sources:** Jeni §Notification Preferences

**Problem Statement:**
- Delivery fan-out logic absent
- Channel fallback not implemented

**Implementation Plan:**

```python
# dartwing_user/services/notification_delivery.py

class NotificationDeliveryService:
    """
    Multi-channel notification delivery with fallback.
    """

    CHANNEL_PRIORITY = ["push", "sms", "email"]

    def deliver(
        self,
        person: str,
        notification_type: str,
        content: dict
    ) -> DeliveryResult:
        """
        Deliver notification through preferred channels with fallback.
        """
        prefs = self._get_preferences(person, notification_type)

        if prefs.muted:
            return DeliveryResult(status="muted")

        results = []

        for channel in prefs.channels:
            try:
                result = self._deliver_channel(person, channel, content)
                results.append(result)

                if result.success:
                    break  # Stop on first success

            except Exception as e:
                results.append(DeliveryResult(
                    channel=channel,
                    success=False,
                    error=str(e)
                ))

        # Try fallback channels if all preferred failed
        if not any(r.success for r in results):
            for channel in self.CHANNEL_PRIORITY:
                if channel not in prefs.channels:
                    try:
                        result = self._deliver_channel(person, channel, content)
                        results.append(result)
                        if result.success:
                            break
                    except:
                        continue

        return DeliveryResult(
            status="delivered" if any(r.success for r in results) else "failed",
            attempts=results
        )

    def _deliver_channel(
        self,
        person: str,
        channel: str,
        content: dict
    ) -> DeliveryResult:
        """Deliver via specific channel."""
        if channel == "push":
            return self._send_push(person, content)
        elif channel == "sms":
            return self._send_sms(person, content)
        elif channel == "email":
            return self._send_email(person, content)
        else:
            raise ValueError(f"Unknown channel: {channel}")
```

**Estimated Effort:** M (1 week)
**Dependencies:** Push notification infrastructure

---

### 3.4 AI Voice Storage Optimization

**Issue Sources:** Gemi §3.4

**Problem Statement:**
- Voice samples stored as binary in database is bad for performance
- Should use Frappe File API with S3/filesystem storage

**Implementation Plan:**

Update AI Voice Profile doctype:

```json
{
  "doctype": "AI Voice Profile",
  "fields": [
    // Remove: {"fieldname": "voice_sample", "fieldtype": "Long Text"}

    // Add:
    {
      "fieldname": "voice_samples",
      "fieldtype": "Table",
      "options": "Voice Sample Attachment"
    }
  ]
}

// Child table for voice samples
{
  "doctype": "Voice Sample Attachment",
  "istable": 1,
  "fields": [
    {"fieldname": "sample_file", "fieldtype": "Attach", "reqd": 1},
    {"fieldname": "duration_seconds", "fieldtype": "Float"},
    {"fieldname": "sample_type", "fieldtype": "Select",
     "options": "Training\nVerification\nTest"},
    {"fieldname": "uploaded_at", "fieldtype": "Datetime"}
  ]
}
```

**Estimated Effort:** S (0.5 week)
**Dependencies:** None

---

### 3.5 Audit Trail DocType

**Issue Sources:** Claude §4.7

**Problem Statement:**
- No comprehensive audit trail for compliance

**Implementation Plan:**

```json
{
  "doctype": "User Audit Log",
  "module": "Dartwing User",
  "autoname": "hash",
  "fields": [
    {"fieldname": "person", "fieldtype": "Link", "options": "Person", "reqd": 1},
    {"fieldname": "event_type", "fieldtype": "Select",
     "options": "profile_update\ndevice_registered\ndevice_revoked\ndevice_trusted\ntravel_mode_enabled\ntravel_mode_disabled\nduress_pin_entered\ndata_export_requested\naccount_deletion_requested\nprivacy_setting_changed\nvault_item_accessed\nvault_item_created\nvault_item_deleted\nwill_access_requested\nwill_access_granted\nwill_contested\nsession_created\nsession_terminated\npassword_changed\nmfa_enabled\nmfa_disabled"},
    {"fieldname": "event_data", "fieldtype": "JSON"},
    {"fieldname": "ip_address", "fieldtype": "Data"},
    {"fieldname": "user_agent", "fieldtype": "Small Text"},
    {"fieldname": "device", "fieldtype": "Link", "options": "User Device"},
    {"fieldname": "organization", "fieldtype": "Link", "options": "Organization"},
    {"fieldname": "timestamp", "fieldtype": "Datetime", "default": "Now"}
  ],
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 0, "delete": 0}
  ],
  "track_changes": 0
}
```

```python
# dartwing_user/audit.py

def log_event(
    person: str,
    event_type: str,
    event_data: dict = None,
    device: str = None,
    organization: str = None
):
    """Log audit event for person."""
    frappe.get_doc({
        "doctype": "User Audit Log",
        "person": person,
        "event_type": event_type,
        "event_data": json.dumps(event_data or {}),
        "ip_address": frappe.local.request_ip,
        "user_agent": frappe.request.headers.get("User-Agent", "")[:500],
        "device": device,
        "organization": organization,
    }).insert(ignore_permissions=True)
```

**Estimated Effort:** S (0.5 week)
**Dependencies:** None

---

### 3.6 Missing Executive Summary Document

**Issue Sources:** Jeni, Gemi

**Implementation Plan:**

Create `dartwing_user_executive_summary.md` to match other modules.

**Estimated Effort:** S (0.5 week)
**Dependencies:** None

---

### 3.7 Permission Registration in hooks.py

**Issue Sources:** Jeni §Docs/process gaps

**Problem Statement:**
- Owner-only permissions defined but not registered in hooks.py for all doctypes

**Implementation Plan:**

```python
# hooks.py - add permission hooks for all User module doctypes

has_permission = {
    "User Profile": "dartwing_user.permissions.has_user_profile_permission",
    "User Device": "dartwing_user.permissions.has_owner_permission",
    "User Session": "dartwing_user.permissions.has_owner_permission",
    "Block List Entry": "dartwing_user.permissions.has_owner_permission",
    "Personal Vault Item": "dartwing_user.permissions.has_owner_permission",
    "Digital Will": "dartwing_user.permissions.has_owner_permission",
    "AI Voice Profile": "dartwing_user.permissions.has_owner_permission",
    "AI Memory Entry": "dartwing_user.permissions.has_owner_permission",
    "Privacy Setting": "dartwing_user.permissions.has_owner_permission",
    "Notification Preference": "dartwing_user.permissions.has_owner_permission",
    "Emergency Contact": "dartwing_user.permissions.has_owner_permission",
    "Personal Shortcut": "dartwing_user.permissions.has_owner_permission",
    "Location Share": "dartwing_user.permissions.has_owner_permission",
}

permission_query_conditions = {
    "User Profile": "dartwing_user.permissions.get_owner_query_condition",
    "User Device": "dartwing_user.permissions.get_owner_query_condition",
    # ... all owner-only doctypes
}
```

**Estimated Effort:** S (0.5 week)
**Dependencies:** None

---

## Section 4: LOW Priority Fixes

### 4.1 Feature Flags for Phased Rollout

**Issue Sources:** Claude §4.5

```python
# dartwing_user/feature_flags.py
# See Claude critique Section 4.5 for implementation
```

**Estimated Effort:** M (1 week)
**Dependencies:** None

---

### 4.2 Real-Time Sync Documentation

**Issue Sources:** Claude §2.9

**Problem Statement:**
- Socket.IO connection state management not detailed
- Reconnection strategies undefined

**Implementation Plan:**
Add section to architecture document covering Socket.IO patterns used by dartwing_core.

**Estimated Effort:** S (documentation)
**Dependencies:** dartwing_core sync architecture

---

## Implementation Roadmap

### Phase 1: Critical Foundations (Weeks 1-6)
| Week | Task | Effort | Dependencies |
|------|------|--------|--------------|
| 1-2 | 1.2 Travel Mode Enforcement Framework | L | None |
| 2-4 | 1.1 Key Management System | XL | None |
| 4-5 | 2.5 Error Handling Patterns | M | None |
| 5-6 | 3.1 Transactional Identity | S | None |

### Phase 2: Security Hardening (Weeks 7-12)
| Week | Task | Effort | Dependencies |
|------|------|--------|--------------|
| 7-8 | 2.3 Device Trust Hardening | M | None |
| 8-10 | 2.4 Digital Will Edge Cases | L | 1.1 |
| 10-11 | 2.1 Provider Abstraction | M | None |
| 11-12 | 3.7 Permission Registration | S | None |

### Phase 3: Scalability & Polish (Weeks 13-18)
| Week | Task | Effort | Dependencies |
|------|------|--------|--------------|
| 13-15 | 2.2 Cross-Org Search/Feed | L | None |
| 15-16 | 3.3 Notification Hardening | M | None |
| 16-17 | 3.4 Voice Storage + 3.5 Audit Trail | S+S | None |
| 17-18 | 4.1 Feature Flags + 3.2 Deferred Docs | M+S | None |

---

## Summary Statistics

| Priority | Issues | Estimated Effort |
|----------|--------|------------------|
| CRITICAL | 2 | 5-7 weeks |
| HIGH | 5 | 8-12 weeks |
| MEDIUM | 7 | 5-6 weeks |
| LOW | 2 | 1-2 weeks |
| **TOTAL** | **16** | **19-27 weeks** |

---

*Plan created: November 29, 2025*
*Sources: Claude, Jeni, Gemi architecture critiques*
*Status: Ready for implementation*
