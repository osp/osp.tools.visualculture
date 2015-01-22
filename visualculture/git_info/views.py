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

from pygit2 import GIT_SORT_TOPOLOGICAL

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from git_info.git import *
from utils import find_mime

import settings


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
    repo = git_collection[repo_name]
    items = []
    dirs = []
    for item in tree:
        if repo[item.hex].type == pygit2.GIT_OBJ_TREE:
            dirs.append({'hex': item.hex, 'name': item.name, 'mime': find_mime(path=item.name)})
        else:
            items.append({'hex': item.hex, 'name': item.name, 'mime': find_mime(path=item.name)})
    hash = {'type':'tree', 'repo_name':repo_name, 'dirs':dirs, 'files':items}
    return hash
    
    
def render_blob(repo_name, blob, path=None):
    """
    Ok so render is not the right name for this.
    Will re-rename them all to get.
    
    """
    
    mime = find_mime(blob, path)
    # Returns cache status as to let the caller decide if it goes for VC or cached files
    return {'type':'blob', 'repo_name':repo_name, 'hex' : blob.hex, 'mime': mime, 'size' : blob.size, 'is_binary': blob.is_binary }

def index(request):
    return HttpResponse(json.dumps({'repos': git_collection.get_names()}, indent=2), mimetype="application/json")

def render_repo(repo_slug, n_commits=5, tree=False, iceberg=False):
    repo = GitCollection(settings.PREFIX)[repo_slug]
    hash = {}
    hash['category'] = repo.repo_category
    hash['name'] = repo.repo_name
    hash['slug'] = repo_slug
    hash['commits'] = []
    i = 0
    try:
        for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
            hash['commits'].append(render_commit(repo_slug, commit))
            i += 1
            if i == n_commits:
                break
    except Exception as exn:
        pass
    if tree:
        head = repo.revparse_single('HEAD')
        hash['tree'] = render_tree(repo_slug, head.tree)
    if iceberg:
        if 'iceberg' in repo.head.get_object().tree:
            icetree = repo[ repo.head.get_object().tree['iceberg'].hex ]
            hash['iceberg'] = render_tree(repo_slug, icetree)
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
def home(request, n=8, category=None):
    if category:
        slugs = [slug for slug in GitCollection(settings.PREFIX).get_names() if len(slug.split('.')) > 1 and slug.split('.')[1] == category]
    else:
        slugs = GitCollection(settings.PREFIX).get_names()[:n]
    hash = repos(slugs)
    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")

def item(request, repo_name, oid):
    print('Requested item: %s %s' % (repo_name, oid))
    repo = git_collection[repo_name]
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
    you just recurse down the tree
    """
    repo = git_collection[repo_name]
    
    paths = path.split('/')
    
    print "looking for %s from %s in %s" % (paths, path, repo_name)
    obj = repo.head.get_object().tree
    for p in paths:
        if p == '':
            break
        try:
            obj = repo[ obj[p].hex ]
        except KeyError:
            raise Http404
    
    if paths[-1] == '':
        if len(paths) == 1:
            # root path named after repo
            name = repo_name
        else:
            # tree named after tree
            name = paths[-2]
    else:
        # blob named after blob
        name = paths[-1]
    
    if obj.type == pygit2.GIT_OBJ_TREE:
        hash = render_tree(repo_name, obj)
        
    elif obj.type == pygit2.GIT_OBJ_BLOB:
        hash = render_blob(repo_name, obj, path)
        hash['raw_url'] = reverse('git_info.views.blob_data', args=[repo_name, hash['hex']]) + name
        # Note: to pass the absolute url:
        hash['raw_url'] = request.build_absolute_uri(hash['raw_url']) 
    
    hash['name'] = name
    hash['paths'] = paths
    
    return HttpResponse(json.dumps(hash, indent=2), mimetype="application/json")

def blob_data(request, repo_name, oid):
    obj = git_collection[repo_name][oid]
    
    if obj.type == pygit2.GIT_OBJ_BLOB:
        mime = find_mime(obj)
        return HttpResponse(obj.data, mimetype=mime)
    
    return HttpResponseBadRequest('Requested object is not a BLOB')

def blob_data_from_path(request, repo_name, path):
    repo = git_collection[repo_name]
    paths = path.split('/')
    
    obj = repo.head.get_object().tree
    for p in paths:
        if p == '':
            break
        try:
            obj = repo[ obj[p].hex ]
        except KeyError:
            raise Http404
    
    if obj.type == pygit2.GIT_OBJ_BLOB:
        mime = find_mime(obj, path)
        return HttpResponse(obj.data, mimetype=mime)
    
    return HttpResponseBadRequest('Requested object is not a BLOB')
