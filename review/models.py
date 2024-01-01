from django.db import models
from django.utils.html import format_html


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

    def pass_audit(self):
        parameter_str = 'review_id={}&review_status={}'.format(str(self.review_id), str(self.review_status))
        btn_str = '<a class="btn btn-xs btn-danger color-green" href="{}">' \
                  '<input style="background-color: green" name="通过审核"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="通过审核">' \
                  '</a>'
        return format_html(btn_str, '/api/review/pass/audit/?{}'.format(parameter_str))

    def reject_audit(self):
        parameter_str = 'review_id={}&review_status={}'.format(str(self.review_id), str(self.review_status))
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input style="background-color: red" name="拒绝审核"' \
                  'type="button" id="rejectButton"' \
                  'title="rejectButton" value="拒绝审核">' \
                  '</a>'
        return format_html(btn_str, '/api/review/reject/audit/?{}'.format(parameter_str))

    def __str__(self):
        return self.review_content
