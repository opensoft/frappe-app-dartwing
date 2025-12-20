# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
OrganizationMixin provides access to parent Organization properties
for concrete organization types (Company, Family, Nonprofit, Club).
"""

import frappe


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

    def _get_organization_cache(self):
        """
        Lazy-load and cache Organization data.

        Single DB query fetches all needed fields, cached for the request lifetime.
        """
        if not hasattr(self, "_org_cache"):
            if not self.organization:
                self._org_cache = None
            else:
                self._org_cache = frappe.db.get_value(
                    "Organization",
                    self.organization,
                    ["org_name", "logo", "status"],
                    as_dict=True
                )
        return self._org_cache

    def _clear_organization_cache(self):
        """Clear the cached Organization data (call after Organization updates)."""
        if hasattr(self, "_org_cache"):
            delattr(self, "_org_cache")

    @property
    def org_name(self):
        """Get the organization name from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("org_name") if cache else None

    @property
    def logo(self):
        """Get the logo from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("logo") if cache else None

    @property
    def org_status(self):
        """Get the status from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("status") if cache else None

    def get_organization_doc(self):
        """Get the full Organization document."""
        if not self.organization:
            return None
        return frappe.get_doc("Organization", self.organization)
