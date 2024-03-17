from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

class KilianAdminSite(admin.AdminSite):
    site_header = "Kilians kleine Hütte Administration Center"
    site_title = "Kilians Admin"
    index_title = "Welcome! Kilian master!"

class KilianAdminConfig(AdminConfig):
    default_site = "project.admin.KilianAdminSite"