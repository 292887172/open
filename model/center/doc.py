__author__ = 'rdy'

from django.db import models

from model.center.api import Api


class Doc(models.Model):
    """
    ebt_doc文档表
    """
    # 文档编号,不能为0
    doc_id = models.AutoField(primary_key=True, db_column='ebf_doc_id')
    # 文档名称
    doc_name = models.CharField(null=True, max_length=64, db_column="ebf_doc_name")
    # 接口编号
    api_id = models.ForeignKey(Api, null=True, db_column='ebf_api_id')
    # 接口文档（Markdown源码，保存示例代码和详细说明）
    doc_markdown = models.TextField(null=True, db_column='ebf_doc_markdown')
    # 文档生成的html源码或者url地址
    doc_html = models.TextField(null=True, db_column='ebf_doc_html')
    # 文档类型（0：普通文档，1：内部加密文档）
    doc_type = models.IntegerField(max_length=2, default=0, db_column='ebf_doc_type')
    # 创建时间，auto_now_add,为添加时的时间，更新对象时不会有变动,auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    doc_create_date = models.DateTimeField(auto_now_add=True, db_column='ebf_doc_create_date')
    # 更新时间
    doc_update_date = models.DateTimeField(auto_now=True, db_column='ebf_doc_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_doc'
        verbose_name = '文档'
