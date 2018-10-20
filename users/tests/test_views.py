from django.shortcuts import resolve_url
from django.test import TestCase

from users import APP_NAME
from users.models import *


class ListTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:list'))
        self.assertEqual(200, resp.status_code)


class MypageTests(TestCase):
    def setUp(self):
        self.user = self.create_user()

    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test') -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme)

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:mypage', username=self.user.username))
        self.assertEqual(200, resp.status_code)


class StatisticsTests(TestCase):
    def setUp(self):
        self.user = self.create_user()

    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test') -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme)

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:statistics', username=self.user.username))
        self.assertEqual(200, resp.status_code)


class SettingsTests(TestCase):
    def setUp(self):
        self.client.force_login(self.create_user())

    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test') -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme)

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:settings'))
        self.assertEqual(200, resp.status_code)


class CleardataTests(TestCase):
    def setUp(self):
        self.user = self.create_user()

    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test') -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme)

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:cleardata', username=self.user.username, sran_level=19))
        self.assertEqual(200, resp.status_code)


class DeactivateTests(TestCase):
    def setUp(self):
        self.client.force_login(self.create_user())

    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test') -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme)

    def test_get(self):
        resp = self.client.get(resolve_url(f'{APP_NAME}:deactivate'))
        self.assertEqual(200, resp.status_code)


class DownloadTests(TestCase):
    @staticmethod
    def create_user(username: str = 'test', location: str = 'test', theme: str = 'test',
                    premium: bool = False) -> object:
        location = Location.objects.create(location=location)
        theme = Theme.objects.create(theme=theme)
        return CustomUser.objects.create_user(username, location=location, theme=theme, premium=premium)

    def test_get(self):
        user = self.create_user(premium=True)
        self.client.force_login(user)
        resp = self.client.get(resolve_url(f'{APP_NAME}:download', file_type='csv'))
        self.assertEqual(404, resp.status_code)

    def test_get_ng(self):
        user = self.create_user()
        self.client.force_login(user)
        resp = self.client.get(resolve_url(f'{APP_NAME}:download', file_type='csv'))
        self.assertEqual(403, resp.status_code)
