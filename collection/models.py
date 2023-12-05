from django.db import models


# Create your models here.
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    # post_id = models.IntegerField(db_index=True)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    collection_time = models.DateTimeField(auto_now_add=True)
    collection_status = models
    collection_time_index = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.collection_id
