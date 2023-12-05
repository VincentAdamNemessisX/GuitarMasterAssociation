from django.db import models


# Create your models here.
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField(db_index=True)
    receiver_id = models.IntegerField(db_index=True)
    message_content = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True, db_index=True)
    message_status = models.IntegerField(db_index=True)
    message_type = models.IntegerField()

    class Meta:
        verbose_name = '消息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message_content