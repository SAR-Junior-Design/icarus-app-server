from django.urls import path

from . import GovernmentOfficialViews

urlpatterns = [
    path('is_government_official/', GovernmentOfficialViews.is_government_official, name='is government official'),
]