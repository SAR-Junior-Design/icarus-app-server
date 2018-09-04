from django.http import HttpResponse
import json
import uuid
from django.utils.timezone import is_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from .MissionModel import Mission
from icarus_backend.assets.AssetModel import Asset
from icarus_backend.drone.DroneModel import Drone
from icarus_backend.clearance.ClearanceModel import Clearance
from django.utils import timezone
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view


@protected_resource()
@api_view(['POST'])
def register_mission(request):
    body = request.data
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
    if coordinates[0] is not coordinates[-1]:
        coordinates += [coordinates[0]]
    area = Polygon(coordinates)
    mission_id = uuid.uuid4()
    clearance_id = uuid.uuid4()
    clearance = Clearance(clearance_id=clearance_id, created_by='', state='PENDING',
                          message='')
    clearance.save()
    new_mission = Mission(id=mission_id, title=title, type=_type, description=description,
                          starts_at=starts_at, ends_at=ends_at, area=area, created_by=request.user,
                          clearance=clearance)
    new_mission.save()
    response_data = {'message': 'Successfully registered the mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
def get_mission_info(request):
    body = request.data
    mission_id = body['mission_id']
    missions = Mission.objects.filter(id=mission_id).first()
    if missions is None:
        message = {"message": "No mission exists with that id."}
        return HttpResponse(json.dumps(message), content_type='application/json')
    else:
        return HttpResponse(json.dumps(missions.as_dict()), content_type='application/json')


@protected_resource()
@api_view(['GET', 'POST'])
def get_missions(request):
    user = request.user
    print(user)
    missions = Mission.objects.filter(created_by=request.user.id)
    dictionaries = []
    for mission in missions:
        mission_dict = mission.as_dict()
        mission_dict['num_drones'] = Asset.objects.filter(mission=mission).count()
        dictionaries += [mission_dict]

    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_upcoming_missions(request):
    user = request.user
    print(user)
    print(request.COOKIES)
    print(request.__dict__)
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, starts_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_past_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, ends_at__lt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_current_missions(request):
    _now = timezone.now()
    missions = Mission.objects.filter(created_by=request.user.id, starts_at__lt=_now,
                                      ends_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['POST'])
def delete_mission(request):
    body = request.data
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


@protected_resource()
@api_view(['POST'])
def edit_mission_details(request):
    body = request.data
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


@protected_resource()
@api_view(['GET'])
def edit_clearance(request):
    body = request.data
    mission_id = body['mission_id']
    created_by = body['created_by']
    state = body['state']
    message = body['message']
    mission = Mission.objects.get(id = mission_id)
    mission = Mission.objects.get(mission_id=mission_id)
    object = mission.clearance
    object.created_by = created_by
    object.state = state
    object.message = message
    object.save()

    response_data = {'message': 'Successfully edited the clearance.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
def add_drone_to_mission(request):
    body = request.data
    drone = Drone.objects.filter(id=body['drone_id']).first()
    mission = Mission.objects.filter(id=body['mission_id']).first()
    asset = Asset(drone=drone, mission=mission, operator=request.user)
    asset.save()
    response_data = {'message': 'Successfully added drone to mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['GET'])
def remove_drone_from_mission(request):
    body = request.data
    drone = Drone.objects.filter(id=body['drone_id']).first()
    mission = Mission.objects.filter(id=body['mission_id']).first()
    asset = Asset.objects.filter(drone=drone, mission=mission).first()
    asset.delete()
    response_data = {'message': 'Successfully removed drone from mission.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
def get_mission_drones(request):
    body = request.data
    mission_id=body['mission_id']
    drones = Drone.objects.filter(asset__mission=mission_id).all()
    dictionaries = [obj.as_dict() for obj in drones]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')
