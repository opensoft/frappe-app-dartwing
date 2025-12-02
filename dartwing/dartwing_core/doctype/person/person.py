# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

try:
    import phonenumbers
    from phonenumbers import NumberParseException

    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False

# Module-level cache for Org Member DocType existence
# Avoids repeated database queries on every Person deletion
_org_member_doctype_exists_cache = None


def _has_org_member_doctype() -> bool:
    """Check if Org Member DocType exists (cached).

    Caches the result at module level to avoid repeated database queries.
    DocType existence is unlikely to change during runtime.

    Returns:
        bool: True if Org Member DocType exists, False otherwise
    """
    global _org_member_doctype_exists_cache
    if _org_member_doctype_exists_cache is None:
        _org_member_doctype_exists_cache = frappe.db.exists("DocType", "Org Member")
    return bool(_org_member_doctype_exists_cache)


class Person(Document):
    """Person DocType - foundational identity layer for Dartwing.

    Links individuals to Frappe Users (system access), Keycloak (external auth),
    and Organizations.
    """

    def validate(self):
        """Validate Person record before save."""
        self._validate_unique_keycloak_user_id()
        self._validate_unique_frappe_user()
        self._validate_mobile_no()
        self._validate_status_transition()
        self._check_minor_consent_block()

    def before_save(self):
        """Compute derived fields before save."""
        self._compute_full_name()

    def after_insert(self):
        """Trigger User auto-creation when keycloak_user_id is set (FR-011)."""
        self._trigger_user_auto_creation()

    def before_delete(self):
        """Prevent deletion if linked to Org Member (FR-006)."""
        self._check_org_member_links()

    def _check_org_member_links(self):
        """Check for Org Member links and block deletion if found.

        Per FR-006: System MUST prevent deletion of Person records that
        are linked to Org Member records.
        """
        # Early return if "Org Member" doctype does not exist (cached check).
        # This check is critical: without the doctype, there can be no links,
        # and attempting to query it would cause errors. This preserves security/integrity
        # and prevents accidental deletion-blocking logic from failing unexpectedly.
        if not _has_org_member_doctype():
            return

        linked_org_members = frappe.get_all(
            "Org Member", filters={"person": self.name}, limit=1
        )

        if linked_org_members:
            frappe.throw(
                _(
                    "Cannot delete Person linked to Org Member. "
                    "Please deactivate or merge instead."
                ),
                frappe.LinkExistsError,
            )

    def _trigger_user_auto_creation(self):
        """Auto-create Frappe User when keycloak_user_id is set and enabled.

        Per FR-011: System MUST auto-create a Frappe User with default
        'Dartwing User' role when keycloak_user_id is present, no frappe_user
        exists, and auto-creation is enabled by site configuration.
        """
        if not self.keycloak_user_id:
            return

        if self.frappe_user:
            return

        from dartwing.utils.person_sync import is_auto_creation_enabled, queue_user_sync

        # Check if auto-creation is enabled
        if not is_auto_creation_enabled():
            return

        # Set initial sync status and queue the job
        self.user_sync_status = "pending"
        self.db_set("user_sync_status", "pending", update_modified=False)
        queue_user_sync(self.name, attempt=1)

    def _validate_unique_keycloak_user_id(self):
        """Enforce uniqueness on keycloak_user_id when set (FR-002).

        Frappe's unique constraint allows multiple NULLs but we add explicit
        validation for better error messages.
        """
        if self.keycloak_user_id:
            existing = frappe.db.get_value(
                "Person",
                {"keycloak_user_id": self.keycloak_user_id, "name": ["!=", self.name]},
            )
            if existing:
                frappe.throw(
                    _(
                        "Keycloak User ID {0} is already linked to another Person"
                    ).format(self.keycloak_user_id),
                    frappe.DuplicateEntryError,
                )

    def _validate_unique_frappe_user(self):
        """Enforce uniqueness on frappe_user when set (FR-003).

        Frappe's unique constraint allows multiple NULLs but we add explicit
        validation for better error messages.
        """
        if self.frappe_user:
            existing = frappe.db.get_value(
                "Person", {"frappe_user": self.frappe_user, "name": ["!=", self.name]}
            )
            if existing:
                frappe.throw(
                    _("Frappe User {0} is already linked to another Person").format(
                        self.frappe_user
                    ),
                    frappe.DuplicateEntryError,
                )

    def _validate_mobile_no(self):
        """Validate and normalize mobile_no to E.164 format (FR-010)."""
        if not self.mobile_no:
            return

        if not HAS_PHONENUMBERS:
            # Skip validation if phonenumbers library not available
            return

        try:
            # Parse with default country (US) - can be overridden by international format
            parsed = phonenumbers.parse(self.mobile_no, "US")
            if not phonenumbers.is_valid_number(parsed):
                frappe.throw(_("Invalid mobile number format"), frappe.ValidationError)

            # Normalize to E.164 format
            self.mobile_no = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
        except NumberParseException:
            frappe.throw(_("Invalid mobile number"), frappe.ValidationError)

    def _check_minor_consent_block(self):
        """Block updates to minor's record if consent not captured (FR-013).

        Exceptions:
        1. Consent capture operation (consent_captured, consent_timestamp)
        2. System user sync updates (frappe_user, user_sync_status, last_sync_at, sync_error_message)
        """
        if self.is_new():
            return

        if self.is_minor and not self.consent_captured:
            # Get all changed fields
            valid_columns = self.meta.get_valid_columns()
            changed_fields = {
                field for field in valid_columns if self.has_value_changed(field)
            }

            # Always allow modifications of audit fields
            audit_fields = {"modified", "modified_by"}
            changed_fields_without_audit = changed_fields - audit_fields

            # Exception 1: Check if this is a consent capture operation
            if self.has_value_changed("consent_captured") and self.consent_captured:
                # Authentication check: Only allow if current user is NOT the minor
                if (
                    hasattr(self, "frappe_user")
                    and self.frappe_user is not None
                    and frappe.session.user == self.frappe_user
                ):
                    frappe.throw(
                        _(
                            "Minors cannot capture their own consent. Only an authorized parent or guardian may perform this operation."
                        ),
                        frappe.PermissionError,
                    )
                # Validate that ONLY consent-related fields are being modified
                allowed_consent_fields = {"consent_captured", "consent_timestamp"}
                unauthorized_changes = changed_fields_without_audit - allowed_consent_fields
                if unauthorized_changes:
                    frappe.throw(
                        _(
                            "During consent capture, only consent_captured and consent_timestamp may be modified. "
                            "Attempted to modify: {0}"
                        ).format(", ".join(sorted(unauthorized_changes))),
                        frappe.PermissionError,
                    )

                return  # Allow consent capture

            # Exception 2: Check if this is a system user sync update
            allowed_sync_fields = {
                "frappe_user",
                "user_sync_status",
                "last_sync_at",
                "sync_error_message",
            }
            if changed_fields_without_audit and changed_fields_without_audit.issubset(allowed_sync_fields):
                # This is a system sync operation - allow it
                return

            # No valid exception - block the update
            frappe.throw(
                _("Cannot modify Person record for a minor until consent is captured"),
                frappe.PermissionError,
            )

    def _compute_full_name(self):
        """Compute full_name from first_name + last_name."""
        parts = [self.first_name, self.last_name]
        self.full_name = " ".join(filter(None, parts))

    def _validate_status_transition(self):
        """Validate status transitions (T029).

        Allowed transitions per data-model.md:
        - (new) → Active: Default on creation
        - Active → Inactive: Deactivate person
        - Inactive → Active: Reactivate person
        - Active → Merged: Merge into another person
        - Inactive → Merged: Merge into another person

        Merged is a terminal state - no transitions allowed from it.
        """
        if self.is_new():
            return

        old_status = self.get_db_value("status")
        new_status = self.status

        if old_status == new_status:
            return

        # Merged is terminal - no transitions allowed
        if old_status == "Merged":
            frappe.throw(
                _("Cannot change status of a merged Person record"),
                frappe.ValidationError,
            )

        # All other transitions are allowed per the state machine
        valid_transitions = {
            "Active": ["Inactive", "Merged"],
            "Inactive": ["Active", "Merged"],
        }

        if new_status not in valid_transitions.get(old_status, []):
            frappe.throw(
                _("Invalid status transition from {0} to {1}").format(
                    old_status, new_status
                ),
                frappe.ValidationError,
            )


def get_list_filters():
    """Return default filters to exclude Merged persons from list queries (T034).

    Usage in hooks.py or custom scripts:
        from dartwing.dartwing_core.doctype.person.person import get_list_filters
    """
    return {"status": ["!=", "Merged"]}
