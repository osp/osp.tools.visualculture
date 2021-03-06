from osp.settings import API_PATH, PREFIX
from urllib2 import  Request, urlopen, URLError
from urllib import quote
import json

class ApiError(Exception):
    def __init__(self, url, what):
        self.url = url
        self.what = what
    def __str__(self):
        return '(%s) => %s'%(self.url,self.what)

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
    url = API_PATH + quote( ( '/'.join(args)).encode('utf-8') )
    req = Request(url)
    print('[API] %s'%url)
    res = None
    try:
        res = urlopen(req)
        api_dict = json.loads(res.read())
    except URLError, e:  # This error checking code doesnt always work
        if hasattr(e, 'reason'):
            raise ApiError(url, e.reason)
        elif hasattr(e, 'code'):
            raise ApiError(url, e.code)
    return api_dict

def get_url_contents(url):
    req = Request(url)
    res = urlopen(req)
    res = None
    try:
        res = urlopen(req)
        data = res.read()
    except URLError, e:
        if hasattr(e, 'reason'):
            raise ApiError(url, e.reason)
        elif hasattr(e, 'code'):
            raise ApiError(url, e.code)
    return data
