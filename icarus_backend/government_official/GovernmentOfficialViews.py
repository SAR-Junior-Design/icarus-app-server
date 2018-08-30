from django.http import HttpResponse
from rest_framework.decorators import api_view
from oauth2_provider.decorators import protected_resource
import json
from icarus_backend.mission.MissionModel import Mission
from django.utils import timezone


@protected_resource()
@api_view(['GET'])
def is_government_official(request):
    response_json = json.dumps(request.user.role == 'government_official')
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['GET'])
def get_missions(request):
    if request.user.role == 'government_official':
        missions = Mission.objects.filter()
        dictionaries = [obj.as_dict() for obj in missions]
        return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_upcoming_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(starts_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_past_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(ends_at__lt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_current_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(starts_at__lt=_now,
                                      ends_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')