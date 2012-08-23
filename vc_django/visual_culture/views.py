"""
visual_culture.views
"""

HAVE_GITCOLLECTION = True
magic_find_mime = None

try:
	from git_info import git
	import magic
except ImportError:
	HAVE_GITCOLLECTION = False
	import urllib
	import json

from visual_culture.readers import *

vc_reader = Reader()


if HAVE_GITCOLLECTION:
	try:
		magic_find_mime = magic.open(magic.MIME_TYPE)
		magic_find_mime.load()
	except AttributeError:
		magic_find_mime = magic.Magic(mime=True)

def get_from_network(repo_name, oid):
	"""
	#TODO
	"""
	pass

def get_from_module(repo_name, oid):
	repo = getattr(git.git_collection, repo_name)
	commit = repo[oid]
	if commit.type != git.pygit2.GIT_OBJ_BLOB:
		return HttpResponseBadRequest('Requested object is not a BLOB')
		
	try:
		mime = magic_find_mime.buffer(commit.data)
	except AttributeError:
		mime = magic_find_mime.from_buffer(commit.data)
	return vc_reader.read_blob({'type':'blob', 'repo_name':repo_name, 'commit' : commit.hex, 'mime':mime}, commit.data)
	

def blob_data(request, repo_name, oid):
	"""
	the game here is to get data and mime type, whether from git_info module
	or from a git_info server, to feed the Reader
	"""
	if HAVE_GITCOLLECTION:
		return get_from_module(repo_name, oid)
	return get_from_network(repo_name, oid)
	