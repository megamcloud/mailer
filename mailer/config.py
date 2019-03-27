import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from . import __about__


# ------------------------------------------------------------------------------


def _get_sensitive_config(config_name, default_value=None):
    config_name_file = config_name + "_FILE"
    config_file = os.environ.get(config_name_file, None)
    config = os.environ.get(config_name, default_value)

    if config_file is not None:
        return open(config_file, "r").read().strip()

    return config


# ------------------------------------------------------------------------------


class Config:
    TO_EMAIL = os.environ.get("TO_EMAIL")
    TO_NAME = os.environ.get("TO_NAME")

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").replace(" ", "").split(",")

    RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED", "false") == "true"
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "10 per hour")
    RATELIMIT_APPLICATION = os.environ.get("RATELIMIT_APPLICATION", "100 per day")
    RATELIMIT_STORAGE_URL = os.environ.get("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_STRATEGY = os.environ.get("RATELIMIT_STRATEGY", "moving-window")
    RATELIMIT_HEADERS_ENABLED = True

    RECAPTCHA_ENABLED = os.environ.get("RECAPTCHA_ENABLED", "false") == "true"
    RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
    RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

    MAILER_SERVICE = os.environ.get("MAILER_SERVICE")

    SENDGRID_API_KEY = _get_sensitive_config("SENDGRID_API_KEY")
    SENDGRID_SANDBOX = os.environ.get("SENDGRID_SANDBOX", "false") == "true"

    APISPEC_SPEC = APISpec(
        title=__about__.__title__,
        version=__about__.__version__,
        openapi_version="2.0",
        plugins=[MarshmallowPlugin()],
    )
    APISPEC_SWAGGER_URL = "/docs-json/"
    APISPEC_SWAGGER_UI_URL = "/docs/"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    SERVER_NAME = os.environ.get("SERVER_NAME")
    PREFERRED_URL_SCHEME = os.environ.get("PREFERRED_URL_SCHEME", "https")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    SERVER_NAME = None
    PREFERRED_URL_SCHEME = None

    RATELIMIT_ENABLED = False

    SENDGRID_SANDBOX = True


# ------------------------------------------------------------------------------


def get_app_config(config_name):
    configs = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "default": ProductionConfig,
    }

    return configs.get(config_name, configs["default"])
