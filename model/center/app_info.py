from django.db import models
import datetime


class AppInfo(models.Model):
    """
    ebt_app_info表
    """
    # 产品信息编号
    ai_id = models.AutoField(primary_key=True, db_column='ebf_ai_id')
    # 产品编号
    app_id = models.IntegerField(max_length=11, db_column='ebf_app_id')
    # 负责方对象{"responsible_party": []}
    responsible_party = models.TextField(null=True, db_column='ebf_responsible_party')
    # 负责人
    responsible_people = models.CharField(max_length=64, db_column='ebf_responsible_people')
    # 创建时间
    create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_ai_create_date')
    # 更新时间
    update_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_ai_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_app_info'
        verbose_name = '产品信息表'
