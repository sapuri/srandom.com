from unittest.mock import patch

from django.conf import settings
from django.core.files.storage import storages
from django.http import HttpResponseRedirect
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from social_core.backends.google import GoogleOAuth2
from social_core.backends.twitter import TwitterOAuth
from social_core.exceptions import AuthAlreadyAssociated, AuthMissingParameter, AuthStateForbidden
from social_core.pipeline.social_auth import social_user
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy
from storages.backends.gcloud import GoogleCloudStorage

from users.tests.utils import create_user


class StorageCompatibilityTests(SimpleTestCase):
    def test_production_keeps_google_storage_for_media_and_static_files(self):
        if settings.DEBUG:
            self.skipTest('Production storage requires DEBUG=False')
        for alias in ('default', 'staticfiles'):
            self.assertIsInstance(storages[alias], GoogleCloudStorage)
            self.assertEqual(storages[alias].bucket_name, 'static.srandom.com')
            self.assertEqual(storages[alias].custom_endpoint, 'https://static.srandom.com')
            self.assertFalse(storages[alias].querystring_auth)


class SessionCompatibilityTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.user)

    def test_logout_requires_post_and_csrf(self):
        url = reverse('auth:logout')
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertIn('_auth_user_id', self.client.session)
        self.client.get(reverse('main:index'))
        response = self.client.post(url, {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
            'next': reverse('main:index'),
        })
        self.assertRedirects(response, reverse('main:index'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_deactivation_ends_session_and_redirects_home(self):
        url = reverse('users:deactivate')
        self.client.get(url)
        response = self.client.post(url, {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
        })
        self.assertRedirects(response, reverse('main:index'))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertNotIn('_auth_user_id', self.client.session)


class SocialAuthCompatibilityTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.strategy = load_strategy()

    def test_login_initiation_requires_csrf_protected_post(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse('main:index'))
        for provider, backend in (('twitter', TwitterOAuth), ('google-oauth2', GoogleOAuth2)):
            with self.subTest(provider=provider):
                url = reverse('social:begin', args=[provider])
                self.assertEqual(client.get(url).status_code, 405)
                self.assertEqual(client.post(url).status_code, 403)
                with patch.object(backend, 'start', return_value=HttpResponseRedirect('https://provider.example/login')) as start:
                    response = client.post(url, {'csrfmiddlewaretoken': client.cookies['csrftoken'].value})
                self.assertEqual(response.status_code, 302)
                start.assert_called_once()

    def test_existing_twitter_identity_resolves_for_integer_uid(self):
        # 5.4.1 compared the stored string with the integer returned by Twitter.
        uid = 1234567890123456789
        existing = UserSocialAuth.objects.create(
            user=self.user, provider='twitter', uid=str(uid))
        for value in (uid, str(uid)):
            with self.subTest(uid_type=type(value).__name__):
                self.assertEqual(UserSocialAuth.get_social_auth('twitter', value), existing)

    def assert_repeated_oauth_reuses_identity(self, backend, uid, response, token):
        existing = UserSocialAuth.objects.create(
            user=self.user, provider=backend.name, uid=uid)
        counts = (self.user.__class__.objects.count(), UserSocialAuth.objects.count())
        storage = self.strategy.storage.user
        with patch.object(storage, 'create_user', wraps=storage.create_user) as create, \
                patch.object(storage, 'create_social_auth', wraps=storage.create_social_auth) as associate:
            for _ in range(3):
                with patch.object(backend, 'user_data', return_value=dict(response)):
                    user = backend.do_auth(token)
                self.assertEqual(user.pk, self.user.pk)
                existing.refresh_from_db()
                self.assertEqual(existing.user_id, self.user.pk)
                self.assertEqual(existing.uid, uid)
                self.assertEqual(
                    (self.user.__class__.objects.count(), UserSocialAuth.objects.count()), counts)
            create.assert_not_called()
            associate.assert_not_called()

    def test_repeated_twitter_login_does_not_create_user_or_association(self):
        self.assert_repeated_oauth_reuses_identity(
            TwitterOAuth(self.strategy), '1234567890123456789',
            {'id': 1234567890123456789, 'id_str': '1234567890123456789',
             'screen_name': 'renamed_twitter_user', 'name': 'Renamed User'},
            {'oauth_token': 'test-token', 'oauth_token_secret': 'test-secret'},
        )

    def test_repeated_google_login_does_not_create_user_or_association(self):
        self.assert_repeated_oauth_reuses_identity(
            GoogleOAuth2(self.strategy), 'existing@example.com',
            {'sub': 'google-stable-id', 'email': 'existing@example.com',
             'email_verified': True, 'name': 'Renamed Google User'},
            'test-google-token',
        )

    def test_cannot_link_another_users_google_identity(self):
        backend = GoogleOAuth2(self.strategy)
        UserSocialAuth.objects.create(user=self.user, provider=backend.name, uid='existing@example.com')
        other = create_user(username='other', location='other', theme='other')
        with self.assertRaises(AuthAlreadyAssociated):
            social_user(backend, 'existing@example.com', user=other)

    def test_twitter_keeps_token_shape_used_for_posting(self):
        backend = TwitterOAuth(self.strategy)
        token = {'oauth_token': 'test-token', 'oauth_token_secret': 'test-secret'}
        data = backend.extra_data(self.user, '123', {'access_token': token, 'id': 123}, {}, {})
        self.assertEqual(data['access_token'], token)

    def test_google_callback_rejects_missing_or_wrong_state(self):
        backend = GoogleOAuth2(self.strategy)
        with patch.object(backend, 'get_session_state', return_value='expected'):
            for data, error in (({}, AuthMissingParameter), ({'state': 'wrong'}, AuthStateForbidden)):
                with self.subTest(data=data), patch.object(backend, 'data', data):
                    with self.assertRaises(error):
                        backend.validate_state()
            with patch.object(backend, 'data', {'state': 'expected'}):
                self.assertEqual(backend.validate_state(), 'expected')
