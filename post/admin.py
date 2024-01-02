from django.contrib import admin, messages

from post.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['zone_id', 'post_title', 'post_layout_mode', 'post_status', 'post_view', 'post_like',
                    'post_create_time', 'pass_audit', 'reject_audit']
    list_filter = ['post_status', 'post_create_time', 'post_update_time', 'zone_id']
    actions = ['pass_audit_batch', 'reject_audit_batch']

    def pass_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.post_status == 1:
                continue
            obj.post_status = 1
            obj.save()
        self.message_user(request, '审核通过', messages.SUCCESS)

    pass_audit_batch.short_description = '通过审核'

    def reject_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.post_status == 3:
                continue
            obj.post_status = 3
            obj.save()
        self.message_user(request, '审核不通过', messages.WARNING)

    reject_audit_batch.short_description = '拒绝通过'
