from django.db import models
import datetime


class AppPlan(models.Model):
    """
    ebf_app_plan
    """
    # ui产品编号
    ui_app_id = models.AutoField(primary_key=True, db_column='ebf_ui_id')
    # ui_上传编号
    ui_plan_id = models.IntegerField(max_length=2, default=0, db_column='ebf_ui_upload_id')
    # ui产品key
    ui_plan_key = models.CharField(max_length=8, null=True, db_column='ebf_ui_key')
    # ui产品任务

    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_create_date')
    # 更新时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_ui_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_doc_ui'
        verbose_name = 'UI上传记录表'