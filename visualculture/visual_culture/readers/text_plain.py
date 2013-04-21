"""
visual_culture.readers.text_plain

"""

from visual_culture.readers import reader, MimeNotSupported
from markdown2 import markdown

import cairo
import pango
import pangocairo

@reader(r'text/plain')
class VC_TextPlain(object):
    """
    Handles plain text
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
        """
        We only return a text representation if the requested
        resource has a large width. (For example, a series of
        thumbnails would not be well suited by having each thumbnail
        contain the full text representation)
        """
        if 'width' in options and int(options['width']) > 400:
            if 'filter' in options:
                if options['filter'] == 'markdown':
                    return {'data':self.md(blob_data), 'mime': 'text/html'}
            blob_data = self.get_blob_data(blob_info)
            return {'data':blob_data, 'mime': blob_info['mime'] }
        """
        Not sure what to return in other cases.
        """
        raise MimeNotSupported(blob_info['mime'])
        blob_data = self.get_blob_data(blob_info)

