from django.db import models


# Create your models here.
class Zone(models.Model):
    zone_id = models.AutoField(primary_key=True)
    zone_name = models.CharField(max_length=255)
    zone_description = models.TextField()
    zone_image = models.ImageField(upload_to='zone_images/')
    zone_status = models.IntegerField(default=1, choices=((1, '正常'), (0, '异常')))

    class Meta:
        verbose_name = '专区管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.zone_name
