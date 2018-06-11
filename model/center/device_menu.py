__author__ = ''
import datetime

from django.db import models



class DeviceMenu(models.Model):
    device_menu_id = models.AutoField(primary_key=True, db_column='ebf_dm_id')
    device_type = models.IntegerField(max_length=11,default='',db_column='ebf_device_type')
    device_key = models.CharField(max_length=8,default='',db_column='ebf_device_key')
    menu_name = models.CharField(max_length=64,db_column='ebf_dm_name')
    menu_url = models.CharField(max_length=2048,default="#",db_column='ebf_dm_url')
    update_time = models.DateTimeField(datetime.datetime.utcnow(),db_column='ebf_dm_update_date')
    create_time = models.DateTimeField(datetime.datetime.utcnow(),db_column='ebf_dm_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_device_menu'
        verbose_name = '设备菜单目录'
