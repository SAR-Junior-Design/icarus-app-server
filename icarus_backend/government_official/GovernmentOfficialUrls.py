from django.urls import path

from . import GovernmentOfficialViews

urlpatterns = [
    path('is_government_official/', GovernmentOfficialViews.is_government_official, name='is government official'),
    path('get_missions/', GovernmentOfficialViews.get_missions, name='jurisdiction get missions'),
    path('get_past_missions/', GovernmentOfficialViews.get_past_missions, name='jurisdiction get past missions'),
    path('get_upcoming_missions/', GovernmentOfficialViews.get_upcoming_missions, name='jurisdiction get upcoming missions'),
    path('get_current_missions/', GovernmentOfficialViews.get_current_missions, name='jurisdiction get current missions'),
    path('upgrade_to/', GovernmentOfficialViews.upgrade_to_government_official, name='upgrade to official'),
]