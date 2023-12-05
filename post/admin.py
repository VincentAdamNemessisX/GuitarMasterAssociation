from django.contrib import admin
from post.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'user_id', 'zone_id', 'post_title', 'post_time', 'post_status', 'post_view', 'post_like', 'post_comment', 'post_favorite']