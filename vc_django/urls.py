from django.conf.urls.defaults import patterns, include, url



urlpatterns = patterns('',
    (r'^repos/', include('git_info.urls')),
    (r'^vc/', include('visual_culture.urls')),
)
