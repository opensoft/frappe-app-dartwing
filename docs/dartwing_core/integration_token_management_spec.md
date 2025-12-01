# Integration Token Management Specification

**Objective:** Define secure, reliable OAuth2 token lifecycle management for third-party integrations.

## Goals

- Proactively refresh tokens before expiration to prevent API failures
- Encrypt credentials at rest using strong cryptography
- Handle refresh failures gracefully with admin notifications
- Support multiple concurrent integrations per organization
- Thread-safe token access for parallel requests

## Problem Statement

Third-party integrations (Google, Slack, QuickBooks, etc.) use OAuth2 tokens that expire. Without proper lifecycle management:

- API calls fail when tokens expire mid-operation
- Race conditions occur when multiple requests refresh simultaneously
- Expired tokens go unnoticed until users report failures
- Credentials stored in plaintext are security risks

## Architecture

### Token Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN LIFECYCLE MANAGEMENT                    │
│                                                                  │
│  ┌──────────────┐                                               │
│  │ OAuth Flow   │                                               │
│  │ (User Auth)  │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Organization Integration (Doctype)                       │   │
│  │                                                           │   │
│  │  - access_token (encrypted)                              │   │
│  │  - refresh_token (encrypted)                             │   │
│  │  - expires_at (datetime)                                 │   │
│  │  - status: Connected | Expired | Error                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  TokenManager (Singleton)                                 │   │
│  │                                                           │   │
│  │  get_access_token(integration, org)                      │   │
│  │    1. Check expiry (with 5-min buffer)                   │   │
│  │    2. Refresh if needed (thread-safe)                    │   │
│  │    3. Return decrypted token                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Proactive Refresh Job (every 5 minutes)                 │   │
│  │                                                           │   │
│  │  - Find tokens expiring in next 10 minutes               │   │
│  │  - Refresh before they expire                            │   │
│  │  - Notify admins on refresh failure                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Model

### Organization Integration Doctype

```json
{
    "doctype": "Organization Integration",
    "module": "Dartwing Core",
    "autoname": "hash",
    "fields": [
        {
            "fieldname": "organization",
            "label": "Organization",
            "fieldtype": "Link",
            "options": "Organization",
            "reqd": 1
        },
        {
            "fieldname": "integration",
            "label": "Integration",
            "fieldtype": "Select",
            "options": "Google\nSlack\nQuickBooks\nSalesforce\nZapier\nMicrosoft365",
            "reqd": 1
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "Connected\nExpired\nError\nDisconnected",
            "default": "Connected"
        },
        {
            "fieldname": "access_token",
            "label": "Access Token",
            "fieldtype": "Password",
            "hidden": 1
        },
        {
            "fieldname": "refresh_token",
            "label": "Refresh Token",
            "fieldtype": "Password",
            "hidden": 1
        },
        {
            "fieldname": "expires_at",
            "label": "Token Expires At",
            "fieldtype": "Datetime"
        },
        {
            "fieldname": "last_refreshed",
            "label": "Last Refreshed",
            "fieldtype": "Datetime"
        },
        {
            "fieldname": "error_message",
            "label": "Error Message",
            "fieldtype": "Small Text"
        },
        {
            "fieldname": "connected_by",
            "label": "Connected By",
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "connected_at",
            "label": "Connected At",
            "fieldtype": "Datetime"
        }
    ]
}
```

## Implementation

### TokenManager Class

```python
# dartwing_core/integrations/token_manager.py

import os
import threading
from datetime import timedelta
from cryptography.fernet import Fernet
import frappe
from frappe.utils import now_datetime


class IntegrationNotConnectedError(Exception):
    pass


class IntegrationReauthRequiredError(Exception):
    pass


class TokenManager:
    """
    Centralized OAuth token management with:
    - Proactive refresh before expiry
    - Thread-safe per-token locking
    - Encrypted credential storage
    - Admin notification on auth failure
    """

    REFRESH_BUFFER_SECONDS = 300  # Refresh 5 min before expiry
    _locks: dict[str, threading.Lock] = {}
    _encryption_key: bytes = None

    @classmethod
    def get_access_token(
        cls,
        integration: str,
        organization: str,
    ) -> str:
        """
        Get valid access token, refreshing if needed.

        Args:
            integration: Integration name (e.g., "Google", "Slack")
            organization: Organization name

        Returns:
            Decrypted access token

        Raises:
            IntegrationNotConnectedError: Integration not set up
            IntegrationReauthRequiredError: Refresh token expired
        """
        token_key = f"{integration}:{organization}"

        # Get or create lock for this token
        if token_key not in cls._locks:
            cls._locks[token_key] = threading.Lock()

        with cls._locks[token_key]:
            token_doc = cls._get_token_doc(integration, organization)

            if not token_doc:
                raise IntegrationNotConnectedError(
                    f"{integration} not connected for {organization}"
                )

            if token_doc.status == "Expired":
                raise IntegrationReauthRequiredError(
                    f"{integration} requires reconnection"
                )

            if cls._needs_refresh(token_doc):
                token_doc = cls._refresh_token(token_doc)

            return cls._decrypt(token_doc.access_token)

    @classmethod
    def _get_token_doc(cls, integration: str, organization: str):
        """Fetch token document from database."""
        name = frappe.db.get_value(
            "Organization Integration",
            {"integration": integration, "organization": organization},
            "name"
        )
        if name:
            return frappe.get_doc("Organization Integration", name)
        return None

    @classmethod
    def _needs_refresh(cls, token_doc) -> bool:
        """Check if token needs refresh (expiring within buffer period)."""
        if not token_doc.expires_at:
            return False

        threshold = now_datetime() + timedelta(
            seconds=cls.REFRESH_BUFFER_SECONDS
        )
        return token_doc.expires_at <= threshold

    @classmethod
    def _refresh_token(cls, token_doc):
        """
        Refresh token using provider-specific logic.
        Updates database and returns updated doc.
        """
        from dartwing_core.integrations.providers import get_provider

        provider = get_provider(token_doc.integration)

        try:
            refresh_token = cls._decrypt(token_doc.refresh_token)
            new_tokens = provider.refresh_access_token(refresh_token)

            # Update token document
            token_doc.access_token = cls._encrypt(new_tokens["access_token"])
            token_doc.expires_at = now_datetime() + timedelta(
                seconds=new_tokens.get("expires_in", 3600)
            )

            # Some providers rotate refresh tokens
            if "refresh_token" in new_tokens:
                token_doc.refresh_token = cls._encrypt(
                    new_tokens["refresh_token"]
                )

            token_doc.last_refreshed = now_datetime()
            token_doc.status = "Connected"
            token_doc.error_message = None
            token_doc.save(ignore_permissions=True)
            frappe.db.commit()

            frappe.logger().info(
                f"Token refreshed: {token_doc.integration} for {token_doc.organization}"
            )

            return token_doc

        except Exception as e:
            # Check if refresh token expired
            if "invalid_grant" in str(e).lower():
                token_doc.status = "Expired"
                token_doc.error_message = "Refresh token expired - reconnection required"
                token_doc.save(ignore_permissions=True)
                frappe.db.commit()

                cls._notify_reconnection_needed(token_doc)
                raise IntegrationReauthRequiredError(
                    f"{token_doc.integration} requires reconnection"
                )

            # Other errors - mark as error state
            token_doc.status = "Error"
            token_doc.error_message = str(e)[:500]
            token_doc.save(ignore_permissions=True)
            frappe.db.commit()

            frappe.logger().error(
                f"Token refresh failed: {token_doc.integration}",
                exc_info=True
            )
            raise

    @classmethod
    def _encrypt(cls, value: str) -> str:
        """Encrypt credential value using Fernet symmetric encryption."""
        if cls._encryption_key is None:
            cls._encryption_key = cls._get_encryption_key()

        f = Fernet(cls._encryption_key)
        return f.encrypt(value.encode()).decode()

    @classmethod
    def _decrypt(cls, encrypted: str) -> str:
        """Decrypt credential value."""
        if cls._encryption_key is None:
            cls._encryption_key = cls._get_encryption_key()

        f = Fernet(cls._encryption_key)
        return f.decrypt(encrypted.encode()).decode()

    @classmethod
    def _get_encryption_key(cls) -> bytes:
        """
        Get encryption key from secure storage.
        Priority: frappe.conf > environment > error
        """
        # Option 1: From site config
        key = frappe.conf.get("integration_encryption_key")
        if key:
            return key.encode() if isinstance(key, str) else key

        # Option 2: From environment variable
        key = os.environ.get("DARTWING_INTEGRATION_KEY")
        if key:
            return key.encode()

        # No key configured - this is a setup error
        frappe.throw(
            "Integration encryption key not configured. "
            "Set 'integration_encryption_key' in site_config.json or "
            "DARTWING_INTEGRATION_KEY environment variable."
        )

    @classmethod
    def _notify_reconnection_needed(cls, token_doc):
        """Notify org admins that integration needs reconnection."""
        admins = frappe.get_all(
            "Org Member",
            filters={
                "organization": token_doc.organization,
                "role": ["in", ["Admin", "Owner"]],
                "status": "Active"
            },
            pluck="person"
        )

        # Get user emails for admins
        for person in admins:
            user = frappe.db.get_value("Person", person, "frappe_user")
            if user:
                # Send real-time notification
                frappe.publish_realtime(
                    "integration_expired",
                    {
                        "integration": token_doc.integration,
                        "organization": token_doc.organization,
                        "message": f"{token_doc.integration} connection expired. Please reconnect.",
                    },
                    user=user
                )

                # Queue email notification
                frappe.enqueue(
                    "dartwing_core.integrations.notifications.send_reconnect_email",
                    user=user,
                    integration=token_doc.integration,
                    organization=token_doc.organization
                )
```

### Proactive Refresh Scheduler

```python
# dartwing_core/integrations/scheduler.py

import frappe
from frappe.utils import now_datetime
from datetime import timedelta


def proactive_token_refresh():
    """
    Scheduled job: Run every 5 minutes.
    Refreshes tokens BEFORE they expire to prevent API failures.
    """
    # Find tokens expiring in the next 10 minutes
    expiring_threshold = now_datetime() + timedelta(minutes=10)

    expiring_tokens = frappe.get_all(
        "Organization Integration",
        filters={
            "status": "Connected",
            "expires_at": ["<=", expiring_threshold]
        },
        fields=["name", "integration", "organization"]
    )

    from dartwing_core.integrations.token_manager import TokenManager

    refreshed = 0
    failed = 0

    for token in expiring_tokens:
        try:
            TokenManager.get_access_token(
                token.integration,
                token.organization
            )
            refreshed += 1
            frappe.db.commit()
        except Exception as e:
            failed += 1
            frappe.log_error(
                f"Proactive refresh failed: {token.integration} for {token.organization}",
                str(e)
            )

    if refreshed or failed:
        frappe.logger().info(
            f"Proactive token refresh: {refreshed} refreshed, {failed} failed"
        )
```

### Hooks Configuration

```python
# dartwing_core/hooks.py

scheduler_events = {
    "cron": {
        # Run every 5 minutes
        "*/5 * * * *": [
            "dartwing_core.integrations.scheduler.proactive_token_refresh"
        ]
    }
}
```

## Configuration

### Encryption Key Setup

Generate a Fernet key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add to `site_config.json`:

```json
{
    "integration_encryption_key": "your-fernet-key-here"
}
```

Or set environment variable:

```bash
export DARTWING_INTEGRATION_KEY="your-fernet-key-here"
```

### Key Rotation

1. Generate new key
2. Decrypt all tokens with old key, re-encrypt with new key (migration script)
3. Update configuration
4. Restart workers

## Provider Interface

```python
# dartwing_core/integrations/providers/base.py

from abc import ABC, abstractmethod


class IntegrationProvider(ABC):
    """Base class for OAuth2 integration providers."""

    @abstractmethod
    def get_authorize_url(self, state: str, redirect_uri: str) -> str:
        """Generate OAuth2 authorization URL."""
        pass

    @abstractmethod
    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for tokens."""
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh access token.

        Returns:
            dict with keys: access_token, expires_in, refresh_token (optional)
        """
        pass

    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """Revoke token on disconnect."""
        pass
```

## Observability

### Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `integration_tokens_total` | gauge | `integration`, `status` | Token count by status |
| `integration_refresh_total` | counter | `integration`, `result` | Refresh attempts (success/failure) |
| `integration_refresh_latency_ms` | histogram | `integration` | Refresh operation latency |
| `integration_expiring_soon` | gauge | `integration` | Tokens expiring in next hour |

### Alerts

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Token expired | status = "Expired" | Warning | Notify org admins |
| Refresh failures | > 5 failures in 1 hour | Warning | Check provider status |
| No healthy tokens | All org tokens expired | Critical | Page on-call |
| Key not configured | Encryption key missing | Critical | Block startup |

## Security Considerations

1. **Encryption at Rest:** All tokens encrypted with Fernet (AES-128-CBC)
2. **Key Management:** Encryption key stored in config, not database
3. **Access Control:** Token doctype restricted to System Manager
4. **Audit Trail:** All token operations logged with timestamp and user
5. **No Plaintext Logging:** Tokens never logged in plaintext

## Test Matrix

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Get valid token | Request with valid non-expired token | Token returned |
| Auto-refresh | Request with token expiring in 2 min | Token refreshed, new token returned |
| Expired refresh token | Refresh with invalid refresh token | `IntegrationReauthRequiredError` raised |
| Concurrent requests | 10 parallel requests for same token | Only one refresh, all get valid token |
| Missing integration | Request for non-existent integration | `IntegrationNotConnectedError` raised |
| Proactive refresh | Token expiring in 8 min, scheduler runs | Token refreshed before expiry |
| Encryption roundtrip | Encrypt then decrypt value | Original value recovered |

---

*Specification version: 1.0*
*Last updated: November 2025*
