from django.http import HttpResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from .DroneModel import Drone
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon


@csrf_exempt
def get_user_drones(request):
    if request.method == 'GET':

        user_object = request.user


        json_array = []
        for drone in user_drones:
            dron_json = {}
            dron_json["owner"] = drone.owner.username
            dron_json["drone_id"] = drone.drone_id
            dron_json["description"] = drone.description
            dron_json[""]

            # owner = models.ForeignKey(User, on_delete=models.CASCADE)
            # drone_id = models.TextField()
            # description = models.TextField()
            # manufacturer = models.TextField()
            # drone_type = models.CharField()
            # color = models.CharField()
            # created_at = models.DateTimeField()




    pass

@csrf_exempt
def delete_drone(request):
    pass

@csrf_exempt
def get_drones_past_missions(request):
    pass

@csrf_exempt
def register_drone():
   pass
