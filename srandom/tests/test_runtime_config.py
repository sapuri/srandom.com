import os
import subprocess
import sys
import tempfile
from pathlib import Path

from django.test import SimpleTestCase


class RuntimeConfigTests(SimpleTestCase):
    def load_settings(self, path, assertions, **overrides):
        env = {
            key: value for key, value in os.environ.items()
            if key not in ('APP_ENV_FILE', 'SECRET_KEY', 'DATABASE_NAME')
        }
        env.update({
            'APP_ENV_FILE': str(path),
            'ALLOWED_HOSTS': 'localhost',
            'DATABASE_ENGINE': 'django.db.backends.dummy',
            'DATABASE_USER': 'unused',
            'DATABASE_PASSWORD': 'unused',
            'DATABASE_HOST': 'unused',
            **overrides,
        })
        return subprocess.run(
            [sys.executable, '-c', 'from srandom import settings\n' + assertions],
            env=env, capture_output=True, text=True,
        )

    def test_reads_runtime_secret_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'production.env'
            path.write_text('SECRET_KEY=runtime-test-key\nDATABASE_NAME=runtime-db\n', encoding='utf-8')
            result = self.load_settings(path, '''
assert settings.SECRET_KEY == 'runtime-test-key'
assert settings.DATABASES['default']['NAME'] == 'runtime-db'
''')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_explicit_environment_overrides_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'production.env'
            path.write_text('SECRET_KEY=runtime-test-key\nDATABASE_NAME=runtime-db\n', encoding='utf-8')
            result = self.load_settings(path, '''
assert settings.SECRET_KEY == 'process-test-key'
assert settings.DATABASES['default']['NAME'] == 'process-db'
''', SECRET_KEY='process-test-key', DATABASE_NAME='process-db')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_runtime_secret_fails_instead_of_using_local_dotenv(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.load_settings(
                Path(directory) / 'missing.env', '',
                SECRET_KEY='otherwise-valid-key', DATABASE_NAME='otherwise-valid-db',
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FileNotFoundError', result.stderr)

    def test_empty_runtime_secret_path_is_not_a_fallback(self):
        result = self.load_settings('', '', SECRET_KEY='otherwise-valid-key', DATABASE_NAME='otherwise-valid-db')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FileNotFoundError', result.stderr)
