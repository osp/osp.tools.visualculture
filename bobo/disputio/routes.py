# -*- coding: utf-8 -*-

import bobo
import webob
import jinja2

import pymongo as mongo



def datetimeformat(value):
    return datetime.date.fromtimestamp(value).isoformat()
    
    
template_env = jinja2.Environment(loader=jinja2.PackageLoader('disputio', 'templates'))
template_env.filters['datetimeformat'] = datetimeformat


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
	cn = mongo.Connection()
	db = cn.RCE
	col= db.disputio
	col.insert(doc)
	return bobo.redirect('/')

