from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

handler500 = 'visualculture.errors.error_500'

urlpatterns = patterns('',
    (r'^api/', include('git_info.urls')),
    (r'^visual/', include('visual_culture.urls')),
    (r'^test/', include('test_browser.urls')),
    (r'^', include('osp.urls')),
)
