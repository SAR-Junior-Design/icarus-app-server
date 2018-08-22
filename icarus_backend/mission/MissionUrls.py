
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('register_mission/', MissionViews.register_mission, name='register mission'),
    path('get_missions/', MissionViews.get_missions, name='get missions'),
    path('delete_missions/', MissionViews.delete_mission, name='delete missions'),
    path('edit_clearance/', MissionViews.editClearance, name='edit clearance')
]