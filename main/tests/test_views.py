from django.shortcuts import resolve_url
from django.test import TestCase

from main import APP_NAME
from main.tests.utils import create_music
from users.tests.utils import create_user


class IndexTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:index'))
        self.assertEqual(200, resp.status_code)

    def test_get_authenticated_user(self):
        self.client.force_login(create_user())
        resp = self.client.get(resolve_url(f'{APP_NAME}:index'))
        self.assertEqual(200, resp.status_code)


class NewsTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:news'))
        self.assertEqual(200, resp.status_code)


class SearchTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:search'))
        self.assertEqual(200, resp.status_code)


class LevelSelectTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:level_select'))
        self.assertEqual(200, resp.status_code)


class LevelTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:level', level=1))
        self.assertEqual(200, resp.status_code)

    def test_get_ng(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:level', level=51))
        self.assertEqual(404, resp.status_code)


class DifflistLevelSelectTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:difflist_level_select'))
        self.assertEqual(200, resp.status_code)


class DifflistTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:difflist', sran_level=1))
        self.assertEqual(200, resp.status_code)

    def test_get_ng(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:difflist', sran_level=20))
        self.assertEqual(404, resp.status_code)


class EditTests(TestCase):
    def setUp(self):
        self.client.force_login(create_user())
        self.music = create_music()

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:edit', music_id=self.music.id))
        self.assertEqual(200, resp.status_code)

    def test_get_ng(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:edit', music_id=0))
        self.assertEqual(404, resp.status_code)


class RankingLevelSelectTests(TestCase):
    def setUp(self):
        self.client.force_login(create_user())

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:ranking_level_select'))
        self.assertEqual(200, resp.status_code)


class RankingTests(TestCase):
    def setUp(self):
        self.client.force_login(create_user())

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:ranking', sran_level=19))
        self.assertEqual(200, resp.status_code)

    def test_get_ng(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:ranking', sran_level=20))
        self.assertEqual(404, resp.status_code)


class RankingDetailTests(TestCase):
    def setUp(self):
        self.client.force_login(create_user())
        self.music = create_music()

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:ranking_detail', music_id=self.music.id))
        self.assertEqual(200, resp.status_code)

    def test_get_ng(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:ranking_detail', music_id=0))
        self.assertEqual(404, resp.status_code)


class OmikujiTests(TestCase):
    def setUp(self):
        self.client.force_login(create_user())

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:omikuji'))
        self.assertEqual(200, resp.status_code)


class PremiumTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:premium'))
        self.assertEqual(200, resp.status_code)
