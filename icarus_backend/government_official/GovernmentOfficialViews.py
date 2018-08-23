from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

@login_required
def is_government_official(request):
    response_json = json.dumps(request.user.role == 'government_official')
    return HttpResponse(response_json, content_type="application/json")