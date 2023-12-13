from django.db import models
from django.utils import timezone


# Create your models here.
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    collection_create_time = models.DateTimeField(auto_now_add=True)
    collection_status = models.IntegerField(default=1, choices=((1, '正常'), (0, '删除')))
    collection_time_index = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'collection'
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.collection_id)
