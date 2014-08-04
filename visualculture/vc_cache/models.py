import os

import settings
from django.db import models

from git_info import git
from vc_cache import utils 
from visual_culture.readers import Reader

import time
import magic

magic_find_mime = None
try:
    magic_find_mime = magic.open(magic.MIME_TYPE)
    magic_find_mime.load()
except AttributeError:
    magic_find_mime = magic.Magic(mime=True)

class VCCache(models.Model):
    """
    Interface to (for now) file based cache
    The point to have a DB record is mainly to cache mime types attached to files
    """
    class Meta:
        db_table = u'vc_cache'


    repo_name = models.CharField(max_length=256, blank=False)
    blob_hex = models.CharField(max_length=40, blank=False)
    blob_mime = models.CharField(max_length=256, blank=False)
    cache_options = models.CharField(max_length=512, blank=False)

    root_path = os.path.join(settings.MEDIA_ROOT, 'cache')
    root_url = os.path.join(settings.MEDIA_URL, 'cache')

    def get_from_module(self, repo_name, blob_hex):
        git_collection = git.GitCollection()
        repo = git_collection[repo_name]
        commit = repo[blob_hex]
        if commit.type != git.pygit2.GIT_OBJ_BLOB:
            raise Exception('Requested object is not a BLOB')
            
        try:
            mime = magic_find_mime.buffer(commit.data)
        except AttributeError:
            mime = magic_find_mime.from_buffer(commit.data)
        return {'type':'blob', 
            'repo_name':repo_name, 
            'blob_hex': blob_hex,
            'blob_url':'/'.join([settings.API_HOST, 'api', repo_name, blob_hex, 'blob_data']), 
            'commit' : commit.hex, 
            'mime':mime}

    def GetCacheInfo(self, repo, blob_hex):
        vc = VCCache.objects.filter(repo_name=repo, blob_hex=blob_hex)
        ci = []
        for c in vc:
            ci.append({
                'url':'/'.join([self.root_path, c.cache_options, blob_hex]),
                'options': utils.de_hash_options(c.cache_options)
                })
        return ci
        

    def Get(self, repo_name, blob_hex, options = {}):
        obj = None
        data = None
        mime = None
        options_h = utils.hash_options(options)
        try:
            obj = VCCache.objects.get(repo_name=repo_name, blob_hex=blob_hex, cache_options=options_h)
            mime = obj.blob_mime
        except VCCache.DoesNotExist:
            blob_info = self.get_from_module(repo_name, blob_hex)
            r = Reader()
            result = r.read_blob(blob_info, options)
            cpath = os.path.join(self.root_path, repo_name, options_h)
            utils.ensure_dir(cpath)
            f = open(os.path.join(cpath, blob_hex), 'wb')
            f.write(result['data'])
            f.close()
            obj = VCCache()
            obj.repo_name = repo_name
            obj.blob_hex = blob_hex
            obj.blob_mime = result['mime']
            obj.cache_options = options_h
            obj.save()
            mime = obj.blob_mime
            
        cache_url = os.path.join(self.root_url, repo_name, options_h, blob_hex)
        return {'url':cache_url, 'mime':mime}

