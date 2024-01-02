from django.db import models
from django.utils.html import format_html


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True, db_index=True)
    user_password = models.CharField(max_length=128)
    user_email = models.CharField(max_length=30, db_index=True)
    user_wechat = models.CharField(max_length=16, default='', blank=True)
    user_qq = models.CharField(max_length=12, default='', blank=True)
    user_phone = models.CharField(max_length=11, db_index=True)
    user_nickname = models.CharField(max_length=20, default='', blank=True)
    user_sex = models.IntegerField(default=0, choices=((1, '男'), (2, '女'), (0, '保密')))
    user_status = models.IntegerField(default=1, choices=((1, '正常'), (2, '冻结')))
    user_headicon = models.ImageField(upload_to='user_headicon', default='user_headicon/default.png')
    user_description = models.CharField(max_length=200, default='', blank=True)
    user_create_time = models.DateTimeField(auto_now_add=True)
    user_update_time = models.DateTimeField(auto_now=True)
    user_last_active_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def freeze(self):
        parameter_str = 'user_id={}&user_status={}'.format(str(self.user_id), str(self.user_status))
        btn_str = '<a class="btn btn-xs btn-danger color-green" href="{}">' \
                  '<input style="background-color: green" name="冻结"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="冻结">' \
                  '</a>'
        return format_html(btn_str, '/api/user/freeze/?{}'.format(parameter_str))

    def unfreeze(self):
        parameter_str = 'user_id={}&user_status={}'.format(str(self.user_id), str(self.user_status))
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input style="background-color: red" name="解冻"' \
                  'type="button" id="rejectButton"' \
                  'title="rejectButton" value="解冻">' \
                  '</a>'
        return format_html(btn_str, '/api/user/unfreeze/?{}'.format(parameter_str))

    def __str__(self):
        return self.user_name


class RecentBrowsing(models.Model):
    recent_id = models.AutoField(primary_key=True)
    recent_user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    recent_post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    recent_browsing_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recent_browsing'
        verbose_name = '最近浏览'
        verbose_name_plural = verbose_name
        unique_together = ('recent_post_id', 'recent_user_id')

    def __str__(self):
        return str(self.recent_id)
