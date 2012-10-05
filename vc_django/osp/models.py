from osp.settings import API_PATH, PREFIX
from urllib2 import urlopen, HTTPError
import json

def repo_parts(repo_slug):
    parts = repo_slug.split('.')
    if PREFIX:
        return { 'slug' : repos.slug,
              'category' : parts[1],
              'name' : '.'.join(self.repo_parts[2:]) }
    else:
        return { 'slug' : repos.slug,
              'category' : '',
              'name' : repos.slug }

def which_repo(category, name):
    if PREFIX:
        return '.'.join((PREFIX, category, name))
    return '.'.join((category, name))

def get_api(*args):
    url = API_PATH + '/'.join(args)
    res = None
    try:
        res = urlopen(url)
        api_dict = json.loads(res.read())
    except Exception:
        api_dict = {}
    finally:
        if res:
            res.close()
    
    return api_dict

