import bobo
import webob
import pygit2
import os
import magic


GIT_REPO_ROOT = '/home/pierre/System/src/'



@bobo.query('')
def base(bobo_request):
	return bobo.redirect(bobo_request.url+'/')
	
	
@bobo.query('/')
def root():
	entries = os.listdir(GIT_REPO_ROOT)
	repos = []
	for d in entries:
		name = os.path.join(GIT_REPO_ROOT,d)
		if os.path.isdir(name):
			try:
				repos.append((d, pygit2.Repository(name)))
			except Exception:
				pass
	ret = []
	for repo in repos:
		name, r = repo
		ret.append('<div><h4><a href="/osp/%s/%s">%s</a></h4>%s</div>'%(name, r.head.tree.hex, name, r.head.message))
		
	return '\n'.join(ret)

@bobo.query('/:name/:oid')
def item(name,oid):
	entries = os.listdir(GIT_REPO_ROOT)
	repo = None
	if name in entries:
		try:
			repo = pygit2.Repository(os.path.join(GIT_REPO_ROOT,name))
		except Exception:
			return 'Could not instanciate a pygit2.Repository for: %s'%name
	if repo is None:
		return 'pygit2.Repository %s could not be found'%name
	
	commit = repo[oid]
	
	if commit.type == pygit2.GIT_OBJ_TREE:
		ret = []
		for item in commit:
			ret.append('<div><a href="/osp/%s/%s">%s</a></div>'%(name, item.hex, item.name))
		return '\n'.join(ret)
		
	if commit.type == pygit2.GIT_OBJ_BLOB:
		ms = magic.open(magic.MIME_TYPE)
		ms.load()
		res = webob.Response()
		res.headerlist = [('Content-type', ms.buffer(commit.data))]
		res.body = commit.data
		return res
		
		
	return 'Unhandled object type %s'%commit.type