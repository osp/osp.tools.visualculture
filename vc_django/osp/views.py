# -*- coding: utf-8 -*-

from osp.models import get_api, which_repo, ApiError
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse, NoReverseMatch
from datetime import datetime
from math import log1p

import settings
# dummy data

import json
import os
#all = json.loads(open(os.path.join(os.path.dirname(__file__), 'all.json')).read())

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
                ellipse = log1p(ellipse) * 50
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

    return render_to_response('category.html',
        { 'repos' : repos[:8], "said": said, 'vc_url' :settings.VC_URL, 'category' : category },
    context_instance=RequestContext(request))

def browse(request, category, name, path):
    repo_slug = which_repo(category, name)
    try:
        repo = get_api(repo_slug)
        obj = get_api(repo_slug, 'path', path)
        commits = []
        ellipse = 0
        i = 0
        for commit in repo['commits']:
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
    except ApiError:
        return Http404()

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


    title = "Browsing %s in %s" % (path, name)
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
        
#            path_to = '/'.join(obj['paths'][:i+1] + [''])

        
        return render_to_response('tree.html', 
              {'title': title,
               'breadcrumbs' : breadcrumbs,
               'repo' : repo,
               'said': said,
               'vc_url': settings.VC_URL,
               'tree' : tree },
              context_instance=RequestContext(request))
    if obj['type'] == 'blob':
        blob = obj
        blob['size'] = 0
        if 'vc' in blob:
            if 'vc.mime' in ['text/html', 'text/plain' ]:
                # get the data, wrap it in html, and pass
                # it to vc.data
                # vc['data'] =
                pass
            vc['image'] = False
            if 'image' in vc.mime:
                vc['image'] = True
        return render_to_response('blob.html', 
              {'title': title,
               'breadcrumbs' : breadcrumbs,
               'repo' : repo,
               'said': said,
               'vc_url': settings.VC_URL,
               'blob' : blob },
              context_instance=RequestContext(request))


def project(request, category, name, path=""):
    #repo_slug = which_repo(category, name)
    #try:
        #repo = get_api(repo_slug)
        #obj = get_api(repo_slug, 'path', path)
        #commits = []
        #ellipse = 0
        #i = 0
        #for commit in repo['commits']:
            #c = commit
            
            #if i != 0:
                #commit_time=  datetime.fromtimestamp(c['commit_time'])
                #ellipse = float((previous_commit - c['commit_time']))/(24*60*60)
                #ellipse = log1p(ellipse) * 50
            #i += 1
            #previous_commit = c['commit_time']
            #c['commit_time'] = datetime.fromtimestamp(c['commit_time'])
            #c['ellipse'] = ellipse
            #commits.append(c)
        #repo['commits'] = commits
    #except ApiError:
        #return Http404()
    return browse(request, category, name, path)

    #return render_to_response('project_base.html',
            #{ 'repo' : repo, "said": said, 'vc_url' :settings.VC_URL },
        #context_instance=RequestContext(request))


