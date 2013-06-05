from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    ('^menu.html$', direct_to_template, {
        'template': 'menu.html',
        'extra_context' : { 'HOST' : 'http://osp.constantvzw.org' },
    }),
    ('^summer-school-2013/$', direct_to_template, {'template': 'summer-school-2013.html', })
)

urlpatterns += patterns('osp.views',
    url(r'^$', 'home'),
    url(r'(?P<category>[\w\.\-_]+)/(?P<name>[\w\.\-_]+)/tree/master/(?P<path>.*)$', 'browse'),
    url(r'(?P<category>[\w\.\-_]+)/(?P<name>[\w\.\-_]+)/$', 'project'),
    url(r'(?P<category>[\w\.\-_]+)/$', 'category'),
)

