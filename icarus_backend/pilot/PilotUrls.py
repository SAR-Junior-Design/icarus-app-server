
from django.urls import path

from . import PilotViews

urlpatterns = [
    path('register/', PilotViews.icarus_register_pilot, name='register pilot'),
    path('get/', PilotViews.get_pilot_data, name='get pilot')
]