# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission utilities for Dartwing.

This module provides organization-scoped access control for all Dartwing DocTypes.
It implements User Permission-based row-level security to ensure users can only
access data belonging to organizations they are members of.

Modules:
    - organization: Permission functions for Organization DocType
    - family: Permission functions for Family DocType and Family Member
    - company: Permission functions for Company DocType
    - association: Permission functions for Association DocType
    - nonprofit: Permission functions for Nonprofit DocType
    - helpers: Core permission propagation logic (create/remove on Org Member events)
    - api: Whitelisted API endpoints for permission queries
"""

# Family permissions (original)
from dartwing.permissions.family import (
    get_permission_query_conditions as family_get_permission_query_conditions,
    has_permission as family_has_permission,
    get_member_permission_query_conditions,
)

# Organization permissions
from dartwing.permissions.organization import (
    get_permission_query_conditions as organization_get_permission_query_conditions,
    has_permission as organization_has_permission,
)

# Company permissions
from dartwing.permissions.company import (
    get_permission_query_conditions as company_get_permission_query_conditions,
    has_permission as company_has_permission,
)

# Association permissions
from dartwing.permissions.association import (
    get_permission_query_conditions as association_get_permission_query_conditions,
    has_permission as association_has_permission,
)

# Nonprofit permissions
from dartwing.permissions.nonprofit import (
    get_permission_query_conditions as nonprofit_get_permission_query_conditions,
    has_permission as nonprofit_has_permission,
)

# Permission lifecycle helpers
from dartwing.permissions.helpers import (
    create_user_permissions,
    remove_user_permissions,
    handle_status_change,
)

# API endpoints
from dartwing.permissions.api import (
    get_user_organizations,
    check_organization_access,
    get_organization_members,
    get_permission_audit_log,
)

__all__ = [
    # Family
    "family_get_permission_query_conditions",
    "family_has_permission",
    "get_member_permission_query_conditions",
    # Organization
    "organization_get_permission_query_conditions",
    "organization_has_permission",
    # Company
    "company_get_permission_query_conditions",
    "company_has_permission",
    # Association
    "association_get_permission_query_conditions",
    "association_has_permission",
    # Nonprofit
    "nonprofit_get_permission_query_conditions",
    "nonprofit_has_permission",
    # Helpers
    "create_user_permissions",
    "remove_user_permissions",
    "handle_status_change",
    # API
    "get_user_organizations",
    "check_organization_access",
    "get_organization_members",
    "get_permission_audit_log",
]
