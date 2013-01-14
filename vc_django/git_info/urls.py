"""
git_info.urls

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('git_info.views',
    url(r'^$', 'index'),
    url(r'^all/$', 'all_repos'),
    url(r'(?P<repo_name>[\w\.\-_]+)/path/(?P<path>.*)$', 'item_from_path'),
    url(r'(?P<repo_name>[\w\.\-_]+)/(?P<oid>\w+)/blob-data/$', 'blob_data'),
    url(r'(?P<repo_name>[\w\.\-_]+)/(?P<oid>\w+)/$', 'item'),
    url(r'(?P<repo_name>[\w\.\-_]+)/$', 'repo'),
)
