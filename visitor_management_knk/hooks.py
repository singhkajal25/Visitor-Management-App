app_name = "visitor_management_knk"
app_title = "Visitors Management"
app_publisher = "Kanak Infosystems LLP"
app_description = "Visitors Management"
app_email = "sales@kanakinfosystems.com"
app_license = "mit"

# Apps
# ------------------

fixtures = [
    {"dt": "Web Page", "filters": [["module", "in", ["Visitors Management"]]]},
]

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "visitor_management_knk",
# 		"logo": "/assets/visitor_management_knk/logo.png",
# 		"title": "Visitors Management",
# 		"route": "/visitor_management_knk",
# 		"has_permission": "visitor_management_knk.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/visitor_management_knk/css/visitor_management_knk.css"
# app_include_js = "/assets/visitor_management_knk/js/visitor_management_knk.js"

# include js, css files in header of web template
# web_include_css = "/assets/visitor_management_knk/css/visitor_management_knk.css"
# web_include_js = "/assets/visitor_management_knk/js/visitor_management_knk.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "visitor_management_knk/public/scss/website"

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
# app_include_icons = "visitor_management_knk/public/icons.svg"

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
# 	"methods": "visitor_management_knk.utils.jinja_methods",
# 	"filters": "visitor_management_knk.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "visitor_management_knk.install.before_install"
# after_install = "visitor_management_knk.visitor_management_knk.doctype.visitor_pass.visitor_pass.ensure_workflow_exists"


after_migrate = [
    "visitor_management_knk.visitors_management.doctype.visitor_pass.visitor_pass.setup_visitor_pass_workflow"
]

# Uninstallation
# ------------

# before_uninstall = "visitor_management_knk.uninstall.before_uninstall"
# after_uninstall = "visitor_management_knk.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "visitor_management_knk.utils.before_app_install"
# after_app_install = "visitor_management_knk.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "visitor_management_knk.utils.before_app_uninstall"
# after_app_uninstall = "visitor_management_knk.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "visitor_management_knk.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"visitor_management_knk.tasks.all"
# 	],
# 	"daily": [
# 		"visitor_management_knk.tasks.daily"
# 	],
# 	"hourly": [
# 		"visitor_management_knk.tasks.hourly"
# 	],
# 	"weekly": [
# 		"visitor_management_knk.tasks.weekly"
# 	],
# 	"monthly": [
# 		"visitor_management_knk.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "visitor_management_knk.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "visitor_management_knk.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "visitor_management_knk.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["visitor_management_knk.utils.before_request"]
# after_request = ["visitor_management_knk.utils.after_request"]

# Job Events
# ----------
# before_job = ["visitor_management_knk.utils.before_job"]
# after_job = ["visitor_management_knk.utils.after_job"]

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
# 	"visitor_management_knk.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

