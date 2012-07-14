# -*- coding: utf-8 -*-
"""
image.py

"""

class VCImage:
	mime_type = ['image/png','image/jpg']
	
	def __init__(self, request, blob, mime):
		self.request = request
		self.blob = blob
		self.mime = mime
		
	def render(self):
		# TODO
		return {'data':self.blob, 'mime': self.mime}




