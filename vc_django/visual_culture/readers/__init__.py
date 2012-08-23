"""
visual_culture.readers

"""

import re

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden, HttpResponseNotAllowed

Readers = {}

# class decorator

def reader(mime_pattern):
	def decorator(cls):
		name = cls.__name__
		print('Decorating [%s] with [%s]'%(name, mime_pattern))
		Readers[mime_pattern] = cls
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
			
		raise MimeNotSupported(mime)
		
	def read_blob(self, blob_info, blob_data):
		reader = self.get_reader(blob_info['mime'])
		result = reader.read_blob(blob_info, blob_data)
		return HttpResponse(result['data'], mimetype=result['mime'])
		

from config import *