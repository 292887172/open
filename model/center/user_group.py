from django.db import models
from model.center.group import Group
import datetime
__author__ = 'rdy'


class UserGroup(models.Model):
    """
    ebt_user_group表
    """
    ug_id = models.AutoField(max_length=11, primary_key=True, db_column='ebf_ug_id')
    group = models.ForeignKey(Group, null=True, db_column='ebf_group_id', related_name='user_related_group')
    user_account = models.CharField(max_length=64, db_column='ebf_user_account')
    update_date = models.DateTimeField(datetime.datetime.utcnow, db_column='ebf_ug_update_date')
    create_date = models.DateTimeField(datetime.datetime.utcnow, db_column='ebf_ug_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_user_group'
        verbose_name = '用户组关联表'
