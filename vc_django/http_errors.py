import traceback
import sys
from django.http import HttpRequest, HttpResponse
        
def error_500(req):
    etype, value, tb = sys.exc_info()
    e_txt = []
    e_txt.append('<h1>%s : %s</h1>'%(etype.__name__, value))
    for t in traceback.format_tb(tb):
        e_txt.append('<div style="font-family:monospace">%s</div>'%(t,))
    return HttpResponse('\n'.join(e_txt))