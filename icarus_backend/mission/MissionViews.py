from django.http import HttpResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
import uuid

import datetime
from django.utils.dateparse import parse_datetime

from .MissionModel import Mission


@csrf_exempt
def getMissions(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

@csrf_exempt
def registerMissions(request):
    body = json.loads(request.body)
    title = body['title']
    type = body['type']
    description = body['description']
    created_at = timezone.now()
    starts_at = timezone.make_aware(parse_datetime(body['starts_at']))
    ends_at = timezone.make_aware(parse_datetime(body['ends_at']))

    mission_id = uuid.uuid4()

    newMission = Mission(mission_id = mission_id, title = title, type = type,
                            description = description, created_at = created_at, starts_at=starts_at,
                              ends_at=ends_at)
    newMission.save();

    response_data = {'message': 'Successfully registered the mission.'}
    responseJson = json.dumps(response_data)
    return HttpResponse(responseJson, content_type="application/json")