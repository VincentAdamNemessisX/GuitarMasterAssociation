from django.db import models


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    review_content = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)
    parent_id = models.IntegerField()
    review_like = models.IntegerField(default=0)
    review_type = models.IntegerField()
    review_status = models.IntegerField()
    review_time_index = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.review_content
