# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
OrganizationMixin provides access to parent Organization properties
for concrete organization types (Company, Family, Nonprofit, Club).
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

import frappe
from frappe import _

if TYPE_CHECKING:
    from frappe.model.document import Document

# Fields fetched from Organization in a single query for caching
CACHED_ORG_FIELDS = ["org_name", "logo", "status"]


class OrganizationMixin:
    """
    Mixin class that provides access to parent Organization's properties.

    Concrete organization types (Company, Family, etc.) should inherit from
    both Document and OrganizationMixin to get access to org_name, logo,
    and org_status properties.

    Usage:
        class Company(Document, OrganizationMixin):
            pass

    The concrete type must have an 'organization' field linking to Organization.

    CR-009 FIX: Uses lazy loading with caching to avoid N+1 query problem.
    All Organization fields are fetched in a single query on first access.
    """

    def _get_organization_cache(self) -> Optional[Dict[str, Any]]:
        """
        Lazy-load and cache Organization data.

        Single DB query fetches all needed fields, cached for the request lifetime.

        Returns:
            Dict with org_name, logo, status fields, or None if no organization linked.
        """
        if not hasattr(self, "_org_cache"):
            if not self.organization:
                self._org_cache = None
            else:
                self._org_cache = frappe.db.get_value(
                    "Organization",
                    self.organization,
                    CACHED_ORG_FIELDS,
                    as_dict=True
                )
        return self._org_cache

    def _clear_organization_cache(self) -> None:
        """Clear the cached Organization data (call after Organization updates)."""
        if hasattr(self, "_org_cache"):
            delattr(self, "_org_cache")

    @property
    def org_name(self) -> Optional[str]:
        """Get the organization name from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("org_name") if cache else None

    @property
    def logo(self) -> Optional[str]:
        """Get the logo from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("logo") if cache else None

    @property
    def org_status(self) -> Optional[str]:
        """Get the status from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("status") if cache else None

    def get_organization_doc(self) -> Optional["Document"]:
        """Get the full Organization document."""
        if not self.organization:
            return None
        return frappe.get_doc("Organization", self.organization)

    def update_org_name(self, new_name: str) -> None:
        """
        Update the organization name on the linked Organization record.

        This method enforces permission checks to ensure the user has write
        access to the Organization before updating.

        Args:
            new_name: The new organization name to set.

        Raises:
            frappe.ValidationError: If new_name is empty/whitespace or no
                organization is linked.
            frappe.PermissionError: If user lacks write permission on Organization.
        """
        # Normalize and validate input
        org_name = (new_name or "").strip()
        if not org_name:
            frappe.throw(_("Organization name cannot be empty"))

        # Validate organization link exists
        if not self.organization:
            frappe.throw(_("Cannot update organization name: No organization linked"))

        # Load Organization document (checks read permission)
        org = frappe.get_doc("Organization", self.organization)

        # Check write permission explicitly
        org.check_permission("write")

        # Update and save (runs validations, hooks, and audit logging)
        org.org_name = org_name
        org.save()

        # Clear cache so subsequent property access returns fresh data
        self._clear_organization_cache()
