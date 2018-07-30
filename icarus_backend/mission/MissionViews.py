from django.http import HttpResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from .MissionModel import Mission

@csrf_exempt
def registerMissions(request):
    body = json.loads(request.body)
    title = body['title']
    type = body['type']
    description = body['description']
    created_at = timezone.now()
    starts_at = timezone.make_aware(parse_datetime(body['starts_at']))
    ends_at = timezone.make_aware(parse_datetime(body['ends_at']))
    print(body['area']['features'][0]['geometry']['coordinates'])
    area = Polygon(body['area']['features'][0]['geometry']['coordinates'])
    mission_id = uuid.uuid4()
    newMission = Mission(mission_id = mission_id, title = title, type = type, description = description,
                         created_at = created_at, starts_at=starts_at, ends_at=ends_at, area = area)
    newMission.save();
    response_data = {'message': 'Successfully registered the mission.'}
    responseJson = json.dumps(response_data)
    return HttpResponse(responseJson, content_type="application/json")