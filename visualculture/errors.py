import traceback
import sys
from django.http import HttpRequest, HttpResponse,  HttpResponseServerError
        
def error_500(req):
    etype, value, tb = sys.exc_info()
    e_txt = []
    e_txt.append('<h1>%s : %s</h1>'%(etype.__name__, value))
    tb_fmt = traceback.format_tb(tb)
    for t in tb_fmt:
        e_txt.append('<div style="font-family:monospace">%s</div>'%(t,))
    return  HttpResponseServerError('\n'.join(e_txt))
    