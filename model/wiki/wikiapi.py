import datetime

from django.db import models


class Application(models.Model):
    """
    应用程序
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    version = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(default=datetime.datetime.now())
    createdate = models.DateTimeField(default=datetime.datetime.now())
    pass

    class Meta:
        app_label = 'wiki'


class AppErrorCode(models.Model):
    """
    app错误代码
    """
    id = models.AutoField(primary_key=True)
    # 故障代码
    code = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    # 故障描述
    describe = models.TextField()
    pass

    class Meta:
        app_label = 'wiki'


class StatusType(models.Model):
    """
    状态类型
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    describe = models.TextField()
    pass

    class Meta:
        app_label = 'wiki'


class Api(models.Model):
    """
    接口信息表
    """
    id = models.AutoField(primary_key=True)
    port = models.IntegerField(default=8002)
    # 启动状态(1:启用,0:禁用,-1:未实现)
    status = models.IntegerField(default=1)
    # 接口地址
    address = models.CharField(max_length=1025)
    # 接口参数和默认值
    parameters = models.TextField()
    # 描述
    describe = models.TextField()
    # 文档地址
    wiki = models.TextField()

    class Meta:
        app_label = 'wiki'


class ApiDoc(models.Model):
    """
    接口文档
    """
    api = models.OneToOneField(Api, primary_key=True)
    title = models.TextField(null=True)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    # 修改时间,default不能用字符串，否则在admin后台会报错
    updatedate = models.DateTimeField(default=datetime.datetime.now())
    pass

    class Meta:
        app_label = 'wiki'


# 将模型添加到admin管理后台中
# admin.site.register(Application)
# admin.site.register(AppErrorCode)
# admin.site.register(StatusType)
# admin.site.register(Api)
# admin.site.register(ApiDoc)










