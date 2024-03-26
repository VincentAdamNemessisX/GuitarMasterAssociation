from django.db import models
from django.utils.html import format_html
import bs4


# Create your models here.
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    zone_id = models.ForeignKey('zone.Zone', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_image = models.ImageField(upload_to='post/%Y/%m', default='post/default.png')
    post_status = models.IntegerField(default=1, choices=((1, '正常'), (2, '审核中'), (3, '审核不通过')))
    post_layout_mode = models.CharField(default='normal', choices=(('normal', '普通'), ('immersion', '沉浸式')),
                                        max_length=20)
    post_view = models.IntegerField(default=0)
    post_like = models.IntegerField(default=0)
    post_create_time = models.DateTimeField(auto_now_add=True)
    post_update_time = models.DateTimeField(auto_now=True)

    def plain_content(self):
        soup = bs4.BeautifulSoup(self.post_content, 'html.parser')
        return soup.get_text()

    class Meta:
        db_table = 'post'
        verbose_name = '帖子管理'
        verbose_name_plural = verbose_name

    def pass_audit(self):
        parameter_str = 'post_id={}&post_status={}'.format(str(self.post_id), str(self.post_status))
        btn_str = '<a class="btn btn-xs btn-danger color-green" href="{}">' \
                  '<input style="background-color: green" name="通过审核"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="通过审核">' \
                  '</a>'
        return format_html(btn_str, '/api/post/pass/audit/?{}'.format(parameter_str))

    def reject_audit(self):
        parameter_str = 'post_id={}&post_status={}'.format(str(self.post_id), str(self.post_status))
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input style="background-color: red" name="拒绝审核"' \
                  'type="button" id="rejectButton"' \
                  'title="rejectButton" value="拒绝审核">' \
                  '</a>'
        return format_html(btn_str, '/api/post/reject/audit/?{}'.format(parameter_str))

    def __str__(self):
        return self.post_title


class PostLike(models.Model):
    post_like_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    post_like_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_like'
        verbose_name = '帖子点赞'
        verbose_name_plural = verbose_name
        unique_together = ('user_id', 'post_id')

    def __str__(self):
        return str(self.post_like_id)
