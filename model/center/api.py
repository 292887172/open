__author__ = 'rdy'
from django.db import models


class Api(models.Model):
    """
    ebt_api表
    """
    # api编号
    api_id = models.AutoField(primary_key=True, db_column='ebf_api_id')
    # api地址
    api_url = models.CharField(max_length=2048, default='', db_column='ebf_api_url')
    # api 类型 (0:普通接口, 1:鉴权）
    api_type = models.IntegerField(max_length=3, default=0, db_column='ebf_api_type')
    # api 请求方式
    api_request_type = models.CharField(max_length=64, null=True, db_column='ebf_api_request_type')
    # api接口参数(json格式字符串)
    api_params = models.TextField(null=True, db_column='ebf_api_params')
    # api名称
    api_name = models.CharField(max_length=64, null=True, db_column='ebf_api_name')
    # api接口返回值（json格式字符串）
    api_return = models.TextField(null=True, db_column='ebf_api_return')
    # api接口描述
    api_describe = models.CharField(max_length=2048, null=True, db_column='ebf_api_describe')
    # 文档地址
    api_doc_url = models.CharField(max_length=128, null=True, db_column='ebf_api_doc_url')
    # 未获得权限时候提示的操作地址
    api_action_url = models.CharField(max_length=128, null=True, db_column='ebf_api_action_url')
    # api接口对应端口号
    api_port = models.IntegerField(default=80, db_column='ebf_api_port')
    # 接口分类
    api_classify = models.CharField(max_length=64, default="", db_column="ebf_api_classify")
    # 接口功能
    api_function = models.CharField(max_length=64, default="", db_column="ebf_api_function")
    # api接口等级（0：普通接口，1：高级接口，2：内部接口）
    api_level = models.IntegerField(max_length=3, default=0, db_column='ebf_api_level')
    # api接口分组（0：所有人可用接口，1：内部接口，2：某某类型伙伴接口）
    api_group = models.IntegerField(max_length=8, default=0, db_column='ebf_api_group')
    # 每日最大调用次数
    api_invoke_total = models.IntegerField(max_length=20, default=0, db_column="ebf_api_invoke_total")
    # 是否禁用(0:未禁用, 1:禁用)
    api_is_forbid = models.IntegerField(max_length=3, default=0, db_column='ebf_api_is_forbid')
    # api创建时间auto_now_add,为添加时的时间，更新对象时不会有变动,auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    api_create_date = models.DateTimeField(auto_now_add=True, db_column='ebf_api_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_api'
        verbose_name = 'api接口'
