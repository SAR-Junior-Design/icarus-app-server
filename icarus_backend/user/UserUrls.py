
from django.urls import path

from . import UserViews

urlpatterns = [
    path('login/', UserViews.icarus_login, name='icarus login'),
    path('logout/', UserViews.icarus_logout, name='icarus logout'),
    path('get/', UserViews.icarus_get_user, name='get user'),
    path('is_logged_in/', UserViews.icarus_is_logged_in, name='is logged in'),
    path('register_user/', UserViews.icarus_register_user, name='icarus register user')
]