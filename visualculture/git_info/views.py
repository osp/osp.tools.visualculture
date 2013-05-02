# -*- coding: utf-8 -*-
"""
git_info.views

Views that render the GitCollection accessible over HTTP a JSON API.

All the `render` functions should basically get out of here and become part
of the GitCollection class from git.py, in the form of `to_hash` methods.
That would clean up a bunch and save us the necessity to pass `repo_name`
around all the time.

"""


import json
import magic

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from vc_cache.models import VCCache
from git_info.git import *

import settings

try:
    magic_find_mime = magic.open(magic.MIME_TYPE)
    magic_find_mime.load()
    magic_finder = magic_find_mime.buffer
except AttributeError:
    magic_find_mime = magic.Magic(mime=True)
    magic_finder = magic_find_mime.from_buffer
        

if settings.PREFIX:
    git_collection = GitCollection(settings.PREFIX)
else:
    git_collection = GitCollection()

def render_commit(repo_name, commit):
    hash = {'type':'commit', 'repo_name': repo_name, 'hex' : commit.hex , 'author':commit.author.name, 'message':commit.message, 'files':commit.tree.hex, 'commit_time': commit.commit_time}
    if commit.parents:
        hash['parent'] = commit.parents[0].hex
    return hash

def render_tree(repo_name, tree):
    items = []
    dirs = []
    for item in tree:
        try:
            if item.to_object().type == pygit2.GIT_OBJ_TREE:
                dirs.append({'hex': item.hex, 'name': item.name})
            else:
                items.append({'hex': item.hex, 'name': item.name})
        except Exception:
            pass
    hash = {'type':'tree', 'repo_name':repo_name, 'dirs':dirs, 'files':items}
    return hash
    
    
def render_blob(repo_name, blob):
    """
    Ok so render is not the right name for this.
    Will re-rename them all to get.
    
    """
    mime = magic_finder(blob.data)
    # Returns cache status as to let the caller decide if it goes for VC or cached files
    cache = VCCache().GetCacheInfo(repo_name, blob.hex)
    return {'type':'blob', 'repo_name':repo_name, 'hex' : blob.hex, 'mime': mime, 'size' : blob.size, 'cache':cache}

def index(request):
    return HttpResponse(json.dumps({'repos': GitCollection(settings.PREFIX).get_names()}, indent=2), mimetype="application/json")

def render_repo(repo_slug, n_commits=5, tree=False, iceberg=False):
    repo = GitCollection(settings.PREFIX)[repo_slug]
    hash = {}
    hash['category'] = repo.repo_category
    hash['name'] = repo.repo_name
    hash['slug'] = repo_slug
    hash['commits'] = []
    i = 0
    try:
        for commit in repo.walk(repo.head.hex, pygit2.GIT_OBJ_TREE):
            hash['commits'].append(render_commit(repo_slug, commit))
            i += 1
            if i == n_commits:
                break
    except Exception as exn:
        pass
    if tree:
        hash['tree'] = render_tree(repo_slug, repo.head.tree)
    if iceberg:
        if repo.has_iceberg():
            hash['iceberg'] = render_tree(repo_slug, repo.head.tree['iceberg'].to_object())
    return hash
    
def repo(request, repo_name):
    print('Requested repo: %s'%repo_name)
    hash = render_repo(repo_name, n_commits=-1, tree=True, iceberg=True)
    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")

def repos(repo_names):
    hash = []
    for repo_name in repo_names:
        hash.append(render_repo(repo_name, iceberg=True))
    return hash

@cache_page(60 * 60)
def all_repos(request):
    hash = repos(GitCollection(settings.PREFIX).get_names())
    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")

def item(request, repo_name, oid):
    print('Requested item: %s %s' % (repo_name, oid))
    repo = GitCollection(settings.PREFIX)[repo_name]
    obj = None
    if(oid == 'head'):
        obj = repo.head
    else:
        try:
            obj = repo[oid]
        except KeyError:
            raise Http404
    
    if obj.type == pygit2.GIT_OBJ_COMMIT:
        hash = render_commit(repo_name, obj)
        
    elif obj.type == pygit2.GIT_OBJ_TREE:
        hash = render_tree(repo_name, obj)
        
    elif obj.type == pygit2.GIT_OBJ_BLOB:
        hash = render_blob(repo_name, obj)

    else:
        return HttpResponseBadRequest('Unhandled object type %s'%obj.type)

    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")


def item_from_path(request, repo_name, path):
    """
    Git doesn’t have a specific way to search for a tree or blob by path,
    you just recurse down the tree:
    /libs/transducers -> repo.head.tree['libs'].to_object()['transducers'].to_object()
    """
    repo = GitCollection(settings.PREFIX)[repo_name]
    
    paths = path.split('/')
    
    print "looking for %s from %s in %s" % (paths, path, repo_name)
    obj = repo.head.tree
    for p in paths:
        if p == '':
            break
        try:
            obj = obj[p].to_object()
        except KeyError:
            raise Http404
    
    if len(paths) == 1:
        # root path named after repo
        name = repo_name
    elif paths[-1] == '':
        # tree named after tree
        name = paths[-2]
    else:
        # blob named after blob
        name = paths[-1]
    
    if obj.type == pygit2.GIT_OBJ_TREE:
        hash = render_tree(repo_name, obj)
        
    elif obj.type == pygit2.GIT_OBJ_BLOB:
        hash = render_blob(repo_name, obj)
        hash['raw_url'] = reverse('git_info.views.blob_data', args=[repo_name, hash['hex']]) + name
        # Note: to pass the absolute url:
        hash['raw_url'] = request.build_absolute_uri(hash['raw_url']) 
    
    hash['name'] = name
    hash['paths'] = paths
    
    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")

def blob_data(request, repo_name, oid):
    obj = GitCollection(settings.PREFIX)[repo_name][oid]
    
    if obj.type == pygit2.GIT_OBJ_BLOB:
        mime = magic_finder(obj.data)
        return HttpResponse(obj.data, mimetype=mime)
    
    return HttpResponseBadRequest('Requested object is not a BLOB')

def blob_data_from_path(request, repo_name, path):
    repo = GitCollection(settings.PREFIX)[repo_name]
    try:
        oid = repo.index[path].oid
    except KeyError:
         raise Http404
    obj = repo[oid]
    
    if obj.type == pygit2.GIT_OBJ_BLOB:
        mime = magic_finder(obj.data)
        return HttpResponse(obj.data, mimetype=mime)
    
    return HttpResponseBadRequest('Requested object is not a BLOB')