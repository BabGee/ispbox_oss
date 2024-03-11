from django.contrib import admin

from tenant.models import *


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'ip_address', 'port') 
    list_filter = ('port',)  

admin.site.register(Tenant, TenantAdmin)
