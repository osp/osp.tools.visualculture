from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('osp.views',
    (r'^$', 'home'),
)

