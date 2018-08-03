from django.http import HttpResponse
import json
import uuid
from django.utils.timezone import is_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from .MissionModel import Mission
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import assign_perm


@login_required
def register_mission(request):
    body = json.loads(request.body)
    title = body['title']
    _type = body['type']
    description = body['description']
    starts_at = parse_datetime(body['starts_at'])
    if not is_aware(starts_at):
        response_data = {'message': 'Starts at has not timezone.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
    ends_at = parse_datetime(body['ends_at'])
    if not is_aware(ends_at):
        response_data = {'message': 'Ends at has no timezone.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
    print(body['area']['features'][0]['geometry']['coordinates'])
    area = Polygon(body['area']['features'][0]['geometry']['coordinates'])
    mission_id = uuid.uuid4()
    new_mission = Mission(mission_id=mission_id, title=title, type=_type, description=description,
                          starts_at=starts_at, ends_at=ends_at, area=area)
    new_mission.save()
    user = request.user
    assign_perm()
    response_data = {'message': 'Successfully registered the mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


def get_missions(request):
    return 'todo'


def delete_missions(request):
    return 'todo'
