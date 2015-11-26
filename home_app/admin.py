from django.contrib import admin
from models import *

# Register your models here.

@admin.register(HostInfo)
class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'hostname')

@admin.register(Monitoring_data)
class Monitoring_dataAdmin(admin.ModelAdmin):
    list_display = ('data_date', 'get_hostname', 'type')

    def get_hostname(self, obj):
        return obj.hostname.hostname
    get_hostname.short_description = 'hostname'
    get_hostname.admin_order_field = 'hostinfo_hostname'

# admin.site.register(HostInfo)
# admin.site.register(Monitoring_data)