from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.debug.urls import debug_patterns

from app.wiki.urls import wiki_patterns
from app.center.urls import doc_urlpatterns

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^', include('app.home.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', 'app.home.views.test'),
    url(r'^center/', include('app.center.urls')),
    url(r'^product/', include("app.product.urls")),
    # 开发文档
    url(r"^wiki/", include(wiki_patterns)),
    # 调试
    url(r"^debug/", include(debug_patterns)),
    # api
    url(r'^api/', include('api.urls')),
)
