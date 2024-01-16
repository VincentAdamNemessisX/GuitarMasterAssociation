from django.contrib import admin

from collection.models import Collection

admin.site.site_header = '吉他爱好者兴趣社区后台'
admin.site.site_title = '吉他爱好者兴趣社区后台'
admin.site.index_title = '吉他爱好者兴趣社区后台'


# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['collection_id', 'user_id', 'post_id', 'collection_create_time',
                    'collection_time_index']
