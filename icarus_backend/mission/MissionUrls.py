
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('register_mission/', MissionViews.register_mission, name='register mission'),
    path('get_missions/', MissionViews.get_missions, name='get missions')
]