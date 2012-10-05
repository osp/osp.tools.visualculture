from osp.models import get_api, which_repo, ApiError
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse, NoReverseMatch

import settings
# dummy data

import json
import os
#all = json.loads(open(os.path.join(os.path.dirname(__file__), 'all.json')).read())

def home(request):
    data = get_api('all')
    repos = []
    for repo in data:
        r = repo
        try:
            r['web_path'] = reverse('osp.views.project', args=[ r['category'], r['name'] ])
        except NoReverseMatch:
            r['web_path'] = ''
            
        # iceberg ?
        
        r['iceberg'] = []
        try:
            ice = get_api(repo['slug'],'path/iceberg')
            if 'files' in ice:
                for penguin in ice['files']:
                    r['iceberg'].append(penguin)
        except ApiError:
            pass
    
        commits = []
        for commit in r['commits']:
            c = commit
            c['ellipse'] = 0
            commits.append(c)
        r['commits'] = commits
        repos.append(r)

    return render_to_response('home2.html',
        { 'repos' : repos, 'vc_url' :settings.VC_URL },
        context_instance=RequestContext(request))

def browse(request, category, name, path):
    repo_slug = which_repo(category, name)
    try:
        repo = get_api(repo_slug)
        obj = get_api(repo_slug, 'path', path)
    except ApiError:
        return Http404()


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
        
        return render_to_response('tree.html', 
              {'title': title,
               'repo' : repo,
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
               'repo' : repo,
               'blob' : blob },
              context_instance=RequestContext(request))

def project(request, category, name):
    return browse(request, category, name, '')