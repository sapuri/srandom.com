from http import HTTPStatus

from django.test import RequestFactory, SimpleTestCase, TestCase
from django.views.defaults import server_error


class RobotsTxtTests(TestCase):
    def test_get(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(resp['content-type'], 'text/plain')

    def test_post_disallowed(self):
        resp = self.client.post("/robots.txt")
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, resp.status_code)


class ErrorPageTests(SimpleTestCase):
    def test_server_error_offers_home_link_without_csrf_less_login(self):
        response = server_error(RequestFactory().get('/'))
        self.assertContains(response, 'トップへ戻る', status_code=500)
        self.assertNotContains(response, '<form', status_code=500)
