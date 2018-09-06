"""icarus_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.conf.urls import url

from icarus_backend.cors.CorsModel import CorsModel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clearance/', include('icarus_backend.clearance.ClearanceUrls')),
    path('user/', include('icarus_backend.user.UserUrls')),
    path('mission/', include('icarus_backend.mission.MissionUrls')),
    path('drone/', include('icarus_backend.drone.DroneUrls')),
    path('official/', include('icarus_backend.government_official.GovernmentOfficialUrls')),
    path('pilot/', include('icarus_backend.pilot.PilotUrls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
