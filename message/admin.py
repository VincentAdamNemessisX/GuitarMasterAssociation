from django.contrib import admin
from message.models import Message


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id','sender_id','receiver_id','message_content','message_time','message_status','message_type']
