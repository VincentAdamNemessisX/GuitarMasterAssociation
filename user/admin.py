from django.contrib import admin, messages

from .models import User, RecentBrowsing


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_name', 'user_email', 'user_phone', 'user_status', 'user_create_time',
                    'user_update_time', 'freeze', 'unfreeze']
    list_filter = ['user_status', 'user_create_time', 'user_status']
    list_display_links = ['user_id', 'user_name']
    actions = ['freeze_batch', 'unfreeze_batch']

    def freeze_batch(self, request, queryset):
        for obj in queryset:
            if obj.user_status == 2:
                continue
            obj.user_status = 2
            obj.save()
        self.message_user(request, '已冻结！', level='warning')

    freeze_batch.short_description = '冻结'

    def unfreeze_batch(self, request, queryset):
        for obj in queryset:
            if obj.user_status == 1:
                continue
            obj.user_status = 1
            obj.save()
        self.message_user(request, '已解冻！', messages.SUCCESS)

    unfreeze_batch.short_description = '解冻'


@admin.register(RecentBrowsing)
class RecentAdmin(admin.ModelAdmin):
    list_display = ['recent_id', 'recent_user_id', 'recent_post_id', 'recent_browsing_time']
    list_filter = ['recent_browsing_time', 'recent_user_id', 'recent_post_id']
    list_display_links = ['recent_id', 'recent_user_id', 'recent_post_id']
