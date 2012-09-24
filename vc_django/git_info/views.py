# -*- coding: utf-8 -*-
"""
git_info.views

"""


import json
import magic

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from git_info.git import *

from vc_django.settings import PREFIX

try:
	magic_find_mime = magic.open(magic.MIME_TYPE)
	magic_find_mime.load()
except AttributeError:
	magic_find_mime = magic.Magic(mime=True)
		
# This module only serves JSON, reflecting the state of a GIT repository

if PREFIX:
	git_collection = GitCollection(PREFIX)
else:
	git_collection = GitCollection()

def render_commit(repo_name, commit):
	context = {'type':'commit', 'repo_name': repo_name, 'hex' : commit.hex , 'author':commit.author.name, 'message':commit.message, 'files':commit.tree.hex, 'commit_time': commit.commit_time}
	if commit.parents:
		context['parent'] = commit.parents[0].hex
	return context

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
	context = {'type':'tree', 'repo_name':repo_name, 'dirs':dirs, 'files':items}
	return context
	
	
def render_blob(repo_name, blob):
	"""
	Ok so render is not the right name for this.
	Will re-rename them all to get.
	
	"""
	try:
		mime = magic_find_mime.buffer(blob.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(blob.data)
	return {'type':'blob', 'repo_name':repo_name, 'hex' : blob.hex, 'mime':mime}

	
def get_blob_data(obj):
	try:
		mime = magic_find_mime.buffer(obj.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(obj.data)
	return HttpResponse(obj.data, mimetype=mime)
	
def index(request):
	return HttpResponse(json.dumps({'repos': git_collection.get_names()}, indent=2), mimetype="application/json")

def render_repo(repo_slug, n_commits=5, tree=False):
	repo = getattr(git_collection, repo_slug)
#	context = render_commit(repo_slug, repo.head)
	context = {}
	context['category'] = repo.repo_category
	context['name'] = repo.repo_name
	context['slug'] = repo_slug
	context['commits'] = []
	i = 0
	for commit in repo.walk(repo.head.hex, pygit2.GIT_OBJ_TREE):
		context['commits'].append(render_commit(repo_slug, commit))
		i += 1
		if i == n_commits:
			break
	if tree:
		context['tree'] = render_tree(repo_slug, repo.head.tree)
	return context
	
def repo(request, repo_name):
	print('Requested repo: %s'%repo_name)
	context = render_repo(repo_name, tree=True)
	return HttpResponse(json.dumps(context, indent=2), mimetype="application/json")

def repos(repo_names):
	context = []
	for repo_name in repo_names:
		context.append(render_repo(repo_name))
	return context

@cache_page(60 * 60)
def all_repos(request):
	context = repos(git_collection.get_names())
	return HttpResponse(json.dumps(context, indent=2), mimetype="application/json")

def item(request, repo_name, oid):
	print('Requested item: %s %s' % (repo_name, oid))
	repo = git_collection[repo_name]
	obj = None
	if(oid == 'head'):
		commit = repo.head
	else:
		try:
			obj = repo[oid]
		except KeyError:
			raise Http404
	
	if obj.type == pygit2.GIT_OBJ_COMMIT:
		context = render_commit(repo_name, obj)
		
	elif obj.type == pygit2.GIT_OBJ_TREE:
		context = render_tree(repo_name, obj)
		
	elif obj.type == pygit2.GIT_OBJ_BLOB:
		context = render_blob(repo_name, obj)

	else:
		return HttpResponseBadRequest('Unhandled object type %s'%commit.type)

	return HttpResponse(json.dumps(context, indent=2), mimetype="application/json")


def item_from_path(request, repo_name, path):
	"""
	Git doesn’t have a specific way to search for a tree or blob by path,
	you just recurse down the tree:
	/libs/transducers -> repo.head.tree['libs'].to_object()['transducers'].to_object()
	"""
	repo = git_collection[repo_name]
	
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
		
	if obj.type == pygit2.GIT_OBJ_TREE:
		context = render_tree(repo_name, obj)
		
	elif obj.type == pygit2.GIT_OBJ_BLOB:
		context = render_blob(repo_name, obj)
		context['raw_url'] = reverse('git_info.views.blob_data', args=[repo_name, context['hex']])
		# Note: to pass the absolute url:
		context['raw_url'] = request.build_absolute_uri(context['raw_url'])
	
	context['paths'] = paths

	if len(paths) == 1:
		# root path named after repo
		context['name'] = repo_name
	elif paths[-1] == '':
		# tree named after tree
		context['name'] = paths[-2]
	else:
		# blob named after blob
		context['name'] = paths[-1]
	
	return HttpResponse(json.dumps(context, indent=2), mimetype="application/json")
	
def blob_data(request, repo_name, oid):
	obj = git_collection[repo_name][oid]
	if obj.type == pygit2.GIT_OBJ_BLOB:
		return get_blob_data(obj)
		
	return HttpResponseBadRequest('Requested object is not a BLOB')
