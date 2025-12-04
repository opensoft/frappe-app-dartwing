# Section 1: System Architecture Overview

## 1.1 High-Level Architecture

Dartwing AMS (Association Management System) is built on Dartwing Core and provides a comprehensive platform for managing homeowner associations, country clubs, alumni associations, and professional societies. The architecture leverages the existing Dartwing Core infrastructure while adding association-specific modules.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DARTWING AMS - HIGH-LEVEL ARCHITECTURE                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         CLIENT LAYER                                 │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Member     │  │   Board      │  │    Staff     │              │    │
│  │  │   Portal     │  │   Portal     │  │   Console    │              │    │
│  │  │   (Web/PWA)  │  │   (Web/PWA)  │  │   (Web)      │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │ DartwingFone │  │  White-Label │  │   Chapter    │              │    │
│  │  │ Mobile App   │  │   Branded    │  │   Microsites │              │    │
│  │  │ (Flutter)    │  │   Apps       │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      API GATEWAY / EDGE                              │    │
│  │                                                                      │    │
│  │  • CloudFlare WAF & DDoS      • Rate Limiting                       │    │
│  │  • SSL/TLS Termination        • Custom Domain Routing               │    │
│  │  • Geographic Routing          • API Versioning                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   DARTWING      │    │   DARTWING      │    │   DARTWING      │         │
│  │   AMS MODULE    │    │   CORE          │    │   FONE          │         │
│  │                 │    │                 │    │                 │         │
│  │ • Properties    │    │ • Person/Org    │    │ • Push Notifs   │         │
│  │ • Violations    │    │ • Payments      │    │ • Offline Sync  │         │
│  │ • ARC           │    │ • Events        │    │ • QR Codes      │         │
│  │ • Work Orders   │    │ • Comms         │    │ • Geolocation   │         │
│  │ • Governance    │    │ • Workflows     │    │                 │         │
│  │ • Amenities     │    │                 │    │                 │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│         │                          │                          │             │
│         └──────────────────────────┼──────────────────────────┘             │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      FRAPPE FRAMEWORK                                │    │
│  │                                                                      │    │
│  │  • DocType ORM           • Background Jobs (RQ)                     │    │
│  │  • REST + GraphQL API    • Scheduler                                │    │
│  │  • Permission Engine     • WebSocket (Socket.IO)                    │    │
│  │  • Workflow Engine       • Report Builder                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         DATA LAYER                                   │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  PostgreSQL  │  │    Redis     │  │  S3/Azure    │              │    │
│  │  │  (Primary)   │  │   (Cache +   │  │  Blob        │              │    │
│  │  │              │  │   Queue)     │  │  Storage     │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  TimescaleDB │  │    Qdrant    │  │  Elasticsearch│              │    │
│  │  │  (Metrics)   │  │   (Vector)   │  │  (Search)    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     EXTERNAL INTEGRATIONS                            │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Accounting  │  │   Payment    │  │   E-Sign     │              │    │
│  │  │  QB/Xero/NS  │  │  Stripe/ACH  │  │  DocuSign    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Access     │  │    POS       │  │   Identity   │              │    │
│  │  │  Control     │  │  Systems     │  │  Keycloak    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 Technology Stack

### Backend Stack

| Component      | Technology      | Purpose                           |
| -------------- | --------------- | --------------------------------- |
| Framework      | Frappe v15      | Full-stack web framework with ORM |
| Language       | Python 3.10+    | Backend logic and API             |
| Database       | PostgreSQL 15   | Primary data store                |
| Cache          | Redis 7         | Session, cache, and job queue     |
| Search         | Elasticsearch 8 | Full-text search for KB, docs     |
| Time-Series    | TimescaleDB     | Metrics and analytics             |
| Vector DB      | Qdrant          | AI embeddings for KB search       |
| Object Storage | S3/Azure Blob   | Documents, images, backups        |

### Frontend Stack

| Component        | Technology            | Purpose                        |
| ---------------- | --------------------- | ------------------------------ |
| Mobile App       | Flutter 3.16+         | Cross-platform iOS/Android     |
| Web Portal       | Frappe Web + Vue.js 3 | Member and staff portals       |
| State Management | Riverpod (Flutter)    | Mobile app state               |
| Offline Storage  | Hive + SQLite         | Mobile offline data            |
| Real-time        | Socket.IO             | Live updates and notifications |

### Infrastructure Stack

| Component  | Technology           | Purpose                |
| ---------- | -------------------- | ---------------------- |
| Container  | Docker + K8s         | Orchestration          |
| CI/CD      | GitHub Actions       | Automated deployment   |
| CDN        | CloudFlare           | Edge caching and WAF   |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |
| Logging    | Loki                 | Centralized logs       |
| Tracing    | Jaeger               | Distributed tracing    |
| Identity   | Keycloak             | SSO, MFA, WebAuthn     |

## 1.3 Multi-Tenant Architecture

### Association Isolation Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MULTI-TENANT ISOLATION                                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     ORGANIZATION HIERARCHY                           │    │
│  │                                                                      │    │
│  │                    ┌─────────────────────┐                          │    │
│  │                    │   Management Co     │                          │    │
│  │                    │   (Parent Org)      │                          │    │
│  │                    └──────────┬──────────┘                          │    │
│  │                               │                                      │    │
│  │         ┌─────────────────────┼─────────────────────┐               │    │
│  │         │                     │                     │               │    │
│  │         ▼                     ▼                     ▼               │    │
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐         │    │
│  │  │  HOA #1     │      │  HOA #2     │      │  Country    │         │    │
│  │  │ 500 Units   │      │ 200 Units   │      │  Club       │         │    │
│  │  └─────────────┘      └─────────────┘      └─────────────┘         │    │
│  │         │                     │                     │               │    │
│  │         ▼                     ▼                     ▼               │    │
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐         │    │
│  │  │ Buildings   │      │ Lots/Units  │      │ Membership  │         │    │
│  │  │ Units       │      │             │      │ Types       │         │    │
│  │  │ Common Area │      │             │      │ Amenities   │         │    │
│  │  └─────────────┘      └─────────────┘      └─────────────┘         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     DATA ISOLATION LAYERS                            │    │
│  │                                                                      │    │
│  │  Layer 1: Organization Boundary                                     │    │
│  │  └─ All DocTypes have `organization` field with automatic filter    │    │
│  │                                                                      │    │
│  │  Layer 2: Property/Unit Scoping                                     │    │
│  │  └─ Members see only their units; Board sees all in association     │    │
│  │                                                                      │    │
│  │  Layer 3: Role-Based Views                                          │    │
│  │  └─ Manager, Board, Committee, Member, Resident, Vendor roles       │    │
│  │                                                                      │    │
│  │  Layer 4: Chapter/Building Scoping (for federated orgs)             │    │
│  │  └─ Chapter admins see only their chapter's data                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Tenant Configuration

```python
# dartwing_ams/config/tenant.py

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class AssociationType(Enum):
    HOA = "hoa"
    CONDO = "condo"
    COUNTRY_CLUB = "country_club"
    GOLF_CLUB = "golf_club"
    ALUMNI = "alumni"
    PROFESSIONAL_SOCIETY = "professional_society"
    TRADE_ASSOCIATION = "trade_association"

class FinancialModel(Enum):
    STANDARD = "standard"           # Single org billing
    FEDERATED = "federated"         # National + chapters split
    MANAGEMENT_CO = "management_co" # Management company umbrella

@dataclass
class TenantConfiguration:
    """Configuration for an association tenant."""

    # Identity
    organization_id: str
    association_type: AssociationType
    legal_name: str
    dba_name: Optional[str] = None

    # Branding
    custom_domain: Optional[str] = None       # e.g., app.sunsetterracehoa.com
    logo_url: Optional[str] = None
    primary_color: str = "#1976D2"
    secondary_color: str = "#424242"

    # Financial
    financial_model: FinancialModel = FinancialModel.STANDARD
    currency: str = "USD"
    fiscal_year_start_month: int = 1          # January

    # Compliance
    jurisdiction: str = "US-FL"               # State/country code
    compliance_pack: Optional[str] = None     # e.g., "FL-HOA", "CA-DAVIS-STIRLING"

    # Features
    enabled_modules: List[str] = None         # Subset of available modules

    # Hierarchy
    parent_organization: Optional[str] = None # For chapters/managed associations

    def __post_init__(self):
        if self.enabled_modules is None:
            self.enabled_modules = self._default_modules()

    def _default_modules(self) -> List[str]:
        """Get default modules based on association type."""
        base_modules = [
            "membership",
            "dues_billing",
            "communications",
            "events",
            "documents",
            "requests",
            "voting"
        ]

        if self.association_type in [AssociationType.HOA, AssociationType.CONDO]:
            return base_modules + [
                "properties",
                "violations",
                "arc_requests",
                "work_orders",
                "amenities",
                "governance"
            ]

        elif self.association_type in [AssociationType.COUNTRY_CLUB, AssociationType.GOLF_CLUB]:
            return base_modules + [
                "amenities",
                "tee_times",
                "house_charges",
                "pos_integration",
                "tournaments"
            ]

        elif self.association_type == AssociationType.ALUMNI:
            return base_modules + [
                "chapters",
                "donations",
                "career_center",
                "mentorship",
                "class_years"
            ]

        elif self.association_type in [AssociationType.PROFESSIONAL_SOCIETY,
                                        AssociationType.TRADE_ASSOCIATION]:
            return base_modules + [
                "chapters",
                "certifications",
                "ce_tracking",
                "job_board",
                "sponsorships",
                "publications"
            ]

        return base_modules
```

## 1.4 Module Architecture

### Core Modules Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DARTWING AMS MODULE MAP                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     FOUNDATION (Dartwing Core)                       │    │
│  │                                                                      │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │
│  │  │ Person  │ │  Org    │ │Payments │ │ Events  │ │  Comms  │       │    │
│  │  │ Graph   │ │ Graph   │ │ Engine  │ │ Engine  │ │ Engine  │       │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     ASSOCIATION LAYER (dartwing_ams)                 │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    MEMBERSHIP & CRM                            │  │    │
│  │  │  • Member Roster      • Households        • 360° Timeline     │  │    │
│  │  │  • Membership Tiers   • Renewals          • Tasks & Follow-up │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    PROPERTY MANAGEMENT (HOA/Condo)             │  │    │
│  │  │  • Units/Lots         • Buildings         • Common Areas      │  │    │
│  │  │  • Violations         • ARC Requests      • Inspections       │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    FINANCIAL OPERATIONS                        │  │    │
│  │  │  • Dues Billing       • Assessments       • Collections       │  │    │
│  │  │  • Reserve Funds      • GL Integration    • Delinquencies     │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    OPERATIONS & MAINTENANCE                    │  │    │
│  │  │  • Work Orders        • Vendors           • PM Schedules      │  │    │
│  │  │  • Assets             • Contracts         • Inspections       │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    GOVERNANCE & COMPLIANCE                     │  │    │
│  │  │  • Board Portal       • Meeting Mgmt      • Minutes/Motions   │  │    │
│  │  │  • Elections          • Proxies           • Resolutions       │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │                    MEMBER SERVICES                             │  │    │
│  │  │  • Requests/Cases     • Knowledge Base    • Amenity Booking   │  │    │
│  │  │  • Access Control     • Guest Passes      • Emergency Alert   │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     VERTICAL EXTENSIONS                              │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │  Club/Golf  │  │   Alumni    │  │ Professional │                 │    │
│  │  │  Extension  │  │  Extension  │  │  Society Ext │                 │    │
│  │  │             │  │             │  │              │                 │    │
│  │  │ • Tee Times │  │ • Class Yrs │  │ • CE Credits │                 │    │
│  │  │ • House $   │  │ • Donations │  │ • Job Board  │                 │    │
│  │  │ • POS Link  │  │ • Chapters  │  │ • Certs      │                 │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.5 Security Architecture

### Authentication & Authorization

```python
# dartwing_ams/security/auth.py

from enum import Enum
from typing import List, Optional
import frappe

class AMSRole(Enum):
    """Standard AMS roles."""

    # Staff roles
    SYSTEM_ADMIN = "System Admin"
    ASSOCIATION_MANAGER = "Association Manager"
    PROPERTY_MANAGER = "Property Manager"
    ACCOUNTANT = "Accountant"
    FRONT_DESK = "Front Desk"
    MAINTENANCE_STAFF = "Maintenance Staff"

    # Board roles
    BOARD_PRESIDENT = "Board President"
    BOARD_MEMBER = "Board Member"
    COMMITTEE_CHAIR = "Committee Chair"
    COMMITTEE_MEMBER = "Committee Member"

    # Member roles
    OWNER = "Owner"
    RESIDENT = "Resident"
    TENANT = "Tenant"
    FAMILY_MEMBER = "Family Member"

    # External roles
    VENDOR = "Vendor"
    GUEST = "Guest"

    # Chapter roles (for federated orgs)
    CHAPTER_ADMIN = "Chapter Admin"
    CHAPTER_TREASURER = "Chapter Treasurer"


class PermissionMatrix:
    """Permission matrix for AMS operations."""

    PERMISSIONS = {
        # Format: (role, doctype, permission_level)
        # Permission levels: 0=None, 1=Read, 2=Read+Create, 3=Read+Create+Write, 4=Full

        # Property Management
        ("Association Manager", "Unit", 4),
        ("Board Member", "Unit", 1),
        ("Owner", "Unit", 1),  # Own unit only

        # Violations
        ("Association Manager", "Violation", 4),
        ("Board Member", "Violation", 3),
        ("Committee Chair", "Violation", 2),  # ARC chair
        ("Owner", "Violation", 1),  # Own violations only

        # Financials
        ("Accountant", "Invoice", 4),
        ("Association Manager", "Invoice", 3),
        ("Board Treasurer", "Invoice", 1),
        ("Owner", "Invoice", 1),  # Own invoices only

        # Work Orders
        ("Maintenance Staff", "Work Order", 3),
        ("Association Manager", "Work Order", 4),
        ("Owner", "Work Order", 2),  # Can create for own unit

        # Governance
        ("Board President", "Board Meeting", 4),
        ("Board Member", "Board Meeting", 3),
        ("Association Manager", "Board Meeting", 3),
        ("Owner", "Board Meeting", 1),  # Published meetings only
    }

    @classmethod
    def get_permission_level(
        cls,
        role: str,
        doctype: str
    ) -> int:
        """Get permission level for role and doctype."""
        for r, d, level in cls.PERMISSIONS:
            if r == role and d == doctype:
                return level
        return 0


class AssociationPermissionEngine:
    """Permission engine for association access control."""

    def __init__(self, user: str):
        self.user = user
        self.member = self._get_member()
        self.roles = self._get_roles()
        self.organization = self.member.organization if self.member else None

    def _get_member(self) -> Optional["Member"]:
        """Get member record for user."""
        return frappe.db.get_value(
            "Member",
            {"user": self.user, "status": "Active"},
            ["name", "organization", "membership_type"],
            as_dict=True
        )

    def _get_roles(self) -> List[str]:
        """Get all roles for user in their organization."""
        if not self.member:
            return []

        roles = frappe.get_all(
            "Member Role Assignment",
            filters={
                "member": self.member.name,
                "status": "Active"
            },
            pluck="role"
        )

        return roles

    def can_access_organization(self, org_id: str) -> bool:
        """Check if user can access an organization."""
        if not self.organization:
            return False

        # Direct membership
        if self.organization == org_id:
            return True

        # Management company access
        if self._is_management_company_staff(org_id):
            return True

        # Parent organization access (for chapters)
        if self._is_parent_org_admin(org_id):
            return True

        return False

    def can_view_unit(self, unit_id: str) -> bool:
        """Check if user can view a unit."""
        unit = frappe.get_doc("Unit", unit_id)

        # Staff and board can view all units
        if self._has_any_role(["Association Manager", "Board Member", "Property Manager"]):
            return True

        # Owners/residents can view their own unit
        if self._is_unit_member(unit_id):
            return True

        return False

    def can_view_member_financials(self, member_id: str) -> bool:
        """Check if user can view another member's financials."""
        # Self
        if self.member and self.member.name == member_id:
            return True

        # Staff with financial access
        if self._has_any_role(["Association Manager", "Accountant", "Property Manager"]):
            return True

        # Board treasurer
        if "Board Treasurer" in self.roles:
            return True

        return False

    def can_create_violation(self) -> bool:
        """Check if user can create violations."""
        return self._has_any_role([
            "Association Manager",
            "Property Manager",
            "Board Member",
            "Committee Chair"
        ])

    def can_approve_arc_request(self) -> bool:
        """Check if user can approve ARC requests."""
        return self._has_any_role([
            "Association Manager",
            "Board Member",
            "ARC Committee Chair"
        ])

    def _has_any_role(self, roles: List[str]) -> bool:
        """Check if user has any of the specified roles."""
        return bool(set(self.roles) & set(roles))

    def _is_unit_member(self, unit_id: str) -> bool:
        """Check if user is associated with a unit."""
        return frappe.db.exists(
            "Unit Member",
            {
                "unit": unit_id,
                "member": self.member.name if self.member else None,
                "status": "Active"
            }
        )

    def _is_management_company_staff(self, org_id: str) -> bool:
        """Check if user is staff of management company for org."""
        org = frappe.get_doc("Organization", org_id)
        if org.management_company:
            return frappe.db.exists(
                "Member",
                {
                    "user": self.user,
                    "organization": org.management_company,
                    "is_staff": 1
                }
            )
        return False

    def _is_parent_org_admin(self, org_id: str) -> bool:
        """Check if user is admin of parent organization."""
        org = frappe.get_doc("Organization", org_id)
        if org.parent_organization:
            return frappe.db.exists(
                "Member Role Assignment",
                {
                    "member": ["in", frappe.get_all(
                        "Member",
                        filters={"user": self.user, "organization": org.parent_organization},
                        pluck="name"
                    )],
                    "role": ["in", ["System Admin", "Association Manager"]],
                    "status": "Active"
                }
            )
        return False
```

## 1.6 White-Label Architecture

### Custom Domain & Branding

```python
# dartwing_ams/whitelabel/branding.py

import frappe
from typing import Optional
from dataclasses import dataclass

@dataclass
class BrandingConfig:
    """Branding configuration for white-label deployment."""

    organization_id: str

    # Domain
    custom_domain: Optional[str] = None        # app.sunsetterracehoa.com
    email_domain: Optional[str] = None         # @sunsetterracehoa.com

    # Visual Identity
    logo_light: Optional[str] = None           # URL to light mode logo
    logo_dark: Optional[str] = None            # URL to dark mode logo
    favicon: Optional[str] = None              # URL to favicon

    # Colors
    primary_color: str = "#1976D2"
    secondary_color: str = "#424242"
    accent_color: str = "#FF5722"

    # Typography
    font_family: str = "Inter"
    heading_font: Optional[str] = None

    # App Store
    app_name: str = "DartwingFone"
    ios_app_id: Optional[str] = None
    android_app_id: Optional[str] = None


class WhiteLabelService:
    """Service for managing white-label configurations."""

    @staticmethod
    def get_branding(organization_id: str) -> BrandingConfig:
        """Get branding config for an organization."""
        doc = frappe.get_value(
            "Association Branding",
            {"organization": organization_id},
            ["*"],
            as_dict=True
        )

        if not doc:
            return WhiteLabelService._default_branding(organization_id)

        return BrandingConfig(
            organization_id=organization_id,
            custom_domain=doc.custom_domain,
            email_domain=doc.email_domain,
            logo_light=doc.logo_light,
            logo_dark=doc.logo_dark,
            favicon=doc.favicon,
            primary_color=doc.primary_color or "#1976D2",
            secondary_color=doc.secondary_color or "#424242",
            accent_color=doc.accent_color or "#FF5722",
            font_family=doc.font_family or "Inter",
            heading_font=doc.heading_font,
            app_name=doc.app_name or "DartwingFone"
        )

    @staticmethod
    def _default_branding(organization_id: str) -> BrandingConfig:
        """Get default branding."""
        return BrandingConfig(organization_id=organization_id)

    @staticmethod
    def setup_custom_domain(organization_id: str, domain: str) -> dict:
        """Setup custom domain for organization."""
        # Verify domain ownership via DNS TXT record
        verification_token = frappe.generate_hash(length=32)

        # Store pending verification
        frappe.get_doc({
            "doctype": "Domain Verification",
            "organization": organization_id,
            "domain": domain,
            "verification_token": verification_token,
            "status": "Pending"
        }).insert(ignore_permissions=True)

        return {
            "status": "pending",
            "verification_type": "DNS_TXT",
            "record_name": f"_dartwing-verify.{domain}",
            "record_value": verification_token,
            "instructions": f"Add a TXT record to your DNS: _dartwing-verify.{domain} = {verification_token}"
        }

    @staticmethod
    def verify_domain(organization_id: str, domain: str) -> bool:
        """Verify domain ownership via DNS."""
        import dns.resolver

        verification = frappe.get_doc(
            "Domain Verification",
            {"organization": organization_id, "domain": domain}
        )

        try:
            answers = dns.resolver.resolve(f"_dartwing-verify.{domain}", "TXT")
            for rdata in answers:
                if verification.verification_token in str(rdata):
                    verification.status = "Verified"
                    verification.save()

                    # Update branding with verified domain
                    branding = frappe.get_doc(
                        "Association Branding",
                        {"organization": organization_id}
                    )
                    branding.custom_domain = domain
                    branding.save()

                    # Trigger SSL certificate provisioning
                    frappe.enqueue(
                        "dartwing_ams.whitelabel.ssl.provision_certificate",
                        domain=domain
                    )

                    return True
        except Exception:
            pass

        return False

    @staticmethod
    def generate_css_variables(config: BrandingConfig) -> str:
        """Generate CSS variables for branding."""
        return f"""
:root {{
    --primary-color: {config.primary_color};
    --secondary-color: {config.secondary_color};
    --accent-color: {config.accent_color};
    --font-family: '{config.font_family}', system-ui, sans-serif;
    --heading-font: '{config.heading_font or config.font_family}', system-ui, sans-serif;
}}
"""
```

## 1.7 Real-Time Communication Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME COMMUNICATION                                 │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     SOCKET.IO CLUSTER                                │    │
│  │                                                                      │    │
│  │  Client ─────►  Socket.IO ─────►  Redis Pub/Sub ─────►  All Nodes   │    │
│  │                  Server            Adapter                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     EVENT CHANNELS                                   │    │
│  │                                                                      │    │
│  │  org:{org_id}              → All members of organization            │    │
│  │  org:{org_id}:board        → Board members only                     │    │
│  │  org:{org_id}:staff        → Staff members only                     │    │
│  │  org:{org_id}:unit:{id}    → Residents of specific unit             │    │
│  │  org:{org_id}:building:{id}→ Residents of specific building         │    │
│  │  user:{user_id}            → Direct to user (all devices)           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     EVENT TYPES                                      │    │
│  │                                                                      │    │
│  │  • announcement_broadcast   • violation_created                     │    │
│  │  • emergency_alert          • arc_status_changed                    │    │
│  │  • work_order_update        • payment_received                      │    │
│  │  • meeting_reminder         • amenity_booking_confirmed             │    │
│  │  • vote_open                • document_shared                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
# dartwing_ams/realtime/manager.py

import frappe
from typing import List, Optional, Dict, Any
import socketio

class AMSRealtimeManager:
    """Manages real-time events for association."""

    EVENT_TYPES = {
        "announcement_broadcast": "announcement",
        "emergency_alert": "emergency",
        "violation_created": "violation",
        "violation_status_changed": "violation",
        "arc_request_submitted": "arc",
        "arc_status_changed": "arc",
        "work_order_created": "work_order",
        "work_order_status_changed": "work_order",
        "payment_received": "financial",
        "invoice_generated": "financial",
        "meeting_scheduled": "governance",
        "vote_opened": "governance",
        "vote_closed": "governance",
        "amenity_booking_confirmed": "amenity",
        "document_shared": "document",
        "request_status_changed": "request"
    }

    def __init__(self, organization: str):
        self.organization = organization
        self.sio = socketio.Client()

    def broadcast_to_org(
        self,
        event_type: str,
        data: Dict[str, Any],
        exclude_users: List[str] = None
    ):
        """Broadcast event to all organization members."""
        frappe.publish_realtime(
            event=event_type,
            message={
                "organization": self.organization,
                "data": data,
                "timestamp": frappe.utils.now_datetime().isoformat()
            },
            room=f"org:{self.organization}",
            after_commit=True
        )

    def broadcast_to_board(
        self,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Broadcast event to board members only."""
        frappe.publish_realtime(
            event=event_type,
            message={
                "organization": self.organization,
                "data": data,
                "timestamp": frappe.utils.now_datetime().isoformat()
            },
            room=f"org:{self.organization}:board",
            after_commit=True
        )

    def broadcast_to_unit(
        self,
        unit_id: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Broadcast event to unit residents."""
        frappe.publish_realtime(
            event=event_type,
            message={
                "organization": self.organization,
                "unit": unit_id,
                "data": data,
                "timestamp": frappe.utils.now_datetime().isoformat()
            },
            room=f"org:{self.organization}:unit:{unit_id}",
            after_commit=True
        )

    def send_to_user(
        self,
        user: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Send event to specific user."""
        frappe.publish_realtime(
            event=event_type,
            message={
                "organization": self.organization,
                "data": data,
                "timestamp": frappe.utils.now_datetime().isoformat()
            },
            user=user,
            after_commit=True
        )

    def send_emergency_alert(
        self,
        title: str,
        message: str,
        severity: str = "high",
        require_acknowledgment: bool = True
    ):
        """Send emergency alert to all members with tracking."""
        alert_id = frappe.generate_hash(length=16)

        # Create alert record
        alert = frappe.get_doc({
            "doctype": "Emergency Alert",
            "alert_id": alert_id,
            "organization": self.organization,
            "title": title,
            "message": message,
            "severity": severity,
            "require_acknowledgment": require_acknowledgment,
            "sent_at": frappe.utils.now_datetime()
        })
        alert.insert(ignore_permissions=True)

        # Broadcast to all members
        self.broadcast_to_org(
            "emergency_alert",
            {
                "alert_id": alert_id,
                "title": title,
                "message": message,
                "severity": severity,
                "require_acknowledgment": require_acknowledgment
            }
        )

        # Also send push notifications
        frappe.enqueue(
            "dartwing_ams.notifications.push.send_emergency_push",
            organization=self.organization,
            alert_id=alert_id,
            title=title,
            message=message
        )

        # Send SMS for high severity
        if severity == "critical":
            frappe.enqueue(
                "dartwing_ams.notifications.sms.send_emergency_sms",
                organization=self.organization,
                alert_id=alert_id,
                message=f"EMERGENCY: {title}\n\n{message}"
            )

        return alert_id

    def track_alert_acknowledgment(self, alert_id: str, user: str):
        """Track user acknowledgment of emergency alert."""
        frappe.get_doc({
            "doctype": "Emergency Alert Acknowledgment",
            "alert": alert_id,
            "user": user,
            "acknowledged_at": frappe.utils.now_datetime()
        }).insert(ignore_permissions=True)

        # Update alert stats
        alert = frappe.get_doc("Emergency Alert", {"alert_id": alert_id})
        alert.acknowledgment_count = frappe.db.count(
            "Emergency Alert Acknowledgment",
            {"alert": alert_id}
        )
        alert.save()
```

---

_End of Section 1: System Architecture Overview_

**Next Section:** Section 2 - Data Model Architecture

# Section 2: Data Model Architecture

## 2.1 Core DocTypes Overview

The Dartwing AMS data model extends Dartwing Core with association-specific entities:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AMS DATA MODEL OVERVIEW                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  CORE ENTITIES (from Dartwing Core)                  │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │   Person    │  │Organization │  │   Invoice   │                 │    │
│  │  │   (Global)  │  │   (Tenant)  │  │   Payment   │                 │    │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────────┘                 │    │
│  │         │                │                                          │    │
│  └─────────┼────────────────┼──────────────────────────────────────────┘    │
│            │                │                                                │
│            ▼                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  MEMBERSHIP & PROPERTY                               │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │   Member    │──│    Unit     │──│  Building   │                 │    │
│  │  │             │  │   (Lot)     │  │             │                 │    │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────────┘                 │    │
│  │         │                │                                          │    │
│  │         │         ┌──────┴──────┐                                   │    │
│  │         │         │             │                                   │    │
│  │         ▼         ▼             ▼                                   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │  Household  │  │ Common Area │  │   Asset     │                 │    │
│  │  │             │  │             │  │             │                 │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  COMPLIANCE & ENFORCEMENT                            │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │  Violation  │  │ ARC Request │  │ Inspection  │                 │    │
│  │  │             │  │             │  │             │                 │    │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────────┘                 │    │
│  │         │                │                                          │    │
│  │         ▼                ▼                                          │    │
│  │  ┌─────────────┐  ┌─────────────┐                                  │    │
│  │  │   Hearing   │  │ARC Approval │                                  │    │
│  │  │             │  │   History   │                                  │    │
│  │  └─────────────┘  └─────────────┘                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  OPERATIONS & MAINTENANCE                            │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │ Work Order  │  │   Vendor    │  │  Contract   │                 │    │
│  │  │             │  │             │  │             │                 │    │
│  │  └──────┬──────┘  └─────────────┘  └─────────────┘                 │    │
│  │         │                                                           │    │
│  │         ▼                                                           │    │
│  │  ┌─────────────┐  ┌─────────────┐                                  │    │
│  │  │     PM      │  │ Work Order  │                                  │    │
│  │  │  Schedule   │  │   Labor     │                                  │    │
│  │  └─────────────┘  └─────────────┘                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  GOVERNANCE & MEETINGS                               │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │Board Meeting│  │   Motion    │  │  Election   │                 │    │
│  │  │             │  │             │  │             │                 │    │
│  │  └──────┬──────┘  └─────────────┘  └──────┬──────┘                 │    │
│  │         │                                 │                         │    │
│  │         ▼                                 ▼                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │   Agenda    │  │   Minutes   │  │   Ballot    │                 │    │
│  │  │    Item     │  │             │  │    Vote     │                 │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  MEMBER SERVICES                                     │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │   Request   │  │   Amenity   │  │   KB        │                 │    │
│  │  │   (Case)    │  │   Booking   │  │   Article   │                 │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                 │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐                                  │    │
│  │  │   Access    │  │   Guest     │                                  │    │
│  │  │    Pass     │  │    Pass     │                                  │    │
│  │  └─────────────┘  └─────────────┘                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Organization & Association DocTypes

### Association DocType

```python
# dartwing_ams/doctype/association/association.py

import frappe
from frappe.model.document import Document
from typing import Optional, List

class Association(Document):
    """
    Core association entity extending Organization.

    Fields:
    - name: Auto-generated ID
    - organization: Link to Organization (Dartwing Core)
    - association_type: Select [HOA, Condo, Country Club, Golf Club, Alumni, Professional Society, Trade Association]
    - legal_name: Data (required)
    - dba_name: Data
    - ein: Data (encrypted)
    - incorporation_state: Data
    - incorporation_date: Date
    - fiscal_year_start: Select [January..December]

    # Location
    - address_line_1: Data
    - address_line_2: Data
    - city: Data
    - state: Data
    - postal_code: Data
    - country: Link to Country

    # Contact
    - phone: Data
    - email: Data
    - website: Data

    # Configuration
    - compliance_pack: Link to Compliance Pack
    - timezone: Select
    - currency: Link to Currency
    - default_language: Link to Language

    # Hierarchy
    - management_company: Link to Organization
    - parent_association: Link to Association (for chapters)

    # Stats (computed)
    - total_units: Int (read-only)
    - total_members: Int (read-only)
    - total_outstanding: Currency (read-only)

    # Status
    - status: Select [Active, Suspended, Dissolved]
    """

    def validate(self):
        self.validate_ein()
        self.validate_fiscal_year()

    def validate_ein(self):
        """Validate EIN format if provided."""
        if self.ein:
            import re
            if not re.match(r'^\d{2}-\d{7}$', self.ein):
                frappe.throw("EIN must be in format XX-XXXXXXX")

    def validate_fiscal_year(self):
        """Set default fiscal year start."""
        if not self.fiscal_year_start:
            self.fiscal_year_start = "January"

    def on_update(self):
        self.update_computed_stats()

    def update_computed_stats(self):
        """Update computed statistics."""
        self.total_units = frappe.db.count(
            "Unit",
            {"association": self.name, "status": ["!=", "Dissolved"]}
        )

        self.total_members = frappe.db.count(
            "Member",
            {"organization": self.organization, "status": "Active"}
        )

        self.total_outstanding = frappe.db.sql("""
            SELECT COALESCE(SUM(outstanding_amount), 0)
            FROM `tabInvoice`
            WHERE organization = %s
            AND docstatus = 1
            AND outstanding_amount > 0
        """, self.organization)[0][0]

        frappe.db.set_value("Association", self.name, {
            "total_units": self.total_units,
            "total_members": self.total_members,
            "total_outstanding": self.total_outstanding
        }, update_modified=False)

    def get_board_members(self) -> List[dict]:
        """Get current board members."""
        return frappe.get_all(
            "Board Position",
            filters={
                "association": self.name,
                "status": "Active"
            },
            fields=["member", "position", "term_start", "term_end"]
        )

    def get_committees(self) -> List[dict]:
        """Get all committees."""
        return frappe.get_all(
            "Committee",
            filters={"association": self.name, "status": "Active"},
            fields=["name", "committee_name", "committee_type", "chair"]
        )
```

### Association DocType JSON

```json
{
  "name": "Association",
  "module": "Dartwing AMS",
  "doctype": "DocType",
  "document_type": "Document",
  "engine": "InnoDB",
  "field_order": [
    "basic_section",
    "organization",
    "association_type",
    "legal_name",
    "dba_name",
    "column_break_1",
    "ein",
    "incorporation_state",
    "incorporation_date",
    "fiscal_year_start",
    "location_section",
    "address_line_1",
    "address_line_2",
    "city",
    "column_break_2",
    "state",
    "postal_code",
    "country",
    "contact_section",
    "phone",
    "email",
    "website",
    "config_section",
    "compliance_pack",
    "timezone",
    "currency",
    "default_language",
    "hierarchy_section",
    "management_company",
    "parent_association",
    "stats_section",
    "total_units",
    "total_members",
    "total_outstanding",
    "status_section",
    "status"
  ],
  "fields": [
    {
      "fieldname": "basic_section",
      "fieldtype": "Section Break",
      "label": "Basic Information"
    },
    {
      "fieldname": "organization",
      "fieldtype": "Link",
      "options": "Organization",
      "label": "Organization",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "association_type",
      "fieldtype": "Select",
      "options": "\nHOA\nCondo\nCountry Club\nGolf Club\nAlumni\nProfessional Society\nTrade Association",
      "label": "Association Type",
      "reqd": 1
    },
    {
      "fieldname": "legal_name",
      "fieldtype": "Data",
      "label": "Legal Name",
      "reqd": 1
    },
    {
      "fieldname": "dba_name",
      "fieldtype": "Data",
      "label": "DBA Name"
    },
    {
      "fieldname": "ein",
      "fieldtype": "Password",
      "label": "EIN"
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "options": "Active\nSuspended\nDissolved",
      "label": "Status",
      "default": "Active"
    }
  ],
  "permissions": [
    {
      "role": "Association Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0
    },
    {
      "role": "Board Member",
      "read": 1,
      "write": 0
    }
  ]
}
```

## 2.3 Property & Unit DocTypes

### Unit DocType

```python
# dartwing_ams/doctype/unit/unit.py

import frappe
from frappe.model.document import Document
from typing import Optional, List

class Unit(Document):
    """
    Property unit/lot within an association.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - unit_number: Data (required) - e.g., "101", "A-15", "Lot 42"
    - unit_type: Select [Unit, Lot, Townhome, Villa, Penthouse]

    # Location
    - building: Link to Building
    - floor: Int
    - address_line_1: Data
    - address_line_2: Data
    - city: Data
    - state: Data
    - postal_code: Data

    # Property Details
    - bedrooms: Int
    - bathrooms: Float
    - square_feet: Int
    - lot_size_sqft: Int
    - year_built: Int
    - parking_spaces: Int
    - has_garage: Check
    - garage_spaces: Int

    # Financial
    - assessment_value: Currency
    - ownership_percentage: Percent (for condos)
    - monthly_assessment: Currency
    - special_assessment_balance: Currency

    # Ownership
    - ownership_type: Select [Owner Occupied, Rented, Vacant, Commercial]
    - current_owner: Link to Member
    - purchase_date: Date
    - purchase_price: Currency

    # Status
    - status: Select [Active, Foreclosure, Sold, Dissolved]
    - is_delinquent: Check (computed)
    - delinquent_amount: Currency (computed)
    - delinquent_days: Int (computed)

    # Rental Info (if rented)
    - is_rented: Check
    - tenant: Link to Member
    - lease_start: Date
    - lease_end: Date
    - monthly_rent: Currency

    # Child Tables
    - unit_members: Table (Unit Member)
    - vehicles: Table (Unit Vehicle)
    - pets: Table (Unit Pet)
    """

    def validate(self):
        self.validate_ownership()
        self.calculate_delinquency()

    def validate_ownership(self):
        """Validate ownership percentage for condos."""
        if self.ownership_percentage and self.ownership_percentage > 100:
            frappe.throw("Ownership percentage cannot exceed 100%")

    def calculate_delinquency(self):
        """Calculate delinquency status."""
        outstanding = frappe.db.sql("""
            SELECT
                COALESCE(SUM(outstanding_amount), 0) as amount,
                DATEDIFF(CURDATE(), MIN(due_date)) as days
            FROM `tabInvoice`
            WHERE unit = %s
            AND docstatus = 1
            AND outstanding_amount > 0
            AND due_date < CURDATE()
        """, self.name, as_dict=True)[0]

        self.is_delinquent = outstanding.amount > 0
        self.delinquent_amount = outstanding.amount
        self.delinquent_days = outstanding.days or 0

    def get_residents(self) -> List[dict]:
        """Get all residents of this unit."""
        return frappe.get_all(
            "Unit Member",
            filters={"parent": self.name, "status": "Active"},
            fields=["member", "relationship", "is_primary", "move_in_date"]
        )

    def get_violation_history(self) -> List[dict]:
        """Get violation history for this unit."""
        return frappe.get_all(
            "Violation",
            filters={"unit": self.name},
            fields=["name", "violation_type", "status", "created_date", "fine_amount"],
            order_by="created_date desc"
        )

    def get_arc_history(self) -> List[dict]:
        """Get ARC request history for this unit."""
        return frappe.get_all(
            "ARC Request",
            filters={"unit": self.name},
            fields=["name", "request_type", "status", "submitted_date", "decision_date"],
            order_by="submitted_date desc"
        )

    def get_work_orders(self, status: str = None) -> List[dict]:
        """Get work orders for this unit."""
        filters = {"unit": self.name}
        if status:
            filters["status"] = status

        return frappe.get_all(
            "Work Order",
            filters=filters,
            fields=["name", "category", "priority", "status", "created_date"],
            order_by="created_date desc"
        )

    def transfer_ownership(
        self,
        new_owner: str,
        transfer_date: str,
        sale_price: float = None
    ):
        """Transfer unit ownership to new member."""
        # Archive current owner
        if self.current_owner:
            frappe.get_doc({
                "doctype": "Unit Ownership History",
                "unit": self.name,
                "owner": self.current_owner,
                "start_date": self.purchase_date,
                "end_date": transfer_date,
                "purchase_price": self.purchase_price,
                "sale_price": sale_price
            }).insert(ignore_permissions=True)

        # Update unit
        self.current_owner = new_owner
        self.purchase_date = transfer_date
        self.purchase_price = sale_price
        self.save()

        # Update unit members
        frappe.db.sql("""
            UPDATE `tabUnit Member`
            SET status = 'Inactive', move_out_date = %s
            WHERE parent = %s AND relationship = 'Owner'
        """, (transfer_date, self.name))

        # Add new owner as unit member
        frappe.get_doc({
            "doctype": "Unit Member",
            "parent": self.name,
            "parenttype": "Unit",
            "parentfield": "unit_members",
            "member": new_owner,
            "relationship": "Owner",
            "is_primary": 1,
            "move_in_date": transfer_date,
            "status": "Active"
        }).insert(ignore_permissions=True)
```

### Building DocType

```python
# dartwing_ams/doctype/building/building.py

import frappe
from frappe.model.document import Document

class Building(Document):
    """
    Building within an association (for condos/high-rises).

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - building_name: Data (required)
    - building_code: Data (e.g., "A", "North Tower")

    # Location
    - address_line_1: Data
    - address_line_2: Data
    - city: Data
    - state: Data
    - postal_code: Data
    - latitude: Float
    - longitude: Float

    # Details
    - floors: Int
    - total_units: Int (computed)
    - year_built: Int
    - building_type: Select [High Rise, Mid Rise, Low Rise, Garden Style, Townhome, Mixed Use]

    # Amenities
    - has_elevator: Check
    - elevator_count: Int
    - has_pool: Check
    - has_gym: Check
    - has_lobby: Check
    - has_parking_garage: Check
    - parking_spaces: Int

    # Management
    - building_manager: Link to Member
    - front_desk_phone: Data
    - emergency_phone: Data

    # Child Tables
    - common_areas: Table (Building Common Area)
    - assets: Table (Building Asset)

    # Status
    - status: Select [Active, Under Construction, Renovation, Demolished]
    """

    def on_update(self):
        self.update_unit_count()

    def update_unit_count(self):
        """Update total units count."""
        count = frappe.db.count("Unit", {"building": self.name, "status": "Active"})
        frappe.db.set_value("Building", self.name, "total_units", count, update_modified=False)

    def get_units(self, floor: int = None) -> list:
        """Get all units in building, optionally filtered by floor."""
        filters = {"building": self.name, "status": "Active"}
        if floor:
            filters["floor"] = floor

        return frappe.get_all(
            "Unit",
            filters=filters,
            fields=["name", "unit_number", "floor", "current_owner", "is_delinquent"],
            order_by="floor, unit_number"
        )

    def get_common_areas(self) -> list:
        """Get all common areas in building."""
        return frappe.get_all(
            "Common Area",
            filters={"building": self.name, "status": "Active"},
            fields=["name", "area_name", "area_type", "floor", "is_reservable"]
        )
```

### Common Area DocType

```python
# dartwing_ams/doctype/common_area/common_area.py

import frappe
from frappe.model.document import Document

class CommonArea(Document):
    """
    Common area/amenity within association.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - building: Link to Building
    - area_name: Data (required)
    - area_type: Select [Pool, Gym, Clubhouse, Tennis Court, Basketball Court,
                         Playground, Dog Park, Garden, Parking, Lobby,
                         Meeting Room, Party Room, Business Center, Other]
    - description: Text

    # Location
    - floor: Int
    - location_notes: Small Text

    # Booking
    - is_reservable: Check
    - booking_advance_days: Int (how far in advance can book)
    - max_booking_hours: Int
    - max_bookings_per_member: Int (per week/month)
    - booking_fee: Currency
    - deposit_required: Currency
    - requires_approval: Check

    # Capacity
    - capacity: Int
    - min_capacity: Int

    # Hours
    - operating_hours: Table (Operating Hours)
    - holiday_closures: Table (Holiday Closure)

    # Rules
    - rules_document: Attach
    - age_restriction: Int (minimum age)
    - guest_policy: Text
    - max_guests: Int

    # Status
    - status: Select [Active, Closed for Maintenance, Seasonal Closure, Permanently Closed]
    - closure_reason: Data
    - expected_reopen_date: Date
    """

    def validate(self):
        self.validate_booking_settings()

    def validate_booking_settings(self):
        """Validate booking-related settings."""
        if self.is_reservable:
            if not self.booking_advance_days:
                self.booking_advance_days = 30
            if not self.max_booking_hours:
                self.max_booking_hours = 4

    def is_available(self, date: str, start_time: str, end_time: str) -> bool:
        """Check if common area is available for booking."""
        if self.status != "Active":
            return False

        # Check operating hours
        day_of_week = frappe.utils.get_datetime(date).strftime("%A")
        hours = frappe.get_value(
            "Operating Hours",
            {"parent": self.name, "day_of_week": day_of_week},
            ["open_time", "close_time"],
            as_dict=True
        )

        if not hours:
            return False

        if start_time < str(hours.open_time) or end_time > str(hours.close_time):
            return False

        # Check existing bookings
        conflicting = frappe.db.exists(
            "Amenity Booking",
            {
                "common_area": self.name,
                "booking_date": date,
                "status": ["in", ["Confirmed", "Pending"]],
                "start_time": ["<", end_time],
                "end_time": [">", start_time]
            }
        )

        return not conflicting

    def get_bookings(self, date: str) -> list:
        """Get all bookings for a specific date."""
        return frappe.get_all(
            "Amenity Booking",
            filters={
                "common_area": self.name,
                "booking_date": date,
                "status": ["in", ["Confirmed", "Pending"]]
            },
            fields=["name", "member", "start_time", "end_time", "guest_count", "status"],
            order_by="start_time"
        )
```

## 2.4 Member DocTypes

### Member DocType

```python
# dartwing_ams/doctype/member/member.py

import frappe
from frappe.model.document import Document
from typing import Optional, List

class Member(Document):
    """
    Association member (extends Person from Dartwing Core).

    Fields:
    - name: Auto-generated ID
    - person: Link to Person (Dartwing Core, required)
    - organization: Link to Organization (required)

    # Membership
    - membership_type: Link to Membership Type
    - membership_number: Data (auto-generated)
    - join_date: Date
    - renewal_date: Date
    - expiry_date: Date
    - membership_status: Select [Active, Pending, Suspended, Expired, Cancelled]

    # Contact (inherited from Person, but can override for association)
    - preferred_email: Data
    - preferred_phone: Data
    - communication_preference: Select [Email, SMS, Both, Mail]

    # Account
    - user: Link to User
    - portal_enabled: Check
    - last_login: Datetime

    # Staff flags
    - is_staff: Check
    - is_board_member: Check (computed)
    - is_committee_member: Check (computed)

    # Financial
    - account_balance: Currency (computed, can be credit or debit)
    - lifetime_dues_paid: Currency (computed)
    - autopay_enabled: Check
    - default_payment_method: Link to Payment Method

    # Units
    - primary_unit: Link to Unit
    - units: Table (Member Unit)

    # Child Tables
    - role_assignments: Table (Member Role Assignment)
    - communication_preferences: Table (Communication Preference)

    # Status
    - status: Select [Active, Inactive, Suspended, Deceased]
    """

    def before_insert(self):
        self.generate_membership_number()

    def generate_membership_number(self):
        """Generate unique membership number."""
        if not self.membership_number:
            prefix = frappe.get_value("Association", self.organization, "membership_prefix") or "M"
            last = frappe.db.sql("""
                SELECT MAX(CAST(SUBSTRING(membership_number, %s) AS UNSIGNED))
                FROM `tabMember`
                WHERE organization = %s
            """, (len(prefix) + 1, self.organization))[0][0] or 0

            self.membership_number = f"{prefix}{str(last + 1).zfill(6)}"

    def validate(self):
        self.validate_membership_dates()
        self.update_computed_fields()

    def validate_membership_dates(self):
        """Validate membership date logic."""
        if self.expiry_date and self.join_date:
            if self.expiry_date < self.join_date:
                frappe.throw("Expiry date cannot be before join date")

    def update_computed_fields(self):
        """Update computed fields."""
        # Check if board member
        self.is_board_member = frappe.db.exists(
            "Board Position",
            {"member": self.name, "status": "Active"}
        )

        # Check if committee member
        self.is_committee_member = frappe.db.exists(
            "Committee Member",
            {"member": self.name, "status": "Active"}
        )

        # Calculate account balance
        self.account_balance = self.calculate_account_balance()

    def calculate_account_balance(self) -> float:
        """Calculate member's account balance (negative = owes money)."""
        # Total invoiced
        invoiced = frappe.db.sql("""
            SELECT COALESCE(SUM(grand_total), 0)
            FROM `tabInvoice`
            WHERE member = %s AND docstatus = 1
        """, self.name)[0][0]

        # Total paid
        paid = frappe.db.sql("""
            SELECT COALESCE(SUM(amount), 0)
            FROM `tabPayment`
            WHERE member = %s AND docstatus = 1
        """, self.name)[0][0]

        # Credits
        credits = frappe.db.sql("""
            SELECT COALESCE(SUM(amount), 0)
            FROM `tabMember Credit`
            WHERE member = %s AND status = 'Active'
        """, self.name)[0][0]

        return paid + credits - invoiced

    def get_timeline(self, limit: int = 50) -> List[dict]:
        """Get unified timeline of all member activities."""
        timeline = []

        # Invoices
        invoices = frappe.get_all(
            "Invoice",
            filters={"member": self.name},
            fields=["name", "invoice_date as date", "grand_total as amount", "status"],
            limit=limit
        )
        for inv in invoices:
            inv["type"] = "invoice"
            inv["description"] = f"Invoice #{inv.name} - ${inv.amount}"
            timeline.append(inv)

        # Payments
        payments = frappe.get_all(
            "Payment",
            filters={"member": self.name, "docstatus": 1},
            fields=["name", "posting_date as date", "amount", "payment_type"],
            limit=limit
        )
        for pmt in payments:
            pmt["type"] = "payment"
            pmt["description"] = f"Payment received - ${pmt.amount}"
            timeline.append(pmt)

        # Violations
        violations = frappe.get_all(
            "Violation",
            filters={"member": self.name},
            fields=["name", "created_date as date", "violation_type", "status"],
            limit=limit
        )
        for vio in violations:
            vio["type"] = "violation"
            vio["description"] = f"Violation: {vio.violation_type} - {vio.status}"
            timeline.append(vio)

        # ARC Requests
        arc_requests = frappe.get_all(
            "ARC Request",
            filters={"member": self.name},
            fields=["name", "submitted_date as date", "request_type", "status"],
            limit=limit
        )
        for arc in arc_requests:
            arc["type"] = "arc_request"
            arc["description"] = f"ARC Request: {arc.request_type} - {arc.status}"
            timeline.append(arc)

        # Work Orders
        work_orders = frappe.get_all(
            "Work Order",
            filters={"reported_by": self.name},
            fields=["name", "created_date as date", "category", "status"],
            limit=limit
        )
        for wo in work_orders:
            wo["type"] = "work_order"
            wo["description"] = f"Work Order: {wo.category} - {wo.status}"
            timeline.append(wo)

        # Sort by date descending
        timeline.sort(key=lambda x: x.get("date") or "", reverse=True)

        return timeline[:limit]

    def get_units(self) -> List[dict]:
        """Get all units associated with member."""
        return frappe.get_all(
            "Unit Member",
            filters={"member": self.name, "status": "Active"},
            fields=["parent as unit", "relationship", "is_primary", "move_in_date"]
        )

    def send_communication(
        self,
        subject: str,
        message: str,
        channels: List[str] = None
    ):
        """Send communication to member via preferred channels."""
        if not channels:
            channels = [self.communication_preference or "Email"]

        person = frappe.get_doc("Person", self.person)

        if "Email" in channels and (self.preferred_email or person.email):
            frappe.sendmail(
                recipients=[self.preferred_email or person.email],
                subject=subject,
                message=message
            )

        if "SMS" in channels and (self.preferred_phone or person.mobile):
            frappe.enqueue(
                "dartwing_core.communications.sms.send_sms",
                phone=self.preferred_phone or person.mobile,
                message=f"{subject}\n\n{message[:160]}"
            )
```

### Membership Type DocType

```python
# dartwing_ams/doctype/membership_type/membership_type.py

import frappe
from frappe.model.document import Document

class MembershipType(Document):
    """
    Membership tier/type configuration.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - type_name: Data (required) - e.g., "Full Golf", "Social", "Student"
    - type_code: Data (required) - e.g., "FG", "SOC", "STU"
    - description: Text

    # Pricing
    - initiation_fee: Currency
    - annual_dues: Currency
    - monthly_dues: Currency
    - billing_frequency: Select [Monthly, Quarterly, Semi-Annual, Annual]
    - proration_method: Select [None, Monthly, Daily]

    # Benefits
    - voting_rights: Check
    - board_eligible: Check
    - guest_passes_per_year: Int
    - amenity_access: Table (Amenity Access)

    # Eligibility
    - min_age: Int
    - max_age: Int
    - requires_sponsor: Check
    - requires_approval: Check
    - max_members: Int (0 = unlimited)

    # Renewal
    - auto_renew: Check
    - renewal_reminder_days: Int (days before expiry)
    - grace_period_days: Int

    # Display
    - display_order: Int
    - is_public: Check (show on website)
    - badge_color: Color

    # Status
    - status: Select [Active, Inactive, Grandfathered]
    """

    def validate(self):
        self.validate_pricing()
        self.validate_eligibility()

    def validate_pricing(self):
        """Ensure at least one pricing option is set."""
        if not self.annual_dues and not self.monthly_dues:
            frappe.throw("Either annual or monthly dues must be specified")

    def validate_eligibility(self):
        """Validate age restrictions."""
        if self.min_age and self.max_age and self.min_age > self.max_age:
            frappe.throw("Minimum age cannot be greater than maximum age")

    def get_current_member_count(self) -> int:
        """Get count of active members with this type."""
        return frappe.db.count(
            "Member",
            {"membership_type": self.name, "membership_status": "Active"}
        )

    def is_available(self) -> bool:
        """Check if membership type is available for new signups."""
        if self.status != "Active":
            return False

        if self.max_members and self.get_current_member_count() >= self.max_members:
            return False

        return True
```

## 2.5 Violation & Compliance DocTypes

### Violation DocType

```python
# dartwing_ams/doctype/violation/violation.py

import frappe
from frappe.model.document import Document
from typing import Optional, List
from datetime import datetime, timedelta

class Violation(Document):
    """
    Rule violation tracking and enforcement.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - unit: Link to Unit (required)
    - member: Link to Member (computed from unit owner)

    # Violation Details
    - violation_type: Link to Violation Type (required)
    - violation_category: Data (from type)
    - description: Text (required)
    - location: Data
    - occurred_date: Date
    - discovered_date: Date
    - reported_by: Link to Member

    # Evidence
    - photos: Attach Multiple
    - documents: Attach Multiple
    - inspector_notes: Text

    # Status & Workflow
    - status: Select [Draft, Notice Sent, Cure Period, Hearing Scheduled,
                      Hearing Held, Fined, Resolved, Dismissed, Escalated]
    - cure_deadline: Date
    - is_repeat_offense: Check
    - repeat_count: Int (how many times same type)

    # Notices
    - first_notice_date: Date
    - first_notice_method: Select [Email, Mail, Both]
    - second_notice_date: Date
    - third_notice_date: Date

    # Hearing
    - hearing: Link to Violation Hearing
    - hearing_date: Date
    - hearing_result: Select [Pending, Upheld, Dismissed, Modified]

    # Fines
    - fine_amount: Currency
    - fine_due_date: Date
    - fine_paid: Check
    - fine_waived: Check
    - fine_waived_reason: Text

    # Resolution
    - resolution_date: Date
    - resolution_notes: Text
    - resolved_by: Link to User

    # Liens (for severe cases)
    - lien_filed: Check
    - lien_date: Date
    - lien_amount: Currency
    - lien_released: Check
    - lien_release_date: Date
    """

    def before_insert(self):
        self.set_member_from_unit()
        self.check_repeat_offense()

    def validate(self):
        self.validate_dates()
        self.calculate_fine()

    def set_member_from_unit(self):
        """Set member from unit's current owner."""
        if self.unit and not self.member:
            self.member = frappe.get_value("Unit", self.unit, "current_owner")

    def check_repeat_offense(self):
        """Check if this is a repeat offense."""
        if self.unit and self.violation_type:
            count = frappe.db.count(
                "Violation",
                {
                    "unit": self.unit,
                    "violation_type": self.violation_type,
                    "status": ["not in", ["Draft", "Dismissed"]],
                    "name": ["!=", self.name or ""]
                }
            )
            self.is_repeat_offense = count > 0
            self.repeat_count = count

    def validate_dates(self):
        """Validate date logic."""
        if self.cure_deadline and self.discovered_date:
            if self.cure_deadline < self.discovered_date:
                frappe.throw("Cure deadline cannot be before discovered date")

    def calculate_fine(self):
        """Calculate fine amount based on violation type and repeat count."""
        if self.violation_type and not self.fine_amount:
            vtype = frappe.get_doc("Violation Type", self.violation_type)

            if self.is_repeat_offense and vtype.repeat_fine_amount:
                self.fine_amount = vtype.repeat_fine_amount * min(self.repeat_count, 3)
            else:
                self.fine_amount = vtype.base_fine_amount

    def send_notice(self, notice_type: str = "first"):
        """Send violation notice to member."""
        template_map = {
            "first": "First Violation Notice",
            "second": "Second Violation Notice",
            "final": "Final Violation Notice",
            "hearing": "Hearing Notice"
        }

        template = frappe.get_doc("Email Template", template_map.get(notice_type))
        member = frappe.get_doc("Member", self.member)

        # Render template
        message = frappe.render_template(template.response, {
            "violation": self,
            "member": member,
            "unit": frappe.get_doc("Unit", self.unit)
        })

        # Send notification
        member.send_communication(
            subject=f"Violation Notice - {self.violation_type}",
            message=message,
            channels=["Email", "Mail"] if notice_type == "final" else ["Email"]
        )

        # Update notice dates
        if notice_type == "first":
            self.first_notice_date = frappe.utils.today()
            self.status = "Notice Sent"
        elif notice_type == "second":
            self.second_notice_date = frappe.utils.today()
        elif notice_type == "final":
            self.third_notice_date = frappe.utils.today()

        self.save()

        # Log the notice
        frappe.get_doc({
            "doctype": "Violation Notice Log",
            "violation": self.name,
            "notice_type": notice_type,
            "sent_date": frappe.utils.today(),
            "sent_by": frappe.session.user
        }).insert(ignore_permissions=True)

    def schedule_hearing(self, hearing_date: str, hearing_time: str, location: str):
        """Schedule a violation hearing."""
        hearing = frappe.get_doc({
            "doctype": "Violation Hearing",
            "violation": self.name,
            "hearing_date": hearing_date,
            "hearing_time": hearing_time,
            "location": location,
            "status": "Scheduled"
        })
        hearing.insert()

        self.hearing = hearing.name
        self.hearing_date = hearing_date
        self.status = "Hearing Scheduled"
        self.save()

        # Send hearing notice
        self.send_notice("hearing")

        return hearing.name

    def resolve(self, resolution_notes: str = None):
        """Mark violation as resolved."""
        self.status = "Resolved"
        self.resolution_date = frappe.utils.today()
        self.resolution_notes = resolution_notes
        self.resolved_by = frappe.session.user
        self.save()

        # Send resolution confirmation
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"Violation Resolved - {self.violation_type}",
            message=f"The violation at {self.unit} has been marked as resolved."
        )
```

### Violation Type DocType

```python
# dartwing_ams/doctype/violation_type/violation_type.py

import frappe
from frappe.model.document import Document

class ViolationType(Document):
    """
    Violation type/category configuration.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - type_name: Data (required) - e.g., "Trash Can Visible", "Unapproved Modification"
    - category: Select [Architectural, Landscaping, Parking, Noise, Pet,
                        Trash, Common Area, Rental, Other]
    - description: Text
    - governing_rule: Data (bylaw reference)

    # Cure Period
    - cure_period_days: Int (default 14)
    - allows_extension: Check
    - max_extension_days: Int

    # Fines
    - base_fine_amount: Currency
    - repeat_fine_amount: Currency (for 2nd+ offense)
    - daily_fine_amount: Currency (after cure period)
    - max_fine_amount: Currency

    # Escalation
    - auto_escalate: Check
    - escalate_after_days: Int
    - escalate_to_lien: Check
    - lien_threshold: Currency (fine amount before lien filed)

    # Workflow
    - requires_hearing: Check (for certain fine amounts)
    - hearing_threshold: Currency
    - auto_dismiss_on_cure: Check

    # Templates
    - first_notice_template: Link to Email Template
    - second_notice_template: Link to Email Template
    - final_notice_template: Link to Email Template
    - hearing_notice_template: Link to Email Template

    # Status
    - is_active: Check
    """

    def validate(self):
        self.validate_fine_structure()

    def validate_fine_structure(self):
        """Validate fine amount logic."""
        if self.repeat_fine_amount and self.repeat_fine_amount < self.base_fine_amount:
            frappe.throw("Repeat fine amount should be greater than base fine")

        if self.max_fine_amount and self.base_fine_amount > self.max_fine_amount:
            frappe.throw("Base fine cannot exceed maximum fine")
```

## 2.6 ARC (Architectural Review) DocTypes

### ARC Request DocType

```python
# dartwing_ams/doctype/arc_request/arc_request.py

import frappe
from frappe.model.document import Document
from typing import List

class ARCRequest(Document):
    """
    Architectural Review Committee request.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - unit: Link to Unit (required)
    - member: Link to Member (required)

    # Request Details
    - request_type: Link to ARC Request Type (required)
    - title: Data (required)
    - description: Long Text (required)
    - estimated_cost: Currency
    - estimated_start_date: Date
    - estimated_completion_date: Date
    - contractor_name: Data
    - contractor_license: Data
    - contractor_insurance: Check

    # Documents
    - plans: Attach Multiple
    - specifications: Attach Multiple
    - photos_before: Attach Multiple
    - color_samples: Attach Multiple

    # Status & Workflow
    - status: Select [Draft, Submitted, Under Review, Additional Info Needed,
                      Committee Review, Approved, Approved with Conditions,
                      Denied, Withdrawn, Expired]
    - submitted_date: Date
    - review_deadline: Date

    # Review
    - assigned_reviewer: Link to Member
    - review_notes: Text (internal)

    # Committee Decision
    - committee_meeting: Link to Board Meeting
    - decision_date: Date
    - decision_by: Link to User
    - decision_notes: Text
    - conditions: Text (if approved with conditions)
    - denial_reason: Text

    # Approval Details (if approved)
    - approval_valid_until: Date
    - work_must_start_by: Date
    - work_must_complete_by: Date
    - requires_final_inspection: Check

    # Completion
    - actual_start_date: Date
    - actual_completion_date: Date
    - final_inspection_date: Date
    - final_inspection_passed: Check
    - photos_after: Attach Multiple
    - completion_notes: Text

    # Child Tables
    - review_history: Table (ARC Review History)
    - approvals: Table (ARC Approval) - for multi-step approvals
    """

    def before_insert(self):
        self.set_review_deadline()

    def validate(self):
        self.validate_dates()
        self.validate_documents()

    def set_review_deadline(self):
        """Set review deadline based on association rules."""
        if not self.review_deadline:
            review_days = frappe.get_value(
                "Association",
                self.association,
                "arc_review_days"
            ) or 30

            self.review_deadline = frappe.utils.add_days(
                frappe.utils.today(),
                review_days
            )

    def validate_dates(self):
        """Validate date logic."""
        if self.estimated_start_date and self.estimated_completion_date:
            if self.estimated_completion_date < self.estimated_start_date:
                frappe.throw("Completion date cannot be before start date")

    def validate_documents(self):
        """Check required documents based on request type."""
        if self.request_type:
            req_type = frappe.get_doc("ARC Request Type", self.request_type)

            if req_type.requires_plans and not self.plans:
                frappe.throw("Plans are required for this request type")

            if req_type.requires_contractor_info:
                if not self.contractor_name:
                    frappe.throw("Contractor information is required")

    def submit_request(self):
        """Submit the ARC request for review."""
        self.status = "Submitted"
        self.submitted_date = frappe.utils.today()
        self.save()

        # Notify ARC committee
        self._notify_committee()

        # Send confirmation to member
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"ARC Request Submitted - {self.title}",
            message=f"Your ARC request has been submitted and is under review. "
                    f"Review deadline: {self.review_deadline}"
        )

    def request_additional_info(self, info_needed: str):
        """Request additional information from member."""
        self.status = "Additional Info Needed"
        self.save()

        # Log the request
        frappe.get_doc({
            "doctype": "ARC Review History",
            "parent": self.name,
            "parenttype": "ARC Request",
            "parentfield": "review_history",
            "action": "Additional Info Requested",
            "notes": info_needed,
            "action_by": frappe.session.user,
            "action_date": frappe.utils.today()
        }).insert(ignore_permissions=True)

        # Notify member
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"ARC Request - Additional Information Needed",
            message=f"Additional information is needed for your ARC request:\n\n{info_needed}"
        )

    def approve(
        self,
        conditions: str = None,
        valid_until: str = None,
        start_by: str = None,
        complete_by: str = None
    ):
        """Approve the ARC request."""
        self.status = "Approved with Conditions" if conditions else "Approved"
        self.decision_date = frappe.utils.today()
        self.decision_by = frappe.session.user
        self.conditions = conditions
        self.approval_valid_until = valid_until
        self.work_must_start_by = start_by
        self.work_must_complete_by = complete_by
        self.save()

        # Notify member
        member = frappe.get_doc("Member", self.member)
        message = f"Your ARC request '{self.title}' has been approved."
        if conditions:
            message += f"\n\nConditions:\n{conditions}"

        member.send_communication(
            subject=f"ARC Request Approved - {self.title}",
            message=message
        )

    def deny(self, reason: str):
        """Deny the ARC request."""
        self.status = "Denied"
        self.decision_date = frappe.utils.today()
        self.decision_by = frappe.session.user
        self.denial_reason = reason
        self.save()

        # Notify member
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"ARC Request Denied - {self.title}",
            message=f"Your ARC request has been denied.\n\nReason:\n{reason}"
        )

    def _notify_committee(self):
        """Notify ARC committee of new request."""
        committee = frappe.get_all(
            "Committee Member",
            filters={
                "committee": ["like", "%ARC%"],
                "status": "Active"
            },
            pluck="member"
        )

        for member_id in committee:
            member = frappe.get_doc("Member", member_id)
            member.send_communication(
                subject=f"New ARC Request - {self.title}",
                message=f"A new ARC request has been submitted for review.\n\n"
                        f"Unit: {self.unit}\n"
                        f"Type: {self.request_type}\n"
                        f"Review Deadline: {self.review_deadline}"
            )
```

## 2.7 Work Order DocTypes

### Work Order DocType

```python
# dartwing_ams/doctype/work_order/work_order.py

import frappe
from frappe.model.document import Document
from typing import Optional, List
from datetime import datetime

class WorkOrder(Document):
    """
    Maintenance work order for common areas and units.

    Fields:
    - name: Auto-generated ID (WO-XXXXX)
    - association: Link to Association (required)

    # Location
    - location_type: Select [Common Area, Building, Unit]
    - common_area: Link to Common Area
    - building: Link to Building
    - unit: Link to Unit
    - specific_location: Data

    # Request Details
    - category: Link to Work Order Category (required)
    - subcategory: Data
    - title: Data (required)
    - description: Long Text (required)
    - priority: Select [Emergency, High, Medium, Low]

    # Reporter
    - reported_by: Link to Member
    - reported_by_type: Select [Member, Staff, Board, Vendor, Inspection]
    - report_date: Date
    - report_time: Time

    # Photos & Docs
    - photos: Attach Multiple
    - documents: Attach Multiple

    # Assignment
    - assigned_to: Link to Vendor
    - assigned_staff: Link to Member
    - assigned_date: Date
    - due_date: Date

    # Status & Workflow
    - status: Select [Submitted, Triaged, Assigned, Scheduled, In Progress,
                      On Hold, Pending Parts, Pending Approval, Completed,
                      Closed, Cancelled]
    - hold_reason: Data

    # Scheduling
    - scheduled_date: Date
    - scheduled_time_start: Time
    - scheduled_time_end: Time
    - access_instructions: Text

    # Work Details
    - work_started: Datetime
    - work_completed: Datetime
    - work_notes: Text
    - completion_photos: Attach Multiple

    # Cost Tracking
    - estimated_cost: Currency
    - actual_cost: Currency
    - cost_breakdown: Table (Work Order Cost)
    - billable_to_unit: Check
    - invoice: Link to Invoice

    # SLA Tracking
    - sla_response_due: Datetime
    - sla_response_met: Check
    - sla_resolution_due: Datetime
    - sla_resolution_met: Check

    # Linked Items
    - linked_asset: Link to Asset
    - linked_contract: Link to Vendor Contract
    - pm_schedule_item: Link to PM Schedule Item (if from PM)

    # Approval (for high-cost items)
    - requires_approval: Check
    - approval_threshold: Currency
    - approved_by: Link to User
    - approved_date: Datetime

    # Satisfaction
    - member_rating: Rating
    - member_feedback: Text
    - feedback_date: Date

    # Child Tables
    - labor_entries: Table (Work Order Labor)
    - material_entries: Table (Work Order Material)
    - status_history: Table (Work Order Status History)
    """

    def autoname(self):
        """Generate work order number."""
        self.name = frappe.model.naming.make_autoname("WO-.#####")

    def before_insert(self):
        self.set_sla_deadlines()
        self.check_approval_required()

    def validate(self):
        self.validate_assignment()
        self.calculate_costs()

    def on_update(self):
        self.check_sla_compliance()
        self.log_status_change()

    def set_sla_deadlines(self):
        """Set SLA deadlines based on priority."""
        sla_config = {
            "Emergency": {"response_hours": 1, "resolution_hours": 4},
            "High": {"response_hours": 4, "resolution_hours": 24},
            "Medium": {"response_hours": 24, "resolution_hours": 72},
            "Low": {"response_hours": 48, "resolution_hours": 168}
        }

        config = sla_config.get(self.priority, sla_config["Medium"])
        now = frappe.utils.now_datetime()

        self.sla_response_due = frappe.utils.add_to_date(
            now, hours=config["response_hours"]
        )
        self.sla_resolution_due = frappe.utils.add_to_date(
            now, hours=config["resolution_hours"]
        )

    def check_approval_required(self):
        """Check if approval is required based on estimated cost."""
        threshold = frappe.get_value(
            "Association",
            self.association,
            "work_order_approval_threshold"
        ) or 500

        if self.estimated_cost and self.estimated_cost >= threshold:
            self.requires_approval = True
            self.approval_threshold = threshold

    def validate_assignment(self):
        """Validate vendor/staff assignment."""
        if self.assigned_to and self.assigned_staff:
            frappe.throw("Work order can be assigned to either vendor or staff, not both")

    def calculate_costs(self):
        """Calculate total costs from labor and materials."""
        labor_cost = sum(
            entry.total_cost for entry in self.labor_entries
        ) if self.labor_entries else 0

        material_cost = sum(
            entry.total_cost for entry in self.material_entries
        ) if self.material_entries else 0

        self.actual_cost = labor_cost + material_cost

    def check_sla_compliance(self):
        """Check and update SLA compliance status."""
        now = frappe.utils.now_datetime()

        # Response SLA (when first assigned/acknowledged)
        if self.status not in ["Submitted"] and not self.sla_response_met:
            self.sla_response_met = now <= self.sla_response_due

        # Resolution SLA (when completed)
        if self.status in ["Completed", "Closed"] and not self.sla_resolution_met:
            self.sla_resolution_met = now <= self.sla_resolution_due

    def log_status_change(self):
        """Log status changes for audit trail."""
        if self.has_value_changed("status"):
            frappe.get_doc({
                "doctype": "Work Order Status History",
                "parent": self.name,
                "parenttype": "Work Order",
                "parentfield": "status_history",
                "status": self.status,
                "changed_by": frappe.session.user,
                "changed_at": frappe.utils.now_datetime(),
                "notes": self.hold_reason if self.status == "On Hold" else None
            }).insert(ignore_permissions=True)

    def assign_to_vendor(self, vendor: str, due_date: str = None):
        """Assign work order to vendor."""
        self.assigned_to = vendor
        self.assigned_date = frappe.utils.today()
        self.due_date = due_date
        self.status = "Assigned"
        self.save()

        # Notify vendor
        vendor_doc = frappe.get_doc("Vendor", vendor)
        if vendor_doc.email:
            frappe.sendmail(
                recipients=[vendor_doc.email],
                subject=f"New Work Order Assignment - {self.name}",
                message=f"You have been assigned work order {self.name}.\n\n"
                        f"Location: {self.specific_location}\n"
                        f"Priority: {self.priority}\n"
                        f"Due Date: {self.due_date}"
            )

        # Notify reporter
        if self.reported_by:
            member = frappe.get_doc("Member", self.reported_by)
            member.send_communication(
                subject=f"Work Order Update - {self.name}",
                message=f"Your work order has been assigned to {vendor_doc.vendor_name}."
            )

    def start_work(self):
        """Mark work as started."""
        self.status = "In Progress"
        self.work_started = frappe.utils.now_datetime()
        self.save()

    def complete_work(self, notes: str = None, photos: list = None):
        """Mark work as completed."""
        self.status = "Completed"
        self.work_completed = frappe.utils.now_datetime()
        self.work_notes = notes

        if photos:
            for photo in photos:
                self.append("completion_photos", {"file": photo})

        self.save()

        # Request feedback from reporter
        if self.reported_by:
            self._request_feedback()

    def _request_feedback(self):
        """Request feedback from the reporter."""
        member = frappe.get_doc("Member", self.reported_by)
        member.send_communication(
            subject=f"Work Order Completed - Please Rate",
            message=f"Work order {self.name} has been completed. "
                    f"Please rate your satisfaction with the service."
        )
```

---

_End of Section 2: Data Model Architecture_

**Next Section:** Section 3 - Financial & Billing Architecture

# Section 3: Financial & Billing Architecture

## 3.1 Financial System Overview

The Dartwing AMS financial system handles the complete lifecycle of association finances including dues billing, special assessments, collections, reserve funds, and accounting integration.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FINANCIAL SYSTEM ARCHITECTURE                           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     REVENUE SOURCES                                  │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Regular     │  │   Special    │  │   Non-Dues   │              │    │
│  │  │  Assessments │  │  Assessments │  │   Revenue    │              │    │
│  │  │              │  │              │  │              │              │    │
│  │  │ • Monthly    │  │ • One-time   │  │ • Fines      │              │    │
│  │  │ • Quarterly  │  │ • Staged     │  │ • Fees       │              │    │
│  │  │ • Annual     │  │ • Emergency  │  │ • Rentals    │              │    │
│  │  └──────────────┘  └──────────────┘  │ • Events     │              │    │
│  │                                       │ • Store      │              │    │
│  │                                       └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     BILLING ENGINE                                   │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Invoice    │  │  Proration   │  │   Late Fee   │              │    │
│  │  │  Generator   │  │   Engine     │  │   Calculator │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Payment    │  │   Auto-Pay   │  │   Payment    │              │    │
│  │  │   Allocation │  │   Processor  │  │   Plans      │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     PAYMENT PROCESSING                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Stripe     │  │   Plaid      │  │   Check      │              │    │
│  │  │   (Cards)    │  │   (ACH)      │  │   Processing │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │  Apple Pay   │  │  Google Pay  │                                │    │
│  │  │              │  │              │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     COLLECTIONS & DELINQUENCY                        │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Reminder    │  │  Escalation  │  │    Lien      │              │    │
│  │  │  Automation  │  │  Workflow    │  │  Management  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     ACCOUNTING & REPORTING                           │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  GL Engine   │  │  Fund        │  │  External    │              │    │
│  │  │  (Double     │  │  Accounting  │  │  Sync        │              │    │
│  │  │   Entry)     │  │  (Reserve/Op)│  │  (QB/Xero)   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3.2 Assessment & Dues Configuration

### Assessment Schedule DocType

```python
# dartwing_ams/doctype/assessment_schedule/assessment_schedule.py

import frappe
from frappe.model.document import Document
from typing import List, Optional
from datetime import date
from decimal import Decimal

class AssessmentSchedule(Document):
    """
    Configuration for regular assessments (dues).

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - schedule_name: Data (required) - e.g., "2024 Regular Assessment"
    - assessment_type: Select [Regular, Special, Capital]
    - description: Text

    # Timing
    - effective_date: Date (required)
    - end_date: Date (optional, for time-bound assessments)
    - billing_frequency: Select [Monthly, Quarterly, Semi-Annual, Annual]
    - billing_day: Int (1-28, day of month to bill)
    - due_day: Int (1-28, day of month payment is due)

    # Amount Calculation
    - calculation_method: Select [Flat, Per Unit, By Ownership %, By Square Footage, Tiered]
    - base_amount: Currency
    - per_sqft_rate: Currency
    - tier_table: Table (Assessment Tier)

    # Proration
    - proration_method: Select [None, Monthly, Daily]
    - prorate_on_transfer: Check

    # Late Fees
    - late_fee_type: Select [None, Flat, Percentage, Daily]
    - late_fee_amount: Currency
    - late_fee_percentage: Percent
    - late_fee_daily_rate: Currency
    - late_fee_max: Currency
    - grace_period_days: Int

    # GL Mapping
    - revenue_account: Link to Account
    - receivable_account: Link to Account
    - late_fee_account: Link to Account

    # Status
    - status: Select [Draft, Active, Suspended, Ended]

    # Child Tables
    - unit_overrides: Table (Unit Assessment Override)
    - exemptions: Table (Assessment Exemption)
    """

    def validate(self):
        self.validate_dates()
        self.validate_billing_days()
        self.validate_late_fees()

    def validate_dates(self):
        """Validate date logic."""
        if self.end_date and self.end_date < self.effective_date:
            frappe.throw("End date cannot be before effective date")

    def validate_billing_days(self):
        """Validate billing and due days."""
        if self.billing_day and (self.billing_day < 1 or self.billing_day > 28):
            frappe.throw("Billing day must be between 1 and 28")
        if self.due_day and (self.due_day < 1 or self.due_day > 28):
            frappe.throw("Due day must be between 1 and 28")

    def validate_late_fees(self):
        """Validate late fee configuration."""
        if self.late_fee_type == "Flat" and not self.late_fee_amount:
            frappe.throw("Late fee amount is required for flat fee type")
        if self.late_fee_type == "Percentage" and not self.late_fee_percentage:
            frappe.throw("Late fee percentage is required")

    def calculate_assessment_for_unit(self, unit: str) -> Decimal:
        """Calculate assessment amount for a specific unit."""
        unit_doc = frappe.get_doc("Unit", unit)

        # Check for unit-specific override
        override = self._get_unit_override(unit)
        if override:
            return Decimal(str(override.amount))

        # Check for exemption
        if self._is_exempt(unit):
            return Decimal("0")

        # Calculate based on method
        if self.calculation_method == "Flat":
            return Decimal(str(self.base_amount))

        elif self.calculation_method == "Per Unit":
            return Decimal(str(self.base_amount))

        elif self.calculation_method == "By Ownership %":
            ownership_pct = Decimal(str(unit_doc.ownership_percentage or 0)) / 100
            return Decimal(str(self.base_amount)) * ownership_pct

        elif self.calculation_method == "By Square Footage":
            sqft = Decimal(str(unit_doc.square_feet or 0))
            return sqft * Decimal(str(self.per_sqft_rate))

        elif self.calculation_method == "Tiered":
            return self._calculate_tiered_amount(unit_doc)

        return Decimal(str(self.base_amount))

    def _get_unit_override(self, unit: str) -> Optional[dict]:
        """Get unit-specific amount override."""
        for override in self.unit_overrides:
            if override.unit == unit:
                return override
        return None

    def _is_exempt(self, unit: str) -> bool:
        """Check if unit is exempt from this assessment."""
        for exemption in self.exemptions:
            if exemption.unit == unit:
                if not exemption.end_date or exemption.end_date >= frappe.utils.today():
                    return True
        return False

    def _calculate_tiered_amount(self, unit_doc) -> Decimal:
        """Calculate amount based on tier table."""
        sqft = unit_doc.square_feet or 0

        for tier in sorted(self.tier_table, key=lambda x: x.min_sqft):
            if tier.min_sqft <= sqft <= (tier.max_sqft or 999999):
                return Decimal(str(tier.amount))

        return Decimal(str(self.base_amount))

    def calculate_late_fee(self, invoice_amount: Decimal, days_late: int) -> Decimal:
        """Calculate late fee for an overdue invoice."""
        if self.late_fee_type == "None" or days_late <= (self.grace_period_days or 0):
            return Decimal("0")

        if self.late_fee_type == "Flat":
            fee = Decimal(str(self.late_fee_amount))

        elif self.late_fee_type == "Percentage":
            fee = invoice_amount * Decimal(str(self.late_fee_percentage)) / 100

        elif self.late_fee_type == "Daily":
            effective_days = days_late - (self.grace_period_days or 0)
            fee = Decimal(str(self.late_fee_daily_rate)) * effective_days

        else:
            fee = Decimal("0")

        # Apply maximum cap
        if self.late_fee_max and fee > Decimal(str(self.late_fee_max)):
            fee = Decimal(str(self.late_fee_max))

        return fee


class SpecialAssessment(Document):
    """
    Special/one-time assessment configuration.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - assessment_name: Data (required)
    - description: Long Text
    - reason: Select [Capital Improvement, Emergency Repair, Legal, Insurance, Reserve Funding, Other]

    # Amount
    - total_amount: Currency (required)
    - calculation_method: Select [Equal Split, By Ownership %, By Square Footage, Custom]

    # Timing
    - assessment_date: Date (required)
    - due_date: Date (required)

    # Payment Options
    - allow_installments: Check
    - installment_count: Int
    - installment_frequency: Select [Monthly, Quarterly]
    - first_installment_date: Date

    # Approval
    - requires_vote: Check
    - vote_date: Date
    - vote_result: Select [Pending, Approved, Rejected]
    - approval_percentage: Percent

    # GL Mapping
    - revenue_account: Link to Account
    - fund: Select [Operating, Reserve, Capital]

    # Status
    - status: Select [Draft, Approved, Billed, Completed, Cancelled]

    # Child Tables
    - unit_assessments: Table (Special Assessment Unit)
    """

    def validate(self):
        self.validate_amounts()
        self.validate_installments()

    def validate_amounts(self):
        """Validate total matches unit breakdown."""
        if self.unit_assessments:
            total = sum(ua.amount for ua in self.unit_assessments)
            if abs(total - self.total_amount) > 0.01:
                frappe.throw(f"Unit assessments total ({total}) must equal total amount ({self.total_amount})")

    def validate_installments(self):
        """Validate installment configuration."""
        if self.allow_installments:
            if not self.installment_count or self.installment_count < 2:
                frappe.throw("Installment count must be at least 2")
            if not self.first_installment_date:
                frappe.throw("First installment date is required")

    def calculate_unit_amounts(self):
        """Calculate and populate unit assessment amounts."""
        units = frappe.get_all(
            "Unit",
            filters={"association": self.association, "status": "Active"},
            fields=["name", "ownership_percentage", "square_feet"]
        )

        self.unit_assessments = []

        if self.calculation_method == "Equal Split":
            per_unit = self.total_amount / len(units)
            for unit in units:
                self.append("unit_assessments", {
                    "unit": unit.name,
                    "amount": per_unit
                })

        elif self.calculation_method == "By Ownership %":
            for unit in units:
                pct = (unit.ownership_percentage or 0) / 100
                self.append("unit_assessments", {
                    "unit": unit.name,
                    "amount": self.total_amount * pct
                })

        elif self.calculation_method == "By Square Footage":
            total_sqft = sum(u.square_feet or 0 for u in units)
            for unit in units:
                sqft_pct = (unit.square_feet or 0) / total_sqft if total_sqft else 0
                self.append("unit_assessments", {
                    "unit": unit.name,
                    "amount": self.total_amount * sqft_pct
                })

    def generate_invoices(self):
        """Generate invoices for all units."""
        if self.status != "Approved":
            frappe.throw("Special assessment must be approved before generating invoices")

        for ua in self.unit_assessments:
            unit = frappe.get_doc("Unit", ua.unit)
            member = unit.current_owner

            if not member:
                continue

            if self.allow_installments:
                self._generate_installment_invoices(ua, member)
            else:
                self._generate_single_invoice(ua, member)

        self.status = "Billed"
        self.save()

    def _generate_single_invoice(self, unit_assessment, member: str):
        """Generate single invoice for unit."""
        invoice = frappe.get_doc({
            "doctype": "Invoice",
            "organization": self.association,
            "member": member,
            "unit": unit_assessment.unit,
            "invoice_type": "Special Assessment",
            "invoice_date": self.assessment_date,
            "due_date": self.due_date,
            "special_assessment": self.name,
            "items": [{
                "description": self.assessment_name,
                "amount": unit_assessment.amount,
                "account": self.revenue_account
            }]
        })
        invoice.insert()
        invoice.submit()

    def _generate_installment_invoices(self, unit_assessment, member: str):
        """Generate installment invoices for unit."""
        installment_amount = unit_assessment.amount / self.installment_count

        for i in range(self.installment_count):
            if self.installment_frequency == "Monthly":
                due_date = frappe.utils.add_months(self.first_installment_date, i)
            else:  # Quarterly
                due_date = frappe.utils.add_months(self.first_installment_date, i * 3)

            invoice = frappe.get_doc({
                "doctype": "Invoice",
                "organization": self.association,
                "member": member,
                "unit": unit_assessment.unit,
                "invoice_type": "Special Assessment",
                "invoice_date": frappe.utils.add_days(due_date, -30),
                "due_date": due_date,
                "special_assessment": self.name,
                "installment_number": i + 1,
                "total_installments": self.installment_count,
                "items": [{
                    "description": f"{self.assessment_name} - Installment {i + 1} of {self.installment_count}",
                    "amount": installment_amount,
                    "account": self.revenue_account
                }]
            })
            invoice.insert()
            invoice.submit()
```

## 3.3 Invoice Generation Engine

```python
# dartwing_ams/billing/invoice_engine.py

import frappe
from frappe.utils import today, add_months, add_days, getdate, flt
from typing import List, Optional
from decimal import Decimal
from datetime import date

class InvoiceEngine:
    """Engine for generating and managing invoices."""

    def __init__(self, association: str):
        self.association = association
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load association billing configuration."""
        return frappe.get_value(
            "Association",
            self.association,
            ["billing_email_template", "statement_template", "currency"],
            as_dict=True
        ) or {}

    def generate_regular_assessments(self, billing_period: str):
        """
        Generate invoices for all active assessment schedules.

        Args:
            billing_period: Format "YYYY-MM" for the billing period
        """
        schedules = frappe.get_all(
            "Assessment Schedule",
            filters={
                "association": self.association,
                "status": "Active"
            }
        )

        results = {
            "generated": 0,
            "skipped": 0,
            "errors": []
        }

        for schedule in schedules:
            schedule_doc = frappe.get_doc("Assessment Schedule", schedule.name)

            # Check if this schedule bills in this period
            if not self._should_bill_in_period(schedule_doc, billing_period):
                continue

            # Get all active units
            units = frappe.get_all(
                "Unit",
                filters={
                    "association": self.association,
                    "status": "Active"
                }
            )

            for unit in units:
                try:
                    # Check if invoice already exists
                    if self._invoice_exists(schedule.name, unit.name, billing_period):
                        results["skipped"] += 1
                        continue

                    # Generate invoice
                    self._create_assessment_invoice(schedule_doc, unit.name, billing_period)
                    results["generated"] += 1

                except Exception as e:
                    results["errors"].append({
                        "unit": unit.name,
                        "schedule": schedule.name,
                        "error": str(e)
                    })

        return results

    def _should_bill_in_period(self, schedule, billing_period: str) -> bool:
        """Check if schedule should generate invoices for this period."""
        year, month = map(int, billing_period.split("-"))

        if schedule.billing_frequency == "Monthly":
            return True

        elif schedule.billing_frequency == "Quarterly":
            # Bill in Jan, Apr, Jul, Oct
            return month in [1, 4, 7, 10]

        elif schedule.billing_frequency == "Semi-Annual":
            # Bill in Jan and Jul
            return month in [1, 7]

        elif schedule.billing_frequency == "Annual":
            # Bill in month matching effective date
            effective_month = getdate(schedule.effective_date).month
            return month == effective_month

        return False

    def _invoice_exists(self, schedule: str, unit: str, billing_period: str) -> bool:
        """Check if invoice already exists for this period."""
        return frappe.db.exists(
            "Invoice",
            {
                "assessment_schedule": schedule,
                "unit": unit,
                "billing_period": billing_period,
                "docstatus": ["<", 2]  # Not cancelled
            }
        )

    def _create_assessment_invoice(
        self,
        schedule,
        unit: str,
        billing_period: str
    ):
        """Create invoice for a unit's assessment."""
        unit_doc = frappe.get_doc("Unit", unit)
        member = unit_doc.current_owner

        if not member:
            frappe.log_error(f"No owner for unit {unit}", "Invoice Generation")
            return

        # Calculate amount
        amount = schedule.calculate_assessment_for_unit(unit)

        if amount <= 0:
            return

        # Calculate dates
        year, month = map(int, billing_period.split("-"))
        invoice_date = date(year, month, schedule.billing_day or 1)
        due_date = date(year, month, schedule.due_day or 15)

        # Handle due date in next month if needed
        if schedule.due_day and schedule.due_day < schedule.billing_day:
            due_date = add_months(due_date, 1)

        # Create invoice
        invoice = frappe.get_doc({
            "doctype": "Invoice",
            "organization": self.association,
            "member": member,
            "unit": unit,
            "invoice_type": "Assessment",
            "assessment_schedule": schedule.name,
            "billing_period": billing_period,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "items": [{
                "description": f"{schedule.schedule_name} - {billing_period}",
                "amount": float(amount),
                "account": schedule.revenue_account
            }]
        })
        invoice.insert()
        invoice.submit()

        return invoice.name

    def apply_late_fees(self, as_of_date: str = None):
        """Apply late fees to overdue invoices."""
        if not as_of_date:
            as_of_date = today()

        # Get overdue invoices without late fees applied
        overdue_invoices = frappe.db.sql("""
            SELECT
                i.name,
                i.assessment_schedule,
                i.grand_total,
                i.due_date,
                DATEDIFF(%s, i.due_date) as days_late
            FROM `tabInvoice` i
            WHERE i.organization = %s
            AND i.docstatus = 1
            AND i.outstanding_amount > 0
            AND i.due_date < %s
            AND i.late_fee_applied = 0
        """, (as_of_date, self.association, as_of_date), as_dict=True)

        results = {"applied": 0, "amount": 0}

        for inv in overdue_invoices:
            if not inv.assessment_schedule:
                continue

            schedule = frappe.get_doc("Assessment Schedule", inv.assessment_schedule)
            late_fee = schedule.calculate_late_fee(
                Decimal(str(inv.grand_total)),
                inv.days_late
            )

            if late_fee > 0:
                # Create late fee invoice
                fee_invoice = frappe.get_doc({
                    "doctype": "Invoice",
                    "organization": self.association,
                    "member": frappe.get_value("Invoice", inv.name, "member"),
                    "unit": frappe.get_value("Invoice", inv.name, "unit"),
                    "invoice_type": "Late Fee",
                    "related_invoice": inv.name,
                    "invoice_date": as_of_date,
                    "due_date": as_of_date,
                    "items": [{
                        "description": f"Late Fee for Invoice {inv.name}",
                        "amount": float(late_fee),
                        "account": schedule.late_fee_account
                    }]
                })
                fee_invoice.insert()
                fee_invoice.submit()

                # Mark original invoice
                frappe.db.set_value("Invoice", inv.name, "late_fee_applied", 1)

                results["applied"] += 1
                results["amount"] += float(late_fee)

        return results

    def generate_statements(self, as_of_date: str = None):
        """Generate account statements for all members with balances."""
        if not as_of_date:
            as_of_date = today()

        # Get members with outstanding balances
        members = frappe.db.sql("""
            SELECT
                m.name,
                m.person,
                m.preferred_email,
                SUM(i.outstanding_amount) as total_due
            FROM `tabMember` m
            JOIN `tabInvoice` i ON i.member = m.name
            WHERE m.organization = %s
            AND m.status = 'Active'
            AND i.docstatus = 1
            AND i.outstanding_amount > 0
            GROUP BY m.name
            HAVING total_due > 0
        """, self.association, as_dict=True)

        for member in members:
            self._generate_member_statement(member, as_of_date)

    def _generate_member_statement(self, member: dict, as_of_date: str):
        """Generate statement for a single member."""
        # Get all invoices and payments
        invoices = frappe.get_all(
            "Invoice",
            filters={
                "member": member.name,
                "docstatus": 1
            },
            fields=["name", "invoice_date", "due_date", "grand_total",
                    "outstanding_amount", "invoice_type"],
            order_by="invoice_date"
        )

        payments = frappe.get_all(
            "Payment",
            filters={
                "member": member.name,
                "docstatus": 1
            },
            fields=["name", "posting_date", "amount", "payment_type"],
            order_by="posting_date"
        )

        # Create statement record
        statement = frappe.get_doc({
            "doctype": "Account Statement",
            "organization": self.association,
            "member": member.name,
            "statement_date": as_of_date,
            "opening_balance": self._get_opening_balance(member.name, as_of_date),
            "total_charges": sum(i.grand_total for i in invoices),
            "total_payments": sum(p.amount for p in payments),
            "closing_balance": member.total_due
        })
        statement.insert()

        # Send statement email
        if member.preferred_email:
            self._send_statement_email(statement, member)


class PaymentAllocationEngine:
    """Engine for allocating payments to invoices."""

    ALLOCATION_METHODS = {
        "FIFO": "oldest_first",
        "LIFO": "newest_first",
        "SPECIFIC": "specific_invoices",
        "PROPORTIONAL": "proportional"
    }

    def __init__(self, association: str):
        self.association = association
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load allocation configuration."""
        return frappe.get_value(
            "Association",
            self.association,
            ["payment_allocation_method", "allocate_to_oldest_first"],
            as_dict=True
        ) or {"payment_allocation_method": "FIFO"}

    def allocate_payment(
        self,
        payment: str,
        method: str = None,
        specific_invoices: List[dict] = None
    ) -> List[dict]:
        """
        Allocate a payment to outstanding invoices.

        Args:
            payment: Payment document name
            method: Allocation method (FIFO, LIFO, SPECIFIC, PROPORTIONAL)
            specific_invoices: List of {invoice, amount} for SPECIFIC method

        Returns:
            List of allocation records created
        """
        payment_doc = frappe.get_doc("Payment", payment)
        method = method or self.config.get("payment_allocation_method", "FIFO")

        remaining_amount = payment_doc.amount
        allocations = []

        if method == "SPECIFIC" and specific_invoices:
            allocations = self._allocate_specific(payment_doc, specific_invoices)

        elif method == "PROPORTIONAL":
            allocations = self._allocate_proportional(payment_doc)

        else:  # FIFO or LIFO
            oldest_first = method == "FIFO"
            allocations = self._allocate_sequential(payment_doc, oldest_first)

        return allocations

    def _allocate_sequential(self, payment, oldest_first: bool) -> List[dict]:
        """Allocate payment sequentially (FIFO or LIFO)."""
        order = "due_date ASC" if oldest_first else "due_date DESC"

        invoices = frappe.get_all(
            "Invoice",
            filters={
                "member": payment.member,
                "docstatus": 1,
                "outstanding_amount": [">", 0]
            },
            fields=["name", "outstanding_amount", "due_date"],
            order_by=order
        )

        remaining = payment.amount
        allocations = []

        for inv in invoices:
            if remaining <= 0:
                break

            alloc_amount = min(remaining, inv.outstanding_amount)

            allocation = self._create_allocation(
                payment.name,
                inv.name,
                alloc_amount
            )
            allocations.append(allocation)

            remaining -= alloc_amount

        # Handle overpayment as credit
        if remaining > 0:
            self._create_member_credit(payment.member, remaining, payment.name)

        return allocations

    def _allocate_proportional(self, payment) -> List[dict]:
        """Allocate payment proportionally across all invoices."""
        invoices = frappe.get_all(
            "Invoice",
            filters={
                "member": payment.member,
                "docstatus": 1,
                "outstanding_amount": [">", 0]
            },
            fields=["name", "outstanding_amount"]
        )

        total_outstanding = sum(i.outstanding_amount for i in invoices)
        allocations = []

        for inv in invoices:
            proportion = inv.outstanding_amount / total_outstanding
            alloc_amount = min(
                payment.amount * proportion,
                inv.outstanding_amount
            )

            allocation = self._create_allocation(
                payment.name,
                inv.name,
                alloc_amount
            )
            allocations.append(allocation)

        return allocations

    def _allocate_specific(self, payment, specific_invoices: List[dict]) -> List[dict]:
        """Allocate payment to specific invoices."""
        allocations = []

        for spec in specific_invoices:
            invoice = frappe.get_doc("Invoice", spec["invoice"])
            alloc_amount = min(spec["amount"], invoice.outstanding_amount)

            allocation = self._create_allocation(
                payment.name,
                spec["invoice"],
                alloc_amount
            )
            allocations.append(allocation)

        return allocations

    def _create_allocation(self, payment: str, invoice: str, amount: float) -> dict:
        """Create payment allocation record and update invoice."""
        allocation = frappe.get_doc({
            "doctype": "Payment Allocation",
            "payment": payment,
            "invoice": invoice,
            "allocated_amount": amount,
            "allocation_date": today()
        })
        allocation.insert()

        # Update invoice outstanding
        invoice_doc = frappe.get_doc("Invoice", invoice)
        invoice_doc.outstanding_amount -= amount
        invoice_doc.save()

        return allocation.as_dict()

    def _create_member_credit(self, member: str, amount: float, source: str):
        """Create credit for overpayment."""
        credit = frappe.get_doc({
            "doctype": "Member Credit",
            "member": member,
            "amount": amount,
            "source_type": "Overpayment",
            "source_reference": source,
            "status": "Active"
        })
        credit.insert()
```

## 3.4 Payment Processing

```python
# dartwing_ams/billing/payment_processor.py

import frappe
from frappe.utils import today, flt
from typing import Optional, Dict, Any
import stripe
from decimal import Decimal

class PaymentProcessor:
    """Unified payment processing for multiple gateways."""

    SUPPORTED_GATEWAYS = ["stripe", "plaid", "manual"]

    def __init__(self, association: str):
        self.association = association
        self.config = self._load_config()
        self._init_gateways()

    def _load_config(self) -> dict:
        """Load payment gateway configuration."""
        return frappe.get_value(
            "Association Payment Settings",
            {"association": self.association},
            ["stripe_account_id", "stripe_publishable_key", "plaid_client_id",
             "accept_cards", "accept_ach", "accept_checks", "convenience_fee_type",
             "convenience_fee_amount", "convenience_fee_percentage"],
            as_dict=True
        ) or {}

    def _init_gateways(self):
        """Initialize payment gateway clients."""
        if self.config.get("stripe_account_id"):
            stripe.api_key = frappe.get_value(
                "Stripe Settings",
                None,
                "secret_key"
            )
            self.stripe_account = self.config.stripe_account_id

    def create_payment_intent(
        self,
        member: str,
        amount: float,
        payment_method_type: str = "card",
        metadata: Dict[str, Any] = None
    ) -> dict:
        """Create a Stripe payment intent."""
        # Calculate convenience fee if applicable
        convenience_fee = self._calculate_convenience_fee(amount, payment_method_type)
        total_amount = amount + convenience_fee

        # Convert to cents for Stripe
        amount_cents = int(total_amount * 100)

        member_doc = frappe.get_doc("Member", member)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            customer=self._get_or_create_stripe_customer(member_doc),
            payment_method_types=[payment_method_type],
            metadata={
                "association": self.association,
                "member": member,
                "convenience_fee": convenience_fee,
                **(metadata or {})
            },
            stripe_account=self.stripe_account
        )

        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": total_amount,
            "convenience_fee": convenience_fee
        }

    def process_card_payment(
        self,
        member: str,
        amount: float,
        payment_method_id: str,
        invoices: list = None
    ) -> dict:
        """Process a card payment."""
        convenience_fee = self._calculate_convenience_fee(amount, "card")
        total_amount = amount + convenience_fee
        amount_cents = int(total_amount * 100)

        member_doc = frappe.get_doc("Member", member)
        customer_id = self._get_or_create_stripe_customer(member_doc)

        try:
            # Create and confirm payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="usd",
                customer=customer_id,
                payment_method=payment_method_id,
                confirm=True,
                stripe_account=self.stripe_account,
                metadata={
                    "association": self.association,
                    "member": member
                }
            )

            if intent.status == "succeeded":
                # Create payment record
                payment = self._create_payment_record(
                    member=member,
                    amount=amount,
                    convenience_fee=convenience_fee,
                    payment_type="Card",
                    gateway="stripe",
                    gateway_reference=intent.id,
                    invoices=invoices
                )

                return {
                    "success": True,
                    "payment": payment.name,
                    "gateway_reference": intent.id
                }
            else:
                return {
                    "success": False,
                    "error": f"Payment status: {intent.status}",
                    "requires_action": intent.status == "requires_action"
                }

        except stripe.error.CardError as e:
            return {
                "success": False,
                "error": e.user_message,
                "error_code": e.code
            }

    def process_ach_payment(
        self,
        member: str,
        amount: float,
        bank_account_id: str,
        invoices: list = None
    ) -> dict:
        """Process an ACH bank transfer."""
        convenience_fee = self._calculate_convenience_fee(amount, "ach")
        total_amount = amount + convenience_fee
        amount_cents = int(total_amount * 100)

        member_doc = frappe.get_doc("Member", member)
        customer_id = self._get_or_create_stripe_customer(member_doc)

        try:
            # Create ACH payment via Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="usd",
                customer=customer_id,
                payment_method=bank_account_id,
                payment_method_types=["us_bank_account"],
                confirm=True,
                stripe_account=self.stripe_account,
                mandate_data={
                    "customer_acceptance": {
                        "type": "online",
                        "online": {
                            "ip_address": frappe.local.request_ip,
                            "user_agent": frappe.request.headers.get("User-Agent")
                        }
                    }
                }
            )

            # ACH payments are pending until cleared
            payment = self._create_payment_record(
                member=member,
                amount=amount,
                convenience_fee=convenience_fee,
                payment_type="ACH",
                gateway="stripe",
                gateway_reference=intent.id,
                invoices=invoices,
                status="Pending"  # Will be confirmed via webhook
            )

            return {
                "success": True,
                "payment": payment.name,
                "gateway_reference": intent.id,
                "status": "pending"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def record_check_payment(
        self,
        member: str,
        amount: float,
        check_number: str,
        check_date: str,
        invoices: list = None
    ) -> dict:
        """Record a check payment."""
        payment = self._create_payment_record(
            member=member,
            amount=amount,
            convenience_fee=0,
            payment_type="Check",
            gateway="manual",
            gateway_reference=check_number,
            invoices=invoices,
            additional_data={
                "check_number": check_number,
                "check_date": check_date
            }
        )

        return {
            "success": True,
            "payment": payment.name
        }

    def setup_autopay(
        self,
        member: str,
        payment_method_id: str,
        payment_method_type: str = "card"
    ) -> dict:
        """Setup autopay for a member."""
        member_doc = frappe.get_doc("Member", member)
        customer_id = self._get_or_create_stripe_customer(member_doc)

        # Attach payment method to customer
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
            stripe_account=self.stripe_account
        )

        # Set as default
        stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method_id},
            stripe_account=self.stripe_account
        )

        # Update member record
        member_doc.autopay_enabled = True
        member_doc.default_payment_method = payment_method_id
        member_doc.save()

        # Create autopay enrollment record
        frappe.get_doc({
            "doctype": "Autopay Enrollment",
            "member": member,
            "payment_method_id": payment_method_id,
            "payment_method_type": payment_method_type,
            "status": "Active",
            "enrolled_date": today()
        }).insert()

        return {"success": True, "message": "Autopay enrolled successfully"}

    def process_autopay_batch(self, billing_period: str):
        """Process autopay for all enrolled members."""
        enrollments = frappe.get_all(
            "Autopay Enrollment",
            filters={
                "status": "Active"
            },
            fields=["member", "payment_method_id", "payment_method_type"]
        )

        results = {"processed": 0, "failed": 0, "errors": []}

        for enrollment in enrollments:
            # Get outstanding balance for member
            outstanding = frappe.db.sql("""
                SELECT SUM(outstanding_amount) as total
                FROM `tabInvoice`
                WHERE member = %s
                AND docstatus = 1
                AND outstanding_amount > 0
                AND due_date <= CURDATE()
            """, enrollment.member)[0][0] or 0

            if outstanding <= 0:
                continue

            # Process payment
            if enrollment.payment_method_type == "card":
                result = self.process_card_payment(
                    member=enrollment.member,
                    amount=outstanding,
                    payment_method_id=enrollment.payment_method_id
                )
            else:
                result = self.process_ach_payment(
                    member=enrollment.member,
                    amount=outstanding,
                    bank_account_id=enrollment.payment_method_id
                )

            if result.get("success"):
                results["processed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "member": enrollment.member,
                    "error": result.get("error")
                })

        return results

    def _calculate_convenience_fee(self, amount: float, payment_type: str) -> float:
        """Calculate convenience fee based on configuration."""
        if not self.config.get("convenience_fee_type"):
            return 0

        # Some associations only charge fees for certain payment types
        if payment_type == "ach" and not self.config.get("ach_convenience_fee"):
            return 0

        if self.config.convenience_fee_type == "Flat":
            return self.config.convenience_fee_amount or 0
        elif self.config.convenience_fee_type == "Percentage":
            return amount * (self.config.convenience_fee_percentage or 0) / 100

        return 0

    def _get_or_create_stripe_customer(self, member) -> str:
        """Get existing or create new Stripe customer."""
        if member.stripe_customer_id:
            return member.stripe_customer_id

        person = frappe.get_doc("Person", member.person)

        customer = stripe.Customer.create(
            email=member.preferred_email or person.email,
            name=person.full_name,
            metadata={
                "member_id": member.name,
                "association": self.association
            },
            stripe_account=self.stripe_account
        )

        member.stripe_customer_id = customer.id
        member.save()

        return customer.id

    def _create_payment_record(
        self,
        member: str,
        amount: float,
        convenience_fee: float,
        payment_type: str,
        gateway: str,
        gateway_reference: str,
        invoices: list = None,
        status: str = "Completed",
        additional_data: dict = None
    ):
        """Create payment record in the system."""
        payment = frappe.get_doc({
            "doctype": "Payment",
            "organization": self.association,
            "member": member,
            "amount": amount,
            "convenience_fee": convenience_fee,
            "total_amount": amount + convenience_fee,
            "payment_type": payment_type,
            "payment_gateway": gateway,
            "gateway_reference": gateway_reference,
            "posting_date": today(),
            "status": status,
            **(additional_data or {})
        })
        payment.insert()

        if status == "Completed":
            payment.submit()

            # Allocate to invoices
            allocator = PaymentAllocationEngine(self.association)
            if invoices:
                allocator.allocate_payment(
                    payment.name,
                    method="SPECIFIC",
                    specific_invoices=invoices
                )
            else:
                allocator.allocate_payment(payment.name)

        return payment
```

## 3.5 Collections & Delinquency Management

```python
# dartwing_ams/billing/collections.py

import frappe
from frappe.utils import today, add_days, date_diff
from typing import List, Optional
from enum import Enum

class DelinquencyStage(Enum):
    CURRENT = "current"
    REMINDER = "reminder"
    PAST_DUE_30 = "past_due_30"
    PAST_DUE_60 = "past_due_60"
    PAST_DUE_90 = "past_due_90"
    COLLECTIONS = "collections"
    LIEN = "lien"
    FORECLOSURE = "foreclosure"

class CollectionsManager:
    """Manages delinquency tracking and collection workflows."""

    def __init__(self, association: str):
        self.association = association
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load collections configuration."""
        return frappe.get_doc("Collections Settings", {"association": self.association})

    def run_delinquency_workflow(self):
        """Run the daily delinquency workflow."""
        # Get all members with outstanding balances
        delinquent_accounts = self._get_delinquent_accounts()

        for account in delinquent_accounts:
            current_stage = self._determine_stage(account)
            previous_stage = account.get("delinquency_stage")

            # Update stage if changed
            if current_stage != previous_stage:
                self._update_delinquency_stage(account["member"], current_stage)
                self._execute_stage_actions(account, current_stage)

    def _get_delinquent_accounts(self) -> List[dict]:
        """Get all accounts with outstanding balances."""
        return frappe.db.sql("""
            SELECT
                m.name as member,
                m.primary_unit as unit,
                m.delinquency_stage,
                SUM(i.outstanding_amount) as total_outstanding,
                MIN(i.due_date) as oldest_due_date,
                DATEDIFF(CURDATE(), MIN(i.due_date)) as days_past_due
            FROM `tabMember` m
            JOIN `tabInvoice` i ON i.member = m.name
            WHERE m.organization = %s
            AND i.docstatus = 1
            AND i.outstanding_amount > 0
            GROUP BY m.name
            HAVING total_outstanding > 0
        """, self.association, as_dict=True)

    def _determine_stage(self, account: dict) -> DelinquencyStage:
        """Determine delinquency stage based on days past due."""
        days = account.get("days_past_due", 0)

        if days <= 0:
            return DelinquencyStage.CURRENT
        elif days <= 15:
            return DelinquencyStage.REMINDER
        elif days <= 30:
            return DelinquencyStage.PAST_DUE_30
        elif days <= 60:
            return DelinquencyStage.PAST_DUE_60
        elif days <= 90:
            return DelinquencyStage.PAST_DUE_90
        elif days <= 120:
            return DelinquencyStage.COLLECTIONS
        else:
            # Check lien threshold
            if account.get("total_outstanding", 0) >= self.config.lien_threshold:
                return DelinquencyStage.LIEN
            return DelinquencyStage.COLLECTIONS

    def _update_delinquency_stage(self, member: str, stage: DelinquencyStage):
        """Update member's delinquency stage."""
        frappe.db.set_value("Member", member, "delinquency_stage", stage.value)

        # Log the change
        frappe.get_doc({
            "doctype": "Delinquency Log",
            "member": member,
            "stage": stage.value,
            "changed_date": today(),
            "changed_by": "System"
        }).insert(ignore_permissions=True)

    def _execute_stage_actions(self, account: dict, stage: DelinquencyStage):
        """Execute actions for delinquency stage transition."""
        member = frappe.get_doc("Member", account["member"])

        if stage == DelinquencyStage.REMINDER:
            self._send_reminder(member, account)

        elif stage == DelinquencyStage.PAST_DUE_30:
            self._send_past_due_notice(member, account, 30)
            if self.config.suspend_amenities_at_30:
                self._suspend_amenities(member)

        elif stage == DelinquencyStage.PAST_DUE_60:
            self._send_past_due_notice(member, account, 60)

        elif stage == DelinquencyStage.PAST_DUE_90:
            self._send_demand_letter(member, account)
            if self.config.attorney_referral_at_90:
                self._create_attorney_referral(member, account)

        elif stage == DelinquencyStage.COLLECTIONS:
            self._send_final_notice(member, account)

        elif stage == DelinquencyStage.LIEN:
            self._initiate_lien_process(member, account)

    def _send_reminder(self, member, account: dict):
        """Send friendly payment reminder."""
        template = frappe.get_doc("Email Template", self.config.reminder_template)

        member.send_communication(
            subject="Payment Reminder",
            message=frappe.render_template(template.response, {
                "member": member,
                "amount": account["total_outstanding"],
                "due_date": account["oldest_due_date"]
            })
        )

    def _send_past_due_notice(self, member, account: dict, days: int):
        """Send past due notice."""
        template_name = f"past_due_{days}_template"
        template = frappe.get_doc("Email Template", getattr(self.config, template_name))

        member.send_communication(
            subject=f"Past Due Notice - {days} Days",
            message=frappe.render_template(template.response, {
                "member": member,
                "amount": account["total_outstanding"],
                "days_past_due": account["days_past_due"]
            }),
            channels=["Email", "Mail"]
        )

    def _send_demand_letter(self, member, account: dict):
        """Send formal demand letter."""
        # Generate demand letter document
        letter = frappe.get_doc({
            "doctype": "Demand Letter",
            "member": member.name,
            "unit": account["unit"],
            "amount_demanded": account["total_outstanding"],
            "letter_date": today(),
            "response_deadline": add_days(today(), 10),
            "status": "Sent"
        })
        letter.insert()

        # Send via certified mail (integration with mail service)
        frappe.enqueue(
            "dartwing_ams.integrations.mail.send_certified_mail",
            letter=letter.name
        )

    def _suspend_amenities(self, member):
        """Suspend member's amenity access."""
        frappe.db.sql("""
            UPDATE `tabAmenity Access`
            SET status = 'Suspended', suspension_reason = 'Delinquent Account'
            WHERE member = %s
        """, member.name)

        # Deactivate access cards/codes
        frappe.enqueue(
            "dartwing_ams.integrations.access_control.deactivate_member_access",
            member=member.name
        )

    def _create_attorney_referral(self, member, account: dict):
        """Create attorney referral for collections."""
        referral = frappe.get_doc({
            "doctype": "Attorney Referral",
            "member": member.name,
            "unit": account["unit"],
            "amount_owed": account["total_outstanding"],
            "referral_date": today(),
            "status": "Pending"
        })
        referral.insert()

        # Notify management
        frappe.sendmail(
            recipients=[self.config.collections_manager_email],
            subject=f"Attorney Referral Created - {member.name}",
            message=f"Account referred to attorney for collection.\n\n"
                    f"Member: {member.name}\n"
                    f"Amount: ${account['total_outstanding']}"
        )

    def _initiate_lien_process(self, member, account: dict):
        """Initiate lien filing process."""
        # Create lien record
        lien = frappe.get_doc({
            "doctype": "Association Lien",
            "association": self.association,
            "unit": account["unit"],
            "member": member.name,
            "lien_amount": account["total_outstanding"],
            "initiation_date": today(),
            "status": "Pending Filing"
        })
        lien.insert()

        # Notify board
        self._notify_board_of_lien(lien)

        return lien.name

    def _notify_board_of_lien(self, lien):
        """Notify board members of lien initiation."""
        board_members = frappe.get_all(
            "Board Position",
            filters={
                "association": self.association,
                "status": "Active"
            },
            pluck="member"
        )

        for board_member in board_members:
            member = frappe.get_doc("Member", board_member)
            member.send_communication(
                subject="Lien Filing Initiated",
                message=f"A lien filing has been initiated for unit {lien.unit}.\n\n"
                        f"Amount: ${lien.lien_amount}\n\n"
                        f"Please review and approve in the board portal."
            )

    def create_payment_plan(
        self,
        member: str,
        total_amount: float,
        down_payment: float,
        installments: int,
        frequency: str = "Monthly"
    ) -> str:
        """Create a payment plan for delinquent account."""
        remaining = total_amount - down_payment
        installment_amount = remaining / installments

        plan = frappe.get_doc({
            "doctype": "Payment Plan",
            "member": member,
            "total_amount": total_amount,
            "down_payment": down_payment,
            "remaining_balance": remaining,
            "installment_amount": installment_amount,
            "installment_count": installments,
            "frequency": frequency,
            "start_date": today(),
            "status": "Active"
        })

        # Generate installment schedule
        current_date = add_days(today(), 30)  # First installment in 30 days
        for i in range(installments):
            plan.append("installments", {
                "installment_number": i + 1,
                "due_date": current_date,
                "amount": installment_amount,
                "status": "Pending"
            })

            if frequency == "Monthly":
                current_date = add_days(current_date, 30)
            elif frequency == "Bi-Weekly":
                current_date = add_days(current_date, 14)

        plan.insert()

        # Process down payment if provided
        if down_payment > 0:
            # This would trigger the payment flow
            pass

        return plan.name
```

## 3.6 Reserve Fund & Fund Accounting

```python
# dartwing_ams/accounting/fund_accounting.py

import frappe
from frappe.utils import flt, today
from typing import Dict, List
from decimal import Decimal

class FundAccountingEngine:
    """
    Manages fund-based accounting for associations.
    Supports Operating, Reserve, and Capital funds.
    """

    FUND_TYPES = ["Operating", "Reserve", "Capital", "Special"]

    def __init__(self, association: str):
        self.association = association
        self.funds = self._load_funds()

    def _load_funds(self) -> Dict[str, dict]:
        """Load all funds for the association."""
        funds = frappe.get_all(
            "Association Fund",
            filters={"association": self.association},
            fields=["name", "fund_type", "fund_name", "current_balance",
                    "target_balance", "status"]
        )
        return {f.fund_type: f for f in funds}

    def get_fund_balance(self, fund_type: str) -> Decimal:
        """Get current balance for a fund."""
        fund = self.funds.get(fund_type)
        return Decimal(str(fund.current_balance)) if fund else Decimal("0")

    def record_fund_transaction(
        self,
        fund_type: str,
        amount: float,
        transaction_type: str,  # "credit" or "debit"
        description: str,
        source_doctype: str = None,
        source_name: str = None
    ):
        """Record a transaction to a fund."""
        fund = self.funds.get(fund_type)
        if not fund:
            frappe.throw(f"Fund type {fund_type} not found")

        # Create transaction record
        transaction = frappe.get_doc({
            "doctype": "Fund Transaction",
            "fund": fund.name,
            "transaction_type": transaction_type,
            "amount": amount,
            "description": description,
            "transaction_date": today(),
            "source_doctype": source_doctype,
            "source_name": source_name,
            "balance_before": fund.current_balance
        })

        # Update fund balance
        if transaction_type == "credit":
            new_balance = fund.current_balance + amount
        else:
            new_balance = fund.current_balance - amount

        transaction.balance_after = new_balance
        transaction.insert()

        # Update fund
        frappe.db.set_value("Association Fund", fund.name, "current_balance", new_balance)

        return transaction.name

    def transfer_between_funds(
        self,
        from_fund: str,
        to_fund: str,
        amount: float,
        description: str,
        requires_approval: bool = True
    ):
        """Transfer funds between fund types."""
        if requires_approval:
            # Create transfer request for board approval
            transfer = frappe.get_doc({
                "doctype": "Fund Transfer Request",
                "from_fund": from_fund,
                "to_fund": to_fund,
                "amount": amount,
                "description": description,
                "requested_by": frappe.session.user,
                "request_date": today(),
                "status": "Pending Approval"
            })
            transfer.insert()
            return {"status": "pending", "transfer_request": transfer.name}

        # Execute transfer immediately
        self.record_fund_transaction(
            from_fund, amount, "debit",
            f"Transfer to {to_fund}: {description}"
        )
        self.record_fund_transaction(
            to_fund, amount, "credit",
            f"Transfer from {from_fund}: {description}"
        )

        return {"status": "completed"}

    def allocate_payment_to_funds(
        self,
        payment: str,
        allocations: Dict[str, float]
    ):
        """
        Allocate a payment across multiple funds.

        Args:
            payment: Payment document name
            allocations: Dict of {fund_type: amount}
        """
        payment_doc = frappe.get_doc("Payment", payment)

        for fund_type, amount in allocations.items():
            if amount > 0:
                self.record_fund_transaction(
                    fund_type,
                    amount,
                    "credit",
                    f"Payment {payment}",
                    source_doctype="Payment",
                    source_name=payment
                )

                # Record allocation
                frappe.get_doc({
                    "doctype": "Payment Fund Allocation",
                    "payment": payment,
                    "fund": fund_type,
                    "amount": amount
                }).insert(ignore_permissions=True)


class ReserveStudyManager:
    """Manages reserve study and funding analysis."""

    def __init__(self, association: str):
        self.association = association

    def create_reserve_study(
        self,
        study_date: str,
        study_type: str,  # "Full", "Update", "Visual"
        prepared_by: str
    ) -> str:
        """Create a new reserve study."""
        study = frappe.get_doc({
            "doctype": "Reserve Study",
            "association": self.association,
            "study_date": study_date,
            "study_type": study_type,
            "prepared_by": prepared_by,
            "status": "Draft"
        })
        study.insert()
        return study.name

    def add_reserve_component(
        self,
        study: str,
        component_name: str,
        category: str,
        useful_life_years: int,
        remaining_life_years: int,
        replacement_cost: float,
        quantity: int = 1
    ):
        """Add a component to reserve study."""
        frappe.get_doc({
            "doctype": "Reserve Component",
            "parent": study,
            "parenttype": "Reserve Study",
            "parentfield": "components",
            "component_name": component_name,
            "category": category,
            "useful_life_years": useful_life_years,
            "remaining_life_years": remaining_life_years,
            "replacement_cost": replacement_cost,
            "quantity": quantity,
            "total_cost": replacement_cost * quantity
        }).insert(ignore_permissions=True)

    def calculate_funding_plan(
        self,
        study: str,
        method: str = "Component"  # "Component", "Cash Flow", "Pooled"
    ) -> dict:
        """Calculate reserve funding plan."""
        study_doc = frappe.get_doc("Reserve Study", study)

        if method == "Component":
            return self._component_method(study_doc)
        elif method == "Cash Flow":
            return self._cash_flow_method(study_doc)
        else:
            return self._pooled_method(study_doc)

    def _component_method(self, study) -> dict:
        """Calculate funding using component method."""
        annual_contributions = {}

        for component in study.components:
            # Annual contribution = (Replacement Cost - Current Reserve) / Remaining Life
            current_reserve = self._get_component_reserve(component.name)
            annual = (component.total_cost - current_reserve) / max(component.remaining_life_years, 1)
            annual_contributions[component.component_name] = annual

        return {
            "method": "Component",
            "total_annual_contribution": sum(annual_contributions.values()),
            "by_component": annual_contributions
        }

    def _cash_flow_method(self, study) -> dict:
        """Calculate funding using cash flow method."""
        # Project expenditures over 30 years
        projections = self._project_expenditures(study, years=30)

        # Calculate required annual contribution to maintain positive balance
        current_balance = self._get_reserve_balance()

        # Binary search for minimum contribution
        min_contrib = self._find_minimum_contribution(
            projections,
            current_balance,
            study.inflation_rate or 3.0
        )

        return {
            "method": "Cash Flow",
            "total_annual_contribution": min_contrib,
            "projections": projections
        }

    def _pooled_method(self, study) -> dict:
        """Calculate funding using pooled method."""
        total_future_cost = sum(
            c.total_cost for c in study.components
        )

        # Apply inflation
        inflation_rate = (study.inflation_rate or 3.0) / 100
        weighted_years = sum(
            c.remaining_life_years * c.total_cost for c in study.components
        ) / total_future_cost if total_future_cost else 0

        inflated_cost = total_future_cost * ((1 + inflation_rate) ** weighted_years)

        # Annual contribution
        current_balance = self._get_reserve_balance()
        annual = (inflated_cost - current_balance) / weighted_years if weighted_years else 0

        return {
            "method": "Pooled",
            "total_annual_contribution": max(annual, 0),
            "total_future_cost": inflated_cost,
            "current_balance": current_balance
        }

    def _get_reserve_balance(self) -> float:
        """Get current reserve fund balance."""
        return frappe.get_value(
            "Association Fund",
            {"association": self.association, "fund_type": "Reserve"},
            "current_balance"
        ) or 0

    def _get_component_reserve(self, component: str) -> float:
        """Get allocated reserve for a specific component."""
        return frappe.get_value(
            "Component Reserve Allocation",
            {"component": component},
            "allocated_amount"
        ) or 0

    def _project_expenditures(self, study, years: int = 30) -> List[dict]:
        """Project expenditures over specified years."""
        projections = []
        inflation_rate = (study.inflation_rate or 3.0) / 100

        for year in range(1, years + 1):
            year_expenses = []

            for component in study.components:
                if component.remaining_life_years == year:
                    inflated_cost = component.total_cost * ((1 + inflation_rate) ** year)
                    year_expenses.append({
                        "component": component.component_name,
                        "cost": inflated_cost
                    })

            projections.append({
                "year": year,
                "expenses": year_expenses,
                "total": sum(e["cost"] for e in year_expenses)
            })

        return projections

    def _find_minimum_contribution(
        self,
        projections: List[dict],
        starting_balance: float,
        inflation_rate: float
    ) -> float:
        """Binary search for minimum annual contribution."""
        low, high = 0, sum(p["total"] for p in projections)
        interest_rate = 0.02  # Assume 2% interest on reserves

        while high - low > 100:  # Within $100
            mid = (low + high) / 2

            if self._test_contribution(mid, projections, starting_balance, interest_rate, inflation_rate):
                high = mid
            else:
                low = mid

        return high

    def _test_contribution(
        self,
        annual_contribution: float,
        projections: List[dict],
        starting_balance: float,
        interest_rate: float,
        inflation_rate: float
    ) -> bool:
        """Test if contribution maintains positive balance."""
        balance = starting_balance
        contribution = annual_contribution

        for proj in projections:
            # Add contribution (increases with inflation)
            balance += contribution

            # Add interest
            balance *= (1 + interest_rate)

            # Subtract expenses
            balance -= proj["total"]

            if balance < 0:
                return False

            # Increase contribution by inflation for next year
            contribution *= (1 + inflation_rate)

        return True
```

---

_End of Section 3: Financial & Billing Architecture_

**Next Section:** Section 4 - Governance & Board Management Architecture

# Section 4: Governance & Board Management Architecture

## 4.1 Governance System Overview

The Dartwing AMS governance module provides comprehensive tools for board management, meeting administration, voting, elections, and compliance tracking.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GOVERNANCE SYSTEM ARCHITECTURE                          │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     BOARD & COMMITTEE STRUCTURE                      │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Board     │  │  Committees  │  │   Officer    │              │    │
│  │  │  Positions   │  │   (ARC,      │  │   Terms &    │              │    │
│  │  │              │  │   Finance,   │  │   Limits     │              │    │
│  │  │ • President  │  │   Social)    │  │              │              │    │
│  │  │ • VP         │  │              │  │              │              │    │
│  │  │ • Secretary  │  │              │  │              │              │    │
│  │  │ • Treasurer  │  │              │  │              │              │    │
│  │  │ • At-Large   │  │              │  │              │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     MEETING MANAGEMENT                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Meeting    │  │   Agenda     │  │   Minutes    │              │    │
│  │  │  Scheduling  │  │   Builder    │  │   Recording  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Board      │  │   Motion     │  │  Resolution  │              │    │
│  │  │   Packets    │  │   Tracking   │  │    Log       │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     VOTING & ELECTIONS                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Election   │  │    Ballot    │  │    Proxy     │              │    │
│  │  │   Management │  │   System     │  │  Management  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │   Quorum     │  │   Results    │                                │    │
│  │  │   Tracking   │  │   Certification│                              │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     DOCUMENTS & COMPLIANCE                           │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Document    │  │   E-Sign     │  │  Compliance  │              │    │
│  │  │   Vault      │  │  Integration │  │   Tracking   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Board & Committee Structure

### Board Position DocType

```python
# dartwing_ams/doctype/board_position/board_position.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_years, getdate

class BoardPosition(Document):
    """
    Board position/officer record.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - member: Link to Member (required)

    # Position
    - position: Select [President, Vice President, Secretary, Treasurer,
                        Director, At-Large, Committee Chair]
    - position_title: Data (custom title override)
    - is_officer: Check (computed from position)

    # Term
    - term_start: Date (required)
    - term_end: Date (required)
    - term_number: Int (which term for this member)
    - is_partial_term: Check (appointed mid-term)
    - appointed_by: Select [Election, Board Appointment, Automatic Succession]

    # Voting
    - has_voting_rights: Check (default True)
    - voting_weight: Float (default 1.0, for weighted voting)

    # Responsibilities
    - committee_assignments: Table (Committee Assignment)
    - signing_authority: Check
    - spending_limit: Currency

    # Status
    - status: Select [Active, Resigned, Removed, Term Expired, Deceased]
    - resignation_date: Date
    - resignation_reason: Text
    - removal_date: Date
    - removal_reason: Text

    # Certification
    - certification_required: Check
    - certification_completed: Check
    - certification_date: Date
    - certification_document: Attach
    """

    def validate(self):
        self.validate_term_dates()
        self.validate_term_limits()
        self.set_officer_flag()
        self.check_conflicts()

    def validate_term_dates(self):
        """Validate term date logic."""
        if self.term_end <= self.term_start:
            frappe.throw("Term end date must be after term start date")

        # Typical term is 1-3 years
        max_term_days = 365 * 4
        term_days = (getdate(self.term_end) - getdate(self.term_start)).days
        if term_days > max_term_days:
            frappe.throw("Term length exceeds maximum of 4 years")

    def validate_term_limits(self):
        """Check if member has exceeded term limits."""
        config = frappe.get_value(
            "Association",
            self.association,
            ["max_consecutive_terms", "term_limit_position_specific"],
            as_dict=True
        )

        if not config.max_consecutive_terms:
            return

        # Count previous terms
        if config.term_limit_position_specific:
            # Term limits per position
            previous_terms = frappe.db.count(
                "Board Position",
                {
                    "member": self.member,
                    "position": self.position,
                    "status": ["in", ["Active", "Term Expired"]],
                    "name": ["!=", self.name or ""]
                }
            )
        else:
            # Overall board term limits
            previous_terms = frappe.db.count(
                "Board Position",
                {
                    "member": self.member,
                    "status": ["in", ["Active", "Term Expired"]],
                    "name": ["!=", self.name or ""]
                }
            )

        if previous_terms >= config.max_consecutive_terms:
            frappe.throw(
                f"Member has reached the maximum of {config.max_consecutive_terms} consecutive terms"
            )

    def set_officer_flag(self):
        """Set officer flag based on position."""
        officer_positions = ["President", "Vice President", "Secretary", "Treasurer"]
        self.is_officer = self.position in officer_positions

    def check_conflicts(self):
        """Check for conflicts with existing positions."""
        # Check if already holding this position
        existing = frappe.db.exists(
            "Board Position",
            {
                "association": self.association,
                "position": self.position,
                "status": "Active",
                "name": ["!=", self.name or ""]
            }
        )

        if existing:
            frappe.throw(f"Position {self.position} is already held by another member")

    def on_update(self):
        self.update_member_flags()

    def update_member_flags(self):
        """Update member's board member flag."""
        if self.status == "Active":
            frappe.db.set_value("Member", self.member, "is_board_member", 1)
        else:
            # Check if member has other active positions
            other_active = frappe.db.exists(
                "Board Position",
                {
                    "member": self.member,
                    "status": "Active",
                    "name": ["!=", self.name]
                }
            )
            if not other_active:
                frappe.db.set_value("Member", self.member, "is_board_member", 0)

    def resign(self, reason: str, effective_date: str = None):
        """Process board member resignation."""
        self.status = "Resigned"
        self.resignation_date = effective_date or today()
        self.resignation_reason = reason
        self.save()

        # Notify other board members
        self._notify_board_of_vacancy()

        # Log the event
        frappe.get_doc({
            "doctype": "Board Event Log",
            "association": self.association,
            "event_type": "Resignation",
            "member": self.member,
            "position": self.position,
            "event_date": self.resignation_date,
            "notes": reason
        }).insert(ignore_permissions=True)

    def _notify_board_of_vacancy(self):
        """Notify board of vacancy."""
        board_members = frappe.get_all(
            "Board Position",
            filters={
                "association": self.association,
                "status": "Active",
                "name": ["!=", self.name]
            },
            pluck="member"
        )

        for bm in board_members:
            member = frappe.get_doc("Member", bm)
            member.send_communication(
                subject=f"Board Vacancy - {self.position}",
                message=f"The position of {self.position} is now vacant due to resignation."
            )


class Committee(Document):
    """
    Committee configuration.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - committee_name: Data (required)
    - committee_type: Select [Standing, Ad-Hoc, Advisory]
    - description: Text

    # Leadership
    - chair: Link to Member
    - vice_chair: Link to Member
    - board_liaison: Link to Member (board member assigned)

    # Configuration
    - min_members: Int
    - max_members: Int
    - term_length_months: Int
    - requires_board_member: Check
    - has_budget_authority: Check
    - budget_amount: Currency

    # Meetings
    - meeting_frequency: Select [Weekly, Bi-Weekly, Monthly, Quarterly, As Needed]
    - default_meeting_day: Select [Monday..Sunday]
    - default_meeting_time: Time

    # Scope
    - charter_document: Attach
    - responsibilities: Long Text
    - authority_limits: Long Text

    # Child Tables
    - members: Table (Committee Member)

    # Status
    - status: Select [Active, Inactive, Dissolved]
    - created_date: Date
    - dissolution_date: Date
    """

    def validate(self):
        self.validate_membership()
        self.validate_leadership()

    def validate_membership(self):
        """Validate committee membership constraints."""
        member_count = len([m for m in self.members if m.status == "Active"])

        if self.min_members and member_count < self.min_members:
            frappe.msgprint(
                f"Committee has {member_count} members, minimum is {self.min_members}"
            )

        if self.max_members and member_count > self.max_members:
            frappe.throw(
                f"Committee cannot exceed {self.max_members} members"
            )

    def validate_leadership(self):
        """Validate chair is a committee member."""
        if self.chair:
            member_ids = [m.member for m in self.members if m.status == "Active"]
            if self.chair not in member_ids:
                frappe.throw("Committee chair must be a committee member")

    def add_member(
        self,
        member: str,
        role: str = "Member",
        term_start: str = None,
        term_end: str = None
    ):
        """Add a member to the committee."""
        # Check if already a member
        existing = [m for m in self.members if m.member == member and m.status == "Active"]
        if existing:
            frappe.throw("Member is already on this committee")

        self.append("members", {
            "member": member,
            "role": role,
            "term_start": term_start or today(),
            "term_end": term_end,
            "status": "Active"
        })
        self.save()

        # Update member's committee flag
        frappe.db.set_value("Member", member, "is_committee_member", 1)

    def remove_member(self, member: str, reason: str = None):
        """Remove a member from the committee."""
        for cm in self.members:
            if cm.member == member and cm.status == "Active":
                cm.status = "Removed"
                cm.end_date = today()
                cm.removal_reason = reason

        self.save()

        # Check if member is on other committees
        other_committees = frappe.db.count(
            "Committee Member",
            {
                "member": member,
                "status": "Active",
                "parent": ["!=", self.name]
            }
        )
        if not other_committees:
            frappe.db.set_value("Member", member, "is_committee_member", 0)
```

## 4.3 Meeting Management

### Board Meeting DocType

```python
# dartwing_ams/doctype/board_meeting/board_meeting.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, now_datetime, add_days
from typing import List, Optional
import json

class BoardMeeting(Document):
    """
    Board/committee meeting management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - meeting_type: Select [Regular Board, Special Board, Annual, Committee,
                            Emergency, Executive Session]
    - committee: Link to Committee (if committee meeting)
    - title: Data (required)

    # Scheduling
    - meeting_date: Date (required)
    - start_time: Time (required)
    - end_time: Time
    - timezone: Data

    # Location
    - location_type: Select [In Person, Virtual, Hybrid]
    - location_name: Data
    - location_address: Text
    - virtual_meeting_link: Data
    - virtual_meeting_id: Data
    - virtual_meeting_password: Data

    # Notice
    - notice_sent: Check
    - notice_sent_date: Datetime
    - notice_document: Attach
    - notice_days_required: Int

    # Attendance
    - quorum_required: Int
    - quorum_achieved: Check
    - attendance: Table (Meeting Attendance)

    # Agenda
    - agenda_items: Table (Agenda Item)
    - agenda_locked: Check
    - agenda_locked_by: Link to User
    - agenda_locked_at: Datetime

    # Documents
    - board_packet: Attach
    - packet_generated_at: Datetime
    - supporting_documents: Table (Meeting Document)

    # Minutes
    - minutes_draft: Long Text
    - minutes_final: Attach
    - minutes_approved: Check
    - minutes_approved_date: Date
    - minutes_approved_meeting: Link to Board Meeting

    # Status
    - status: Select [Scheduled, Notice Sent, In Progress, Completed,
                      Cancelled, Rescheduled]
    - cancellation_reason: Text
    - rescheduled_to: Link to Board Meeting
    """

    def validate(self):
        self.validate_notice_requirements()
        self.check_scheduling_conflicts()
        self.calculate_quorum_requirements()

    def validate_notice_requirements(self):
        """Validate meeting notice requirements."""
        if self.meeting_type in ["Regular Board", "Annual"]:
            min_notice = frappe.get_value(
                "Association",
                self.association,
                "regular_meeting_notice_days"
            ) or 7
        elif self.meeting_type == "Special Board":
            min_notice = frappe.get_value(
                "Association",
                self.association,
                "special_meeting_notice_days"
            ) or 3
        elif self.meeting_type == "Emergency":
            min_notice = 0
        else:
            min_notice = 3

        self.notice_days_required = min_notice

    def check_scheduling_conflicts(self):
        """Check for scheduling conflicts."""
        conflicts = frappe.get_all(
            "Board Meeting",
            filters={
                "association": self.association,
                "meeting_date": self.meeting_date,
                "status": ["not in", ["Cancelled", "Rescheduled"]],
                "name": ["!=", self.name or ""]
            }
        )

        if conflicts:
            frappe.msgprint(
                f"There is another meeting scheduled on {self.meeting_date}"
            )

    def calculate_quorum_requirements(self):
        """Calculate quorum based on bylaws."""
        if self.meeting_type in ["Regular Board", "Special Board", "Emergency"]:
            # Board meeting quorum
            total_board = frappe.db.count(
                "Board Position",
                {"association": self.association, "status": "Active"}
            )
            # Typically majority required
            self.quorum_required = (total_board // 2) + 1

        elif self.meeting_type == "Annual":
            # Member meeting quorum (from bylaws)
            config = frappe.get_value(
                "Association",
                self.association,
                ["member_quorum_percentage", "member_quorum_minimum"],
                as_dict=True
            )

            total_members = frappe.db.count(
                "Member",
                {"organization": self.association, "status": "Active"}
            )

            if config.member_quorum_percentage:
                self.quorum_required = int(total_members * config.member_quorum_percentage / 100)
            else:
                self.quorum_required = config.member_quorum_minimum or 10

    def send_notice(self):
        """Send meeting notice to attendees."""
        if self.notice_sent:
            frappe.throw("Notice has already been sent")

        # Get recipients based on meeting type
        recipients = self._get_notice_recipients()

        # Generate notice document
        notice = self._generate_notice_document()

        # Send to all recipients
        for recipient in recipients:
            member = frappe.get_doc("Member", recipient)
            member.send_communication(
                subject=f"Meeting Notice: {self.title}",
                message=self._get_notice_message(),
                channels=["Email"]
            )

        self.notice_sent = True
        self.notice_sent_date = now_datetime()
        self.notice_document = notice
        self.status = "Notice Sent"
        self.save()

    def _get_notice_recipients(self) -> List[str]:
        """Get list of members to receive notice."""
        if self.meeting_type in ["Regular Board", "Special Board", "Emergency"]:
            # Board members only
            return frappe.get_all(
                "Board Position",
                filters={"association": self.association, "status": "Active"},
                pluck="member"
            )

        elif self.committee:
            # Committee members
            return frappe.get_all(
                "Committee Member",
                filters={"parent": self.committee, "status": "Active"},
                pluck="member"
            )

        else:
            # All members (annual meeting, etc.)
            return frappe.get_all(
                "Member",
                filters={"organization": self.association, "status": "Active"},
                pluck="name"
            )

    def _get_notice_message(self) -> str:
        """Generate meeting notice message."""
        template = frappe.get_doc("Email Template", "Meeting Notice")
        return frappe.render_template(template.response, {
            "meeting": self,
            "agenda_items": self.agenda_items
        })

    def _generate_notice_document(self) -> str:
        """Generate formal notice PDF."""
        # Generate PDF using template
        html = frappe.render_template(
            "templates/meeting_notice.html",
            {"meeting": self}
        )

        pdf = frappe.utils.pdf.get_pdf(html)

        # Save as attachment
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"Meeting_Notice_{self.name}.pdf",
            "content": pdf,
            "attached_to_doctype": "Board Meeting",
            "attached_to_name": self.name
        })
        file_doc.insert(ignore_permissions=True)

        return file_doc.file_url

    def generate_board_packet(self):
        """Generate comprehensive board packet."""
        from dartwing_ams.governance.packet_generator import BoardPacketGenerator

        generator = BoardPacketGenerator(self.name)
        packet_url = generator.generate()

        self.board_packet = packet_url
        self.packet_generated_at = now_datetime()
        self.save()

        return packet_url

    def record_attendance(self, member: str, status: str, method: str = "In Person"):
        """Record member attendance."""
        # Check if already recorded
        existing = [a for a in self.attendance if a.member == member]
        if existing:
            existing[0].status = status
            existing[0].attendance_method = method
        else:
            self.append("attendance", {
                "member": member,
                "status": status,  # Present, Absent, Excused, Proxy
                "attendance_method": method,
                "check_in_time": now_datetime() if status == "Present" else None
            })

        self.save()
        self._update_quorum_status()

    def _update_quorum_status(self):
        """Update quorum achieved status."""
        present_count = len([
            a for a in self.attendance
            if a.status in ["Present", "Proxy"]
        ])

        self.quorum_achieved = present_count >= self.quorum_required

    def start_meeting(self):
        """Start the meeting."""
        if not self.quorum_achieved:
            frappe.throw("Cannot start meeting - quorum not achieved")

        self.status = "In Progress"
        self.save()

        # Create meeting log entry
        frappe.get_doc({
            "doctype": "Meeting Log Entry",
            "meeting": self.name,
            "entry_type": "Meeting Started",
            "timestamp": now_datetime()
        }).insert(ignore_permissions=True)

    def end_meeting(self):
        """End the meeting."""
        self.status = "Completed"
        self.end_time = frappe.utils.now_datetime().time()
        self.save()

        # Create meeting log entry
        frappe.get_doc({
            "doctype": "Meeting Log Entry",
            "meeting": self.name,
            "entry_type": "Meeting Ended",
            "timestamp": now_datetime()
        }).insert(ignore_permissions=True)


class AgendaItem(Document):
    """Embedded agenda item for meetings."""

    # Fields:
    # - item_number: Data
    # - title: Data (required)
    # - description: Text
    # - item_type: Select [Information, Discussion, Action, Vote, Report]
    # - presenter: Link to Member
    # - time_allocated_minutes: Int
    # - supporting_documents: Attach Multiple
    # - requires_vote: Check
    # - motion: Link to Motion (if vote taken)
    # - notes: Text
    # - status: Select [Pending, In Progress, Completed, Tabled, Deferred]
    pass
```

### Board Packet Generator

```python
# dartwing_ams/governance/packet_generator.py

import frappe
from frappe.utils import today, add_months, flt
from typing import List, Dict
import io
from PyPDF2 import PdfMerger

class BoardPacketGenerator:
    """Generates comprehensive board meeting packets."""

    SECTIONS = [
        "cover_page",
        "agenda",
        "previous_minutes",
        "financial_reports",
        "delinquency_report",
        "violations_summary",
        "arc_summary",
        "work_orders_summary",
        "committee_reports",
        "new_business",
        "supporting_documents"
    ]

    def __init__(self, meeting: str):
        self.meeting = frappe.get_doc("Board Meeting", meeting)
        self.association = self.meeting.association
        self.pdf_merger = PdfMerger()

    def generate(self) -> str:
        """Generate complete board packet."""
        sections = []

        # Generate each section
        for section in self.SECTIONS:
            method = getattr(self, f"_generate_{section}", None)
            if method:
                pdf = method()
                if pdf:
                    sections.append(pdf)

        # Merge all PDFs
        for section_pdf in sections:
            self.pdf_merger.append(io.BytesIO(section_pdf))

        # Save merged PDF
        output = io.BytesIO()
        self.pdf_merger.write(output)

        # Create file record
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"Board_Packet_{self.meeting.name}.pdf",
            "content": output.getvalue(),
            "attached_to_doctype": "Board Meeting",
            "attached_to_name": self.meeting.name
        })
        file_doc.insert(ignore_permissions=True)

        return file_doc.file_url

    def _generate_cover_page(self) -> bytes:
        """Generate packet cover page."""
        html = frappe.render_template(
            "templates/packet/cover_page.html",
            {
                "meeting": self.meeting,
                "association": frappe.get_doc("Association", self.association),
                "generated_date": today()
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_agenda(self) -> bytes:
        """Generate agenda section."""
        html = frappe.render_template(
            "templates/packet/agenda.html",
            {
                "meeting": self.meeting,
                "agenda_items": self.meeting.agenda_items
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_previous_minutes(self) -> bytes:
        """Generate previous meeting minutes."""
        previous_meeting = frappe.get_all(
            "Board Meeting",
            filters={
                "association": self.association,
                "status": "Completed",
                "meeting_date": ["<", self.meeting.meeting_date]
            },
            order_by="meeting_date desc",
            limit=1
        )

        if not previous_meeting:
            return None

        prev = frappe.get_doc("Board Meeting", previous_meeting[0].name)

        if prev.minutes_final:
            # Return the attached minutes PDF
            file_doc = frappe.get_doc("File", {"file_url": prev.minutes_final})
            return file_doc.get_content()

        # Generate from draft
        html = frappe.render_template(
            "templates/packet/minutes.html",
            {"meeting": prev, "minutes_text": prev.minutes_draft}
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_financial_reports(self) -> bytes:
        """Generate financial summary reports."""
        # Get current period data
        period_end = self.meeting.meeting_date
        period_start = add_months(period_end, -1)

        # Income statement data
        income_data = self._get_income_statement_data(period_start, period_end)

        # Balance sheet data
        balance_data = self._get_balance_sheet_data(period_end)

        # Fund balances
        fund_balances = frappe.get_all(
            "Association Fund",
            filters={"association": self.association},
            fields=["fund_type", "fund_name", "current_balance", "target_balance"]
        )

        # Collections summary
        collections = self._get_collections_summary()

        html = frappe.render_template(
            "templates/packet/financial_reports.html",
            {
                "period_start": period_start,
                "period_end": period_end,
                "income_statement": income_data,
                "balance_sheet": balance_data,
                "fund_balances": fund_balances,
                "collections": collections
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_delinquency_report(self) -> bytes:
        """Generate delinquency report."""
        delinquent_accounts = frappe.db.sql("""
            SELECT
                u.unit_number,
                m.name as member,
                p.full_name as owner_name,
                SUM(i.outstanding_amount) as total_due,
                MIN(i.due_date) as oldest_due,
                DATEDIFF(CURDATE(), MIN(i.due_date)) as days_past_due,
                m.delinquency_stage
            FROM `tabUnit` u
            JOIN `tabMember` m ON m.primary_unit = u.name
            JOIN `tabPerson` p ON p.name = m.person
            JOIN `tabInvoice` i ON i.member = m.name
            WHERE u.association = %s
            AND i.docstatus = 1
            AND i.outstanding_amount > 0
            GROUP BY u.name
            ORDER BY days_past_due DESC
        """, self.association, as_dict=True)

        # Summary stats
        total_delinquent = sum(d.total_due for d in delinquent_accounts)
        account_count = len(delinquent_accounts)

        html = frappe.render_template(
            "templates/packet/delinquency_report.html",
            {
                "accounts": delinquent_accounts,
                "total_delinquent": total_delinquent,
                "account_count": account_count,
                "as_of_date": today()
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_violations_summary(self) -> bytes:
        """Generate violations summary."""
        # Active violations
        violations = frappe.get_all(
            "Violation",
            filters={
                "association": self.association,
                "status": ["not in", ["Resolved", "Dismissed"]]
            },
            fields=["name", "unit", "violation_type", "status",
                    "created_date", "fine_amount"]
        )

        # Violations by status
        status_summary = {}
        for v in violations:
            status_summary[v.status] = status_summary.get(v.status, 0) + 1

        html = frappe.render_template(
            "templates/packet/violations_summary.html",
            {
                "violations": violations,
                "status_summary": status_summary,
                "total_fines": sum(v.fine_amount or 0 for v in violations)
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_arc_summary(self) -> bytes:
        """Generate ARC requests summary."""
        # Pending requests
        pending = frappe.get_all(
            "ARC Request",
            filters={
                "association": self.association,
                "status": ["in", ["Submitted", "Under Review", "Committee Review"]]
            },
            fields=["name", "unit", "title", "request_type",
                    "submitted_date", "review_deadline"]
        )

        # Recent decisions
        recent = frappe.get_all(
            "ARC Request",
            filters={
                "association": self.association,
                "status": ["in", ["Approved", "Approved with Conditions", "Denied"]],
                "decision_date": [">=", add_months(today(), -1)]
            },
            fields=["name", "unit", "title", "status", "decision_date"]
        )

        html = frappe.render_template(
            "templates/packet/arc_summary.html",
            {
                "pending_requests": pending,
                "recent_decisions": recent
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_work_orders_summary(self) -> bytes:
        """Generate work orders summary."""
        work_orders = frappe.get_all(
            "Work Order",
            filters={
                "association": self.association,
                "status": ["not in", ["Closed", "Cancelled"]]
            },
            fields=["name", "title", "category", "priority",
                    "status", "created_date", "estimated_cost"]
        )

        # Summary by status
        status_summary = {}
        for wo in work_orders:
            status_summary[wo.status] = status_summary.get(wo.status, 0) + 1

        html = frappe.render_template(
            "templates/packet/work_orders_summary.html",
            {
                "work_orders": work_orders,
                "status_summary": status_summary,
                "total_estimated": sum(wo.estimated_cost or 0 for wo in work_orders)
            }
        )
        return frappe.utils.pdf.get_pdf(html)

    def _generate_committee_reports(self) -> bytes:
        """Generate committee reports section."""
        committees = frappe.get_all(
            "Committee",
            filters={"association": self.association, "status": "Active"},
            fields=["name", "committee_name", "chair"]
        )

        reports = []
        for committee in committees:
            # Get latest committee report
            report = frappe.get_all(
                "Committee Report",
                filters={
                    "committee": committee.name,
                    "report_date": ["<=", self.meeting.meeting_date]
                },
                order_by="report_date desc",
                limit=1
            )

            if report:
                reports.append({
                    "committee": committee,
                    "report": frappe.get_doc("Committee Report", report[0].name)
                })

        html = frappe.render_template(
            "templates/packet/committee_reports.html",
            {"committee_reports": reports}
        )
        return frappe.utils.pdf.get_pdf(html)

    def _get_income_statement_data(self, start_date: str, end_date: str) -> dict:
        """Get income statement data for period."""
        # Revenue
        revenue = frappe.db.sql("""
            SELECT
                account,
                SUM(credit - debit) as amount
            FROM `tabGL Entry`
            WHERE organization = %s
            AND posting_date BETWEEN %s AND %s
            AND account LIKE '4%%'
            GROUP BY account
        """, (self.association, start_date, end_date), as_dict=True)

        # Expenses
        expenses = frappe.db.sql("""
            SELECT
                account,
                SUM(debit - credit) as amount
            FROM `tabGL Entry`
            WHERE organization = %s
            AND posting_date BETWEEN %s AND %s
            AND account LIKE '5%%' OR account LIKE '6%%'
            GROUP BY account
        """, (self.association, start_date, end_date), as_dict=True)

        return {
            "revenue": revenue,
            "expenses": expenses,
            "total_revenue": sum(r.amount for r in revenue),
            "total_expenses": sum(e.amount for e in expenses)
        }

    def _get_balance_sheet_data(self, as_of_date: str) -> dict:
        """Get balance sheet data."""
        # Assets
        assets = frappe.db.sql("""
            SELECT
                account,
                SUM(debit - credit) as balance
            FROM `tabGL Entry`
            WHERE organization = %s
            AND posting_date <= %s
            AND account LIKE '1%%'
            GROUP BY account
        """, (self.association, as_of_date), as_dict=True)

        # Liabilities
        liabilities = frappe.db.sql("""
            SELECT
                account,
                SUM(credit - debit) as balance
            FROM `tabGL Entry`
            WHERE organization = %s
            AND posting_date <= %s
            AND account LIKE '2%%'
            GROUP BY account
        """, (self.association, as_of_date), as_dict=True)

        # Equity
        equity = frappe.db.sql("""
            SELECT
                account,
                SUM(credit - debit) as balance
            FROM `tabGL Entry`
            WHERE organization = %s
            AND posting_date <= %s
            AND account LIKE '3%%'
            GROUP BY account
        """, (self.association, as_of_date), as_dict=True)

        return {
            "assets": assets,
            "liabilities": liabilities,
            "equity": equity,
            "total_assets": sum(a.balance for a in assets),
            "total_liabilities": sum(l.balance for l in liabilities),
            "total_equity": sum(e.balance for e in equity)
        }

    def _get_collections_summary(self) -> dict:
        """Get collections summary."""
        return frappe.db.sql("""
            SELECT
                COUNT(*) as account_count,
                SUM(CASE WHEN days_past_due BETWEEN 1 AND 30 THEN outstanding ELSE 0 END) as past_30,
                SUM(CASE WHEN days_past_due BETWEEN 31 AND 60 THEN outstanding ELSE 0 END) as past_60,
                SUM(CASE WHEN days_past_due BETWEEN 61 AND 90 THEN outstanding ELSE 0 END) as past_90,
                SUM(CASE WHEN days_past_due > 90 THEN outstanding ELSE 0 END) as past_90_plus
            FROM (
                SELECT
                    member,
                    SUM(outstanding_amount) as outstanding,
                    DATEDIFF(CURDATE(), MIN(due_date)) as days_past_due
                FROM `tabInvoice`
                WHERE organization = %s
                AND docstatus = 1
                AND outstanding_amount > 0
                GROUP BY member
            ) sub
        """, self.association, as_dict=True)[0]
```

## 4.4 Motion & Resolution Tracking

```python
# dartwing_ams/doctype/motion/motion.py

import frappe
from frappe.model.document import Document
from frappe.utils import today

class Motion(Document):
    """
    Motion tracking for board/member votes.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - meeting: Link to Board Meeting (required)
    - agenda_item: Link to Agenda Item

    # Motion Details
    - motion_number: Data
    - motion_type: Select [Resolution, Policy Change, Budget Approval,
                           Contract Approval, Assessment Approval,
                           Rule Change, Election, Other]
    - title: Data (required)
    - motion_text: Long Text (required)

    # Maker & Second
    - maker: Link to Member (required)
    - seconder: Link to Member

    # Discussion
    - discussion_notes: Long Text
    - amendments: Table (Motion Amendment)

    # Voting
    - voting_method: Select [Voice Vote, Roll Call, Ballot, Unanimous Consent]
    - voting_threshold: Select [Simple Majority, Two-Thirds, Three-Fourths, Unanimous]
    - votes_for: Int
    - votes_against: Int
    - votes_abstain: Int
    - vote_details: Table (Motion Vote)

    # Result
    - result: Select [Pending, Passed, Failed, Tabled, Withdrawn, Amended]
    - effective_date: Date

    # If creates resolution
    - creates_resolution: Check
    - resolution: Link to Resolution

    # Status
    - status: Select [Pending, Discussion, Voting, Decided, Tabled]
    """

    def validate(self):
        self.validate_voting_threshold()

    def validate_voting_threshold(self):
        """Validate voting threshold based on motion type."""
        required_thresholds = {
            "Assessment Approval": "Two-Thirds",
            "Rule Change": "Simple Majority",
            "Budget Approval": "Simple Majority"
        }

        if self.motion_type in required_thresholds:
            min_threshold = required_thresholds[self.motion_type]
            # Could add stricter validation here

    def record_vote(self, member: str, vote: str):
        """Record a member's vote."""
        # Check if already voted
        existing = [v for v in self.vote_details if v.member == member]
        if existing:
            existing[0].vote = vote
        else:
            self.append("vote_details", {
                "member": member,
                "vote": vote,  # For, Against, Abstain
                "voted_at": frappe.utils.now_datetime()
            })

        self._recalculate_totals()
        self.save()

    def _recalculate_totals(self):
        """Recalculate vote totals."""
        self.votes_for = len([v for v in self.vote_details if v.vote == "For"])
        self.votes_against = len([v for v in self.vote_details if v.vote == "Against"])
        self.votes_abstain = len([v for v in self.vote_details if v.vote == "Abstain"])

    def determine_result(self):
        """Determine motion result based on votes."""
        total_votes = self.votes_for + self.votes_against

        if total_votes == 0:
            return

        threshold_percentages = {
            "Simple Majority": 0.5,
            "Two-Thirds": 0.667,
            "Three-Fourths": 0.75,
            "Unanimous": 1.0
        }

        required_pct = threshold_percentages.get(self.voting_threshold, 0.5)
        actual_pct = self.votes_for / total_votes

        if actual_pct > required_pct:
            self.result = "Passed"

            # Create resolution if needed
            if self.creates_resolution:
                self._create_resolution()
        else:
            self.result = "Failed"

        self.status = "Decided"
        self.save()

    def _create_resolution(self):
        """Create resolution from passed motion."""
        resolution = frappe.get_doc({
            "doctype": "Resolution",
            "association": self.association,
            "source_motion": self.name,
            "title": self.title,
            "resolution_text": self.motion_text,
            "passed_date": today(),
            "effective_date": self.effective_date or today(),
            "status": "Active"
        })
        resolution.insert()

        self.resolution = resolution.name


class Resolution(Document):
    """
    Association resolution record.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - resolution_number: Data (auto-generated)
    - source_motion: Link to Motion

    # Content
    - title: Data (required)
    - resolution_text: Long Text (required)
    - category: Select [Operational, Financial, Policy, Rules, Governance]

    # Dates
    - passed_date: Date (required)
    - effective_date: Date
    - expiration_date: Date

    # Approval
    - vote_summary: Data
    - meeting: Link to Board Meeting
    - signed_by: Link to Member
    - signature_date: Date
    - signed_document: Attach

    # Supersedes
    - supersedes: Link to Resolution
    - superseded_by: Link to Resolution

    # Status
    - status: Select [Active, Superseded, Expired, Revoked]
    - revocation_date: Date
    - revocation_reason: Text
    """

    def before_insert(self):
        self.generate_resolution_number()

    def generate_resolution_number(self):
        """Generate resolution number."""
        year = frappe.utils.getdate(self.passed_date or today()).year

        count = frappe.db.count(
            "Resolution",
            {
                "association": self.association,
                "passed_date": [">=", f"{year}-01-01"],
                "passed_date": ["<=", f"{year}-12-31"]
            }
        )

        self.resolution_number = f"RES-{year}-{str(count + 1).zfill(3)}"
```

## 4.5 Elections & Voting System

```python
# dartwing_ams/doctype/election/election.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, now_datetime
from typing import List, Dict
import hashlib
import secrets

class Election(Document):
    """
    Election/ballot management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - election_type: Select [Board Election, Bylaw Amendment, Special Assessment,
                             Rule Change, Recall, Other]
    - title: Data (required)
    - description: Long Text

    # Timing
    - nomination_start: Date
    - nomination_end: Date
    - voting_start: Datetime (required)
    - voting_end: Datetime (required)

    # Configuration
    - voting_method: Select [Online Only, Paper Only, Hybrid]
    - anonymous_voting: Check
    - allow_proxies: Check
    - quorum_required: Int
    - approval_threshold: Select [Simple Majority, Two-Thirds, Three-Fourths]

    # For board elections
    - positions_available: Int
    - max_votes_per_member: Int

    # Eligibility
    - voter_eligibility: Select [All Members, Owners Only, Good Standing Only]
    - eligible_voter_count: Int (computed)

    # Candidates/Options
    - ballot_items: Table (Ballot Item)

    # Results
    - total_votes_cast: Int
    - quorum_achieved: Check
    - results_certified: Check
    - certified_by: Link to User
    - certified_date: Datetime
    - results_document: Attach

    # Status
    - status: Select [Draft, Nominations Open, Nominations Closed,
                      Voting Open, Voting Closed, Certified, Cancelled]
    """

    def validate(self):
        self.validate_dates()
        self.calculate_eligible_voters()

    def validate_dates(self):
        """Validate election date sequence."""
        if self.nomination_start and self.nomination_end:
            if self.nomination_end < self.nomination_start:
                frappe.throw("Nomination end date must be after start date")

        if self.voting_end <= self.voting_start:
            frappe.throw("Voting end must be after voting start")

    def calculate_eligible_voters(self):
        """Calculate number of eligible voters."""
        filters = {
            "organization": self.association,
            "status": "Active"
        }

        if self.voter_eligibility == "Owners Only":
            filters["membership_type"] = ["like", "%Owner%"]

        if self.voter_eligibility == "Good Standing Only":
            # Exclude delinquent members
            delinquent = frappe.get_all(
                "Member",
                filters={
                    "organization": self.association,
                    "delinquency_stage": ["not in", ["current", None]]
                },
                pluck="name"
            )
            filters["name"] = ["not in", delinquent]

        self.eligible_voter_count = frappe.db.count("Member", filters)

    def open_nominations(self):
        """Open nomination period."""
        self.status = "Nominations Open"
        self.save()

        # Notify eligible members
        self._notify_members("Nominations are now open")

    def close_nominations(self):
        """Close nomination period."""
        self.status = "Nominations Closed"
        self.save()

    def open_voting(self):
        """Open voting period."""
        if self.status != "Nominations Closed":
            frappe.throw("Cannot open voting until nominations are closed")

        self.status = "Voting Open"
        self.save()

        # Generate ballot access tokens for all eligible voters
        self._generate_ballot_tokens()

        # Notify members
        self._notify_members("Voting is now open")

    def close_voting(self):
        """Close voting period."""
        self.status = "Voting Closed"
        self.save()

        # Calculate results
        self._calculate_results()

    def _generate_ballot_tokens(self):
        """Generate unique ballot access tokens."""
        eligible_members = self._get_eligible_voters()

        for member in eligible_members:
            token = secrets.token_urlsafe(32)

            frappe.get_doc({
                "doctype": "Ballot Token",
                "election": self.name,
                "member": member,
                "token": token,
                "token_hash": hashlib.sha256(token.encode()).hexdigest(),
                "status": "Active"
            }).insert(ignore_permissions=True)

            # Send ballot notification with token
            member_doc = frappe.get_doc("Member", member)
            member_doc.send_communication(
                subject=f"Your Ballot for: {self.title}",
                message=f"Your secure voting link: {self._get_voting_url(token)}"
            )

    def _get_voting_url(self, token: str) -> str:
        """Generate voting URL with token."""
        site_url = frappe.utils.get_url()
        return f"{site_url}/vote/{self.name}?token={token}"

    def _get_eligible_voters(self) -> List[str]:
        """Get list of eligible voter member IDs."""
        filters = {
            "organization": self.association,
            "status": "Active"
        }

        if self.voter_eligibility == "Owners Only":
            # Get members who are unit owners
            return frappe.db.sql("""
                SELECT DISTINCT m.name
                FROM `tabMember` m
                JOIN `tabUnit Member` um ON um.member = m.name
                WHERE m.organization = %s
                AND m.status = 'Active'
                AND um.relationship = 'Owner'
                AND um.status = 'Active'
            """, self.association, pluck="name")

        return frappe.get_all("Member", filters=filters, pluck="name")

    def _calculate_results(self):
        """Calculate election results."""
        # Count votes for each ballot item
        for item in self.ballot_items:
            vote_count = frappe.db.count(
                "Ballot Vote",
                {"election": self.name, "ballot_item": item.name}
            )
            item.vote_count = vote_count

        # Total votes cast (unique voters)
        self.total_votes_cast = frappe.db.sql("""
            SELECT COUNT(DISTINCT voter_hash)
            FROM `tabBallot Vote`
            WHERE election = %s
        """, self.name)[0][0]

        # Check quorum
        if self.quorum_required:
            self.quorum_achieved = self.total_votes_cast >= self.quorum_required
        else:
            self.quorum_achieved = True

        self.save()

    def certify_results(self):
        """Certify election results."""
        if not self.quorum_achieved:
            frappe.throw("Cannot certify - quorum not achieved")

        self.results_certified = True
        self.certified_by = frappe.session.user
        self.certified_date = now_datetime()
        self.status = "Certified"

        # Generate results document
        self.results_document = self._generate_results_document()

        self.save()

        # Apply results (e.g., seat elected board members)
        self._apply_results()

    def _generate_results_document(self) -> str:
        """Generate official results document."""
        html = frappe.render_template(
            "templates/election_results.html",
            {
                "election": self,
                "ballot_items": sorted(
                    self.ballot_items,
                    key=lambda x: x.vote_count,
                    reverse=True
                )
            }
        )

        pdf = frappe.utils.pdf.get_pdf(html)

        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"Election_Results_{self.name}.pdf",
            "content": pdf,
            "attached_to_doctype": "Election",
            "attached_to_name": self.name
        })
        file_doc.insert(ignore_permissions=True)

        return file_doc.file_url

    def _apply_results(self):
        """Apply election results (seat winners, etc.)."""
        if self.election_type == "Board Election":
            # Get top vote-getters
            winners = sorted(
                self.ballot_items,
                key=lambda x: x.vote_count,
                reverse=True
            )[:self.positions_available]

            for winner in winners:
                if winner.candidate:
                    # Create board position
                    frappe.get_doc({
                        "doctype": "Board Position",
                        "association": self.association,
                        "member": winner.candidate,
                        "position": winner.position_title or "Director",
                        "term_start": self._get_term_start_date(),
                        "term_end": self._get_term_end_date(),
                        "appointed_by": "Election",
                        "status": "Active"
                    }).insert()

    def _notify_members(self, message: str):
        """Notify eligible members."""
        eligible = self._get_eligible_voters()

        for member_id in eligible:
            member = frappe.get_doc("Member", member_id)
            member.send_communication(
                subject=f"Election Notice: {self.title}",
                message=message
            )


class BallotVote(Document):
    """
    Individual ballot vote record.

    Fields:
    - name: Auto-generated ID
    - election: Link to Election (required)
    - ballot_item: Link to Ballot Item (required)

    # Voter (for anonymous elections, only hash stored)
    - voter_hash: Data (SHA256 of member + election)
    - is_proxy: Check
    - proxy_for: Data (voter hash of represented member)

    # Vote
    - voted_at: Datetime
    - vote_value: Int (for ranked choice or weighted voting)

    # Verification
    - receipt_code: Data (given to voter for verification)
    """

    def before_insert(self):
        self.generate_receipt_code()

    def generate_receipt_code(self):
        """Generate receipt code for vote verification."""
        self.receipt_code = secrets.token_hex(8).upper()


class ProxyAssignment(Document):
    """
    Proxy voting assignment.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - election: Link to Election
    - meeting: Link to Board Meeting

    # Assignment
    - grantor: Link to Member (required) - member giving proxy
    - holder: Link to Member (required) - member receiving proxy

    # Scope
    - proxy_type: Select [General, Limited, Directed]
    - directed_votes: Table (Directed Vote) - for directed proxies

    # Validity
    - valid_from: Date
    - valid_until: Date

    # Verification
    - grantor_signature: Attach
    - signature_date: Date
    - verified_by: Link to User
    - verification_date: Datetime

    # Status
    - status: Select [Active, Revoked, Expired, Used]
    - used_at: Datetime
    - used_in_election: Link to Election
    - used_in_meeting: Link to Board Meeting
    """

    def validate(self):
        self.validate_assignment()
        self.check_proxy_limits()

    def validate_assignment(self):
        """Validate proxy assignment."""
        if self.grantor == self.holder:
            frappe.throw("Cannot assign proxy to yourself")

    def check_proxy_limits(self):
        """Check if holder exceeds proxy limits."""
        config = frappe.get_value(
            "Association",
            self.association,
            "max_proxies_per_member"
        )

        if config:
            current_proxies = frappe.db.count(
                "Proxy Assignment",
                {
                    "association": self.association,
                    "holder": self.holder,
                    "status": "Active"
                }
            )

            if current_proxies >= config:
                frappe.throw(f"Proxy holder already has maximum of {config} proxies")
```

## 4.6 Document Management & E-Signatures

```python
# dartwing_ams/governance/document_manager.py

import frappe
from frappe.utils import today, now_datetime
from typing import List, Optional
import hashlib

class GovernanceDocumentManager:
    """Manages governance documents and e-signatures."""

    DOCUMENT_CATEGORIES = [
        "Governing Documents",
        "Policies & Rules",
        "Meeting Minutes",
        "Resolutions",
        "Contracts",
        "Financial Records",
        "Legal",
        "Compliance"
    ]

    def __init__(self, association: str):
        self.association = association

    def upload_document(
        self,
        file_content: bytes,
        filename: str,
        category: str,
        document_type: str,
        effective_date: str = None,
        requires_signature: bool = False,
        visibility: str = "Members"
    ) -> str:
        """Upload a governance document."""
        # Calculate file hash for integrity
        file_hash = hashlib.sha256(file_content).hexdigest()

        # Create file record
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "content": file_content,
            "attached_to_doctype": "Governance Document",
            "attached_to_name": None  # Will update after doc creation
        })
        file_doc.insert(ignore_permissions=True)

        # Create governance document record
        doc = frappe.get_doc({
            "doctype": "Governance Document",
            "association": self.association,
            "document_name": filename.rsplit(".", 1)[0],
            "category": category,
            "document_type": document_type,
            "file": file_doc.file_url,
            "file_hash": file_hash,
            "effective_date": effective_date,
            "requires_signature": requires_signature,
            "visibility": visibility,
            "version": 1,
            "status": "Draft" if requires_signature else "Active"
        })
        doc.insert()

        # Update file attachment
        file_doc.attached_to_name = doc.name
        file_doc.save()

        return doc.name

    def create_new_version(
        self,
        document: str,
        file_content: bytes,
        change_notes: str
    ) -> str:
        """Create new version of existing document."""
        original = frappe.get_doc("Governance Document", document)

        # Archive current version
        frappe.get_doc({
            "doctype": "Document Version History",
            "document": document,
            "version": original.version,
            "file": original.file,
            "file_hash": original.file_hash,
            "archived_date": today(),
            "archived_by": frappe.session.user
        }).insert(ignore_permissions=True)

        # Calculate new file hash
        file_hash = hashlib.sha256(file_content).hexdigest()

        # Create new file
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"{original.document_name}_v{original.version + 1}.pdf",
            "content": file_content,
            "attached_to_doctype": "Governance Document",
            "attached_to_name": document
        })
        file_doc.insert(ignore_permissions=True)

        # Update document
        original.file = file_doc.file_url
        original.file_hash = file_hash
        original.version += 1
        original.last_updated = today()
        original.change_notes = change_notes
        original.save()

        return original.name

    def request_signatures(
        self,
        document: str,
        signers: List[dict],
        due_date: str = None,
        reminder_days: int = 3
    ) -> str:
        """Request e-signatures for a document."""
        doc = frappe.get_doc("Governance Document", document)

        # Create signature request
        request = frappe.get_doc({
            "doctype": "Signature Request",
            "document": document,
            "association": self.association,
            "due_date": due_date,
            "reminder_days": reminder_days,
            "status": "Pending"
        })

        for signer in signers:
            request.append("signers", {
                "member": signer.get("member"),
                "role": signer.get("role"),
                "signing_order": signer.get("order", 1),
                "status": "Pending"
            })

        request.insert()

        # Send first signature request
        self._send_signature_request(request, request.signers[0])

        return request.name

    def _send_signature_request(self, request, signer):
        """Send signature request notification."""
        member = frappe.get_doc("Member", signer.member)
        doc = frappe.get_doc("Governance Document", request.document)

        # Generate signing link with token
        token = frappe.generate_hash(length=32)
        signer.signing_token = token
        signer.save()

        signing_url = f"{frappe.utils.get_url()}/sign/{request.name}?token={token}"

        member.send_communication(
            subject=f"Signature Required: {doc.document_name}",
            message=f"Please review and sign the following document:\n\n"
                    f"{doc.document_name}\n\n"
                    f"Click here to sign: {signing_url}\n\n"
                    f"Due date: {request.due_date}"
        )

    def apply_signature(
        self,
        request: str,
        signer_member: str,
        signature_data: str,
        ip_address: str
    ) -> bool:
        """Apply e-signature to document."""
        sig_request = frappe.get_doc("Signature Request", request)

        # Find signer record
        signer = None
        for s in sig_request.signers:
            if s.member == signer_member and s.status == "Pending":
                signer = s
                break

        if not signer:
            frappe.throw("Invalid signer or already signed")

        # Record signature
        signer.signature_data = signature_data
        signer.signed_at = now_datetime()
        signer.ip_address = ip_address
        signer.status = "Signed"

        # Check if all signatures collected
        all_signed = all(s.status == "Signed" for s in sig_request.signers)

        if all_signed:
            sig_request.status = "Completed"
            sig_request.completed_at = now_datetime()

            # Update document status
            doc = frappe.get_doc("Governance Document", sig_request.document)
            doc.status = "Active"
            doc.signed_date = today()
            doc.save()

            # Generate signed document with signature page
            self._generate_signed_document(sig_request)
        else:
            # Send request to next signer
            next_signer = self._get_next_signer(sig_request)
            if next_signer:
                self._send_signature_request(sig_request, next_signer)

        sig_request.save()
        return all_signed

    def _get_next_signer(self, request):
        """Get next signer in sequence."""
        pending = [s for s in request.signers if s.status == "Pending"]
        if pending:
            return min(pending, key=lambda x: x.signing_order)
        return None

    def _generate_signed_document(self, request):
        """Generate final signed document with signature page."""
        # Implementation would merge original PDF with signature page
        pass
```

---

_End of Section 4: Governance & Board Management Architecture_

**Workgroup 2 Complete!**

**Files Created:**

- Section 3: Financial & Billing Architecture (~1,960 lines)
- Section 4: Governance & Board Management Architecture (~1,000 lines)

**Next Workgroup:** Workgroup 3 - Sections 5, 6, 7 (Member Services, Operations & Maintenance, Integration Architecture)

# Section 5: Member Services & Portal Architecture

## 5.1 Member Services Overview

The Dartwing AMS member services module provides comprehensive self-service capabilities through web and mobile portals, including request management, amenity booking, communication preferences, and account management.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEMBER SERVICES ARCHITECTURE                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     MEMBER PORTAL (Web/Mobile)                       │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Dashboard  │  │   Account    │  │    Dues &    │              │    │
│  │  │   & Alerts   │  │   Profile    │  │   Payments   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Request    │  │   Amenity    │  │   Document   │              │    │
│  │  │    Center    │  │   Booking    │  │    Library   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Community  │  │   Directory  │  │   Voting &   │              │    │
│  │  │    Events    │  │   & Groups   │  │   Elections  │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     REQUEST MANAGEMENT                               │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Service    │  │     ARC      │  │  Maintenance │              │    │
│  │  │   Requests   │  │   Requests   │  │   Reports    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Access     │  │    Guest     │  │   Move-In/   │              │    │
│  │  │   Requests   │  │    Passes    │  │   Move-Out   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     COMMUNICATIONS                                   │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Announce-  │  │    Email     │  │    Push      │              │    │
│  │  │    ments     │  │   Campaigns  │  │   Notifs     │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │     SMS      │  │   Emergency  │                                │    │
│  │  │    Alerts    │  │    Alerts    │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     ACCESS CONTROL                                   │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Access     │  │   Guest      │  │   Vehicle    │              │    │
│  │  │   Cards/Fobs │  │   Entry      │  │ Registration │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 5.2 Member Portal Architecture

### Portal Configuration

```python
# dartwing_ams/portal/portal_config.py

import frappe
from frappe.utils import today
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class PortalModuleConfig:
    """Configuration for a portal module."""
    name: str
    enabled: bool = True
    icon: str = ""
    display_order: int = 0
    requires_good_standing: bool = False
    member_types: List[str] = field(default_factory=list)  # Empty = all
    custom_permissions: Dict = field(default_factory=dict)

@dataclass
class MemberPortalConfig:
    """Complete portal configuration for an association."""
    association: str
    theme: Dict = field(default_factory=dict)
    modules: List[PortalModuleConfig] = field(default_factory=list)
    features: Dict = field(default_factory=dict)

    @classmethod
    def load(cls, association: str) -> 'MemberPortalConfig':
        """Load portal configuration for association."""
        config = frappe.get_doc("Portal Configuration", {"association": association})

        return cls(
            association=association,
            theme={
                "primary_color": config.primary_color,
                "secondary_color": config.secondary_color,
                "logo": config.logo,
                "favicon": config.favicon,
                "custom_css": config.custom_css
            },
            modules=[
                PortalModuleConfig(
                    name=m.module_name,
                    enabled=m.enabled,
                    icon=m.icon,
                    display_order=m.display_order,
                    requires_good_standing=m.requires_good_standing
                )
                for m in config.modules
            ],
            features={
                "online_payments": config.enable_online_payments,
                "amenity_booking": config.enable_amenity_booking,
                "document_library": config.enable_document_library,
                "community_directory": config.enable_directory,
                "messaging": config.enable_messaging,
                "maintenance_requests": config.enable_maintenance_requests,
                "arc_submissions": config.enable_arc_submissions,
                "guest_registration": config.enable_guest_registration,
                "vehicle_registration": config.enable_vehicle_registration,
                "pet_registration": config.enable_pet_registration,
                "event_rsvp": config.enable_event_rsvp,
                "voting": config.enable_online_voting
            }
        )


class MemberPortalService:
    """Service layer for member portal operations."""

    def __init__(self, member: str):
        self.member = frappe.get_doc("Member", member)
        self.association = self.member.organization
        self.config = MemberPortalConfig.load(self.association)

    def get_dashboard_data(self) -> Dict:
        """Get member dashboard data."""
        return {
            "member": self._get_member_summary(),
            "account": self._get_account_summary(),
            "alerts": self._get_alerts(),
            "upcoming_events": self._get_upcoming_events(),
            "pending_requests": self._get_pending_requests(),
            "announcements": self._get_announcements(),
            "quick_actions": self._get_quick_actions()
        }

    def _get_member_summary(self) -> Dict:
        """Get member summary information."""
        person = frappe.get_doc("Person", self.member.person)
        primary_unit = None

        if self.member.primary_unit:
            primary_unit = frappe.get_value(
                "Unit",
                self.member.primary_unit,
                ["unit_number", "building"],
                as_dict=True
            )

        return {
            "name": person.full_name,
            "membership_number": self.member.membership_number,
            "membership_type": self.member.membership_type,
            "status": self.member.status,
            "primary_unit": primary_unit,
            "profile_photo": person.image,
            "is_board_member": self.member.is_board_member,
            "is_committee_member": self.member.is_committee_member
        }

    def _get_account_summary(self) -> Dict:
        """Get account balance and recent activity."""
        # Outstanding balance
        outstanding = frappe.db.sql("""
            SELECT COALESCE(SUM(outstanding_amount), 0)
            FROM `tabInvoice`
            WHERE member = %s AND docstatus = 1 AND outstanding_amount > 0
        """, self.member.name)[0][0]

        # Next due
        next_due = frappe.db.sql("""
            SELECT due_date, outstanding_amount
            FROM `tabInvoice`
            WHERE member = %s AND docstatus = 1 AND outstanding_amount > 0
            ORDER BY due_date
            LIMIT 1
        """, self.member.name, as_dict=True)

        # Recent payments
        recent_payments = frappe.get_all(
            "Payment",
            filters={"member": self.member.name, "docstatus": 1},
            fields=["posting_date", "amount", "payment_type"],
            order_by="posting_date desc",
            limit=3
        )

        return {
            "current_balance": outstanding,
            "next_due": next_due[0] if next_due else None,
            "autopay_enabled": self.member.autopay_enabled,
            "recent_payments": recent_payments,
            "is_delinquent": outstanding > 0 and next_due and next_due[0].due_date < today()
        }

    def _get_alerts(self) -> List[Dict]:
        """Get member-specific alerts."""
        alerts = []

        # Overdue balance
        if self._get_account_summary()["is_delinquent"]:
            alerts.append({
                "type": "warning",
                "title": "Payment Overdue",
                "message": "Your account has an overdue balance.",
                "action": {"label": "Pay Now", "url": "/portal/payments"}
            })

        # Expiring membership
        if self.member.expiry_date:
            days_to_expiry = (frappe.utils.getdate(self.member.expiry_date) -
                            frappe.utils.getdate(today())).days
            if 0 < days_to_expiry <= 30:
                alerts.append({
                    "type": "info",
                    "title": "Membership Expiring",
                    "message": f"Your membership expires in {days_to_expiry} days.",
                    "action": {"label": "Renew", "url": "/portal/membership/renew"}
                })

        # Pending ARC request action
        pending_arc = frappe.db.exists(
            "ARC Request",
            {"member": self.member.name, "status": "Additional Info Needed"}
        )
        if pending_arc:
            alerts.append({
                "type": "action",
                "title": "ARC Request Needs Attention",
                "message": "Additional information is needed for your ARC request.",
                "action": {"label": "View Request", "url": f"/portal/arc/{pending_arc}"}
            })

        # Open violation
        open_violation = frappe.get_all(
            "Violation",
            filters={
                "member": self.member.name,
                "status": ["not in", ["Resolved", "Dismissed"]]
            },
            limit=1
        )
        if open_violation:
            alerts.append({
                "type": "warning",
                "title": "Open Violation",
                "message": "You have an open violation that requires attention.",
                "action": {"label": "View Details", "url": "/portal/violations"}
            })

        return alerts

    def _get_upcoming_events(self, limit: int = 5) -> List[Dict]:
        """Get upcoming community events."""
        return frappe.get_all(
            "Event",
            filters={
                "organization": self.association,
                "event_date": [">=", today()],
                "status": "Published"
            },
            fields=["name", "title", "event_date", "start_time", "location", "image"],
            order_by="event_date",
            limit=limit
        )

    def _get_pending_requests(self) -> List[Dict]:
        """Get member's pending requests."""
        requests = []

        # Service requests
        service_requests = frappe.get_all(
            "Service Request",
            filters={
                "member": self.member.name,
                "status": ["not in", ["Closed", "Cancelled"]]
            },
            fields=["name", "title", "status", "created_date", "category"]
        )
        for sr in service_requests:
            sr["type"] = "service_request"
            requests.append(sr)

        # ARC requests
        arc_requests = frappe.get_all(
            "ARC Request",
            filters={
                "member": self.member.name,
                "status": ["not in", ["Approved", "Denied", "Withdrawn"]]
            },
            fields=["name", "title", "status", "submitted_date"]
        )
        for ar in arc_requests:
            ar["type"] = "arc_request"
            requests.append(ar)

        # Work orders
        work_orders = frappe.get_all(
            "Work Order",
            filters={
                "reported_by": self.member.name,
                "status": ["not in", ["Closed", "Cancelled"]]
            },
            fields=["name", "title", "status", "created_date", "priority"]
        )
        for wo in work_orders:
            wo["type"] = "work_order"
            requests.append(wo)

        return sorted(requests, key=lambda x: x.get("created_date") or x.get("submitted_date"), reverse=True)

    def _get_announcements(self, limit: int = 5) -> List[Dict]:
        """Get recent announcements."""
        return frappe.get_all(
            "Announcement",
            filters={
                "organization": self.association,
                "status": "Published",
                "publish_date": ["<=", today()]
            },
            fields=["name", "title", "summary", "publish_date", "priority", "category"],
            order_by="publish_date desc",
            limit=limit
        )

    def _get_quick_actions(self) -> List[Dict]:
        """Get available quick actions based on configuration."""
        actions = [
            {"id": "pay_dues", "label": "Pay Dues", "icon": "credit-card", "url": "/portal/payments"},
            {"id": "submit_request", "label": "Submit Request", "icon": "file-plus", "url": "/portal/requests/new"}
        ]

        if self.config.features.get("amenity_booking"):
            actions.append({
                "id": "book_amenity",
                "label": "Book Amenity",
                "icon": "calendar",
                "url": "/portal/amenities"
            })

        if self.config.features.get("guest_registration"):
            actions.append({
                "id": "register_guest",
                "label": "Register Guest",
                "icon": "user-plus",
                "url": "/portal/guests/new"
            })

        if self.config.features.get("arc_submissions"):
            actions.append({
                "id": "arc_request",
                "label": "ARC Request",
                "icon": "home",
                "url": "/portal/arc/new"
            })

        return actions
```

## 5.3 Service Request Management

```python
# dartwing_ams/doctype/service_request/service_request.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, now_datetime
from typing import Optional, List

class ServiceRequest(Document):
    """
    General service/support request from members.

    Fields:
    - name: Auto-generated ID (SR-XXXXX)
    - association: Link to Association (required)
    - member: Link to Member (required)
    - unit: Link to Unit

    # Request Details
    - category: Link to Request Category (required)
    - subcategory: Data
    - title: Data (required)
    - description: Long Text (required)
    - priority: Select [Low, Medium, High, Urgent]

    # Attachments
    - attachments: Attach Multiple

    # Assignment
    - assigned_to: Link to User
    - assigned_date: Datetime
    - department: Select [Management, Maintenance, Accounting, Compliance]

    # SLA
    - sla_response_due: Datetime
    - sla_resolution_due: Datetime
    - sla_response_met: Check
    - sla_resolution_met: Check

    # Resolution
    - resolution_notes: Long Text
    - resolved_date: Datetime
    - resolved_by: Link to User

    # Communication
    - communication_log: Table (Request Communication)

    # Satisfaction
    - satisfaction_rating: Rating
    - satisfaction_feedback: Text

    # Status
    - status: Select [New, In Progress, Pending Member, Pending Approval,
                      Escalated, Resolved, Closed, Cancelled]
    - created_date: Datetime
    - last_updated: Datetime
    """

    def autoname(self):
        """Generate request number."""
        self.name = frappe.model.naming.make_autoname("SR-.#####")

    def before_insert(self):
        self.created_date = now_datetime()
        self.status = "New"
        self.set_sla_deadlines()

    def validate(self):
        self.last_updated = now_datetime()

    def on_update(self):
        self.check_sla_compliance()
        self.notify_on_status_change()

    def set_sla_deadlines(self):
        """Set SLA deadlines based on category and priority."""
        category = frappe.get_doc("Request Category", self.category)

        # Get SLA hours based on priority
        sla_config = {
            "Urgent": {"response": 1, "resolution": 4},
            "High": {"response": 4, "resolution": 24},
            "Medium": {"response": 8, "resolution": 48},
            "Low": {"response": 24, "resolution": 72}
        }

        config = sla_config.get(self.priority, sla_config["Medium"])

        # Apply category multiplier if exists
        if category.sla_multiplier:
            config["response"] *= category.sla_multiplier
            config["resolution"] *= category.sla_multiplier

        now = now_datetime()
        self.sla_response_due = frappe.utils.add_to_date(now, hours=config["response"])
        self.sla_resolution_due = frappe.utils.add_to_date(now, hours=config["resolution"])

    def check_sla_compliance(self):
        """Check SLA compliance on status changes."""
        now = now_datetime()

        # Response SLA (when first assigned)
        if self.assigned_to and not self.sla_response_met:
            self.sla_response_met = self.assigned_date <= self.sla_response_due

        # Resolution SLA
        if self.status in ["Resolved", "Closed"] and not self.sla_resolution_met:
            self.sla_resolution_met = now <= self.sla_resolution_due

    def notify_on_status_change(self):
        """Send notification on status change."""
        if self.has_value_changed("status"):
            member = frappe.get_doc("Member", self.member)

            messages = {
                "In Progress": "Your request is now being worked on.",
                "Pending Member": "We need additional information from you.",
                "Resolved": "Your request has been resolved.",
                "Closed": "Your request has been closed."
            }

            if self.status in messages:
                member.send_communication(
                    subject=f"Request Update: {self.title}",
                    message=f"{messages[self.status]}\n\nRequest: {self.name}"
                )

    def assign(self, user: str, notes: str = None):
        """Assign request to staff member."""
        self.assigned_to = user
        self.assigned_date = now_datetime()
        self.status = "In Progress"

        if notes:
            self.add_communication("internal", f"Assigned to {user}: {notes}")

        self.save()

        # Notify assignee
        frappe.sendmail(
            recipients=[user],
            subject=f"Request Assigned: {self.name}",
            message=f"You have been assigned request {self.name}.\n\n"
                    f"Title: {self.title}\n"
                    f"Priority: {self.priority}"
        )

    def add_communication(
        self,
        comm_type: str,  # "member", "internal", "system"
        message: str,
        attachments: List[str] = None
    ):
        """Add communication entry to request."""
        self.append("communication_log", {
            "communication_type": comm_type,
            "message": message,
            "sent_by": frappe.session.user,
            "sent_at": now_datetime(),
            "attachments": attachments
        })
        self.save()

        # If member communication, notify member
        if comm_type == "member":
            member = frappe.get_doc("Member", self.member)
            member.send_communication(
                subject=f"Update on Request: {self.title}",
                message=message
            )

    def resolve(self, resolution_notes: str):
        """Mark request as resolved."""
        self.status = "Resolved"
        self.resolution_notes = resolution_notes
        self.resolved_date = now_datetime()
        self.resolved_by = frappe.session.user
        self.save()

        # Request satisfaction feedback
        self._request_feedback()

    def _request_feedback(self):
        """Request satisfaction feedback from member."""
        member = frappe.get_doc("Member", self.member)

        feedback_url = f"{frappe.utils.get_url()}/portal/requests/{self.name}/feedback"

        member.send_communication(
            subject=f"How was your experience? - Request {self.name}",
            message=f"Your request has been resolved. "
                    f"We'd love to hear your feedback!\n\n"
                    f"Please rate your experience: {feedback_url}"
        )

    def escalate(self, reason: str, escalate_to: str = None):
        """Escalate request."""
        self.status = "Escalated"
        self.add_communication("internal", f"Escalated: {reason}")

        if escalate_to:
            self.assign(escalate_to, f"Escalation: {reason}")

        self.save()


class RequestCategory(Document):
    """
    Service request category configuration.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association
    - category_name: Data (required)
    - description: Text
    - icon: Data

    # Routing
    - default_department: Select
    - default_assignee: Link to User
    - auto_assign: Check

    # SLA
    - sla_multiplier: Float (1.0 = standard, 0.5 = faster, 2.0 = slower)

    # Forms
    - custom_form: Link to Custom Form (for additional fields)
    - requires_unit: Check

    # Visibility
    - is_public: Check (show in member portal)
    - member_types: Table (eligible member types)

    # Status
    - status: Select [Active, Inactive]
    """
    pass
```

## 5.4 Amenity Booking System

```python
# dartwing_ams/doctype/amenity_booking/amenity_booking.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, now_datetime, add_days, time_diff_in_hours
from typing import List, Optional
from datetime import datetime, time

class AmenityBooking(Document):
    """
    Amenity/facility booking record.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - common_area: Link to Common Area (required)
    - member: Link to Member (required)
    - unit: Link to Unit

    # Booking Details
    - booking_date: Date (required)
    - start_time: Time (required)
    - end_time: Time (required)
    - duration_hours: Float (computed)

    # Purpose
    - purpose: Data
    - event_name: Data
    - is_private_event: Check

    # Guests
    - expected_guests: Int
    - guest_list: Table (Booking Guest)

    # Fees
    - booking_fee: Currency
    - deposit_amount: Currency
    - deposit_paid: Check
    - deposit_returned: Check
    - deposit_forfeited: Check
    - forfeiture_reason: Text

    # Requirements
    - setup_requested: Check
    - setup_notes: Text
    - cleanup_included: Check
    - catering_allowed: Check
    - alcohol_allowed: Check

    # Approval
    - requires_approval: Check
    - approved_by: Link to User
    - approved_date: Datetime
    - denial_reason: Text

    # Check-in/out
    - checked_in: Check
    - check_in_time: Datetime
    - checked_out: Check
    - check_out_time: Datetime
    - condition_notes: Text

    # Status
    - status: Select [Pending, Confirmed, Denied, Checked In, Completed,
                      Cancelled, No Show]
    - cancellation_date: Datetime
    - cancellation_reason: Text
    - cancelled_by: Link to User
    """

    def validate(self):
        self.validate_booking_times()
        self.validate_availability()
        self.validate_member_limits()
        self.calculate_fees()
        self.calculate_duration()

    def validate_booking_times(self):
        """Validate booking time constraints."""
        common_area = frappe.get_doc("Common Area", self.common_area)

        # Check operating hours
        day_of_week = frappe.utils.get_datetime(self.booking_date).strftime("%A")
        hours = frappe.get_value(
            "Operating Hours",
            {"parent": self.common_area, "day_of_week": day_of_week},
            ["open_time", "close_time"],
            as_dict=True
        )

        if not hours:
            frappe.throw(f"{common_area.area_name} is closed on {day_of_week}")

        if self.start_time < hours.open_time:
            frappe.throw(f"Booking cannot start before {hours.open_time}")

        if self.end_time > hours.close_time:
            frappe.throw(f"Booking cannot end after {hours.close_time}")

        # Check maximum duration
        if common_area.max_booking_hours:
            duration = time_diff_in_hours(self.end_time, self.start_time)
            if duration > common_area.max_booking_hours:
                frappe.throw(
                    f"Maximum booking duration is {common_area.max_booking_hours} hours"
                )

        # Check advance booking limit
        if common_area.booking_advance_days:
            max_date = add_days(today(), common_area.booking_advance_days)
            if frappe.utils.getdate(self.booking_date) > frappe.utils.getdate(max_date):
                frappe.throw(
                    f"Cannot book more than {common_area.booking_advance_days} days in advance"
                )

    def validate_availability(self):
        """Check for conflicting bookings."""
        conflicts = frappe.get_all(
            "Amenity Booking",
            filters={
                "common_area": self.common_area,
                "booking_date": self.booking_date,
                "status": ["in", ["Pending", "Confirmed", "Checked In"]],
                "name": ["!=", self.name or ""],
                "start_time": ["<", self.end_time],
                "end_time": [">", self.start_time]
            }
        )

        if conflicts:
            frappe.throw("This time slot is already booked")

    def validate_member_limits(self):
        """Check member booking limits."""
        common_area = frappe.get_doc("Common Area", self.common_area)

        if common_area.max_bookings_per_member:
            # Count bookings this week/month
            period_start = frappe.utils.get_first_day(self.booking_date)
            period_end = frappe.utils.get_last_day(self.booking_date)

            existing_bookings = frappe.db.count(
                "Amenity Booking",
                {
                    "common_area": self.common_area,
                    "member": self.member,
                    "booking_date": ["between", [period_start, period_end]],
                    "status": ["not in", ["Cancelled", "Denied"]],
                    "name": ["!=", self.name or ""]
                }
            )

            if existing_bookings >= common_area.max_bookings_per_member:
                frappe.throw(
                    f"You have reached the maximum of {common_area.max_bookings_per_member} "
                    f"bookings per month for this amenity"
                )

    def calculate_fees(self):
        """Calculate booking fees."""
        common_area = frappe.get_doc("Common Area", self.common_area)

        self.booking_fee = common_area.booking_fee or 0
        self.deposit_amount = common_area.deposit_required or 0

        # Check if approval required
        self.requires_approval = common_area.requires_approval

    def calculate_duration(self):
        """Calculate booking duration in hours."""
        self.duration_hours = time_diff_in_hours(self.end_time, self.start_time)

    def confirm(self):
        """Confirm the booking."""
        if self.requires_approval:
            frappe.throw("This booking requires approval")

        self.status = "Confirmed"
        self.save()

        # Send confirmation
        self._send_confirmation()

    def approve(self, approved_by: str = None):
        """Approve pending booking."""
        self.status = "Confirmed"
        self.approved_by = approved_by or frappe.session.user
        self.approved_date = now_datetime()
        self.save()

        self._send_confirmation()

    def deny(self, reason: str):
        """Deny pending booking."""
        self.status = "Denied"
        self.denial_reason = reason
        self.save()

        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"Booking Denied - {self.common_area}",
            message=f"Your booking request has been denied.\n\nReason: {reason}"
        )

    def check_in(self, condition_notes: str = None):
        """Check in for booking."""
        self.status = "Checked In"
        self.checked_in = True
        self.check_in_time = now_datetime()
        self.condition_notes = condition_notes
        self.save()

    def check_out(self, condition_notes: str = None, issues: List[str] = None):
        """Check out from booking."""
        self.status = "Completed"
        self.checked_out = True
        self.check_out_time = now_datetime()

        if condition_notes:
            self.condition_notes = (self.condition_notes or "") + f"\n\nCheck-out: {condition_notes}"

        # Handle deposit
        if issues:
            self.deposit_forfeited = True
            self.forfeiture_reason = ", ".join(issues)
        else:
            self.deposit_returned = True

        self.save()

    def cancel(self, reason: str):
        """Cancel booking."""
        self.status = "Cancelled"
        self.cancellation_date = now_datetime()
        self.cancellation_reason = reason
        self.cancelled_by = frappe.session.user
        self.save()

        # Check refund policy
        common_area = frappe.get_doc("Common Area", self.common_area)
        # Refund logic would go here

    def _send_confirmation(self):
        """Send booking confirmation."""
        member = frappe.get_doc("Member", self.member)
        common_area = frappe.get_doc("Common Area", self.common_area)

        member.send_communication(
            subject=f"Booking Confirmed - {common_area.area_name}",
            message=f"Your booking has been confirmed!\n\n"
                    f"Amenity: {common_area.area_name}\n"
                    f"Date: {self.booking_date}\n"
                    f"Time: {self.start_time} - {self.end_time}\n\n"
                    f"Booking ID: {self.name}"
        )


class AmenityBookingService:
    """Service for amenity booking operations."""

    def __init__(self, association: str):
        self.association = association

    def get_availability(
        self,
        common_area: str,
        date: str
    ) -> List[dict]:
        """Get available time slots for a date."""
        area = frappe.get_doc("Common Area", common_area)
        day_of_week = frappe.utils.get_datetime(date).strftime("%A")

        # Get operating hours
        hours = frappe.get_value(
            "Operating Hours",
            {"parent": common_area, "day_of_week": day_of_week},
            ["open_time", "close_time"],
            as_dict=True
        )

        if not hours:
            return []

        # Get existing bookings
        bookings = frappe.get_all(
            "Amenity Booking",
            filters={
                "common_area": common_area,
                "booking_date": date,
                "status": ["in", ["Pending", "Confirmed", "Checked In"]]
            },
            fields=["start_time", "end_time"]
        )

        # Generate available slots (1-hour increments)
        slots = []
        current_time = hours.open_time

        while current_time < hours.close_time:
            end_time = frappe.utils.add_to_date(
                f"{date} {current_time}",
                hours=1
            ).time()

            # Check if slot is available
            is_booked = any(
                b.start_time < end_time and b.end_time > current_time
                for b in bookings
            )

            slots.append({
                "start_time": str(current_time),
                "end_time": str(end_time),
                "available": not is_booked
            })

            current_time = end_time

        return slots

    def get_member_bookings(
        self,
        member: str,
        include_past: bool = False
    ) -> List[dict]:
        """Get member's bookings."""
        filters = {
            "member": member,
            "status": ["not in", ["Cancelled", "Denied"]]
        }

        if not include_past:
            filters["booking_date"] = [">=", today()]

        return frappe.get_all(
            "Amenity Booking",
            filters=filters,
            fields=["name", "common_area", "booking_date", "start_time",
                    "end_time", "status", "purpose"],
            order_by="booking_date, start_time"
        )
```

## 5.5 Guest & Access Management

```python
# dartwing_ams/doctype/guest_pass/guest_pass.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, now_datetime, add_days
import secrets
import qrcode
import io
import base64

class GuestPass(Document):
    """
    Guest access pass for visitors.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - member: Link to Member (required) - host
    - unit: Link to Unit

    # Guest Details
    - guest_name: Data (required)
    - guest_email: Data
    - guest_phone: Data
    - guest_company: Data
    - guest_photo: Attach

    # Visit Details
    - visit_type: Select [One-Time, Recurring, Contractor, Delivery]
    - purpose: Data

    # Validity
    - valid_from: Datetime (required)
    - valid_until: Datetime (required)
    - recurring_pattern: Select [Daily, Weekdays, Weekly]
    - recurring_end_date: Date

    # Access
    - access_areas: Table (Guest Access Area)
    - parking_pass_issued: Check
    - parking_spot: Data

    # Verification
    - pass_code: Data (auto-generated)
    - qr_code: Attach
    - pin_code: Data (4-digit)

    # Check-in/out
    - checked_in: Check
    - check_in_time: Datetime
    - check_in_method: Select [QR Scan, PIN, Manual]
    - checked_out: Check
    - check_out_time: Datetime

    # Verification
    - id_verified: Check
    - verified_by: Link to User

    # Vehicle
    - has_vehicle: Check
    - vehicle_make: Data
    - vehicle_model: Data
    - vehicle_color: Data
    - license_plate: Data

    # Status
    - status: Select [Active, Used, Expired, Revoked]
    - revoked_reason: Text
    """

    def before_insert(self):
        self.generate_pass_codes()
        self.generate_qr_code()

    def validate(self):
        self.validate_dates()
        self.validate_member_guest_limits()

    def generate_pass_codes(self):
        """Generate unique pass codes."""
        self.pass_code = secrets.token_urlsafe(16)
        self.pin_code = str(secrets.randbelow(10000)).zfill(4)

    def generate_qr_code(self):
        """Generate QR code for pass."""
        qr_data = f"GUEST:{self.association}:{self.pass_code}"

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        # Save as file
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"guest_pass_qr_{self.name}.png",
            "content": buffer.getvalue(),
            "attached_to_doctype": "Guest Pass",
            "attached_to_name": self.name
        })
        file_doc.insert(ignore_permissions=True)

        self.qr_code = file_doc.file_url

    def validate_dates(self):
        """Validate pass validity dates."""
        if self.valid_until <= self.valid_from:
            frappe.throw("Valid until must be after valid from")

        # Check maximum duration
        max_days = frappe.get_value(
            "Association",
            self.association,
            "max_guest_pass_days"
        ) or 7

        duration = (frappe.utils.get_datetime(self.valid_until) -
                   frappe.utils.get_datetime(self.valid_from)).days

        if duration > max_days:
            frappe.throw(f"Guest pass cannot exceed {max_days} days")

    def validate_member_guest_limits(self):
        """Check member's guest pass limits."""
        config = frappe.get_value(
            "Association",
            self.association,
            ["max_active_guest_passes", "max_monthly_guest_passes"],
            as_dict=True
        )

        # Active passes
        if config.max_active_guest_passes:
            active = frappe.db.count(
                "Guest Pass",
                {
                    "member": self.member,
                    "status": "Active",
                    "name": ["!=", self.name or ""]
                }
            )
            if active >= config.max_active_guest_passes:
                frappe.throw(
                    f"Maximum of {config.max_active_guest_passes} active guest passes allowed"
                )

        # Monthly limit
        if config.max_monthly_guest_passes:
            month_start = frappe.utils.get_first_day(today())
            month_end = frappe.utils.get_last_day(today())

            monthly = frappe.db.count(
                "Guest Pass",
                {
                    "member": self.member,
                    "creation": ["between", [month_start, month_end]],
                    "name": ["!=", self.name or ""]
                }
            )
            if monthly >= config.max_monthly_guest_passes:
                frappe.throw(
                    f"Maximum of {config.max_monthly_guest_passes} guest passes per month"
                )

    def check_in(self, method: str = "Manual", verified_by: str = None):
        """Check in guest."""
        now = now_datetime()

        # Validate pass is active
        if self.status != "Active":
            frappe.throw("Guest pass is not active")

        if now < frappe.utils.get_datetime(self.valid_from):
            frappe.throw("Guest pass is not yet valid")

        if now > frappe.utils.get_datetime(self.valid_until):
            self.status = "Expired"
            self.save()
            frappe.throw("Guest pass has expired")

        self.checked_in = True
        self.check_in_time = now
        self.check_in_method = method

        if verified_by:
            self.id_verified = True
            self.verified_by = verified_by

        self.save()

        # Notify host
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject=f"Guest Arrived: {self.guest_name}",
            message=f"Your guest {self.guest_name} has checked in."
        )

    def check_out(self):
        """Check out guest."""
        self.checked_out = True
        self.check_out_time = now_datetime()

        if self.visit_type == "One-Time":
            self.status = "Used"

        self.save()

    def revoke(self, reason: str):
        """Revoke guest pass."""
        self.status = "Revoked"
        self.revoked_reason = reason
        self.save()

    def send_to_guest(self):
        """Send pass details to guest via email."""
        if not self.guest_email:
            frappe.throw("Guest email is required")

        host = frappe.get_doc("Member", self.member)
        host_person = frappe.get_doc("Person", host.person)

        frappe.sendmail(
            recipients=[self.guest_email],
            subject=f"Your Guest Pass for {self.association}",
            message=frappe.render_template(
                "templates/guest_pass_email.html",
                {
                    "pass": self,
                    "host_name": host_person.full_name,
                    "qr_code": self.qr_code,
                    "pin_code": self.pin_code
                }
            )
        )


class AccessCard(Document):
    """
    Physical/digital access card management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - member: Link to Member (required)
    - unit: Link to Unit

    # Card Details
    - card_type: Select [Key Fob, Access Card, Mobile Credential]
    - card_number: Data (required)
    - facility_code: Data

    # Access Levels
    - access_profile: Link to Access Profile
    - custom_access_areas: Table (Access Area Assignment)

    # Validity
    - issued_date: Date
    - expiry_date: Date
    - activation_date: Date

    # Status
    - status: Select [Active, Suspended, Lost, Stolen, Returned, Expired]
    - suspension_reason: Text
    - suspension_date: Date

    # Tracking
    - last_used: Datetime
    - last_used_location: Data
    - use_count: Int
    """

    def suspend(self, reason: str):
        """Suspend access card."""
        self.status = "Suspended"
        self.suspension_reason = reason
        self.suspension_date = today()
        self.save()

        # Sync with access control system
        self._sync_to_access_control()

    def activate(self):
        """Activate access card."""
        self.status = "Active"
        self.activation_date = today()
        self.save()

        self._sync_to_access_control()

    def report_lost(self):
        """Report card as lost."""
        self.status = "Lost"
        self.save()

        # Immediately deactivate in access system
        self._sync_to_access_control()

        # Notify member about replacement
        member = frappe.get_doc("Member", self.member)
        member.send_communication(
            subject="Access Card Reported Lost",
            message="Your access card has been deactivated. "
                    "Please contact the office for a replacement."
        )

    def _sync_to_access_control(self):
        """Sync card status to physical access control system."""
        frappe.enqueue(
            "dartwing_ams.integrations.access_control.sync_card",
            card=self.name,
            queue="short"
        )
```

## 5.6 Communication & Notification System

```python
# dartwing_ams/communications/notification_service.py

import frappe
from frappe.utils import today, now_datetime
from typing import List, Dict, Optional
from enum import Enum

class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class NotificationService:
    """Unified notification service for all communication channels."""

    def __init__(self, association: str):
        self.association = association
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load notification configuration."""
        return frappe.get_doc(
            "Communication Settings",
            {"association": self.association}
        )

    def send_notification(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        channels: List[NotificationChannel] = None,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        category: str = None,
        data: Dict = None
    ) -> Dict:
        """Send notification through specified channels."""
        if not channels:
            channels = [NotificationChannel.EMAIL, NotificationChannel.IN_APP]

        results = {}

        for recipient in recipients:
            member = frappe.get_doc("Member", recipient)
            person = frappe.get_doc("Person", member.person)

            # Check member preferences
            prefs = self._get_member_preferences(recipient)

            for channel in channels:
                # Skip if member opted out of this channel/category
                if not self._should_send(prefs, channel, category, priority):
                    continue

                if channel == NotificationChannel.EMAIL:
                    result = self._send_email(
                        person.email or member.preferred_email,
                        subject,
                        message,
                        priority
                    )

                elif channel == NotificationChannel.SMS:
                    result = self._send_sms(
                        person.mobile or member.preferred_phone,
                        message,
                        priority
                    )

                elif channel == NotificationChannel.PUSH:
                    result = self._send_push(
                        recipient,
                        subject,
                        message,
                        data
                    )

                elif channel == NotificationChannel.IN_APP:
                    result = self._create_in_app_notification(
                        recipient,
                        subject,
                        message,
                        category,
                        data
                    )

                results[f"{recipient}_{channel.value}"] = result

        return results

    def _get_member_preferences(self, member: str) -> Dict:
        """Get member's notification preferences."""
        prefs = frappe.get_all(
            "Communication Preference",
            filters={"parent": member},
            fields=["category", "email_enabled", "sms_enabled",
                    "push_enabled", "quiet_hours_start", "quiet_hours_end"]
        )
        return {p.category: p for p in prefs}

    def _should_send(
        self,
        prefs: Dict,
        channel: NotificationChannel,
        category: str,
        priority: NotificationPriority
    ) -> bool:
        """Check if notification should be sent based on preferences."""
        # Always send urgent notifications
        if priority == NotificationPriority.URGENT:
            return True

        # Check category preferences
        if category and category in prefs:
            pref = prefs[category]

            if channel == NotificationChannel.EMAIL and not pref.email_enabled:
                return False
            if channel == NotificationChannel.SMS and not pref.sms_enabled:
                return False
            if channel == NotificationChannel.PUSH and not pref.push_enabled:
                return False

            # Check quiet hours
            if pref.quiet_hours_start and pref.quiet_hours_end:
                now = frappe.utils.now_datetime().time()
                if pref.quiet_hours_start <= now <= pref.quiet_hours_end:
                    return priority == NotificationPriority.HIGH

        return True

    def _send_email(
        self,
        email: str,
        subject: str,
        message: str,
        priority: NotificationPriority
    ) -> Dict:
        """Send email notification."""
        if not email:
            return {"success": False, "error": "No email address"}

        try:
            frappe.sendmail(
                recipients=[email],
                subject=subject,
                message=message,
                now=priority in [NotificationPriority.HIGH, NotificationPriority.URGENT]
            )
            return {"success": True, "channel": "email"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _send_sms(
        self,
        phone: str,
        message: str,
        priority: NotificationPriority
    ) -> Dict:
        """Send SMS notification."""
        if not phone:
            return {"success": False, "error": "No phone number"}

        # Truncate message for SMS
        sms_message = message[:160] if len(message) > 160 else message

        try:
            from dartwing_core.communications.sms import send_sms
            send_sms(phone, sms_message)
            return {"success": True, "channel": "sms"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _send_push(
        self,
        member: str,
        title: str,
        body: str,
        data: Dict = None
    ) -> Dict:
        """Send push notification."""
        # Get member's device tokens
        devices = frappe.get_all(
            "Member Device",
            filters={"member": member, "push_enabled": True},
            fields=["device_token", "platform"]
        )

        if not devices:
            return {"success": False, "error": "No registered devices"}

        try:
            from dartwing_core.communications.push import send_push_notification

            for device in devices:
                send_push_notification(
                    token=device.device_token,
                    title=title,
                    body=body,
                    data=data,
                    platform=device.platform
                )

            return {"success": True, "channel": "push", "devices": len(devices)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_in_app_notification(
        self,
        member: str,
        title: str,
        message: str,
        category: str = None,
        data: Dict = None
    ) -> Dict:
        """Create in-app notification."""
        try:
            notif = frappe.get_doc({
                "doctype": "In App Notification",
                "member": member,
                "title": title,
                "message": message,
                "category": category,
                "data": frappe.as_json(data) if data else None,
                "status": "Unread",
                "created_at": now_datetime()
            })
            notif.insert(ignore_permissions=True)

            return {"success": True, "channel": "in_app", "notification": notif.name}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_broadcast(
        self,
        subject: str,
        message: str,
        target_audience: str = "all",
        filters: Dict = None,
        channels: List[NotificationChannel] = None,
        schedule_time: str = None
    ) -> str:
        """Send broadcast message to multiple members."""
        # Create broadcast record
        broadcast = frappe.get_doc({
            "doctype": "Broadcast Message",
            "association": self.association,
            "subject": subject,
            "message": message,
            "target_audience": target_audience,
            "audience_filters": frappe.as_json(filters) if filters else None,
            "channels": ",".join([c.value for c in (channels or [])]),
            "scheduled_time": schedule_time,
            "status": "Scheduled" if schedule_time else "Sending"
        })
        broadcast.insert()

        if not schedule_time:
            # Send immediately
            frappe.enqueue(
                "dartwing_ams.communications.notification_service.process_broadcast",
                broadcast=broadcast.name,
                queue="long"
            )

        return broadcast.name

    def send_emergency_alert(
        self,
        title: str,
        message: str,
        severity: str = "high",
        target_buildings: List[str] = None,
        target_units: List[str] = None
    ) -> str:
        """Send emergency alert to all affected members."""
        # Create emergency alert record
        alert = frappe.get_doc({
            "doctype": "Emergency Alert",
            "association": self.association,
            "title": title,
            "message": message,
            "severity": severity,
            "target_buildings": target_buildings,
            "target_units": target_units,
            "sent_at": now_datetime(),
            "status": "Sending"
        })
        alert.insert()

        # Get recipients
        recipients = self._get_emergency_recipients(target_buildings, target_units)

        # Send through all channels immediately
        channels = [
            NotificationChannel.PUSH,
            NotificationChannel.SMS,
            NotificationChannel.EMAIL,
            NotificationChannel.IN_APP
        ]

        self.send_notification(
            recipients=recipients,
            subject=f"🚨 EMERGENCY: {title}",
            message=message,
            channels=channels,
            priority=NotificationPriority.URGENT,
            category="emergency"
        )

        alert.status = "Sent"
        alert.recipient_count = len(recipients)
        alert.save()

        return alert.name

    def _get_emergency_recipients(
        self,
        buildings: List[str] = None,
        units: List[str] = None
    ) -> List[str]:
        """Get all members for emergency notification."""
        filters = {"organization": self.association, "status": "Active"}

        if units:
            # Get members in specific units
            return frappe.db.sql("""
                SELECT DISTINCT um.member
                FROM `tabUnit Member` um
                WHERE um.parent IN %s
                AND um.status = 'Active'
            """, (units,), pluck="member")

        elif buildings:
            # Get members in specific buildings
            return frappe.db.sql("""
                SELECT DISTINCT um.member
                FROM `tabUnit Member` um
                JOIN `tabUnit` u ON u.name = um.parent
                WHERE u.building IN %s
                AND um.status = 'Active'
            """, (buildings,), pluck="member")

        else:
            # All members
            return frappe.get_all("Member", filters=filters, pluck="name")


def process_broadcast(broadcast: str):
    """Process a broadcast message (called async)."""
    doc = frappe.get_doc("Broadcast Message", broadcast)
    service = NotificationService(doc.association)

    # Get recipients based on audience
    recipients = _get_broadcast_recipients(doc)

    channels = [NotificationChannel(c) for c in doc.channels.split(",")]

    # Send to all recipients
    results = service.send_notification(
        recipients=recipients,
        subject=doc.subject,
        message=doc.message,
        channels=channels,
        priority=NotificationPriority.NORMAL
    )

    # Update broadcast status
    doc.status = "Sent"
    doc.sent_at = now_datetime()
    doc.recipient_count = len(recipients)
    doc.save()


def _get_broadcast_recipients(broadcast) -> List[str]:
    """Get recipients for broadcast based on audience settings."""
    filters = {"organization": broadcast.association, "status": "Active"}

    if broadcast.target_audience == "all":
        return frappe.get_all("Member", filters=filters, pluck="name")

    elif broadcast.target_audience == "owners":
        return frappe.db.sql("""
            SELECT DISTINCT um.member
            FROM `tabUnit Member` um
            WHERE um.relationship = 'Owner'
            AND um.status = 'Active'
        """, pluck="member")

    elif broadcast.target_audience == "board":
        return frappe.get_all(
            "Board Position",
            filters={"association": broadcast.association, "status": "Active"},
            pluck="member"
        )

    elif broadcast.target_audience == "custom" and broadcast.audience_filters:
        filters.update(frappe.parse_json(broadcast.audience_filters))
        return frappe.get_all("Member", filters=filters, pluck="name")

    return []
```

---

_End of Section 5: Member Services & Portal Architecture_

**Next Section:** Section 6 - Operations & Maintenance Architecture

# Section 6: Operations & Maintenance Architecture

## 6.1 Operations System Overview

The Dartwing AMS operations module manages all aspects of property maintenance, vendor relationships, asset tracking, and preventive maintenance scheduling.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OPERATIONS & MAINTENANCE ARCHITECTURE                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     WORK ORDER MANAGEMENT                            │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Request    │  │    Triage    │  │  Assignment  │              │    │
│  │  │   Intake     │  │   & Priority │  │   & Dispatch │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Execution  │  │    Cost      │  │   Completion │              │    │
│  │  │   Tracking   │  │   Tracking   │  │   & Review   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     PREVENTIVE MAINTENANCE                           │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │     PM       │  │   Schedule   │  │   Auto Work  │              │    │
│  │  │   Templates  │  │   Generator  │  │    Order     │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │  Compliance  │  │   History    │                                │    │
│  │  │   Tracking   │  │   & Trends   │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     VENDOR MANAGEMENT                                │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │   Vendor     │  │   Contract   │  │   Insurance  │              │    │
│  │  │   Registry   │  │   Management │  │   Tracking   │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │ Performance  │  │    Bid       │                                │    │
│  │  │   Scoring    │  │  Management  │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     ASSET MANAGEMENT                                 │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Asset     │  │  Lifecycle   │  │  Depreciation│              │    │
│  │  │   Registry   │  │   Tracking   │  │   & Value    │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │  Inspection  │  │  Replacement │                                │    │
│  │  │   Schedules  │  │   Planning   │                                │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Vendor Management

### Vendor DocType

```python
# dartwing_ams/doctype/vendor/vendor.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, getdate
from typing import List, Dict, Optional

class Vendor(Document):
    """
    Vendor/contractor management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association
    - vendor_name: Data (required)
    - vendor_type: Select [Contractor, Service Provider, Supplier, Consultant]

    # Contact
    - primary_contact: Data
    - email: Data
    - phone: Data
    - website: Data

    # Address
    - address_line_1: Data
    - address_line_2: Data
    - city: Data
    - state: Data
    - postal_code: Data

    # Business Details
    - tax_id: Data
    - business_license: Data
    - license_expiry: Date

    # Service Categories
    - service_categories: Table (Vendor Service Category)
    - primary_category: Link to Work Order Category

    # Insurance
    - general_liability: Currency
    - general_liability_expiry: Date
    - workers_comp: Currency
    - workers_comp_expiry: Date
    - auto_insurance_expiry: Date
    - insurance_certificate: Attach

    # Compliance
    - w9_on_file: Check
    - w9_document: Attach
    - background_check_completed: Check
    - background_check_date: Date

    # Financial
    - payment_terms: Select [Net 15, Net 30, Net 45, Net 60, Upon Completion]
    - default_hourly_rate: Currency
    - requires_po: Check
    - spending_limit: Currency

    # Performance
    - performance_score: Float (0-5)
    - total_work_orders: Int
    - on_time_percentage: Percent
    - quality_score: Float
    - response_time_avg_hours: Float

    # Status
    - status: Select [Active, Inactive, Suspended, Blacklisted]
    - suspension_reason: Text
    - blacklist_reason: Text

    # Child Tables
    - contacts: Table (Vendor Contact)
    - notes: Table (Vendor Note)
    """

    def validate(self):
        self.validate_insurance()
        self.validate_compliance()

    def validate_insurance(self):
        """Check insurance expiration warnings."""
        if self.general_liability_expiry:
            days_to_expiry = (getdate(self.general_liability_expiry) - getdate(today())).days
            if days_to_expiry < 0:
                frappe.throw("General liability insurance has expired")
            elif days_to_expiry < 30:
                frappe.msgprint(f"General liability insurance expires in {days_to_expiry} days")

        if self.workers_comp_expiry:
            days_to_expiry = (getdate(self.workers_comp_expiry) - getdate(today())).days
            if days_to_expiry < 0:
                frappe.throw("Workers compensation insurance has expired")
            elif days_to_expiry < 30:
                frappe.msgprint(f"Workers comp insurance expires in {days_to_expiry} days")

    def validate_compliance(self):
        """Check compliance requirements."""
        if self.status == "Active":
            if not self.w9_on_file:
                frappe.msgprint("W-9 not on file for active vendor")

    def update_performance_score(self):
        """Recalculate vendor performance score."""
        # Get completed work orders
        work_orders = frappe.get_all(
            "Work Order",
            filters={
                "assigned_to": self.name,
                "status": ["in", ["Completed", "Closed"]]
            },
            fields=["name", "sla_resolution_met", "member_rating",
                    "scheduled_date", "work_completed", "created_date"]
        )

        if not work_orders:
            return

        self.total_work_orders = len(work_orders)

        # On-time percentage
        on_time = sum(1 for wo in work_orders if wo.sla_resolution_met)
        self.on_time_percentage = (on_time / len(work_orders)) * 100

        # Quality score (average rating)
        ratings = [wo.member_rating for wo in work_orders if wo.member_rating]
        self.quality_score = sum(ratings) / len(ratings) if ratings else 0

        # Response time average
        response_times = []
        for wo in work_orders:
            if wo.scheduled_date and wo.created_date:
                diff = (getdate(wo.scheduled_date) - getdate(wo.created_date)).days * 24
                response_times.append(diff)

        self.response_time_avg_hours = (
            sum(response_times) / len(response_times) if response_times else 0
        )

        # Overall performance score (weighted average)
        self.performance_score = (
            (self.on_time_percentage / 100 * 2) +
            (self.quality_score) +
            (min(48 / max(self.response_time_avg_hours, 1), 2))  # Faster = higher score
        ) / 3 * 5  # Scale to 0-5

        self.save()

    def get_active_contracts(self) -> List[dict]:
        """Get all active contracts with this vendor."""
        return frappe.get_all(
            "Vendor Contract",
            filters={
                "vendor": self.name,
                "status": "Active"
            },
            fields=["name", "contract_type", "start_date", "end_date",
                    "contract_value", "remaining_value"]
        )

    def get_pending_work_orders(self) -> List[dict]:
        """Get pending work orders assigned to this vendor."""
        return frappe.get_all(
            "Work Order",
            filters={
                "assigned_to": self.name,
                "status": ["not in", ["Completed", "Closed", "Cancelled"]]
            },
            fields=["name", "title", "priority", "status", "due_date"]
        )

    def suspend(self, reason: str):
        """Suspend vendor."""
        self.status = "Suspended"
        self.suspension_reason = reason
        self.save()

        # Reassign pending work orders
        pending = self.get_pending_work_orders()
        if pending:
            frappe.msgprint(
                f"{len(pending)} work orders need to be reassigned"
            )

    def blacklist(self, reason: str):
        """Blacklist vendor."""
        self.status = "Blacklisted"
        self.blacklist_reason = reason
        self.save()

        # Terminate active contracts
        contracts = self.get_active_contracts()
        for contract in contracts:
            frappe.db.set_value(
                "Vendor Contract",
                contract.name,
                {"status": "Terminated", "termination_reason": "Vendor blacklisted"}
            )


class VendorContract(Document):
    """
    Vendor contract management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - vendor: Link to Vendor (required)
    - contract_type: Select [Service Agreement, Maintenance Contract,
                             Project Contract, Blanket PO]
    - title: Data (required)
    - description: Long Text

    # Dates
    - start_date: Date (required)
    - end_date: Date (required)
    - auto_renew: Check
    - renewal_notice_days: Int

    # Financial
    - contract_value: Currency
    - payment_schedule: Select [Monthly, Quarterly, Annual, Milestone, Upon Completion]
    - remaining_value: Currency (computed)

    # Scope
    - scope_of_work: Long Text
    - deliverables: Table (Contract Deliverable)
    - service_areas: Table (Contract Service Area)

    # Terms
    - payment_terms: Select
    - termination_notice_days: Int
    - penalty_clause: Text

    # Documents
    - contract_document: Attach
    - amendments: Table (Contract Amendment)

    # Insurance Requirements
    - min_general_liability: Currency
    - min_workers_comp: Currency

    # Performance
    - sla_requirements: Table (Contract SLA)
    - performance_reviews: Table (Contract Review)

    # Status
    - status: Select [Draft, Pending Approval, Active, Expired, Terminated, Renewed]
    - termination_date: Date
    - termination_reason: Text
    """

    def validate(self):
        self.validate_dates()
        self.validate_vendor_insurance()
        self.calculate_remaining_value()

    def validate_dates(self):
        """Validate contract dates."""
        if self.end_date <= self.start_date:
            frappe.throw("End date must be after start date")

    def validate_vendor_insurance(self):
        """Validate vendor meets insurance requirements."""
        vendor = frappe.get_doc("Vendor", self.vendor)

        if self.min_general_liability:
            if not vendor.general_liability or vendor.general_liability < self.min_general_liability:
                frappe.throw(
                    f"Vendor's general liability ({vendor.general_liability}) "
                    f"is below required minimum ({self.min_general_liability})"
                )

        if self.min_workers_comp:
            if not vendor.workers_comp or vendor.workers_comp < self.min_workers_comp:
                frappe.throw(
                    f"Vendor's workers comp ({vendor.workers_comp}) "
                    f"is below required minimum ({self.min_workers_comp})"
                )

    def calculate_remaining_value(self):
        """Calculate remaining contract value."""
        spent = frappe.db.sql("""
            SELECT COALESCE(SUM(actual_cost), 0)
            FROM `tabWork Order`
            WHERE linked_contract = %s
            AND docstatus = 1
        """, self.name)[0][0]

        self.remaining_value = (self.contract_value or 0) - spent

    def check_renewal(self):
        """Check if contract needs renewal action."""
        if not self.auto_renew:
            return

        days_to_end = (getdate(self.end_date) - getdate(today())).days

        if days_to_end <= (self.renewal_notice_days or 30):
            # Create renewal reminder
            frappe.get_doc({
                "doctype": "Contract Renewal Reminder",
                "contract": self.name,
                "vendor": self.vendor,
                "end_date": self.end_date,
                "status": "Pending"
            }).insert(ignore_permissions=True)
```

## 6.3 Preventive Maintenance System

```python
# dartwing_ams/maintenance/preventive_maintenance.py

import frappe
from frappe.utils import today, add_days, add_months, getdate
from typing import List, Dict, Optional
from datetime import date
from enum import Enum

class PMFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi-annual"
    ANNUAL = "annual"
    CUSTOM = "custom"

class PMSchedule(frappe.model.document.Document):
    """
    Preventive maintenance schedule template.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - schedule_name: Data (required)
    - description: Text

    # Target
    - target_type: Select [Asset, Common Area, Building, System]
    - asset: Link to Asset
    - common_area: Link to Common Area
    - building: Link to Building
    - system_type: Data

    # Frequency
    - frequency: Select [Daily, Weekly, Bi-Weekly, Monthly, Quarterly,
                         Semi-Annual, Annual, Custom]
    - custom_interval_days: Int
    - preferred_day: Select [Monday..Sunday]
    - preferred_week: Select [First, Second, Third, Fourth, Last]

    # Task Details
    - category: Link to Work Order Category
    - priority: Select [Low, Medium, High]
    - estimated_duration_hours: Float
    - estimated_cost: Currency

    # Assignment
    - assigned_vendor: Link to Vendor
    - assigned_staff: Link to Member
    - requires_specialist: Check
    - specialist_type: Data

    # Checklist
    - checklist_items: Table (PM Checklist Item)
    - requires_photos: Check
    - requires_readings: Check

    # Compliance
    - is_regulatory: Check
    - regulation_reference: Data
    - compliance_due_days: Int

    # Notifications
    - notify_before_days: Int
    - notify_on_completion: Check
    - notification_recipients: Table (PM Notification Recipient)

    # Status
    - status: Select [Active, Paused, Archived]
    - last_completed: Date
    - next_due: Date
    """

    def validate(self):
        self.calculate_next_due()

    def calculate_next_due(self):
        """Calculate next due date based on frequency."""
        base_date = self.last_completed or today()

        frequency_days = {
            "daily": 1,
            "weekly": 7,
            "bi-weekly": 14,
            "monthly": 30,
            "quarterly": 90,
            "semi-annual": 180,
            "annual": 365
        }

        if self.frequency == "custom" and self.custom_interval_days:
            days = self.custom_interval_days
        else:
            days = frequency_days.get(self.frequency.lower(), 30)

        self.next_due = add_days(base_date, days)


class PreventiveMaintenanceEngine:
    """Engine for managing preventive maintenance schedules."""

    def __init__(self, association: str):
        self.association = association

    def generate_work_orders(self, days_ahead: int = 7) -> Dict:
        """Generate work orders for upcoming PM tasks."""
        target_date = add_days(today(), days_ahead)

        # Get schedules due within range
        schedules = frappe.get_all(
            "PM Schedule",
            filters={
                "association": self.association,
                "status": "Active",
                "next_due": ["<=", target_date]
            }
        )

        results = {"created": 0, "skipped": 0, "errors": []}

        for schedule in schedules:
            try:
                # Check if work order already exists for this period
                if self._work_order_exists(schedule.name):
                    results["skipped"] += 1
                    continue

                # Create work order
                wo = self._create_pm_work_order(schedule.name)
                results["created"] += 1

            except Exception as e:
                results["errors"].append({
                    "schedule": schedule.name,
                    "error": str(e)
                })

        return results

    def _work_order_exists(self, schedule: str) -> bool:
        """Check if work order already exists for this PM period."""
        schedule_doc = frappe.get_doc("PM Schedule", schedule)

        return frappe.db.exists(
            "Work Order",
            {
                "pm_schedule_item": schedule,
                "status": ["not in", ["Cancelled"]],
                "created_date": [">=", schedule_doc.last_completed or "2000-01-01"]
            }
        )

    def _create_pm_work_order(self, schedule: str) -> str:
        """Create work order from PM schedule."""
        schedule_doc = frappe.get_doc("PM Schedule", schedule)

        # Determine location
        location_type = None
        common_area = None
        building = None
        unit = None

        if schedule_doc.target_type == "Common Area":
            location_type = "Common Area"
            common_area = schedule_doc.common_area
        elif schedule_doc.target_type == "Building":
            location_type = "Building"
            building = schedule_doc.building
        elif schedule_doc.target_type == "Asset":
            asset = frappe.get_doc("Asset", schedule_doc.asset)
            location_type = asset.location_type
            common_area = asset.common_area
            building = asset.building

        # Create work order
        wo = frappe.get_doc({
            "doctype": "Work Order",
            "association": self.association,
            "location_type": location_type,
            "common_area": common_area,
            "building": building,
            "category": schedule_doc.category,
            "title": f"PM: {schedule_doc.schedule_name}",
            "description": schedule_doc.description,
            "priority": schedule_doc.priority,
            "reported_by_type": "Inspection",
            "assigned_to": schedule_doc.assigned_vendor,
            "assigned_staff": schedule_doc.assigned_staff,
            "estimated_cost": schedule_doc.estimated_cost,
            "pm_schedule_item": schedule,
            "linked_asset": schedule_doc.asset,
            "status": "Submitted"
        })

        # Add checklist items
        for item in schedule_doc.checklist_items:
            wo.append("checklist", {
                "task": item.task,
                "required": item.required,
                "completed": False
            })

        wo.insert()

        # Update schedule
        schedule_doc.calculate_next_due()
        schedule_doc.save()

        return wo.name

    def get_overdue_schedules(self) -> List[dict]:
        """Get all overdue PM schedules."""
        return frappe.get_all(
            "PM Schedule",
            filters={
                "association": self.association,
                "status": "Active",
                "next_due": ["<", today()]
            },
            fields=["name", "schedule_name", "next_due", "target_type",
                    "asset", "common_area", "building", "is_regulatory"]
        )

    def get_compliance_status(self) -> Dict:
        """Get compliance status for regulatory PM items."""
        regulatory = frappe.get_all(
            "PM Schedule",
            filters={
                "association": self.association,
                "status": "Active",
                "is_regulatory": True
            },
            fields=["name", "schedule_name", "next_due", "last_completed",
                    "regulation_reference", "compliance_due_days"]
        )

        compliant = []
        due_soon = []
        overdue = []

        for item in regulatory:
            days_until_due = (getdate(item.next_due) - getdate(today())).days

            if days_until_due < 0:
                overdue.append(item)
            elif days_until_due <= (item.compliance_due_days or 30):
                due_soon.append(item)
            else:
                compliant.append(item)

        return {
            "compliant": compliant,
            "due_soon": due_soon,
            "overdue": overdue,
            "compliance_rate": len(compliant) / len(regulatory) * 100 if regulatory else 100
        }


class PMChecklistItem(frappe.model.document.Document):
    """PM checklist item."""
    # Fields:
    # - task: Data (required)
    # - instructions: Text
    # - required: Check
    # - requires_photo: Check
    # - requires_reading: Check
    # - reading_type: Data (e.g., "Temperature", "Pressure")
    # - reading_unit: Data
    # - min_reading: Float
    # - max_reading: Float
    pass
```

## 6.4 Asset Management

```python
# dartwing_ams/doctype/asset/asset.py

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_years, getdate, flt
from typing import List, Optional
from decimal import Decimal

class Asset(Document):
    """
    Physical asset tracking and management.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - asset_name: Data (required)
    - asset_tag: Data (unique identifier/barcode)
    - asset_type: Link to Asset Type
    - category: Select [HVAC, Plumbing, Electrical, Structural,
                        Landscaping, Pool, Elevator, Security, Other]

    # Location
    - location_type: Select [Common Area, Building, Unit]
    - common_area: Link to Common Area
    - building: Link to Building
    - unit: Link to Unit
    - specific_location: Data

    # Details
    - manufacturer: Data
    - model: Data
    - serial_number: Data
    - specifications: Long Text

    # Dates
    - purchase_date: Date
    - installation_date: Date
    - warranty_expiry: Date
    - expected_lifespan_years: Int
    - expected_end_of_life: Date (computed)

    # Financial
    - purchase_cost: Currency
    - current_value: Currency
    - depreciation_method: Select [Straight Line, Declining Balance]
    - annual_depreciation: Currency
    - salvage_value: Currency
    - replacement_cost: Currency

    # Condition
    - condition: Select [Excellent, Good, Fair, Poor, Critical]
    - last_inspection_date: Date
    - next_inspection_due: Date
    - condition_notes: Text
    - condition_photos: Attach Multiple

    # Maintenance
    - pm_schedules: Table (Asset PM Link)
    - maintenance_cost_ytd: Currency
    - maintenance_cost_lifetime: Currency
    - last_maintenance_date: Date

    # Warranty
    - has_warranty: Check
    - warranty_provider: Data
    - warranty_terms: Text
    - warranty_document: Attach

    # Reserve Study
    - in_reserve_study: Check
    - reserve_component: Link to Reserve Component

    # Documents
    - manuals: Attach Multiple
    - photos: Attach Multiple

    # Status
    - status: Select [Active, Under Repair, Decommissioned, Disposed]
    - disposal_date: Date
    - disposal_method: Select [Sold, Scrapped, Donated, Traded]
    - disposal_value: Currency
    """

    def validate(self):
        self.calculate_depreciation()
        self.calculate_end_of_life()
        self.update_maintenance_costs()

    def calculate_depreciation(self):
        """Calculate current value based on depreciation."""
        if not self.purchase_cost or not self.purchase_date:
            return

        years_owned = (getdate(today()) - getdate(self.purchase_date)).days / 365

        if self.depreciation_method == "Straight Line":
            if self.expected_lifespan_years:
                annual_dep = (self.purchase_cost - (self.salvage_value or 0)) / self.expected_lifespan_years
                self.annual_depreciation = annual_dep
                self.current_value = max(
                    self.purchase_cost - (annual_dep * years_owned),
                    self.salvage_value or 0
                )

        elif self.depreciation_method == "Declining Balance":
            rate = 0.2  # 20% declining balance
            self.current_value = self.purchase_cost * ((1 - rate) ** years_owned)
            self.annual_depreciation = self.current_value * rate

    def calculate_end_of_life(self):
        """Calculate expected end of life date."""
        if self.installation_date and self.expected_lifespan_years:
            self.expected_end_of_life = add_years(
                self.installation_date,
                self.expected_lifespan_years
            )

    def update_maintenance_costs(self):
        """Update maintenance cost totals."""
        # Year to date
        year_start = f"{getdate(today()).year}-01-01"
        self.maintenance_cost_ytd = frappe.db.sql("""
            SELECT COALESCE(SUM(actual_cost), 0)
            FROM `tabWork Order`
            WHERE linked_asset = %s
            AND status IN ('Completed', 'Closed')
            AND work_completed >= %s
        """, (self.name, year_start))[0][0]

        # Lifetime
        self.maintenance_cost_lifetime = frappe.db.sql("""
            SELECT COALESCE(SUM(actual_cost), 0)
            FROM `tabWork Order`
            WHERE linked_asset = %s
            AND status IN ('Completed', 'Closed')
        """, self.name)[0][0]

    def record_inspection(
        self,
        condition: str,
        notes: str,
        photos: List[str] = None,
        next_inspection_date: str = None
    ):
        """Record asset inspection."""
        self.condition = condition
        self.last_inspection_date = today()
        self.condition_notes = notes
        self.next_inspection_due = next_inspection_date

        if photos:
            for photo in photos:
                self.append("condition_photos", {"file": photo})

        self.save()

        # Create inspection record
        frappe.get_doc({
            "doctype": "Asset Inspection",
            "asset": self.name,
            "inspection_date": today(),
            "condition": condition,
            "notes": notes,
            "inspected_by": frappe.session.user
        }).insert(ignore_permissions=True)

    def get_maintenance_history(self, limit: int = 20) -> List[dict]:
        """Get maintenance history for asset."""
        return frappe.get_all(
            "Work Order",
            filters={
                "linked_asset": self.name,
                "status": ["in", ["Completed", "Closed"]]
            },
            fields=["name", "title", "category", "work_completed",
                    "actual_cost", "assigned_to"],
            order_by="work_completed desc",
            limit=limit
        )

    def get_cost_analysis(self) -> Dict:
        """Get cost analysis for asset."""
        maintenance_history = frappe.db.sql("""
            SELECT
                YEAR(work_completed) as year,
                SUM(actual_cost) as total_cost,
                COUNT(*) as work_order_count
            FROM `tabWork Order`
            WHERE linked_asset = %s
            AND status IN ('Completed', 'Closed')
            GROUP BY YEAR(work_completed)
            ORDER BY year
        """, self.name, as_dict=True)

        return {
            "purchase_cost": self.purchase_cost,
            "current_value": self.current_value,
            "total_maintenance": self.maintenance_cost_lifetime,
            "total_cost_of_ownership": (self.purchase_cost or 0) + (self.maintenance_cost_lifetime or 0),
            "annual_breakdown": maintenance_history,
            "replacement_cost": self.replacement_cost,
            "remaining_life_years": (
                (getdate(self.expected_end_of_life) - getdate(today())).days / 365
                if self.expected_end_of_life else None
            )
        }

    def decommission(self, reason: str, disposal_method: str = None, disposal_value: float = None):
        """Decommission asset."""
        self.status = "Decommissioned"
        self.disposal_date = today()
        self.disposal_method = disposal_method
        self.disposal_value = disposal_value
        self.save()

        # Cancel any scheduled PM
        frappe.db.sql("""
            UPDATE `tabPM Schedule`
            SET status = 'Archived'
            WHERE asset = %s
        """, self.name)

        # Log the event
        frappe.get_doc({
            "doctype": "Asset Event Log",
            "asset": self.name,
            "event_type": "Decommissioned",
            "event_date": today(),
            "notes": reason,
            "recorded_by": frappe.session.user
        }).insert(ignore_permissions=True)


class AssetType(Document):
    """
    Asset type/category configuration.

    Fields:
    - name: Auto-generated ID
    - type_name: Data (required)
    - category: Select
    - description: Text

    # Defaults
    - default_lifespan_years: Int
    - default_depreciation_method: Select
    - default_inspection_frequency: Select [Monthly, Quarterly, Semi-Annual, Annual]

    # PM Templates
    - pm_templates: Table (Asset Type PM Template)

    # Status
    - is_active: Check
    """
    pass
```

## 6.5 Inspection Management

```python
# dartwing_ams/maintenance/inspection_manager.py

import frappe
from frappe.utils import today, add_days, now_datetime
from typing import List, Dict, Optional

class InspectionManager:
    """Manages property and unit inspections."""

    INSPECTION_TYPES = [
        "Move-In",
        "Move-Out",
        "Annual",
        "Complaint",
        "Violation Follow-Up",
        "Pre-Sale",
        "Insurance",
        "Safety",
        "Common Area"
    ]

    def __init__(self, association: str):
        self.association = association

    def schedule_inspection(
        self,
        inspection_type: str,
        target_type: str,  # "Unit", "Building", "Common Area"
        target: str,
        scheduled_date: str,
        inspector: str = None,
        notes: str = None
    ) -> str:
        """Schedule a new inspection."""
        inspection = frappe.get_doc({
            "doctype": "Property Inspection",
            "association": self.association,
            "inspection_type": inspection_type,
            "target_type": target_type,
            "unit": target if target_type == "Unit" else None,
            "building": target if target_type == "Building" else None,
            "common_area": target if target_type == "Common Area" else None,
            "scheduled_date": scheduled_date,
            "inspector": inspector,
            "notes": notes,
            "status": "Scheduled"
        })
        inspection.insert()

        # Notify relevant parties
        if target_type == "Unit":
            self._notify_unit_residents(target, inspection)

        return inspection.name

    def _notify_unit_residents(self, unit: str, inspection):
        """Notify unit residents of upcoming inspection."""
        residents = frappe.get_all(
            "Unit Member",
            filters={"parent": unit, "status": "Active"},
            pluck="member"
        )

        for resident in residents:
            member = frappe.get_doc("Member", resident)
            member.send_communication(
                subject=f"Scheduled Inspection: {inspection.inspection_type}",
                message=f"An inspection has been scheduled for your unit.\n\n"
                        f"Date: {inspection.scheduled_date}\n"
                        f"Type: {inspection.inspection_type}\n\n"
                        f"Please ensure access is available."
            )

    def conduct_inspection(
        self,
        inspection: str,
        checklist_results: List[dict],
        photos: List[str] = None,
        overall_condition: str = None,
        findings: str = None
    ) -> str:
        """Record inspection results."""
        insp = frappe.get_doc("Property Inspection", inspection)

        insp.status = "Completed"
        insp.completed_date = today()
        insp.completed_time = now_datetime().time()
        insp.completed_by = frappe.session.user
        insp.overall_condition = overall_condition
        insp.findings = findings

        # Record checklist results
        for result in checklist_results:
            insp.append("checklist_results", {
                "item": result.get("item"),
                "result": result.get("result"),  # Pass, Fail, N/A
                "notes": result.get("notes"),
                "photo": result.get("photo")
            })

        # Attach photos
        if photos:
            for photo in photos:
                insp.append("photos", {"file": photo})

        insp.save()

        # Process findings - create violations or work orders as needed
        self._process_findings(insp)

        return insp.name

    def _process_findings(self, inspection):
        """Process inspection findings to create violations or work orders."""
        failed_items = [
            r for r in inspection.checklist_results
            if r.result == "Fail"
        ]

        for item in failed_items:
            # Check if this creates a violation
            checklist_item = frappe.get_doc("Inspection Checklist Item", item.item)

            if checklist_item.creates_violation:
                # Create violation
                frappe.get_doc({
                    "doctype": "Violation",
                    "association": self.association,
                    "unit": inspection.unit,
                    "violation_type": checklist_item.violation_type,
                    "description": item.notes or checklist_item.item_name,
                    "discovered_date": today(),
                    "photos": [{"file": item.photo}] if item.photo else [],
                    "status": "Draft"
                }).insert()

            elif checklist_item.creates_work_order:
                # Create work order
                frappe.get_doc({
                    "doctype": "Work Order",
                    "association": self.association,
                    "location_type": inspection.target_type,
                    "unit": inspection.unit,
                    "building": inspection.building,
                    "common_area": inspection.common_area,
                    "category": checklist_item.work_order_category,
                    "title": f"Inspection Finding: {checklist_item.item_name}",
                    "description": item.notes,
                    "priority": checklist_item.work_order_priority or "Medium",
                    "reported_by_type": "Inspection",
                    "status": "Submitted"
                }).insert()

    def get_due_inspections(self, days_ahead: int = 30) -> List[dict]:
        """Get inspections due within specified days."""
        target_date = add_days(today(), days_ahead)

        return frappe.get_all(
            "Property Inspection",
            filters={
                "association": self.association,
                "status": "Scheduled",
                "scheduled_date": ["<=", target_date]
            },
            fields=["name", "inspection_type", "target_type", "unit",
                    "building", "common_area", "scheduled_date", "inspector"],
            order_by="scheduled_date"
        )

    def generate_annual_inspection_schedule(self, year: int = None) -> Dict:
        """Generate annual inspection schedule for all units."""
        if not year:
            year = getdate(today()).year

        units = frappe.get_all(
            "Unit",
            filters={
                "association": self.association,
                "status": "Active"
            },
            fields=["name", "unit_number", "building"]
        )

        # Distribute inspections throughout the year
        units_per_month = len(units) // 12 + 1

        results = {"scheduled": 0, "errors": []}

        for i, unit in enumerate(units):
            month = (i // units_per_month) + 1
            day = ((i % units_per_month) * 2) + 1  # Spread across month
            day = min(day, 28)  # Avoid month-end issues

            scheduled_date = f"{year}-{month:02d}-{day:02d}"

            try:
                self.schedule_inspection(
                    inspection_type="Annual",
                    target_type="Unit",
                    target=unit.name,
                    scheduled_date=scheduled_date
                )
                results["scheduled"] += 1
            except Exception as e:
                results["errors"].append({
                    "unit": unit.name,
                    "error": str(e)
                })

        return results


class PropertyInspection(frappe.model.document.Document):
    """
    Property inspection record.

    Fields:
    - name: Auto-generated ID
    - association: Link to Association (required)
    - inspection_type: Select (required)

    # Target
    - target_type: Select [Unit, Building, Common Area]
    - unit: Link to Unit
    - building: Link to Building
    - common_area: Link to Common Area

    # Schedule
    - scheduled_date: Date (required)
    - scheduled_time: Time
    - inspector: Link to User
    - access_notes: Text

    # Completion
    - status: Select [Scheduled, In Progress, Completed, Cancelled, No Access]
    - completed_date: Date
    - completed_time: Time
    - completed_by: Link to User

    # Results
    - checklist_template: Link to Inspection Checklist
    - checklist_results: Table (Inspection Result)
    - overall_condition: Select [Excellent, Good, Fair, Poor]
    - findings: Long Text
    - recommendations: Long Text

    # Documentation
    - photos: Table (Inspection Photo)
    - report: Attach

    # Follow-up
    - requires_follow_up: Check
    - follow_up_date: Date
    - follow_up_notes: Text
    - linked_violations: Table (Linked Violation)
    - linked_work_orders: Table (Linked Work Order)
    """
    pass
```

---

_End of Section 6: Operations & Maintenance Architecture_

**Next Section:** Section 7 - Integration Architecture

# Section 7: Integration Architecture

## 7.1 Integration System Overview

The Dartwing AMS integration layer provides connectivity to external systems including accounting platforms, payment processors, access control systems, and third-party services.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION ARCHITECTURE                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     DARTWING AMS CORE                                │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                 INTEGRATION HUB                               │   │    │
│  │  │                                                               │   │    │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │    │
│  │  │  │   Event     │  │   Webhook   │  │   API       │          │   │    │
│  │  │  │   Router    │  │   Manager   │  │   Gateway   │          │   │    │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │    │
│  │  │                                                               │   │    │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │   │    │
│  │  │  │   Sync      │  │   Transform │  │   Error     │          │   │    │
│  │  │  │   Engine    │  │   Pipeline  │  │   Handler   │          │   │    │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐       │
│  │  ACCOUNTING │           │  PAYMENTS   │           │   ACCESS    │       │
│  │             │           │             │           │   CONTROL   │       │
│  │ • QuickBooks│           │ • Stripe    │           │             │       │
│  │ • Xero      │           │ • Plaid     │           │ • PDK       │       │
│  │ • NetSuite  │           │ • Authorize │           │ • Brivo     │       │
│  │ • Sage      │           │ • PayPal    │           │ • LiftMaster│       │
│  └─────────────┘           └─────────────┘           └─────────────┘       │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐       │
│  │  DOCUMENTS  │           │   E-SIGN    │           │    POS      │       │
│  │             │           │             │           │             │       │
│  │ • Google    │           │ • DocuSign  │           │ • Square    │       │
│  │ • Box       │           │ • Adobe     │           │ • Jonas     │       │
│  │ • Dropbox   │           │ • HelloSign │           │ • Northstar │       │
│  │ • SharePoint│           │             │           │             │       │
│  └─────────────┘           └─────────────┘           └─────────────┘       │
│         │                          │                          │             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐       │
│  │   COMMS     │           │  TEE TIMES  │           │   BANKING   │       │
│  │             │           │  (Clubs)    │           │             │       │
│  │ • Twilio    │           │             │           │ • Plaid     │       │
│  │ • SendGrid  │           │ • ForeTees  │           │ • Finicity  │       │
│  │ • Firebase  │           │ • GolfNow   │           │ • Yodlee    │       │
│  │ • OneSignal │           │ • EZLinks   │           │             │       │
│  └─────────────┘           └─────────────┘           └─────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 7.2 Integration Hub Architecture

```python
# dartwing_ams/integrations/hub.py

import frappe
from frappe.utils import now_datetime
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from enum import Enum
import json
import hashlib
import hmac

class IntegrationStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"

class IntegrationEventType(Enum):
    # Financial
    INVOICE_CREATED = "invoice.created"
    INVOICE_PAID = "invoice.paid"
    PAYMENT_RECEIVED = "payment.received"
    PAYMENT_FAILED = "payment.failed"

    # Member
    MEMBER_CREATED = "member.created"
    MEMBER_UPDATED = "member.updated"
    MEMBER_DEACTIVATED = "member.deactivated"

    # Access
    ACCESS_GRANTED = "access.granted"
    ACCESS_REVOKED = "access.revoked"
    GUEST_CHECKED_IN = "guest.checked_in"

    # Maintenance
    WORK_ORDER_CREATED = "work_order.created"
    WORK_ORDER_COMPLETED = "work_order.completed"

    # Governance
    DOCUMENT_SIGNED = "document.signed"
    VOTE_CAST = "vote.cast"

class BaseIntegration(ABC):
    """Base class for all integrations."""

    def __init__(self, association: str, config: Dict = None):
        self.association = association
        self.config = config or self._load_config()
        self.status = IntegrationStatus.INACTIVE

    @abstractmethod
    def _load_config(self) -> Dict:
        """Load integration configuration."""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test integration connection."""
        pass

    @abstractmethod
    def sync(self) -> Dict:
        """Perform data synchronization."""
        pass

    def log_activity(
        self,
        action: str,
        status: str,
        details: Dict = None,
        error: str = None
    ):
        """Log integration activity."""
        frappe.get_doc({
            "doctype": "Integration Log",
            "integration": self.__class__.__name__,
            "association": self.association,
            "action": action,
            "status": status,
            "details": json.dumps(details) if details else None,
            "error": error,
            "timestamp": now_datetime()
        }).insert(ignore_permissions=True)


class IntegrationHub:
    """Central hub for managing all integrations."""

    def __init__(self, association: str):
        self.association = association
        self.integrations: Dict[str, BaseIntegration] = {}
        self._load_integrations()

    def _load_integrations(self):
        """Load all configured integrations."""
        configs = frappe.get_all(
            "Integration Configuration",
            filters={"association": self.association, "enabled": True},
            fields=["integration_type", "config"]
        )

        for config in configs:
            integration_class = self._get_integration_class(config.integration_type)
            if integration_class:
                self.integrations[config.integration_type] = integration_class(
                    self.association,
                    json.loads(config.config) if config.config else None
                )

    def _get_integration_class(self, integration_type: str):
        """Get integration class by type."""
        integration_map = {
            "quickbooks": QuickBooksIntegration,
            "xero": XeroIntegration,
            "stripe": StripeIntegration,
            "plaid": PlaidIntegration,
            "docusign": DocuSignIntegration,
            "pdk": PDKAccessControlIntegration,
            "brivo": BrivoAccessControlIntegration,
            "twilio": TwilioIntegration,
            "sendgrid": SendGridIntegration
        }
        return integration_map.get(integration_type)

    def dispatch_event(self, event_type: IntegrationEventType, data: Dict):
        """Dispatch event to relevant integrations."""
        event_handlers = {
            IntegrationEventType.INVOICE_CREATED: ["quickbooks", "xero"],
            IntegrationEventType.PAYMENT_RECEIVED: ["quickbooks", "xero", "stripe"],
            IntegrationEventType.MEMBER_CREATED: ["pdk", "brivo", "mailchimp"],
            IntegrationEventType.ACCESS_GRANTED: ["pdk", "brivo"],
            IntegrationEventType.ACCESS_REVOKED: ["pdk", "brivo"]
        }

        handlers = event_handlers.get(event_type, [])
        results = {}

        for handler_type in handlers:
            if handler_type in self.integrations:
                integration = self.integrations[handler_type]
                try:
                    result = integration.handle_event(event_type, data)
                    results[handler_type] = {"success": True, "result": result}
                except Exception as e:
                    results[handler_type] = {"success": False, "error": str(e)}
                    integration.log_activity(
                        action=event_type.value,
                        status="error",
                        error=str(e)
                    )

        return results

    def sync_all(self) -> Dict:
        """Sync all integrations."""
        results = {}

        for name, integration in self.integrations.items():
            try:
                result = integration.sync()
                results[name] = {"success": True, "result": result}
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}

        return results

    def get_status(self) -> Dict:
        """Get status of all integrations."""
        status = {}

        for name, integration in self.integrations.items():
            status[name] = {
                "status": integration.status.value,
                "last_sync": integration.config.get("last_sync"),
                "error_count": integration.config.get("error_count", 0)
            }

        return status


class WebhookManager:
    """Manages incoming webhooks from external services."""

    def __init__(self, association: str):
        self.association = association

    def verify_signature(
        self,
        payload: bytes,
        signature: str,
        secret: str,
        algorithm: str = "sha256"
    ) -> bool:
        """Verify webhook signature."""
        if algorithm == "sha256":
            computed = hmac.new(
                secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
        elif algorithm == "sha1":
            computed = hmac.new(
                secret.encode(),
                payload,
                hashlib.sha1
            ).hexdigest()
        else:
            return False

        return hmac.compare_digest(computed, signature)

    def process_webhook(
        self,
        source: str,
        event_type: str,
        payload: Dict,
        headers: Dict
    ) -> Dict:
        """Process incoming webhook."""
        # Log webhook
        log = frappe.get_doc({
            "doctype": "Webhook Log",
            "association": self.association,
            "source": source,
            "event_type": event_type,
            "payload": json.dumps(payload),
            "headers": json.dumps(headers),
            "received_at": now_datetime(),
            "status": "Received"
        })
        log.insert(ignore_permissions=True)

        try:
            # Route to appropriate handler
            handler = self._get_handler(source)
            if handler:
                result = handler.process(event_type, payload)
                log.status = "Processed"
                log.result = json.dumps(result)
            else:
                log.status = "No Handler"

            log.save()
            return {"success": True, "log": log.name}

        except Exception as e:
            log.status = "Error"
            log.error = str(e)
            log.save()
            return {"success": False, "error": str(e)}

    def _get_handler(self, source: str):
        """Get webhook handler for source."""
        handlers = {
            "stripe": StripeWebhookHandler,
            "plaid": PlaidWebhookHandler,
            "docusign": DocuSignWebhookHandler,
            "pdk": PDKWebhookHandler
        }

        handler_class = handlers.get(source)
        if handler_class:
            return handler_class(self.association)
        return None
```

## 7.3 Accounting Integrations

```python
# dartwing_ams/integrations/accounting/quickbooks.py

import frappe
from frappe.utils import today, flt
from typing import Dict, List, Optional
from ..hub import BaseIntegration, IntegrationEventType
import requests

class QuickBooksIntegration(BaseIntegration):
    """QuickBooks Online integration."""

    BASE_URL = "https://quickbooks.api.intuit.com/v3/company"

    def _load_config(self) -> Dict:
        """Load QuickBooks configuration."""
        config = frappe.get_doc(
            "QuickBooks Settings",
            {"association": self.association}
        )
        return {
            "client_id": config.client_id,
            "client_secret": config.get_password("client_secret"),
            "realm_id": config.realm_id,
            "access_token": config.get_password("access_token"),
            "refresh_token": config.get_password("refresh_token"),
            "token_expiry": config.token_expiry,
            "account_mapping": config.account_mapping
        }

    def _get_headers(self) -> Dict:
        """Get API headers with auth."""
        self._refresh_token_if_needed()
        return {
            "Authorization": f"Bearer {self.config['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _refresh_token_if_needed(self):
        """Refresh OAuth token if expired."""
        from datetime import datetime

        if datetime.now() > self.config['token_expiry']:
            response = requests.post(
                "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.config["refresh_token"]
                },
                auth=(self.config["client_id"], self.config["client_secret"])
            )

            if response.status_code == 200:
                tokens = response.json()
                self._save_tokens(tokens)

    def test_connection(self) -> bool:
        """Test QuickBooks connection."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/{self.config['realm_id']}/companyinfo/{self.config['realm_id']}",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except Exception:
            return False

    def sync(self) -> Dict:
        """Sync data with QuickBooks."""
        results = {
            "invoices_synced": 0,
            "payments_synced": 0,
            "customers_synced": 0,
            "errors": []
        }

        # Sync invoices
        results["invoices_synced"] = self._sync_invoices()

        # Sync payments
        results["payments_synced"] = self._sync_payments()

        # Sync customers (members)
        results["customers_synced"] = self._sync_customers()

        return results

    def _sync_invoices(self) -> int:
        """Sync invoices to QuickBooks."""
        # Get unsynced invoices
        invoices = frappe.get_all(
            "Invoice",
            filters={
                "organization": self.association,
                "docstatus": 1,
                "qb_synced": False
            },
            fields=["*"]
        )

        synced = 0
        for invoice in invoices:
            try:
                qb_invoice = self._create_qb_invoice(invoice)

                response = requests.post(
                    f"{self.BASE_URL}/{self.config['realm_id']}/invoice",
                    headers=self._get_headers(),
                    json={"Invoice": qb_invoice}
                )

                if response.status_code == 200:
                    qb_data = response.json()
                    frappe.db.set_value(
                        "Invoice",
                        invoice.name,
                        {
                            "qb_synced": True,
                            "qb_id": qb_data["Invoice"]["Id"],
                            "qb_sync_date": today()
                        }
                    )
                    synced += 1

                    self.log_activity(
                        action="sync_invoice",
                        status="success",
                        details={"invoice": invoice.name, "qb_id": qb_data["Invoice"]["Id"]}
                    )

            except Exception as e:
                self.log_activity(
                    action="sync_invoice",
                    status="error",
                    details={"invoice": invoice.name},
                    error=str(e)
                )

        return synced

    def _create_qb_invoice(self, invoice: Dict) -> Dict:
        """Create QuickBooks invoice payload."""
        # Get customer (member) QB ID
        member = frappe.get_doc("Member", invoice.member)
        customer_ref = member.qb_customer_id

        # Map line items
        lines = []
        for item in frappe.get_all(
            "Invoice Item",
            filters={"parent": invoice.name},
            fields=["description", "amount", "account"]
        ):
            # Map account to QB account
            qb_account = self._get_qb_account(item.account)

            lines.append({
                "Amount": flt(item.amount),
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {"value": qb_account},
                    "Qty": 1,
                    "UnitPrice": flt(item.amount)
                },
                "Description": item.description
            })

        return {
            "CustomerRef": {"value": customer_ref},
            "TxnDate": str(invoice.invoice_date),
            "DueDate": str(invoice.due_date),
            "Line": lines,
            "DocNumber": invoice.name
        }

    def _sync_payments(self) -> int:
        """Sync payments to QuickBooks."""
        payments = frappe.get_all(
            "Payment",
            filters={
                "organization": self.association,
                "docstatus": 1,
                "qb_synced": False
            },
            fields=["*"]
        )

        synced = 0
        for payment in payments:
            try:
                qb_payment = self._create_qb_payment(payment)

                response = requests.post(
                    f"{self.BASE_URL}/{self.config['realm_id']}/payment",
                    headers=self._get_headers(),
                    json={"Payment": qb_payment}
                )

                if response.status_code == 200:
                    qb_data = response.json()
                    frappe.db.set_value(
                        "Payment",
                        payment.name,
                        {
                            "qb_synced": True,
                            "qb_id": qb_data["Payment"]["Id"]
                        }
                    )
                    synced += 1

            except Exception as e:
                self.log_activity(
                    action="sync_payment",
                    status="error",
                    details={"payment": payment.name},
                    error=str(e)
                )

        return synced

    def _create_qb_payment(self, payment: Dict) -> Dict:
        """Create QuickBooks payment payload."""
        member = frappe.get_doc("Member", payment.member)

        # Get linked invoices
        allocations = frappe.get_all(
            "Payment Allocation",
            filters={"payment": payment.name},
            fields=["invoice", "allocated_amount"]
        )

        lines = []
        for alloc in allocations:
            invoice = frappe.get_doc("Invoice", alloc.invoice)
            if invoice.qb_id:
                lines.append({
                    "Amount": flt(alloc.allocated_amount),
                    "LinkedTxn": [{
                        "TxnId": invoice.qb_id,
                        "TxnType": "Invoice"
                    }]
                })

        return {
            "CustomerRef": {"value": member.qb_customer_id},
            "TotalAmt": flt(payment.amount),
            "TxnDate": str(payment.posting_date),
            "Line": lines
        }

    def _sync_customers(self) -> int:
        """Sync members to QuickBooks as customers."""
        members = frappe.get_all(
            "Member",
            filters={
                "organization": self.association,
                "status": "Active",
                "qb_customer_id": ["is", "not set"]
            },
            fields=["name", "person"]
        )

        synced = 0
        for member in members:
            try:
                person = frappe.get_doc("Person", member.person)

                qb_customer = {
                    "DisplayName": person.full_name,
                    "PrimaryEmailAddr": {"Address": person.email},
                    "PrimaryPhone": {"FreeFormNumber": person.mobile}
                }

                response = requests.post(
                    f"{self.BASE_URL}/{self.config['realm_id']}/customer",
                    headers=self._get_headers(),
                    json={"Customer": qb_customer}
                )

                if response.status_code == 200:
                    qb_data = response.json()
                    frappe.db.set_value(
                        "Member",
                        member.name,
                        "qb_customer_id",
                        qb_data["Customer"]["Id"]
                    )
                    synced += 1

            except Exception as e:
                self.log_activity(
                    action="sync_customer",
                    status="error",
                    details={"member": member.name},
                    error=str(e)
                )

        return synced

    def _get_qb_account(self, dartwing_account: str) -> str:
        """Map Dartwing account to QuickBooks account."""
        mapping = json.loads(self.config.get("account_mapping", "{}"))
        return mapping.get(dartwing_account, "1")  # Default to first account

    def handle_event(self, event_type: IntegrationEventType, data: Dict) -> Dict:
        """Handle integration events."""
        if event_type == IntegrationEventType.INVOICE_CREATED:
            return self._handle_invoice_created(data)
        elif event_type == IntegrationEventType.PAYMENT_RECEIVED:
            return self._handle_payment_received(data)

        return {"handled": False}

    def _handle_invoice_created(self, data: Dict) -> Dict:
        """Handle invoice created event."""
        invoice = frappe.get_doc("Invoice", data["invoice"])
        synced = self._sync_single_invoice(invoice)
        return {"synced": synced}

    def _handle_payment_received(self, data: Dict) -> Dict:
        """Handle payment received event."""
        payment = frappe.get_doc("Payment", data["payment"])
        synced = self._sync_single_payment(payment)
        return {"synced": synced}
```

## 7.4 Access Control Integration

```python
# dartwing_ams/integrations/access_control/pdk.py

import frappe
from frappe.utils import today, now_datetime
from typing import Dict, List, Optional
from ..hub import BaseIntegration, IntegrationEventType
import requests

class PDKAccessControlIntegration(BaseIntegration):
    """PDK Access Control integration."""

    def _load_config(self) -> Dict:
        """Load PDK configuration."""
        config = frappe.get_doc(
            "PDK Settings",
            {"association": self.association}
        )
        return {
            "api_url": config.api_url,
            "api_key": config.get_password("api_key"),
            "panel_id": config.panel_id,
            "default_access_level": config.default_access_level,
            "credential_format": config.credential_format
        }

    def _get_headers(self) -> Dict:
        """Get API headers."""
        return {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        """Test PDK connection."""
        try:
            response = requests.get(
                f"{self.config['api_url']}/panels/{self.config['panel_id']}",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except Exception:
            return False

    def sync(self) -> Dict:
        """Sync access credentials with PDK."""
        results = {
            "credentials_synced": 0,
            "credentials_revoked": 0,
            "errors": []
        }

        # Sync active credentials
        results["credentials_synced"] = self._sync_active_credentials()

        # Revoke deactivated credentials
        results["credentials_revoked"] = self._revoke_inactive_credentials()

        return results

    def _sync_active_credentials(self) -> int:
        """Sync active access cards to PDK."""
        cards = frappe.get_all(
            "Access Card",
            filters={
                "association": self.association,
                "status": "Active",
                "pdk_synced": False
            },
            fields=["*"]
        )

        synced = 0
        for card in cards:
            try:
                # Get member details
                member = frappe.get_doc("Member", card.member)
                person = frappe.get_doc("Person", member.person)

                # Create or update credential in PDK
                pdk_credential = {
                    "card_number": card.card_number,
                    "facility_code": card.facility_code or self.config.get("default_facility_code"),
                    "person": {
                        "first_name": person.first_name,
                        "last_name": person.last_name,
                        "email": person.email
                    },
                    "access_levels": self._get_access_levels(card),
                    "valid_from": str(card.activation_date or today()),
                    "valid_until": str(card.expiry_date) if card.expiry_date else None
                }

                response = requests.post(
                    f"{self.config['api_url']}/credentials",
                    headers=self._get_headers(),
                    json=pdk_credential
                )

                if response.status_code in [200, 201]:
                    pdk_data = response.json()
                    frappe.db.set_value(
                        "Access Card",
                        card.name,
                        {
                            "pdk_synced": True,
                            "pdk_credential_id": pdk_data.get("id"),
                            "pdk_sync_date": today()
                        }
                    )
                    synced += 1

                    self.log_activity(
                        action="sync_credential",
                        status="success",
                        details={"card": card.name, "pdk_id": pdk_data.get("id")}
                    )

            except Exception as e:
                self.log_activity(
                    action="sync_credential",
                    status="error",
                    details={"card": card.name},
                    error=str(e)
                )

        return synced

    def _revoke_inactive_credentials(self) -> int:
        """Revoke deactivated credentials in PDK."""
        cards = frappe.get_all(
            "Access Card",
            filters={
                "association": self.association,
                "status": ["in", ["Suspended", "Lost", "Stolen", "Returned"]],
                "pdk_synced": True,
                "pdk_revoked": False
            },
            fields=["name", "pdk_credential_id"]
        )

        revoked = 0
        for card in cards:
            try:
                response = requests.delete(
                    f"{self.config['api_url']}/credentials/{card.pdk_credential_id}",
                    headers=self._get_headers()
                )

                if response.status_code in [200, 204]:
                    frappe.db.set_value(
                        "Access Card",
                        card.name,
                        {"pdk_revoked": True}
                    )
                    revoked += 1

            except Exception as e:
                self.log_activity(
                    action="revoke_credential",
                    status="error",
                    details={"card": card.name},
                    error=str(e)
                )

        return revoked

    def _get_access_levels(self, card) -> List[str]:
        """Get access levels for card."""
        access_levels = [self.config.get("default_access_level", "General")]

        # Add custom access areas
        for area in card.custom_access_areas:
            if area.pdk_access_level:
                access_levels.append(area.pdk_access_level)

        return access_levels

    def grant_guest_access(
        self,
        guest_pass: str,
        access_areas: List[str] = None
    ) -> Dict:
        """Grant temporary access for guest."""
        guest = frappe.get_doc("Guest Pass", guest_pass)

        # Create temporary credential
        temp_credential = {
            "card_number": guest.pass_code[:8],
            "credential_type": "temporary",
            "person": {
                "first_name": guest.guest_name.split()[0],
                "last_name": " ".join(guest.guest_name.split()[1:]) or "Guest"
            },
            "access_levels": access_areas or ["Guest"],
            "valid_from": str(guest.valid_from),
            "valid_until": str(guest.valid_until)
        }

        response = requests.post(
            f"{self.config['api_url']}/credentials/temporary",
            headers=self._get_headers(),
            json=temp_credential
        )

        if response.status_code in [200, 201]:
            pdk_data = response.json()
            frappe.db.set_value(
                "Guest Pass",
                guest_pass,
                {"pdk_credential_id": pdk_data.get("id")}
            )
            return {"success": True, "credential_id": pdk_data.get("id")}

        return {"success": False, "error": response.text}

    def revoke_guest_access(self, guest_pass: str) -> Dict:
        """Revoke guest access."""
        guest = frappe.get_doc("Guest Pass", guest_pass)

        if not guest.pdk_credential_id:
            return {"success": True, "message": "No credential to revoke"}

        response = requests.delete(
            f"{self.config['api_url']}/credentials/{guest.pdk_credential_id}",
            headers=self._get_headers()
        )

        return {"success": response.status_code in [200, 204]}

    def get_access_log(
        self,
        start_date: str,
        end_date: str,
        card_number: str = None
    ) -> List[Dict]:
        """Get access log from PDK."""
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "panel_id": self.config["panel_id"]
        }

        if card_number:
            params["card_number"] = card_number

        response = requests.get(
            f"{self.config['api_url']}/access-log",
            headers=self._get_headers(),
            params=params
        )

        if response.status_code == 200:
            return response.json().get("events", [])

        return []

    def handle_event(self, event_type: IntegrationEventType, data: Dict) -> Dict:
        """Handle integration events."""
        if event_type == IntegrationEventType.ACCESS_GRANTED:
            return self._handle_access_granted(data)
        elif event_type == IntegrationEventType.ACCESS_REVOKED:
            return self._handle_access_revoked(data)
        elif event_type == IntegrationEventType.GUEST_CHECKED_IN:
            return self._handle_guest_checkin(data)

        return {"handled": False}

    def _handle_access_granted(self, data: Dict) -> Dict:
        """Handle access granted event."""
        card = data.get("card")
        if card:
            frappe.enqueue(
                "dartwing_ams.integrations.access_control.pdk.sync_single_card",
                card=card
            )
        return {"queued": True}

    def _handle_access_revoked(self, data: Dict) -> Dict:
        """Handle access revoked event."""
        card = data.get("card")
        if card:
            return self._revoke_single_credential(card)
        return {"handled": False}
```

## 7.5 E-Signature Integration

```python
# dartwing_ams/integrations/esign/docusign.py

import frappe
from frappe.utils import today, now_datetime
from typing import Dict, List, Optional
from ..hub import BaseIntegration
import requests
import base64

class DocuSignIntegration(BaseIntegration):
    """DocuSign e-signature integration."""

    def _load_config(self) -> Dict:
        """Load DocuSign configuration."""
        config = frappe.get_doc(
            "DocuSign Settings",
            {"association": self.association}
        )
        return {
            "integration_key": config.integration_key,
            "user_id": config.user_id,
            "account_id": config.account_id,
            "base_path": config.base_path,
            "private_key": config.get_password("private_key"),
            "access_token": config.get_password("access_token"),
            "token_expiry": config.token_expiry
        }

    def _get_headers(self) -> Dict:
        """Get API headers with auth."""
        self._refresh_token_if_needed()
        return {
            "Authorization": f"Bearer {self.config['access_token']}",
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        """Test DocuSign connection."""
        try:
            response = requests.get(
                f"{self.config['base_path']}/accounts/{self.config['account_id']}",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except Exception:
            return False

    def sync(self) -> Dict:
        """Sync envelope status with DocuSign."""
        # Get pending envelopes
        pending = frappe.get_all(
            "Signature Request",
            filters={
                "association": self.association,
                "status": ["in", ["Pending", "Sent"]],
                "docusign_envelope_id": ["is", "set"]
            },
            fields=["name", "docusign_envelope_id"]
        )

        updated = 0
        for req in pending:
            status = self._get_envelope_status(req.docusign_envelope_id)
            if status:
                self._update_signature_request(req.name, status)
                updated += 1

        return {"envelopes_updated": updated}

    def send_for_signature(
        self,
        signature_request: str,
        document_content: bytes,
        document_name: str
    ) -> Dict:
        """Send document for signature via DocuSign."""
        sig_req = frappe.get_doc("Signature Request", signature_request)

        # Build envelope definition
        envelope = {
            "emailSubject": f"Please sign: {document_name}",
            "documents": [{
                "documentId": "1",
                "name": document_name,
                "documentBase64": base64.b64encode(document_content).decode()
            }],
            "recipients": {
                "signers": []
            },
            "status": "sent"
        }

        # Add signers
        for i, signer in enumerate(sig_req.signers):
            member = frappe.get_doc("Member", signer.member)
            person = frappe.get_doc("Person", member.person)

            envelope["recipients"]["signers"].append({
                "recipientId": str(i + 1),
                "routingOrder": str(signer.signing_order),
                "email": person.email,
                "name": person.full_name,
                "tabs": {
                    "signHereTabs": [{
                        "anchorString": "/sig/",
                        "anchorUnits": "pixels",
                        "anchorXOffset": "0",
                        "anchorYOffset": "0"
                    }],
                    "dateSignedTabs": [{
                        "anchorString": "/date/",
                        "anchorUnits": "pixels",
                        "anchorXOffset": "0",
                        "anchorYOffset": "0"
                    }]
                }
            })

        # Create envelope
        response = requests.post(
            f"{self.config['base_path']}/accounts/{self.config['account_id']}/envelopes",
            headers=self._get_headers(),
            json=envelope
        )

        if response.status_code == 201:
            envelope_data = response.json()

            sig_req.docusign_envelope_id = envelope_data["envelopeId"]
            sig_req.status = "Sent"
            sig_req.save()

            self.log_activity(
                action="send_envelope",
                status="success",
                details={
                    "request": signature_request,
                    "envelope_id": envelope_data["envelopeId"]
                }
            )

            return {
                "success": True,
                "envelope_id": envelope_data["envelopeId"]
            }

        return {
            "success": False,
            "error": response.text
        }

    def _get_envelope_status(self, envelope_id: str) -> Optional[Dict]:
        """Get envelope status from DocuSign."""
        response = requests.get(
            f"{self.config['base_path']}/accounts/{self.config['account_id']}/envelopes/{envelope_id}",
            headers=self._get_headers()
        )

        if response.status_code == 200:
            return response.json()
        return None

    def _update_signature_request(self, request: str, envelope_status: Dict):
        """Update signature request based on envelope status."""
        sig_req = frappe.get_doc("Signature Request", request)

        ds_status = envelope_status.get("status")

        if ds_status == "completed":
            sig_req.status = "Completed"
            sig_req.completed_at = now_datetime()

            # Download signed document
            signed_doc = self._download_signed_document(envelope_status["envelopeId"])
            if signed_doc:
                # Save signed document
                file_doc = frappe.get_doc({
                    "doctype": "File",
                    "file_name": f"signed_{sig_req.document}.pdf",
                    "content": signed_doc,
                    "attached_to_doctype": "Signature Request",
                    "attached_to_name": request
                })
                file_doc.insert(ignore_permissions=True)
                sig_req.signed_document = file_doc.file_url

        elif ds_status == "declined":
            sig_req.status = "Declined"

        elif ds_status == "voided":
            sig_req.status = "Cancelled"

        sig_req.save()

    def _download_signed_document(self, envelope_id: str) -> Optional[bytes]:
        """Download signed document from DocuSign."""
        response = requests.get(
            f"{self.config['base_path']}/accounts/{self.config['account_id']}/envelopes/{envelope_id}/documents/combined",
            headers=self._get_headers()
        )

        if response.status_code == 200:
            return response.content
        return None

    def void_envelope(self, envelope_id: str, reason: str) -> Dict:
        """Void an envelope."""
        response = requests.put(
            f"{self.config['base_path']}/accounts/{self.config['account_id']}/envelopes/{envelope_id}",
            headers=self._get_headers(),
            json={
                "status": "voided",
                "voidedReason": reason
            }
        )

        return {"success": response.status_code == 200}
```

## 7.6 Sync Engine & Data Mapping

```python
# dartwing_ams/integrations/sync_engine.py

import frappe
from frappe.utils import now_datetime, today
from typing import Dict, List, Optional, Callable
from datetime import datetime
import json

class SyncEngine:
    """Engine for managing data synchronization between systems."""

    def __init__(self, association: str):
        self.association = association
        self.sync_log = []

    def run_scheduled_syncs(self):
        """Run all scheduled synchronization jobs."""
        schedules = frappe.get_all(
            "Sync Schedule",
            filters={
                "association": self.association,
                "enabled": True,
                "next_run": ["<=", now_datetime()]
            },
            fields=["name", "integration", "sync_type", "direction"]
        )

        for schedule in schedules:
            self._execute_sync(schedule)

    def _execute_sync(self, schedule: Dict):
        """Execute a scheduled sync."""
        log = frappe.get_doc({
            "doctype": "Sync Log",
            "association": self.association,
            "schedule": schedule.name,
            "integration": schedule.integration,
            "sync_type": schedule.sync_type,
            "direction": schedule.direction,
            "started_at": now_datetime(),
            "status": "Running"
        })
        log.insert(ignore_permissions=True)

        try:
            # Get integration handler
            from .hub import IntegrationHub
            hub = IntegrationHub(self.association)
            integration = hub.integrations.get(schedule.integration)

            if not integration:
                raise Exception(f"Integration {schedule.integration} not found")

            # Run sync
            result = integration.sync()

            log.status = "Completed"
            log.result = json.dumps(result)
            log.records_processed = result.get("total", 0)
            log.records_created = result.get("created", 0)
            log.records_updated = result.get("updated", 0)
            log.records_failed = len(result.get("errors", []))

        except Exception as e:
            log.status = "Failed"
            log.error = str(e)

        finally:
            log.completed_at = now_datetime()
            log.save()

            # Update schedule next run
            self._update_next_run(schedule.name)

    def _update_next_run(self, schedule: str):
        """Update next run time for schedule."""
        sched = frappe.get_doc("Sync Schedule", schedule)

        interval_map = {
            "Hourly": 60,
            "Daily": 1440,
            "Weekly": 10080,
            "Monthly": 43200
        }

        minutes = interval_map.get(sched.frequency, 1440)
        next_run = frappe.utils.add_to_date(now_datetime(), minutes=minutes)

        sched.next_run = next_run
        sched.last_run = now_datetime()
        sched.save()


class DataMapper:
    """Maps data between Dartwing and external systems."""

    def __init__(self, mapping_config: Dict):
        self.config = mapping_config

    def map_to_external(self, data: Dict, entity_type: str) -> Dict:
        """Map Dartwing data to external format."""
        mapping = self.config.get(entity_type, {}).get("outbound", {})

        result = {}
        for external_field, dartwing_field in mapping.items():
            if isinstance(dartwing_field, dict):
                # Complex mapping with transformation
                value = self._get_nested_value(data, dartwing_field["field"])
                if "transform" in dartwing_field:
                    value = self._apply_transform(value, dartwing_field["transform"])
                result[external_field] = value
            else:
                # Simple field mapping
                result[external_field] = self._get_nested_value(data, dartwing_field)

        return result

    def map_from_external(self, data: Dict, entity_type: str) -> Dict:
        """Map external data to Dartwing format."""
        mapping = self.config.get(entity_type, {}).get("inbound", {})

        result = {}
        for dartwing_field, external_field in mapping.items():
            if isinstance(external_field, dict):
                value = self._get_nested_value(data, external_field["field"])
                if "transform" in external_field:
                    value = self._apply_transform(value, external_field["transform"])
                result[dartwing_field] = value
            else:
                result[dartwing_field] = self._get_nested_value(data, external_field)

        return result

    def _get_nested_value(self, data: Dict, path: str):
        """Get value from nested dict using dot notation."""
        keys = path.split(".")
        value = data

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None

        return value

    def _apply_transform(self, value, transform: str):
        """Apply transformation to value."""
        transforms = {
            "uppercase": lambda v: v.upper() if v else v,
            "lowercase": lambda v: v.lower() if v else v,
            "date_to_iso": lambda v: v.isoformat() if isinstance(v, datetime) else v,
            "cents_to_dollars": lambda v: v / 100 if v else 0,
            "dollars_to_cents": lambda v: int(v * 100) if v else 0,
            "boolean_to_yesno": lambda v: "Yes" if v else "No",
            "yesno_to_boolean": lambda v: v.lower() == "yes" if v else False
        }

        transform_func = transforms.get(transform)
        if transform_func:
            return transform_func(value)

        return value


class ConflictResolver:
    """Resolves conflicts during data synchronization."""

    STRATEGIES = ["last_write_wins", "source_priority", "manual", "merge"]

    def __init__(self, strategy: str = "last_write_wins"):
        self.strategy = strategy

    def resolve(
        self,
        local_data: Dict,
        external_data: Dict,
        local_modified: datetime,
        external_modified: datetime
    ) -> Dict:
        """Resolve conflict between local and external data."""
        if self.strategy == "last_write_wins":
            if external_modified > local_modified:
                return external_data
            return local_data

        elif self.strategy == "source_priority":
            # Local data always wins
            return local_data

        elif self.strategy == "merge":
            # Merge non-conflicting fields
            merged = local_data.copy()
            for key, value in external_data.items():
                if key not in local_data or local_data[key] is None:
                    merged[key] = value
            return merged

        elif self.strategy == "manual":
            # Create conflict record for manual resolution
            frappe.get_doc({
                "doctype": "Sync Conflict",
                "local_data": json.dumps(local_data),
                "external_data": json.dumps(external_data),
                "status": "Pending"
            }).insert(ignore_permissions=True)

            return local_data  # Keep local until resolved

        return local_data
```

---

_End of Section 7: Integration Architecture_

**Workgroup 3 Complete!**

**Files Created:**

- Section 5: Member Services & Portal Architecture
- Section 6: Operations & Maintenance Architecture
- Section 7: Integration Architecture

**Next Workgroup:** Workgroup 4 - Sections 8, 9, 10 (Mobile Application, Testing & QA, Deployment & DevOps)
