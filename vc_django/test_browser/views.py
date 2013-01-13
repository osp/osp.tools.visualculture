from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('test_browser.html', {'title':'Test Browser'}, context_instance=RequestContext(request))