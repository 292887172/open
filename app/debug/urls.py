from django.conf.urls import patterns, url

__author__ = 'sunshine'


debug_patterns = patterns(
    'app.debug.views',
    url('^debug_interface$', 'debug_interface', name='debug_interface'),
    url('^debug_device$', 'debug_device', name='debug_device'),
)