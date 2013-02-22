# -*- coding: utf-8 -*-

from osp.models import get_api, which_repo, get_url_contents, ApiError
from django.http import HttpResponse, Http404
from django.template import Context, loader, TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse, NoReverseMatch
from datetime import datetime
from math import log1p

import settings

import json
import os

said = ["said", "whispered", "shouted", "cried", "confessed", "expressed", "verbalized", "verbalised", "uttered", "claimed", "argued", "complained", "ironized", "said", "tweeted", "told", "stated", "song", "interpreted", "rendered", "emited", "let out", "let loose", "talked", "spoke", "said", "whistled", "spilled the beans", "let the cat out of the bag", "talked", "tattled", "blabed", "peached", "babbled", "babbled out", "blabed out", "unwraped", "disclosed", "let on", "said", "bring out", "revealed", "discovered", "exposed", "published", "divulged", "gave away"]

def home(request):
    data = get_api('all')
    repos = []
    for repo in data:
        r = repo
        try:
            r['web_path'] = reverse('osp.views.project', args=[ r['category'], r['name'] ])
        except NoReverseMatch:
            r['web_path'] = ''
            
        ice = []
        # The iceberg returned by the APO is just like a regular tree, 
        # so there’s files and folders
        if 'iceberg' in r and 'files' in r['iceberg']:
            for penguin in r['iceberg']['files']:
                # This is where you would add specific logic to not include
                # certain file types
                ice.append(penguin)
        r['iceberg'] = ice

        commits = []
        ellipse = 0
        i = 0
        for commit in r['commits']:
            c = commit
            
            if i != 0:
                commit_time=  datetime.fromtimestamp(c['commit_time'])
                ellipse = float((previous_commit - c['commit_time']))/(24*60*60)
                ellipse = (log1p(ellipse) * 50) + 3
            i += 1
            previous_commit = c['commit_time']
            c['commit_time'] = datetime.fromtimestamp(c['commit_time'])
            c['ellipse'] = ellipse
            commits.append(c)
        r['commits'] = commits
        repos.append(r)

    return render_to_response('home.html',
            { 'repos' : repos[:8], "said": said, 'vc_url' :settings.VC_URL },
        context_instance=RequestContext(request))

def category(request, category):
    data = get_api('all')
    repos = []
    for repo in data:
        r = repo
        if r['category'] != category:
            continue
        
        try:
            r['web_path'] = reverse('osp.views.project', args=[ r['category'], r['name'] ])
        except NoReverseMatch:
            r['web_path'] = ''
            
        ice = []
        # The iceberg returned by the APO is just like a regular tree, 
        # so there’s files and folders
        if 'iceberg' in r and 'files' in r['iceberg']:
            for penguin in r['iceberg']['files']:
                # This is where you would add specific logic to not include
                # certain file types
                ice.append(penguin)
        r['iceberg'] = ice
        repos.append(r)

    #try:
        #t = loader.get_template('category_%s.html'%(category))
    #except TemplateDoesNotExist:
    t = loader.get_template('category.html')
    c = RequestContext(request,
           { 'repos' : repos[:8], "said": said, 'vc_url' :settings.VC_URL, 'category' : category }
       )
    return HttpResponse(t.render(c))

def browse(request, category, name, path):
    title = "you're traveling toward %s in %s" % (path, name)
    
    repo_slug = which_repo(category, name)
    try:
        repo = get_api(repo_slug)
        obj = get_api(repo_slug, 'path', path)
    except ApiError:
        return Http404()

    # Render commits with time apart
    
    commits = []
    ellipse = 0
    i = 0
    for commit in repo['commits']: # default is newest first, we start from the beginning
        c = commit
        
        if i != 0:
            commit_time=  datetime.fromtimestamp(c['commit_time'])
            ellipse = float((previous_commit - c['commit_time']))/(24*60*60)
            ellipse = log1p(ellipse) * 50
        i += 1
        previous_commit = c['commit_time']
        c['commit_time'] = datetime.fromtimestamp(c['commit_time'])
        c['ellipse'] = ellipse
        commits.append(c)
            
    
    # Render README
    
    root_files = [i['name'] for i in repo['tree']['files']]
    README = ''
    for f in root_files:
        if 'README' in f or 'readme' in f: # A regex would be more flexible
            README = get_url_contents(get_api(repo_slug, 'path', f)['raw_url'])
            # OSP Convention: the part of the README that equals the description is 
            # terminated by a Markdown representation of a horizontal line - - -.
            README = README.split('- - -')[0]
            break


    # Render a breadcrumbs navigation for the current path
    
    breadcrumbs = []
    repo_home = {}
    repo_home['name'] = obj['repo_name']
    repo_home['href'] = reverse('osp.views.project', args=[ category, name ])
    breadcrumbs.append(repo_home)
    
    path_to = ''
    for i, path in enumerate(obj['paths']):
        path_to += path + '/'
        if i == len(obj['paths']) -1:
            if obj['type'] == 'blob':
                "we want to render the breadcrumb for the blob, but without a trailing slash"
                path_to = path_to.rstrip('/')
            else:
                "the list of 'paths' of a tree ends with an empty string, we do not need to render"
                break
        breadcrumb = {}
        breadcrumb['name'] = path
        breadcrumb['href'] = reverse('osp.views.browse', args=[ category, name, path_to ])
        breadcrumbs.append(breadcrumb)

    if obj['type'] == 'tree':
        
        # Add hyperlinks to all files and folders
        
        dirs = []
        for dir in obj['dirs']:
            # the last element of the paths array is empty 
            # '/some/path/to/tree/'.split('/') -> ['some', 'path', 'to', 'tree', '']
            # which we have to take into account when adding new elements to the path
            dir['path'] = '/'.join(obj['paths'][:-1] + [dir['name'], ''])
            dir['href'] = reverse('osp.views.browse', args=[ repo['category'], repo['name'], dir['path'] ])
            dirs.append(dir)
        files = []
        for file in obj['files']:
            file['path'] = '/'.join(obj['paths'][:-1] + [file['name']])
            file['href'] = reverse('osp.views.browse', args=[ repo['category'], repo['name'], file['path'] ])
            files.append(file)
        tree = obj
        tree['dirs'] = dirs
        tree['files'] = files
        
        return render_to_response('tree.html', 
              {'title': title,
               'breadcrumbs' : breadcrumbs,
               'repo' : repo,
               'said': said,
               'vc_url': settings.VC_URL,
               'tree' : tree,
               'README' : README },
              context_instance=RequestContext(request))
    
    if obj['type'] == 'blob':
        blob = obj
        blob['size'] = 0
        
        return render_to_response('blob.html', 
              {'title': title,
               'breadcrumbs' : breadcrumbs,
               'repo' : repo,
               'said': said,
               'vc_url': settings.VC_URL,
               'blob' : blob,
               'README' : README },
              context_instance=RequestContext(request))


def project(request, category, name, path=""):
    # For now a project home page is the same as all the other browse views--
    # up for change of course!
    return browse(request, category, name, path)
