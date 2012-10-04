"""
visual_culture.readers.font

"""

from visual_culture.readers import reader

import fontforge
from tempfile import NamedTemporaryFile

class ContourDecomposer(object):
	def noop_(self, *args, **kwargs):
		print('noop')
		pass
	
	def mid_point_(self, p1, p2, on_curve= True):
		return fontforge.point((p1.x + p2.x)/2, (p1.y + p2.y)/2, on_curve)
		
	def decompose(self, glyph):
		"""
		from Fontforge documentation (http://fontforge.org/python.html#Contour)
		A contour is a collection of points. A contour may be either
		based on cubic or quadratic splines.
			If based on cubic splines there should be either 0 or 2
		off-curve points between every two on-curve points. If there are no off-curve
		points then we have a line between those two points. If there are 2 off-curve
		points we have a cubic bezier curve between the two end points.

			If based on quadratic splines things are more complex. Again,
		two adjacent on-curve points yield a line between those points. Two on-curve
		points with an off-curve point between them yields a quadratic bezier curve.
		However if there are two adjacent off-curve points then an on-curve point will
		be interpolated between them. (This should be familiar to anyone who has read
		the truetype 'glyf' table docs).

			For examples of what these splines can look like see the section
		on bezier curves.

			A contour may be open in which case it is just a long wiggly
		line, or closed when it is more like a circle with an inside and an outside.
		Unless you are making stroked fonts all your contours should eventually be
		closed.

			Contours may also be expressed in terms of Raph Levien's spiro
		points. This is an alternate representation for the contour, and is not always
		available (Only if fontforge.hasSpiro() is True. If available the spiro member
		will return a tuple of spiro control points, while assigning to this member will
		change the shape of the contour to match the new spiros.

			Two contours may be compared to see if they describe similar
		paths.
		"""
		move_to = getattr(self, 'move_to', self.noop_)
		line_to = getattr(self, 'line_to', self.noop_)
		conic_to = getattr(self, 'conic_to', self.noop_)
		cubic_to = getattr(self, 'cubic_to', self.noop_)
		end_path = getattr(self, 'end_path', self.noop_)
		
		
		layer = glyph.foreground
		
		control_points = []
		if layer.is_quadratic == 0:
			print('CUBIC LAYER')
			for contour in layer:
				first_point = None
				for point in contour:
					if first_point is None:
						first_point = point
						move_to(to=point)
						continue
					if point.on_curve == 0:
						control_points.append(point)
					else:
						if control_points:
							cubic_to(ct0=control_points[0], ct1=control_points[1], to=point)
							control_points = []
						else:
							line_to(to=point)
				end_path()
		else:
			print('QUADRATIC LAYER')
			for contour in layer:
				first_point = None
				for point in contour:
					if first_point is None:
						first_point = point
						move_to(to=point)
						continue
					if point.on_curve == 1:
						if len(control_points) == 0:
							line_to(to=point)
						if len(control_points) == 1:
							conic_to(ct=control_points[0], to=point)
							control_points = []
					else:
						if len(control_points) == 1:
							interpolated_point = self.mid_point_(control_points[0], point)
							conic_to(ct=control_points[0], to=interpolated_point)
							control_points = [point]
						else:
							control_points.append(point)
					
				if control_points:
					conic_to(ct=control_points[0], to=first_point)
					
				end_path()
					
		

		
class DebugDecomp(ContourDecomposer):
	def move_to(self, to):
		print('%d %d m'%(to.x, to.y))
	
	def line_to(self, to):
		print('%d %d l'%(to.x, to.y))
	
	def cubic_to(self, ct0, ct1, to):
		print('%d %d %d %d %d %d c'%(ct0.x, ct0.y, ct1.x, ct1.y, to.x, to.y))
		
	def conic_to(self, ct, to):
		print('%d %d %d %d q'%(ct.x, ct.y, to.x, to.y))
		
	def end_path(self):
		print('END')
		
		
class SVGPathDecomp(ContourDecomposer):
	def __init__(self):
		self.path_string=''
		
	def pp(self, a):
		self.path_string += a + ' ';
		
	def move_to(self, to):
		self.pp('M %d %d'%(to.x, to.y))
	
	def line_to(self, to):
		self.pp('L %d %d'%(to.x, to.y))
	
	def cubic_to(self, ct0, ct1, to):
		self.pp('C %d %d %d %d %d %d'%(ct0.x, ct0.y, ct1.x, ct1.y, to.x, to.y))
		
	def conic_to(self, ct, to):
		self.pp('Q %d %d %d %d'%(ct.x, ct.y, to.x, to.y))
		
	def end_path(self):
		self.pp('z')

@reader(r'application/vnd.ms-opentype')
@reader(r'application/x-font.*')
class VC_Font(object):
	"""
	PFont "rendering" (SVG) with Fontforge
	"""
	def __init__(self):
		pass
		
	def load_from_buffer(self, buf):
		f = NamedTemporaryFile(mode='w+b', delete=False)
		f.write(buf)
		self.font = fontforge.open(f.name)
	
	def read_blob(self, blob_info, options):
		blob_data = self.get_blob_data(blob_info)
		self.load_from_buffer(blob_data)
		
		dc = SVGPathDecomp()
		dc.decompose(self.font['c'])
		
		print(dc.path_string)
		
		doctype = r'<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
		svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000"><g><path d="'+dc.path_string+'" style="fill:#000000;fill-opacity:1;stroke:none;" /></g></svg>'
		
		#raise Exception('Loaded font: %s'%(self.font.fullname,)) # to avoid filling cache
		return {'data':svg, 'mime': 'image/svg+xml'}