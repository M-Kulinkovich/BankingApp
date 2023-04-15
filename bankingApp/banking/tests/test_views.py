from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.username = 'test_user'
        self.password = 'test_pass'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.login_data = {
            'username': self.username,
            'password': self.password,
        }

    def test_login_user(self):
        response = self.client.post(self.login_url, data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_register_user(self):
        new_user_data = {
            'username': 'new_user',
            'password1': 'new_pass',
            'password2': 'new_pass',
        }
        response = self.client.post(reverse('register'), data=new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_logout_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
