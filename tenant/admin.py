from django.contrib import admin

from tenant.models import *


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location',)   

admin.site.register(Tenant, TenantAdmin)


class PortAdmin(admin.ModelAdmin):
    list_display = ('port_number', 'is_allocated',)
    list_filter = ('is_allocated',)

admin.site.register(Port, PortAdmin)

class TenantPortAssignmentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'port',)

admin.site.register(TenantPortAssignment, TenantPortAssignmentAdmin)