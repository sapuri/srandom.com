from django.test import TestCase, RequestFactory

from users.models import *
from users.views import *

class UrlTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        theme = Theme.objects.create(theme='test')
        self.user = CustomUser.objects.create_user(username='admin', email='test@example.com', password='top_secret', theme=theme, premium=True)

    def test_settings(self):
        request = self.factory.get('/users/settings/')
        request.user = self.user
        response = settings(request)
        self.assertEqual(response.status_code, 200)

    def test_deactivate(self):
        request = self.factory.get('/users/deactivate/')
        request.user = self.user
        response = deactivate(request)
        self.assertEqual(response.status_code, 200)

    def test_download(self):
        request = self.factory.get('/users/download/csv/')
        request.user = self.user
        response = download(request, 'csv')
        self.assertEqual(response.status_code, 200)
