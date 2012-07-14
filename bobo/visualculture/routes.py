# -*- coding: utf-8 -*-

import bobo
import webob
import pygit2
import os
import magic
import jinja2
import datetime

import transducer


GIT_REPO_ROOT = '/home/pierre/System/src/'
#GIT_REPO_ROOT = '/home/pierre/public_html/'

def datetimeformat(value):
    return datetime.date.fromtimestamp(value).isoformat()
    
    
template_env = jinja2.Environment(loader=jinja2.PackageLoader('visualculture', 'templates'))
template_env.filters['datetimeformat'] = datetimeformat


@bobo.query('')
def base(bobo_request):
	return bobo.redirect(bobo_request.url+'/')
	
	
@bobo.query('/')
def root(reponame = None):
	entries = os.listdir(GIT_REPO_ROOT)
	print 'R %s'%(reponame,)
	max_commits = 6
	repos = []
	for d in entries:
		name = os.path.join(GIT_REPO_ROOT,d)
		if os.path.isdir(name):
			try:
				repo = None
				try:
					repo = pygit2.Repository(name)
				except Exception:
					pass
					#print 'Can not create a repo off [%s]'%name
				if repo != None:
					iceberg_t = None
					try:
						iceberg_t = repo.head.tree['iceberg']
					except Exception:
						print 'No Iceberg in %s'%(d,)
					penguins = []
					commits = []
					
					if iceberg_t != None:
						print 'ICEBERG!!!%s'%d
						try:
							for p in iceberg_t.to_object():
								print '\tp => %s'%p.name
								penguins.append(p.to_object().hex)
						except Exception as e:
							print 'ERROR (penguins): %s'%e
					
					ccount = 0
					try:
						for w in repo.walk(repo.head.hex, pygit2.GIT_SORT_TIME):
							commits.append(w)
							if ccount == max_commits:
								break
							ccount += 1
					except Exception as e:
						print 'ERROR (commits): %s'%e
							
					if penguins:
						print ':'.join(penguins)
					repos.append({'name':d, 'repo':repo, 'iceberg':penguins, 'commits':commits})

			except Exception as e:
				print 'ERROR (root): %s'%e
	#ret = []
	#for repo in repos:
		#name, r = repo
		#ret.append('<div><h4><a href="/osp/%s/%s">%s</a></h4>%s</div>'%(name, r.head.tree.hex, name, r.head.message))
		
	#return '\n'.join(ret)
	template = template_env.get_template('index.html')
	return template.render({'repos' : repos, 'page':'root'})

	
	
def show_commit(name, commit):
	diff = commit.tree.diff(commit.parents[0].tree)
	template = template_env.get_template('commit.html')
	return template.render({'name':name, 'commit' : commit, 'diff': diff, 'page':'commit %s'%(commit.hex,)})
	
	
def show_tree(name, commit):
	ret = []
	for item in commit:
		if item.to_object().type == pygit2.GIT_OBJ_TREE:
			ret.append('<div class="tree">[<a href="/osp/%s/%s">%s</a>]</div>'%(name, item.hex, item.name))
		else:
			ret.append('<div><a href="/osp/%s/%s">%s</a></div>'%(name, item.hex, item.name))
	return '\n'.join(ret)
	
	
@bobo.query('/:name')
def repo(name):
	entries = os.listdir(GIT_REPO_ROOT)
	repo = None
	if name in entries:
		try:
			repo = pygit2.Repository(os.path.join(GIT_REPO_ROOT,name))
		except Exception:
			return 'Could not instanciate a pygit2.Repository for: %s'%name
	if repo is None:
		return 'pygit2.Repository %s could not be found'%name
	
	return show_tree(name, repo.head.tree)

@bobo.query('/:name/:oid')
def item(bobo_request,name,oid):
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
	
	if commit.type == pygit2.GIT_OBJ_COMMIT:
		return show_commit(name, commit)
		
	if commit.type == pygit2.GIT_OBJ_TREE:
		return show_tree(name, commit)
		
	if commit.type == pygit2.GIT_OBJ_BLOB:
		ms = magic.open(magic.MIME_TYPE)
		ms.load()
		res = webob.Response()
		mime = ms.buffer(commit.data)
		t = transducer.tr(bobo_request, commit.data, mime)
		res.content_type = t['mime']
		res.body = t['data']
		return res
		
		
	return 'Unhandled object type %s'%commit.type
	
@bobo.query('/:name/:oid/')
def item2(name,oid):
	return item(name, oid)
	
	
#@bobo.query('/vc/:name/:oid/')
#def vc(request, name, oid):
	
	