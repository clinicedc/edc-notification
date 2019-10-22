#!/usr/bin/env python
import django
import environ
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from os.path import abspath, dirname, join


class DisableMigrations:

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


base_dir = dirname(abspath(__file__))
app_name = 'edc_notification'
# to enable a test that actually sends notifications
# $ export ENVFILE=.env
# $ echo $ENVFILE
# .env
env = environ.Env(
    DJANGO_EDC_BOOTSTRAP=(int, 3),
    DJANGO_EMAIL_ENABLED=(bool, False),
    TWILIO_ENABLED=(bool, False),
)
try:
    envfile = os.environ["ENVFILE"] or "env.sample"
except KeyError:
    envfile = "env.sample"
env.read_env(os.path.join(base_dir, envfile))

installed_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'edc_auth.apps.AppConfig',
    'edc_sites.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    'edc_notification.apps.AppConfig',
]

DEFAULT_SETTINGS = dict(
    BASE_DIR=base_dir,
    SITE_ID=10,
    ALLOWED_HOSTS=['localhost'],
    # AUTH_USER_MODEL='custom_user.CustomUser',
    ROOT_URLCONF=f'{app_name}.urls',
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        # required for tests when acting as a server that deserializes
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': join(base_dir, 'db.sqlite3'),
        },
    },
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'edc_dashboard.middleware.DashboardMiddleware',
        # 'edc_dashboard.middleware.DashboardMiddleware',
    ],

    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,

    APP_NAME=app_name,
    EDC_BOOTSTRAP=3,

    EMAIL_ENABLED=env("DJANGO_EMAIL_ENABLED"),
    EMAIL_CONTACTS={"data_manager": "data_manager@clinicedc.org"},
    # if ENVFILE != '.env':
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    TWILIO_ENABLED=env("TWILIO_ENABLED"),
    TWILIO_ACCOUNT_SID=env.str("TWILIO_ACCOUNT_SID"),
    TWILIO_AUTH_TOKEN=env.str("TWILIO_AUTH_TOKEN"),
    TWILIO_SENDER=env.str("TWILIO_SENDER"),
    TWILIO_TEST_RECIPIENT=env.str("TWILIO_TEST_RECIPIENT"),
    LIVE_SYSTEM=False,
    ENVFILE=envfile,

    STATIC_ROOT=join(base_dir, 'edc_notification', 'static'),

    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    MIGRATION_MODULES=DisableMigrations(),
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher', ),
)

if DEFAULT_SETTINGS.get('EMAIL_ENABLED'):
    DEFAULT_SETTINGS.update(
        EMAIL_HOST=env.str("DJANGO_EMAIL_HOST"),
        EMAIL_PORT=env.int("DJANGO_EMAIL_PORT"),
        EMAIL_HOST_USER=env.str("DJANGO_EMAIL_HOST_USER"),
        EMAIL_HOST_PASSWORD=env.str("DJANGO_EMAIL_HOST_PASSWORD"),
        EMAIL_USE_TLS=env("DJANGO_EMAIL_USE_TLS"),
        MAILGUN_API_KEY=env("MAILGUN_API_KEY"),
        MAILGUN_API_URL=env("MAILGUN_API_URL"),
    )

if os.environ.get("TRAVIS"):
    DEFAULT_SETTINGS.update(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'edc',
                'USER': 'travis',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
            },
        })


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
