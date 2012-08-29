"""
visual_culture.readers.pdf

"""

from visual_culture.readers import reader

import vc_poppler as poppler
from PIL import Image
import StringIO

@reader(r'application/pdf')
class VC_PDF(object):
	"""
	PDF rendering through Cairo
	"""
	def __init__(self):
		self.ratio = .3
	
	#def create_context(self, page_width, page_height):
		#self.width = page_width * self.ratio
		#self.height = page_height * self.ratio
		#self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
		#self.ctx = cairo.Context(surface)
		#self.ctx.translate(0, 0)
		#self.ctx.scale(self.width/page_width, self.height/page_height)
		
	def render_page(self):
		#page.render(self.ctx)
		#self.ctx.set_operator(cairo.OPERATOR_DEST_OVER)
		#self.ctx.set_source_rgb(1, 1, 1)
		#self.ctx.paint()
		#im = Image.frombuffer("L", (self.width, self.height), self.surface.get_data(), "raw", "L", 0, 1)
		#buf = StringIO.StringIO()
		#image.save(buf, 'PNG')
		#self.data = buf.getvalue()
		#buf.close()
		pr = poppler.PageRenderer()
		pr.set_render_hint(poppler.render_hint.antialiasing, True)
		pr.set_render_hint(poppler.render_hint.text_antialiasing, True)
		i = pr.render_page(self.page)
		print('PDF rendered in %d %d : %s %d'%(i.width(), i.height(), i.format(), i.bytes_per_row()))
		data = i.data()
		print('Data Type => %s'%type(data))
		im = Image.frombuffer("RGBA", (i.width(), i.height()), data, "raw", "RGBA", 0, 1)
		buf = StringIO.StringIO()
		im.save(buf, 'PNG')
		self.data = buf.getvalue()
		buf.close()
	
	def read_blob(self, blob_info, blob_data):
		loader = poppler.Loader()
		self.doc = loader.from_data(blob_data)
		self.page = self.doc.page(0)
		self.render_page()
		
		return {'data':self.data, 'mime': 'image/png'}