from django.db import models

from model.center.api import Api


class Firmware(models.Model):
    """
    ebt_doc文档表
    """
    # 固件编号,不能为0
    firmware_id = models.AutoField(primary_key=True, db_column='ebf_firmware_id')
    # 固件名称名称
    firmware_name = models.CharField(null=True, max_length=64, db_column="ebf_firmware_filename")
    # 屏端固件url
    firmware_url = models.TextField(null=True, db_column='ebf_firmware_url')
    # 固件版本
    firmware_version = models.CharField(null=True,max_length=8,db_column='ebf_firmware_version')
    # 屏幕尺寸 1 6.8 2 5/4.3
    firmware_size = models.IntegerField(null=True,max_length=4,db_column='ebf_firmware_size')
    # 创建时间
    firmware_create_date = models.DateTimeField(null=True, db_column='ebf_firmware_create_time')
    # 更新时间
    firmware_update_date = models.DateTimeField(null=True, db_column='ebf_firmware_update_time')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_firmware'
        verbose_name = '固件'
