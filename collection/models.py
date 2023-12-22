from django.db import models


# Create your models here.
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    collection_create_time = models.DateTimeField(auto_now_add=True)
    collection_time_index = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'collection'
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name
        unique_together = ('user_id', 'post_id')

    def __str__(self):
        return str(self.collection_id)
