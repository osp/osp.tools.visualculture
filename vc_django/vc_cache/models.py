




import os
#import json
#from urlparse import urljoin
#from gevent.server import StreamServer, socket

import settings
from django.db import models

from git_info import git
from vc_cache import tasks 
from vc_cache import utils 

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
            f = open(os.path.join(self.root_path, repo_name, options_h, blob_hex), 'rb')
            data = f.read()
            f.close()
            mime = obj.blob_mime
        except VCCache.DoesNotExist:
            print('[%s][%s] Not found in cache'%(options_h,time.asctime()))
            blob_info = self.get_from_module(repo_name, blob_hex)
            print('[%s][%s] Got the blob info'%(blob_info['blob_url'],time.asctime()))
            task_result = tasks.read_blob.delay(self.root_path, blob_info, options)
            result = task_result.get() # synchronous
            obj = VCCache()
            obj.repo_name = repo_name
            obj.blob_hex = blob_hex
            obj.blob_mime = result['mime']
            obj.cache_options = options_h
            obj.save()
            data = result['data']
            mime =obj.blob_mime
            
        return {'data':data, 'mime':mime}


#class VCCacheProcessServer(StreamServer):
	
	#def __init__(self,lstnr):
		#super(StreamServer, self).__init__(lstnr)
		#self.ssl_enabled = False
		#self.clients = {} # ???
		#self.reader = Reader()
		#self.current_nice = 0
	
	#def start(self):
		##assert not self.started, '%s already started' % self.__class__.__name__
		#self.pre_start()
		#self.started = True
		#try:
			#self.start_accepting()
		#except Exception as e:
			#self.kill()
			#raise e


	
	#def handle(self, j_data, address):
		#data = None
		#try:
			#data = json.loads(j_data)
		#except Exception as e:
			#self.socket.sendto(json.dumps({'status':'ERROR', 'error':'%s'%e}), address)
			#return
			
		#repo_name = data['rn']
		#blob_hex = data['bh']
		#nice = data['nice']
		#repo = getattr(git.git_collection, repo_name)
		#commit = repo[blob_hex]
		
		#if commit.type != git.pygit2.GIT_OBJ_BLOB:
			#self.socket.sendto(json.dumps({'status':'ERROR', 'error':'commit.type != git.pygit2.GIT_OBJ_BLOB'}), address)
			
		#try:
			#mime = magic_find_mime.buffer(commit.data)
		#except AttributeError:
			#mime = magic_find_mime.from_buffer(commit.data)
		
		#while (self.current_nice + nice) > settings.CACHE_QUEUE_MAX_NICE:
			#gevent.sleep(seconds=.5)
			
		#self.current_nice += nice
		#result = self.reader.read_blob({'type':'blob', 'repo_name':repo_name, 'commit' : commit.hex, 'mime':mime}, commit.data)
		#self.current_nice -= nice
		
		#f = open(data['path'], 'wb')
		#f.write(result['data'])
		#f.close()
		
		
		#self.socket.sendto(json.dumps({'status':'SUCCESS', 'rn':repo_name, 'bh':blob_hex, 'mime':mime}), address)
		#self.socket.shutdown()

#class VCCacheQueue(models.Model):
	#"""
	#It implements a basic queue on top of Django ORM
	#"""
	
	#repo_name = models.CharField(max_length=256, blank=False)
	#blob_hex = models.CharField(max_length=40, blank=False)
	#nice = models.IntegerField(default=10)
	#ts = models.TimeField(auto_now=True)
	
	#class Meta:
		#db_table = u'vc_cache_queue'
		
	
	#def throw_server(self):
		#pid = os.fork()
		#if not pid:
			#print('Throwing cache process server on %s:%s'%settings.CACHE_QUEUE_PSERVER)
			#cps = VCCacheProcessServer(settings.CACHE_QUEUE_PSERVER)
			#cps.serve_forever()
	
	#def connect_pserver(self):
		#sock = None
		#try:
			#sock = socket.create_connection(settings.CACHE_QUEUE_PSERVER)
		#except Exception:
			#self.throw_server()
			#try:
				#sock = socket.create_connection(settings.CACHE_QUEUE_PSERVER)
			#except Exception as e:
				#raise e
		#sock.setblocking(True)
		#return sock
		
		
	#def Push(self, path, rn, bh, n = 10):
		#obj = None
		#IsInQueue = False
		#try:
			#obj = VCCacheQueue.objects.get(repo_name=rn, blob_hex=bh)
			#IsInQueue = True
		#except VCCacheQueue.DoesNotExist:
			#obj = VCCacheQueue()
			#obj.repo_name=rn
			#obj.blob_hex=bh
			#obj.nice=n
			#obj.save()
			
		#if IsInQueue:
			#obj.delete()
			#raise Exception('We got a problem #TODO')
			
		
		#sock = self.connect_pserver()
		#sock.send(json.dumps({'path':path, 'rn':rn, 'bh':bh, 'nice':n}))
		#j_data = []
		#while True:
			#d = socket.recv(32)
			#if not d:
				#break
			#j_data.append(d)
			
		#data = json.loads(u''.join(j_data))
		#obj.delete()
		
		#if data['status'] == 'ERROR':
			#raise Exception(data['error'])
		
		#return data['mime']
		
	
	
#class VCCache(models.Model):
	#"""
	#Interface to (for now) file based cache
	#"""
	#class Meta:
		#db_table = u'vc_cache'
		
	#class Entry:
		#def __init__(self, base, rn, bh, bm):
			##self.url = urljoin(base, rn, bh)
			#self.path = os.path.join(base, rn, bh)
			#self.mime = bm
			
	
	#repo_name = models.CharField(max_length=256, blank=False)
	#blob_hex = models.CharField(max_length=40, blank=False)
	#blob_mime = models.CharField(max_length=256, blank=False)
	
	#root_path = os.path.join(settings.MEDIA_ROOT, 'cache')
	#root_url = os.path.join(settings.MEDIA_URL, 'cache')
	
	
	#def Get(self, repo_name, blob_hex):
		#obj = None
		#try:
			#obj = VCCache.objects.get(repo_name=repo_name, blob_hex=blob_hex)
		#except VCCache.DoesNotExist:
			#q = VCCacheQueue()
			#mime = q.Push(os.path.join(self.root_path,repo_name,blob_hex), repo_name, blob_hex)
			#obj = VCCache()
			#obj.repo_name = repo_name
			#obj.blob_hex = blob_hex
			#obj.blob_mime = mime
			#obj.save()
			
		#return Entry(self.root_path, obj.repo_name, obj.blob_hex, obj.mime)
		
		
		
