from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('osp.views',
    url(r'^$', 'home'),
    url(r'(?P<category>[\w\.\-_]+)/(?P<name>[\w\.\-_]+)/tree/master/(?P<path>.*)$', 'browse'),
    url(r'(?P<category>[\w\.\-_]+)/(?P<name>[\w\.\-_]+)/$', 'project'),
)

