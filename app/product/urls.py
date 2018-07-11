# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.product.views',
    url(r"^list/$", "product_list", name="product/list"),
    url(r"^controldown/$", "product_controldown", name="product/controldown"),
    url(r"^protocol/$", "protocol", name="product/protocol"),
    url(r"^kitchen/$", "product_kitchen", name="product/kitchen"),
    url(r"^add/$", "product_add", name="product/add"),
    url(r"^main/$", "product_main", name="product/main"),
    url(r"^verify$", "key_verify", name="product/key_verify"),
    url(r"^control$", "control", name="control"),
    url(r"^portal", "portal", name="portal"),
    url(r"^upload_file", "upload_file", name="upload_file"),
    url(r'^wx_code', "wx_scan_code", name='product/wx_code'),
    url(r"^uiconf/(?P<device_key>\w{8})$", "ui_conf_main", name="uiconf"),
)
