__author__ = 'rdy'
import datetime

from django.db import models
from model.center.doc import Doc


class DocMenu(models.Model):
    """
    ebt_doc_menu文档菜单表
    """
    # 文档菜单编号
    dm_id = models.AutoField(primary_key=True, db_column='ebf_dm_id')
    # 接口编号
    doc_id = models.ForeignKey(Doc, null=True, db_column='ebf_doc_id')
    # 菜单名称
    dm_name = models.CharField(max_length=64, db_column='ebf_dm_name')
    # 是否为目录菜单（0：非目录菜单，1：目录菜单）
    dm_is_parent = models.IntegerField(max_length=2, default=0, db_column='ebf_dm_is_parent')
    # 菜单url地址
    dm_url = models.CharField(max_length=2048, default="#", db_column='ebf_dm_url')
    # 菜单样式
    dm_class = models.CharField(max_length=64, null=True, db_column='ebf_dm_class')
    # 菜单深度（1：一级菜单，2：二级菜单）
    dm_depth = models.IntegerField(max_length=2, default=0, db_column='ebf_dm_depth')
    # 排序序号（排序只针对同一目录下的同级菜单有效）
    dm_order_num = models.IntegerField(default=0, db_column='ebf_dm_ordernum')
    # 上级菜单编号（根目录的上级菜单为0）
    dm_parent_id = models.IntegerField(default=0, db_column='ebf_dm_parent_id')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_doc_menu'
        verbose_name = '文档目录'
