from django.contrib import admin

from collection.models import Collection


# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['collection_id', 'user_id', 'post_id', 'collection_create_time', 'collection_status',
                    'collection_time_index']
