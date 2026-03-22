from django.contrib import admin
from django.urls import path
from deproke.analytics import dashboard_analytics

# Extend admin URLs
original_get_urls = admin.site.__class__.get_urls

def custom_get_urls(self):
    urls = original_get_urls(self)
    custom = [path('analytics/', dashboard_analytics, name='analytics_dashboard')]
    return custom + urls

admin.site.__class__.get_urls = custom_get_urls
admin.site.index_title = 'Deproke Administration'
admin.site.site_header = 'Deproke Admin'
admin.site.site_title = 'Deproke'
