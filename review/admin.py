from django.contrib import admin

from review.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'post_id', 'review_content', 'review_time', 'parent_id',
                    'review_status', 'pass_audit', 'reject_audit']
    list_filter = ['review_status', 'user_id', 'post_id', 'review_time', 'parent_id']
    search_fields = ['review_content', 'user_id', 'post_id']
    actions = ['pass_audit_batch', 'reject_audit_batch']

    def pass_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.review_status == 1:
                continue
            obj.review_status = 1
            obj.save()
        self.message_user(request, '审核通过', level='success')

    pass_audit_batch.short_description = '通过审核'

    def reject_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.review_status == 3:
                continue
            obj.review_status = 3
            obj.save()
        self.message_user(request, '审核不通过', level='warning')

    reject_audit_batch.short_description = '拒绝通过'
