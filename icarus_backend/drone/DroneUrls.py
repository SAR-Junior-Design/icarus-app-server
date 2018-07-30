from django.urls import path

from . import DroneViews

urlpatterns = [
    path('get_user_drones/', DroneViews.get_user_drones, name='get user drones'),
    path('delete_drone/', DroneViews.delete_drone, name='get user drones'),
    path('get_drones_past_missions/', DroneViews.get_drones_past_missions, name='get user drones'),
    path('register_drone/', DroneViews.register_drone, name='get user drones'),
]
