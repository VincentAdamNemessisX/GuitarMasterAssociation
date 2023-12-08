from django.db import models
from django.contrib.auth.models import User as Admin_User


# Create your models here.
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(Admin_User, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    message_content = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True, db_index=True)
    message_status = models.IntegerField(default=1, choices=((1, '已读'), (0, '未读')), db_index=True)

    class Meta:
        db_table = 'message'
        verbose_name = '消息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message_content
