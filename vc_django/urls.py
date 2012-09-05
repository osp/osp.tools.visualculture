from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    (r'^repos/', include('git_info.urls')),
    (r'^vc/', include('visual_culture.urls')),
    (r'^test/', include('test_browser.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serve media in debug
