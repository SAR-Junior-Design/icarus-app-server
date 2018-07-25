
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('get_missions/', MissionViews.get_missions, name='get missions'),
    path('register_mission/', MissionViews.register_mission, name='register missions')
]