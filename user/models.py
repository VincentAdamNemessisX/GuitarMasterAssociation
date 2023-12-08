from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True, db_index=True)
    user_password = models.CharField(max_length=20)
    user_email = models.CharField(max_length=30, unique=True, db_index=True)
    user_phone = models.CharField(max_length=11, unique=True, db_index=True)
    user_status = models.IntegerField(default=1)
    user_create_time = models.DateTimeField(auto_now_add=True)
    user_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name
