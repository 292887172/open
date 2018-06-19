from django.db import models
import datetime
__author__ = ''


class Protocol(models.Model):
    """
    ebt_factory_protocol表
    """
    protocol_id = models.AutoField(max_length=11,primary_key=True,db_column='ebf_fp_id')
    protocol_device_key = models.CharField(max_length=10,db_column='ebf_device_key')
    protocol_factory_type = models.IntegerField(max_length=2,default=0,db_column='ebf_factory_protocol_type')
    protocol_factory_content = models.TextField(db_column='ebf_factory_protocol_content')
    protocol_update_date = models.DateTimeField(datetime.datetime.utcnow(),db_column='ebf_df_update_date')
    protocol_create_date = models.DateTimeField(datetime.datetime.utcnow(),db_column='ebf_df_create_date')
    class Meta:
        app_label = 'center'
        db_table = 'ebt_factory_protocol'
        verbose_name = '协议表'
