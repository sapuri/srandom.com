from http import HTTPStatus

from django.test import TestCase


class RobotsTxtTests(TestCase):
    def test_get(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(resp['content-type'], 'text/plain')

    def test_post_disallowed(self):
        resp = self.client.post("/robots.txt")
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, resp.status_code)
