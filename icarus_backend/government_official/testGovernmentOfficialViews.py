from django.test import TestCase
from django.urls import reverse
from users.models import IcarusUser as User
import json


class GovernmentOfficialViewTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='user1',
                                        email='e@mail.com',
                                        password='12345')
        User.objects.create_user(username='jeffrey',
                                 email='e@mail.com',
                                 password='12345',
                                 role='government_official')

    def test_is_government_official(self):
        login_info = {
            'username': 'user1',
            'password': '12345'
        }
        login_info_gov = {
            'username': 'jeffrey',
            'password': '12345'
        }
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('is government official'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response, False)
        response = self.client.get(reverse('icarus logout'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('icarus login'), json.dumps(login_info_gov),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('is government official'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response, True)