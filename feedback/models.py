from django.contrib.auth.models import User as Admin_User
from django.db import models


# Create your models here.
class Help(models.Model):
    help_id = models.AutoField(primary_key=True)
    help_title = models.CharField(max_length=100)
    help_content = models.TextField()
    help_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'help'
        verbose_name = '帮助管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.help_title
