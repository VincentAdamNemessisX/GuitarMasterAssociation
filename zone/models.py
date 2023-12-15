from django.db import models


# Create your models here.
class Zone(models.Model):
    zone_id = models.AutoField(primary_key=True)
    zone_name = models.CharField(max_length=255)
    zone_description = models.TextField()
    zone_image = models.ImageField(upload_to='zone_images/')
    zone_layout_mode = models.IntegerField(default=1,
                                           choices=((1, '普通'), (2, '融合'), (3, '普通排行'), (4, '融合排行'), (5, '普通沉浸排行')))
    zone_status = models.IntegerField(default=1, choices=((1, '正常'), (0, '异常')))

    class Meta:
        db_table = 'zone'
        verbose_name = '专区管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.zone_name
