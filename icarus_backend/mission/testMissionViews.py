from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.gis.geos import Polygon
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from icarus_backend.mission.MissionModel import Mission

import json

area = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates":
            [
              [
                -78.046875,
                13.581920900545844
              ],
              [
                -73.47656249999999,
                -3.162455530237848
              ],
              [
                -60.8203125,
                14.26438308756265
              ],
              [
                -78.046875,
                13.581920900545844
              ]
            ]
        },
        "properties": {}
      }
    ]
  }

register_info = {
  "title": "Venezuela",
  "area": area,
  "description": "testing minimap",
  "starts_at": "2018-10-12T11:45:00+05:00",
  "ends_at": "2018-11-12T11:45:00+05:00",
  "type": "commercial"
}

register_info_2 = {
  "title": "Columbia",
  "area": area,
  "description": "Reconnaissance",
  "starts_at": "2018-10-12T11:45:00+05:00",
  "ends_at": "2018-11-12T11:45:00+05:00",
  "type": "commercial"
}

login_info = {
    'username': 'user1',
    'password': '12345'
}


class MissionViewTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='user1',
                                 email='e@mail.com',
                                 password='12345')
        area_polygon = Polygon(area['features'][0]['geometry']['coordinates'])
        starts_at = parse_datetime(register_info['starts_at'])
        ends_at = parse_datetime(register_info['ends_at'])
        Mission.objects.create(mission_id=1, title=register_info['title'], area=area_polygon,
                               description=register_info['description'], starts_at=starts_at,
                               ends_at=ends_at, type=register_info['type'])

    def test_register_mission(self):
        response = self.client.post(reverse('register mission'), json.dumps(register_info_2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register mission'), json.dumps(register_info_2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Mission.objects.get(title=register_info_2['title']))

    def test_get_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # response = self.client.get(reverse('get missions'))

    def test_delete_missions(self):
        return 'TODO'
