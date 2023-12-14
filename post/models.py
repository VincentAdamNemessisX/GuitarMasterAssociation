from django.db import models


# Create your models here.
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    zone_id = models.ForeignKey('zone.Zone', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_image = models.ImageField(upload_to='post/%Y/%m', default='post/default.png')
    post_status = models.IntegerField(default=1, choices=((1, '正常'), (2, '审核中'), (3, '审核不通过')))
    post_view = models.IntegerField(default=0)
    post_like = models.IntegerField(default=0)
    post_comment = models.IntegerField(default=0)
    post_favorite = models.IntegerField(default=0)
    post_create_time = models.DateTimeField(auto_now_add=True)
    post_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        verbose_name = '帖子管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.post_title
