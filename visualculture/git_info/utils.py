import os
from mimetypes import guess_type

import magic

def find_mime(obj=None, path=None):
    """
    First try to determine the mime-type based on the file extension
    
    Fall back to libmagic
    """
    if path:
        extension = os.path.splitext(path)[1]
        if extension:
            mime = guess_type(path)[0]
            if mime:
                return mime
    if not obj:
        return 'application/octet-stream'
    return magic.from_buffer(obj.data, mime=True)
