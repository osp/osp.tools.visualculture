# -*- coding: utf-8 -*-
"""
transducer.py

A factory for trasducers

"""

class MimeNotSupported(Exception):
	def __init__(self, mime):
		self.mime = mime
	def __str__(self):
		return '[%s] not supported (yet)'%(self.mime)

import transducers as _transducers

transducers = {}

for resource in _transducers.__dict__.itervalues():
	transname = getattr(resource, '__name__', None)
	print '__name__ => %s'%transname
	if transname is None:
		continue
	
	try:
		submodule = __import__('transducers.%s'%transname, None)
		for r in submodule.__dict__.itervalues():
			mime = getattr(r, 'mime_type', None)
			if mime is not None:
				for mime in trans_mime:
					transducers[mime] = resource
					print 'Register transducer for mime type [%s]'%mime
	except:
		continue
	
	

def tr(request, blob, mime):
	if mime in transducers:
		t = transducers[mime](request, blob, mime)
		return t.render()
		
	raise MimeNotSupported(mime)
	





