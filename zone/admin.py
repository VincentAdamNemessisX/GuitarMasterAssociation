from django.contrib import admin
from zone.models import Zone


# Register your models here.
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['zone_id', 'zone_name', 'zone_description', 'zone_image', 'zone_status']