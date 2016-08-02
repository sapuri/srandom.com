from django.test import TestCase, RequestFactory

from users.models import *
from users.views import *

class UrlTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        theme = Theme.objects.create(theme='something')
        self.user = CustomUser.objects.create_user(username='test', email='test@example.com', password='secret', theme=theme, premium=True)

    def test_mypage(self):
        url = '/users/test/'
        request = self.factory.get(url)
        request.user = self.user
        response = settings(request)
        self.assertEqual(response.status_code, 200)

    def test_settings(self):
        url = '/users/settings/'
        request = self.factory.get(url)
        request.user = self.user
        response = settings(request)
        self.assertEqual(response.status_code, 200)

    def test_cleardata(self):
        for i in range(1, 18):
            url = '/users/cleardata/' + str(i) + '/'
            request = self.factory.get(url)
            request.user = self.user
            response = cleardata(request, self.user, i)
            self.assertEqual(response.status_code, 200)

    def test_deactivate(self):
        url = '/users/deactivate/'
        request = self.factory.get(url)
        request.user = self.user
        response = deactivate(request)
        self.assertEqual(response.status_code, 200)

    def test_download(self):
        url = '/users/download/csv/'
        request = self.factory.get(url)
        request.user = self.user
        response = download(request, 'csv')
        self.assertEqual(response.status_code, 200)
