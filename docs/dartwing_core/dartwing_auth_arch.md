# Dartwing Authentication Architecture

**Version 1.0 | November 2025**

_Keycloak-Based Identity Management for Flutter + Frappe_

---

## Table of Contents

1. Overview
2. Architecture Diagram
3. Keycloak Configuration
4. Client Types & Flows
5. Frappe Integration
6. Flutter Mobile Integration
7. Token Management
8. Personal vs Business Identity
9. Multi-Factor Authentication
10. Social Login Providers
11. Session Management
12. Security Considerations
13. Implementation Guide

---

## 1. Overview

Dartwing uses **Keycloak** as the central Identity Provider (IdP) for all authentication across:

- Flutter mobile apps (iOS, Android)
- Flutter web app
- Flutter desktop apps
- Frappe backend (Desk + API)
- Frappe Builder websites
- External third-party integrations

### 1.1 Design Principles

- **Single Source of Truth:** Keycloak manages all user identities
- **SSO Everywhere:** One login works across all Dartwing applications
- **API-First:** All auth flows work via standard OAuth2/OIDC protocols
- **Personal/Business Separation:** Users have distinct personal and organizational identities
- **Zero Trust:** Every request is authenticated, tokens are short-lived

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                         │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│  Flutter Mobile │  Flutter Web    │  Flutter Desktop│  External Websites    │
│  (iOS/Android)  │  (PWA)          │  (macOS/Win/Lin)│  (React/Vue/etc)      │
└────────┬────────┴────────┬────────┴────────┬────────┴───────────┬───────────┘
         │                 │                 │                     │
         │         OAuth2 + PKCE / OIDC      │                     │
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEYCLOAK SERVER                                    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         REALMS                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │  │
│  │  │  dartwing-dev   │  │  dartwing-prod  │  │  dartwing-test  │       │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │    Clients      │  │  Identity       │  │  User           │             │
│  │ - dartwing-app  │  │  Providers      │  │  Federation     │             │
│  │ - frappe-api    │  │ - Google        │  │ - LDAP          │             │
│  │ - web-portal    │  │ - Apple         │  │ - SAML          │             │
│  │ - admin-cli     │  │ - Facebook      │  │ - Active Dir    │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       │ Token Validation / User Info
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRAPPE BACKEND                                     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Social Login Key (OIDC Client)                     │  │
│  │  - Validates tokens from Keycloak                                     │  │
│  │  - Creates/maps Frappe User from Keycloak identity                   │  │
│  │  - Syncs roles/permissions from Keycloak groups                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  REST API       │  │  Frappe Desk    │  │  Frappe Builder │             │
│  │  /api/resource  │  │  (Admin UI)     │  │  (Public Site)  │             │
│  │  /api/method    │  │                 │  │                 │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Keycloak Configuration

### 3.1 Realm Structure

Each environment has its own realm:

| Realm           | Purpose     | Base URL                                             |
| --------------- | ----------- | ---------------------------------------------------- |
| `dartwing-dev`  | Development | `https://auth-dev.dartwing.io/realms/dartwing-dev`   |
| `dartwing-test` | Staging/QA  | `https://auth-test.dartwing.io/realms/dartwing-test` |
| `dartwing-prod` | Production  | `https://auth.dartwing.io/realms/dartwing-prod`      |

### 3.2 Clients Configuration

#### dartwing-mobile (Public Client)

```json
{
  "clientId": "dartwing-mobile",
  "name": "Dartwing Mobile App",
  "protocol": "openid-connect",
  "publicClient": true,
  "standardFlowEnabled": true,
  "directAccessGrantsEnabled": false,
  "attributes": {
    "pkce.code.challenge.method": "S256"
  },
  "redirectUris": [
    "io.dartwing.app://callback",
    "io.dartwing.app://logout-callback"
  ],
  "webOrigins": ["+"]
}
```

#### dartwing-web (Public Client)

```json
{
  "clientId": "dartwing-web",
  "name": "Dartwing Web App",
  "protocol": "openid-connect",
  "publicClient": true,
  "standardFlowEnabled": true,
  "attributes": {
    "pkce.code.challenge.method": "S256"
  },
  "redirectUris": [
    "https://app.dartwing.io/callback",
    "https://app.dartwing.io/logout-callback",
    "http://localhost:3000/callback"
  ],
  "webOrigins": ["https://app.dartwing.io", "http://localhost:3000"]
}
```

#### frappe-backend (Confidential Client)

```json
{
  "clientId": "frappe-backend",
  "name": "Frappe API Server",
  "protocol": "openid-connect",
  "publicClient": false,
  "standardFlowEnabled": true,
  "serviceAccountsEnabled": true,
  "authorizationServicesEnabled": true,
  "secret": "${FRAPPE_CLIENT_SECRET}",
  "redirectUris": [
    "https://api.dartwing.io/api/method/frappe.integrations.oauth2_logins.custom"
  ]
}
```

### 3.3 Realm Settings

```json
{
  "realm": "dartwing-prod",
  "enabled": true,
  "registrationAllowed": true,
  "registrationEmailAsUsername": true,
  "verifyEmail": true,
  "resetPasswordAllowed": true,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "sslRequired": "external",
  "accessTokenLifespan": 300,
  "refreshTokenMaxReuse": 0,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "offlineSessionIdleTimeout": 2592000,
  "accessCodeLifespan": 60,
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5
}
```

---

## 4. Client Types & Flows

### 4.1 Authorization Code Flow with PKCE (Mobile/Web Apps)

Used by Flutter mobile, web, and desktop apps.

```
┌──────────┐                              ┌──────────┐                              ┌──────────┐
│  Flutter │                              │ Keycloak │                              │  Frappe  │
│   App    │                              │  Server  │                              │  Backend │
└────┬─────┘                              └────┬─────┘                              └────┬─────┘
     │                                         │                                         │
     │ 1. Generate code_verifier + code_challenge                                        │
     │                                         │                                         │
     │ 2. Open browser/webview                 │                                         │
     │────────────────────────────────────────►│                                         │
     │    GET /auth?response_type=code         │                                         │
     │        &client_id=dartwing-mobile       │                                         │
     │        &redirect_uri=io.dartwing.app://callback                                   │
     │        &code_challenge={challenge}      │                                         │
     │        &code_challenge_method=S256      │                                         │
     │        &scope=openid profile email      │                                         │
     │                                         │                                         │
     │ 3. User authenticates                   │                                         │
     │◄────────────────────────────────────────│                                         │
     │    Redirect: io.dartwing.app://callback?code={auth_code}                          │
     │                                         │                                         │
     │ 4. Exchange code for tokens             │                                         │
     │────────────────────────────────────────►│                                         │
     │    POST /token                          │                                         │
     │        grant_type=authorization_code    │                                         │
     │        code={auth_code}                 │                                         │
     │        code_verifier={verifier}         │                                         │
     │                                         │                                         │
     │◄────────────────────────────────────────│                                         │
     │    {access_token, refresh_token, id_token}                                        │
     │                                         │                                         │
     │ 5. Call Frappe API with access_token    │                                         │
     │─────────────────────────────────────────┼────────────────────────────────────────►│
     │    GET /api/resource/Organization       │                                         │
     │    Authorization: Bearer {access_token} │                                         │
     │                                         │                                         │
     │                                         │ 6. Validate token                       │
     │                                         │◄────────────────────────────────────────│
     │                                         │    GET /userinfo or introspect          │
     │                                         │────────────────────────────────────────►│
     │                                         │                                         │
     │◄────────────────────────────────────────┼─────────────────────────────────────────│
     │    {data}                               │                                         │
```

### 4.2 Client Credentials Flow (Service-to-Service)

Used for backend services, background jobs, integrations.

```
POST /realms/dartwing-prod/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=frappe-backend
&client_secret={secret}
&scope=openid
```

### 4.3 Resource Owner Password Grant (Legacy/Testing Only)

**NOT recommended for production.** Only for testing or legacy system migration.

```
POST /realms/dartwing-prod/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&client_id=dartwing-mobile
&username=user@example.com
&password=secret123
&scope=openid profile email
```

---

## 5. Frappe Integration

### 5.1 Social Login Key Configuration

Frappe connects to Keycloak as an OIDC client via the Social Login Key doctype.

```json
{
  "doctype": "Social Login Key",
  "name": "keycloak",
  "enable_social_login": 1,
  "social_login_provider": "Custom",
  "provider_name": "Keycloak",
  "client_id": "frappe-backend",
  "client_secret": "${KEYCLOAK_CLIENT_SECRET}",
  "icon": "fa fa-key",
  "base_url": "https://auth.dartwing.io/realms/dartwing-prod",
  "authorize_url": "/protocol/openid-connect/auth",
  "access_token_url": "/protocol/openid-connect/token",
  "redirect_url": "/api/method/frappe.integrations.oauth2_logins.custom",
  "api_endpoint": "/protocol/openid-connect/userinfo",
  "api_endpoint_args": null,
  "auth_url_data": "{\"scope\": \"openid profile email\"}",
  "user_id_property": "sub",
  "user_email_property": "email"
}
```

### 5.2 User Mapping

When a user authenticates via Keycloak, Frappe:

1. Receives the OAuth callback with authorization code
2. Exchanges code for tokens
3. Fetches user info from Keycloak `/userinfo` endpoint
4. Creates or updates Frappe User based on email
5. Maps Keycloak groups/roles to Frappe roles (optional, via custom hook)

#### User Creation Hook (hooks.py)

```python
# dartwing_core/hooks.py

def after_oauth_login(login_manager, user_info):
    """
    Called after successful OAuth login.
    Syncs Keycloak groups to Frappe roles.
    """
    user = frappe.get_doc("User", login_manager.user)

    # Get Keycloak groups from token claims
    keycloak_groups = user_info.get("groups", [])

    # Map Keycloak groups to Frappe roles
    role_mapping = {
        "/dartwing/admins": "System Manager",
        "/dartwing/org-admins": "Organization Admin",
        "/dartwing/users": "Dartwing User"
    }

    for kc_group, frappe_role in role_mapping.items():
        if kc_group in keycloak_groups:
            if not user.has_role(frappe_role):
                user.add_roles(frappe_role)

    user.save(ignore_permissions=True)
```

### 5.3 API Token Validation

For API calls from Flutter/external clients, Frappe validates the Keycloak access token:

```python
# dartwing_core/api.py

import frappe
import requests
from frappe import _

@frappe.whitelist(allow_guest=True)
def validate_keycloak_token():
    """
    Validates the Bearer token from Authorization header against Keycloak.
    Used for API authentication from Flutter apps.
    """
    auth_header = frappe.get_request_header("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        frappe.throw(_("Missing or invalid Authorization header"), frappe.AuthenticationError)

    token = auth_header.split(" ")[1]

    # Introspect token with Keycloak
    keycloak_url = frappe.conf.get("keycloak_url")
    realm = frappe.conf.get("keycloak_realm")
    client_id = frappe.conf.get("keycloak_client_id")
    client_secret = frappe.conf.get("keycloak_client_secret")

    introspect_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token/introspect"

    response = requests.post(
        introspect_url,
        data={
            "token": token,
            "client_id": client_id,
            "client_secret": client_secret
        }
    )

    token_info = response.json()

    if not token_info.get("active"):
        frappe.throw(_("Token is invalid or expired"), frappe.AuthenticationError)

    # Get or create Frappe user
    email = token_info.get("email")
    if not frappe.db.exists("User", email):
        # Auto-create user from Keycloak
        create_user_from_keycloak(token_info)

    # Set session user
    frappe.set_user(email)

    return {"status": "ok", "user": email}
```

### 5.4 site_config.json Settings

```json
{
  "keycloak_url": "https://auth.dartwing.io",
  "keycloak_realm": "dartwing-prod",
  "keycloak_client_id": "frappe-backend",
  "keycloak_client_secret": "your-secret-here",
  "keycloak_auto_create_users": true,
  "keycloak_default_roles": ["Dartwing User"]
}
```

---

## 6. Flutter Mobile Integration

### 6.1 Package Dependencies

```yaml
# pubspec.yaml
dependencies:
  flutter_appauth: ^6.0.0
  flutter_secure_storage: ^9.0.0
  jwt_decoder: ^2.0.1
```

### 6.2 Auth Service Implementation

```dart
// lib/services/auth_service.dart

import 'package:flutter_appauth/flutter_appauth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class AuthService {
  static const String _issuer = 'https://auth.dartwing.io/realms/dartwing-prod';
  static const String _clientId = 'dartwing-mobile';
  static const String _redirectUrl = 'io.dartwing.app://callback';
  static const String _postLogoutRedirectUrl = 'io.dartwing.app://logout-callback';

  static const List<String> _scopes = [
    'openid',
    'profile',
    'email',
    'offline_access'
  ];

  final FlutterAppAuth _appAuth = const FlutterAppAuth();
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  // Token storage keys
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _idTokenKey = 'id_token';

  /// Initiates the login flow
  Future<AuthResult> login() async {
    try {
      final AuthorizationTokenResponse? result =
          await _appAuth.authorizeAndExchangeCode(
        AuthorizationTokenRequest(
          _clientId,
          _redirectUrl,
          issuer: _issuer,
          scopes: _scopes,
          promptValues: ['login'],
        ),
      );

      if (result != null) {
        await _storeTokens(result);
        return AuthResult.success(
          accessToken: result.accessToken!,
          user: _parseUserFromIdToken(result.idToken!),
        );
      }

      return AuthResult.failure('Login cancelled');
    } catch (e) {
      return AuthResult.failure(e.toString());
    }
  }

  /// Refreshes the access token
  Future<String?> refreshToken() async {
    final refreshToken = await _secureStorage.read(key: _refreshTokenKey);
    if (refreshToken == null) return null;

    try {
      final TokenResponse? result = await _appAuth.token(
        TokenRequest(
          _clientId,
          _redirectUrl,
          issuer: _issuer,
          refreshToken: refreshToken,
          scopes: _scopes,
        ),
      );

      if (result != null && result.accessToken != null) {
        await _storeTokens(result);
        return result.accessToken;
      }
    } catch (e) {
      // Refresh failed, need to re-authenticate
      await logout();
    }

    return null;
  }

  /// Logs out the user
  Future<void> logout() async {
    final idToken = await _secureStorage.read(key: _idTokenKey);

    try {
      await _appAuth.endSession(
        EndSessionRequest(
          idTokenHint: idToken,
          postLogoutRedirectUrl: _postLogoutRedirectUrl,
          issuer: _issuer,
        ),
      );
    } catch (e) {
      // End session failed, but still clear local tokens
    }

    await _clearTokens();
  }

  /// Gets the current access token, refreshing if needed
  Future<String?> getValidAccessToken() async {
    final accessToken = await _secureStorage.read(key: _accessTokenKey);
    if (accessToken == null) return null;

    // Check if token is expired
    if (JwtDecoder.isExpired(accessToken)) {
      return await refreshToken();
    }

    return accessToken;
  }

  /// Checks if user is authenticated
  Future<bool> isAuthenticated() async {
    final token = await getValidAccessToken();
    return token != null;
  }

  // Private methods
  Future<void> _storeTokens(dynamic result) async {
    if (result.accessToken != null) {
      await _secureStorage.write(key: _accessTokenKey, value: result.accessToken);
    }
    if (result.refreshToken != null) {
      await _secureStorage.write(key: _refreshTokenKey, value: result.refreshToken);
    }
    if (result.idToken != null) {
      await _secureStorage.write(key: _idTokenKey, value: result.idToken);
    }
  }

  Future<void> _clearTokens() async {
    await _secureStorage.delete(key: _accessTokenKey);
    await _secureStorage.delete(key: _refreshTokenKey);
    await _secureStorage.delete(key: _idTokenKey);
  }

  User _parseUserFromIdToken(String idToken) {
    final payload = JwtDecoder.decode(idToken);
    return User(
      id: payload['sub'],
      email: payload['email'],
      name: payload['name'],
      emailVerified: payload['email_verified'] ?? false,
    );
  }
}

class AuthResult {
  final bool success;
  final String? accessToken;
  final User? user;
  final String? error;

  AuthResult.success({required this.accessToken, required this.user})
      : success = true,
        error = null;

  AuthResult.failure(this.error)
      : success = false,
        accessToken = null,
        user = null;
}

class User {
  final String id;
  final String email;
  final String? name;
  final bool emailVerified;

  User({
    required this.id,
    required this.email,
    this.name,
    required this.emailVerified,
  });
}
```

### 6.3 Riverpod Provider

```dart
// lib/providers/auth_provider.dart

import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../services/auth_service.dart';

part 'auth_provider.g.dart';

@riverpod
AuthService authService(AuthServiceRef ref) {
  return AuthService();
}

@riverpod
class AuthState extends _$AuthState {
  @override
  Future<User?> build() async {
    final authService = ref.watch(authServiceProvider);
    final isAuthenticated = await authService.isAuthenticated();

    if (isAuthenticated) {
      final token = await authService.getValidAccessToken();
      if (token != null) {
        // Parse user from stored token
        return authService.getCurrentUser();
      }
    }

    return null;
  }

  Future<void> login() async {
    final authService = ref.read(authServiceProvider);
    final result = await authService.login();

    if (result.success) {
      state = AsyncData(result.user);
    } else {
      state = AsyncError(result.error!, StackTrace.current);
    }
  }

  Future<void> logout() async {
    final authService = ref.read(authServiceProvider);
    await authService.logout();
    state = const AsyncData(null);
  }
}
```

### 6.4 iOS Configuration (Info.plist)

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>io.dartwing.app</string>
    </array>
    <key>CFBundleURLName</key>
    <string>io.dartwing.app</string>
  </dict>
</array>
```

### 6.5 Android Configuration (AndroidManifest.xml)

```xml
<activity
    android:name="net.openid.appauth.RedirectUriReceiverActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="io.dartwing.app" />
    </intent-filter>
</activity>
```

---

## 7. Token Management

### 7.1 Token Lifecycle

| Token Type    | Lifespan  | Purpose                         |
| ------------- | --------- | ------------------------------- |
| Access Token  | 5 minutes | API authorization               |
| Refresh Token | 30 days   | Obtain new access tokens        |
| ID Token      | 5 minutes | User identity claims            |
| Offline Token | 30 days   | Background refresh without user |

### 7.2 Token Refresh Flow

```
┌─────────────────────────────────┐
│   App Makes API Request         │
└─────────────┬───────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Access Token    │
    │ Valid?          │
    └────┬──────┬─────┘
         │      │
      No │      │ Yes
         │      │
         ▼      └──────────────────────────────────┐
    ┌─────────────────┐                            │
    │ Refresh Token   │                            │
    │ Exists?         │                            │
    └────┬──────┬─────┘                            │
         │      │                                  │
      No │      │ Yes                              │
         │      ▼                                  │
         │ ┌─────────────────┐                     │
         │ │ Call Keycloak   │                     │
         │ │ /token endpoint │                     │
         │ │ with refresh    │                     │
         │ └────┬──────┬─────┘                     │
         │      │      │                           │
         │ Fail │      │ Success                   │
         │      │      ▼                           │
         │      │ ┌─────────────────┐              │
         │      │ │ Store new       │              │
         │      │ │ access token    │              │
         │      │ └────────┬────────┘              │
         │      │          │                       │
         ▼      ▼          ▼                       ▼
    ┌─────────────────┐  ┌─────────────────────────────┐
    │ Redirect to     │  │ Make API call with          │
    │ Login Screen    │  │ valid access token          │
    └─────────────────┘  └─────────────────────────────┘
```

---

## 8. Personal vs Business Identity

### 8.1 Identity Separation Model

```
┌─────────────────────────────────────────────────────────────┐
│                     KEYCLOAK REALM                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    USER ACCOUNT                      │    │
│  │                                                      │    │
│  │  - email: john@gmail.com (personal)                 │    │
│  │  - Keycloak User ID: uuid-1234                      │    │
│  │                                                      │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Personal        │  │ Business        │          │    │
│  │  │ Identity        │  │ Identities      │          │    │
│  │  │                 │  │                 │          │    │
│  │  │ - Own data      │  │ - Acme Corp     │          │    │
│  │  │ - Own devices   │  │   (john@acme)   │          │    │
│  │  │ - Family orgs   │  │ - Tech Inc     │          │    │
│  │  │                 │  │   (jsmith@tech) │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Implementation in Dartwing

```python
# dartwing_core/person.py

# Person doctype links Keycloak identity to org memberships
{
  "doctype": "Person",
  "fields": [
    {"fieldname": "keycloak_user_id", "label": "Keycloak User ID", "fieldtype": "Data", "unique": 1},
    {"fieldname": "primary_email", "label": "Primary Email", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "frappe_user", "label": "Frappe User", "fieldtype": "Link", "options": "User"},
    {"fieldname": "personal_org", "label": "Personal Organization", "fieldtype": "Link", "options": "Organization"},
    # Org memberships via Org Member doctype
  ]
}
```

### 8.3 Signup Flow with Personal/Business Separation

1. User signs up with personal email (required)
2. System creates Person + personal Family organization
3. User can optionally add business email
4. User receives invitation to join company organization
5. Business identity linked to same Person record
6. Company has no access to personal org data

---

## 9. Multi-Factor Authentication

### 9.1 Supported MFA Methods

| Method         | Keycloak Config       | Notes                       |
| -------------- | --------------------- | --------------------------- |
| Email OTP      | Conditional OTP       | Sent via email              |
| SMS OTP        | Custom Authenticator  | Twilio integration          |
| TOTP           | OTP Form              | Google Authenticator, Authy |
| WebAuthn       | WebAuthn Passwordless | FIDO2, biometrics           |
| Recovery Codes | Backup codes          | One-time use                |

### 9.2 Keycloak Authentication Flow

```json
{
  "alias": "dartwing-browser",
  "description": "Dartwing browser-based authentication",
  "providerId": "basic-flow",
  "topLevel": true,
  "builtIn": false,
  "authenticationExecutions": [
    {
      "authenticator": "auth-cookie",
      "requirement": "ALTERNATIVE"
    },
    {
      "authenticator": "auth-username-password-form",
      "requirement": "REQUIRED"
    },
    {
      "authenticator": "conditional-otp",
      "requirement": "CONDITIONAL"
    },
    {
      "authenticator": "webauthn-authenticator",
      "requirement": "ALTERNATIVE"
    }
  ]
}
```

---

## 10. Social Login Providers

### 10.1 Configured Identity Providers

| Provider  | Client ID Location                        | Scopes                 |
| --------- | ----------------------------------------- | ---------------------- |
| Google    | Keycloak > Identity Providers > Google    | openid, profile, email |
| Apple     | Keycloak > Identity Providers > Apple     | openid, name, email    |
| Facebook  | Keycloak > Identity Providers > Facebook  | email, public_profile  |
| Microsoft | Keycloak > Identity Providers > Microsoft | openid, profile, email |

### 10.2 Keycloak Identity Provider Config (Google Example)

```json
{
  "alias": "google",
  "displayName": "Google",
  "providerId": "google",
  "enabled": true,
  "trustEmail": true,
  "storeToken": false,
  "firstBrokerLoginFlowAlias": "first broker login",
  "config": {
    "clientId": "${GOOGLE_CLIENT_ID}",
    "clientSecret": "${GOOGLE_CLIENT_SECRET}",
    "defaultScope": "openid profile email",
    "syncMode": "IMPORT"
  }
}
```

---

## 11. Session Management

### 11.1 Session Types

| Session Type         | Storage         | Timeout                   |
| -------------------- | --------------- | ------------------------- |
| Keycloak SSO Session | Keycloak Server | 30 min idle, 10 hours max |
| Frappe Session       | Redis           | 6 hours                   |
| Flutter App Token    | Secure Storage  | Based on token expiry     |

### 11.2 Logout Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Flutter    │    │   Keycloak   │    │    Frappe    │
│     App      │    │    Server    │    │   Backend    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       │ 1. User clicks logout                 │
       │                   │                   │
       │ 2. End Keycloak session               │
       │──────────────────►│                   │
       │   GET /logout     │                   │
       │   ?id_token_hint  │                   │
       │   &post_logout_redirect_uri           │
       │                   │                   │
       │◄──────────────────│                   │
       │   Redirect to app │                   │
       │                   │                   │
       │ 3. Clear local tokens                 │
       │   (SecureStorage) │                   │
       │                   │                   │
       │ 4. Call Frappe logout (optional)      │
       │───────────────────┼──────────────────►│
       │   POST /api/method/logout             │
       │                   │                   │
       │◄──────────────────┼───────────────────│
       │                   │                   │
       │ 5. Redirect to login screen           │
       │                   │                   │
```

---

## 12. Security Considerations

### 12.1 Token Security

- **PKCE Required:** All public clients must use PKCE (S256)
- **Short-lived Access Tokens:** 5-minute expiry reduces exposure
- **Secure Storage:** Tokens stored in platform secure storage (Keychain/Keystore)
- **No Token in URLs:** Tokens never passed in query parameters
- **HTTPS Only:** All endpoints require TLS 1.2+

### 12.2 Keycloak Hardening

```json
{
  "bruteForceProtected": true,
  "failureFactor": 5,
  "maxDeltaTimeSeconds": 43200,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "permanentLockout": false,
  "quickLoginCheckMilliSeconds": 1000,
  "waitIncrementSeconds": 60
}
```

### 12.3 CORS Configuration

```python
# Frappe site_config.json
{
  "allow_cors": [
    "https://app.dartwing.io",
    "https://auth.dartwing.io"
  ]
}
```

---

## 13. Implementation Guide

### 13.1 Phase 1: Keycloak Setup

1. Deploy Keycloak server
2. Create realm (dartwing-dev, dartwing-prod)
3. Configure clients (dartwing-mobile, frappe-backend)
4. Set up identity providers (Google, Apple)
5. Configure authentication flows
6. Create initial admin users

### 13.2 Phase 2: Frappe Integration

1. Install/configure Social Login Key
2. Create custom auth hooks for user sync
3. Implement token validation API
4. Configure site_config.json
5. Test login flow from Frappe Desk

### 13.3 Phase 3: Flutter Integration

1. Add flutter_appauth dependency
2. Implement AuthService
3. Configure iOS/Android redirect URIs
4. Create auth providers (Riverpod)
5. Build login/logout UI
6. Test on physical devices

### 13.4 Phase 4: Advanced Features

1. Implement MFA
2. Add social login buttons
3. Build personal/business identity UI
4. Implement session management
5. Add offline token support

---

## Appendix A: Environment Variables

```bash
# Keycloak
KEYCLOAK_URL=https://auth.dartwing.io
KEYCLOAK_REALM=dartwing-prod
KEYCLOAK_ADMIN_USER=admin
KEYCLOAK_ADMIN_PASSWORD=<secure-password>

# Frappe Client
KEYCLOAK_CLIENT_ID=frappe-backend
KEYCLOAK_CLIENT_SECRET=<client-secret>

# Flutter (build-time)
KEYCLOAK_ISSUER=https://auth.dartwing.io/realms/dartwing-prod
KEYCLOAK_MOBILE_CLIENT_ID=dartwing-mobile
```

---

## Appendix B: Troubleshooting

| Issue                       | Cause                                 | Solution                                                     |
| --------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| "Email not verified" error  | Keycloak email_verified claim not set | Configure Keycloak to trust IdP emails or verify in Keycloak |
| PKCE code_verifier mismatch | Code challenge/verifier not matching  | Ensure S256 method, proper encoding                          |
| Redirect URI mismatch       | Client redirect URI not registered    | Add exact URI to Keycloak client config                      |
| Token expired immediately   | Clock skew between servers            | Sync NTP on all servers                                      |
| CORS errors                 | Origin not whitelisted                | Add origin to Keycloak client Web Origins                    |
