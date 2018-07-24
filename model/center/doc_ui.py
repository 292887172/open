from django.db import models
import datetime


class DocUi(models.Model):
    """
    ebt_doc_ui表
    """
    # ui产品编号
    ui_id = models.AutoField(primary_key=True, db_column='ebf_ui_id')
    # ui产品key
    ui_key = models.CharField(max_length=8, null=True, db_column='ebf_ui_key')
    # ui上传内容
    ui_content = models.TextField(max_length=512, db_column='ebf_ui_content')
    # ui上传类型（ui，protocol）
    ui_type = models.CharField(max_length=8, db_column='ebf_ui_type')
    # ui说明（版本代号1.1,1.2）
    ui_title = models.CharField(max_length=64, default=1.0, db_column='ebf_ui_title')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_create_date')
    # 更新时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_doc_ui'
        verbose_name = 'UI上传记录表'
