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
    
    def read_blob(self, blob_info, options):
        blob_data = self.get_blob_data(blob_info)
        return {'data':blob_data, 'mime': blob_info['mime']}