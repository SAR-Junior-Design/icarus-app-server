
from django.urls import path

from . import MissionViews

urlpatterns = [
    path('register_mission/', MissionViews.register_mission, name='register mission'),
    path('get_missions/', MissionViews.get_missions, name='get missions'),
    path('get_past_missions/', MissionViews.get_past_missions, name='get past missions'),
    path('get_upcoming_missions/', MissionViews.get_upcoming_missions, name='get upcoming missions'),
    path('get_current_missions/', MissionViews.get_current_missions, name='get current missions'),
    path('get_mission_info/', MissionViews.get_mission_info, name='get mission info'),
    path('delete_missions/', MissionViews.delete_mission, name='delete missions'),
    path('edit_clearance/', MissionViews.edit_clearance, name='edit clearance'),
    path('edit/', MissionViews.edit_mission, name='edit mission details'),
    path('add_drone_to_mission/', MissionViews.add_drone_to_mission, name='add drone to mission'),
    path('remove_drone_from_mission/', MissionViews.remove_drone_from_mission, name='remove drone from mission'),
    path('get_mission_drones/', MissionViews.get_mission_drones, name='get mission drones')
]