app_name = "dartwing"
app_title = "Dartwing"
app_publisher = "Opensoft"
app_description = "Dartwing backend API and family management"
app_email = "dev@dartwingers.com"
app_license = "MIT"
app_version = "0.1.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dartwing_frappe",
# 		"logo": "/assets/dartwing_frappe/logo.png",
# 		"title": "Dartwing Frappe",
# 		"route": "/dartwing_frappe",
# 		"has_permission": "dartwing_frappe.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dartwing_frappe/css/dartwing_frappe.css"
# app_include_js = "/assets/dartwing_frappe/js/dartwing_frappe.js"

# include js, css files in header of web template
# web_include_css = "/assets/dartwing_frappe/css/dartwing_frappe.css"
# web_include_js = "/assets/dartwing_frappe/js/dartwing_frappe.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dartwing_frappe/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dartwing_frappe/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dartwing_frappe.utils.jinja_methods",
# 	"filters": "dartwing_frappe.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dartwing_frappe.install.before_install"
# after_install = "dartwing_frappe.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dartwing_frappe.uninstall.before_uninstall"
# after_uninstall = "dartwing_frappe.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dartwing_frappe.utils.before_app_install"
# after_app_install = "dartwing_frappe.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dartwing_frappe.utils.before_app_uninstall"
# after_app_uninstall = "dartwing_frappe.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dartwing_frappe.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Organization": "dartwing.permissions.organization.get_permission_query_conditions",
	"Family": "dartwing.permissions.family.get_permission_query_conditions",
	"Family Member": "dartwing.permissions.family.get_member_permission_query_conditions",
	"Company": "dartwing.permissions.company.get_permission_query_conditions",
	"Association": "dartwing.permissions.association.get_permission_query_conditions",
	"Nonprofit": "dartwing.permissions.nonprofit.get_permission_query_conditions",
	# P2-02 FIX: Use consistent naming with _equipment suffix
	"Equipment": "dartwing.permissions.equipment.get_permission_query_conditions_equipment",
}

has_permission = {
	"Organization": "dartwing.permissions.organization.has_permission",
	"Family": "dartwing.permissions.family.has_permission",
	"Company": "dartwing.permissions.company.has_permission",
	"Association": "dartwing.permissions.association.has_permission",
	"Nonprofit": "dartwing.permissions.nonprofit.has_permission",
	# P2-02 FIX: Use consistent naming with _equipment suffix
	"Equipment": "dartwing.permissions.equipment.has_permission_equipment",
}

# Fixtures
# --------
# Data to be exported/imported during migrations

fixtures = [
	{
		"doctype": "Role",
		"filters": [["name", "in", [
			"Dartwing User",
			"Family Manager",
			"Family Admin",
			"Family Parent",
			"Family Teen",
			"Family Child",
			"Family Extended"
		]]]
	},
	{
		"doctype": "Role Template",
		"filters": []
	}
]

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# CR-011 FIX: Address deletion protection for Company links
doc_events = {
	"Address": {
		"before_delete": "dartwing.dartwing_company.utils.check_address_company_links"
	},
	"Org Member": {
		"after_insert": "dartwing.permissions.helpers.create_user_permissions",
		# P1-04 FIX: Reorder on_trash - check equipment first, then remove permissions
		"on_trash": [
			"dartwing.dartwing_core.doctype.equipment.equipment.check_equipment_assignments_on_member_removal",
			"dartwing.permissions.helpers.remove_user_permissions"
		],
		# P1-03 FIX: Add equipment check on status change (deactivation)
		# P2-NEW-03 FIX: Equipment check first to block deactivation before permission changes
		"on_update": [
			"dartwing.dartwing_core.doctype.equipment.equipment.check_equipment_assignments_on_member_deactivation",
			"dartwing.permissions.helpers.handle_status_change"
		],
	},
	"Person": {
		"on_trash": "dartwing.dartwing_core.doctype.org_member.org_member.handle_person_deletion"
	},
	"Organization": {
		"on_trash": "dartwing.dartwing_core.doctype.equipment.equipment.check_equipment_on_org_deletion"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dartwing_frappe.tasks.all"
# 	],
# 	"daily": [
# 		"dartwing_frappe.tasks.daily"
# 	],
# 	"hourly": [
# 		"dartwing_frappe.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dartwing_frappe.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dartwing_frappe.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dartwing_frappe.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dartwing_frappe.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dartwing_frappe.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dartwing_frappe.utils.before_request"]
# after_request = ["dartwing_frappe.utils.after_request"]

# Job Events
# ----------
# before_job = ["dartwing_frappe.utils.before_job"]
# after_job = ["dartwing_frappe.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dartwing_frappe.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

