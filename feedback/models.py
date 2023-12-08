from django.db import models
from django.contrib.auth.models import User as Admin_User


# Create your models here.
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    admin_id = models.ForeignKey(Admin_User, on_delete=models.CASCADE)
    feedback_content = models.TextField()
    feedback_time = models.DateTimeField(auto_now_add=True, db_index=True)
    feedback_reply = models.TextField(null=True, blank=True)
    feedback_rate = models.IntegerField(default=0)
    feedback_status = models.IntegerField(default=1, choices=((0, '已解决'), (1, '待解决')))

    class Meta:
        db_table = 'feedback'
        verbose_name = '反馈管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.feedback_id)
