from django.db import models
import datetime


class DocUi(models.Model):
    """
    ebt_doc_ui表
    """
    # ui产品编号
    ui_id = models.AutoField(primary_key=True, db_column='ebf_ui_id')
    # ui_上传编号
    ui_upload_id = models.IntegerField(max_length=2,default=0,db_column='ebf_ui_upload_id')
    # ui产品key
    ui_key = models.CharField(max_length=8, null=True, db_column='ebf_ui_key')
    # ui上传内容
    ui_content = models.TextField(max_length=512, db_column='ebf_ui_content')
    # ui上传类型（ui，protocol）
    ui_type = models.CharField(max_length=8, db_column='ebf_ui_type')
    # ui说明（版本代号1.1,1.2）
    ui_title = models.CharField(max_length=64, default=1.0, db_column='ebf_ui_title')
    # ui 计划
    ui_plan = models.CharField(max_length=64,default='',db_column='ebf_ui_plan')
    # ack 确认 0 非确认 1确认
    ui_ack = models.IntegerField(max_length=2,default=0,db_column='ebf_ui_ack')
    # 备注
    ui_remark = models.CharField(max_length=64,default='',db_column='ebf_ui_remark')
    # 负责方
    ui_party = models.CharField(max_length=64,db_column='ebf_ui_party')
    # 时间戳
    ui_time_stemp = models.TextField(max_length=32,db_column='ebf_ui_time_stemp')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_create_date')
    # 更新时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_doc_ui'
        verbose_name = 'UI上传记录表'
