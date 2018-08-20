from django.http import HttpResponse
import json
import uuid
from django.utils.timezone import is_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from icarus_backend.mission.MissionModel import Mission
from django.contrib.auth.decorators import login_required


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
    area = Polygon(body['area']['features'][0]['geometry']['coordinates'])
    mission_id = uuid.uuid4()
    new_mission = Mission(id=mission_id, title=title, type=_type, description=description,
                          starts_at=starts_at, ends_at=ends_at, area=area, created_by=request.user)
    new_mission.save()
    response_data = {'message': 'Successfully registered the mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@login_required
def get_missions(request):
    missions = Mission.objects.filter(created_by=request.user.id)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def delete_mission(request):
    body = json.loads(request.body)
    mission_id = body['mission_id']
    mission_query = Mission.objects.filter(pk=mission_id)
    if len(mission_query) == 0:
        response_data = {'message': 'Mission does not exist.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)
    mission = mission_query[0].as_dict()
    if mission['created_by'] == request.user.id:
        mission_query.delete()
        response_data = {'message': 'Mission deleted successfully.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json")
    else:
        response_data = {'message': 'User does not have permissions to delete mission.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=403)
