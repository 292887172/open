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
    # 保存用户邮寄地址
    url(r'^save/user/address$', views.save_user_address),
    #====================yq-vue==============
    url(r"^apimain/$", views.product_main),
    url(r"^apigetdevice/$", views.device_list),
    url(r"^getfactory/$", views.get_factory),
    url(r"^upload_file/$", views.upload_file),
    url(r"^get_flist/$", views.get_function_list),
    url(r"^get_protocol$", views.protocol),

]