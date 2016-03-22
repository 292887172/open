# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

wiki_patterns = patterns(
    'app.wiki.views',
    url(r"^$", "wiki", name='wiki'),
    url(r"^new_wiki$", "new_wiki"),
    # web 调试工具
    url(r"^webtools$", "wiki_webtools"),
    # 接口测试执行程序
    url(r"^service$", "wiki_service"),
    url(r"^doc$", "wiki_doc"),
    url(r"^doc-test$", 'wiki_doc_test'),
    url(r"^download$", "wiki_download"),
)
