from django.db import models
import datetime
__author__ = 'rdy'


class Message(models.Model):
    """
    ebt_message表
    """
    # 消息编号
    message_id = models.AutoField(primary_key=True, db_column='ebf_message_id')
    # 消息内容
    message_content = models.CharField(max_length=512, db_column='ebf_message_content')
    # 消息类型
    message_type = models.IntegerField(max_length=2, default=1, db_column='ebf_message_type')
    # 发送者
    message_sender = models.CharField(max_length=64, db_column='ebf_message_sender')
    # 消息接收者
    message_target = models.CharField(max_length=64, db_column='ebf_message_target')
    # 是否阅读
    is_read = models.IntegerField(max_length=2, default=0, db_column='ebf_is_read')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_message_create_date')
    # 更新时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_message_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_message'
        verbose_name = '消息表'
