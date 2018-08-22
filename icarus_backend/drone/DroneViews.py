from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .DroneModel import Drone
from icarus_backend.assets.AssetModel import Asset
import json, uuid


@login_required
def get_user_drones(request):
    drones = Drone.objects.filter(owner=request.user)
    dictionaries = [obj.as_dict() for obj in drones]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def delete_drone(request):
    body = json.loads(request.body)
    drone_id = body['drone_id']
    drones = Drone.objects.filter(id=drone_id).first()
    drones.delete()
    response_data = {'message': 'Drone successfully deleted.'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def get_drones_past_missions(request):
    body = json.loads(request.body)
    drone = Drone.objects.filter(id=body['drone_id']).first()
    assets = Asset.objects.filter(drone=drone)
    dictionaries = [obj.as_dict() for obj in assets]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@login_required
def register_drone(request):
    body = json.loads(request.body)
    drone_id = uuid.uuid4()
    new_drone = Drone(id=drone_id, owner=request.user, description=body['description'],
                      manufacturer=body['manufacturer'], type=body['type'],
                      color=body['color'])
    new_drone.save()
    response_data = {'message': 'Successfully registered this drone.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")
