"""
visual_culture.views
"""

import os
import errno

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from visual_culture.readers import Reader
from git_info.utils import find_mime

def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise exception


import settings

from git_info import git

if settings.PREFIX:
    git_collection = git.GitCollection(settings.PREFIX)
else:
    git_collection = git.GitCollection()


def transduce(request, repo_name, oid, key, value, filename, extension):
    try:
        repo = git_collection[repo_name]
    except KeyError:
        raise Http404
    try:
        obj = repo[oid]
    except KeyError:
        raise Http404
    
    if obj.type != git.pygit2.GIT_OBJ_BLOB:
        return HttpResponseBadRequest('Requested object is not a BLOB')
    
    mime = find_mime(obj, filename)
    r = Reader()
    options = {}
    if key and value:
        options = {key: value}
    result = r.read_blob({'mime': mime, 'repo_name': repo_name, 'blob_hex': oid}, options)
    cpath = os.path.join(settings.MEDIA_ROOT, repo_name, oid, '%s..%s' % (key, value))
    ensure_dir(cpath)
    with open(os.path.join(cpath, '%s%s' % (filename, extension)), 'wb') as f:
        f.write(result['data'])
    return HttpResponse(result['data'], result['mime'])
