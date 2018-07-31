
from django.urls import path

from . import UserViews

urlpatterns = [
    path('login/', UserViews.icarus_login, name='login'),
    path('logout/', UserViews.icarus_logout, name='logout')
]