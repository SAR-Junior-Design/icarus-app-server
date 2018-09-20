from django.http import HttpResponse
from rest_framework.decorators import api_view
from oauth2_provider.decorators import protected_resource
import json
from icarus_backend.mission.MissionModel import Mission
from django.utils import timezone
from users.models import IcarusUser as User
from icarus_backend.government_official.GovernmentOfficialModel import GovernmentOfficial
from django.contrib.gis.geos import Polygon
from icarus_backend.government_official.GovernmentOfficialSchemas import upgrade_to_government_official
from icarus_backend.utils import validate_body

from icarus_backend.government_official.GovernmentOfficialController import GovernmentOfficialController


@protected_resource()
@api_view(['GET'])
def is_government_official(request):
    response_json = json.dumps(request.user.role == 'government_official')
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
@validate_body(upgrade_to_government_official)
def upgrade_to_government_official(request):
    current_user = User.objects.filter(id=request.user.id).first()
    if not current_user.is_staff:
        response_data = {'message': 'Must be admin to use this endpoint.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
    body = request.data
    user_id = body['user_id']
    coordinates = body['area']['features'][0]['geometry']['coordinates'][0]
    if coordinates[0] is not coordinates[-1]:
        coordinates += [coordinates[0]]
    user = User.objects.filter(id=user_id).first()
    if user.role == 'government_official':
        response_data = {'message': 'Already a government official.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=400, content_type="application/json")
    user.role = 'government_official'
    user.save()
    area = Polygon(coordinates)
    gov_off = GovernmentOfficial(user=user, area=area)
    gov_off.save()
    response_json = {'message': 'User successfully upgraded to government official.'}
    return HttpResponse(json.dumps(response_json), content_type='application/json')


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


@protected_resource()
@api_view(['POST'])
def flight_histogram(request):
    body = request.data
    flight_histogram_data = GovernmentOfficialController.jurisdiction_drone_flight_histogram(
        body['start_day'], body['end_day'], request.user)
    response_json = {'flight_histogram': flight_histogram_data}
    return HttpResponse(json.dumps(response_json), content_type='application/json')
