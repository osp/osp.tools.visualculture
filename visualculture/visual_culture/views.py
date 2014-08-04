"""
visual_culture.views
"""


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from visual_culture.readers import MimeNotSupported


HAVE_GITCOLLECTION = True

try:
    from git_info import git
    import magic
except ImportError:
    HAVE_GITCOLLECTION = False
    import urllib

import json

from vc_cache.models import VCCache

def get_from_network(repo_name, oid):
    """
    #TODO
    """
    pass

def get_from_module(repo_name, oid):
    repo = getattr(git.git_collection, repo_name)
    obj = repo[oid]
    if obj.type != git.pygit2.GIT_OBJ_BLOB:
        return HttpResponseBadRequest('Requested object is not a BLOB')
        
    mime = magic.from_buffer(obj.data, mime=True)
    return vc_reader.read_blob({'type':'blob', 'repo_name':repo_name, 'commit' : obj.hex, 'mime':mime}, obj.data)
    

def blob_data(request, repo_name, oid):
    """
    the game here is to get data and mime type, whether from git_info module
    or from a git_info server, to feed the Reader
    """
    #if HAVE_GITCOLLECTION:
        #return get_from_module(repo_name, oid)
    #return get_from_network(repo_name, oid)
    
    options = {}
    for k in request.POST:
        options[k] = request.POST.get(k, '')
    for k in request.GET:
        options[k] = request.GET.get(k, '')
        
    cache = VCCache()
    
    try:
        blob = cache.Get(repo_name, oid, options=options)
        blob['url'] = request.build_absolute_uri(blob['url']) # add domain name to url
    except MimeNotSupported:
        blob = {'url': '', 'mime': ''}
    
    #return HttpResponse(blob['data'], mimetype=blob['mime'])
    return HttpResponse(json.dumps(blob, indent=2), mimetype="application/json")
    
    