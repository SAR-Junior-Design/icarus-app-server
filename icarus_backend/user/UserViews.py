from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot
from users.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from icarus_backend.user.tasks import send_verification_email, reset_password_email
from django.contrib.sites.shortcuts import get_current_site
from icarus_backend.utils import validate_body
from oauth2_provider.decorators import protected_resource
from .userViewSchemas import register_user_schema, update_user_info_schema


@api_view(['POST'])
@validate_body(register_user_schema)
def icarus_register_user(request):
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
        user.is_active = False
        user.save()
        domain = get_current_site(request).domain
        send_verification_email.delay(user.username, user.email, user.id, domain)
        response_data = {'message': 'User successfully registered.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'User already exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=403)


@protected_resource()
@api_view(['GET'])
def icarus_get_current_user(request):
    response_dict = dict()
    response_dict['user'] = request.user.as_dict()
    if request.user.role == 'pilot':
        print('it happened!')
        pilot = Pilot.objects.filter(user=request.user).first()
        if pilot:
            response_dict['pilot'] = Pilot.objects.filter(user=request.user).first().as_dict()
    response_json = json.dumps(response_dict)
    return HttpResponse(response_json, content_type="application/json", status=200)


@protected_resource()
@api_view(['GET'])
def icarus_get_user(request):
    id = request.query_params.get('id')
    user = User.objects.filter(id=id).first()
    if not user:
        response_data = {'message': 'No user with this id exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=400)
    response_dict = dict()
    response_dict['user'] = user.as_dict()
    if request.user.role == 'pilot':
        pilot = Pilot.objects.filter(user=request.user).first()
        if pilot:
            response_dict['pilot'] = Pilot.objects.filter(user=request.user).first().as_dict()
    response_json = json.dumps(response_dict)
    return HttpResponse(response_json, content_type="application/json", status=200)


@protected_resource()
@api_view(['POST'])
@validate_body(update_user_info_schema)
def update_user_info(request):
    if request.user.is_active:
        parsed_json = request.data
        user = User.objects.filter(id=request.user.id).first()
        if 'email' in parsed_json and user.email != parsed_json['email']:
            user.email = parsed_json['email']
        if 'password' in parsed_json and user.password != parsed_json['password']:
            user.password = parsed_json['password']
        if 'username' in parsed_json and user.username != parsed_json['username']:
            check_user = User.objects.filter(username=parsed_json['username']).first()
            if check_user:
                response_json = json.dumps({'message': 'Username already taken.'})
                return HttpResponse(response_json, content_type="application/json", status=401)
            user.username = parsed_json['username']
        if 'picture_url' in parsed_json and user.picture_url != parsed_json['picture_url']:
            user.picture_url = parsed_json['picture_url']
        user.save()
        response_json = json.dumps({'message': 'Info updated successfully.'})
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)


@api_view(['GET'])
def icarus_is_logged_in(request):
    if request.user.is_active:
        response_json = json.dumps(True)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_json = json.dumps(False)
        return HttpResponse(response_json, content_type="application/json", status=200)


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


@api_view(['GET'])
def forgot_password(request):
    email = request.query_params.get('email')
    user = User.objects.filter(email=email).first()
    if not user:
        response_data = {'message': 'No user with this email exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)
    domain = get_current_site(request).domain
    reset_password_email.delay(user.username, user.email, user.id, domain)
    response_data = {'message': 'Password reset email is being sent.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@api_view(['GET', 'POST'])
def reset_password(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
            validlink = True
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            validlink = False
        return TemplateResponse(request, 'password_reset_confirm.html', {
            'validlink': validlink,
            'uid': uidb64,
            'token': token
            })
    elif request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
            validlink = True
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            validlink = False
        if user is not None and account_activation_token.check_token(user.username, token):
            body = request.data
            new_password = body['new_password']
            print(new_password)
            user.set_password(new_password)
            user.save()
            # return redirect('home')
            return HttpResponse('Your password has been updated. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


