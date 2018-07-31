from django.test import TestCase
from django.urls import reverse
import json

class UserViewTest(TestCase):

    def test_login(self):
        login_info = {
            'username': 'samcrane8',
            'password': 'lawrence8'
        }
        response = self.client.post(reverse('login'), json.dumps(login_info), content_type='application/json')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

