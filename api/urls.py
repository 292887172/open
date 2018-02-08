# -*- coding: utf-8 -*-
from django.conf.urls import url
from api import views

urlpatterns = [
    # 保存自定ui配置文件
    url(r'^upload_ui_conf$', views.upload_ui_conf),
    # 获取设备功能列表配置文件
    url(r'^pull_ui_conf$', views.pull_ui_conf),
    # 获取自定义ui配置文件
    url(r'^diy_ui_conf$', views.diy_ui_conf),
]