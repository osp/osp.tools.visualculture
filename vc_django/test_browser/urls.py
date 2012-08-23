"""
visual_culture.urls

"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('test_browser.views',
	url(r'.*', 'index'),
)