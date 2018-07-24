from django.db import models
import datetime
__author__ = 'rdy'


class Group(models.Model):
    """
    ebt_group表
    """
    group_id = models.AutoField(max_length=11, primary_key=True, db_column='ebf_group_id')
    create_user = models.CharField(max_length=64, db_column='ebf_create_user')
    relate_project = models.IntegerField(max_length=11, default=0, db_column='ebf_relate_project_id')
    update_date = models.DateTimeField(datetime.datetime.utcnow, db_column='ebf_group_update_date')
    create_date = models.DateTimeField(datetime.datetime.utcnow, db_column='ebf_group_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_group'
        verbose_name = '产品组表'
