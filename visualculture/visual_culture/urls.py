"""
visual_culture.urls

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('visual_culture.views',
    url(r'(?P<repo_name>[\w\.\-_]+)/(?P<oid>\w+)/(?P<key>[\w]+)\.\.(?P<value>[\w]+)/(?P<filename>[^/]+)(?P<extension>\.[\w]+)', 'transduce'),
)
