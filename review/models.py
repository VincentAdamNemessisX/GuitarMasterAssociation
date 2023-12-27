from django.db import models


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post_id = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    review_content = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    review_status = models.IntegerField(default=1, choices=((1, '正常'), (2, '审核中'), (3, '审核不通过')))
    review_time_index = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'review'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.review_content
