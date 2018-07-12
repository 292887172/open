# -*- coding: utf-8 -*-
from django.conf.urls import url,patterns

urlpatterns = patterns(
    'app.home.views',
    # url(r'^$', 'home', name='home'),
    url(r'^$', 'home', name='home'),
    url(r'^SmartRecipe', 'smart_menu', name='smart_menu'),
    url(r'^guide$', 'guide', name='home/guide'),
    url(r'^test$', 'test', name='test'),
    url(r'^left$', 'left', name='left'),
    url(r'^top$', 'top', name='top'),
    url(r'^hz$', 'hz', name='hz'),
    url(r'^zy$', 'zy', name='zy'),
    url(r'^zny$', 'zny', name='zny'),
    url(r'^dynamic$', 'dynamic', name='dynamic'),
    url(r'^kfz$', 'kfz', name='kfz'),
    url(r'^sdk$', 'sdk', name='sdk'),
    url(r'^error$', 'error', name='error'),
    url(r'^big$', 'big', name='big'),
    url(r'^contact$', 'contact', name='contact'),
    url(r'^app/user$', 'app_user', name='app'),

)