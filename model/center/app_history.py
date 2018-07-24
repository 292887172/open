__author__ = 'rdy'
import datetime
from model.center.developer import Developer
from django.db import models


class AppHistory(models.Model):
    """
    ebt_app——history应用历史记录表
    """
    # app编号
    app_id = models.AutoField(primary_key=True, db_column='ebf_app_id')
    # 开发者编号
    developer = models.ForeignKey(Developer, null=True, db_column='ebf_developer_id', related_name="app_related_apphistory")
    # 应用名称
    app_name = models.CharField(max_length=64, db_column='ebf_app_name')
    # 应用描述
    app_describe = models.TextField(null=True, db_column='ebf_app_describe')
    # 应用描述网站
    app_site = models.CharField(max_length=512, default='', db_column="ebf_app_site")
    # 应用图标url地址
    app_logo = models.CharField(max_length=2048, null=True, db_column='ebf_app_logo')
    # 操作类型（1：添加，2：修改，3：删除）
    app_action = models.IntegerField(max_length=2, null=True, db_column='ebf_app_action')
    # 应用审核状态（0：审核中，1：审核通过，-1：审核未通过）
    check_status = models.IntegerField(max_length=2, null=True, db_column='ebf_app_check_status')
    # 审核备注
    check_remarks = models.CharField(max_length=1024, null=True, db_column='ebf_app_check_remarks')
    # appid
    app_appid = models.CharField(max_length=512, db_column='ebf_app_appid')
    # appsecret
    app_appsecret = models.CharField(max_length=1024, db_column='ebf_app_appsecret')
    # 应用是否禁用 （0：未禁用，1：禁用）
    app_is_forbid = models.IntegerField(max_length=2, default=0, db_column='ebf_app_is_forbid')
    # 设备品牌
    app_brand = models.CharField(max_length=64, null=True, db_column='ebf_app_brand')
    # 设备类别
    app_category = models.CharField(max_length=64, null=True, db_column='ebf_app_category')
    # 设备型号
    app_model = models.CharField(max_length=64, null=True, db_column='ebf_app_model')
    # 应用等级
    app_level = models.IntegerField(max_length=3, default=0, db_column='ebf_app_level')
    # 应用分组
    app_group = models.IntegerField(max_length=8, default=0, db_column='ebf_app_group')
    # 设备消息推送地址
    app_push_url = models.CharField(max_length=2048, null=True, db_column='ebf_app_push_url')
    # 设备消息推送地址
    app_push_token = models.CharField(max_length=2048, null=True, db_column='ebf_app_push_token')
    # 设备类型（0：未知,1：油烟机，2：集成灶，3：冰柜，4：洗衣机）
    app_device_type = models.IntegerField(max_length=2, default=0, db_column='ebf_app_device_type')
    # 设备默认配置
    device_conf = models.TextField(null=True, db_column='ebf_device_conf')
    # 协议类型（1:53iq协议，2：阿里小智协议，3：京东协议）
    app_protocol_type = models.IntegerField(max_length=2, default=1, db_column='ebf_app_protocol_type')
    # 应用创建时间
    app_create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_app_create_date')
    # 应用更新时间
    app_update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_app_update_date')
    # 应用删除时间
    app_delete_date = models.DateTimeField(auto_now_add=True, db_column='ebf_app_delete_date')
    # 全指令
    app_command = models.CharField(max_length=8, null=True, db_column='ebf_app_command')
    # 厂家/品牌uid
    app_factory_uid = models.CharField(max_length=64, null=True, db_column='ebf_app_factory_uid')
    # 云菜谱可控
    app_is_cloudmenu_device = models.IntegerField(default=0, db_column='ebf_app_is_cloudmenu_device')
    # app创建来源,0：默认创建，1：模板创建
    app_create_source = models.IntegerField(default=0, db_column='ebf_app_create_source')
    # 产品组id
    group_id = models.IntegerField(max_length=11, default=0, db_column='ebf_group_id')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_app_history'
        verbose_name = 'app应用历史记录'
