from django.db import models


# Create your models here.
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    zone_id = models.IntegerField()
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    post_status = models.IntegerField()
    post_view = models.IntegerField(default=0)
    post_like = models.IntegerField(default=0)
    post_comment = models.IntegerField(default=0)
    post_favorite = models.IntegerField(default=0)

    class Meta:
        verbose_name = '帖子管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.post_title
