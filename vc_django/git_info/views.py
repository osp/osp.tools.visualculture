# -*- coding: utf-8 -*-
"""
git_info.views

"""


import json
import magic

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed
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
	context = {'type':'commit', 'repo_name': repo_name, 'commit' : commit.hex , 'author':commit.author.name, 'message':commit.message, 'files':commit.tree.hex, 'commit_time': commit.commit_time}
	if commit.parents:
		context['parent'] = commit.parents[0].hex
	return context

def get_commit(repo_name, commit):
	context = render_commit(commit)
	return HttpResponse(json.dumps(context), mimetype="application/json")

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
	
def get_tree(repo_name, tree):
	context = render_tree(repo_name, tree)
	return HttpResponse(json.dumps(context), mimetype="application/json")
	
def get_blob(name, blob):
	try:
		mime = magic_find_mime.buffer(blob.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(blob.data)
	context = {'type':'blob', 'repo_name':name, 'commit' : blob.hex, 'mime':mime}
	return HttpResponse(json.dumps(context), mimetype="application/json")
	
def get_blob_data(commit):
	try:
		mime = magic_find_mime.buffer(commit.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(commit.data)
	return HttpResponse(commit.data, mimetype=mime)
	
def index(request):
	return HttpResponse(json.dumps({'repos': git_collection.get_names()}), mimetype="application/json")

def render_repo(repo_slug):
	repo = getattr(git_collection, repo_slug)
	context = render_commit(repo_slug, repo.head)
#	context = {}
	context['category'] = repo.repo_category
	context['name'] = repo.repo_name
	context['slug'] = repo_slug
	context['commits'] = []
	for commit in repo.walk(repo.head.hex, pygit2.GIT_OBJ_TREE):
		context['commits'].append(render_commit(repo_slug, commit))
	context['tree'] = render_tree(repo_slug, repo.head.tree)	
	return context
	
def repo(request, repo_name):
	print('Requested repo: %s'%repo_name)
	context = render_repo(repo_name)
	return HttpResponse(json.dumps(context), mimetype="application/json")

def repos(repo_names):
	context = []
	for repo_name in repo_names:
		context.append(render_repo(repo_name))
	return context

@cache_page(60 * 60)
def all_repos(request):
	context = repos(git_collection.get_names())
	return HttpResponse(json.dumps(context), mimetype="application/json")

def item(request,repo_name, oid):
	print('Requested item: %s %s' % (repo_name, oid))
	repo = getattr(git_collection, repo_name)
	obj = None
	if(oid == 'head'):
		commit = repo.head
	else:
		obj = repo[oid]
	
	if obj.type == pygit2.GIT_OBJ_COMMIT:
		return get_commit(repo_name, obj)
		
	if obj.type == pygit2.GIT_OBJ_TREE:
		return get_tree(repo_name, obj)
		
	if obj.type == pygit2.GIT_OBJ_BLOB:
		return get_blob(repo_name, obj)
		
	return HttpResponseBadRequest('Unhandled object type %s'%commit.type)

def item_from_path(request, repo_name, path):
	"""
	Git doesn’t have a specific way to search for a tree or blob by path,
	you just recurse down the tree:
	/libs/transducers -> repo.head.tree['libs'].to_object()['transducers'].to_object()
	"""
	repo = getattr(git_collection, repo_name)
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
		return get_tree(repo_name, obj)
		
	if obj.type == pygit2.GIT_OBJ_BLOB:
		return get_blob(repo_name, obj)
	
def blob_data(request, repo_name, oid):
	obj = getattr(git_collection, repo_name)[oid]
	if obj.type == pygit2.GIT_OBJ_BLOB:
		return get_blob_data(commit)
		
	return HttpResponseBadRequest('Requested object is not a BLOB')
