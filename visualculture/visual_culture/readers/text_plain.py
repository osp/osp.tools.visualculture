"""
visual_culture.readers.text_plain

"""

from visual_culture.readers import reader, MimeNotSupported
# from markdown2 import markdown

# Well probably need this kind of stuff once we want to implement draw_image but
# Im commenting it out for now
# import cairo
# import pango
# import pangocairo

@reader(r'text/.*')
class VC_TextPlain(object):
    """
    Handles plain text
    """
    def __init__(self):
        pass
    
    def md(self, txt):
        return markdown(txt)
        
    def draw_text(self, txt, options):
        # This is not implemented yet, but could be used to send
        # an image representation of text
        width = 200
        height = 200
        if 'width' in options:
            width = int(options['width'])
            if 'height' not in options:
                height = width
        if 'height' in options:
            height = int(options['height'])
            if 'width' not in options:
                width = height
    
    def read_blob(self, blob_info, options):
        """
        We only return a text representation if the requested
        resource has a large width. (For example, a series of
        thumbnails would not be well suited by having each thumbnail
        contain the full text representation)
        """
        if 'width' in options and int(options['width']) > 400:
            blob_data = self.get_blob_data(blob_info)
#            if 'filter' in options:
#                if options['filter'] == 'markdown':
#                    return {'data':self.md(blob_data), 'mime': 'text/html'}
            return {'data':blob_data, 'mime': blob_info['mime'] }
        """
        Not sure what to return in other cases.
        """
        raise MimeNotSupported(blob_info['mime'])
        blob_data = self.get_blob_data(blob_info)

