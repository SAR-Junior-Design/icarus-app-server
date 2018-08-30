from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from .UserService import UserService
from users.models import IcarusUser as User


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
    username = body['username']
    password = body['password']
    email = body['email']
    user = authenticate(username=username, password=password)
    if user is None:
        User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        response_data = {'message': 'User successfully registered.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=200)
    else:
        response_data = {'message': 'User already exists.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=403)


@api_view(['GET'])
def icarus_logout(request):
    if request.user.is_active:
        logout(request)
        response_data = {'message': 'Logout successful.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=401)


@api_view(['GET'])
def icarus_get_user(request):
    if request.user.is_active:
        userInfo= UserService.user_info(request.user)
        responseJson = json.dumps(userInfo)
        return HttpResponse(responseJson, content_type="application/json", status=200)
    else:
        response_data = {'message': 'Already logged out.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=401)


@api_view(['GET'])
def icarus_is_logged_in(request):
    if request.user.is_active:
        responseJson = json.dumps(True)
        return HttpResponse(responseJson, content_type="application/json", status=200)
    else:
        responseJson = json.dumps(False)
        return HttpResponse(responseJson, content_type="application/json", status=200)