from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from users.models import IcarusUser as User
from icarus_backend.user.tasks import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from icarus_backend.utils import validate_body
from oauth2_provider.decorators import protected_resource

from .pilotViewSchemas import register_pilot_schema, update_pilot_info_schema
from .PilotModel import Pilot


@api_view(['POST'])
@validate_body(register_pilot_schema)
def icarus_register_pilot(request):
    body = request.data
    username = body['username']
    password = body['password']
    email = body['email']
    user = authenticate(username=username, password=password)
    if user is None:
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        role='pilot')
        register_pilot(body,user)
        user.is_active = False
        domain = get_current_site(request).domain
        send_verification_email.delay(user.username, user.email, user.id, domain)
        user.save()
        response_data = {'message': 'User successfully registered.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'User already exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=403)


def register_pilot(body, user):
    faa_registration_number = body['faa_registration_number']
    remote_pilot_certificate_number = body['remote_pilot_certificate_number']
    mobile_phone_number = body['mobile_phone_number']
    pilot = Pilot(user=user, FAARegistrationNumber=faa_registration_number,
                  remotePilotCertificateNumber=remote_pilot_certificate_number,
                  mobilePhoneNumber=mobile_phone_number)
    pilot.save()
    return True


@protected_resource()
@api_view(['GET'])
def get_pilot_data(request):
    id = request.query_params.get('id')
    pilot = Pilot.objects.filter(user=id).first()
    if not pilot:
        response_data = {'message': 'No pilot with this id exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=400)
    response_json = json.dumps(pilot.as_dict())
    return HttpResponse(response_json, content_type="application/json", status=200)


@protected_resource()
@api_view(['POST'])
@validate_body(update_pilot_info_schema)
def update_pilot_info(request):
    if request.user.is_active:
        parsed_json = request.data
        pilot = Pilot.objects.filter(user_id=request.user.id).first()
        if 'faa_registration_number' in parsed_json and pilot.FAARegistrationNumber \
                != parsed_json['faa_registration_number']:
            pilot.FAARegistrationNumber = parsed_json['faa_registration_number']
        if 'remote_pilot_certificate_number' in parsed_json and pilot.remotePilotCertificateNumber \
                != parsed_json['remote_pilot_certificate_number']:
            pilot.remotePilotCertificateNumber = parsed_json['remote_pilot_certificate_number']
        if 'mobile_phone_number' in parsed_json and pilot.mobilePhoneNumber != parsed_json['mobile_phone_number']:
            pilot.mobilePhoneNumber = parsed_json['mobile_phone_number']
        pilot.save()
        response_json = json.dumps({'message': 'Info updated successfully.'})
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)