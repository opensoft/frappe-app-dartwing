// Copyright (c) 2025, Brett and contributors
// For license information, please see license.txt

frappe.ui.form.on("Company", {
	entity_type: function(frm) {
		// Warn if changing entity type when members/partners have been recorded
		if (!frm.is_new() && frm.doc.members_partners && frm.doc.members_partners.length > 0) {
			frappe.msgprint({
				title: __("Warning"),
				indicator: "orange",
				message: __(
					"Changing the entity type may affect the ownership section visibility. " +
					"The ownership section is only visible for LLC, Limited Partnership (LP), LLP, and General Partnership entity types."
				)
			});
		}
	}
	// CR-016 FIX: Removed redundant refresh handler that set organization read_only
	// The read_only property is already set in company.json
});
