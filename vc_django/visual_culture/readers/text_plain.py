"""
visual_culture.readers.text_plain

"""

from visual_culture.readers import reader
from markdown2 import markdown

import cairo
import pango
import pangocairo

@reader(r'text/plain')
class VC_TextPlain(object):
    """
    Handle any kind of images
    """
    def __init__(self):
        pass
    
    def md(self, txt):
        return markdown(txt)
        
    def draw_text(self, txt, options):
        width = 0
        height = 0
        if 'width' in options:
            width = int(options['width'])
            if 'height' not in options:
                height = width
        if 'height' in options:
            height = int(options['height'])
            if 'width' not in options:
                width = height
                
                
        if height == 0 and width == 0:
            width = height = 200
    
    def read_blob(self, blob_info, options):
        blob_data = self.get_blob_data(blob_info)
        if 'filter' in options:
            if options['filter'] == 'markdown':
                return {'data':self.md(blob_data), 'mime': 'text/html'}
            if options['filter'] == 'none':
                return {'data':blob_data, 'mime': blob_info['mime']}
                
        