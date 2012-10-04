"""
visual_culture.readers.pdf

"""

from visual_culture.readers import reader

import vc_poppler as poppler
from PIL import Image
import StringIO

import time


@reader(r'application/pdf')
class VC_PDF(object):
	"""
	PDF rendering through Cairo
	"""
	def __init__(self):
		self.ratio = .3
		
	def get_res(self, options):
		width = 0
		height = 0
		if 'width' in options:
			width = int(options['width'])
		elif 'height' in options:
			height = int(options['height'])	
		if height == 0 and width == 0:
			width = 200
		
		res = 1
		pw = self.page.rect(poppler.page_box.crop_box).width() / 72.0
		ph = self.page.rect(poppler.page_box.crop_box).height() / 72.0
		if width > 0:
			res = width / pw
		else:
			res = height / ph
			
		return res
		
	
	def render_page(self, res):
		print('[VC_PDF][%s] render page @%d'%(time.asctime(), res))
		pr = poppler.PageRenderer()
		pr.set_render_hint(poppler.render_hint.antialiasing, True)
		pr.set_render_hint(poppler.render_hint.text_antialiasing, True)
		#raise Exception('About to render page @%d'%res)
		i = pr.render_page(self.page, xres=res, yres=res)
		print('PDF rendered in %d %d : %s %d'%(i.width(), i.height(), i.format(), i.bytes_per_row()))
		data = i.data()
		print('Data Type => %s'%type(data))
		im = Image.frombuffer("RGBA", (i.width(), i.height()), data, "raw", "RGBA", 0, 1)
		buf = StringIO.StringIO()
		im.save(buf, 'PNG')
		self.data = buf.getvalue()
		buf.close()
	
	def read_blob(self, blob_info, options):
		print('[VC_PDF][%s] read blob (%s)'%(time.asctime(), blob_info['blob_url']))
		blob_data = self.get_blob_data(blob_info)
		loader = poppler.Loader()
		self.doc = loader.from_data(blob_data)
		self.page = self.doc.page(0)
		res = self.get_res(options)
		self.render_page(res)
		
		return {'data':self.data, 'mime': 'image/png'}
		
		