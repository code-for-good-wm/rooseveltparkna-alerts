import os
from datetime import timedelta

from django.contrib import messages
from django.utils import timezone

import grappelli

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(CONFIG_ROOT)

ALLOW_DEBUG = False

###############################################################################
# Core

INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "allauth",
    "allauth.account",
    "corsheaders",
    "django_extensions",
    "rest_framework",
    "drf_yasg",
    "crispy_forms",
    "crispy_bootstrap5",
    "rpna.api",
    "rpna.core",
    "rpna.alerts",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates", os.path.join(PROJECT_ROOT, "rpna", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "rpna": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/setup"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = ["rpna.core.backends.CustomModelBackend"]

###############################################################################
# Sessions

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 52

###############################################################################
# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "US/Michigan"

USE_I18N = True
LOCALE_PATHS = [os.path.join(PROJECT_ROOT, "locale")]

USE_L10N = True

USE_TZ = True

###############################################################################
# Static files

STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")

###############################################################################
# CORS

CORS_ORIGIN_ALLOW_ALL = True

###############################################################################
# Grappelli

GRAPPELLI_ADMIN_TITLE = "RPNA Alerts Admin"

del grappelli.default_app_config  # fixes RemovedInDjango41Warning

###############################################################################
# Django Debug Toolbar

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED": True,
    "SHOW_TOOLBAR_CALLBACK": "rpna.core.utils.allow_debug",
}

###############################################################################
# Bootstrap

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

###############################################################################
# Twilio

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = "+16162242352"

SMS_TEMPLATE = (
    "Roosevelt Park Neighborhood Association:"
    "\n\n"
    "{message}"
    "\n\n"
    "{details}: {url}"
)
SMS_MAX_LENGTH = 320 - len(
    SMS_TEMPLATE.format(
        message="", details="Detalles", url="https://alerts.rooseveltparkna.org/$$/####"
    )
)

###############################################################################
# WordPress

AUTH_URL = os.getenv("AUTH_URL")
