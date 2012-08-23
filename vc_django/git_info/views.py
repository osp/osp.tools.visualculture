"""
git_info.views

"""

import json
import magic

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed

from git_info.git import *

try:
	magic_find_mime = magic.open(magic.MIME_TYPE)
	magic_find_mime.load()
except AttributeError:
	magic_find_mime = magic.Magic(mime=True)
		
# This module only serves JSON, reflecting the state of a GIT repository

def get_commit(name, commit):
	files = []
	#for entry in commit.tree:
		#files.append({'name':entry.name, 'hex':entry.hex})
	parent = None
	if commit.parents:
		parent = commit.parents[0]

	context = {'type':'commit', 'repo_name':name, 'commit' : commit.hex , 'author':commit.author.name, 'message':commit.message, 'files':commit.tree.hex, 'parent':parent.hex}
	return HttpResponse(json.dumps(context), mimetype="application/json")
	
def get_tree(name, commit):
	items = []
	dirs = []
	for item in commit:
		try:
			if item.to_object().type == pygit2.GIT_OBJ_TREE:
				dirs.append({'hex': item.hex, 'name': item.name})
			else:
				items.append({'hex': item.hex, 'name': item.name})
		except Exception:
			pass
	return HttpResponse(json.dumps({'type':'tree', 'repo_name':name, 'dirs':dirs, 'files':items}), mimetype="application/json")
	
def get_blob(name, commit):
	try:
		mime = magic_find_mime.buffer(commit.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(commit.data)
	context = {'type':'blob', 'repo_name':name, 'commit' : commit.hex, 'mime':mime}
	return HttpResponse(json.dumps(context), mimetype="application/json")
	
def get_blob_data(commit):
	try:
		mime = magic_find_mime.buffer(commit.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(commit.data)
	return HttpResponse(commit.data, mimetype=mime)
	
def index(request):
	return HttpResponse(json.dumps({'repos': git_collection.get_names()}), mimetype="application/json")
	
def repo(request, repo_name):
	print('Requested repo: %s'%repo_name)
	repo = getattr(git_collection, repo_name)
	return get_commit(repo_name, repo.head)

def item(request,repo_name, oid):
	print('Requested item: %s %s' % (repo_name, oid))
	repo = getattr(git_collection, repo_name)
	commit = None
	if(oid == 'head'):
		commit = repo.head
	else:
		commit = repo[oid]
	
	if commit.type == pygit2.GIT_OBJ_COMMIT:
		return get_commit(repo_name, commit)
		
	if commit.type == pygit2.GIT_OBJ_TREE:
		return get_tree(repo_name, commit)
		
	if commit.type == pygit2.GIT_OBJ_BLOB:
		return get_blob(repo_name, commit)
		
	return HttpResponseBadRequest('Unhandled object type %s'%commit.type)
	
def blob_data(request, repo_name, oid):
	commit = getattr(git_collection, repo_name)[oid]
	if commit.type == pygit2.GIT_OBJ_BLOB:
		return get_blob_data(commit)
		
	return HttpResponseBadRequest('Requested object is not a BLOB')
