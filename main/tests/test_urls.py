from django.test import TestCase

class UrlTests(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_difflist(self):
        response = self.client.get('/difflist/')
        self.assertEqual(response.status_code, 200)
