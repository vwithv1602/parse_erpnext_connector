# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "parse_erpnext_connector"
app_title = "Parse Erpnext Connector"
app_publisher = "vavcoders"
app_description = "Parses response from ERPNext connectors like shopclues, amazon which makes developing connectors much more easy."
app_icon = "octicon octicon-git-compare"
app_color = "#3498db"
app_email = "vavcoders@gmail.com"
app_license = "license.txt"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/parse_erpnext_connector/css/parse_erpnext_connector.css"
# app_include_js = "/assets/parse_erpnext_connector/js/parse_erpnext_connector.js"

# include js, css files in header of web template
# web_include_css = "/assets/parse_erpnext_connector/css/parse_erpnext_connector.css"
# web_include_js = "/assets/parse_erpnext_connector/js/parse_erpnext_connector.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "parse_erpnext_connector.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "parse_erpnext_connector.install.before_install"
# after_install = "parse_erpnext_connector.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "parse_erpnext_connector.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"parse_erpnext_connector.tasks.all"
# 	],
# 	"daily": [
# 		"parse_erpnext_connector.tasks.daily"
# 	],
# 	"hourly": [
# 		"parse_erpnext_connector.tasks.hourly"
# 	],
# 	"weekly": [
# 		"parse_erpnext_connector.tasks.weekly"
# 	]
# 	"monthly": [
# 		"parse_erpnext_connector.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "parse_erpnext_connector.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "parse_erpnext_connector.event.get_events"
# }

