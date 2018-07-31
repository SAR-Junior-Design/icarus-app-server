from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json

@api_view(['POST'])
def icarus_login(request):
    body = json.loads(request.body)
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
            return HttpResponse(responseJson, content_type="application/json", status=400)
    else:
        response_data = {'message': 'Bad user credentials.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=400)


@api_view(['GET'])
def icarus_logout(request):
    if request.user is not None:
        if request.user.is_active:
            logout(request)
            response_data = {'message': 'Logout successful.'}
            responseJson = json.dumps(response_data)
            return HttpResponse(responseJson, content_type="application/json", status=200)
        else:
            response_data = {'message': 'Already logged out.'}
            responseJson = json.dumps(response_data)
            return HttpResponse(responseJson, content_type="application/json", status=400)
    else:
        response_data = {'message': 'Bad user credentials.'}
        responseJson = json.dumps(response_data)
        return HttpResponse(responseJson, content_type="application/json", status=400)
