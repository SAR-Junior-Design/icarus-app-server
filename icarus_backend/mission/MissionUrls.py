
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('get_missions/', MissionViews.getMissions, name='get missions'),
    path('register_mission/', MissionViews.registerMissions, name='register missions')
]