
from django.urls import path

from . import PilotViews

urlpatterns = [
    path('register/', PilotViews.icarus_register_pilot, name='icarus register pilot'),
]