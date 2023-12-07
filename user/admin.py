from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_name', 'user_email', 'user_phone', 'user_status', 'user_create_time', 'user_update_time']
