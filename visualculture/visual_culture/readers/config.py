"""
visual_culture.readers.config

import readers here
"""
import sys

def try_import(module):
    try:
        m_ = __import__(module, globals())
        globals()[module] = m_
    except Exception as e:
        sys.stderr.write('Could not import %s because of exception: %s'%(module, e))

try_import( 'text_plain' )
try_import( 'pdf' )
try_import( 'image' )
#try_import( 'font' )