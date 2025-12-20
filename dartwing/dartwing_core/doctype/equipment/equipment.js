// Copyright (c) 2025, Opensoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Equipment", {
    refresh: function(frm) {
        // Set query filter for assigned_to on form load
        frm.trigger("set_assigned_to_query");
        // Store original org for change detection
        frm._last_owner_org = frm.doc.owner_organization;
    },

    owner_organization: function(frm) {
        // Update assigned_to query when organization changes
        frm.trigger("set_assigned_to_query");

        // Clear assigned_to if organization changes (person may not be valid for new org)
        // P2-08 FIX: Use tracked value for reliable change detection
        if (frm.doc.assigned_to && frm._last_owner_org && frm._last_owner_org !== frm.doc.owner_organization) {
            frm.set_value("assigned_to", null);
        }
        frm._last_owner_org = frm.doc.owner_organization;
    },

    set_assigned_to_query: function(frm) {
        // P2-08 FIX: Disable assigned_to and show helpful message when no org selected
        if (!frm.doc.owner_organization) {
            frm.set_df_property("assigned_to", "read_only", 1);
            frm.set_df_property("assigned_to", "description", "Select an organization first to enable assignment");
            return;
        }

        // Enable the field and clear description when org is selected
        frm.set_df_property("assigned_to", "read_only", 0);
        frm.set_df_property("assigned_to", "description", "");

        // Filter assigned_to field to show only active Org Members of the selected organization
        frm.set_query("assigned_to", function() {
            return {
                query: "dartwing.dartwing_core.doctype.equipment.equipment.get_org_members",
                filters: {
                    organization: frm.doc.owner_organization
                }
            };
        });
    }
});
