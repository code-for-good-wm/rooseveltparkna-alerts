# mypy: ignore-errors

from .production import *

BASE_NAME = os.environ["HEROKU_APP_NAME"]
if BASE_NAME.count("-") >= 2:
    BASE_DOMAIN = f"{BASE_NAME}.herokuapp.com"
else:
    BASE_DOMAIN = BASE_NAME
BASE_URL = f"https://{BASE_DOMAIN}"

ALLOW_DEBUG = True

###############################################################################
# Core

ALLOWED_HOSTS += [".herokuapp.com"]
