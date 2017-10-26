# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.product.views',
    url(r"^list/$", "product_list", name="product/list"),
    url(r"^add/$", "product_add", name="product/add"),
    url(r"^main/$", "product_main", name="product/main"),
    url(r"^verify$", "key_verify", name="product/key_verify"),
    url(r"^control$", "control", name="control"),
    url(r"^upload_file", "upload_file", name="upload_file"),
    url(r'^webPage$', "webPage", name='webPage'),
)
