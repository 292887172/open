# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.product.views',
    url(r"^list/$", "product_list", name="product/list"),
    url(r"^add/$", "product_add", name="product/add"),
    url(r"^main/$", "product_main", name="product/main"),
    url(r"^export/$", "export", name="product/export"),
)
