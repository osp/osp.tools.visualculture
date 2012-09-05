# -*- coding: utf-8 -*-

import bobo
import webob
import jinja2

import pymongo as mongo
from pymongo import objectid



    
    
template_env = jinja2.Environment(loader=jinja2.PackageLoader('disputio', 'templates'))


def get_collection(name = None):
	if name is None:
		name = 'disputio'
	cn = mongo.Connection()
	db = cn.RCE
	col = db[name]
	return col

@bobo.query('')
def base(bobo_request):
	return bobo.redirect(bobo_request.url+'/')
	
	
@bobo.query('/')
def root(reponame = None):
	template = template_env.get_template('index.html')
	return template.render({'page':'root'})


	
@bobo.post('/add')
def add(bobo_request):
	doc = {}
	for k in bobo_request.POST:
		doc[k] = bobo_request.POST[k]
	
	col = get_collection()
	col.insert(doc)
	return bobo.redirect('/disputio')
	
	
def r_to_doc(r, keys):
	doc = {}
	for k in keys:
		if k == '_id':
			doc[k] = str(r[k])
		else:
			if r.has_key(k):
				doc[k] = r.get(k)
			else:
				doc[k] = ''
	return doc
	
@bobo.query('/docs')
def docs():
	col = get_collection()
	res = col.find()
	ids = []
	for r in res:
		ids.append(str(r.get('_id')))
		
	template = template_env.get_template('docs.html')
	return template.render({'ids':ids})

@bobo.query('/:key/:value')
def bykey(key, value):
	col = get_collection()
	pat = {key:value}
	if key == 'id' or key == '_id':
		pat = {'_id':objectid.ObjectId(value)}
	res = col.find(pat)
	keys_ = {}
	for r in res:
		for k in r.iterkeys():
			keys_[k] = 1
	keys = keys_.keys()
	resource = []
	res.rewind()
	for r in res:
		resource.append(r_to_doc(r, keys))
		
	print('KEYS: %s'%keys)
	print('R: %s'%resource)
		
	template = template_env.get_template('find.html')
	return template.render({'key':key, 'value':value, 'keys':keys, 'resource':resource})

