"""
visual_culture.readers.text_plain

"""

from visual_culture.readers import reader, MimeNotSupported

@reader(r'text/plain')
class VC_TextPlain(object):
    """
    Handles plain text
    """
    def __init__(self):
        pass
    
    def read_blob(self, blob_info, options):
        """
        We only return a text representation if the requested
        resource has a large width. (For example, a series of
        thumbnails would not be well suited by having each thumbnail
        contain the full text representation)
        """
        if 'width' in options and int(options['width']) > 400:
            blob_data = self.get_blob_data(blob_info)
            return {'data':blob_data, 'mime': blob_info['mime'] }
        """
        Not sure what to return in other cases.
        """
        raise MimeNotSupported(blob_info['mime'])
