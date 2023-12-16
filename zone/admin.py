from django.contrib import admin

from zone.models import Zone


# Register your models here.
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['zone_id', 'zone_name', 'zone_layout_mode', 'zone_create_time', 'zone_last_active_time', 'zone_description', 'zone_image', 'zone_status']
