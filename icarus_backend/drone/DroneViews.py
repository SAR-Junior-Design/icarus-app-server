from django.http import HttpResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon


@csrf_exempt
def get_user_drones(request):
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
