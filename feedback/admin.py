# Register your models here.
from django.contrib import admin

from .models import Feedback, Help


@admin.register(Feedback)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['feedback_id', 'user_id', 'admin_id', 'feedback_content', 'feedback_time', 'feedback_reply',
                    'feedback_rate', 'feedback_status']


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ['help_id', 'help_title', 'help_content', 'help_time']