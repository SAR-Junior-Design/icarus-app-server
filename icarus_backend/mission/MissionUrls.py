
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('register_mission/', MissionViews.registerMissions, name='register missions')
]