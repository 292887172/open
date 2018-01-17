# -*- coding: utf-8 -*-
from django.conf.urls import url
from api import views

urlpatterns = [
    # 保存自定ui配置文件
    url(r'^get_ui_conf$', views.get_ui_conf),
    # 获取自定义ui配置
    url(r'^pull_ui_conf$', views.pull_ui_conf),
]