from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot
from icarus_backend.user.tasks import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from schema import Schema, SchemaError

from .pilotViewSchemas import register_pilot_schema


@api_view(['POST'])
def icarus_register_pilot(request):
    body = request.data
    try:
        schema = Schema([register_pilot_schema])
        schema.validate([body])
    except SchemaError as error:
        response_json = json.dumps({"message": str(error)})
        return HttpResponse(response_json, content_type="application/json", status=401)
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