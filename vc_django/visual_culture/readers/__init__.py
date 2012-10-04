"""
visual_culture.readers

"""

import re
import git_info.git as git


Readers = {}


# class decorator

def reader(mime_pattern):
	def decorator(cls):
		name = cls.__name__
		print('Decorating [%s] with [%s]'%(name, mime_pattern))
		Readers[mime_pattern] = cls
		
		def get_blob_data(self, blob_info):
			repo = git.GitCollection()[blob_info['repo_name']]
			return repo[blob_info['blob_hex']].data
		
		setattr(cls, 'get_blob_data', get_blob_data)
		return cls
	return decorator


class MimeNotSupported(Exception):
	def __init__(self, mime):
		self.mime = mime
	def __str__(self):
		return '[%s] not supported (yet)'%(self.mime)

class Reader(object):
	"""
	Factory reader.
	"""
	def __init__(self):
		#self.service = service_root
		self.readers = {}
		self.tasks = []
	
	def get_reader(self, mime):
		reader = None
		for r in self.readers.keys():
			if re.match(r, mime) != None:
				return  self.readers[r]
				
		for R in Readers.keys():
			cr = re.compile(R)
			if re.match(cr, mime) != None:
				self.readers[cr] = Readers[R]()
				return  self.readers[cr]
		
		print('MimeNotSupported %s'%(mime,))
		raise MimeNotSupported(mime)
		
	def read_blob(self, blob_info, options={}):
		reader = self.get_reader(blob_info['mime'])
		result = reader.read_blob(blob_info, options)
		return result
		#return HttpResponse(result['data'], mimetype=result['mime'])
		
		

from config import *