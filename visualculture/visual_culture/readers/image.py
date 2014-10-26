"""
visual_culture.readers.image

"""

from visual_culture.readers import reader
from PIL import Image
import StringIO


@reader(r'image/(gif|png|jpeg|jpg|tiff)')
class VC_Image(object):
    """
    Handle any kind of images
    """
    def __init__(self):
        pass
    
    def scale_image(self, image, options):
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
            
        image.thumbnail((width,height), Image.ANTIALIAS)
        return image
    
    def read_blob(self, blob_info, options):
        blob_data = self.get_blob_data(blob_info)
        buf_in = StringIO.StringIO(blob_data)
        image = Image.open(buf_in)
        simage = self.scale_image(image, options)
        buf_out = StringIO.StringIO()
        simage.save(buf_out, 'PNG') # check options there
        data = buf_out.getvalue()
        buf_in.close()
        buf_out.close()
        return {'data':data, 'mime': 'image/png'}