from django.contrib import admin

from review.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'user_id', 'post_id', 'review_content', 'review_time', 'parent_id',
                    'review_status', 'review_time_index']
