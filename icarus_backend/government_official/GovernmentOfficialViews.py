from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from icarus_backend.mission.MissionModel import Mission
from django.utils import timezone


@login_required
def is_government_official(request):
    response_json = json.dumps(request.user.role == 'government_official')
    return HttpResponse(response_json, content_type="application/json")


@login_required
def get_missions(request):
    if request.user.role == 'government_official':
        missions = Mission.objects.filter()
        dictionaries = [obj.as_dict() for obj in missions]
        return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def get_upcoming_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(starts_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def get_past_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(ends_at__lt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def get_current_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(starts_at__lt=_now,
                                      ends_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')