"""
visual_culture.urls

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('visual_culture.views',
	url(r'(?P<repo_name>[\w\.\-_]+)/(?P<oid>\w+)/$', 'blob_data'),
)
