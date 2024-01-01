# Register your models here.
from django.contrib import admin

from .models import Help


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ['help_id', 'help_title', 'help_content', 'help_time']
