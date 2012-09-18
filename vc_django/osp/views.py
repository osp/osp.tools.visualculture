from osp.models import get_api, which_repo
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# dummy data
import json
import os
all = json.loads(open(os.path.join(os.path.dirname(__file__), 'all.json')).read())

def home(request):
#    repos = {"repos": ["osp.tools.visualculture", "osp.work.bessst", "osp.work.danslab", "gitolite-admin", "osp.work.visual-grammar", "aa.wiki", "aa.core", "osp.web.themes", "osp.work.osp-website", "linguist", "gitorious-test", "osp.tools.bootstrap", "osp.workshop.write-me-a-shadow", "osp.workshop.morphologic", "gitolite-admin.bak", "osp.tools.fonzie", "osp.tools.visualculture.bak", "osp.workshop.pzi", "osp.tools.lazylandscape", "osp.tools.visualculture.test", "osp.work.gallait", "osp.tools.portfolio", "osp.work.panik", "osp.web.gitweb", "osp.foundry.logisoso", "vgit", "osp.auto-newspaper-grid", "osp.marmite", "osp.foundry.din", "osp.foundry.sansguilt", "osp.workshop.vietnam", "osp.workshop.rca", "osp.foundry.universelse", "osp.foundry.libertinage", "osp.foundry.VJ12", "osp.foundry.limousine", "osp.foundry.cimatics", "osp.foundry.polsku", "osp.foundry.DLF", "osp.foundry.wdroge", "osp.foundry.skeleton", "osp.foundry.notcourriersans", "osp.workshop.pcmmd"]}
    data = all # get_api('all')
    repos = []
    for repo in data:
        r = repo
        r['web_path'] = 'http://foo.net/'
        r['iceberg'] = ['foo', 'foo', 'foo']
        commits = []
        for commit in r['commits']:
            c = commit
            c['ellipse'] = 0
            commits.append(c)
        r['commits'] = commits
        repos.append(r)
#    return HttpResponse(json.dumps(repos), mimetype="application/json")
    return render_to_response('home2.html',
        { 'repos' : repos },
        context_instance=RequestContext(request))

def browse(request, category, name, path):
    repo_slug = which_repo(category, name)

    repo = get_api(repo_slug)
    obj = get_api(repo_slug, 'path', path)

    if obj['type'] == 'tree':
        return render_to_response('tree.html', 
              {'title': title,
               'repo' : repo,
               'tree' : tree },
              context_instance=RequestContext(request))
    if obj['type'] == 'blob':
        return render_to_response('blob.html', 
              {'title': title,
               'repo' : repo,
               'blob' : blob },
              context_instance=RequestContext(request))
