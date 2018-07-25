from django.http import HttpResponse
import datetime
import json


def get_missions(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def register_mission(request):
    body = json.loads(request.body)
    content = body['content']
    html = "%s" % content
    return HttpResponse(html)