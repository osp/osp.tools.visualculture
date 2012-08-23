"""
visual_culture.readers.text_plain

"""

from visual_culture.readers import reader

@reader(r'text/plain')
class VC_TextPlain(object):
	"""
	Handle any kind of images
	"""
	def __init__(self):
		pass
	
	def read_blob(self, blob_info, blob_data):
		return {'data':blob_data, 'mime': blob_info['mime']}