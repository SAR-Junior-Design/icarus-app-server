from django.http import HttpResponse
import json
import uuid
from django.utils.timezone import is_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from django.contrib.auth.decorators import login_required
from .MissionModel import Mission
from icarus_backend.assets.AssetModel import Asset
from icarus_backend.drone.DroneModel import Drone
from django.utils import timezone


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
    coordinates = body['area']['features'][0]['geometry']['coordinates']
    print(coordinates)
    if coordinates[0] != coordinates[-1]:
        coordinates += [coordinates[0]]
    area = Polygon(coordinates)
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
def get_upcoming_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, starts_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def get_past_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, ends_at__lt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def get_current_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, starts_at__lt=_now,
                                      ends_at__gt=_now)
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


@login_required
def edit_mission_details(request):
    body = json.loads(request.body)
    mission_id = body['mission_id']
    mission = Mission.objects.filter(pk=mission_id).first()
    if 'title' in body.keys():
        mission.title = body['title']
    if 'description' in body.keys():
        mission.description = body['description']
    mission.save()
    response_data = {'message': 'Mission Successfully updated.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=200)


@login_required()
def edit_clearance(request):
    body = json.loads(request.body)
    mission_id = body['mission_id']
    created_by = body['created_by']
    state = body['state']
    message = body['message']

    mission = Mission.objects.get(mission_id=mission_id)
    object = mission.clearance
    object.created_by = created_by
    object.state = state
    object.message = message
    object.save()

    response_data = {'message': 'Successfully edited the clearance.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@login_required()
def add_drone_to_mission(request):
    body = json.loads(request.body)
    drone = Drone.objects.filter(id=body['drone_id']).first()
    mission = Mission.objects.filter(id=body['mission_id']).first()
    asset = Asset(drone=drone, mission=mission, operator=request.user)
    asset.save()
    response_data = {'message': 'Successfully added drone to mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")

@login_required()
def remove_drone_from_mission(request):
    body = json.loads(request.body)
    drone = Drone.objects.filter(id=body['drone_id']).first()
    mission = Mission.objects.filter(id=body['mission_id']).first()
    asset = Asset.objects.filter(drone=drone, mission=mission).first()
    asset.delete()
    response_data = {'message': 'Successfully removed drone from mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")
