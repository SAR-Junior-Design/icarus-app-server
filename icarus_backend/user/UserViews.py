from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot
from users.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from icarus_backend.user.tasks import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from schema import Schema, SchemaError

from .userViewSchemas import register_user_schema


@api_view(['POST'])
def icarus_login(request):
    body = request.data
    username = body['username']
    password = body['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            request.session.set_expiry(86400) #sets the exp. value of the session
            login(request, user) #the user is now logged in
            response_data = {'message': 'Login successful.'}
            responseJson = json.dumps(response_data)
            return HttpResponse(responseJson, content_type="application/json", status=200)
        else:
            response_data = {'message': 'Bad user credentials.'}
            responseJson = json.dumps(response_data)
            return HttpResponse(responseJson, content_type="application/json", status=401)
    else:
        response_data = {'message': 'Bad user credentials.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=401)


@api_view(['POST'])
def icarus_register_user(request):
    body = request.data
    try:
        schema = Schema([register_user_schema])
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


@api_view(['GET'])
def icarus_logout(request):
    if request.user.is_active:
        logout(request)
        response_data = {'message': 'Logout successful.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=401)


@api_view(['GET'])
def icarus_get_user(request):
    if request.user.is_active:
        response_dict = dict()
        response_dict['user'] = request.user.as_dict()
        if request.user.role == 'pilot':
            response_dict['pilot'] = Pilot.objects.filter(user=request.user).first().as_dict()
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)


@api_view(['GET'])
def icarus_is_logged_in(request):
    if request.user.is_active:
        responseJson = json.dumps(True)
        return HttpResponse(responseJson, content_type="application/json", status=200)
    else:
        responseJson = json.dumps(False)
        return HttpResponse(responseJson, content_type="application/json", status=200)


@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=int(uid))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user.username, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')