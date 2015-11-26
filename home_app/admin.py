from django.contrib import admin
from models import *

# Register your models here.

@admin.register(HostInfo)
class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'hostname')

@admin.register(Monitoring_data)
class Monitoring_dataAdmin(admin.ModelAdmin):
    list_display = ('data_date', 'hostname', 'type')

# admin.site.register(HostInfo)
# admin.site.register(Monitoring_data)