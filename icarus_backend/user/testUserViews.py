from django.test import TestCase
from django.urls import reverse
import json

from users.models import IcarusUser as User
from django.contrib.auth import authenticate

login_info = {
        'username': 'user1',
        'password': '12345'
    }

register_info = {
        'username': 'user2',
        'password': '12345',
        'email': "e2@mail.com"
    }

user_info = {
    "username": "user1",
    "email": "e@mail.com",
    "first_name": "",
    "last_name": ""
}


class UserViewTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='user1',
                                        email='e@mail.com',
                                        password='12345')

    def test_login(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('icarus logout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_register(self):
        response = self.client.post(reverse('icarus register user'), json.dumps(register_info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = authenticate(username=register_info['username'], password=register_info['password'])
        self.assertTrue(user)

    def test_get_user(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get user'))
        user = json.loads(response.content.decode('utf-8'))
        self.assertEqual(user, user_info)

    def test_is_logged_in(self):
        response = self.client.get(reverse('is logged in'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content.decode('utf-8')))
        response = self.client.post(reverse('icarus login'), json.dumps(login_info), content_type='application/json')
        self.assertTrue(json.loads(response.content.decode('utf-8')))